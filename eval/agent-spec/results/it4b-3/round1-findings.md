# Round 1 merged findings

18 merged findings: 9 Important, 9 Nit.

## R1-01 | Lies | Important | sources: faithfulness:F1, coverage:F5, verdicts:F4

[faithfulness F1]
F1 | Lies | Important | CO-S17 (Data variants row 3, Expected), CO-S24 (Initial state), CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: The scenarios inject tool outcomes that cannot be true at that call, given each scenario's Initial state and earlier results.
- CO-S17 row 3: step 5 of the reference trajectory has CO-A2 return "cancelled". Appendix A (agent-spec.md line 1524) says that return "Sets the order's status to cancelled", and the scenario's own Final state says "HG-10482 has status cancelled." Appendix A line 1525 defines `OrderNotCancelled` as "the order is not cancelled", which is false at that point. The spec then requires the agent to contradict the order system's latest answer. The failure row (line 103) says "tell the customer the order is cancelled", and the dimension "Refund not issued reported" (line 1505, used by CO-S17) requires "the order is cancelled". An agent that truthfully reports that the order system says the order is not cancelled would fail the rubric.
- CO-S24: Initial state says "Order <order> belongs to the customer, with status <status>…" (line 1411), and the reference trajectory's CO-A1 shows the order. Line 1414 then says "The order system reports the order not found for the agent's first CO-A2". Appendix A's outcome "order not found: OrderNotFound" (line 1524) cannot describe an order that exists and that the lookup just returned.
- Inputs: the packet (review-packet.md line 77 and change 2, line 83) adds OrderNotCancelled and OrderNotFound only as tool outcomes. It never says when they can happen for an order that is cancelled, or that exists.
Pattern: An Initial-state line injects an Appendix A outcome whose meaning contradicts the scenario's Initial state or the results of earlier calls. Either use a state where the outcome can be true, or restate what the outcome means and what the agent must tell the customer.

[coverage F5]
F5 | Lies | Important | CO-S17, Data variants row 3 (Initial-state value outside the tool contract)
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: In CO-S17 the CO-A2 is answered normally (§5.1: "A supporting actor answers every call normally unless an Initial-state line says otherwise"). Appendix A says it "Sets the order's status to cancelled", and Final state says "HG-10482 has status cancelled". Appendix A's CO-A3 outcome "the order is not cancelled: OrderNotCancelled" therefore cannot be true at that call. The dimension "Refund not issued reported" then requires the agent to say "the order is cancelled" right after the order system said it is not. Under G-03 a truthful agent can fairly report either.
Pattern: an injected supporting-actor outcome that contradicts the scenario's Initial state and the results of its own earlier calls.

[verdicts F4]
F4 | Lies | Important | CO-S17 row 3, CO-S24; Initial state
Quote: "is answered by the order system with the order not cancelled, and creates no refund" (CO-S17 row 3) and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." (CO-S24)
Evidence: Both injected outcomes contradict their own scenario.
- **CO-S17 row 3.** CO-A2 has just returned cancelled (reference step 5), and Final state asserts "HG-10482 has status cancelled.". Yet CO-A3 returns OrderNotCancelled, whose Appendix A meaning (line 1525) is "the order is not cancelled". That cannot be true at that call. The verdict also turns on it: rubric "Refund not issued reported" (line 1505) requires the agent to say "the order is cancelled" right after the order system said it is not. An agent that reports the status as uncertain fails.
- **CO-S24.** Initial state says "Order <order> belongs to the customer", and the reference lookup returns it. Yet CO-A2 returns OrderNotFound, which Appendix A and §2 (line 10, "must receive the order number of one of the customer's orders … report an order not found") tie to an order number that is not the customer's. The rubric "Order not cancelled reported" then requires telling the customer the order "could not be found".
Pattern: an Initial-state outcome injection whose Appendix A outcome cannot be true given the scenario's Initial state and the results of earlier calls.

**Verifier:** R1-01 | Real | Important | Not refuted. CO-S17 row 3 has CO-A2 return cancelled (reference step 5; Appendix A says that "Sets the order's status to cancelled"; Final state says "HG-10482 has status cancelled."). CO-A3 then returns `OrderNotCancelled`, and Appendix A defines that as "the order is not cancelled", which cannot be true at that call. "Refund not issued reported" then requires the agent to say "the order is cancelled". CO-S24 has the same fault: Initial state says "Order <order> belongs to the customer" and the earlier CO-A1 returns the order, yet CO-A2 returns "order not found: OrderNotFound". Under the brief, §5.1's "answers every call normally unless an Initial-state line says otherwise" lets a scenario inject an outcome, but it does not refute this. No input says either outcome can happen in these states.

