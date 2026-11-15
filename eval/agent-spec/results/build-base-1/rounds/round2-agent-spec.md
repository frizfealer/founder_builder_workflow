# Harbor Goods Order-Support Agent — Agent Spec

## 1. Purpose

The agent lets a signed-in Harbor Goods customer cancel an order they placed and get their money back through natural-language conversation, without knowing the store's cancellation and refund rules or finding the right form. It may cancel one whole order that has not shipped, issue that order's full refund to the order's payment method once the customer confirms, and ask store staff to follow up on that order when the refund or the cancellation cannot be confirmed; it never changes any other order, refund or record.

## 2. Stakeholders & Interests

- **Primary actor:** the customer, who wants the order they mean cancelled and the full amount they paid returned to the card they paid with, wants nothing cancelled or refunded that they did not agree to, and wants to be told truthfully what happened, including when something is not yet confirmed.
- **Supporting actors:** the store's order system, which must receive the order number of an order the customer confirmed, rejects a cancellation once the order has shipped or been delivered, and may not answer; the payment provider, which receives the refund through the store, may be temporarily unavailable, may decline, may find the payment method can no longer receive money, and may not answer; store staff, who work every follow-up task the agent creates (Appendix B, SG-02) and need the order number and the reason to act on it.
- **Offstage stakeholders:** Harbor Goods, which wants no shipped order cancelled, no refund of more than was paid, at most one refund per order, and no promise made on its behalf that it did not make (a fee waiver, store credit, an arrival date); the customer's other orders, which must stay exactly as they are; the store's manual refund process, which needs a follow-up task for every order whose refund is not confirmed, so no customer is left cancelled without their money.

## 3. Global Contract

Rules that apply to every state-changing capability.

**G-01 — No unrelated changes** [minimal guarantee]
The agent changes only the order the current request is about: its cancellation, its refund and a staff follow-up for it. Every other order, refund and follow-up task is unchanged at the end of the conversation.

**G-02 — Current authorization** [minimal guarantee]
The agent cancels an order or issues its refund only after the customer has confirmed the full proposal that action carries out: the order number, the refund amount and the payment method the refund goes to, as the proposal stands at that moment. A statement that the customer wants to cancel, or a question about what they would get back, is not confirmation, and any change to the proposal after confirmation voids it. One confirmation authorizes both the cancellation and the refund of that proposal, and any repeat of either that a rule of this spec allows.

**G-03 — Truthful reporting** [minimal guarantee]
The agent tells the customer the outcome of each action as the store last reported it. It never says an order was cancelled, a refund issued or a follow-up created unless the store reported it, and when an outcome is not known it says that it is not known.

**G-04 — No blind repeat** [minimal guarantee]
After a state-changing action got no answer or an error, the agent sends it again only where a rule of this spec allows it, and never sends the same action for the same order more than twice in one conversation.

## 4. Capabilities

### 4.1 Cancel an Order and Refund It (state-changing) — prefix CO

#### Scope & Authority

The agent may:
- CO-A1 cancel the customer's whole order, after the customer confirms the full proposal [state-changing]
- CO-A2 issue the refund of the order's total paid to the order's payment method, after the store reports the order cancelled [state-changing]
- CO-A3 ask store staff to follow up on the order, stating the reason [state-changing]
- CO-A4 look up the customer's orders and their refunds [read-only]

The agent must not:
- cancel some items of an order, or start a return;
- cancel an order that is shipped, delivered or already cancelled;
- refund an amount other than the order's total paid, refund to any other payment method, offer store credit or charge a fee;
- promise when the refunded money will arrive;
- choose which order the customer means when more than one could be meant;
- cancel, refund or change any other order.

#### Preconditions and Trigger

Preconditions:
- The customer is signed in, and the agent sees only that customer's orders and their refunds.

Trigger:
- The customer asks to cancel an order or to get their money back for an order.

#### Contract

**CO-01 — Only placed or processing orders are cancelled** [minimal guarantee]
The agent proposes and cancels only an order whose status is placed or processing. For a shipped or delivered order it says the order can no longer be cancelled and that returns are a separate process; for a cancelled order it says the order is already cancelled. In each case it changes nothing.

**CO-02 — Whole order only** [minimal guarantee]
The agent cancels only whole orders. When the customer asks to cancel some of an order's items, the agent says only the whole order can be cancelled, and cancels nothing the customer has not confirmed as a whole-order proposal.

**CO-03 — The order is named, never guessed** [minimal guarantee]
The agent proposes a cancellation only for an order the customer identified among their own orders. When more than one placed or processing order could be meant, it asks which one; when the order the customer names matches none of their orders, it says so and changes nothing.

**CO-04 — The proposal is the full refund** [minimal guarantee]
The proposal states the order number, a refund of the order's total paid (items, shipping and tax) and the order's payment method. The agent offers no store credit, charges no fee and promises nothing about when the money arrives.

**CO-05 — Refund only after a reported cancellation** [minimal guarantee]
The agent issues the refund only after the store has reported the order cancelled, in answer to the cancellation or in a look-up after it. When the store rejected the cancellation or its outcome is unknown, the agent issues no refund.

**CO-06 — An unanswered cancellation is resolved by a look-up** [minimal guarantee]
When the cancellation got no answer, the agent looks the order up before taking any other action for it. Cancelled: it goes on to the refund. Still placed or processing: it sends the cancellation once more under the same confirmation. Shipped or delivered: it reports that and issues no refund. No answer to the look-up: it tells the customer the outcome is unknown, issues no refund and asks staff to follow up on the unknown cancellation.

**CO-07 — Refund errors are retried only when temporary** [minimal guarantee]
When the payment provider is temporarily unavailable, the agent sends the refund once more. When the refund failed because the payment method can no longer receive money or the provider declined, the agent does not send it again, tells the customer the refund was not issued and asks staff to follow up on the refund not issued.

