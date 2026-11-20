---
name: manage
description: Run the repo's task list unattended. Takes up to N independent Ready tasks at once, builds or iterates each on its own branch in its own worktree, has another agent verify it, and merges them into the working branch one at a time, parking what needs the owner.
argument-hint: "[--dry-run]"
disable-model-invocation: true
---

# manage

The owner commits to tasks by setting them Ready; the manager takes up to N of them at a time,
independent of each other, builds them side by side, and runs them without asking what is next.
It never interrupts the owner during a run. What needs him is *parked*: the task is set to
"Needs you" with the question in its file, and the manager goes on to another task. He reads one
report at his review.

While a run is active, your own commit on the working branch, or your edit to a tracked file in
the main folder, ends that run at the next `checks.py main-folder`: the manager dispatches,
merges and parks nothing more. Nothing is lost: every task branch and worktree stays, and the
next run reports them. To work meanwhile, use a worktree of your own on another branch, outside
`build/worktrees/` (`git worktree add ../my-work -b my-work`), or another clone; a run leaves both
alone.

## Terms

- **Task:** one file `tasks/<id>.json` (id zero-padded to 3). Field meanings and who sets each:
  `references/task-fields.md`.
- **Working branch:** `re-create-from-scratch`. Each task gets its own branch, cut from it.
- **Protected path:** a pattern in `protected-paths.txt`. A task may change it only when the
  task's `may_edit` names it; history paths are append-only whatever `may_edit` says.
- **Review tag:** `review/<date>`, set by the owner on the working branch after each review
  (`git tag review/2026-11-20 re-create-from-scratch`; add `-2` for a second review that day).
- **Task merge:** a merge commit on the working branch whose subject starts `Merge task <id>:`.
- **Main folder:** the repo's own folder. It stays on the working branch for the whole run.
- **Worktree:** a task's own git worktree, `build/worktrees/<branch>` with each `/` as `-`
  (`build/worktrees/task-058`), on its task branch. `build/` is git-ignored, so the main folder
  shows no change, and the folder is inside the project, so agents need no extra permission.
- **Batch:** the tasks a run takes together, at most `tasks_at_once` in `limits.json` (the owner
  sets it; 1 gives one task at a time).

## Rules

1. Only the owner sets Ready. Once a task is Ready its `done_means`, `verified_by`,
   `verifier_of_line`, `may_edit`, `may_delete`, `runs_as`, `priority`, `depends_on` and `tags`
   are his; the manager drafts them only before then.
2. An agent creates a task in one case only: a problem that existed before the task's branch and
   lies outside its change. Such a task is Proposed, and its `outside_problems` names each
   earlier file and the problem in it. A task run adds at most one, the builder's and the
   manager's together; `checks.py protected` fails a branch that adds one without
   `outside_problems` naming a file that existed when the branch left, or adds two. A problem in
   lines the task's own branch added or changed is the task's to fix (rule 3), in its fix pass
   or, when it parks, through its `for_retry`, and never becomes a task. A builder that needs a
   protected path its task may not edit does not propose a task either: the task parks
   (`never`) with that path in the question. A rule of this skill that is broken with no script
   to check it is an earlier problem too, and the manager proposes a task to build that check.
3. The builder never verifies its own work. The reviewer gets a fresh context, read-only tools,
   and a brief written from the task file and the diff, not from the builder's report. It
   labels each problem blocking, minor or outside the change; `agents/reviewer.md` defines the
   labels. Only a blocking problem fails the review. A fail
   gets one fresh retry, whose builder fixes the blocking problems and changes nothing else.
   If the retry fails too, the park that follows consults the advisor (rule 7, job b), and one
   `GO ON` from it per task run can send one more fresh builder briefed with its reply.
   Fix it here: the minor problems on lines the task's own branch added or changed
   (`checks.py unmerged`) are fixed before the merge, in one fix pass. Its builder gets only
   that list, and its re-check looks only at those fixes. A blocking problem stays the only
   reason a review fails, and whatever is still open after the one pass stays in the review
   file and creates no task. Every reviewer reply is saved verbatim in `tasks/reviews/`, in the
   task's merge commit or, when the task is parked, its park commit.
4. One merge commit per task. The task file shows Done, `finished` and `tokens` in that merge.
5. Inside an iterate task, skill-iterate's `references/escalation.md` applies as well. Outside
   it, this skill's stop list is the only one. `DECISIONS.md` is the direction every brief
   points to; the manager does not restate it.
