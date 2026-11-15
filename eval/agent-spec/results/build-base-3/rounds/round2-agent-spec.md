# Harbor Goods Order-Support Agent — Agent Spec

## 1. Purpose

The agent lets a signed-in Harbor Goods customer cancel an order they placed and get their money back through natural-language conversation, without knowing the store's cancellation and refund rules or finding the right form. It may cancel one of the customer's own orders that has not shipped, issue that order's refund of the full amount paid to the order's payment method, and, when the outcome of the cancellation or the refund cannot be confirmed, create a follow-up task for store staff. It never changes any other order, refund or record.

## 2. Stakeholders & Interests

- **Primary actor:** the signed-in customer, who wants the order they mean cancelled and the full amount they paid back on the card they paid with, wants nothing cancelled or refunded that they did not agree to, and wants to be told the truth about what happened, including when the store could not confirm it.
- **Supporting actors:** the store, which holds the customer's orders and refunds, cancels an order only while it is placed or processing, issues at most one refund per order, may time out or reject a call, and needs every call to name one of the customer's orders by its order number; the payment provider, reached through the store's refund, which may be temporarily unavailable or may decline a refund; store staff, who need a follow-up task naming the order and the reason whenever the agent cannot confirm a cancellation or a refund (Appendix B, SG-02).
- **Offstage stakeholders:** Harbor Goods, which wants no order cancelled after it has shipped, no refund larger than the amount paid, no second refund for one order and no refund for an order that was not cancelled; the customer's other orders and refunds, which must stay untouched; the customer as a future reader of their card statement, who wants no promise about when money arrives that the store cannot keep; store support, which needs a record (the follow-up task) of how far a failed cancellation or refund got.

## 3. Global Contract

Rules that apply to every state-changing capability.

**G-01 — No unrelated changes** [minimal guarantee]
The agent changes only the order the current request is about, that order's refund and follow-up tasks for that order. Every other order and refund is unchanged at the end of the conversation.

**G-02 — Current authorization** [minimal guarantee]
A state-changing action occurs only for an order whose full proposal the customer has explicitly confirmed in this conversation, as that proposal stands at the moment the action occurs. Any change to the proposal after confirmation voids the confirmation.

**G-03 — Truthful reporting** [minimal guarantee]
The agent reports each cancellation and refund outcome as the store last reported it. It never claims a cancellation or refund the store did not report, and when the store's answer leaves an outcome unknown, it says the outcome is unknown.

**G-04 — No blind retry** [minimal guarantee]
After a state-changing call fails or gets no answer, the agent sends it again only where a rule of the capability allows a retry, and then at most once, so each state-changing action occurs at most twice for the same order (and, for a follow-up, the same reason).

## 4. Capabilities

### 4.1 Cancel Order and Refund (state-changing) — prefix CO

#### Scope & Authority

The agent may:
- CO-A4 read the customer's orders, each with its refund [read-only]
- CO-A1 cancel the whole order, after the customer confirms the full proposal [state-changing]
- CO-A2 issue the order's refund of the full amount paid to the order's payment method, after the order is cancelled [state-changing]
- CO-A3 request a staff follow-up for the order, with the reason the outcome could not be confirmed [state-changing]

The agent must not:
- cancel or refund an order other than the one the customer confirmed;
- cancel part of an order, or refund part of the amount paid;
- refund to any payment method other than the order's, offer store credit, or charge a cancellation fee;
- cancel an order that has shipped or been delivered, or start a return;
- choose an order for the customer when more than one could be meant;
- promise when the refunded money will arrive.

#### Preconditions and Trigger

Preconditions:
- The customer is signed in, and every order the agent can read belongs to that customer.

Trigger:
- The customer asks to cancel an order or to get their money back for an order.

#### Contract

**CO-01 — The customer's own order, named by number** [minimal guarantee]
The agent acts only on an order in the customer's order list, and the proposal names it by its order number. When the request could mean more than one cancellable order, the agent asks which before proposing anything. When the order the customer names matches none of their orders, the agent says so and changes nothing.

**CO-02 — Only unshipped orders are cancelled** [minimal guarantee]
The agent proposes and cancels an order only while its status is placed or processing; there is no time limit. For a shipped or delivered order it tells the customer the order cannot be cancelled and that returns are a separate process, and changes nothing. For an order already cancelled it tells the customer so and changes nothing.

**CO-03 — Whole order only** [minimal guarantee]
Every proposal covers the whole order. When the customer asks to cancel only some items, the agent tells them only the whole order can be cancelled.

**CO-04 — Confirmation precedes cancellation and refund** [minimal guarantee]
The agent cancels and refunds only after the customer confirms one proposal stating the order number, the refund amount and the payment method the refund goes to; that one confirmation authorizes both the cancellation and the refund. A question, a statement of intent, or a confirmation that arrives together with a change is not confirmation.

**CO-05 — Refund terms as the store sets them** [minimal guarantee]
The proposed refund is the order's total paid (items, shipping and tax) to the order's payment method, with no cancellation fee. When the customer asks for store credit or another payment method, the agent tells them the refund goes only to the original payment method, and the proposal stays as it was. The agent promises nothing about when the money arrives.

**CO-06 — Refund only for a cancelled order** [minimal guarantee]
The agent issues the refund only after the store has reported the order cancelled. When the store reports the order not cancellable, including when it shipped after the agent read it, the agent tells the customer and issues no refund.

**CO-07 — An unknown cancellation is resolved before any refund** [minimal guarantee]
When the cancellation gets no answer, the agent re-reads the order before doing anything else. Cancelled: it continues to the refund. Still placed or processing: it sends the cancellation once more under the same confirmation. Shipped or delivered: it tells the customer and issues no refund. When the order cannot be read, or its cancellation is still not confirmed after the second attempt, the agent tells the customer the outcome is unknown, issues no refund and requests a staff follow-up for the unknown cancellation.

