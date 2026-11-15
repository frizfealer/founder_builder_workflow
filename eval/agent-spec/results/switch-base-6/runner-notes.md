# Runner notes (switch-base-6)

## Dispatch and timing

- Stand-in turns were dispatched one at a time, sequentially, each with the brief path and the questions only. Their replies came back as hand-back messages; the task notifications with usage arrived after each one.
- No grilling skill was invoked: SKILL.md at d93de6e does not mention grilling or grill-with-docs.
- The skill at d93de6e has one verification round ("There is no second round"), so round2/round3 files do not exist. The step-4 stop condition is the skill's own: one round, then the report.
- Step 3.4 used both of its turns (turns 4 and 5). Turn 4 carried the tool-set confirmation.

## Interview judgement calls

- Q2: my recommendation added a staff task for a shipped order; the record overrode it (no task, returns are a separate process). Logged as D-01, decided by the owner.
- Q9: the record changed the tool set: cancel outcomes became cancelled / not cancellable (shipped or delivered) / not found / timeout; the refund got an "order not cancelled" outcome; the task call became idempotent and retried once (this superseded the earlier "handoff timeout not retried", so C-29 was rewritten); reads retry without limit. The last one raised a new limit-with-no-end question, put in turn 5 (Q13).
- Q13: the stand-in answered from the record by repeating "Reads may be retried on timeout without limit", so the owner kept no bound. I logged it as owner decision D-08 and kept the open "what if it never answers" for the report.
- Q12 reply mapping: "failed or no refund ... not confirmed yet" mapped to the reason refund not issued; "re-read fails ... status unknown" mapped to refund status unknown. That mapping is mine; the owner gave only the messages.
- The decision filter asked 12 claims, above the cap of 10. I did not convert any to `missing`; the report says so.
- "A read fails" versus "a read gets no answer": modelled as two outcomes because the owner used both words. The lookup failing (C-45) and its message (C-34) are spec only.

## Keep and drop decisions, round 1

- F1 dropped: I read Q13's reply and D-08. The owner was asked "what ends it" against a recommended bound and replied that reads retry without limit. That is a decision, not a missing answer. I agree with the verifier. Kept as an open question in the report.
- F2 dropped: I read Q11 and Q12; the owner uses "fails" and "timeout" as two outcomes. I agree it is the owner's own word. I still trimmed C-44's "rather than get no answer" under F8's pattern.
- F3 kept and fixed: the re-read path really did report any refund as success; the model could not reach a differing refund after a timeout.
- F4 kept at Nit (the verifier's lower severity): behaviour was settled in R-12, D-03 and SC-44, but no row existed.
- F5 kept: R-03 matched only the two-order example.
- F6 dropped: I read Q7 (system-side change goes to staff) and Q11 ("under the same confirmation"). I agree R-05's scope is right and the re-read total-change case has no evidence.
- F7, F8 kept as Nits and fixed.
- The four rule-text fixes (R-03, R-08, R-09, R-12) went to the owner in one turn with before and after, as the skill requires; all four were accepted (stand-in default) and logged as D-11 to D-14.

## Harness

- The Write of results/switch-base-6/report.md was refused by the harness ("Subagents should return findings as text"). Per rule 17 the report goes into the hand-back under REPORT.MD.
- No script that ships with the skill failed. My helper scripts: run-switch-base-6/log_turn.py and run-switch-base-6/fill_scenarios.py, plus inline python edits.
