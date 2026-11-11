# Round 1 merged findings

17 merged findings: 14 Important, 3 Nit.

## R1-01 | Lies | Important | sources: faithfulness:F1, verdicts:F5, coverage:F6

[faithfulness F1]
F1 | Lies | Important | CO-A3 failure row "reported the order not cancelled"; CO-S17 Data variants row 3; CO-S24 Initial state
Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. |" and CO-S17 row 3: "is answered by the order system with the order not cancelled, and creates no refund"
Evidence: Appendix A (agent-spec.md line 1525) defines `OrderNotCancelled` as "the order is not cancelled". In CO-S17 the CO-A2 just returned `status: "cancelled"` (Reference trajectory step 5), and Final state says "HG-10482 has status cancelled". So the injected result cannot be true at that call. The failure row (line 103) then requires the agent to tell the customer "the order is cancelled" right after the order system said it is not. The shared rubric "Refund not issued reported" (line 1505) requires "the order is cancelled". An agent that truthfully reports the store's latest answer fails. No input says how to handle OrderNotCancelled. The packet's tool confirmation turn only adds the outcome ("issue_refund adds outcome OrderNotCancelled"). The same pattern shows in CO-S24 (lines 1411, 1414): the order "belongs to the customer", CO-A1 returned it, and the Final state keeps it with status <status>, yet CO-A2 returns `OrderNotFound`, which Appendix A defines as "order not found".
Pattern: A scenario injects a tool outcome whose Appendix A meaning contradicts the scenario's own Initial state and earlier results. The failure row then tells the agent to assert a fact that the latest tool result contradicts. Either give each injected outcome a world state where it can be true, or drop the scenario and row, or make the required message match what the system reported.

[verdicts F5]
F5 | Lies | Important | CO-S17 row 3; CO-S24, Initial state
Quote: "is answered by the order system with the order not cancelled, and creates no refund" (CO-S17 row 3); "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." (CO-S24)
Evidence:
- CO-S17: the CO-A2 just before answers normally, which Appendix A says "Sets the order's status to cancelled when it returns status: \"cancelled\"". The injected `OrderNotCancelled` outcome ("the order is not cancelled") cannot be true at the CO-A3 call. Its rubric "Refund not issued reported" then requires the agent to say "the order is cancelled" just after the system said it is not, so an agent that reports the system's answer, or says the cancellation is uncertain, fails.
- CO-S24: Initial state says "Order <order> belongs to the customer" and the CO-A1 just before returned it, so `OrderNotFound` cannot be true of the order at the CO-A2 call.
The verification brief requires that an injected outcome "must still describe something that can be true of the scenario at that call, given its Initial state and the results of the calls before it."
Pattern: A failure injected through Initial state that contradicts world state or an earlier call's result. Either change the setup so the outcome can occur (for example, a cancellation whose answer the agent never saw) or drop the row.

[coverage F6]
F6 | Lies | Important | CO-S17, Data variants row 3
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Appendix A defines `issue_refund`'s outcome "the order is not cancelled: `OrderNotCancelled`" (l.1525). In CO-S17, CO-A2 returns cancelled (reference step 5, l.1044), and Final state asserts "HG-10482 has status cancelled." (l.1023). So when CO-A3 runs, the order is cancelled, and the tool's own contract cannot return `OrderNotCancelled`. The Initial-state value lies outside the contract it is supposed to fall within. A correct agent that sees the conflict and looks up the order (it shows cancelled) has no consistent rule to follow. It might reasonably treat the cancellation as uncertain and use reason cancellation unknown, failing the Required event "reason refund not issued" (l.1020) and the rubric "Refund not issued reported", which requires saying "the order is cancelled" (l.1505).
Pattern: An Initial-state outcome for a supporting actor contradicts the world state and the Appendix A outcome condition that the same scenario sets up.

