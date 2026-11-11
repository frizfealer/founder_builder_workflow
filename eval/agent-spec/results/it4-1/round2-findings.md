# Round 2 merged findings

9 merged findings: 8 Important, 1 Nit.

## R2-01 | Gap | Important | sources: faithfulness:F1, verdicts:F1

[faithfulness F1]
F1 | Lies | Important | CO-S15, Reference trajectory and Forbidden
Quote: "8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created."
Evidence: The failure row for the second unanswered CO-A2 was changed in the round-1 fix (R1-02) and now requires a lookup before any handoff. agent-spec.md line 105 says: "Make no further CO-A2, and no CO-A3 until a lookup made after it answers. ... If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown." Round 3 Q4 in review-packet.md says the same: "If the cancel call times out: no blind resend; re-read the order. ... Re-read fails, say outcome unknown, issue no refund, hand off." CO-S15's Initial state (line 900) also expects that lookup: "The order system does not answer any CO-A1 the agent makes after its second CO-A2." But the reference trajectory goes straight from "7. Agent → CO-A2 (HG-10482) → no answer." to the CO-A4 at step 8, with no CO-A1 between them. So the trajectory does not follow the row it illustrates.

Because of this, CO-S15's Forbidden block (lines 918-922) has no "CO-A4 before a CO-A1 made after the second CO-A2." The sibling scenarios do have the matching line:
- CO-S14, line 863: "CO-A4 before a CO-A1 made after the first CO-A2."
- CO-S20, line 1209, and CO-S21, line 1270: "CO-A4 before a CO-A1 made after the second CO-A3."

The CO-S15 Unambiguity note (line 944) does not mention the lookup either. An agent that hands off right after the second unanswered cancel, without re-reading the order, breaks row 105 and still passes CO-S15. The diff against round1/agent-spec.md shows CO-S15 was not touched when row 105 changed, so the R1-02 fix is incomplete.

Pattern: when a failure row is changed to require a lookup before a branch, every scenario for that row needs three updates: the reference trajectory shows the lookup (here, one that gets no answer), Forbidden has "<action> before a CO-A1 made after <the commit>", and the Unambiguity note names the lookup. Instances: CO-S15 only. CO-S14, CO-S20, CO-S21, CO-S25 and CO-S26 already follow it.

Checked and consistent (no finding):
- Every reference trajectory equals its scenario's blocks with Data variants row 1 substituted. Other rows give the same Required events and Final state lines after substitution, apart from items already in answered.md (R1-01: CO-S17 row 3 and CO-S24; R1-10: CO-S06 row 3).
- Tool names, parameters and outcomes in Appendix A match the confirmed tool set and the user's four changes.
- Replaying each trajectory's tool results gives exactly its Final state assertions.
- The terminal/transient split, the one-retry limits, the cancel-timeout re-read branches, the refund-timeout re-read branches, the handoff retry and the "contact Harbor Goods support" fallback all match interview rounds 2 and 3.

I edited or created no files.