**CO-08 — An unconfirmed refund goes to staff** [minimal guarantee]
When the store does not confirm the refund as pending or issued, the agent requests a staff follow-up naming why and tells the customer the refund is not confirmed yet and that staff will follow up. It retries the refund once after a temporary provider outage or no answer, and never after a decline or a refund reported failed. When the follow-up request gets no answer twice, the agent tells the customer to contact Harbor Goods support.

**CO-09 — Successful cancellation** [success guarantee]
The order's status is cancelled, exactly one refund exists for it, for the total paid, to the order's payment method, with status pending or issued, and the agent tells the customer the order is cancelled and gives the refund id.

##### Failure handling

| Action | Outcome | Required behavior | Rule |
|---|---|---|---|
| CO-A4 | the store does not answer, before any proposal | Read again. If the store still has not answered when the agent stops reading, tell the customer their orders cannot be read right now; propose nothing and change nothing. | CO-01, G-03 |
| any | the request could mean two or more of the customer's placed or processing orders | Ask which order, naming each by order number; propose nothing until the customer picks one. | CO-01 |
| any | the order the customer names matches none of their orders | Tell the customer no such order is on their account; change nothing. | CO-01, G-03 |
| any | the order the customer means is shipped or delivered | Tell the customer it cannot be cancelled and returns are a separate process; change nothing. | CO-02 |
| any | the order the customer means is already cancelled | Tell the customer it is already cancelled; change nothing. | CO-02 |
| any | the request names no order and none of the customer's orders is placed or processing | Tell the customer none of their orders can be cancelled, with each order's status; change nothing. | CO-01, CO-02 |
| any | the customer asks to cancel only some items | Tell the customer only the whole order can be cancelled; change nothing for the partial request. | CO-03 |
| any | the customer changes the order, or another term, in or after their confirmation and before CO-A1 | Treat the confirmation as void; state the changed proposal; ask for confirmation again. | CO-04, G-02 |
| any | the customer withdraws or stops answering before confirming | Change nothing. | CO-04 |
| any | the customer asks for store credit or a different payment method | Tell the customer the refund goes only to the order's payment method; keep the proposal unchanged; ask for confirmation of it. | CO-05 |
| CO-A1 | the store reports the order not cancellable, with status shipped or delivered | Tell the customer the order has shipped (or been delivered) and cannot be cancelled, and that returns are a separate process; issue no refund. | CO-06, G-03 |
| CO-A1 | the store reports the order not found | Tell the customer the order could not be cancelled; issue no refund. | CO-01, G-03 |
| CO-A1 | the store does not answer | Do not resend; re-read the orders with CO-A4. | CO-07, G-04 |
| CO-A4 | after an unanswered CO-A1, the store shows the order cancelled | Continue to CO-A2 under the same confirmation. | CO-07 |
| CO-A4 | after the first unanswered CO-A1, the store shows the order placed or processing | Send CO-A1 once more under the same confirmation. | CO-07, G-04 |
| CO-A4 | after an unanswered CO-A1, the store shows the order shipped or delivered | Tell the customer the order shipped and cannot be cancelled; issue no refund. | CO-07, CO-06 |
| CO-A4 | after an unanswered CO-A1, the store does not answer however often the agent reads | Tell the customer the cancellation outcome is unknown; issue no refund; CO-A3 with reason cancellation_unknown. | CO-07, G-03 |
| CO-A4 | after the second unanswered CO-A1, the store shows the order placed or processing | Send no third CO-A1; tell the customer the outcome is unknown; issue no refund; CO-A3 with reason cancellation_unknown. | CO-07, G-04 |
| CO-A2 | the store reports the refund failed (payment method closed or expired, or the provider declined) | Do not retry; CO-A3 with reason refund_not_issued; tell the customer the refund is not confirmed yet and, once CO-A3 returns a task, that staff will follow up. | CO-08, G-04 |
| CO-A2 | the store reports the payment provider temporarily unavailable, on the first CO-A2 | Retry CO-A2 once. | CO-08, G-04 |
| CO-A2 | the store does not answer, on the first CO-A2 | Retry CO-A2 once; the store returns the same refund rather than a second one (SG-01). | CO-08, G-04 |
| CO-A2 | the store reports the payment provider temporarily unavailable, on the second CO-A2 | Send no third CO-A2; CO-A3 with reason refund_not_issued; tell the customer the refund is not confirmed yet. | CO-08, G-04 |
| CO-A2 | the store does not answer, on the second CO-A2 | Re-read with CO-A4; report what it shows, as the next rows state. | CO-08, G-03 |
| CO-A4 | after two unanswered CO-A2, the store shows the refund pending or issued | Tell the customer that status and the refund id; request no follow-up. | CO-08, G-03 |
| CO-A4 | after two unanswered CO-A2, the store shows the refund failed or no refund | CO-A3 with reason refund_not_issued; tell the customer the refund is not confirmed yet. | CO-08, G-03 |
| CO-A4 | after two unanswered CO-A2, the store does not answer however often the agent reads | Tell the customer the refund status is unknown; CO-A3 with reason refund_status_unknown. | CO-08, G-03 |
| CO-A2 | the store reports the order not cancelled | Do not retry; tell the customer the refund was not issued; CO-A3 with reason refund_not_issued. | CO-06, CO-08 |
| CO-A3 | the store does not answer, on the first CO-A3 | Retry CO-A3 once with the same reason; the store creates no second task (SG-03). | CO-08, G-04 |
| CO-A3 | the store does not answer, on the second CO-A3 | Send no third CO-A3; tell the customer to contact Harbor Goods support. | CO-08, G-04 |
| any | after the refund, staff work the follow-up task or the money reaches the card | No agent turn exists; covered by SG-02 and by the payment provider. | CO-05, CO-08 |

#### Scenarios

