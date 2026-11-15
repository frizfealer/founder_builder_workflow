# Runner notes (switch-base-10)

Not for reviewers of the scratch dir; my own reasons.

## Interview
- Turn 1 asked the systems question together with three row-1/row-3/row-4 questions that do not depend on the systems answer (systems question first in the turn). Did not invoke grilling: this SKILL.md version does not tell the runner to.
- The stand-in answered largely from the record, which carried far more detail (tool contracts, failure cases, race) than the product idea. Questions 9 to 16 are the step-3.4 turns (two turns, the skill's maximum).
- Question 9 (tool set): the stand-in replied "No. The record says:" and quoted the confirmed tool set with four changes. I took the record's set; my proposed fourth reason "refund amount differs" was not in it, so I asked which existing reason applies (question 15; accepted: refund status unknown).
- Question 13 (bound on read retries): rejected by the record ("Reads may be retried on timeout without limit"). With no third 3.4 turn allowed, I modelled the owner's literal answer: a timed-out list read is sent again (a cycle in the model, still finite). C-45 is kind missing; it is an open question in the report. Before that I had briefly left a `no-step` open break for "list call fails"; it blocked "Steps no scenario takes: 0" (a dead state has no complete path), and modelling the owner's words removed the need.
- The record holds two contradictory staff-timeout answers ("handoff timeout not retried" in the proposed set, then "On timeout, retry once" in the confirmed changes). I followed the later, confirmed one.
- C-31/C-55: after a refund call with no answer, the agent retries and then always re-reads (the owner's words "after the retry the agent re-reads"). One break (R-11) showed that a re-read failing after the retry returned a different amount lost the amount; I made that branch tell the amount returned (model fix, row added).

## Round 1 keep/drop
- F3 dropped: D-02 plus SC-38/SC-39 say what the agent does for two orders in one message and a second order after the first; the model is scoped to one order per run by its docstring. Agreed with the verifier.
- F4 dropped: R-10's sentence states the behavior regardless of what the second call returned; the row's wording does not change behavior. Agreed with the verifier (it rated Nit).
- F1, F2, F5, F6, F7 kept. Rule-text fixes (R-07, R-10, R-12, R-01) went to the owner in one 4.5 turn (questions 17 to 20); all four accepted (question 17 answered with record passages that state the After text; logged D-07 decided by "the owner"). Non-rule fixes (C-30, C-26, C-04, C-58, the R-04 row wording) applied directly.
- F1 part (1), no end to timed-out reads, stays open: the owner already declined a bound in question 13; re-asking would repeat a rejected proposal.

## Dispatch timing
- Finder dispatched 14:53:38Z, returned before 14:56:53Z; verifier dispatched 14:56:53Z, returned before 14:59:48Z; 4.5 stand-in turn returned before 15:01:45Z.
- I fetched https://docs.stripe.com/refunds (WebFetch) while stand-in turn 2 ran, to settle the payment-provider claims from its docs (C-23 to C-26).

## Harness
- The Write of results/switch-base-10/report.md was refused ("Subagents should return findings as text"); the report text is returned in the hand-back under REPORT.MD, per rule 17.
- I wrote one checker JSON output to /private/tmp/claude-501/x.json by mistake (outside the run dir) and deleted it at once.
- subagents.jsonl in this folder is my running record of task-notification numbers, written as each notification arrived.
