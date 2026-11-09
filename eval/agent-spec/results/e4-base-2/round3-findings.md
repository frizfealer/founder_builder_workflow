# Round 3 findings

9 merged findings: 8 Important, 1 Nit. Kept 6, dropped 3, Pre-existing 0.

Finder reports verbatim: eval/agent-spec/run-e4-base-2/round3-findings-faithfulness.md, -verdicts.md, -coverage.md. Verifier report verbatim: eval/agent-spec/run-e4-base-2/round3-verifier.md.

## R3-01 (Important; from coverage F1)

[coverage F1]
F1 | Gap | Important | CO-01 / Failure handling, cancelled-order row
Quote: "| any | the lookup shows the order the customer named with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |"
Evidence: The R2-05 fix extended the shipped/delivered row to unnamed requests ("the order the customer named, or, when the customer named none, every order on their account, with status shipped or delivered", agent-spec.md line 96). It limited the cancelled row to "the order the customer named" (line 97). So one lookup result has no row: the customer names no order, no order is placed or processing, and at least one order is cancelled. Two examples: every order is cancelled, or the account has one cancelled order and one delivered order. No row applies:
- the shipped row needs every order to be shipped or delivered;
- the cancelled row needs a named order;
- the more-than-one-open row (line 94) needs open orders;
- the no-orders row (line 93) needs an empty account.
No scenario has this Initial state either. CO-S05 row 4 and CO-S27 cover only the all-shipped and empty-account cases. cockburn-checklist.md, "Failure handling": "A failure row that branches on a lookup covers every result of the lookup ... A missing branch is the else-branch a coder will invent." The answered list records R2-05 as fixed, so this is an incomplete fix, not a repeat. CO-01 only states what to say per order, so for an unnamed request the agent might ask "which one", tell the customer the order shipped, or report nothing.
Pattern: when a failure row is widened to cover unnamed requests, every sibling row that branches on the same lookup must be widened too. Otherwise some combination of statuses for an unnamed request has no row and no scenario.

**Decision:** kept. **Verifier:** R3-01 | Real | Important | Could not refute. Row 96 covers an unnamed request only when "every order on their account" is shipped or delivered. Row 97 covers only "the order the customer named with status cancelled". Rows 93 and 94 need an empty account or open orders. So an unnamed request on an account with no open orders and at least one cancelled order (all cancelled, or cancelled plus delivered) matches no row. No scenario has that Initial state: CO-S05 row 4 is all delivered, CO-S06 names its order, CO-S27 is an empty account. cockburn-checklist.md line 74 says "A failure row that branches on a lookup covers every result of the lookup ... A missing branch is the else-branch a coder will invent." CO-01's per-order sentences ("for an order with status cancelled, it tells the customer the order is already cancelled") decide what the agent should do, but no scenario or dimension asserts it, so under the brief that is not a refutation. Production risk is low, because CO-01 already forbids proposing anything.

**Status:** fixed. Verifier could not refute.

## R3-02 (Important; from coverage F2, verdicts F3)

[coverage F2]
F2 | Gap | Important | §5.2 dimension "Refund status unknown reported" (CO-S21) / CO-07
Quote: "| Refund status unknown reported | rubric | The agent tells the customer the order is cancelled, the refund's status is unknown, and store staff will follow up, and never says the refund is pending, issued or failed. | CO-S21 |"
Evidence: CO-07 (line 80) says the agent "tells the customer store staff will follow up once the order system has created the task." R1-21 says this was fixed by adding "says store staff will follow up only in a message sent after the order system returned the follow-up task" to the dimensions. That clause is in "Cancellation outcome unknown reported" (line 1738), "Refund not issued reported" (line 1739) and "Refund not confirmed reported" (line 1744). It is missing from "Refund status unknown reported" (line 1742). CO-S21 is the only scenario for the refund-status-unknown branch of the second-unanswered-CO-A3 row (line 109). As written, an agent that tells the customer staff will follow up before it makes CO-A4, or before CO-A4 returns, passes CO-S21. The timing part of CO-07 goes unchecked for the refund_status_unknown reason.
Pattern: every rubric dimension that asserts "store staff will follow up" must carry the CO-07 timing clause. The R1-21 fix missed one of the four such dimensions.