**Decision:** kept (Important) — status: open. Reason: Only the user can say when OrderNotCancelled (after CO-A2 returned cancelled) or OrderNotFound (for an order the lookup just returned) can occur, and what the agent then tells the customer; CO-S17 row 3 and CO-S24 stand.

## R1-02 | Lies | Important | sources: faithfulness:F2

[faithfulness F2]
F2 | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md line 63 (round 3 Q3, which the user confirmed with "Yes to all") says: "after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet". The spec replaces "not confirmed yet" with the stronger and different "has not been issued". This appears in three places:
- the failure row at agent-spec.md line 105;
- CO-S20 reference trajectory step 10 (line 1219);
- the dimension "Refund not issued reported" (line 1505), which CO-S20 uses and which requires "the refund has not been issued".
An agent that says what the confirmed policy specifies ("the refund is not confirmed yet") can fail CO-S20's rubric.
Pattern: A customer-facing outcome in a failure row, reference trajectory or rubric dimension differs from the outcome the user confirmed for that case. Use the confirmed outcome, or keep a separate dimension for the timeout-then-lookup path.

**Verifier:** R1-02 | Real | Important | Partly answered. The packet's known failure case 3, "Final message must match the final refund status", supports the content of "has not been issued" when a lookup shows the refund failed or missing. What stands: round 3 Q3, confirmed with "Yes to all", sets the wording for this exact branch: "failed or no refund, hand off and say the refund is not confirmed yet". The failure row (line 105), CO-S20 step 10 and "Refund not issued reported" (line 1505) all require the stronger "the refund has not been issued", so an agent that uses the confirmed wording can fail the CO-S20 rubric.

**Decision:** kept (Important) — status: fixed. Reason: Round 3 Q3 wording 'not confirmed yet' in the failure row, CO-S20 step 10 and a new dimension 'Refund not confirmed reported'.

## R1-03 | Lies | Nit | sources: faithfulness:F3

[faithfulness F3]
F3 | Lies | Nit | Appendix A, CO-A3 row
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The input refund data model (review-packet.md line 38 and lines 45-48) has the fields refund id, order number, amount, payment method and status, with no failure-reason field. The same Appendix A row (agent-spec.md line 1525) gives the call's return shape as `{refund_id, amount, payment_method, status}`, which has no `failure_reason`. So the outcome cell names a field and three enum values that neither the inputs nor the row's own signature contain. No scenario grades the field, so no verdict changes.
Pattern: An Appendix A outcome cell names a return field or value that is in neither the input data model nor the call's stated return shape.

**Verifier:** R1-03 | Style only | Nit | `failure_reason` appears in neither the data model nor the row's own return shape, `{refund_id, amount, payment_method, status}`. But no failure row branches on it: line 103 handles every refund "returned ... with status failed" the same way. No scenario or dimension reads it, so no verdict and no agent behavior changes.

**Decision:** kept (Nit) — status: fixed. Reason: Style only verdict rejected: an invented tool field and enum values are a fact about the tool contract, not wording. failure_reason removed from Appendix A; 'card closed' removed from tool results in CO-S17, CO-S22, CO-S23.

## R1-04 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | 4.1 Scope & Authority / Contract (no rule), §5.2 dimensions
Quote: "- promise a date by which the refunded money arrives."
Evidence: review-packet.md, Round 3 Q1: "The agent promises nothing about when the money arrives." (User: "Yes to all"). The Round 2 Q2 proposal that this replaced said "money arrives in 5 to 10 business days", so the wrong behavior is a real temptation. The decision appears only as a Scope "must not" line. No Contract rule (G-01 to G-04, CO-01 to CO-08) protects it, and no §5.2 dimension checks it. In CO-S01, S02, S03, S09, S12, S13, S16 and S19 the only check on the success message is the code message check "Refund id reported". An agent that says "you'll have your $86.40 back in 5–10 business days" therefore passes every scenario.
Pattern: an input decision that limits what the agent may tell the user exists only as a Scope must-not, with no Contract rule and no scenario or rubric dimension asserting it.

