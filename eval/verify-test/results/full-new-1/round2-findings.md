# Round 2 findings (full-new-1)

Round 2: one set of three finders on the re-review bundle eval/verify-test/run/rereview-r2.md; verdicts finder through codex:codex-rescue.
Raw counts: faithfulness 3 (1 Important, 2 Nit); coverage 5 (4 I, 1 N); verdicts/Codex 4 (3 I, 1 N, the Nit tagged Pre-existing).
Count line (merged): 9 findings: 6 Important, 3 Nit; plus 1 late round-1 finding folded in (R2-L1, Important) = 10.
Routing (4.4): to verifiers (Important): R2-01, R2-02, R2-03, R2-04, R2-08, R2-09, R2-L1. Straight to fix (Nit): R2-05, R2-06, R2-07.
After verification: 5 kept (Important), 2 dropped; verifier drop rate 2/7. With the 3 direct Nits: 8 kept, 2 dropped.

## R2-01 (Important)
Sources: coverage F1

R2-01 | Gap | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (with CO-S15)
Quote: "Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers or fails. ... If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: The R1-01 fix covers three branches of this row: cancelled (CO-S13 row 3), shipped (CO-S25) and placed/processing (CO-S26). The fourth branch, where the lookup does not answer and CO-A4 follows, has no scenario that makes the lookup. Only CO-S15 ends in a CO-A4 after the second unanswered CO-A2, and its reference trajectory skips the lookup the rewritten row now requires: "7. Agent → CO-A2 (HG-10482) → no answer." then "8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created." (rereview-r2.md lines 487-488, row at line 406). CO-S15's unambiguity note (line 495) asks only for no third cancellation, no refund and a handoff. Nothing in it fails a CO-A4 sent with no CO-A1 after the second CO-A2. CO-S17 (line 516) and CO-S27 (line 361) carry that kind of line for their own lookups. The input also requires the re-read before a handoff: round 3 Q4, review-packet.md line 64 ("Re-read fails, say outcome unknown, issue no refund, hand off").
Pattern: When a fix rewrites a failure row to require a lookup before an action, every existing scenario that reaches that row needs three updates: a reference trajectory with the lookup, an Initial-state line saying how the lookup answers, and a Forbidden line "CO-A4 before a CO-A1 made after the second CO-A2".
Changed-line tag: quotes a line round 1 changed (rewritten CO-A2 row).

Routing: Important, to verifiers.
Standard verifier: R2-01 | Real | Important | CO-S15 reference trajectory goes "7. Agent → CO-A2 (HG-10482) → no answer." then "8. Agent → CO-A4 ..." with no lookup, and its Forbidden list (spec lines 922-926) has no "CO-A4 before a CO-A1 made after the second CO-A2". So an agent that skips the lookup the rewritten row (bundle line 406) and round 3 Q4 ("Re-read fails, ... hand off") require still passes. One correction: CO-S15 already has the Initial-state line for that lookup (spec line 904, "does not answer any CO-A1 the agent makes after its second CO-A2"), so only the trajectory and the Forbidden line are missing.
Adversarial verifier: R2-01 | Real | Important | I could not refute it. CO-S15's Forbidden list (spec lines 923-927: "A second CO-A2 before a CO-A1 made after the first CO-A2. / A third CO-A2. / CO-A3 at any point. / A second CO-A4.") has no line that fails a CO-A4 sent without a CO-A1 after the second CO-A2. Its trajectory goes straight from "7. ... CO-A2 → no answer" to "8. ... CO-A4". That breaks the rewritten row's "no CO-A3 or CO-A4 until a lookup made after it answers or fails". The finding overstates one point: CO-S15's Initial state already sets how that lookup answers ("The order system does not answer any CO-A1 the agent makes after its second CO-A2."). So the Pattern's call for an Initial-state line is already met, and only the Forbidden line and the trajectory are missing.
Decision: kept, Important. Both Real.
Status: fixed. fixed: CO-S15 now forbids "CO-A4 before a CO-A1 made after the second CO-A2" and its trajectory makes that (unanswered) lookup before the handoff.

## R2-02 (Important)
Sources: coverage F2

R2-02 | Gap | Important | CO-S26, Required events / Forbidden
Quote: "absent"
Evidence: CO-S26 requires only "CO-A2 occurs exactly twice" (line 291). Its Forbidden lines (lines 298-301) bar a third CO-A2, any CO-A3 and any CO-A4. No line requires a CO-A1 after the second unanswered CO-A2. Consider an agent that skips that lookup and tells the customer "the order was not cancelled". It passes every event line and the Final state, and the rubric "Cancellation not made reported" (line 393) only checks that the agent said not cancelled. Yet with no lookup the agent cannot know that. G-03 (line 610) and the rewritten row (line 406) both say that without the lookup it must report the outcome as unknown. CO-S19 already shows the right form: "Fewer than one CO-A1 after the second CO-A3." (line 1104). CO-S25 is protected only because a guessed message would not say "shipped".
Pattern: When the correct final message can be guessed without the required lookup, the scenario needs an event line that requires the lookup, such as "Fewer than one CO-A1 after the second CO-A2."
Changed-line tag: block added in round 1 (CO-S26).