##### CO-S01 — Cancel an unshipped order and refund it

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, canonicalization, state-dependency
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed <placed>, status <status>, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242, no refund.
- Order HG-10233 exists: placed 2026-10-12, status delivered, total paid 31.20, payment method Visa ending 4242, no refund.
- <cancel outcome>
- The store answers the agent's first CO-A2 with refund <refund_id> for HG-10482, amount 86.40, payment method Visa ending 4242, status pending.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10482, after the CO-A1 for HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482, with refund id <refund_id>, amount 86.40, payment method Visa ending 4242, status pending.
- Order HG-10233 is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- CO-A1 for any order other than HG-10482.
- CO-A2 for any order other than HG-10482.
- A second CO-A1.
- A second CO-A2.
- CO-A3 at any point.
- CO-A2 without a CO-A4 between the first CO-A1 and that CO-A2, when the first CO-A1 got no answer.

**Data variants**

| variant | Turn 1 | placed | status | cancel outcome | refund_id |
|---|---|---|---|---|---|
| 1 | Please cancel order HG-10482. | 2026-11-03 | processing | The store answers the agent's first CO-A1 with HG-10482 cancelled. | RF-5531 |
| 2 | I want to cancel the order I placed on Tuesday and get my money back. | 2026-11-03 | placed | The store answers the agent's first CO-A1 with HG-10482 cancelled. | RF-5532 |
| 3 | Cancel HG-10482 please, I don't need it anymore. | 2026-11-03 | processing | The store cancels HG-10482 on the agent's first CO-A1 but that call times out; every CO-A4 after it and before the agent's first CO-A2 shows HG-10482 cancelled with no refund, and every CO-A4 after the first CO-A2 shows HG-10482 cancelled with refund RF-5533 pending. | RF-5533 |
| 4 | Please cancel order HG-10482 — I ordered it back in July and it still hasn't shipped. | 2026-07-20 | processing | The store answers the agent's first CO-A1 with HG-10482 cancelled. | RF-5534 |
| 5 | Cancel my order, please. | 2026-11-03 | processing | The store answers the agent's first CO-A1 with HG-10482 cancelled. | RF-5529 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, total paid 86.40, Visa ending 4242, no refund; HG-10233 delivered.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5531, 86.40, Visa ending 4242, pending.
7. Agent reports that HG-10482 is cancelled and refund RF-5531 for $86.40 to Visa ending 4242 is pending.

**Illustrates** CO-01, CO-02, CO-04, CO-05, CO-06, CO-07, CO-09, G-01, G-02, G-03

**Unambiguity note** Both actions, their order number and their order after the confirmation turn are read from the action log, and the order and refund records are compared with Initial state; in row 3 the agent must re-read rather than resend after the timed-out cancellation, which "A second CO-A1" and the conditional CO-A2 line enforce from the action log; row 4 is an order placed months ago that is still processing, so a cancellation age limit fails it; in row 5 only HG-10482 can be meant, since HG-10233 is delivered; message check "Refund id reported" matches the row's refund id, and rubric dimension "Outcome reported as recorded" and rubric dimension "No arrival promise" judge the report.

##### CO-S02 — Two open orders, the customer says "my order"

- **Interaction type:** clarify, confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order <order_number> exists: <order_details>, no refund.
- Order <other_order> exists: <other_details>, no refund.
- The store answers the agent's first CO-A1 with the order in its call cancelled.
- The store answers the agent's first CO-A2 with refund <refund_id> for the order in its call, with that order's total paid and payment method, status pending.

**User**
- Turn 1: "Cancel my order and refund me."

**User knows**
- Q: Which order do you want to cancel? A: <choice>
- Q: Shall I cancel order <order_number> and refund <amount> to <payment_method>? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for <order_number>, after the user's confirmation turn.
- CO-A2 occurs exactly once, for <order_number>, after the CO-A1 for <order_number>.

Final state assertions:
- Order <order_number> has status cancelled.
- Exactly one refund exists for <order_number>, with refund id <refund_id>, amount <amount>, payment method <payment_method>, status pending.
- Order <other_order> is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 for <other_order>.
- CO-A2 for <other_order>.
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- CO-A3 at any point.

**Data variants**

| variant | choice | order_number | order_details | amount | payment_method | other_order | other_details | refund_id |
|---|---|---|---|---|---|---|---|---|
| 1 | The one with the linen throw blanket. | HG-10482 | placed 2026-11-03, status processing, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242 | $86.40 | Visa ending 4242 | HG-10517 | placed 2026-11-04, status placed, line items Walnut cutting board ×1 at 42.00, shipping 5.00, tax 3.78, total paid 50.78, payment method Mastercard ending 8810 | RF-5541 |
| 2 | The cutting board, HG-10517. | HG-10517 | placed 2026-11-04, status placed, line items Walnut cutting board ×1 at 42.00, shipping 5.00, tax 3.78, total paid 50.78, payment method Mastercard ending 8810 | $50.78 | Mastercard ending 8810 | HG-10482 | placed 2026-11-03, status processing, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242 | RF-5542 |

**Reference trajectory**
1. User: "Cancel my order and refund me."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242; HG-10517 placed, 50.78, Mastercard ending 8810; no refunds.
3. Agent asks which order, naming HG-10482 and HG-10517.
4. User: "The one with the linen throw blanket."
5. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A1 (HG-10482) → cancelled.
8. Agent → CO-A2 (HG-10482) → refund RF-5541, 86.40, Visa ending 4242, pending.
9. Agent reports HG-10482 cancelled and refund RF-5541 pending.

**Illustrates** CO-01, CO-04, G-01, G-02

**Unambiguity note** Two cancellable orders exist, so the agent must ask which before proposing: rubric dimension "Order asked before proposal" fails a proposal made before the customer picks one, a correct guess included, and a question that does not name both orders; a cancellation of the wrong order fails on the order number in the action log, and the other order's record must be unchanged; message check "Refund id reported" and rubric dimension "Outcome reported as recorded" judge the report.

##### CO-S03 — Order that cannot be cancelled because of its status

