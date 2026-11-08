# Round 1 merged findings

## R1-01 (Important)
Sources: faithfulness F1, coverage F3

R1-01 | Lies | Important | §4.1 Failure handling, rows "CO-A2 / did not answer the second CO-A2" and "CO-A3 / payment provider temporarily unavailable for the second CO-A3"
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: review-packet.md, Round 3 Q4 (user: "Yes to all"): "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Re-read fails, say outcome unknown, issue no refund, hand off." That procedure applies to any cancel timeout, and the second cancel call is a cancel call. The spec row skips the re-read after the second timeout and bans CO-A3, so an order that the second call did cancel gets no refund, and the customer is told the outcome is "not known" when one lookup would show it. That also breaks the spec's own G-03 (line 24), which allows "outcome is unknown" only "when it cannot tell". Second instance, line 104: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued ...". Line 102 sends a first CO-A3 that "did not answer" into this row too. Inputs: packet Round 2 Q4 case 3 ("refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status") and Round 3 Q3 ("For case 3, after the retry the agent re-reads the refund record"). Appendix A, CO-A3 row (line 1525), says "A timeout creates the refund or not as Initial state says". So after a timed-out first call, "the refund has not been issued" may be false, and the input requires a re-read before reporting. CO-S15 and CO-S18 pass either way because their lookups fail or their first call is a ProviderUnavailable, so the scenarios do not catch it.
Pattern: When the bounded retry of a commit call follows a timeout, the failure row for the retry's outcome drops the re-read the inputs require after any timeout. The agent then reports or hands off based on an unread state.

## R1-02 (Important)
Sources: faithfulness F2

R1-02 | Lies | Important | CO-S17 Data variants row 3; §4.1 Failure handling row "CO-A3 / returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Appendix A, CO-A3 row (line 1525), defines the outcome "the order is not cancelled: `OrderNotCancelled`". In CO-S17 row 3, CO-A2 has just returned cancelled, and the scenario's own Final state (line 1023) asserts "HG-10482 has status cancelled". So the tool returns OrderNotCancelled for an order that is cancelled, which contradicts the outcome condition Appendix A gives. On that result, the failure row (line 103) tells the agent to "make CO-A4 with reason refund not issued; tell the customer the order is cancelled". Rubric "Refund not issued reported" (line 1505) enforces "tells the customer the order is cancelled". But the order system's latest answer says it is not cancelled. CO-07 (line 80) sends exactly this case, "when the agent cannot tell whether the order was cancelled", to reason cancellation unknown. Nothing in the packet says what to do on OrderNotCancelled (it was only added as an outcome in the tool confirmation turn, change 2). An agent that reports the conflict honestly, or hands off as cancellation unknown, fails the Required event and the rubric.
Pattern: An injected supporting-actor answer that contradicts the scenario's own world state, followed by a prescribed report and handoff reason that ignore the contradiction.

## R1-03 (Important)
Sources: faithfulness F3

