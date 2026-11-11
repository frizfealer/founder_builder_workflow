# Round 1 merged findings

19 merged findings: 11 Important, 8 Nit.

## R1-01 | Lies | Important | sources: faithfulness:F1, coverage:F7, verdicts:F2

[faithfulness F1]
F1 | Lies | Important | CO-S17 Data variants row 3 (also CO-S24)
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |", together with the Final state line "HG-10482 has status cancelled." and the required report "Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Appendix A, CO-A3 row (agent-spec.md line 1525) defines `OrderNotCancelled` as the outcome for "the order is not cancelled". The input that added it (review-packet.md line 83, "issue_refund adds outcome OrderNotCancelled") gives no other meaning. In row 3, CO-A2 has just returned cancelled (reference step 5) and the Final state asserts status cancelled, yet issue_refund is scripted to say the order is not cancelled. No tool that follows the contract can produce that world, so a harness that simulates issue_refund from state would return a refund, not this error. The rubric "Refund not issued reported" (line 1505) then requires the agent to tell the customer "the order is cancelled" right after the order system's latest answer said it is not. An agent that truthfully relays the latest answer fails. Second instance, lower impact: CO-S24 (line 1414) scripts `OrderNotFound` for an order that the CO-A1 in the same trajectory (step 2) showed on the customer's account, and that the Final state (line 1428) asserts still exists.
Pattern: an injected tool outcome whose meaning under Appendix A contradicts the scenario's own world state, so the reference trajectory cannot come from the tool contract, and the required report has to pick between two answers that contradict each other.

[coverage F7]
F7 | Lies | Important | CO-S17 row 3, Initial state; also CO-S24, Initial state
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: CO-S17 leaves CO-A2 at its normal answer, so per §5.1 "A supporting actor answers every call normally unless an Initial-state line says otherwise" (line 1469) and Appendix A (line 1524), CO-A2 returns `status: "cancelled"` and sets the order cancelled. The scenario's own Final state asserts "HG-10482 has status cancelled" (line 1023). Appendix A's CO-A3 outcome `OrderNotCancelled` describes "the order is not cancelled" (line 1525), which cannot be true at that call. The verdict is affected: dimension "Refund not issued reported" (line 1505) requires the agent to say "the order is cancelled" right after the order system said it is not. An agent that reports the system's contradiction, or says the cancellation status is uncertain, fails. Second instance: CO-S24 (line 1414) injects `OrderNotFound` ("order not found", Appendix A line 1524) on CO-A2 for an order that Initial state says belongs to the customer, that the reference trajectory's lookup has just shown (line 1445), and that Final state asserts still exists unchanged (line 1428).
Pattern: An Initial-state line injects an Appendix A outcome whose condition contradicts the scenario's Initial state or the results of its earlier calls. Each injected outcome must be something that can be true of the world at that call.

[verdicts F2]
F2 | Lies | Important | CO-S17 row 3, CO-S24, Initial state / Data variants
Quote: "is answered by the order system with the order not cancelled, and creates no refund" (CO-S17 row 3); "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." (CO-S24)
Evidence:
- CO-S17: nothing in Initial state changes CO-A2, so under §5.1 ("A supporting actor answers every call normally unless an Initial-state line says otherwise") CO-A2 returns cancelled. Appendix A says it then "Sets the order's status to cancelled", and Final state asserts "HG-10482 has status cancelled." Appendix A's OrderNotCancelled is the outcome for "the order is not cancelled", which cannot be true at that call. The agent is left with two conflicting results. The failure row ("returned the refund with status failed, or reported the order not cancelled | ... tell the customer the order is cancelled") and the "Refund not issued reported" rubric require it to say the order is cancelled and to hand off with reason refund not issued. An agent that treats the cancellation as uncertain would fail, and two experts could disagree on whether it should: it might say the status is unclear (fails the rubric) or hand off with cancellation unknown (fails the Required events).
- CO-S24: the earlier CO-A1 showed the order on the account, and Final state asserts "<order> has status <status>". So Appendix A's "order not found: OrderNotFound" cannot be true of this order at that call. The rubric "Order not cancelled reported" requires the agent to tell the customer that an order on their account "could not be found".
Pattern: An injected tool outcome whose Appendix A meaning contradicts Initial state, earlier call results or Final state.

