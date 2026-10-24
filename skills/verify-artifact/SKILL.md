---
name: verify-artifact
description: Verify a phase artifact (product-sense.md, agent_spec.md, architecture-notes.md, BDD test files) against its producing skill's VERIFY.md before the owner confirms it. Use when a phase skill finishes a draft or a scoped update, or after a VERIFY.md changes. Not for judging agent behavior at runtime.
argument-hint: <artifact path> <VERIFY.md path> [--prior <previous artifact version> --scope <sections>]
---

# /verify-artifact

Verify one artifact against one standard. This skill owns **how** verification runs. The producing skill owns **what failure looks like**: its `VERIFY.md` (the standard), its `scripts/verify_mechanical.py` (the D-checks, built on `scripts/verify_lib.py` here), and its `fixtures/planted/` (smoke fixtures), all beside its `SKILL.md`. Check exactly what `VERIFY.md` and the four cross-artifact rules below list.

Verification is the producing agent's **loop**: produce, verify, fix, re-verify. Its signal comes from scripts and spans wherever possible, because the failure it hunts, filling a gap with a plausible default, is a habit the verifying model shares with the author. Three things follow. Scripts run first, and finders start only when the scripts pass. Finders fill tables that ask "where is the span?". The author has no way to close a finding by saying it is fine.

## Terms

- **Span**: a verbatim quote from a file, with its location. Spans are the only evidence. "Verbatim" ignores whitespace and curly versus straight quotes, and nothing else.
- **Open truth**: a fact the sources do not settle.
- **Commitment**: a behavior recorded in an authoritative artifact, or the confirmed phase objective. Commitments decide whether a missing fact needs an open marker or an OMIT statement.
- **Open marker**: the sentence the artifact writes where an open truth's value would go, for example "unresolved and deliberately not stated". Each `VERIFY.md` defines its markers.
- **OMIT statement**: the sentence an artifact may write for a fact the sources do not settle and no commitment needs, for example "No hold window is established by the authoritative inputs". It is complete as written: it is not an open marker, and nobody answers it. A `VERIFY.md` that defines none allows none.
- **Status header**: the artifact's `Status:` line. `Status: Draft — N open` means N open markers remain. `Status: Confirmed` requires zero.

## Inputs

All are required. If one is missing, the report says `Inputs status: incomplete` and the run cannot report a pass. A verifier missing an input returns silence, and the loop reads silence as a pass.

- The artifact.
- Its `VERIFY.md`.
- The authoritative sources `VERIFY.md` names.
- The confirmed phase objective and the commitments recorded in authoritative artifacts. Rule 3 needs them to tell a gap that must stay open from one that can be omitted.
- On a scoped update, `--prior` (the previous version) and the declared changed scope. Rule 2 needs both.

## Four cross-artifact rules

Checked in every run, on top of `VERIFY.md`. A violation is Important unless the rule says otherwise.

1. **Traceability.** Every statement points at a source: a rule ID, a span from an authoritative input, or an existing fact in an upstream artifact. `VERIFY.md` defines "statement" and "source" for its artifact.
2. **Write scope.** Only the files and sections the producing skill declares writable changed. On a scoped update, only the declared scope differs from `--prior`.
3. **Gaps stay open.** Where the sources are silent, the artifact carries an open marker or an OMIT statement, never a decision. An authored decision with no source is Important. If a commitment needs the value, the fix replaces it with an open marker, and the verifier writes the open-truth line the author should have reported. If no commitment needs it, the fix replaces it with the OMIT statement `VERIFY.md` defines, and nothing is reported. A problem in the source itself (two sources contradict, or one is ambiguous) is Pre-existing.
4. **Done-when needs evidence.** A claim that a check ran ("tests pass", "validated") comes with the output that shows it.

## Severity

| Severity | Assigned to | Effect |
|---|---|---|
| Important | Any Stage 1 failure, any check `VERIFY.md` marks Important, any violation of the four rules | Blocks gate 1 while open |
| Nit | Checks `VERIFY.md` marks Nit, and verified problems no check lists. A wording problem counts only when `VERIFY.md` lists it | Never blocks. Capped by `VERIFY.md`'s Nit cap |
| Pre-existing | A real problem in an upstream source | Not counted against this artifact. Reported as an open truth for the upstream owner |

## Procedure

### Stage 1: scripts

Run, in order:

