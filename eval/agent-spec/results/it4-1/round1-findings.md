# Round 1 merged findings

17 merged findings: 10 Important, 7 Nit.

## R1-01 | Lies | Important | sources: faithfulness:F1, coverage:F4, verdicts:F4

[faithfulness F1]
F1 | Lies | Important | CO-S24 Initial state; CO-S17 Data variants row 3; Failure handling row "CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled"
Quote: "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." / "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Both scenarios inject a tool result that cannot be true at that call, given the Initial state and the earlier calls.
- CO-S24: Initial state (agent-spec.md line 1411) says "Order <order> belongs to the customer", and reference step 2 has CO-A1 return that order as processing. Appendix A (line 1524) defines `OrderNotFound` as "order not found", and the agent then calls `cancel_order` with that same, existing number. No input says the order system can fail to find one of the customer's own listed orders. The packet's tool confirmation turn, change 1, only names `OrderNotFound` as an outcome. The scenario then requires the agent to tell the customer that an order it just listed "could not be found" (step 6, dimension "Order not cancelled reported").
- CO-S17 row 3: reference step 5 has CO-A2 return "cancelled", and Final state says "HG-10482 has status cancelled". Appendix A (line 1525) defines `OrderNotCancelled` as "the order is not cancelled", so this tool result contradicts both the earlier call result and the Final state.
- The failure row (line 103) carries the same contradiction. After the order system has just reported "the order not cancelled", it tells the agent to "tell the customer the order is cancelled" with reason refund not issued. No input says how OrderNotCancelled is handled (packet, tool confirmation turn change 2, only adds the outcome).
Pattern: A scenario injects an Appendix A outcome whose meaning contradicts its own Initial state or the results of earlier calls. The spec then builds required behavior and final-state lines on that impossible world.

[coverage F4]
F4 | Lies | Important | CO-S17, Data variants row 3 (Initial state value outside the tool contract)
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: In CO-S17, CO-A2 returns cancelled, which per Appendix A "Sets the order's status to cancelled", and Final state asserts "HG-10482 has status cancelled". Appendix A defines the `OrderNotCancelled` outcome of issue_refund as "the order is not cancelled". So this row has the order system return an outcome its own contract rules out for that state. The verdict then depends on which signal the agent believes. Dimension "Refund not issued reported" requires the agent to say "the order is cancelled". An agent that applies CO-07 ("when the agent cannot tell whether the order was cancelled") would hand off with reason cancellation unknown and tell the customer the outcome is unknown. Experts could reasonably call that correct, yet it fails both the Required event (reason refund not issued) and the rubric.
Pattern: Every Initial-state line that sets a tool outcome must describe a world that Appendix A's outcome definitions allow, given the state earlier calls in the same trial produced.

[verdicts F4]
F4 | Lies | Important | CO-S17 row 3; CO-S24 Initial state
Quote: "is answered by the order system with the order not cancelled, and creates no refund" (CO-S17 row 3); "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." (CO-S24, line 1414)
Evidence:
- CO-S17: the CO-A2 just before returned "cancelled", and Final state asserts "HG-10482 has status cancelled" (line 1023). Appendix A's outcome "the order is not cancelled: OrderNotCancelled" (line 1525) cannot be true at that call. The scenario then requires the agent to tell the customer "the order is cancelled" (failure row line 103; dimension "Refund not issued reported", line 1505). That is right after the order system said the order is not cancelled, which conflicts with G-03 (line 24).
- CO-S24: Initial state says "Order <order> belongs to the customer" (line 1411), and the reference lookup just returned it. Appendix A's OrderNotFound cannot be true of that order.
Pattern: An injected tool outcome must be something that can be true given Initial state and the results of earlier calls in the scenario.

**Verifier:** R1-01 | Real | Important | I could not refute it, and §5.1's limit applies directly. In CO-S17 row 3, CO-A2 has just returned "cancelled" (reference step 5) and Final state says "HG-10482 has status cancelled" (line 1023). Appendix A's OrderNotCancelled means "the order is not cancelled" (line 1525), which cannot be true at that call. In CO-S24, Initial state says "Order <order> belongs to the customer" (line 1411) and the lookup just listed that order, so OrderNotFound cannot be true of it either. The user's tool confirmation turn lists OrderNotFound and OrderNotCancelled as outcomes, but that only permits such lines in general. It does not make them possible at this call in these scenarios.

