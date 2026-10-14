# Café example: updating Architecture Notes after a tracer

The default action after a tracer is **not** to redesign.

## Case 1 — Evidence supports the current design

The Create tracer passes its behavior scenarios and the implementation follows the existing Architecture Vision.

Result:

```text
No architecture change.
```

Do not add hypothesis state, check state, or a new decision just because evidence was collected.

## Case 2 — Modify introduces a materially different workflow

Suppose a later Modify tracer reveals long-lived intermediate state and recovery behavior that Create does not have.

Ask whether the existing Reservation Application boundary still gives good locality. If yes, keep the notes unchanged. If no, compare the minimum credible alternatives (potentially using `codebase-design` after the need for a different boundary is established) and update the current Architecture Vision/decision.

Use version control or an ADR if the old decision's rationale is important enough to preserve explicitly. Do not maintain a mandatory supersession graph inside Architecture Notes.

## Case 3 — A factual provider unknown becomes blocking

Before a real-provider tracer, R1 becomes blocking because the implementation cannot safely decide what to do after an ambiguous timeout.

Route the question to `research` or a bounded provider probe. Do not ask the user to choose "idempotency" as an architecture pattern without first establishing the provider facts.

Once the facts are known, update only the affected driver/decision/risk.
