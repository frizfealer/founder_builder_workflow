# Runner notes

- Skill at e8ed321 has one verification round (4.3 to 4.5, "There is no second round"). Only round1-findings.md exists. The prompt's steps 3.8 and 3.9 do not exist in this skill version: step 3 runs 3.1 to 3.5, and the tool confirmation happened in 3.4. They are logged under 3.4.
- The skill at this commit does not tell the runner to invoke grilling, so it was not used.
- Read eval/agent-spec/new-format/FORMAT.md only. Rule 6 of the prompt names it for the interview-log format, though rule 3 lists new-format/ as off limits. Nothing else under new-format/ was read.
- Docs read: docs.stripe.com/refunds and docs.stripe.com/api/idempotent_requests. Claims C-22 to C-25 are sourced from them. No claim contradicted the owner, so no docs-versus-owner question was asked.
- The record contradicted itself on the follow-up timeout ("handoff timeout not retried" against "On timeout, retry once"). This was put to the owner in Q9, and the record's confirmation picked retry once.
- The owner said reads retry with no limit. The recommended bound (Q13) was answered by repeating the record, so the loop was modelled as a self-loop (finite state graph) and the case was reported open. The skill allows at most two turns in 3.4, so it was not asked again.
- Keep or drop: all 10 findings were kept.
  - F10 was rated Style only, but it is a "claim says more than its quote" defect, which verification.md lists under Lies. It is not a phrasing preference, so it was kept and fixed.
  - The verifier refuted F6 part (b). It was kept for part (a), and no returns message was added on the late-shipped path.
  - The verifier partly refuted F3. It was kept for the pending row and the re-read amount check.
- The rule-text fixes (F2, F3, F4, F6, F7, F8) went to the owner in one 4.5 turn of 4 questions, with the before and after text shown. All were accepted (stand-in default).
- After the label changes, the first rerun in 4.5 showed 13 scenario-replay errors. The stale World lines were updated and the rerun reached 0 errors. These were errors in the spec under construction, not failures of the skill's scripts, so script_errors = 0.
- In the first 3.3 attempt, the runner's own shell quoting failed ("no such file or directory"). The command was rerun directly. This was not a skill script error.
- Helper scripts written: run-switch-smoke-1/addlog.py (appends to the interview log) and run-switch-smoke-1/fill_scenarios.py (fills scenario titles and Rules lines by keyword).
- The token split is not available from the task notifications. Only the subagent_tokens total was recorded.
