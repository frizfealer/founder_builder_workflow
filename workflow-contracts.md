# Workflow Contracts

Shared interface for every phase skill.

A phase run ends by returning a `PhaseResult` in exactly this shape. A `PhaseResult` reports what happened this round; routing — direct repair, Decision Management, reruns — belongs to the always-on policies in `CLAUDE.md`.

## PhaseResult

```yaml
phase_result:
  status: complete  # complete | blocked

  artifact_changes:  # 0..N
    - artifact: product-sense.md
      scope: confirmation
      summary: Updated confirmation semantics.

  issues:  # 0..N
    - id: I-001
      statement: <what appears wrong or unresolved>
      evidence: <what exposed the problem>
      affected_phase: P0  # P0 | P1 | P2 | P3 | unknown
      uncertainty: true
      blocks_current_phase: true

  invalidates:  # 0..N
    - artifact_or_scope: verification-design / confirmation
      reason: Confirmation semantics changed.
```

When a collection is empty, return an empty list:

```yaml
artifact_changes: []
issues: []
invalidates: []
```

- **`status`** — whether this round of phase work could finish. Use `blocked` only when an open Issue has `blocks_current_phase: true`.
- **`artifact_changes`** — 0..N changes to artifacts this phase owns.
- **`issues`** — 0..N observations requiring routing. Each Issue has its own `id` so the outer loop can route them independently.
- **`invalidates`** — 0..N downstream scopes known to be stale because of this change. Include only impacts known from the change; do not list speculative impacts. Reporting an invalidation does not itself trigger a rerun; the Lifecycle Policy does.

## Issue

An Issue reports observations only. Classification (`DROP / DEFER / RESOLVE NOW`), decision owner, and resolution are Decision Management output — leave them out of the Issue. One Issue carries one independently routable unresolved problem: split a finding when its parts can be resolved independently, may have different owners, or may receive different Decision Management verdicts.

- **`id`** — stable identifier for this Issue within the phase result, such as `I-001`.
- **`statement`** — what appears wrong or unresolved.
- **`evidence`** — what exposed the problem.
- **`affected_phase`** — routing hint: the lifecycle phase most likely responsible for inspecting or correcting the issue, given current evidence. No root-cause proof is required; use `unknown` when it cannot reasonably be determined.
- **`uncertainty`**
  - `false` — no unresolved judgment about what should be true is required; proceed through direct diagnosis/repair without Decision Management.
  - `true` — what should be true is not derivable from current authoritative artifacts; use Decision Management.
- **`blocks_current_phase`** — whether the current phase can finish honest work without resolving the issue.

## Ownership Contract

```text
P0 owns → Product Sense

P1 owns → Verification Design / Example Map / Eval Specs

P2 owns → Engineering Design + Build

P3 owns → Verification Evidence / Observed Learning
```

Rules:

- No phase may silently redefine another phase's authoritative truth.
- When a phase needs truth another phase owns and finds it missing or ambiguous, it reports an Issue with `affected_phase` set to that phase — it does not fill the gap inside its own artifacts.
- P3 learning is evidence, not automatically product truth.
