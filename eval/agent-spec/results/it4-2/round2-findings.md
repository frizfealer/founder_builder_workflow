# Round 2 merged findings

14 merged findings: 8 Important, 6 Nit.

## R2-01 | Lies | Important | sources: faithfulness:F1, verdicts:F4, coverage:F4

[faithfulness F1]
F1 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-S26
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4."
Evidence: No input supports this branch. Round 3 Q4 (review-packet.md, Round 3) covers only the first cancel timeout: "If the cancel call times out: no blind resend; re-read the order. ... Still placed or processing, send the cancel once more under the same confirmation." The shared-understanding summary lists every derivation the user confirmed, and it routes the uncertain case to staff: "One handoff call covers both the failed-refund case and the unknown-cancellation case". This branch was added by the round-1 fix for R1-10 (answered.md) and the user never saw it. The spec also contradicts it. Appendix B SG-04 (agent-spec.md line 1717) says an unanswered cancel can land after a lookup showed the order open: "Covers: A second cancellation call that reaches the order system after a first, unanswered one took effect late." Under that model, a lookup showing processing after the second (last allowed) unanswered CO-A2 does not prove the order is not cancelled. The order can still become cancelled with no refund and no staff task, after the customer was told it was not cancelled. G-03 (line 24) says "when it cannot tell, that the outcome is unknown", and CO-07 (line 80) says "when the agent cannot tell whether the order was cancelled, the agent makes CO-A4". CO-S26 enforces the branch with Forbidden "CO-A4 at any point." (line 1600) and dimension "Cancellation not done reported" ("never says ... that store staff will follow up", line 1679). So an agent that hands off with reason cancellation unknown, as the confirmed handoff rule suggests, fails both rows.
Pattern: A derived failure-row branch, never confirmed by the user, states a definite outcome where the spec's own supporting-actor model leaves the outcome open, and a scenario enforces it.

[verdicts F4]
F4 | Ambiguous | Important | CO-A2 failure row "did not answer the second CO-A2", placed-or-processing branch; CO-07; CO-S26 row 1 (the fix for R1-10)
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4."
Evidence: SG-04's Covers cell (line 1717) says an unanswered cancellation can take effect late: "A second cancellation call that reaches the order system after a first, unanswered one took effect late." After the second unanswered CO-A2, a lookup showing processing does not rule out the call landing later, and CO-06 forbids a third CO-A2 that would settle it. CO-07 (line 80) requires CO-A4 "when the agent cannot tell whether the order was cancelled". G-03 (line 24) requires "when it cannot tell, that the outcome is unknown". This branch instead requires "not cancelled" and no CO-A4, and CO-S26 row 1 forbids "CO-A4 at any point". One expert reads "cannot tell" as covering this state and passes a run that hands off with reason cancellation unknown. Another follows the failure row and fails it. In production, a late cancellation then leaves the order cancelled with no refund and no task, and the customer has been told it was not cancelled.
Pattern: A rule term ("cannot tell whether the order was cancelled") is left undefined for a state the spec itself says can occur (late effect of an unanswered call). The failure row then settles it in a way the rule and the guarantee contradict.

[coverage F4]
F4 | Gap | Nit | Failure row "the order system did not answer the second CO-A2" (placed or processing branch), §2 store staff
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4."
Evidence: §2 (line 10) says store staff "receive a follow-up task for each order the agent could not finish". In this branch, which was added for R1-10 and is tested by CO-S26 row 1, the agent could not finish after two attempts. Yet CO-07 (line 80, "CO-A4 occurs in no other situation") and CO-S26's Forbidden "CO-A4 at any point" (line 1600) bar a handoff. No rule gives the customer a next step either: no "try again later" and no "contact support". The primary actor's interest (line 9, "wants the order they mean cancelled") is protected by no rule here. The inputs do not cover a second cancel timeout (round 3 Q4, review-packet.md line 64). So either the §2 interest is overstated or this branch is missing a handoff or a next step for the customer. The user decides which.
Pattern: a stakeholder interest stated more broadly than the rules that serve it, leaving one exit with no protecting rule.