**Decision:** kept (Important) — status: open. Reason: Verifier Real. Only the user can say what situation produces OrderNotFound for an order list_orders just returned, or OrderNotCancelled right after cancel_order returned cancelled; the inputs name both outcomes (tool confirmation turn, changes 1 and 2) and no situation. Lines left unchanged; open question in the report.

## R1-02 | Lies | Important | sources: faithfulness:F2, coverage:F2

[faithfulness F2]
F2 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-06
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. |"
Evidence: Packet, round 3 Q4 (confirmed with "Yes to all"): "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." This applies to any cancel timeout. The spec row skips the re-read after the second timeout and forbids CO-A3 outright. That has three wrong effects:
- When a lookup would show the order cancelled, the input says "continue to refund". The spec forbids the refund and leaves a cancelled order unrefunded.
- When a lookup would show the order shipped, the input says report it and issue no refund, with no handoff. The spec requires a cancellation-unknown handoff and the "not known whether cancelled" message, which conflicts with CO-07 ("CO-A4 occurs in no other situation") and G-03.
- CO-S15 hides this by making every later lookup unanswered (line 892).
Pattern: A failure row for a repeated call drops the handling the inputs give for that outcome in general.

[coverage F2]
F2 | Gap | Important | Failure handling, CO-A2 timeout rows (lines 100–101)
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: (a) The input sets one rule for every cancel timeout: review-packet.md Round 3 Q4, "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." The row for the second CO-A2 timeout has no re-read and no branch on what a re-read finds. CO-S15's Initial state expects the agent to read again ("The order system does not answer any CO-A1 the agent makes after its second CO-A2", line 892), yet it covers only the branch where that read gets no answer. Suppose the read answers and shows the order cancelled: CO-05 allows CO-A3 and CO-07 forbids CO-A4 ("CO-A4 occurs in no other situation"; the agent can tell it was cancelled), while this row forbids CO-A3 and requires CO-A4. Suppose it shows shipped, or still open: no branch says what to do. (b) The first-timeout row (line 100) does branch on the read, but it misses one result: the order is gone from the list. That result is possible, since `OrderNotFound` is a declared cancel_order outcome (Appendix A). use-case checklist (cockburn-checklist.md): "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer."
Pattern: Every failure row that follows an unanswered commit call needs a branch for every result of the lookup made after it: cancelled, open, shipped/delivered, not found, and no answer. That applies to the second unanswered call as well as the first.

**Verifier:** R1-02 | Real | Important | The packet's round 3 Q4 begins "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund..." and covers every cancel timeout. Row 101 forbids CO-A3 and requires CO-A4 "cancellation unknown" with no re-read. If a lookup after the second timeout showed the order cancelled, CO-07 ("CO-A4 occurs in no other situation") would forbid the handoff that this row requires. CO-S15 line 892 covers only the branch where the lookup gets no answer, so the cancelled, shipped and open branches still stand.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. Second-unanswered-CO-A2 row now re-reads and branches as round 3 Q4 says; CO-S25 (lookup shows cancelled) and CO-S26 (lookup shows open or shipped) added; CO-S15 keeps the no-answer branch. Coverage F2(b), an 'order gone from the list' branch, answered: list_orders returns every order of the customer, cancelled included (user change 4), and no input lets a listed order disappear (see R1-01).

## R1-03 | Lies | Important | sources: faithfulness:F3

[faithfulness F3]
F3 | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Packet, round 3 Q3 (confirmed): "For case 3, after the retry the agent re-reads the refund record: ... failed or no refund, hand off and say the refund is not confirmed yet". The spec turns "not confirmed yet" into the stronger claim "has not been issued". CO-S20 (lines 1219, 1223) grades this with "Refund not issued reported" (line 1505), which requires "the refund has not been issued". An agent that says what the input specifies ("your refund is not confirmed yet") can fail that rubric in both CO-S20 rows.
Pattern: The spec swaps the customer-facing wording the user confirmed for a different claim, then grades the swapped wording.