6. A stop or choice that can be decided mechanically is decided by a script, not by the
   manager reading text. Two cases came from task 49: whether a task's outside needs are met is
   checked before its builder starts (`checks.py needs`), not found after the build; and whether
   a review or builder finding belongs to the task itself is decided from the file and lines it
   names (`checks.py unmerged`): a finding on a file only the branch has, or on lines the branch
   added or changed since it left the working branch, is the task's own, for its fix pass or its
   `for_retry`, and not for a Proposed task. Whether the owner has done
   his check is a field the owner sets, `owner_verified`, read by `checks.py owner`; the manager
   never sets it and never infers it from other text. Whether a task's leftover branch may be
   deleted is decided by `checks.py superseded`, not by git's `-d`, which refuses an earlier
   attempt whose work the retry copied as a new commit (tasks 28, 36 and 49).
7. The advisor (`agents/advisor.md`) gets a fresh context and read-only tools, like the reviewer,
   and has four jobs: (a) verify the `done_means` lines assigned to it, given only the paths the
   line names (its Read tool can open any file in the repo, so only the brief keeps a blind check
   blind; no tool enforces it); for a line that compares labels with verdicts it must not see, it
   gives the labels, and the manager writes them to a labels file and runs the comparison command
   the line names; (b) before a park, say whether the task can go on without the owner,
   and how; (c) when a builder's decision changes what a line proves, say whether the line still
   proves what it was written to prove; (d) after a merge, review the manager's draft of the
   fields of a Proposed task that hard-depends on the merged one and has an empty `done_means`:
   it rules HOLDS or FAILS on whether each pass line can be checked and traces back to a finding
   or a result, and lists anything in the draft that is new scope, which it names and does not
   add. The advisor writes no field; the task stays Proposed. What it never
   decides is decided by a script, `checks.py consult`: the always-park cases below. Every advisor
   reply is saved verbatim in `tasks/advice/<id>-<n>.md` and its ruling is logged under
   `decided_for_you` with what would change it.
8. Tasks run side by side only when `tasks.py batch` finds them independent: no hard dependency
   between them in either direction, no protected path named in both `may_edit`, and at most
   one iterate task per skill (another task may run beside an iterate task). Tags are not part
   of the test. Each task's builder and verifiers work only in its worktree, on its branch.
   Only the manager commits in the main folder, and only on the working branch;
   `checks.py main-folder` checks that after every agent that can write returns. Merges stay
   one at a time.
   Before each merge after the first of a run, `checks.py try-merge` runs the task's checks on
   its branch merged with the updated working branch; a conflict or a failing check sends the
   task back to its builder once, on a branch cut from the updated working branch, and a second
   failure parks it. An iterate result parks when a task that merged meanwhile changed its
   skill's folder or its eval folder (`checks.py stale`), since it was measured on an older
   version. Claude Code's Agent `cwd` parameter and `isolation: "worktree"` do not keep a
   subagent's Bash in a folder. On 2026-11-17 (`tasks/advice/061-1.md`), with `cwd` the
   builders' Bash ran in the main folder; with `isolation: worktree` the builders worked in their
   own worktree, and their Bash still wrote to the main folder when told to. So the manager makes
   each worktree itself, and the brief and `checks.py main-folder` keep the builder in it.

## Park, never ask

Park the task when one of these holds. Each case has a reason, in backticks. Before every park
the manager runs `checks.py consult <id> <reason> [<branch>]`: for a case marked *always* it exits
1 and the task parks without the advisor; for any other case it exits 0 and the advisor (job b) is
consulted first. The script also checks for itself each always-park condition the repo shows: a
line verified by `you` with `owner_verified` empty, `runs_as` `you`, the protected-path check on
the task's branch, the outside-need check, the task limit. When one holds, the task always parks,
whatever the reason. Money, accounts, owner's fields, Ready and the never list have no state to
read, so for them the reason alone decides.
- `needs`, *always*: `checks.py needs <id>` fails, an outside need is not met. Park before any
  branch or builder, with the script's reason as the question;
- `owner-fact`: it needs a fact about the owner's product or an outside system that only he knows;
- `protected`, *always*: the protected-path check fails;
- `verification`: verification still fails after its one fresh retry (a review, an advisor
  line, or the advisor's check of a builder's decision);