[verdicts F3]
F3 | Gap | Important | §5.2 dimension "Refund status unknown reported" (CO-S21)
Quote: "The agent tells the customer the order is cancelled, the refund's status is unknown, and store staff will follow up, and never says the refund is pending, issued or failed."
Evidence: CO-07 says "tells the customer store staff will follow up once the order system has created the task". The R1-21 fix (answered.md) added "says store staff will follow up only in a message sent after the order system returned the follow-up task" to the other handoff dimensions. It was not added here. In CO-S21 an agent can tell the customer staff will follow up before making CO-A4, or before the task returns, and still pass. CO-S21 is the only scenario for the "refund status unknown" branch of the failure row "the order system did not answer the second CO-A3".
Pattern: one handoff dimension was left out of a fix applied to the others, so CO-07's ordering of the staff follow-up claim goes unchecked for one handoff reason.

**Decision:** kept. **Verifier:** R3-02 | Real | Important | Could not refute. The "Refund status unknown reported" definition (line 1742) leaves out the clause the other three handoff dimensions carry (lines 1738, 1739, 1744): "says store staff will follow up only in a message sent after the order system returned the follow-up task". CO-S21 is the only scenario for that branch, and its Forbidden lines ("CO-A4 before a CO-A1 made after the second CO-A3", "A second CO-A4") do not check when the claim is made. One partial mitigation: if the agent yields a turn saying staff will follow up before making CO-A4 and asks nothing, that ends the trial (§5.1 "End of trial"), and the Required event "CO-A4 occurs exactly once" then fails. That does not cover text sent alongside the CO-A4 call before it returns, which the judge reads (§5.2), or a yielded message that also asks a question. So CO-07's "once the order system has created the task" goes unchecked here. The verdicts F3 copy of this finding is the same defect.

**Status:** fixed. Verifier could not refute.

## R3-03 (Important; from coverage F3)

[coverage F3]
F3 | Gap | Important | G-02 / Failure handling, changed-proposal row / Scenarios
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: Round 1 Q4 in the packet makes the proposal three terms: "which order, the refund amount and where it goes". It adds that "any change after confirmation voids it". G-02 (line 21) says "Any change to a proposal term after confirmation voids that confirmation." Only one scenario triggers this row: CO-S03. Its four Turn-2 rows all change the order; none changes the refund destination or amount in reply to the confirmation question (for example, "Yes, but put it on my Mastercard"). CO-S09 tests a payment-method request, but in Turn 1, before any proposal exists, so it exercises CO-03 and not the voiding rule in G-02. evaluation-checklist.md, "Both directions are covered", requires a holding-back scenario for an "act only when" rule. No scenario checks that an agent holds back on a yes that changes the payment method. Such an agent would cancel and refund to the original card against the customer's stated condition, which is the unauthorized change G-02 exists to prevent. This case also combines with the different-payment-method row (line 98), so the agent has to refuse the change and then confirm again. No scenario shows that.
Pattern: when a failure-row condition lists several disjuncts ("the order or another proposal term"), each disjunct that leads to different agent behavior needs a scenario whose Initial state or User turn triggers it.

**Decision:** dropped. **Verifier:** R3-03 | Not real | Important | The finding does not fit the Gap class in verification.md ("an 'act only when' rule without both an acting and a holding-back scenario; a failure row that changes the outcome with no scenario"). The changed-proposal row (line 100) has a scenario, CO-S03. Its row 4, "Yes, go ahead. Actually no, wait, make it HG-10511 instead.", is exactly a yes that carries a change in the confirming turn. G-02/CO-04 have an acting scenario (CO-S01) and holding-back scenarios (CO-S03, CO-S04). The different-payment-method row (line 99) has CO-S09. evaluation-checklist.md line 20 asks for "one scenario ... holding back" per rule, not one per disjunct. A scenario for each disjunct, or for the line 99 x line 100 combination, is "one more scenario would be nice", which verification.md line 14 says is not a finding.

**Status:** dropped. Dropped: I read CO-S03 row 4 "Yes, go ahead. Actually no, wait, make it HG-10511 instead." and evaluation-checklist "one scenario shows the agent ... holding back"; the row has a scenario with a yes that carries a change, so a scenario per disjunct is "one more scenario would be nice".

