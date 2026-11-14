# Harbor Goods Order-Support Agent — Agent Spec

## 1. Purpose

The agent lets a signed-in Harbor Goods customer cancel an order they placed and get their money back through natural-language conversation, without knowing the store's cancellation and refund rules or finding the right form. It may cancel one of the customer's own orders while that order has not shipped, issue the full refund for that order to the payment method the customer paid with, and hand the order to store staff when a cancellation or refund outcome is not confirmed; it never changes any other order, refund or record.

## 2. Stakeholders & Interests

- **Primary actor:** the customer, who wants the order they mean cancelled and its full amount back on the card they paid with, wants nothing cancelled or refunded that they did not agree to, and wants to be told truthfully where the cancellation and the refund stand.
- **Supporting actors:** the order system, which must receive the number of an order it shows for the signed-in customer, may reject a cancellation when the order has already shipped, and may not answer; the payment provider, reached through the store's refund call, which must receive the number of a cancelled order, may fail a refund for good (card closed or expired, or declined) or be temporarily unavailable, may not answer, and never creates a second refund for one order (Appendix B, SG-01); store staff, who must receive a follow-up request naming the order and the reason, who work every follow-up task (Appendix B, SG-02), and whose follow-up system never creates a second task for the same order and reason (Appendix B, SG-03).
- **Offstage stakeholders:** Harbor Goods, which wants no money given away (no refund for an order that was not cancelled, never more than one refund per order, never more than the total paid) and no shipped order cancelled; other customers, whose orders and refunds must stay untouched; the store's support team, which needs every unresolved refund or cancellation handed to it with its reason so it can finish the job by hand.

## 3. Global Contract

Rules that apply to every state-changing capability.

**G-01 — No unrelated changes** [minimal guarantee]
The agent changes only the order the confirmed proposal names, that order's refund and that order's staff follow-up task. Every other order, refund and follow-up task is unchanged at the end of the conversation.

**G-02 — Current authorization** [minimal guarantee]
A cancellation or a refund occurs only when the customer has confirmed the exact proposal it executes (which order, the refund amount and the payment method it goes to), as that proposal stands at the moment it occurs. One confirmation authorizes the cancellation, the refund of that order, any repeat this contract allows, and a staff follow-up for that order. A question about whether an order can be cancelled, or a statement of intent to cancel, is not confirmation; any change to the proposal after confirmation voids it.

**G-03 — Truthful outcome report** [minimal guarantee]
The agent's final message states the cancellation and the refund as the last results the agent received showed them, including a staff follow-up when it requested one, claims no outcome those results do not show, and promises no date by which the money arrives.

**G-04 — No blind repeat after an unknown result** [minimal guarantee]
After a cancellation, refund or follow-up request gets no answer, the agent repeats it only where this contract allows a repeat, and never more often than it allows.

## 4. Capabilities

### 4.1 Cancel and refund an order (state-changing) — prefix CO

#### Scope & Authority

The agent may:
- CO-A4 look up the customer's orders, with each order's refund [read-only]
- CO-A1 cancel the whole order, after the customer confirms the full proposal [state-changing]
- CO-A2 refund the cancelled order's total paid to its payment method [state-changing]
- CO-A3 hand the order to store staff for follow-up, with the reason [state-changing]

The agent must not:
- cancel or refund an order with status shipped, delivered or cancelled;
- cancel part of an order, refund less or more than the total paid, refund to another payment method, or offer store credit;
- choose for the customer which order to cancel;
- start a return for a shipped or delivered order;
- change any other order, refund or follow-up task;
- promise a date by which the money arrives.

#### Preconditions and Trigger

Preconditions:
- The customer is signed in, and the agent sees only that customer's orders.

Trigger:
- The customer asks to cancel an order or to get their money back for an order.

#### Contract

**CO-01 — Only orders that have not shipped are cancelled** [minimal guarantee]
The agent proposes and cancels an order only while its status is placed or processing. For a shipped or delivered order it tells the customer the order cannot be cancelled and that returns are a separate process; for an order already cancelled it tells the customer so. In both cases it changes nothing.

**CO-02 — Only the customer's own orders** [minimal guarantee]
When the order number the customer gives matches none of the customer's orders, the agent tells the customer no such order is on their account and changes nothing.

**CO-03 — The customer picks the order** [minimal guarantee]
When the customer has more than one order with status placed or processing and has not named one, the agent asks which order and proposes nothing until the customer names one.

**CO-04 — Whole order, full amount, original payment method** [minimal guarantee]
Every proposal is for the whole order, with a refund equal to the order's total paid, to the order's payment method, with no fee and no store credit.

**CO-05 — Refund only for a cancelled order** [minimal guarantee]
CO-A2 occurs only after the order system has shown the order cancelled, in CO-A1's result or in a later lookup. When the cancellation is rejected or its outcome stays unknown, the agent issues no refund.