**Verifier:** R1-03 | Not real | Important | An input supports the line in exactly this case. Round 2 Q4 case 3 says the agent "re-reads the order and refund records and reports what it finds. Final message must match the final refund status." For both branches the row covers, a refund with status failed and no refund, "the refund has not been issued" matches the final status, and "not confirmed yet" does not. "Has not been issued" also implies "not confirmed", so it does not contradict round 3 Q3. It is the stronger, status-matching wording, and G-03 ("Otherwise it tells the customer the action was not done") supports it too. This one is close, so it deserves a look.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Not real; refutation not agreed. The verifier's clause (round 2 Q4 case 3, 'Final message must match the final refund status') supports the status, but round 3 Q3, confirmed later and written for exactly this branch, says 'failed or no refund, hand off and say the refund is not confirmed yet'. The quoted clause does not answer the finding's case, an agent that says the confirmed wording failing the rubric. Fixed: row 105, CO-S20 trajectory and note, new dimension 'Refund not confirmed reported'.

## R1-04 | Lies | Important | sources: faithfulness:F4

[faithfulness F4]
F4 | Lies | Important | CO-08; CO-A3 failure row "did not answer the second CO-A3"; dimension "Refund id reported"
Quote: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id."
Evidence: No input requires the agent to tell the customer the refund id.
- product-idea.md, the interview rounds and the shared-understanding summary (which lists every derivation the user confirmed) say nothing about reporting the id. Round 2 Q3 only lists the refund id as a data field.
- The same unsupported requirement appears in failure row line 105 ("tell the customer that status and the refund id").
- It is graded by the message check "Refund id reported" in CO-S01, S02, S03, S09, S12, S13, S16 and S19 (line 1497). In all eight, an agent that truthfully says "order cancelled, $86.40 refund to Visa ending 4242 is pending" without the id fails.
Pattern: A success guarantee adds a required customer-facing detail no input asks for and grades it in every success scenario.

**Verifier:** R1-04 | Real | Important | I found no input that requires telling the customer the refund id. product-idea.md, rounds 1 to 3, the shared-understanding summary and the tool confirmation turn give the refund id only as a data field (round 2 Q3). Case 3 asks for the message to "match the final refund status", which is the status, not the id. CO-08, row 105 and the code check "Refund id reported" in 8 scenarios grade a requirement no input gives.

