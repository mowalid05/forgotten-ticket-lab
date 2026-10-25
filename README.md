# The Forgotten Ticket: lab files

A small Flask app for the CyberX web CTF methodology session. Five flags. The source contains every solution, so treat it as instructor material.
Do not expose it to the public internet.

## Run

```bash
docker compose up --build
```

Open <http://127.0.0.1:5000>. Stop with `docker compose down`.


## Contents

```
compose.yaml, Dockerfile, requirements.txt   Docker setup
app.py, templates/, static/                  The lab application
instructor/INSTRUCTOR.md                     Solutions, hints, rubric, smoke test (instructor only)
student/STUDENT_HANDOUT.md                   Task sheet for students (no solution)
student/obsidian-template.md                 Report template for Obsidian
```



## Sharing with students

- Host one instance on a server reachable only by students (a tunnel, VPN or allow-list).
- If students run it locally they receive the source, which contains the solutions. Share a pre-built image instead, or rely on the graded explanation.
- Give students only `student/STUDENT_HANDOUT.md` and `student/obsidian-template.md`.
