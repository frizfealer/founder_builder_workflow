# Round 1 merged findings (18)

## R1-01 (Important)
Sources: A-faithfulness F1, A-coverage F2

R1-01 | Lies | Important | CO failure handling, row "CO-A2 | the order system did not answer the second CO-A2"
Quote: "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown."
Evidence: review-packet.md line 64 (round 3 Q4, which the user accepted with "Yes to all") says: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." That rule covers any cancel timeout. Change 4 at line 85 lets reads be retried without limit. The spec's row for the second timeout skips the re-read. Even if a lookup would show the order cancelled (SG-04 covers a late cancel), the row forbids the refund and forces "not known whether the order was cancelled" with reason cancellation_unknown. If the lookup shows it shipped, the row still forces "unknown". This also contradicts the spec's own G-03 (spec line 24), which allows "cancelled" whenever "a lookup shows it cancelled" and allows "unknown" only "when it cannot tell". CO-S15 (lines 892, 925-932) never answers the lookup, so no scenario exposes this. In production, a cancelled order is left unrefunded, the handoff gets the wrong reason, and the customer is told something false.
Pattern: a failure row for a repeated timeout that drops the re-read step the inputs require on every timeout, and orders a fixed report the lookup's result could contradict.

## R1-02 (Important)
Sources: A-faithfulness F2, B-faithfulness F2, A-coverage F5

R1-02 | Lies | Important | CO failure handling row "CO-A3 | ... or reported the order not cancelled"; CO-07; CO-S17 row 3
Quote: "the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Appendix A (spec line 1525) defines OrderNotCancelled as "the order is not cancelled". The user added it at review-packet.md line 84 ("issue_refund adds outcome OrderNotCancelled") and gave no handling for it. Even so, the spec has the agent tell the customer "the order is cancelled" right after the order system said it is not. CO-S17 row 3 (line 1037) has the system answer "with the order not cancelled" for an order whose CO-A2 returned cancelled (line 1044). The Final state still says "HG-10482 has status cancelled" (line 1023). So the scenario's tool result contradicts both the binding's meaning and the Final state. CO-07 (line 80) sends this case to CO-A4 under "the order is cancelled but its refund is not shown". The rubric "Refund not issued reported" (line 1505) used by CO-S17 then fails an agent that truthfully reports what the order system said.
Pattern: handling and a scenario row that make an outcome mean the opposite of what Appendix A says it means, and that grade the agent on contradicting the latest tool result.

## R1-03 (Important)
Sources: A-faithfulness F3, B-faithfulness F1

R1-03 | Lies | Important | CO failure handling row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md line 63 (round 3 Q3, accepted) says for this case: "failed or no refund, hand off and say the refund is not confirmed yet". The spec instead requires the stronger claim "the refund has not been issued". This appears in the failure row (line 105), in CO-S20 reference step 10 (line 1219), and in the rubric "Refund not issued reported" used by CO-S20 (line 1505: "tells the customer ... the refund has not been issued"). An agent using the user's own wording can fail CO-S20.
Pattern: a required report reworded into a different claim from the one the user approved, then enforced by a rubric.

## R1-04 (Important)
Sources: A-faithfulness F4

R1-04 | Lies | Important | §5.2 rubric dimensions "Cancellation outcome unknown reported" and "Refund status reported"
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: These rubrics require statements that no rule or failure row requires, so an agent that follows the rows can fail.
- Cancellation outcome unknown reported (line 1504, used by CO-S14 and CO-S15). The rows at lines 100-101 require only "tell the customer it is not known whether the order was cancelled and store staff will follow up" plus "make no CO-A3". In the input (review-packet.md line 64), "issue no refund" is an action, not something to say. The reference trajectories add the clause anyway: CO-S14 step 8 (line 873) and CO-S15 step 9 (line 932).
- Refund status reported (line 1507, used by CO-S19) requires "the order is cancelled and the refund's status is ...". The row at line 105 requires only "tell the customer that status and the refund id".
Pattern: a rubric definition that adds clauses beyond the rule or failure row it grades.

## R1-05 (Nit)
Sources: A-faithfulness F5, B-faithfulness F6

R1-05 | Lies | Nit | Appendix A, CO-A3 row
Quote: "`issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` ... refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The refund data model at review-packet.md line 38, with the changes at lines 46-48, is: refund id, order number, amount, payment method, status (pending, issued, failed). It has no failure-reason field. The spec's own return signature in the same cell leaves `failure_reason` out. The terminal causes at line 63 are categories of error, not field values. No check reads the field: CO-S17 rows 1-2 and CO-S23's "failure reason" column assert only status failed, so no verdict changes.
Pattern: a tool-result field, with its enum values, that the data model does not have and that contradicts the stated return shape.

## R1-06 (Important)
Sources: B-coverage F1, A-coverage F4