**Verifier:** R1-01 | Real | Important | I found nothing that refutes it. §5.1 "A supporting actor answers every call normally unless an Initial-state line says otherwise" lets the scenario inject an outcome, but the outcome still has to be possible at that call. Appendix A defines `OrderNotCancelled` as "the order is not cancelled". In CO-S17 the CO-A2 just before returned cancelled (Reference step 5), and Final state says "HG-10482 has status cancelled", so row 3's outcome cannot be true at the CO-A3 call. Failure row 103 and the "Refund not issued reported" rubric then make the agent say "the order is cancelled" right after that answer. CO-S24 has the same problem: its Initial state says "Order <order> belongs to the customer" and CO-A1 returned it, yet the next CO-A2 gets `OrderNotFound`. No input says how to handle OrderNotCancelled; the packet only records that it was added ("issue_refund adds outcome OrderNotCancelled").

**Decision:** kept (Important) — status: open. Reason: Partly fixed: CO-S17 row 3 removed, because OrderNotCancelled cannot be true right after CO-A2 returned cancelled. Open: no input says in what world OrderNotCancelled (after the agent saw the order cancelled) or OrderNotFound (for an order the lookup just listed) can occur, nor what the agent then tells the customer; the CO-A3 failure row's 'order not cancelled' branch and CO-S24 stand until the user decides.

## R1-02 | Lies | Important | sources: faithfulness:F2, coverage:F5

[faithfulness F2]
F2 | Lies | Important | Failure row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. |"
Evidence: The review packet, interview round 3 Q4 (confirmed "Yes to all"), says: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Re-read fails, say outcome unknown, issue no refund, hand off." The rule covers any cancel timeout, so the re-read applies after the second one too. The row instead skips the re-read and forbids CO-A3 even when the order was in fact cancelled. That also contradicts the spec's own rules. CO-07 makes CO-A4 for cancellation only "when the agent cannot tell whether the order was cancelled" and says "CO-A4 occurs in no other situation". G-03 makes "unknown" the message only "when it cannot tell". CO-S15 hides the conflict: its Initial state makes every lookup after the second CO-A2 go unanswered, and it requires no lookup. An agent that skips the input's re-read passes. In production, an order cancelled by the second call is left cancelled with no refund, handed off as "cancellation unknown", and the customer is told the outcome is unknown.
Pattern: The failure row for a repeated unanswered commit drops the re-read and branch-on-result procedure that the input sets for every unanswered call of that kind.

[coverage F5]
F5 | Gap | Important | Failure handling rows for unanswered CO-A2; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. |"
Evidence: Instances:
(a) After the second unanswered CO-A2, the row has no lookup branch. Lookups are unlimited (l.77, l.1519; user change 4: "Reads may be retried on timeout without limit"), so a lookup can still answer and show the order cancelled, open or shipped. In that case the row conflicts with three rules:
- CO-07 allows CO-A4 "cancellation unknown" only when "the agent cannot tell whether the order was cancelled" and says "CO-A4 occurs in no other situation" (l.80).
- CO-05 allows CO-A3 when "a lookup shows cancelled" (l.74).
- G-03 asks the agent to report what a lookup shows (l.24).
CO-S15 avoids the question by making every CO-A1 after the second CO-A2 unanswered (l.892). No scenario has an answered lookup after a second unanswered CO-A2, so the case where the late cancel did land (customer cancelled, never refunded, task mislabelled) is never decided or tested.
(b) The first-unanswered-CO-A2 row (l.100) branches on a lookup that shows cancelled, open, shipped/delivered, or no answer. It has no branch for a lookup that answers without the order. The spec itself allows an order that was listed to come back `OrderNotFound` (CO-S24, l.1414). The Cockburn checklist says: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer."
Pattern: After an unanswered commit call, the follow-up lookup's results are not all mapped to handling. A coder or agent will invent the missing else-branches, and the scenario sidesteps them by making the lookup fail.

**Verifier:** R1-02 | Real | Important | I found nothing that refutes it. Round 3 Q4 ("If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund... Re-read fails, say outcome unknown") covers any cancel timeout, including the second. Row 101 has no re-read branch and requires CO-A4 "cancellation unknown" and no CO-A3 whatever a lookup shows. That contradicts CO-07 ("when the agent cannot tell whether the order was cancelled... CO-A4 occurs in no other situation"), CO-05 (a refund is allowed when "a lookup shows cancelled") and G-03 ("when it cannot tell"). CO-S15's Initial state ("does not answer any CO-A1 the agent makes after its second CO-A2") steps around the case and settles nothing. Part (b), the first-timeout row having no branch for a lookup that answers without the order, also stands under the Cockburn checklist ("covers every result of the lookup: nothing found...").

