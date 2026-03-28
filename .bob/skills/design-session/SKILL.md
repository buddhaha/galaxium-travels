---
name: design-session
description: Run a structured design decision session for a feature after issue intake is approved. Trigger when the user types 'approve' after /issue-intake, or '/design-session', or 'let's design this'. Walks through each key architectural decision one at a time using ADR format, waits for human approval at each gate, then generates PLAN.md. Never skip a gate. Never generate PLAN.md until all decisions are approved.
---

# Design Session

You are running the design phase of the SDLC workflow. The issue intake is complete and approved. Your job is to surface the key architectural decisions — one at a time — get a human decision on each, then produce the implementation plan.

## How This Works

You present each ADR in sequence. Each one ends with a `👤 GATE` where the human types their choice. You wait. You do not move to the next ADR until you have an explicit answer. You do not generate PLAN.md until all gates are resolved.

At the end of each session, write a summary table of all decisions before generating PLAN.md.

---

## ADR Presentation Format

For each decision, use this structure — keep it concise enough to read in 90 seconds:

```
## ADR-00N: [Decision Title]

[One sentence: what this decision is about and why it matters.]

**Option A — [Name]**
  + [Strongest pro]
  + [Second pro if relevant]
  - [Main con]

**Option B — [Name]**
  + [Strongest pro]
  - [Main con]
  - [Second con if relevant]

**Option C — [Name]** (if applicable)
  [Brief assessment — pros/cons or why it's inferior]

Bob recommends: Option [X] — [one sentence reason]

👤 GATE N — Type A, B, or C (or '[letter] with changes: ...')
```

Do not list more than 3 options. Do not pad with generic trade-off text. Every pro and con should be specific to *this* codebase and *this* feature.

---

## ADRs for the Group Booking Feature

Work through these three decisions in order:

### ADR-001: Group Booking Data Model

**What's at stake:** Where does group identity live in the database? The issue proposes adding nullable columns to the existing Booking table. Evaluate this honestly — recommend the better architecture even if it differs from the issue proposal.

**Options to present:**

- **Option A — Add group_id columns to Booking table** (as proposed in issue)
  - Pros: minimal migration, zero breaking changes, single-table queries
  - Cons: group_size is denormalised (can go stale), no clean home for future group-level data (group discount, notifications), `is_primary_booking` flag is redundant since primary user_id is already on every row

- **Option B — Separate GroupBooking table** (recommended)
  - Pros: group_size stored authoritatively once, cancellation has a single status field, future group features attach to GroupBooking cleanly
  - Cons: one extra migration file, queries need a LEFT JOIN to include group context

- **Option C — Pure junction table**
  - Brief: no natural home for group metadata — just re-invents Option B with more joins. Not recommended.

**Recommendation:** B — the extra migration file is a one-time cost; the normalisation benefit is permanent.

---

### ADR-002: Atomicity Strategy

**What's at stake:** How do we guarantee all-or-nothing booking for a group? This project uses SQLite — that changes the answer compared to Postgres.

**Options to present:**

- **Option A — Single SQLAlchemy transaction** (recommended)
  - Wrap the entire group creation (availability check → GroupBooking insert → N Booking inserts → seat decrement) in one `async with db.begin()` block. Rolls back entirely on any failure.
  - Pros: standard SQLAlchemy pattern, zero extra infrastructure, `with_for_update=True` is a no-op on SQLite but correct on Postgres (future-proof)
  - Cons: under SQLite WAL, concurrent writes queue — acceptable here

- **Option B — Optimistic locking (version column on Flight)**
  - Pros: strongest guarantee under high write concurrency on Postgres
  - Cons: requires new version column migration, retry logic in callers, zero practical benefit on SQLite. Over-engineered for this context.

**Recommendation:** A — standard, correct, and proportionate to the stack.

---

### ADR-003: API Endpoint Shape

**What's at stake:** One new endpoint vs extending the existing one vs a multi-step flow.

**Options to present:**

- **Option A — New dedicated endpoint `POST /api/book/group`** (recommended)
  - Pros: zero risk to existing /api/book, clean purpose-built schema, existing tests unaffected, MCP tool addition is clear
  - Cons: two booking endpoints to maintain

- **Option B — Extend existing `POST /api/book` to handle arrays**
  - Pros: single URL for all bookings
  - Cons: union types in Pydantic are a common source of validation bugs, existing endpoint contract becomes ambiguous, existing tests need auditing for regressions

- **Option C — Two-step: create group shell → confirm**
  - Pros: natural extension point for "add passenger later" (out of scope for Phase 1)
  - Cons: introduces a "pending group" state that must be cleaned up on abandonment — significant complexity for no Phase 1 benefit

**Recommendation:** A — clean, safe, and right-sized for Phase 1.

---

## After All Three Gates Are Approved

**1. Print a summary table:**

```
## Design Decisions — Resolved

| ADR | Decision | Key reason |
|-----|----------|------------|
| ADR-001 Data Model    | Option [X] | [one phrase] |
| ADR-002 Atomicity     | Option [X] | [one phrase] |
| ADR-003 API Shape     | Option [X] | [one phrase] |
```

**2. Generate PLAN.md** in the repo root using the template below, filling in tasks consistent with the approved decisions.

---

## PLAN.md Template

```markdown
# Plan: Issue #<N> — <Title>
> Decisions: ADR-001=[X] · ADR-002=[X] · ADR-003=[X]

## Context
<Two sentences: what the feature does and the key architectural choices made.>

## Tasks
- [ ] T1 (S): Add GroupBooking model to models.py (id, primary_user_id, flight_id, seat_class, group_size, status, created_at)
- [ ] T2 (S): Add Alembic migration for group_bookings table + group_booking_id FK on bookings
- [ ] T3 (S): Add GroupBookingCreate and GroupBookingResponse Pydantic schemas
- [ ] T4 (M): Implement group_booking.py service — atomic creation using SQLAlchemy transaction
- [ ] T5 (S): Add POST /api/book/group endpoint to server.py
- [ ] T6 (S): Add corresponding MCP tool for group booking
- [ ] T7 (M): Add cascade cancel logic — cancelling GroupBooking cancels all child Bookings
- [ ] T8 (M): Write integration tests — happy path, insufficient seats, partial availability

## File impact
| File | Change | Task |
|------|--------|------|
| models.py | Add GroupBooking model, FK on Booking | T1 |
| alembic/versions/ | New migration | T2 |
| schemas.py | GroupBookingCreate, GroupBookingResponse | T3 |
| services/group_booking.py | New service | T4 |
| server.py | New route + MCP tool | T5, T6 |
| services/booking.py | Cancel cascade | T7 |
| tests/test_services.py | Group booking tests | T8 |

## Security notes
- Validate all user_ids exist before inserting (prevent ghost bookings)
- Enforce group_size 2–10 in schema validation
- Availability check must happen inside the transaction (not before it)

## Test strategy
- Integration: book 3 seats, assert 3 Booking rows + 1 GroupBooking row created
- Integration: attempt 8-seat booking on flight with 5 available, assert 0 rows created
- Integration: cancel group, assert all child Bookings status = 'cancelled'
- Unit: validate group_size bounds (1 → error, 2 → ok, 10 → ok, 11 → error)

## Out of scope (Phase 1)
- Frontend changes
- Individual cancellation within a group
- Add/remove passengers after creation
- Email notifications to group members
```

---

## After Writing PLAN.md

Say:
```
✓ PLAN.md written to repo root.

Design session complete. All decisions locked and documented.

Next: open PLAN.md, review the task list, then start implementation
with: "Implement T1 from PLAN.md. Show me the diff before committing."
```