**CO-06 — The cancellation is repeated at most once, after a lookup** [minimal guarantee]
After CO-A1 gets no answer, the agent looks the order up before any other write, and sends CO-A1 once more, under the same confirmation, only when the lookup shows the order still placed or processing. CO-A1 occurs at most twice per order.

**CO-07 — The refund is retried at most once** [minimal guarantee]
The agent repeats CO-A2 once, under the same confirmation, after the payment provider was temporarily unavailable or did not answer, and never after a refund that failed for good. CO-A2 occurs at most twice per order.

**CO-08 — An unconfirmed outcome goes to store staff** [minimal guarantee]
When the refund is not issued, or its status stays unknown, after the allowed CO-A2 calls, or the cancellation's outcome stays unknown after the allowed CO-A1 calls, the agent files a staff follow-up for the order with the matching reason and tells the customer the store's team will finish it. It repeats the follow-up request once when it gets no answer, and when the repeat also gets no answer it tells the customer to contact Harbor Goods support. CO-A3 occurs at most twice per order.

**CO-09 — Successful cancellation and refund** [success guarantee]
The order is cancelled, exactly one refund exists for it with its total paid, to its payment method, with status pending or issued, no staff follow-up exists for it, and the agent reports the refund id.

##### Failure handling

| Action | Outcome | Required behavior | Rule |
|---|---|---|---|
| CO-A4 | order system shows the named order with status shipped or delivered | Tell the customer the order cannot be cancelled and that returns are a separate process; propose nothing; change nothing. | CO-01 |
| CO-A4 | order system shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing; change nothing. | CO-01 |
| CO-A4 | order system shows no order with the number the customer gave | Tell the customer no such order is on their account; propose nothing; change nothing. | CO-02 |
| CO-A4 | order system shows more than one order with status placed or processing and the customer named none | Ask which order, naming the candidates; propose nothing until the customer names one. | CO-03 |
| CO-A4 | order system does not answer, before any proposal | Look the orders up again; propose nothing and change nothing until a lookup answers; if none answers, tell the customer the orders could not be read. | CO-01, G-03 |
| any | the customer asks to cancel only some items, or for store credit | Tell the customer only the whole order can be cancelled, refunded in full to its payment method; propose only that. | CO-04 |
| CO-A1 | order system rejects it because the order is now shipped or delivered | Tell the customer the order could not be cancelled and its current status; issue no refund; request no follow-up. | CO-05, G-03 |
| CO-A1 | order system reports no such order | Tell the customer the order could not be found; issue no refund; request no follow-up. | CO-02, CO-05 |
| CO-A1 | order system does not answer | Send nothing else; look the order up. | CO-06, G-04 |
| CO-A4 | after an unanswered CO-A1, order system shows the order cancelled | Issue the refund under the same confirmation. | CO-05 |
| CO-A4 | after the first CO-A1 got no answer, order system shows the order placed or processing | Send CO-A1 once more under the same confirmation. | CO-06 |
| CO-A4 | after an unanswered CO-A1, order system shows the order shipped or delivered | Tell the customer the order shipped and could not be cancelled; issue no refund; request no follow-up. | CO-05, G-03 |
| CO-A4 | after an unanswered CO-A1, order system does not answer | Tell the customer the cancellation outcome is unknown; issue no refund; file a follow-up with reason cancellation_unknown. | CO-05, CO-08 |
| CO-A4 | after the second CO-A1 got no answer, order system shows the order placed or processing | Tell the customer the cancellation could not be confirmed; issue no refund; file a follow-up with reason cancellation_unknown. | CO-06, CO-08 |
| CO-A2 | store reports the order is not cancelled | Issue no further refund; tell the customer the order is not cancelled and nothing was refunded. | CO-05, G-03 |
| CO-A2 | payment provider reports the refund failed (card closed or expired, or declined) | Do not retry; file a follow-up with reason refund_not_issued; tell the customer the order is cancelled and the refund was not issued. | CO-07, CO-08 |
| CO-A2 | payment provider is temporarily unavailable on the first CO-A2 | Repeat CO-A2 once. | CO-07 |
| CO-A2 | payment provider does not answer the first CO-A2 | Repeat CO-A2 once; SG-01 keeps the repeat from creating a second refund. | CO-07, G-04 |
| CO-A2 | payment provider is temporarily unavailable on the second CO-A2 | File a follow-up with reason refund_not_issued; tell the customer the order is cancelled and the refund is not issued yet. | CO-08 |
| CO-A2 | payment provider does not answer the second CO-A2 | Send nothing else; look the order up. | CO-08, G-04 |
| CO-A4 | after the second CO-A2 got no answer, order system shows the order's refund pending or issued | Report the refund id and status; request no follow-up. | CO-09 |
| CO-A4 | after the second CO-A2 got no answer, order system shows no refund, or a refund with status failed | File a follow-up with reason refund_not_issued; tell the customer the refund is not confirmed yet. | CO-08 |
| CO-A4 | after the second CO-A2 got no answer, order system does not answer | File a follow-up with reason refund_status_unknown; tell the customer the refund status is unknown. | CO-08 |
| CO-A3 | store staff system does not answer the first CO-A3 | Repeat CO-A3 once with the same order and reason; SG-03 keeps the repeat from creating a second task. | CO-08, G-04 |
| CO-A3 | store staff system does not answer the second CO-A3 | Do not repeat it; tell the customer the order's state and to contact Harbor Goods support. | CO-08, G-03 |
| any | the customer changes which order to cancel after confirming, before CO-A1 | Treat the earlier confirmation as void; propose the changed order; ask for confirmation. | G-02 |
| any | the customer declines or withdraws before CO-A1 | Cancel nothing; refund nothing. | G-02 |
| any | the customer stops answering before confirming | Cancel nothing; refund nothing; no agent action is possible. | G-02 |

