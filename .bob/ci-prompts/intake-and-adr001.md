# Issue Intake & ADR-001 Generation

You are analyzing GitHub issue #{{ISSUE_NUMBER}}: "{{ISSUE_TITLE}}"

## Your Task

1. **Analyze the issue** and extract:
   - The feature request or problem being solved
   - Key requirements and constraints
   - Success criteria

2. **Generate ADR-001** (Architecture Decision Record 001) with:
   - A clear problem statement
   - Three distinct design options (A, B, C)
   - Pros and cons for each option
   - A recommendation (but let the human decide)

## Output Format

Structure your response as follows:

```markdown
# 📋 Issue Intake Complete

## Summary
[Brief 2-3 sentence summary of what the issue is requesting]

## Key Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Success Criteria
- [Criterion 1]
- [Criterion 2]

---

# 🏗️ ADR-001: [Decision Title]

## Context
[Explain the architectural decision that needs to be made - typically about data model, core approach, or system design]

## Options

### Option A: [Approach Name]
**Description:** [Clear description of this approach]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Implementation Notes:**
- [Key implementation detail 1]
- [Key implementation detail 2]

### Option B: [Approach Name]
**Description:** [Clear description of this approach]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Implementation Notes:**
- [Key implementation detail 1]
- [Key implementation detail 2]

### Option C: [Approach Name]
**Description:** [Clear description of this approach]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Implementation Notes:**
- [Key implementation detail 1]
- [Key implementation detail 2]

## Recommendation
[Your analysis of which option might be best and why, but emphasize that the human should decide]

---

**Next Step:** Please reply with **A**, **B**, or **C** to select your preferred approach. You can add notes like "B with changes: [your modifications]"
```

## Guidelines

- Focus ADR-001 on the **core architectural decision** - usually data model or fundamental approach
- Make options meaningfully different (not just minor variations)
- Be specific about implementation implications
- Consider the existing codebase (FastAPI, SQLAlchemy, SQLite, Pydantic v2)
- Keep it concise but thorough
- Don't make the decision - present options for human choice

## Context About This Project

This is the Galaxium Travels booking system:
- **Backend:** Python 3.11, FastAPI, SQLAlchemy (sync), SQLite, Pydantic v2, FastMCP
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS
- **Database:** SQLite with models: User, Flight, Booking
- **Current Features:** User registration, flight search/filtering, single-passenger bookings, cancellations
- **Architecture:** REST API + MCP protocol for AI agents

The issue body follows below.