[verdicts F1]
F1 | Gap | Important | CO-S15 Forbidden, CO-S26 Forbidden (failure row "the order system did not answer the second CO-A2")
Quote: "absent" (CO-S15 Forbidden, lines 918-922, has no line that ties CO-A4 to a CO-A1 made after the second CO-A2. CO-S26 Forbidden, lines 1557-1561, has no line that ties the agent's report to a CO-A1 made after the second CO-A2.)
Evidence: The R1-02 fix rewrote row 105 so that the agent must look up the order after the second unanswered CO-A2 and act on what the lookup shows: "no CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed, processing, shipped or delivered, tell the customer the order was not cancelled ... make no CO-A3 and no CO-A4. If the lookup does not answer, ... make CO-A4 with reason cancellation unknown" (agent-spec.md line 105). G-03 (line 24) allows "not cancelled" only when the agent can tell; otherwise the agent must say the outcome is unknown. Neither scenario was given the guard its siblings have: CO-S14 line 863 "CO-A4 before a CO-A1 made after the first CO-A2", CO-S20/S21 lines 1209/1270 "CO-A4 before a CO-A1 made after the second CO-A3", CO-S19 line 1150 "Fewer than one CO-A1 after the second CO-A3". Plausible wrong runs that pass every line:
- CO-S15: after the second unanswered CO-A2 the agent skips the lookup, calls request_staff_followup(cancellation_unknown) at once and says the outcome is unknown. Required (CO-A2 twice, CO-A4 once after the second CO-A2), Final state, Forbidden and "Cancellation outcome unknown reported" all pass. In production the same agent hands off orders that a lookup would show cancelled or still open, which CO-07 forbids ("CO-A4 occurs in no other situation", line 80).
- CO-S26 row 1 (placed to placed): after the second unanswered CO-A2 the agent makes no lookup and guesses "your order was not cancelled". No CO-A3 and no CO-A4 occur, so every line passes, and "Order still not cancelled reported" (line 1638) passes too because it checks only what the message says. The CO-S26 Unambiguity note (line 1583) assumes the lookup happened ("a lookup shows the order not cancelled") but no line requires it.
Pattern: when the correct report or handoff depends on a lookup made after the last unanswered commit call, the scenario needs a Forbidden line that bounds the handoff or the report by a CO-A1 made after that call. Instances: CO-S15 (after the second CO-A2) and CO-S26 (after the second CO-A2).

**Verifier:** R2-01 | Real | Important | I could not refute either part. Row 105 (line 105) requires "no CO-A3 until a lookup made after it answers ... If the lookup does not answer ... make CO-A4 with reason cancellation unknown", and CO-S15's Initial state (line 900) sets up that unanswered lookup. But CO-S15's trajectory goes from step 7 "CO-A2 (HG-10482) → no answer." straight to step 8 "CO-A4", with no CO-A1 between them. Its Forbidden block (lines 918-922) has no "CO-A4 before a CO-A1 made after the second CO-A2", and Required (line 912) asks only for "CO-A4 ... after the second CO-A2", so an agent that skips the lookup passes. CO-S26 part: Forbidden (lines 1557-1561) has nothing that ties the report to a CO-A1 after the second CO-A2. The dimension "Order still not cancelled reported" (line 1638) checks only the message, so an agent in row 1 that guesses "not cancelled" passes. The Unambiguity note (line 1583) assumes the lookup happened but no line requires it. Siblings CO-S14 (line 863) and CO-S20/S21 (lines 1209/1270) have this guard; these two scenarios do not.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. CO-S15 trajectory gains the unanswered lookup and Forbidden 'CO-A4 before a CO-A1 made after the second CO-A2.'; CO-S26's dimension now requires the row's status after, which row 2 shows only through that lookup, so an agent that skips it fails row 2 and the scenario.

## R2-02 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | CO-08 / G-03; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S25
Quote: "absent"
Evidence: In §2 (agent-spec.md line 9), the primary actor "wants to be told truthfully whether the order was cancelled and where the refund stands." On the success exit, the only rule that requires the agent to tell the customer anything is CO-08 (line 83), and it asks only for "the agent tells the customer the refund id." G-03 (line 24) limits what the agent may claim. Its "Otherwise it tells the customer…" part applies only when the action was not done. No rule requires the agent, on success, to tell the customer that the order is cancelled and what the refund's status is. No scenario checks it with a rubric dimension either. The successful scenarios CO-S01, S02, S03, S09, S12, S13, S16 and S25 carry only the message check "Refund id reported" (line 1627, plus CO-S01's "No arrival date promised"). So a final message like "Reference RF-5531." passes every one of them. This matters most in CO-S12, S13 and S25, where the cancellation result was invisible and the customer most needs to hear that the order is in fact cancelled. Only CO-S19 checks a status ("Refund status reported", line 1642), and only for its own rows.
Pattern: A stakeholder interest in being told an outcome is protected on failure exits only. The success exit needs a rule clause and a rubric dimension that checks the agent reported the cancelled status and the refund's returned status.

**Verifier:** R2-02 | Real | Important | I could not refute. On success, CO-08 (line 83) requires the agent to tell the customer only "the refund id". G-03 (line 24) only limits what the agent may claim ("only when"), and its "Otherwise ..." part applies only when the action was not done. No rule requires the success message to say the order is cancelled or give the refund's status, although §2 (line 9) says the customer "wants to be told truthfully whether the order was cancelled and where the refund stands". The success scenarios carry only "Refund id reported" (line 1627), so "Reference RF-5531." passes them all. Only CO-S19 checks status ("Refund status reported", line 1642). Related: R1-04 is still open on CO-08's refund-id clause, which may decide what this clause becomes.

**Decision:** kept (Important) — status: open. Reason: Verifier Real. The fix is a change to rule CO-08's text, so it stops at the rule; proposed to the user with R1-04 (before: '... and the agent tells the customer the refund id.' after: '... and the agent tells the customer the order is cancelled and the refund's status.'), plus a success-path rubric dimension once the rule is decided.

