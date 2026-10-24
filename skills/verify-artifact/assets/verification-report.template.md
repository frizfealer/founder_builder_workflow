# Verification report — <artifact path>

Standard: <VERIFY.md path>  
Inputs: artifact · sources <list> · phase objective <quoted> · commitments <artifact list> · prior <path | n/a> · scope <declared | fresh draft>  
Inputs status: **complete** | **incomplete — <what is missing>** (an incomplete run cannot report a pass)

## Stage 1 — Mechanical

`verify_mechanical.py --kind <kind> …` → <n> failure(s). <Paste the script output verbatim; a clean run pastes the summary line.>

## Stage 2–3 — Finders and verifier

Finders (one per family): <family: model> · … Candidates: <n> · Verified: <n> · Dropped: <n> · Nit cap <n> applied after merge.

## Summary

Important: <n> open / <n> fixed / <n> refuted / <n> owner-resolved · Nit: <n> · Pre-existing: <n> (listed under Open truths below)

Verification status: **open** | **closed** (closed = no open Important and inputs complete)

## Findings

### Important

#### V-01 — <check ID>: <failure, one sentence>
- artifact: "<quote>" (<location>)
- source: "<quote>" (<location>) | none — searched <files>
- resolution: open | fixed in <location>, re-verified <run id> | refuted by span "<quote>" (<location>), script-confirmed | owner-resolved by <name>: <reason>

### Nit

#### V-nn — <check ID>: <failure>
- artifact: "<quote>" (<location>)
- source: …

### Pre-existing (upstream)

#### V-nn — <check ID>: <failure>
- artifact: "<quote>" (<location>)
- source: "<quote>" (<location>)
- open truth for: <P0|P1|P2 owner>

## Open truths for the owner

One line each; the producing skill repeats these in its reply and confirms each has an open marker in the artifact.

- <unresolved truth> · evidence: "<span>" (<location>) · decides: <P0 owner | P1 owner | …>

## Dropped candidates

| id | stage | reason dropped |
|----|-------|----------------|
| C-nn | 3a | artifact quote not found verbatim (script) |
| C-nn | 3b | source quote not found verbatim (script) |
| C-nn | 3b | `none` claim disproved: span found at <location> |
| C-nn | 3c | quoted evidence does not support the stated failure |
| C-nn | cap | Nit over cap, weaker evidence |
