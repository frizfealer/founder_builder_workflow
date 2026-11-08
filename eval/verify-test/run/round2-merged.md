# Round 2 merged findings

## R2-01 (Important)
Sources: faithfulness F1

R2-01 | Lies | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (section 3)
Quote: "Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers. ... If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: The row's first sentence says no CO-A4 until a lookup *answers*. Its last branch then requires CO-A4 when the lookup does *not* answer. The row contradicts itself. CO-S15 (section 2) sets Initial state "The order system does not answer any CO-A1 the agent makes after its second CO-A2", so under the opening clause no lookup ever answers and CO-A4 is never allowed. Yet CO-S15 Required events demand "CO-A4 occurs exactly once, for <order>, reason cancellation unknown, after the second CO-A2", and its Forbidden line uses a different condition: "CO-A4 before a CO-A1 *made* after the second CO-A2", not one that *answers*. Reads may be retried without limit (review-packet.md, tool confirmation turn, change 4). So an agent that follows the opening clause can keep retrying the lookup and never hand off, and it fails CO-S15. The first-CO-A2 row (section 4) says "Make no CO-A2 or CO-A3 until a lookup made after it answers". It leaves CO-A4 out of that clause, so it is consistent. The fix round added "or CO-A4" to the new row and broke that.
Pattern: A "no X until a lookup answers" gate also lists an action that a later branch requires when the lookup does not answer. Gate on "until a lookup has been made after it", matching the Forbidden lines, or take CO-A4 out of the gate.

## R2-02 (Important)
Sources: coverage F1

R2-02 | Gap | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (placed-or-processing branch); CO-S27
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 or CO-A4."
Evidence: product-idea.md lines 5-6 ("A customer should be able to ... cancel an order they placed and get their money back"). The order is still cancellable, but the agent cannot cancel it in this conversation: CO-06 (bundle §4) allows "at most two CO-A2 ... in a conversation", and CO-07 says "CO-A4 occurs in no other situation". So no rule gives the customer a next step. The dimension "Cancellation not made reported" (bundle §2) even forbids saying staff will follow up. Compare the CO-A4 second-unanswered row (bundle §4), which tells the customer "to contact Harbor Goods customer support" once retries run out. The interview never decides this case: round 3 Q4 covers only the first unanswered cancel (review-packet.md, Round 3). In CO-S27 the agent passes by saying "not cancelled" and stopping, while the customer's open order goes on to ship.
Pattern: when the retry budget is spent and the order can still be cancelled, the customer's goal is left unmet and no rule says what next step the agent offers (try again later, contact support, or a handoff).

## R2-L2 (Important)
Sources: r1-verdicts-codex (late) F2

R2-L2 | Ambiguous | Important | CO-S01–CO-S24, Initial state and Final state assertions  
Quote: "- No follow-up task exists."  
Evidence: Every scenario asserts either zero or exactly one follow-up task: CO-S01:141, CO-S02:201, CO-S03:263, CO-S04:320, CO-S05:372, CO-S06:422, CO-S07:471, CO-S08:521, CO-S09:576, CO-S10:630, CO-S11:680, CO-S12:735, CO-S13:792, CO-S14:850, CO-S15:908, CO-S16:967, CO-S17:1025, CO-S18:1081, CO-S19:1137, CO-S20:1195, CO-S21:1255, CO-S22:1316, CO-S23:1375, and CO-S24:1429. No scenario supplies a pre-conversation follow-up-task baseline; the only Initial-state task references describe effects of later CO-A4 calls. The checklist requires every fact on which the verdict depends to have a concrete Initial-state value. Thus a pre-existing task can make the same trajectory pass or fail, and "No follow-up task exists" can also be read globally or as limited to the scenario order.  
Pattern: A final record-count assertion has no corresponding initial full-set baseline and no stated scope.

## R2-L3 (Important)
Sources: r1-verdicts-codex (late) F3

R2-L3 | Untestable | Important | CO-S03 and CO-S04, User  
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""  
Evidence: The same trigger appears in CO-S03:248 and CO-S04:308. Section 5.1 defines a confirmation question more narrowly as one stating every proposal value; it does not define the looser event "a question that proposes cancelling … and asks to go ahead." The checklist requires a scripted User turn to be anchored to a defined §5.1 event, not merely a proposal or offer. A partial question such as asking only whether to cancel HG-10482 could therefore trigger Turn 2 under one conversion but not another.  
Pattern: A scripted User turn is anchored to an informal message description instead of a defined harness event.