R1-06 | Gap | Important | §4.1 Contract (no rule); §5.2 dimension table
Quote: "absent" (the only mention is the Scope line "- promise a date by which the refunded money arrives.", agent-spec.md line 49, under "The agent must not")
Evidence: review-packet.md, Round 3 Q1: "The agent promises nothing about when the money arrives." The user answered "Yes to all". Round 2 Q2 had first proposed "money arrives in 5 to 10 business days", so an agent repeating that timeline is a likely failure. No Contract rule (G-01 to G-04, CO-01 to CO-08) states this constraint. No rubric dimension in §5.2 (lines 1497-1509) checks that the agent stated no arrival date, including "Refund id reported" and "Refund status reported" on the success paths. An agent that tells every customer "your money will arrive in 5-10 business days" passes every scenario.
Pattern: an input constraint that appears only in the "must not" list of Scope & Authority, with no Contract rule protecting it and no scenario or dimension asserting it.

## R1-07 (Important)
Sources: B-coverage F2, A-coverage F1

R1-07 | Gap | Important | Failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" (line 96); G-02, CO-04
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: The only scenario that triggers this row is CO-S03. Its Turn 2 is scripted "in place of a confirmation" (line 248) and changes only the order. No scenario's confirming turn itself carries a change (for example "Yes, but put it on my Mastercard" or "Yes, but make it HG-10511"). CO-S09 puts the different payment method in Turn 1 (lines 587-589), before any proposal exists. Packet Round 1 Q4: "any change after confirmation voids it". An agent that reads "Yes, but …" as a confirmation, then cancels and refunds, passes the whole suite.
Pattern: a compound failure-row condition where only one of its causes (here, a change in place of confirmation) has a scenario whose Initial state or User turns trigger it.

## R1-08 (Important)
Sources: B-coverage F3, B-faithfulness F4

R1-08 | Gap | Important | G-03; success-path scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16; CO-08
Quote: "The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: On every success path the refund status is pending (for example CO-S01 line 139). The only check on the agent's words there is the message check "Refund id reported" (CO-S01 Unambiguity note, line 170: "the only check on the agent's words"). An agent that says "refund RF-5531 has been issued" when it is pending therefore passes. The status the agent reports is graded only in CO-S19 ("Refund status reported", line 1507). §2 (line 9) says the customer "wants to be told truthfully whether the order was cancelled and where the refund stands", yet CO-08 requires the agent to tell only the refund id. Packet Round 2 Q4, case 3: "Final message must match the final refund status."
Pattern: a G-03 truthfulness clause, or a stakeholder interest in being told an outcome, that is asserted by a rubric dimension on failure paths but by no dimension on the success paths where the same false claim is possible.

## R1-09 (Nit)
Sources: B-coverage F4, A-coverage F8

R1-09 | Gap | Nit | Failure row "the order system did not answer the first CO-A2" (line 100)
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, … If the lookup does not answer, …"
Evidence: use-case checklist (cockburn-checklist.md, Failure handling): "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." The "lookup answers but the order is not in the list" branch is missing. That result can happen: OrderNotFound is a declared cancel_order outcome (packet, tool confirmation turn, change 1), and CO-S24 already sets up the order system reporting a listed order as not found. Nit because CO-05 and CO-06 already block a further CO-A2 and any CO-A3, and CO-07's "cannot tell whether the order was cancelled" plausibly decides the handoff.
Pattern: a lookup-branching failure row with no "nothing found" branch.

## R1-10 (Nit)
Sources: B-coverage F5

R1-10 | Gap | Nit | §4.1 Failure handling (rows at lines 90-93); CO-01, CO-02
Quote: "absent"
Evidence: use-case checklist brainstorm: "the lookup returns more than one plausible match, or none". The rows cover more than one open order with no order named (line 90), a named number not on the account (line 91), and a named order that is shipped, delivered or cancelled (lines 92-93). No row covers an unnamed request ("I want to cancel my order") when the customer has no orders at all, or none with status placed or processing. The rows at lines 92-93 are keyed to "the named order", so they do not apply. CO-01 keeps the agent from proposing, so no write is at risk, but what the agent tells the customer is left undefined.
Pattern: an ambiguous-match failure covered for "more than one" but not for "none" when the user names no record.

## R1-11 (Important)
Sources: B-faithfulness F3

R1-11 | Lies | Important | CO-08; dimension "Refund id reported" (CO-S01, S02, S03, S09, S12, S13, S16, S19)
Quote: "The order has status cancelled, exactly one refund exists for it ... and the agent tells the customer the refund id."
Evidence: No input requires the agent to tell the customer the refund id. The packet's only reporting requirement for the success and timeout paths is "Final message must match the final refund status" (line 54) and "pending or issued, report that status" (line 63). The refund id is not among the confirmed derivations either (lines 70-73). Because of this, an agent that reports "order cancelled, your $86.40 refund to Visa ending 4242 is pending" without the id fails eight scenarios, although the inputs call that behavior correct.
Pattern: A success guarantee adds a reporting requirement the inputs do not state, and a pass condition across many scenarios is built on it.

## R1-12 (Nit)
Sources: B-faithfulness F5

