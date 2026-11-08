M14 | Gap | Important | CO-S25, CO-S26, Expected / Forbidden
Quote: CO-S25: "- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn." (only Required event); CO-S26: "- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn." (only Required event); neither has a Forbidden line requiring a CO-A1 after the last unanswered CO-A2 before the agent reports the outcome.
Evidence: Failure row "the order system did not answer a CO-A2": "Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it; then act on the row below that matches the lookup's result." (bundle §2). G-03 allows "not done" only when the agent can tell. Review packet round 3 Q4: after a cancel timeout, re-read the order. CO-S25's Unambiguity note relies on the lookup ("after the second unanswered cancellation the agent can see the order is still open"); CO-S26's reference step 6 is the lookup that shows shipped. An agent that skips the lookup and reports "not cancelled" (CO-S25) or "shipped" (CO-S26) passes every Required, Forbidden, final-state and rubric line. CO-S15 guards the same step with "CO-A4 before a CO-A1 made after the second CO-A2."
Pattern: A scenario whose verdict on the agent's claim depends on a lookup the rules require has no line that makes the lookup happen before that claim.

M15 | Gap | Important | row: Order not cancelled reported (CO-S24)
Quote: "| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |"
Evidence: Failure row "CO-A2 | the order system reported the order not found" requires "Tell the customer the order could not be found and was not cancelled" (bundle §4). CO-S24's reference trajectory step 6 still says "Agent tells the customer the order could not be found and was not cancelled." The round-1 edit removed "could not be found" from the dimension so it could be shared with CO-S25, so no scenario asserts the not-found part.
Pattern: Generalizing a shared message dimension drops a required element that one of its scenarios still needs.

M16 | Gap | Important | row: Refund not issued reported (CO-S17, CO-S18, CO-S22)
Quote: "| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |"
Evidence: Review packet round 2 Q4 known case 2: "refund not issued, state known; agent reports it". CO-S17, CO-S18 and CO-S22 expose a known failed refund and their reference trajectories report that the refund has not been issued. The broadened rubric lets them pass with "not confirmed yet", the uncertainty wording meant for CO-S20.
Pattern: A shared rubric was relaxed for an uncertain-outcome scenario and stopped asserting the known outcome in the others.

M17 | Lies | Important | CO-03; row: No arrival date promised
Quote: "The agent states no date or time frame by which the refunded money arrives."
Evidence: Review packet round 3 Q1, confirmed: "The agent promises nothing about when the money arrives." It does not prohibit a non-promissory estimate or disclaimer. The rubric "No arrival date promised" applies the stronger prohibition to ten scenarios.
Pattern: A prohibition on promising a timeline was strengthened into a prohibition on stating any timeline.

M18 | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29
Quote: absent
Evidence: Each reference trajectory first uses CO-A1 to obtain the order facts on which the proposal or refusal depends, but none of these scenarios requires that lookup before the proposal or decision; their Required and Forbidden checks therefore permit a lucky guess.
Pattern: A scenario depends on facts available only through a read-only lookup but has no executable check that the lookup preceded the proposal or outcome report.

M19 | Lies | Nit | Appendix A row CO-A3; CO-S22, CO-S23 reference trajectories
Quote: "refund failed (the payment method is closed or expired, or the provider declined): returns the refund with `status: \"failed\"`"
Evidence: After the round-1 removal of failure_reason (M4), the CO-A3 result carries only status "failed", while CO-S22 and CO-S23 reference trajectories still show CO-A3 returning the reason "card closed" (agent-spec.md, CO-S22 and CO-S23 blocks).
Pattern: Removing a tool-result field left reference trajectories displaying information the result cannot return.

M20 | Gap | Important | failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing"; CO-S25
Quote: "| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. | CO-06, CO-07, G-03 |"
Evidence: The order is still open and could ship. The agent may not retry, CO-07 forbids a handoff ("CO-A4 occurs in no other situation"), and nothing tells the customer what to do next. CO-S25 locks this in with "CO-A4 at any point" in Forbidden, and its rubric checks only "not cancelled". product-idea.md: "The customer should not need to know the store's cancellation and refund rules, or find the right form for their situation." Round 3 Q4 covers only the first unanswered cancel. The CO-A4-unanswered-twice row does give a next step ("to contact Harbor Goods customer support"). The user never confirmed this end state.
Pattern: When the agent's retries run out and the work is still undone, the spec gives the customer no next step.