**Decision:** kept (Important) — status: fixed. Reason: Second-unanswered-CO-A2 row now looks up and branches (cancelled: CO-A3; open: report not cancelled, no CO-A3/CO-A4; shipped; no answer: CO-A4 cancellation unknown); CO-S15 gains the lookup; new CO-S25, CO-S26 and dimension 'Cancellation not done reported'. Part (b), a lookup that answers without the order, is left as an open question.

## R1-03 | Ambiguous | Important | sources: verdicts:F2, faithfulness:F6

[verdicts F2]
F2 | Ambiguous | Important | G-04 vs CO-06 / CO-A2 failure rows / SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (Appendix B) says the order system makes cancellation idempotent: repeating a cancellation "returns it cancelled and changes nothing". G-04's second clause therefore allows a blind second CO-A2 after a timeout. CO-06 ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing"), the CO-A2 no-answer failure row, CO-S12 (Forbidden "A second CO-A2") and CO-S13 (Forbidden "A second CO-A2 before a CO-A1 made after the first CO-A2") all forbid it. The input agrees with CO-06: review-packet round 3 Q4, "If the cancel call times out: no blind resend; re-read the order." Under G-04 a blind cancel retry is allowed; under CO-06 it is forbidden. An agent built to G-04 fails CO-S12 and CO-S13.
Pattern: A global rule's general exception (any idempotency guarantee) is wider than the capability rule. This spec cites four idempotency guarantees, so G-04 must either name the actions its exception covers or exclude CO-A2.

[faithfulness F6]
F6 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 (line 1544) gives exactly such a guarantee for cancellation: "cancelling an order that is already cancelled returns it cancelled and changes nothing". So G-04 as worded permits a blind resend of CO-A2 after a timeout. The input forbids that: round 3 Q4, "If the cancel call times out: no blind resend; re-read the order." The user's later change, making cancel_order idempotent, did not withdraw that rule. CO-06 and the Forbidden lines in CO-S12 and S13 still forbid the blind resend, so no verdict changes.
Pattern: A global permission is written as a general condition, and a supporting-actor guarantee added later makes it license behavior the input forbids. Name the guarantees it covers (SG-01, SG-03) instead.

Checked with no defect found: tool names and parameters against the confirmed tool set; dates (2026-11-05 is a Thursday, and "placed yesterday" resolves to HG-10511); every Reference trajectory against its Data variants row 1; Required events and Final state for every other row; the refund and task idempotency effects in CO-S16, S19, S21 and S22.

**Verifier:** R1-03 | Not real | Nit | CO-06 settles the whole case: "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing." The Forbidden lines enforce it: CO-S12 "A second CO-A2" and CO-S13 "A second CO-A2 before a CO-A1 made after the first CO-A2". G-04's own exception cites only "(Appendix B, SG-01)", the refund guarantee. No trajectory gets a different verdict and no agent behavior is left open. The faithfulness reviewer concedes "no verdict changes".

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: CO-06 ('It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing') and the Forbidden lines of CO-S12 ('A second CO-A2') and CO-S13 decide every trajectory the finding names, and G-04's exception cites only SG-01; no verdict is left to judgment.

## R1-04 | Lies | Important | sources: faithfulness:F3

[faithfulness F3]
F3 | Lies | Important | Failure row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported" as used by CO-S20
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: The review packet, interview round 3 Q3 (confirmed), covers exactly this case (refund timed out, retried, then re-read): "failed or no refund, hand off and say the refund is not confirmed yet". The spec swaps in a different statement, "the refund has not been issued". This appears in the failure row (line 105), in CO-S20 Reference trajectory step 10, and in the "Refund not issued reported" rubric (line 1505), which CO-S20 uses. An agent that follows the input and says the refund "is not confirmed yet" can fail a rubric that requires "has not been issued".
Pattern: A message the input specifies for a failure case is replaced with a stronger claim of the spec's own. The shared rubric then grades the substitute.