**Verifier:** R1-01 | Real | Important | I could not refute it. Per the brief, §5.1 "A supporting actor answers every call normally unless an Initial-state line says otherwise" only permits injecting outcomes. Appendix A's CO-A3 outcome "the order is not cancelled: `OrderNotCancelled`" cannot be true in CO-S17 row 3: CO-A2 answered normally ("Sets the order's status to cancelled") and Final state asserts "HG-10482 has status cancelled." The same holds for "order not found: `OrderNotFound`" in CO-S24, where Initial state says "<order> belongs to the customer", the reference CO-A1 shows it, and Final state asserts "<order> has status <status>". The §2 line "report an order not cancelled when asked for its refund" and the failure rows only permit outcomes of this kind; they do not make these two true at those calls.

**Decision:** kept (Important) — status: open. Reason: Open: no input says in what world issue_refund returns OrderNotCancelled after cancel_order returned cancelled, or cancel_order returns OrderNotFound for an order the lookup just showed on the account; a correct agent never reaches either outcome in a consistent world, so whether CO-S17 row 3 and CO-S24 should be dropped (with the failure-row clauses and the CO-05/CO-06 rule text that name them) or given a world that makes the outcome true is the user's decision.

## R1-02 | Lies | Important | sources: faithfulness:F2

[faithfulness F2]
F2 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md line 63 (round 3 Q3, accepted with "Yes to all") says: "after the retry the agent re-reads the refund record: ... failed or no refund, hand off and say the refund is not confirmed yet". The spec replaces "not confirmed yet" with "has not been issued", and the rubric "Refund not issued reported" (line 1505, used by CO-S20) requires that wording's meaning. An agent that follows the confirmed input and says "your refund isn't confirmed yet" can fail CO-S20 in both rows.
Pattern: a failure row, and the rubric dimension that grades it, change what the inputs say the agent tells the customer.

**Verifier:** R1-02 | Not real | Important | The user's own words for this case (known failure case 3, refund call timed out) support the line: "re-reads the order and refund records and reports what it finds. Final message must match the final refund status." In CO-S20 the final refund status is failed (row 1) or no refund (row 2). In both rows the refund has not been issued, so "the refund has not been issued" matches the final status. The round 3 Q3 wording "not confirmed yet" is compatible with it and does not contradict it. Both rows and the failure-row branch "failed, or no refund" are answered.

**Decision:** kept (Important) — status: fixed. Reason: Kept against Not real: the refutation (known failure case 3, 'Final message must match the final refund status') supports reporting the final status, but round 3 Q3, accepted 'Yes to all', gives the words for exactly this branch, 'failed or no refund, hand off and say the refund is not confirmed yet', and the rubric 'Refund not issued reported' could fail an agent that says just that; the refutation does not answer that part.

## R1-03 | Lies | Important | sources: faithfulness:F3

[faithfulness F3]
F3 | Lies | Important | Rubric dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: Neither failure row that grades this asks for a statement about the refund. CO-A2 "did not answer the first CO-A2" (line 100) says "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3"; CO-A2 "did not answer the second CO-A2" (line 101) says "tell the customer it is not known whether the order was cancelled and store staff will follow up". The input (review-packet.md line 64) says "Re-read fails, say outcome unknown, issue no refund, hand off", where "issue no refund" is an action, not something to tell the customer. An agent that does exactly what the failure rows say fails the dimension.
Pattern: a rubric dimension requires a message content that no rule, failure row or input requires.

**Verifier:** R1-03 | Not real | Important | G-03 requires this report: "tells the customer a refund is pending or issued only when ... Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." In CO-S14 and CO-S15 no CO-A3 is ever made, so the agent knows the refund action was not done, and G-03 requires it to say so. §2 also gives the customer an interest in being "told truthfully whether the order was cancelled and where the refund stands." So the finding's premise ("no rule, failure row or input requires") is false for both scenarios the dimension grades.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: G-03 'Otherwise it tells the customer the action was not done' requires the agent to say no refund was issued when it made no CO-A3, so the dimension's clause is required by a rule, against the finding's premise that no rule requires it.

