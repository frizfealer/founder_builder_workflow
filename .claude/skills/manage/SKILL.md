---
name: manage
description: Run the repo's task list unattended. Takes the next Ready task, builds or iterates it on its own branch, has another agent verify it, and merges it into the working branch, parking what needs the owner.
argument-hint: "[--dry-run]"
disable-model-invocation: true
---

# manage

The owner commits to tasks by setting them Ready; the manager takes them one at a time and runs
them without asking what is next. It never interrupts the owner during a run. What needs him is
*parked*: the task is set to "Needs you" with the question in its file, and the manager goes on
to another task. He reads one report at his review.

## Terms

- **Task:** one file `tasks/<id>.json` (id zero-padded to 3). Field meanings and who sets each:
  `references/task-fields.md`.
- **Working branch:** `re-create-from-scratch`. Each task gets its own branch, cut from it.
- **Protected path:** a pattern in `protected-paths.txt`. A task may change it only when the
  task's `may_edit` names it; history paths are append-only whatever `may_edit` says.
- **Review tag:** `review/<date>`, set by the owner on the working branch after each review
  (`git tag review/2026-11-20 re-create-from-scratch`; add `-2` for a second review that day).
- **Task merge:** a merge commit on the working branch whose subject starts `Merge task <id>:`.

## Rules

1. Only the owner sets Ready. Once a task is Ready its `done_means`, `verified_by`, `may_edit`,
   `runs_as`, `priority` and `depends_on` are his; the manager drafts them only before then.
2. The manager and its agents may add tasks with status Proposed. When a rule in this skill is
   broken and no script checks it, propose a task to build that check.
3. The builder never verifies its own work. The reviewer gets a fresh context, read-only tools,
   and a brief written from the task file and the diff, not from the builder's report. It
   labels each problem in the task's change or outside it. A problem in the task's change
   fails the review and gets the one fresh retry. Only a problem outside it becomes a Proposed
   task. Every reviewer reply is saved verbatim in `tasks/reviews/`, in the task's merge commit or,
   when the task is parked, its park commit.
4. One merge commit per task. The task file shows Done, `finished` and `tokens` in that merge.
5. Inside an iterate task, skill-iterate's `references/escalation.md` applies as well. Outside
   it, this skill's stop list is the only one. `DECISIONS.md` is the direction every brief
   points to; the manager does not restate it.

## Park, never ask

Park the task when:
- it needs a fact about the owner's product or an outside system that only he knows;
- the protected-path check fails, or verification still fails after one fresh retry;
- `verified_by` includes `you`, or `runs_as` is `you`;
- finishing would need something from the never list.

A parked task's `needs_you` holds the question, a recommended answer the owner can veto, and
what changes if he vetoes.

## Never

Push. Delete a branch, or anything outside the task's own branch. Change a protected path the
task's `may_edit` does not name. Set a task to Ready, or change the owner's fields on a Ready
task. Start a task whose hard dependency is not Done. Let the builder verify its own work.

## What the scripts enforce

All from the repo root, all with `python3`:

- `scripts/tasks.py lint | list | next`: field validity; the task to take (Ready, every hard
  dependency Done; then priority, then most open dependents, then lowest id).
- `scripts/checks.py protected <id> <branch>`: the branch's changes since it left the working
  branch, against `protected-paths.txt` and the working branch's copy of the task's `may_edit`.
  In `tasks/`, a task branch may change only `status`, `finished`, `tokens`, `needs_you` and
  `decided_for_you` of its own task file, and add Proposed tasks. The whole skill folder and
  its three links in `.claude/` are protected.
- `scripts/checks.py merge-limit`: task merges since the latest review tag, against
  `limits.json`. At the limit the manager merges nothing more and ends the run.
- `scripts/checks.py review <id>`: the task's highest-numbered reply in
  `tasks/reviews/<id>-<n>.md`, in the working tree during the merge. It refuses the merge when
  no reply is saved or the latest's first line is not `VERDICT: PASS`. A task verified by
  neither `reviewer` nor `script` has no reviewer and passes.
- `scripts/checks.py run-start | run-end`: mark a run active with `.git/manage-run-active`.
  While it exists, the `PreToolUse` hook in `.claude/settings.json` refuses any Bash command
  whose text runs `git push`, for the main session and every subagent. It reads command text,
  so it is an early stop, not proof: an alias, a script or `gh` can still push. If a run
  crashed and left the marker, the owner deletes the file.

Tests: `uv run --with pytest pytest .claude/skills/manage/tests`. They run in temporary git repos.

Every other rule here is prose until it is broken once.

## Commands and agents

- `/manage [--dry-run]`: one run, `commands/manage.md`.
- `manager-builder` (`agents/builder.md`) and `manager-reviewer` (`agents/reviewer.md`).

## Installing in a repo

Link the command and agents (the skill folder stays the source), then open a new session:

```
ln -s ../skills/manage/commands/manage.md   .claude/commands/manage.md
ln -s ../skills/manage/agents/builder.md    .claude/agents/manager-builder.md
ln -s ../skills/manage/agents/reviewer.md   .claude/agents/manager-reviewer.md
```

## Records

- Each task's file: `decided_for_you` (one entry per decision made without the owner: chosen,
  rejected, what would change it), `needs_you` when parked, `tokens`.
- `tasks/reviews/<id>-<n>.md`: each reviewer reply verbatim, in the task's merge or park commit.
- `tasks/RUNS.md`: one report per run, newest first, in skill-iterate's three sections.