Sources (commands Codex ran, all read-only):
- Spec lines 17-21, 56-72, 238-252, 300-311, 1457-1465 in /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/verify-test/run/agent-spec.md
- rg for follow-up-task assertions over the same spec
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/evaluation-checklist.md lines 34-41

## R2-03 (Nit)
Sources: faithfulness F2, coverage F4

R2-03 | Lies | Nit | CO-S26, Initial state / Data variants row 2
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's second CO-A2 reaches the order system, and status <final status> from that moment on" with row "| 2 | delivered |"
Evidence: Row 2 has the order jump from processing straight to delivered, mid-conversation, at the moment of a cancel call. The only race the inputs describe is "status can flip processing → shipped between the agent's read and its cancel call" (review-packet.md, Round 2 user answer, Q1). The status list is placed, processing, shipped, delivered, cancelled. Nothing supports an instant processing-to-delivered change that skips shipped. CO-S11 uses only shipped for the same race. The verdict does not change, because shipped and delivered are handled the same way.
Pattern: A data-variant row invents a domain transition that the inputs' state model does not allow.

## R2-04 (Nit)
Sources: faithfulness F3, coverage F5

R2-04 | Lies | Nit | row: CO-A3 issue the refund (Appendix A, section 3): the R1-09 fix is incomplete
Quote: "refund failed: returns the refund with `status: \"failed\"`; payment provider temporarily unavailable: `ProviderUnavailable`"
Evidence: The fix took `failure_reason` out of CO-A3's result. The refund record now has only refund id, order number, amount, payment method and status (review-packet.md, Round 2 Q3 and the user's changes). But three reference trajectories still show the tool returning a failure reason. CO-S17 step 6: "Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed." CO-S22 step 6 and CO-S23 step 6 say the same: "refund RF-5531, failed, card closed". CO-A3 can no longer produce that result. A side effect: CO-S17 rows 1 and 2, and CO-S23 rows 1 and 2, now differ only in a cause the agent cannot observe.
Pattern: When a field is removed from a tool's result, some reference trajectories still show that field in the tool's result.

## R2-05 (Nit)
Sources: faithfulness F4

R2-05 | Ambiguous | Nit | failure: CO-A2 | the order system did not answer the second CO-A2 (section 3), lookup-does-not-answer branch
Quote: "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: The row lists telling the customer "store staff will follow up" before making CO-A4. CO-07 says the agent "tells the customer store staff will follow up once the order system has created the task". The CO-A4 double-timeout row says that if CO-A4 goes unanswered twice, the agent tells the customer "it could not confirm store staff were told, and to contact Harbor Goods customer support". Read in order, this row lets the agent promise follow-up before the task exists, which conflicts with CO-07 and G-03. The two new CO-A3 rows in section 2 list CO-A4 first and the message second, so the spec orders these steps inconsistently. Instances: this row, plus the first-CO-A2 row (section 4, pre-existing, same wording).
Pattern: A failure-row action list puts the "staff will follow up" message ahead of the CO-A4 it depends on.

Pre-existing: failure row "CO-A2 | the order system did not answer the first CO-A2" (section 4) has the same message-before-CO-A4 ordering as F4.

## R2-06 (Nit)
Sources: coverage F2

R2-06 | Gap | Nit | failure: any | the customer named no order, and none of their orders has status placed or processing; CO-S05 row 4
Quote: "Tell the customer, for each of their orders, what CO-01 says for its status; propose nothing."
Evidence: the only scenario that triggers this row is CO-S05 row 4. There the customer has one order, HG-10466, status delivered, and "The customer has no other orders" (spec CO-S05 Initial state). No scenario gives a customer several non-open orders, or an order with status cancelled, under this row. So the "for each of their orders" clause and the cancelled branch of CO-01 ("tells the customer the order is already cancelled") are never asserted here. An agent that reports only one of several orders would pass.
Pattern: a per-item telling clause exercised only with a single item and a single status.

## R2-07 (Nit)
Sources: coverage F3

R2-07 | Gap | Nit | failure: any | the customer named no order, and none of their orders has status placed or processing
Quote: "the customer named no order, and none of their orders has status placed or processing"
Evidence: a signed-in customer with no orders at all meets this condition (vacuously). The row's action, "for each of their orders, what CO-01 says", then produces no message. No rule says what the agent tells a customer who has no orders (CO-01, bundle §4, speaks only of orders with a status), and no scenario covers it.
Pattern: a condition that also matches the empty set, with an action defined only over its members.
