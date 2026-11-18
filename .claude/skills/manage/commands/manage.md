---
description: One manager run over the task list — take up to N independent Ready tasks at once, build and verify each in its own worktree, merge one at a time or park; report at the end
argument-hint: "[--dry-run]"
---

Run the task list. Read `.claude/skills/manage/SKILL.md` first; its rules, park list and never
list apply to every step. The owner is not watching: never ask him anything during the run.
What needs him is parked, and goes in the report. `S` below is `.claude/skills/manage`.

With `--dry-run`: run `python3 S/scripts/tasks.py lint`, `python3 S/scripts/checks.py
merge-limit` and `python3 S/scripts/tasks.py batch`, print their output, and stop. Change
nothing: no branch, no marker, no file.

**The main folder and the worktrees.** The main folder stays on the working branch until the run
ends: never switch it to another branch. You commit there only the commits this command names.
Each task is built, verified and fixed in its own worktree, `build/worktrees/<branch>` with each
`/` as `-`, on its own branch; `<worktree>` below is its absolute path. Every brief to an agent
that works on a task names that path as the only folder it works in.

**Agents and tokens.** Every agent dispatch's description starts `task <id>:` (`task 58:
builder`), so each result, and each notice of a background agent finishing, belongs to one task.
After each agent returns, `checks.py tokens <id> <n>` with its tokens: `subagent_tokens` in the
result, or `total_tokens` in a background agent's notice. After each agent that can write
returns (a builder, or an agent of an iterate task with Edit, Write or Bash), run
`checks.py main-folder`. If it fails, an agent worked in the main folder: end the run at once
(step 9, "main folder check failed"), change nothing on the working branch, and put its output
under Needs you.

## 1. Start

On the working branch, with no uncommitted changes to tracked files. Run `tasks.py lint` and
`checks.py merge-limit`; if either fails, end the run with its output as the one-line reason.
Then `checks.py run-start`; if it fails, end the run the same way. It records the working
branch's commit, removes each worktree an earlier run left under `build/worktrees/` with no
uncommitted change (its branch stays), and prints a line for each worktree that holds one, left
as it is, and for each task left In progress, with a recommendation. Each of those lines goes
under Needs you in the run report as it is.

## 2. Take

`tasks.py batch`: up to `tasks_at_once` tasks (`limits.json`) that are independent of each other
(SKILL.md rule 8). If it prints no task, or `merge-limit` now fails, go to step 9.

Steps 3 to 6 run for every task of the batch side by side: for each step, dispatch the agents of
all the batch's tasks that are at it in one message, so they run at the same time, and take each
task on as its agents return. Step 7 merges the tasks one at a time, in the order they reach it.
When every task of the batch has merged or parked, go to step 2 again.

## 3. Branch

First `checks.py needs <id>`. If it fails, park the task at once (step 8, reason `needs`) with
its one-line output as the question: no branch, no builder, no worktree.

On the working branch, set each remaining task of the batch to In progress and commit `task <id>:
in progress`, one commit per task, so the board, which reads the main folder, shows it. Then
cut each task's branch from the working branch in its own worktree: `git worktree add
build/worktrees/task-<id> -b task/<id> <working branch>` (an iterate task uses the branch
`/iterate` names, `iterate/<skill>/<set>`, in `build/worktrees/iterate-<skill>-<set>`). If the
branch name exists from an earlier run, add `-2`, `-3`, to the worktree's name too.

## 4. Work, by `runs_as`

- **build**, **measurement:** dispatch `manager-builder` with a complete brief: the task file's
  path and its `done_means` and `may_edit` quoted; the branch and `<worktree>`, where it works:
  every Bash command starts `cd <worktree> &&`, every file path is under it, and it never
  touches the main folder. Do not use the Agent tool's `cwd` or `isolation` for this; neither
  kept a builder out of the main folder (SKILL.md rule 8). The brief also gives the paths
  involved; the earlier branch of this task if one exists, whose work the builder brings over
  without any file under `tasks/`, so the new branch's task files stay as the working branch has
  them; the task's `for_retry`, when set, quoted in full as faults this run fixes;
  `DECISIONS.md` as the direction. It commits on the branch, in `<worktree>`, and returns what
  it changed, the check it wrote or ran for `done_means`, its decisions, a Proposed task only
  when `done_means` needs a protected path outside `may_edit`, and what it noticed outside the
  task. When it stops on a fact about the owner's product or an outside system, park (reason
  `owner-fact`) with its question.
- **iterate:** follow `.claude/commands/iterate.md` for the skill the task names, with the
  task's problem, all of it in the task's worktree: every brief names `<worktree>` as for a
  builder, and its trials and grades run there. Its preconditions and stop list apply. The
  standing merge / revert question in its *Needs you* is answered here: keep the result only
  when its report says no gated metric failed in any trial; otherwise park (reason `iterate`)
  with the report as the question (rule 4 of skill-iterate: inconclusive is a revert). Any other
  item under its *Needs you* parks the task, with the same reason.
- **you:** prepare what the owner needs to decide or do (the files to read, the options, a
  recommendation), commit it on the branch in its worktree, and park (reason `runs-as-you`).

**The builder's decisions (advisor, job c).** After each builder returns, here and in step 5,
read its decisions. For each one that changes what a `done_means` line proves (what the line
measures, its inputs, its threshold, or what counts as a pass), dispatch a fresh
`manager-advisor` for job (c) with the task file's path, the line's number and text quoted, the
decision quoted (chosen, rejected, would change), `git diff <working branch>...<branch>`, and
`<worktree>` as the place to read the branch's files. Tell it to start its reply with `RULING:
HOLDS` or `RULING: FAILS`, then `JOB: c (<n>)`. On `FAILS`, the task goes back to the builder
once: a fresh `manager-builder` with the reply quoted, told to make the line prove what it was
written to prove and change nothing else; then this check again on its decisions. A second
`FAILS` on the task parks it (reason `verification`).

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

- **reviewer**, **script:** dispatch `manager-reviewer` with the task file's path, the
  output of `git diff <working branch>...<branch>`, `<worktree>` as the place to read the
  changed files in full (the main folder holds the working branch, not the task's files), and
  the numbers of the lines that are neither the reviewer's nor the script's, as lines it does
  not judge. Not the builder's report. Tell it to look for what is wrong. For `script`, it
  names the commands that prove its lines; run exactly those yourself in the worktree (`cd
  <worktree> && <command>`), and every one must exit 0.
- **advisor:** for each line the advisor verifies, dispatch a fresh `manager-advisor` for job
  (a) with the line's number and text quoted and only the paths the line names, in the task's
  worktree: not the task file, not the diff, not another reply. When the line names its inputs
  without paths, give the files of the branch that hold them, never a file that holds what the
  line tests them against (for labelling: the transcripts, never the verdicts), and log that
  list under `decided_for_you`. Tell it to start its reply with `RULING: HOLDS` or
  `RULING: FAILS`, then `JOB: a (<n>)`. Any reply that does not start `RULING: HOLDS` is a fail.
  Never give the advisor a line whose verifier is `you`.
- **metrics:** `python3 .claude/skills/skill-iterate/scripts/grade.py eval/<skill> --set <set>
  --gate` exits 0, run in the task's worktree.
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
one fresh retry: dispatch a new `manager-builder`, in the same worktree and branch, with only
the blocking problems and each advisor reply that did not hold, told to fix those and change
nothing else, then a new `manager-reviewer` and a new `manager-advisor` for each advisor line.
If it still fails, park (reason `verification`).

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

One task at a time: start no merge while another task is in this step. `checks.py merge-limit`;
at the limit park the task (reason `merge-limit`) with "merge limit reached; review and set a
review tag"; its branch stays. For an iterate task, `checks.py stale <skill> <branch>`; if it
fails, park (reason `stale`) with its output: the result was measured on an older version of
the skill.

Before each merge after the first of the run: `checks.py try-merge <id> <worktree> <command>...`
with the task's check commands, the ones step 5 ran for `script` and the builder's check. It
merges the updated working branch into the worktree without committing, runs each command
there, and undoes the merge. On exit 1 the task goes back to its builder once: cut
`task/<id>-<n>` from the working branch in a new worktree (step 3's names), dispatch a fresh
`manager-builder` with the failed branch as the earlier branch whose work it brings over and
the script's output quoted as the fault to fix, then steps 4 to 7 for it again. On exit 3, or
2, park (reason `conflict`) with its output.

Then, on the working branch in the main folder: `git merge --no-ff --no-commit <branch>`. Write
each reviewer reply from step 5 verbatim to `tasks/reviews/<id>-<n>.md` and each advisor reply
verbatim to `tasks/advice/<id>-<n>.md` (id zero-padded to 3; `n` counts on from the task's
highest existing number in that folder, from 1). Run `checks.py review <id>` and `checks.py
advice <id>`; if either fails, `git merge --abort` and park the task with its output (reason
`review` or `advice`). Then set the task file's `status` to Done, `finished` to today, `tokens`
(its `agents` so far plus this run's count from `checks.py tokens`), and `decided_for_you` with
each advisor ruling, add the Proposed task from step 5, and commit all of it with the subject
`Merge task <id>: <title>`.

Right after that commit, remove each worktree of this task's branches with `git worktree remove
<path>`, never `--force`. Then run `git branch -d <name>`, one branch per command, for every
branch of this task named `task/<id>` or `task/<id>-<n>` (`git branch --list 'task/<id>'
'task/<id>-*'`). Use `-d` only, never `-D`, and delete no other branch. If git refuses a
worktree or a branch, leave it and list it under Needs you in the run report.

**Draft the next task (advisor, job d).** `checks.py drafts <id>` lists the Proposed tasks that
hard-depend on the merged task and have an empty `done_means`. For each, dispatch a fresh
`manager-advisor` for job (d) with that task's file path, the merged task's file path, `git diff
<merge>^1 <merge>`, and the paths of the results the merged task produced. Tell it to start its
reply with `RULING: DRAFTED`, then `JOB: d`. Write the fields of its reply into that task's file,
keep its status Proposed, add to the end of `draft_note` (or start it) a sentence saying who drafted
the fields from which task and when, keeping what it held, save the reply verbatim to
`tasks/advice/<draft id>-<n>.md`, and log the draft under that task's `decided_for_you`. If
`tasks.py lint` then fails, restore the task file, keep the saved reply, and list it under Needs you
in the run report. Commit as `task <draft id>: drafted from task <id>`. Then the next task of the
batch that reaches this step; when the batch is done, step 2.

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
`decided_for_you`, `tokens` (as in step 7), and `for_retry`: the findings step 5 sorted into it,
replacing any earlier list; remove the field when step 5 sorted none. Write each reviewer reply
from step 5 verbatim to `tasks/reviews/<id>-<n>.md` and each advisor reply, the job (b) one
included, to `tasks/advice/<id>-<n>.md`, numbered as in step 7, log each advisor ruling under
`decided_for_you`, and add the Proposed task from step 5. Commit all of it as `task <id>:
parked`. The task's branch stays. Remove its worktree with `git worktree remove <path>`, never
`--force`; if git refuses, leave it and list it under Needs you. Go on with the batch's other
tasks; when every one has merged or parked, go to step 2.

## 9. End

`checks.py tokens` for the Tokens lines, then `checks.py run-end`. Prepend this run to
`tasks/RUNS.md` and commit it on the working branch as `manage: run report <date>`:

```markdown
## Run <date> <time>

Stopped because: <no task to take | merge limit | start check failed: ... | main folder check failed: ...>.

### Done
- task <id>: <title>; merge <hash>; tokens <agents this run> (task total <agents>; main session: not recorded)

### Tokens
- task <id>: <n>, one line per task `checks.py tokens` lists, merged or parked
- total: <n>

### Decided for you
- task <id>: chose <x> over <y>; would change if <z>

### Needs you
- task <id> (parked): <question>. Recommended: <answer>. If you veto: <what changes>.
- task <id> (Proposed): <title>. <why>.
- branch <name> (not deleted): <git's refusal, one line>.
```

Tokens: `checks.py tokens` holds every agent result counted on its task in this run, including
judges and trials inside an iterate task.

Report in one message: tasks merged, tasks parked, Proposed tasks, and the path of `tasks/RUNS.md`.
