# Manager runs

## Run 2026-11-15 21:27

Stopped because: no task to take.

### Done
- none.

### Decided for you
- task 028: chose merging build2 into grading.json and keeping the retired kinds there over replacing it with grading-new.json; would change if old kinds should be graded only through a separate file.
- task 028: chose new fields `default_kind` and `kinds.<kind>.prompt`, read by /trial and /iterate, over a `PROMPT-<kind>.md` naming rule; would change if you prefer the naming rule.
- task 028: chose to keep grading-new.json, marked superseded, over deleting it; would change once task 038 lands.
- task 028: chose to park over merging with one protected test failing; would change if you accept the failing test until 038.
- task 036: chose filtering the found verdict files with `git status` before add and commit over `git add` then `git diff --cached --quiet`; would change if you prefer the cached check.

### Needs you
- task 028 (parked): branch `task/028` meets every clause of done_means. Both reviews failed it because `eval/agent-spec/new-format/grader/tests/test_grade_build2.py::test_grade_skips_unknown_kind` asserts grading.json has no build2 kind. That test is protected and not in may_edit. Recommended: add that test file to task 28's may_edit and fold task 038 in, then set Ready; the retry also fixes three minor review points. If you veto: say you accept a failing test until 038, and the next run merges `task/028` as it stands. Also: the six branches merged into the working branch (agent-spec/switch, manager/build, iterate/agent-spec/it1, iterate/agent-spec/it2, claude/verifier-ruling-stability-4811l2, add-develop-architecture-notes) are yours to delete; add-agent-spec-to-pytest-bdd and add-review-artifact are not merged.
- task 036 (parked): verification still failed after one retry. Branch `task/036` meets done_means and 6 tests pass, but the second review found the empty-`<paths>` guard is not tested against grade.md, `git status` without `--untracked-files=all` depends on git config, `-z` output is hard for an agent to read, and renames are not parsed. Recommended: drop `-z`, add `--untracked-files=all`, add an ordering test, and set the task Ready again. If you veto: the next run merges `task/036` as it stands and the four points become one Proposed task.
- task 038 (Proposed): point the build2 grader tests at grading.json and remove grading-new.json. The test above fails once task 28 lands.
- task 039 (Proposed): document `default_kind` and `kinds.<kind>.prompt` in grading-schema.md. /trial and /iterate now read fields the protected schema doesn't describe.
- task 040 (Proposed): keep the seeded-demo fixture out of a plain grade. With build2 live, a bare /grade and /iterate step 1 grade it and dispatch a paid judge.
- task 041 (Proposed): /trial steps 4-5 match the build2 folder layout. They still describe the old one-file spec.
- task 042 (Proposed): record the rest of HARNESS-PLAN section 5 retirements. Metrics, keys and queued experiments it retires still read as open.
- task 043 (Proposed): grade.py lists only the metrics of the graded kinds. A build2 grade now prints every retired metric.
- task 044 (Proposed): /grade step 2 and the no-re-dispatch rule agree on unusable verdicts. They contradict each other for exactly those tasks.
- task 045 (Proposed): /grade step 4 git commands survive ignore rules and pattern characters. An ignored verdict is skipped silently; `*`, `?`, `[` in a label act as patterns.

## Run 2026-11-15 20:36

Stopped because: no task to take.

### Done
- task 020: /grade commits its verdicts; merge 72116d6; tokens 111854 (main session: not recorded)

### Decided for you
- task 020: chose committing only the verdict files over also committing the .task.md files next to them; would change if you want both committed together (one-line change to step 4 and the test).
- task 020: chose exact git commands in grade.md, tested by parsing them from the file, over a commit script; would change if agents get the verdict path wrong in practice.
- task 020: chose the message `eval/<skill>: judge verdicts for <set>`, matching past verdict commits; would change if you have a house format.

### Needs you
- task 036 (Proposed): /grade commit step skips unchanged verdict files. If the only re-listed verdict file is already committed and unchanged, step 4's `git commit` exits 1 with "nothing to commit".