**CO-08 — An unanswered refund is resolved before it is reported** [minimal guarantee]
When the refund got no answer, the agent sends it once more. When that also got no answer, the agent looks up the refund: pending or issued, it reports that status; failed or no refund, it tells the customer the refund is not confirmed yet and asks staff to follow up on the refund not issued; no answer to the look-up, it tells the customer the refund's status is unknown and asks staff to follow up on the unknown refund status.

**CO-09 — Staff follow up whatever is not confirmed** [minimal guarantee]
When the conversation would otherwise end with the cancellation unknown, or with an order the store reported cancelled and no refund the store reported pending or issued, the agent asks staff to follow up on that order, with the reason that matches, and tells the customer that store staff will follow up. When the follow-up request got no answer, the agent sends it once more; when that also got no answer, it tells the customer to contact Harbor Goods support about the order.

**CO-10 — Rejected cancellation is reported, not refunded** [minimal guarantee]
When the store rejects the cancellation because the order has shipped or been delivered since the agent read it, or because it finds no such order, the agent tells the customer the order was not cancelled and why, and issues no refund and no follow-up.

**CO-11 — Successful cancellation** [success guarantee]
The order's status is cancelled; exactly one refund exists for it, for the order's total paid, to the order's payment method, with status pending or issued; no follow-up task exists for it; and the agent has told the customer the refund id and the refund's status.

##### Failure handling

| Action | Outcome | Required behavior | Rule |
|---|---|---|---|
| any | the customer asks to cancel some of an order's items | Say only the whole order can be cancelled; propose the whole order only if the customer wants that; cancel nothing partial. | CO-02 |
| any | more than one placed or processing order could be the one the customer means | Ask which order; propose nothing until the customer names one. | CO-03 |
| any | the order the customer names matches none of their orders | Say no such order was found; change nothing. | CO-03 |
| any | the order the customer names is shipped, delivered or cancelled | Say it cannot be cancelled and why (returns are a separate process for shipped or delivered); change nothing. | CO-01 |
| any | the customer changes the proposal in reply to it, or after confirming and before CO-A1 | Treat the confirmation as void; state the changed proposal; ask for confirmation again. | G-02 |
| any | the customer does not confirm, or stops answering | Cancel and refund nothing. | G-02 |
| CO-A4 | before any proposal, the store's order system does not answer the look-up, however often the agent repeats it | Tell the customer their orders cannot be looked up right now; propose, cancel and refund nothing, including from figures the customer gives. | CO-04, G-02, G-03 |
| CO-A1 | the store's order system reports the order not cancellable, with status shipped or delivered | Tell the customer the order has shipped or been delivered and was not cancelled, and that returns are a separate process; issue no refund and no follow-up. | CO-10 |
| CO-A1 | the store's order system reports no such order | Tell the customer the order was not found and was not cancelled; issue no refund and no follow-up. | CO-10 |
| CO-A1 | the store's order system does not answer (result unknown) | Send nothing else for the order until a look-up has answered or failed; continue by the CO-A4 rows below. | CO-06, G-04 |
| CO-A4 | after an unanswered CO-A1, the look-up shows the order cancelled | Go on to CO-A2. | CO-06, CO-05 |
| CO-A4 | after an unanswered first CO-A1, the look-up shows the order placed or processing | Send CO-A1 once more under the same confirmation. | CO-06, G-04 |
| CO-A4 | after an unanswered CO-A1, the look-up shows the order shipped or delivered | Tell the customer the order shipped or was delivered and was not cancelled; issue no refund and no follow-up. | CO-06, CO-10 |
| CO-A4 | after an unanswered CO-A1, the store's order system does not answer the look-up, however often the agent repeats it | Tell the customer the cancellation's outcome is unknown; issue no refund; CO-A3 with reason cancellation unknown. | CO-06, CO-09 |
| CO-A4 | after an unanswered second CO-A1, the look-up shows the order placed or processing | Send no further CO-A1; tell the customer the order could not be cancelled and is unchanged; issue no refund and no follow-up. | CO-06, G-03, G-04 |
| CO-A2 | the payment provider is temporarily unavailable, on the first CO-A2 | Send CO-A2 once more. | CO-07, G-04 |
| CO-A2 | the payment provider is temporarily unavailable, on the second CO-A2 | Send no further CO-A2; tell the customer the refund was not issued; CO-A3 with reason refund not issued. | CO-07, CO-09, G-04 |
| CO-A2 | the store returns the refund with status failed (the payment method can no longer receive money, or the provider declined; the result does not say which) | Send no further CO-A2; tell the customer the refund was not issued; CO-A3 with reason refund not issued. | CO-07, CO-09 |
| CO-A2 | the store does not answer the first CO-A2 (result unknown) | Send CO-A2 once more. | CO-08, G-04 |
| CO-A2 | the store does not answer the second CO-A2 (result unknown) | Look up the refund before reporting; continue by the CO-A4 rows below. | CO-08 |
| CO-A4 | after an unanswered second CO-A2, the look-up shows the refund pending or issued | Report the refund id and that status. | CO-08, CO-11 |
| CO-A4 | after an unanswered second CO-A2, the look-up shows the refund failed or no refund | Tell the customer the refund is not confirmed yet; CO-A3 with reason refund not issued. | CO-08, CO-09 |
| CO-A4 | after an unanswered second CO-A2, the store's order system does not answer the look-up, however often the agent repeats it | Tell the customer the refund's status is unknown; CO-A3 with reason refund status unknown. | CO-08, CO-09 |
| CO-A3 | store staff's task system does not answer the first CO-A3 (result unknown) | Send CO-A3 once more, with the same order and reason. | CO-09, G-04 |
| CO-A3 | store staff's task system does not answer the second CO-A3 (result unknown) | Send no further CO-A3; tell the customer to contact Harbor Goods support about the order, and do not say staff will follow up. | CO-09, G-03, G-04 |
| CO-A2 | the store reports the order is not cancelled | Send no further CO-A2; tell the customer the refund was not issued; CO-A3 with reason refund not issued. | CO-05, CO-09 |

