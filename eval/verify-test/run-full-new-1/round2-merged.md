# Round 2 merged findings

## R2-01 (Important)
Sources: coverage F1

R2-01 | Gap | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (with CO-S15)
Quote: "Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers or fails. ... If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: The R1-01 fix covers three branches of this row: cancelled (CO-S13 row 3), shipped (CO-S25) and placed/processing (CO-S26). The fourth branch, where the lookup does not answer and CO-A4 follows, has no scenario that makes the lookup. Only CO-S15 ends in a CO-A4 after the second unanswered CO-A2, and its reference trajectory skips the lookup the rewritten row now requires: "7. Agent → CO-A2 (HG-10482) → no answer." then "8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created." (rereview-r2.md lines 487-488, row at line 406). CO-S15's unambiguity note (line 495) asks only for no third cancellation, no refund and a handoff. Nothing in it fails a CO-A4 sent with no CO-A1 after the second CO-A2. CO-S17 (line 516) and CO-S27 (line 361) carry that kind of line for their own lookups. The input also requires the re-read before a handoff: round 3 Q4, review-packet.md line 64 ("Re-read fails, say outcome unknown, issue no refund, hand off").
Pattern: When a fix rewrites a failure row to require a lookup before an action, every existing scenario that reaches that row needs three updates: a reference trajectory with the lookup, an Initial-state line saying how the lookup answers, and a Forbidden line "CO-A4 before a CO-A1 made after the second CO-A2".

## R2-02 (Important)
Sources: coverage F2

R2-02 | Gap | Important | CO-S26, Required events / Forbidden
Quote: "absent"
Evidence: CO-S26 requires only "CO-A2 occurs exactly twice" (line 291). Its Forbidden lines (lines 298-301) bar a third CO-A2, any CO-A3 and any CO-A4. No line requires a CO-A1 after the second unanswered CO-A2. Consider an agent that skips that lookup and tells the customer "the order was not cancelled". It passes every event line and the Final state, and the rubric "Cancellation not made reported" (line 393) only checks that the agent said not cancelled. Yet with no lookup the agent cannot know that. G-03 (line 610) and the rewritten row (line 406) both say that without the lookup it must report the outcome as unknown. CO-S19 already shows the right form: "Fewer than one CO-A1 after the second CO-A3." (line 1104). CO-S25 is protected only because a guessed message would not say "shipped".
Pattern: When the correct final message can be guessed without the required lookup, the scenario needs an event line that requires the lookup, such as "Fewer than one CO-A1 after the second CO-A2."

## R2-03 (Important)
Sources: faithfulness F1, coverage F3, verdicts-codex F2

R2-03 | Lies | Important | failure: CO-A3 | the order system reported the order not cancelled (new)
Quote: "Otherwise, including when the lookup does not answer, make CO-A4 with reason cancellation unknown and tell the customer it is not known whether the order was cancelled and store staff will follow up."
Evidence: "Otherwise" also covers a lookup that answers and shows the order placed, processing, shipped or delivered. In each of those cases the agent can tell the order was not cancelled, and the spec's own lines say what to do then:
- CO-05 (bundle §4): "a lookup shows the order shipped or delivered, the agent tells the customer the order shipped and was not cancelled, and that returns are a separate process."
- G-03 (bundle §4): "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown."
- CO-07 (bundle §4) allows CO-A4 only "when the agent cannot tell whether the order was cancelled" (or the order is cancelled and the refund is not shown), and says "CO-A4 occurs in no other situation."
- The parallel row rewritten in the same round, "CO-A2 | the order system did not answer the second CO-A2" (bundle §3), handles these same lookup results as known: placed or processing means "tell the customer the order was not cancelled ... no CO-A4", and shipped or delivered means the shipped explanation with no CO-A4.
The new row tells the agent to report "unknown" and hand off when its lookup has answered the question. That breaks G-03, CO-05 and CO-07. This is the R1-02 fix, and the fix is wrong for these branches. No scenario covers them: CO-S17 row 3's lookup shows cancelled, and CO-S27's lookup goes unanswered. So the defect would show up in production, not in a verdict.
Pattern: a failure row whose catch-all "Otherwise" groups lookup results the agent can read (the order is open, or the order shipped) with "the lookup did not answer". Each answered lookup result should get its own branch, matching G-03, CO-05 and CO-07.

## R2-04 (Important)
Sources: coverage F4

R2-04 | Gap | Important | failure: CO-A3 | the order system reported the order not cancelled (new)
Quote: "absent"
Evidence: This row has three outcomes. Two have scenarios: the lookup shows cancelled (CO-S17 row 3, unambiguity note at line 523) and the lookup does not answer (CO-S27, Initial state line 339). No scenario's Initial state makes the lookup after OrderNotCancelled answer with a status other than cancelled. That branch changes the outcome (CO-A4 with a different reason, a different message, and possibly a further CO-A2), so a scenario should trigger it.
Pattern: Each branch of a failure row that leads to a different action or message needs a scenario whose Initial state triggers that branch.

