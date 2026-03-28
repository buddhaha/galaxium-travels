---
name: issue-intake
description: Fetch and analyse a GitHub issue to produce a structured intake summary. Trigger when the user types '/issue-intake <N>' or says 'let's work on issue #N' or 'pick up issue N'. Always the first step — never skip to design or code without doing this first.
---

# Issue Intake

Fetch the issue, understand it, identify what needs a decision before any design begins.

## Steps

**1. Fetch:**
```bash
gh issue view <N> --json title,body,labels,comments
```

**2. Produce a structured summary with these sections:**

- **Problem** — what is broken or missing, and why it matters to users
- **What's well-defined** — requirements clear enough to implement directly
- **Needs a design decision** — numbered list of questions that must be answered before coding; each should be a genuine choice with trade-offs, not a trivial detail
- **Risk** — Low / Medium / High + one sentence why

**3. End with the gate:**
```
👤 GATE 1 — Intake complete.
Type 'approve' to move into the design session, or ask questions.
```

## Rules
- No code, no design, no opinions during intake
- If the issue proposes a technical approach, note it but do not evaluate it yet — that happens in the design session
- Keep the output short enough to read in 60 seconds
