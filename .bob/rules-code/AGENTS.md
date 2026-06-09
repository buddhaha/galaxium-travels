# Code Mode Rules (Non-Obvious Only)

This file contains project-specific coding rules discovered by reading the codebase.

## Backend Service Layer
- Service functions return `ModelOut | ErrorResponse` union types - NEVER raise exceptions
- MCP tools use manual session management: `db = SessionLocal()` with try/finally
- REST endpoints use dependency injection: `db: Session = Depends(get_db)`
- Email normalization happens in user service (lowercase conversion for case-insensitive lookups)

## Database Patterns
- Seat counters (economy/business/galaxium) updated in service layer, NOT via DB triggers
- No cascade deletes configured - bookings persist when flights/users deleted
- SQLite file `booking.db` in backend directory - delete to reset with seed data

## Type System
- Seat class uses Literal['economy', 'business', 'galaxium'] - exact string match required
- Pricing multipliers hardcoded in `services/booking.py:8-12` (not configurable)
- Integer pricing only: `int(base_price * multiplier)` - no decimal handling

## Testing
- Tests MUST run from `booking_system_backend/` directory (not project root)
- Running from root causes `conftest.py` import failures
- Test DB uses in-memory SQLite with StaticPool
- Fixtures patch SessionLocal to use test session

## MCP Integration
- MCP server created BEFORE FastAPI app (line 16 before 118 in server.py)
- Required for proper lifespan combination
- MCP mounted at `/mcp` after FastAPI app creation

## Frontend API
- Vite proxy rewrites `/api/*` to backend (strips `/api` prefix)
- Base URL: `import.meta.env.VITE_API_URL || '/api'`
- Error responses have `success: false` field for type guard: `isErrorResponse()`

## Startup Script
- `start.sh` creates venv if missing, kills processes on ports 8080/5173
- Backend uses `.venv/bin/python` directly after venv activation (not system python)