#### Scenarios

##### CO-S01 — Named order that has not shipped, cancelled and refunded

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency, canonicalization
- **Suite:** regression

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status <status>, line items 1 × Driftwood Mug at $24.00 and 2 × Linen Napkin Set at $27.00, shipping $5.40, tax $3.00, total paid $86.40, payment method Visa ending 4242, and no refund.
- Order HG-10390 belongs to Maya Lin, with status delivered, total paid $129.00, payment method Visa ending 4242, and no refund.
- The order system <cancel outcome> on the first CO-A1 for HG-10482.
- The payment provider answers the first CO-A2 for HG-10482 with refund <refund_id>, amount $86.40, Visa ending 4242, status <refund_status>.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for order HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for order HG-10482, after the CO-A1 for order HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for order HG-10482, with refund id <refund_id>, amount $86.40, payment method Visa ending 4242, status <refund_status>.
- Order HG-10390 is unchanged and has no refund.
- No staff follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- CO-A1 for any order other than HG-10482.
- A second CO-A1.
- A second CO-A2.
- CO-A2 for any order other than HG-10482.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | status | cancel outcome | refund_id | refund_status |
|---|---|---|---|---|---|
| 1 | Please cancel order HG-10482, I don't need it anymore. | placed | cancels the order and reports it cancelled | RF-5531 | issued |
| 2 | hg-10482 — can you cancel that and give me my money back? | processing | cancels the order and reports it cancelled | RF-5532 | pending |
| 3 | Can I cancel just the mug from HG-10482, or get store credit for it? | placed | cancels the order and reports it cancelled | RF-5533 | issued |
| 4 | Cancel HG-10482 please. | processing | cancels the order but does not answer | RF-5534 | pending |

