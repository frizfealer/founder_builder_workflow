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
`checks.py main-folder`. Never run it while step 7's merge is open in the main folder, from its
`git merge --no-commit` until that merge is committed or aborted: for an agent that returns
meanwhile, run it right after. If it fails, an agent or the owner worked in the main folder: end
the run at once. Dispatch, merge and park nothing more. A task whose agent is still running
stays In progress, with its branch and worktree, for the next run-start to report. Go to step 9
with "main folder check failed" and the check's output under Needs you; step 9 commits the run
report only while the main folder is on the working branch, and then only `tasks/RUNS.md`, never
together with a file an agent changed.

**Decided for you.** Every entry you add to a task's `decided_for_you` holds `chosen`,
`rejected`, `why` (one sentence, the reason for the choice) and `would_change`.

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
(SKILL.md rule 8). If it prints no task, or `checks.py merge-limit` now fails, go to step 9.

Steps 3 to 6 run for every task of the batch side by side: for each step, dispatch the agents of
all the batch's tasks that are at it in one message, so they run at the same time, and take each
task on as its agents return. Step 7 merges the tasks one at a time, in the order they reach it.
When every task of the batch has merged or parked, go to step 2 again.

## 3. Branch

First `checks.py needs <id>`. If it fails, park the task at once (step 8, reason `your-action`)
with its one-line output as the question: no branch, no builder, no worktree.

