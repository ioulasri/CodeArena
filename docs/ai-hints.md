# AI Hint Assistant (MVP Integration Notes)

This document ties the AI hint assistant to the existing CodeArena MVP. It is friendly enough to share, but specific to the current repo structure.

## 0) Current project context (from this repo)

- **Backend**: FastAPI in `backend/app`
- **Frontend**: React in `frontend`
- **Database**: PostgreSQL via Docker Compose (`docker-compose.yml`)
- **Live match updates**: WebSocket endpoint in `backend/app/api/v1/endpoints/websocket.py`
- **Match + puzzle data**: `backend/app/models/puzzle.py` (Match, Puzzle, PlayerAnswer)
- **Auth**: JWT helpers in `backend/app/api/v1/endpoints/auth.py`

This design keeps changes small and consistent with the current setup.

## 1) What if a player asks something other than a hint?

**Goal:** stay helpful, but only within the current puzzle.

Recommended behavior:
- **Off-topic request** ("tell me a joke", "explain databases")
  - Reply with a polite refusal and redirect to the puzzle.
  - Example: "I can only help with hints about the current puzzle. What part is confusing you?"

- **Full solution request** ("give me the algorithm", "write the code")
  - Refuse and offer a smaller, safe hint.
  - Example: "I can't provide the full solution, but here is a small hint: focus on how you track state between moves."

- **Normal hint request**
  - Provide 1 to 3 short hints, no code blocks, no step-by-step solution.

How to enforce this (simple + maintainable):
- Always include a **strict no-solutions policy** in the prompt.
- Add a **small output check**: block code blocks or long step-by-step replies.
- Optional **light intent check** on the user message (keywords like "full solution", "final answer", "write the code").

## 2) What does "local model" mean?

A **local model** is a pre-trained open-source LLM running on your machine. You **do not** build or train it from scratch.

You only need:
- A local inference server (or binary) that exposes an HTTP API.
- A small HTTP client call from FastAPI (use `httpx`, already in `backend/requirements.txt`).

Practical options for local dev:
- Run the model **directly on your host** and call it from the backend.
- Or add a **new service** in `docker-compose.yml` so the backend can call it on the same Docker network.

## 3) Where the hint feature fits in the existing backend

### Recommended API shape (simple REST)
Add a new endpoint:

- `POST /api/v1/matches/{match_id}/hint`

Why REST?
- Fast to build and test.
- Fits existing match endpoints in `backend/app/api/v1/endpoints/matches.py`.

Minimal request payload (example):
```json
{
  "message": "I am stuck on the input parsing",
  "code": "// current editor content (optional)",
  "hint_level": 1
}
```

Minimal response:
```json
{
  "hint": "Focus on separating parsing from logic before optimizing.",
  "remaining_hints": 2
}
```

### Optional WebSocket variant
If you want the hint to stream inside the match WebSocket, add a new message type inside:
`backend/app/api/v1/endpoints/websocket.py`

- Incoming: `ai_hint_request`
- Outgoing: `ai_hint_response`

This is slightly more work, but looks more "live" in the UI.

## 4) What data we already have (and what we should NOT send)

- The backend already has **puzzle text** (title, description, story) in `Puzzle`.
- It also has `PlayerPuzzleInput.expected_answer` for each match.
- **Never include `expected_answer` in the prompt**. It is the ground truth and can leak the solution.

For code context:
- If the duel has a code editor, **send the current editor content** in the hint request payload.
- If there is no code editor, you can pass the user's last attempt or a short text description.

## 5) Database logging (minimal and consistent)

Add a new table to store hint requests and responses:

Table: `ai_hint_messages`
- `id` (SERIAL)
- `match_id` (UUID, FK to matches)
- `user_id` (INT, FK to users)
- `hint_level` (SMALLINT)
- `user_message` (TEXT)
- `prompt` (TEXT)
- `response` (TEXT)
- `created_at` (TIMESTAMP)

Why log?
- It enforces hint limits.
- It makes debugging easy during evaluation.

**Migration note:**
- The repo uses SQL files in `backend/migrations/` and the Makefile runs them.
- Add a new SQL migration and update `make db-migrate` if needed.

## 6) Guardrails (must-haves for fair play)

1) Strict prompt policy (no solutions, no code).
2) Hard output limit (short hints only).
3) Block code blocks in output (e.g., remove text between ``` markers).
4) If the user asks for a solution, refuse + redirect.

## 7) Suggested prompt template (short and safe)

```
You are a helpful, minimal-hint tutor.
Do NOT provide full solutions, code, or step-by-step algorithms.
Give 1 to 3 short hints only.
If the request asks for a full solution, refuse and redirect.

Puzzle: {title}
Description: {description}
Story: {story}
User request: {message}
User code (optional): {code}

Return a short hint only.
```

## 8) Hint limits (keeps the duel engaging)

Recommended default:
- **3 hints per player per match**, with a **30 to 60 second cooldown**.

Rationale:
- It supports learning but keeps the competitive spirit.

## 9) Minimal implementation checklist (aligned to this repo)

Backend
- Add a new endpoint in `backend/app/api/v1/endpoints/matches.py` or a new `hints.py`.
- Use `get_current_user_dependency` to authenticate.
- Verify the user is part of the match and the match is active.
- Build the prompt from puzzle text + user message + optional code.
- Call the local model via `httpx`.
- Log the prompt and response to `ai_hint_messages`.

Database
- Add `ai_hint_messages` table in a new migration SQL file.
- Update `Makefile` migration list if you use `make db-migrate`.

Frontend
- Add a small chat panel in the duel screen.
- Limit requests (disable button if hints are exhausted or cooldown is active).

## 10) Why this fits the MVP goals

- **Local and free**: no external API costs.
- **Low complexity**: reuses FastAPI, Postgres, and existing match flow.
- **Easy to explain**: strict policy + short hints + logging.
- **Safe for evaluation**: no direct solutions are provided.
