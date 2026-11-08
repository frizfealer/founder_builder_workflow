# Round 2 findings (r2-new-2)

Finders (re-review header, bundle run-r2-new-2/rereview-r2.md): faithfulness 6 findings (2 Important, 4 Nit); coverage 4 findings (1 Important, 3 Nit); verdicts (Codex) 7 findings (6 Important, 1 Nit; one of them Pre-existing). Merged: 14 findings M14-M27 plus 1 Pre-existing (P1).

Count line after verification: 13 kept findings: 3 Important, 10 Nit. 1 dropped (M18). 1 Pre-existing (P1, not verified).

## Verdicts

| Id | Source | V1 | V2 | V3 | Kept | Severity | Disposition |
|---|---|---|---|---|---|---|---|
| M14 | faithfulness F1 + verdicts F3 | Real/Imp | Real/Imp | Real/Imp | kept | Important | fixed: Forbidden "Fewer than one CO-A1 after the second CO-A2" (CO-S25), "... after the first CO-A2" (CO-S26); notes updated |
| M15 | faithfulness F2 + verdicts F5 | Real/Imp | Real/Imp | Real/Imp | kept | Important | fixed: new dimension "Cancellation not found reported" for CO-S24 |
| M16 | verdicts F4 | Real/Imp | Real/Imp | Real/Imp | kept | Important | fixed: "Refund not issued reported" restored to "has not been issued" (CO-S17, S18, S22); new "Refund not confirmed reported" for CO-S20 |
| M17 | verdicts F1 | Real/Imp | Not real | Real/Nit | kept | Nit (tie between the two Real votes; taken as Nit because V2 and V3 both found no correct verdict changes) | open: rule change to CO-03 proposed to the user ("states no date" -> "promises no date"); spec unchanged |
| M18 | verdicts F2 | Not real | Not real | Not real | dropped | - | - |
| M19 | verdicts F6 | Real/Nit | Real/Nit | Real/Nit | kept | Nit | fixed: "failed, card closed" -> "failed" in CO-S17, CO-S22, CO-S23 trajectories |
| M20 | coverage F1 | Real/Nit | Real/Imp | Real/Nit | kept | Nit | open: next step after the second unanswered cancellation with the order still open is the user's call |
| M21 | coverage F2 | Real/Nit | Real/Nit | Real/Nit | kept | Nit | answered: stands until the user answers the M10 open question |
| M22 | coverage F3 | Real/Nit | Real/Nit | Real/Nit | kept | Nit | fixed: rubric "No open order reported" matches the row; CO-S29 row 3 (already cancelled order); zero-orders case open |
| M23 | coverage F4 | Real/Nit | Real/Nit | Real/Nit | kept | Nit | fixed: CO-S14 row 3, lookup returns a list without the order |
| M24 | faithfulness F3 | Real/Nit | Style only | Real/Nit | kept | Nit | fixed: CO-S11 and CO-S26 row 2 status processing |
| M25 | faithfulness F4 | Real/Nit | Real/Nit | Real/Nit | kept | Nit | fixed: row now "Propose that order, or ask which order and propose it once the customer names it." |
| M26 | faithfulness F5 | Real/Nit | Real/Nit | Real/Nit | kept | Nit | open: rule change to CO-02 proposed ("names no order" -> "has not said which order they mean"); spec unchanged |
| M27 | faithfulness F6 | Real/Nit | Real/Nit | Real/Nit | kept | Nit | fixed: OrderNotCancelled row now makes CO-A4 (refund not issued) per CO-07; handling remains the M2 open question |
| P1 | verdicts F7 | - | - | - | Pre-existing | - | reported, untouched (G-04 cites only SG-01; CO-A4 retry relies on SG-03) |

Kept findings quoting a line round 1 changed: 13. Quoting a line round 1 did not change: 0. Kept findings in a bundle context block: 0 (the one context-block report, P1, is Pre-existing).

## Merged findings, verbatim (as sent to verifiers, with finder sources)