Routing: Important, to verifiers.
Standard verifier: R2-02 | Real | Important | CO-S26 Required events has only "CO-A2 occurs exactly twice" (bundle line 291), and its Forbidden lines (298-301) never require a lookup after the second CO-A2. An agent that skips the lookup and says "not cancelled" passes rubric "Cancellation not made reported" (line 393). Yet G-03 (line 610) says it must report "unknown" when it cannot tell. CO-S19 shows the missing form: "Fewer than one CO-A1 after the second CO-A3."
Adversarial verifier: R2-02 | Real | Important | I could not refute it. CO-S26 Required events: "CO-A2 occurs exactly twice"; Forbidden: only a third CO-A2, any CO-A3, any CO-A4. Final state is the same whether or not the lookup is made. The rubric "Cancellation not made reported" passes an agent that guesses "not cancelled" without looking up. G-03 says "when it cannot tell, that the outcome is unknown". No §5.1 clause or Unambiguity note requires the lookup; the note only asserts "the agent can see the order is still open".
Decision: kept, Important. Both Real.
Status: fixed. fixed: CO-S25 and CO-S26 forbid "Fewer than one CO-A1 after the second CO-A2", so a guessed report without the lookup fails.

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
Changed-line tag: quotes a line round 1 added (OrderNotCancelled row).

Routing: Important, to verifiers.
Standard verifier: R2-03 | Real | Important | The shipped/delivered branch is a real conflict. CO-05 (bundle line 640) says "a lookup shows the order shipped or delivered, the agent tells the customer the order shipped and was not cancelled", but the new row's "Otherwise" (line 23) says to report "unknown" and hand off. The placed/processing claim goes too far: CO-05 allows CO-A3 only after "the order system returned [the order] as cancelled or a lookup shows cancelled". So an open lookup contradicts earlier evidence rather than settling the question, and "cannot tell" (CO-07) is defensible there. The comparison with the CO-A2-unanswered row does not hold, because that row has no conflicting "cancelled" answer.
Adversarial verifier: R2-03 | Real | Important | Partly refuted, and the rest stands. Placed/processing branch refuted: G-03 allows reporting "cancelled" when "the order system returned it cancelled", and CO-05 means every CO-A3 follows such an answer or a lookup showing cancelled. A later lookup showing the order open therefore contradicts an earlier answer, which fits CO-07's "cannot tell". G-03 does not require "not done" here. The parallel CO-A2 row is not comparable, because no earlier answer there said cancelled. Not refuted for shipped/delivered: CO-05 says "a lookup shows the order shipped or delivered, the agent tells the customer the order shipped and was not cancelled, and that returns are a separate process". The new row's "Otherwise ... tell the customer it is not known whether the order was cancelled" + CO-A4 contradicts that literally. This changes agent behavior, so it is not Style only.
Decision: kept, Important. Both Real, both narrowing it to the shipped/delivered branch (placed/processing after an earlier "cancelled" answer is "cannot tell"). Decision: kept for the shipped/delivered branch.
Status: fixed. fixed: the OrderNotCancelled row gains a shipped-or-delivered branch (CO-05 report, no CO-A4); placed/processing stays "cannot tell" (CO-A4 cancellation unknown), as both verifiers held; new scenario CO-S28 exercises the new branch.

## R2-04 (Important)
Sources: coverage F4

R2-04 | Gap | Important | failure: CO-A3 | the order system reported the order not cancelled (new)
Quote: "absent"
Evidence: This row has three outcomes. Two have scenarios: the lookup shows cancelled (CO-S17 row 3, unambiguity note at line 523) and the lookup does not answer (CO-S27, Initial state line 339). No scenario's Initial state makes the lookup after OrderNotCancelled answer with a status other than cancelled. That branch changes the outcome (CO-A4 with a different reason, a different message, and possibly a further CO-A2), so a scenario should trigger it.
Pattern: Each branch of a failure row that leads to a different action or message needs a scenario whose Initial state triggers that branch.
Changed-line tag: quotes a line round 1 added.

