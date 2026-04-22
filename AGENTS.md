# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Critical Non-Obvious Patterns

**MCP Server Initialization:**
- MCP server (`mcp = FastMCP(...)`) MUST be created BEFORE FastAPI app to properly combine lifespans (see server.py:14-16)
- MCP tools raise exceptions on error; REST routes return `Union[ModelOut, ErrorResponse]` (no exceptions)

**Database Sessions:**
- MCP tools manually manage sessions (`SessionLocal()` + try/finally)
- REST routes use dependency injection (`Depends(get_db)`)
- Tests override `SessionLocal` via monkeypatch AND `app.dependency_overrides` (both required, see conftest.py:49-62)

**Seat Class Pricing:**
- Price multipliers in `services/booking.py:8-12` (economy: 1.0, business: 2.5, galaxium: 5.0)
- `base_price` on Flight model is economy price; other classes calculated at booking time
- Seat availability tracked separately: `economy_available`, `business_available`, `galaxium_available`

**Testing:**
- Run single test: `cd booking_system_backend && pytest tests/test_services.py::test_function_name -v`
- Tests use in-memory SQLite with `StaticPool` (not file-based)
- `seed()` is monkeypatched to no-op during tests (conftest.py:53)

**Server Startup:**
- Backend runs on port 8080 (not 8000 as typical FastAPI default)
- `start.sh` uses Python 3.11 specifically and creates `.venv` if missing
- Backend logs to `backend.log` (deleted on cleanup)

**Type Checking:**
- Pyright disabled globally (`pyrightconfig.json`) - project uses runtime validation via Pydantic v2

## SDLC Workflow Rules

This project uses Bob's structured human-in-the-loop workflow:

1. **Never commit without explicit human approval** in the current session
2. **Never push to remote** without explicit human approval
3. **Never create PRs or GitHub comments** autonomously
4. **One PLAN.md task at a time** — no scope creep between tasks
5. **Always show the diff** before staging anything
6. **PLAN.md is the contract** — do not deviate without asking
