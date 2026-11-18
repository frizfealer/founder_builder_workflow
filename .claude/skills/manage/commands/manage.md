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

First `checks.py needs <id>`. If it fails, park the task at once (step 8, reason `needs`) with
its one-line output as the question: no branch, no builder. Then go to step 2.

Cut `task/<id>` from the working branch (an iterate task uses the branch `/iterate` names,
cut from the working branch). If that name exists from an earlier run, add `-2`, `-3`. On the
branch, set the task to In progress and commit `task <id>: in progress`.

## 4. Work, by `runs_as`

- **build**, **measurement:** dispatch `manager-builder` with a complete brief: the task file's
  path and its `done_means` and `may_edit` quoted; the branch; the paths involved; the earlier
  branch of this task if one exists, whose work the builder brings over without any file under
  `tasks/`, so the new branch's task files stay as the working branch has them; the task's
  `for_retry`, when set, quoted in full as faults this run fixes; `DECISIONS.md`
  as the direction. It commits on the branch
  and returns what it changed, the check it wrote or ran for `done_means`, its decisions, a
  Proposed task only when `done_means` needs a protected path outside `may_edit`, and what it
  noticed outside the task. When it stops on a fact about the owner's product or an outside
  system, park (reason `owner-fact`) with its question.
- **iterate:** follow `.claude/commands/iterate.md` for the skill the task names, with the
  task's problem. Its preconditions and stop list apply. The standing merge / revert question
  in its *Needs you* is answered here: keep the result only when its report says no gated
  metric failed in any trial; otherwise park (reason `iterate`) with the report as the question
  (rule 4 of skill-iterate: inconclusive is a revert). Any other item under its *Needs you*
  parks the task, with the same reason.
- **you:** prepare what the owner needs to decide or do (the files to read, the options, a
  recommendation), commit it on the branch, and park (reason `runs-as-you`).

**The builder's decisions (advisor, job c).** After each builder returns, here and in step 5,
read its decisions. For each one that changes what a `done_means` line proves (what the line
measures, its inputs, its threshold, or what counts as a pass), dispatch a fresh
`manager-advisor` for job (c) with the task file's path, the line's number and text quoted, the
decision quoted (chosen, rejected, would change), and `git diff <working branch>...<branch>`.
Tell it to start its reply with `RULING: HOLDS` or `RULING: FAILS`, then `JOB: c (<n>)`. On
`FAILS`, the task goes back to the builder once: a fresh `manager-builder` with the reply quoted,
told to make the line prove what it was written to prove and change nothing else; then this
check again on its decisions. A second `FAILS` on the task parks it (reason `verification`).

## 5. Verify, by `verified_by` and `verifier_of_line`

Never by the builder. Each line of `done_means` is verified by the one verifier
`verifier_of_line` names for it, or else by every verifier in `verified_by`
(`references/task-fields.md`). Run every verifier that has a line, `you` last. An empty or
failed review is a fail, and so is a reply whose first line is not `VERDICT: PASS`, and so is a
reply with any problem labelled blocking. Minor and outside problems never fail it. Keep every reviewer reply verbatim, in order; step 7 or 8 saves
them. From the minor and outside problems and what the builder noticed, add at most one Proposed
task for this task run, bundling the ones worth doing, or none; step 7 or 8 commits it. Give it
`tags`: 1 to 3 lines of `tasks/tags.txt` that fit its title, notes and `may_edit` (`repo` when
none fits).

- **reviewer**, **script:** dispatch `manager-reviewer` with the task file's path and the
  output of `git diff <working branch>...task/<id>`, and the numbers of the lines that are
  neither the reviewer's nor the script's, as lines it does not judge. Not the builder's report.
  Tell it to look for what is wrong. For `script`, it names the commands that prove its lines;
  run exactly those yourself, and every one must exit 0.
- **advisor:** for each line the advisor verifies, dispatch a fresh `manager-advisor` for job
  (a) with the line's number and text quoted and only the paths the line names, on the task's
  branch: not the task file, not the diff, not another reply. When the line names its inputs
  without paths, give the files of the branch that hold them, never a file that holds what the
  line tests them against (for labelling: the transcripts, never the verdicts), and log that
  list under `decided_for_you`. Tell it to start its reply with `RULING: HOLDS` or
  `RULING: FAILS`, then `JOB: a (<n>)`. Any reply that does not start `RULING: HOLDS` is a fail.
  Never give the advisor a line whose verifier is `you`.
- **metrics:** `python3 .claude/skills/skill-iterate/scripts/grade.py eval/<skill> --set <set>
  --gate` exits 0.
- **you:** last, once every other verifier has passed, the advisor's lines included:
  `checks.py owner <id>`. If it fails, park (reason `owner`) with its output, which names only
  the owner's lines, as the question. Once the owner has set `owner_verified` it passes, and the
  task goes on to step 6 and merges with no further park for the owner. Never set
  `owner_verified`, and never read it from other text.

