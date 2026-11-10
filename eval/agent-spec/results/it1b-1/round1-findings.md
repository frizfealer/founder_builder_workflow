# Round 1 merged findings

14 findings: 8 Important, 6 Nit. (17 raw: faithfulness 5, verdicts 4, coverage 8.) 13 kept, 1 dropped.

Severity as the finders gave it; status is fixed / answered / open / dropped / Pre-existing (none Pre-existing: whole-spec scope). Verifier verdicts are from the one adversarial verifier; Nits went straight to 4.5 unverified, as the skill states.

## M1 — KEPT — fixed

Severity: finder Important; final Important. Sources: faithfulness F1, coverage F4.

Verifier: M1 | Real | Important | could not refute (Round 3 Q4 re-read applies to every cancel timeout; G-03, CO-07 and line 1519 conflict with the row)

Decision / fix: Kept. The second-CO-A2-timeout row now requires a lookup and handles cancelled (make CO-A3), shipped or delivered, placed or processing (not cancelled, no CO-A3, no CO-A4) and no answer (unknown, CO-A4 cancellation unknown). CO-S15 gains the lookup step and Forbidden 'CO-A4 before a CO-A1 made after the second CO-A2'. New CO-S25 (lookup shows cancelled) and CO-S26 (lookup shows shipped / still processing) cover the new branches. The placed-or-processing branch's no-handoff behaviour follows from CO-06 and CO-07 but no input states it: open question.

Finder text (faithfulness F1), verbatim:
```
F1 | Lies | Important | CO-A2 failure row "did not answer the second CO-A2" (§4.1 Failure handling); CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: review-packet.md, Interview Round 3 Q4 (confirmed "Yes to all") says that when a cancel call times out, the agent does not resend blindly. It re-reads the order: "Cancelled, continue to refund... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." Tool confirmation turn, change 4: "Reads may be retried on timeout without limit." The spec's row for the second timeout drops the re-read. It sends the agent straight to "not known" and a cancellation_unknown handoff, and it forbids CO-A3 even when a lookup would show the order cancelled. That conflicts with the spec's own CO-07 trigger ("when the agent cannot tell whether the order was cancelled"), since a lookup would tell. It also conflicts with G-03: saying "not known" is untrue once a lookup shows cancelled or shipped. CO-S15 hides the conflict with its Initial-state line "The order system does not answer any CO-A1 the agent makes after its second CO-A2". Its reference trajectory, step 8, hands off with no lookup after the second CO-A2. In production, a late-landing second cancel leaves a cancelled order with no refund and a needless staff task.
Pattern: a failure row for an unanswered commit call ends in an "unknown" handoff without the lookup the inputs require after every timeout. Check each timeout row for a lookup before the agent reports the outcome as unknown.
```

Finder text (coverage F4), verbatim:
```
F4 | Gap | Important | Failure handling row "did not answer the second CO-A2" / CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: Lookups are unlimited (review-packet.md line 85: "Reads may be retried on timeout without limit"; Appendix A line 1519). The agent may therefore look up the order after the second unanswered CO-A2, but this row has no branch for that lookup's result. If the lookup shows the order cancelled, the row still forbids CO-A3 and orders the agent to say the outcome is unknown and hand off with reason cancellation_unknown. That conflicts with:
- G-03 (line 24): "unknown" only "when it cannot tell";
- CO-05 (line 74): a refund is allowed when a lookup shows the order cancelled;
- CO-07 (line 80): the cancellation-unknown handoff applies only when the agent "cannot tell whether the order was cancelled".
A lookup showing placed/processing or shipped is equally unhandled. CO-S15 (line 892) hides the gap by making every CO-A1 after the second CO-A2 unanswered. The cocklist item "A failure row that branches on a lookup covers every result of the lookup" (cockburn-checklist.md) applies here. In production a customer whose order was in fact cancelled gets no refund and is told the outcome is unknown.
Pattern: A failure row for an unknown result skips the lookup that the rules for the first unknown result require. Every unknown-result row should state the lookup and handle every result of it (cancelled, open, shipped/delivered, absent, no answer).
```

## M2 — KEPT — fixed

Severity: finder Important; final Important. Sources: faithfulness F2, coverage F5, verdicts F2.

Verifier: M2 | Real | Important | could not refute either instance (OrderNotCancelled impossible after a CO-A2 that returned cancelled; OrderNotFound impossible for an order the lookup just returned)