On the working branch, set each remaining task of the batch to In progress and commit `task <id>:
in progress`, one commit per task, so the board, which reads the main folder, shows it. Then
cut each task's branch from the working branch in its own worktree: `git worktree add
build/worktrees/task-<id> -b task/<id> <working branch>` (an iterate task uses the branch
`/iterate` names, `iterate/<skill>/<set>`, in `build/worktrees/iterate-<skill>-<set>`). If the
branch name exists from an earlier run, add `-2`, `-3`, to the worktree's name too.

## 4. Work, by `runs_as`

- **build**, **measurement:** dispatch `manager-builder` with a complete brief: the task file's
  path and its `done_means`, `may_edit`, and, when set, `may_delete` and `outside_needs` quoted
  (with no `outside_needs`, say that it runs no paid command); the branch and `<worktree>`, where
  it works:
  every Bash command starts `cd <worktree> &&`, every file path is under it, and it never
  touches the main folder. Do not use the Agent tool's `cwd` or `isolation` for this; neither
  kept a builder out of the main folder (SKILL.md rule 8). The brief also gives the paths
  involved; the earlier branch of this task if one exists, whose work the builder brings over
  without any file under `tasks/`, so the new branch's task files stay as the working branch has
  them; the task's `for_retry`, when set, quoted in full as faults this run fixes;
  `DECISIONS.md` as the direction. It commits on the branch, in `<worktree>`, and returns what
  it changed, the check it wrote or ran for `done_means`, its decisions, at most one Proposed
  task, only for a problem that existed before its branch and lies outside its change
  (SKILL.md rule 2), and what it noticed outside the task. When it stops on a fact about the
  owner's product or an outside system, park (reason `owner-fact`) with its question. When it
  stops because `done_means` needs a protected path `may_edit` does not name, park (reason
  `permission`) with that path in the question; it proposes no task for it. When it stops because
  finishing needs money the task's `outside_needs` does not name, park (reason `permission`).
- **iterate:** follow `.claude/commands/iterate.md` for the skill the task names, with the
  task's problem, all of it in the task's worktree: every brief names `<worktree>` as for a
  builder, and its trials and grades run there. Its preconditions and stop list apply. The
  standing merge / revert question in its *Needs you* is answered here: keep the result only
  when its report says no gated metric failed in any trial; otherwise park (reason `failed`)
  with the report as the question (rule 4 of skill-iterate: inconclusive is a revert). Any other
  item under its *Needs you* parks the task, with the same reason.
- **you:** prepare what the owner needs to decide or do (the files to read, the options, a
  recommendation), commit it on the branch in its worktree, and park (reason `your-action`).

**The builder's decisions (advisor, job c).** After each builder returns, here and in step 5,
read its decisions. For each one that changes what a `done_means` line proves (what the line
measures, its inputs, its threshold, or what counts as a pass), dispatch a fresh
`manager-advisor` for job (c) with the task file's path, the line's number and text quoted, the
decision quoted (chosen, rejected, would change), `git diff <working branch>...<branch>`, and
`<worktree>` as the place to read the branch's files. Tell it to start its reply with `RULING:
HOLDS` or `RULING: FAILS`, then `JOB: c (<n>)`. On `FAILS`, the task goes back to the builder
once: a fresh `manager-builder` with the reply quoted, told to make the line prove what it was
written to prove and change nothing else; then this check again on its decisions. A second
`FAILS` on the task parks it (reason `failed`).

## 5. Verify, by `verified_by` and `verifier_of_line`

Never by the builder. Each line of `done_means` is verified by the one verifier
`verifier_of_line` names for it, or else by every verifier in `verified_by`
(`references/task-fields.md`). Run every verifier that has a line, `you` last. An empty or
failed review is a fail, and so is a reply whose first line is not `VERDICT: PASS`, and so is a
reply with any problem labelled blocking. Minor and outside problems never fail it. Keep every
reviewer reply verbatim, in order; step 7 or 8 saves them.

An agent creates a task in one case only (SKILL.md rule 2): a problem that existed before the
task's branch and lies outside its change. From the outside problems, the minor ones that
`checks.py unmerged` does not give the task (step 5a), and what the builder noticed, add at most
one Proposed task for this task run, bundling the earlier problems worth doing, or none; step 7
or 8 commits it. A finding on lines the branch added or changed never goes there. Its
`outside_problems` names each earlier file and the problem in it; give it `tags`: 1 to 3 lines
of `tasks/tags.txt` that fit its title, notes and `may_edit` (`repo` when none fits). When the
branch already adds a Proposed task, add none: in the merge or park commit, put the earlier
problems into that task's `outside_problems` and `notes`.

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
- **advisor, labels against verdicts:** when an advisor line compares labels with verdicts the
  advisor must not see (task 56 line 3), the line names the comparison command and the form of
  its labels file. Brief job (a) as above, with only the inputs to label and that form quoted,
  and tell it to give its labels under **Labels:** as one JSON object in that form, starting
  `RULING: HOLDS` when it labelled every item and `RULING: FAILS` when it could not. Write the
  object as it stands to `<worktree>/build/labels/<id>-<line>.json` with the Write tool (`build/`
  is git-ignored, so the branch stays as its builder left it), and run the command in the
  worktree with that file as its labels: `cd <worktree> && <command>`. The line holds only when
  the reply starts `RULING: HOLDS` and the command exits 0; anything else is a failed advisor
  line. Add the command to the task's check commands for step 7's `try-merge`.
- **metrics:** `python3 .claude/skills/skill-iterate/scripts/grade.py eval/<skill> --set <set>
  --gate` exits 0, run in the task's worktree.
- **you:** last, once every other verifier has passed, the advisor's lines included, and after
  step 5a's fix pass: `checks.py owner <id>`. If it fails, park (reason `your-action`) with its
  output, which names only the owner's lines, as the question. Once the owner has set `owner_verified` it passes, and the
  task goes on to step 6 and merges with no further park for the owner. Never set
  `owner_verified`, and never read it from other text.

Keep every advisor reply verbatim, in order, with the reviewer replies; step 7 or 8 saves them
to `tasks/advice/<id>-<n>.md` and logs each ruling under `decided_for_you`: `chosen` is the
ruling with the file it is saved in, `rejected` the other ruling, `why` the reply's *Why* in one
sentence, `would_change` the reply's *Would change*.

On a fail: if a blocking problem can be fixed only in a protected path the task's `may_edit`
does not name, park at once (reason `permission`) with that path in the recommendation. Otherwise,
one fresh retry: dispatch a new `manager-builder`, in the same worktree and branch, with only
the blocking problems and each advisor reply that did not hold, told to fix those and change
nothing else, then a new `manager-reviewer` and a new `manager-advisor` for each advisor line.
If it still fails, park (reason `failed`).

Whenever the task parks, at this step or a later one, sort the findings first. A blocking
problem still open is the task's own, by its label: it goes, quoted, into the task's `for_retry`
(step 8). For each minor and outside problem and each point the builder noticed, run `checks.py
unmerged <branch> <path>:<lines>...` with the task's branch and the file and lines the finding
names. When it exits 0, the finding is on a file only the branch has or on lines the branch
added or changed: it goes, quoted, into `for_retry`, and not into the Proposed task. When it
exits 1, it is an earlier problem, for the Proposed task as above, unless the review says the
lines are wrong only because of the branch's change (SKILL.md rule 2): then it goes into
`for_retry`; a finding that names no file
stays in the review file. When the task merges, a finding the fix pass left open stays in the
review file and creates no task.

## 5a. One fix pass

Fix it here (SKILL.md rule 3), between the review and the merge. Once every verifier of step 5
but `you` has passed, sort the minor problems of the latest review: for each, `checks.py
unmerged <branch> <path>:<lines>...` with the file and lines it names. Exit 0 puts it on the fix
list; exit 1 makes it an earlier problem, for step 5's Proposed task, unless the review says the
lines are wrong only because of the branch's change (SKILL.md rule 2): then it goes on the fix
list. With an empty fix list, go
on to the `you` check and step 6.

Otherwise run one fix pass, with its three limits:
- The builder gets only that list. Note the branch's last commit as `<before>`, then dispatch a
  fresh `manager-builder` in the same worktree and branch with the minor findings of the fix
  list quoted, each as the review wrote it, and nothing else of the review: not the blocking
  problems, not the outside problems, not the verdict. Tell it to fix those, change nothing
  else, and commit.
- The re-check looks only at those fixes. Dispatch a fresh `manager-reviewer` with the task
  file's path, the fix list, `git diff <before> <branch>` and `<worktree>`, told to judge only
  whether each finding is fixed and whether a fix broke something, and to start its reply
  `VERDICT: PASS` or `VERDICT: FAIL`. Run the `script` commands of step 5 again in the worktree;
  each must exit 0.
- Whatever is still open after the one pass, a finding not fixed or a new minor problem, stays
  in the review file and creates no task, no second pass and no `for_retry`. A blocking problem
  stays the only reason a review fails: a blocking problem in the fixes, or a failing command,
  fails step 5 (its one fresh retry when the task has not had it, else park, reason
  `failed`).

Keep the re-check's reply with the other reviewer replies; step 7 saves it last, so it is the
reply `checks.py review` reads.

## 6. Protected paths

`checks.py protected <id> <branch>`. A failure parks the task (reason `permission`). It also
fails a file the branch deleted or renamed that the task's `may_delete` does not name.

## 7. Merge

One task at a time: start no merge while another task is in this step. `checks.py merge-limit`;
`tasks.py batch` took no more tasks than the merges left, so it passes, but if the limit is
reached all the same, park the task (reason `your-action`) with its output; its branch stays.
For an iterate task, `checks.py stale <skill> <branch>`; if it fails, park (reason `failed`)
with its output: the result was measured on an older version of the skill.

Before each merge after the first of the run: `checks.py try-merge <id> <worktree> <command>...`
with the task's check commands, the ones step 5 ran for `script` and the builder's check. It
merges the updated working branch into the worktree without committing, runs each command
there, and undoes the merge. On exit 1 the task goes back to its builder once: cut
`task/<id>-<n>` from the working branch in a new worktree (step 3's names), dispatch a fresh
`manager-builder` with the failed branch as the earlier branch whose work it brings over and
the script's output quoted as the fault to fix, then steps 4 to 7 for it again. On exit 3, or
2, park (reason `failed`) with its output.

Then, on the working branch in the main folder, write each reviewer reply from steps 5 and 5a
verbatim to `tasks/reviews/<id>-<n>.md` and each advisor reply verbatim to
`tasks/advice/<id>-<n>.md` (id zero-padded to 3; `n` counts on from the task's highest existing
number in that folder, from 1). They stay uncommitted until the merge commit. Run `checks.py
review <id>` and `checks.py advice <id>`; if either fails, park the task with its output (reason
`failed`).

Then `git merge --no-ff --no-commit <branch>`, alone in its command. While the run is active the
hook refuses it unless `checks.py protected`, `checks.py owner`, `checks.py review`, `checks.py
advice` and `checks.py merge-limit` all pass for the task; if it refuses, park the task with that
output, under the reason for the check its output names: `permission` for `checks.py protected`,
`your-action` for `checks.py owner` or `checks.py merge-limit`, `failed` for `checks.py review` or
`checks.py advice`. Then set the task file's `status` to Done, `finished` to
today, `tokens` (its `agents` so far plus this run's count from `checks.py tokens`), and
`decided_for_you` with each advisor ruling, remove its `for_retry`, add the Proposed task from
step 5, and commit all of it with the subject `Merge task <id>: <title>`.
Write that subject with the Write tool to `build/merge-message-<id>.txt` in the main folder
(git-ignored), not with echo or a heredoc, and commit with `git commit -F
build/merge-message-<id>.txt`: bash then expands nothing in the title, whatever it holds, and the
hook reads no title as commands.

Right after that commit, remove each worktree of this task's branches with `git worktree remove
<path>`, never `--force`; if git refuses, leave it and list it under Needs you in the run report,
with git's refusal and your recommendation.
Then, for every branch of this task (`git branch --list 'task/<id>' 'task/<id>-*'`), run
`checks.py superseded <name>`. Only when it exits 0, delete the branch with `git branch -D
<name>` alone in its command: one branch, no other command, no `$` or backtick, and no `-C`,
`--git-dir` or `GIT_DIR=`. While the run is active, the hook allows a forced deletion only in
that form and only for a branch the script confirms. Keep the name and the
last commit id the script printed for the run report's Done section. When it exits 1, leave the
branch and put the script's output, as it is, under Needs you: it names the condition that
failed, how many files differ from the working branch and how many exist only on the branch,
and a recommendation with its reason. Delete no other branch.

**Draft the next task (manager; advisor, job d).** `checks.py drafts <id>` lists the Proposed
tasks that hard-depend on the merged task and have an empty `done_means`. For each, draft its
`done_means` (numbered `(1)`, `(2)`, ...), `verified_by`, `verifier_of_line` if a line needs one
verifier, `may_edit` and `runs_as` yourself, from that task's own text and the merged task's
results and findings, following `references/task-fields.md`: each pass line one a verifier can
check, and each traced to a finding or a result. Then dispatch a fresh `manager-advisor` for job
(d) to review the draft, with the draft quoted as one JSON object, that task's file path, the
merged task's file path, `git diff <merge>^1 <merge>`, and the paths of the results the merged
task produced. Tell it to start its reply with `RULING: HOLDS` or `RULING: FAILS`, then `JOB: d`.
On `HOLDS`, write the draft into that task's file. On `FAILS`, write only the lines it holds,
numbered again from `(1)`, with none of what it names as new scope, or no `done_means` when none
is left; add nothing it suggests. Keep the status Proposed, add to the end of `draft_note` (or
start it) a sentence saying that the manager drafted the fields from which task, the advisor's
ruling and the date, keeping what it held, save the reply verbatim to `tasks/advice/<draft
id>-<n>.md`, and log the ruling under that task's `decided_for_you`. If `tasks.py lint` then
fails, restore the task file, keep the saved reply, and list it under Needs you in the run
report. Commit as `task <draft id>: drafted from task <id>`. Then the next task of the batch that
reaches this step; when the batch is done, step 2.

## 8. Park

Every park names one of the four reasons of SKILL.md's park list: `permission`, `your-action`,
`owner-fact` or `failed`. The question in `needs_you` starts with the specific cause: the output
of the script that failed or of `checks.py consult`, or the name of the check that failed; then
what the owner must decide or do. First `checks.py consult <id> <reason> <branch>`, with the
task's branch, or without it when there is none (the outside-need park at step 3). It also
checks the always-park conditions the repo shows, whatever the reason; when one holds, the task
parks under the one reason its output names, `permission` when a permission condition holds
beside a your-action one, and the question gives every cause it names. If it exits 1, the task always parks: go on below
without the advisor, with its output in the question. If it exits 3, it could not decide: park
without the advisor, with its output in the question. If it exits 0, dispatch a fresh
`manager-advisor` for job (b) with the task file's path, the reason and the question, the branch,
`git diff <working branch>...<branch>` and `<worktree>` as the place to read the branch's files
when there is one, and the reviewer and advisor replies so far. Tell it to start its reply with
`RULING: PARK` or `RULING: NO PARK`, then `JOB: b`. On `RULING: NO PARK`, the first in this task
run, do what its *How* says, through the steps of this command only (a fresh builder briefed with
the reply, a choice logged under `decided_for_you`, a verifier run again), and carry on from that
step. After `RULING: NO PARK` on a `failed` park, the check that failed runs again before any
merge: the review or the advisor's line of step 5, `checks.py review` or `checks.py advice`,
`checks.py try-merge`, or `checks.py stale`; the advisor never overrides a check, and the merge hook still
refuses a merge whose checks fail. If the check fails again, park through this step again. On
`RULING: PARK`, or a `RULING: NO PARK` after one was already followed in this task run, park below
with the reply's points in the recommendation.

On the working branch, edit only this task's file: `status` Needs you, `needs_you`,
`decided_for_you`, `tokens` (as in step 7), and `for_retry`. When step 5 ran in this task run,
`for_retry` is the findings step 5 sorted into it, replacing any earlier list, and the field is
removed when step 5 sorted none. A park before step 5 (the outside-need park at step 3) leaves
`for_retry` as it is, so an earlier list is not lost. Write each reviewer reply
from step 5 verbatim to `tasks/reviews/<id>-<n>.md` and each advisor reply, the job (b) one
included, to `tasks/advice/<id>-<n>.md`, numbered as in step 7, log each advisor ruling under
`decided_for_you`, and add the Proposed task from step 5. Commit all of it as `task <id>:
parked`. The task's branches stay, when it has any. Remove every worktree of the task's branches
(`git worktree list` shows them; a task rebuilt after `try-merge` has two) with `git worktree
remove <path>`, never `--force`; if git refuses, leave it and list it under Needs you, with
git's refusal and your recommendation. Go on with
the batch's other tasks; when every one has merged or parked, go to step 2.

## 9. End

`checks.py tokens` for the Tokens lines, then `checks.py run-end`. Prepend this run to
`tasks/RUNS.md` and commit only that file on the working branch: `git commit -m 'manage: run
report <date>' -- tasks/RUNS.md`, which leaves out any other change in the main folder, a file an
agent changed included. When the run ended on a failed main-folder check with the main folder on
another branch, commit nothing and give the report in your final message only.

```markdown
## Run <date> <time>

Stopped because: <no task to take | merge limit | start check failed: ... | main folder check failed: ...>.

### Done
- task <id>: <title>; merge <hash>; tokens <agents this run> (task total <agents>; main session: not recorded)
- branch <name> deleted, last commit <id>

A deleted branch is restored with `git branch <name> <id>` while git still holds the commit.

### Tokens
- task <id>: <n>, one line per task `checks.py tokens` lists, merged or parked
- total: <n>

### Decided for you
- task <id>: chose <x> over <y>, because <why>; would change if <z>

### Needs you
- task <id> (parked): <question>. Recommended: <answer>. If you veto: <what changes>.
- task <id> (Proposed): <title>. <why>.
- branch <name> (not deleted): <checks.py superseded's output, as it is>
- worktree <path> (not removed): <git's refusal, one line>. Recommended: <remove or keep, with its reason>.
```

The restore sentence appears once, under Done, when the report lists a deleted branch.

Tokens: `checks.py tokens` holds every agent result counted on its task in this run, including
judges and trials inside an iterate task.

Report in one message: tasks merged, tasks parked, Proposed tasks, and the path of `tasks/RUNS.md`.