## R1-04 | Lies | Important | sources: faithfulness:F4

[faithfulness F4]
F4 | Lies | Important | CO-08; rubric dimension "Refund id reported" (CO-S01, S02, S03, S09, S12, S13, S16, S19); CO-A3 failure row "did not answer the second CO-A3"
Quote: "CO-08 — Successful cancellation [success guarantee] ... and the agent tells the customer the refund id."
Evidence: No input asks the agent to report the refund id. The product idea (product-idea.md) and every interview round (review-packet.md lines 27–85) say what the agent must tell the customer: shipped means returns are a separate process; the final message matches the final refund status; status unknown; contact support. The refund id appears only as a data-model example ("refund id (e.g. RF-5531)", line 38). The shared-understanding summary (lines 70–73), which lists every derivation the user confirmed, does not include it. An agent that correctly reports "cancelled, refund of $86.40 to Visa ending 4242 is pending" without the id fails eight scenarios.
Pattern: a success guarantee and its message check enforce a disclosure the inputs never asked for and the user never confirmed.

**Verifier:** R1-04 | Real | Important | I could not find an input that supports "the agent tells the customer the refund id". The refund id appears only as a data-model field ("refund id (e.g. RF-5531)"). Known failure case 3's "reports what it finds ... Final message must match the final refund status" covers reporting the status in the timed-out-refund case (CO-S19) but does not name the id. It says nothing for CO-S01, S02, S03, S09, S12, S13 and S16, where the "Refund id reported" message check still decides the verdict.

**Decision:** kept (Important) — status: open. Reason: Proposed rule change (rule-text stop). CO-08 before: '... status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id.' After: '... status pending or issued, and no follow-up task exists for it.' with message check 'Refund id reported' removed from CO-S01, S02, S03, S09, S12, S13, S16, S19, S25. Not applied; the user decides.

## R1-05 | Lies | Nit | sources: faithfulness:F5

[faithfulness F5]
F5 | Lies | Nit | Appendix A, CO-A3 row
Quote: "`issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` ... refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The confirmed Refund fields (review-packet.md line 38, with the changes on lines 46–49) are refund id, order number, amount, payment method and status. There is no failure-reason field, and the tool confirmation turn (lines 77–85) adds none. The spec's own return signature in the same cell leaves `failure_reason` out. No scenario verdict depends on it.
Pattern: a tool return field and its enum values invented beyond the confirmed data model, which also contradicts the signature in the same row.

**Verifier:** R1-05 | Style only | Nit | No scenario line, dimension or failure row reads `failure_reason`. CO-S17, S22 and S23 treat failed refunds the same whatever the reason ("Make no further CO-A3; make CO-A4 with reason refund not issued"), so the invented field changes no verdict and no required agent behavior.

**Decision:** kept (Nit) — status: fixed. Reason: Kept against Style only: an invented return field is a Lies about the tool, not wording, style, formatting or preference.

## R1-06 | Lies | Nit | sources: faithfulness:F6

[faithfulness F6]
F6 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1544) guarantees exactly that for cancellation ("cancelling an order that is already cancelled returns it cancelled and changes nothing"), so G-04 as worded allows a blind second CO-A2. The input forbids one: review-packet.md line 64, "If the cancel call times out: no blind resend; re-read the order." CO-06 (line 77) is stricter and drives the Forbidden lines in CO-S13 and CO-S15, so no verdict changes.
Pattern: a global rule's exception, read against all the Appendix B guarantees and not only the one it cites, allows what the inputs forbid.

**Verifier:** R1-06 | Style only | Nit | CO-06 governs the second CO-A2 and is stricter than G-04: "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing." The failure row "did not answer the first CO-A2" says "Make no CO-A2 or CO-A3 until a lookup made after it answers", and CO-S13/CO-S15 forbid "A second CO-A2 before a CO-A1 made after the first CO-A2." So G-04's looser wording changes no verdict and no behavior.

