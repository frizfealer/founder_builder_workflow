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
4. Print the table and the set summary verbatim. Add nothing to the numbers.
5. If `--gate` was asked for, report the exit code.

Judges never see each other's output or the grade table. Do not re-dispatch a judge whose
verdict file exists; delete the verdict file first only when the human asked for a re-judge
(escalation case 4).
