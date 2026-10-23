# REVIEW.md — product-sense.md

Standard for `/review-artifact` when the artifact is a Product Sense produced by `/product-definition`. The mechanism lives in `skills/review-artifact/SKILL.md`; this file only says what failure looks like here.

## Artifact and sources

- **Artifact:** `product-sense.md`, plus `phase-result.yaml` from the same run.
- **Authoritative sources:** the Product Idea (`product-idea.md`) and any business/domain context the invocation or product directory established as authoritative. Nothing else counts as a source — not prior drafts, not the producing conversation, not "common practice".
- **Statement** (for traceability): any sentence in sections 1–7 that says what is or must be true of the product — it uses must / may / never / only / always / requires, names a value, threshold, limit, policy, or authority, or names an actor and what they can do.
- **Source** (for traceability): a verbatim span from an authoritative input that explicitly states the statement, or a span whose denial the statement would contradict (the admission gate's step 2).
- **Write scope:** `product-sense.md` and `phase-result.yaml` only. On a scoped update, only the sections the declared changed scope names.

## Deterministic pre-checks (run before finders; failures are Important)

- D-1 Eight section headings present, in order: Product Framing, Product Scope, Responsibilities & Authority, Capabilities & Behaviors, Business & Domain Rules, Failure & Recovery, Acceptable Quality, Open Questions.
- D-2 No Issue ID pattern (`I-\d{3}`) anywhere in `product-sense.md`.
- D-3 `phase-result.yaml` parses and has `status`, `artifact_changes`, `issues`, `invalidates`; empty collections are `[]`.
- D-4 `status: blocked` iff some Issue has `blocks_current_phase: true`.
- D-5 Every Issue has `uncertainty` and `affected_phase` set; `affected_phase` is one of P0 P1 P2 P3 unknown.

## What failure looks like — Important

Each check names the admission-gate rule it enforces. The finder quotes the artifact statement and either the source span that fails to support it or "no source found".

- **PS-1 Over-admission.** A statement with no explicit source, whose denial would not contradict any source. The author wrote something plausible, conventional, or safe. *Evidence:* the statement; the closest source span, with a one-line argument that denying the statement is consistent with it.
- **PS-2 Exclusivity from sufficiency.** A source says the user can reach an outcome one way; the artifact says that is the only way, or forbids other ways. *Evidence:* both spans.
- **PS-3 Outcome relieved because a person was relieved.** A source says someone need not know or apply a rule; the artifact says the outcome need not satisfy it. *Evidence:* both spans.
- **PS-4 Guessed value.** A number, threshold, time window, ranking, default, or policy appears where no source establishes one. The correct artifact text is "no X is established by the authoritative inputs". *Evidence:* the value; "no source found".
- **PS-5 Missing Issue.** A committed capability's correctness, authority, or required behavior depends on a truth the sources do not settle, and `phase-result.yaml` has no Issue for it. *Evidence:* the capability statement; the dependency; absence in `issues`.
- **PS-6 Spurious Issue.** An Issue was raised for a question no recorded commitment and no confirmed phase objective requires — the OMIT branch written as ISSUE. *Evidence:* the Issue statement; no artifact commitment that needs it.
- **PS-7 Downstream leakage.** A statement about how the product is verified (tests, evaluators, examples, coverage), designed, built, or observed. *Evidence:* the statement. Fix: restate as a product-level truth or delete.
- **PS-8 Self-classified Open Question.** An entry in Open Questions that is neither an owner-kept-open item nor a Decision Management DEFER. *Evidence:* the entry; no owner or DM record.
- **PS-9 Scope overreach.** On a scoped update, a section outside the declared scope changed. *Evidence:* diff hunk; declared scope.
- **PS-10 Speculative invalidation.** `invalidates` lists a downstream scope not consumed by the semantics that actually changed. *Evidence:* the entry; the artifact change.
- **PS-11 Silent authority.** Section 3 grants the agent an action without a source stating the grant, or omits a confirmation requirement a source states. Authority is the highest-cost over-admission, so it is listed separately. *Evidence:* both spans.
- **PS-12 Interaction semantics by accident.** A statement decides persistence across sessions, failure behavior, or which quality concern outranks another, without a source. *Evidence:* the statement; "no source found".

## What failure looks like — Nit (cap: 5 per review)

- **PS-N1** A derivation is annotated where a reader could reconstruct it, or missing where they could not.
- **PS-N2** A statement is phrased as procedure rather than as what should be true.
- **PS-N3** A committed-future-scope item lives in "in scope now" or vice versa, with the source agreeing on the commitment but not the timing.
- **PS-N4** `artifact_changes` on a fresh draft has more than one entry, or on a scoped update is more granular than routing needs.

## Pre-existing (not counted against the artifact; routed as Issues)

- **PS-P1** Two authoritative inputs contradict each other on a product truth.
- **PS-P2** An authoritative input is ambiguous in a way that admits two incompatible product-level readings, and the artifact picked one.

Routing: `affected_phase: P0`, `uncertainty: true`, `blocks_current_phase` as the reviewer judges from whether the artifact can stand with the truth marked unresolved. The founder, not the artifact author, owns the answer.

## Skip

Nothing is skipped. Section 8 is reviewed only under PS-8.

## Relationship to evals

`evals/cases.yaml` (when added for this skill) tests whether the *skill* applies the gate on fixtures. This file tests whether a *given artifact* passed the gate. Same must/must-not list, different object under test; keep them in sync.