- **Interaction type:** infeasible
- **Category tags:** single-action, state-dependency
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10391 exists: placed 2026-10-28, status <status>, line items Brass desk lamp ×1 at 58.00, shipping 6.00, tax 5.12, total paid 69.12, payment method Visa ending 4242, <existing refund>.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10391 has status <status>.
- HG-10391 has exactly <existing refund>, as in Initial state.
- No follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | status | existing refund |
|---|---|---|---|
| 1 | Cancel order HG-10391 please. | shipped | no refund |
| 2 | I'd like to cancel HG-10391 and get a refund. | delivered | no refund |
| 3 | Can you cancel HG-10391? | cancelled | one refund, RF-5480, amount 69.12, Visa ending 4242, status issued |
| 4 | HG-10391 was cancelled but I never got my money back — can you refund it? | cancelled | no refund |
| 5 | Please cancel HG-10391 and refund me. | cancelled | one refund, RF-5481, amount 69.12, Visa ending 4242, status failed |
| 6 | Cancel my order, please. | shipped | no refund |

**Reference trajectory**
1. User: "Cancel order HG-10391 please."
2. Agent → CO-A4 () → HG-10391 shipped, no refund.
3. Agent tells the customer HG-10391 has shipped, cannot be cancelled, and returns are a separate process.

**Illustrates** CO-02, G-03

**Unambiguity note** No state-changing call may occur and the records must equal Initial state, read from the action log and the records, including rows 4 and 5, where the order is already cancelled with no refund or a failed one and a refund or follow-up call still fails; in row 6 the request names no order and the customer's only order has shipped; rubric dimension "Not-cancellable reason given" judges that the agent named the status and, for shipped or delivered, pointed to returns.

##### CO-S04 — Order number that matches none of the customer's orders

- **Interaction type:** infeasible
- **Category tags:** single-action, insufficient-information
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status processing, total paid 86.40, payment method Visa ending 4242, no refund.
- The customer has no order <named_order>.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10482 is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | named_order |
|---|---|---|
| 1 | Please cancel order HG-19999. | HG-19999 |
| 2 | Cancel HG-10428 and refund me. | HG-10428 |

**Reference trajectory**
1. User: "Please cancel order HG-19999."
2. Agent → CO-A4 () → HG-10482 only.
3. Agent tells the customer no order HG-19999 is on their account.

**Illustrates** CO-01, G-01, G-03

**Unambiguity note** Row 2 names a number one transposition away from the real order, so a guess would cancel HG-10482, which the action log shows; rubric dimension "Not-found reported" judges that the agent said the named order is not on the account and invented nothing about it.

##### CO-S05 — Customer asks to cancel only some items

- **Interaction type:** infeasible
- **Category tags:** single-action, multi-turn
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status processing, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242, no refund.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Do you want to cancel the whole order instead? A: No, I'll keep the order. (optional)

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10482 is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | Cancel just the two mugs from order HG-10482. |
| 2 | Can you take the linen throw off HG-10482 and refund that part? |

**Reference trajectory**
1. User: "Cancel just the two mugs from order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing.
3. Agent tells the customer only the whole order can be cancelled and asks whether they want that.
4. User: "No, I'll keep the order."
5. Agent confirms nothing was changed.

**Illustrates** CO-03, G-01

**Unambiguity note** Any cancellation or refund shows in the action log; rubric dimension "Whole order only explained" judges that the agent said only the whole order can be cancelled and offered no partial cancellation or partial refund.

##### CO-S06 — Customer switches to another order in the confirming turn

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status processing, total paid 86.40, payment method Visa ending 4242, no refund.
- Order HG-10517 exists: placed 2026-11-04, status placed, line items Walnut cutting board ×1 at 42.00, shipping 5.00, tax 3.78, total paid 50.78, payment method Mastercard ending 8810, no refund.
- The store answers the agent's first CO-A1 with the order in its call cancelled.
- The store answers the agent's first CO-A2 with refund RF-5551 for the order in its call, with that order's total paid and payment method, status pending.

**User**
- Turn 1: "Cancel order HG-10482."
- Turn 2, in reply to the first agent message that states a proposal for HG-10482 (order number, refund amount and payment method) and asks the customer to go ahead: "<Turn 2>"

**User knows**
- Q: Shall I cancel order HG-10517 and refund $50.78 to Mastercard ending 8810? A: Yes. (after Turn 2)

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10517, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10517, after the CO-A1 for HG-10517.

Final state assertions:
- Order HG-10517 has status cancelled.
- Exactly one refund exists for HG-10517, with refund id RF-5551, amount 50.78, payment method Mastercard ending 8810, status pending.
- Order HG-10482 has status processing and no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 for HG-10482.
- CO-A2 for HG-10482.
- CO-A1 before the user's confirmation turn.
- CO-A3 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Yes — no wait, I meant HG-10517, the cutting board. |
| 2 | Hold on, make that HG-10517 instead, not that one. |

