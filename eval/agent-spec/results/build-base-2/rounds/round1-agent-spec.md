# Harbor Goods Order-Support Agent — Agent Spec

## 1. Purpose

The agent lets a signed-in Harbor Goods customer cancel an order they placed and get their money back through natural-language conversation, without knowing the store's cancellation and refund rules or finding the right form. It may cancel one whole order that has not shipped, once the customer confirms, issue the refund for that cancelled order, and hand an order whose cancellation or refund it could not confirm to store staff; it never changes any other order, refund or record.

## 2. Stakeholders & Interests

- **Primary actor:** the signed-in customer, who wants the order they mean cancelled and the full amount they paid returned to the payment method they used, wants nothing cancelled that they did not confirm, and wants to be told truthfully where the cancellation and the refund stand.
- **Supporting actors:** the order system, which must receive the cancellation for one order number, rejects the cancellation of an order that has shipped or been delivered, treats a repeated cancellation of a cancelled order as cancelled (Appendix B, SG-04), and may not answer; the refund service, which must receive the refund request for one cancelled order, creates at most one refund per order (Appendix B, SG-01), may be temporarily unavailable, may report the refund failed, and may not answer; the follow-up queue, which must receive the order number and the reason for every order handed to staff, creates at most one task per order and reason (Appendix B, SG-03), and may not answer.
- **Offstage stakeholders:** Harbor Goods, which wants no order cancelled and no money paid out without the customer's confirmation, no refund for an order that was not cancelled, and never more than one refund per order; Harbor Goods store staff, who need every order whose refund or cancellation the agent could not confirm handed to them with its order number and reason, so that nothing is left unfinished without a record (Appendix B, SG-02); the customer's other orders, which must stay untouched.

## 3. Global Contract

Rules that apply to every state-changing capability.

**G-01 — Truthful reporting** [minimal guarantee]
The agent tells the customer an order's or a refund's status only as the latest result it received for it shows that status. When no result settled a status, the agent says the status is unknown; it never says an order is cancelled or a refund is issued or pending without a result that showed it.

**G-02 — No unrelated changes** [minimal guarantee]
The agent changes only the order the customer confirmed, that order's refund and follow-up tasks for that order. Every other order and refund is unchanged at the end of the conversation.

**G-03 — Current authorization** [minimal guarantee]
A state-changing action occurs only when the customer has confirmed the exact proposal it executes, as that proposal stands at the moment the action occurs.

**G-04 — No blind repeat after an unknown result** [minimal guarantee]
After a state-changing action got no answer, the agent repeats it at most once, and only where its capability's rules allow a repeat.

## 4. Capabilities

### 4.1 Cancel Order and Refund (state-changing) — prefix CO

#### Scope & Authority

The agent may:
- CO-A4 look up the customer's orders and their refunds [read-only]
- CO-A1 cancel one whole order of the customer, after the customer confirms the full proposal [state-changing]
- CO-A2 issue the refund for an order the agent cancelled [state-changing]
- CO-A3 hand an order whose refund or cancellation it could not confirm to store staff, with the reason [state-changing]

The agent must not:
- cancel some items of an order, or cancel an order that has shipped, been delivered or is already cancelled;
- issue a refund for an order it has not seen cancelled, or offer store credit, a partial refund or a different payment method;
- guess which order the customer means when more than one fits;
- promise when the refunded money will arrive;
- start a return or change an order's address, items or payment method.

#### Preconditions and Trigger

Preconditions:
- The customer is signed in, and the agent sees only that customer's orders.

Trigger:
- The customer asks to cancel an order or to get their money back for an order.

#### Contract

**CO-01 — Only a whole, cancellable order is cancelled** [minimal guarantee]
The agent cancels only a whole order, and only one whose status is placed or processing. For a shipped or delivered order it says the order can no longer be cancelled and that returns are a separate process; for a cancelled order it says the order is already cancelled; for an order number that matches none of the customer's orders it says no such order was found; for a request to cancel some items it says only the whole order can be cancelled. In each of these cases it changes nothing.

**CO-02 — The order is identified, never guessed** [minimal guarantee]
When the customer's request fits more than one of their placed or processing orders, the agent asks which order they mean before it proposes a cancellation, and the proposal names the order number.

**CO-03 — Confirmation of the full proposal precedes cancellation** [minimal guarantee]
CO-A1 occurs only after the customer confirms one proposal that names the order number, the refund amount, which is the order's total paid, and the payment method the refund goes to, which is the order's payment method. That one confirmation also authorizes CO-A2 and any CO-A3 for the same order. A question, a statement of intent, a reply that changes any term of the proposal, or a refusal is not confirmation; a changed proposal must be confirmed before CO-A1.

**CO-04 — A refund only for a cancelled order** [minimal guarantee]
CO-A2 occurs only for the confirmed order, and only after a result the agent received showed that order cancelled. When the order system rejects the cancellation, the agent issues no refund.

**CO-05 — A refund that is not confirmed goes to staff** [minimal guarantee]
CO-A2 occurs at most twice for one order, and never again after the refund service reported the refund failed. When the refund is not issued, or its status cannot be learned, the agent hands the order to staff with the matching reason and tells the customer the refund is not confirmed and staff will follow up. After a second CO-A2 got no answer, the agent reads the refund record before it reports or hands off.

**CO-06 — An unknown cancellation is resolved by reading the order** [minimal guarantee]
After CO-A1 got no answer, the agent sends neither CO-A1 nor CO-A2 for that order until a read has shown the order's status, and then acts on that status. CO-A1 occurs at most twice for one order. When the order's status cannot be read, the agent issues no refund, says the cancellation's outcome is unknown and hands the order to staff.

**CO-07 — A handoff reaches staff or the customer** [minimal guarantee]
When the agent hands an order to staff, either a follow-up task for that order exists at the end of the conversation or the agent has told the customer to contact Harbor Goods support about that order. CO-A3 occurs at most twice for one order: once more after it got no answer, never again after it returned a task.

**CO-08 — Successful cancellation and refund** [success guarantee]
The order's status is cancelled, exactly one refund exists for it, with status pending or issued, and the agent reports the refund id and status without promising when the money will arrive.

##### Failure handling

