---
name: verify-artifact
description: Shared authoring-time verifier for any phase artifact (product-sense.md, agent_spec.md, architecture-notes.md, BDD test files). Runs mechanical checks first, then narrow fresh-context finders against the artifact's own VERIFY.md, verifies every finding has quoted evidence, assigns Important / Nit / Pre-existing, reports upstream problems as open truths for their owner, and requires every Important to be fixed — the author cannot close a finding by assertion. Use after a phase skill finishes a round and before the owner confirms the artifact. Not a runtime judge of agent behavior.
argument-hint: <artifact path> <VERIFY.md path> [--prior <previous artifact version> --scope <sections>]
---

# /verify-artifact — shared verification mechanism

One mechanism, many standards. This skill owns **how** verification runs and nothing that is specific to one artifact kind. Each producing skill owns **what failure looks like** for its artifact — its `VERIFY.md` (the standard), its `scripts/verify_mechanical.py` (the D-checks), and its `fixtures/planted/` (the smoke test), all beside its `SKILL.md`. Never verify without a `VERIFY.md`; never add a check that is not in it or in the four cross-artifact rules below.

What lives here, because it is identical for every artifact: `scripts/verify_lib.py` (quote lookup, section parsing, open-marker counting, write-scope diff, the finding Report) and `scripts/verify_generic.py` (findings quote-existence, status-header count, write-scope as CLI modes). A producing skill's checker imports `verify_lib`; nothing in this folder knows about Product Sense, Agent Spec, or any other kind.

Design goal: give the producing agent a feedback signal it can loop on (produce → verify → fix → re-verify) whose source is, as far as possible, **not the same model's judgment**. Three consequences shape everything below: mechanical checks run first and gate the rest; finders are narrow and adversarial rather than general reviewers; the author has no path to close a finding by asserting it is fine.

## Inputs

A verifier without its inputs returns silence, and the loop reads silence as pass. All of these are required; a missing one is reported as `inputs: incomplete` and the run does not claim a pass.

- Artifact under verification (path).
- `VERIFY.md` for that artifact kind.
- Authoritative sources, as `VERIFY.md` names them (Product Idea, `product-sense.md`, `agent_spec.md`, `example-map.md`, …).
- `decisions.md` or equivalent Decision Management record, if the workflow has one — resolutions are sources; a claim citing one is admitted.
- The confirmed **phase objective** and the **commitments** currently recorded in authoritative artifacts — needed to judge whether a gap should be left open or omitted.
- `--prior`: the previous version of the artifact (or a diff), when this is a scoped update. Without it, write-scope cannot be checked.
- The declared changed scope, for a scoped update.

## Four cross-artifact rules

Checked in every run in addition to `VERIFY.md`:

1. **Traceability.** Every statement in the artifact points at a source: a rule ID, a quoted span from an authoritative input, or an existing fact in an upstream artifact. `VERIFY.md` says what "statement" and "source" mean for its artifact. No source → **Important**.
2. **Write scope.** Only files and sections the producing skill declares writable changed; a scoped update touched only the declared scope (checked against `--prior`). Otherwise → **Important**.
3. **Gaps stay open, not filled.** Where sources are silent, the author must have left the truth open with the artifact's marker — never decided it. Authored decision with no source → **Important**; the fix is to replace the value with an open marker, and the verifier writes the open-truth line the author should have reported. A genuine problem in the *source* (contradiction, ambiguity) → **Pre-existing**, reported as an open truth for the upstream owner, not counted against this artifact.
4. **Done-when needs evidence.** A claim that a check ran ("tests pass", "validated") must come with the output that shows it. Bare assertion → **Important**.

## Procedure

### Stage 1 — Mechanical checks (script)

Run the script the artifact's `VERIFY.md` names on its `mechanical:` line (by convention `<producing skill>/scripts/verify_mechanical.py`), then `scripts/verify_generic.py status` (the artifact's `Status: Draft — N open` header equals the count of open markers the `VERIFY.md` defines) and, on a scoped update, `scripts/verify_generic.py write-scope`. The skill-owned script implements that kind's **D-checks** (structure, IDs, citation quotes found verbatim); the generic script covers what every artifact header and every scoped update must satisfy. Any failure is an **Important** finding with exact locations, written to the report before any model runs. The producing skill fixes these and re-runs Stage 1 until clean; Stage 2 does not start on a failing Stage 1. This is the fast, exact signal — spend model effort only on artifacts that already have the right shape.