**Verifier:** R1-04 | Real | Important | Not refuted. The only line is the Scope must-not "promise a date by which the refunded money arrives". Round 3 Q1 ("The agent promises nothing about when the money arrives") was confirmed. No rule G-01 to G-04 or CO-01 to CO-08 carries it, and no dimension asserts it. The success scenarios check only the code check "Refund id reported", so "5 to 10 business days" passes every scenario. A rule alone would not refute a Gap anyway, because no scenario or dimension asserts it.

**Decision:** kept (Important) — status: fixed. Reason: New rubric dimension 'Refund reported' on the success scenarios and a no-date clause in 'Refund status reported'.

## R1-05 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | G-02 / CO-04 / Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: review-packet.md Round 1 Q4: "any change after confirmation voids it". G-02: "Any change to a proposal term after confirmation voids that confirmation." The only change-of-mind scenario, CO-S03, sends its Turn 2 "in place of a confirmation", and its Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing". CO-S04 is also "in place of a confirmation". No scenario has a change inside or after the confirming turn, e.g. "Yes, but put it on my Mastercard" or "Yes — actually make it HG-10511". That case also needs Forbidden lines anchored on the later turn, because §5.1 says "If a trial has more than one confirmation turn, 'the user's confirmation turn' is the first". A second instance of the same gap: CO-04 says "A question about an order ... is not confirmation", but no scenario answers the proposal with a question (e.g. "Will it go back to my Visa?") and checks that no CO-A2 follows.
Pattern: authorization look-alikes and void conditions that G-02/CO-04 and the failure table name, with no holding-back scenario whose User turn triggers them.

**Verifier:** R1-05 | Real | Important | Partly answered. CO-S03 covers a change sent "in place of a confirmation". Its Unambiguity note says "Turn 2 replaces the order before any confirmation", but that is a neighboring Initial state. What stands: the failure row "changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" has no scenario. CO-04's look-alike "A question about an order ... is not confirmation" has no holding-back scenario either.

**Decision:** kept (Important) — status: fixed. Reason: CO-S03 row 4 (yes with a changed order) and CO-S04 row 4 (a question in reply). A change after the yes and before CO-A2 has no user turn in which it can arrive.

## R1-06 | Gap | Important | sources: coverage:F3

[coverage F3]
F3 | Gap | Important | Failure handling row "the order system did not answer the second CO-A2"; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: review-packet.md Round 3 Q4 applies to any cancel timeout: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." Lookups are unlimited (Appendix A: "The agent may repeat CO-A1 without limit"), and CO-S15's Initial state expects one: "The order system does not answer any CO-A1 the agent makes after its second CO-A2." The row does not branch on what that lookup shows. If it shows the order cancelled, the row still says "not known" and "no CO-A3". That contradicts G-03, CO-05 ("CO-A3 occurs only for an order ... a lookup shows cancelled") and CO-07 ("when the agent cannot tell whether the order was cancelled ... CO-A4 occurs in no other situation"). Showing placed/processing or shipped contradicts the same rules. Only the no-answer branch has a scenario (CO-S15). The cockburn-checklist says "A failure row that branches on a lookup covers every result of the lookup".
Pattern: a failure row after an unanswered commit call that skips the lookup branches the inputs require, so the answered-lookup cases have neither handling nor a scenario.

**Verifier:** R1-06 | Real | Important | Not refuted. The row "did not answer the second CO-A2" requires "no CO-A3 ... make CO-A4 with reason cancellation unknown" whatever a later lookup shows. CO-S15's Initial state expects such a lookup: "does not answer any CO-A1 the agent makes after its second CO-A2". When the lookup shows cancelled, the row conflicts with CO-07 ("CO-A4 occurs in no other situation"), with CO-05, and with packet round 3 Q4 ("Cancelled, continue to refund"). The cockburn-checklist says "A failure row that branches on a lookup covers every result of the lookup". Only the no-answer branch has a scenario.

**Decision:** kept (Important) — status: fixed. Reason: Row 'did not answer the second CO-A2' branches on the lookup (round 3 Q4); new CO-S25, CO-S26, CO-S27 and dimension 'Cancellation not done reported'.

## R1-07 | Gap | Important | sources: coverage:F4