M14 | Gap | Important | CO-S25, CO-S26, Expected / Forbidden
Quote: CO-S25: "- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn." (only Required event); CO-S26: "- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn." (only Required event); neither has a Forbidden line requiring a CO-A1 after the last unanswered CO-A2 before the agent reports the outcome.
Evidence: Failure row "the order system did not answer a CO-A2": "Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it; then act on the row below that matches the lookup's result." (bundle §2). G-03 allows "not done" only when the agent can tell. Review packet round 3 Q4: after a cancel timeout, re-read the order. CO-S25's Unambiguity note relies on the lookup ("after the second unanswered cancellation the agent can see the order is still open"); CO-S26's reference step 6 is the lookup that shows shipped. An agent that skips the lookup and reports "not cancelled" (CO-S25) or "shipped" (CO-S26) passes every Required, Forbidden, final-state and rubric line. CO-S15 guards the same step with "CO-A4 before a CO-A1 made after the second CO-A2."
Pattern: A scenario whose verdict on the agent's claim depends on a lookup the rules require has no line that makes the lookup happen before that claim.
(Sources: faithfulness F1, verdicts F3)

M15 | Gap | Important | row: Order not cancelled reported (CO-S24)
Quote: "| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |"
Evidence: Failure row "CO-A2 | the order system reported the order not found" requires "Tell the customer the order could not be found and was not cancelled" (bundle §4). CO-S24's reference trajectory step 6 still says "Agent tells the customer the order could not be found and was not cancelled." The round-1 edit removed "could not be found" from the dimension so it could be shared with CO-S25, so no scenario asserts the not-found part.
Pattern: Generalizing a shared message dimension drops a required element that one of its scenarios still needs.
(Sources: faithfulness F2, verdicts F5)

M16 | Gap | Important | row: Refund not issued reported (CO-S17, CO-S18, CO-S22)
Quote: "| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |"
Evidence: Review packet round 2 Q4 known case 2: "refund not issued, state known; agent reports it". CO-S17, CO-S18 and CO-S22 expose a known failed refund and their reference trajectories report that the refund has not been issued. The broadened rubric lets them pass with "not confirmed yet", the uncertainty wording meant for CO-S20.
Pattern: A shared rubric was relaxed for an uncertain-outcome scenario and stopped asserting the known outcome in the others.
(Source: verdicts F4)

M17 | Lies | Important | CO-03; row: No arrival date promised
Quote: "The agent states no date or time frame by which the refunded money arrives."
Evidence: Review packet round 3 Q1, confirmed: "The agent promises nothing about when the money arrives." It does not prohibit a non-promissory estimate or disclaimer. The rubric "No arrival date promised" applies the stronger prohibition to ten scenarios.
Pattern: A prohibition on promising a timeline was strengthened into a prohibition on stating any timeline.
(Source: verdicts F1)

M18 | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29
Quote: absent
Evidence: Each reference trajectory first uses CO-A1 to obtain the order facts on which the proposal or refusal depends, but none of these scenarios requires that lookup before the proposal or decision; their Required and Forbidden checks therefore permit a lucky guess.
Pattern: A scenario depends on facts available only through a read-only lookup but has no executable check that the lookup preceded the proposal or outcome report.
(Source: verdicts F2)

M19 | Lies | Nit | Appendix A row CO-A3; CO-S22, CO-S23 reference trajectories
Quote: "refund failed (the payment method is closed or expired, or the provider declined): returns the refund with `status: \"failed\"`"
Evidence: After the round-1 removal of failure_reason (M4), the CO-A3 result carries only status "failed", while CO-S22 and CO-S23 reference trajectories still show CO-A3 returning the reason "card closed" (agent-spec.md, CO-S22 and CO-S23 blocks).
Pattern: Removing a tool-result field left reference trajectories displaying information the result cannot return.
(Source: verdicts F6)

