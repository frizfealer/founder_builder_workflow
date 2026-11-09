# Round 2 merged findings

Finder count lines: faithfulness "3 findings: 2 Important, 1 Nit."; verdicts "7 findings: 4 Important, 3 Nit."; coverage "5 findings: 2 Important, 3 Nit." Merged after dropping duplicates: 14 findings, 8 Important, 6 Nit.

Count line: 14 merged: 8 Important verified, 6 Nit sent straight to 4.5. Kept 10 (4 Important, 6 Nit). Dropped 4. Pre-existing 0.

R2-01 | Lies | Important | CO-S17 row 3; Failure handling row "CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund |" and "Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Appendix A, CO-A3 row (agent-spec.md line 1654), defines this outcome as "the order is not cancelled: `OrderNotCancelled`". In CO-S17 row 3, though, CO-A2 has already returned cancelled (reference step 5) and the Final state says "HG-10482 has status cancelled." (line 1027). So the order system gives an answer its own interface definition rules out, and the world described cannot produce that tool result. The spec then makes the agent tell the customer "the order is cancelled" (rubric "Refund not issued reported", line 1631, used by CO-S17) right after the order system's latest answer said it is not. Under CO-07 (line 80), "when the agent cannot tell whether the order was cancelled", the agent must use reason cancellation unknown. The inputs give no handling for OrderNotCancelled: the tool confirmation turn only adds the outcome ("issue_refund adds outcome OrderNotCancelled", review-packet.md, tool confirmation turn, change 2). Suppose an agent reports the conflicting answers truthfully, or re-reads and hands off with cancellation_unknown. It fails the Required event "CO-A4 ... reason refund not issued" (line 1024) and the rubric, even though CO-07 and G-03 support what it did.
Pattern: an outcome that says the order is not cancelled is handled as though the order were known to be cancelled. Instances: the failure row at line 103 (the "or reported the order not cancelled" clause, with its "the order is cancelled" message and reason refund not issued); CO-S17 row 3 (line 1041) together with its Required event at line 1024 and the rubric "Refund not issued reported" (line 1631).
Source: faithfulness F1
Verifier: R2-01 | Not real | Important | The inputs support the row. The packet's failure case 2 reads: "Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process ... none on a terminal one." In CO-S17 row 3, CO-A2 has already returned cancelled (reference step 5). So G-03 ("tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled") allows "the order is cancelled", and the agent can tell, so CO-07's "cannot tell whether the order was cancelled" branch does not apply. The finding says the world cannot produce that result, but §5.1 allows it: "A supporting actor answers every call normally unless an Initial-state line says otherwise." Here the Initial-state line says otherwise ("The agent's first CO-A3 <first refund outcome>", row 3).
Decision reason: Main thread: I read the packet's failure case 2 ("Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off"), G-03 ("the order system returned it cancelled") and §5.1 ("A supporting actor answers every call normally unless an Initial-state line says otherwise"). CO-A2 returned cancelled, so the agent can tell, CO-07's cannot-tell branch does not apply, and the input supports the row; dropped.
Decision: dropped
Status: dropped

R2-02 | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported" and "Refund status reported"
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not." and "The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it."
Evidence: These rubrics require statements that the governing rows do not. The failure rows for an unanswered first or second CO-A2 whose lookup also goes unanswered (lines 100 and 101) say only "tell the customer it is not known whether the order was cancelled and store staff will follow up". Neither those rows nor CO-07 requires saying no refund was issued. The row for an unanswered second CO-A3 whose lookup shows pending or issued (line 105) says "tell the customer that status and the refund id". It does not require saying the order is cancelled. The input for that branch is only "pending or issued, report that status" (review-packet.md, Round 3 Q3). An agent that follows those rows word for word fails CO-S14 and CO-S15 (and the matching reference step 8/10, "no refund was issued") or CO-S19.
Pattern: a rubric dimension's definition adds a required statement that the failure row or rule it grades does not contain. Either the row or the rubric must change so they say the same thing. Instances: "Cancellation outcome unknown reported" (line 1630) against rows 100 and 101, used by CO-S14 and CO-S15; "Refund status reported" (line 1633) against row 105, used by CO-S19.
Source: faithfulness F2
Verifier: R2-02 | Real | Important | Only the first instance can be refuted. For CO-S14/S15, G-03 ("Otherwise it tells the customer the action was not done") covers the refund that was never made, so "no refund was issued" has a rule behind it. The second instance stands. Row 105's pending/issued branch says only "tell the customer that status and the refund id, and make no CO-A4". No rule (G-03, CO-08 "the agent tells the customer the refund id") requires saying the order is cancelled. Yet "Refund status reported" requires "tells the customer the order is cancelled", so an agent that follows row 105 word for word fails CO-S19.
Decision: kept
Status: fixed (second instance, "Refund status reported"; the CO-S14/S15 instance was refuted)

