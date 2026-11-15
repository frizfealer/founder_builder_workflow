# Build the task list and the manager skill

Build three things on a new branch `manager/build`, cut from `re-create-from-scratch`: the task
list as files in the repo, three checks, and a manager skill. Then stop and report.

Do not merge the branch, push, run the manager for real, run trials, or edit any existing skill,
`DECISIONS.md`, or anything under `eval/`. Leave the untracked paths outside `manager-build/` alone
(`git status` shows eight); never `git add -A`.

## Why

The owner has about 10 hours a week for this repo. He wants Claude Code to take tasks from a
list and run them without asking what is next. Two failures must be avoided: a manager that
asks him about every decision, and a manager that makes a decision that is costly to undo.

The task list is a Google Sheet today. On 2026-11-15 it was six rows behind the repo. So the
list moves into the repo, where a task's status changes in the same commit as its work, and a
manager skill runs it under gates. The gates that a script can check are enforced by scripts.

## Read first

- `DECISIONS.md`: the direction, and the workflow stages the tasks belong to.
- `.claude/skills/skill-iterate/SKILL.md`, `references/escalation.md`,
  `references/report-template.md`, `commands/iterate.md`: the loop for changing one skill. The
  manager calls it and never copies it. Use its install convention (symlinks into
  `.claude/commands/` and `.claude/agents/`) and its report sections.
- `manager-build/tasks-seed.json`: 33 tasks. Rows 1 to 30 come from the sheet as read on
  2026-11-15 17:10 ET, with drafted new fields for the open ones. Tasks 31 to 33 are this build.
- The file and folder names under `eval/agent-spec/` and `.claude/skills/skill-iterate/`, to
  write the protected-path list. Names only; you need not read the contents.
- Claude Code's current hook documentation (https://code.claude.com/docs/en/hooks-guide) before
  writing the hook. Do not write it from memory.

## Terms

- **Task:** one unit of work with a stated finish. One file.
- **Ready:** the owner has committed to the task. Only the owner sets this status.
- **Park:** stop work on one task, record the question for the owner, set the task to
  "Needs you", and go on to another task.
- **Protected path:** a file or folder that a task may change only if its "May edit" field
  names it.
- **Working branch:** `re-create-from-scratch`.
- **Review tag:** a git tag the owner sets each time he has reviewed what the manager merged.

## Part 1: the task list in the repo

One file per task, in one folder. Each task has these fields:

| Field | Values | Who sets it |
| --- | --- | --- |
| id, title, item, motivation, notes, added, finished, source chat | As in the seed | Owner; manager sets `finished` |
| status | Proposed, Backlog, Ready, In progress, Needs you, Done, Dropped | Owner sets Ready. Manager sets In progress, Needs you, Done, and creates Proposed tasks |
| done means | The observable end state | Owner; manager may draft |
| verified by | Any of: script, metrics, reviewer, you. Never the agent that built the task | Owner; manager may draft |
| may edit | Protected paths this task may change. Empty for most | Owner; manager may draft |
| runs as | build, iterate, measurement, you | Owner; manager may draft |
| priority | high, medium, low | Owner |
| depends on | Task ids, each hard unless marked soft | Owner; manager may draft |
| tokens | Tokens spent on the task | Manager |

A draft counts only when the owner sets the task to Ready. After that the manager may not
change done means, verified by, may edit, runs as, priority or depends on.

Build one script with these commands (names are yours):

- **lint:** every field is valid; every dependency id exists; a Ready task has done means,
  verified by, runs as and priority.
- **list:** print all tasks as one table the owner can read in a terminal.
- **next:** print the task the manager should take, or say why there is none. A task can be
  taken when it is Ready and every hard dependency is Done. Order: highest priority, then the
  task that the most other open tasks depend on, then the lowest id.

Convert all 33 seed tasks. Seed fields `draft_note` and `tokens: null` carry over as they are.

## Part 2: three checks

**Protected paths (a lint, run before a merge).** Given a task and its branch, compare the
files the branch changes against the working branch with a protected-path list.

- A changed protected path that the task's "may edit" does not name fails the check.
- History paths are append-only: a new file or folder passes; a changed, renamed or removed
  existing file fails, whatever "may edit" says.
- Keep the list in one file of path patterns. Seed it with the table below.
- On a task's branch, the only task-file changes allowed are to that task's own file and to
  new files with status Proposed.

| Group | Paths | Rule |
| --- | --- | --- |
| Direction | `DECISIONS.md` | Named in "may edit" only |
| Measurement, all skills | `.claude/skills/skill-iterate/scripts/grade.py`, `scripts/calibrate.py`, `agents/judge.md`, `references/escalation.md`, `references/grading-schema.md` | Named only |
| Measurement, per skill | `eval/*/grading*.json`, `eval/agent-spec/judge-verifier-brief.md`, `eval/agent-spec/new-format/key-build2.md`, `judge-brief-key.md`, `FORMAT.md`, `grader/`, `seeded/`, `seeded-clean/`, `seeded-defects.md` | Named only |
| Frozen trial inputs | `eval/agent-spec/PROMPT*.md`, `stand-in-brief.md`, `owner-brief.md`, `product-idea.md`, `review-packet.md` | Named only |
| Owner's rulings | `eval/*/calibration/` | Named only |
| History | `eval/*/baseline/`, `eval/*/results/`, `eval/*/EXPERIMENTS.md` | Append-only |
| The manager's own checks | The protected-path list, the check scripts and their tests, the limits config, `.claude/settings*.json`, `.git/hooks/` | Named only |