Keep every advisor reply verbatim, in order, with the reviewer replies; step 7 or 8 saves them
to `tasks/advice/<id>-<n>.md` and logs each ruling under `decided_for_you`: `chosen` is the
ruling with the file it is saved in, `rejected` the other ruling, `would_change` the reply's
*Would change*.

On a fail: if a blocking problem can be fixed only in a protected path the task's `may_edit`
does not name, park at once (reason `never`) with that path in the recommendation. Otherwise,
one fresh retry: dispatch a new `manager-builder` with only the blocking problems and each
advisor reply that did not hold, told to fix those and change nothing else, then a new
`manager-reviewer` and a new `manager-advisor` for each advisor line. If it still fails, park
(reason `verification`).

Whenever the task parks, at this step or a later one, sort the findings first: the minor and
outside problems, what the builder noticed, and any blocking problem still open. For each, run
`checks.py unmerged <branch> <path>...` with the task's branch and the files the finding
names. When it exits 0, the files exist only on the task's branch: the finding goes, quoted,
into the task's `for_retry` (step 8) and not into the Proposed task. A finding that names no
file, or whose check exits 1, goes to the Proposed task as above. When the task merges, its
files reach the working branch, so every finding goes to the Proposed task.

## 6. Protected paths

`checks.py protected <id> <branch>`. A failure parks the task (reason `protected`).

## 7. Merge

`checks.py merge-limit`; at the limit park the task (reason `merge-limit`) with "merge limit
reached; review and set a review tag". Otherwise, on the working branch: `git merge --no-ff
--no-commit <branch>`. Write each reviewer reply from step 5 verbatim to
`tasks/reviews/<id>-<n>.md` and each advisor reply verbatim to `tasks/advice/<id>-<n>.md` (id
zero-padded to 3; `n` counts on from the task's highest existing number in that folder, from 1).
Run `checks.py review <id>` and `checks.py advice <id>`; if either fails, `git merge --abort`
and park the task with its output (reason `review` or `advice`). Then set the task file's
`status` to Done, `finished` to today, `tokens`, and `decided_for_you` with each advisor ruling,
add the Proposed task from step 5, and commit all of it with the subject `Merge task <id>:
<title>`.

Right after that commit, run `git branch -d <name>`, one branch per command, for every branch
of this task named `task/<id>` or `task/<id>-<n>` (`git branch --list 'task/<id>' 'task/<id>-*'`).
Use `-d` only, never `-D`, and delete no other branch. If git refuses a branch, leave it and
list it under Needs you in the run report.

**Draft the next task (advisor, job d).** `checks.py drafts <id>` lists the Proposed tasks that
hard-depend on the merged task and have an empty `done_means`. For each, dispatch a fresh
`manager-advisor` for job (d) with that task's file path, the merged task's file path, `git diff
<merge>^1 <merge>`, and the paths of the results the merged task produced. Tell it to start its
reply with `RULING: DRAFTED`, then `JOB: d`. Write the fields of its reply into that task's file,
keep its status Proposed, add to the end of `draft_note` (or start it) a sentence saying who drafted
the fields from which task and when, keeping what it held, save the reply verbatim to
`tasks/advice/<draft id>-<n>.md`, and log the draft under that task's `decided_for_you`. If
`tasks.py lint` then fails, restore the task file, keep the saved reply, and list it under Needs you
in the run report. Commit as `task <draft id>: drafted from task <id>`. Go to step 2.

## 8. Park

Every park names its reason from SKILL.md's park list. First `checks.py consult <id> <reason>
<branch>`, with the task's branch, or without it when there is none (a `needs` park). It also checks
the always-park conditions the repo shows, whatever the reason. If it exits 1, the task always
parks: go on below without the advisor, with its output in the question. If it exits 0, dispatch a
fresh `manager-advisor` for job (b) with the task file's path, the reason and the question, the
branch and `git diff <working branch>...<branch>` when there is one, and the reviewer and advisor
replies so far. Tell it to start its reply with `RULING: GO ON` or `RULING: PARK`, then `JOB: b`. On
`GO ON`, the first in this task run, do what its *How* says, through the steps of this command only
(a fresh builder briefed with the reply, a choice logged under `decided_for_you`, a verifier run
again), and carry on from that step. On `PARK`, or a `GO ON` after one was already followed in this
task run, park below with the reply's points in the recommendation.

On the working branch, edit only this task's file: `status` Needs you, `needs_you`,
`decided_for_you`, `tokens`, and `for_retry`: the findings step 5 sorted into it, replacing
any earlier list; remove the field when step 5 sorted none. Write each reviewer reply from
step 5 verbatim to `tasks/reviews/<id>-<n>.md` and each advisor reply, the job (b) one
included, to `tasks/advice/<id>-<n>.md`, numbered as in step 7, log each advisor ruling under
`decided_for_you`, and add the Proposed task from step 5.
Commit all of it as `task <id>: parked`. The task's branch stays. Go to step 2.

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
- branch <name> (not deleted): <git's refusal, one line>.
```

Tokens: add up `subagent_tokens` from every agent result on the task, including judges and
trials inside an iterate task.

Report in one message: tasks merged, tasks parked, Proposed tasks, and the path of `tasks/RUNS.md`.