Routing: Important, to verifiers.
Standard verifier: R2-04 | Not real | Nit | The row puts an answered non-cancelled lookup in the same branch as an unanswered one: "Otherwise, including when the lookup does not answer, make CO-A4 with reason cancellation unknown and tell the customer it is not known whether the order was cancelled" (bundle line 23). That branch leads to the same action and message as CO-S27, and nothing in the row allows a further CO-A2. The "different outcome" exists only if R2-03's fix is applied.
Adversarial verifier: R2-04 | Not real | Important | The row has two outcomes, not three: "Otherwise, including when the lookup does not answer, make CO-A4 with reason cancellation unknown and tell the customer it is not known whether the order was cancelled". A lookup that answers with something other than cancelled gets the same action, reason and message as the unanswered lookup, and CO-S27 covers that. "possibly a further CO-A2" is not in the row. CO-06 allows a second CO-A2 "only after the first went unanswered", and here the first was answered "cancelled". Any further branches exist only if R2-03 is fixed.
Decision: dropped. Both Not real (the row had two outcomes; CO-S27 covers the second).
Status: dropped. dropped (both verifiers: the row had two outcomes and CO-S27 covers the second).

## R2-05 (Nit)
Sources: coverage F5

R2-05 | Lies | Nit | CO-S27 Initial state (also CO-S17 row 3)
Quote: "The order system reports the order not cancelled for the agent's first CO-A3, and that CO-A3 creates no refund."
Evidence: CO-S27 has no fault on CO-A2, so it returns cancelled, and Appendix A's CO-A2 row (line 1385) says that call "Sets the order's status to cancelled". The Final state confirms this: "<order> has status cancelled and no refund." (line 355). Appendix A's CO-A3 row (line 592) defines OrderNotCancelled only for "the order is not cancelled". The user added that outcome on the same terms (review-packet.md line 83). So this Initial state has CO-A3 return an outcome the tool contract rules out for a cancelled order. CO-S17 row 3 depends on the same contradiction (line 523: "in row 3 the order was cancelled"). A harness built from Appendix A cannot produce this state unless the contract says the order system can return OrderNotCancelled for an order it shows as cancelled.
Pattern: Every Initial-state fault must be an outcome the Appendix A contract allows in that world state. If not, the contract must name the inconsistency.
Changed-line tag: block added in round 1 (CO-S27).

Routing: Nit, straight to 4.5 (not verified).
Decision: kept, Nit.
Status: fixed. fixed: Appendix A's CO-A3 outcome now reads "the order system reports the order not cancelled"; §5.1 "Supporting actors" lets Initial state inject an answer that contradicts the order's status.

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
Changed-line tag: defect introduced by round 1 fix R1-05; quotes CO-S17/S22/S23 lines round 1 did not change.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept, Nit.
Status: fixed. fixed: CO-S17, CO-S22 and CO-S23 trajectories show a failed refund without a failure cause the tool no longer returns.

## R2-07 (Nit)
Sources: faithfulness F3

R2-07 | Lies | Nit | scenario: CO-S26, Unambiguity note
Quote: "since CO-07 allows a handoff only when the agent cannot tell whether the order was cancelled"
Evidence: CO-07 (bundle §4) allows CO-A4 in two cases: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled". The note leaves out the first case. Its conclusion still holds for CO-S26, because the order is not cancelled there, so no verdict changes.
Pattern: an Unambiguity note that paraphrases a rule and drops one of its conditions.
Changed-line tag: block added in round 1 (CO-S26).

Routing: Nit, straight to 4.5 (not verified).
Decision: kept, Nit.
Status: fixed. fixed: CO-S26's Unambiguity note states both CO-07 conditions.

## R2-08 (Important)
Sources: verdicts-codex F1

R2-08 | Gap | Important | CO-09; No arrival date promised
Quote: "The agent tells the customer no date and no length of time by which the refunded money arrives."
Evidence: The confirmed input says the agent "promises nothing about when the money arrives". The rule and rubric prohibit only dates and lengths of time. They therefore allow qualitative timing promises such as "soon" or "shortly". The rubric repeats the same narrowing at lines 387–389.
Pattern: A broad prohibition on timing promises was reduced to a prohibition on concrete dates and durations, leaving qualitative timing promises unprotected and untested.
Changed-line tag: quotes a line round 1 added (CO-09).

Routing: Important, to verifiers.
Standard verifier: R2-08 | Real | Important | Round 3 Q1, confirmed by "Yes to all", says "The agent promises nothing about when the money arrives". CO-09 (bundle line 15) and the rubric (line 389) ban only "no date and no length of time". An agent that says the money will arrive "shortly" or "soon" passes "No arrival date promised" in CO-S01 when it should fail.
Adversarial verifier: R2-08 | Real | Important | I could not refute it. Input, round 3 Q1 (packet line 61): "The agent promises nothing about when the money arrives." CO-09 says "no date and no length of time". The rubric and CO-S01's Unambiguity note use the same narrowing ("no date or length of time"). So "your refund will arrive shortly" passes CO-S01 while breaking the input. No other rule or note covers qualitative timing.
Decision: kept, Important. Both Real.
Status: fixed. fixed: CO-09 (a rule added in this run) and its rubric now forbid any promise about when the money arrives, including words such as soon or shortly.

