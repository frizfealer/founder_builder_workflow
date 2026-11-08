# Verify-only test for the agent-spec skill

Tests step 4 (Verify) of `.claude/skills/agent-spec/SKILL.md` on frozen inputs, so that a
change to the verification process can be compared before and after.

## Files

| File | What it is |
|---|---|
| `round0-agent-spec.md` | The order-support spec as it was before any verification round (1,544 lines). Never edited; each run copies it. |
| `review-packet.md` | The step-4.2 packet from the original run: input ledger, interview verbatim, confirmed tool set. Paths point at `run/agent-spec.md` and `product-idea.md` in this directory. |
| `product-idea.md` | The one source document the packet lists. |
| `baseline/round{1,2,3}-findings.md` | The merged findings the original run produced in each round (M1–M13, N1–N13, P1–P9). Used to grade recall. |
| `baseline/subagent-stats.md` | Token, tool-use and duration figures per subagent from the original run. |
| `grading.json` | Metrics, gates, key defects and judge context for `skill-iterate/scripts/grade.py`. Changing it is a human decision. |
| `EXPERIMENTS.md` | One entry per skill change: hypothesis, trials, grade, outcome. |
| `run-<label>/` | Scratch for one trial (gitignored). Parallel trials never share one. |
| `results/<label>/` | One directory per trial, written at the end of the run. Must include `trial.json` (see `skill-iterate/references/trial-schema.md`); the seven folders from before the schema were converted with `legacy_extract.py`. `baseline-1/` is the original run, reconstructed from `baseline/`. |
| `results/<label>/judge/` | Judge task files written by `grade.py` and the verdict JSON a judge writes back. |

If the repo is not at `/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow`,
replace that prefix in `review-packet.md` first.

## Running one trial

Paste `PROMPT.md` into Claude Code from the repo root, with `<label>` filled in
(`baseline-2`, `new-1`, `new-2`, `new-3`, `cafe-1`).

Order of trials:

1. `baseline-2` — before applying the skill change. Gives a second baseline sample so run-to-run variance is known.
2. Apply the change (script, briefs, SKILL.md edits). Commit.
3. `new-1`, `new-2`, `new-3` — three trials of the new skill on the same inputs.
4. `cafe-1` — the new skill on `examples/cafe_reservation_agent/agent-spec.md` (no packet exists for it; let the run write one from the example's own inputs). Checks the bundle script on a second spec.

## Grading a trial

Run `/grade agent-spec --set <set>` (or `python3 .claude/skills/skill-iterate/scripts/grade.py eval/agent-spec --set <set>` for the code metrics alone). The table below is what `grading.json` encodes; the gated metrics are:

| Metric | Source | Pass |
|---|---|---|
| Finder tool calls | `subagent-stats.md`, round 2+ finders | each ≤ 6 |
| Finder wall clock | same | each ≤ 60% of the baseline finder's duration |
| Recall of known Important defects | compare `round2-findings.md` to `baseline/round2-findings.md`: N1, N2, N9, N10 | ≥ 3 of 4 reported (same block, same defect) |
| False positives | new findings not in the baseline list that you judge Not real after reading | ≤ 1 |
| Context-block misses | findings reported only as a one-line Pre-existing that are in fact in-scope defects | 0 |
| Pipeline integrity | `run.log`: no script error, checker printed 0 errors, rounds ran without a question to the user | all three |

A gated metric must pass in every trial of a set, not on average, and must not be worse than
the worst baseline trial by more than 10 %. Recall and false positives are judged by a
fresh-context `skill-eval-judge` subagent from the task files `grade.py` writes; calibrate it
once by grading ~20 findings yourself and comparing, before trusting its verdicts.

Baselines per kind are listed in `grading.json`. As of 2026-11-08 the `full` kind has two
(`baseline-1`, `full-new-3`) and `round2` has one (`r2-old-1`); three per kind is the minimum
for a regression to be told from run-to-run variance.