Decision / fix: Kept. CO-S17 row 3 removed (dropped row; it exercised the OrderNotCancelled clause of the CO-A3 failure row); CO-S24 Initial state makes the order leave the order system when the first CO-A2 reaches it, Final state asserts the order system holds no such order. How the agent should handle OrderNotCancelled, which a rule-following agent cannot meet, left as an open question.

Finder text (faithfulness F2), verbatim:
```
F2 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "- The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
Evidence: Appendix A gives these outcomes as "the order is not cancelled: OrderNotCancelled" for issue_refund and "order not found: OrderNotFound" for cancel_order.
- CO-S17: reference step 5 is "CO-A2 (HG-10482) → cancelled", the CO-A2 effect is "Sets the order's status to cancelled", and the Final state is "HG-10482 has status cancelled". So OrderNotCancelled cannot be true at the CO-A3 call. The failure row and the rubric "Refund not issued reported" still require the agent to "tell the customer the order is cancelled" right after the order system said it is not. An agent that reports what the system said, or that stops to reconcile it, gets a judgment-dependent verdict.
- CO-S24: Initial state says "Order <order> belongs to the customer", and reference step 2 shows the order returned by list_orders. OrderNotFound cannot be true of an order that exists on the account, yet the rubric "Order not cancelled reported" requires the agent to say the order "could not be found".
Pattern: an injected supporting-actor outcome that contradicts the scenario's Initial state or the results of earlier calls. Each injected outcome must be one that Appendix A's outcome cell allows to be true at that call.
```

Finder text (coverage F5), verbatim:
```
F5 | Lies | Important | CO-S17 Data variants row 3 / Failure handling row "reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: In CO-S17 the first CO-A2 answers normally (§5.1 line 1469, "A supporting actor answers every call normally unless an Initial-state line says otherwise"). It returns cancelled and sets the order cancelled (Appendix A line 1524), and Final state asserts "HG-10482 has status cancelled". Appendix A (line 1525) defines `OrderNotCancelled` as the outcome when "the order is not cancelled", which cannot be true at that call. The verifier brief (verification.md, adversarial verifier section) says an injected outcome's Appendix A entry "must still describe something that can be true of the scenario at that call". The required report (failure row line 103; dimension "Refund not issued reported", line 1505) then makes the agent tell the customer "the order is cancelled" right after the order system said it is not. An agent that reports the contradiction, or says the cancellation status is uncertain, fails the rubric.
Pattern: An injected tool outcome contradicts the world state that the scenario's earlier calls produced. Either anchor the outcome to a state in which it can occur, or define how the agent reports conflicting answers from the order system.
```

Finder text (verdicts F2), verbatim:
```
F2 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: CO-S17's Initial state has no line overriding CO-A2, so CO-A2 answers normally (§5.1 line 1469). The reference trajectory step 5 (line 1044) returns "cancelled", and Final state line 1023 asserts "HG-10482 has status cancelled". So when CO-A3 runs, the order is cancelled, and Appendix A's outcome "the order is not cancelled: OrderNotCancelled" (line 1525) cannot be true at that call. This is the limit verification.md sets on injected outcomes: the outcome "must still describe something that can be true of the scenario at that call". The verdict then turns on a contradiction. A lookup would show the order cancelled. The failure row (line 103) and the rubric "Refund not issued reported" (line 1505) require "tell the customer the order is cancelled" just after the system said it is not. An agent that reports the system's answer ("the store says the order isn't cancelled") fails, and experts could split on whether it should. Second instance, CO-S24: lines 1411 and 1414 say the order belongs to the customer and the agent's lookup shows it, yet CO-A2 returns OrderNotFound. The rubric "Order not cancelled reported" (line 1506) then requires the agent to say the order "could not be found" when the agent has just seen it in a lookup.
Pattern: an injected tool outcome contradicts the scenario's Initial state or an earlier call's result. Any line that grades the agent's report of that outcome is then contradictory. Make the outcome consistent with the world: for example, OrderNotCancelled only when CO-A3 is called on an order that is not cancelled, or OrderNotFound with an Initial state where the order is gone when CO-A2 runs.
```

## M3 — KEPT — fixed

Severity: finder Important; final Important. Sources: faithfulness F3.

Verifier: M3 | Not real | Important | 'Final message must match the final refund status' (known failure case 3) and case 2's 'refund not issued' support 'has not been issued'; the late-landing call is not modelled; style choice between two truthful phrasings