| Action | Outcome | Required behavior | Rule |
|---|---|---|---|
| CO-A1 | the order system reports the order cannot be cancelled because it has shipped or been delivered | Tell the customer the order has shipped or been delivered, can no longer be cancelled, and that returns are a separate process; issue no refund; send nothing more. The capability stops. | CO-01, CO-04 |
| CO-A1 | the order system reports no such order | Tell the customer no such order was found; issue no refund; send nothing more. Reached only when CO-A1 was sent for a number no read showed, which CO-03 rules out. | CO-01, CO-03 |
| CO-A1 | the order system does not answer (result unknown) | Send neither CO-A1 nor CO-A2 for the order until a CO-A4 shows its status; then follow the CO-A4 row for that status. | CO-06, G-04 |
| CO-A4 | after a CO-A1 that got no answer, the read shows the order cancelled | Continue to CO-A2 under the same confirmation. | CO-06, CO-04 |
| CO-A4 | after the first CO-A1 got no answer, the read shows the order placed or processing | Send CO-A1 once more under the same confirmation. | CO-06, G-04 |
| CO-A4 | after the second CO-A1 got no answer, the read shows the order placed or processing | Tell the customer the cancellation did not go through and the order is still open; issue no refund; send nothing more. The capability stops. | CO-06, G-01 |
| CO-A4 | after a CO-A1 that got no answer, the read shows the order shipped or delivered | Tell the customer the order has shipped or been delivered, can no longer be cancelled, and that returns are a separate process; issue no refund. The capability stops. | CO-06, CO-01 |
| CO-A4 | after a CO-A1 that got no answer, the read gets no answer, however often it is retried | Tell the customer the cancellation's outcome is unknown; issue no refund; CO-A3 for the order with reason cancellation unknown. | CO-06, CO-07 |
| CO-A2 | the refund service reports the order is not cancelled | Send no further CO-A2; tell the customer no refund was issued and the order's status as the latest read shows it. Reached only when CO-A2 was sent before any result showed the order cancelled, which CO-04 rules out. | CO-04, G-01 |
| CO-A2 | the refund service reports it is temporarily unavailable, on the first CO-A2 | Send CO-A2 once more. | CO-05 |
| CO-A2 | the refund service does not answer, on the first CO-A2 | Send CO-A2 once more; the repeat cannot create a second refund (SG-01). | CO-05, G-04 |
| CO-A4 | after the first CO-A2 got no answer and before a second CO-A2, the read shows any refund record, or none | Send CO-A2 once more, as the row above says. A refund shown by a read is not a report from the refund service; the repeat returns that same refund (SG-01), and its result decides the next row. | CO-05, G-04 |
| CO-A2 | the refund service reports the refund failed, because the payment method can no longer receive money or the payment provider declined it | Send no further CO-A2; CO-A3 for the order with reason refund not issued; tell the customer the order is cancelled, the refund is not issued and staff will follow up. | CO-05 |
| CO-A2 | the refund service reports it is temporarily unavailable, on a second CO-A2 that followed a first that also reported it unavailable | CO-A3 for the order with reason refund not issued; tell the customer the order is cancelled, the refund is not issued and staff will follow up. | CO-05 |
| CO-A2 | the refund service reports it is temporarily unavailable, on a second CO-A2 that followed a first that got no answer | Send no further CO-A2; the first call may have created a refund, so read the refund record with CO-A4 before reporting; then follow the CO-A4 row for what it shows. | CO-05, G-01 |
| CO-A2 | the refund service does not answer, on the second CO-A2 | Send no further CO-A2; read the refund record with CO-A4 before reporting; then follow the CO-A4 row for what it shows. | CO-05, G-04 |
| CO-A4 | after a second CO-A2 that got no answer, or that reported the service unavailable after a first that got no answer, the read shows a refund pending or issued | Report the refund id and its status. | CO-05, CO-08 |
| CO-A4 | after a second CO-A2 that got no answer, or that reported the service unavailable after a first that got no answer, the read shows a refund failed, or no refund | CO-A3 for the order with reason refund not issued; tell the customer the refund is not confirmed and staff will follow up. | CO-05 |
| CO-A4 | after a second CO-A2 that got no answer, or that reported the service unavailable after a first that got no answer, the read gets no answer, however often it is retried | CO-A3 for the order with reason refund status unknown; tell the customer the refund's status is unknown and staff will follow up. | CO-05, G-01 |
| CO-A3 | the follow-up queue does not answer, on the first CO-A3 | Send CO-A3 once more with the same reason; the repeat cannot create a second task (SG-03). | CO-07, G-04 |
| CO-A3 | the follow-up queue does not answer, on the second CO-A3 | Send no further CO-A3; tell the customer to contact Harbor Goods support about the order. | CO-07 |
| CO-A4 | before any proposal, the read gets no answer, however often it is retried | Tell the customer their orders cannot be looked up right now; propose nothing; change nothing. | CO-03, G-01 |
| any | the customer's request fits more than one of their placed or processing orders | Ask which order they mean; propose only the order they name. | CO-02 |
| any | the customer asks to cancel some items of an order | Say only the whole order can be cancelled; cancel nothing unless the customer then confirms a whole-order proposal. | CO-01 |
| any | a read shows the order the customer named shipped or delivered, before any proposal | Tell the customer the order can no longer be cancelled and that returns are a separate process; send nothing. | CO-01 |
| any | a read shows the order the customer named already cancelled | Tell the customer the order is already cancelled; send nothing. | CO-01 |
| any | the order number the customer gives matches none of their orders | Tell the customer no such order was found; send nothing. | CO-01 |
| any | the customer's request names no order number and fits none of their placed or processing orders | Tell the customer none of their orders can be cancelled, and why for each; send nothing. | CO-01 |
| any | the customer's reply to the confirmation question asks for a different refund amount, a different payment method or store credit | Treat it as no confirmation; tell the customer the refund can only be the order's total paid, to the order's payment method; ask again for confirmation of that proposal; send nothing until it is confirmed. | CO-03 |
| any | the customer's reply to the confirmation question names a different order, or declines | Treat it as no confirmation; for a different order, propose that order and ask for confirmation; for a refusal, send nothing. | CO-03 |
| any | the customer stops answering before confirming | Send nothing. | CO-03 |

#### Scenarios

##### CO-S01 — Cancel a cancellable order and refund it, including after a cancellation that got no answer

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** regression

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly two orders, HG-10482 and HG-10455.
- Order HG-10482: placed 2026-11-03, status <status>, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- Order HG-10455: placed 2026-10-02, status delivered, 1 × Wool throw at $68.00, shipping $5.90, tax $5.44, total paid $79.34, payment method Visa ending 4242, no refund.
- The first CO-A1 for HG-10482 <first cancel>.
- CO-A2 for HG-10482 creates refund RF-5531 for $86.40 to Visa ending 4242 with status <refund_status>.
- No follow-up task exists.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to your Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10482, after the CO-A1 for HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status <refund_status>.
- Order HG-10455 is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- CO-A1 or CO-A2 for any order other than HG-10482.
- A second CO-A1.
- CO-A2 not preceded by a CO-A4 issued after the CO-A1, when the CO-A1 got no answer.
- A second CO-A2.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | status | refund_status | first cancel |
|---|---|---|---|---|
| 1 | Please cancel order HG-10482 and refund me. | processing | pending | reports the order cancelled |
| 2 | I want to cancel my order and get my money back. | placed | pending | reports the order cancelled |
| 3 | Cancel HG-10482, please. | processing | issued | reports the order cancelled |
| 4 | Please cancel order HG-10482 and refund me, please. | processing | pending | gets no answer, and the order system records HG-10482 as cancelled |

