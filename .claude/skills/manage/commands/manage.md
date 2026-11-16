---
description: One manager run over the task list — take Ready tasks one at a time, build, verify, merge or park; report at the end
argument-hint: "[--dry-run]"
---

Run the task list. Read `.claude/skills/manage/SKILL.md` first; its rules, park list and never
list apply to every step. The owner is not watching: never ask him anything during the run.
What needs him is parked, and goes in the report. `S` below is `.claude/skills/manage`.

With `--dry-run`: run `python3 S/scripts/tasks.py lint`, `python3 S/scripts/checks.py
merge-limit` and `python3 S/scripts/tasks.py next`, print their output, and stop. Change
nothing: no branch, no marker, no file.

## 1. Start

On the working branch, with no uncommitted changes to tracked files. Run `tasks.py lint` and
`checks.py merge-limit`; if either fails, end the run with its output as the one-line reason.
Then `checks.py run-start`; if it fails, end the run the same way.

## 2. Take

`tasks.py next`. If it prints no task, or `merge-limit` now fails, go to step 9.

## 3. Branch

Cut `task/<id>` from the working branch (an iterate task uses the branch `/iterate` names,
cut from the working branch). If that name exists from an earlier run, add `-2`, `-3`. On the
branch, set the task to In progress and commit `task <id>: in progress`.

## 4. Work, by `runs_as`

- **build**, **measurement:** dispatch `manager-builder` with a complete brief: the task file's
  path and its `done_means` and `may_edit` quoted; the branch; the paths involved; the earlier
  branch of this task if one exists; `DECISIONS.md` as the direction. It commits on the branch
  and returns what it changed, the check it wrote or ran for `done_means`, its decisions and
  any Proposed tasks.
- **iterate:** follow `.claude/commands/iterate.md` for the skill the task names, with the
  task's problem. Its preconditions and stop list apply. The standing merge / revert question
  in its *Needs you* is answered here: keep the result only when its report says no gated
  metric failed in any trial; otherwise park with the report as the question (rule 4 of
  skill-iterate: inconclusive is a revert). Any other item under its *Needs you* parks the task.
- **you:** prepare what the owner needs to decide or do (the files to read, the options, a
  recommendation), commit it on the branch, and park.

## 5. Verify, by `verified_by`

Never by the builder. An empty or failed review is a fail, and so is a reply whose first line
is not `VERDICT: PASS`.

- **reviewer**, **script:** dispatch `manager-reviewer` with the task file's path and the
  output of `git diff <working branch>...task/<id>`. Not the builder's report. Tell it to look
  for what is wrong. For `script`, it names the commands that prove `done_means`; run exactly
  those yourself, and every one must exit 0.
- **metrics:** `python3 .claude/skills/skill-iterate/scripts/grade.py eval/<skill> --set <set>
  --gate` exits 0.
- **you:** park.

On a fail: one fresh retry. Dispatch a new `manager-builder` with the reviewer's findings, then
a new `manager-reviewer`. If it still fails, park.

## 6. Protected paths

`checks.py protected <id> <branch>`. A failure parks the task.

## 7. Merge

`checks.py merge-limit`; at the limit park the task with "merge limit reached; review and set
a review tag". Otherwise, on the working branch: `git merge --no-ff --no-commit <branch>`, set
the task file's `status` to Done, `finished` to today, `tokens`, and `decided_for_you`, then
commit with the subject `Merge task <id>: <title>`. Go to step 2.

## 8. Park

On the working branch, edit only this task's file: `status` Needs you, `needs_you`,
`decided_for_you`, `tokens`. Commit `task <id>: parked`. The task's branch stays. Go to step 2.

## 9. End

`checks.py run-end`. Prepend this run to `tasks/RUNS.md` and commit it on the working branch as
`manage: run report <date>`:

```markdown
## Run <date> <time>

Stopped because: <no task to take | merge limit | start check failed: ...>.

### Done
- task <id>: <title>; merge <hash>; tokens <agents> (main session: not recorded)

### Decided for you
- task <id>: chose <x> over <y>; would change if <z>

### Needs you
- task <id> (parked): <question>. Recommended: <answer>. If you veto: <what changes>.
- task <id> (Proposed): <title>. <why>.
```

Tokens: add up `subagent_tokens` from every agent result on the task, including judges and
trials inside an iterate task.

Report in one message: tasks merged, tasks parked, Proposed tasks, and the path of `tasks/RUNS.md`.
