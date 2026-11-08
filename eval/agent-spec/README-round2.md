# Round-2-only trials

Why: round-1 fixes differ from run to run (13 findings fixed in the original run, 24 in baseline-2),
so two full trials never review the same text in round 2. The diff-only change affects round 2+,
so it is tested from a frozen round-1 state.

Frozen inputs: round0-agent-spec.md (before round 1), round1-agent-spec.md (after the original
run's round-1 fixes), round1-answered.md (the original run's M1–M13, answered). The original
run's round 2 on exactly these inputs produced baseline/round2-findings.md (N1–N13).

Trials, with PROMPT-round2.md:
1. `r2-old-1` — before the skill change. Second old-skill sample on the frozen round-1 state.
2. Apply the change, commit.
3. `r2-new-1`, `r2-new-2`, `r2-new-3`.

Grading key: the Important findings of baseline/round2-findings.md (N1, N2, N9, N10) plus the
Important findings of r2-old-1. For each trial, count how many of the key it reports (same block,
same defect). Pass: the new trials' lowest recall is not below the lower of the two old-skill
recalls. Plus the speed, false-positive, context-block and integrity checks from README.md.
