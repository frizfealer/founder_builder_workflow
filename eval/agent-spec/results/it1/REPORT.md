# agent-spec: adversarial verifier drops M2 by citing the §5.1 supporting-actor clause   (it1, 2026-11-09)

Change: e473b91, 9fddf59, 29e7be1 on branch `iterate/agent-spec/it1`. Adds limits to the adversarial verifier brief (`references/verification.md` line 79):
- A clause that only *permits* a kind of line, such as §5.1's "A supporting actor answers every call normally unless…", does not refute a finding that the line contradicts the scenario's Initial state or the results of earlier calls.
- A verifier may not refute a finding by restating the line the finding quotes.

Verdict: **INCONCLUSIVE** (advisor). The deciding metric is false_positives: the set's worst is 3 (it1-1) against a baseline worst of 2. it1-2 and it1-3 scored 1 each.
- `grade.py` marks the set FAIL. Two trials fail a gate: it1-1 on false_positives, and it1-3 on integrity.
- The advisor discounts the integrity FAIL as a counting artefact (Needs you, item 2).
- Under rule 4 ("kept only when no gated metric fails in any trial"), the change cannot be kept as it stands.

Hypothesis check: recall_key → 1.0 in every trial. **Not met.** The values were 0.86 / 1.0 / 0.86.
- **The M2 mechanism worked.** M2 was matched to a kept finding in 3 of 3 trials. The baselines kept it in 2 of 4: in one the verifier said Real, and in the other the main thread overrode a Not real. In it1-2 the verifier cited the new limit by name.
- **Both misses are M10, and no finder reported it.** recall_found was 0.86 in it1-1 and it1-3; it was 1.0 in all four E4 baselines. A finder miss is outside what this edit changes.

## Grade table

Columns marked * are gated. Units: wall clock and finder duration in seconds; tokens in thousands. recall = share of the 7 key Important defects. false_positives = kept findings the judge ruled Not real or Style only.

| trial | *integrity | *recall_key | recall_found | *false_positives | *wall_clock_s | *finder_tool_calls_max | finder_duration_max_s | tokens_total_k | kept_total | important_kept | verifier_drop_rate | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-1 | pass | (excl.) | (excl.) | 2 | 2154 | 19 | – | 1060 | 33 | 19 | 0.0 | baseline |
| e4-base-1 | pass | 0.86 | 1.0 | 1 | 1877 | 14 | 302 | 1405 | 31 | 15 | 0.23 | baseline |
| e4-base-2 | pass | 1.0 | 1.0 | 1 | 2162 | 13 | 300 | 1446 | 37 | 21 | 0.14 | baseline |
| e4-base-3 | pass | 0.86 | 1.0 | 0 | 2007 | 12 | 307 | 1355 | 25 | 9 | 0.34 | baseline |
| full-new-3 | pass | 1.0 | 1.0 | 0 | 1588 | 11 | 179 | 1633 | 31 | 19 | 0.28 | baseline |
| **it1-1** | pass | 0.86 | 0.86 | **3** | 2309 | 11 | 199 | 1139 | 28 | 16 | 0.18 | FAIL: false_positives 3 vs 2 |
| **it1-2** | pass | 1.0 | 1.0 | 1 | 1424 | 11 | 217 | 3737 | 29 | 17 | 0.26 | PASS |
| **it1-3** | **FAIL** | 0.86 | 0.86 | 1 | 1226 | 11 | 218 | 1111 | 31 | 16 | 0.16 | FAIL: integrity |
| baseline worst (full) | | 0.86 | 1.0 | 2 | 2162 | 19 | 307 | 1633 | 25 | 9 | 0.0 | |

Set it1 worst value per gated metric, against the baseline worst:
- recall_key: 0.86 vs 0.86
- false_positives: 3 vs 2 (fail)
- wall_clock_s: 2309 vs 2162 (+6.8 %, within the 10 % tolerance; it1-1 includes about 18 min lost to a failed first finder dispatch)
- finder_tool_calls_max: 11 vs 19

Notes on false_positives:
- **it1-1's three FPs** are M14 (Not real), M7 (Style only) and P4 (Style only). All three are **Nit findings the skill sends to fix without verification**: their findings files say "Verifier: Nit (not verified)". The verifier edit cannot have kept them. M14 does rest on CO-S24's "order not found" outcome, which round 1 itself found impossible, and it was removed again in round 2 (N10).
- **it1-2's FP** is R2-09: a Forbidden action-count line was wrongly called Untestable.
- **it1-3's FP** is R2-04, which the main thread kept against the verifier's own Not real.

Per-trial extraction warnings are in each `results/it1-k/trial.json`.

