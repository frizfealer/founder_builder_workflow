9 findings: 6 Important, 3 Nit.

F1 | Gap | Important | G-02; failure row "the customer changed the order or another proposal term in the confirming turn or after confirming"
Quote: "Any change to a proposal term after confirmation voids that confirmation."
Evidence: review-packet.md Round 1 Q4 (accepted with "Yes to all"): "any change after confirmation voids it." The failure row at agent-spec.md line 96 says the trigger is a change "in the confirming turn or after confirming". The only change-of-mind scenario is CO-S03, and its Turn 2 comes "in place of a confirmation" (line 248). So there is never a confirmation to void. No scenario has a turn that both confirms and changes a term, such as "Yes, but make it HG-10511." An agent that takes that turn as confirmation of HG-10482, or cancels HG-10511 without re-confirming its $23.75 / Mastercard terms, passes every scenario.
Pattern: a rule clause and failure row whose trigger no scenario's User block produces.

F2 | Gap | Important | CO-A2 failure row "the order system did not answer the second CO-A2"
Quote: "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown."
Evidence: Reads are unlimited (Appendix A line 1519; review-packet.md tool confirmation change 4). An agent may therefore look up the order after the second unanswered CO-A2, and the lookup may show cancelled, shipped or still open. This row has no branch for that lookup, and it conflicts with other rules:
- CO-07 (line 80) allows CO-A4 only "when the agent cannot tell whether the order was cancelled" and says "CO-A4 occurs in no other situation".
- CO-05 (line 74) allows CO-A3 for an order "a lookup shows cancelled".
- G-03 (line 24) lets the agent say cancelled once a lookup shows it.
CO-S15 (line 892) makes every lookup after the second CO-A2 unanswered, so no scenario reaches the case. The inputs set the re-read procedure only for the first timeout (Round 3 Q4).
Pattern: a commit-call timeout row that forbids or ignores a lookup the agent may make, with no branch for each result that lookup can return.

F3 | Gap | Important | CO-01 / CO-S06; row "the lookup shows the named order with status cancelled"
Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence:
- The Trigger (line 57) includes a customer asking "to get their money back for an order".
- list_orders returns each order's refund or null, and a refund can have status failed (Appendix A lines 1523 and 1525).
- CO-S17 and CO-S23 leave exactly such an order behind: cancelled, refund failed or missing, and in CO-S23 staff contact unconfirmed. A customer coming back in a new conversation is realistic.
- CO-05 (line 74) allows CO-A3 for any order a lookup shows cancelled.
- The primary-actor interest (line 9) is being told "where the refund stands".
- The input says "An already cancelled order: the agent reports that and changes nothing" (review-packet.md shared-understanding summary).
CO-S06 has an issued refund in both rows. No scenario has a cancelled order with a null or failed refund, which is the state that tempts an unconfirmed CO-A3 or CO-A4. No rule says what the agent tells the customer about that refund.
Pattern: a holding-back case whose scenario uses only the untempting state (refund already issued) and leaves out the boundary states (null or failed refund).

F4 | Gap | Important | Scope & Authority "must not" / Contract
Quote: "promise a date by which the refunded money arrives."
Evidence: review-packet.md Round 3 Q1 (accepted): "The agent promises nothing about when the money arrives." This replaced Round 2 Q2's proposed "money arrives in 5 to 10 business days". The prohibition exists only as a Scope line (line 49). No Contract rule states it, and no §5.2 rubric dimension (lines 1495–1509) forbids it. An agent that ends CO-S01 with "your $86.40 will be back on your Visa in 3 days" passes every scenario.
Pattern: an input prohibition on what the agent tells the customer that lives only in Scope, with no rule and no rubric check in any scenario.

F5 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state
Quote: "is answered by the order system with the order not cancelled, and creates no refund" (CO-S17 row 3), with Final state "HG-10482 has status cancelled."
Evidence:
- Appendix A (line 1525) defines OrderNotCancelled as "the order is not cancelled".
- Line 1524 sets the order to cancelled when cancel_order returns cancelled, which CO-S17 step 5 does. So the scenario has the order system contradict its own outcome definition.
- The required report, row at line 103 and dimension "Refund not issued reported" (line 1505), makes the agent tell the customer "the order is cancelled" right after the order system said it is not. Experts would split on a truthful agent that reports the conflict.
- Second instance: CO-S24 (line 1414) has cancel_order report "order not found" for an order that line 1411 says belongs to the customer and that the lookup in step 2 shows.
Pattern: an Initial-state line makes a supporting actor give an outcome that contradicts that outcome's meaning in Appendix A, so the required behavior rests on an impossible world.

F6 | Gap | Important | G-01 / CO-06 / CO-02
Quote: "The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation"
Evidence:
- Known failure case 1 (review-packet.md Round 2 Q4) has a customer with two open orders.
- Nothing in the inputs or the spec says what happens when that customer wants both cancelled ("cancel both my orders"), or asks for a second order after the first succeeds.
- CO-06 counts per conversation and allows a second CO-A2 only after an unanswered first, which forbids cancelling the second order. CO-02 (line 65) says every proposal names one order. G-01 (line 18) limits the agent to "the one order the current request is about".
- No rule, failure row or scenario says what the agent tells the customer in this case, so the coder will invent it.
Pattern: a realistic multi-record request the per-conversation caps silently forbid, with no stated handling.

F7 | Gap | Nit | CO-02 (act-only-when, holding-back side)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-S02 is the acting scenario. In every other scenario Turn 1 names the order number:
- CO-S01's three rows, even though it also has delivered HG-09977;
- CO-S03 to CO-S24, "Please cancel order <order>".
No scenario has exactly one open order and an unnamed request ("cancel my order"), where the agent should propose without asking.
Pattern: an "act only when" rule with an acting scenario and no holding-back scenario.

F8 | Gap | Nit | CO-A2 failure row "the order system did not answer the first CO-A2"
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
Evidence: The use-case checklist (cockburn-checklist.md, Failure handling) says a row that branches on a lookup covers every result, "nothing found" included. This row has no branch for a lookup that answers but does not list the order. The order system can fail to find an order: cancel_order has an OrderNotFound outcome (Appendix A line 1524).
Pattern: a lookup-branching row missing the not-found branch.

F9 | Gap | Nit | CO-A3 failure row "payment provider temporarily unavailable for the second CO-A3"
Quote: "Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence:
- Known failure case 3 (review-packet.md Round 2 Q4): after a refund timeout the agent "retries once, then re-reads the order and refund records and reports what it finds".
- Round 3 Q3: "For case 3, after the retry the agent re-reads the refund record."
- This row applies to any second CO-A3 that reports the provider unavailable, including one after a timed-out first call that may have created the refund. It skips the re-read and states "not issued".
- No scenario has a timeout followed by provider unavailable: CO-S16's rows end in success and CO-S18 is unavailable twice.
- Nit because SG-01 (line 1541) arguably means a second call would have returned a refund that the first call created.
Pattern: a combination of outcomes from a known failure case that falls into a row with different handling than the input prescribes, with no scenario.

Files read: briefs/r1-finder-coverage.md, review-packet.md, product-idea.md, run/agent-spec.md, references/cockburn-checklist.md, cockburn-checklist.html (headings only), evaluation-checklist.md, specification-by-example-checklist.md, verification.md