- `never`, *always*: a blocking problem can be fixed only in a protected path the task's
  `may_edit` does not name (park at once, with no retry, and name that path in the
  recommendation), the builder stops because `done_means` needs such a path, or finishing would
  need anything else from the never list;
- `owner`, *always*: `checks.py owner <id>` fails, a line is verified by `you` and
  `owner_verified` is empty. It parks after every other verifier, the advisor's lines included,
  and its question names only the owner's lines. Once the owner has set `owner_verified`, the
  task is not parked for him again;
- `runs-as-you`, *always*: `runs_as` is `you`;
- `money`, `owner-field`, `set-ready`, *always*: finishing would spend money or touch an account,
  change an owner's field, or set a task to Ready. A builder spends money (`claude -p`, `ant`, a
  paid API call) only when its task's `outside_needs` names the need (`claude-api`); otherwise it
  stops, and the task parks (`money`);
- `iterate`: an iterate task's result is not kept, or its *Needs you* holds an item;
- `merge-limit`, *always*: `checks.py merge-limit` refuses the merge; the task limit is the
  owner's own control;
- `review`, `advice`, *always*: `checks.py review` or `advice` refuses the merge after
  verification passed in step 5;
- `conflict`, *always*: `checks.py try-merge` fails for the task a second time in the run, on
  its rebuild (exit 3), or cannot run (exit 2);
- `stale`, *always*: `checks.py stale` fails, an iterate result was measured on an older version
  of its skill.

A parked task's `needs_you` holds the question, a recommended answer the owner can veto, and
what changes if he vetoes.

## Never

Push. Delete a branch, except with `git branch -D` a branch of the merged task that `checks.py
superseded` has just confirmed (step 7 of `commands/manage.md`). Run `git clean`. Delete or
rename a file the working branch held when the task's branch left it, unless the task's
`may_delete` names it. Delete anything outside the task's own branch. Change a protected path the
task's `may_edit` does not name. Set a task to Ready, or change the owner's fields on a Ready
task. Start a task whose hard dependency is not Done. Let the builder verify its own work.
Switch the main folder to another branch during a run. Remove a worktree with `--force`, or one
outside `build/worktrees/`.

## What the scripts enforce

All from the repo root, all with `python3`:

- `scripts/tasks.py lint | list | next`: field validity; the task to take (Ready, every hard
  dependency Done; then priority, then most open dependents, then lowest id).
- `scripts/tasks.py batch [<n>]`: the batch, in `next`'s order: a task joins when it is
  independent (rule 8) of every task already taken, up to `n`, which defaults to `tasks_at_once`
  in `limits.json`. An iterate task's skill is the one folder of `.claude/skills/` its title or
  item names as a whole name; one that names none, or two, counts as iterating every skill. Its
  `why:` line names each takeable task left out and the reason.
- `scripts/checks.py protected <id> <branch>`: the branch's changes since it left the working
  branch, against `protected-paths.txt` and the working branch's copy of the task's `may_edit`.
  In `tasks/`, a task branch may change only `status`, `finished`, `tokens`, `needs_you` and
  `decided_for_you` of its own task file, read against that file's copy at the fork point, so a
  field the owner set on the working branch since then is not the branch's change; it cannot set
  `owner_verified` or `for_retry`. It may add one Proposed task, whose `outside_problems` names,
  for each problem, a file that existed when the branch left and the problem (rule 2). The whole
  skill folder and
  its four links in `.claude/` are protected, and so are `tasks/reviews/` and `tasks/advice/`:
  only the manager writes there, on the working branch. It also fails each file the branch
  deletes or renames that existed on the working branch at the fork point, unless the working
  branch's copy of the task's `may_delete` names it; it reads git's record of the change, so it
  does not matter which command deleted it. A file the branch added itself may go freely.
- `scripts/checks.py superseded <branch>`: exits 0 when the branch is superseded, so the manager
  may delete it with `git branch -D`: its name is `task/<id>` or `task/<id>-<n>`; task `<id>` is
  Done on the working branch and its task merge is on it; and no worktree, the main folder
  included, has it checked out. It prints the branch's last commit id, which restores it with
  `git branch <name> <id>` while git still holds the commit. Otherwise it exits 1 with one line
  for the run report: each condition that failed, how many files differ from the working branch
  and how many exist only on the branch, and a recommendation, delete or keep, with its reason.
  Exit 2 when the name is not a branch. A branch of a task that is not Done, or one not named
  for a task, never passes.