Decision / fix: Kept against the verifier. I read the refutation and do not agree it refutes the finding: Round 3 Q3 is the user's specific instruction for exactly this branch ('failed or no refund, hand off and say the refund is not confirmed yet'); case 3's general line does not choose the wording, and the rubric grades the wording, so an agent using the user's words can fail the judge (the verifier itself flags this). Fixed: the branch now says 'the refund is not confirmed yet'; CO-S20 trajectory step 10 and note; new dimension 'Refund not confirmed reported' for CO-S20.

Finder text (faithfulness F3), verbatim:
```
F3 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20 Reference trajectory step 10; dimension "Refund not issued reported" as used by CO-S20
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md, Interview Round 3 Q3 (confirmed): "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet." Known failure case 3 adds: "state unknown; ... Final message must match the final refund status." The spec turns the user's hedged "not confirmed yet" into the definite claim "the refund has not been issued". The rubric in §5.2 ("tells the customer ... the refund has not been issued") then grades CO-S20 on that claim. An agent that says what the user specified ("the refund is not confirmed yet") can fail the judge. After two unanswered calls, "has not been issued" can also turn false if a call lands late.
Pattern: a customer-facing message the inputs specify is reworded into a different, stronger claim in a rule, failure row or rubric. Check every "tell the customer" clause against the input's wording for that case.
```

## M4 — KEPT — open

Severity: finder Nit; final Nit. Sources: faithfulness F4.

Verifier: Nit (not verified)

Decision / fix: Kept; the fix changes G-04's rule text, so it stops at the rule and is reported as a proposed rule change for the user (open). Before: 'After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).' Proposed after: 'After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or, for CO-A3 and CO-A4 only, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03).'

Finder text (faithfulness F4), verbatim:
```
F4 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 in Appendix B, from the user's tool-confirmation change 1, guarantees that cancellation is idempotent ("cancelling an order that is already cancelled returns it cancelled and changes nothing"). That is a guarantee that repeating creates nothing new, so G-04 as written would let the agent resend a timed-out cancel_order blindly. Interview Round 3 Q4 says "If the cancel call times out: no blind resend; re-read the order." CO-06 and the scenarios' Forbidden lines already require the lookup, so no verdict changes. G-04 also cites only SG-01, while the CO-A4 retry row relies on G-04 together with SG-03.
Pattern: a global rule's exception, read literally, licenses behavior that a stricter input-specified rule forbids for one action. The exception should name the actions it applies to (CO-A3 under SG-01, CO-A4 under SG-03) and exclude CO-A2.
```

## M5 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: faithfulness F5.

Verifier: Nit (not verified)

Decision / fix: Fixed: `failure_reason` and its enumerated values removed from Appendix A's CO-A3 outcomes cell.

Finder text (faithfulness F5), verbatim:
```
F5 | Lies | Nit | Appendix A, CO-A3 row "Outcomes, as tool results"
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: review-packet.md, Interview Round 2 Q3, defines the Refund fields as "refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued)", and the user's change adds only "Refund status: pending, issued, failed." No input defines a failure_reason field or its values. Round 3 Q3 names terminal causes but no field that carries them. The same row's return shape `{refund_id, amount, payment_method, status}` leaves out failure_reason and also the input's order number field. No grader reads failure_reason, so no verdict changes.
Pattern: a tool result field, or enumerated values, not in the confirmed data model. Remove it, or record it as a proposal to confirm.
```

## M6 — KEPT — fixed

Severity: finder Important; final Important. Sources: coverage F1.

Verifier: M6 | Real | Important | could not refute (no scenario meets 'changed ... in the confirming turn or after confirming'; a scripted turn is not a confirmation turn)