R2-03 | Lies | Nit | CO-S01, Unambiguity note
Quote: "the only check on the agent's words, message check "Refund id reported", is a match on one exact value, the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or length of time by which the refunded money arrives."
Evidence: The same sentence names a second check on the agent's words, the rubric dimension "No arrival date promised". The §5.2 table (line 1637) also lists CO-S01 as using that dimension. The R1-03 fix (answered.md) added the rubric to CO-S01 but left "the only check on the agent's words" in place, so the fix is incomplete.
Pattern: an Unambiguity note says something about the scenario's checks that the scenario's own dimensions contradict. Only CO-S01's note has the "only check" wording; the notes of the other scenarios that gained the rubric (CO-S02, S03, S09, S12, S13, S16, S19, S25) do not claim exclusivity.
Source: faithfulness F3; verdicts F7 (duplicates merged; text above is from faithfulness F3)
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: fixed

R2-04 | Gap | Important | CO-01 / CO-07 / CO-S06, Initial state
Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence: The trigger (agent-spec.md line 57) is "The customer asks to cancel an order or to get their money back for an order." Three scenarios end with exactly this state: an order cancelled while its refund is missing or failed. They are CO-S17 (line 1028), CO-S18 ("<order> has status cancelled and no refund", line 1084) and CO-S20 (line 1200). A customer who comes back in a later conversation asking for their money hits that state. The only already-cancelled scenario, CO-S06, has an issued refund in both rows (lines 434-437). For the missing or failed refund case, three rules point different ways: CO-05 (line 74) allows "CO-A3 occurs only for an order ... a lookup shows cancelled", so an issue_refund call looks allowed. CO-07 (line 80), "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4", can be read as applying, with zero retries made. The confirmed derivation in the packet (Shared-understanding summary) says "An already cancelled order: the agent reports that and changes nothing." No scenario holds the agent back here. An agent that issues an unconfirmed refund, or creates a follow-up task, for a cancelled and unrefunded order passes every scenario.
Pattern: A contract boundary that splits on a second attribute (here the refund status of an already-cancelled order) is shown only on its safe side. Add CO-S06 rows, or a sibling scenario, with a cancelled order whose refund is failed or absent. Forbid CO-A3 and CO-A4 there, as the "changes nothing" derivation requires.
Source: coverage F1
Verifier: R2-04 | Real | Important | No scenario asserts the case. Both CO-S06 rows hold a refund with "status issued", and no other scenario starts from a cancelled order whose refund is failed or absent. G-02 and CO-01 ("proposes nothing for that order") arguably settle CO-A3, but under the brief that is no refutation without a scenario. CO-A4 is left open between CO-07 ("cancelled but its refund is not shown pending or issued") and the confirmed derivation "An already cancelled order: the agent reports that and changes nothing."
Decision: kept
Status: fixed (CO-S06 row 3, refund failed); narrowing CO-07 is a proposed rule change, open

R2-05 | Gap | Important | Failure handling (some items row) / CO-S08
Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
Evidence: This row is an act-only-when ("propose nothing until ..."). CO-S08 covers only the holding-back side: its only User-knows pair is "Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)" (line 514), and every row forbids CO-A2. No scenario has the customer first ask for a partial cancellation and then accept cancelling the whole order. An agent that refuses to cancel anything after a partial request passes the whole suite. Compare CO-S09, which does show the acting side after a request for a different payment method.
Pattern: For each "propose nothing until X" failure row, add an acting scenario in which X happens and the write follows the confirmation.
Source: coverage F2
Verifier: R2-05 | Real | Important | Could not refute. The row's acting side, "propose nothing until the customer asks to cancel the whole order", has no scenario. CO-S08's only pair is "A: No, I'll keep it. (optional)" and every row forbids CO-A2. CO-S01 shows acting on a whole-order request, but never after a request to cancel only some items, so it does not exercise this row.
Decision: kept
Status: fixed (new CO-S27)