### Stage 2 — Finders (fresh context, one per check family)

`VERIFY.md` groups its checks into **families** (for example: traceability, authority, gaps-and-issues, boundary-leakage). One finder per family, run in parallel. Each finder receives only: the artifact, the sources, the inputs above, and *its family's* checks. It does not see the producing conversation, the other families, or the other finders' output.

Finders are narrow and adversarial. The traceability finder does not "review"; it fills a table — one row per statement, columns `statement | source quote | none` — and every `none` row is a candidate finding. The authority finder lists every action the artifact grants and, for each, the §3 span or `none`. A finder that returns prose instead of its table is re-run. This shape matters because the main failure these checks exist for — filling gaps with plausible defaults — is a habit the finder's model shares with the author; a finder asked "does this look right?" will under-report it, a finder asked "where is the span?" cannot.

Where the workflow has a second model family available (the `codex-rescue` route in the pointers pipeline is the existing example), the traceability and gaps families run on it. Same-model finders are acceptable for structural families.

### Stage 3 — Verifier (fresh context, 1)

Receives the artifact, sources, and the merged candidate list. For each candidate it runs:

- (a) artifact quote exists verbatim — **scripted**, `verify_generic.py findings`;
- (b) source quote exists verbatim, or the `none` claim holds after a search of the sources — **scripted** for existence; the model only judges `none` claims that the script could not disprove;
- (c) the quoted evidence supports the stated failure — model judgment.

Any check fails → dropped, with the reason logged. Duplicates across finders merged. Then the **Nit cap** from `VERIFY.md` is applied to the merged, verified list — not per finder — keeping the Nits with the strongest evidence.

### Stage 4 — Report

Write `verification-report.md` beside the artifact from `assets/verification-report.template.md`. Severity is whatever `VERIFY.md` assigns the check; unlisted but verified problems default to Nit. Pre-existing findings and rule-3 gaps are listed in the report's **Open truths for the owner** block, one line each: unresolved truth · evidence span · who decides. The verifier writes only `verification-report.md`; the producing skill repeats those lines in its reply and makes sure each has an open marker in the artifact.

### Stage 5 — Resolution (no self-approval)

For every **Important**, exactly three outcomes exist:

1. **Fixed** — the artifact changed; the next verification run confirms the finding no longer reproduces.
2. **Refuted** — the producing skill supplies a verbatim source span the finder missed, at a stated location. The script confirms the span exists; the verifier confirms it supports the statement. Only then is the finding closed as refuted.
3. **Owner-resolved** — the accountable human owner closes it with a reason, recorded in the report with their name. This is the owner deciding; it is not available to the producing agent.

There is no "resolved with a one-line reason" by the author. A finding the author disagrees with and cannot refute with a span stays **open**, and open Importants block confirmation. Nits may be left open.

Verification is closed when no Important is open. This is Lifecycle Policy 7(a); owner confirmation (7(b)) follows and is not part of this skill.

## Smoke test after changing a VERIFY.md

Each `VERIFY.md` folder may hold `fixtures/planted/`: two or three copies of a known-good artifact with one defect planted per copy, each named for the check it should trigger (`PS-1-over-admission.md`). After editing a `VERIFY.md` or this skill, run verification on each fixture once and confirm the named check fires. This is not an eval program; it answers one question — does the signal still detect the thing it was built for — and is run by hand when the standard changes.

## What this skill is not

- Not a runtime judge. It verifies artifacts at authoring time. Runtime judgment of agent responses belongs to the evaluation implementation.
- Not a style reviewer. Wording is a Nit at most, and only if `VERIFY.md` lists it.
- Not an escalation path. It reports open truths; classification (DROP / DEFER / RESOLVE NOW) stays with Decision Management.

## Voting

Not used. Mandatory quoted evidence plus scripted quote-existence is the false-positive control. Add a second verifier only if the owner-overturn rate in verification reports says so.