## Done
- I did not edit the skill myself. The skill-editor made the changes in `.claude/skills/agent-spec/references/verification.md`, one paragraph, in three commits: e473b91 (the advisor's edit), then 9fddf59 and 29e7be1 (two rounds of flag follow-ups). `check_spec.py` on the café example exits 0. The pytest suite did not run because pytest is not installed.
- Three trials, it1-1, it1-2 and it1-3, ran in parallel on skill commit 29e7be1, each in its own `run-it1-k/` scratch dir. All three ran 3 rounds, stopped at the round cap, and ended with the checker at 0 errors.
- Nine judges (3 metrics × 3 trials) ran; every cell holds a number. The results are committed in 142b118.

## Decided for you
- **Set name:** it1, because no earlier `it*` set existed. **Branch:** `iterate/agent-spec/it1`, cut from `claude/agent-spec-verification-test-iayxp5` at 0a70e72.
- **Scratch layout:** `eval/agent-spec/run-it1-{1,2,3}/`, which is git-ignored and was not committed.
- **Label substitution:** PROMPT.md still reads "Label: baseline-2". Each trial brief overrode the label with it1-k and set `kind: full` and `skill_commit: 29e7be1`.
- **Flag rounds:** round 1 had 3 flags and round 2 had 3 flags. The advisor ruled all six real and gave a fix for each; none was answered "intended". The flags still open after round 2 are listed under Needs you.
- **How trials dispatched subagents:** the trial runners had no Agent tool, so each runner started its finders and verifiers as `claude -p --model claude-opus-5-5` processes limited to Read/Grep/Glob. I accepted this rather than stopping, and the runners recorded it in `trial.json` warnings. Its effect on comparability is under Needs you.
- **it1-3's integrity:** I left its `trial.json` as written (script_errors = 1) rather than recount it; see Needs you.
- **Commit timing:** I committed the trial results (142b118) before REPORT.md was written. I push only after REPORT.md is written, as the session's exception allows.

## Needs you
1. **The editor's flags still open after two rounds.** All are wording issues in line 79 of `verification.md`:
   - (a) The new label "Every refutation above is limited as follows. A refutation must show the finding does not fit its class…" now formally covers Style-only refutations and missing-evidence refutations, and neither argues about class fit.
   - (b) "above" has to reach back past the reference-checklists sentence to find the list it refers to.
   - (c) The first refutation route ("a rule, failure row, §5.1 or §5.2 clause … that already settles the case") still invites the move the limits forbid, before the reader reaches the limits.
   - (d) Line 79 is now one very long line; the rest of the brief wraps at about 100 characters.

   Options: fix them in the next iteration, or accept them as they are. (a) could affect false_positives, because it makes Style-only drops look disallowed.
2. **Integrity counting is inconsistent.** Changing it is a measurement change (escalation case 1). it1-3 counted script_errors = 1 for the runner's own ad-hoc fix script aborting on its assertion, plus one checker call run from the wrong directory. it1-1, it1-2 and e4-base-2 recorded 0 for the same kind of event. No trial had a `check_spec.py` failure. Options:
   - (a) Define script_errors as failures of the skill's own scripts, and re-extract every trial. it1-3 then passes.
   - (b) Count every runner script failure, and re-extract it1-1, it1-2 and e4-base-2. A baseline would then fail.
   - (c) Leave it as it is.
3. **The trials ran on different infrastructure from the baseline.** it1's finders and verifiers ran as `claude -p` processes; the baselines used native subagents. tokens_total_k is not comparable (it1-2 shows 3737k), and finder recall may be affected. M10's absence from two trials is the main unexplained change. Options:
   - (a) Treat it1 as provisional and rerun with the Agent tool available.
   - (b) Accept it1, with a note that cost metrics and recall_found are not comparable to the baseline.
4. **Keep, revert, or try more (escalation case 2).**
   - **Keep:** M2 is fixed in 3 of 3 trials, and recall_key is never below the baseline. None of it1-1's three FPs passed through the verifier. But rule 4 blocks keeping the change while the gate shows FAIL.
   - **Revert:** the false_positives gate failed in one trial, and recall_key did not reach the stated 1.0.
   - **One more trial would settle it:** run it1-4 on native subagents. If M2 is kept, false_positives ≤ 2 and recall_found = 1.0, keep the change.
5. **Merge, revert, or next problem?** The branch is `iterate/agent-spec/it1`. Merge it into `claude/agent-spec-verification-test-iayxp5`, revert the three skill commits, or open the next problem? A candidate next problem: unverified Nit findings account for all of it1-1's FPs.