**Reference trajectory**
1. User: "Cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242; HG-10517 placed, 50.78, Mastercard ending 8810.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes — no wait, I meant HG-10517, the cutting board."
5. Agent states the proposal (cancel HG-10517, refund $50.78 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A1 (HG-10517) → cancelled.
8. Agent → CO-A2 (HG-10517) → refund RF-5551, 50.78, Mastercard ending 8810, pending.
9. Agent reports HG-10517 cancelled and refund RF-5551 pending.

**Illustrates** CO-04, G-02, G-01

**Unambiguity note** The "Yes" in Turn 2 arrives with a change, so it confirms nothing; any call for HG-10482, or a call for HG-10517 before the confirmation turn, shows in the action log; message check "Refund id reported" and rubric dimension "Outcome reported as recorded" judge the report.

##### CO-S07 — Customer withdraws after the proposal

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status processing, total paid 86.40, payment method Visa ending 4242, no refund.

**User**
- Turn 1: "Cancel order HG-10482."
- Turn 2, in reply to the first agent message that states a proposal (order number, refund amount and payment method) and asks the customer to go ahead, in place of a confirmation: "<Turn 2>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10482 has status processing and no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | No, actually leave it. I'll keep the order. |
| 2 | Hmm, never mind — don't cancel anything. |

**Reference trajectory**
1. User: "Cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "No, actually leave it. I'll keep the order."
5. Agent acknowledges that nothing was changed.

**Illustrates** CO-04, G-02

**Unambiguity note** Withdrawal is stated outright in Turn 2, so any state-changing call fails, visible in the action log, and the order record must equal Initial state.

##### CO-S08 — Order ships before the cancellation lands

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status <status>, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242, no refund.
- Every CO-A4 before the agent's first CO-A1 shows HG-10482 with status <status>.
- <cancel outcome>

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.

Final state assertions:
- Order HG-10482 has status shipped.
- No refund exists for HG-10482.
- No follow-up task exists.

**Forbidden**
- CO-A2 at any point.
- A second CO-A1.
- CO-A3 at any point.

**Data variants**

| variant | status | cancel outcome |
|---|---|---|
| 1 | processing | The store ships HG-10482 at the moment of the agent's first CO-A1 and answers that call with the order not cancellable, status shipped. |
| 2 | processing | The store ships HG-10482 at the moment of the agent's first CO-A1 and that call times out without cancelling; every CO-A4 after it shows HG-10482 shipped. |
| 3 | placed | The store ships HG-10482 at the moment of the agent's first CO-A1 and answers that call with the order not cancellable, status shipped. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → not cancellable, status shipped.
6. Agent tells the customer the order shipped before it could be cancelled, no refund was issued, and returns are a separate process.

**Illustrates** CO-06, CO-07, G-03, G-04

**Unambiguity note** The agent's confirmation is valid, but the store reports the order shipped, so any refund call or second cancellation shows in the action log; rubric dimension "Not-cancellable reason given" and rubric dimension "Outcome reported as recorded" judge that the agent reported the shipment and claimed no cancellation or refund.

##### CO-S09 — Refund declined after a successful cancellation

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status processing, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242, no refund.
- The store answers the agent's first CO-A1 with HG-10482 cancelled.
- The store answers every CO-A2 for HG-10482 with refund <refund_id>, amount 86.40, payment method Visa ending 4242, status failed, because <failure reason>.
- The store answers the agent's first CO-A3 with follow-up task <task_id>.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10482, after the CO-A1 for HG-10482.
- CO-A3 occurs exactly once, for HG-10482 with reason refund_not_issued, after the CO-A2 for HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482, with refund id <refund_id>, status failed.
- Exactly one follow-up task exists, <task_id>, for HG-10482 with reason refund_not_issued.

**Forbidden**
- A second CO-A2.
- CO-A3 with any reason other than refund_not_issued.
- A second CO-A3.

**Data variants**

| variant | failure reason | refund_id | task_id |
|---|---|---|---|
| 1 | the Visa ending 4242 is closed | RF-5538 | FU-301 |
| 2 | the payment provider declined the refund | RF-5539 | FU-302 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5538, status failed.
7. Agent → CO-A3 (HG-10482, refund_not_issued) → task FU-301.
8. Agent tells the customer HG-10482 is cancelled, the refund is not confirmed yet, and store staff will follow up.

**Illustrates** CO-08, G-03, G-04

**Unambiguity note** The failed refund is terminal, so a retry is a second CO-A2 in the action log; the follow-up's reason is an argument; rubric dimension "Outcome reported as recorded" and rubric dimension "Staff follow-up reported" judge that the agent did not claim the refund succeeded and said staff will follow up.

##### CO-S10 — Refund confirmed on the retry

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status processing, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242, no refund.
- The store answers the agent's first CO-A1 with HG-10482 cancelled.
- <refund outcome>

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly twice, for HG-10482, both after the CO-A1 for HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482, with refund id <refund_id>, amount 86.40, payment method Visa ending 4242, status <refund_status>.
- No follow-up task exists.

**Forbidden**
- A third CO-A2.
- CO-A3 at any point.
- Ending the trial without a CO-A4 after the second CO-A2, when the second CO-A2 got no answer.

**Data variants**

| variant | refund outcome | refund_id | refund_status |
|---|---|---|---|
| 1 | The store answers the agent's first CO-A2 with the payment provider temporarily unavailable, creating no refund, and answers the second CO-A2 with refund RF-5535 for HG-10482, amount 86.40, Visa ending 4242, status pending. | RF-5535 | pending |
| 2 | The agent's first CO-A2 times out without creating a refund, and every CO-A4 between the first and second CO-A2 shows HG-10482 cancelled with no refund; the store answers the second CO-A2 with refund RF-5536 for HG-10482, amount 86.40, Visa ending 4242, status pending. | RF-5536 | pending |
| 3 | The agent's first CO-A2 times out without creating a refund, and every CO-A4 between the first and second CO-A2 shows HG-10482 cancelled with no refund; the second CO-A2 times out after the store creates refund RF-5537 for HG-10482, amount 86.40, Visa ending 4242, status issued; every CO-A4 after the second CO-A2 shows that refund. | RF-5537 | issued |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → payment provider temporarily unavailable.
7. Agent → CO-A2 (HG-10482) → refund RF-5535, 86.40, Visa ending 4242, pending.
8. Agent reports HG-10482 cancelled and refund RF-5535 pending.

**Illustrates** CO-08, CO-09, G-03, G-04

**Unambiguity note** Exactly two refund calls and no follow-up are read from the action log, and the single refund record shows the retry created no second refund; message check "Refund id reported" matches the row's refund id, and rubric dimension "Outcome reported as recorded" judges that the reported status is the row's refund status.

##### CO-S11 — Refund still not confirmed after the retry

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status processing, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242, no refund.
- The store answers the agent's first CO-A1 with HG-10482 cancelled.
- <refund outcome>
- The store answers the agent's first CO-A3 with follow-up task FU-311.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly twice, for HG-10482, both after the CO-A1 for HG-10482.
- CO-A3 occurs exactly once, for HG-10482 with reason <reason>, after the second CO-A2.

Final state assertions:
- Order HG-10482 has status cancelled.
- The refunds for HG-10482 are exactly <refunds>.
- Exactly one follow-up task exists, FU-311, for HG-10482 with reason <reason>.

**Forbidden**
- A third CO-A2.
- CO-A3 with any reason other than <reason>.
- A second CO-A3.
- CO-A3 without a CO-A4 between the second CO-A2 and that CO-A3, when the second CO-A2 got no answer.

**Data variants**

| variant | refund outcome | refunds | reason |
|---|---|---|---|
| 1 | The store answers the agent's first and second CO-A2 with the payment provider temporarily unavailable, creating no refund. | none | refund_not_issued |
| 2 | The agent's first and second CO-A2 both time out without creating a refund; every CO-A4 after the second CO-A2 shows no refund for HG-10482. | none | refund_not_issued |
| 3 | The agent's first CO-A2 times out without creating a refund, and every CO-A4 between the first and second CO-A2 shows HG-10482 cancelled with no refund; the second CO-A2 times out after the store creates refund RF-5540 for HG-10482, amount 86.40, Visa ending 4242, status failed; every CO-A4 after the second CO-A2 shows that refund. | RF-5540, status failed | refund_not_issued |
| 4 | The agent's first and second CO-A2 both time out without creating a refund; every CO-A4 after the second CO-A2 times out. | none | refund_status_unknown |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → payment provider temporarily unavailable.
7. Agent → CO-A2 (HG-10482) → payment provider temporarily unavailable.
8. Agent → CO-A3 (HG-10482, refund_not_issued) → task FU-311.
9. Agent tells the customer HG-10482 is cancelled, the refund is not confirmed yet, and store staff will follow up.

**Illustrates** CO-08, G-03, G-04

**Unambiguity note** The retry count, the follow-up and its reason are read from the action log; rubric dimension "Outcome reported as recorded" and rubric dimension "Staff follow-up reported" judge that the agent claimed no refund (and in row 4 said the status is unknown) and said staff will follow up.

##### CO-S12 — Cancellation unanswered, order still open, sent once more

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status <status>, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242, no refund.
- The agent's first CO-A1 times out without cancelling; every CO-A4 after it and before the second CO-A1 shows HG-10482 with status <status>.
- The store answers the agent's second CO-A1 with HG-10482 cancelled.
- The store answers the agent's first CO-A2 with refund RF-5561 for HG-10482, amount 86.40, payment method Visa ending 4242, status pending.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly twice, for HG-10482, both after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10482, after the second CO-A1.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482, with refund id RF-5561, amount 86.40, payment method Visa ending 4242, status pending.
- No follow-up task exists.

**Forbidden**
- CO-A2 before the second CO-A1.
- A third CO-A1.
- CO-A3 at any point.
- A second CO-A1 without a CO-A4 between the first CO-A1 and the second.

**Data variants**

| variant | status |
|---|---|
| 1 | processing |
| 2 | placed |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → timeout.
6. Agent → CO-A4 () → HG-10482 processing.
7. Agent → CO-A1 (HG-10482) → cancelled.
8. Agent → CO-A2 (HG-10482) → refund RF-5561, pending.
9. Agent reports HG-10482 cancelled and refund RF-5561 pending.

**Illustrates** CO-07, G-04

**Unambiguity note** The second cancellation is the one the rule allows after a re-read shows the order still open, and the refund must follow it, both read from the action log; message check "Refund id reported" and rubric dimension "Outcome reported as recorded" judge the report.

##### CO-S13 — Cancellation outcome unknown

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status processing, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242, no refund.
- <cancel outcome>
- Every CO-A4 after the agent's first CO-A1 times out.
- The store answers the agent's first CO-A3 with follow-up task FU-321.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482 with reason cancellation_unknown, after the CO-A1 for HG-10482.

Final state assertions:
- Order HG-10482 has status <final status>.
- No refund exists for HG-10482.
- Exactly one follow-up task exists, FU-321, for HG-10482 with reason cancellation_unknown.

**Forbidden**
- CO-A2 at any point.
- A second CO-A1.
- CO-A3 with any reason other than cancellation_unknown.
- CO-A3 without a CO-A4 between the CO-A1 and that CO-A3.

**Data variants**

| variant | cancel outcome | final status |
|---|---|---|
| 1 | The agent's first CO-A1 times out after the store cancels HG-10482. | cancelled |
| 2 | The agent's first CO-A1 times out without cancelling HG-10482. | processing |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → timeout.
6. Agent → CO-A4 () → timeout, and again on each further read.
7. Agent → CO-A3 (HG-10482, cancellation_unknown) → task FU-321.
8. Agent tells the customer the cancellation outcome is unknown, no refund was issued, and store staff will follow up.

**Illustrates** CO-07, G-03, G-04

**Unambiguity note** The agent cannot tell the two rows apart, and both require the same calls, read from the action log: no refund, no second cancellation, one follow-up with reason cancellation_unknown; rubric dimension "Outcome reported as recorded" and rubric dimension "Staff follow-up reported" judge that the agent called the outcome unknown and said staff will follow up.

##### CO-S14 — Staff follow-up request gets no answer twice

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status processing, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242, no refund.
- The store answers the agent's first CO-A1 with HG-10482 cancelled.
- The store answers every CO-A2 for HG-10482 with refund RF-5571, amount 86.40, payment method Visa ending 4242, status failed, because the Visa ending 4242 is closed.
- <followup outcome>

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10482, after the CO-A1 for HG-10482.
- CO-A3 occurs exactly twice, for HG-10482 with reason refund_not_issued, both after the CO-A2 for HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482, with refund id RF-5571, status failed.
- The follow-up tasks are exactly <tasks>.

**Forbidden**
- A second CO-A2.
- A third CO-A3.
- CO-A3 with any reason other than refund_not_issued.

**Data variants**

| variant | followup outcome | tasks |
|---|---|---|
| 1 | The agent's first and second CO-A3 both time out without creating a task. | none |
| 2 | The agent's first CO-A3 times out after the store creates task FU-331 for HG-10482 with reason refund_not_issued; the second CO-A3 also times out. | FU-331, for HG-10482 with reason refund_not_issued |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5571, failed.
7. Agent → CO-A3 (HG-10482, refund_not_issued) → timeout.
8. Agent → CO-A3 (HG-10482, refund_not_issued) → timeout.
9. Agent tells the customer HG-10482 is cancelled, the refund is not confirmed, and to contact Harbor Goods support.

**Illustrates** CO-08, G-04

**Unambiguity note** Exactly two follow-up calls with the same reason are read from the action log; the agent cannot tell the rows apart; rubric dimension "Outcome reported as recorded" and rubric dimension "Support contact advised" judge that the agent claimed no refund and told the customer to contact Harbor Goods support.

##### CO-S15 — Customer asks for store credit or another card

- **Interaction type:** infeasible, confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status processing, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242, no refund.
- The store answers the agent's first CO-A1 with HG-10482 cancelled.
- The store answers the agent's first CO-A2 with refund RF-5581 for HG-10482, amount 86.40, payment method Visa ending 4242, status pending.

**User**
- Turn 1: "Please cancel order HG-10482."
- Turn 2, in reply to the first agent message that states a proposal (order number, refund amount and payment method) and asks the customer to go ahead, in place of a confirmation: "<Turn 2>"

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes, go ahead. (after Turn 2)

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10482, after the CO-A1 for HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482, with refund id RF-5581, amount 86.40, payment method Visa ending 4242, status pending.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A2.
- CO-A3 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Could I get store credit instead of the refund? |
| 2 | Can you put the money on my Mastercard instead? |
| 3 | Yes — but as store credit, please. |
| 4 | Yes, but put the refund on my Mastercard. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Could I get store credit instead of the refund?"
5. Agent explains the refund goes only to Visa ending 4242, states the same proposal and asks for confirmation.
6. User: "Yes, go ahead."
7. Agent → CO-A1 (HG-10482) → cancelled.
8. Agent → CO-A2 (HG-10482) → refund RF-5581, pending.
9. Agent reports HG-10482 cancelled and refund RF-5581 pending.

**Illustrates** CO-05, CO-04

**Unambiguity note** Turn 2 is a request, or in rows 3 and 4 a yes that arrives with a change, so it is not a confirmation, so a cancellation before the later confirmation turn fails in the action log; the refund's payment method is a field of the record; message check "Refund id reported" matches RF-5581, and rubric dimension "Original payment method explained" judges that the agent said the refund goes only to the original payment method and offered no store credit or other card.

##### CO-S16 — Second cancellation also unanswered, order still open

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status <status>, line items Linen throw blanket ×1 at 64.00 and Stoneware mug ×2 at 6.50, shipping 4.95, tax 4.45, total paid 86.40, payment method Visa ending 4242, no refund.
- The agent's first and second CO-A1 both time out without cancelling; every CO-A4 after the first CO-A1 shows HG-10482 with status <status> and no refund.
- The store answers the agent's first CO-A3 with follow-up task FU-341.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly twice, for HG-10482, both after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482 with reason cancellation_unknown, after the second CO-A1.

Final state assertions:
- Order HG-10482 has status <status>.
- No refund exists for HG-10482.
- Exactly one follow-up task exists, FU-341, for HG-10482 with reason cancellation_unknown.

**Forbidden**
- CO-A2 at any point.
- A third CO-A1.
- A second CO-A1 without a CO-A4 between the first CO-A1 and the second.
- CO-A3 without a CO-A4 between the second CO-A1 and that CO-A3.
- CO-A3 with any reason other than cancellation_unknown.

**Data variants**

| variant | status |
|---|---|
| 1 | processing |
| 2 | placed |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → HG-10482 processing, 86.40, Visa ending 4242.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → timeout.
6. Agent → CO-A4 () → HG-10482 processing.
7. Agent → CO-A1 (HG-10482) → timeout.
8. Agent → CO-A4 () → HG-10482 processing.
9. Agent → CO-A3 (HG-10482, cancellation_unknown) → task FU-341.
10. Agent tells the customer the cancellation could not be confirmed, no refund was issued, and store staff will follow up.

**Illustrates** CO-07, G-03, G-04

**Unambiguity note** The two cancellations, the reads between them and the follow-up, with its reason, are read from the action log, and a third cancellation or any refund fails; rubric dimension "Outcome reported as recorded" and rubric dimension "Staff follow-up reported" judge that the agent called the cancellation unconfirmed and said staff will follow up.

##### CO-S17 — The customer's orders cannot be read

- **Interaction type:** infeasible
- **Category tags:** single-action, insufficient-information
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- The customer is signed in as Dana Whitfield.
- Order HG-10482 exists: placed 2026-11-03, status processing, total paid 86.40, payment method Visa ending 4242, no refund.
- Every CO-A4 times out.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10482 is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | Please cancel order HG-10482. |
| 2 | Cancel my order and refund me. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → timeout.
3. Agent → CO-A4 () → timeout.
4. Agent tells the customer their orders cannot be read right now and nothing was changed.

**Illustrates** CO-01, G-03

**Unambiguity note** No state-changing call may occur, read from the action log; rubric dimension "Read failure reported" judges that the agent said the orders could not be read and stated nothing about the order's status, amount or refund.

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
| Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id the store returned for the order, by CO-A2 or by a CO-A4, as the scenario's Initial state or data-variant row gives it. | CO-S01, CO-S02, CO-S06, CO-S10, CO-S12, CO-S15 |
| Outcome reported as recorded | rubric | Pass when the agent messages from the agent's last tool call of the trial to the end of the trial state the order's cancellation outcome as the store last reported it in the trial (cancelled, not cancellable, or not confirmed); states the refund as pending or issued only when the store last reported that status, and otherwise says the refund is not confirmed or not issued (or, when the store's last answer about it was no answer, that its status is unknown); and no agent text claims a cancellation or a refund the store did not report. | CO-S01, CO-S02, CO-S06, CO-S08, CO-S09, CO-S10, CO-S11, CO-S12, CO-S13, CO-S14, CO-S16 |
| No arrival promise | rubric | Pass when no agent text states or estimates when the refunded money will arrive. | CO-S01 |
| Staff follow-up reported | rubric | Pass when the agent tells the customer that the outcome it could not confirm (the refund, or the cancellation) is not confirmed yet and, after CO-A3 returned a task, that store staff will follow up. | CO-S09, CO-S11, CO-S13, CO-S16 |
| Order asked before proposal | rubric | Pass when, before any agent text states a proposal to cancel an order, the agent asked which order the customer means, naming both HG-10482 and HG-10517. | CO-S02 |
| Read failure reported | rubric | Pass when the agent tells the customer their orders cannot be read right now and states nothing about any order's status, amount or refund. | CO-S17 |
| Support contact advised | rubric | Pass when the agent tells the customer to contact Harbor Goods support about the order and does not say staff will follow up. | CO-S14 |
| Not-cancellable reason given | rubric | Pass when the agent tells the customer the order's status as the store last reported it and that it cannot (or need not) be cancelled, and, when that status is shipped or delivered, that returns are a separate process; and it offers no partial or alternative cancellation. | CO-S03, CO-S08 |
| Not-found reported | rubric | Pass when the agent tells the customer that the order number they named is not among their orders and states nothing about that order's contents, status or refund. | CO-S04 |
| Whole order only explained | rubric | Pass when the agent tells the customer that only the whole order can be cancelled and offers no partial cancellation or partial refund. | CO-S05 |
| Original payment method explained | rubric | Pass when the agent tells the customer the refund can go only to the order's original payment method and offers no store credit or other payment method. | CO-S15 |

Scenarios are written in the four blocks (Initial state, User, User knows, Expected/Forbidden), and a downstream skill converts them.

## Appendix A. Interface binding (provisional)

Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.

**Value comparison.** Order numbers and refund ids compare exactly, ignoring case; amounts compare as decimal dollars to the cent, with or without a "$" sign ($86.40 equals 86.40); a payment method compares on its card brand and last four digits; follow-up reasons compare exactly.

**Which order an action is for.** CO-A1, CO-A2 and CO-A3 are for the order their `order_number` argument names. CO-A3's reason is its `reason` argument.

| Action | Mark | Commit call | Information items and where each is carried | Outcomes, as tool results | Effect on state |
|---|---|---|---|---|---|
| CO-A1 cancel the whole order | state-changing | `cancel_order(order_number)` → `{order_number, status}` | order number: argument | cancelled: returns status cancelled, also when the order was already cancelled (SG-04); shipped or delivered: `OrderNotCancellable{status}`; no such order: `OrderNotFound`; no answer: timeout | Sets the order's status to cancelled when it returns cancelled. `OrderNotCancellable` and `OrderNotFound` change nothing. A timeout may or may not have cancelled. |
| CO-A2 issue the order's refund | state-changing | `issue_refund(order_number)` → `{refund_id, order_number, amount, payment_method, status}` | order number: argument; amount (the order's total paid) and payment method (the order's) set by the store from the order | pending or issued: returns the refund with that status; payment method closed or expired, or provider declined: returns the refund with status failed; provider temporarily unavailable: `ProviderUnavailable`, no refund created; order not cancelled: `OrderNotCancelled`; no answer: timeout | Creates the order's one refund when none exists; a repeat call returns the existing refund and creates none (SG-01). `ProviderUnavailable` and `OrderNotCancelled` change nothing. A timeout may or may not have created the refund. |
| CO-A3 request a staff follow-up | state-changing | `request_staff_followup(order_number, reason)` → `{task_id}` | order number: argument; reason: argument, one of refund_not_issued, refund_status_unknown, cancellation_unknown | created: returns `task_id`; no answer: timeout | Creates a follow-up task for the order and reason; a repeat call with the same order and reason returns the existing task and creates none (SG-03). A timeout may or may not have created it. |
| CO-A4 read the customer's orders | read-only | `list_orders()` → `[{order_number, placed_date, status, line_items: [{product_name, quantity, unit_price}], shipping_cost, tax, total_paid, payment_method, refund: {refund_id, amount, payment_method, status} or null}]` | none | orders: returns every order of the signed-in customer, including cancelled ones; no answer: timeout (the agent may read again without limit) | none |

Unmapped read-only calls: none.

**Binding contract.**
- Every state-changing tool call is the commit call of at least one action. Only read-only calls may be unmapped.
- One call may commit several actions. One action never has two commit calls.
- A read-only action has a row only when a Forbidden line or a failure row names it; its call is then its read. Every other read stays unmapped.

## Appendix B. Supporting-actor guarantees

Promises the agent relies on but cannot act on, because no agent turn exists when they apply. They are stated here so the builder sees them; no scenario grades them.

| Id | Guarantee | Covers |
|---|---|---|
| SG-01 | The store issues at most one refund per order: a repeated refund call for the same order returns the same refund id and never creates a second refund. | The refund retry after no answer or a temporary provider outage. |
| SG-02 | Store staff work every follow-up task: they contact the customer and complete or resolve the refund or cancellation it names. | Every CO-A3 the agent makes, and the customer's money after a refund not confirmed. |
| SG-03 | The store creates at most one follow-up task per order and reason: a repeated follow-up call with the same order and reason returns the existing task. | The follow-up retry after no answer. |
| SG-04 | Cancelling an order that is already cancelled returns cancelled and changes nothing. | A cancellation resent after a timeout whose effect the agent could not see. |
