---
description: Grade one skill's trials — run grade.py, dispatch a judge for every pending judge metric, rerun, print the table
argument-hint: <skill> [--set <set>] [--labels a,b,c]
---

Grade the trials of skill `$ARGUMENTS`.

1. Run `python3 .claude/skills/skill-iterate/scripts/grade.py eval/<skill> <flags>` from the repo
   root. Pass `--set` or `--labels` through from the arguments.
2. For every judge task it lists (`results/<label>/judge/<metric>.task.md`), dispatch one
   `skill-eval-judge` subagent per task, in parallel, with the task file path and the eval dir
   `eval/<skill>` as its working directory. Wait for all of them.
3. Rerun `grade.py` with the same flags. Every judge cell should now hold a number. If one is
   still pending, read that judge's output, say why it failed, and leave the cell pending; do
   not fill it in by hand.
4. Commit the verdict files this run's judges wrote, in one commit, and nothing else. Take
   `eval/<skill>/results/<label>/judge/<metric>.verdict.json` for each task step 1 listed, where
   that file now exists; call them `<found>`. If `<found>` is empty, run no git command, make no
   commit and skip the rest of this step, since git status with nothing after `--` lists every
   dirty file in the repo. Otherwise run
   `git status --porcelain --untracked-files=all -- <found>` and keep only the files it prints,
   which are new or changed; call them `<paths>`. Its output is one line per file: two status
   letters, a space, then the path from the repo root, so the path is everything after the first
   three characters. If the status letters include `R` or `C`, that part reads `old -> new`: take
   the path after ` -> `. If the path starts with `"`, git quoted it because it holds a character
   such as a space, a tab, a non-ASCII letter, `"` or `\`: drop the outer quotes and undo the
   backslash escapes (`\"` is `"`, `\\` is `\`, `\t` is a tab, and octal escapes such as
   `\303\251` are the path's UTF-8 bytes, here `é`). Each path read this way is one of `<found>`,
   of the shape above. grade.py re-lists a task whose verdict file exists but is unusable, so a
   listed verdict can be committed and unchanged; it is left out.
   If `<paths>` is empty, no verdict file was written: make no commit and skip the rest of this
   step. Run `git add -- <paths>`, then
   `git commit -m "eval/<skill>: judge verdicts for <set>" -- <paths>` with the attribution lines
   this session requires (`<set>` is the `--set` value, else the labels graded). The paths after
   `--` keep every other staged or dirty file out of the commit. Then
   `git status --porcelain -- <paths>` must print nothing. Report the commit hash.
5. Print the table and the set summary verbatim. Add nothing to the numbers.
6. If `--gate` was asked for, report the exit code.

Judges never see each other's output or the grade table. Do not re-dispatch a judge whose
verdict file exists; delete the verdict file first only when the human asked for a re-judge
(escalation case 4).