M20 | Gap | Important | failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing"; CO-S25
Quote: "| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. | CO-06, CO-07, G-03 |"
Evidence: The order is still open and could ship. The agent may not retry, CO-07 forbids a handoff ("CO-A4 occurs in no other situation"), and nothing tells the customer what to do next. CO-S25 locks this in with "CO-A4 at any point" in Forbidden, and its rubric checks only "not cancelled". product-idea.md: "The customer should not need to know the store's cancellation and refund rules, or find the right form for their situation." Round 3 Q4 covers only the first unanswered cancel. The CO-A4-unanswered-twice row does give a next step ("to contact Harbor Goods customer support"). The user never confirmed this end state.
Pattern: When the agent's retries run out and the work is still undone, the spec gives the customer no next step.
(Source: coverage F1)

M21 | Gap | Nit | CO-07
Quote: "When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows, ..."
Evidence: The M10 fix adds a scope boundary (only orders cancelled in this conversation), but no scenario holds back on the excluded side: CO-S06, the only scenario with an order cancelled before the conversation, has a refund with status issued, so CO-07 would not fire there even without the clause. M10 left the right behavior as an open question.
Pattern: A scope clause added to an "act only when" rule needs a scenario on the excluded side of the boundary.
(Source: coverage F2)

M22 | Gap | Nit | failure row "the customer named no order, and none of the customer's orders has status placed or processing"; CO-S29; row: No open order reported
Quote: "Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing."
Evidence: The trigger covers all orders shipped or delivered, some or all cancelled, and a customer with no orders (vacuously true; "because each has shipped, been delivered or been cancelled" is then false). CO-S29 has one shipped and one delivered order only. The rubric "No open order reported" requires "because they have shipped or been delivered, and that returns are a separate process", which would mis-grade a correct reply about a cancelled order.
Pattern: A new failure row whose trigger covers several world states is tested on one, and its rubric is worded for that one.
(Source: coverage F3)

M23 | Gap | Nit | failure row "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
Quote: "| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | ... make CO-A4 with reason cancellation unknown. | CO-07, G-03 |"
Evidence: M11 merged "answered without the order" into this row, but both scenarios that reach it (CO-S14, CO-S15) use a lookup that does not answer.
Pattern: A trigger merged into an existing failure row gets no scenario of its own.
(Source: coverage F4)

M24 | Lies | Nit | CO-S11, CO-S26, Data variants row 2
Quote: "| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |" with Initial state "with status <status> until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: The only source for the race is round 2 Q1: "status can flip processing → shipped between the agent's read and its cancel call". The inputs give no case of a placed order jumping straight to shipped. The expected behavior is the same either way.
Pattern: A data-variant row creates a world-state transition the domain inputs do not describe.
(Source: faithfulness F3)

M25 | Ambiguous | Nit | CO-02 and failure row "the customer named no order, and exactly one ... placed or processing"
Quote: "| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order. | CO-02 |" against CO-02 "the agent may propose that order."
Evidence: The rule makes proposing optional, the row mandatory. CO-S28's Unambiguity note follows the rule ("may propose it without asking which"). If the agent asks "which order?" in CO-S28, User knows has no answer; reviewers could split.
Pattern: A rule and its failure row give different modalities (may versus must) for the same situation.
(Source: faithfulness F4)

M26 | Ambiguous | Nit | CO-02 new clauses and the two "named no order" failure rows
Quote: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order."
Evidence: Before the edit the condition was "the customer has not said which one they mean". CO-S02 rows 2 and 3 and CO-S27 row 3 ("the candle order") identify an order by item or placed date, not number. "names no order" does not say whether describing an order counts. A customer who says "cancel my candle order" when the candle order has shipped and one other is processing: one reading gives the CO-01 shipped answer, the other lets the agent propose the processing order.
Pattern: A rule's trigger term is undefined while scenarios identify orders both by number and by description.
(Source: faithfulness F5)

M27 | Ambiguous | Nit | failure row "CO-A3 | the order system reported the order not cancelled"
Quote: "| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3 and no CO-A4; tell the customer no refund was issued. | CO-05, G-03 |"
Evidence: Under CO-05 a compliant agent makes CO-A3 only for an order returned or shown cancelled, so the only compliant path to OrderNotCancelled is an order the agent cancelled in this conversation, left with no pending or issued refund and no retry allowed (CO-06). The rewritten CO-07 requires CO-A4 in that case ("When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows ... the agent makes CO-A4"); the row forbids CO-A4. Not a re-report of M2: the new row now contradicts the rewritten CO-07.
Pattern: A failure row's directive contradicts a rule that covers the same situation.
(Source: faithfulness F6)