**Reference trajectory**
1. User: "Please cancel order HG-10482 and refund me."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund; HG-10455 delivered, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, status pending.
7. Agent reports that HG-10482 is cancelled and refund RF-5531 is pending.

**Illustrates** CO-01, CO-03, CO-04, CO-06, CO-08, G-01, G-02, G-03, G-04

**Unambiguity note** The cancellation, the refund and their order after the confirmation turn are read from the action log, and the orders and refunds are compared with Initial state; row 2 needs no question about which order, because HG-10455 is delivered; in row 4 the cancellation gets no answer, so a resend, or a refund before a read made after that cancellation, fails on the action log. The checks on the agent's words are message check "Refund id reported" (the exact id RF-5531), rubric dimension "Truthful status report" and rubric dimension "No arrival-time promise".

##### CO-S02 — Two open orders and "cancel my order"

- **Interaction type:** clarify, confirm
- **Category tags:** multi-action, multi-turn, state-dependency, canonicalization
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly three orders, HG-10482, HG-10517 and HG-10455.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- Order HG-10517: placed 2026-11-08, status placed, 1 × Brass desk lamp at $119.00, shipping $0.00, tax $9.52, total paid $128.52, payment method Mastercard ending 8810, no refund.
- Order HG-10455: placed 2026-10-02, status delivered, 1 × Wool throw at $68.00, shipping $5.90, tax $5.44, total paid $79.34, payment method Visa ending 4242, no refund.
- CO-A2 for HG-10517 creates refund RF-5532 for $128.52 to Mastercard ending 8810 with status pending.
- No follow-up task exists.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Which order do you want to cancel? A: <which>
- Q: Shall I cancel order HG-10517 and refund $128.52 to your Mastercard ending 8810? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10517, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10517, after the CO-A1 for HG-10517.

Final state assertions:
- Order HG-10517 has status cancelled.
- Exactly one refund exists for HG-10517: RF-5532, amount $128.52, payment method Mastercard ending 8810, status pending.
- Order HG-10482 is unchanged: status processing, no refund.
- Order HG-10455 is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 for HG-10482.
- CO-A2 for HG-10482.
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- A second CO-A2.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | which |
|---|---|---|
| 1 | Cancel my order, please. I want a refund. | The desk lamp one. |
| 2 | I need to cancel my order. | The one I placed on November 8th. |