R1-03 | Lies | Important | §4.1 Failure handling row "CO-A3 / did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md, Round 3 Q3 (user: "Yes to all"): "For case 3, after the retry the agent re-reads the refund record: ... failed or no refund, hand off and say the refund is not confirmed yet". The spec replaces the user's chosen message, "not confirmed yet", with the stronger claim "has not been issued". It does so in the failure row (line 105), in CO-S20's Reference trajectory step 10 (line 1219), and in CO-S20's Unambiguity note (line 1223). The shared rubric "Refund not issued reported" (line 1505, used by CO-S20) checks for "the refund has not been issued". An agent that says what the user specified ("your refund is not confirmed yet") can be judged as failing that dimension.
Pattern: A message the inputs dictate for one path is replaced by the wording of a different path (case 2's "not issued") through a shared rubric dimension.

## R1-04 (Important)
Sources: coverage F1

R1-04 | Gap | Important | Scope & Authority "must not" list; no Contract rule; no scenario
Quote: "- promise a date by which the refunded money arrives."
Evidence: review-packet.md Round 3 Q1, confirmed with "Yes to all": "The agent promises nothing about when the money arrives." Round 2 Q2 had first proposed "money arrives in 5 to 10 business days", so an agent that states that window is a realistic failure. In the spec the rule appears only as a must-not bullet (agent-spec.md line 49). No CO-xx rule carries it, §2 names no interest it protects, and no rubric dimension in §5.2 (lines 1495-1509) checks for it. That includes every success scenario where the agent reports the refund: CO-S01, S02, S03, S09, S12, S13, S16, S19. An agent that says "your refund will arrive in 5-10 business days" passes every scenario.
Pattern: A confirmed input rule that lives only in the must-not list has no tagged Contract rule and no scenario or dimension asserting it.

## R1-05 (Important)
Sources: coverage F2

R1-05 | Gap | Important | Failure handling row "changed … in the confirming turn or after confirming"; G-02
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: G-02 (line 21): "Any change to a proposal term after confirmation voids that confirmation". This comes from review-packet.md Round 1 Q4: "any change after confirmation voids it". The only scenario with a change is CO-S03. Its Turn 2 is given "in place of a confirmation" (line 248), and its Unambiguity note (line 292) says "Turn 2 replaces the order before any confirmation, so it confirms nothing". No scenario has the customer confirm and change in the same turn (e.g. "Yes — actually make it HG-10511"), or change after confirming. So the row's trigger and the voiding clause of G-02 are never exercised. Two wrong agents would pass every scenario: one that treats "yes, but HG-10511" as confirmation for HG-10511, and one that cancels HG-10482 on that "yes".
Pattern: A failure row (and the rule clause it implements) whose trigger condition no scenario's User block or Initial state produces. The nearest scenario tests a neighbouring condition instead.

## R1-06 (Important)
Sources: coverage F4

R1-06 | Gap | Important | Global Contract G-01 / CO-06; Failure handling
Quote: "absent"
Evidence: Nothing covers a customer who asks for more than one order in one conversation, either together ("cancel both") or one after the other. Such a request is realistic: CO-S02 and CO-S03 both start with two open orders (lines 180, 240-241). G-01 limits the agent to "the one order the current request is about" (line 18). CO-06 counts "at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation" (line 77), and allows a second CO-A2 "only after the first went unanswered". So cancelling a second order in the same conversation is implicitly forbidden, but no rule or failure row says what the agent tells the customer, and no scenario tests it. An agent that cancels both orders under one "yes", or that silently ignores the second, faces no defined verdict. Checklist cockburn-checklist.md brainstorm: "the lookup returns more than one plausible match"; "the user … changes the request mid-way".
Pattern: A request shape the spec's own limits forbid only by implication (per-request vs per-conversation counts) has no rule telling the agent what to do or say, and no scenario.

## R1-07 (Important)
Sources: coverage F5

R1-07 | Gap | Important | §2 customer-support interest; Failure handling row "status cancelled"; CO-S06
Quote: "| any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |"
Evidence: §2 (line 11): the customer-support team "wants every order whose refund is unfinished or whose cancellation is uncertain handed to it". The primary actor (line 9) wants to be told "where the refund stands". CO-07 (line 80) allows CO-A4 "in no other situation" than the current conversation's unfinished refund or cancellation. The already-cancelled row does not branch on the refund that list_orders returns (Appendix A line 1523: `refund` is an object with a status, or null). So an order that is already cancelled but whose refund is failed or missing gets only "already cancelled". That is exactly the end state CO-S23 leaves when both handoffs time out (refund failed, no task). CO-S06 tests only an issued refund (line 406). The packet's confirmed derivation ("An already cancelled order: the agent reports that and changes nothing") settles the state side: no CO-A4. It does not settle what the customer is told, and it leaves the §2 interest with no rule for this case.
Pattern: A lookup-driven row ignores a field of the lookup result (the refund) that changes what a stakeholder needs, and its scenario uses only the easy value of that field.

## R1-08 (Nit)
Sources: faithfulness F4

R1-08 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1544), "cancelling an order that is already cancelled returns it cancelled and changes nothing", is exactly such a guarantee for cancellation. So G-04 read literally permits a blind CO-A2 resend, which packet Round 3 Q4 forbids ("If the cancel call times out: no blind resend; re-read the order"). The parenthetical also cites only SG-01, while the CO-A4 retry relies on SG-03 (failure row line 106). CO-06 (line 77) and the Forbidden lines in CO-S12 and CO-S13 ("A second CO-A2 before a CO-A1 made after the first CO-A2") pin the actual behavior, so no verdict changes.
Pattern: A global rule's general permission is wider than a capability-specific constraint from the inputs, and its citation list is incomplete.

## R1-09 (Nit)
Sources: faithfulness F5

R1-09 | Lies | Nit | Appendix A, CO-A3 row
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The data model in packet Round 2 Q3, with the user's changes, defines Refund as "refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued, failed)". It has no failure-reason field, and the tool confirmation turn says only "terminal refund error returns a refund with status failed". The `failure_reason` field and its three enum values are invented. No scenario grades them (CO-S17 and CO-S23 vary the failure cause only in Initial state).
Pattern: A tool result field or enum that the data model and tool confirmation do not contain.

## R1-10 (Nit)
Sources: coverage F6

R1-10 | Nit | Gap | Failure handling; CO-01 / CO-02
Quote: "| any | the lookup shows the named order with status shipped or delivered | … |" and "| any | the lookup shows the named order with status cancelled | … |"
Evidence: Every "no proposal" row needs either a named order (lines 91-93) or more than one open order (line 90, CO-02 line 65). Nothing covers a customer who names no order ("cancel my order") and has no order with status placed or processing: no orders at all, or only shipped, delivered or cancelled ones. CO-01's "proposes nothing" keeps the state safe, but no rule says what to tell the customer, and no scenario tests the case. Checklist cockburn-checklist.md brainstorm: "the lookup returns more than one plausible match, or none".
Pattern: The "none found" result of the order lookup, when the customer names no order, has no failure row.
