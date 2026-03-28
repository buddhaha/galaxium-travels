# Galaxium Travels — Agent Context

## What This Project Is

A demo interplanetary travel booking system built for IBM Bob tutorials.
FastAPI backend (Python 3.11, SQLite, SQLAlchemy, Pydantic v2) +
React 18 frontend (Vite, TypeScript, Tailwind). Dual REST + MCP protocol support.

## Stack

- **Backend:** Python 3.11 · FastAPI · SQLAlchemy (sync, SQLite) · Pydantic v2 · FastMCP
- **Frontend:** React 18 · TypeScript · Vite · Tailwind CSS · Axios
- **Database:** SQLite (development) — WAL mode, serialised writes
- **Testing:** pytest · test_services.py (unit) · test_rest.py (integration)
- **Start:** `./start.sh` — runs both backend (port 8000) and frontend (port 5173)

## Key Files

```
booking_system_backend/
├── server.py       ← FastAPI app + REST routes + MCP tools
├── models.py       ← SQLAlchemy ORM: Flight, User, Booking
├── schemas.py      ← Pydantic request/response schemas
├── db.py           ← DB engine + session setup
├── seed.py         ← Demo data (10 users, 10 flights, 20 bookings)
└── services/
    ├── booking.py  ← book_flight(), cancel_booking(), get_user_bookings()
    ├── flight.py   ← get_flights(), update_availability()
    └── user.py     ← register_user(), get_user()
```

## Coding Patterns

- Services return `Union[ModelOut, ErrorResponse]` — no exceptions raised to the route layer
- Routes are thin: validate input, call service, return response
- Seat classes: `"economy"` / `"business"` / `"galaxium"` (string literals, not enum in current code)
- Availability tracked as `economy_available`, `business_available`, `galaxium_available` on Flight

## SDLC Workflow Rules

This project uses Bob's structured human-in-the-loop workflow:

1. **Never commit without explicit human approval** in the current session
2. **Never push to remote** without explicit human approval
3. **Never create PRs or GitHub comments** autonomously
4. **One PLAN.md task at a time** — no scope creep between tasks
5. **Always show the diff** before staging anything
6. **PLAN.md is the contract** — do not deviate without asking

## Active Workflow Skills

- `/issue-intake <N>` — Phase 1: fetch and structure a GitHub issue
- `/design-session` — Phase 2: walk through ADRs, collect decisions, generate PLAN.md
- After PLAN.md is approved: implement task by task (`"Implement T1 from PLAN.md. Show diff before committing."`)
