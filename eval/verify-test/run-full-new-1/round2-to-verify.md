# Round 2 findings to verify (Important only)

Each finding is quoted verbatim from the first finder in its Sources line. R2-L1 is a late round-1 finding (round-1 Codex verdicts finder, set B) folded into this round; it quotes the spec, not the bundle — grep the spec at /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/verify-test/run/agent-spec.md for CO-S19, CO-S20 and CO-S21.

## R2-01
Sources: coverage F1

R2-01 | Gap | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (with CO-S15)
Quote: "Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers or fails. ... If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: The R1-01 fix covers three branches of this row: cancelled (CO-S13 row 3), shipped (CO-S25) and placed/processing (CO-S26). The fourth branch, where the lookup does not answer and CO-A4 follows, has no scenario that makes the lookup. Only CO-S15 ends in a CO-A4 after the second unanswered CO-A2, and its reference trajectory skips the lookup the rewritten row now requires: "7. Agent → CO-A2 (HG-10482) → no answer." then "8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created." (rereview-r2.md lines 487-488, row at line 406). CO-S15's unambiguity note (line 495) asks only for no third cancellation, no refund and a handoff. Nothing in it fails a CO-A4 sent with no CO-A1 after the second CO-A2. CO-S17 (line 516) and CO-S27 (line 361) carry that kind of line for their own lookups. The input also requires the re-read before a handoff: round 3 Q4, review-packet.md line 64 ("Re-read fails, say outcome unknown, issue no refund, hand off").
Pattern: When a fix rewrites a failure row to require a lookup before an action, every existing scenario that reaches that row needs three updates: a reference trajectory with the lookup, an Initial-state line saying how the lookup answers, and a Forbidden line "CO-A4 before a CO-A1 made after the second CO-A2".

## R2-02
Sources: coverage F2

R2-02 | Gap | Important | CO-S26, Required events / Forbidden
Quote: "absent"
Evidence: CO-S26 requires only "CO-A2 occurs exactly twice" (line 291). Its Forbidden lines (lines 298-301) bar a third CO-A2, any CO-A3 and any CO-A4. No line requires a CO-A1 after the second unanswered CO-A2. Consider an agent that skips that lookup and tells the customer "the order was not cancelled". It passes every event line and the Final state, and the rubric "Cancellation not made reported" (line 393) only checks that the agent said not cancelled. Yet with no lookup the agent cannot know that. G-03 (line 610) and the rewritten row (line 406) both say that without the lookup it must report the outcome as unknown. CO-S19 already shows the right form: "Fewer than one CO-A1 after the second CO-A3." (line 1104). CO-S25 is protected only because a guessed message would not say "shipped".
Pattern: When the correct final message can be guessed without the required lookup, the scenario needs an event line that requires the lookup, such as "Fewer than one CO-A1 after the second CO-A2."

## R2-03
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

## R2-04
Sources: coverage F4

R2-04 | Gap | Important | failure: CO-A3 | the order system reported the order not cancelled (new)
Quote: "absent"
Evidence: This row has three outcomes. Two have scenarios: the lookup shows cancelled (CO-S17 row 3, unambiguity note at line 523) and the lookup does not answer (CO-S27, Initial state line 339). No scenario's Initial state makes the lookup after OrderNotCancelled answer with a status other than cancelled. That branch changes the outcome (CO-A4 with a different reason, a different message, and possibly a further CO-A2), so a scenario should trigger it.
Pattern: Each branch of a failure row that leads to a different action or message needs a scenario whose Initial state triggers that branch.

## R2-08
Sources: verdicts-codex F1

R2-08 | Gap | Important | CO-09; No arrival date promised
Quote: "The agent tells the customer no date and no length of time by which the refunded money arrives."
Evidence: The confirmed input says the agent "promises nothing about when the money arrives". The rule and rubric prohibit only dates and lengths of time. They therefore allow qualitative timing promises such as "soon" or "shortly". The rubric repeats the same narrowing at lines 387–389.
Pattern: A broad prohibition on timing promises was reduced to a prohibition on concrete dates and durations, leaving qualitative timing promises unprotected and untested.

## R2-09
Sources: verdicts-codex F3

R2-09 | Untestable | Important | Refund status reported
Quote: "| Refund status reported | rubric | The agent tells the customer the refund's status is the status the scenario's Final state assertions give the refund, and states no other status for it. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 |"
Evidence: The review criterion classifies a rubric dimension as untestable when a verbatim-value message check would suffice. Here the expected value is the literal refund-status enum in the confirmed model (pending, issued, or failed), so this can be a deterministic message check. Instances: CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19.
Pattern: A rubric grader is used to judge reporting of a literal enum value that can be checked directly in the message window.

## R2-L1
Sources: r1-B-verdicts-codex (late) F2

R2-L1 | Ambiguous | Important | CO-S19, CO-S20 and CO-S21, Initial state
Quote: "- The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: CO-S19 (line 1120), CO-S20 (line 1177) and CO-S21 (line 1236) all assign an aggregate effect to two timed-out refund calls without saying which call creates the refund. In CO-S21, only CO-A1 calls after the second CO-A3 are forced not to answer, so a valid extra lookup between the two calls has an undefined result: it may reveal the refund if the first call created it, or show no refund if the second creates it. This conflicts with the Unambiguity note's claim that the agent can see neither the refund nor its status, and it matters because the scenario's rubric requires "unknown" and forbids reporting pending, issued or failed.
Pattern: Effects of multiple timed-out writes are specified only in aggregate, leaving intermediate world state undefined; assign the effect of each timed-out call separately so optional intervening reads have one determined result.