M21 | Gap | Nit | CO-07
Quote: "When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows, ..."
Evidence: The M10 fix adds a scope boundary (only orders cancelled in this conversation), but no scenario holds back on the excluded side: CO-S06, the only scenario with an order cancelled before the conversation, has a refund with status issued, so CO-07 would not fire there even without the clause. M10 left the right behavior as an open question.
Pattern: A scope clause added to an "act only when" rule needs a scenario on the excluded side of the boundary.

M22 | Gap | Nit | failure row "the customer named no order, and none of the customer's orders has status placed or processing"; CO-S29; row: No open order reported
Quote: "Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing."
Evidence: The trigger covers all orders shipped or delivered, some or all cancelled, and a customer with no orders (vacuously true; "because each has shipped, been delivered or been cancelled" is then false). CO-S29 has one shipped and one delivered order only. The rubric "No open order reported" requires "because they have shipped or been delivered, and that returns are a separate process", which would mis-grade a correct reply about a cancelled order.
Pattern: A new failure row whose trigger covers several world states is tested on one, and its rubric is worded for that one.

M23 | Gap | Nit | failure row "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
Quote: "| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | ... make CO-A4 with reason cancellation unknown. | CO-07, G-03 |"
Evidence: M11 merged "answered without the order" into this row, but both scenarios that reach it (CO-S14, CO-S15) use a lookup that does not answer.
Pattern: A trigger merged into an existing failure row gets no scenario of its own.

M24 | Lies | Nit | CO-S11, CO-S26, Data variants row 2
Quote: "| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |" with Initial state "with status <status> until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: The only source for the race is round 2 Q1: "status can flip processing → shipped between the agent's read and its cancel call". The inputs give no case of a placed order jumping straight to shipped. The expected behavior is the same either way.
Pattern: A data-variant row creates a world-state transition the domain inputs do not describe.

M25 | Ambiguous | Nit | CO-02 and failure row "the customer named no order, and exactly one ... placed or processing"
Quote: "| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order. | CO-02 |" against CO-02 "the agent may propose that order."
Evidence: The rule makes proposing optional, the row mandatory. CO-S28's Unambiguity note follows the rule ("may propose it without asking which"). If the agent asks "which order?" in CO-S28, User knows has no answer; reviewers could split.
Pattern: A rule and its failure row give different modalities (may versus must) for the same situation.

M26 | Ambiguous | Nit | CO-02 new clauses and the two "named no order" failure rows
Quote: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order."
Evidence: Before the edit the condition was "the customer has not said which one they mean". CO-S02 rows 2 and 3 and CO-S27 row 3 ("the candle order") identify an order by item or placed date, not number. "names no order" does not say whether describing an order counts. A customer who says "cancel my candle order" when the candle order has shipped and one other is processing: one reading gives the CO-01 shipped answer, the other lets the agent propose the processing order.
Pattern: A rule's trigger term is undefined while scenarios identify orders both by number and by description.

M27 | Ambiguous | Nit | failure row "CO-A3 | the order system reported the order not cancelled"
Quote: "| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3 and no CO-A4; tell the customer no refund was issued. | CO-05, G-03 |"
Evidence: Under CO-05 a compliant agent makes CO-A3 only for an order returned or shown cancelled, so the only compliant path to OrderNotCancelled is an order the agent cancelled in this conversation, left with no pending or issued refund and no retry allowed (CO-06). The rewritten CO-07 requires CO-A4 in that case ("When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows ... the agent makes CO-A4"); the row forbids CO-A4. Not a re-report of M2: the new row now contradicts the rewritten CO-07.
Pattern: A failure row's directive contradicts a rule that covers the same situation.

