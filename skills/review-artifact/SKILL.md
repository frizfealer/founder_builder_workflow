---
name: review-artifact
description: Shared authoring-time reviewer for any phase artifact (product-sense.md, agent_spec.md, architecture-notes.md, BDD test files). Runs fresh-context finders against the artifact's own REVIEW.md, verifies every finding has quoted evidence, assigns Important / Nit / Pre-existing, converts upstream problems into PhaseResult Issues, and requires every Important to be fixed or resolved with a reason. Use after a phase skill finishes a round and before the owner confirms the artifact. Not a runtime judge of agent behavior.
argument-hint: <artifact path> <REVIEW.md path> [phase-result.yaml]
---

# /review-artifact — shared review mechanism

One mechanism, many standards. This skill owns **how** a review runs. Each producing skill owns **what failure looks like** for its artifact, in a `REVIEW.md` beside its `SKILL.md`. Never review without a `REVIEW.md`; never add a check that is not in it or in the four cross-artifact rules below.

## Inputs

- Artifact under review (path).
- `REVIEW.md` for that artifact kind.
- Authoritative sources the artifact must trace to, as `REVIEW.md` names them (Product Idea, product-sense.md, agent_spec.md, …).
- `phase-result.yaml` from the producing run, if it exists.
- For a scoped update: the declared changed scope.

## Four cross-artifact rules

These hold for every artifact and are checked in every review in addition to `REVIEW.md`:

1. **Traceability.** Every normative statement in the artifact points at a source: a rule ID, a quoted span from an authoritative input, or an existing fact in an upstream artifact. `REVIEW.md` says what "statement" and "source" mean for its artifact. No source → **Important**.
2. **Write scope.** Only files and sections the producing skill declares writable were changed; a scoped update touched only the declared scope. Otherwise → **Important**.
3. **Gaps become Issues, not fills.** Where sources are silent, the author must have left the gap explicit or reported an Issue — never decided it. An authored decision with no source → **Important**, and the reviewer drafts the Issue the author should have raised. A genuine problem in the *source* (contradiction, ambiguity) → **Pre-existing**, routed upstream as an Issue, not counted against this artifact.
4. **Done-when needs evidence.** Any claim that a check ran ("tests pass", "validated", "all steps implemented") must come with the output that shows it. Bare assertion → **Important**.

## Procedure

1. **Finders (fresh context, 2 in parallel).** Each finder receives only: the artifact, `REVIEW.md`, the sources, and the four rules. It does not see the producing conversation. It walks the artifact statement by statement and emits candidate findings in the format below. Finders are told the Nit cap from `REVIEW.md` and stop emitting Nits at the cap.
2. **Verifier (fresh context, 1).** Receives the artifact, sources, and the merged candidate list. For each finding it checks: (a) the artifact quote exists verbatim; (b) the source quote exists verbatim, or the "no source found" claim holds after searching the sources; (c) the quoted evidence actually supports the stated failure. Any check fails → finding dropped. Duplicates merged.
3. **Severity.** Verified findings keep the severity `REVIEW.md` assigns their check. Unlisted but verified problems default to Nit.
4. **Report.** Write `review-report.md` beside the artifact from `assets/review-report.template.md`. Append Pre-existing findings and rule-3 gaps to `phase-result.yaml` `issues` in the `workflow-contracts.md` shape (`affected_phase` as `REVIEW.md` routes it, `uncertainty: true`).
5. **Resolution.** The producing skill (or owner) must, for every **Important**: fix it, or mark it resolved with a one-line reason. Nits may be ignored. The review is closed when no Important is open. The artifact is not presented for owner confirmation until then.

## Finding format

```
id: R-nn
check: <REVIEW.md check ID or rule 1–4>
severity: Important | Nit | Pre-existing
artifact: "<verbatim quote>"  (<section / line>)
source:   "<verbatim quote>"  (<file, location>)  | no source found in <files searched>
failure:  <one sentence: what is wrong, in the words of the check>
```

A finding without both quote fields (or the explicit "no source found") is invalid and is dropped by the verifier.

## What this skill is not

- Not a runtime judge. It reviews artifacts at authoring time. Runtime judgment of agent responses belongs to the evaluation implementation.
- Not a style reviewer. Wording is a Nit at most, and only if `REVIEW.md` lists it.
- Not an escalation path. It drafts Issues; classification (DROP / DEFER / RESOLVE NOW) stays with Decision Management.

## Voting

Not used. One verifier with mandatory quoted evidence is the false-positive control. Add a second verifier only if a review log shows verified findings being overturned by owners more than occasionally.
