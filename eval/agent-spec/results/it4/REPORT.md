# agent-spec: make the verifier's rulings stable across rounds for the same defect   (it4, 2026-11-11)

Change: 0862313, a277cec and 6c52278 on branch `claude/verifier-ruling-stability-4811l2`. They add one bullet to the adversarial verifier brief in `references/verification.md`: a refutation by a clause or a quoted line must answer the case the finding names, and all of it. A clause that answers only part of a finding leaves it Real, and the verifier's line says which part stands.

Verdict: **NOT RUN.** No trial ran, so there is no grade. The three trial runners were subagents of this session, and subagents here have no Agent tool. They could not dispatch the finders and verifiers that step 4 needs, and each stopped before round 1.

Hypothesis (advisor): dropped_real ≤ 1 in every trial and ≤ 1 summed over the three trials (it2: 0 / 1 / 0). No defect is dropped in one round and kept in a later one (it2 had one such defect, in it2-2). recall_key stays at 1.0, false_positives at 0, and wall_clock_s within 2625 s (it2's worst, 2386 s, + 10 %).

The diagnosis behind the edit, from the advisor reading results/it2-* and it3-*:
- **Every recorded flip went drop then keep.** There are three: it2-2 R1-10 → R2-04, it3-3 R1-12 → R2-10 and it3-3 R2-06 → R3-01. The dropped_real judge ruled the dropped finding Real each time. So the first ruling was wrong, and re-reports corrected it.
- **The wrong first drops share a cause.** The quoted clause answered a neighboring case, not the case the finding named. In it2-2 R1-10, the packet supports the three values, but no input defines the field. The re-report won only because its Evidence pre-empted that clause.
- **Findings dropped in two rounds were ruled Not real by the judge in all three it2-2 cases.** So pinning a later ruling to the earlier one would have kept R1-10's defect unfixed.

## Grade table

None for it4. Baseline rows (`grade.py eval/agent-spec`; * = gated):

| trial | *integrity | *recall_key | *false_positives | *dropped_real | *wall_clock_s | *finder_tool_calls_max | cost_usd | kept_total |
|---|---|---|---|---|---|---|---|---|
| it2-1 | pass | 1.0 | 0 | 0 | 1992 | 14 | 7.35 | 26 |
| it2-2 | pass | 1.0 | 0 | 1 | 2193 | 11 | 7.67 | 26 |
| it2-3 | pass | 1.0 | 0 | 0 | 2386 | 13 | 8.11 | 34 |
| baseline worst (full) | | 1.0 | 0 | 1 | 2386 | 19 | 8.11 | |

## Done
- The advisor proposed the edit. The skill-editor applied it as 0862313; `uv run pytest .claude/skills/agent-spec/tests` gave 56 passed.
- **Flags, round 1:** the editor raised 5 flags. The advisor fixed 3 of them in one follow-up, a277cec, which reworded the bullet's last sentence and changed "neighbouring" to "neighboring". It ruled the other 2 intended: the partial clause belongs in the line's "why you could not refute it" field, and SKILL.md 4.4's "agree it refutes the finding" already blocks a drop.
- **Flags, round 2:** the editor raised 3 flags. The advisor fixed all 3 in 6c52278, which scoped the bullet to the first two routes, used "your line for that finding" and covered "clause, line, scenario or input". 56 tests passed.
- **Trials:** three runners (it4-1, it4-2, it4-3) were dispatched in parallel at effort high on the session model (opus). All three returned within 40 s without starting round 1, each reporting that no Agent tool was available. it4-2 did the setup copies and one step-4.1 checker run in `run-it4-2/`, which is git-ignored scratch. No `results/it4-k/` folder exists, so nothing can be graded by mistake.
- The E8 entry in `EXPERIMENTS.md` is marked "not trialed". The skill commits, this report and E8 are pushed to the branch.

## Decided for you
- **Set name:** it4, one more than it3, the highest existing set. **Branch:** `claude/verifier-ruling-stability-4811l2`, the branch this cloud session must use, not `iterate/agent-spec/it4`. It was cut from 6c345b6.
- **Pushed the branch.** The /iterate instructions treat a push as case 3. I pushed anyway, because this session's git rules and its stop hook require it and the container is ephemeral, so unpushed work would be lost. Nothing was merged.
- **Editor flags left after round 2:** bullets 1–3 don't name their scope the way bullet 4 now does, and a scenario-based refutation isn't assigned to either route. The advisor ruled in advance that the text stands: both are stylistic, and a third rewording would not change what the verifier does. No fix was applied for either.
- **Runner effort:** each runner was dispatched with `effort: high` to match the baseline's recorded `effort`, because I could not read this session's `/effort`. `CLAUDE_CODE_EFFORT_LEVEL` is unset.
- **Scratch layout:** the per-trial prompts are in the session scratchpad. Each run's scratch dir was to be `eval/agent-spec/run-it4-k/`, which is git-ignored.
- **No fallback machinery.** I did not run the trials as `claude -p` processes, as child cloud sessions, or with the main thread as runner:
  - `claude -p` processes are E5's it1 mistake: results that are not comparable with the baseline.
  - Child cloud sessions would each push their own branch, which is case 3.
  - With the main thread as runner, I could not confirm its effort level matches the baseline.

## Needs you
1. **How should the it4 trials run?** In this cloud session a subagent cannot start subagents, so `/trial` cannot work as written: its runners are subagents, and each must dispatch 12 finders and verifiers. Options:
   - (a) **Recommended:** rerun `/trial agent-spec it4 --n 3` on branch `claude/verifier-ruling-stability-4811l2` from a session where runners can dispatch subagents. That is where it2 and it3 ran (a local Claude Code session at effort high on opus), so the trials stay comparable with the baseline. Then run `/grade agent-spec --set it4` and ask the advisor for the verdict.
   - (b) Allow the main thread of a cloud session to be the runner, one trial per session at effort high. This works here, but it is a change of trial machinery and needs a note on every trial.
   - (c) Allow child cloud sessions as runners, each pushing a branch `claude/verifier-ruling-stability-4811l2-it4-k`. This needs your approval for the pushes and the credits.
2. **After the trials: merge, revert or next problem?** Branch `claude/verifier-ruling-stability-4811l2`. There is nothing to decide until the set is graded. Do not merge before then.
3. **The advisor's measurement suggestions** need a separate measurement commit (rule 5), not part of this iteration:
   - (a) **Recommended:** keep `judge-verifier-brief.md` frozen for it4, so the judges stay independent of the skill under test.
   - (b) **Recommended:** add a report-only count of defects dropped in one round and kept in a later round of the same trial. That is the behavior this problem names, and no metric counts it. The alternative is for the advisor to count it by hand in each verdict.
   - (c) **Recommended:** change nothing in the judges now, but treat a one-finding miss on false_positives or dropped_real as INCONCLUSIVE rather than FAIL. The judges have ruled the same CO-S11 defect Real in one trial and Not real in three others, depending on whether the run kept or dropped it.