- `scripts/checks.py merge-limit`: task merges since the latest review tag, against
  `limits.json`. At the limit the manager merges nothing more and ends the run.
- `scripts/checks.py review <id>`: the task's highest-numbered reply in
  `tasks/reviews/<id>-<n>.md`, in the working tree during the merge. It refuses the merge when
  no reply is saved or the latest's first line is not `VERDICT: PASS`. A task verified by
  neither `reviewer` nor `script` has no reviewer and passes.
- `scripts/checks.py needs <id>`: runs one check per entry of the task's `outside_needs` and
  exits 1 with a one-line reason at the first that fails. For `claude-api` the check is one
  call with one output token to the smallest model through the ant CLI, with the credentials a
  builder would use; it costs under 0.01 USD and prints no credential.
- `scripts/checks.py unmerged <branch> <path>[:<line>[-<line>]]...`: one argument per finding,
  with the lines it names in the branch's copy. Exits 0 when every finding is the task's own: its
  file did not exist when the branch left the working branch, or a line it names is one the
  branch added or changed (its diff against the fork point; a deletion counts the lines on either
  side). Those go to the task's fix pass, or its `for_retry` when it parks. Exits 1 otherwise: a
  finding on lines the branch left as they were, or on an earlier file with no line named, is an
  earlier problem.
- `scripts/checks.py owner <id>`: exits 1 while a line of `done_means` is verified by `you`
  (`verified_by` and `verifier_of_line`) and `owner_verified` is empty on the working branch. Its
  output names only the owner's lines.
- `scripts/checks.py advice <id>`: for each line the advisor verifies and `you` does not, the
  highest-numbered reply in `tasks/advice/<id>-<n>.md` whose second line is `JOB: a (<line>)`, in
  the working tree during the merge. It refuses the merge when a line has none or the latest's
  first line is not `RULING: HOLDS`.
- `scripts/checks.py consult <id> <reason> [<branch>]`: exits 1 for an always-park case of the
  park list, or when an always-park condition the repo shows holds, whatever the reason; 0 when
  the advisor is consulted first; 2 for a reason not in the list; 3 when it cannot decide, because
  the working branch holds no file for the task or the branch does not exist. `<branch>` is the
  task's branch, left out when there is none. For a task whose `outside_needs` names
  `claude-api`, it re-runs the paid check of `checks.py needs` on every park, under 0.01 USD each.
- `scripts/checks.py drafts <id>`: the Proposed tasks that hard-depend on the task and have an
  empty `done_means`, one id per line, whose fields the manager drafts and the advisor reviews
  (job d).