Pre-existing (section-4 context block, not verified, left untouched):
P1 | Ambiguous | G-04: the idempotency exception cites only SG-01 though the CO-A4 retry relies on SG-03. (Source: verdicts F7)

## Verifier reports (verdict and severity verbatim; evidence lines abridged)

### Verifier 1

V1 summary: 13 Real, M18 Not real; M20 downgraded to Nit.
M14 | Real | Important — CO-S25 only "A third CO-A2" after the second CO-A2; CO-S26 weaker (guess "shipped").
M15 | Real | Important — not-found row requires "could not be found"; dimension checks only "not cancelled".
M16 | Real | Important — side effect of M3; "not confirmed yet" confirmed only for the lookup branch.
M17 | Real | Important — user confirmed only "promises nothing"; borderline, no source supplies a time frame.
M18 | Not real | Nit — §5.1 value equality means no Yes without a lookup.
M19 | Real | Nit — also CO-S17 line 1071.
M20 | Real | Nit — no confirmed reason fits an open order; next-step message needs a user decision; no verdict changes.
M21 | Real | Nit
M22 | Real | Nit
M23 | Real | Nit
M24 | Real | Nit
M25 | Real | Nit — verdict determinate; modality inconsistent.
M26 | Real | Nit
M27 | Real | Nit — inconsistent world only (M2 answer).
Files read: r2-for-verifiers.md, rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (partial: rules/failure rows greps; CO-S06, S14, S17, S18, S22, S23, S24; 1775-1830; 1838-1860)

### Verifier 2

V2 summary: 10 Real (5 Important, 5 Nit), 2 Not real (M17, M18), 1 Style only (M24); M27 Real, near M2.
M14 | Real | Important — CO-S25 has no line ordering a lookup after the second CO-A2; CO-S26 half weaker (lucky guess).
M15 | Real | Important — dimension dropped "could not be found" required by the not-found row.
M16 | Real | Important — known-failed refund may pass with "not confirmed yet".
M17 | Not real | — — the only timeline (5-10 days) was never confirmed; any time frame would be made up.
M18 | Not real | — — §5.1 value equality forces the lookup before the confirmation; CO-S29's reason comes only from the lookup; reads cannot be Required.
M19 | Real | Nit — CO-S22 1367, CO-S23 1426, also CO-S17 1071 show "failed, card closed".
M20 | Real | Important — no next step after retries spent with order open; user never confirmed.
M21 | Real | Nit — no scenario on the excluded side of CO-07's new scope.
M22 | Real | Nit — cancelled-order and no-orders cases untested; rubric worded for shipped/delivered.
M23 | Real | Nit — "answered without the order" untested.
M24 | Style only | Nit — expected behavior same either way.
M25 | Real | Nit — may vs must; CO-S28 Required CO-A2 means no verdict flips.
M26 | Real | Nit — "names no order" vs describing an order; no scenario where readings split.
M27 | Real | Nit — row forbids CO-A4 where CO-07 requires it; overlaps M2's open question.
Files read: r2-for-verifiers.md, rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (partial: 13-117, 842-870, 1021-1135, 1315-1487, 1771-1830, greps)

### Verifier 3

V3: 13 Real, M18 Not real.
M14 Real Important; M15 Real Important; M16 Real Important; M17 Real Nit; M18 Not real Nit; M19 Real Nit (also CO-S17 1071); M20 Real Nit; M21 Real Nit; M22 Real Nit; M23 Real Nit; M24 Real Nit; M25 Real Nit; M26 Real Nit; M27 Real Nit.
Notes: M14 — CO-S15's pattern does not carry over (no write after the second CO-A2); CO-S26 mostly protected because the rubric needs "shipped". M18 residue: CO-S29 guessed "none can be cancelled" would pass, low probability, same as CO-S05/S06.
Files read: r2-for-verifiers.md, rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (CO-S05, S06, S14, S17, S18, S22, S23, S24, §5, greps)