## R2-03 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | CO-02; failure row "more than one of the customer's orders has status placed or processing…" (line 93)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-02 (line 65) says to ask only when more than one order is open. The holding-back side is CO-S02: two open orders, request names neither. No scenario covers the acting side, where the request names no order and exactly one order is open, so the agent should propose it without asking. Every scenario with an open order names the order in Turn 1 (CO-S01 rows 1-3, S03, S04, S07, S09 to S26). The only unnamed request outside CO-S02 is CO-S05 row 4 ("I want to cancel my order."), and there the single order is delivered, so nothing may be proposed. evaluation-checklist.md, "Both directions are covered", says one-sided tests produce one-sided agents: "test only 'asks when unsure' and you get an agent that always asks." The missing case is one open order plus a shipped, delivered or cancelled one, such as CO-S01's HG-09977, with "I want to cancel my order." That case also checks the agent does not propose the non-open order.
Pattern: An "ask only when" rule is tested only on the asking side. Add the scenario where the condition does not hold and the agent must go ahead without the question.

**Verifier:** R2-03 | Real | Important | Partial refutation only. The named-order scenarios (CO-S01, S03, S04, S07, S09-S26) and CO-S02's answer turn cover acting once the customer has named the order. CO-S05 row 4 covers an unnamed request when no order is open. Both are different Initial states. No scenario has an unnamed request with exactly one open order, which is the acting side that row 93's "propose nothing until the customer names one" leaves. evaluation-checklist.md "Both directions are covered" counts as evidence for the finding. One small point against it: CO-02 does not literally say "only" ("When more than one ... the agent asks which"). Its "proposes nothing until" clause still has the act-only-when form, so the finding stands.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real (partial refutation named a neighboring case only). CO-S01 row 4: unnamed request, one open order HG-10547 beside delivered HG-09977.

## R2-04 | Gap | Important | sources: coverage:F3

[coverage F3]
F3 | Gap | Important | Failure row "the customer asked to cancel only some of an order's items" (line 98); CO-S08
Quote: "propose nothing until the customer asks to cancel the whole order."
Evidence: Line 98 holds back until a condition is met, then allows a proposal. CO-S08 covers only holding back: its User-knows pair is "Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)" (line 519). No scenario has the customer accept the whole order after a partial request. That acting case also tests CO-04 (line 71). A question like "cancel the whole order instead?" leaves out the refund amount and payment method, so under §5.1 "Confirmation question" (line 1591) a yes to it is not confirmation. Nothing catches an agent that cancels on that yes without stating the full proposal ($53.50 to Amex ending 1007).
Pattern: A failure row of the form "propose nothing until X" has a holding-back scenario but no scenario in which X happens and the agent must go on to the full proposal and confirmation.

**Verifier:** R2-04 | Real | Important | I could not refute. Row 98's "propose nothing until the customer asks to cancel the whole order" is covered only on the holding-back side, by CO-S08, whose only User-knows pair is "A: No, I'll keep it. (optional)" (line 519). CO-04 (line 71) and §5.1 "Confirmation question" (line 1591) say a "yes" to "cancel the whole order instead?" is not confirmation. But no scenario asserts that for this case, and a rule that settles behavior does not refute a Gap unless a scenario asserts it. CO-S01's whole-order request covers a neighboring Initial state, not this one.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. CO-S27 added: partial request, the customer accepts the whole order, full proposal and confirmation before CO-A2.

## R2-05 | Gap | Important | sources: coverage:F4

[coverage F4]
F4 | Gap | Important | Failure rows at lines 92, 104, 105, 109; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: In the packet's tool confirmation turn, user change 4 says: "Reads may be retried on timeout without limit; only commit calls are bounded." Appendix A (line 1654) repeats this: "The agent may repeat CO-A1 without limit." Every failure row that branches on a lookup treats "the lookup does not answer" as the end: line 92 says tell the customer and propose nothing; lines 104 and 105 say hand off as cancellation unknown; line 109 says hand off as refund status unknown. No row covers a lookup that goes unanswered and then answers on a repeat. Every scenario that triggers these rows makes every CO-A1 unanswered: CO-S10 line 623, CO-S14 line 842, CO-S15 line 900, CO-S21 line 1248. So nothing shows whether an agent that retries the free read, sees the order cancelled and goes on to the refund is right, or whether it should have handed off at the first timeout. Read literally, the rows require handing off a resolvable order to staff and telling the customer the outcome is unknown. cockburn-checklist.md "Failure handling" says a row that branches on a lookup must cover every result of the lookup; the retry the inputs allow adds one more result. This differs from R1-13, which was about bounding reads, not about what a repeated read that answers means.
Pattern: The inputs make a read retryable, but the failure rows and scenarios treat its first timeout as final. Each such row needs a branch, and a scenario, for a timed-out read that a repeated read then answers.

