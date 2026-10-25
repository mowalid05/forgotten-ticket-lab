// Northstar Support Portal - front-end script

const TICKET_REF = "NS-7QK2X";
const API = "/api/tickets/" + TICKET_REF;

// Parts of the portal that are still under development.
const SHOW_COMMENTS = false;     // TODO: turn on when the design is approved
const SHOW_ATTACHMENTS = false;

const ticketBox = document.getElementById("ticket");

// Ask the API for data and return it as JSON.
async function getJSON(path) {
  const response = await fetch(API + path, {
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    throw new Error("Request failed with status " + response.status);
  }
  return response.json();
}

// Show the main ticket.
function showTicket(ticket) {
  ticketBox.innerHTML = `
    <p class="muted">Ticket #${ticket.ref}</p>
    <h1></h1>
    <span class="badge"></span>
    <p class="description"></p>
  `;
  // textContent is safer than putting server data straight into HTML.
  ticketBox.querySelector("h1").textContent = ticket.subject;
  ticketBox.querySelector(".badge").textContent = ticket.status;
  ticketBox.querySelector(".description").textContent = ticket.description;
}

// Add an extra card (comments, attachments) under the ticket.
function addCard(title, lines) {
  const card = document.createElement("section");
  card.className = "card extra";
  card.innerHTML = "<h2></h2>";
  card.querySelector("h2").textContent = title;

  for (const text of lines) {
    const p = document.createElement("p");
    p.textContent = text;
    card.append(p);
  }
  document.querySelector("main").append(card);
}

async function showComments() {
  const data = await getJSON("/comments");
  addCard("Comments", data.comments.map((c) => c.author + ": " + c.text));
}

async function showAttachments() {
  const data = await getJSON("/attachments");
  addCard("Attachments", data.files || []);
}

// Start here: load the ticket, then the optional parts.
async function main() {
  try {
    showTicket(await getJSON(""));
    if (SHOW_COMMENTS) await showComments();
    if (SHOW_ATTACHMENTS) await showAttachments();
  } catch (error) {
    ticketBox.textContent = "Could not load the ticket. " + error.message;
  }
}

main();
