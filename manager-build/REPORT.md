# Manager build: the task list, three checks, the manager skill   (manager/build, 2026-11-15)

Branch `manager/build`, cut from `re-create-from-scratch` at `0c27a00`. Four commits: tasks 31,
33 and 32, then this report with tasks 31 to 33 set to Done. Nothing was merged or pushed, and
the manager was not run for real.

## Done

1. **33 of 33 seed tasks exist as task files, every seed field equal; the lint passes.**
   `python3 manager-build/seed.py check` printed `33 of 33 seed tasks equal in every seed field`
   (run after conversion and again before the last commit). `tasks.py lint` prints
   `33 task(s), 0 problem(s)`. `draft_note` and `tokens: null` carried over unchanged.
   `manager-build/tasks-seed.json` was then deleted; `seed.py` stays as the record.
2. **The tests pass: 41 of 41.**
   `uv run --with pytest pytest .claude/skills/manage/tests`. Each runs in a temporary git repo.
   - Protected paths, 15 tests, including every case the prompt lists: a `DECISIONS.md` edit
     fails with empty may edit and passes when may edit names it; a changed existing results
     file fails; a new results folder passes; an edit to another task's file fails; a new
     Proposed task file passes. Also: a branch that adds `DECISIONS.md` to its own may edit
     still fails.
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
3. **`/manage --dry-run` prints task 20.** Run in a fresh headless session
   (`claude -p "/manage --dry-run"`): lint `33 task(s), 0 problem(s)`, merge limit `0 task
   merge(s) ... the limit is 3`, next `task 20: /grade commits its verdicts`. HEAD, tracked
   files and branches were unchanged afterwards and no marker was left.
4. **Tasks 31, 32 and 33 are Done in the branch's last commit**, with `finished` 2026-11-15,
   tokens and their *Decided for you* records. Task 32's `verified_by` includes `you`; your
   review of this branch is that verification.
5. **The branch changes only the allowed paths.** `git diff --name-only
   re-create-from-scratch...manager/build` lists 52 files, all under `tasks/` (33),
   `.claude/skills/manage/` (12), the 3 symlinks, `.claude/settings.json`, and
   `manager-build/` (`PROMPT.md`, `seed.py`, `REPORT.md`). The 8 untracked paths outside
   `manager-build/` were left alone.

Tokens: task 31, 0 agent tokens; task 32, 116,946 (the dry-run session); task 33, 83,000 (the
agent that read the hook docs). Main session: not recorded.

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

## Needs you

1. **Merge `manager/build` into `re-create-from-scratch`, then tag it `review/2026-11-15`, then
   open a new session before `/manage`.** The command, agents and hook load at session start.
   If you veto the tag, the first run counts from the start of history, where there are 0 task
   merges, so the effect is the same until your first review.
2. **Keep append-only as "an existing file may only grow at its end".** `/iterate` step 7
   appends to `EXPERIMENTS.md`, so the strict reading in the prompt ("a changed existing file
   fails") would fail every iterate task. If you veto, I make the check strict and every
   iterate task parks at the protected-path check.
3. **Keep answering `/iterate`'s standing merge / revert question with the keep rule.** Every
   iterate report lists that question under *Needs you*, so "anything under *Needs you* parks
   the task" would park every iterate task. Any other item there still parks. If you veto,
   every iterate task parks for your merge decision.
4. **Keep the push hook failing open.** If the hook script cannot start, the push goes
   through. The alternative, `onFailure: block`, needs Claude Code v2.1.295 or later, and a
   broken script would then block every Bash call in every session. If you veto, I add
   `"onFailure": "block"` to `.claude/settings.json`.
5. **Do not work in the same checkout during a run.** The manager switches branches and merges
   in the checkout where `/manage` starts. If you veto, a run needs its own worktree, and the
   working branch has to be checked out there and nowhere else.