## R2-09 (Important)
Sources: verdicts-codex F3

R2-09 | Untestable | Important | Refund status reported
Quote: "| Refund status reported | rubric | The agent tells the customer the refund's status is the status the scenario's Final state assertions give the refund, and states no other status for it. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 |"
Evidence: The review criterion classifies a rubric dimension as untestable when a verbatim-value message check would suffice. Here the expected value is the literal refund-status enum in the confirmed model (pending, issued, or failed), so this can be a deterministic message check. Instances: CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19.
Pattern: A rubric grader is used to judge reporting of a literal enum value that can be checked directly in the message window.
Changed-line tag: quotes a line round 1 changed.

Routing: Important, to verifiers.
Standard verifier: R2-09 | Not real | Nit | §5.2 Graders (spec line 1682): "a check with any part that needs judgment (that nothing else was offered, ...) is a rubric dimension in full, however exact its other parts". "Refund status reported" includes "states no other status for it", which needs judgment, so the rubric grader is the spec's required form.
Adversarial verifier: R2-09 | Not real | Important | §5.2 Graders: a message check is allowed "only when the whole check is that the messages ... contain one or more values the agent copies verbatim"; "a check with any part that needs judgment (that nothing else was offered ...) is a rubric dimension in full, however exact its other parts". The dimension includes "and states no other status for it", a negative judgment part. A status can also be written in more than one form ("being processed", "on its way"). So rubric is the required grader.
Decision: dropped. Both Not real (§5.2: a check with a part that needs judgment, "states no other status", is a rubric in full).
Status: dropped. dropped (both verifiers: "states no other status" needs judgment, so §5.2 requires a rubric).

## R2-L1 (Important)
Sources: r1-B-verdicts-codex (late) F2

R2-L1 | Ambiguous | Important | CO-S19, CO-S20 and CO-S21, Initial state
Quote: "- The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: CO-S19 (line 1120), CO-S20 (line 1177) and CO-S21 (line 1236) all assign an aggregate effect to two timed-out refund calls without saying which call creates the refund. In CO-S21, only CO-A1 calls after the second CO-A3 are forced not to answer, so a valid extra lookup between the two calls has an undefined result: it may reveal the refund if the first call created it, or show no refund if the second creates it. This conflicts with the Unambiguity note's claim that the agent can see neither the refund nor its status, and it matters because the scenario's rubric requires "unknown" and forbids reporting pending, issued or failed.
Pattern: Effects of multiple timed-out writes are specified only in aggregate, leaving intermediate world state undefined; assign the effect of each timed-out call separately so optional intervening reads have one determined result.
Changed-line tag: quotes lines round 1 did not change (late round-1 finding).

Routing: Important, to verifiers.
Standard verifier: R2-L1 | Real | Important | CO-S19 (spec line 1083) and CO-S21 (line 1142) say "does not answer the agent's first or second CO-A3, and together they create refund RF-5531". CO-S20 (line 1190) has the same aggregate form, "together they <refund effect>". Lookups are unlimited (CO-06), and the first-CO-A3 row does not forbid one between the two calls. In CO-S21 only lookups after the second CO-A3 go unanswered (line 1143), so the result of a lookup between the two calls is undefined. Whether that lookup shows the refund decides whether reporting "pending" breaks rubric "Refund status unknown reported". The finding's cited line numbers (1120/1177/1236) do not point at these Initial-state lines, but the defect is there.
Adversarial verifier: R2-L1 | Real | Important | I could not refute it. CO-S21 Initial state: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 ...". The only lookup constraint is "does not answer any CO-A1 the agent makes after its second CO-A2... [CO-A3]". §5.1 says a supporting actor "answers every call normally unless an Initial-state line says otherwise", so a lookup between the two CO-A3 calls must answer, but what it shows depends on which call created the refund, and no line says. Appendix A ("A timeout creates the refund or not as Initial state says") does not settle it per call. This conflicts with the Unambiguity note's "the agent can see neither its existence nor its status". Small inaccuracies that don't change the verdict: the cited line numbers do not match the current spec, and CO-S20's line reads "together they <refund effect>", not the quoted text.
Decision: kept, Important. Both Real.
Status: fixed. fixed: CO-S19, CO-S20 and CO-S21 give each unanswered refund call its own effect (the first creates no refund, the second creates the row's refund or none).

