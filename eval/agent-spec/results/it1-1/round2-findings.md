# Round 2 merged findings

11 findings: 9 Important, 2 Nit.

Severity as the finders gave it; status is fixed / answered / open / dropped / Pre-existing (none were Pre-existing: whole-spec scope).

## N1 — KEPT — fixed

Severity: finder Important; final Important. Sources: faithfulness F1.

Verifier: Real | Important | could not refute (input round 3 Q3: "say the refund is not confirmed yet")

Decision / fix: Row wording and new dimension "Refund not confirmed reported" for CO-S20.

Attribution: quotes a line round 1 did not change.

Finder text (faithfulness F1), verbatim:
```
F1 | Lies | Important | CO-07; §4.1 Failure handling, CO-A3 rows "did not answer the second CO-A3" and "returned the refund with status failed, or reported the order not cancelled"; CO-S20; dimension "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md Round 3 Q3 (the user answered "Yes to all"): "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet". Known failure case 3 (Round 2 Q4) also treats the timeout path as one where the state is unknown. The spec gives the agent a different message, "the refund has not been issued", which is the wording for the known-terminal case 2. CO-S20 then holds the agent to that wording through rubric dimension "Refund not issued reported" (§5.2 table: "the refund has not been issued … and never says a refund is pending or issued"). An agent that says what the user approved ("your refund is not confirmed yet; store staff will follow up") may fail CO-S20 rows 1 and 2. In row 2 the spec's sentence is also a stronger claim than the agent can see: two calls went unanswered, so "not issued" asserts more than the user approved.
Pattern: The agent's report on the timeout→re-read path should use the input's wording ("not confirmed yet"). It must not reuse the terminal-error wording. Fix the failure row and CO-S20's rubric dimension, or give CO-S20 its own dimension.
```

## N2 — KEPT — open

Severity: finder Important; final Nit. Sources: faithfulness F2, coverage F3.

Verifier: Real | Nit | could not refute; graded Nit because the outcome is reachable only if the order system contradicts its earlier CO-A2 answer

Decision / fix: Row split; the agent says the order is cancelled only if a later lookup shows it. Handling and a scenario remain an open question.

Attribution: quotes a line round 1 did not change.

Finder text (faithfulness F2), verbatim:
```
F2 | Lies | Important | §4.1 Failure handling, CO-A3 row "returned the refund with status failed, or reported the order not cancelled"; CO-06
Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |"
Evidence: The inputs give only the outcome "issue_refund adds outcome OrderNotCancelled" (review-packet.md, Tool confirmation turn, change 2). They say nothing about what the agent does or tells the customer when it gets that outcome. answered.md M1 says: "What the agent does on OrderNotCancelled after a cancelled result is left as an open question for the user." Even so, this row still prescribes the behavior: no retry, handoff reason refund_not_issued, and the message "the order is cancelled". That message contradicts the tool result the agent just got, which says the order is not cancelled. CO-06 ("never after … reported the order not cancelled") also turns the unanswered question into a rule. This is not the M1 issue again: that fix removed the scenario but kept the invented behavior in the row and the rule.
Pattern: When a question is left open for the user, the rule or failure row for it must not prescribe an answer. Mark OrderNotCancelled as open in the row and in CO-06. At minimum, do not tell the customer "the order is cancelled" right after the order system has reported it not cancelled.
```

Finder text (coverage F3), verbatim:
```
F3 | Gap | Nit | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |"
Evidence: The user added the OrderNotCancelled outcome to issue_refund (packet, tool confirmation change 2), and Appendix A lists it ("the order is not cancelled: `OrderNotCancelled`"). Since CO-S17 row 3 was removed (answered.md M1), no scenario triggers it. The CO-S17 rows, CO-S20 row 1, CO-S22 and CO-S23 all trigger only the "status failed" half of this row. For the OrderNotCancelled half, the row also has the agent tell the customer "the order is cancelled" right after the order system said it is not, which G-03 forbids. answered.md M1 leaves this behavior as an open question for the user, so the row is untested, and in that half it contradicts G-03. Graded Nit because the current scenarios can only reach the outcome if the order system contradicts its own earlier answer.
Pattern: A tool outcome the user named, with a failure row and no scenario, kept in a row merged with an outcome that needs different handling.
```

## N3 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: faithfulness F3, verdicts F6.