- `scripts/checks.py run-start | run-end`: mark a run active with `.git/manage-run-active`.
  While it exists, the `PreToolUse` hook in `.claude/settings.json` (`checks.py push-hook`)
  reads the text of every Bash command, for the main session and every subagent, and refuses
  with exit 2:
  - a command that runs `git push` or `git clean`;
  - a forced branch deletion (`git branch -D`, `--delete --force`, `-d -f`, `-df`, and git's
    abbreviations of the long options, such as `--del --forc`), except the manager's cleanup
    step: `git branch -D <name>` alone in its command, once `checks.py superseded <name>`
    passes. So it refuses one whose text holds `$` or a backtick, that runs anything besides the
    one `git branch` call, or that points git at another repository (`-C`, `--git-dir`, a
    `GIT_DIR=` prefix), even for a confirmed branch;
  - a `git merge` of a task branch (`task/<id>`, `task/<id>-<n>`) unless `checks.py protected`,
    `owner`, `review`, `advice` and `merge-limit` all pass for its task, read in the main folder,
    and any `git merge` whose text holds `$` or a backtick;
  - `claude -p` (`--print`) or `ant`, unless the command's text or its folder names the worktree
    of a task (`build/worktrees/task-<id>`, a rebuild's `-<n>` included) whose file on the
    working branch has `claude-api` in `outside_needs`. The refusal tells the agent to stop and
    report it, and the task parks (`money`).

  When a refused command also runs `git commit`, the refusal ends by saying that a message that
  only names the refused command goes in single quotes or in a file given with `-F`.
  It reads command text, so it is an early stop, not proof. It misses an alias, a script, an SDK
  call or `gh`, any of which can push, merge or spend money; a program that another program
  starts (`find -exec`); a merge written as a commit id or as `git pull`, and the merge of an
  iterate branch, whose name holds no task id; and a `-m` that sits inside another quoted string,
  a heredoc body or a comment, or `bash -cm`, the three forms recorded in
  `tasks/advice/058-2.md`, which can hide a command after them. It does not try to stop `rm`,
  which builders use on their own temporary files. It over-refuses too: a heredoc or other text
  that only quotes a push or a paid command is refused like the command itself, and so is
  `claude -p` or `ant` in an iterate worktree. A `-m` or `--message` argument that bash runs
  nothing in is a message, not commands: a single-quoted argument, or a double-quoted one with no
  backtick and no `$(`. Any other message, a heredoc's included, is read as commands like the
  rest; write such a message to a file and commit with `git commit -F <file>`. The task merge's
  commit always takes that form: its subject, `Merge task <id>: <title>`, is written with the
  Write tool to `build/merge-message-<id>.txt` and committed with `git commit -F
  build/merge-message-<id>.txt`, so bash expands nothing in the title. If a run
  crashed and left the marker, the owner deletes the file. The marker also holds the run's
  state: the working branch's commit at the start, each failed `try-merge`, each agent's tokens.
  `run-start` then removes each worktree under `build/worktrees/` that holds no uncommitted
  change (its branch stays), and prints a line for each one that does, left as it is, and for
  each task left In progress, with a recommendation.
- `scripts/checks.py main-folder`: exits 1 unless the main folder is on the working branch with
  no change to a tracked file, and every commit the working branch gained since `run-start` is
  a task merge or a `task <id>: in progress | parked | drafted from task <id>` commit that changes
  only files under `tasks/`. It does not see a new untracked file.
- `scripts/checks.py try-merge <id> <worktree> [<command>...]`: in the task's worktree, merges
  the working branch with `--no-commit`, runs each command there, and undoes the merge. Exit 0
  when it merges and every command passes. On a conflict or a failing command: exit 1 the first
  time for the task in the run (rebuild once) and 3 after that (park); exit 2 when it cannot run.
- `scripts/checks.py stale <skill> <branch>`: exits 1 when the working branch changed
  `.claude/skills/<skill>/` or `eval/<skill>/` since the branch left it.
- `scripts/checks.py tokens [<id> <n>]`: adds an agent's tokens to its task's count for the run;
  with no arguments, prints each task's count and the total.

Tests: `uv run --with pytest pytest .claude/skills/manage/tests`. They run in temporary git repos.

Every other rule here is prose until it is broken once.

## Commands and agents

- `/manage [--dry-run]`: one run, `commands/manage.md`.
- `manager-builder` (`agents/builder.md`), `manager-reviewer` (`agents/reviewer.md`) and
  `manager-advisor` (`agents/advisor.md`).

## Installing in a repo

Link the command and agents (the skill folder stays the source), then open a new session:

```
ln -s ../skills/manage/commands/manage.md   .claude/commands/manage.md
ln -s ../skills/manage/agents/builder.md    .claude/agents/manager-builder.md
ln -s ../skills/manage/agents/reviewer.md   .claude/agents/manager-reviewer.md
ln -s ../skills/manage/agents/advisor.md    .claude/agents/manager-advisor.md
```

## Records

- Each task's file: `decided_for_you` (one entry per decision made without the owner: chosen,
  rejected, what would change it), `needs_you` when parked, `for_retry` when parked with
  findings on files or lines only its branch has, `tokens`. With tasks side by side, every agent's
  description starts `task <id>:`, so each result, its tokens and its decisions belong to one
  task; `checks.py tokens` counts the tokens per task.
- `tasks/reviews/<id>-<n>.md`: each reviewer reply verbatim, in the task's merge or park commit.
- `tasks/advice/<id>-<n>.md`: each advisor reply verbatim, in the task's merge or park commit,
  or for job (d) in the drafted task's commit.
- `tasks/RUNS.md`: one report per run, newest first, in skill-iterate's three sections. It lists
  each branch the manager deleted with its last commit id, and makes the case for each leftover
  task branch it kept.