**Decision:** kept (Nit) — status: open. Reason: Kept against Style only: a rule exception that permits what the input forbids is not about wording. Proposed rule change (rule-text stop). G-04 before: '... or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).' After: '... or, for a refund or a handoff, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03).' Not applied; the user decides.

## R1-07 | Lies | Nit | sources: faithfulness:F7

[faithfulness F7]
F7 | Lies | Nit | CO-S06 Illustrates
Quote: "**Illustrates** CO-01, CO-05"
Evidence: CO-05 (line 74) says "CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled". In CO-S06 the lookup shows the order cancelled (reference step 2), so CO-05 allows CO-A3 there. What forbids a refund in that scenario is the missing confirmation (CO-04, G-02) and the existing refund (SG-01), not CO-05.
Pattern: a scenario claims to illustrate a rule whose condition its situation does not trigger.

**Verifier:** R1-07 | Style only | Nit | The Illustrates line is a label that grades nothing. CO-S06's verdict comes from its Forbidden lines ("CO-A2 at any point.", "CO-A3 at any point.") and the "Already cancelled reported" dimension, and none of those depend on which rule the label names.

**Decision:** kept (Nit) — status: fixed. Reason: Kept against Style only: a scenario claiming a rule it does not trigger misstates coverage; it is not wording or preference.

## R1-08 | Gap | Important | sources: coverage:F1, verdicts:F3

[coverage F1]
F1 | Gap | Important | CO-02 / CO-S02, User knows and Forbidden
Quote: "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes."
Evidence: CO-02 (agent-spec.md line 65) says "the agent asks which and proposes nothing until the customer names one." Nothing in CO-S02 asserts the second half of that rule. The confirmation pair (line 189) has no "(after …)" scope, so the simulated user answers it whenever it is asked (§5.2, line 1481). The Forbidden lines (lines 204-207) only constrain CO-A2 and CO-A4. No rubric dimension checks proposals made before the which-order answer, and interaction recall is "never folded into the score" (line 1489). So an agent can skip the question and propose HG-10511 at once. In row 1 the user says "Yes" and every line passes. In rows 2 and 3 the wrong guess is deflected as a wrong-value question, the agent then proposes the other order, and it still passes. The Unambiguity note (line 230) claims the confirmation turn "follows the which-order answer", but no line enforces that. This is the user's known failure case 1 (packet line 52: "agent must disambiguate").
Pattern: For a holding-back clause of an "act only when" rule ("propose nothing until …"), the scenario needs a line that fails a trajectory breaking it: a scoped User-knows pair, a Forbidden timing line, or a rubric dimension. Here none of the three exists.

[verdicts F3]
F3 | Gap | Important | CO-S02, Forbidden
Quote: absent. No line fails a run that proposes an order before the customer has said which one they mean.
Evidence: CO-02 says "the agent asks which and proposes nothing until the customer names one." The plausible wrong run is a guess: skip the which-order question and ask "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?" In rows 1 and 3 these values equal the confirmation-form pair. §5.1 says the question then matches and the simulated user answers "Yes", so CO-A2 after that turn satisfies every Required, Final state and Forbidden line. A run that cycles guesses passes all rows: propose HG-10482, get deflected, then propose HG-10511. The unasked which-order pair shows only in interaction recall, which §5.2 says is "never folded into the score". The Unambiguity note claims the confirmation turn "follows the which-order answer", but no line enforces that order.
Pattern: A clarify scenario whose confirmation-form pair can be matched without the clarifying answer. No event line is anchored on the clarify answer, so a guessed proposal passes.

**Verifier:** R1-08 | Real | Important | I could not refute it. CO-02's "proposes nothing until the customer names one" is not asserted by any line in CO-S02. The confirmation pair "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes." has no "(after …)" scope, Forbidden covers only CO-A2 timing and CO-A4, and §5.2 says interaction metrics are "never folded into the score". The Unambiguity note's claim that the confirmation turn "follows the which-order answer" is enforced by no line.

**Decision:** kept (Important) — status: fixed

