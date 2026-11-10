---
name: skill-iterate
description: Improve a Claude Code skill against a graded baseline. Use when changing a skill's instructions, scripts or briefs and the change must be shown not to regress; sets up the eval harness, runs trials, grades them, and keeps the human to the decisions only a human can make.
---

# skill-iterate

A process for changing a skill without guessing whether the change helped. It applies to any
skill in this repo. Each managed skill has an `eval/<skill>/` folder with frozen inputs, a run
prompt, a grading config and a baseline; every change is three trials, graded, against three
baseline trials.

## Rules

1. One change per iteration. No second change until the first has three graded trials.
2. Evidence is the grade table from `scripts/grade.py`, worst value across the trials of a set,
   against the worst baseline value. Count lines, wall clock alone and "fewer findings" are not
   evidence.
3. A reference citation (a book chapter, an article) is a reason to try a change, never evidence
   that it worked.
4. A change is kept only when no gated metric fails in any trial of its set. A change that
   cannot be graded is not made.
5. The measurement and the thing measured never change in the same iteration. Skill text and
   its scripts in one iteration; `grading.json`, the key, thresholds, frozen inputs or baseline
   folders in another, with the human.
6. Every iteration ends with one `REPORT.md`: *Done*, *Decided for you*, *Needs you*.
7. Trials run on the same machinery as their baseline: same subagent mechanism, same model.
   A cloud session without native subagents can run the advisor and editor steps, not trials.

## Commands

- `/setup-eval <skill>` — scaffold `eval/<skill>/`, collect the frozen inputs and run prompt,
  write `grading.json`, run the current skill three times for the baseline, grade.
- `/trial <skill> <set> [--n 3]` — run n trials in parallel in isolated scratch dirs, each
  writing `results/<set>-k/trial.json`, then grade the set.
- `/grade <skill> [--set <set>]` — run `grade.py`; dispatch a judge for every pending judge
  metric; rerun `grade.py`; print the table.
- `/iterate <skill> "<problem>"` — advisor proposes an edit → editor applies it on a branch →
  advisor answers the editor's consistency flags (two rounds at most, then the human) →
  `/trial` → `/grade` → advisor's verdict → `REPORT.md`. One human touch: the merge /
  revert / next-problem question at the end.

## What the human decides

Read `references/escalation.md`. In short: the measurement, the experiment's direction when the
table is inconclusive, anything outside the repo, and anything that loses results. Everything
else the agent decides and logs under *Decided for you*.

## Installing in a repo

Claude Code loads project slash commands from `.claude/commands/` and subagents from
`.claude/agents/`, not from inside a skill folder. Link them (the skill folder stays the
source):

```
ln -s ../skills/skill-iterate/commands/{setup-eval,trial,grade,iterate}.md .claude/commands/
ln -s ../skills/skill-iterate/agents/judge.md   .claude/agents/skill-eval-judge.md
ln -s ../skills/skill-iterate/agents/advisor.md .claude/agents/skill-advisor.md
ln -s ../skills/skill-iterate/agents/editor.md  .claude/agents/skill-editor.md
```

Commands load at session start; open a new session after linking.

## Files

- `scripts/grade.py` — code metrics, judge-task emission, verdict ingestion, the table, the gate.
- `scripts/legacy_extract.py` — one-off: builds `trial.json` from a results folder written by
  hand before the schema existed. New trials write `trial.json` directly.
- `agents/advisor.md`, `agents/editor.md`, `agents/judge.md` — the three subagents.
- `references/escalation.md`, `references/trial-schema.md`, `references/grading-schema.md`,
  `references/report-template.md`.

## Context the agents read

`DECISIONS.md` at the repo root (direction, ownership, boundaries), `eval/<skill>/EXPERIMENTS.md`
(what was tried and what the table said), the skill's own files, and whatever `DECISIONS.md`
lists under references. The advisor retrieves from references by search, not by reading them
whole.
