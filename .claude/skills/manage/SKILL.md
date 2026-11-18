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

1. Only the owner sets Ready. Once a task is Ready its `done_means`, `verified_by`,
   `verifier_of_line`, `may_edit`, `runs_as`, `priority`, `depends_on` and `tags` are his; the
   manager drafts them only before then.
2. The manager adds at most one Proposed task per task run, bundling the review findings worth
   doing. The builder proposes a task only when `done_means` needs a protected path its
   `may_edit` does not name. When a rule in this skill is broken and no script checks it, the
   manager proposes a task to build that check.
3. The builder never verifies its own work. The reviewer gets a fresh context, read-only tools,
   and a brief written from the task file and the diff, not from the builder's report. It
   labels each problem blocking, minor or outside the change; `agents/reviewer.md` defines the
   labels. Only a blocking problem fails the review. A fail
   gets one fresh retry, whose builder fixes the blocking problems and changes nothing else.
   If the retry fails too, the park that follows consults the advisor (rule 7, job b), and one
   `GO ON` from it per task run can send one more fresh builder briefed with its reply.
   Minor and outside problems stay in the review file. Every reviewer reply is saved verbatim
   in `tasks/reviews/`, in the task's merge commit or, when the task is parked, its park commit.
4. One merge commit per task. The task file shows Done, `finished` and `tokens` in that merge.
5. Inside an iterate task, skill-iterate's `references/escalation.md` applies as well. Outside
   it, this skill's stop list is the only one. `DECISIONS.md` is the direction every brief
   points to; the manager does not restate it.
6. A stop or choice that can be decided mechanically is decided by a script, not by the
   manager reading text. Two cases so far, both from task 49: whether a task's outside needs
   are met is checked before its builder starts (`checks.py needs`), not found after the build;
   and whether review or builder findings belong to the task's own retry, because the files they
   name exist only on the task's branch, is decided from the paths (`checks.py unmerged`), so
   they go into that task's `for_retry` and not into a Proposed task. Whether the owner has done
   his check is a field the owner sets, `owner_verified`, read by `checks.py owner`; the manager
   never sets it and never infers it from other text.
7. The advisor (`agents/advisor.md`) gets a fresh context and read-only tools, like the reviewer,
   and has four jobs: (a) verify the `done_means` lines assigned to it, given only the paths the
   line names (its Read tool can open any file in the repo, so only the brief keeps a blind check
   blind; no tool enforces it); (b) before a park, say whether the task can go on without the owner,
   and how; (c) when a builder's decision changes what a line proves, say whether the line still
   proves what it was written to prove; (d) after a merge, draft the fields of a Proposed task that
   hard-depends on the merged one and has an empty `done_means`, which stays Proposed. What it never
   decides is decided by a script, `checks.py consult`: the always-park cases below. Every advisor
   reply is saved verbatim in `tasks/advice/<id>-<n>.md` and its ruling is logged under
   `decided_for_you` with what would change it.

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
  recommendation), or finishing would need anything else from the never list;
- `owner`, *always*: `checks.py owner <id>` fails, a line is verified by `you` and
  `owner_verified` is empty. It parks after every other verifier, the advisor's lines included,
  and its question names only the owner's lines. Once the owner has set `owner_verified`, the
  task is not parked for him again;
- `runs-as-you`, *always*: `runs_as` is `you`;
- `money`, `owner-field`, `set-ready`, *always*: finishing would spend money or touch an account,
  change an owner's field, or set a task to Ready;
- `iterate`: an iterate task's result is not kept, or its *Needs you* holds an item;
- `merge-limit`, *always*: `checks.py merge-limit` refuses the merge; the task limit is the
  owner's own control;
- `review`, `advice`, *always*: `checks.py review` or `advice` refuses the merge after
  verification passed in step 5.

A parked task's `needs_you` holds the question, a recommended answer the owner can veto, and
what changes if he vetoes.

## Never

Push. Delete a branch, except the merged task's own branches with `git branch -d` (step 7 of
`commands/manage.md`). Delete anything outside the task's own branch. Change a protected path the
task's `may_edit` does not name. Set a task to Ready, or change the owner's fields on a Ready
task. Start a task whose hard dependency is not Done. Let the builder verify its own work.

## What the scripts enforce

All from the repo root, all with `python3`:

- `scripts/tasks.py lint | list | next`: field validity; the task to take (Ready, every hard
  dependency Done; then priority, then most open dependents, then lowest id).
- `scripts/checks.py protected <id> <branch>`: the branch's changes since it left the working
  branch, against `protected-paths.txt` and the working branch's copy of the task's `may_edit`.
  In `tasks/`, a task branch may change only `status`, `finished`, `tokens`, `needs_you` and
  `decided_for_you` of its own task file, and add Proposed tasks; so it cannot set
  `owner_verified` or `for_retry`. The whole skill folder and
  its four links in `.claude/` are protected, and so are `tasks/reviews/` and `tasks/advice/`:
  only the manager writes there, on the working branch.
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
- `scripts/checks.py unmerged <branch> <path>...`: exits 0 when every path exists on the branch
  and not on the working branch (the findings go to the task's `for_retry`), 1 otherwise.
- `scripts/checks.py owner <id>`: exits 1 while a line of `done_means` is verified by `you`
  (`verified_by` and `verifier_of_line`) and `owner_verified` is empty on the working branch. Its
  output names only the owner's lines.
- `scripts/checks.py advice <id>`: for each line the advisor verifies and `you` does not, the
  highest-numbered reply in `tasks/advice/<id>-<n>.md` whose second line is `JOB: a (<line>)`, in
  the working tree during the merge. It refuses the merge when a line has none or the latest's
  first line is not `RULING: HOLDS`.
- `scripts/checks.py consult <id> <reason> [<branch>]`: exits 1 for an always-park case of the
  park list, or when an always-park condition the repo shows holds, whatever the reason; 0 when
  the advisor is consulted first; 2 for a reason not in the list. `<branch>` is the task's
  branch, left out when there is none.
- `scripts/checks.py drafts <id>`: the Proposed tasks that hard-depend on the task and have an
  empty `done_means`, one id per line, for the advisor's job (d).
- `scripts/checks.py run-start | run-end`: mark a run active with `.git/manage-run-active`.
  While it exists, the `PreToolUse` hook in `.claude/settings.json` refuses any Bash command
  whose text runs `git push`, for the main session and every subagent. It reads command text,
  so it is an early stop, not proof: an alias, a script or `gh` can still push. If a run
  crashed and left the marker, the owner deletes the file.

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
  findings on files only its branch has, `tokens`.
- `tasks/reviews/<id>-<n>.md`: each reviewer reply verbatim, in the task's merge or park commit.
- `tasks/advice/<id>-<n>.md`: each advisor reply verbatim, in the task's merge or park commit,
  or for job (d) in the drafted task's commit.
- `tasks/RUNS.md`: one report per run, newest first, in skill-iterate's three sections.
