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
| `run/` | Created by a run. Deleted before the next one. |
| `results/<label>/` | One directory per run, written at the end of the run. |

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

For each `results/<label>/`:

| Metric | Source | Pass |
|---|---|---|
| Finder tool calls | `subagent-stats.md`, round 2+ finders | each ≤ 6 |
| Finder wall clock | same | each ≤ 60% of the baseline finder's duration |
| Recall of known Important defects | compare `round2-findings.md` to `baseline/round2-findings.md`: N1, N2, N9, N10 | ≥ 3 of 4 reported (same block, same defect) |
| False positives | new findings not in the baseline list that you judge Not real after reading | ≤ 1 |
| Context-block misses | findings reported only as a one-line Pre-existing that are in fact in-scope defects | 0 |
| Pipeline integrity | `run.log`: no script error, checker printed 0 errors, rounds ran without a question to the user | all three |

A threshold must pass in every `new-*` trial, not on average. Read the findings yourself for
recall and false positives before trusting any agent to grade them.