R1-12 | Lies | Nit | G-04; Appendix B SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1544) is just such a guarantee for cancellation: "cancelling an order that is already cancelled returns it cancelled and changes nothing". G-04's general clause therefore permits a blind CO-A2 resend after a timeout. The spec already applies the same reasoning to CO-A4 through SG-03 (failure row, line 106). The input forbids a blind resend: "If the cancel call times out: no blind resend; re-read the order" (packet line 64). CO-06 (line 77) and the CO-S12 and CO-S13 Forbidden lines enforce the input, so no verdict changes, but the global rule says the opposite of the input.
Pattern: A general retry permission keyed on "guarantees nothing new" covers a supporting-actor guarantee for an action the input says must not be blindly retried.

## R1-13 (Important)
Sources: A-coverage F3

R1-13 | Gap | Important | CO-01 / CO-S06; row "the lookup shows the named order with status cancelled"
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

## R1-14 (Important)
Sources: A-coverage F6

R1-14 | Gap | Important | G-01 / CO-06 / CO-02
Quote: "The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation"
Evidence:
- Known failure case 1 (review-packet.md Round 2 Q4) has a customer with two open orders.
- Nothing in the inputs or the spec says what happens when that customer wants both cancelled ("cancel both my orders"), or asks for a second order after the first succeeds.
- CO-06 counts per conversation and allows a second CO-A2 only after an unanswered first, which forbids cancelling the second order. CO-02 (line 65) says every proposal names one order. G-01 (line 18) limits the agent to "the one order the current request is about".
- No rule, failure row or scenario says what the agent tells the customer in this case, so the coder will invent it.
Pattern: a realistic multi-record request the per-conversation caps silently forbid, with no stated handling.

## R1-15 (Nit)
Sources: A-coverage F7

R1-15 | Gap | Nit | CO-02 (act-only-when, holding-back side)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-S02 is the acting scenario. In every other scenario Turn 1 names the order number:
- CO-S01's three rows, even though it also has delivered HG-09977;
- CO-S03 to CO-S24, "Please cancel order <order>".
No scenario has exactly one open order and an unnamed request ("cancel my order"), where the agent should propose without asking.
Pattern: an "act only when" rule with an acting scenario and no holding-back scenario.

## R1-16 (Nit)
Sources: A-coverage F9

R1-16 | Gap | Nit | CO-A3 failure row "payment provider temporarily unavailable for the second CO-A3"
Quote: "Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence:
- Known failure case 3 (review-packet.md Round 2 Q4): after a refund timeout the agent "retries once, then re-reads the order and refund records and reports what it finds".
- Round 3 Q3: "For case 3, after the retry the agent re-reads the refund record."
- This row applies to any second CO-A3 that reports the provider unavailable, including one after a timed-out first call that may have created the refund. It skips the re-read and states "not issued".
- No scenario has a timeout followed by provider unavailable: CO-S16's rows end in success and CO-S18 is unavailable twice.
- Nit because SG-01 (line 1541) arguably means a second call would have returned a refund that the first call created.
Pattern: a combination of outcomes from a known failure case that falls into a row with different handling than the input prescribes, with no scenario.

## R1-17 (Important)
Sources: A-verdicts-codex F1

R1-17 | Ambiguous | Important | CO-S01–CO-S21, CO-S23–CO-S24, Initial state / Final state assertions
Quote: "- No follow-up task exists."
Evidence: Each affected scenario makes an exact final assertion about the number of follow-up tasks, at these lines of agent-spec.md: CO-S01:141, CO-S02:201, CO-S03:263, CO-S04:320, CO-S05:372, CO-S06:422, CO-S07:471, CO-S08:521, CO-S09:576, CO-S10:630, CO-S11:680, CO-S12:735, CO-S13:792, CO-S14:850, CO-S15:908, CO-S16:967, CO-S17:1025, CO-S18:1081, CO-S19:1137, CO-S20:1195, CO-S21:1255, CO-S23:1375 and CO-S24:1429. Only CO-S22 constrains the pre-existing task population; CO-S23 merely says its two calls create none. The evaluation checklist (evaluation-checklist.md, lines 34-42) requires every fact needed by a grader to have a value in Initial state.
Pattern: An exact final-state cardinality is asserted for an entity whose starting population is unspecified, so the verdict depends on whether the test author assumes an unstated empty set.

## R1-18 (Important)
Sources: A-verdicts-codex F2

R1-18 | Untestable | Important | CO-S03 and CO-S04, User block
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: The line occurs at agent-spec.md:248 and :308. Section 5.1 defines and labels a "confirmation question" at agent-spec.md:1459-1461, but does not define or label a question that merely "proposes cancelling … and asks to go ahead." The scenario checklist (evaluation-checklist.md, lines 34-42) expressly requires a scripted User turn to be triggered by a §5.1-defined event and says never to use "a proposal".
Pattern: A scripted user turn is anchored to an undefined semantic description rather than a harness-recognizable event; it must be reworded to a defined event before it can become one deterministic step.