Verifier: Nit (not verified)

Decision / fix: ", card closed" removed from three trajectories.

Attribution: quotes a line round 1 did not change.

Finder text (faithfulness F3), verbatim:
```
F3 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A, CO-A3 row: `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}`. The result has no field for why a refund failed: answered.md M3 removed `failure_reason`, and the inputs' refund data model (Round 2 Q3 and its changes) has none. So no tool result can contain "card closed", and the agent cannot see the cause that the Initial state gives ("because the card has been closed", "because <failure reason>"). Instances: CO-S17 step 6, CO-S22 step 6, CO-S23 step 6.
Pattern: A reference trajectory's tool results show only fields that Appendix A's return shape carries. Drop "card closed" from those three results.
```

Finder text (verdicts F6), verbatim:
```
F6 | Untestable | Nit | CO-S17 Initial state and Data variants; CO-S22 Initial state; CO-S23 Initial state and Data variants; their Reference trajectories, step 6
Quote: "creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has been closed"
Evidence: Appendix A's CO-A3 row returns `{refund_id, amount, payment_method, status}`. The only result for this outcome is "refund failed: returns the refund with `status: \"failed\"`", and the failure_reason field was removed (answered.md, M3). The harness has no way to carry "because the card has been closed / expired / the provider declined", so the Given cannot be built as written. CO-S17 rows 1 and 2, and CO-S23 rows 1 and 2, give the agent identical tool results. The Reference trajectories show a result the tool cannot return: "refund RF-5531, failed, card closed".
Pattern: An Initial-state fact or a reference tool result goes beyond what Appendix A lets the tool return. Remove the cause, or make the rows differ in something the agent can see.
```

## N4 — DROPPED — dropped

Severity: finder Important; final Important. Sources: verdicts F1.

Verifier: Not real | Important | failure row "the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01." and input case 3 "agent retries once"

Decision / fix: Dropped: I read the row and the input; the retry is required, so "exactly twice" is the contract.

Finder text (verdicts F1), verbatim:
```
F1 | Ambiguous | Important | CO-S16, Required events (row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (CO-S16 Data variants row 2). Take an agent that, after that timeout, makes a CO-A1 (lookups are unlimited, CO-06 and Appendix A). The lookup shows RF-5531 pending. The agent then tells the customer the order is cancelled and RF-5531 is pending. G-03 allows that report ("or a lookup shows it"). CO-06 only allows a second call: "It makes a second CO-A3 only after the first … went unanswered". The world ends in exactly the Final state assertions. This run makes one CO-A3, so it fails "exactly twice". The CO-A3 failure row ("did not answer it | Make CO-A3 once more") says to retry, while G-03 and CO-06 accept the lookup-and-report path. Two experts could give this trajectory opposite verdicts. evaluation-checklist.md, "Outcome, not path": "agents find valid paths the author did not anticipate, and a path assertion punishes them."
Pattern: An exact retry count is Required in a row where a read-only lookup after the unanswered call already shows the call took effect, so a valid lookup-then-report path fails. Either require the retry only in rows where nothing is created (rows 1 and 3), or say outright that the retry is required even when a lookup shows the refund.
```

## N5 — KEPT — fixed

Severity: finder Important; final Important. Sources: verdicts F2.

Verifier: Real | Important | could not refute (nothing defines stating a proposal; Scope allows listing orders with refunds)

Decision / fix: "Order choice asked" and "Order not found reported" definitions now say what counts as an offer.

Attribution: quotes a line round 1 changed.

Finder text (verdicts F2), verbatim:
```
F2 | Ambiguous | Important | "propose"/"states a proposal" at message level: CO-01, CO-02, CO-S02 dimension "Order choice asked", CO-S08 failure row, CO-S10 dimension
Quote: "Before any agent message that states a proposal, the agent asks which of the customer's open orders they mean, and it states no proposal for any order before the customer's answer names one."
Evidence: §5.1 defines the confirmation question, but nowhere does the spec define what counts as "stating a proposal" or "proposing" in a message. Scope & Authority allows the agent to "tell the customer which of their orders can be cancelled and what the refund would be". So a which-order question like "HG-10482 ($86.40 back to Visa ending 4242) or HG-10511 ($23.75 back to Mastercard ending 8810) — which one?" is allowed by Scope, yet one judge could read it as stating two proposals under "Order choice asked". Other instances:
(a) CO-S08 failure row: "propose nothing until the customer asks to cancel the whole order". The CO-S08 Reference trajectory step 3 itself "asks whether they want to cancel the whole order", so it is unclear whether that offer is a proposal.
(b) CO-S07: an agent that answers "No HG-10428 on your account — did you mean HG-10482? Shall I cancel it and refund $86.40 to Visa ending 4242?" breaks "must not … guess which order the customer means, or turn an order number the customer gave into a different one". But "Order not found reported" only forbids saying an order was cancelled, and CO-02 forbids a proposal only "for it" (the number the customer gave), so whether this passes is a judgment call.
(c) CO-S10 dimension "Orders unavailable reported": "proposes no cancellation".
Pattern: A message-level verdict depends on an undefined term ("proposal"/"propose"). Define it in §5.1 (for example, a message naming an order number together with a refund amount or payment method and offering to cancel), or say which offers and listings are allowed, so judges agree.
```

## N6 — KEPT — fixed

Severity: finder Important; final Important. Sources: verdicts F3.

Verifier: Real | Important | could not refute (no row requires saying "no refund was issued")

Decision / fix: Clause removed from the dimension (notes aligned in round 3).

Attribution: quotes a line round 1 did not change.

Finder text (verdicts F3), verbatim:
```
F3 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows this dimension grades require less:
- CO-A2 "did not answer the first CO-A2": "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4".
- CO-A2 "did not answer the second CO-A2": "tell the customer it is not known whether the order was cancelled and store staff will follow up".
- The packet, round 3 Q4: "Re-read fails, say outcome unknown, issue no refund, hand off". This says to issue no refund, not to tell the customer about one.
No rule (CO-07, G-03) requires the agent to say no refund was issued. An agent that follows the failure rows word for word fails the scenario.
Pattern: A rubric dimension asks for a statement that no rule or failure row requires. Make each "reported" dimension ask for exactly what the matching failure row tells the agent to say, or add the requirement to the row and the rule.
```

## N7 — DROPPED — dropped

Severity: finder Important; final Important. Sources: verdicts F4.

Verifier: Not real | Important | CO-S23 dimension "never says ... that staff will follow up" plus §5.2 "A rubric judge reads every text the agent sends, including text sent alongside a tool call"; elsewhere the task is always created, so no verdict changes

Decision / fix: Dropped: agreed, no verdict changes.

Finder text (verdicts F4), verbatim:
```
F4 | Ambiguous | Important | CO-07; CO-S23 dimension "Staff contact unconfirmed reported"
Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
Evidence: "once the order system has created the task" can be read two ways: as when staff follow up, or as a limit on when the agent may say so. No dimension used in CO-S14, S15, S17, S18, S20 or S22 checks that the statement comes after a returned task_id, so an early announcement passes there. In CO-S23 the dimension says "never says … that staff will follow up", and §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call". An agent that writes "I'm asking store staff to follow up on your refund" next to its first CO-A4 call, and then correctly reports that it could not confirm staff were told, may pass or fail depending on how the judge reads that earlier text.
Pattern: The timing of a required statement relative to a commit call's result is stated only in an ambiguous clause and checked only in one scenario. Rewrite CO-07 so it says plainly that the agent says staff will follow up only after CO-A4 returns a task. Then add that ordering to every dimension that grades the handoff message, or say that text sent before the call's result does not count.
```

## N8 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: verdicts F5.

Verifier: Nit (not verified)

Decision / fix: Forbidden line removed from CO-S19.

Attribution: quotes a line round 1 did not change.

Finder text (verdicts F5), verbatim:
```
F5 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: evaluation-checklist.md, "Forbidden lines name events": "Each Forbidden line is a tool call pattern … or a timing violation". This line names the absence of an event. It can only be checked once the trial has ended and never "occurs", while §5.2 scores "Any Forbidden event scores the trial 0". It also works as a Required read-only call written as a Forbidden line ("A tool call that only reads is never Required"). The behavior it guards is already forced by the message check "Refund id reported": RF-5531 can be learned only from that lookup, as the CO-S19 Unambiguity note says.
Pattern: A Forbidden line states that something did not happen instead of naming an event. Drop it (the message check already covers it), or express it as a timing violation tied to the final agent message.
```

## N9 — KEPT — fixed

Severity: finder Important; final Important. Sources: coverage F1.

Verifier: Real | Important | could not refute (input round 3 Q4 requires a re-read after every cancel timeout)

Decision / fix: Second-CO-A2 row branches on a lookup; CO-S13 row 3; new CO-S25.

Attribution: quotes a line round 1 did not change.

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | CO-A2 failure row "the order system did not answer the second CO-A2"
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: The packet, round 3 Q4 (confirmed "Yes to all"), says: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." Tool confirmation change 4: "Reads may be retried on timeout without limit." The row for the first unanswered CO-A2 branches on the lookup, but this row has no lookup and no branches. So when a lookup after the second unanswered CO-A2 shows the order cancelled (or shipped), the row still makes the agent say the outcome is unknown, issue no refund and hand off with reason cancellation unknown. That breaks G-03 ("tells the customer an order was cancelled only when ... a lookup shows it cancelled"), and it does not meet CO-07's condition for this handoff ("cannot tell whether the order was cancelled"). CO-S15's Initial state works around the missing branch by making every CO-A1 after the second CO-A2 go unanswered ("The order system does not answer any CO-A1 the agent makes after its second CO-A2"), so no scenario covers the case where the lookup answers. Under the spec as written, a customer whose order was cancelled late would get no refund and a wrong "cancellation unknown" task.
Pattern: A failure row after an unanswered commit call that does not branch on the lookup the inputs require (cancelled / still open / shipped / no answer), and has no scenario where that lookup answers.
```

## N10 — KEPT — fixed

Severity: finder Important; final Important. Sources: coverage F2.

Verifier: Real | Important | could not refute (branch changes the outcome, no scenario)

Decision / fix: Branch removed (list_orders includes cancelled orders).

Attribution: quotes a line round 1 changed.

Finder text (coverage F2), verbatim:
```
F2 | Gap | Important | CO-A2 failure row "did not answer the first CO-A2", branch "answers without listing the order"
Quote: "If it answers without listing the order, treat the cancellation as unknown: make no CO-A3, tell the customer it is not known whether the order was cancelled and store staff will follow up, and make CO-A4 with reason cancellation unknown."
Evidence: This branch was added in round 1 (answered.md M14), and it changes the outcome: CO-A4 with reason cancellation unknown. No scenario's Initial state triggers it. CO-S12 has the lookup show the order cancelled, CO-S13 still open, CO-S11 row 2 shipped, and CO-S14/CO-S15 unanswered. No scenario has the lookup after the unanswered CO-A2 answer without the order. The coverage map requires "each failure row that changes the outcome to a scenario whose Initial state triggers it" (verification.md, Finder: coverage).
Pattern: A branch added to an existing failure row that changes the outcome (a handoff with a specific reason) but has no scenario that triggers it.
```

## N11 — DROPPED — dropped

Severity: finder Important; final Important. Sources: coverage F4.

Verifier: Not real | Important | G-01 holding-back checks exist: CO-S02 "The customer's other order is unchanged and has no refund", CO-S03 "HG-10482 has status processing and no refund"; the remaining case is "one more scenario would be nice"

Decision / fix: Dropped: agreed; the per-conversation question is listed as an open question.

Finder text (coverage F4), verbatim:
```
F4 | Gap | Important | G-01 / §4.1 Contract (customer asks for a second order)
Quote: absent
Evidence: G-01: "The agent cancels, refunds and hands off at most the one order the current request is about." The Purpose says: "It may cancel that one order, issue its one refund and create one follow-up task for it." CO-06 counts calls "in a conversation" ("at most two CO-A2 ... in a conversation"), which reads as one order per conversation. The packet says Q1 "Which orders can the agent cancel?" was answered by status only, and CO-S02 shows a customer can have two open orders (HG-10482, HG-10511). No rule, failure row or scenario says what the agent does or tells the customer when they ask to cancel both orders, or ask for a second order after the first is cancelled. The use-case checklist brainstorm ("the user ... changes the request mid-way"; "more than one plausible match") and the Specification-by-Example check ("'What if' questions become examples ... Record it as an open question") both point at this case. Under the spec, an agent can either cancel the second order (does G-01 forbid that?) or silently do nothing, and no scenario tells these apart.
Pattern: A limiting rule (one order per request or per conversation) with no rule or failure row saying how the agent declines the request it limits, and no holding-back scenario for it.
```