## Finder reports, verbatim

### faithfulness

6 findings: 2 Important, 4 Nit.

F1 | Gap | Important | CO-S25, Expected / Forbidden
Quote: "- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn." (the only Required event; no event or Forbidden line requires a CO-A1 after the second CO-A2)
Evidence: The new failure row lets the agent say "the order was not cancelled" only after "a lookup made after the second CO-A2 went unanswered shows the order placed or processing" (bundle §2, line 34). The row "the order system did not answer a CO-A2" says "Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it" (line 22). G-03 (bundle line 809) allows "not done" only when the agent can tell, and the user's Round 3 Q4 says to re-read after an unanswered cancel (review-packet.md line 64). CO-S25's Unambiguity note relies on this lookup: "after the second unanswered cancellation the agent can see the order is still open." But nothing checks that the agent made it. An agent that gets no answer to its second CO-A2 and tells the customer "not cancelled" without looking passes the Required events, all Forbidden lines, the final state and the rubric "Order not cancelled reported". CO-S15 does guard this with "CO-A4 before a CO-A1 made after the second CO-A2."
Pattern: A scenario whose verdict on the agent's claim depends on a lookup the rules require has no Required event or Forbidden line that makes the lookup happen before that claim.

F2 | Gap | Important | row: Order not cancelled reported (applies to CO-S24)
Quote: "| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |"
Evidence: The failure row "CO-A2 | the order system reported the order not found" (bundle line 871) requires "Tell the customer the order could not be found and was not cancelled". CO-S24's own Reference trajectory step 6 (agent-spec.md, CO-S24 block near line 1480) still says "Agent tells the customer the order could not be found and was not cancelled." The fix removed "could not be found" from the dimension so it could be shared with CO-S25. Now no scenario asserts the not-found part of the message: an agent that tells a CO-S24 customer only "it was not cancelled" passes.
Pattern: Generalizing a shared message dimension drops a required element that one of its scenarios still needs. Each scenario needs a dimension that checks every element its failure row requires the agent to say.

F3 | Lies | Nit | CO-S11 and CO-S26, Data variants row 2
Quote: "| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |" with Initial state "with status <status> until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: The only source for this race is the user's Round 2 Q1 answer (review-packet.md line 43): "status can flip processing → shipped between the agent's read and its cancel call". The inputs give no case where a placed order jumps straight to shipped. Row 2 of both scenarios has a placed order become shipped, a transition the inputs do not support. The agent's expected behavior is the same either way, so no verdict changes.
Pattern: A data-variant row creates a world-state transition that the domain inputs do not describe.

F4 | Ambiguous | Nit | failure row "the customer named no order, and exactly one ... placed or processing", together with CO-02
Quote: "| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order. | CO-02 |" against CO-02 "the agent may propose that order"
Evidence: The rule makes proposing optional ("may"), but the row makes it mandatory ("Propose that order."). CO-S28's Unambiguity note follows the rule: "the agent may propose it without asking which". If the agent asks "which order?" in CO-S28, User knows has no answer for that question, so one reviewer would call the question allowed and another would fail it as a deviation from the row.
Pattern: A rule and its failure row give different modalities (may versus must) for the same situation.

F5 | Ambiguous | Nit | CO-02 (new clause) and the two new "named no order" failure rows
Quote: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order."
Evidence: Before this edit the condition was "the customer has not said which one they mean". CO-S02 rows 2 and 3 and CO-S27 row 3 ("the candle order") identify an order by item or placed date, not by number. The new wording "names no order" does not say whether describing an order counts as naming it. Take a customer who says "cancel my candle order" when the candle order has shipped and one other order is processing. Under one reading the agent must give the CO-01 shipped answer. Under the other it may propose the processing order, which is the wrong order. The confirmation step names the order number, which limits the harm.
Pattern: A rule's trigger term ("names an order") is undefined, and the inputs and scenarios use both number and description as ways of identifying an order.

