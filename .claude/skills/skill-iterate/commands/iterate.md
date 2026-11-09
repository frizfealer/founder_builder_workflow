---
description: One graded iteration on a skill — advisor proposes, editor applies on a branch, trials run, grade, REPORT.md; asks the human once, at the end
argument-hint: <skill> "<problem statement>" [--set <set>] [--n 3]
---

Run one iteration of `skill-iterate` on skill `$ARGUMENTS`. Read
`.claude/skills/skill-iterate/SKILL.md` and `references/escalation.md` first. The human is
not watching; everything they must read goes in `REPORT.md`, and the run stops mid-way only
for escalation cases 3 and 4.

Preconditions, checked before anything else; any failure ends the run with a one-line reason:
- `eval/<skill>/grading.json` names at least three baseline labels for the kind this
  iteration will run, each with a `trial.json` and complete judge verdicts.
- The skill's working tree is clean and `eval/<skill>/EXPERIMENTS.md` has no entry whose
  trials are ungraded (rule 1: one change at a time).
- The problem statement names a metric in `grading.json` that should move.

Set defaults: `--set` = `it<N>` where N is one more than the highest `it*` set in
`results/`; `--n` = 3. The branch is `iterate/<skill>/<set>`.

## 1. Propose

Dispatch `skill-advisor` with: the problem statement; the latest grade table
(`grade.py eval/<skill>`); the paths of `DECISIONS.md`, `eval/<skill>/EXPERIMENTS.md`,
`eval/<skill>/grading.json`, the skill folder, and the results folders the problem refers to.
It returns one edit prompt (file, paragraph, replacement text, hypothesis naming the metric,
what must not change, commit message). If it returns a measurement change or says the idea
was already tried and failed, write that under *Needs you* and stop.

## 2. Apply

Dispatch `skill-editor` with the edit prompt and the branch name. It applies the edit
exactly, runs the skill's checks, commits, and returns the commit and its inconsistency list.

## 3. Resolve flags

If the list is non-empty, send it to the advisor; it returns follow-up edits or "intended,
because …" per flag. Dispatch the editor again with the follow-ups. Two rounds at most. Flags
still open after round two go under *Needs you*; the iteration continues with them noted,
because an open wording flag does not block a trial.

## 4. Trial

`/trial <skill> <set> --n <n>` on the branch. Reruns on infrastructure failure follow
`/trial`'s own rule.

## 5. Grade

`/grade <skill> --set <set>`. All judge cells must hold numbers before step 6.

## 6. Verdict

Send the advisor the set summary and the baseline rows. It returns the verdict line:
PASS, FAIL or INCONCLUSIVE, naming the deciding metric with its worst value against the
baseline worst, plus the hypothesis check: did the named metric move the predicted way in
every trial?

## 7. Record

- `eval/<skill>/results/<set>/REPORT.md` per `references/report-template.md`. *Needs you*
  always ends with the merge / revert / next-problem question and the branch name.
- Append an entry to `eval/<skill>/EXPERIMENTS.md`: hypothesis, change (commit), trials,
  grade table rows, verdict. Commit `results/<set>/` and `EXPERIMENTS.md` on the branch.
- Log under *Decided for you* every choice not in the instructions: set name, scratch layout,
  how a stalled subagent was handled, which flag answers were "intended".

Never: edit the skill yourself (the editor does); edit `grading.json`, the key, frozen inputs,
baseline folders or `grade.py` (case 1); push, kill processes outside the trials, or delete
results (cases 3–4); merge the branch (the human's question).

Report in one message: the verdict line, the set's worst values against the baseline, the
branch, and the path of `REPORT.md`.
