# VERIFY.md — product-sense.md

Standard for `/verify-artifact` when the artifact is a Product Sense produced by `/product-definition`. The mechanism lives in `skills/verify-artifact/SKILL.md`; this file only says what failure looks like here.

## Artifact and sources

- **Artifact:** `product-sense.md`, plus the producing run's reply (its list of reported open truths).
- **Authoritative sources:** the Product Idea (`product-idea.md`), any business/domain context the invocation or product directory established as authoritative, and the Decision Management record (`decisions.md`) when one exists — an accepted resolution is a source. Nothing else counts — not prior drafts, not the producing conversation, not "common practice".
- **Required inputs beyond sources:** the confirmed phase objective; the commitments recorded in authoritative artifacts (needed for PS-5/PS-6); the prior `product-sense.md` and declared scope on a scoped update (needed for PS-9).
- **Statement** (for traceability): every sentence in sections 1–7, except headings and sentences the artifact itself marks as derivation notes ("derived from …"). No keyword filter: a sentence with no modal verb can still assert product truth ("Tables seat four."), and the finder decides nothing — it looks for the span.
- **Source** (for traceability): a verbatim span from an authoritative input that explicitly states the statement, or a span whose denial the statement would contradict (the admission gate's step 2).
- **Write scope:** `product-sense.md` only. On a scoped update, only the sections the declared changed scope names.

## Stage 1 — Mechanical checks (failures are Important; finders do not run until clean)

mechanical: `skills/product-definition/scripts/verify_mechanical.py --artifact product-sense.md [--prior … --scope …]`  
then, on a scoped update: `skills/verify-artifact/scripts/verify_generic.py write-scope …`.

- D-1 Eight section headings present, in order: Product Framing, Product Scope, Responsibilities & Authority, Capabilities & Behaviors, Business & Domain Rules, Failure & Recovery, Acceptable Quality, Open Questions.
- D-2 Open truths use the artifact's own marker ("No X is established by the authoritative inputs" / "unresolved and deliberately not stated"), never an ID, `TBD`, or `TODO`.
- D-3 `Status: Draft — N open` equals the number of open markers; `Status: Confirmed` requires zero.
- D-W On a scoped update, no section outside the declared scope differs from `--prior`.

## Stage 2 — Finder families

One fresh-context finder per family; each receives only its family's checks and returns a table, not prose.

| Family | Checks | Finder output |
|---|---|---|
| Traceability | PS-1, PS-2, PS-3, PS-4, PS-11, PS-12 | one row per statement: `statement \| source span \| none` — every `none` is a candidate; PS-2/PS-3/PS-11/PS-12 are the labels the finder attaches when the nearest span exists but does not support the statement |
| Gaps & open truths | PS-5, PS-6, PS-8 | one row per committed capability: `capability \| dependent truths \| source or none \| open marker or none`; plus one row per reported open truth and per Open Question with its justification |
| Boundary & scope | PS-7, PS-9, PS-10 | one row per flagged sentence / section / invalidates entry |

Run the Traceability family on a different model family when one is available; it checks for the author model's own habit.

## What failure looks like — Important

Each check names the admission-gate rule it enforces. The finder quotes the artifact statement and either the source span that fails to support it or "no source found".

- **PS-1 Over-admission.** A statement with no explicit source, whose denial would not contradict any source. The author wrote something plausible, conventional, or safe. *Evidence:* the statement; the closest source span, with a one-line argument that denying the statement is consistent with it.
- **PS-2 Exclusivity from sufficiency.** A source says the user can reach an outcome one way; the artifact says that is the only way, or forbids other ways. *Evidence:* both spans.
- **PS-3 Outcome relieved because a person was relieved.** A source says someone need not know or apply a rule; the artifact says the outcome need not satisfy it. *Evidence:* both spans.
- **PS-4 Guessed value.** A number, threshold, time window, ranking, default, or policy appears where no source establishes one. The correct artifact text is "no X is established by the authoritative inputs". *Evidence:* the value; "no source found".
- **PS-5 Gap not left open.** A committed capability's correctness, authority, or required behavior depends on a truth the sources do not settle, and the artifact neither marks it open nor does the reply report it. *Evidence:* the capability statement; the dependency; no marker, no report line.
- **PS-6 Spurious open truth.** A truth is reported open that no recorded commitment and no confirmed phase objective requires — the OMIT branch written as OPEN. *Evidence:* the reported line; no artifact commitment that needs it.
- **PS-7 Downstream leakage.** A statement about how the product is verified (tests, evaluators, examples, coverage), designed, built, or observed. *Evidence:* the statement. Fix: restate as a product-level truth or delete.
- **PS-8 Self-classified Open Question.** An entry in Open Questions that is neither an owner-kept-open item nor a Decision Management DEFER. *Evidence:* the entry; no owner or DM record.
- **PS-9 Scope overreach.** On a scoped update, a section outside the declared scope changed. *Evidence:* diff hunk; declared scope.
- **PS-10 Speculative invalidation.** `invalidates` lists a downstream scope not consumed by the semantics that actually changed. *Evidence:* the entry; the artifact change.
- **PS-11 Silent authority.** Section 3 grants the agent an action without a source stating the grant, or omits a confirmation requirement a source states. Authority is the highest-cost over-admission, so it is listed separately. *Evidence:* both spans.
- **PS-12 Interaction semantics by accident.** A statement decides persistence across sessions, failure behavior, or which quality concern outranks another, without a source. *Evidence:* the statement; "no source found".

## What failure looks like — Nit (cap: 5, applied after merge across finders)

- **PS-N1** A derivation is annotated where a reader could reconstruct it, or missing where they could not.
- **PS-N2** A statement is phrased as procedure rather than as what should be true.
- **PS-N3** A committed-future-scope item lives in "in scope now" or vice versa, with the source agreeing on the commitment but not the timing.
- **PS-N4** `artifact_changes` on a fresh draft has more than one entry, or on a scoped update is more granular than routing needs.

## Resolution

Per `verify-artifact` Stage 5: an Important is **fixed**, **refuted** by a verbatim span the finder missed (script-confirmed), or **owner-resolved** by the founder. The producing skill cannot close a finding by explanation. For PS-1 in particular, "it's obvious" is not a span.

## Pre-existing (not counted against the artifact; reported as open truths for the P0 owner)

- **PS-P1** Two authoritative inputs contradict each other on a product truth.
- **PS-P2** An authoritative input is ambiguous in a way that admits two incompatible product-level readings, and the artifact picked one.

Each is one line in the report's Open truths block, decided by the founder. The artifact author does not resolve them.

## Skip

Nothing is skipped. Section 8 is reviewed only under PS-8.

## Smoke fixtures

`fixtures/planted/` (when added): copies of a known-good Product Sense each with one planted defect, named for the check it must trigger — at minimum `PS-1-over-admission.md`, `PS-4-guessed-value.md`, `PS-5-missing-issue.md`. Run once after editing this file; each named check must fire.