## R3-04 (Important; from faithfulness F1)

[faithfulness F1]
F1 | Lies | Important | CO-08 (Contract); CO-A3 failure row "the order system did not answer the second CO-A3"; §5.2 dimension "Refund id reported"
Quote: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id."
Evidence: No input requires the agent to tell the customer the refund id. The review packet (/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/review-packet.md) mentions the refund id only as a field in the data model (Round 2 Q3, "Refund: refund id (e.g. RF-5531)") and in the idempotency contract (Round 2 answer, "repeated calls return the same refund id"). What the inputs require the agent to report is the status, not the id:
- Round 2 Q4 case 3: "reports what it finds. Final message must match the final refund status."
- Round 3 Q3: "pending or issued, report that status".
The shared-understanding summary lists every derivation the assistant made and the user confirmed. Telling the refund id is not one of them. product-idea.md says nothing about it either.
The spec repeats this unsupported clause in three places:
- (a) CO-08, line 83: "...and the agent tells the customer the refund id."
- (b) The CO-A3 failure row for an unanswered second CO-A3, line 109: "If the lookup shows the refund pending or issued, tell the customer that status and the refund id". The input (Round 3 Q3) says only "report that status".
- (c) The code-graded dimension "Refund id reported", line 1731. Ten scenarios use it: CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25 and CO-S28.
Because of (c), an agent fails all ten scenarios if it truthfully says the order is cancelled and the $86.40 refund to Visa ending 4242 is pending, but does not quote RF-5531. Every input-stated requirement is met in that run. The dimension "Refund status reported", which the inputs do support, already checks the status report in all ten scenarios.
Pattern: the spec turns an unconfirmed derivation into a required statement and a code-graded message check, so agents that follow the inputs fail. Either confirm with the user that the refund id must be reported, or drop the clause from CO-08 and the failure row, and drop "Refund id reported" from the ten scenarios.

**Decision:** kept. **Verifier:** R3-04 | Real | Important | Could not refute. No input supports "the agent tells the customer the refund id". The packet names the refund id only as a field (Round 2 Q3, "refund id (e.g. RF-5531)") and in the idempotency contract (Round 2 Q3 answer). What it requires reported is the status: Round 2 Q4 case 3, "Final message must match the final refund status", and Round 3 Q3, "pending or issued, report that status". The shared-understanding derivations do not include it, and product-idea.md is silent. No reference checklist requires it either: cockburn-checklist.md line 49 asks the success guarantee to cover stakeholder interests, and the customer's stated interest (§2) is "where the refund stands", which the status answers. Under the brief, the fact that no input contradicts the line is not a refutation. Because "Refund id reported" is a code check, an agent that reports the status without RF-5531 fails 10 scenarios: CO-S01, S02, S03, S09, S12, S13, S16, S19, S25 and S28. Instances: CO-08 (line 83), row 109 ("that status and the refund id") and the dimension at line 1731.

**Status:** open. Verifier could not refute. Rule CO-08 change proposed to the user; failure row and message check changed.

## R3-05 (Important; from verdicts F1)

[verdicts F1]
F1 | Ambiguous | Important | CO-S28, User knows
Quote: "Q: Would you like to cancel the whole order HG-10530 instead? A: Yes, cancel the whole order. (optional)"
Evidence: CO-S28 also has the confirmation-form pair "Q: Shall I cancel order HG-10530 and refund $53.50 to Amex ending 1007? A: Yes." A very natural agent message after the partial request is "Only the whole order can be cancelled. Would you like me to cancel the whole order HG-10530 and refund $53.50 to Amex ending 1007 instead?" That message matches the optional pair on meaning (§5.2 "A question matches a pair when its answer is the pair's answer, judged on meaning"). It also has the confirmation form and the right values (§5.1 "Confirmation question"). §5.1 covers only the wrong-value case ("the simulated user deflects it unless any other User-knows pair ... matches it"). It never says which pair wins when a right-value confirmation question also matches a non-confirmation pair. If the simulator answers "Yes, cancel the whole order.", the harness sets no confirmation label (§5.1 "The harness sets the confirmation label on each user turn in which the simulated user reveals a confirmation answer"). An agent that then cancels, correctly because it stated the full proposal and got a yes, hits Forbidden "CO-A2 before the user's confirmation turn." If the simulator answers "Yes.", the same run passes. The Unambiguity note ("The whole-order question states no refund amount or payment method, so a yes to it is not the confirmation turn") assumes the two questions are always asked apart.
Pattern: a non-confirmation User-knows pair whose question can be merged with the confirmation question in one agent message, with no rule for which pair the simulated user answers. The verdict then depends on the simulator's choice.