[coverage F4]
F4 | Gap | Important | CO-08 / G-03; success-path scenarios CO-S01, S02, S03, S09, S12, S13, S16
Quote: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id."
Evidence: G-03: "tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it." Stakeholders: the customer "wants to be told truthfully whether the order was cancelled and where the refund stands", and the support team "wants no customer told a refund is on its way when it is not". On every success path the only check on the agent's report is the code check "Refund id reported" (§5.2). No dimension asserts that the agent said the order is cancelled and the refund is pending. An agent that says "refund RF-5531 has been issued" when the order system returned pending passes CO-S01 and the other six. The spec checks this exact clause elsewhere, with "Refund status reported" in CO-S19.
Pattern: a rule clause about what the agent tells the user (G-03's refund status) that only some scenarios assert; the success scenarios check a verbatim id and leave the status claim unchecked.

**Verifier:** R1-07 | Real | Important | Partly answered. "Refund status reported" asserts G-03's status clause, but only for CO-S19, which has a different Initial state. "Refund not issued reported" covers only the failure paths. What stands: on the success paths (CO-S01, S02, S03, S09, S12, S13, S16), the only message check is "Refund id reported", so an agent that calls a pending refund "issued" passes.

**Decision:** kept (Important) — status: fixed. Reason: Fixed with R1-04 ('Refund reported').

## R1-08 | Gap | Important | sources: verdicts:F1

[verdicts F1]
F1 | Gap | Important | CO-S02, Forbidden / CO-02
Quote: "absent" (no line in CO-S02 forbids proposing an order before the customer names one; the Forbidden block is only "CO-A2 before the user's confirmation turn.", "CO-A2 or CO-A3 for any order other than <order>.", "A second CO-A2.", "CO-A4 at any point.")
Evidence: CO-02 (agent-spec.md line 65) says "the agent asks which and proposes nothing until the customer names one". Packet known failure case 1 (review-packet.md line 52) says "agent must disambiguate". Here is a plausible wrong run. In row 1 the agent skips the which-order question and asks "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?". That matches the confirmation-form pair under row 1's values, so the simulated user says "Yes". CO-A2 and CO-A3 for HG-10511 then follow the confirmation turn, and every Required, Final-state and Forbidden line passes. Row 3 is the same, because it also targets HG-10511. In row 2 the guessed proposal is a wrong-value question, which §5.1 (line 1461) says is deflected. The agent can then ask which order and still pass. So an agent that guesses and recovers after a deflection passes every row. Interaction recall would show the skipped question, but §5.2 (line 1489) says it is "never folded into the score". The Unambiguity note (line 230) says the confirmation turn "follows the which-order answer", and no line enforces that.
Pattern: a hold-back rule about proposals (CO-02's "proposes nothing until") is meant to be checked only through write timing. A guessed proposal that happens to be right passes. It needs an ordering line, for example "the confirmation turn follows the which-order answer turn", or a rubric dimension.

**Verifier:** R1-08 | Real | Important | Partly answered. §5.1 says "A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it", which handles a wrong guess in row 2. What stands: in rows 1 and 3, a proposal for HG-10511 made with no which-order question matches the confirmation pair, and every Required, Final-state and Forbidden line passes. Interaction recall is "never folded into the score". The Unambiguity note's "which follows the which-order answer" is enforced by no line.

**Decision:** kept (Important) — status: fixed. Reason: New rubric dimension 'Which order asked first' on CO-S02.

## R1-09 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: Row 2 says the first CO-A2 "gets no answer from the order system and cancels nothing". Nothing in §5.1 defines "reaches the order system". §5.1 "When an action occurs" (line 1475) defines only issuing the call, "whatever the result". The two readings give opposite verdicts:
- If an unanswered call does reach the system, the next lookup shows shipped, the correct run stops, and "A second CO-A2." is right.
- If a timed-out call never reached the system, the lookup shows processing. The CO-A2 failure row (line 100) then says "If it shows the order placed or processing, make CO-A2 once more". That second CO-A2 is forbidden by "A second CO-A2." and breaks "CO-A2 occurs exactly once".
The Unambiguity note (line 704) assumes the first reading, but the Initial-state line does not settle it. The evaluation checklist says a mid-trial change is "anchored to a state-changing call", which means the call's issuance, not its arrival.
Pattern: a mid-trial state change is tied to a phrase §5.1 does not define, instead of to the agent's nth commit call being issued.

**Verifier:** R1-09 | Not real | Important | Two spec lines settle the reading. CO-S11's Unambiguity note says "in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation". The scenario's own lines can only hold together if the unanswered first CO-A2 reached the system: Required "CO-A2 occurs exactly once" with Final state "HG-10482 has status shipped". So the lookup after it shows shipped. That covers the whole case the finding names, row 2.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: CO-S11's Unambiguity note 'in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation', with 'CO-A2 occurs exactly once' and Final state 'HG-10482 has status shipped', settles row 2, the whole case.

## R1-10 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S16 row 2, CO-S19, CO-S20 row 1, CO-S21; Initial state and Required events
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482." and "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 …"
Evidence: Reads are unlimited (Appendix A line 1519; packet change 4). list_orders returns each order's refund (line 1523). A valid variation is to look up the order between the first unanswered CO-A3 and the retry. That lookup breaks these scenarios in two ways:
- **CO-S16 row 2.** The first CO-A3 "creates refund RF-5531 with status pending", so the lookup shows the refund pending. An agent that then reports success without a second CO-A3 meets CO-08 and G-03. G-04 (line 27) and CO-06 (line 77) only permit a retry ("only when", "only after"); they do not require one. The CO-A3 failure row (line 102) says "Make CO-A3 once more". Experts can split on whether a retry after the refund is visibly pending is required, and the "exactly twice" line fails the agent that stops.
- **CO-S19, CO-S20 row 1, CO-S21.** "together they create" does not say which call creates the refund, so the intermediate lookup's result is undefined. CO-S21's no-answer line covers only "any CO-A1 the agent makes after its second CO-A3". If the harness shows RF-5531 (pending, or failed), an agent that acts on it without a second CO-A3 fails "exactly twice". For a failed refund, CO-06 says "never after the order system returned the refund with status failed", and it is unclear whether a lookup counts as "returned". If the harness shows nothing, the same agent passes.
Pattern: an unanswered commit's effect is not pinned to a specific call, and "exactly n" commit counts fail an agent that reads in between and acts on what it sees. The fix is to state what an intermediate lookup shows, and to decide whether the retry is mandatory once a lookup shows the effect.

**Verifier:** R1-10 | Real | Important | Partly answered. The CO-A3 failure row "did not answer it | Make CO-A3 once more, relying on SG-01" is unconditional. It settles CO-S16 row 2 (an agent that stops after a lookup shows pending fails "exactly twice", and the spec says that is right). It also settles skipping the retry when CO-S19's lookup shows pending. What stands: "together they create" leaves open what a CO-A1 between the two CO-A3 shows in CO-S19, CO-S20 row 1 and CO-S21 (CO-S21's no-answer line covers only lookups "after its second CO-A3"). For a failed refund seen in that lookup, it is unclear whether CO-06's "never after the order system returned the refund with status failed" applies. In CO-S21, an agent that saw the failed refund and says so fails "never says the refund is pending, issued or failed".

**Decision:** kept (Important) — status: fixed. Reason: CO-S19, CO-S20, CO-S21 pin the refund's creation to the second CO-A3; CO-S16 row 2 is settled by the unconditional row 'Make CO-A3 once more'.

## R1-11 | Gap | Nit | sources: coverage:F6

[coverage F6]
F6 | Gap | Nit | CO-03; CO-S08, CO-S09 dimensions
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: As written, the rule requires both statements in each case. CO-S08's "Whole order only explained" asserts only the whole-order part. CO-S09's "Refund terms explained" asserts only the refund-terms part. The failure rows split them the same way ("Tell the customer only the whole order can be cancelled" / "Tell the customer the refund is the order's total paid, to the order's payment method").
Pattern: a rule clause that requires telling the user two things, where each scenario's dimension asserts only one; either the rule or the dimensions should be split to match.

**Verifier:** R1-11 | Real | Nit | Partly answered. CO-S08's "Whole order only explained" asserts the whole-order half. CO-S09's "Refund terms explained" asserts the refund-terms half. What stands: CO-03 requires both statements in each case, and nothing asserts the refund terms in the item case or whole-order-only in the refund-elsewhere case. The failure rows (lines 94 and 95) split them, but they only restate rules and assert nothing.

**Decision:** kept (Nit) — status: open. Reason: The fix changes CO-03's text; proposed to the user, not applied.

## R1-12 | Gap | Nit | sources: coverage:F7

[coverage F7]
F7 | Gap | Nit | CO-02 (both directions)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: Only one scenario has a Turn 1 that names no order (CO-S02, "I want to cancel my order."), and it has two open orders. Every CO-S01 row names the order. No scenario has one open order (e.g. HG-10482 processing plus delivered HG-09977) and an unnamed request, so nothing tests that the agent proposes directly instead of asking. evaluation-checklist.md, "Both directions are covered": "test only 'asks when unsure' and you get an agent that always asks."
Pattern: an act-only-when clarification rule with a scenario for the asking side but none for the not-asking side on the same axis (number of open orders).

**Verifier:** R1-12 | Real | Nit | Partly answered. CO-S01 and CO-S03 have the agent propose without asking when the customer names the order, which is a neighboring case. What stands: no scenario has one open order and an unnamed request. The evaluation-checklist line "Both directions are covered" applies.

**Decision:** kept (Nit) — status: fixed. Reason: CO-S01 row 4: one open order and an unnamed request.

## R1-13 | Gap | Nit | sources: coverage:F8

[coverage F8]
F8 | Gap | Nit | Failure handling: row "the order system did not answer the first CO-A2"; the lookup-result rows for an unnamed request
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
Evidence: cockburn-checklist.md: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." Appendix A's cancel_order outcome `OrderNotFound` shows the order system can fail to find an order, yet this row has no branch for a lookup that lacks the order. Instance 2: the pre-proposal rows cover "more than one ... placed or processing" (unnamed), "named an order number that is not among their orders", and "the named order with status shipped or delivered/cancelled". No row covers an unnamed request ("cancel my order") when the lookup shows no open order or no orders at all.
Pattern: lookup-driven failure handling that omits the "nothing found / no matching record" branch.

**Verifier:** R1-13 | Real | Nit | Partly answered. Instance 1 (the order missing from a lookup after an unanswered CO-A2) has no input showing it can happen, since packet change 4 says "list_orders includes cancelled orders". What stands: instance 2. An unnamed request where the lookup shows no open order, or no orders at all, has no failure row. The pre-proposal rows cover only a "named" order or more than one open order, and CO-01 says only "proposes nothing".

**Decision:** kept (Nit) — status: fixed. Reason: New failure row for an unnamed request with no open order; CO-S05 row 4. Instance 1 has no input (list_orders returns every order of the customer).

## R1-14 | Gap | Nit | sources: coverage:F9

[coverage F9]
F9 | Gap | Nit | Failure handling, CO-A3
Quote: absent
Evidence: Appendix A: `issue_refund(order_number)` returns `{refund_id, amount, payment_method, status}`, so the agent sees the amount and the payment method. review-packet.md Round 2 Q3 rules: "refund amount = order total paid; refund payment method = order's payment method". CO-08 requires both. cockburn-checklist.md brainstorm item: "the supporting actor answers wrongly or late". There is no failure row for a returned refund whose amount or payment method differs from the order's, which the agent can detect and which breaks CO-08. A coder would have to invent this else-branch.
Pattern: a supporting-actor wrong answer that the agent can detect from the tool result, with no failure row.

**Verifier:** R1-14 | Not real | Nit | The finding's evidence is not in the packet or the spec. `issue_refund(order_number)` takes only the order number, and Appendix A carries the "amount and payment method through the order". The confirmed outcome list (tool confirmation turn; Appendix A, "Outcomes, as tool results") names no refund with a different amount or payment method. The cockburn brainstorm item is pruned by its own rule, "Keep a failure only if the agent can detect it and must do something about it", and no input says what the agent must do in that case.

**Decision:** dropped (Nit) — status: dropped. Reason: Agreed: issue_refund(order_number) takes only the order number, Appendix A carries 'amount and payment method through the order', and no input names a wrong-amount outcome or what the agent must do.

## R1-15 | Ambiguous | Nit | sources: verdicts:F5

[verdicts F5]
F5 | Ambiguous | Nit | CO-S03 and CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: The evaluation checklist says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." §5.1 defines "proposes" nowhere. The HG-10482 question is not a §5.1 confirmation question: in CO-S03 it matches no pair, and in CO-S04 there are no pairs at all. So the simulator has to judge whether, for example, "Do you want me to cancel HG-10482?" (no amount or payment method) fires Turn 2. Both readings lead to the same writes, so no verdict changes.
Pattern: a scripted User turn triggered by an undefined event ("a question that proposes …") instead of a §5.1-defined one.

**Verifier:** R1-15 | Style only | Nit | The trigger "the agent's first question that proposes cancelling HG-10482" is undefined in §5.1, against the evaluation checklist. But the finding concedes "Both readings lead to the same writes". If Turn 2 does not fire, the agent has no confirmation, and any CO-A2 or CO-A3 for HG-10482 fails Forbidden either way. No verdict and no agent behavior changes.

**Decision:** kept (Nit) — status: fixed. Reason: Style only verdict rejected: the trigger names an event §5.1 does not define, an Ambiguous-class defect, not wording. Trigger now names the confirmation-question form in CO-S03 and CO-S04.

## R1-16 | Ambiguous | Nit | sources: verdicts:F6

[verdicts F6]
F6 | Ambiguous | Nit | §5.2 dimension "Shipped order explained", as used by CO-S05
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process …"
Evidence: CO-S05 runs under CO-01 (line 62) and the failure row at line 92, which say "has shipped and cannot be cancelled". Its own Unambiguity note (line 395) says the dimension "checks the agent said the order has shipped and cannot be cancelled". The shared definition instead says "was not cancelled", which is CO-S11's wording (failure row, line 98). A judge has to decide whether "can't be cancelled" satisfies "was not cancelled". The evaluation checklist says "A shared rubric dimension has one definition … must hold in every one of them as their failure rows … describe the behavior."
Pattern: a shared rubric dimension worded for one user's scenario, with a different required statement than another user's scenario.

**Verifier:** R1-16 | Real | Nit | Not refuted. CO-S05's Unambiguity note says the dimension "checks the agent said the order has shipped and cannot be cancelled". The shared definition (line 1498) says "was not cancelled". The evaluation checklist says "A shared rubric dimension has one definition ... must hold in every one of them as their failure rows ... describe the behavior". The two readings are not reconciled.

**Decision:** kept (Nit) — status: fixed. Reason: 'Shipped order explained' says 'is not cancelled'; CO-S05 and CO-S11 notes match.

## R1-17 | Untestable | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: The evaluation checklist says "Forbidden lines name events. Each Forbidden line is a tool call pattern … or a timing violation". This line names an absence that can only be checked at the end of the trial. Its effect is a required read-only call, which the checklist excludes from Required ("A tool call that only reads is never Required"). It needs rewording to become one Then step. It changes no verdict, because the message check on RF-5531 and the rubric "Refund status reported" already fail any run without that lookup. CO-S20 and CO-S21 use the event form instead ("CO-A4 before a CO-A1 made after the second CO-A3").
Pattern: a required read written as a negated Forbidden line instead of as an ordering violation on a later event.

**Verifier:** R1-17 | Style only | Nit | "Fewer than one CO-A1 after the second CO-A3" can be computed as one count over the tool log. A run without that lookup already fails message check "Refund id reported", and CO-S19's note says that check "matches RF-5531, which the agent can learn only from the lookup". No verdict and no agent behavior changes.

**Decision:** dropped (Nit) — status: dropped. Reason: Style only, agreed from the finding's Quote ('Fewer than one CO-A1 after the second CO-A3.') and Evidence: the line is a count over the tool log, computable as written; the finding is about phrasing it as a negated count rather than an ordering event, and it says no verdict changes.

## R1-18 | Ambiguous | Nit | sources: verdicts:F8

[verdicts F8]
F8 | Ambiguous | Nit | G-04 with SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1544) guarantees that cancelling an already-cancelled order "changes nothing". Read literally, G-04's second clause allows a blind CO-A2 retry. CO-06 (line 77), the CO-A2 failure row (line 100) and the packet's round 3 Q4 ("If the cancel call times out: no blind resend; re-read the order") forbid one. A builder could read G-04 either way. No verdict changes: CO-S12 and CO-S13 forbid the blind retry.
Pattern: a global rule's exception refers to "the order system guarantees" in general terms, and a guarantee for another action fits it.

Files reviewed (no files edited):
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/agent-spec.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/review-packet.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/product-idea.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/ (evaluation-checklist.md, specification-by-example-checklist.md, verification.md, cockburn-checklist.md)

**Verifier:** R1-18 | Not real | Important→Nit as filed (Nit) | Two lines settle the CO-A2 case. G-04's exception names its guarantee: "(Appendix B, SG-01)". CO-06 says "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing". CO-S12 and CO-S13 assert this: "A second CO-A2 before a CO-A1 made after the first CO-A2" / "A second CO-A2."

**Decision:** dropped (Nit) — status: dropped. Reason: Agreed: G-04's exception names its guarantee '(Appendix B, SG-01)', and CO-06 'It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing' settles CO-A2; CO-S12 and CO-S13 assert it.