**Reference trajectory**
1. User: "Cancel my order, please. I want a refund."
2. Agent → CO-A4 () → HG-10482 processing, HG-10517 placed, HG-10455 delivered, no refunds.
3. Agent says two orders can be cancelled, HG-10482 (pour-over set and tea towels) and HG-10517 (desk lamp), and asks which one.
4. User: "The desk lamp one."
5. Agent states the proposal (cancel HG-10517, refund $128.52 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A1 (HG-10517) → cancelled.
8. Agent → CO-A2 (HG-10517) → refund RF-5532, $128.52, Mastercard ending 8810, status pending.
9. Agent reports that HG-10517 is cancelled and refund RF-5532 is pending.

**Illustrates** CO-02, CO-03, CO-08, G-03

**Unambiguity note** Two orders are open, so the agent must ask which one; a cancellation of HG-10482 at any point, or of HG-10517 before the confirmation turn, fails on the action log. The checks on the agent's words are message check "Refund id reported" (RF-5532), rubric dimension "Truthful status report" and rubric dimension "Order asked, not guessed", which fails a run that proposes HG-10517 without asking.

##### CO-S03 — Customer switches to another order in reply to the confirmation question

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly two orders, HG-10482 and HG-10517.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- Order HG-10517: placed 2026-11-08, status placed, 1 × Brass desk lamp at $119.00, shipping $0.00, tax $9.52, total paid $128.52, payment method Mastercard ending 8810, no refund.
- CO-A2 for HG-10517 creates refund RF-5532 for $128.52 to Mastercard ending 8810 with status pending.
- No follow-up task exists.

**User**
- Turn 1: "Please cancel order HG-10482."
- Turn 2, in reply to the first agent message that asks her to confirm cancelling HG-10482: "<Turn 2>"

**User knows**
- Q: Shall I cancel order HG-10517 and refund $128.52 to your Mastercard ending 8810? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10517, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10517, after the CO-A1 for HG-10517.

Final state assertions:
- Order HG-10517 has status cancelled.
- Exactly one refund exists for HG-10517: RF-5532, amount $128.52, payment method Mastercard ending 8810, status pending.
- Order HG-10482 is unchanged: status processing, no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 for HG-10482.
- CO-A2 for HG-10482.
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- A second CO-A2.
- CO-A3 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Yes. Oh wait, not that one. Cancel HG-10517, the desk lamp order. |
| 2 | Actually, I meant HG-10517, not HG-10482. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, HG-10517 placed, no refunds.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes. Oh wait, not that one. Cancel HG-10517, the desk lamp order."
5. Agent states the proposal (cancel HG-10517, refund $128.52 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A1 (HG-10517) → cancelled.
8. Agent → CO-A2 (HG-10517) → refund RF-5532, $128.52, Mastercard ending 8810, status pending.
9. Agent reports that HG-10517 is cancelled and refund RF-5532 is pending.

**Illustrates** CO-03, G-03

**Unambiguity note** The "Yes" in Turn 2 arrives with a change of order in the same message, so it confirms nothing; a cancellation of HG-10482 at any point, or of HG-10517 before the confirmation turn, is visible in the action log. The check on the agent's words is message check "Refund id reported" (RF-5532).

##### CO-S04 — Customer declines the proposal

- **Interaction type:** confirm
- **Category tags:** multi-turn
- **Suite:** regression

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly two orders, HG-10482 and HG-10455.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- Order HG-10455: placed 2026-10-02, status delivered, 1 × Wool throw at $68.00, shipping $5.90, tax $5.44, total paid $79.34, payment method Visa ending 4242, no refund.
- No follow-up task exists.

**User**
- Turn 1: "Cancel order HG-10482."
- Turn 2, in reply to the first agent message that asks her to confirm cancelling HG-10482, in place of a confirmation: "<Turn 2>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10482 is unchanged: status processing, no refund.
- Order HG-10455 is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | No, leave it. I'll keep the order. |
| 2 | Hmm, never mind, don't cancel anything. |

**Reference trajectory**
1. User: "Cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund; HG-10455 delivered.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "No, leave it. I'll keep the order."
5. Agent acknowledges that nothing was cancelled.

**Illustrates** CO-03, G-03

**Unambiguity note** Turn 2 refuses the proposal outright, so no confirmation turn exists; any cancellation, refund or follow-up in the action log fails the trial, and the orders are compared with Initial state.

##### CO-S05 — Order that cannot be cancelled

- **Interaction type:** infeasible
- **Category tags:** state-dependency
- **Suite:** regression

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly two orders, HG-10377 and HG-10455.
- Order HG-10377: placed 2026-10-20, status <status>, 1 × Cast-iron skillet at $42.00, shipping $5.90, tax $3.36, total paid $51.26, payment method Visa ending 4242, <refund>.
- Order HG-10455: placed 2026-10-02, status delivered, 1 × Wool throw at $68.00, shipping $5.90, tax $5.44, total paid $79.34, payment method Visa ending 4242, no refund.
- Every CO-A4 call <lookup>.
- No follow-up task exists.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10377 is unchanged: status <status>, <refund>.
- Order HG-10455 is unchanged and has no refund.
- No refund was created.
- No follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | status | refund | lookup | reason |
|---|---|---|---|---|---|
| 1 | Please cancel order HG-10377. | shipped | without a refund | is answered normally | HG-10377 has shipped, so it can no longer be cancelled, and returns are a separate process |
| 2 | Cancel HG-10377 and give me my money back. | delivered | without a refund | is answered normally | HG-10377 was delivered, so it can no longer be cancelled, and returns are a separate process |
| 3 | I need to cancel order HG-10377. | cancelled | with refund RF-5470 for $51.26 to Visa ending 4242, status issued | is answered normally | HG-10377 is already cancelled |
| 4 | Cancel order HG-10399, please. | shipped | without a refund | is answered normally | no order HG-10399 was found among her orders |
| 5 | Please cancel my skillet order, HG-10377. | processing | without a refund | gets no answer | her orders cannot be looked up right now, so nothing was cancelled |
| 6 | I want to cancel my order. | shipped | without a refund | is answered normally | none of her orders can be cancelled: HG-10377 has shipped and HG-10455 was delivered, and returns are a separate process |

**Reference trajectory**
1. User: "Please cancel order HG-10377."
2. Agent → CO-A4 () → HG-10377 shipped, no refund; HG-10455 delivered, no refund.
3. Agent tells the customer HG-10377 has shipped, so it can no longer be cancelled, and that returns are a separate process.

**Illustrates** CO-01, G-01, G-02

**Unambiguity note** No row allows a cancellation, so any CO-A1, CO-A2 or CO-A3 fails on the action log and the orders are compared with Initial state; what the agent tells the customer is rubric dimension "Cannot-cancel reason given", read against the row's reason column.

##### CO-S06 — Request to cancel only some items

- **Interaction type:** infeasible
- **Category tags:** insufficient-information
- **Suite:** regression

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly one order, HG-10482.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- No follow-up task exists.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Do you want to cancel the whole order instead? A: No, I'll keep the whole order then. (optional)

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10482 is unchanged: status processing, both line items, no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | Can you cancel just the tea towels from order HG-10482? I still want the pour-over set. |
| 2 | Please remove one of the two tea towels from HG-10482 and refund me for it. |

**Reference trajectory**
1. User: "Can you cancel just the tea towels from order HG-10482? I still want the pour-over set."
2. Agent → CO-A4 () → HG-10482 processing, two line items, no refund.
3. Agent says only the whole order can be cancelled and asks whether to cancel the whole order instead.
4. User: "No, I'll keep the whole order then."
5. Agent acknowledges that nothing was cancelled.

**Illustrates** CO-01, G-02

**Unambiguity note** No tool cancels part of an order, so any CO-A1, CO-A2 or CO-A3 fails on the action log; the explanation is rubric dimension "Whole-order-only explained".

##### CO-S07 — Order ships between the read and the cancellation, whether the cancellation is rejected or gets no answer

- **Interaction type:** confirm
- **Category tags:** multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly one order, HG-10482.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- The order system changes HG-10482 to status shipped just before the first CO-A1 reaches it, and that CO-A1 <first cancel>.
- No follow-up task exists.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to your Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.

Final state assertions:
- Order HG-10482 has status shipped.
- No refund exists for HG-10482.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- CO-A2 at any point.
- CO-A3 at any point.
- Ending the trial without a CO-A4 issued after the CO-A1, when the CO-A1 got no answer.

**Data variants**

| variant | Turn 1 | first cancel | reason |
|---|---|---|---|
| 1 | Cancel order HG-10482, please. | reports the order cannot be cancelled because it has shipped | HG-10482 has shipped, so it can no longer be cancelled, and returns are a separate process |
| 2 | Please cancel HG-10482 and refund it. | reports the order cannot be cancelled because it has shipped | HG-10482 has shipped, so it can no longer be cancelled, and returns are a separate process |
| 3 | Cancel order HG-10482, please, and refund it. | gets no answer | HG-10482 has shipped, so it can no longer be cancelled, and returns are a separate process |

**Reference trajectory**
1. User: "Cancel order HG-10482, please."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → rejected: the order has shipped.
6. Agent tells the customer HG-10482 has shipped, so it can no longer be cancelled, that returns are a separate process, and that no refund was issued.

**Illustrates** CO-01, CO-04, CO-06, G-01, G-04

**Unambiguity note** The order ships before the first cancellation reaches the order system, which rejects it (rows 1 and 2) or gives no answer (row 3, where a read shows the order shipped), so a refund or a second cancellation is visible in the action log; what the agent tells the customer is rubric dimension "Cannot-cancel reason given", read against the row's reason column, and rubric dimension "Truthful status report".

##### CO-S09 — Cancellation gets no answer, the order is still open, and the agent sends it once more

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly one order, HG-10482.
- Order HG-10482: placed 2026-11-03, status <status>, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- The first CO-A1 for HG-10482 gets no answer and does not cancel the order.
- The second CO-A1 for HG-10482 <second cancel>.
- CO-A2 for HG-10482 creates refund RF-5531 for $86.40 to Visa ending 4242 with status pending.
- No follow-up task exists.

**User**
- Turn 1: "Please cancel order HG-10482 and refund me."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to your Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly twice, for HG-10482, both after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10482, after the second CO-A1 for HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status pending.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A1 not preceded by a CO-A4 issued after the first CO-A1.
- A third CO-A1.
- CO-A2 before the second CO-A1.
- CO-A2 not preceded by a CO-A4 issued after the second CO-A1, when the second CO-A1 got no answer.
- A second CO-A2.
- CO-A3 at any point.

**Data variants**

| variant | status | second cancel |
|---|---|---|
| 1 | processing | reports the order cancelled |
| 2 | placed | reports the order cancelled |
| 3 | processing | gets no answer, and the order system records HG-10482 as cancelled |

**Reference trajectory**
1. User: "Please cancel order HG-10482 and refund me."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → no answer.
6. Agent → CO-A4 () → HG-10482 processing.
7. Agent → CO-A1 (HG-10482) → cancelled.
8. Agent → CO-A2 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, status pending.
9. Agent reports that HG-10482 is cancelled and refund RF-5531 is pending.

**Illustrates** CO-06, G-04, CO-04

**Unambiguity note** The resend must follow a read made after the unanswered cancellation, and in row 3 the refund must follow a read made after the second unanswered cancellation; each order is read from the action log. The checks on the agent's words are message check "Refund id reported" (RF-5531) and rubric dimension "Truthful status report".

##### CO-S11 — Cancellation outcome cannot be learned: handed to staff

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly one order, HG-10482.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- The first CO-A1 for HG-10482 gets no answer; afterwards the order system holds HG-10482 with status <status after>.
- Every CO-A4 call after the first CO-A1 gets no answer.
- CO-A3 for HG-10482 creates follow-up task FT-2201.
- No follow-up task exists.

**User**
- Turn 1: "Please cancel order HG-10482 and refund me."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to your Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482 with reason cancellation unknown, after the CO-A1 for HG-10482.

Final state assertions:
- Order HG-10482 has status <status after>.
- No refund exists for HG-10482.
- Exactly one follow-up task exists: FT-2201, for HG-10482, reason cancellation unknown.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- CO-A2 at any point.
- CO-A3 with any reason other than cancellation unknown.
- CO-A3 not preceded by a CO-A4 issued after the CO-A1.
- A second CO-A3.

**Data variants**

| variant | status after |
|---|---|
| 1 | cancelled |
| 2 | processing |

**Reference trajectory**
1. User: "Please cancel order HG-10482 and refund me."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → no answer.
6. Agent → CO-A4 () → no answer.
7. Agent → CO-A3 (HG-10482, cancellation unknown) → task FT-2201.
8. Agent tells the customer the cancellation's outcome is unknown, no refund was issued, and staff will follow up.

**Illustrates** CO-06, CO-07, G-01, G-04

**Unambiguity note** The agent cannot learn the order's status, so both rows require the same calls; a resend, a refund, or a handoff before a read after the unanswered cancellation is visible in the action log. The checks on the agent's words are rubric dimension "Handoff explained" and rubric dimension "Truthful status report".

##### CO-S12 — Both cancellation attempts get no answer, and the order is still open

- **Interaction type:** confirm
- **Category tags:** multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly one order, HG-10482.
- Order HG-10482: placed 2026-11-03, status <status>, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- The first and the second CO-A1 for HG-10482 get no answer and do not cancel the order.
- No follow-up task exists.

**User**
- Turn 1: "Please cancel order HG-10482 and refund me."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to your Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly twice, for HG-10482, both after the user's confirmation turn.

Final state assertions:
- Order HG-10482 is unchanged: status <status>, no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A1 not preceded by a CO-A4 issued after the first CO-A1.
- A third CO-A1.
- CO-A2 at any point.
- CO-A3 at any point.
- Ending the trial without a CO-A4 issued after the second CO-A1.

**Data variants**

| variant | status |
|---|---|
| 1 | processing |
| 2 | placed |

**Reference trajectory**
1. User: "Please cancel order HG-10482 and refund me."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → no answer.
6. Agent → CO-A4 () → HG-10482 processing.
7. Agent → CO-A1 (HG-10482) → no answer.
8. Agent → CO-A4 () → HG-10482 processing.
9. Agent tells the customer the cancellation did not go through, HG-10482 is still open, and no refund was issued.

**Illustrates** CO-06, G-01, G-04

**Unambiguity note** Two cancellations, the read before the second, the read after the second, and the absence of any refund or third cancellation are read from the action log; the report is rubric dimension "Truthful status report".

##### CO-S13 — Refund call repeated once, and the refund is confirmed

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly one order, HG-10482.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- The first CO-A2 for HG-10482 <first refund>.
- The second CO-A2 for HG-10482 <second refund>.
- No follow-up task exists.

**User**
- Turn 1: "Please cancel order HG-10482 and refund me."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to your Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly twice, for HG-10482, both after the CO-A1 for HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status <refund_status>.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- A third CO-A2.
- CO-A3 at any point.
- Ending the trial without a CO-A4 issued after the second CO-A2, when the second CO-A2 got no answer, or reported the refund service temporarily unavailable after a first CO-A2 that got no answer.

**Data variants**

| variant | first refund | second refund | refund_status |
|---|---|---|---|
| 1 | reports the refund service temporarily unavailable and creates no refund | returns refund RF-5531 for $86.40 to Visa ending 4242 with status pending | pending |
| 2 | gets no answer and creates no refund | returns refund RF-5531 for $86.40 to Visa ending 4242 with status pending | pending |
| 3 | gets no answer and creates refund RF-5531 with status pending | returns the same refund RF-5531 with status pending | pending |
| 4 | gets no answer and creates refund RF-5531 for $86.40 to Visa ending 4242 with status pending | gets no answer | pending |
| 5 | gets no answer and creates refund RF-5531 for $86.40 to Visa ending 4242 with status issued | gets no answer | issued |
| 6 | gets no answer and creates refund RF-5531 for $86.40 to Visa ending 4242 with status pending | reports the refund service temporarily unavailable and creates no refund | pending |

**Reference trajectory**
1. User: "Please cancel order HG-10482 and refund me."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund service temporarily unavailable.
7. Agent → CO-A2 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, status pending.
8. Agent reports that HG-10482 is cancelled and refund RF-5531 is pending.

**Illustrates** CO-05, CO-08, G-01, G-04

**Unambiguity note** Exactly two refund calls and no handoff are read from the action log; in row 3 the second call returns the refund the first created (SG-01), and in rows 4 to 6 the second call leaves the refund unsettled, so a read after the second call must show the refund before the trial ends. The checks on the agent's words are message check "Refund id reported" (RF-5531) and rubric dimension "Truthful status report".

##### CO-S14 — Refund not issued: handed to staff

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly one order, HG-10482.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- The first CO-A2 for HG-10482 <first refund>.
- A second CO-A2 for HG-10482 <second refund>.
- CO-A3 for HG-10482 creates follow-up task FT-2201.
- No follow-up task exists.

**User**
- Turn 1: "Please cancel order HG-10482 and refund me."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to your Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly <refund calls>, for HG-10482, after the CO-A1 for HG-10482.
- CO-A3 occurs exactly once, for HG-10482 with reason refund not issued, after the last CO-A2.

Final state assertions:
- Order HG-10482 has status cancelled.
- For HG-10482, <refund record>.
- Exactly one follow-up task exists: FT-2201, for HG-10482, reason refund not issued.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- A CO-A2 after a CO-A2 that reported the refund failed.
- A third CO-A2.
- CO-A3 with any reason other than refund not issued.
- CO-A3 not preceded by a CO-A4 issued after the second CO-A2, when the second CO-A2 got no answer, or reported the refund service temporarily unavailable after a first CO-A2 that got no answer.
- A second CO-A3.

**Data variants**

| variant | first refund | second refund | refund calls | refund record |
|---|---|---|---|---|
| 1 | reports the refund failed because the payment method can no longer receive money, creating refund RF-5531 with status failed | returns the same failed refund RF-5531 | one time | exactly one refund exists: RF-5531, amount $86.40, payment method Visa ending 4242, status failed |
| 2 | reports the refund failed because the payment provider declined it, creating refund RF-5531 with status failed | returns the same failed refund RF-5531 | one time | exactly one refund exists: RF-5531, amount $86.40, payment method Visa ending 4242, status failed |
| 3 | reports the refund service temporarily unavailable and creates no refund | reports the refund service temporarily unavailable and creates no refund | two times | no refund exists |
| 4 | gets no answer and creates refund RF-5531 with status failed | gets no answer | two times | exactly one refund exists: RF-5531, amount $86.40, payment method Visa ending 4242, status failed |
| 5 | gets no answer and creates no refund | gets no answer and creates no refund | two times | no refund exists |
| 6 | gets no answer and creates no refund | reports the refund service temporarily unavailable and creates no refund | two times | no refund exists |

**Reference trajectory**
1. User: "Please cancel order HG-10482 and refund me."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5531 failed: the payment method can no longer receive money.
7. Agent → CO-A3 (HG-10482, refund not issued) → task FT-2201.
8. Agent tells the customer HG-10482 is cancelled, the refund is not issued, and staff will follow up.

**Illustrates** CO-05, G-01, G-04

**Unambiguity note** The refund-call count per row, the handoff reason, and in rows 4 to 6 the read before the handoff are read from the action log; the report is rubric dimension "Handoff explained" and rubric dimension "Truthful status report".

##### CO-S16 — Refund status cannot be learned: handed to staff

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly one order, HG-10482.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- The first CO-A2 for HG-10482 <first refund>.
- The second CO-A2 for HG-10482 gets no answer.
- Every CO-A4 call after the second CO-A2 gets no answer.
- CO-A3 for HG-10482 creates follow-up task FT-2201.
- No follow-up task exists.

**User**
- Turn 1: "Please cancel order HG-10482 and refund me."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to your Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly twice, for HG-10482, both after the CO-A1 for HG-10482.
- CO-A3 occurs exactly once, for HG-10482 with reason refund status unknown, after the second CO-A2.

Final state assertions:
- Order HG-10482 has status cancelled.
- For HG-10482, <refund record>.
- Exactly one follow-up task exists: FT-2201, for HG-10482, reason refund status unknown.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- A third CO-A2.
- CO-A3 with any reason other than refund status unknown.
- CO-A3 not preceded by a CO-A4 issued after the second CO-A2.
- A second CO-A3.

**Data variants**

| variant | first refund | refund record |
|---|---|---|
| 1 | gets no answer and creates refund RF-5531 with status pending | exactly one refund exists: RF-5531, amount $86.40, payment method Visa ending 4242, status pending |
| 2 | gets no answer and creates no refund | no refund exists |

**Reference trajectory**
1. User: "Please cancel order HG-10482 and refund me."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → no answer.
7. Agent → CO-A2 (HG-10482) → no answer.
8. Agent → CO-A4 () → no answer.
9. Agent → CO-A3 (HG-10482, refund status unknown) → task FT-2201.
10. Agent tells the customer HG-10482 is cancelled, the refund's status is unknown, and staff will follow up.

**Illustrates** CO-05, G-01, G-04

**Unambiguity note** The agent cannot learn whether a refund exists, so both rows require the same calls; the read before the handoff and the handoff reason are read from the action log. The checks on the agent's words are rubric dimension "Handoff explained" and rubric dimension "Truthful status report".

##### CO-S17 — Follow-up request gets no answer once, then goes through

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly one order, HG-10482.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- The first CO-A2 for HG-10482 reports the refund failed because the payment method can no longer receive money, creating refund RF-5531 with status failed.
- The first CO-A3 for HG-10482 gets no answer and <first followup>.
- The second CO-A3 for HG-10482 returns follow-up task FT-2201.
- No follow-up task exists.

**User**
- Turn 1: "Please cancel order HG-10482 and refund me."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to your Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10482, after the CO-A1 for HG-10482.
- CO-A3 occurs exactly twice, for HG-10482 with reason refund not issued, both after the CO-A2.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status failed.
- Exactly one follow-up task exists: FT-2201, for HG-10482, reason refund not issued.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- A second CO-A2.
- CO-A3 with any reason other than refund not issued.
- A third CO-A3.

**Data variants**

| variant | first followup |
|---|---|
| 1 | creates no task |
| 2 | creates follow-up task FT-2201 |

**Reference trajectory**
1. User: "Please cancel order HG-10482 and refund me."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5531 failed: the payment method can no longer receive money.
7. Agent → CO-A3 (HG-10482, refund not issued) → no answer.
8. Agent → CO-A3 (HG-10482, refund not issued) → task FT-2201.
9. Agent tells the customer HG-10482 is cancelled, the refund is not issued, and staff will follow up.

**Illustrates** CO-07, CO-05, G-04

**Unambiguity note** In row 2 the second request returns the task the first created (SG-03), so both rows end with exactly one task; the two requests and their reason are read from the action log, and the report is rubric dimension "Handoff explained".

##### CO-S18 — Follow-up request gets no answer twice: customer sent to support

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly one order, HG-10482.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- Every CO-A2 for HG-10482 <refund outcome>.
- Every CO-A3 for HG-10482 gets no answer and creates no task.
- No follow-up task exists.

**User**
- Turn 1: "Please cancel order HG-10482 and refund me."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to your Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly <refund calls>, for HG-10482, after the CO-A1 for HG-10482.
- CO-A3 occurs exactly twice, for HG-10482 with reason refund not issued, both after the last CO-A2.

Final state assertions:
- Order HG-10482 has status cancelled.
- For HG-10482, <refund record>.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- A CO-A2 after a CO-A2 that reported the refund failed.
- A third CO-A2.
- CO-A3 with any reason other than refund not issued.
- A third CO-A3.

**Data variants**

| variant | refund outcome | refund calls | refund record |
|---|---|---|---|
| 1 | reports the refund failed because the payment method can no longer receive money, with refund RF-5531 in status failed | one time | exactly one refund exists: RF-5531, amount $86.40, payment method Visa ending 4242, status failed |
| 2 | reports the refund service temporarily unavailable and creates no refund | two times | no refund exists |

**Reference trajectory**
1. User: "Please cancel order HG-10482 and refund me."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5531 failed: the payment method can no longer receive money.
7. Agent → CO-A3 (HG-10482, refund not issued) → no answer.
8. Agent → CO-A3 (HG-10482, refund not issued) → no answer.
9. Agent tells the customer HG-10482 is cancelled, the refund is not issued, and to contact Harbor Goods support about HG-10482.

**Illustrates** CO-07, G-01

**Unambiguity note** Both follow-up requests get no answer and no task exists, so the customer must be told to contact support; the calls are read from the action log and the referral is rubric dimension "Support referral".

##### CO-S19 — Customer asks for a different refund destination or store credit

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- The customer is signed in as Dana Reyes.
- Dana Reyes has exactly one order, HG-10482.
- Order HG-10482: placed 2026-11-03, status processing, 1 × Ceramic pour-over set at $54.00 and 2 × Linen tea towel at $11.50 each, shipping $5.90, tax $3.50, total paid $86.40, payment method Visa ending 4242, no refund.
- CO-A2 for HG-10482 creates refund RF-5531 for $86.40 to Visa ending 4242 with status pending.
- No follow-up task exists.

**User**
- Turn 1: "Please cancel order HG-10482."
- Turn 2, in reply to the first agent message that asks her to confirm cancelling HG-10482: "<Turn 2>"

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to your Visa ending 4242? A: Yes. (after Turn 2)

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10482, after the CO-A1 for HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status pending.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- A second CO-A2.
- CO-A3 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Yes, but refund it to my Mastercard ending 8810 instead. |
| 2 | Okay, but can I get store credit instead of a refund? |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, total paid $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes, but refund it to my Mastercard ending 8810 instead."
5. Agent says the refund can only be $86.40 to the Visa ending 4242 the order was paid with, and asks again for confirmation of that proposal.
6. User: "Yes."
7. Agent → CO-A1 (HG-10482) → cancelled.
8. Agent → CO-A2 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, status pending.
9. Agent reports that HG-10482 is cancelled and refund RF-5531 is pending.

**Illustrates** CO-03, CO-08, G-03

**Unambiguity note** Turn 2 asks for a term the store does not offer, so it confirms nothing and the confirmation pair is in scope only after it; a cancellation before the later confirmation turn is visible in the action log. The checks on the agent's words are message check "Refund id reported" (RF-5531), rubric dimension "Truthful status report" and rubric dimension "Refund terms explained".

## 5. Evaluation

### 5.1 How lines are read

**Turn anchors.** "Turn n" is the nth scripted User turn of the scenario. "The user's confirmation turn" is the user turn in which the simulated user gives a User-knows answer to a confirmation question. If a trial has more than one confirmation turn, "the user's confirmation turn" is the first. The harness labels both turn kinds on the user events it records, so no grader infers them from text.

**Confirmation question.** The confirmation question is a question that states every value of the proposal and asks the user to go ahead; in User knows it is a pair whose question has that form. A question about only some of those values is not the confirmation question, and the simulated user does not give the confirmation answer to it. Each proposal value the question states must equal that value in the confirmation-form pair it matches, under the trial's data variant row, and that pair must be in scope; compared as Appendix A's value comparison states: the question's form is matched on meaning, its values on equality. A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it unless any other User-knows pair, confirmation-form or not, matches it. When more than one confirmation-form pair is in scope, a question matches the one whose values it equals; a question whose values equal none of them is a wrong-value question, handled as above. Two confirmation-form pairs whose values are equal in some data variant row while both are in scope are a spec error, which the checker refuses. The harness sets the confirmation label on each user turn in which the simulated user reveals a confirmation answer.

**Agent message.** An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one.

**End of trial.** A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first. That message is the agent's final message.

**Message-check window.** A message check reads every agent message from the event that made its value available (the commit call that returned it, or the read that showed it) to the end of the trial. The check passes when any of those messages contains the value.

**Supporting actors.** A supporting actor answers every call normally unless an Initial-state line says otherwise.

**Confirmed proposal.** "The confirmed proposal" is the proposal stated in the scenario's User-knows confirmation question, with the values of the trial's data variant row.

**Several confirmation pairs.** A scenario with more than one confirmation-form pair anchors its Required events and Forbidden lines on turns or on explicit values, never on the confirmed proposal.

**When an action occurs.** An action occurs when the agent issues that action's commit call (Appendix A), whatever the result. A rejected or timed-out commit call still counts as one occurrence. A read-only action with no Appendix A row has no occurrences, and no event line names it.

**Conditional Forbidden lines.** A Forbidden line that applies to only some data variant rows ends with its condition, as in "Ending the trial without a lookup after the second call, when the second call got no answer." The condition must be decidable from the action log: it names calls the agent made and the results those calls returned. When the condition does not hold, the line passes.

**Events and effects.** Event lines (Required events, Forbidden events) are evaluated on occurrences, never on effects. Effects are asserted only in Final state assertions, which are read against Initial state, and in Forbidden lines phrased as state.

### 5.2 Metrics and graders

**Simulated user.** An LLM plays the user in each trial. It says the User turns on its own, at the points they state. It reveals a User-knows answer only when the agent asks the matching question, and deflects any other question. A question matches a pair when its answer is the pair's answer, judged on meaning, not wording; a confirmation question's values must also be equal (§5.1). A pair marked (after Turn n) is revealed only after Turn n, and a pair marked (before Turn n) only before Turn n; outside its scope, the pair matches no question. When an agent message makes a scripted User turn due, the simulated user says the User turn, and gives no User-knows answer and no deflection to any question in that message.

**Trials and metrics.** Each data variant of each scenario runs 5 trials. Forbidden lines report pass^k (every trial passes). Required events and Final state assertions report pass@1 and pass^k.

**Scoring per trial.** Any Forbidden event scores the trial 0. Otherwise the trial scores Required events satisfied / Required events total, and Final state assertions report pass or fail beside it. A scenario with no Required events scores 1 on that component when no Forbidden event occurred.

**Scenario pass.** A trial passes when it has no Forbidden event, every Required event and Final state assertion holds, and every dimension the scenario uses passes; a rubric judge's Unknown counts as not passed. A data variant passes when every one of its trials passes. A scenario passes only when every data variant passes.

**Interaction metrics.** For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked. Every User-knows pair is a required question unless marked (optional). Both numbers are reported beside pass/fail and are never folded into the score.

**Efficiency.** Turn count, write count and read count are reported per trial, separately from the score. Write count is the number of state-changing calls issued and read count the number of read-only calls issued, by the tool's effect, whether the call is bound in Appendix A or unmapped.

**Graders.** State checks and action-log checks are code graders. A check on the agent's messages is a code grader, called a message check, only when the whole check is that the messages in its window (§5.1) contain one or more values the agent copies verbatim from a tool result or Initial state, such as a confirmation id or a reference number. A value the agent can write in more than one form (a date, a time, an amount, a name) is not such a value, and a check with any part that needs judgment (that nothing else was offered, that a detail was withheld, that a result was reported without inventing anything) is a rubric dimension in full, however exact its other parts. LLM-rubric graders cover only those judgments. Each judge grades one dimension and may answer Unknown. A rubric judge reads every text the agent sends, including text sent alongside a tool call. Dimensions used in this spec, each with its grader:

| Dimension | Grader | Definition | Used by |
|---|---|---|---|
| Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the order's refund, as the CO-A2 or CO-A4 result that showed it gives it (the id the scenario's Initial state names). | CO-S01, CO-S02, CO-S03, CO-S09, CO-S13, CO-S19 |
| Truthful status report | rubric | Pass when the agent's final message states the order's status as the latest result the agent received showed it, states the refund's status as the latest result showed it or, when the agent sent no CO-A2, that no refund was issued, says a status is unknown when no result settled it, and no agent message says an order was cancelled or a refund was issued or pending without a result that showed it. | CO-S01, CO-S02, CO-S07, CO-S09, CO-S11, CO-S12, CO-S13, CO-S14, CO-S16, CO-S19 |
| No arrival-time promise | rubric | Pass when no agent message states or promises when the refunded money will arrive. | CO-S01 |
| Cannot-cancel reason given | rubric | Pass when the agent tells the customer the fact in the scenario's reason column and no agent message says an order was cancelled or a refund was issued. | CO-S05, CO-S07 |
| Order asked, not guessed | rubric | Pass when, before any agent message proposes cancelling a particular order, an agent message asks the customer which of their open orders they mean. | CO-S02 |
| Refund terms explained | rubric | Pass when, after the customer asks for a different refund amount, payment method or store credit, an agent message tells them the refund can only be the order's total paid, to the order's payment method. | CO-S19 |
| Whole-order-only explained | rubric | Pass when the agent tells the customer that only a whole order can be cancelled and no agent message says any item was cancelled or refunded. | CO-S06 |
| Handoff explained | rubric | Pass when, after CO-A3 returned a task, an agent message tells the customer that store staff will follow up on the order and that the cancellation or refund the handoff reason names is not confirmed. | CO-S11, CO-S14, CO-S16, CO-S17 |
| Support referral | rubric | Pass when an agent message after the last CO-A3 tells the customer to contact Harbor Goods support about the order, and no agent message says staff will follow up. | CO-S18 |

Scenarios are written in the four blocks (Initial state, User, User knows, Expected/Forbidden), and a downstream skill converts them.

## Appendix A. Interface binding (provisional)

Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.

**Value comparison.** Order numbers and refund ids compare case-insensitively, ignoring spaces; amounts compare as dollars to the cent; payment methods compare on card brand and last four digits. A handoff reason written in a scenario as "refund not issued", "refund status unknown" or "cancellation unknown" is the `reason` value `refund_not_issued`, `refund_status_unknown` or `cancellation_unknown`.

**Which order an action is for.** CO-A1, CO-A2 and CO-A3 are for the order whose number is their `order_number` argument. A refund belongs to the order its `order_number` field names.

| Action | Mark | Commit call | Information items and where each is carried | Outcomes, as tool results | Effect on state |
|---|---|---|---|---|---|
| CO-A4 look up the customer's orders and their refunds | read-only | `list_orders()` → `[{order_number, placed_date, status, line_items: [{product_name, quantity, unit_price}], shipping_cost, tax, total_paid, payment_method, refund: {refund_id, amount, payment_method, status} or null}]` | none; the list holds every order of the signed-in customer, cancelled orders included, and no other customer's | orders: the list; no answer: timeout, which the agent may retry without limit | none |
| CO-A1 cancel the whole order | state-changing | `cancel_order(order_number)` → `{order_number, status}` | order number: argument | cancelled, including for an order already cancelled: returns `status: cancelled`; shipped or delivered: `OrderNotCancellable{status}` with `status` shipped or delivered; no such order: `OrderNotFound`; no answer: timeout | Sets the order's status to cancelled when it returns `status: cancelled`; a repeat for a cancelled order changes nothing (SG-04). A rejection changes nothing. A timeout may or may not have cancelled the order. |
| CO-A2 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, order_number, amount, payment_method, status}` | order number: argument; amount (the order's total paid) and payment method (the order's) set by the refund service from the order | pending or issued: returns the refund with that status; refund failed (payment method cannot receive money, or provider declined): returns the refund with `status: failed`; temporarily unavailable: `RefundServiceUnavailable`, no refund created; order not cancelled: `OrderNotCancelled`, no refund created; no answer: timeout | Creates the order's refund when it returns one; a repeat returns the same refund (SG-01). `RefundServiceUnavailable` and `OrderNotCancelled` create nothing. A timeout may or may not have created the refund. |
| CO-A3 hand the order to store staff | state-changing | `request_staff_followup(order_number, reason)` → `{task_id}` | order number and reason (`refund_not_issued`, `refund_status_unknown` or `cancellation_unknown`): arguments | created: returns `task_id`; no answer: timeout | Creates a follow-up task for the order and reason when it returns `task_id`; a repeat with the same order number and reason returns the same task (SG-03). A timeout may or may not have created it. |

Unmapped read-only calls: none.

**Binding contract.**
- Every state-changing tool call is the commit call of at least one action. Only read-only calls may be unmapped.
- One call may commit several actions. One action never has two commit calls.
- A read-only action has a row only when a Forbidden line or a failure row names it; its call is then its read. Every other read stays unmapped.

## Appendix B. Supporting-actor guarantees

Promises the agent relies on but cannot act on, because no agent turn exists when they apply. They are stated here so the builder sees them; no scenario grades them.

| Id | Guarantee | Covers |
|---|---|---|
| SG-01 | The refund service creates at most one refund per order: a repeated CO-A2 for the same order number returns the refund it already created and never creates a second. | The repeat of CO-A2 after no answer or a temporary outage; the at-most-one-refund rule. |
| SG-02 | Store staff work every follow-up task the follow-up queue receives. | Every CO-A3 that returns a task: the refund not issued, refund status unknown and cancellation unknown handoffs. |
| SG-03 | The follow-up queue creates at most one task per order number and reason: a repeated CO-A3 with the same order number and reason returns the task it already created. | The repeat of CO-A3 after no answer. |
| SG-04 | The order system treats a cancellation of an order that is already cancelled as cancelled and changes nothing. | The second CO-A1 after a first that got no answer; a CO-A1 whose earlier copy took effect unseen. |