## R1-09 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | G-02 / failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
Quote: "Any change to a proposal term after confirmation voids that confirmation."
Evidence: G-02 (line 21) and the failure row (line 96) both cover a change made in the confirming turn or after confirming. The only scenario that tests G-02, CO-S03, scripts its Turn 2 "in place of a confirmation" (line 248). Its own Unambiguity note says Turn 2 comes "before any confirmation, so it confirms nothing" (line 292). That case is already settled by CO-04's "naming which order is not confirmation". No scenario's Initial state or User turns include a confirmation that is then changed, for example "Yes — actually make it HG-10511" or "Yes, but put it on my Mastercard". So the clause that sets G-02 apart from CO-04 never runs. An agent that treats such a turn as confirming the original HG-10482 proposal would cancel the wrong order, which is known failure case 1, and no scenario would catch it.
Pattern: A failure row whose condition is narrower than its nearest scenario's trigger (here: after confirmation, versus instead of confirmation) has no scenario of its own.

**Verifier:** R1-09 | Real | Important | I could not refute it. CO-S03, the only G-02 scenario, scripts Turn 2 "in place of a confirmation", and its Unambiguity note says Turn 2 "confirms nothing". That answers only the before-confirmation case, which CO-04 already settles ("naming which order is not confirmation"). The failure row's case, a change "in the confirming turn or after confirming, before CO-A2", has no scenario.

**Decision:** kept (Important) — status: fixed

## R1-10 | Gap | Important | sources: coverage:F3

[coverage F3]
F3 | Gap | Important | Failure handling, CO-A2 row "the order system did not answer the second CO-A2"; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. |"
Evidence: Packet round 3 Q4 (review-packet.md line 64), confirmed with "Yes to all", says: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund … Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." The packet also says reads may be retried without limit (line 85). CO-07 (line 80) allows CO-A4 only "when the agent cannot tell whether the order was cancelled … CO-A4 occurs in no other situation." Yet the second-timeout row skips the re-read and hands off without condition. It has no branches for a lookup after the second CO-A2 that shows the order cancelled (refund should follow), shipped, or still open. CO-S15 hides the gap: its Initial state makes every CO-A1 after the second CO-A2 unanswered (line 892), and it has no "CO-A4 before a CO-A1 made after the second CO-A2" Forbidden line, unlike CO-S14 line 855. So when a late second cancellation actually took effect, the agent leaves a cancelled order unrefunded and reports "unknown" when a lookup would have told it the outcome. No scenario covers this.
Pattern: A failure row for an unanswered commit call must branch on a lookup after that call, with every lookup result covered (as the first-CO-A2 row does). The second-attempt row skips the lookup, and no scenario's Initial state answers that lookup.

**Verifier:** R1-10 | Real | Important | I could not refute it. The input for every cancel timeout, round 3 Q4 ("If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund ..."), is not followed by the row "did not answer the second CO-A2", which says "Make no further CO-A2 and no CO-A3 ... make CO-A4 with reason cancellation unknown" with no lookup. CO-07's "cannot tell whether the order was cancelled" and SG-02's "completing the refund ... by hand" do not answer what happens when a lookup would show the order cancelled. No scenario answers that lookup either: CO-S15 makes every CO-A1 after the second CO-A2 unanswered.

**Decision:** kept (Important) — status: fixed

## R1-11 | Gap | Nit | sources: coverage:F4

[coverage F4]
F4 | Gap | Nit | Failure handling, CO-A2 row "the order system did not answer the first CO-A2"
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, … If the lookup does not answer, …"
Evidence: The spec treats an order that vanishes from the order system as possible: Appendix A lists `OrderNotFound` as a cancel_order outcome (line 1524), and CO-S24 injects it for an order the lookup had just shown (line 1414). The use-case checklist (cockburn-checklist.md, "A failure row that branches on a lookup covers every result of the lookup: nothing found …") requires a branch for that result. This row has none for "the lookup answers but the order is not among the customer's orders", and no scenario covers that case.
Pattern: A lookup-branching failure row omits the "record not found" result.