**Verifier:** R1-04 | Real | Important | Partly answered, not refuted. Round 2 Q4 case 3 ("re-reads the order and refund records and reports what it finds") supports saying the refund failed or does not exist. What stands: round 3 Q3, confirmed with "Yes to all", sets this exact case's message as "failed or no refund, hand off and say the refund is not confirmed yet". Row 105, CO-S20 Reference step 10 and the rubric "Refund not issued reported" (line 1505) require "the refund has not been issued" instead, so an agent that uses the input's words can fail the rubric.

**Decision:** kept (Important) — status: fixed

## R1-05 | Lies | Important | sources: faithfulness:F4

[faithfulness F4]
F4 | Lies | Important | CO-08; message check "Refund id reported" (CO-S01, S02, S03, S09, S12, S13, S16, S19)
Quote: "The order has status cancelled, exactly one refund exists for it ... and the agent tells the customer the refund id."
Evidence: No input asks the agent to tell the customer the refund id. product-idea.md says nothing on it. The packet mentions the refund id only as a field (round 2 Q3) and as the idempotency key ("repeated calls return the same refund id"). What the input does require about the final message is: "Final message must match the final refund status" (round 2 Q4, case 3). As a result, CO-08 and the code check "Refund id reported" (line 1497) fail any success-path agent that reports the cancellation and the pending refund without the id, in eight scenarios. Meanwhile, apart from CO-S19, no success-path scenario checks the status the input does require.
Pattern: The spec invents a success-message requirement the inputs do not state, and makes it a pass condition across scenarios.

**Verifier:** R1-05 | Real | Important | I found nothing that refutes it. No input requires telling the customer the refund id: product-idea.md is silent, and the packet mentions the refund id only as a field (round 2 Q3) and as the idempotency key ("repeated calls return the same refund id"). It is also not among the derivations the user confirmed in the shared-understanding summary. CO-08 ("the agent tells the customer the refund id") and the message check "Refund id reported" still make it a pass condition in 8 scenarios.

**Decision:** kept (Important) — status: open. Reason: The fix is to CO-08's text, which step 4.5 stops at: proposed rule change for the user (drop 'and the agent tells the customer the refund id', or confirm it); the message check 'Refund id reported' follows the rule and stands with it.

## R1-06 | Lies | Nit | sources: faithfulness:F5

