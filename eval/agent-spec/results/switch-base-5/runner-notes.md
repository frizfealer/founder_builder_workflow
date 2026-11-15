# Runner notes (switch-base-5)

## Dispatch and models

- Every subagent ran on opus: five stand-in turns, one finder and one verifier. The verifier ran on the session's model (opus), as step 4.4 requires.
- Each subagent ran in the background. I waited for its hand-back and task notification before going on. The turn-1 Monitor watch expired unused.
- I did not invoke grilling. SKILL.md does not tell step 2 to.

## Interview choices

- Step 2 took two turns: systems plus three row gaps, then data, failure cases, money mismatch and the orders-per-conversation limit.
- I sent the claims under the decision filter, the tool confirmation and the policy gaps (cancel with no answer, staff call with no answer) in step 3.4's first turn. The second turn (the last allowed) took the owner's "reads without limit" (limit set to none), the second cancel with no answer, the fourth staff reason and the pending refund.
- In question 13 the owner kept "without limit" instead of my bound. The spec writes "nothing" in C-05's "what ends it" cell and lists it as an open question. The model folds the read loop into one state.
- The owner's "re-read fails" next to "retried on timeout without limit" read to me as two outcomes: an error answer, and a timeout that is read again. So reads answer, answer an error, or get no answer. C-56 marks this spec only.
- "handoff timeout not retried" (the first tool set) and "On timeout, retry once" (the owner's confirmation, change 3) conflict. I went with the later confirmation and logged it as D-09.
- The stand-in answered question 9 (the tool set with my fourth reason) from the record, so the fourth reason was not confirmed. I asked it again as question 15, and the owner accepted it.
- Question 17 (the F1 proposal) was answered with the record's own rule, not "Yes". The rule matches the proposal, so I treated it as acceptance. D-15 is logged as "the owner, accepting the recommendation", as the skill wants for an accepted rule change.

## Model notes

- The first checker run found an R-11 break. It was a model bug: after a reread with no answer, the model ignored what the retry had answered. I fixed the model (round 0 era). Under the owner's final D-15, that branch was later removed again on purpose, which re-creates the R-11 break as an open decision. I did not change R-11's text: under the skill, a rule-text change needs an owner proposal, and the one 4.5 turn had been used.
- I mutation-tested the model by hand for R-10 (staff retry), R-02/R-07 (cancel again after a failed reread) and R-09 (a pending refund reported without being shown). All broke as expected. The first R-10 mutation also changed the rule's own check, and showed no break until I redid it.
- The outcome "refund call answers order not cancelled" is in the model even though the order is cancelled at that point. The owner listed it as an outcome, and the checklist lists "the system answers wrongly". That is why F5 was real.

## Keep/drop reasons

- F6 dropped: C-44 (idempotent refund keyed on the order) means an open order that already has a refund gets no second refund, and the agent reports that refund's real status. I agree the verifier's refutation answers the whole finding.
- F8 dropped: C-13 (Stripe docs) says a refund can only go to the original payment method, so a method mismatch cannot happen.
- F9 dropped as Style only: the owner's own words separate a read that fails from one that times out. The R-01 wording covers a case the owner gave no wording for, and changes no behavior.
- F2 and F4 kept at the verifier's lower severity (Nit).

## Timing

- wall_clock_s runs from step 1 start (2026-11-15T02:56:38Z) to step 5 end. run.log has every step and round timestamp.
- The harness refused the Write of report.md ("Subagents should return findings as text"). Per rule 17, the report text goes back in the hand-back under REPORT.MD.