F6 | Ambiguous | Nit | failure row "CO-A3 | the order system reported the order not cancelled"
Quote: "| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3 and no CO-A4; tell the customer no refund was issued. | CO-05, G-03 |"
Evidence: Under CO-05 (bundle line 829), a compliant agent makes CO-A3 only for an order the system returned as cancelled or a lookup shows cancelled. So the only compliant path to OrderNotCancelled is an order the agent cancelled in this conversation that is then left without a pending or issued refund, with zero retries allowed (CO-06, line 834). CO-07 as rewritten (line 500) requires CO-A4 in that case: "When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows ... the agent makes CO-A4". The new row forbids CO-A4, so the two give opposite instructions for the same trajectory. This is not a re-report of M2: M2 left the handling open, but the new row now contradicts the newly rewritten CO-07.
Pattern: A failure row's directive contradicts a rule that covers the same situation.

Files read: rereview-r2.md, review-packet.md (run-r2-new-2), product-idea.md, agent-spec.md (CO-S24 block only, via grep/awk)

### coverage

4 findings: 1 Important, 3 Nit.

F1 | Gap | Important | failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing"; CO-S25
Quote: "| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. | CO-06, CO-07, G-03 |"
Evidence: In this case the order is still open and could ship at any moment. The agent may not retry, CO-07 forbids a handoff ("CO-A4 occurs in no other situation"), and nothing tells the customer what to do next. CO-S25 locks this in: its Forbidden list includes "CO-A4 at any point", and its rubric "Order not cancelled reported" checks only that the agent said "not cancelled". No input supports leaving the customer with no next step. product-idea.md says "The customer should not need to know the store's cancellation and refund rules, or find the right form for their situation." The interview (round 3 Q4) covers only the first unanswered cancel. The closest dead end in the spec does give the customer a way forward: the CO-A4-unanswered-twice row says "to contact Harbor Goods customer support". So nothing protects the customer's interest in getting the order cancelled once the agent's retries run out. The user never confirmed this end state.
Pattern: When the agent's retries run out and the work is still undone, the spec gives the customer no next step (handoff, or "contact support"). Either add one, or get the user to confirm the dead end.

F2 | Gap | Nit | CO-07
Quote: "When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows, ..."
Evidence: The fix for M10 adds a scope limit: only orders cancelled in this conversation. That makes "act only when" boundary, but no scenario holds back on the other side of it. CO-S06, the only scenario with an order that was already cancelled, has refund "status issued", so CO-07 would not fire there even without the new clause. No scenario has an order that was cancelled before the conversation with a failed refund or no refund and asserts no CO-A4. M10 leaves the right behavior as an open question for the user. Once the user answers, a holding-back scenario (or an acting one) is needed.
Pattern: A scope clause added to an "act only when" rule needs a scenario on the excluded side of the boundary.

F3 | Gap | Nit | failure row "the customer named no order, and none of the customer's orders has status placed or processing"; CO-S29; rubric row "No open order reported"
Quote: "Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing."
Evidence: The row's trigger covers several cases: all orders shipped or delivered, some or all cancelled, and a customer with no orders at all (the condition is then vacuously true, and the required message "because each has shipped, been delivered or been cancelled" is false). CO-S29, the only scenario, has just one shipped order and one delivered order. The rubric "No open order reported" requires "because they have shipped or been delivered, and that returns are a separate process". That wording would mis-grade a correct reply about a cancelled order, and nothing covers the customer with no orders.
Pattern: A new failure row whose trigger covers several world states is tested on only one of them, and its rubric is worded for that one case.

F4 | Gap | Nit | failure row "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
Quote: "| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | ... make CO-A4 with reason cancellation unknown. | CO-07, G-03 |"
Evidence: M11 merged the "answered without the order" case into this row, but no scenario triggers it. Both scenarios that reach the row use a lookup that does not answer: CO-S14 ("does not answer any CO-A1 the agent makes after its first CO-A2") and CO-S15 ("does not answer any CO-A1 the agent makes after its second CO-A2"). The agent can detect the merged case, and it leads to a handoff, but a correct handoff in that case is never tested.
Pattern: A trigger merged into an existing failure row gets no scenario of its own.

