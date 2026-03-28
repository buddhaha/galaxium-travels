# PLAN.md Generation

You are generating the final implementation plan for GitHub issue #{{ISSUE_NUMBER}}.

## Design Decisions Made

**ADR-001:** Option {{CHOICE_001}}

**ADR-002:** Option {{CHOICE_002}}

**ADR-003:** Option {{CHOICE_003}}

## Your Task

Generate a **PLAN.md** file that breaks down the implementation into ordered, atomic tasks.

## Output Format

Create a complete PLAN.md file with this structure:

```markdown
# Implementation Plan: [Feature Name]

**Issue:** #{{ISSUE_NUMBER}}

## Design Decisions

### ADR-001: [Decision Title]
**Selected:** Option {{CHOICE_001}}

### ADR-002: [Decision Title]
**Selected:** Option {{CHOICE_002}}

### ADR-003: [Decision Title]
**Selected:** Option {{CHOICE_003}}

---

## Implementation Tasks

### Phase 1: Database & Models

#### T1: Update Database Schema
**Goal:** [What this task accomplishes]

**Changes:**
- [ ] Modify `booking_system_backend/models.py`:
  - Add field: `field_name` (type, description)
  - Add field: `field_name` (type, description)
- [ ] Update database initialization in `db.py` if needed

**Acceptance:**
- Schema changes applied
- Database initializes without errors
- Existing data/tests still work

---

#### T2: Update Pydantic Schemas
**Goal:** [What this task accomplishes]

**Changes:**
- [ ] Modify `booking_system_backend/schemas.py`:
  - Add `SchemaName` for [purpose]
  - Update `ExistingSchema` with new fields
  - Add validation rules

**Acceptance:**
- Request/response schemas match new data model
- Validation rules enforce constraints
- Schemas are properly typed

---

### Phase 2: Business Logic

#### T3: Implement Core Service Logic
**Goal:** [What this task accomplishes]

**Changes:**
- [ ] Create/modify `booking_system_backend/services/[service].py`:
  - Implement `function_name()` with [specific behavior]
  - Add validation for [constraints]
  - Handle [error cases]

**Acceptance:**
- Service function works correctly
- Returns `Union[ModelOut, ErrorResponse]`
- Handles all edge cases

---

#### T4: Update Related Services
**Goal:** [What this task accomplishes]

**Changes:**
- [ ] Modify `booking_system_backend/services/[service].py`:
  - Update `existing_function()` to [handle new scenario]
  - Add [new behavior]

**Acceptance:**
- Existing functionality still works
- New behavior integrated smoothly
- No breaking changes

---

### Phase 3: API Endpoints

#### T5: Add REST Endpoint
**Goal:** [What this task accomplishes]

**Changes:**
- [ ] Modify `booking_system_backend/server.py`:
  - Add `POST /endpoint` route
  - Wire up to service layer
  - Add proper error handling

**Acceptance:**
- Endpoint accessible at `/endpoint`
- Returns correct response format
- Handles errors gracefully
- Appears in Swagger UI docs

---

#### T6: Add MCP Tool (if applicable)
**Goal:** [What this task accomplishes]

**Changes:**
- [ ] Modify `booking_system_backend/server.py`:
  - Add `@mcp.tool()` decorator
  - Implement tool function
  - Add proper docstring

**Acceptance:**
- MCP tool available to AI agents
- Raises exceptions on error (MCP pattern)
- Properly documented

---

### Phase 4: Testing

#### T7: Add Service Tests
**Goal:** [What this task accomplishes]

**Changes:**
- [ ] Create/modify `booking_system_backend/tests/test_services.py`:
  - Test successful [operation]
  - Test validation failures
  - Test edge cases
  - Test error handling

**Acceptance:**
- All service tests pass
- Coverage includes happy path and error cases
- Tests use in-memory SQLite

---

#### T8: Add REST API Tests
**Goal:** [What this task accomplishes]

**Changes:**
- [ ] Create/modify `booking_system_backend/tests/test_rest.py`:
  - Test endpoint with valid data
  - Test endpoint with invalid data
  - Test error responses

**Acceptance:**
- All REST tests pass
- Tests use TestClient
- Response formats validated

---

### Phase 5: Documentation & Cleanup

#### T9: Update Documentation
**Goal:** [What this task accomplishes]

**Changes:**
- [ ] Update `booking_system_backend/README.md` with new endpoint
- [ ] Update API documentation if needed
- [ ] Add code comments for complex logic

**Acceptance:**
- Documentation reflects new functionality
- Examples provided where helpful
- Code is well-commented

---

## Testing Strategy

**Unit Tests:** Service layer functions with mocked database
**Integration Tests:** REST endpoints with TestClient and in-memory SQLite
**Manual Testing:** Use Swagger UI at http://localhost:8080/docs

## Success Criteria

- [ ] All tasks completed
- [ ] All tests passing (pytest)
- [ ] No breaking changes to existing functionality
- [ ] API documented in Swagger UI
- [ ] Code follows project patterns (see AGENTS.md)

## Notes

- Each task should be completed and tested before moving to the next
- Run `cd booking_system_backend && pytest -v` after each task
- Use `./start.sh` to test the full system
- Backend runs on port 8080, frontend on 5173
```

## Guidelines

1. **Break down into atomic tasks** - each task should be completable in one focused session
2. **Order tasks logically** - database → models → services → API → tests → docs
3. **Be specific** - include exact file paths and function names
4. **Include acceptance criteria** - clear definition of "done" for each task
5. **Reference project patterns** - mention AGENTS.md patterns where relevant
6. **Consider the full stack** - backend changes, tests, documentation
7. **Make it actionable** - someone should be able to implement task-by-task

## Context About This Project

- **Backend:** Python 3.11, FastAPI, SQLAlchemy (sync), SQLite, Pydantic v2, FastMCP
- **Testing:** pytest, in-memory SQLite with StaticPool
- **Patterns:** Services return `Union[ModelOut, ErrorResponse]`, MCP tools raise exceptions
- **File structure:** See AGENTS.md for critical patterns

Review the issue and all ADR decisions to create a comprehensive implementation plan.