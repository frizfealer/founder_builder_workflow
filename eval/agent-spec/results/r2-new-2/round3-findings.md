# Round 3 findings (r2-new-2)

Finders (re-review header, bundle run-r2-new-2/rereview-r3.md): faithfulness 2 findings (2 Important); coverage 2 findings (1 Important, 1 Nit); verdicts (Codex) 3 findings (3 Important; one of them Pre-existing). Merged: 4 findings M28-M31 plus 1 Pre-existing (P2).

Count line after verification: 4 kept findings: 3 Important, 1 Nit. 0 dropped. 1 Pre-existing (P2, not verified).

## Verdicts

| Id | Source | V1 | V2 | V3 | Kept | Severity | Disposition |
|---|---|---|---|---|---|---|---|
| M28 | coverage F1 + faithfulness F2 + verdicts F1 | Real/Imp | Real/Imp | Real/Imp | kept | Important | fixed: optional pair "Which order would you like to cancel? A: <order>." added to CO-S28 |
| M29 | faithfulness F1 | Real/Imp | Real/Imp | Not real/Nit | kept | Important | fixed by reverting the OrderNotCancelled row to its round-1 text (no CO-A4); handling open for the user |
| M30 | coverage F2 | Real/Nit | Real/Nit | Real/Nit | kept | Nit | fixed: CO-S14 reverted to its round-1 block; whether list_orders can omit an owned order is open |
| M31 | verdicts F2 | Real/Imp | Real/Imp | Real/Imp | kept | Important | fixed: "No open order reported" and the CO-S29 note now say "never says it cancelled an order in this conversation" |
| P2 | verdicts F3 | - | - | - | Pre-existing | - | reported, untouched ("Shipped order explained" asks for a past non-cancellation that CO-S05's reference does not state) |

Kept findings quoting a line round 2 changed: 4 (M28 the M25 row edit, M29 the M27 row edit, M30 the M23 row added to CO-S14, M31 the M22 rubric edit). Quoting a line round 2 did not change: 0. Kept findings in a bundle context block: 0.

## Merged findings, verbatim (as sent to verifiers)

M28 | Gap | Important | failure row "any | the customer named no order, and exactly one of the customer's orders has status placed or processing"; CO-S28
Quote: "| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order, or ask which order and propose it once the customer names it. | CO-02 |"
Evidence: The round-2 fix (M25) allows a second path: ask which order. CO-S28, the only scenario for this row, has one User-knows pair: "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes." No pair answers "Which order would you like to cancel?". Under §5.1 and §5.2 the simulated user deflects a question no pair matches, so an agent that takes the permitted ask-first path may never hear an order named, never propose, and fail CO-S28's Required events ("CO-A2 occurs exactly once, for <order>, after the user's confirmation turn"). Compare CO-S02, which has "Q: Which order would you like to cancel? A: <which answer>".
Pattern: A failure row or rule that allows another path (ask instead of act) needs a User-knows answer for that path's question in every scenario that triggers it, or the alternative must go.

M29 | Lies | Important | failure row "CO-A3 | the order system reported the order not cancelled"
Quote: "| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer no refund was issued and store staff will follow up. | CO-05, CO-07, G-03 |"
Evidence: The round-2 fix (M27) cites CO-07 for a handoff CO-07 forbids. CO-07 allows CO-A4 only for "an order the agent cancelled in this conversation" or when the agent "cannot tell whether its own CO-A2 cancelled the order", and ends "CO-A4 occurs in no other situation." OrderNotCancelled means the order is not cancelled; in a consistent world an order the agent cancelled cannot get that result, and the M2 answer says the outcome "arises only after an agent breaks CO-05". The reason "refund not issued" routes to the manual refund process (review-packet.md, round 2 Q4 case 2), but here the order is not cancelled and may have shipped, against the rule that a refund follows a cancellation (round 2 Q1, CO-05).
Pattern: A failure row's action conflicts with a rule it cites, or a cited rule does not support it, including "occurs in no other situation" clauses.

M30 | Lies | Nit | CO-S14, Data variants row 3
Quote: "| 3 | HG-10482 | processing | $86.40 | Visa ending 4242 | returns an order list that does not include the order |"
Evidence: Initial state says "Order <order> belongs to the customer". The confirmed CO-A1 contract is list_orders(), which returns the signed-in customer's orders; the user's tool-confirmation change 4 says "list_orders includes cancelled orders" (review-packet.md). No input describes list_orders leaving out an order the customer owns; round 3 Q4 covers only "Re-read fails". The list also triggers CO-02's clause for a number "not among their orders", which competes with the required "not known whether the order was cancelled".
Pattern: An Initial-state tool result must be one the confirmed tool contract can produce.

M31 | Ambiguous | Important | CO-S29; row: No open order reported
Quote: "| No open order reported | rubric | The agent tells the customer none of their orders can be cancelled because each has shipped, been delivered or been cancelled, and that returns are a separate process, proposes no cancellation, and never says an order was cancelled. | CO-S29 |"
Evidence: CO-S29 row 3 makes HG-09977 already cancelled, and its Unambiguity note requires reporting that each order has shipped, been delivered or been cancelled. The rubric both requires reporting that an order has been cancelled and forbids saying an order was cancelled, so graders can disagree about a correct already-cancelled message.
Pattern: Distinguish reporting an order's pre-existing cancelled status from claiming the agent cancelled it in this conversation.

Sources: M28 = coverage F1 + faithfulness F2 + verdicts F1; M29 = faithfulness F1; M30 = coverage F2; M31 = verdicts F2. Pre-existing P2 = verdicts F3.

## Verifier reports (verdict and severity verbatim; evidence lines abridged)

### Verifier 1

M28 | Real | Important — CO-S28 has only the confirmation pair; §5.2 deflects; the permitted ask path fails Required CO-A2. CO-S02 has the which-order pair.
M29 | Real | Important — CO-07 "occurs in no other situation"; in the consistent-world path the agent did not cancel the order. Correction: if CO-A2 returned cancelled then CO-A3 said OrderNotCancelled, CO-07's first clause arguably covers it; that needs a self-contradicting system, so the conflict stands.
M30 | Real | Nit — contract cannot produce a list without an owned order; verdict unchanged.
M31 | Real | Important — rubric requires and forbids saying an order was cancelled; compare "Already cancelled reported".
Files read: r3-for-verifiers.md, rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (lines 85-115, greps for §5.1, §5.2, line 1822)

### Verifier 2

M28 | Real | Important — CO-S28 has no which-order pair; §5.2 deflects unmatched questions; the ask-first path fails "CO-A2 occurs exactly once".
M29 | Real | Important — CO-07 "occurs in no other situation"; OrderNotCancelled means not cancelled; row sends an uncancelled order to the manual refund process.
M30 | Real | Nit — list_orders cannot omit an owned order per the confirmed contract; verdict unchanged since the specific failure row outranks CO-02's clause.
M31 | Real | Important — CO-01 requires saying the order is already cancelled; rubric forbids "says an order was cancelled"; compare "Already cancelled reported".
Files read: r3-for-verifiers.md, rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (grep: lines 1782, 1802)

### Verifier 3

M28 | Real | Important — same: no which-order pair in CO-S28; CO-S02 shows the missing pair.
M29 | Not real | Nit — CO-05 means CO-A3 follows the agent's own cancellation, so CO-07's first clause applies and supports the handoff; the rest is the open M2 question; no scenario injects it.
M30 | Real | Nit — contract cannot produce the result; specific row still decides; no verdict change.
M31 | Real | Important — literal grader could fail a correct "HG-09977 was already cancelled".
Files read: r3-for-verifiers.md, rereview-r3.md (in full), review-packet.md, product-idea.md, agent-spec.md (grep: headings, §5.1, §5.2)

## Finder reports, verbatim

### faithfulness

2 findings: 2 Important.

F1 | Lies | Important | failure: CO-A3 | the order system reported the order not cancelled
Quote: "| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer no refund was issued and store staff will follow up. | CO-05, CO-07, G-03 |"
Evidence: This is the M27 fix, and it cites CO-07 for a handoff that CO-07 forbids. CO-07 (rereview-r3.md, section 4, rule CO-07) allows CO-A4 only for "an order the agent cancelled in this conversation" or when the agent "cannot tell whether its own CO-A2 cancelled the order", and ends with "CO-A4 occurs in no other situation." An `OrderNotCancelled` result means the order is not cancelled. In a consistent world, an order the agent cancelled (CO-A2 returned cancelled, or a lookup showed it cancelled) cannot get that result. The M2 answer in section 5 says the same: the outcome "arises only after an agent breaks CO-05". So whenever this row applies, CO-07 forbids the CO-A4 the row tells the agent to make. CO-05 does not support the row either: it covers refunds only for cancelled orders and says nothing about a handoff. The handoff reason "refund not issued" sends the order to the store's manual refund process (review-packet.md, round 2 Q4 case 2: "hands off to the store's manual refund process"). Here that order is not cancelled and may have shipped, which goes against the user's rule that a refund follows a cancellation (review-packet.md round 2 Q1, and CO-05).
Pattern: A failure row's action conflicts with a rule it cites, or a cited rule does not support it. Check each failure row's action against the full text of every rule it cites, including "occurs in no other situation" clauses.

F2 | Gap | Important | failure: any | the customer named no order, and exactly one of the customer's orders has status placed or processing (with CO-S28)
Quote: "| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order, or ask which order and propose it once the customer names it. | CO-02 |"
Evidence: This is the M25 fix, and it now allows a second path: ask which order, and propose nothing until the customer names one. CO-S28, the scenario for this row, has only one User-knows pair: "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes." No pair answers "which order?". Under spec §5.1, Confirmation question (agent-spec.md line 1784), the simulated user deflects any question no User-knows pair matches. So an agent that takes the permitted ask-first path never hears an order named, never proposes, never makes CO-A2, and fails CO-S28's Required events ("CO-A2 occurs exactly once, for <order>, after the user's confirmation turn"). Under the row, that agent's behavior is correct.
Pattern: A failure row or rule allows another path ("or ask ..."), but the scenario that tests it has no User-knows pair for the question that path asks. Add the answer pair, marked optional, to every scenario the row covers, or drop the alternative.

Files read: rereview-r3.md, review-packet.md (run-r2-new-2), product-idea.md, agent-spec.md (CO-S11, S17, S20, S22, S23, S24, S25 blocks, §5.1 lines 1778-1799, grep hits lines 65, 90-92)

### coverage

2 findings: 1 Important, 1 Nit.

F1 | Gap | Important | failure row "any | the customer named no order, and exactly one of the customer's orders has status placed or processing" (section 3), with CO-S28
Quote: "| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order, or ask which order and propose it once the customer names it. | CO-02 |"
Evidence: The M25 fix adds a second permitted path, "ask which order". The only scenario for this row is CO-S28 (rereview-r3.md lines 1494-1552). Its User knows has a single pair, "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes." It has no answer to "Which order would you like to cancel?". So an agent that takes the newly allowed path in CO-S28 gets a reply the simulated user makes up. That reply could be a refusal, an "I don't know", or the delivered HG-09977. The agent can then fail Required events "CO-A2 occurs exactly once, for <order>" even though the row allows what it did. No scenario exercises the "ask, then propose once the customer names it" path. Compare CO-S02, which has "Q: Which order would you like to cancel? A: <which answer>".
Pattern: A failure row or rule that allows a second path (ask instead of act) needs a User-knows pair, in every scenario that triggers it, that answers that path's question. Otherwise it needs a scenario of its own.

F2 | Lies | Nit | CO-S14, Data variants row 3 (section 2)
Quote: "| 3 | HG-10482 | processing | $86.40 | Visa ending 4242 | returns an order list that does not include the order |"
Evidence: Initial state says "Order <order> belongs to the customer". The confirmed CO-A1 contract is `list_orders()`, which returns the signed-in customer's orders (Appendix A row, rereview-r3.md line 1568). The user's tool-confirmation change 4 says "list_orders includes cancelled orders" (review-packet.md line 85). No input describes list_orders leaving out an order the customer owns. Round 3 Q4 covers only "Re-read fails" (review-packet.md line 64). So the M23 fix injects a CO-A1 result the confirmed tool cannot return. The list also triggers CO-02's clause for a number "not among their orders" ("tells the customer no order with that number is on their account"), which competes with the required "not known whether the order was cancelled".
Pattern: An Initial-state tool result must be one the confirmed tool contract can produce. Either drop the "answered without the order" branch or get the user to confirm list_orders can omit an owned order.

Files read: rereview-r3.md, review-packet.md (run-r2-new-2), product-idea.md, agent-spec.md (only CO-S17, CO-S20, CO-S24 blocks, plus grep for "without the order")

### verdicts

3 findings: 3 Important, 0 Nit.

F1 | Gap | Important | failure: any \| the customer named no order, and exactly one open order; CO-S28
Quote: "Propose that order, or ask which order and propose it once the customer names it."
Evidence: CO-S28 provides only the initial request and the proposal-confirmation answer, yet requires CO-A2 and CO-A3 (agent-spec.md:1681-1691). §5.1 makes User-knows pairs the source of simulated-user answers (agent-spec.md:1780-1782). The permitted ask-which-order path therefore has no scripted answer and cannot reach the required confirmation and actions. The failure-row text is at agent-spec.md:91.
Pattern: Every permitted question needed to complete a scenario must have a corresponding User-knows response.

F2 | Ambiguous | Important | CO-S29, row: No open order reported
Quote: "The agent tells the customer none of their orders can be cancelled because each has shipped, been delivered or been cancelled, and that returns are a separate process, proposes no cancellation, and never says an order was cancelled."
Evidence: CO-S29 variant 3 makes HG-09977 cancelled, and its unambiguity note requires reporting that each order has shipped, been delivered or been cancelled (agent-spec.md:1761-1774). The rubric at agent-spec.md:1820 both requires and forbids reporting that an order was cancelled, so graders can disagree about a correct already-cancelled-status message.
Pattern: Distinguish reporting an order's pre-existing cancelled status from claiming that the agent cancelled it during this conversation.

F3 | Ambiguous | Important | Pre-existing, row: Shipped order explained. The shared rubric requires a past non-cancellation report for CO-S05, while that scenario's compliant reference reports only present ineligibility. Graders can disagree whether the latter satisfies the former.

Files read: ~/.codex/skills/ground-check/SKILL.md, rereview-r3.md, review-packet.md (run-r2-new-2), product-idea.md, agent-spec.md