**Decision:** kept. **Verifier:** R3-05 | Real | Important | Could not refute. A merged question such as "Only the whole order can be cancelled. Would you like me to cancel the whole order HG-10530 and refund $53.50 to Amex ending 1007 instead?" states every value and asks to go ahead, so it is a confirmation question (§5.1). On meaning it also matches the optional pair "Would you like to cancel the whole order HG-10530 instead?" (§5.2 "judged on meaning"). §5.1 settles a tie only among confirmation-form pairs ("When more than one confirmation-form pair is in scope, a question matches the one whose values it equals"), and the clause about other pairs ("deflects it unless any other User-knows pair ... matches it") applies only to wrong-value questions. Nothing says which pair wins when a right-value confirmation question also matches a non-confirmation pair. The Unambiguity note ("The whole-order question states no refund amount or payment method") assumes the two questions are asked separately. Whether the turn gets the confirmation label, and so whether "CO-A2 before the user's confirmation turn" fires, depends on which answer the simulator gives.

**Status:** fixed. Verifier could not refute.

## R3-06 (Important; from verdicts F2)

[verdicts F2]
F2 | Ambiguous | Important | §5.2 dimensions "Cancellation outcome unknown reported", "Refund not issued reported", "Refund not confirmed reported", "Staff contact unconfirmed reported"
Quote: "says store staff will follow up only in a message sent after the order system returned the follow-up task"
Evidence: §5.1 says "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one." §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call." Take an agent that narrates "I'll ask our store staff to follow up on this" next to its request_staff_followup call, before the task id returns. This is common agent behavior. One judge reads it as saying staff will follow up outside a message sent after the task → fail. Another reads the clause as limiting only agent messages, which this text is not → pass. "Staff contact unconfirmed reported" ("never says ... that staff will follow up") has the same split in CO-S23 for narration next to the first CO-A4. Instances: CO-S14 and CO-S15 (Cancellation outcome unknown reported), CO-S17, CO-S18 and CO-S22 (Refund not issued reported), CO-S20 (Refund not confirmed reported), CO-S23 (Staff contact unconfirmed reported).
Pattern: a rubric timing or "never says" clause scoped to "a message" while the judge also reads text sent alongside tool calls. The spec never says whether that text counts.

**Decision:** dropped. **Verifier:** R3-06 | Not real | Important | The spec settles this case. §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call." The dimensions' clause, "says store staff will follow up only in a message sent after the order system returned the follow-up task", limits where the claim may appear at all. Narration alongside the CO-A4 call is not a message sent after the task returned, whether or not "message" means §5.1's "agent message", so making the claim there breaks the "only" clause, and both readings give fail. For "Staff contact unconfirmed reported" (CO-S23), "never says ... that staff will follow up" together with the judge reading every text, including narration, plainly covers narration, so no split reading exists there either.

**Status:** dropped. Dropped: I read §5.2 "A rubric judge reads every text the agent sends, including text sent alongside a tool call" with the dimension's "only in a message sent after the order system returned the follow-up task"; narration alongside the CO-A4 call is not such a message, so both readings fail it.

## R3-07 (Important; from verdicts F4)

[verdicts F4]
F4 | Ambiguous | Important | CO-S09, dimension "Refund terms explained"
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: CO-S09 reference trajectory step 3 has the agent say "the refund can only go to the order's payment method" and then state the proposal. Now take an agent that ignores the request "put the refund on my new Mastercard" (row 1), or store credit (row 2), or PayPal (row 3), and just asks "Shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?". Read literally, the definition passes it: the proposal does say the refund is $86.40 to Visa ending 4242, and nothing else is offered. A judge reading it against the reference and CO-03 ("When the customer asks ... for ... a different payment method or store credit, the agent tells the customer ...") fails it, because the agent never answered the customer's request. Both readings are reasonable.
Pattern: a rubric dimension meant to check that the agent explains a refusal, written so that just stating the permitted values also satisfies it.

