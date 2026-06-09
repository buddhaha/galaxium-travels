# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Test Execution
- **CRITICAL**: Tests MUST be run from `booking_system_backend/` directory, not project root
- Running from root causes `conftest.py` import failures
- Single test: `cd booking_system_backend && pytest tests/test_services.py::test_function_name`

## Service Layer Pattern
- All service functions return `ModelOut | ErrorResponse` - NEVER raise exceptions
- MCP tools manually manage sessions: `db = SessionLocal()` with try/finally blocks
- REST endpoints use FastAPI dependency injection: `db: Session = Depends(get_db)`
- Email addresses auto-normalized to lowercase in user service (case-insensitive lookups)

## Database Operations
- Seat counters updated in service layer functions, not via DB triggers
- No cascade deletes - bookings don't auto-delete when flights/users deleted
- SQLite file: `booking.db` in backend directory (delete to reset with seed data)

## MCP Integration
- MCP server MUST be created before FastAPI app (line 16 before line 118 in server.py)
- Required for proper lifespan combination
- MCP mounted at `/mcp` endpoint after FastAPI app creation

## Pricing System
- Hardcoded multipliers in `services/booking.py:8-12`: economy=1.0, business=2.5, galaxium=5.0
- Integer pricing: `int(base_price * multiplier)` - no decimal handling
- Seat class validation uses Literal type: must be exact strings 'economy', 'business', 'galaxium'

## Frontend API Integration
- Vite proxy rewrites `/api/*` to backend (removes `/api` prefix)
- API base URL: `import.meta.env.VITE_API_URL || '/api'`
- Error responses have `success: false` field for type guard checking

## Startup
- `start.sh` creates venv if missing, kills existing processes on ports 8080/5173
- Backend uses `.venv/bin/python` directly (not system python) after venv activation