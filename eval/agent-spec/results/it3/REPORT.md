# agent-spec: dispatch the step-4.4 verifier on sonnet instead of the inherited model   (it3, 2026-11-11)

Change: 840bee9 on branch `iterate/agent-spec/it3`. Step 4.4 of `SKILL.md` now dispatches the one verifier "on the sonnet model, not the session's model (in Claude Code, the Agent tool's `model: sonnet`)". The finders, the verifier brief and everything else are unchanged.

Verdict: **FAIL** (advisor and `grade.py`). The deciding metric is dropped_real. The set's worst is 3 (it3-1), and the trials are 3 / 2 / 2 against a baseline worst of 1. It fails in every trial. recall_key also fails: 0.86 / 0.86 / 1.0 against 1.0.

Hypothesis check: the quality gates must not be worse than it2's worst (recall_key 1.0, false_positives 0, dropped_real 1) in any trial, and cost_usd and wall_clock_s should fall. **Not met.** Cost and time fell, and all three quality gates were worse.

| metric | predicted | it3-1 | it3-2 | it3-3 | met? |
|---|---|---|---|---|---|
| recall_key | 1.0 | 0.86 | 0.86 | 1.0 | no |
| false_positives (your bar 0; `grade.py` gate 2) | 0 | 1 (Nit) | 1 (Nit) | 1 (Nit) | no on your bar; passes `grade.py`'s gate |
| dropped_real | ≤ 1 | 3 | 2 | 2 | no, all three |
| cost_usd | 6.4–7.2 | 6.74 | 6.74 | 6.69 | yes |
| verifier time, 3 rounds summed (s) | < 581 | 251 | 226 | 184 | yes |
| wall_clock_s | each ≤ 2386, mean < 2190 | 2148 | 2234 | 1877 | yes (mean 2086) |

- **Only one of the two recall misses comes from the edit.** In it3-1 a finder reported key defect M10 (R1-04) and the sonnet verifier dropped it; the dropped_real judge ruled R1-04 Real. In it3-2 no finder reported M10 (recall_found 0.86), and the finders were unchanged on opus.
- **Sonnet dropped the wrong findings, not more of them.** Its drop rate was 0.23 / 0.18 / 0.06, against it2's 0.19 / 0.28 / 0.13. Yet 7 of its drops were ruled Real across the set. it3-3 dropped only 2 findings and both were real.
- **Cost fell 13 %:** mean cost_usd was 6.72 against it2's 7.71, about $1 per trial. The token counts in every row are totals, so cost is tokens × blended rate, comparable with it2.
- **Time fell less than the verifier did.** Verifier time fell about 65 % (mean 220 s against 647 s per run), but mean wall clock fell only about 100 s (2086 against 2190). The trials kept more findings (36 / 32 / 30 against 26 / 26 / 34), and the extra fixes used up most of the saving.

## Grade table

Columns marked * are gated. Units: wall clock and finder duration in seconds; tokens in thousands; cost in USD at grading.json's blended rates.

| trial | *integrity | *recall_key | recall_found | *false_positives | fp_important | fp_nit | *dropped_real | *wall_clock_s | *finder_tool_calls_max | tokens_total_k | cost_usd | kept_total | verifier_drop_rate | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-1 | pass | (excl.) | (excl.) | 2 | 1 | 1 | 0 | 2154 | 19 | 1060 | 5.6 | 33 | 0.0 | baseline |
| it2-1 | pass | 1.0 | 1.0 | 0 | 0 | 0 | 0 | 1992 | 14 | 1393 | 7.35 | 26 | 0.19 | baseline |
| it2-2 | pass | 1.0 | 1.0 | 0 | 0 | 0 | 1 | 2193 | 11 | 1453 | 7.67 | 26 | 0.28 | baseline |
| it2-3 | pass | 1.0 | 1.0 | 0 | 0 | 0 | 0 | 2386 | 13 | 1536 | 8.11 | 34 | 0.13 | baseline |
| **it3-1** | pass | 0.86 | 1.0 | 1 | 0 | 1 | 3 | 2148 | 14 | 1433 | 6.74 | 36 | 0.23 | FAIL: recall_key 0.86 vs 1.0; dropped_real 3 vs 1 |
| **it3-2** | pass | 0.86 | 0.86 | 1 | 0 | 1 | 2 | 2234 | 15 | 1427 | 6.74 | 32 | 0.18 | FAIL: recall_key 0.86 vs 1.0; dropped_real 2 vs 1 |
| **it3-3** | pass | 1.0 | 1.0 | 1 | 0 | 1 | 2 | 1877 | 16 | 1422 | 6.69 | 30 | 0.06 | FAIL: dropped_real 2 vs 1 |
| baseline worst (full) | | 1.0 | | 2 | | | 1 | 2386 | 19 | 1536 | 8.11 | | | |