#### Scenarios

##### CO-S01 — One open order cancelled and refunded, including after an unanswered cancellation

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** regression

**Initial state**
- Today is 2026-11-05.
- Order HG-10482 exists for the customer: order date 2026-11-02, status <status>, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- Order HG-10391 exists for the customer: order date 2026-10-12, status delivered, total paid $42.00, payment method Visa ending 4242, no refund.
- No follow-up task exists.
- The store's order system answers the first CO-A1 with: <first_cancel_answer>.
- The store will create refund <refund_id> with status <refund_status> for the first CO-A2 that creates a refund.

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
- Exactly one refund exists for HG-10482: <refund_id>, amount $86.40, payment method Visa ending 4242, status <refund_status>.
- Order HG-10391 is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- CO-A1 or CO-A2 for HG-10391.
- A second CO-A1.
- A second CO-A2.
- CO-A3 at any point.
- CO-A2 with no CO-A4 between the CO-A1 and it, when the CO-A1 got no answer.

**Data variants**

| variant | Turn 1 | status | first_cancel_answer | refund_id | refund_status | outcome told |
|---|---|---|---|---|---|---|
| 1 | Please cancel order HG-10482. | placed | the order cancelled | RF-5531 | pending | HG-10482 is cancelled and refund RF-5531 of $86.40 to Visa ending 4242 is pending. |
| 2 | I'd like my money back for HG-10482, I don't want it anymore. | processing | the order cancelled | RF-5602 | issued | HG-10482 is cancelled and refund RF-5602 of $86.40 to Visa ending 4242 is issued. |
| 3 | Please cancel order HG-10482. | processing | no answer, though that CO-A1 cancels the order | RF-5570 | pending | HG-10482 is cancelled and refund RF-5570 of $86.40 to Visa ending 4242 is pending. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → HG-10482 placed, total paid $86.40, Visa ending 4242; HG-10391 delivered.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, pending.
7. Agent reports the order cancelled and refund RF-5531 pending to Visa ending 4242.

**Illustrates** CO-01, CO-04, CO-05, CO-06, CO-11, G-01, G-02, G-03, G-04

**Unambiguity note** The two actions, their order number and their order after the confirmation turn are read from the action log, and in row 3 so is the look-up between the unanswered cancellation and the refund, and the order and refund records are compared with Initial state; the checks on the agent's words are message check "Refund id reported", a match on the row's refund id, and rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S02 — Two open orders, the customer says which

- **Interaction type:** clarify, confirm
- **Category tags:** multi-action, multi-turn, canonicalization
- **Suite:** capability

**Initial state**
- Today is 2026-11-05.
- Orders HG-10482 and HG-10517 exist for the customer. HG-10482: order date 2026-11-02, status processing, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund. HG-10517: order date 2026-11-04, status placed, line items 4 × Stoneware mug at $12.50 and 1 × Oak serving board at $38.00, shipping $6.00, tax $11.70, total paid $105.70, payment method Mastercard ending 8810, no refund.
- No follow-up task exists.
- The store will create refund RF-5540 with status pending for the first CO-A2 that creates a refund.

**User**
- Turn 1: "Cancel my order please."

**User knows**
- Q: Which order do you want to cancel? A: <which order>
- Q: Shall I cancel order <order_number> and refund <amount> to <payment_method>? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for <order_number>, after the user's confirmation turn.
- CO-A2 occurs exactly once, for <order_number>, after the CO-A1 for <order_number>.

Final state assertions:
- Order <order_number> has status cancelled.
- Exactly one refund exists for <order_number>: RF-5540, amount <amount>, payment method <payment_method>, status pending.
- Order <other_order> has status <other_status> and no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- CO-A1 for <other_order>.
- CO-A2 for <other_order>.
- A second CO-A1.
- CO-A3 at any point.

**Data variants**

| variant | which order | order_number | amount | payment_method | other_order | other_status | outcome told |
|---|---|---|---|---|---|---|---|
| 1 | The mugs and the serving board. | HG-10517 | $105.70 | Mastercard ending 8810 | HG-10482 | processing | HG-10517 is cancelled and refund RF-5540 of $105.70 to Mastercard ending 8810 is pending |
| 2 | The blanket one. | HG-10482 | $86.40 | Visa ending 4242 | HG-10517 | placed | HG-10482 is cancelled and refund RF-5540 of $86.40 to Visa ending 4242 is pending |
| 3 | The one I placed yesterday. | HG-10517 | $105.70 | Mastercard ending 8810 | HG-10482 | processing | HG-10517 is cancelled and refund RF-5540 of $105.70 to Mastercard ending 8810 is pending |