**Decision:** kept (Important) — status: open. Reason: Verifier Real. The fix changes rule CO-08's text, so it stops at the rule: proposed rule change for the user (before: '... no follow-up task exists for it, and the agent tells the customer the refund id.' after: '... no follow-up task exists for it, and the agent tells the customer the order is cancelled and the refund's status.'). The dependent lines (row 105's 'and the refund id', message check 'Refund id reported' in 9 scenarios) are left until the user decides.

## R1-05 | Lies | Nit | sources: faithfulness:F5

[faithfulness F5]
F5 | Lies | Nit | Appendix A, CO-A3 row
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`); payment provider temporarily unavailable: `ProviderUnavailable`"
Evidence:
- The data model the user confirmed (packet, round 2 Q3 plus the user's changes) lists the refund's fields as refund id, order number, amount, payment method and status (pending, issued, failed). It has no `failure_reason` field and no enum for it.
- The tool confirmation turn says only "terminal refund error returns a refund with status failed, transient error creates none". It names no `ProviderUnavailable` error, while the user did name the other errors (`OrderNotCancellable`, `OrderNotFound`, `OrderNotCancelled`).
- The same row's return shape `{refund_id, amount, payment_method, status}` also drops the order number from the data model.
- No verdict depends on these fields (CO-S17 and CO-S23 vary only the narrative "because ..." text).
Pattern: The interface binding invents fields or error names that the confirmed tool contract and data model do not have.

**Verifier:** R1-05 | Style only | Nit | The finding concedes "No verdict depends on these fields (CO-S17 and CO-S23 vary only the narrative 'because ...' text)". The transient outcome itself is confirmed (round 3 Q3: "transient = payment provider temporarily unavailable, retry once"; tool turn: "transient error creates none"), so the name `ProviderUnavailable` only labels a confirmed outcome. `failure_reason` and the missing order_number in the return shape change no Required, Forbidden, state or rubric line, and no agent behavior. Appendix A is also marked "(provisional)... architecture notes may rewrite it".

**Decision:** kept (Nit) — status: fixed. Reason: Verifier Style only; not dropped: the finding is about an invented field (failure_reason) in the binding, not about wording, style, formatting, heading choice or preference. Fixed: failure_reason removed from Appendix A's CO-A3 row. ProviderUnavailable answered: it names the confirmed transient outcome (round 3 Q3, tool turn 'transient error creates none'), and Appendix A is provisional.

## R1-06 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | G-02 / CO-04, Failure handling row "changed ... in the confirming turn or after confirming"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: This failure row changes the outcome, because the confirmation becomes void and no CO-A2 happens on the old proposal. But no scenario's User block triggers it. CO-S03 is the only change-of-proposal scenario, and its Turn 2 is scripted "in place of a confirmation" (agent-spec.md line 248). So the change comes before any confirmation, which is neither "in the confirming turn" nor "after confirming". The input asks for this case: review-packet.md, Round 1 Q4, "any change after confirmation voids it" (user: "Yes to all"). G-02 also says: "Any change to a proposal term after confirmation voids that confirmation." An agent that hears "Yes, but make it HG-10511" and cancels HG-10482, or cancels HG-10511 with no fresh confirmation, passes every scenario in the spec.
Pattern: When a failure row's condition is narrower than or different from the nearest scenario's trigger, that row has no scenario. Every outcome-changing row needs a scenario whose User turn or Initial state meets that row's condition exactly.

**Verifier:** R1-06 | Real | Important | No scenario's User block meets the row's condition "in the confirming turn or after confirming". CO-S03's Turn 2 is scripted "in place of a confirmation" (line 248), and its Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing". The row changes the outcome: the old confirmation becomes void and no CO-A2 follows on the old proposal. Input round 1 Q4 asks for this case ("any change after confirmation voids it").

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. CO-S03 row 4 'Yes, but cancel HG-10511 instead of that one.' changes the order in the confirming turn; note updated.

## R1-07 | Gap | Important | sources: coverage:F3, verdicts:F6

[coverage F3]
F3 | Gap | Important | 4.1 Scope & Authority "must not" / Contract / §5.2 dimensions
Quote: "- promise a date by which the refunded money arrives."
Evidence: review-packet.md Round 3 Q1, "The agent promises nothing about when the money arrives" (user: "Yes to all"). Round 2 Q2 had first proposed "money arrives in 5 to 10 business days", so an agent is likely to repeat that figure. The ban appears only in the Scope must-not list. No Contract rule states it, §2 names no stakeholder interest it serves, and no rubric dimension checks it. Every success scenario (CO-S01, S02, S03, S09, S12, S13, S16, S19) grades the agent's words only through message check "Refund id reported" and, in S19, "Refund status reported". So an agent that says "you'll see the money in 5–10 business days" passes all of them.
Pattern: When a domain rule from the inputs limits what the agent says, it needs a Contract rule and a rubric dimension in at least one scenario where the agent would be tempted to break it (the success report).

[verdicts F6]
F6 | Gap | Important | CO Scope & Authority, "must not"
Quote: "promise a date by which the refunded money arrives."
Evidence: Interview round 3 Q1, confirmed: "The agent promises nothing about when the money arrives" (review-packet.md line 61). Round 2 Q2 mentions "5 to 10 business days" (line 37), so the agent has an obvious date to promise. No rule CO-01 to CO-08 or G-01 to G-04 carries this prohibition, and no scenario or dimension asserts it. CO-S01 has no rubric at all, so a run that says "your money will arrive in 5-10 business days" passes every scenario.
Pattern: Each "must not" item needs a rule, and a scenario or dimension that fails a run violating it.

**Verifier:** R1-07 | Real | Important | Under the brief, being settled by a rule is not enough without a scenario or dimension that asserts it, and none asserts this. The only place the ban appears is Scope & Authority, "promise a date by which the refunded money arrives." No §5.2 dimension checks it ("Refund status reported" checks only "states no other status"), and CO-S01, S02, S03, S12, S13 and S16 have only the code check "Refund id reported". Input round 3 Q1 confirms the ban.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. New rule CO-09 'No arrival date promised' [minimal guarantee]; §2 Harbor Goods interest extended; rubric dimension 'No arrival date promised' on CO-S01.

## R1-08 | Gap | Nit | sources: coverage:F5

[coverage F5]
F5 | Gap | Nit | CO-03 / CO-S09
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: Nothing tests the "different amount" clause. CO-S09's rows (lines 587–589) ask for a new Mastercard, store credit and PayPal; no row asks for a different amount. In CO-S08, dimension "Whole order only explained" checks only the whole-order statement, not that the refund is the total paid to the order's payment method. issue_refund takes only order_number, so no state check can catch this; only the agent's words can be wrong.
Pattern: Every clause of a rule that requires the agent to tell the user something needs at least one data-variant row that triggers it and a rubric dimension that checks it.

**Verifier:** R1-08 | Real | Nit | One part is answered. CO-S09's dimension "Refund terms explained" ("the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit") asserts the told refund terms, but only for the triggers its rows use: different card, store credit and PayPal. Two parts stand. No row triggers CO-03's "different amount" clause. CO-S08's "Whole order only explained" also checks only the whole-order statement and not the refund-terms statement that CO-03 requires for partial-item requests.

**Decision:** kept (Nit) — status: fixed. Reason: Verifier Real. CO-S09 row 4 asks for a different amount; partial-items failure row, CO-S08 trajectory, note and dimension 'Whole order only explained' now carry CO-03's refund-terms statement.

## R1-09 | Gap | Nit | sources: coverage:F6

[coverage F6]
F6 | Gap | Nit | 4.1 Failure handling (no row)
Quote: absent
Evidence: cockburn-checklist.md brainstorm: "the lookup returns more than one plausible match, or none (ambiguous match)". The failure table has rows for "more than one ... placed or processing, and the customer has not said which" and "named an order number that is not among their orders". The shipped and cancelled rows apply only to "the named order" (lines 92–93). No row covers a customer who names no order when the lookup shows no order with status placed or processing: every order is shipped, delivered or cancelled, or the customer has no orders at all. The trigger "The customer asks to cancel an order or to get their money back" allows this ("I want to cancel my order"), and the agent can detect it. With no row, the agent's reply is unspecified.
Pattern: Every lookup used to resolve which record the user means needs rows for the none, one and many results, whether or not the user named the record.

**Verifier:** R1-09 | Real | Nit | CO-01 ("For an order with status shipped or delivered, it tells the customer...") settles the case where the customer names no order and none is open. Under the brief that is not a refutation without a scenario that asserts it, and none does. Rows 92 and 93 apply only to "the named order". Nothing covers a customer with no orders at all. The cockburn checklist ("the lookup returns more than one plausible match, or none") counts as evidence.

**Decision:** kept (Nit) — status: fixed. Reason: Verifier Real. New failure row 'the customer named no order, and none of the customer's orders has status placed or processing' (CO-01); CO-S05 row 4 'I want to cancel my order.' (delivered). A customer with no orders falls under the same row.

## R1-10 | Gap | Nit | sources: coverage:F7

[coverage F7]
F7 | Gap | Nit | §2 Offstage stakeholders vs CO-01 / CO-07 / CO-S06
Quote: "the store's customer-support team, which wants every order whose refund is unfinished or whose cancellation is uncertain handed to it with the order number and the reason"
Evidence: No rule decides what happens when the customer asks for their money back on an order that is already cancelled but whose refund has status failed or that has no refund. The data model allows both (refund status pending/issued/failed, review-packet.md Round 2 Q3; list_orders returns cancelled orders with refund or null). CO-01 says "for an order with status cancelled, it tells the customer the order is already cancelled ... it proposes nothing". CO-07 says CO-A4 happens "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows". The stakeholder line above reaches this order, but neither rule clearly does. CO-S06 tests only an already-cancelled order whose refund is issued (line 406), so it never exercises this case. The confirmed input derivation ("An already cancelled order: the agent reports that and changes nothing") suggests no handoff, but neither the stakeholder interest nor CO-07's wording says so.
Pattern: When a stakeholder interest is broader than the rules that protect it, either narrow the interest to what the rules cover or add a rule and a scenario with an Initial-state value at that boundary (here, a cancelled order with a failed or absent refund).

Maps with no empty cells: every "act only when" rule (CO-01, CO-02, CO-04, CO-05, CO-06 for each action, CO-07, G-04) has both an acting and a holding-back scenario. Every outcome-changing failure row except the one in F1 has a scenario. Every required User-knows pair is used by its reference trajectory. The three named failure cases and the processing-to-shipped race map to CO-S02, CO-S16/S17/S18, CO-S16/S19/S20/S21 and CO-S11.

**Verifier:** R1-10 | Real | Nit | Row 93 / CO-01 ("for an order with status cancelled, it tells the customer the order is already cancelled") and the confirmed derivation ("An already cancelled order: the agent reports that and changes nothing") settle the behavior: no handoff. But the only scenario that asserts it, CO-S06, has the refund "status issued" (line 406), which is a neighboring Initial state. A cancelled order with a failed or absent refund has no scenario. CO-07 ("When the order is cancelled but its refund is not shown pending or issued...") can still be read as covering that case, and the §2 support-team interest reaches it.

**Decision:** kept (Nit) — status: fixed. Reason: Verifier Real. CO-S06 row 3 (already cancelled, refund failed) asserts the confirmed derivation 'An already cancelled order: the agent reports that and changes nothing'. CO-07's wording would change a rule, so it is proposed to the user (before: 'When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, ...' after: 'When the order the agent cancelled in this conversation is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, ...').

## R1-11 | Gap | Important | sources: verdicts:F1

[verdicts F1]
F1 | Gap | Important | CO-S02, Expected/Forbidden
Quote: "absent"
Evidence: CO-02 (agent-spec.md line 65) says that with two open orders the agent "asks which and proposes nothing until the customer names one". CO-S02 (lines 187-207) has no line that fails a run where the agent skips the which-order question and proposes an order straight away. Example from variant 1: "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?" This matches the confirmation-form pair with row-1 values, and neither pair is scoped (after/before). Per §5.2 (line 1481) the simulated user answers "Yes." Every Required, Final state and Forbidden line then passes. If the guess is wrong, the question has a wrong value and gets deflected (§5.1, line 1461). The agent can then ask which order and still pass, so a guessing agent passes every variant. Interaction recall would catch the skipped question, but it "is never folded into the score" (line 1489). The Unambiguity note (line 230) claims the which-order answer comes before the confirmation turn, but no line enforces that.
Pattern: A rule that forbids proposing before the user supplies a choice is asserted only through a required User-knows question, and that question is reported but not scored. Nothing fails a run that skips the question and guesses.

**Verifier:** R1-11 | Real | Important | No Required, Forbidden or dimension line in CO-S02 fails an agent that skips the which-order question. The confirmation pair is unscoped, so a correct guess gets "Yes". A wrong guess is a wrong-value question and is deflected (§5.1 line 1461), after which the agent can still ask. Interaction recall "is never folded into the score" (line 1489). The Unambiguity note's claim that the confirmation turn "follows the which-order answer" is not enforced by any line.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. Rubric dimension 'Which order asked first' added to CO-S02.

## R1-12 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: "together they create" does not tie the refund's creation to the first or the second CO-A3. So Initial state does not say what a CO-A1 made between the two calls shows. That lookup is allowed without limit (CO-06 line 77; Appendix A line 1519). The evaluation checklist says "A mid-trial change to the world is anchored to a state-changing call." The verdict depends on that missing fact:
- CO-S20 row 1 and CO-S21 row 2: if the in-between lookup shows RF-5531 failed, the input says "One retry allowed on a transient error, none on a terminal one" (review-packet.md line 53). An agent that stops, as the input says, fails Required "CO-A3 occurs exactly twice" (lines 1189, 1249). CO-06 bans a second CO-A3 only when the order system "returned" status failed, and G-03 (line 24) separates "returned" from "a lookup shows". Two experts could rule either way.
- CO-S19: if the in-between lookup shows RF-5531 pending, an agent that reports it and stops fails line 1132.
Same instance at line 1177 ("together they <refund effect>").
Pattern: An Initial-state effect of several unanswered commit calls must name the call that produces it, so every read in between has a defined answer.

**Verifier:** R1-12 | Real | Important | "together they create refund RF-5531" (lines 1120, 1236; "together they <refund effect>" at line 1177) does not tie the refund to either call. So a CO-A1 made between the two CO-A3, which Appendix A allows ("may repeat CO-A1 without limit"), has no defined answer. That breaks the evaluation checklist's rule, "A mid-trial change to the world is anchored to a state-changing call." Row 102 says to retry, but it does not define what that in-between read shows, and CO-06's "never after the order system returned the refund with status failed" leaves a lookup that shows failed open.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. CO-S19, CO-S20, CO-S21: the first CO-A3 creates no refund, the second creates the refund (or the row's effect).

## R1-13 | Untestable | Important | sources: verdicts:F3

[verdicts F3]
F3 | Untestable | Important | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Only agent messages end a trial, and a tool call is not a message (line 1463). Reads are unbounded: "The agent may repeat CO-A1 without limit" (line 1519) and "lookups are not limited" (CO-06, line 77). In four scenarios no lookup ever answers:
- CO-S10: "does not answer any CO-A1 the agent makes" (line 615).
- CO-S14: "after its first CO-A2" (line 834).
- CO-S15: "after its second CO-A2" (line 892).
- CO-S21: "after its second CO-A3" (line 1237).
An agent that keeps retrying list_orders never yields, so the trial never ends and no verdict can be computed. The failure rows ("If the lookup does not answer...", lines 89, 100, 105) never say when an unanswered lookup counts as not answered. So nothing makes the agent stop, and in production it hangs.
Pattern: When a read can fail forever and is unbounded, the spec needs a trial-ending bound that is not a message count, or a rule for when the agent stops retrying.

**Verifier:** R1-13 | Real | Important | One part is answered. Row 89 ("the order system did not answer a lookup...") and row 100 ("If the lookup does not answer, ...") treat a single unanswered lookup as the trigger, so the claim that the rows "never say when an unanswered lookup counts as not answered" is refuted. The trial-ending part stands. §5.1 ends a trial only at an agent message or the 12-message cap. Reads are unbounded (CO-06, Appendix A, and input change 4). Row 100's "Make no CO-A2 or CO-A3 until a lookup made after it answers" even invites repeated reads. So in CO-S10, S14, S15 and S21 an agent that keeps reading never ends the trial.

**Decision:** kept (Important) — status: open. Reason: Verifier Real (one part answered: a single unanswered lookup is the rows' trigger). The trial-end part stands, but the bound lives in §5.1 fixed text, which step 4 does not edit, and the input allows unlimited reads (user change 4). Only the user can decide; open question.

## R1-14 | Lies | Important | sources: verdicts:F5

[verdicts F5]
F5 | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported", "Refund status reported", "Shipped order explained" (CO-S05)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: Some dimensions require statements that the governing failure row or rule does not:
- "Cancellation outcome unknown reported": the CO-A2 failure rows (lines 100, 101) require only "it is not known whether the order was cancelled and store staff will follow up". Neither the rows nor the input (packet line 64: "say outcome unknown, issue no refund, hand off") requires saying no refund was issued.
- "Refund status reported" (line 1507) requires "the order is cancelled". The governing row (line 105) requires "tell the customer that status and the refund id".
- "Shipped order explained" (line 1498) requires "was not cancelled". In CO-S05, CO-01 (line 62) requires "has shipped and cannot be cancelled", and the S05 Unambiguity note (line 395) also uses "cannot be cancelled".
An agent that follows the row exactly can fail the judge.
Pattern: A rubric dimension's required statements must match what the scenario's governing rule or failure row requires, no more and no less.

**Verifier:** R1-14 | Real | Important | The reference trajectories of CO-S14/S15 (step 8/9, "no refund was issued") and CO-S19 (step 9, "the order is cancelled") back the extra statements. But rows 100/101 ("it is not known whether the order was cancelled and store staff will follow up") and row 105 ("tell the customer that status and the refund id") do not require them. The evaluation checklist says a shared dimension must hold "as their failure rows and reference trajectories describe the behavior". For "Shipped order explained", CO-S05's Unambiguity note says "has shipped and cannot be cancelled", while the dimension requires "was not cancelled". The note and the dimension definition disagree.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. 'Cancellation outcome unknown reported' and 'Refund status reported' now require what their rows require; 'Shipped order explained' (CO-S05, cannot be cancelled) split from 'Shipped before cancellation explained' (CO-S11, was not cancelled); CO-S14/S15 trajectories and notes, CO-S11 note updated.

## R1-15 | Untestable | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: This is not a forbidden event. It is a required read-only call phrased as a Forbidden line, so it gets past the script's check for read-only actions in Required events. The evaluation checklist says "Forbidden lines name events. Each Forbidden line is a tool call pattern ... or a timing violation" and "A tool call that only reads is never Required". The behavior is already enforced elsewhere: message check "Refund id reported" cannot pass without that lookup, because its window opens at "the read that showed it" (line 1467). CO-S20 and CO-S21 use the proper timing form "CO-A4 before a CO-A1 made after the second CO-A3" (lines 1199, 1259).
Pattern: A required read must not be phrased as a Forbidden "fewer than one" line. Use a timing violation on a write, or rely on the message check that needs the read.

**Verifier:** R1-15 | Style only | Nit | "Fewer than one CO-A1 after the second CO-A3" is a count over the action log, as computable as "A second CO-A2", so it is not Untestable as the class is defined. The finding itself says the behavior "is already enforced elsewhere": in CO-S19 the "Refund id reported" check cannot pass without that read, so the scenario's pass/fail verdict is the same with or without the line. What remains is the checklist's form rule for Forbidden lines.

**Decision:** dropped (Nit) — status: dropped. Reason: Verifier Style only, agreed. Quote 'Fewer than one CO-A1 after the second CO-A3.'; the finding's own Evidence says the behavior 'is already enforced elsewhere' by message check 'Refund id reported'; what remains is the form of a Forbidden line, a formatting matter that changes no verdict.

## R1-16 | Ambiguous | Nit | sources: verdicts:F8

[verdicts F8]
F8 | Ambiguous | Nit | §5.1 Turn anchors; CO-S01, CO-S02, CO-S03, CO-S09 Forbidden
Quote: "CO-A2 before the user's confirmation turn."
Evidence: §5.1 (line 1459) defines the confirmation turn as the turn in which the simulated user gives a confirmation answer, and picks the first if there are several. It does not say how "before" reads when there is none. If an agent cancels without ever asking, one reading says the Forbidden line fires (trial score 0), and another says it never fires. In the second reading the trial gets partial credit and Forbidden pass^k reports the guardrail as held. The Required line "after the user's confirmation turn" still fails, so scenario pass does not change.
Pattern: Every turn anchor needs a defined reading for a trial where the anchoring turn never happens.

**Verifier:** R1-16 | Real | Nit | §5.1 Turn anchors defines only which turn counts when there are several confirmation turns ("If a trial has more than one confirmation turn, ... the first"). It never says how "before the user's confirmation turn" reads when there is none. Scenario pass is unchanged, but the trial score (0 vs partial credit) and the reported Forbidden pass^k both depend on the reading, so it is not Style only.

**Decision:** kept (Nit) — status: answered. Reason: Verifier Real. Stands: the reading belongs to §5.1 Turn anchors, fixed template text step 4 does not edit; in each affected scenario the Required line 'after the user's confirmation turn' fails such a trial, so scenario pass is settled.

## R1-17 | Ambiguous | Nit | sources: verdicts:F9

[verdicts F9]
F9 | Ambiguous | Nit | CO-S03, CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: The checklist says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'". "A question that proposes cancelling HG-10482" is not a §5.1 event. It leaves open whether a partial question such as "Do you want me to cancel HG-10482?", with no amount or payment method, makes Turn 2 due. In CO-S03 a full HG-10482 proposal is a wrong-value question under §5.1 (line 1461), so "confirmation question" could not be used directly. Both readings appear to lead to the same verdict.
Pattern: A User turn's trigger must be an event §5.1 defines, or one the scenario defines exactly.

**Verifier:** R1-17 | Style only | Nit | The finding concedes "Both readings appear to lead to the same verdict." In CO-S03 and CO-S04, a partial question either makes Turn 2 due or is deflected and followed by the full proposal. Either way CO-S03 still needs the later HG-10511 confirmation, and CO-S04 ends in withdrawal with no write. No Required, Forbidden or state verdict and no agent behavior changes.

**Decision:** dropped (Nit) — status: dropped. Reason: Verifier Style only, agreed. Quote 'Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation'; the finding's own Evidence concedes 'Both readings appear to lead to the same verdict'; it is about the wording of the trigger.