R2-06 | Gap | Nit | CO-03 / CO-S08, CO-S09 dimensions
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: Parts of this clause are asserted by no scenario: (a) No scenario triggers the "different amount" condition. CO-S09's rows (lines 589-591) ask for a new Mastercard, store credit and PayPal, never a different amount. (b) The clause requires both statements in every case, but each case's dimension checks only one. "Whole order only explained" (line 1627, CO-S08) never checks the refund-terms statement. "Refund terms explained" (line 1628, CO-S09) never checks the whole-order statement. The failure rows (lines 94-95) split the two statements by case, so the rule and its rows also disagree.
Pattern: Every "tells the customer" clause, for every condition it lists, needs a scenario whose dimension asserts that statement. Otherwise narrow the rule to match the rows.
Source: coverage F3
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: fixed (a) CO-S09 row 4; (b) narrowing CO-03 is a proposed rule change, open

R2-07 | Gap | Nit | CO-01 / CO-02, Failure handling
Quote: absent
Evidence: The use-case checklist brainstorm (cockburn-checklist.md, Failure handling) lists "the lookup returns more than one plausible match, or none (ambiguous match)". The spec handles more than one open order when no order is named (CO-02, line 65; row at line 90). It handles a named number not on the account (line 91). It handles exactly one open order with none named (CO-S01 row 4). It has no row and no scenario for a request that names no order when the lookup shows no order with status placed or processing, for example only shipped, delivered or cancelled orders, or no orders at all. CO-01 (line 62) blocks a proposal, but what the agent tells the customer is undefined. With several non-open orders, it is also unclear which order the "has shipped" or "already cancelled" message is about.
Pattern: A lookup-driven selection must have a failure row and a scenario for each match count: none, one and many.
Source: coverage F4
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: answered: CO-01 states what the agent says for each shipped, delivered or cancelled order and that it proposes nothing; an account with no orders is not in the inputs (open question)

R2-08 | Gap | Nit | CO-S08, Initial state
Quote: "Order HG-10530 belongs to the customer, with status placed, items 1 × Stoneware mug set at $28.00 and 1 × Linen napkins, set of 4, at $16.00, total paid $53.50, payment method Amex ending 1007."
Evidence: The confirmed data model (review-packet.md, Round 2 Q3) and Appendix A's list_orders result (line 1652) include `shipping` and `tax`. The packet's Round 2 Q2 says total paid covers items, shipping and tax. No scenario's Initial state gives shipping or tax. In CO-S08 the items come to $44.00 against a total paid of $53.50, which is consistent only if shipping plus tax is the unstated $9.50. A harness that fills in shipping and tax as 0 returns order data that contradicts itself.
Pattern: When Initial state gives fields linked by a contract relation (items + shipping + tax = total paid), state every term of the relation, or drop the line items.
Source: coverage F5
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: fixed

