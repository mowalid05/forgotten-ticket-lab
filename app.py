import base64
import json
import os

from flask import Flask, Response, jsonify, make_response, render_template, request

app = Flask(__name__)
app.json.sort_keys = False  # keep field order stable in JSON responses

# ---------------------------------------------------------------------------
# Flags. Set FLAG_SUFFIX to make them unique per instance, for example
# FLAG_SUFFIX=group2 gives CyberX{page_hides_what_api_shows_group2}.
# ---------------------------------------------------------------------------
SUFFIX = os.environ.get("FLAG_SUFFIX", "")


def make_flag(name):
    return "CyberX{" + name + ("_" + SUFFIX if SUFFIX else "") + "}"


FLAG_COMMENTS = make_flag("page_hides_what_api_shows")  # Flag 1
FLAG_ROBOTS = make_flag("robots_say_where_not_to_look")  # Flag 2
FLAG_EXPORT = make_flag("errors_are_instructions")  # Flag 3
FLAG_COOKIE = make_flag("base64_is_not_encryption")  # Flag 4
FLAG_VERBOSE = make_flag("options_lists_the_methods")  # Flag 5

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
REF = "NS-7QK2X"  # the only ticket. It is not a number, so there is nothing to count.

TICKET = {
    "ref": REF,
    "subject": "Cannot access my account",
    "status": "open",
    "description": "The customer cannot access the support portal.",
    "comment_count": 5,  # the page never displays this
}

COMMENTS = [
    {"author": "customer", "text": "I still can't log in after resetting my password."},
    {"author": "agent_07", "text": "Reset email resent. Please check your spam folder."},
    {
        "author": "agent_03",
        "text": "Diagnostics for this ticket are available at /api/tickets/" + REF + "/export.",
    },
    {
        "author": "agent_03",
        "text": "Support staff: the export endpoint has an extra mode. "
        "Check which methods it accepts.",
    },
    {
        "author": "agent_07",
        "text": "Internal note, delete before closing: QA token is " + FLAG_COMMENTS,
    },
]

SUPPORTED_FORMATS = ["json", "csv"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
@app.after_request
def no_cache(response):
    # Always show fresh responses in Burp.
    response.headers["Cache-Control"] = "no-store"
    return response


def error(message, status, **extra):
    body = {"error": message}
    body.update(extra)
    return jsonify(body), status


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
@app.get("/")
def index():
    # Flag 4: the portal remembers preferences in a cookie. The value is
    # base64-encoded JSON, which is encoding, not encryption.
    prefs = {"theme": "light", "lang": "en", "support_note": FLAG_COOKIE}
    encoded = base64.b64encode(json.dumps(prefs).encode()).decode()
    response = make_response(render_template("index.html"))
    response.set_cookie("portal_prefs", encoded)
    return response


# ---------------------------------------------------------------------------
# Ticket API
# ---------------------------------------------------------------------------
@app.get("/api/tickets/<ref>")
def get_ticket(ref):
    if ref != REF:
        return error("Ticket not found", 404)
    return jsonify(TICKET)


@app.get("/api/tickets/<ref>/comments")
def get_comments(ref):
    if ref != REF:
        return error("Ticket not found", 404)
    return jsonify({"ticket": REF, "comments": COMMENTS})


@app.get("/api/tickets/<ref>/attachments")
def get_attachments(ref):
    # Decoy: the page's JavaScript mentions it, but the feature is not enabled.
    return error("Attachments are not enabled", 404)


# Flags 3 and 5: the export endpoint.
# POST is the normal method. OPTIONS reveals a second, unusual method: VERBOSE.
@app.route("/api/tickets/<ref>/export", methods=["GET", "POST", "OPTIONS", "VERBOSE"])
def export_ticket(ref):
    if ref != REF:
        return error("Ticket not found", 404)

    # OPTIONS: "which methods can I use here?"
    if request.method == "OPTIONS":
        response = make_response("", 204)
        response.headers["Allow"] = "POST, OPTIONS, VERBOSE"
        return response

    # Step 1: wrong method.
    if request.method == "GET":
        response, status = error("Method not allowed", 405)
        response.headers["Allow"] = "POST"
        return response, status

    # Step 2: wrong content type. POST and VERBOSE share these checks.
    if request.mimetype != "application/json":
        return error(
            "Unsupported media type", 415, expected="Content-Type: application/json"
        )

    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error("Invalid JSON", 400, expected="A JSON object")

    # Step 3: missing field.
    if "format" not in body:
        return error("Missing field", 400, required=["format"])

    # Step 4: unsupported value.
    if body["format"] not in SUPPORTED_FORMATS:
        return error("Unsupported format", 400, supported=SUPPORTED_FORMATS)

    # Success. VERBOSE returns the extra "verbose" diagnostics (Flag 5).
    verbose = request.method == "VERBOSE"
    diagnostics = FLAG_VERBOSE if verbose else FLAG_EXPORT

    if body["format"] == "csv":
        csv_body = "ticket,diagnostics\n{},{}\n".format(REF, diagnostics)
        return csv_body, 200, {"Content-Type": "text/csv"}

    return jsonify(
        {
            "status": "exported",
            "mode": "verbose" if verbose else "standard",
            "format": "json",
            "data": {"ticket": REF, "diagnostics": diagnostics},
        }
    )


# ---------------------------------------------------------------------------
# Flag 2: the old portal, found through robots.txt
# ---------------------------------------------------------------------------
@app.get("/robots.txt")
def robots():
    text = "User-agent: *\nDisallow: /old-portal/\nDisallow: /staging/\n"
    return Response(text, mimetype="text/plain")


@app.get("/old-portal/")
def old_portal():
    html = (
        "<!doctype html><title>Northstar (old portal)</title>"
        "<h1>Northstar Support Portal (old)</h1>"
        "<p>This portal has been replaced by the new one.</p>"
        '<p><a href="/old-portal/changelog.txt">Changelog</a></p>'
    )
    return Response(html, mimetype="text/html")


@app.get("/old-portal/changelog.txt")
def changelog():
    text = (
        "Northstar Support Portal - changelog\n"
        "\n"
        "v2.4  Ticket pages moved to the new portal.\n"
        "v2.3  Debug page moved to /old-portal/debug. It needs the ticket reference.\n"
        "v2.2  Attachments removed until the feature is ready.\n"
    )
    return Response(text, mimetype="text/plain")


@app.get("/old-portal/debug")
def old_portal_debug():
    ref = request.args.get("ref")
    if ref is None:
        return error("Missing parameter", 400, required=["ref"])
    if ref != REF:
        return error("Unknown ticket reference", 404)
    return jsonify({"ref": REF, "debug": {"cache": "off", "note": FLAG_ROBOTS}})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