Decision / fix: Kept. CO-S03 row 4: Turn 2 'Yes, go ahead. Oh wait, no, I meant HG-10511, cancel that one instead.'; Unambiguity note explains the yes is voided under G-02 and is not a confirmation turn under §5.1.

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | G-02 / CO-04, Failure handling row "changed ... in the confirming turn or after confirming"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: This row changes the outcome, but no scenario's Initial state or User block triggers it. CO-S03 (agent-spec.md line 248) is the only scenario where the customer changes the proposal, and its Turn 2 is scripted "in place of a confirmation", so the customer changes the proposal before ever confirming. No scenario has a turn that confirms and changes at once (e.g. "Yes, but make it HG-10511") or a change after confirming. G-02's clause "Any change to a proposal term after confirmation voids that confirmation" (line 21) is therefore never exercised. §5.1 (line 1459), "If a trial has more than one confirmation turn ... is the first", shows the author expected this case. An agent that treats "Yes, but cancel HG-10511 instead" as authorization and cancels HG-10511 with no new confirmation passes every scenario.
Pattern: A failure row whose condition is a variant of a scenario's trigger (here: change after or with confirmation, versus the scenario's change before confirmation) is counted as covered by that scenario. Each row needs a scenario whose Initial state or User turns meet its condition literally.
```

## M7 — DROPPED — dropped

Severity: finder Important; final Important. Sources: coverage F2.

Verifier: M7 | Not real | Important | 'Refund status reported' (line 1507, 'states no other status for it', CO-S19) and the failure dimensions ('never says a refund is pending or issued') assert G-03's refund-status clause; the Gap class needs a telling rule with no scenario asserting it; CO-08 requires only the refund id, asserted by 'Refund id reported'; known failure case 3 maps to CO-S19..S21, not CO-S16

Decision / fix: Dropped. I read 'Refund status reported' (used by CO-S19) and the failure dimensions and agree: G-03's refund-status clause has scenarios asserting it, which takes the finding outside the Gap class; and case 3's retry-then-re-read path is CO-S19..S21.

Finder text (coverage F2), verbatim:
```
F2 | Gap | Important | G-03 / CO-08, success-path scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
Quote: "The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: On every success path, the only check on the agent's words is the code message check "Refund id reported" (§5.2 line 1497). The refund status the agent states is never checked. In all of these scenarios the refund is pending, and an agent that says "your refund has been issued" passes. The dimension "Refund status reported" (line 1507) exists but only CO-S19 uses it. Known failure case 3 in the packet (review-packet.md line 54: "Cancel succeeded, refund call timed out ... Final message must match the final refund status") is exactly CO-S16 rows 2 and 3, where the first refund call times out and the retry returns pending. Those rows assert only the refund id, so the known case's own pass condition goes untested there. The customer's interest "to be told truthfully ... where the refund stands" (§2 line 9) has no assertion on any success exit.
Pattern: A truthfulness rule is asserted by rubric only on failure exits. Every exit where the agent reports a status (pending or issued) needs a dimension that checks the stated status against the tool result.
```

## M8 — KEPT — fixed

Severity: finder Important; final Important. Sources: coverage F3.

Verifier: M8 | Real | Important | could not refute (Round 3 Q1 'promises nothing about when the money arrives' carried by no rule and no dimension)

Decision / fix: Kept. New rule CO-09 'No promised arrival date' [minimal guarantee] from Round 3 Q1; new rubric dimension 'No arrival date promised' used by CO-S01; CO-S01 Illustrates and Unambiguity note.

Finder text (coverage F3), verbatim:
```
F3 | Gap | Important | Scope & Authority "must not" / Contract (no rule)
Quote: "- promise a date by which the refunded money arrives."
Evidence: Round 2 Q2 (review-packet.md line 37) proposed "money arrives in 5 to 10 business days". Round 3 Q1 (line 61) replaced it with "The agent promises nothing about when the money arrives", and the user accepted ("Yes to all", line 66). The spec states this only in the must-not list (agent-spec.md line 49). No Contract rule (G-01..G-04, CO-01..CO-08) carries it, and no rubric dimension in §5.2 checks that no arrival date was promised. An agent that tells the customer "you'll see the money in 5 to 10 business days", the very figure in the interview, passes every scenario and misbehaves in production.
Pattern: A domain constraint confirmed in the interview appears only in Scope & Authority, with no rule and no scenario or dimension asserting it. Each must-not that the agent can break in words needs a rule and a dimension in at least one scenario, here the success scenarios.
```

## M9 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: coverage F6.

Verifier: Nit (not verified)

Decision / fix: Fixed: CO-S01 row 4 (unnamed request, one open order beside the delivered one; CO-02 added to Illustrates); CO-S05 row 4 (unnamed request, the only order delivered); the shipped and cancelled failure rows now read 'the order the customer asked about, or their only order when they named none'. A customer with no orders at all is not covered (no input).

Finder text (coverage F6), verbatim:
```
F6 | Gap | Nit | CO-02 / Failure handling (unnamed request)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: An unnamed request ("I want to cancel my order") is handled only when there is more than one open order (CO-S02). Two other cases are missing:
- (a) Acting side of the "asks only when" rule: no scenario has an unnamed request with exactly one placed/processing order (for example, beside a delivered one), where the agent should propose without asking. Every Turn 1 in CO-S01, CO-S05 to CO-S07 and CO-S09 to CO-S24 names the order number. evaluation-checklist.md, "Both directions are covered": "test only 'asks when unsure' and you get an agent that always asks."
- (b) Brainstorm item "the lookup returns ... none" (cockburn-checklist.md): no failure row covers an unnamed request when the customer has no open order, or no orders at all. The not-found, shipped and cancelled rows (agent-spec.md lines 91–93) all assume a named order.
Pattern: A rule keyed on a count (more than one open order) is specified and tested only for the branch that triggers it. The 1 and 0 branches each need a row or a scenario.
```

## M10 — KEPT — open

Severity: finder Nit; final Nit. Sources: coverage F7.

Verifier: Nit (not verified)

Decision / fix: Stands: what the agent says and whether it hands off when a lookup after an unanswered call no longer lists the order is not in the inputs; only the user can decide it (open question).

Finder text (coverage F7), verbatim:
```
F7 | Gap | Nit | Failure handling row "did not answer the first CO-A2"
Quote: "| CO-A2 | the order system did not answer the first CO-A2 | Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3. If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown. | G-04, CO-05, CO-06, CO-07 |"
Evidence: The row has no branch for a lookup that answers but no longer lists the order. `cancel_order` can report `OrderNotFound` for an order the agent has already seen (Appendix A line 1524; CO-S24), so the order can also be absent from a later `list_orders`. cockburn-checklist.md requires a lookup row to cover "nothing found". CO-05 and CO-06 still forbid a refund and a second cancel, but what the agent tells the customer, and whether it hands off, is left for a coder to invent.
Pattern: A lookup branch list omits the "record absent" result. Add it to every row that branches on a lookup (this row, and the "did not answer the second CO-A3" row at line 105).
```

## M11 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: coverage F8.

Verifier: Nit (not verified)

Decision / fix: Fixed: the four handoff dimensions ('Cancellation outcome unknown reported', 'Refund not issued reported', 'Refund not confirmed reported', 'Refund status unknown reported') now require 'store staff will follow up' only in text sent after the order system returned the follow-up task.

Finder text (coverage F8), verbatim:
```
F8 | Gap | Nit | CO-07 "once the order system has created the task" / CO-S22
Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
Evidence: The timing clause "once the order system has created the task" is asserted only in CO-S23, whose dimension forbids saying staff will follow up. In CO-S22 (line 1297) the first CO-A4 goes unanswered, and the dimension "Refund not issued reported" (line 1505) reads all agent text, including text sent alongside a tool call (§5.2 line 1493). It accepts "store staff will follow up" said alongside that first, unanswered CO-A4, before any task is known to exist. The same holds for text sent with the first CO-A4 in CO-S14, CO-S15, CO-S17, CO-S18, CO-S20 and CO-S21. In each of these the claim becomes true later in the trial, so no verdict changes in practice.
Pattern: A rule clause that orders a statement after an event is graded by a dimension that checks only whether the statement was made, not when. Either state the ordering in the dimension or drop the clause from the rule.
```

## M12 — KEPT — fixed

Severity: finder Important; final Important. Sources: verdicts F1.

Verifier: M12 | Real | Important | could not refute (CO-01/CO-02 'proposes nothing' asserted only by 'Orders unavailable reported'; simulated-user deflection hides a proposal from the action log)

Decision / fix: Kept. 'Shipped order explained', 'Already cancelled reported' and 'Order not found reported' now require no cancellation proposal of any order; CO-S05, CO-S06, CO-S07 and CO-S11 Unambiguity notes updated (CO-S07's action-log claim corrected).

Finder text (verdicts F1), verbatim:
```
F1 | Gap | Important | CO-S05, CO-S06, CO-S07 (§5.2 rubric dimensions "Shipped order explained", "Already cancelled reported", "Order not found reported")
Quote: "| Order not found reported | rubric | The agent tells the customer no order with the number they gave is on their account, and never says an order was cancelled or a refund issued. | CO-S07 |"
Evidence: CO-01 (agent-spec.md line 62) says "In both cases it proposes nothing for that order". CO-02 (line 65) says "proposes nothing for it". Scope & Authority must-not (line 46) says "guess which order the customer means, or turn an order number the customer gave into a different one". No line in CO-S05, CO-S06 or CO-S07 asserts that the agent proposes nothing. The three rubric definitions (lines 1498-1500) leave the proposal out. The Forbidden lines only ban CO-A2/A3/A4, and the simulated user deflects any proposal because none of these scenarios has a confirmation pair. So a wrong run passes every line. Example for CO-S07: the agent says HG-10428 is not on the account, then asks "Shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?", and the user deflects. This is the packet's known failure case 1, "Wrong order cancelled" (review-packet.md, round 2 Q4): in production a real customer would say yes to that proposal. The CO-S07 Unambiguity note (line 494) claims the action log catches this, but no confirmation can ever occur, so the log can only catch a cancellation made with no confirmation. Compare "Orders unavailable reported" (line 1503), which does include "proposes no cancellation".
Pattern: in a holding-back (infeasible) scenario, the rule's "proposes nothing" clause is asserted by no line. The rubric dimension checks only what was reported, and the simulated user's deflection hides any proposal from the action log. Add "proposes no cancellation (of that order or any other)" to every such dimension.
```

## M13 — KEPT — fixed

Severity: finder Important; final Important. Sources: verdicts F3.

Verifier: M13 | Real | Important | could not refute ('together they create' ties the refund to neither call; a lookup between the calls answers and its result is open)

Decision / fix: Kept. CO-S19, CO-S20 and CO-S21 Initial state now pin the first CO-A3 to create no refund and the second to create the row's refund (or none); CO-S16 row 2 (first unanswered CO-A3 created RF-5531, so a lookup before the retry would show it) dropped.

Finder text (verdicts F3), verbatim:
```
F3 | Ambiguous | Important | CO-S19, CO-S20, CO-S21 Initial state; CO-S16 row 2; Required events "CO-A3 occurs exactly twice"
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: "together they create" (CO-S19 line 1120, CO-S20 line 1177, CO-S21 line 1236) never says which call creates the refund. Lookups between the two CO-A3 calls do answer (CO-S21 line 1237 blocks only lookups after the second call), so a lookup there could show RF-5531 or show no refund, and the verdict depends on which. Different read-only lookups are a valid variation. In CO-S21 row 1, a lookup between the calls could show RF-5531 pending. An agent that then reports pending and stops is following CO-07 (line 80: hand off only when the refund "is not shown pending or issued") and G-03. Yet it fails "CO-A3 occurs exactly twice" (line 1249) and the required CO-A4 (line 1250). In CO-S20 row 1, a lookup showing the failed refund could lead the agent to hand off at once. Then Forbidden "CO-A4 before a CO-A1 made after the second CO-A3" (lines 1199 and 1259) refers to a second CO-A3 that never happened, and the line cannot be evaluated. CO-S16 row 2 (line 979) does fix the fact (the first call creates RF-5531), and it shows the same verdict split. CO-06 (line 77) says "at most two CO-A3", but the failure row (line 102) says "Make CO-A3 once more". So an agent that looks up, sees RF-5531 pending and stops gets the right outcome under the rule but fails Required line 962 "CO-A3 occurs exactly twice".
Pattern: a retry count is required ("exactly twice") while the world either leaves open what a lookup between the calls shows, or lets that lookup show the first call took effect. A rule-compliant agent that looks up between attempts then fails, and later Forbidden lines anchored on "the second" call become undefined. Pin which call takes effect in Initial state, and make the rules and failure row agree on whether the retry is mandatory or "at most". Or assert only "at most two" and leave the rest to the outcome.
```

## M14 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: verdicts F4.

Verifier: Nit (not verified)

Decision / fix: Fixed: CO-S19 Forbidden 'Fewer than one CO-A1 after the second CO-A3.' removed; the Unambiguity note names message check 'Refund id reported' as what catches a missing lookup.

Finder text (verdicts F4), verbatim:
```
F4 | Untestable | Nit | CO-S19 Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: evaluation-checklist.md says "Forbidden lines name events. Each Forbidden line is a tool call pattern ... or a timing violation" and "A tool call that only reads is never Required". This line names no event. It asserts that an event is absent, which makes a read-only lookup required in disguise, and it cannot become a "Then no <event> occurs" step without rewording. It changes no verdict: an agent that skips the lookup cannot learn RF-5531, so it already fails message check "Refund id reported" (line 1497), as the Unambiguity note (line 1164) says.
Pattern: a required read is written as a Forbidden "fewer than one" line. Drop it and let the outcome check (the message check on a value only the read reveals) carry the requirement.
```