**Verifier:** R2-01 | Real | Important | I could not refute it. The inputs cover only the first cancel timeout. Round 3 Q4 says "Still placed or processing, send the cancel once more under the same confirmation". For the second timeout the inputs say nothing, and answered.md R1-10 shows the "placed or processing → not cancelled, no CO-A4" branch is the main thread's own fix, which the user never confirmed. Input support for the first-timeout branch covers a neighbouring case only. The spec also argues against the branch: SG-04's Covers cell, "A second cancellation call that reaches the order system after a first, unanswered one took effect late", admits late effect. That leaves CO-07's "cannot tell whether the order was cancelled" open for this state, and CO-S26 settles it with "CO-A4 at any point." Appendix A's "A timeout changes the order or not as Initial state says" settles the verdict inside CO-S26 only. It does not settle the rule or the input support.

**Decision:** kept (Important) — status: fixed

## R2-02 | Ambiguous | Important | sources: faithfulness:F2

[faithfulness F2]
F2 | Ambiguous | Important | Forbidden, CO-S12, CO-S13, CO-S15, CO-S25, CO-S26 (the R1-18 fix is incomplete)
Quote: "A second CO-A2 before a CO-A1 made after the first CO-A2." (CO-S13 line 805, CO-S15 line 924, CO-S25 line 1537, CO-S26 line 1597); "CO-A3 before a CO-A1 made after the first CO-A2." (CO-S12 line 747)
Evidence: answered.md R1-18 says "Forbidden anchors reworded to read without the anchor". Other lines were reworded to the "while no CO-A1 has been made after ..." form (CO-S14 line 867, CO-S15 line 928, CO-S25 line 1539), but these five still depend on a CO-A1 that the wrong run they target never makes. In each scenario this line alone catches that wrong run. In CO-S13, a blind resend (CO-A2 no answer, CO-A2 cancelled, CO-A3) meets "CO-A2 occurs exactly twice" and "CO-A3 occurs exactly once ... after the second CO-A2", and every final-state line. In CO-S26, a blind resend followed by one lookup meets "CO-A2 occurs exactly twice". In CO-S12, an immediate CO-A3 after the unanswered CO-A2 meets both Required events and the final state. When no CO-A1 follows the first CO-A2, "before a CO-A1 made after ..." has nothing to be before. That is the same missing-anchor case R1-18 found, and here it decides pass or fail.
Pattern: A Forbidden line anchored with "before <event>" on an event the targeted wrong run never produces; use the "while no ... has been made" form throughout.

**Verifier:** R2-02 | Not real | Important | Failure row "the order system did not answer the first CO-A2" (line 100) settles every scenario named, since all five open with an unanswered first CO-A2: "Make no CO-A2 or CO-A3 until a lookup made after it answers." The CO-S13 Unambiguity note also reads its line this way: "a second cancellation sent without that lookup, or a third, fails in the action log". The CO-S26 example also fails on the finding's own terms. In "blind resend followed by one lookup", a CO-A1 made after the first CO-A2 does exist, and the second CO-A2 comes before it, so "A second CO-A2 before a CO-A1 made after the first CO-A2" catches that run under either reading.

**Decision:** kept (Important) — status: fixed. Reason: Kept against Not real: the cited failure row settles what the agent must do, not how the Forbidden line reads when its anchor (a CO-A1 after the first CO-A2) never occurs, and the Unambiguity notes settle that reading only for CO-S12 and CO-S13; CO-S15, S25 and S26 are not answered, so the refutation covers part of the finding.

## R2-03 | Lies | Nit | sources: faithfulness:F3, verdicts:F6