R2-09 | Ambiguous | Important | CO-S16, Required events (row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In CO-S16 row 2, the first refund call "gets no answer from the order system, and creates refund RF-5531 with status pending" (agent-spec.md line 983). Lookups can be repeated without limit (Appendix A, line 1648; packet tool confirmation change 4). So a valid agent may look up the order after the unanswered first CO-A3, see RF-5531 pending, report it and stop. That run meets CO-08 (line 83) and G-03 (line 24). CO-06 (line 77) and G-04 (line 27) only permit a second CO-A3; they do not require one. Yet the run fails this Required line, which counts calls exactly. The Unambiguity note (line 998) says "exactly two refund calls pass", which pins the path. Two experts could split: one reads the failure row "Make CO-A3 once more" (line 102) as mandatory even after a lookup shows the refund, the other reads the rules as permissive. evaluation-checklist.md "Outcome, not path" says an assertion that punishes a valid unanticipated path is a defect.
Pattern: A Required event counts an exact number of retries while a free read can show the retry is unnecessary. Either tie the row so a lookup cannot see the refund before the retry, or move the row out of the "exactly twice" scenario.
Source: verdicts F1
Verifier: R2-09 | Not real | Important | The retry is required, not just permitted. Failure row 102 is unconditional: "the order system ... did not answer it | Make CO-A3 once more, relying on SG-01." The input sets the same path, case 3: "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads." So an agent that looks up the order and stops departs from both the row and the input, which makes it an invalid path, not a valid unanticipated one. "Exactly twice" counts a state-changing call, which the evaluation checklist allows as a Required event.
Decision reason: Main thread: I read failure row 102 ("Make CO-A3 once more, relying on SG-01.") and the packet's case 3 ("agent retries once, then re-reads"). The retry is required by the row and the input, so stopping after a lookup is not a valid path; dropped.
Decision: dropped
Status: dropped

R2-10 | Gap | Important | CO-S02 User knows and Unambiguity note; CO-S07
Quote: "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes. (after Turn 2)" and "so a proposal made before asking which order is deflected"
Evidence: CO-02 (line 65) says the agent "asks which and proposes nothing until the customer names one", and Scope must-not (line 46) says "guess which order the customer means". The R1-12 fix only makes a guessed proposal get deflected. The following wrong run still passes every line: in CO-S02 the agent proposes a guessed order with full values, is deflected, then asks which order, receives Turn 2, and completes. No Forbidden line, Required event or dimension checks the premature proposal. Interaction precision would catch it, but §5.2 (line 1615) says precision is never scored. Second instance: in CO-S07 the agent proposes the near-miss HG-10482 ("Shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?") when the customer named HG-10428 or HG-10483. It is deflected and writes nothing. The dimension "Order not found reported" (line 1626) checks only that the agent said not found and never said something was cancelled, so the run passes. Compare "Orders unavailable reported" (line 1629), which does include "proposes no cancellation".
Pattern: A "proposes nothing" or "do not guess the order" clause is protected only by simulator deflection, so a guessing agent that recovers passes. Add a "proposed nothing for another or unchosen order" part to a rubric dimension in each scenario that tests the clause.
Source: verdicts F2
Verifier: R2-10 | Real | Important | Could not refute. CO-S02's dimensions are only "Refund id reported" and "No arrival date promised". Its Unambiguity note relies on deflection alone: "a proposal made before asking which order is deflected". No Forbidden line or dimension catches the early proposal that CO-02 forbids ("proposes nothing until the customer names one"). In CO-S07, "Order not found reported" checks only "no order with the number they gave is on their account, and never says an order was cancelled or a refund issued", so a deflected proposal for HG-10482 passes. That breaks Scope's "turn an order number the customer gave into a different one".
Decision: kept
Status: fixed

R2-11 | Gap | Important | CO-S26, rubric dimension "Cancellation not done reported" (row 1)
Quote: "| Cancellation not done reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S26 |"
Evidence: CO-S26 row 1 has the lookup show HG-10482 shipped. The failure row for the second CO-A2 (line 101) and CO-05 (line 74) require the agent to say "the order shipped and was not cancelled, and that returns are a separate process". The reference trajectory step 9 (line 1575) does say it. But the single dimension shared by both rows checks only "not cancelled". An agent that says only "your order was not cancelled" in row 1 passes. CO-S11 asserts the same clause through "Shipped order explained", but only on the first-CO-A2 path.
Pattern: One dimension shared across data-variant rows checks only what the rows have in common, so a row-specific required message goes unasserted. Use a separate dimension (or scenario) for the shipped row.
Source: verdicts F3
Verifier: R2-11 | Not real | Important | A scenario already asserts the message. CO-05 says "a lookup shows the order shipped or delivered, the agent tells the customer the order shipped and was not cancelled, and that returns are a separate process". CO-S11 row 2 ("gets no answer from the order system and cancels nothing", after which a lookup shows shipped) asserts that clause with "Shipped order explained" (Used by CO-S05, CO-S11). The Gap class is a rule's tell-requirement that no scenario asserts, and this one is asserted. The second-CO-A2 path in CO-S26 repeats the same CO-05 clause.
Decision reason: Main thread: I read CO-S11 row 2 ("gets no answer from the order system and cancels nothing", lookup then shows shipped) and "Shipped order explained" (Used by CO-S05, CO-S11). CO-05's shipped-and-returns statement is asserted by a scenario, so the Gap class does not fit; dropped.
Decision: dropped
Status: dropped

R2-12 | Untestable | Important | §5.1 End of trial, with CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: The packet's tool confirmation change 4 says "Reads may be retried on timeout without limit", and Appendix A (line 1648) says "The agent may repeat CO-A1 without limit". These Initial states make every lookup go unanswered: CO-S10 "does not answer any CO-A1 the agent makes" (line 617), CO-S14 (line 836), CO-S15 (line 894), CO-S21 (line 1244). An agent that keeps calling list_orders and never yields sends no agent message, so neither end condition is reached. The rubric dimensions that read the final report ("Orders unavailable reported", "Cancellation outcome unknown reported", "Refund status unknown reported") and the Required CO-A4 lines then have no defined verdict. One grader would fail the trial for having no report; another would treat it as a harness error.
Pattern: An end-of-trial rule that counts only agent messages, in a spec that allows unlimited tool calls against a supporting actor that never answers. Bound the trial by tool calls too, or say how a trial that never yields is scored.
Source: verdicts F4
Verifier: R2-12 | Style only | Nit | The verdict is already settled. §5.2 says: "A trial passes when ... every dimension the scenario uses passes; a rubric judge's Unknown counts as not passed." An agent that loops on CO-A1 and never yields sends no text. Wherever the harness stops it, "Orders unavailable reported", "Cancellation outcome unknown reported" and "Refund status unknown reported" cannot pass, and in CO-S14/S15/S21 the Required CO-A4 also never occurs. So such a trial always fails. The missing tool-call bound is a harness stopping detail that changes no verdict, and no spec text supports the "harness error" reading.
Decision reason: Main thread: I read §5.2 "a rubric judge's Unknown counts as not passed" and the Required CO-A4 lines of CO-S14/S15/S21. A trial that never yields fails in every case, so the verdict is defined; Style only, dropped. (§5.1 is fixed template text step 4 does not edit in any case.)
Decision: dropped
Status: dropped

R2-13 | Lies | Nit | CO-S17 rows 1–2, CO-S22 Initial state, CO-S23 Initial state and Data variants; reference trajectories CO-S17, S22, S23 step 6
Quote: "- The agent's first CO-A3 creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because <failure reason>." and "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A CO-A3 (line 1654) returns `{refund_id, amount, payment_method, status}`; R1-10 removed failure_reason. The tool result therefore cannot carry "card closed", "card has expired" or "provider declined". The reference steps show a result field the tool does not return. CO-S23's only column (`failure reason`) varies nothing the harness can set or the agent can observe, so its two rows are identical runs.
Pattern: After a field is removed from the interface, scenarios still state or vary it. Remove the "because …" clauses and the result text, or drop the column.
Source: verdicts F5
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: fixed

R2-14 | Ambiguous | Nit | CO-S02, CO-S03, CO-S04, User block
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\"" (CO-S03 line 249, CO-S04 line 310) and "- Turn 2, in reply to the first agent message that asks the customer which order to cancel: \"<which answer>\"" (CO-S02 line 187)
Evidence: evaluation-checklist.md "A User turn's trigger is a defined event": "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." §5.1 defines no "question that proposes cancelling" and no "message that asks which order". The simulator has to judge whether a partial question fires Turn 2, for example "Do you want me to cancel HG-10482?" with no amount or payment method. In the runs I traced, the verdict comes out the same either way.
Pattern: A User-turn trigger that names an event §5.1 does not define. Define the event in §5.1, or anchor the turn to a defined one.
Source: verdicts F6
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: fixed for CO-S03 and CO-S04; CO-S02 stands (no §5.1 event fits a which-order question; step 4 does not edit §5.1)
