# Manager runs

## Run 2026-11-17 18:32

Stopped because: no task to take.

### Done
- task 049: BDD slice A: three café scenarios, with a real-agent measurement; merge 93682a8; tokens 757645 (main session: not recorded). No agent ran this run; the count is the task's earlier runs.

### Decided for you
- task 049: merged a fresh branch `task/049-3` (the working branch plus `task/049-2`'s cafe folder, no task files) over merging `task/049-2`, whose stale copy of `tasks/049.json` failed the protected-path check on `notes`; the code is identical to `task/049-2`.
- task 049: took review 049-3 (PASS on `task/049-2`'s final head) as the reviewer verdict and reran its 10 commands on `task/049-3`, all exit 0, over a fresh reviewer on an unchanged diff; would change if you want a new review whenever a branch is recut.
- task 049: counted your `you` verification as done from the task's notes (lines 4 and 5 hold, you said merge), over parking again because `verified_by` includes `you`; would change if you want such tasks parked until a separate field is set.

### Needs you
- branch task/049 (not deleted): the branch 'task/049' is not fully merged. Its work was carried over into `task/049-2`, so it is superseded.
- branch task/049-2 (not deleted): the branch 'task/049-2' is not fully merged. Its cafe folder is merged byte for byte through `task/049-3`; only its stale task file differs.

## Run 2026-11-17 %H:%M

Stopped because: no task to take.

### Done
- none.

### Decided for you
- task 049: cited text of a claim is its row plus the Systems-table row it names, and of a rule its rules.md section plus the "What the agent does" rows naming it, over citing the id-less Systems table; would change if Systems rows get their own ids.
- task 049: a checker "undecided" counts as a disagreement in line 4, over leaving it out; would change if you rule an undecided verdict is no verdict.
- task 049: judge calls send thinking `between_tools`, over raising max_tokens, because sonnet-5-5 thought first and returned no text; would change if you want judge thinking on.
- task 049: both bad prompts rewritten to name the rule they override and the call to make, over keeping the plan's sentences, which broke their rule in 0 of 6 runs; would change if you want subtler wording.
- task 049: all 36 runs rerun with the first try kept in `runs/part2-first-try/`, over rerunning only the affected runs.

### Needs you
- task 049 (parked): bring `.claude/skills/agent-spec-to-pytest-bdd/examples/cafe/runs/part2/transcripts/` (branch `task/049-2`) to chat for labelling. Lines 1 to 3 hold (review 049-3 PASS, 69 tests and the drift check exit 0); part 2 ran on claude-sonnet-5-5, 27 of 27 runs and 9 of 9 conversations reached a verdict, $0.88 spent. The rewritten bad prompts dictate the exact booking call, so line 5 adds little beyond line 2; transcripts still hint that the unanswered booking went through. Recommended: label from `probe/agreement.py --template` without opening the verdict folders, run `probe/agreement.py labels.json`, and set 049 Ready if lines 4 and 5 hold. If you veto: ask for weaker bad prompts and a rerun (about $0.45), or merge part 1 alone and move lines 4 and 5 to a new task.
- task 055 (Proposed): Café slice A: transcripts without labelling hints, and total spend in the part 2 summary. The hints can bias the labels lines 4 and 5 rest on, so it is best done before labelling.

## Run 2026-11-17 08:14

Stopped because: no task to take.

### Done
- none.

### Decided for you
- task 049: probe model claude-sonnet-5-5, priced at grading.json model_rates.sonnet, over another model; would change if you name another model or the real price differs.
- task 049: each tested moment judged on its home scenario's cited rules, over every scenario's rules at every moment; would change if you want the union (moments.*.scenario and CITED).
- task 049: histories stored literally in data.json, over references; would change if the file grows too large in slice B.
- task 049: the second sentence of R-01 left unchecked, over checking it now; would change in slice B, where a scenario reaches it.
- task 049: preflight usage kept in verdicts/ and skipped as a verdict, over moving it out; would change if you want verdicts/ to hold verdicts only.

### Needs you
- task 049 (parked): part 1 passed review (049-2: PASS) and its 5 check commands exit 0 on task/049; part 2 did not run because the API refuses calls with "credit balance is too low" ($0 spent). Also read the 3 feature files and say whether this is the format you want. Recommended: add about $5 of credit, re-run `ant auth login` if expired, run `uv run python probe/run_part2.py` from the cafe folder, bring the transcripts to chat, then set 049 back to Ready. If you veto: lines 4 and 5 stay unproven and tasks 50 to 53 stay blocked; or move lines 4 and 5 to a new task and merge part 1 alone.
- task 054 (Proposed): Café slice A: make the part 2 runner and data file robust before the real run. The fake's 3-id limit and lost usage on errored runs can waste or misreport the paid part 2 run.

## Run 2026-11-15 22:05

Stopped because: merge limit (3 task merges since review/2026-11-15; no other task is Ready either).

### Done
- task 028: Make build2 the default trial kind; merge 91b38d1; tokens 529833 (main session: not recorded)
- task 036: /grade commit step skips unchanged verdict files; merge d74610e; tokens 184471 (main session: not recorded)

### Decided for you
- task 028: chose keeping `owner-brief.md` in `judge_context.inputs` for every kind, recorded as an accepted trade-off in grading.json's notes, over dropping it; would change if grade.py gains per-kind judge inputs.
- task 028: chose to have the README state what each command does over adding a kind argument to /trial; would change if you want /trial to take a kind.
- task 028: chose to leave HARNESS-PLAN.md, SWITCH-PLAN.md and PROMPT-switch-plan.md mentioning grading-new.json over editing dated plan records; would change if you treat those plans as live.
- task 036: chose a plain-porcelain parsing rule that also covers `old -> new` rename lines and git's quoted paths (tab included) over naming only the characters in your ruling; would change if you want the shorter rule.
- task 036: chose to update the no-verdict-found test's command assertion to the new status command over leaving a stray `-z` there; would change if you read "change nothing else" strictly.

### Needs you
- Review and set a review tag: the merge limit is reached, so the next run merges nothing until `git tag review/2026-11-15-2 re-create-from-scratch`.
- Branches to delete (the manager may not delete): merged into the working branch are `task/020`, `task/028-2` and `task/036-2`. `task/028` and `task/036` are not merged, but their work was carried over into the `-2` branches, so they are superseded.
- task 040 (Backlog): with build2 live, a grade.py run with no `--labels`/`--set` (/iterate step 1, a bare /grade) now grades `results/seeded-demo` and writes a judge task there. The task 028 reviewer confirmed this; task 040 already covers it, so it may deserve a higher priority.
- task 046 (Proposed): small eval doc fixes left by task 028. The README omits `judge-verifier-brief.md`, /trial step 0 refers forward to step 1, and grading.json's long note prints under every grade table. Its note change needs `eval/agent-spec/grading.json` in may_edit.

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