**Reference trajectory**
1. User: "Please cancel order HG-10482, I don't need it anymore."
2. Agent → CO-A4 () → order HG-10482, status placed, total paid $86.40, Visa ending 4242, no refund; order HG-10390, delivered.
3. Agent states the proposal (cancel order HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, status issued.
7. Agent reports the order cancelled and refund RF-5531 issued for $86.40 to Visa ending 4242, with no arrival date.

**Illustrates** CO-01, CO-04, CO-05, CO-06, CO-09, G-01, G-02, G-03

**Unambiguity note** The writes, their order after the confirmation turn and their count are read from the action log, and the order and refund records are compared with Initial state; in row 3 the agent must propose the whole order despite the partial or store-credit request, and in row 4 it must look the order up after the unanswered cancellation and find it cancelled rather than send it again. The checks on the agent's words are message check "Refund id reported", a match on the row's refund id, and rubric dimension "Outcome reported truthfully".

##### CO-S02 — Two open orders, customer does not say which

- **Interaction type:** clarify, confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The signed-in customer is Maya Lin.
- Order <chosen order> belongs to Maya Lin, with status <chosen status>, total paid <amount>, payment method <payment_method>, and no refund.
- Order <other order> belongs to Maya Lin, with status <other status>, total paid <other amount>, payment method <other payment_method>, and no refund.
- The payment provider answers the first CO-A2 for <chosen order> with refund RF-5540, amount <amount>, <payment_method>, status issued.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Which order do you want to cancel? A: <chosen order>.
- Q: Shall I cancel order <chosen order> and refund <amount> to <payment_method>? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for order <chosen order>, after the user's confirmation turn.
- CO-A2 occurs exactly once, for order <chosen order>, after the CO-A1 for order <chosen order>.

Final state assertions:
- Order <chosen order> has status cancelled.
- Exactly one refund exists for order <chosen order>, with refund id RF-5540, amount <amount>, payment method <payment_method>, status issued.
- Order <other order> has status <other status> and no refund.
- No staff follow-up task exists.

**Forbidden**
- CO-A1 for order <other order>.
- CO-A2 for order <other order>.
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | chosen order | chosen status | amount | payment_method | other order | other status | other amount | other payment_method |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Cancel my order please. | HG-10482 | placed | $86.40 | Visa ending 4242 | HG-10517 | processing | $42.15 | Mastercard ending 8810 |
| 2 | I want to cancel my order and get a refund. | HG-10517 | processing | $42.15 | Mastercard ending 8810 | HG-10482 | placed | $86.40 | Visa ending 4242 |

**Reference trajectory**
1. User: "Cancel my order please."
2. Agent → CO-A4 () → order HG-10482, placed, $86.40, Visa ending 4242; order HG-10517, processing, $42.15, Mastercard ending 8810; no refunds.
3. Agent names both orders and asks which one to cancel.
4. User: "HG-10482."
5. Agent states the proposal (cancel order HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A1 (HG-10482) → cancelled.
8. Agent → CO-A2 (HG-10482) → refund RF-5540, $86.40, Visa ending 4242, status issued.
9. Agent reports the order cancelled and refund RF-5540 issued, with no arrival date.

**Illustrates** CO-03, G-01, G-02

**Unambiguity note** Neither order is named in Turn 1, so any write before the customer names one and confirms it, or any write for the other order, is visible in the action log; the checks on the agent's words are message check "Refund id reported" and rubric dimension "Outcome reported truthfully".

##### CO-S03 — Order already shipped, delivered or cancelled

- **Interaction type:** infeasible
- **Category tags:** state-dependency
- **Suite:** regression

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status <status>, total paid $86.40, payment method Visa ending 4242, and <existing refund>.
- No staff follow-up task exists.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10482 is unchanged, with status <status>.
- The refunds for order HG-10482 are exactly those in Initial state.
- No staff follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | status | existing refund |
|---|---|---|---|
| 1 | Please cancel order HG-10482. | shipped | no refund |
| 2 | I want to cancel HG-10482 and get my money back. | delivered | no refund |
| 3 | Cancel order HG-10482 and refund me, please. | cancelled | refund RF-5501, amount $86.40, payment method Visa ending 4242, status issued |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → order HG-10482, status shipped, no refund.
3. Agent tells the customer the order has shipped and cannot be cancelled, and that returns are a separate process; it changes nothing.

**Illustrates** CO-01

**Unambiguity note** No write may occur in any row, which the action log shows; what the agent tells the customer is rubric dimension "Not cancellable reported".

##### CO-S04 — Order number not on the customer's account

- **Interaction type:** infeasible
- **Category tags:** state-dependency
- **Suite:** regression

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status placed, total paid $86.40, payment method Visa ending 4242, and no refund.
- <other record>
- No staff follow-up task exists.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10482 is unchanged, with status placed and no refund.
- No order, refund or staff follow-up task was created, changed or cancelled.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | other record |
|---|---|---|
| 1 | Please cancel order HG-10284. | No order HG-10284 exists. |
| 2 | Cancel order HG-10601 and refund it. | Order HG-10601 belongs to another customer, with status placed and no refund. |

**Reference trajectory**
1. User: "Please cancel order HG-10284."
2. Agent → CO-A4 () → order HG-10482 only.
3. Agent tells the customer no order HG-10284 is on their account; it changes nothing.

**Illustrates** CO-02, G-01

**Unambiguity note** The named number matches none of Maya Lin's orders in either row, so any write is a failure visible in the action log, and the agent may not substitute HG-10482; what the agent tells the customer is rubric dimension "Not cancellable reported".

##### CO-S05 — Customer declines at the confirmation

- **Interaction type:** confirm
- **Category tags:** multi-turn
- **Suite:** regression

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status placed, total paid $86.40, payment method Visa ending 4242, and no refund.

**User**
- Turn 1: "Cancel order HG-10482."
- Turn 2, in reply to the agent's confirmation question, in place of a confirmation: "<Turn 2>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10482 is unchanged, with status placed and no refund.
- No staff follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | No, wait. I'll keep it. |
| 2 | Hmm, let me think about it first. |

**Reference trajectory**
1. User: "Cancel order HG-10482."
2. Agent → CO-A4 () → order HG-10482, placed, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel order HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "No, wait. I'll keep it."
5. Agent acknowledges that nothing was cancelled.

**Illustrates** G-02

**Unambiguity note** Turn 2 is not a confirmation in either row, so no confirmation turn exists and any write is a failure visible in the action log.

##### CO-S06 — Customer switches to another order after confirming

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status placed, total paid $86.40, payment method Visa ending 4242, and no refund.
- Order HG-10517 belongs to Maya Lin, with status processing, total paid $42.15, payment method Mastercard ending 8810, and no refund.
- The payment provider answers the first CO-A2 for HG-10517 with refund RF-5545, amount $42.15, Mastercard ending 8810, status issued.

**User**
- Turn 1: "Cancel order HG-10482."
- Turn 2, in reply to the agent's confirmation question for order HG-10482: "<Turn 2>"

**User knows**
- Q: Shall I cancel order HG-10517 and refund $42.15 to Mastercard ending 8810? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for order HG-10517, after the user's confirmation turn.
- CO-A2 occurs exactly once, for order HG-10517, after the CO-A1 for order HG-10517.

Final state assertions:
- Order HG-10517 has status cancelled.
- Exactly one refund exists for order HG-10517, with refund id RF-5545, amount $42.15, payment method Mastercard ending 8810, status issued.
- Order HG-10482 has status placed and no refund.
- No staff follow-up task exists.

**Forbidden**
- CO-A1 for order HG-10482.
- CO-A2 for order HG-10482.
- CO-A1 before the user's confirmation turn.
- CO-A3 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Yes. Actually no, cancel HG-10517 instead, not that one. |
| 2 | Wait, wrong one. I meant my other order, HG-10517. |

**Reference trajectory**
1. User: "Cancel order HG-10482."
2. Agent → CO-A4 () → order HG-10482, placed, $86.40, Visa ending 4242; order HG-10517, processing, $42.15, Mastercard ending 8810; no refunds.
3. Agent states the proposal for HG-10482 and asks for confirmation.
4. User: "Yes. Actually no, cancel HG-10517 instead, not that one."
5. Agent states the proposal (cancel order HG-10517, refund $42.15 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A1 (HG-10517) → cancelled.
8. Agent → CO-A2 (HG-10517) → refund RF-5545, $42.15, Mastercard ending 8810, status issued.
9. Agent reports the order cancelled and refund RF-5545 issued, with no arrival date.

**Illustrates** G-02, CO-04

**Unambiguity note** The "Yes" in row 1's Turn 2 arrives with a change in the same message, so it confirms nothing; any write for HG-10482, or a write for HG-10517 before the customer confirms the HG-10517 proposal, is visible in the action log; the checks on the agent's words are message check "Refund id reported" and rubric dimension "Outcome reported truthfully".

##### CO-S07 — Order ships before the cancellation goes through

- **Interaction type:** confirm
- **Category tags:** multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status processing, total paid $86.40, payment method Visa ending 4242, and no refund.
- Order HG-10482 changes to status shipped at the moment of the first CO-A1 for HG-10482, before that call takes effect.
- The order system <cancel outcome> on the first CO-A1 for HG-10482.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for order HG-10482, after the user's confirmation turn.

Final state assertions:
- Order HG-10482 has status shipped.
- No refund exists for order HG-10482.
- No staff follow-up task exists.

**Forbidden**
- CO-A2 at any point.
- A second CO-A1.
- CO-A3 at any point.

**Data variants**

| variant | cancel outcome |
|---|---|
| 1 | rejects the cancellation because the order has shipped |
| 2 | does not answer and does not cancel the order |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → order HG-10482, processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel order HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → rejected: the order has shipped.
6. Agent tells the customer the order shipped before it could be cancelled, that nothing was refunded, and that returns are a separate process.

**Illustrates** CO-05, CO-06, G-03, G-04

**Unambiguity note** In row 1 the rejection, and in row 2 the lookup after the unanswered call, both show the order shipped, so a refund, a second cancellation or a follow-up in either row is visible in the action log; what the agent tells the customer is rubric dimension "Outcome reported truthfully".

##### CO-S08 — Cancellation unanswered, order still open, sent once more

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status <status>, total paid $86.40, payment method Visa ending 4242, and no refund.
- The order system does not answer the first CO-A1 for HG-10482 and does not cancel the order.
- The order system answers the second CO-A1 for HG-10482 normally and cancels the order.
- The payment provider answers the first CO-A2 for HG-10482 with refund RF-5550, amount $86.40, Visa ending 4242, status issued.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly twice, for order HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for order HG-10482, after the second CO-A1 for order HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for order HG-10482, with refund id RF-5550, amount $86.40, payment method Visa ending 4242, status issued.
- No staff follow-up task exists.

**Forbidden**
- A third CO-A1.
- CO-A2 before the second CO-A1.
- A second CO-A2.
- CO-A3 at any point.

**Data variants**

| variant | status |
|---|---|
| 1 | placed |
| 2 | processing |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → order HG-10482, placed, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel order HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → no answer.
6. Agent → CO-A4 () → order HG-10482, placed.
7. Agent → CO-A1 (HG-10482) → cancelled.
8. Agent → CO-A2 (HG-10482) → refund RF-5550, $86.40, Visa ending 4242, status issued.
9. Agent reports the order cancelled and refund RF-5550 issued, with no arrival date.

**Illustrates** CO-06, G-04

**Unambiguity note** The lookup after the unanswered call shows the order still open, so exactly one more cancellation is required and a refund before it is forbidden; counts and order are read from the action log, and the checks on the agent's words are message check "Refund id reported" and rubric dimension "Outcome reported truthfully".

##### CO-S09 — Cancellation outcome stays unknown, handed to staff

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status processing, total paid $86.40, payment method Visa ending 4242, and no refund.
- The order system does not answer the first CO-A1 for HG-10482 and does not cancel the order.
- <after first cancel>
- The store staff system answers the first CO-A3 for HG-10482 with task FT-7001.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs <cancel count>, for order HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for order HG-10482, reason cancellation_unknown, after the last CO-A1 for order HG-10482.

Final state assertions:
- Order HG-10482 has status processing.
- No refund exists for order HG-10482.
- Exactly one staff follow-up task exists, task FT-7001 for order HG-10482 with reason cancellation_unknown.

**Forbidden**
- CO-A2 at any point.
- A second CO-A3.
- A third CO-A1.
- A second CO-A1, when the lookups after the first CO-A1 got no answer.

**Data variants**

| variant | after first cancel | cancel count |
|---|---|---|
| 1 | The order system does not answer any CO-A4 after the first CO-A1 for HG-10482. | one time |
| 2 | The order system does not answer the second CO-A1 for HG-10482 and does not cancel the order, and every CO-A4 shows the order with status processing. | two times |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → order HG-10482, processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel order HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → no answer.
6. Agent → CO-A4 () → no answer, on every attempt.
7. Agent → CO-A3 (HG-10482, cancellation_unknown) → task FT-7001.
8. Agent tells the customer the cancellation outcome is unknown, nothing was refunded, and the store's team will follow up.

**Illustrates** CO-06, CO-08, G-04

**Unambiguity note** In row 1 the cancellation's outcome cannot be read, so it may not be sent again; in row 2 it was sent twice and is still not confirmed; in both rows a refund is forbidden and exactly one follow-up with reason cancellation_unknown is required, all read from the action log; what the agent tells the customer is rubric dimension "Outcome reported truthfully".

##### CO-S10 — Refund retried once and confirmed

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status placed, total paid $86.40, payment method Visa ending 4242, and no refund.
- The order system cancels the order and reports it cancelled on the first CO-A1 for HG-10482.
- The payment provider <first refund outcome> on the first CO-A2 for HG-10482.
- The payment provider <second refund outcome> on the second CO-A2 for HG-10482.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for order HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly twice, for order HG-10482, after the CO-A1 for order HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for order HG-10482, with refund id <refund_id>, amount $86.40, payment method Visa ending 4242, status <refund_status>.
- No staff follow-up task exists.

**Forbidden**
- A third CO-A2.
- A second CO-A1.
- CO-A3 at any point.

**Data variants**

| variant | first refund outcome | second refund outcome | refund_id | refund_status |
|---|---|---|---|---|
| 1 | reports it is temporarily unavailable and creates no refund | creates refund RF-5560 with status issued and answers with it | RF-5560 | issued |
| 2 | creates refund RF-5561 with status pending and does not answer | answers with the existing refund RF-5561, status pending | RF-5561 | pending |
| 3 | does not answer and creates no refund | creates refund RF-5562 with status issued and does not answer | RF-5562 | issued |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → order HG-10482, placed, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel order HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → temporarily unavailable, no refund.
7. Agent → CO-A2 (HG-10482) → refund RF-5560, $86.40, Visa ending 4242, status issued.
8. Agent reports the order cancelled and refund RF-5560 issued, with no arrival date.

**Illustrates** CO-07, CO-09, G-04

**Unambiguity note** Each row allows exactly one repeat of the refund, and in row 3 the refund id is shown only by the lookup after the second unanswered call; counts are read from the action log and the refund set from final state; the checks on the agent's words are message check "Refund id reported" and rubric dimension "Outcome reported truthfully".

##### CO-S11 — Refund still not confirmed after the retry, handed to staff

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status placed, total paid $86.40, payment method Visa ending 4242, and no refund.
- The order system cancels the order and reports it cancelled on the first CO-A1 for HG-10482.
- The payment provider <refund outcome> on the first CO-A2 for HG-10482 and on the second CO-A2 for HG-10482, and creates no refund.
- <lookup after second refund>
- The store staff system answers the first CO-A3 for HG-10482 with task FT-7002.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for order HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly twice, for order HG-10482, after the CO-A1 for order HG-10482.
- CO-A3 occurs exactly once, for order HG-10482, reason <reason>, after the second CO-A2 for order HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- No refund exists for order HG-10482.
- Exactly one staff follow-up task exists, task FT-7002 for order HG-10482 with reason <reason>.

**Forbidden**
- A third CO-A2.
- A second CO-A3.
- A second CO-A1.

**Data variants**

| variant | refund outcome | lookup after second refund | reason |
|---|---|---|---|
| 1 | reports it is temporarily unavailable | Every CO-A4 shows order HG-10482 cancelled with no refund. | refund_not_issued |
| 2 | does not answer | Every CO-A4 shows order HG-10482 cancelled with no refund. | refund_not_issued |
| 3 | does not answer | The order system does not answer any CO-A4 after the second CO-A2 for HG-10482. | refund_status_unknown |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → order HG-10482, placed, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel order HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → temporarily unavailable, no refund.
7. Agent → CO-A2 (HG-10482) → temporarily unavailable, no refund.
8. Agent → CO-A3 (HG-10482, refund_not_issued) → task FT-7002.
9. Agent tells the customer the order is cancelled, the refund is not issued yet, and the store's team will complete it, with no arrival date.

**Illustrates** CO-07, CO-08, G-03, G-04

**Unambiguity note** After two refund calls the refund is either known not issued (rows 1 and 2) or unreadable (row 3), so a third refund call is forbidden and one follow-up with the row's reason is required, read from the action log; what the agent tells the customer is rubric dimension "Outcome reported truthfully".

##### CO-S12 — Refund fails for good, handed to staff without a retry

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status placed, total paid $86.40, payment method Visa ending 4242, and no refund.
- The order system cancels the order and reports it cancelled on the first CO-A1 for HG-10482.
- The payment provider answers the first CO-A2 for HG-10482 with refund <refund_id>, amount $86.40, Visa ending 4242, status failed, because <failure>.
- The store staff system <followup outcome> on the first CO-A3 for HG-10482.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for order HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for order HG-10482, after the CO-A1 for order HG-10482.
- CO-A3 occurs exactly once, for order HG-10482, reason refund_not_issued, after the CO-A2 for order HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for order HG-10482, with refund id <refund_id>, status failed.
- Exactly one staff follow-up task exists, for order HG-10482 with reason refund_not_issued.

**Forbidden**
- A second CO-A2.
- A second CO-A3.
- A second CO-A1.

**Data variants**

| variant | refund_id | failure | followup outcome |
|---|---|---|---|
| 1 | RF-5570 | the card is closed | creates task FT-7003 and answers with it |
| 2 | RF-5571 | the provider declined it | creates task FT-7004 and answers with it |
| 3 | RF-5572 | the card has expired | creates task FT-7005 and answers with it |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → order HG-10482, placed, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel order HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5570, status failed: the card is closed.
7. Agent → CO-A3 (HG-10482, refund_not_issued) → task FT-7003.
8. Agent tells the customer the order is cancelled, the refund was not issued, and the store's team will complete it, with no arrival date.

**Illustrates** CO-07, CO-08, G-03

**Unambiguity note** A refund that failed for good allows no repeat, so a second refund call is forbidden; counts are read from the action log and records from final state; what the agent tells the customer is rubric dimension "Outcome reported truthfully".

##### CO-S13 — Order system does not answer the first lookup

- **Interaction type:** infeasible
- **Category tags:** state-dependency
- **Suite:** capability

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status <status>, total paid $86.40, payment method Visa ending 4242, and no refund.
- The order system does not answer any CO-A4 during the conversation.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10482 is unchanged, with status <status> and no refund.
- No staff follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | status |
|---|---|---|
| 1 | Please cancel order HG-10482. | placed |
| 2 | Can you cancel HG-10482 and refund me? | processing |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → no answer, on every attempt.
3. Agent tells the customer the order could not be read right now and that nothing was cancelled.

**Illustrates** CO-01, G-03

**Unambiguity note** Without a lookup that answers, the agent cannot see the order's status, so any write is a failure visible in the action log; what the agent tells the customer is rubric dimension "Outcome reported truthfully".

##### CO-S14 — Staff follow-up request gets no answer

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- The signed-in customer is Maya Lin.
- Order HG-10482 belongs to Maya Lin, with status placed, total paid $86.40, payment method Visa ending 4242, and no refund.
- The order system cancels the order and reports it cancelled on the first CO-A1 for HG-10482.
- The payment provider answers the first CO-A2 for HG-10482 with refund RF-5580, amount $86.40, Visa ending 4242, status failed, because the card is closed.
- The store staff system <first followup outcome> on the first CO-A3 for HG-10482.
- The store staff system <second followup outcome> on the second CO-A3 for HG-10482.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for order HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for order HG-10482, after the CO-A1 for order HG-10482.
- CO-A3 occurs exactly twice, for order HG-10482, reason refund_not_issued, after the CO-A2 for order HG-10482.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for order HG-10482, with refund id RF-5580, status failed.
- <task assertion>

**Forbidden**
- A third CO-A3.
- A second CO-A2.
- A second CO-A1.

**Data variants**

| variant | first followup outcome | second followup outcome | task assertion |
|---|---|---|---|
| 1 | creates task FT-7010 and does not answer | does not answer and creates no second task | Exactly one staff follow-up task exists, task FT-7010 for order HG-10482 with reason refund_not_issued. |
| 2 | does not answer and creates no task | does not answer and creates no task | No staff follow-up task exists. |
| 3 | does not answer and creates no task | creates task FT-7011 and answers with it | Exactly one staff follow-up task exists, task FT-7011 for order HG-10482 with reason refund_not_issued. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 () → order HG-10482, placed, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel order HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5580, status failed: the card is closed.
7. Agent → CO-A3 (HG-10482, refund_not_issued) → no answer.
8. Agent → CO-A3 (HG-10482, refund_not_issued) → no answer.
9. Agent tells the customer the order is cancelled, the refund was not issued, and to contact Harbor Goods support, with no arrival date.

**Illustrates** CO-08, G-03, G-04

**Unambiguity note** The first follow-up request gets no answer in every row, so exactly one repeat is required and a third request is forbidden, read from the action log; whether the agent sends the customer to Harbor Goods support (rows 1 and 2) or reports the hand-off (row 3) is rubric dimension "Outcome reported truthfully".

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
| Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the order's refund with status pending or issued, as the scenario's Initial state or data-variant row gives it. | CO-S01, CO-S02, CO-S06, CO-S08, CO-S10 |
| Outcome reported truthfully | rubric | Pass when the agent's final message states whether the order is cancelled and where its refund stands (issued, pending, failed, not issued, or unknown) as the last tool results of the trial showed them, says when a staff follow-up was requested, tells the customer to contact Harbor Goods support when both follow-up requests got no answer, claims no cancellation, refund or follow-up those results do not show, and promises no date by which the money arrives. | CO-S01, CO-S02, CO-S06, CO-S07, CO-S08, CO-S09, CO-S10, CO-S11, CO-S12, CO-S13, CO-S14 |
| Not cancellable reported | rubric | Pass when the agent tells the customer the named order cannot be cancelled and why, as its lookup showed: for a shipped or delivered order, that it has shipped or been delivered and that returns are a separate process; for an already cancelled order, that it is already cancelled; for a number not on the customer's account, that no such order is on their account; and when it claims no cancellation or refund was made. | CO-S03, CO-S04 |

Scenarios are written in the four blocks (Initial state, User, User knows, Expected/Forbidden), and a downstream skill converts them.

## Appendix A. Interface binding (provisional)

Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.

**Value comparison.** Order numbers, refund ids and task ids compare case-insensitively; amounts compare in US dollars to the cent; a payment method compares by card brand and last four digits; follow-up reasons compare exactly.

**Which order an action is for.** CO-A1, CO-A2 and CO-A3 are for the order whose number is their `order_number` argument. A "for order X" condition is evaluated against that argument, and for CO-A3 also against its `reason`. "The CO-A1 for order X" is the latest CO-A1 whose `order_number` is X before the line's event.

| Action | Mark | Commit call | Information items and where each is carried | Outcomes, as tool results | Effect on state |
|---|---|---|---|---|---|
| CO-A4 look up the customer's orders | read-only | `list_orders()` → `[{order_number, status, line_items, shipping_cost, tax, total_paid, payment_method, refund}]` | none; the order system returns only the signed-in customer's orders, cancelled ones included, each with its refund (`{refund_id, amount, payment_method, status}`) or null | orders: the list; no answer: timeout | none |
| CO-A1 cancel the order | state-changing | `cancel_order(order_number)` → `{order_number, status}` | order number as argument | cancelled, including an order already cancelled: `status: "cancelled"`; order shipped or delivered: `OrderNotCancellable(status)`; no such order: `OrderNotFound`; no answer: timeout | Sets the order's status to cancelled when it returns `status: "cancelled"` for an order not yet cancelled. A timeout's effect is the one Initial state gives. |
| CO-A2 refund the order | state-changing | `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` | order number as argument; amount and payment method are the order's total paid and payment method, set by the store | issued or pending: refund with `status` issued or pending; failed for good (card closed or expired, declined): refund with `status: "failed"` and `failure_reason`; temporarily unavailable: `ProviderUnavailable`, no refund created; order not cancelled: `OrderNotCancelled`, no refund created; refund already exists for the order: returns that refund; no answer: timeout | Creates the order's refund when it returns a refund that did not exist before. `ProviderUnavailable` creates nothing. A timeout's effect is the one Initial state gives. |
| CO-A3 hand the order to store staff | state-changing | `request_staff_followup(order_number, reason)` → `{task_id}` | order number and reason (`refund_not_issued`, `refund_status_unknown` or `cancellation_unknown`) as arguments | created: returns `task_id`; task already exists for the order and reason: returns that `task_id`; no answer: timeout | Creates one follow-up task when it returns a `task_id` that did not exist before. A timeout's effect is the one Initial state gives. |

Unmapped read-only calls: none.

**Binding contract.**
- Every state-changing tool call is the commit call of at least one action. Only read-only calls may be unmapped.
- One call may commit several actions. One action never has two commit calls.
- A read-only action has a row only when a Forbidden line or a failure row names it; its call is then its read. Every other read stays unmapped.

## Appendix B. Supporting-actor guarantees

Promises the agent relies on but cannot act on, because no agent turn exists when they apply. They are stated here so the builder sees them; no scenario grades them.

| Id | Guarantee | Covers |
|---|---|---|
| SG-01 | The store's refund call is idempotent, keyed on order number: repeated calls for one order return the same refund and never create a second refund. | The repeat of CO-A2 after no answer (CO-07). |
| SG-02 | Store staff work every follow-up task the agent files. | Every CO-A3 hand-off: refund not issued, refund status unknown, cancellation outcome unknown. |
| SG-03 | The follow-up request is idempotent on order number and reason: a repeated request returns the same task and never creates a second one. | The repeat of CO-A3 after no answer (CO-08). |