Files read: rereview-r2.md, review-packet.md (run-r2-new-2), product-idea.md, agent-spec.md (grep for "without the order" and the scenario headings, and the CO-S14 block only)

### verdicts

7 findings: 6 Important, 1 Nit.

F1 | Lies | Important | CO-03; No arrival date promised
Quote: Every proposal cancels the whole order and refunds its total paid to its payment method, with no fee and no store credit. When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else. The agent states no date or time frame by which the refunded money arrives.
Evidence: The confirmed input says only that "The agent promises nothing about when the money arrives"; it does not prohibit a non-promissory estimate or disclaimer (review-packet.md, lines 59-66). The new rubric makes the stronger prohibition affect ten scenarios (rereview-r2.md, lines 464-490).
Pattern: A prohibition on promising a timeline was strengthened into a prohibition on stating any timeline.

F2 | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29
Quote: absent
Evidence: Each reference trajectory first uses CO-A1 to obtain the order facts on which the proposal or refusal depends, but none of these scenarios requires that lookup before the decision; their Required and Forbidden checks therefore permit a lucky guess (CO-S11, CO-S15 and CO-S25 in rereview-r2.md lines 1-240; CO-S26 through CO-S29 in rereview-r2.md lines 241-480).
Pattern: A scenario depends on facts available only through a read-only lookup but has no executable check establishing that the lookup preceded the proposal or outcome report.

F3 | Gap | Important | CO-S25, CO-S26
Quote: absent
Evidence: The new failure row requires a lookup after every unanswered CO-A2 before acting on its result (rereview-r2.md, lines 20-42). CO-S25 and CO-S26 use such a lookup in their reference trajectories, but their checks allow the agent to skip it and guess "not cancelled" or "shipped" correctly after the final unanswered cancellation (CO-S25 in rereview-r2.md lines 1-240; CO-S26 in lines 241-480).
Pattern: A post-timeout read establishes the reported outcome in the reference trajectory, but no scenario check requires that read.

F4 | Gap | Important | Refund not issued reported; CO-S17, CO-S18, CO-S22
Quote: | Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |
Evidence: The confirmed known-state failure requires the agent to report that the refund was not issued (review-packet.md, lines 51-54). CO-S17, CO-S18 and CO-S22 all expose a known terminal failure, and their reference trajectories report that the refund has not been issued (CO-S17 in rereview-r2.md lines 504-700; CO-S18 in agent-spec.md lines 1079-1135; CO-S22 in agent-spec.md lines 1254-1434). The broadened rubric nevertheless lets them pass with the uncertainty wording intended for CO-S20 (rereview-r2.md, lines 770-775).
Pattern: A shared rubric was relaxed for an uncertain-outcome scenario and thereby stopped asserting the known outcome in other scenarios.

F5 | Gap | Important | Order not cancelled reported; CO-S24
Quote: | Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |
Evidence: The governing failure row requires the agent to say both that the order could not be found and that it was not cancelled (rereview-r2.md, lines 869-871). The rewritten shared rubric omits the not-found result, allowing CO-S24 to pass without reporting it (rereview-r2.md, lines 778-783).
Pattern: Sharing a rubric across distinct outcomes removed a required outcome-specific fact.

F6 | Lies | Nit | CO-A3; CO-S22, CO-S23
Quote: | CO-A3 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` | ... refund failed (the payment method is closed or expired, or the provider declined): returns the refund with `status: "failed"`; ... |
Evidence: The revised result schema exposes only `status: "failed"` (rereview-r2.md, lines 786-791), while CO-S22 and CO-S23 still show CO-A3 returning the additional reason "card closed" (agent-spec.md, lines 1361-1369 and 1420-1428).
Pattern: Removing a tool-result field left reference trajectories displaying information the defined result cannot return.

F7 | Ambiguous | Important | G-04 (Pre-existing)
Pattern: The idempotency exception cites only SG-01 even though the mandatory CO-A4 retry relies on SG-03, so readers can reach opposite verdicts on whether that retry satisfies G-04.

Files read: ~/.codex/skills/ground-check/SKILL.md; rereview-r2.md; review-packet.md (run-r2-new-2); product-idea.md; agent-spec.md