**No push during a manager run (a hook).** While a manager run is active, a shell command that
pushes is refused, with a message saying the owner pushes. Outside a manager run the hook
allows everything: the owner asks Claude Code to push in his own sessions and that must keep
working. How a run is marked active is yours to decide. The hook reads command text, so it is
an early stop, not proof; say so in the skill.

**Merge limit (a check at the start of a run and before each merge).** Count the task merges on
the working branch since the latest review tag. At the limit, the manager merges nothing more
and ends the run. The limit starts at 3 and lives in a small config file. With no review tag
yet, count every task merge on the working branch.

Write tests for all three, run in temporary git repositories, never in this repo's history.

## Part 3: the manager skill

A skill under `.claude/skills/`, with a `/manage` command and its agents, installed by symlink
the way skill-iterate is. Every agent definition sets `model` and `effort`; default both the
builder and the reviewer to `opus` and `high`. The reviewer gets a fresh context and read-only
tools.

One run:

1. Lint the tasks. Check the merge limit. Mark the run active.
2. Take the task that **next** prints. If there is none, end the run.
3. Cut one branch for the task. Set the task to In progress.
4. Do the work according to "runs as":
   - **build** and **measurement:** brief a builder agent with the task's done means, may edit
     and the paths involved. The agent starts with no context, so the brief is complete.
   - **iterate:** follow `commands/iterate.md` for the skill the task names. Its own stop list
     applies. Whatever its report lists under *Needs you* parks the task. Keep the result only
     when its report says no gated metric failed in any trial; otherwise revert, as
     skill-iterate rule 4 says.
   - **you:** prepare what the owner needs, then park the task.
5. Verify as "verified by" says, with an agent that did not build the task. Brief the reviewer
   from the task file and the diff, not from the builder's report. Tell it to look for what is
   wrong. An empty or failed review is not a pass.
6. Run the protected-path check.
7. On a pass: merge into the working branch as one merge commit whose message carries the task
   id. In that same merge the task file shows Done, the finish date and the tokens.
8. On a fail, or when the task needs the owner: park it. Go to step 2.

The manager parks a task, and never asks mid-run, in these cases:

- a fact about the owner's product or an outside system that only he knows;
- a failed protected-path check, or a verification that still fails after one fresh retry;
- "verified by" includes the owner;
- finishing would need something from the never list.

The manager never:

- pushes;
- deletes a branch, or anything outside the task's own branch;
- changes a protected path the task's "may edit" does not name;
- sets a task to Ready, or changes the owner's fields on a Ready task;
- starts a task whose hard dependency is not Done;
- lets the builder verify its own work.

A parked task holds, in its file: the question, a recommended answer the owner can veto, and
what changes if he vetoes.

Each task gets a *Decided for you* record, merged with the task: one line per decision the
manager or its agents made alone, giving what was chosen, what was rejected and what would
change it.

Tokens: record what Claude Code reports for each agent run, summed per task. The main
session's own use is not available yet (task 30 looks into it); write "main session: not
recorded" until then.

At the end of a run, write one report the owner reads at his review, newest run first, with
skill-iterate's three sections: *Done* (tasks merged, with tokens), *Decided for you*,
*Needs you* (parked tasks and new Proposed tasks).

`/manage --dry-run` lints, prints the task it would take and why, and changes nothing.

Keep the skill's text short, about the length of skill-iterate's. It points to
`escalation.md` and `DECISIONS.md`; it does not restate them.

## Decided by the owner; do not reopen

- The task list lives in the repo, one file per task.
- Only the owner sets Ready. The manager and its agents may add Proposed tasks.
- Nothing interrupts the owner during a run; tasks are parked.
- The manager merges a verified task itself, one merge commit per task, and never pushes.
- The manager has its own stop list. `escalation.md` applies only inside an iterate task.
- Only these three checks are built now. Other rules stay prose until one is broken; then the
  manager proposes a task to build the check.
- A daily token cap is wanted but not built now.

## Yours to decide

The file format and folder for tasks, the script layout, the review tag's name, how an active
run is marked, agent names, and where the reports and the *Decided for you* records live. Log
each choice in your report under *Decided for you* with its reason.

## Done means

1. All 33 seed tasks exist as task files. A check reads them back and every seed field is
   equal, 33 of 33. The lint passes.
2. The tests pass. They cover at least:
   - protected paths: an edit to `DECISIONS.md` with empty "may edit" fails; the same edit
     with `DECISIONS.md` in "may edit" passes; a change to an existing file under a results
     folder fails; a new results folder passes; an edit to another task's file fails; a new
     Proposed task file passes;
   - push hook: refused while a run is active, allowed otherwise;
   - merge limit: with 3 task merges since the review tag, a fourth is refused.
3. `/manage --dry-run` on the converted list prints task 20.
4. Tasks 31, 32 and 33 are set to Done in the branch's last commit.
5. The branch changes nothing outside: the tasks folder, the manager skill's folder, the
   symlinks, `.claude/settings.json`, the protected-path list and limits config, and
   `manager-build/`. Delete `manager-build/tasks-seed.json` once check 1 passes; keep this
   prompt as the record of the build.

## Report

End with `manager-build/REPORT.md`, in three sections: *Done* (each "done means" item above
with its evidence), *Decided for you*, *Needs you*. Put at most five items under *Needs you*,
each as a recommendation the owner can veto with one line on what changes if he does. Give
every number with what it counts and out of how many.

The owner reviews the branch and merges it himself. This is the first design of the manager,
so his review of the branch is the approval.