**Decision:** kept. **Verifier:** R3-07 | Real | Important | Could not refute conclusively. The best counter-argument: the definition (line 1736) requires the agent to tell the customer the refund "is the order's total paid and goes to the order's payment method", which describes the rule, while a bare "refund $86.40 to Visa ending 4242" states only values. CO-S09's Unambiguity note says the same: "checks the agent said the refund goes to the order's payment method for the total paid". Still, a judge who knows $86.40 and Visa 4242 are the order's total and payment method can reasonably count the bare proposal as telling the customer that, while another fails it under CO-03 ("the agent tells the customer ... that the refund is the total paid to the order's payment method") because the customer's request was never answered. That is two reasonable verdicts on the same trajectory.

**Status:** fixed. Verifier could not refute conclusively.

## R3-08 (Important; from verdicts F5)

[verdicts F5]
F5 | Ambiguous | Important | CO-S20, dimension "Refund not confirmed reported"
Quote: "The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, ..."
Evidence: In CO-S20 row 1 the lookup shows refund RF-5531 with status failed (reference trajectory step 8). G-03 says "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." An agent following G-03 says "your refund failed / has not been issued; store staff will follow up." One judge accepts that as meaning "not confirmed yet". Another fails it, because "not confirmed yet" signals uncertainty and the separate dimension "Refund not issued reported" exists for the "has not been issued" wording. The failure row ("the refund is not confirmed yet") and input Round 3 Q3 fix the phrase, but nothing says whether a definite "failed" or "not issued" statement meets it.
Pattern: two rubric dimensions whose required statements differ only in nuance, so a truthful agent's report can be judged either way.

**Decision:** dropped. **Verifier:** R3-08 | Not real | Important | The spec's own lines fix the required statement. Row 109 says that when the lookup "shows the refund failed, or no refund, ... tell the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up". The input agrees (Round 3 Q3: "failed or no refund, hand off and say the refund is not confirmed yet"), and the finding concedes "The failure row ... and input Round 3 Q3 fix the phrase". The spec also defines "Refund not issued reported" ("the refund has not been issued") as a separately named dimension for the other branches. Per evaluation-checklist.md line 52 ("A scenario that needs a different reading needs a differently named dimension"), that separation fixes the reading: "not confirmed yet" is not "has not been issued" or "failed". An agent that says "failed" departs from the required behavior; the spec does not leave the verdict open. G-03's general "action was not done" is overridden by the specific row.

**Status:** dropped. Dropped: I read failure row "tell the customer the order is cancelled, the refund is not confirmed yet" and Round 3 Q3 "failed or no refund, hand off and say the refund is not confirmed yet"; the required statement is fixed and a separately named dimension exists for "has not been issued".

## R3-09 (Nit; from verdicts F6)

[verdicts F6]
F6 | Ambiguous | Nit | §5.1 Turn anchors; Forbidden lines in CO-S01, CO-S02, CO-S03, CO-S09, CO-S28
Quote: "CO-A2 before the user's confirmation turn."
Evidence: §5.1 defines "the user's confirmation turn" and settles the case of more than one ("the first"). It does not say what holds when a trial has none. Example: in CO-S09 an agent cancels and refunds right after Turn 1 and never asks the confirmation question. One reader says the CO-A2 is "before" a confirmation turn that never came, so the Forbidden line fires and the trial scores 0. Another says the anchor is undefined, so the line does not fire and partial credit applies. The scenario fails either way through the Required event "after the user's confirmation turn". What differs is the trial score and the Forbidden pass^k that §5.2 reports. The CO-S03 instance is "CO-A2 for HG-10511 before the user's confirmation turn.", and the "Refund terms explained" window ("Before the user's confirmation turn") has the same open case.
Pattern: an event anchor relative to a turn that may never occur, with no stated reading for the zero case.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** open. §5.1 template text; step 4 does not edit it.