**Reference trajectory**
1. User: "Cancel my order please."
2. Agent → CO-A4 → HG-10482 processing and HG-10517 placed.
3. Agent asks which order the customer wants to cancel, naming both.
4. User: "The mugs and the serving board."
5. Agent states the proposal (cancel HG-10517, refund $105.70 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A1 (HG-10517) → cancelled.
8. Agent → CO-A2 (HG-10517) → refund RF-5540, $105.70, Mastercard ending 8810, pending.
9. Agent reports HG-10517 cancelled and refund RF-5540 pending.

**Illustrates** CO-03, CO-04, G-01, G-02

**Unambiguity note** Two orders are open and Turn 1 names neither; the rows differ in which order the customer wants, so an agent that proposes one without asking fails at least one row (a scenario passes only when every row passes), and any action for the other order fails on the action log; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S03 — Order that cannot be cancelled, or no such order

- **Interaction type:** infeasible
- **Category tags:** single-action, state-dependency
- **Suite:** regression

**Initial state**
- Order HG-10391 exists for the customer: order date 2026-10-28, status <status>, line items 1 × Wool rug at $120.00, shipping $0.00, tax $9.60, total paid $129.60, payment method Visa ending 4242.
- HG-10391 has <refund>.
- The customer has no other order.
- No follow-up task exists.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10391 has status <status>.
- HG-10391 has <refund>, and no other refund.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | status | refund | outcome told |
|---|---|---|---|---|
| 1 | Please cancel order HG-10391. | shipped | no refund | HG-10391 has shipped and can no longer be cancelled; returns are a separate process |
| 2 | Cancel HG-10391 and refund me. | delivered | no refund | HG-10391 has been delivered and can no longer be cancelled; returns are a separate process |
| 3 | Can you cancel HG-10391? | cancelled | refund RF-5410, $129.60 to Visa ending 4242, status issued | HG-10391 is already cancelled |
| 4 | Please cancel order HG-10399. | delivered | no refund | No order HG-10399 was found among the customer's orders |

**Reference trajectory**
1. User: "Please cancel order HG-10391."
2. Agent → CO-A4 → HG-10391 shipped.
3. Agent tells the customer HG-10391 has shipped, can no longer be cancelled, and that returns are a separate process.

**Illustrates** CO-01, CO-03, G-03

**Unambiguity note** No row allows any write, so any cancellation, refund or follow-up fails on the action log, and the records are compared with Initial state; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S04 — Customer asks to cancel some items

- **Interaction type:** infeasible
- **Category tags:** single-action, multi-turn
- **Suite:** capability

**Initial state**
- Order HG-10517 exists for the customer: order date 2026-11-04, status placed, line items 4 × Stoneware mug at $12.50 and 1 × Oak serving board at $38.00, shipping $6.00, tax $11.70, total paid $105.70, payment method Mastercard ending 8810, no refund.
- The customer has no other order.
- No follow-up task exists.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Do you want to cancel the whole order instead? A: No, then keep the order as it is.

**Expected**

Required events:
- none.

Final state assertions:
- Order HG-10517 has status placed and its line items are unchanged.
- No refund exists for HG-10517.
- No follow-up task exists.

**Forbidden**
- CO-A1 at any point.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | outcome told |
|---|---|---|
| 1 | Can you cancel just the serving board from HG-10517? I still want the mugs. | Only the whole order can be cancelled |
| 2 | Take two of the mugs off order HG-10517 and refund those. | Only the whole order can be cancelled |

**Reference trajectory**
1. User: "Can you cancel just the serving board from HG-10517? I still want the mugs."
2. Agent → CO-A4 → HG-10517 placed, two kinds of line item.
3. Agent says only the whole order can be cancelled and asks whether the customer wants to cancel the whole order instead.
4. User: "No, then keep the order as it is."
5. Agent confirms that nothing was changed.

**Illustrates** CO-02, G-02

**Unambiguity note** The customer declines the whole-order cancellation, so any write fails on the action log; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S05 — Customer switches orders in the confirming turn

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- Order HG-10482 exists for the customer: order date 2026-11-02, status processing, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- Order HG-10517 exists for the customer: order date 2026-11-04, status placed, line items 4 × Stoneware mug at $12.50 and 1 × Oak serving board at $38.00, shipping $6.00, tax $11.70, total paid $105.70, payment method Mastercard ending 8810, no refund.
- No follow-up task exists.
- The store will create refund RF-5551 with status pending for the first CO-A2 that creates a refund.

**User**
- Turn 1: "Please cancel order HG-10482."
- Turn 2, in reply to the agent's first question that states order HG-10482, a refund of $86.40 and Visa ending 4242 and asks to go ahead (no User-knows pair matches it): "<Turn 2>"

**User knows**
- Q: Shall I cancel order HG-10517 and refund $105.70 to Mastercard ending 8810? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10517, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10517, after the CO-A1 for HG-10517.

Final state assertions:
- Order HG-10517 has status cancelled.
- Exactly one refund exists for HG-10517: RF-5551, amount $105.70, payment method Mastercard ending 8810, status pending.
- Order HG-10482 has status processing and no refund.
- No follow-up task exists.

**Forbidden**
- CO-A1 for HG-10482.
- CO-A2 for HG-10482.
- CO-A1 for HG-10517 before the user's confirmation turn.
- CO-A3 at any point.

**Data variants**

| variant | Turn 2 | outcome told |
|---|---|---|
| 1 | Yes. Oh wait, no, I meant the other one, HG-10517. | HG-10517 is cancelled and refund RF-5551 of $105.70 to Mastercard ending 8810 is pending |
| 2 | Hold on, wrong order. Cancel HG-10517 instead, the mugs. | HG-10517 is cancelled and refund RF-5551 of $105.70 to Mastercard ending 8810 is pending |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → HG-10482 processing and HG-10517 placed.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes. Oh wait, no, I meant the other one, HG-10517."
5. Agent states the proposal (cancel HG-10517, refund $105.70 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A1 (HG-10517) → cancelled.
8. Agent → CO-A2 (HG-10517) → refund RF-5551, $105.70, Mastercard ending 8810, pending.
9. Agent reports HG-10517 cancelled and refund RF-5551 pending.

**Illustrates** G-02, CO-03, G-01

**Unambiguity note** Turn 2 switches the order in the message that answers the HG-10482 proposal, so it confirms nothing, whether or not it also says yes; any action for HG-10482, or a cancellation of HG-10517 before the confirmation turn, fails on the action log; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S06 — Store rejects the cancellation, or a look-up after an unanswered one shows it shipped

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Order HG-10482 exists for the customer: order date 2026-11-02, status processing, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- The customer has no other order.
- No follow-up task exists.
- When the agent sends its first CO-A1, the order's status becomes <status_at_cancel>, and the store's order system answers that CO-A1 with: <cancel_answer>.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.

Final state assertions:
- Order HG-10482 has status <status_at_cancel>.
- No refund exists for HG-10482.
- No follow-up task exists.

**Forbidden**
- A second CO-A1.
- CO-A2 at any point.
- CO-A3 at any point.
- Ending the trial with no CO-A4 after the CO-A1, when the CO-A1 got no answer.

**Data variants**

| variant | status_at_cancel | cancel_answer | outcome told |
|---|---|---|---|
| 1 | shipped | the order is not cancellable, status shipped | HG-10482 shipped before it could be cancelled, so it was not cancelled and no refund was issued; returns are a separate process. |
| 2 | delivered | the order is not cancellable, status delivered | HG-10482 has been delivered, so it was not cancelled and no refund was issued; returns are a separate process. |
| 4 | shipped | no answer, and that CO-A1 cancels nothing | HG-10482 shipped before it could be cancelled, so it was not cancelled and no refund was issued; returns are a separate process. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → HG-10482 processing.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → not cancellable, status shipped.
6. Agent tells the customer the order shipped before it could be cancelled, was not cancelled, no refund was issued, and returns are a separate process.

**Illustrates** CO-10, CO-05, CO-06, G-03, G-04

**Unambiguity note** The rejection, or in row 4 the shipment behind an unanswered cancellation, lands on the first cancellation, so a refund, a follow-up or a second cancellation fails on the action log, and in row 4 so does a report with no look-up after the cancellation; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S07 — Unanswered cancellation, order still open, cancellation sent once more

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Order HG-10482 exists for the customer: order date 2026-11-02, status <status>, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- The customer has no other order.
- No follow-up task exists.
- The store's order system does not answer the first CO-A1, and that CO-A1 changes nothing.
- The store's order system answers the second CO-A1 with: <second_cancel_answer>, and that CO-A1 cancels the order.
- The store will create refund RF-5560 with status pending for the first CO-A2 that creates a refund.

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
- Exactly one refund exists for HG-10482: RF-5560, amount $86.40, payment method Visa ending 4242, status pending.
- No follow-up task exists.

**Forbidden**
- A third CO-A1.
- The second CO-A1 with no CO-A4 between the first CO-A1 and it.
- CO-A2 with no CO-A4 between the second CO-A1 and it, when the second CO-A1 got no answer.
- A second CO-A2.
- CO-A3 at any point.

**Data variants**

| variant | status | second_cancel_answer | outcome told |
|---|---|---|---|
| 1 | placed | the order cancelled | HG-10482 is cancelled and refund RF-5560 of $86.40 to Visa ending 4242 is pending. |
| 2 | processing | the order cancelled | HG-10482 is cancelled and refund RF-5560 of $86.40 to Visa ending 4242 is pending. |
| 3 | processing | no answer, and a look-up after it shows the order cancelled | HG-10482 is cancelled and refund RF-5560 of $86.40 to Visa ending 4242 is pending. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → HG-10482 placed.
3. Agent states the proposal and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → no answer.
6. Agent → CO-A4 → HG-10482 placed.
7. Agent → CO-A1 (HG-10482) → cancelled.
8. Agent → CO-A2 (HG-10482) → refund RF-5560, $86.40, Visa ending 4242, pending.
9. Agent reports HG-10482 cancelled and refund RF-5560 pending.

**Illustrates** CO-06, G-04, G-02

**Unambiguity note** The look-up between the two cancellations and the counts of each action are read from the action log; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S10 — Unanswered cancellation and unanswered look-up

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Order HG-10482 exists for the customer: order date 2026-11-02, status processing, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- The customer has no other order.
- No follow-up task exists.
- The store's order system does not answer the first CO-A1, and that CO-A1 leaves the order with status <final_status>.
- The store's order system does not answer any CO-A4 sent after the first CO-A1, however often it is sent.
- Store staff's task system will create follow-up task FT-301 for the first CO-A3.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482 with reason cancellation unknown, after the CO-A1.

Final state assertions:
- Order HG-10482 has status <final_status>.
- No refund exists for HG-10482.
- Exactly one follow-up task exists: FT-301, for HG-10482, reason cancellation unknown.

**Forbidden**
- A second CO-A1.
- CO-A2 at any point.
- CO-A3 with any reason other than cancellation unknown.
- CO-A3 with no CO-A4 between the CO-A1 and it.

**Data variants**

| variant | final_status | outcome told |
|---|---|---|
| 1 | cancelled | Whether HG-10482 was cancelled is unknown; no refund was issued; store staff will follow up. |
| 2 | processing | Whether HG-10482 was cancelled is unknown; no refund was issued; store staff will follow up. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → HG-10482 processing.
3. Agent states the proposal and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → no answer.
6. Agent → CO-A4 → no answer.
7. Agent → CO-A3 (HG-10482, cancellation unknown) → task FT-301.
8. Agent tells the customer the cancellation's outcome is unknown, no refund was issued, and store staff will follow up.

**Illustrates** CO-06, CO-09, CO-05, G-03

**Unambiguity note** Row 1 cancelled the order and row 2 did not, but the agent cannot tell them apart, so both require the same follow-up and no refund, read from the action log; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S11 — Refund sent once more, then confirmed

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Order HG-10482 exists for the customer: order date 2026-11-02, status processing, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- The customer has no other order.
- No follow-up task exists.
- The store's order system answers the first CO-A1 with cancelled.
- The payment provider answers the first CO-A2 with: <first_refund_answer>.
- The payment provider answers the second CO-A2 with: <second_refund_answer>.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly twice, for HG-10482, after the CO-A1.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5580, amount $86.40, payment method Visa ending 4242, status <refund_status>.
- No follow-up task exists.

**Forbidden**
- A third CO-A2.
- CO-A3 at any point.
- Ending the trial with no CO-A4 after the second CO-A2, when the second CO-A2 got no answer.

**Data variants**

| variant | first_refund_answer | second_refund_answer | refund_status | outcome told |
|---|---|---|---|---|
| 1 | temporarily unavailable, no refund created | refund RF-5580 created, status pending | pending | HG-10482 is cancelled and refund RF-5580 of $86.40 to Visa ending 4242 is pending. |
| 2 | no answer, and no refund created | refund RF-5580 created, status issued | issued | HG-10482 is cancelled and refund RF-5580 of $86.40 to Visa ending 4242 is issued. |
| 3 | no answer, and no refund created | no answer, though refund RF-5580 is created with status pending, and a look-up after it shows it | pending | HG-10482 is cancelled and refund RF-5580 of $86.40 to Visa ending 4242 is pending. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → HG-10482 processing.
3. Agent states the proposal and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → payment provider temporarily unavailable.
7. Agent → CO-A2 (HG-10482) → refund RF-5580, $86.40, Visa ending 4242, pending.
8. Agent reports HG-10482 cancelled and refund RF-5580 pending.

**Illustrates** CO-07, CO-08, CO-11, G-04

**Unambiguity note** The second refund call is allowed in every row and a third is not; in row 3 the report must follow a look-up, all read from the action log; the checks on the agent's words are message check "Refund id reported" and rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S12 — Refund not confirmed after two attempts, staff follow up

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Order HG-10482 exists for the customer: order date 2026-11-02, status processing, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- The customer has no other order.
- No follow-up task exists.
- The store's order system answers the first CO-A1 with cancelled.
- The payment provider answers both CO-A2 calls with: <refund_answers>.
- The first CO-A2 creates no refund.
- After the second CO-A2, HG-10482 has <refunds>.
- The store's order system answers a CO-A4 sent after the second CO-A2 with: <lookup_answer>.
- Store staff's task system will create follow-up task FT-302 for the first CO-A3.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly twice, for HG-10482, after the CO-A1.
- CO-A3 occurs exactly once, for HG-10482 with reason <reason>, after the second CO-A2.

Final state assertions:
- Order HG-10482 has status cancelled.
- HG-10482 has <refunds>, and no other refund.
- Exactly one follow-up task exists: FT-302, for HG-10482, reason <reason>.

**Forbidden**
- A third CO-A2.
- CO-A3 with any reason other than <reason>.
- A second CO-A3.
- CO-A3 with no CO-A4 between the second CO-A2 and it, when the second CO-A2 got no answer.

**Data variants**

| variant | refund_answers | refunds | lookup_answer | reason | outcome told |
|---|---|---|---|---|---|
| 1 | temporarily unavailable, no refund created | zero refunds | no refund for HG-10482 | refund not issued | HG-10482 is cancelled; the refund was not issued; store staff will follow up. |
| 2 | no answer | zero refunds | no refund for HG-10482 | refund not issued | HG-10482 is cancelled; the refund is not confirmed yet; store staff will follow up. |
| 3 | no answer | refund RF-5590, $86.40 to Visa ending 4242, status failed | refund RF-5590 failed | refund not issued | HG-10482 is cancelled; the refund is not confirmed yet; store staff will follow up. |
| 4 | no answer | refund RF-5590, $86.40 to Visa ending 4242, status pending | no answer, however often it is sent | refund status unknown | HG-10482 is cancelled; the refund's status is unknown; store staff will follow up. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → HG-10482 processing.
3. Agent states the proposal and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → payment provider temporarily unavailable.
7. Agent → CO-A2 (HG-10482) → payment provider temporarily unavailable.
8. Agent → CO-A3 (HG-10482, refund not issued) → task FT-302.
9. Agent tells the customer the order is cancelled, the refund was not issued, and store staff will follow up.

**Illustrates** CO-07, CO-08, CO-09, G-03, G-04

**Unambiguity note** In row 4 a refund exists but the agent could not see it, so the follow-up reason is refund status unknown, not refund not issued; reasons and counts are read from the action log; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S13 — Refund failed, staff follow up

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Order HG-10482 exists for the customer: order date 2026-11-02, status processing, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- The customer has no other order.
- No follow-up task exists.
- The store's order system answers the first CO-A1 with cancelled.
- The store answers the first CO-A2 with: <refund_answer>.
- Store staff's task system will create follow-up task FT-303 for the first CO-A3.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10482, after the CO-A1.
- CO-A3 occurs exactly once, for HG-10482 with reason refund not issued, after the CO-A2.

Final state assertions:
- Order HG-10482 has status cancelled.
- HG-10482 has <refunds>, and no other refund.
- Exactly one follow-up task exists: FT-303, for HG-10482, reason refund not issued.

**Forbidden**
- A second CO-A2.
- A second CO-A3.
- CO-A3 with any reason other than refund not issued.

**Data variants**

| variant | refund_answer | refunds | outcome told |
|---|---|---|---|
| 1 | refund RF-5595 created with status failed, because the card has been closed and can no longer receive money | refund RF-5595, $86.40 to Visa ending 4242, status failed | HG-10482 is cancelled; the refund was not issued; store staff will follow up. |
| 2 | refund RF-5595 created with status failed, because the payment provider declined the refund | refund RF-5595, $86.40 to Visa ending 4242, status failed | HG-10482 is cancelled; the refund was not issued; store staff will follow up. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → HG-10482 processing.
3. Agent states the proposal and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5595, $86.40, Visa ending 4242, status failed.
7. Agent → CO-A3 (HG-10482, refund not issued) → task FT-303.
8. Agent tells the customer the order is cancelled, the refund was not issued, and store staff will follow up.

**Illustrates** CO-07, CO-09, G-03, G-04

**Unambiguity note** A terminal refund failure allows no second refund call, read from the action log; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S14 — Follow-up request unanswered

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Order HG-10482 exists for the customer: order date 2026-11-02, status processing, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- The customer has no other order.
- No follow-up task exists.
- The store's order system answers the first CO-A1 with cancelled.
- The store answers the first CO-A2 with refund RF-5596, $86.40 to Visa ending 4242, status failed, because the card has been closed.
- Store staff's task system does not answer the first CO-A3, and that CO-A3 creates no task.
- Store staff's task system answers the second CO-A3 with: <second_followup_answer>.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10482, after the CO-A1.
- CO-A3 occurs exactly twice, for HG-10482 with reason refund not issued, after the CO-A2.

Final state assertions:
- Order HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5596, amount $86.40, payment method Visa ending 4242, status failed.
- The follow-up tasks are exactly: <tasks>.

**Forbidden**
- A second CO-A2.
- A third CO-A3.
- CO-A3 with any reason other than refund not issued.

**Data variants**

| variant | second_followup_answer | tasks | outcome told |
|---|---|---|---|
| 1 | task FT-304 created | FT-304, for HG-10482, reason refund not issued | HG-10482 is cancelled; the refund was not issued; store staff will follow up. |
| 2 | no answer, and no task created | zero tasks | HG-10482 is cancelled; the refund was not issued; the customer should contact Harbor Goods support about the order. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → HG-10482 processing.
3. Agent states the proposal and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → cancelled.
6. Agent → CO-A2 (HG-10482) → refund RF-5596, $86.40, Visa ending 4242, status failed.
7. Agent → CO-A3 (HG-10482, refund not issued) → no answer.
8. Agent → CO-A3 (HG-10482, refund not issued) → task FT-304.
9. Agent tells the customer the order is cancelled, the refund was not issued, and store staff will follow up.

**Illustrates** CO-09, G-03, G-04

**Unambiguity note** Exactly two follow-up requests are allowed and a third is not, read from the action log; in row 2 the agent must not say staff will follow up, which rubric dimension "Outcome reported truthfully" checks against the row's outcome told column.

##### CO-S15 — Two unanswered cancellations, order still open

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Order HG-10482 exists for the customer: order date 2026-11-02, status <status>, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- The customer has no other order.
- No follow-up task exists.
- The store's order system does not answer the first CO-A1 or the second CO-A1, and neither changes the order.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly twice, for HG-10482, both after the user's confirmation turn.

Final state assertions:
- Order HG-10482 has status <status>.
- No refund exists for HG-10482.
- No follow-up task exists.

**Forbidden**
- A third CO-A1.
- The second CO-A1 with no CO-A4 between the first CO-A1 and it.
- Ending the trial with no CO-A4 after the second CO-A1.
- CO-A2 at any point.
- CO-A3 at any point.

**Data variants**

| variant | status | outcome told |
|---|---|---|
| 1 | processing | HG-10482 could not be cancelled and is unchanged; no refund was issued. |
| 2 | placed | HG-10482 could not be cancelled and is unchanged; no refund was issued. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → HG-10482 processing.
3. Agent states the proposal and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10482) → no answer.
6. Agent → CO-A4 → HG-10482 processing.
7. Agent → CO-A1 (HG-10482) → no answer.
8. Agent → CO-A4 → HG-10482 processing.
9. Agent tells the customer the order could not be cancelled, is unchanged, and no refund was issued.

**Illustrates** CO-06, G-03, G-04

**Unambiguity note** The two cancellations, the look-ups after each, and the absence of a third cancellation, a refund or a follow-up are read from the action log; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S16 — Orders cannot be looked up

- **Interaction type:** infeasible
- **Category tags:** single-action, insufficient-information
- **Suite:** capability

**Initial state**
- Order HG-10482 exists for the customer: order date 2026-11-02, status processing, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- The customer has no other order.
- No follow-up task exists.
- The store's order system does not answer any CO-A4, however often it is sent.

**User**
- Turn 1: "<Turn 1>"

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

| variant | Turn 1 | outcome told |
|---|---|---|
| 1 | Please cancel order HG-10482. | The customer's orders cannot be looked up right now |
| 2 | Cancel HG-10482 and put the $86.40 back on my Visa ending 4242. | The customer's orders cannot be looked up right now |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → no answer.
3. Agent → CO-A4 → no answer.
4. Agent tells the customer their orders cannot be looked up right now and nothing was cancelled or refunded.

**Illustrates** CO-04, G-02, G-03

**Unambiguity note** Without a look-up the agent has no total paid or payment method to propose, and in row 2 the customer's own figures do not replace them, so any write fails on the action log; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S17 — Customer declines the proposal

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn
- **Suite:** regression

**Initial state**
- Order HG-10482 exists for the customer: order date 2026-11-02, status processing, line items 1 × Linen throw blanket at $64.00, shipping $8.00, tax $14.40, total paid $86.40, payment method Visa ending 4242, no refund.
- The customer has no other order.
- No follow-up task exists.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: <answer>

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

| variant | Turn 1 | answer | outcome told |
|---|---|---|---|
| 1 | Please cancel order HG-10482. | No, leave it as it is. | HG-10482 was not cancelled. |
| 2 | I'm thinking of cancelling HG-10482. What would I get back? | Hmm, no, I'll keep it after all. | HG-10482 was not cancelled. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A4 → HG-10482 processing.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "No, leave it as it is."
5. Agent confirms that nothing was changed.

**Illustrates** G-02, CO-04

**Unambiguity note** The customer's answer to the full proposal is a refusal, so any write fails on the action log; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

##### CO-S18 — Customer asks to cancel some items, then takes the whole order

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- Order HG-10517 exists for the customer: order date 2026-11-04, status placed, line items 4 × Stoneware mug at $12.50 and 1 × Oak serving board at $38.00, shipping $6.00, tax $11.70, total paid $105.70, payment method Mastercard ending 8810, no refund.
- The customer has no other order.
- No follow-up task exists.
- The store will create refund RF-5545 with status pending for the first CO-A2 that creates a refund.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order HG-10517 and refund $105.70 to Mastercard ending 8810? A: Yes.

**Expected**

Required events:
- CO-A1 occurs exactly once, for HG-10517, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10517, after the CO-A1 for HG-10517.

Final state assertions:
- Order HG-10517 has status cancelled.
- Exactly one refund exists for HG-10517: RF-5545, amount $105.70, payment method Mastercard ending 8810, status pending.
- No follow-up task exists.

**Forbidden**
- CO-A1 before the user's confirmation turn.
- A second CO-A1.
- A second CO-A2.
- CO-A3 at any point.

**Data variants**

| variant | Turn 1 | outcome told |
|---|---|---|
| 1 | Can you cancel just the serving board from HG-10517? If you can't, cancel the whole order. | Only the whole order can be cancelled; HG-10517 is cancelled and refund RF-5545 of $105.70 to Mastercard ending 8810 is pending. |
| 2 | Take two of the mugs off order HG-10517 and refund those, or else just cancel all of it. | Only the whole order can be cancelled; HG-10517 is cancelled and refund RF-5545 of $105.70 to Mastercard ending 8810 is pending. |

**Reference trajectory**
1. User: "Can you cancel just the serving board from HG-10517? If you can't, cancel the whole order."
2. Agent → CO-A4 → HG-10517 placed, two kinds of line item.
3. Agent says only the whole order can be cancelled, states the proposal (cancel HG-10517, refund $105.70 to Mastercard ending 8810) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A1 (HG-10517) → cancelled.
6. Agent → CO-A2 (HG-10517) → refund RF-5545, $105.70, Mastercard ending 8810, pending.
7. Agent reports that only the whole order can be cancelled, HG-10517 cancelled and refund RF-5545 pending.

**Illustrates** CO-02, G-02, CO-11

**Unambiguity note** Turn 1 accepts the whole order only as a fallback and states no proposal values, so it is not a confirmation, and a cancellation before the full proposal is confirmed fails on the action log; the check on the agent's words is rubric dimension "Outcome reported truthfully", against the row's outcome told column.

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
| Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id that CO-A2 returned or CO-A4 showed, as the scenario's Initial state or data-variant row gives it. | CO-S01, CO-S11 |
| Outcome reported truthfully | rubric | The agent's messages tell the customer every fact in the data-variant row's outcome told column, and claim no cancellation, refund, follow-up, fee waiver, store credit or arrival date for the money that the store did not report. | CO-S01, CO-S02, CO-S03, CO-S04, CO-S05, CO-S06, CO-S07, CO-S10, CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S17, CO-S18 |

Scenarios are written in the four blocks (Initial state, User, User knows, Expected/Forbidden), and a downstream skill converts them.

## Appendix A. Interface binding (provisional)

Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.

**Value comparison.** Order numbers, refund ids and task ids compare exactly, ignoring case; amounts compare as US dollars to the cent; a payment method compares by card brand and last four digits; a follow-up reason compares by its value: refund not issued is `refund_not_issued`, refund status unknown is `refund_status_unknown`, cancellation unknown is `cancellation_unknown`.

**Which order an action is for.** CO-A1, CO-A2 and CO-A3 are for the order whose number is their `order_number` argument. An order's order date is its `placed_date`.

| Action | Mark | Commit call | Information items and where each is carried | Outcomes, as tool results | Effect on state |
|---|---|---|---|---|---|
| CO-A1 cancel the order | state-changing | `cancel_order(order_number)` → `{order_number, status}` | order number: `order_number` | cancelled: `status: "cancelled"`, also for an order that is already cancelled (SG-04); not cancellable: `OrderNotCancellable{status}` with status shipped or delivered; no such order: `OrderNotFound`; no answer: timeout | Sets the order's status to cancelled when it returns `status: "cancelled"`; `OrderNotCancellable` and `OrderNotFound` change nothing; a timeout may or may not have cancelled the order. |
| CO-A2 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, order_number, amount, payment_method, status}` | order number: `order_number`; amount (the order's total paid) and payment method (the order's): set by the store from the order | created: refund with status `pending` or `issued`; refund failed (payment method cannot receive money, or provider declined): refund with status `failed`; provider temporarily unavailable: `PaymentProviderUnavailable`, no refund created; order not cancelled: `OrderNotCancelled`, no refund created; no answer: timeout | Creates the order's refund on the first call that creates one; a later call for the same order returns that refund and creates none (SG-01). |
| CO-A3 ask staff to follow up | state-changing | `request_staff_followup(order_number, reason)` → `{task_id, order_number, reason}` | order number: `order_number`; reason: `reason`, one of `refund_not_issued`, `refund_status_unknown`, `cancellation_unknown` | created: returns `task_id`; no answer: timeout | Creates one follow-up task for store staff when it returns `task_id`; a repeat for the same order and reason returns that task and creates none (SG-03); a timeout may or may not have created one. |
| CO-A4 look up the customer's orders | read-only | `list_orders()` → `[{order_number, placed_date, status, line_items, shipping, tax, total_paid, payment_method, refund}]` | none | orders: the signed-in customer's orders, cancelled ones included, each with its refund or `null`; no answer: timeout, and the agent may repeat the call without limit | none |

Unmapped read-only calls: none.

**Binding contract.**
- Every state-changing tool call is the commit call of at least one action. Only read-only calls may be unmapped.
- One call may commit several actions. One action never has two commit calls.
- A read-only action has a row only when a Forbidden line or a failure row names it; its call is then its read. Every other read stays unmapped.

## Appendix B. Supporting-actor guarantees

Promises the agent relies on but cannot act on, because no agent turn exists when they apply. They are stated here so the builder sees them; no scenario grades them.

| Id | Guarantee | Covers |
|---|---|---|
| SG-01 | The store's refund is idempotent, keyed on the order number: repeated refund calls for one order return the same refund id and never create a second refund. | The second CO-A2 after an unanswered or temporarily unavailable first one; at most one refund per order. |
| SG-02 | Store staff work every follow-up task the agent creates, through the store's manual refund process. | Every failure row that ends in CO-A3. |
| SG-03 | Follow-up requests are idempotent, keyed on order number and reason: a repeat returns the same task and never creates a second one. | The second CO-A3 after an unanswered first one. |
| SG-04 | Cancellation is idempotent: cancelling an order that is already cancelled returns cancelled and changes nothing. | The second CO-A1 after an unanswered first one that did cancel the order. |
