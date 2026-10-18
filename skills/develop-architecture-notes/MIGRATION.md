# Migrating from v0.2 to v0.3

v0.3 is intentionally simpler. Do not mechanically convert every v0.2 field.

## 1. Create `docs/architecture/architecture-notes.md`

Keep only information that helps a human/coding agent understand the current architecture needed for the next tracer.

Map roughly as follows:

| v0.2 | v0.3 |
|---|---|
| `scope` | Scope |
| architecture-significant `drivers` | Drivers |
| missing in v0.2 | Architecture Vision (write a fresh low-resolution view) |
| current significant `decisions` | Significant Decisions |
| `assumptions` / `hypotheses` / `open_questions` that still matter | Risks / Unknowns |
| `checks` | Remove from Architecture Notes; keep in behavior/engineering eval systems where they belong |
| implementation status | Remove; inspect code/evidence when an architecture update is requested |
| supersession/history | Rely on VCS and ADRs when durable history matters |
| `readiness` | Replace with the conversational tracer sufficiency stopping rule |

## 2. Do not migrate bookkeeping for its own sake

A v0.2 assumption/hypothesis/check that no longer affects a significant decision should disappear from the architecture artifact rather than being preserved because the old schema had a field for it.

## 3. Preserve durable decisions

If an existing accepted decision is still architecturally significant, carry its substance into Significant Decisions and link its ADR if one exists. The Markdown note is the current working view, not a complete decision ledger.

## 4. Re-scope around the next tracer

v0.3 is intentionally tracer-oriented. Explicitly state what the next tracer covers and what is deferred.