1. The command on the `mechanical:` line of `VERIFY.md`: the producing skill's D-checks (structure, IDs, citation spans).
2. `scripts/verify_generic.py status`: the status header matches the open-marker count.
3. On a scoped update, `scripts/verify_generic.py write-scope`: only the declared scope changed.

`verify_generic.py --help` lists the flags. Each failure is an Important with its exact location, written to the report before any model runs. The producing skill fixes and reruns Stage 1.

Stage 1 is done when every script exits 0. Only then does Stage 2 start, so model effort goes only to artifacts that already have the right shape.

### Stage 2: finders

Run one finder per family `VERIFY.md` defines, in parallel, each in a fresh context (a subagent). A finder receives only the artifact, the sources, the inputs, and its own family's checks. The producing conversation and the other families stay out of its context.

Each finder fills its family's table from `VERIFY.md`. The traceability finder writes one row per statement, `statement | source span | none`, and every `none` row is a candidate finding. An authority finder lists every action the artifact grants, each with its span or `none`. In a table, a missing span shows as an empty cell. A request to "review" invites the same plausible-default judgment the author made. If a finder returns prose instead of its table, re-run it.

When a second model family is available (the `codex-rescue` subagent), run the traceability and gaps families on it. Structural families may run on the same model as the author.

Stage 2 is done when every family has returned its table.

### Stage 3: verifier

One fresh-context verifier receives the artifact, the sources, and the merged candidates. Each candidate passes three checks in order:

- (a) The artifact span exists. Scripted: `verify_generic.py findings`.
- (b) The source span exists, or the `none` claim holds after searching the sources. Scripted for existence. The model judges only the `none` claims the script cannot disprove.
- (c) The span supports the stated failure. Model judgment.

Drop a candidate at its first failed check and log the reason. Merge duplicates across finders. Then apply the Nit cap once to the merged list, keeping the Nits with the strongest evidence.

Stage 3 is done when every candidate is either kept with all three checks passed or dropped with a logged reason.

Mandatory spans plus scripted span checks are the false-positive control, so one verifier is enough. Add a second only if the owner-overturn rate in reports calls for it.

### Stage 4: report

Write `verification-report.md` beside the artifact from `assets/verification-report.template.md`. It is the only file the verifier writes. Pre-existing findings and rule-3 gaps fixed with an open marker go in the **Open truths for the owner** block, one line each: unresolved truth · evidence span · who decides. The producing skill repeats those lines in its reply and makes sure each has an open marker in the artifact.

Stage 4 is done when every template section is filled, including `Inputs status`.

### Stage 5: resolution

Each Important closes in exactly one of three ways:

1. **Fixed**: the artifact changed, and the next run no longer reproduces the finding.
2. **Refuted**: the producing skill supplies a source span the finder missed, with its location. The script confirms the span exists, then the verifier confirms it supports the statement.
3. **Owner-resolved**: the accountable human owner closes it with a reason, recorded in the report with their name. This outcome belongs to the owner alone.

An Important the author disagrees with but cannot refute with a span stays open. Nits may stay open.

Stage 5 is done when no Important is open. That closes gate 1.

## The two gates

An artifact becomes authoritative for downstream phases when two gates close, in order:

1. **Verification closed**: this skill ran against the producing skill's `VERIFY.md`, inputs were complete, and no Important is open. This skill's run ends here.
2. **Owner confirmation**: the owner confirms after seeing the closed report, and only when the artifact has zero open markers. Before confirming, the owner settles every open truth by answering, deferring, or dropping it, as the producing skill defines. An answer goes into the producing skill's sources (for Product Sense, verbatim and dated, in the `## Clarifications` section of `product-idea.md`). The producing skill reruns the affected sections, and verification reruns on that scope. At zero open markers the producing skill sets `Status: Confirmed`, and `verify_generic.py status` rejects `Confirmed` while any marker remains.

Until both gates close, the artifact is a draft. Downstream phases may read it to prepare, but a truth they take from it is unconfirmed. A scoped update reopens both gates for the changed scope only.

## After changing a VERIFY.md: smoke test

`fixtures/planted/` beside a `VERIFY.md` holds two or three copies of a known-good artifact, each with one planted defect and named for the check it should trigger (`PS-1-over-admission.md`). After editing a `VERIFY.md` or this skill, run verification on each fixture once and confirm the named check fires. This answers one question, whether the signal still detects what it was built for, and is run by hand.