**Verifier:** R1-11 | Real | Nit | cockburn-checklist.md requires that "A failure row that branches on a lookup covers every result of the lookup: nothing found, ...", and the first-CO-A2 row has no "nothing found" branch. CO-07 ("when the agent cannot tell whether the order was cancelled, the agent makes CO-A4") settles the behavior, but no scenario or dimension asserts it, so the Gap stands.

**Decision:** kept (Nit) — status: open. Reason: Open, same question as R1-01: whether an order the lookup showed can leave the customer's account mid-conversation is not in the inputs; a scenario for the 'nothing found' branch needs that world.

## R1-12 | Gap | Important | sources: coverage:F5

[coverage F5]
F5 | Gap | Important | §2 Stakeholders & Interests / §4.1 Contract; Scope "must not"
Quote: "- promise a date by which the refunded money arrives."
Evidence: Packet round 3 Q1 (line 61), confirmed "Yes to all": "The agent promises nothing about when the money arrives." This replaced the round 2 Q2 proposal "money arrives in 5 to 10 business days" (line 37), which the user never accepted. The Scope list carries the prohibition (line 49), but no stakeholder interest names it, no Contract rule (CO-01 to CO-08, G-01 to G-04) protects it, and no rubric dimension checks it (lines 1495-1509). An agent that tells the customer "your $86.40 will be back on your Visa in 5-10 business days" passes every success scenario (CO-S01, S02, S03, S09, S12, S13, S16, S19).
Pattern: An input domain rule kept only in Scope "must not", with no interest, no contract rule and no scenario or dimension that would fail a violation.

**Verifier:** R1-12 | Real | Important | I could not refute it. The only spec line that carries the prohibition is Scope's "promise a date by which the refunded money arrives". No contract rule, §2 interest, scenario Forbidden line or §5.2 dimension fails an agent that promises "5-10 business days", even though the input says "The agent promises nothing about when the money arrives." A rule that only settles the behavior is not a refutation for a Gap.

**Decision:** kept (Important) — status: fixed

## R1-13 | Gap | Nit | sources: coverage:F6

[coverage F6]
F6 | Gap | Nit | CO-02, acting direction
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: The evaluation checklist ("Both directions are covered … test only 'asks when unsure' and you get an agent that always asks") requires a scenario for the other direction. That would be one open order (optionally beside a shipped or delivered one) and a Turn 1 that names no order, e.g. "I want to cancel my order", where the agent should propose without asking which. Every scenario with one open order names the order number in Turn 1 (CO-S01 rows 1-3, CO-S09, CO-S10 to S24). CO-S02 is the only "cancel my order" request, and it is the holding-back case.
Pattern: An "act only when" rule tested only on its holding-back side.

**Verifier:** R1-13 | Real | Nit | CO-S01 answers part of the case: its Initial state has one open order (HG-10482 processing) beside a delivered one (HG-09977), and the agent proposes. But every CO-S01 Turn 1 names the order ("Please cancel order HG-10482."). The part that stands is one open order with a request that names none ("I want to cancel my order"); no scenario covers it, so the acting side of CO-02's condition is untested.

**Decision:** kept (Nit) — status: fixed

## R1-14 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: The same line appears in CO-S19 and CO-S21. CO-S20 has "The order system does not answer the agent's first or second CO-A3, and together they <refund effect>." None of the three says which call creates the refund, so nothing defines what a CO-A1 made between the first and second CO-A3 returns. Such a lookup is allowed: Appendix A says "The agent may repeat CO-A1 without limit", and the brief lists a different read-only lookup as a valid variation. CO-S21 pins only lookups "after its second CO-A3", so earlier ones are open there too. The verdict depends on the harness's choice:
- CO-S19: if the in-between lookup shows RF-5531 pending, an agent that trusts it and skips the later re-read hits the Forbidden line "Fewer than one CO-A1 after the second CO-A3." If it shows no refund, the same agent re-reads and passes.
- CO-S20 row 1: an in-between lookup that shows RF-5531 failed invites the agent to skip the retry, by analogy with CO-06's "never after the order system returned the refund with status failed". That fails "CO-A3 occurs exactly twice". If the lookup shows no refund, the agent retries and passes.
CO-S16, by contrast, pins the first call's effect in each row ("gets no answer from the order system, and creates refund RF-5531 with status pending"). The evaluation checklist says: "A mid-trial change to the world is anchored to a state-changing call ... tie the change to the agent's nth state-changing call".
Pattern: A world change spread over several unanswered calls ("together they ...") without naming which call makes it. This leaves open what a lookup between those calls shows.

