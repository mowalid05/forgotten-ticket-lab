# The Forgotten Ticket: lab files

A small Flask app for the CyberX web CTF methodology session. **Five flags** are hidden in it.
Do not expose it to the public internet.

## Scenario

Northstar uses a small support portal to display customer tickets. The portal has undocumented behavior and it has been leaking things. Your mission is to understand how the page gets its data and find all five flags, then write a report that shows how you found each one.

Every flag looks like `CyberX{...}`. Work on your own.

## Run

```bash
docker compose up --build
```

Open <http://127.0.0.1:5000>. Stop with `docker compose down`.

## Rules

- Test only this training application.
- Do not brute-force endpoints, parameters or values.
- Do not flood the application with requests.
- Work from evidence you can see. Every flag can be reached from something you have already seen or been taught in the session.
- Record your findings as you go, including dead ends.
- You must explain how you found each flag, not just submit it.

## Your tasks

1. **Understand the feature.** What does the page show? Write one question you could answer by looking at the HTTP traffic.
2. **Find the relevant request.** In Burp, open `Proxy`, then `HTTP history`. Find the request that loads the ticket. Record its method, path, status and content type.
3. **Establish a baseline.** Send that request to Repeater and send it unchanged. Record the status, headers and body. What does the page show, and what does the response contain?
4. **Hunt for the flags.** There are five. They are not found the same way and they are not in order. For each one: form a hypothesis, change one thing, send, compare, and record. If a test leads nowhere, record that too.
5. **Write your report.** One report with a section for every flag, using the template in `student/obsidian-template_nothenStar_CTF.md`.

## Your report

For each flag you find, write:

| Item | What to include |
|---|---|
| Flag | The exact `CyberX{...}` value |
| Clue | What response, header, file or error made you try it |
| Hypothesis | What you expected to happen |
| Requests | The original request and the modified request (paste them in code blocks) |
| Difference | What changed in the response |
| Explanation | Why it worked, in your own words |

Also include:

- The relevant request and your baseline (tasks 2 and 3)
- A **dead ends** table: what you tried that led nowhere, and what you learned
- A short reflection: what should the team that built this portal change?

A flag without an explanation earns partial credit.

## Scoring (20 points)

| Criterion | Points |
|---|---:|
| Relevant request and baseline | 2 |
| Each flag (5 flags): 1 for the flag, 2 for the evidence and explanation | 15 |
| Investigation trail, including dead ends | 3 |

Ask for a hint privately if you are stuck, after trying on your own. Using a hint carries no penalty.

## Contents
```
compose.yaml, Dockerfile, requirements.txt Docker setup
app.py, templates/, static/ The lab application
student/obsidian-template_nothenStar_CTF.md Report template for Obsidian
```

## For instructors

- Host one instance on a server reachable only by students (a tunnel, VPN or allow-list).
- If students run it locally they receive the source. Share a pre-built image instead, or rely on the graded explanation.
- Give students this README and the Obsidian template.
