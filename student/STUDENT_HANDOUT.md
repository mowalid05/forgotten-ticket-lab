# The Forgotten Ticket

## Scenario

Northstar uses a small support portal to display customer tickets. The portal has undocumented behavior and it has been leaking things. Your mission is to understand how the page gets its data and find **five flags**.

Every flag looks like `CyberX{...}`. Work on your own, in your own note.

## Rules

- Test only the provided training application.
- Do not brute-force endpoints, parameters or values.
- Do not flood the application with requests.
- Work from the evidence you can see. Every flag can be reached from something you have already seen or been taught.
- Record your findings as you go, including dead ends.
- You must explain how you found each flag, not just submit it.

## Tasks

1. **Understand the feature.** What does the page show? Write one question you could answer by looking at the HTTP traffic.
2. **Find the relevant request.** In Burp, open `Proxy` then `HTTP history`. Find the request that loads the ticket. Record its method, path, status and content type.
3. **Establish a baseline.** Send it to Repeater and send it unchanged. Record the status, headers and body. What does the page show, and what does the response contain?
4. **Hunt for the flags.** There are five. They are not all found the same way, and they are not in order. For each one: form a hypothesis, change one thing, send, compare, and record. If a test leads nowhere, record that too.
5. **Write it up.** For each flag, record the flag, the requests behind it, and why it worked.

## Hints

Ask for a hint privately when you are stuck, after trying on your own. Using a hint carries no penalty.

## Scoring (20 points)

| Criterion | Points |
|---|---:|
| Relevant request and baseline | 2 |
| Each flag (5 flags): 1 for the flag, 2 for the evidence and explanation | 15 |
| Investigation trail, including dead ends | 3 |

A flag without an explanation earns partial credit.