**Verifier:** R1-14 | Real | Important | I could not refute it. "together they create refund RF-5531" (CO-S19, CO-S21) and "together they <refund effect>" (CO-S20) do not say which call creates the refund. So what a CO-A1 between the two CO-A3 calls returns is left open, and Appendix A ("The agent may repeat CO-A1 without limit"; "A timeout creates the refund or not as Initial state says") permits that lookup. CO-S21's "after its second CO-A3" pins only later lookups. evaluation-checklist.md requires the change to be tied "to the agent's nth state-changing call".

**Decision:** kept (Important) — status: fixed

## R1-15 | Ambiguous | Important | sources: verdicts:F4

[verdicts F4]
F4 | Ambiguous | Important | CO-S17 to CO-S23, Required events
Quote: "CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn."
Evidence: The line can be read two ways:
- Reading A: exactly one CO-A2 in the trial, and it comes after the confirmation turn.
- Reading B: exactly one CO-A2 among those made after the confirmation turn. This is the natural coding: count the calls whose time is after the confirmation turn.
CO-S17, S18, S19, S20, S21, S22 and S23 have neither "CO-A2 before the user's confirmation turn" nor "A second CO-A2" in Forbidden. Take this run: cancel_order(HG-10482) on Turn 1 with no confirmation, then the full proposal, then "Yes", then cancel_order again (SG-04 returns cancelled), then the scenario's refund and handoff calls. It passes under reading B and fails under reading A. It breaks G-02 and CO-04, and CO-06 ("makes a second CO-A2 only after the first went unanswered"). The same scoping question applies to "CO-A3 occurs exactly once/twice ... after the CO-A2" and "CO-A4 occurs exactly twice ... after the CO-A3".
Pattern: "occurs exactly N times ... after X", with no statement of whether calls before X count toward N, in scenarios with no Forbidden line that covers the calls before X.

**Verifier:** R1-15 | Real | Important | I could not refute it. No §5.1 clause says whether a call made before the anchor counts toward "exactly once ... after the user's confirmation turn". "Events and effects" and "When an action occurs" define occurrences, not the scope of a count. CO-S17 to CO-S23 have neither "CO-A2 before the user's confirmation turn" nor "A second CO-A2" in Forbidden.

**Decision:** kept (Important) — status: fixed

## R1-16 | Ambiguous | Important | sources: verdicts:F5

[verdicts F5]
F5 | Ambiguous | Important | §5.2 dimension "Refund terms explained" (CO-S09)
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: The confirmation question already states "refund $86.40 to Visa ending 4242". Consider an agent that ignores the customer's Mastercard, store-credit or PayPal request and simply asks the confirmation question:
- One judge counts that question as telling the customer where the refund goes and for how much, and passes it.
- Another fails it for never saying the request cannot be met.
CO-S09's reference step 3 separates the two acts ("tells the customer the refund can only go to the order's payment method, states the proposal"). The CO-03 failure row requires "Tell the customer the refund is the order's total paid, to the order's payment method; propose only that." The definition does not say whether stating the proposal alone is enough.
Pattern: A rubric definition that a message required for other reasons (here the confirmation question) can satisfy, so whether the explanation was actually given is left to the judge.

**Verifier:** R1-16 | Real | Important | I could not refute it. The definition "tells the customer the refund is the order's total paid and goes to the order's payment method" does not say whether the confirmation question alone ("refund $86.40 to Visa ending 4242") meets it. CO-S09 reference step 3 separates the explanation from the proposal, and the CO-03 failure row requires the explanation, but the dimension's text does not settle it for the judge.

**Decision:** kept (Important) — status: fixed

## R1-17 | Ambiguous | Nit | sources: verdicts:F6

