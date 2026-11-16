# Manager build: the task list, three checks, the manager skill   (manager/build, 2026-11-15)

Branch `manager/build`, cut from `re-create-from-scratch` at `0c27a00`. Six commits: tasks 31,
33 and 32; the report with tasks 31 to 33 set to Done; the protected-check fix after your first
review; this update with two Proposed tasks. Nothing was merged or pushed, and the manager was
not run for real.

## Done

1. **33 of 33 seed tasks exist as task files, every seed field equal; the lint passes.**
   `python3 manager-build/seed.py check` printed `33 of 33 seed tasks equal in every seed field`
   (run after conversion and again before the last commit). `tasks.py lint` prints
   `33 task(s), 0 problem(s)`. `draft_note` and `tokens: null` carried over unchanged.
   `manager-build/tasks-seed.json` was then deleted; `seed.py` stays as the record.
2. **The tests pass: 45 of 45.**
   `uv run --with pytest pytest .claude/skills/manage/tests`. Each runs in a temporary git repo.
   - Protected paths, 19 tests, including every case the prompt lists: a `DECISIONS.md` edit
     fails with empty may edit and passes when may edit names it; a changed existing results
     file fails; a new results folder passes; an edit to another task's file fails; a new
     Proposed task file passes. Also: a branch that adds `DECISIONS.md` to its own may edit
     still fails; a branch that rewrites its own task's `done_means`, `verified_by`, `may_edit`
     and `priority` fails; an edit to the manager's `SKILL.md`, `agents/reviewer.md` or the
     `/manage` link fails.
   - Push hook, 10 tests, run as Claude Code runs it (JSON on stdin, exit code back): 4 push
     forms refused with exit 2 while a run is active; allowed outside a run and after the run
     ends; `git stash push` and 2 other non-pushes allowed during a run.
   - Merge limit, 4 tests: 3 task merges since the review tag refuses a fourth; merges before
     the tag are not counted; with no tag every task merge counts; non-task merges are not counted.
   - Tasks script, 12 tests on lint and next.
   - Each check's tests were shown to catch a break: 6 deliberate code breaks (hook never
     blocks, limit off by one, no append-only rule, may edit read from the task branch, any new
     task accepted, any task edit accepted) each failed 1 to 4 tests; the code was restored.
   - Live: in this session the hook refused `true || git push` while `.git/manage-run-active`
     existed and allowed it after `run-end`.
   - Live, inside a subagent: with the run marked active, a subagent (haiku) ran
     `cd <repo> && true || git push`. The hook refused it before the shell ran, with the same
     message ("Refused: a manager run is active, and the owner pushes. ..."). The subagent ran
     no other command, and `git ls-remote --heads origin 'manager/*'` lists 0 branches.
3. **`/manage --dry-run` prints task 20.** Run in a fresh headless session
   (`claude -p "/manage --dry-run"`): lint `33 task(s), 0 problem(s)`, merge limit `0 task
   merge(s) ... the limit is 3`, next `task 20: /grade commits its verdicts`. HEAD, tracked
   files and branches were unchanged afterwards and no marker was left.
4. **Tasks 31, 32 and 33 are Done in the branch's last commit**, with `finished` 2026-11-15,
   tokens and their *Decided for you* records. Task 32's `verified_by` includes `you`; your
   review of this branch is that verification.
5. **The branch changes only the allowed paths.** `git diff --name-only
   re-create-from-scratch...manager/build` lists 54 files, all under `tasks/` (35),
   `.claude/skills/manage/` (12), the 3 symlinks, `.claude/settings.json`, and
   `manager-build/` (`PROMPT.md`, `seed.py`, `REPORT.md`). The 8 untracked paths outside
   `manager-build/` were left alone.

Tokens: task 31, 0 agent tokens; task 32, 116,946 (the dry-run session); task 33, 125,103
(83,000 for the agent that read the hook docs, 42,103 for the subagent hook test). Main
session: not recorded.

### Fixed after your first review

Two holes in `checks.py protected`, both reproduced first: in a clone of this branch, a task
branch that rewrote task 20's `done_means`, `verified_by`, `may_edit` and `priority` and edited
the manager's `SKILL.md` and `agents/reviewer.md` passed with 0 failures. With the fix, the same
branch fails with 3 (the two skill files and the task file). One commit, `71c5d3c`:

1. A task branch's own task file may differ from the working branch's copy only in `status`,
   `finished`, `tokens`, `needs_you` and `decided_for_you`.
2. `protected-paths.txt` names the whole `.claude/skills/manage/` folder and its three links
   (`.claude/agents/manager-builder.md`, `.claude/agents/manager-reviewer.md`,
   `.claude/commands/manage.md`), in place of the four separate lines for the list, limits,
   scripts and tests.

The 4 new tests failed before the fix for that reason (0 failures returned) and pass after it.

### Proposed tasks added

- **Task 34, recover from an interrupted manager run:** a stale run marker, the checkout left
  on a task branch, a task left In progress.
- **Task 35, run the manager in its own worktree**, so you can work in the repo during a run.
  Soft dependency on 34.

Both have drafted `done_means`, `verified_by`, `runs_as` and `may_edit`. Priority is left for
you, since only you set it.

## Decided for you

Each line is also in the task's own file under `decided_for_you`, with what was rejected and
what would change it.

- Tasks are JSON, one file each, `tasks/<id>.json`: the repo's scripts use only Python's
  standard library, which has no YAML parser.
- Scripts: `.claude/skills/manage/scripts/tasks.py` (lint, list, next) and `checks.py`
  (protected, merge-limit, run-start, run-end, push-hook). The protected-path list and
  `limits.json` sit beside them in the skill folder.
- A run is marked active by `.git/manage-run-active`. A tracked file would need a `.gitignore`
  change outside the allowed paths, and a running session cannot set an environment variable
  for its hooks.
- The review tag is `review/<date>`, for example `review/2026-11-20`; the check uses the
  nearest such tag on the working branch.
- A task merge is a merge commit whose subject starts `Merge task <id>:`.
- The protected list and the task's may edit are read from the working branch, so a task
  branch cannot grant itself an edit.
- Agents are `manager-builder` and `manager-reviewer`, both opus and high. The reviewer has
  Read, Grep and Glob only. For `script` it names the commands and the manager runs them.
- Run reports go in `tasks/RUNS.md`, newest first. Parking commits only that task's file on
  the working branch, and the task branch stays.
- `next` counts direct dependents, hard and soft, among tasks not Done or Dropped.
- One fresh retry means a new builder with the reviewer's findings, then a new reviewer.
- The skill is user-invoked (`disable-model-invocation: true`), like the repo's other skills.

## Your rulings, 2026-11-15

Kept as built: append-only lets an existing file grow at its end; `/iterate`'s standing merge /
revert question is answered by the keep rule; the push hook fails open; you do not work in the
same checkout during a run (task 35 would lift this).

## Needs you

1. **Merge `manager/build` into `re-create-from-scratch`, then tag it `review/2026-11-15`, then
   open a new session before `/manage`.** The command, agents and hook load at session start.
   If you veto the tag, the first run counts from the start of history, where there are 0 task
   merges, so the effect is the same until your first review.
2. **Set a priority on tasks 34 and 35, and set them Ready if you want them run.** I recommend
   34 high: until it is built, a crashed run leaves a marker that blocks your pushes until you
   delete `.git/manage-run-active` by hand. If you leave them Proposed, `/manage` never takes them.