Set it3 worst value per gated metric, against the baseline worst (`grade.py`: set verdict FAIL, `--gate` exit 1):
- recall_key: 0.86 vs 1.0
- false_positives: 1 vs 2 (it2's worst is 0)
- dropped_real: 3 vs 1
- wall_clock_s: 2234 vs 2386
- finder_tool_calls_max: 16 vs 19

Findings the judges ruled Real after the sonnet verifier dropped them:

| trial | finding | what it is | re-reported and kept later? |
|---|---|---|---|
| it3-1 | R1-04 | key defect M10: an already-cancelled order with a failed or missing refund | no (the recall_key judge found no kept finding for M10) |
| it3-1 | R2-07 | the "never asks which order" dimension does not say whether a yes/no check counts | not checked |
| it3-1 | R2-16 | no guarantee or failure row for a refund with the wrong amount or method | not checked |
| it3-2 | R2-05 | second-timeout branch says "not cancelled" with no handoff, though SG-04 allows a late cancellation | no; the runner listed the branch as an open question |
| it3-2 | R2-10 | CO-S08 step 3 offers a whole-order cancellation the failure row holds back | not checked |
| it3-3 | R1-12 | CO-S11 ties the status change to a call that "gets no answer" | re-reported as R2-10, kept |
| it3-3 | R2-06 | second-timeout branch forbids the staff handoff | re-reported as R3-01, kept |

Per-trial extraction warnings are in each `results/it3-k/trial.json`.

## Done
- The skill-editor applied the advisor's edit verbatim as 840bee9: one sentence in `.claude/skills/agent-spec/SKILL.md` step 4.4. `uv run pytest .claude/skills/agent-spec/tests` gave 56 passed. The editor raised no flags, so step 3 did not run.
- Three trials, it3-1, it3-2 and it3-3, ran in parallel on skill commit 840bee9, session opus at effort high, the same as the baseline. Every finder and verifier was a native subagent, 12 per trial, and every notification arrived. I checked every trial.json by hand: all 9 verifier rows say `sonnet` and all 27 finder rows say `opus`. Each trial ran 3 rounds, stopped at the round cap, and ended with the checker at 0 errors. No rerun was needed.
- Twelve judges ran (4 metrics × 3 trials), and every cell holds a number.
- `results/it3-1..3/`, this report and the E7 entry in `EXPERIMENTS.md` are committed on the branch.

## Decided for you
- **Set name:** it3. The highest `it*` set was it2, and it1 / it1b both count as N = 1. **Branch:** `iterate/agent-spec/it3`, cut from `claude/agent-spec-verification-test-iayxp5` at 267fc2c.
- **Scratch layout:** `eval/agent-spec/run-it3-{1,2,3}/` for the trials, git-ignored and not committed. The per-trial prompts and grade tables are in the session scratchpad. Each runner was told to keep its helper scripts inside its own run dir, which avoided it2-3's scratchpad collision.
- **Runner harness notes:** each runner was told to pass a `model` only where the skill says (the verifier), and to record `sonnet` for verifiers and `opus` for finders in trial.json.
- **it3-2's report.md:** the harness refused the runner's Write call for `report.md` ("Subagents should return findings as text"). The runner returned the text, and I saved it verbatim to `results/it3-2/report.md`. grade.py and the judges do not read that file.
- **it3-2 runner slips** (in its trial.json warnings): two spec edits used plain `python3` / `sed` instead of `uv run`, and it briefly wrote and deleted `/tmp/x` outside the allowed folders. No trial result was affected.
- **Your bar against grade.py's bar:** you set false_positives at it2's worst (0). grade.py's baseline worst is 2, because baseline-1 counts. I did not change `grading.json` (rule 5); the advisor applied both bars in the verdict. The verdict does not depend on this, because dropped_real decides it (Needs you, item 3).
- **Judge disagreement in it3-3:** the false-positive judge ruled R2-10 Not real, and the dropped_real judge ruled R1-12 Real. They are the same CO-S11 defect. Settled either way, it3-3 moves by one in each column, and the set still fails (Needs you, item 4).

## Needs you
1. **Merge or revert `iterate/agent-spec/it3`?** dropped_real failed in all three trials, and it3-1 lost key defect M10 to a verifier drop. Options:
   - (a) **Recommended: revert.** Do not merge 840bee9; delete or keep the branch as you prefer. Keep `results/it3-1..3/` and the E7 entry as history (cherry-pick the results commit onto `claude/agent-spec-verification-test-iayxp5`). The baseline stays it2-1..3.
   - (b) Merge anyway, trading verifier quality for about $1 (13 %) less per trial.
   - (c) Run more trials first. Not recommended: the failure is in all three trials, so more cannot overturn it.
2. **The finders-on-sonnet follow-up.** Your condition was that sonnet is not worse on all three quality gates. It was worse on all three. Options:
   - (a) **Recommended: drop it.** Finding defects is harder than checking them, and recall comes from the finders (recall_found). Sonnet already failed at checking.
   - (b) Try it anyway as a new line of changes.
   - (c) Take the next queued problem instead: the verifier rules the same defect differently across rounds. it3-3's two real drops (R1-12, R2-06) were re-reported and kept in later rounds, which is that pattern again.
3. **The false_positives gate is looser than your bar.** grade.py takes baseline worst false_positives = 2 from baseline-1. grading.json's full-kind description says baseline-1 counts "for cost metrics only", but `baseline_exclude` drops only recall_key and recall_found for it. This set had false positives of 1 / 1 / 1, which passes grade.py and fails your bar. This is a measurement change. Options:
   - (a) **Recommended:** in a separate measurement commit on `claude/agent-spec-verification-test-iayxp5`, add false_positives, fp_important, fp_nit and dropped_real to `baseline_exclude["baseline-1"]`. dropped_real's worst stays 1.
   - (b) Leave grading.json as it is, and the advisor applies your bar in each verdict.
   - (c) Accept the gate of 2.
4. **Two judges disagree on one defect** (it3-3, CO-S11). Options:
   - (a) **Recommended:** record it in E7, as done, and change nothing now.
   - (b) Change the judge rubric so that findings at the same location are judged together across metrics. This is a measurement change, worth making only if the disagreement recurs.