[faithfulness F5]
F5 | Lies | Nit | Appendix A, CO-A3 row, "Outcomes, as tool results"
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The confirmed refund data model (packet, round 2 Q3 plus the user's changes) is: refund id, order number, amount, payment method, status (pending, issued, failed). The tool confirmation turn says only "terminal refund error returns a refund with status failed". No input defines a `failure_reason` field or its enum values. No verdict reads it.
Pattern: Appendix A adds a return field and enum values that are not in the confirmed tool or data model.

**Verifier:** R1-06 | Style only | Nit | No verdict or behavior depends on it. The `failure_reason` enum is in Appendix A only. No Required, Final state, Forbidden or rubric line reads it, and row 103 handles every failed refund the same way. The values also follow round 3 Q3's terminal cases ("card closed or expired) or the provider declines"). Appendix A is labeled "Interface binding (provisional)... architecture notes may rewrite it".

**Decision:** kept (Nit) — status: fixed. Reason: Style only rejected: the finding is about a return field and enum the inputs do not define, a content defect (Lies), not wording, style, formatting, heading or preference.

## R1-07 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | CO-01, CO-S06, Initial state
Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence: The trigger covers "The customer asks to cancel an order or to get their money back for an order" (agent-spec.md l.58). The primary actor wants "to be told truthfully whether the order was cancelled and where the refund stands", and the support team wants "no customer told a refund is on its way when it is not" (l.9, l.11). CO-A1 returns each order's refund, which may be null or have status pending, issued or failed (Appendix A l.1523). For a cancelled order, CO-01 only says "tells the customer the order is already cancelled" (l.62), and failure row l.93 says the same. CO-S06, the only scenario with an already-cancelled order, gives it an issued refund in both rows (l.406, l.432-435). No scenario has a cancelled order with no refund or a failed refund, which is exactly the customer who comes back asking for their money. An agent that tells that customer "your refund has been issued" breaks G-03 (l.24) and still passes every scenario.
Pattern: An infeasible-path scenario sets the related record only to its harmless value (refund issued). The values the agent could misreport (no refund, failed, pending) never appear, and no rule says what to tell the customer about them.

**Verifier:** R1-07 | Real | Important | I found nothing that refutes it. G-03 and CO-01 ("for an order with status cancelled, it tells the customer the order is already cancelled") govern what the agent says, but under the brief's Gap limit a rule does not refute a gap that no scenario asserts. CO-S06 is the only already-cancelled scenario, and both its rows have "status issued". The rules also leave the agent's action open here: CO-05 allows CO-A3 for an order "a lookup shows cancelled", and CO-07 calls for CO-A4 "When the order is cancelled but its refund is not shown pending or issued". So for a cancelled order with no refund or a failed one, it is unclear whether the agent refunds, hands off or does nothing.

**Decision:** kept (Important) — status: fixed. Reason: CO-S06 gains rows with a failed refund and no refund, the already-cancelled failure row says no CO-A3 and no CO-A4 (input: 'reports that and changes nothing'), and 'Already cancelled reported' checks the stated refund status. CO-07's literal reach to an already-cancelled order is a rule text change, proposed to the user.

## R1-08 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | 4.1 Scope & Authority / Contract
Quote: "promise a date by which the refunded money arrives."
Evidence: The input is round 3 Q1, "The agent promises nothing about when the money arrives." (review-packet.md, Round 3), which the user accepted with "Yes to all". Round 2 Q2 had first proposed "money arrives in 5 to 10 business days". In the spec this appears only as a must-not bullet (agent-spec.md l.49). No Contract rule CO-01 to CO-08 or G-01 to G-04 states it, no stakeholder interest names it, and no rubric dimension in §5.2 (l.1497-1509) checks for an arrival-date promise. An agent that tells the customer "the refund will arrive in 3-5 business days" passes every success scenario (CO-S01, S02, S03, S09, S12, S13, S16, S19).
Pattern: A domain rule from the interview appears only as a Scope & Authority must-not. It needs a Contract rule, and a rubric dimension on the success scenarios to enforce it.

**Verifier:** R1-08 | Real | Important | I found nothing that refutes it. The input (round 3 Q1: "The agent promises nothing about when the money arrives") appears only as the Scope & Authority bullet "promise a date by which the refunded money arrives." No §5.2 dimension (lines 1497-1509) and no scenario asserts it. Under the brief's Gap limit, the must-not bullet does not refute the finding.

**Decision:** kept (Important) — status: fixed

## R1-09 | Gap | Important | sources: coverage:F3

[coverage F3]
F3 | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming"; G-02
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: G-02 says "Any change to a proposal term after confirmation voids that confirmation" (l.21). The only scenario with a change is CO-S03, and there Turn 2 comes "in place of a confirmation" (l.248) with no assent in it (rows l.275-277). CO-S09 asks for a different payment method in Turn 1, before any proposal exists (l.587-589). No scenario has a confirming turn that also changes a term, such as "Yes, but put it on my Mastercard" or "Yes, cancel HG-10511 instead". So an agent that reads "yes, but…" as confirmation and cancels on the old proposal passes every scenario. That agent violates G-02, and this row changes the outcome.
Pattern: A failure row that changes the outcome is never triggered by any scenario. Its nearest scenario exercises a different turn position: a change before confirmation, not one inside the confirming turn.

**Verifier:** R1-09 | Real | Important | I found nothing that refutes it. Row 96's condition is "in the confirming turn or after confirming, before CO-A2". CO-S03's Turn 2 comes "in place of a confirmation", so it is not a confirming turn and does not trigger the row. CO-S09's change comes in Turn 1, before any proposal exists. No scenario has an assent that also changes a term, or a change after confirming, so the row changes the outcome but no scenario triggers it.

**Decision:** kept (Important) — status: fixed

## R1-10 | Gap | Important | sources: coverage:F4

[coverage F4]
F4 | Gap | Important | CO-02, holding-back side
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-02 is an "act only when" rule for asking which order. CO-S02 is the acting scenario. There is no graded holding-back scenario:
- Every CO-S01 row names its order (l.155-157).
- No scenario has exactly one open order and an unnamed request ("cancel my order"). CO-S01's Initial state, with one open order and delivered HG-09977, would be the natural place for one.
- In CO-S03 (two open orders, order named), a needless "which order?" is simply deflected, because no User-knows pair or deflection is scored. §5.2 says precision is "never folded into the score" (l.1489).
The evaluation checklist says: "For every rule that says 'act only when', one scenario shows the agent acting when it should and one shows it holding back... test only 'asks when unsure' and you get an agent that always asks", and asks for a deflection pair when over-asking is under test (evaluation-checklist.md, Scenario design). As written, an agent that always asks which order passes everything. So does one that, given an unnamed request, never proposes the single open order.
Pattern: An "act only when" clarification rule has an acting scenario but no holding-back scenario that scores the unneeded question or the unneeded refusal to proceed.

**Verifier:** R1-10 | Real | Important | I found nothing that refutes it. CO-S01 and CO-S03 name their order, but a needless "which order?" there is only deflected, and §5.2 interaction precision is "never folded into the score". No scenario has a single open order and a request that names none. The evaluation checklist requires a holding-back scenario for "act only when" rules ("test only 'asks when unsure' and you get an agent that always asks"), and the brief's Gap class lists this case.

**Decision:** kept (Important) — status: fixed

## R1-11 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | CO-S02, User knows / Expected / Unambiguity note
Quote: "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes."
Evidence: The confirmation pair has no scope marker, so under §5.2 ("A pair marked (after Turn n) is revealed only after Turn n") it is in scope from the start. Consider an agent that never asks which order and proposes "cancel HG-10511, refund $23.75 to Mastercard ending 8810" straight away. In rows 1 and 3 the simulated user answers "Yes", the agent's CO-A2 then comes after the confirmation turn, and every Required event, Final state line and Forbidden line passes. An agent that tries the other order when a wrong-value proposal is deflected passes row 2 the same way. Interaction recall would catch the missing question, but it is "never folded into the score" (§5.2). This contradicts CO-02 ("asks which and proposes nothing until the customer names one") and the scenario's own Unambiguity note ("a cancellation before the confirmation turn, which follows the which-order answer"): nothing in the Expected block makes the confirmation turn follow the which-order answer. The guessed-order run, which CO-S02 exists to catch, passes per variant.
Pattern: A clarify scenario whose confirmation pair is reachable without the clarifying answer. Nothing in the Expected block ties the authorizing write to the clarifying answer, so a guessed value that happens to be right passes.

**Verifier:** R1-11 | Real | Important | I found nothing that refutes it. The confirmation pair in CO-S02's User knows has no "(after Turn n)" marker, so §5.2 puts it in scope from the start. A guessed proposal with the right values matches it under §5.1, gets "Yes", and passes every Required, Final state and Forbidden line. Nothing in the Expected block enforces CO-02's "proposes nothing until the customer names one" or the Unambiguity note's "the confirmation turn, which follows the which-order answer". Interaction recall would show the missing question but is not scored.

**Decision:** kept (Important) — status: fixed

## R1-12 | Gap | Nit | sources: coverage:F7

[coverage F7]
F7 | Gap | Nit | CO-01 / CO-02, Failure handling
Quote: absent
Evidence: The failure rows cover several cases: an unnamed request with more than one open order (l.90), a named number not on the account (l.91), and a named order that is shipped, delivered or cancelled (l.92-93). No row covers an unnamed request ("I want to cancel my order") from a customer whose lookup shows no orders at all, or no order with status placed or processing. The Cockburn brainstorm item "the lookup returns more than one plausible match, or none (ambiguous match)" gets a row only for "more than one". CO-01's per-order sentences assume a named order. Nothing is required here, so no verdict changes, but the agent's message on this path is unspecified.
Pattern: A lookup-driven ambiguity rule handles the many-match case but not the zero-match case for a request that names no order.

**Verifier:** R1-12 | Real | Nit | Partly answered, not refuted. CO-01 settles the proposing part: "The agent proposes cancelling an order only after a lookup shows it with status placed or processing." Its per-order sentences also cover a customer whose orders are all shipped, delivered or cancelled. What stands: for an unnamed request from a customer with no orders at all, no row or rule says what the agent tells them. The Cockburn checklist ("more than one plausible match, or none") calls for that row. No verdict changes.

**Decision:** kept (Nit) — status: open. Reason: No input says what the agent tells a customer with no orders at all who asks to cancel one; open question for the user.

## R1-13 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>." (CO-S19 and CO-S21); "The order system does not answer the agent's first or second CO-A3, and together they <refund effect>." (CO-S20)
Evidence: CO-06 says "lookups are not limited". In CO-S21 only lookups "after its second CO-A3" go unanswered, so a lookup between the two refund calls answers in all three scenarios. That is a valid variation (a different read-only lookup). "Together they create" does not say whether RF-5531 exists after the first call, so the harness cannot say what that lookup returns, and the verdict depends on it:
- If the lookup shows RF-5531 pending or issued (CO-S19, CO-S21 row 1), an agent that reports it and makes no second CO-A3 fails "CO-A3 occurs exactly twice".
- If it shows RF-5531 failed (CO-S20 row 1, CO-S21 row 2), an agent that treats the failure as terminal and hands off fails "CO-A3 occurs exactly twice" and "CO-A4 ... after the second CO-A3". CO-06 forbids retrying only after the refund call itself returned failed, not after a lookup showed it.
Pattern: An Initial-state effect shared across several unanswered calls ("together") leaves open which call produced it, so a read between those calls has no defined result.

**Verifier:** R1-13 | Real | Important | Partly answered, not refuted. Row 102 ("did not answer [the first CO-A3] | Make CO-A3 once more, relying on SG-01") makes the second refund call mandatory whatever a lookup between the calls shows. That settles the finding's two verdict examples for CO-S19 and CO-S20. What stands: "together they create" still leaves undefined what a CO-A1 between the two CO-A3 calls returns, so the harness cannot render it. Against the checklist's "Concrete initial state" and "anchored to a state-changing call", the verdict in CO-S21 depends on that result. If that lookup shows RF-5531 pending (row 1), G-03 ("or a lookup shows it") and CO-07 ("not shown pending or issued after the retries") let the agent report pending without a handoff, which fails the Required "CO-A4... reason refund status unknown".

**Decision:** kept (Important) — status: fixed

## R1-14 | Ambiguous | Important | sources: verdicts:F4

[verdicts F4]
F4 | Ambiguous | Important | CO-S16 row 2 (and CO-S19, CO-S20, CO-S21 once F3 is settled with the refund created by the first call), Required events
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: CO-S16 row 2 says the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". An agent that looks up after the unanswered call sees RF-5531 pending. Reporting it without a second refund call satisfies G-03 ("or a lookup shows it"), CO-08 and every Final state line, and CO-06 is only permissive ("It makes a second CO-A3 only after ..."). It still fails the Required line. Only the failure row "Make CO-A3 once more, relying on SG-01" makes the retry mandatory, and the evaluation checklist says "Outcome, not path ... a path assertion punishes them". One reviewer reads the failure row as binding; another reads CO-06, G-03 and the checklist as allowing the lookup path. They reach different verdicts on the same run.
Pattern: An exact count on a retry the agent may correctly skip once a read shows the first call took effect. Either state that the retry is required whatever a lookup shows, or assert the outcome (one refund, reported) and bound the count with "at most two".

**Verifier:** R1-14 | Not real | Important | Failure row 102 settles the whole case: its "Required behavior" for "the order system... did not answer [the first CO-A3]" is "Make CO-A3 once more, relying on SG-01". The row has no lookup condition, so the second CO-A3 is required whatever a lookup shows, in CO-S16 row 2 and in CO-S19 to S21. CO-06 does not conflict with it, because CO-06 only limits when a second CO-A3 may happen. G-03 governs what the agent reports, not whether it retries. "CO-A3 occurs exactly twice" asserts a state-changing call the spec requires, which the checklist allows ("Required events are state-changing calls").

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: failure row 'the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01' makes the second CO-A3 required with no lookup condition, so 'CO-A3 occurs exactly twice' is the spec's required behavior and one reading only; input case 3 says 'agent retries once, then re-reads'.

## R1-15 | Ambiguous | Important | sources: verdicts:F6

[verdicts F6]
F6 | Ambiguous | Important | CO-S09, rubric "Refund terms explained"
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: The reference trajectory's step 3, "Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242)", never says the refund is the order's total paid. It only states an amount. One judge counts "$86.40" as telling the customer it is the total paid; another does not, and fails the reference run. The agent can only pass if it volunteers a phrase that the judge reads as "total paid". CO-03's required statement and the reference run disagree on what the message must contain.
Pattern: A rubric clause the reference trajectory does not visibly meet, so whether stating a value counts as stating the rule is left to the judge.

**Verifier:** R1-15 | Real | Nit | Partly answered, not refuted. CO-03 ("tells the customer... that the refund is the total paid to the order's payment method") and row 95 match the rubric, so they settle what the agent must say. What stands: CO-S09 Reference step 3 only "states the proposal (... refund $86.40 ...)" and never says the amount is the total paid. So the reference run does not visibly meet "Refund terms explained", against the checklist's "Reference trajectory exists and passes".

**Decision:** kept (Nit) — status: fixed

## R1-16 | Ambiguous | Important | sources: verdicts:F7

[verdicts F7]
F7 | Ambiguous | Important | CO-S15, rubric "Cancellation outcome unknown reported"
Quote: "never says the order was cancelled or that it was not"
Evidence: §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call." In CO-S15 the lookup between the two cancellations answers "HG-10482 still processing" (reference step 6), and the agent truthfully narrates it alongside the second CO-A2 (for example "the first attempt didn't go through, so I'm trying again"). The judge must decide whether that interim, true statement breaks "never says ... that it was not". The definition fits CO-S14, where the agent never sees the status, but not CO-S15, where it does see it mid-trial. A correct agent with a correct final message can fail.
Pattern: A shared rubric "never says X" applied over the whole trial in a scenario where X is briefly true and visible to the agent. Bound it to the final report, or write the definition per scenario.

**Verifier:** R1-16 | Real | Important | I found nothing that refutes it. §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call", and the shared definition "never says the order was cancelled or that it was not" covers the whole trial. In CO-S15 the lookup shows "HG-10482 still processing" (Reference step 6) before the second CO-A2, so a true mid-trial remark can fail the dimension. That breaks the checklist's "A shared rubric dimension has one definition... must hold in every one of them". §5.1's "Agent message" definition does not bound rubric reading.

**Decision:** kept (Important) — status: fixed

## R1-17 | Ambiguous | Nit | sources: verdicts:F8

[verdicts F8]
F8 | Ambiguous | Nit | CO-S03 and CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: The evaluation checklist says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." "A question that proposes cancelling HG-10482" is not a §5.1 event. No confirmation-form pair for HG-10482 is in scope, so §5.1's confirmation question cannot apply. The simulated user has to judge whether a partial question (for example "Do you want HG-10482 cancelled?" with no amount) is the trigger. Both readings end in the same outcome lines, so no verdict changes.
Pattern: A scripted turn triggered by an undefined kind of agent message. Define the trigger, for example as a question stating the full proposal for a named order.

**Verifier:** R1-17 | Style only | Nit | No verdict changes. Whether the simulated user treats a partial question as the trigger or deflects it and waits for the full proposal, CO-S03 and CO-S04 end in the same Required, Final state and Forbidden results. In CO-S04 nothing is ever authorized, and in CO-S03 every action on HG-10482 is forbidden outright. The finding itself says "Both readings end in the same outcome lines, so no verdict changes."

**Decision:** kept (Nit) — status: fixed. Reason: Style only rejected: the finding is that a scripted turn's trigger is an undefined event (Ambiguous, per evaluation-checklist 'A User turn's trigger is a defined event'), not wording or preference.