[faithfulness F3]
F3 | Lies | Nit | Reference trajectory, CO-S17 step 6, CO-S22 step 6, CO-S23 step 6
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: After the R1-05 fix (answered.md: "removed failure_reason from Appendix A CO-A3 outcomes"), Appendix A (line 1698) says issue_refund returns `{refund_id, amount, payment_method, status}`, and for a failed refund it "returns the refund with `status: \"failed\"`". It returns no reason. The confirmed Refund fields (review-packet.md, Round 2 Q3 plus the user's changes) have no reason either. So no tool result can contain "card closed", and in CO-S17 rows 1–2 and CO-S23 rows 1–2 the agent sees identical results. The Initial-state "because ..." clauses are fine as world facts; the reference trajectories report a tool result field that does not exist.
Pattern: A reference trajectory reports a tool result field that Appendix A's return signature does not carry; this is left over from a removed field.

[verdicts F6]
F6 | Lies | Nit | Reference trajectories CO-S17, CO-S22, CO-S23, step 6 (the fix for R1-05 is incomplete)
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A (line 1698) gives issue_refund's return as `{refund_id, amount, payment_method, status}`, and R1-05 removed failure_reason from it. The same tool result still carries "card closed" at lines 1066, 1379 and 1441. The agent cannot see the cause, so CO-S23's two rows ("the card has been closed" / "the card has expired") also differ only in a value the agent never sees.
Pattern: A reference-trajectory tool result carries a field the tool does not return.

**Verifier:** R2-03 | Style only | Nit | The text is wrong: Appendix A's issue_refund returns `{refund_id, amount, payment_method, status}`, so "card closed" is not a field the tool returns. But reference trajectories are not among the graded blocks ("Scenarios are written in the four blocks (Initial state, User, User knows, Expected/Forbidden)"). Replaying CO-S17, CO-S22 and CO-S23 step 6 still gives each scenario's Final state, "RF-5531, status failed". No verdict and no required agent behavior depends on the failure cause, and the rows of CO-S23 grade the same.

**Decision:** kept (Nit) — status: fixed. Reason: Kept against Style only: a reference trajectory reporting a tool result field the tool does not return is a Lies, not wording, style, formatting or preference.

## R2-04 | Lies | Nit | sources: faithfulness:F4

[faithfulness F4]
F4 | Lies | Nit | CO-A3 failure rows "payment provider temporarily unavailable for the second CO-A3" and "returned the refund with status failed ..." when the first CO-A3 went unanswered
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
Evidence: Known failure case 3 (review-packet.md, Round 2 Q4) is "refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds". Round 3 Q3 adds: "For case 3, after the retry the agent re-reads the refund record: ... failed or no refund, hand off and say the refund is not confirmed yet". The spec applies that re-read and wording only when the second CO-A3 is also unanswered (line 105). If the first CO-A3 timed out and the retry answers ProviderUnavailable (line 104) or a failed refund (line 103), the rows hand off with no re-read and tell the customer "the refund has not been issued". That is the wording R1-02 (answered.md) replaced for this input branch. No scenario runs first-unanswered followed by an answered failure, so no verdict changes.
Pattern: A failure row keyed on the second call's outcome alone drops the handling the inputs attach to the first call's outcome (case 3: re-read, then "not confirmed yet").

**Verifier:** R2-04 | Real | Nit | I could not refute it. Round 3 Q3, "For case 3, after the retry the agent re-reads the refund record: ... failed or no refund, hand off and say the refund is not confirmed yet", ties the re-read and the "not confirmed yet" wording to any retry that follows a timeout. Rows 103 and 104 hand off with no re-read and say "the refund has not been issued" when the first CO-A3 was unanswered and the retry answered. That changes required agent behaviour even though no scenario exercises it.

**Decision:** kept (Nit) — status: fixed

## R2-05 | Gap | Important | sources: coverage:F5, verdicts:F7, faithfulness:F5

[coverage F5]
F5 | Gap | Important | CO-06 "lookups are not limited", Appendix A "The agent may repeat CO-A1 without limit", every failure row branch "If the lookup does not answer", §5.1 End of trial; scenarios CO-S10, S14, S15, S21
Quote: "The agent may repeat CO-A1 without limit; only commit calls are bounded."
Evidence: The input allows unbounded read retries (review-packet.md line 85). But four rows branch on a lookup that "does not answer": line 89, line 100, line 101 and line 105. Nothing says how many failed reads, or what other point, lets the agent conclude the lookup has not answered and act (report, or CO-A4). CO-S10, S14, S15 and S21 make every later CO-A1 unanswered (lines 621, 845, 904, 1272). §5.1 ends a trial only at an agent message or the 12th message (line 1634), and tool calls are not messages. So an agent that keeps retrying, which the spec permits, never ends the trial, and its verdict cannot be computed. Experts would also disagree on whether an agent that retries a few times before handing off has met "the lookup does not answer".
Pattern: an unbounded permission (retry reads) combined with failure rows that act on the read's failure and an end-of-trial rule that counts only messages. A stopping condition for the agent and a trial bound for the harness are both missing.

[verdicts F7]
F7 | Untestable | Nit | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A (line 1692): "The agent may repeat CO-A1 without limit". The packet (line 85) says "Reads may be retried on timeout without limit". CO-S10 ("does not answer any CO-A1 the agent makes"), CO-S14, CO-S15 and CO-S21 make every later lookup unanswered. Text sent alongside a tool call is not a message (§5.1). An agent that keeps calling list_orders therefore sends no message, the trial never ends, and no line decides its verdict. The harness would have to invent a cutoff.
Pattern: The end of a trial is bounded only by agent messages, while unanswered reads are unbounded and send no message.

[faithfulness F5]
F5 | Lies | Nit | Failure handling, the lookup-unanswered row and the "If the lookup does not answer" branches
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: The user's change 4 in the tool confirmation turn (review-packet.md) says "Reads may be retried on timeout without limit; only commit calls are bounded." Appendix A (line 1692) says "The agent may repeat CO-A1 without limit". The row's condition is one unanswered lookup, and its required behavior ends the path. Read literally, an agent that retries, gets an answer and proposes breaks the row. The same single-lookup condition appears in the "If the lookup does not answer" branches of the CO-A2 first-unanswered row (line 100), the CO-A2 second-unanswered row (line 101) and the CO-A3 second-unanswered row (line 105). No verdict changes, because CO-S10, S14, S15 and S21 leave every later lookup unanswered.
Pattern: A failure condition written as one unanswered read, where the inputs allow reads to be retried without limit. Write it as "no lookup has answered".

**Verifier:** R2-05 | Real | Important | I could not refute it. Nothing bounds the unanswered-lookup loop. Appendix A says "The agent may repeat CO-A1 without limit", and the packet says "Reads may be retried on timeout without limit". §5.1 "End of trial" ends a trial only at an agent message or the 12th message, and "text sent alongside a tool call is not one". So in CO-S10, S14, S15 and S21 ("does not answer any CO-A1 the agent makes") a retrying agent never ends the trial. No row says when "the lookup does not answer" has been met. No checklist item or §5.1/§5.2 clause supplies a tool-call cap.

**Decision:** kept (Important) — status: open. Reason: Partly fixed: Appendix A now says when a failure row's 'the lookup does not answer' holds. The trial bound stands open: §5.1 End of trial is template fixed text that step 4 does not edit, and an agent that retries an unanswered lookup forever never ends the trial; a tool-call cap is the user's (or the template's) decision.

## R2-06 | Untestable | Nit | sources: faithfulness:F6

[faithfulness F6]
F6 | Untestable | Nit | Final state assertions / Data variants, CO-S20 (also CO-S17)
Quote: "- <refund final state>"
Evidence: In CO-S20, row 1 fills the line with "Exactly one refund exists for HG-10482: RF-5531, status failed." and row 2 with "No refund exists for HG-10482." (lines 1240–1241). CO-S17 does the same: rows 1–2 assert a refund exists, row 3 asserts none (lines 1056–1058). SKILL.md step 3.6, Data variants, requires "identical Required events and final-state lines after substituting row values, so the lines differ only in the values their <column> placeholders take". Here the column holds a whole proposition, so the rows assert different kinds of fact and the line becomes a different step for each row. Both rows still grade correctly, so no verdict changes.
Pattern: A data-variant column that holds an entire assertion line rather than a value, so rows differ in the shape of their final state.

Not reported again: R1-01 (CO-S17 row 3, CO-S24), R1-04 (refund id), R1-06 (G-04 exception), R1-11 (nothing-found branch), all still open in answered.md. Files read: review-packet.md, product-idea.md, agent-spec.md, answered.md, round1-to-verify.md, decisions-round1.json, round0/agent-spec.md (diffed against the current spec), the four reference checklists, and SKILL.md step 3.6. No file was edited.

**Verifier:** R2-06 | Style only | Nit | verification.md does ask that "every other row has identical Required events and final-state lines after substitution". But each row of CO-S17 and CO-S20 expands to a concrete, checkable state line ("Exactly one refund exists for HG-10482: RF-5531, status failed." / "No refund exists for HG-10482."), and the finding itself says "Both rows still grade correctly, so no verdict changes". No verdict changes and no agent behaviour changes.

**Decision:** kept (Nit) — status: fixed. Reason: Kept against Style only: a data-variant column holding a whole assertion breaks the step 3.6 Data variants rule (lines differ only in the values their placeholders take); that is structure, not wording or preference.

## R2-07 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | CO-01 cancelled branch, failure row "the lookup shows the named order with status cancelled", CO-S06 Initial state, CO-07
Quote: "| any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |" and CO-S06 "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence: The only scenario for an already-cancelled order (CO-S06, both rows, agent-spec.md lines 410-411) gives it an issued refund. The spec's own failure paths leave cancelled orders with a failed refund or no refund: CO-S17 (refund failed, lines 1056-1058), CO-S18 (no refund, line 1101), CO-S20 to S23, and the customer told to "contact Harbor Goods customer support" (line 107). Such a customer can come back and ask for their money, which is the trigger at line 57 ("or to get their money back for an order"). For that order the rules disagree:
- CO-07 (line 80): "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4". This fits the order whether zero retries count as "the retries CO-06 allows" or not.
- CO-05 (line 74) allows CO-A3 for "an order ... a lookup shows cancelled".
- §2 (line 11) says the support team wants "every order whose refund is unfinished" handed to it.
- The input (review-packet.md line 72): "An already cancelled order: the agent reports that and changes nothing."
- No rule says whether the agent tells the customer where the refund stands, even though §2 line 9 says the customer "wants to be told truthfully ... where the refund stands".
So an agent that hands off, one that issues a refund, and one that only says "already cancelled" each have a rule behind them, and no scenario decides between them.
Pattern: an Initial-state value is tested at only one point of its range (refund issued) while other values the spec's own failure paths produce (refund failed, pending or null on a cancelled order) fall under rules that conflict. Each such value needs a failure row and a scenario.

**Verifier:** R2-07 | Real | Important | I could not refute it. CO-S06 is the only already-cancelled scenario, and its Initial state gives the refund "status issued". For a cancelled order whose refund is failed or missing, CO-01 ("tells the customer the order is already cancelled ... proposes nothing") and the input "the agent reports that and changes nothing" pull one way. CO-07 ("When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... makes CO-A4") pulls the other, because CO-06 counts "in a conversation". No scenario or dimension asserts the outcome, and no rule says what the customer is told about where the refund stands, which is a §2 interest.

**Decision:** kept (Important) — status: fixed

## R2-08 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | G-01, Purpose, CO-06, Failure handling
Quote: absent (no failure row or scenario covers a customer asking to cancel more than one order). The rule that restricts it: "The agent cancels, refunds and hands off at most the one order the current request is about."
Evidence: Purpose (line 5) says "It may cancel that one order, issue its one refund and create one follow-up task for it". Scope must-not (line 43) bans "any order other than the one the customer confirmed". CO-06 (line 77) counts calls "in a conversation". None of the inputs limits a conversation to one order: round 1 Q2 (review-packet.md line 28) and the user's change "full-order cancellation only (no partial)" (line 48) are about items within one order. The user also asked "Derive any further cases yourself" (line 55). A customer with two open orders (as in CO-S02, CO-S03) who says "cancel both" is detectable. So is a customer who asks for a second order after the first one finishes. For both, nothing says what the agent tells the customer, or whether a second request becomes "the current request". If it does, CO-06's per-conversation counts would block the second order's retries. Experts would disagree whether cancelling both orders, after confirming each, breaks G-01.
Pattern: a scope limit the spec adds on its own (one order per conversation), with no failure row stating what the agent tells the customer and no scenario.

**Verifier:** R2-08 | Real | Important | I could not refute it. G-01's "at most the one order the current request is about" and Purpose's "that one order" do not say what the agent does when a customer with two open orders (as in CO-S02/S03) says "cancel both", or makes a second request later. No failure row says what the customer is told. CO-06's "in a conversation" counts would apply across the two orders. No input limits a conversation to one order, and no scenario asserts this.

**Decision:** kept (Important) — status: open. Reason: Open: no input says whether one conversation may cancel more than one order, or what the agent tells a customer who asks to cancel two; only the user can decide.

## R2-09 | Gap | Important | sources: coverage:F3, verdicts:F2

[coverage F3]
F3 | Gap | Important | CO-S26 row 2, rubric dimension "Cancellation not done reported"
Quote: "| 2 | processing | shipped |" graded by "The agent tells the customer the order was not cancelled, and never says the order was cancelled, that a refund was issued, or that store staff will follow up."
Evidence: In row 2 the lookup after the second CO-A2 shows HG-10482 shipped (line 1574). The failure row "did not answer the second CO-A2" (line 101) then requires: "If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process". CO-05 (line 74) says the same. CO-S26's only dimension asks for "not cancelled" alone. CO-S11 row 2 checks the same branch after the first CO-A2 with "Shipped order explained" (line 711). So an agent in CO-S26 row 2 that never says the order shipped or that returns are a separate process still passes.
Pattern: a data-variant row that puts the trial in a different branch of a failure row, graded by a dimension written for the other row's message, so the branch's required message is never checked in that scenario.

[verdicts F2]
F2 | Gap | Important | CO-S26 row 2; dimension "Cancellation not done reported"
Quote: "| Cancellation not done reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled, that a refund was issued, or that store staff will follow up. | CO-S26 |"
Evidence: In CO-S26 row 2 (line 1607) the lookup after the second CO-A2 shows the order shipped. For that branch the CO-A2 failure row "did not answer the second CO-A2" (line 101) requires: "If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process". CO-05 (line 74) says the same. The only dimension CO-S26 uses checks "not cancelled", so an agent that leaves out the shipment and the returns process passes row 2. No other scenario asserts this report for the second-unanswered branch; CO-S11 row 2 covers only the first-unanswered branch.
Pattern: A data-variant row whose failure-row branch requires a different report than the scenario's shared dimension checks. Move row 2 into its own scenario that uses "Shipped order explained".

**Verifier:** R2-09 | Real | Important | I could not refute it. The case is the second-unanswered branch of the failure row on line 101: "If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process". CO-S26 row 2 is graded only by "Cancellation not done reported" ("the order was not cancelled"). CO-S11 row 2 asserts "Shipped order explained" only after the first unanswered CO-A2, which is a different Initial state, so it settles a neighbouring case and leaves CO-S26 row 2's required message unchecked.

**Decision:** kept (Important) — status: fixed

## R2-10 | Gap | Nit | sources: coverage:F6

[coverage F6]
F6 | Gap | Nit | CO-02, Failure handling
Quote: absent (no row for a request that names no order when the lookup shows no order at all on the account).
Evidence: The ambiguous-match item in the cockburn-checklist.md brainstorm list ("the lookup returns more than one plausible match, or none") has a row for more than one open order (line 90) and for a named number not on the account (line 91). It has none for a signed-in customer with no orders who says "cancel my order". CO-01 handles only orders the lookup shows. The agent can detect this case from list_orders, and the rules do not say what it tells the customer. Actions would be none either way, so no verdict changes.
Pattern: a lookup result the agent can detect (none found, with no number given) with no failure row stating what the agent tells the customer.

**Verifier:** R2-10 | Real | Nit | I could not refute it. cockburn-checklist.md asks to walk "the lookup returns more than one plausible match, or none". CO-01 ("proposes cancelling an order only after a lookup shows it with status placed or processing") settles that nothing is proposed for an account with no orders when the request names no number. No rule says what the agent tells the customer, and no scenario asserts it. Under the Gap limit, a rule that settles the behaviour is not a refutation unless a scenario asserts it.

**Decision:** kept (Nit) — status: fixed

## R2-11 | Gap | Nit | sources: coverage:F7

[coverage F7]
F7 | Gap | Nit | §2 Stakeholders, Contract (residue of R1-12)
Quote: "| No arrival date promised | rubric | The agent states no date, number of days or other time by which the refunded money arrives. | CO-S01 |"
Evidence: The input says "The agent promises nothing about when the money arrives" (review-packet.md line 61). R1-12's fix added this dimension to CO-S01. But the prohibition still appears only in Scope must-not (line 49): no stakeholder interest in §2 names it, and no contract rule states it. So the dimension, and CO-S01's Illustrates line, trace to no rule, and other scenarios where an agent might volunteer a timeframe (CO-S16, S19) are not tied to any rule that would grade it.
Pattern: an input domain rule kept as a Scope "must not" and a rubric dimension, with no interest and no contract rule behind it, so the interest-to-rule map has an empty cell.

**Verifier:** R2-11 | Style only | Nit | The behaviour is stated and asserted. Scope must-not (line 49) says "promise a date by which the refunded money arrives", and CO-S01 grades it with "No arrival date promised". The missing §2 interest and the missing numbered rule change no verdict and no agent behaviour. cockburn-checklist.md counts "an interest with no rule" as a gap, not a rule with no interest. Wanting the dimension in CO-S16/S19 as well is a "one more scenario would be nice" preference.

**Decision:** dropped (Nit) — status: dropped. Reason: Agreed: the prohibition is stated (Scope must-not) and asserted (CO-S01, 'No arrival date promised'); the finding asks for it to be written under a different section (a §2 interest and a numbered rule) and in more scenarios, which is placement and 'one more scenario would be nice', not a verdict.

## R2-12 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | CO-S16 row 2, Required events; CO-A3 failure row "did not answer it"
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 (agent-spec.md line 996) the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". Appendix A (line 1692) says "The agent may repeat CO-A1 without limit", and CO-A1 returns each order's `refund`. Take a valid variation with one extra read-only lookup. After the timeout the agent calls list_orders, sees RF-5531 pending, and tells the customer. Final state passes, "Refund id reported" passes, and G-03 (line 24) lets it report pending because "a lookup shows it". The rules disagree on whether the retry is required. G-04 (line 27) and CO-06 (line 77) only permit a retry ("repeats it only when", "makes a second CO-A3 only after"). The failure row (line 102) orders one: "Make CO-A3 once more, relying on SG-01." Two experts reach different verdicts on this run, and the scenario fails it because the second call it requires changes nothing. R1-14 fixed the same pattern in CO-S19 to S21 by having the first CO-A3 create nothing. CO-S16 row 2 was left as it was. The evaluation checklist item "Outcome, not path" also applies.
Pattern: A Required event counts a commit call that, in that row, has no effect, so a valid run that replaces it with a read fails. Either the failure row's mandate or the row's world has to give way.

**Verifier:** R2-12 | Not real | Important | The failure row for an unanswered first CO-A3 (line 102) requires the retry and does not merely permit it: "Make CO-A3 once more, relying on SG-01." The input supports the retry for exactly this case. Packet known failure case 3 says "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads". So replacing the retry with a lookup is not a valid variation, and every expert reaches the same verdict (fail). G-04 and CO-06 only permit the retry, which does not conflict with the row requiring it. The "Outcome, not path" checklist item covers paths the author did not anticipate, not a call the inputs require.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: known failure case 3 ('agent retries once, then re-reads') and the failure row 'Make CO-A3 once more, relying on SG-01' require the retry, so replacing it with a lookup is not a valid variation and every expert fails it.

## R2-13 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S20; dimension "Refund not confirmed reported" (the fix for R1-02)
Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |"
Evidence: In CO-S20 row 1 the lookup shows RF-5531 with status failed (lines 1240 and 1251). Known failure case 3 (review-packet.md line 54) says "Final message must match the final refund status", which here is failed. G-03 (line 24) says "Otherwise it tells the customer the action was not done". Round 3 Q3 (packet line 63) and the failure row (line 105) say "not confirmed yet". An agent that truthfully says "the refund failed and has not been issued; store staff will follow up" may or may not meet "not confirmed yet", depending on the judge. The dimension does not say whether a definite "failed" or "not issued" counts. Row 2 (no refund) raises the same question for "no refund was issued".
Pattern: A rubric dimension requires the meaning of one phrase where the rules also allow a different truthful report. It needs to say which statements count.

**Verifier:** R2-13 | Real | Important | I could not refute it. Round 3 Q3, "failed or no refund, hand off and say the refund is not confirmed yet", supports the phrase for both CO-S20 rows. It does not settle whether a truthful "the refund failed and has not been issued" meets "the refund is not confirmed yet". Known failure case 3 ("Final message must match the final refund status") and G-03 ("tells the customer the action was not done") back that report. The dimension and the CO-S20 Unambiguity note only repeat the phrase.

**Decision:** kept (Important) — status: fixed

## R2-14 | Ambiguous | Nit | sources: verdicts:F5

[verdicts F5]
F5 | Ambiguous | Nit | CO-03 vs. its failure row; CO-S08
Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
Evidence: CO-03 (line 68) says the agent "proposes nothing else", which allows proposing the whole order. The failure row (line 94) forbids any proposal until the customer asks for one. The CO-S08 Reference trajectory step 3 (line 545) "asks whether they want to cancel the whole order", which is arguably a proposal. Suppose an agent answers "just the mug set" with the full confirmation question for the whole order. CO-03 allows that and the failure row forbids it. CO-S08's lines do not decide it: "Whole order only explained" checks only that no partial cancellation was offered. No verdict changes.
Pattern: A rule and its failure row give different holding-back conditions for the same input.

**Verifier:** R2-14 | Style only | Nit | The finding is in the Ambiguous class, which needs two verdicts on one trajectory, and it says itself "No verdict changes". In CO-S08 a whole-order proposal or a whole-order question gets the same answer under User knows, "Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it.", because questions are matched on meaning (§5.2). CO-S08 has no confirmation-form pair, so no confirmation can happen. "CO-A2 at any point" and the other Forbidden lines grade both paths the same way.

**Decision:** kept (Nit) — status: fixed. Reason: Kept against Style only: a rule and its failure row stating different holding-back conditions is an inconsistency between two lines, not wording or preference.
