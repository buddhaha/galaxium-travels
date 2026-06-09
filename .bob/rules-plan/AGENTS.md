# Plan Mode Rules (Non-Obvious Only)

This file contains project-specific architectural constraints for Plan mode.

## Service Layer Architecture
- Services MUST return union types (`ModelOut | ErrorResponse`) - exception-based error handling breaks MCP tools
- Two session management patterns coexist: manual (MCP) vs dependency injection (REST)
- This dual pattern is intentional - MCP tools can't use FastAPI dependencies

## Database Constraints
- Seat counters updated in service layer only - no DB triggers or constraints
- No cascade deletes configured - intentional to preserve booking history
- Three independent seat counters per flight (economy/business/galaxium) - not a single counter
- SQLite chosen for simplicity - production would need connection pooling

## Type System Constraints
- Seat class uses Literal type - runtime validation requires exact string match
- Pricing multipliers hardcoded in service layer (not configurable by design)
- Integer-only pricing - decimal handling would require schema changes

## Testing Architecture
- Tests require specific directory execution due to sys.path manipulation in conftest.py
- In-memory SQLite with StaticPool prevents "database locked" errors in tests
- Fixtures patch SessionLocal globally - affects both MCP and REST code paths

## MCP Integration Constraint
- MCP server MUST be created before FastAPI app - lifespan combination requirement
- This ordering is non-negotiable due to FastAPI's lifespan handling
- MCP tools manually manage sessions - can't use FastAPI's dependency injection

## Frontend-Backend Coupling
- Vite proxy strips `/api` prefix - backend endpoints don't include `/api`
- Error detection relies on `success: false` field - not HTTP status codes alone
- Base URL fallback pattern allows both dev and production deployments

## Startup Dependencies
- Backend must start before frontend (frontend proxy depends on backend)
- Ports 8080 and 5173 are hardcoded in multiple places (vite.config.ts, start.sh)
- Virtual environment activation required - system Python won't have dependencies

## Performance Considerations
- SQLite file-based DB - concurrent writes will block (not suitable for high load)
- No caching layer - every request hits database
- Seat counter updates not atomic - race conditions possible under load