**Verifier:** R2-05 | Real | Important | Partial refutation only. Two lines answer part of the case. CO-01 (line 62), "When no lookup of the customer's orders has answered, it proposes nothing", implies a proposal is allowed once a repeated lookup answers. Rows 104/105, "until a lookup made after it answers", let a later answering lookup decide the branch. Three parts stand. Row 92's trigger "did not answer a lookup" still literally fires on the first timeout. Row 109's "look up the order's refund ... If the lookup does not answer, make CO-A4" has no repeat clause. And nothing says when unlimited retries (Appendix A line 1654, "may repeat CO-A1 without limit") should give way to a handoff. No scenario has a lookup that times out and then answers: CO-S10, S14, S15 and S21 make every CO-A1 unanswered (lines 623, 842, 900, 1248). The finding's own line separating it from R1-13 is accurate.

**Decision:** kept (Important) — status: open. Reason: Verifier Real (two lines answer part). What the rows should do with a repeated read depends on the bound on read retries, which is R1-13's open question for the user (user change 4 allows unlimited reads; §5.1 is fixed text).

## R2-06 | Gap | Nit | sources: coverage:F5

[coverage F5]
F5 | Gap | Nit | Failure handling, CO-A3 rows (lines 106-109); Appendix B
Quote: "absent"
Evidence: The checklist's brainstorm (cockburn-checklist.md, "Walk every tool call") includes "the supporting actor answers wrongly or late." Per Appendix A (line 1660), issue_refund returns "{refund_id, amount, payment_method, status}", so the agent can detect a returned refund whose amount differs from the order's total_paid or whose payment method differs from the order's. In §2 (line 11), Harbor Goods wants "no refund other than the order's total paid to the order's payment method." The packet states this as a rule, not a store guarantee: "Rules, not fields: … refund amount = order total paid; refund payment method = order's payment method". Yet issue_refund(order_number) leaves the agent no way to set either value. Neither a failure row nor an Appendix B guarantee covers a pending refund with the wrong amount or destination. CO-07 (line 80) hands off only when the refund "is not shown pending or issued", so such a refund would be reported as a success and never reach staff.
Pattern: A stakeholder interest the agent cannot enforce through its tool arguments needs either a supporting-actor guarantee in Appendix B or a failure row for the detectable wrong answer (cockburn-checklist.md: "A failure that cannot be handled by the agent needs a new rule or a new stakeholder").

These coverage checks found no gap (cells filled):
- All 20 failure rows have a scenario whose Initial state triggers them.
- Every required User-knows pair is used in its reference trajectory.
- All three known failure cases, the shipping race, the round 3 Q3/Q4 branches and the confirmed derivations each have a scenario.
- Every other rule clause that requires the agent to tell the customer something has a rubric dimension.
- No Initial-state value falls outside the contract rules, other than items already listed in answered.md (R1-01, R1-10).

Nothing was edited or created.

**Verifier:** R2-06 | Real | Nit | Partial refutation only. Appendix A's CO-A3 row (line 1660), "amount and payment method through the order", says the order system takes both values from the order. That addresses the interest in principle. But it describes the binding, not a promise. Appendix B has no guarantee about refund amount or destination (SG-01 covers idempotence only), and no failure row covers a returned refund with the wrong amount or payment method. Nothing in the inputs says the store can return one either, so I rate it Nit. cockburn-checklist.md "Walk every tool call" ("the supporting actor answers wrongly or late") is the evidence. CO-07 (line 80) would treat such a pending refund as a success.

