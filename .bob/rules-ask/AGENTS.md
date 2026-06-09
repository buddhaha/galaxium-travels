# Ask Mode Rules (Non-Obvious Only)

This file contains project-specific documentation context for Ask mode.

## Project Structure
- Backend in `booking_system_backend/` - FastAPI with dual REST/MCP protocol support
- Frontend in `booking_system_frontend/` - React + TypeScript with Vite
- Tests MUST run from backend directory, not project root (conftest.py import requirement)

## Hidden Architecture Patterns
- Service layer returns union types (`ModelOut | ErrorResponse`) instead of raising exceptions
- MCP tools manually manage DB sessions, REST endpoints use dependency injection
- Two separate session management patterns in same codebase (intentional design)

## Database Design
- Three independent seat counters per flight (economy/business/galaxium)
- No cascade deletes - bookings persist when flights/users deleted (intentional)
- Seat updates happen in service layer, not via DB triggers
- SQLite file location: `booking_system_backend/booking.db`

## Pricing Architecture
- Hardcoded multipliers in `services/booking.py:8-12` (not in config/env)
- Integer-only pricing: `int(base_price * multiplier)` - no decimal support
- Seat class validation uses Literal type - exact string match required

## MCP Integration Pattern
- MCP server MUST be created before FastAPI app (line 16 vs 118 in server.py)
- Required for proper lifespan combination (non-obvious FastAPI pattern)
- MCP mounted at `/mcp` after app creation

## Frontend API Pattern
- Vite proxy strips `/api` prefix before forwarding to backend
- Base URL uses env var fallback: `import.meta.env.VITE_API_URL || '/api'`
- Error detection via `success: false` field (type guard pattern)

## Testing Architecture
- In-memory SQLite with StaticPool for tests (not file-based)
- Fixtures patch SessionLocal to inject test session
- Test directory requirement is due to sys.path manipulation in conftest.py

## Startup Behavior
- `start.sh` auto-creates venv if missing (not documented in quick start)
- Kills existing processes on ports 8080/5173 before starting
- Uses `.venv/bin/python` directly (not system python) after activation