## R2-05 (Nit)
Sources: coverage F5

R2-05 | Lies | Nit | CO-S27 Initial state (also CO-S17 row 3)
Quote: "The order system reports the order not cancelled for the agent's first CO-A3, and that CO-A3 creates no refund."
Evidence: CO-S27 has no fault on CO-A2, so it returns cancelled, and Appendix A's CO-A2 row (line 1385) says that call "Sets the order's status to cancelled". The Final state confirms this: "<order> has status cancelled and no refund." (line 355). Appendix A's CO-A3 row (line 592) defines OrderNotCancelled only for "the order is not cancelled". The user added that outcome on the same terms (review-packet.md line 83). So this Initial state has CO-A3 return an outcome the tool contract rules out for a cancelled order. CO-S17 row 3 depends on the same contradiction (line 523: "in row 3 the order was cancelled"). A harness built from Appendix A cannot produce this state unless the contract says the order system can return OrderNotCancelled for an order it shows as cancelled.
Pattern: Every Initial-state fault must be an outcome the Appendix A contract allows in that world state. If not, the contract must name the inconsistency.

## R2-06 (Nit)
Sources: faithfulness F2, verdicts-codex F4

R2-06 | Lies | Nit | scenario: CO-S17, Reference trajectory step 6 (same line in CO-S22 and CO-S23)
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: The edited Appendix A row "CO-A3 issue the refund" (bundle §3) dropped `failure_reason`. A failed refund now returns only `{refund_id, amount, payment_method, status: "failed"}`, so no tool result can say "card closed". The R1-05 fix was not carried into the trajectories:
- CO-S17 step 6 (an in-scope block; the line is outside the hunk).
- CO-S22 step 6 (bundle §4).
- CO-S23 step 6 (bundle §4). CO-S23's Data variants also vary only `failure reason` ("the card has been closed" / "the card has expired"), and the agent can no longer observe that value.
The Initial state wording "with status failed because ..." describes the world and can stay. The tool-result text in the trajectories is what the edited tool cannot produce.
Pattern: when a field is removed from a tool's outcome, every reference-trajectory tool result that showed the field still shows it.

## R2-07 (Nit)
Sources: faithfulness F3

R2-07 | Lies | Nit | scenario: CO-S26, Unambiguity note
Quote: "since CO-07 allows a handoff only when the agent cannot tell whether the order was cancelled"
Evidence: CO-07 (bundle §4) allows CO-A4 in two cases: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled". The note leaves out the first case. Its conclusion still holds for CO-S26, because the order is not cancelled there, so no verdict changes.
Pattern: an Unambiguity note that paraphrases a rule and drops one of its conditions.

## R2-08 (Important)
Sources: verdicts-codex F1

R2-08 | Gap | Important | CO-09; No arrival date promised
Quote: "The agent tells the customer no date and no length of time by which the refunded money arrives."
Evidence: The confirmed input says the agent "promises nothing about when the money arrives". The rule and rubric prohibit only dates and lengths of time. They therefore allow qualitative timing promises such as "soon" or "shortly". The rubric repeats the same narrowing at lines 387–389.
Pattern: A broad prohibition on timing promises was reduced to a prohibition on concrete dates and durations, leaving qualitative timing promises unprotected and untested.

## R2-09 (Important)
Sources: verdicts-codex F3

R2-09 | Untestable | Important | Refund status reported
Quote: "| Refund status reported | rubric | The agent tells the customer the refund's status is the status the scenario's Final state assertions give the refund, and states no other status for it. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 |"
Evidence: The review criterion classifies a rubric dimension as untestable when a verbatim-value message check would suffice. Here the expected value is the literal refund-status enum in the confirmed model (pending, issued, or failed), so this can be a deterministic message check. Instances: CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19.
Pattern: A rubric grader is used to judge reporting of a literal enum value that can be checked directly in the message window.

## R2-L1 (Important)
Sources: r1-B-verdicts-codex (late) F2

R2-L1 | Ambiguous | Important | CO-S19, CO-S20 and CO-S21, Initial state
Quote: "- The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: CO-S19 (line 1120), CO-S20 (line 1177) and CO-S21 (line 1236) all assign an aggregate effect to two timed-out refund calls without saying which call creates the refund. In CO-S21, only CO-A1 calls after the second CO-A3 are forced not to answer, so a valid extra lookup between the two calls has an undefined result: it may reveal the refund if the first call created it, or show no refund if the second creates it. This conflicts with the Unambiguity note's claim that the agent can see neither the refund nor its status, and it matters because the scenario's rubric requires "unknown" and forbids reporting pending, issued or failed.
Pattern: Effects of multiple timed-out writes are specified only in aggregate, leaving intermediate world state undefined; assign the effect of each timed-out call separately so optional intervening reads have one determined result.