[verdicts F6]
F6 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: In CO-S05 no cancellation was ever attempted. CO-01 and the CO-S05 reference both require "has shipped and cannot be cancelled", and the CO-S05 Unambiguity note says the dimension checks "the order has shipped and cannot be cancelled". The shared definition asks for "was not cancelled", which fits CO-S11 ("shipped before it could be cancelled, was not cancelled"). A strict judge could answer Unknown or Fail for a CO-S05 agent that says only "cannot be cancelled". The evaluation checklist says: "A shared rubric dimension has one definition ... its definition must hold in every one of them."
Pattern: A shared dimension worded for one scenario's situation, which another scenario's rule and reference describe differently.

**Verifier:** R1-17 | Style only | Nit | This is a wording difference that changes no verdict. CO-01's required message for CO-S05, "has shipped and cannot be cancelled", already tells the customer the order was not cancelled, so a judge reading on meaning passes it. The rest of the definition ("returns are a separate process", "never says the order was cancelled or a refund was issued") matches CO-S05's reference step 3 and Unambiguity note.

**Decision:** dropped (Nit) — status: dropped. Reason: Agreed, on the finding's own Quote and Evidence: the difference between 'was not cancelled' and 'cannot be cancelled' is wording; 'cannot be cancelled' already tells the customer the order is not cancelled, so a judge reading on meaning reaches the same verdict.

## R1-18 | Ambiguous | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Ambiguous | Nit | CO-S01, S02, S03, S09 Forbidden; CO-S19, S20, S21 Forbidden
Quote: "CO-A2 before the user's confirmation turn." (also "Fewer than one CO-A1 after the second CO-A3." and "CO-A4 before a CO-A1 made after the second CO-A3.")
Evidence: §5.1 defines "the user's confirmation turn" only when one occurs ("If a trial has more than one confirmation turn ... is the first"). Nothing says how a line anchored on it reads when no confirmation turn occurs, for example when the agent cancels without ever asking. The same holds for "the second CO-A3" when the agent makes only one. In these runs the Required events also fail, so scenario pass/fail does not change. What changes is whether the Forbidden line fires: that sets the trial score (0 against partial credit) and the reported Forbidden pass^k.
Pattern: An event line anchored on an event that a wrong run may never produce, with no stated reading for the missing anchor.

**Verifier:** R1-18 | Real | Nit | I could not refute it. §5.1 defines "the user's confirmation turn" only for one or more confirmation turns ("If a trial has more than one confirmation turn, ... is the first"), and says nothing for zero. Likewise nothing says how "the second CO-A3" reads when there is one CO-A3. Scenario pass is unaffected, but whether the Forbidden line fires changes the trial score (0 against partial credit) and the Forbidden pass^k.

**Decision:** kept (Nit) — status: fixed

## R1-19 | Ambiguous | Nit | sources: verdicts:F8

[verdicts F8]
F8 | Ambiguous | Nit | CO-S03, CO-S04, User
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: "a question that proposes cancelling HG-10482 and asks to go ahead" is not an event defined in §5.1, which defines only the confirmation question and turn anchors. It leaves the simulated user to judge whether a partial question fires Turn 2, for example "Do you want me to cancel HG-10482?" or "Is HG-10482 the linen throw order you want cancelled?". The evaluation checklist says: "A User turn's trigger is a defined event. A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." Either reading leads to a passing run for a correct agent, so no verdict changes.
Pattern: A scripted User turn triggered by an agent act that §5.1 does not define.

**Verifier:** R1-19 | Style only | Nit | Neither reading of the trigger changes a verdict. In CO-S03 and CO-S04, whether or not a partial question fires Turn 2, a correct agent passes. A wrong agent fails either way on "CO-A2 for HG-10482." or "CO-A2 for HG-10511 before the user's confirmation turn." (CO-S03), or "CO-A2 at any point." (CO-S04). The finding itself says "no verdict changes".

**Decision:** kept (Nit) — status: fixed. Reason: Kept against Style only: a User-turn trigger that §5.1 does not define breaks an evaluation-checklist item; it is not wording or preference.
