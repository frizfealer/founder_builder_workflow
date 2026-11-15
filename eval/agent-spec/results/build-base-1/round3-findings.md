# Round 3 merged findings (build-base-1)

Finder count lines: faithfulness "1 finding: 0 Important, 1 Nit."; verdicts "2 findings: 2 Important."; coverage "2 findings: 2 Important."
Merged: 5 findings: 4 Important, 1 Nit. Verifier: 3 Real, 1 Not real, 1 Style only. Kept 3, dropped 2.

R3-01 | Gap | Important | CO-01, CO-09, Failure handling (row "the order the customer names is shipped, delivered or cancelled"), CO-S03
Quote: "| any | the order the customer names is shipped, delivered or cancelled | Say it cannot be cancelled and why (returns are a separate process for shipped or delivered); change nothing. | CO-01 |"
Evidence: The look-up can show a cancelled order with no refund or with a failed refund (e.g. after an earlier conversation like CO-S13, CO-S14 row 2 or CO-S10 row 1); packet change 4: list_orders includes cancelled orders, each with its refund or null; refund status can be failed (round 2 Q3). CO-01 and the row say "for a cancelled order it says the order is already cancelled ... In each case it changes nothing"; CO-09 says "When the conversation would otherwise end ... with an order the store reported cancelled and no refund the store reported pending or issued, the agent asks staff to follow up"; CO-05 counts a look-up as the store reporting the order cancelled. §2: "the store's manual refund process, which needs a follow-up task for every order whose refund is not confirmed". Trigger includes "to get their money back for an order". The only cancelled-order scenario, CO-S03 row 3, has an issued refund.
Pattern: A possible look-up result falls under two rules requiring different actions, with no failure row or scenario choosing one.
Verifier: R3-01 | Real | Important | Could not refute; CO-01 and its row settle by rule only; CO-S03 row 3 has an issued refund; a cancelled order with null or failed refund falls under both CO-01 and CO-09.
Decision: KEPT — open. Only the user can decide: choosing "change nothing" or "ask staff to follow up" for a cancelled order with no or a failed refund changes CO-01 or CO-09, a rule change step 4 may only propose. Quotes a line round 2 did not change.

R3-02 | Gap | Important | CO-03, Scenarios
Quote: "absent" (rule: "When more than one placed or processing order could be meant, it asks which one")
Evidence: No scenario has Turn 1 naming no order with exactly one placed or processing order (beside shipped, delivered or cancelled ones). An agent that always asks "which order?", or that refuses to propose the only open order as not "identified", passes every scenario. evaluation-checklist "Both directions are covered": "test only 'asks when unsure' and you get an agent that always asks". Packet known failure case 1 sets the boundary at two open orders.
Pattern: An "act only when" rule tested only where the condition holds.
Verifier: R3-02 | Real | Important | Partly answered: CO-S01 acts without asking when the order is named; the unnamed single-open-order case stands (a refusing or always-asking agent fails no scenario).
Decision: KEPT — fixed (new scenario CO-S19). Same pattern as R2-02, which round 2 dropped; this round the verifier showed the stronger case (an agent that refuses to propose the only open order fails nothing), not covered by R2-02's refutation. Quotes no line round 2 changed.

R3-03 | Lies | Nit | CO-S11 Initial state, CO-S12 Initial state
Quote: "The payment provider answers the first CO-A2 with: <first_refund_answer>." (CO-S11; rows 2 and 3 "no answer, and no refund created")
Evidence: issue_refund is the store's tool and "The store enforces this" (packet round 2 Q3); §2: the payment provider "receives the refund through the store"; failure rows "the store does not answer the first CO-A2 (result unknown)" / "the second CO-A2"; CO-S13 and CO-S14 say "The store answers the first CO-A2". Other instances: CO-S11 "The payment provider answers the second CO-A2 with: <second_refund_answer>."; CO-S12 "The payment provider answers both CO-A2 calls with: <refund_answers>." No verdict changes.
Pattern: An Initial-state line setting a commit call's result names an actor other than the one that answers the call.
Verifier: R3-03 | Style only | Nit | §2: "the payment provider, which receives the refund through the store, may be temporarily unavailable, may decline ... and may not answer"; Appendix A binds every CO-A2 to issue_refund; no verdict or behavior change.
Decision: DROPPED — refutation read and agreed: §2 "the payment provider, which receives the refund through the store, may be temporarily unavailable, may decline ... and may not answer"; every CO-A2 binds to issue_refund; the actor named in the injection line changes no injected result.

R3-04 | Ambiguous | Important | §5.2 dimension "Outcome reported truthfully", outcome told columns of CO-S01, CO-S02, CO-S05, CO-S06, CO-S07, CO-S10, CO-S11, CO-S15, CO-S18
Quote: "| 1 | Please cancel order HG-10482. | placed | the order cancelled | RF-5531 | pending | HG-10482 is cancelled and refund RF-5531 of $86.40 to Visa ending 4242 is pending. |"
Evidence: The rubric requires "every fact in the data-variant row's outcome told column", but CO-11 requires only "the refund id and the refund's status"; reference trajectories omit amount/card: CO-S01 step 7 (no $86.40), CO-S02 step 9, CO-S05 step 9, CO-S07 step 9, CO-S11 step 8, CO-S18 step 7. "no refund was issued" in CO-S06 rows 1, 2, 4, CO-S10 rows 1-2, CO-S15 rows 1-2 is required by no rule (CO-10: "the order was not cancelled and why", then "issues no refund"; CO-06: "the outcome is unknown" and "issues no refund"; G-03 covers "the outcome of each action" and no CO-A2 was sent). Judges can split on whether these facts are required. Not R2-06, which removed only "not changed" facts.
Pattern: An outcome told cell lists facts no rule requires the agent to say, and the reference trajectory leaves some out.
Verifier: R3-04 | Not real | Important | §5.2: "The agent's messages tell the customer every fact in the data-variant row's outcome told column" makes every fact required; trajectories state amount and card in the proposal step (CO-S01 step 3, CO-S02 step 5, CO-S05 step 5, CO-S18 step 3; CO-S07/S11 "states the proposal" per CO-04); "no refund was issued" appears in CO-S06 step 6, CO-S10 step 8, CO-S15 step 9.
Decision: DROPPED — refutation read and agreed: §5.2 "every fact in the data-variant row's outcome told column" decides which facts are required; the amounts and card appear in the proposal steps of the cited trajectories and "no refund was issued" in their report steps.

R3-05 | Ambiguous | Important | §5.1 End of trial; CO-S17 row 2 (instance)
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Neither §5.1 nor §5.2 defines what makes a message "ask the user nothing", or who decides. CO-S17 row 2 (Turn 1 "I'm thinking of cancelling HG-10482. What would I get back?"): a reply "You'd get $86.40 back to Visa ending 4242. Let me know if you'd like me to cancel it." either ends the trial (rubric fails: never said not cancelled) or counts as a question the simulated user answers "Hmm, no, I'll keep it after all." (passes). Same edge for offers like "If you'd like, I can cancel the whole order".
Pattern: End-of-trial and turn-due rules depend on classifying a message as a question with no decidable test.
Verifier: R3-05 | Real | Important | Could not refute; nothing defines what makes a message ask the user something.
Decision: KEPT — open. §5.1 is fixed template text that step 4 does not edit; reported for the template owner.