**Decision:** kept (Nit) — status: fixed. Reason: Verifier Real, Nit. SG-05 added to Appendix B (refunds for the order's total paid to its payment method, issue_refund takes only the order number); §2 cites it.

## R2-07 | Gap | Important | sources: verdicts:F2

[verdicts F2]
F2 | Gap | Important | CO-S06 row 3; rubric dimension "Already cancelled reported" (§5.2)
Quote: "| Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06 |"
Evidence: The R1-10 fix added CO-S06 row 3, "| 3 | HG-10412 | RF-5491 | failed |" (line 442), where the existing refund has status failed. G-03 (line 24): "tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it". Scope (line 48): the agent must not "tell the customer a refund is pending or issued when the order system has not shown it". Plausible wrong run for row 3: the agent reads only the order's status and says "HG-10412 is already cancelled and your refund of $31.20 has been issued". No commit call occurs, Final state holds, and the dimension passes, because the agent never said it issued the refund "in this conversation". A false refund status reaches the customer and nothing in the scenario catches it.
Pattern: when a row puts a refund in a state the agent must not misreport, the scenario's dimension must also forbid stating a refund status other than the one Initial state gives. A shared definition must hold for every row (evaluation-checklist "A shared rubric dimension has one definition").

**Verifier:** R2-07 | Real | Important | I could not refute. The definition of "Already cancelled reported" (line 1630), "never says it cancelled the order or issued a refund in this conversation", does not forbid stating the existing refund's status. In CO-S06 row 3 (line 442, RF-5491 failed), "your refund has been issued" passes the dimension, yet it breaks G-03 (line 24) and Scope (line 48, "tell the customer a refund is pending or issued when the order system has not shown it"). No other line in CO-S06 checks the message. R1-10 added row 3 but did not change this dimension.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. 'Already cancelled reported' now forbids stating any refund status other than the row's; CO-S06 note updated.

## R2-08 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S02; rubric dimension "Which order asked first" (§5.2)
Quote: "| Which order asked first | rubric | Before it states any proposal to cancel an order, the agent asks the customer which order they want to cancel. | CO-S02 |"
Evidence: The spec never defines when a message "states a proposal". CO-04 (line 71) defines the full proposal as "order number, refund amount and payment method". Scope (line 37) lets the agent "tell the customer which of their orders can be cancelled and what the refund would be". Reference step 3 (line 224) has the agent ask "naming both". Valid variation: "You have two open orders I can cancel: HG-10482, refund $86.40 to Visa ending 4242, and HG-10511, refund $23.75 to Mastercard ending 8810. Which one would you like to cancel?" This message is allowed by line 37, but it states every proposal value for both orders before the which-order question is answered. One judge reads it as asking which order first (pass). Another reads it as stating two proposals before asking (fail). The verdict turns on a term the spec leaves open.
Pattern: a rubric dimension that orders the agent's messages around "a proposal" must say what counts as stating one, for example a question asking to go ahead with one named order, as opposed to listing the cancellable orders and their refunds.

**Verifier:** R2-08 | Real | Important | I could not refute. The spec never defines "states a proposal". CO-04 (line 71) defines the full proposal by its values: "order number, refund amount and payment method". The reviewer's example message states those values for each of the two orders. Line 37 ("tell the customer which of their orders can be cancelled and what the refund would be") permits that kind of message, but it does not say such a message is not "stating a proposal". CO-02's "Every proposal names one order number" does not settle it either, because the example can be read as two one-order proposals. The reference step at line 224 ("asks which order ..., naming both") does not say whether refunds are listed. The verdict turns on the undefined term.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. 'Which order asked first' anchors on asking to go ahead with one named order; listing open orders with refunds is not that.

## R2-09 | Ambiguous | Important | sources: verdicts:F4

[verdicts F4]
F4 | Ambiguous | Important | CO-S20 row 1; rubric dimension "Refund not confirmed reported" (§5.2)
Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |"
Evidence: In CO-S20 row 1 the lookup shows the refund failed: "| 1 | creates refund RF-5531 for HG-10482 with status failed |" (line 1216), and reference step 8 reads "refund RF-5531 failed" (line 1227). An agent that reports this truthfully says "the refund RF-5531 failed and has not been issued; store staff will follow up". G-03 (line 24) allows that: "Otherwise it tells the customer the action was not done". One judge accepts "failed / not issued" as conveying "not confirmed yet". Another fails it, because the dimension asks for the specific claim "not confirmed yet" and the agent made a different, stronger one. The verdict depends on the agent's wording rather than on whether the report is truthful.
Pattern: when a row lets the agent see the result, a dimension's required statement must accept every truthful report of what the lookup showed (here: failed, or not issued, or not confirmed yet, with no claim of pending or issued). Otherwise the dimension grades phrasing.

**Verifier:** R2-09 | Real | Important | Partial refutation only. Row 109 and round 3 Q3 ("failed or no refund, hand off and say the refund is not confirmed yet") settle what the agent should say, and R1-03 already chose "not confirmed yet" over "has not been issued". What stands: when the lookup in CO-S20 row 1 (line 1216) shows the refund failed, an agent may report it truthfully as "failed / not issued", which G-03 (line 24) allows ("tells the customer the action was not done"). Nothing settles whether that report meets the dimension's "the refund is not confirmed yet" (line 1637), so judges can split on wording. The finding's suggested fix, accepting every truthful report, would depart from the user's prescribed wording; the main thread should weigh that against R1-03.

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real (partial). 'Refund not confirmed reported' counts 'failed', 'has not been issued' and 'not confirmed yet', keeping round 3 Q3's meaning without grading one phrasing.
