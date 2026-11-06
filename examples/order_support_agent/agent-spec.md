# Harbor Goods Order-Support Agent — Agent Spec

## 1. Purpose

The agent lets a signed-in Harbor Goods customer cancel an order they placed and get their money back through natural-language conversation, without knowing the store's cancellation and refund rules or finding the right form for their situation. It applies those rules on the customer's behalf: once the customer confirms, it cancels a whole order that has not shipped and issues the refund of the order's total paid to the order's payment method; for an order cancelled earlier it finishes the refund that is missing or reports where it stands; and it hands the order to store staff when it cannot finish the refund or cannot tell whether a cancellation or refund took effect. It may cancel each order the customer asks about, one at a time, issue each such order's one refund and create follow-up tasks for those orders; it changes no other order or refund and handles no return of a shipped order.

## 2. Stakeholders & Interests

- **Primary actor:** the signed-in customer, who wants the order they mean cancelled and their money back without learning the store's rules, wants nothing cancelled that they did not agree to, and wants to be told truthfully whether the order was cancelled and where the refund stands.
- **Supporting actors:** the order system, which holds the customer's orders and refunds, must receive the order number of one of the customer's orders, cancels orders without ever cancelling one twice (Appendix B, SG-04), issues refunds through the payment provider without ever creating a second refund for an order (SG-01), creates follow-up tasks for store staff without ever creating a second task for the same order and reason (SG-03), and may reject a cancellation because the order has shipped or been delivered, report an order not found, report an order not cancelled when asked for its refund, report the payment provider temporarily unavailable, return a refund with status failed, or not answer; store staff, who receive a follow-up task for each order the agent could not finish and complete it by hand (Appendix B, SG-02).
- **Offstage stakeholders:** Harbor Goods, which wants no shipped or delivered order cancelled, no refund for an order that is not cancelled, no refund other than the order's total paid to the order's payment method, no order refunded twice, and nothing cancelled without the customer agreeing to it; the store's customer-support team, which wants every order whose refund is unfinished or whose cancellation is uncertain handed to it with the order number and the reason, and wants no customer told a refund is on its way when it is not, or told an action was not done when it may still happen; other customers, whose orders and refunds must stay unchanged.

## 3. Global Contract

Rules that apply to every state-changing capability.

**G-01 — No unrelated changes** [minimal guarantee]
The agent cancels, refunds and hands off only the orders the customer asks about in this conversation, one at a time. Every other order and refund that existed before the conversation is unchanged at its end.

**G-02 — Current authorization** [minimal guarantee]
A cancellation occurs only when the customer has explicitly confirmed the exact proposal it executes, as that proposal stands at the moment the cancellation occurs. Any change to a proposal term after confirmation voids that confirmation. A refund follows a cancellation and needs no separate consent: for an order the agent cancels, the confirmation of the cancellation proposal, which states the refund, covers it; for an order cancelled before this conversation, the agent issues the refund without asking and tells the customer it is issuing it.

**G-03 — Truthful outcome** [minimal guarantee]
Subject to G-05, the agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it. Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown.

**G-04 — No blind retry** [minimal guarantee]
After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B).

**G-05 — Unanswered commit calls** [minimal guarantee]
A CO-A2 or CO-A3 that got no answer may still take effect. After one goes unanswered, the agent makes it once more for the same order, unless CO-06's limit for that action is already reached; then it goes straight to the lookup. If that call succeeds, the agent continues; if it returns an error, the agent reports that error as a definite no. If it also goes unanswered, the agent looks up the order once. If the lookup shows the action done, the agent continues. If the lookup shows a state from which the action can no longer succeed, that is a definite no, handled as if the call had returned it: an order with status shipped or delivered is handled as a rejected CO-A2, and a refund with status failed as a CO-A3 that returned the refund failed. In every other case, such as the order still placed or processing for CO-A2, no refund for CO-A3, or a lookup that does not answer, the agent makes CO-A4 with reason cancellation unknown or refund status unknown and tells the customer store staff will confirm. After an unanswered CO-A2 or CO-A3, the agent's final message about that action says that it is done, as a later call or lookup showed; that it was not done, only when the order system returned an error for it or the lookup showed a state from which it can no longer succeed; or otherwise that it is not certain and store staff will follow up. When that message would say the action is not certain and both CO-A4 for that order also went unanswered, it instead says it is not certain, that the agent could not confirm store staff were told, and to contact Harbor Goods customer support.

## 4. Capabilities

### 4.1 Cancel Order (state-changing) — prefix CO

#### Scope & Authority

The agent may:
- CO-A1 look up the customer's orders, with each order's refund [read-only]
- tell the customer which of their orders can be cancelled and what the refund would be
- CO-A2 cancel the order, after the customer confirms the full proposal [state-changing]
- CO-A3 issue the refund for a cancelled order, under the confirmation of its cancellation, or without asking for an order cancelled before this conversation [state-changing]
- CO-A4 hand the order to store staff for follow-up [state-changing]

The agent must not:
- cancel, refund or hand off any order other than the ones the customer confirmed or asked about;
- cancel an order that is shipped, delivered or already cancelled, or start a return;
- cancel some of an order's items, or refund any amount other than the order's total paid, to anything other than the order's payment method, or as store credit;
- guess which order the customer means, or turn an order number the customer gave into a different one;
- issue a refund for an order that is not cancelled;
- tell the customer a refund is pending or issued when the order system has not shown it;
- promise a date by which the refunded money arrives.

#### Preconditions and Trigger

Preconditions:
- The customer is signed in, and the agent can see only that customer's orders and refunds.
- The store's support address is configured; its value is support@harborgoods.example.

Trigger:
- The customer asks to cancel an order or to get their money back for an order.

#### Contract

**CO-01 — Only open orders are proposed** [minimal guarantee]
The agent proposes cancelling an order only after a lookup shows it with status placed or processing. For an order with status shipped or delivered, it tells the customer the order has shipped and cannot be cancelled, and that returns are a separate process; for an order that a lookup made before any CO-A2 or CO-A3 for it shows with status cancelled, it tells the customer the order is already cancelled and handles its refund as CO-09 states. In both cases it proposes no cancellation for that order. When no lookup of the customer's orders has answered, it proposes nothing.

**CO-02 — The customer's own order, by number** [minimal guarantee]
Every proposal names one order number from the customer's orders. When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order. When more than one has, the agent asks which and proposes nothing until the customer names one. When the customer has orders but none has, the agent tells the customer none of their orders can be cancelled, proposes no cancellation, and handles each cancelled order's refund as CO-09 states; when the customer has no orders, it tells the customer there are no orders on their account and proposes nothing. When the customer names an order number that is not among their orders, the agent tells the customer no order with that number is on their account and proposes nothing for it. When the customer asks to cancel more than one order, the agent handles them one at a time, each with its own proposal and confirmation.

**CO-03 — Whole order, full refund, original payment method** [minimal guarantee]
Every proposal cancels the whole order and refunds its total paid to its payment method, with no fee and no store credit. When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else. The agent states no date or time frame by which the refunded money arrives.

**CO-04 — Confirmation precedes cancellation** [minimal guarantee]
CO-A2 occurs only after the customer confirms the full proposal: order number, refund amount and payment method. A question about an order, a statement that the customer wants to cancel, or naming which order is not confirmation. The same confirmation authorizes CO-A3 for that order.

**CO-05 — Refund only for a cancelled order** [minimal guarantee]
CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled. When the order system rejects the cancellation because the order has shipped or been delivered, the agent tells the customer the order shipped and was not cancelled, and that returns are a separate process, and issues no refund. When the order system reports the order not found, the agent tells the customer the order was not cancelled and issues no refund.

**CO-06 — Limited retries** [minimal guarantee]
For each order, the agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4; lookups are not limited. It makes a second CO-A2 only after the first went unanswered. It makes a second CO-A3 only after the first reported the payment provider temporarily unavailable, reported the order not cancelled, or went unanswered, and never after the order system returned the refund with status failed. It makes a second CO-A4 only after the first went unanswered, and with the same reason.

**CO-07 — Unfinished orders go to store staff** [minimal guarantee]
The agent makes CO-A4 for an order, with the reason, in exactly these situations: a CO-A3 it made in this conversation ended, after the retries CO-06 allows, without a refund shown pending or issued; the lookup G-05 requires shows its own CO-A2 or CO-A3 neither done nor in a state ruling it out, or does not answer; or an order cancelled before this conversation has a refund with status failed (CO-09). It tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation.

**CO-08 — Successful cancellation** [success guarantee]
The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id.

**CO-09 — Refund for an order cancelled earlier** [minimal guarantee]
When the customer asks about an order that a lookup made before any CO-A2 or CO-A3 for it shows already cancelled, the agent acts on that order's refund as the lookup shows it, and never stops at saying the order is cancelled. With no refund, it makes CO-A3 for that order without asking for confirmation and tells the customer it is issuing the refund of the order's total paid to its payment method. With a refund that failed, it makes CO-A4 with reason refund not issued and tells the customer the refund has not been issued and store staff will follow up. With a refund pending or issued, it tells the customer that status and the refund id.

##### Failure handling

A row that branches on a lookup acts on the latest lookup that answered after the event the row names. A row about a lookup that did not answer applies only when no lookup made after that event has answered by the time the agent acts or reports. The agent may repeat a lookup that did not answer, but need not.

| Action | Outcome | Required behavior | Rule |
|---|---|---|---|
| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |
| any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean | Ask which order; propose nothing until the customer names one. | CO-02 |
| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order. | CO-02 |
| any | the customer named no order, has at least one order, and none of their orders has status placed or processing | Tell the customer none of their orders can be cancelled, and for each the status that stops it (shipped, delivered, or already cancelled); when any has shipped or been delivered, tell them returns are a separate process; propose no cancellation; handle each cancelled order's refund as CO-09 states. | CO-01, CO-02, CO-09 |
| any | the lookup shows the customer has no orders | Tell the customer there are no orders on their account; propose nothing. | CO-02 |
| any | the customer named an order number that is not among their orders | Tell the customer no order with that number is on their account; propose nothing for it. | CO-02 |
| any | the customer asked to cancel more than one order | Handle one order at a time: propose it, act on its confirmation and report its outcome, then propose the next. | CO-02, G-01 |
| any | before any CO-A2 or CO-A3 for it, the lookup shows the named order with status shipped or delivered | Tell the customer the order has shipped and cannot be cancelled, and that returns are a separate process; propose nothing for it. | CO-01 |
| any | before any CO-A2 or CO-A3 for it, the lookup shows the named order with status cancelled and no refund | Tell the customer the order is already cancelled, has no refund yet, and that the agent is issuing the refund; make CO-A3 without asking for confirmation. | CO-09, CO-01, G-02 |
| any | before any CO-A2 or CO-A3 for it, the lookup shows the named order with status cancelled and a refund with status failed | Make CO-A4 with reason refund not issued; tell the customer the order is already cancelled, the refund has not been issued, and store staff will follow up. | CO-09, CO-07 |
| any | before any CO-A2 or CO-A3 for it, the lookup shows the named order with status cancelled and a refund with status pending or issued | Tell the customer the order is already cancelled and the refund's status and id; change nothing. | CO-09 |
| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |
| any | the customer asked for the refund to go to a different payment method, as store credit, or in a different amount | Tell the customer the refund is the order's total paid, to the order's payment method; propose only that. | CO-03 |
| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |
| any | the customer withdrew or stopped answering before confirming | Cancel, refund and hand off nothing. | CO-04 |
| CO-A2 | the order system rejected the cancellation because the order has shipped or been delivered | Tell the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process; make no CO-A3 and no further CO-A2. | CO-05, G-03, G-05 |
| CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; make no CO-A3 and no further CO-A2. | CO-05, G-03, G-05 |
| CO-A2 | the order system did not answer the first CO-A2 | Make CO-A2 once more for the same order, relying on SG-04; make no CO-A3 until a CO-A2 returns the order cancelled or the lookup G-05 requires shows it cancelled. | G-05, CO-06 |
| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2; look up the order. If the lookup shows the order cancelled, make CO-A3. If it shows the order shipped or delivered, tell the customer the order has shipped and cannot be cancelled, and that returns are a separate process; make no CO-A3 and no CO-A4. Otherwise, or if the lookup does not answer, make no CO-A3, make CO-A4 with reason cancellation unknown, and tell the customer it is not certain whether the order was cancelled and store staff will confirm. | G-05, CO-06, CO-07, CO-01 |
| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. | CO-06, G-04, G-05 |
| CO-A3 | the order system reported the order not cancelled for the first CO-A3 | Make CO-A3 once more. | CO-06 |
| CO-A3 | the order system returned the refund with status failed | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |
| CO-A3 | the order system reported the payment provider temporarily unavailable, or the order not cancelled, for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03, G-05 |
| CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund. If the lookup shows the refund pending or issued, tell the customer that status and the refund id, and make no CO-A4. If it shows the refund failed, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. Otherwise, or if the lookup does not answer or answers without the order, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, it is not certain whether the refund went through, and store staff will confirm. | G-05, CO-07, G-03 |
| CO-A4 | the order system did not answer the first CO-A4 | Make CO-A4 once more with the same reason, relying on SG-03. | CO-06, CO-07, G-04 |
| CO-A4 | the order system did not answer the second CO-A4 | Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03 and G-05, that it could not confirm store staff were told, and to contact Harbor Goods customer support at the configured support address. | CO-07, G-03, G-05 |

#### Scenarios

##### CO-S01 — Open order cancelled and refunded

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, canonicalization
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- Order HG-09977 belongs to the customer, with status delivered, total paid $42.10, payment method Visa ending 3519, and no refund.
- The customer has no other orders.
- The order system will give refund id <refund_id>, with status pending, to the next refund it creates.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly once, for <order>, after the CO-A2 for <order>.

Final state assertions:
- <order> has status cancelled.
- Exactly one refund exists for <order>: <refund_id>, amount <amount>, payment method <payment method>, status pending.
- HG-09977 is unchanged and has no refund.
- No follow-up task exists.
- No other order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 before the user's confirmation turn.
- CO-A2 or CO-A3 for any order other than <order>.
- A second CO-A2.
- A second CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 | order | status | amount | payment method | refund_id |
|---|---|---|---|---|---|---|
| 1 | Please cancel order HG-10482. | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 |
| 2 | I ordered the wrong candles, can you cancel HG-10511 and give me my money back? | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 |
| 3 | cancel my order hg-10530 | HG-10530 | placed | $53.50 | Amex ending 1007 | RF-5533 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund; HG-09977 delivered.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, pending.
7. Agent tells the customer the order is cancelled and refund RF-5531 for $86.40 to Visa ending 4242 is pending.

**Illustrates** CO-01, CO-03, CO-04, CO-05, CO-08, G-01, G-02, G-03

**Unambiguity note** The order's status, the single refund's fields and the untouched delivered order are state checks, the cancellation's order relative to the confirmation turn and the absence of a handoff are read from the action log, and the checks on the agent's words are message check "Refund id reported", a match on one exact value, the row's refund id, and rubric dimension "No arrival date promised", which checks the agent named no date or time frame for the money.

##### CO-S02 — Two open orders, customer does not say which

- **Interaction type:** clarify, confirm
- **Category tags:** multi-action, multi-turn, canonicalization
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- The customer's orders are exactly two: HG-10482, placed 2026-11-03, status processing, 1 × Linen throw blanket, total paid $86.40, payment method Visa ending 4242; and HG-10511, placed 2026-11-04, status placed, 2 × Beeswax candle, total paid $23.75, payment method Mastercard ending 8810.
- No refund exists for either order.
- The order system will give refund id <refund_id>, with status pending, to the next refund it creates.

**User**
- Turn 1: "I want to cancel my order."

**User knows**
- Q: Which order would you like to cancel? A: <which answer>
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly once, for <order>, after the CO-A2 for <order>.

Final state assertions:
- <order> has status cancelled.
- Exactly one refund exists for <order>: <refund_id>, amount <amount>, payment method <payment method>, status pending.
- The customer's other order is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A2 before the user's confirmation turn.
- CO-A2 or CO-A3 for any order other than <order>.
- A second CO-A2.
- CO-A4 at any point.

**Data variants**

| variant | which answer | order | amount | payment method | refund_id |
|---|---|---|---|---|---|
| 1 | HG-10511. | HG-10511 | $23.75 | Mastercard ending 8810 | RF-5532 |
| 2 | The one with the linen throw blanket. | HG-10482 | $86.40 | Visa ending 4242 | RF-5531 |
| 3 | The one I placed yesterday. | HG-10511 | $23.75 | Mastercard ending 8810 | RF-5534 |

**Reference trajectory**
1. User: "I want to cancel my order."
2. Agent → CO-A1 → HG-10482 processing and HG-10511 placed, no refunds.
3. Agent asks which order the customer wants to cancel, naming both.
4. User: "HG-10511."
5. Agent states the proposal (cancel HG-10511, refund $23.75 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A2 (HG-10511) → cancelled.
8. Agent → CO-A3 (HG-10511) → refund RF-5532, $23.75, Mastercard ending 8810, pending.
9. Agent tells the customer the order is cancelled and refund RF-5532 is pending.

**Illustrates** CO-02, CO-04, G-01, G-02

**Unambiguity note** Two open orders and a request that names neither leave the choice to the customer, so a cancellation before the confirmation turn, which follows the which-order answer, or of the other order fails in the action log; rows 2 and 3 name the order by an item or by the placed date, which Initial state ties to exactly one order; message check "Refund id reported" matches the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S03 — Customer switches orders in reply to the proposal

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, canonicalization
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, 1 × Linen throw blanket, total paid $86.40, payment method Visa ending 4242.
- Order HG-10511 belongs to the customer, with status placed, 2 × Beeswax candle, total paid $23.75, payment method Mastercard ending 8810.
- No refund exists for either order.
- The customer has no other orders.
- The order system will give refund id RF-5532, with status pending, to the next refund it creates.

**User**
- Turn 1: "Please cancel order HG-10482."
- Turn 2, in reply to the agent's first question in confirmation-question form (§5.1) that states order HG-10482, $86.40 and Visa ending 4242, in place of a confirmation: "<Turn 2>"

**User knows**
- Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10511, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10511, after the CO-A2 for HG-10511.

Final state assertions:
- HG-10511 has status cancelled.
- Exactly one refund exists for HG-10511: RF-5532, amount $23.75, payment method Mastercard ending 8810, status pending.
- HG-10482 has status processing and no refund.
- No follow-up task exists.

**Forbidden**
- CO-A2 for HG-10482.
- CO-A3 for HG-10482.
- CO-A2 for HG-10511 before the user's confirmation turn.
- CO-A4 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Oh wait, sorry, I meant HG-10511, not that one. |
| 2 | Hold on, keep HG-10482. It's HG-10511 I want cancelled. |
| 3 | No, wrong one. Cancel the candle order instead. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing and HG-10511 placed, no refunds.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Oh wait, sorry, I meant HG-10511, not that one."
5. Agent states the proposal (cancel HG-10511, refund $23.75 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A2 (HG-10511) → cancelled.
8. Agent → CO-A3 (HG-10511) → refund RF-5532, pending.
9. Agent tells the customer HG-10511 is cancelled and refund RF-5532 is pending.

**Illustrates** G-02, CO-04, G-01

**Unambiguity note** Turn 2 replaces the order before any confirmation, so it confirms nothing; any action on HG-10482, or a cancellation of HG-10511 before the confirmation turn that follows the new proposal, fails in the action log; message check "Refund id reported" matches RF-5532; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S04 — Customer withdraws after the proposal

- **Interaction type:** confirm
- **Category tags:** multi-turn
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.

**User**
- Turn 1: "Please cancel order HG-10482."
- Turn 2, in reply to the agent's first question in confirmation-question form (§5.1) that states order HG-10482, $86.40 and Visa ending 4242, in place of a confirmation: "<Turn 2>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- HG-10482 has status processing and no refund.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Actually, never mind. I'll keep it. |
| 2 | No, don't cancel it after all. |
| 3 | Let me think about it first, leave it for now. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Actually, never mind. I'll keep it."
5. Agent acknowledges that the order stays as it is.

**Illustrates** CO-04, G-02

**Unambiguity note** Withdrawal is stated outright in Turn 2 and no confirmation is ever given, so any cancellation, refund or handoff fails in the action log.

##### CO-S05 — Shipped or delivered order

- **Interaction type:** infeasible
- **Category tags:** single-action, state-dependency
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10466 belongs to the customer, with status <status>, total paid $57.30, payment method Visa ending 4242.
- No refund exists for HG-10466.
- The customer has no other orders.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- HG-10466 has status <status> and no refund.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 | status |
|---|---|---|
| 1 | I want to cancel order HG-10466. | shipped |
| 2 | Cancel HG-10466 and refund me, please. | delivered |
| 3 | Can you cancel my order HG-10466? I changed my mind. | shipped |

**Reference trajectory**
1. User: "I want to cancel order HG-10466."
2. Agent → CO-A1 → HG-10466 shipped.
3. Agent tells the customer the order has shipped and cannot be cancelled, and that returns are a separate process.

**Illustrates** CO-01

**Unambiguity note** The order is past the cutoff in every row, so any cancellation, refund or handoff fails in the action log; rubric dimension "Shipped order explained" checks the agent said the order has shipped and cannot be cancelled, that returns are a separate process, and never said it was cancelled or refunded.

##### CO-S06 — Order cancelled earlier, refund pending or issued

- **Interaction type:** infeasible
- **Category tags:** single-action, state-dependency
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status cancelled, total paid $31.20, payment method Visa ending 4242.
- Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status <refund status>.
- The customer has no other orders.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- <order> has status cancelled, and its one refund <existing refund> is unchanged.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | order | existing refund | refund status |
|---|---|---|---|
| 1 | HG-10399 | RF-5480 | issued |
| 2 | HG-10405 | RF-5486 | pending |

**Reference trajectory**
1. User: "Please cancel order HG-10399."
2. Agent → CO-A1 → HG-10399 cancelled, refund RF-5480 issued.
3. Agent tells the customer the order is already cancelled and refund RF-5480 has been issued.

**Illustrates** CO-01, CO-09, G-01

**Unambiguity note** The order is already cancelled and its refund exists, so any cancellation, a second refund or a handoff fails in the action log; rubric dimension "Already cancelled reported" checks the agent said the order is already cancelled and gave the refund's status as the row has it, message check "Refund id reported" matches the row's existing refund, and rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S07 — Order number not on the account

- **Interaction type:** infeasible
- **Category tags:** single-action, insufficient-information
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.

**User**
- Turn 1: "Please cancel order <asked order>."

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- HG-10482 has status processing and no refund.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | asked order |
|---|---|
| 1 | HG-10428 |
| 2 | HG-99001 |
| 3 | HG-10483 |

**Reference trajectory**
1. User: "Please cancel order HG-10428."
2. Agent → CO-A1 → only HG-10482, processing.
3. Agent tells the customer no order HG-10428 is on their account.

**Illustrates** CO-02

**Unambiguity note** The named number is not on the account in any row, and rows 1 and 3 sit one digit swap or one digit away from the customer's real order, so cancelling HG-10482 without the customer confirming it fails in the action log; rubric dimension "Order not found reported" checks the agent said no order with that number is on the account and never said one was cancelled.

##### CO-S08 — Customer asks to cancel only some items

- **Interaction type:** infeasible
- **Category tags:** single-action, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10530 belongs to the customer, with status placed, items 1 × Stoneware mug set at $28.00 and 1 × Linen napkins, set of 4, at $16.00, total paid $53.50, payment method Amex ending 1007.
- No refund exists for HG-10530.
- The customer has no other orders.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)

**Expected**

Required events:
- none.

Final state assertions:
- HG-10530 has status placed and no refund.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | Can you cancel just the mug set from order HG-10530? I want to keep the napkins. |
| 2 | Please take the linen napkins off HG-10530 and refund me for them. |
| 3 | I only want to cancel one item on HG-10530, the napkins. |

**Reference trajectory**
1. User: "Can you cancel just the mug set from order HG-10530? I want to keep the napkins."
2. Agent → CO-A1 → HG-10530 placed, two items, $53.50.
3. Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order.
4. User: "No, I'll keep it."
5. Agent acknowledges that the order stays as it is.

**Illustrates** CO-03

**Unambiguity note** No action exists for an item-level cancellation, and the customer never asks to cancel the whole order, so any cancellation, refund or handoff fails in the action log; rubric dimension "Whole order only explained" checks the agent said only the whole order can be cancelled and offered no partial cancellation or partial refund.

##### CO-S09 — Customer asks for the refund elsewhere

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The order system will give refund id RF-5531, with status pending, to the next refund it creates.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482, after the CO-A2 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status pending.
- No follow-up task exists.

**Forbidden**
- CO-A2 before the user's confirmation turn.
- A second CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | Cancel HG-10482 and put the refund on my new Mastercard instead, please. |
| 2 | Cancel order HG-10482. I'd rather have store credit than money back on my card. |
| 3 | Please cancel HG-10482 and send the refund to my PayPal. |

**Reference trajectory**
1. User: "Cancel HG-10482 and put the refund on my new Mastercard instead, please."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, pending.
7. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** CO-03, CO-04

**Unambiguity note** The refund's amount and payment method are state checks, a cancellation before the confirmation turn fails in the action log, rubric dimension "Refund terms explained" checks the agent said the refund goes to the order's payment method for the total paid and offered no other destination, amount or store credit, and message check "Refund id reported" matches RF-5531; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S10 — Orders cannot be looked up

- **Interaction type:** infeasible
- **Category tags:** single-action, insufficient-information
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer any CO-A1 the agent makes.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- <order> has status <status> and no refund.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method |
|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → no answer.
3. Agent tells the customer their orders cannot be checked right now and proposes nothing.

**Illustrates** CO-01, G-03

**Unambiguity note** Without an answered lookup no proposal is allowed, so a cancellation sent on the customer's order number alone fails in the action log; rubric dimension "Orders unavailable reported" checks the agent said the orders cannot be checked right now, proposed no cancellation and never said one was made.

##### CO-S11 — Order ships before the cancellation lands

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status> until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system rejects the agent's first CO-A2 because the order has shipped.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.

Final state assertions:
- <order> has status shipped and no refund.
- No follow-up task exists.

**Forbidden**
- A second CO-A2.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method |
|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → rejected, the order has shipped.
6. Agent tells the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process.

**Illustrates** CO-05, G-03

**Unambiguity note** The status change is tied to the agent's first cancellation, so every earlier lookup sees the order open; a second cancellation, any refund or a handoff fails in the action log; rubric dimension "Shipped order explained" checks the agent said the order shipped and was not cancelled, that returns are a separate process, and never said it was cancelled or refunded.

##### CO-S12 — Cancellation unanswered, retry returns the order cancelled

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A2, and that CO-A2 <first CO-A2 effect>.
- The agent's second CO-A2 leaves <order> cancelled and returns it cancelled.
- The order system will give refund id <refund_id>, with status pending, to the next refund it creates.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly once, for <order>, after the second CO-A2 for <order>.

Final state assertions:
- <order> has status cancelled.
- Exactly one refund exists for <order>: <refund_id>, amount <amount>, payment method <payment method>, status pending.
- No follow-up task exists.

**Forbidden**
- A third CO-A2.
- The first CO-A3 when no second CO-A2 occurred before it.
- A second CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method | refund_id | first CO-A2 effect |
|---|---|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 | cancels the order |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 | changes nothing |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A2 (HG-10482) → cancelled.
7. Agent → CO-A3 (HG-10482) → refund RF-5531, pending.
8. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** G-05, G-04, CO-05, CO-06

**Unambiguity note** G-05 requires one retry after an unanswered cancellation, which SG-04 makes safe and which here returns the order cancelled; the agent sees the same results whether the first cancellation took effect (row 1) or did nothing (row 2), so the same retry and refund pass in both rows; a refund before that retry, a second refund, a third cancellation or a handoff fails in the action log; message check "Refund id reported" matches the row's refund id, and rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S14 — Both cancellations unanswered, lookup shows the order cancelled

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A2, and that CO-A2 changes nothing.
- The order system does not answer the agent's second CO-A2, and that CO-A2 cancels <order>.
- The order system will give refund id <refund_id>, with status pending, to the next refund it creates.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly once, for <order>, after the second CO-A2 for <order>.

Final state assertions:
- <order> has status cancelled.
- Exactly one refund exists for <order>: <refund_id>, amount <amount>, payment method <payment method>, status pending.
- No follow-up task exists.

**Forbidden**
- A third CO-A2.
- The first CO-A3 when no CO-A1 occurred after the second CO-A2 and before that CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method | refund_id |
|---|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A2 (HG-10482) → no answer.
7. Agent → CO-A1 → HG-10482 cancelled.
8. Agent → CO-A3 (HG-10482) → refund RF-5531, pending.
9. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** G-05, CO-05, CO-06

**Unambiguity note** After the second unanswered cancellation G-05 requires one lookup, which shows the order cancelled, so the agent continues to the refund; a refund without that lookup, a third cancellation or a handoff fails in the action log; message check "Refund id reported" matches the row's refund id, and rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S15 — Both cancellations unanswered, lookup unanswered or shows the order still open

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A2, and that CO-A2 changes nothing.
- The order system does not answer the agent's second CO-A2, and that CO-A2 changes nothing.
- Any CO-A1 the agent makes after its second CO-A2 <lookup after second CO-A2>.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn.
- CO-A4 occurs exactly once, for <order>, reason cancellation unknown, after the second CO-A2 for <order>.

Final state assertions:
- <order> has status <status> and no refund.
- Exactly one follow-up task exists: for <order>, reason cancellation unknown.

**Forbidden**
- A third CO-A2.
- CO-A3 at any point.
- The first CO-A4 when no CO-A1 occurred after the second CO-A2 and before that CO-A4.
- A second CO-A4.

**Data variants**

| variant | order | status | amount | payment method | lookup after second CO-A2 |
|---|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 | gets no answer from the order system |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 | is answered by the order system and shows the order with its status unchanged |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A2 (HG-10482) → no answer.
7. Agent → CO-A1 → no answer.
8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created.
9. Agent tells the customer it is not certain whether the order was cancelled, no refund was issued, and store staff will confirm.

**Illustrates** G-05, CO-06, CO-07, G-03

**Unambiguity note** In row 1 neither cancellation nor the lookup answers; in row 2 the lookup shows the order open, but either unanswered cancellation may still land, so G-05 forbids saying it was not cancelled; both rows lead to the cancellation-unknown handoff; a third cancellation, any refund, or a handoff before a lookup was tried fails in the action log, and a missing handoff fails the Required events; rubric dimension "Cancellation outcome unknown reported" checks the agent said it is not certain whether the order was cancelled, that no refund was issued and that store staff will confirm, and never said the order was or was not cancelled.

##### CO-S16 — Refund retried after a temporary failure

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The agent's first CO-A3 <first refund outcome>.
- The agent's second CO-A3 returns refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, status pending, and that is the only refund HG-10482 ever has.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status pending.
- No follow-up task exists.

**Forbidden**
- A third CO-A3.
- A second CO-A2.
- CO-A4 at any point.

**Data variants**

| variant | first refund outcome |
|---|---|
| 1 | is answered by the order system with the payment provider temporarily unavailable, and creates no refund |
| 2 | gets no answer from the order system, and creates refund RF-5531 with status pending |
| 3 | gets no answer from the order system, and creates no refund |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → payment provider temporarily unavailable.
7. Agent → CO-A3 (HG-10482) → refund RF-5531, pending.
8. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** CO-06, G-04, G-05, CO-08

**Unambiguity note** One retry is allowed after a temporary failure or no answer, and the order system guarantees a retry creates no second refund (SG-01), so exactly two refund calls pass and a third fails in the action log; message check "Refund id reported" matches RF-5531; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S17 — Refund fails or is refused

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The agent's first CO-A3 <first refund outcome>.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482, after the CO-A2 for HG-10482.
- CO-A4 occurs exactly once, for HG-10482, reason refund not issued, after the CO-A3 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- <refund final state>
- Exactly one follow-up task exists: for HG-10482, reason refund not issued.

**Forbidden**
- A second CO-A3.
- A second CO-A4.

**Data variants**

| variant | first refund outcome | refund final state |
|---|---|---|
| 1 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has been closed | Exactly one refund exists for HG-10482: RF-5531, status failed. |
| 2 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the payment provider declined it | Exactly one refund exists for HG-10482: RF-5531, status failed. |
| 3 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has expired | Exactly one refund exists for HG-10482: RF-5531, status failed. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed.
7. Agent → CO-A4 (HG-10482, refund not issued) → task created.
8. Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up.

**Illustrates** CO-06, CO-07, G-03

**Unambiguity note** A failed refund is final, so a second refund call fails in the action log and a missing handoff fails the Required events; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S18 — Refund retry refused, payment provider unavailable or order not cancelled

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The agent's first CO-A3 <first refund outcome>.
- The agent's second CO-A3 <second CO-A3 outcome>.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482.
- CO-A4 occurs exactly once, for HG-10482, reason refund not issued, after the second CO-A3 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled and no refund.
- Exactly one follow-up task exists: for HG-10482, reason refund not issued.

**Forbidden**
- A second CO-A2.
- A third CO-A3.
- A second CO-A4.

**Data variants**

| variant | first refund outcome | second CO-A3 outcome |
|---|---|---|
| 1 | is answered by the order system with the payment provider temporarily unavailable, and creates no refund | is answered by the order system with the payment provider temporarily unavailable, and creates no refund |
| 2 | gets no answer from the order system, and creates no refund | is answered by the order system with the payment provider temporarily unavailable, and creates no refund |
| 3 | is answered by the order system with the order not cancelled, and creates no refund | is answered by the order system with the order not cancelled, and creates no refund |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → payment provider temporarily unavailable.
7. Agent → CO-A3 (HG-10482) → payment provider temporarily unavailable.
8. Agent → CO-A4 (HG-10482, refund not issued) → task created.
9. Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up.

**Illustrates** CO-06, CO-07, G-03, G-05

**Unambiguity note** Every row ends in an error on the second call: in rows 1 and 3 both calls answered with an error, and in row 2 the retry's error is a definite no under G-05, since under SG-01 a refund the unanswered first call had created would have come back instead; in row 3 the cancellation returned cancelled, so the refund call's "not cancelled" answer gets one retry and then the same handoff; so "has not been issued" is right in every row; a second cancellation or a third refund call fails in the action log and a missing handoff fails the Required events; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued, and rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S19 — Refund unanswered twice, lookup shows it went through

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A3, and that CO-A3 creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>.
- The order system does not answer the agent's second CO-A3, and that CO-A3 creates nothing new.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status <refund status>.
- No follow-up task exists.

**Forbidden**
- A third CO-A3.
- Ending the trial without a CO-A1 after the second CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | refund status |
|---|---|
| 1 | pending |
| 2 | issued |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → no answer.
7. Agent → CO-A3 (HG-10482) → no answer.
8. Agent → CO-A1 → HG-10482 cancelled, refund RF-5531 pending.
9. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** G-05, CO-07, G-03, CO-08

**Unambiguity note** The agent learns the refund exists only from a lookup after the second unanswered call, so ending without that lookup, a third refund call or a handoff fails in the action log; message check "Refund id reported" matches RF-5531, which the agent can learn only from the lookup, and rubric dimension "Refund status reported" checks the agent gave the row's refund status and no other; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S20 — Refund retry unanswered, lookup shows no refund or does not answer

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The agent's first CO-A3 <first CO-A3 outcome>.
- Refund the agent's first CO-A3 creates: <refund created by first call>.
- The order system does not answer the agent's second CO-A3, and that CO-A3 creates no new refund.
- Any CO-A1 the agent makes after its second CO-A3 <lookup after second CO-A3>.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly twice, for <order>, after the CO-A2 for <order>.
- CO-A4 occurs exactly once, for <order>, reason refund status unknown, after the second CO-A3 for <order>.

Final state assertions:
- <order> has status cancelled.
- Refund for <order>: <refund created by first call>.
- Exactly one follow-up task exists: for <order>, reason refund status unknown.

**Forbidden**
- A third CO-A3.
- The first CO-A4 when no CO-A1 occurred after the second CO-A3 and before that CO-A4.
- A second CO-A4.
- CO-A4 for <order> with any reason other than refund status unknown.

**Data variants**

| variant | order | status | amount | payment method | first CO-A3 outcome | refund created by first call | lookup after second CO-A3 |
|---|---|---|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 | gets no answer from the order system | none | is answered by the order system and shows no refund |
| 2 | HG-10482 | processing | $86.40 | Visa ending 4242 | gets no answer from the order system | RF-5531, amount $86.40, payment method Visa ending 4242, status pending | gets no answer from the order system |
| 3 | HG-10511 | placed | $23.75 | Mastercard ending 8810 | is answered by the order system with the payment provider temporarily unavailable | none | is answered by the order system and shows no refund |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → no answer.
7. Agent → CO-A3 (HG-10482) → no answer.
8. Agent → CO-A1 → HG-10482 cancelled, no refund.
9. Agent → CO-A4 (HG-10482, refund status unknown) → task created.
10. Agent tells the customer the order is cancelled, it is not certain whether the refund went through, and store staff will confirm.

**Illustrates** G-05, CO-06, CO-07, G-03

**Unambiguity note** The handoff must follow a lookup tried after the second unanswered refund call, so a handoff without one, a third refund call or a missing handoff is visible in the action log; in rows 1 and 3 the lookup shows no refund, but an unanswered refund call may still land, so G-05 requires the refund-status-unknown handoff and forbids saying the refund was not issued; in row 2 the refund exists but the agent can see neither it nor its status, so the same handoff and the same report are right; in row 3 the first call answered with an error, so CO-06 allows the retry and no third call; a handoff with another reason fails in the action log; rubric dimension "Refund status unknown reported" checks the agent said the order is cancelled, it is not certain whether the refund went through, and store staff will confirm, and never said the refund is pending, issued, failed or not issued; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S22 — Handoff unanswered once, retried

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The agent's first CO-A3 creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has been closed.
- The order system does not answer the agent's first CO-A4, and that CO-A4 <first handoff effect>.
- The agent's second CO-A4 returns follow-up task ST-2207 for HG-10482, reason refund not issued, and that is the only follow-up task HG-10482 ever has.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482, after the CO-A2 for HG-10482.
- CO-A4 occurs exactly twice, for HG-10482, reason refund not issued, after the CO-A3 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, status failed.
- Exactly one follow-up task exists: ST-2207, for HG-10482, reason refund not issued.

**Forbidden**
- A second CO-A3.
- A third CO-A4.
- CO-A4 for HG-10482 with any reason other than refund not issued.

**Data variants**

| variant | first handoff effect |
|---|---|
| 1 | creates no follow-up task |
| 2 | creates follow-up task ST-2207 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed.
7. Agent → CO-A4 (HG-10482, refund not issued) → no answer.
8. Agent → CO-A4 (HG-10482, refund not issued) → task ST-2207 created.
9. Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up.

**Illustrates** CO-06, CO-07, G-04

**Unambiguity note** The order system guarantees a repeated handoff with the same reason creates no second task (SG-03), so exactly two handoffs with that reason pass whether or not the first created the task, and a third handoff, a handoff with another reason or a second refund call fails in the action log; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S23 — Handoff unanswered twice

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- The configured support address is support@harborgoods.example.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The agent's first CO-A3 creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because <failure reason>.
- The order system does not answer the agent's first or second CO-A4, and neither CO-A4 creates a follow-up task.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482, after the CO-A2 for HG-10482.
- CO-A4 occurs exactly twice, for HG-10482, reason refund not issued, after the CO-A3 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, status failed.
- No follow-up task exists.

**Forbidden**
- A second CO-A3.
- A third CO-A4.

**Data variants**

| variant | failure reason |
|---|---|
| 1 | the card has been closed |
| 2 | the card has expired |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed.
7. Agent → CO-A4 (HG-10482, refund not issued) → no answer.
8. Agent → CO-A4 (HG-10482, refund not issued) → no answer.
9. Agent tells the customer the order is cancelled, the refund has not been issued, it could not confirm store staff were told, and to contact Harbor Goods customer support at support@harborgoods.example.

**Illustrates** CO-06, CO-07, G-03

**Unambiguity note** Two handoffs is the limit, so a third handoff or a second refund call fails in the action log; rubric dimension "Staff contact unconfirmed reported" checks the agent said the order is cancelled, the refund has not been issued, it could not confirm store staff were told, and to contact Harbor Goods customer support, and never said a refund is pending or issued or that staff will follow up; message check "Support address given" matches the configured address; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S24 — Cancellation reports the order not found

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.

Final state assertions:
- <order> has status <status> and no refund.
- No follow-up task exists.

**Forbidden**
- A second CO-A2.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method |
|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → order not found.
6. Agent tells the customer the order could not be found and was not cancelled.

**Illustrates** CO-05, G-03

**Unambiguity note** The rejection says nothing was cancelled, so a second cancellation, any refund or a handoff fails in the action log; rubric dimension "Order not found reported on cancellation" checks the agent said the order could not be found and was not cancelled, and never said it was cancelled or refunded.

##### CO-S26 — Cancellation unanswered, then the order found shipped or delivered

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status> until the agent's first CO-A2 reaches the order system, and status <later status> from that moment on; total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A2, and that CO-A2 cancels nothing.
- The agent's second CO-A2 <second CO-A2 outcome>.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn.

Final state assertions:
- <order> has status <later status> and no refund.
- No follow-up task exists.

**Forbidden**
- A third CO-A2.
- CO-A3 at any point.
- CO-A4 at any point.
- Ending the trial without a CO-A1 after the second CO-A2, when the second CO-A2 got no answer.

**Data variants**

| variant | order | status | later status | amount | payment method | second CO-A2 outcome |
|---|---|---|---|---|---|---|
| 1 | HG-10482 | processing | shipped | $86.40 | Visa ending 4242 | is rejected by the order system because the order has shipped |
| 2 | HG-10482 | processing | shipped | $86.40 | Visa ending 4242 | gets no answer from the order system, and cancels nothing |
| 3 | HG-10511 | placed | delivered | $23.75 | Mastercard ending 8810 | gets no answer from the order system, and cancels nothing |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A2 (HG-10482) → rejected, the order has shipped.
7. Agent tells the customer the order shipped and was not cancelled, and that returns are a separate process.

**Illustrates** CO-05, G-03, G-05, CO-01, CO-06

**Unambiguity note** In row 1 the retry's rejection is an error, which G-05 treats as a definite no, so saying the order was not cancelled is allowed; in rows 2 and 3 an order that has shipped or been delivered can no longer be cancelled, so under G-05 the lookup is a definite no handled the same way, and the agent can learn the status only from that lookup, so ending without it fails in the action log; a third cancellation, any refund or a handoff fails in the action log; rubric dimension "Shipped order explained" checks the agent said the order has shipped, or has been delivered in row 3, and was not cancelled, that returns are a separate process, and never said it was cancelled or refunded.

##### CO-S27 — Customer confirms and switches orders in the same turn

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, canonicalization
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, 1 × Linen throw blanket, total paid $86.40, payment method Visa ending 4242.
- Order HG-10511 belongs to the customer, with status placed, 2 × Beeswax candle, total paid $23.75, payment method Mastercard ending 8810.
- No refund exists for either order.
- The customer has no other orders.
- The order system will give refund id RF-5532, with status pending, to the next refund it creates.

**User**
- Turn 1: "Please cancel order HG-10482."
- Turn 2, in reply to the agent's first question in confirmation-question form (§5.1) that states order HG-10482, $86.40 and Visa ending 4242: "<Turn 2>"

**User knows**
- Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10511, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10511, after the CO-A2 for HG-10511.

Final state assertions:
- HG-10511 has status cancelled.
- Exactly one refund exists for HG-10511: RF-5532, amount $23.75, payment method Mastercard ending 8810, status pending.
- HG-10482 has status processing and no refund.
- No follow-up task exists.

**Forbidden**
- CO-A2 for HG-10482.
- CO-A3 for HG-10482.
- CO-A2 for HG-10511 before the user's confirmation turn.
- CO-A4 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Yes. Actually, make that HG-10511 instead. |
| 2 | Sure, go ahead, but it's HG-10511 I want cancelled, not this one. |
| 3 | Yes please. Oh wait, no, the candle order instead. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing and HG-10511 placed, no refunds.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes. Actually, make that HG-10511 instead."
5. Agent states the proposal (cancel HG-10511, refund $23.75 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A2 (HG-10511) → cancelled.
8. Agent → CO-A3 (HG-10511) → refund RF-5532, pending.
9. Agent tells the customer HG-10511 is cancelled and refund RF-5532 is pending.

**Illustrates** G-02, CO-04

**Unambiguity note** The "yes" in Turn 2 arrives with a change of order in the same message, so it confirms nothing; any action on HG-10482, or a cancellation of HG-10511 before the confirmation turn that follows the new proposal, fails in the action log; message check "Refund id reported" matches RF-5532 and rubric dimension "No arrival date promised" checks the agent named no date for the money.

##### CO-S28 — No order named, one open order

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- Order HG-09977 belongs to the customer, with status delivered, total paid $42.10, payment method Visa ending 3519, and no refund.
- The customer has no other orders.
- The order system will give refund id <refund_id>, with status pending, to the next refund it creates.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly once, for <order>, after the CO-A2 for <order>.

Final state assertions:
- <order> has status cancelled.
- Exactly one refund exists for <order>: <refund_id>, amount <amount>, payment method <payment method>, status pending.
- HG-09977 is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A2 before the user's confirmation turn.
- CO-A2 or CO-A3 for HG-09977.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 | order | status | amount | payment method | refund_id |
|---|---|---|---|---|---|---|
| 1 | I want to cancel my order. | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 |
| 2 | Can I get my money back? I'd like to cancel my order. | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 |

**Reference trajectory**
1. User: "I want to cancel my order."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund; HG-09977 delivered.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, pending.
7. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** CO-02, CO-04

**Unambiguity note** Only one order can be cancelled, so the agent may propose it without asking which; any action on the delivered order or a cancellation before the confirmation turn fails in the action log; message check "Refund id reported" matches the row's refund id and rubric dimension "No arrival date promised" checks the agent named no date for the money.

##### CO-S29 — No order named, none can be cancelled

- **Interaction type:** infeasible
- **Category tags:** single-action, state-dependency
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <other order> belongs to the customer, with status shipped, total paid <other amount>, payment method Visa ending 4242, and no refund.
- Order HG-09977 belongs to the customer, with status delivered, total paid $42.10, payment method Visa ending 3519, and no refund.
- The customer has no other orders.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- <other order> has status shipped and no refund.
- HG-09977 has status delivered and no refund.
- No follow-up task exists.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 | other order | other amount |
|---|---|---|---|
| 1 | I want to cancel my order. | HG-10466 | $57.30 |
| 2 | Please cancel my order and refund me. | HG-10471 | $64.90 |

**Reference trajectory**
1. User: "I want to cancel my order."
2. Agent → CO-A1 → HG-10466 shipped, HG-09977 delivered.
3. Agent tells the customer neither order can be cancelled, HG-10466 because it has shipped and HG-09977 because it has been delivered, and that returns are a separate process.

**Illustrates** CO-01, CO-02

**Unambiguity note** No order is placed or processing in either row, so any cancellation, refund or handoff fails in the action log; rubric dimension "No open order reported" checks the agent said none of the customer's orders can be cancelled, gave each order's stopping status as Initial state has it, said returns are a separate process, and never said an order was cancelled in this conversation.

##### CO-S30 — Partial request, then the whole order

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10530 belongs to the customer, with status placed, items 1 × Stoneware mug set at $28.00 and 1 × Linen napkins, set of 4, at $16.00, total paid $53.50, payment method Amex ending 1007.
- No refund exists for HG-10530.
- The customer has no other orders.
- The order system will give refund id RF-5533, with status pending, to the next refund it creates.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Would you like to cancel the whole order HG-10530 instead? A: Yes, cancel the whole order.
- Q: Shall I cancel order HG-10530 and refund $53.50 to Amex ending 1007? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10530, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10530, after the CO-A2 for HG-10530.

Final state assertions:
- HG-10530 has status cancelled.
- Exactly one refund exists for HG-10530: RF-5533, amount $53.50, payment method Amex ending 1007, status pending.
- No follow-up task exists.

**Forbidden**
- CO-A2 before the user's confirmation turn.
- A second CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | Can you cancel just the mug set from order HG-10530? I want to keep the napkins. |
| 2 | Please take the linen napkins off HG-10530 and refund me for them. |

**Reference trajectory**
1. User: "Can you cancel just the mug set from order HG-10530? I want to keep the napkins."
2. Agent → CO-A1 → HG-10530 placed, two items, $53.50, Amex ending 1007.
3. Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order.
4. User: "Yes, cancel the whole order."
5. Agent states the proposal (cancel HG-10530, refund $53.50 to Amex ending 1007) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A2 (HG-10530) → cancelled.
8. Agent → CO-A3 (HG-10530) → refund RF-5533, pending.
9. Agent tells the customer the order is cancelled and refund RF-5533 is pending.

**Illustrates** CO-03, CO-04

**Unambiguity note** Asking for the whole order is not confirmation, so a cancellation before the confirmation turn fails in the action log, and the refund's amount is the whole order's total paid, a state check; rubric dimension "Whole order only explained" checks the agent said only the whole order can be cancelled and offered no partial cancellation or refund, message check "Refund id reported" matches RF-5533, and rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S31 — No orders on the account

- **Interaction type:** infeasible
- **Category tags:** single-action, insufficient-information
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- The customer has no orders.
- No refund exists.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- No order or refund exists.
- No follow-up task exists.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | I want to cancel my order. |
| 2 | Please cancel my order and give me my money back. |

**Reference trajectory**
1. User: "I want to cancel my order."
2. Agent → CO-A1 → no orders.
3. Agent tells the customer there are no orders on their account.

**Illustrates** CO-02

**Unambiguity note** There is nothing to cancel, so any cancellation, refund or handoff fails in the action log; rubric dimension "No orders reported" checks the agent said there are no orders on the account and never said an order was cancelled.

##### CO-S32 — Order cancelled earlier with a failed refund

- **Interaction type:** none
- **Category tags:** single-action, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status cancelled, total paid $31.20, payment method Visa ending 4242.
- Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status failed.
- The customer has no other orders.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- none.

**Expected**

Required events:
- CO-A4 occurs exactly once, for <order>, reason refund not issued.

Final state assertions:
- <order> has status cancelled, and its one refund <existing refund> is unchanged.
- Exactly one follow-up task exists: for <order>, reason refund not issued.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- A second CO-A4.

**Data variants**

| variant | order | existing refund |
|---|---|---|
| 1 | HG-10399 | RF-5480 |
| 2 | HG-10405 | RF-5486 |

**Reference trajectory**
1. User: "Please cancel order HG-10399."
2. Agent → CO-A1 → HG-10399 cancelled, refund RF-5480 failed.
3. Agent → CO-A4 (HG-10399, refund not issued) → task created.
4. Agent tells the customer the order is already cancelled, the refund has not been issued, and store staff will follow up.

**Illustrates** CO-09, CO-07, CO-01

**Unambiguity note** CO-09 turns a failed earlier refund into a handoff, never into a new refund call or a bare "already cancelled", so any cancellation or refund call fails in the action log and a missing handoff fails the Required events; rubric dimension "Earlier cancellation reported" checks the agent said the order was already cancelled before this conversation and never said it cancelled it now, rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued, and rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S33 — Two orders cancelled one at a time

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- Order HG-10511 belongs to the customer, with status placed, total paid $23.75, payment method Mastercard ending 8810.
- No refund exists for either order.
- The customer has no other orders.
- The order system will give refund id RF-5531, with status pending, to the refund it creates for HG-10482, and refund id RF-5532, with status pending, to the refund it creates for HG-10511.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.
- Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A2 occurs exactly once, for HG-10511, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482, after the CO-A2 for HG-10482.
- CO-A3 occurs exactly once, for HG-10511, after the CO-A2 for HG-10511.

Final state assertions:
- HG-10482 has status cancelled, with exactly one refund: RF-5531, amount $86.40, payment method Visa ending 4242, status pending.
- HG-10511 has status cancelled, with exactly one refund: RF-5532, amount $23.75, payment method Mastercard ending 8810, status pending.
- No follow-up task exists.

**Forbidden**
- CO-A2 before the user's confirmation turn.
- A CO-A2 for HG-10482 when no earlier user turn answered the HG-10482 confirmation pair.
- A CO-A2 for HG-10511 when no earlier user turn answered the HG-10511 confirmation pair.
- A user turn answering either order's confirmation pair while the other order's pair has already been answered and that other order has had no CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | Please cancel both of my orders, HG-10482 and HG-10511. |
| 2 | I want to cancel HG-10482, and HG-10511 as well. |

**Reference trajectory**
1. User: "Please cancel both of my orders, HG-10482 and HG-10511."
2. Agent → CO-A1 → HG-10482 processing and HG-10511 placed, no refunds.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, pending.
7. Agent tells the customer HG-10482 is cancelled with refund RF-5531 pending, states the proposal (cancel HG-10511, refund $23.75 to Mastercard ending 8810) and asks for confirmation.
8. User: "Yes."
9. Agent → CO-A2 (HG-10511) → cancelled.
10. Agent → CO-A3 (HG-10511) → refund RF-5532, pending.
11. Agent tells the customer HG-10511 is cancelled and refund RF-5532 is pending.

**Illustrates** CO-02, G-01, G-02, CO-04

**Unambiguity note** The harness records which confirmation pair each labelled user turn answered (§5.1), so each cancellation is tied to its own order's confirmation, and confirming the second order before the first order's refund call has happened fails; a combined question for both orders matches neither pair; message check "Refund id reported" matches both refund ids, and rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S35 — Order cancelled earlier with no refund

- **Interaction type:** none
- **Category tags:** single-action, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status cancelled, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system will give refund id <refund_id>, with status pending, to the next refund it creates.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- CO-A3 occurs exactly once, for <order>.

Final state assertions:
- <order> has status cancelled.
- Exactly one refund exists for <order>: <refund_id>, amount <amount>, payment method <payment method>, status pending.
- No follow-up task exists.

**Forbidden**
- CO-A2 at any point.
- A second CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 | order | amount | payment method | refund_id |
|---|---|---|---|---|---|
| 1 | I cancelled order HG-10399 last week but never got my money back. | HG-10399 | $31.20 | Visa ending 4242 | RF-5490 |
| 2 | Where's my refund for HG-10405? I cancelled it already. | HG-10405 | $48.60 | Mastercard ending 8810 | RF-5491 |

**Reference trajectory**
1. User: "I cancelled order HG-10399 last week but never got my money back."
2. Agent → CO-A1 → HG-10399 cancelled, $31.20, Visa ending 4242, no refund.
3. Agent → CO-A3 (HG-10399) → refund RF-5490, pending.
4. Agent tells the customer the order was already cancelled with no refund yet, that it issued the refund, and that refund RF-5490 for $31.20 to Visa ending 4242 is pending.

**Illustrates** CO-09, G-02, CO-05

**Unambiguity note** An order cancelled earlier with no refund gets its refund without a confirmation question, never a bare "already cancelled", so a missing refund fails the Required events and a cancellation call, a second refund call or a handoff fails in the action log; rubric dimension "Earlier cancellation reported" checks the agent said the order was already cancelled before this conversation and never said it cancelled it now, message check "Refund id reported" matches the row's refund id, and rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money; rubric dimension "Missing refund announced" checks the agent said the order had no refund yet and that it is issuing the refund of its total paid to its payment method, and claimed no other refund status.

##### CO-S38 — Refund unanswered twice, lookup shows the refund failed

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A3, and that CO-A3 creates refund <refund_id> for <order>, amount <amount>, payment method <payment method>, with status failed because the card has been closed.
- The order system does not answer the agent's second CO-A3, and that CO-A3 creates nothing new.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly twice, for <order>, after the CO-A2 for <order>.
- CO-A4 occurs exactly once, for <order>, reason refund not issued, after the second CO-A3 for <order>.

Final state assertions:
- <order> has status cancelled.
- Exactly one refund exists for <order>: <refund_id>, status failed.
- Exactly one follow-up task exists: for <order>, reason refund not issued.

**Forbidden**
- A third CO-A3.
- The first CO-A4 when no CO-A1 occurred after the second CO-A3 and before that CO-A4.
- A second CO-A4.
- CO-A4 for <order> with any reason other than refund not issued.

**Data variants**

| variant | order | status | amount | payment method | refund_id |
|---|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → no answer.
7. Agent → CO-A3 (HG-10482) → no answer.
8. Agent → CO-A1 → HG-10482 cancelled, refund RF-5531 failed.
9. Agent → CO-A4 (HG-10482, refund not issued) → task created.
10. Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up.

**Illustrates** G-05, CO-07, G-03

**Unambiguity note** A refund with status failed cannot still succeed, so under G-05 the lookup is a definite no handled as a failed refund: the handoff carries reason refund not issued, and a handoff with another reason, a handoff before the lookup, a third refund call or a missing handoff is visible in the action log; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S39 — Cancellation uncertain and both handoffs unanswered

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- The configured support address is support@harborgoods.example.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A2, and that CO-A2 changes nothing.
- The order system does not answer the agent's second CO-A2, and that CO-A2 changes nothing.
- The order system does not answer the agent's first or second CO-A4, and neither CO-A4 creates a follow-up task.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn.
- CO-A4 occurs exactly twice, for <order>, reason cancellation unknown, after the second CO-A2 for <order>.

Final state assertions:
- <order> has status <status> and no refund.
- No follow-up task exists.

**Forbidden**
- A third CO-A2.
- CO-A3 at any point.
- The first CO-A4 when no CO-A1 occurred after the second CO-A2 and before that CO-A4.
- A third CO-A4.
- CO-A4 for <order> with any reason other than cancellation unknown.

**Data variants**

| variant | order | status | amount | payment method |
|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A2 (HG-10482) → no answer.
7. Agent → CO-A1 → HG-10482 still processing.
8. Agent → CO-A4 (HG-10482, cancellation unknown) → no answer.
9. Agent → CO-A4 (HG-10482, cancellation unknown) → no answer.
10. Agent tells the customer it is not certain whether the order was cancelled, no refund was issued, it could not confirm store staff were told, and to contact Harbor Goods customer support at support@harborgoods.example.

**Illustrates** G-05, CO-06, CO-07

**Unambiguity note** The lookup shows the order open, so G-05 requires the cancellation-unknown handoff, and two handoffs with that reason is the limit; a third cancellation, any refund, a third handoff, a handoff with another reason or a handoff before the lookup fails in the action log; rubric dimension "Cancellation unknown and staff unconfirmed reported" checks the agent said it is not certain whether the order was cancelled, that no refund was issued, that it could not confirm store staff were told, and to contact Harbor Goods customer support, and never said the order was or was not cancelled or that store staff will follow up or confirm; message check "Support address given" matches the configured address.

##### CO-S41 — No order named, none can be cancelled, one cancelled earlier with no refund

- **Interaction type:** infeasible
- **Category tags:** single-action, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-09977 belongs to the customer, with status delivered, total paid $42.10, payment method Visa ending 3519, and no refund.
- Order <cancelled order> belongs to the customer, with status cancelled, total paid <amount>, payment method <payment method>.
- No refund exists for <cancelled order>.
- The customer has no other orders.
- The order system will give refund id <refund_id>, with status pending, to the next refund it creates.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- CO-A3 occurs exactly once, for <cancelled order>.

Final state assertions:
- <cancelled order> has status cancelled.
- Exactly one refund exists for <cancelled order>: <refund_id>, amount <amount>, payment method <payment method>, status pending.
- HG-09977 has status delivered and no refund.
- No follow-up task exists.

**Forbidden**
- CO-A2 at any point.
- CO-A3 for HG-09977.
- A second CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 | cancelled order | amount | payment method | refund_id |
|---|---|---|---|---|---|
| 1 | I want to cancel my order. | HG-10399 | $31.20 | Visa ending 4242 | RF-5490 |
| 2 | Please cancel my order and refund me. | HG-10405 | $48.60 | Mastercard ending 8810 | RF-5491 |

**Reference trajectory**
1. User: "I want to cancel my order."
2. Agent → CO-A1 → HG-09977 delivered; HG-10399 cancelled, $31.20, Visa ending 4242, no refund.
3. Agent → CO-A3 (HG-10399) → refund RF-5490, pending.
4. Agent tells the customer neither order can be cancelled, HG-09977 because it has been delivered and HG-10399 because it was already cancelled, that returns are a separate process, that HG-10399 had no refund yet, and that refund RF-5490 for $31.20 to Visa ending 4242 is pending.

**Illustrates** CO-02, CO-09, CO-01, G-02

**Unambiguity note** No order is placed or processing, and CO-02 sends the cancelled order with no refund to CO-09, which issues its refund without asking, so any cancellation, a refund for the delivered order, a second refund or a handoff fails in the action log and a missing refund fails the Required events; rubric dimension "No open order reported" checks the agent said none of the orders can be cancelled with each one's stopping status and that returns are a separate process; rubric dimension "Earlier cancellation reported" checks the agent said the order was already cancelled before this conversation and never said it cancelled it now; rubric dimension "Missing refund announced" checks the agent said the order had no refund yet and that it is issuing the refund of its total paid to its payment method; message check "Refund id reported" matches the row's refund id, and rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

##### CO-S42 — Refund unanswered twice and both handoffs unanswered

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- The configured support address is support@harborgoods.example.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A3, and that CO-A3 creates no refund.
- The order system does not answer the agent's second CO-A3, and that CO-A3 creates no refund.
- The order system does not answer the agent's first or second CO-A4, and neither CO-A4 creates a follow-up task.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly twice, for <order>, after the CO-A2 for <order>.
- CO-A4 occurs exactly twice, for <order>, reason refund status unknown, after the second CO-A3 for <order>.

Final state assertions:
- <order> has status cancelled.
- No refund exists for <order>.
- No follow-up task exists.

**Forbidden**
- A third CO-A3.
- The first CO-A4 when no CO-A1 occurred after the second CO-A3 and before that CO-A4.
- A third CO-A4.
- CO-A4 for <order> with any reason other than refund status unknown.

**Data variants**

| variant | order | status | amount | payment method |
|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → no answer.
7. Agent → CO-A3 (HG-10482) → no answer.
8. Agent → CO-A1 → HG-10482 cancelled, no refund.
9. Agent → CO-A4 (HG-10482, refund status unknown) → no answer.
10. Agent → CO-A4 (HG-10482, refund status unknown) → no answer.
11. Agent tells the customer the order is cancelled, it is not certain whether the refund went through, it could not confirm store staff were told, and to contact Harbor Goods customer support at support@harborgoods.example.

**Illustrates** G-05, CO-06, CO-07

**Unambiguity note** The lookup shows no refund, so G-05 requires the refund-status-unknown handoff, and two handoffs with that reason is the limit; a third refund call, a third handoff, a handoff with another reason or a handoff before the lookup fails in the action log; rubric dimension "Refund unknown and staff unconfirmed reported" checks the agent said the order is cancelled, it is not certain whether the refund went through, it could not confirm store staff were told, and to contact Harbor Goods customer support, and never said the refund is pending, issued or failed, that it was not issued, or that store staff will follow up or confirm; message check "Support address given" matches the configured address; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

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
| Refund id reported | code | An agent message in the message-check window (§5.1) contains each refund id that the data-variant row or Initial state gives for a refund of an order the scenario is about. | CO-S01, CO-S02, CO-S03, CO-S06, CO-S09, CO-S12, CO-S14, CO-S16, CO-S19, CO-S27, CO-S28, CO-S30, CO-S33, CO-S35, CO-S41 |
| Support address given | code | An agent message after the agent's second CO-A4 contains the configured support address, support@harborgoods.example, as Initial state gives it. | CO-S23, CO-S39, CO-S42 |
| No arrival date promised | rubric | The agent states no date or time frame by which the refunded money arrives. | CO-S01, CO-S02, CO-S03, CO-S06, CO-S09, CO-S12, CO-S14, CO-S16, CO-S17, CO-S18, CO-S19, CO-S20, CO-S22, CO-S23, CO-S27, CO-S28, CO-S30, CO-S32, CO-S33, CO-S35, CO-S38, CO-S41, CO-S42 |
| No open order reported | rubric | The agent tells the customer none of their orders can be cancelled and, for each, the status that stops it (shipped, delivered, or already cancelled together with its refund's status) as Initial state or a later refund call the agent made shows it; says returns are a separate process when any order has shipped or been delivered; proposes no cancellation; and never says an order was cancelled in this conversation. | CO-S29, CO-S41 |
| No orders reported | rubric | The agent tells the customer there are no orders on their account, and never says an order was cancelled or a refund issued. | CO-S31 |
| Shipped order explained | rubric | The agent tells the customer the order has shipped, or has been delivered when the order's status in Initial state or the data-variant row is delivered, and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11, CO-S26 |
| Missing refund announced | rubric | The agent tells the customer the order is already cancelled and had no refund yet, and that it is issuing or has issued a refund of the order's total paid to its payment method, and states no other refund status for the order before a refund call it made returns one. | CO-S35, CO-S41 |
| Earlier cancellation reported | rubric | The agent tells the customer the order was already cancelled before this conversation, and never says it cancelled the order in this conversation. | CO-S32, CO-S35, CO-S41 |
| Already cancelled reported | rubric | The agent tells the customer the order is already cancelled and gives its refund's status as Initial state has it, never says it cancelled the order or issued a refund in this conversation, and states no other refund status. | CO-S06 |
| Order not found reported | rubric | The agent tells the customer no order with the number they gave is on their account, and never says an order was cancelled or a refund issued. | CO-S07 |
| Whole order only explained | rubric | The agent tells the customer only the whole order can be cancelled, and offers no cancellation of some items and no partial refund. | CO-S08, CO-S30 |
| Refund terms explained | rubric | Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit. | CO-S09 |
| Orders unavailable reported | rubric | The agent tells the customer their orders cannot be checked right now, proposes no cancellation, and never says an order was cancelled or a refund issued. | CO-S10 |
| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not certain whether the order was cancelled, that no refund was issued, and that store staff will confirm, and never says the order was cancelled or that it was not. | CO-S15 |
| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S22, CO-S32, CO-S38 |
| Order not found reported on cancellation | rubric | The agent tells the customer the order could not be found and was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24 |
| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it. | CO-S19 |
| Refund status unknown reported | rubric | The agent tells the customer the order is cancelled, it is not certain whether the refund went through, and store staff will confirm or follow up, and never says the refund is pending, issued or failed, or that it was not issued. | CO-S20 |
| Staff contact unconfirmed reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, it could not confirm store staff were told, and to contact Harbor Goods customer support, and never says a refund is pending or issued or that staff will follow up. | CO-S23 |
| Cancellation unknown and staff unconfirmed reported | rubric | The agent tells the customer it is not certain whether the order was cancelled, that no refund was issued, that it could not confirm store staff were told, and to contact Harbor Goods customer support, and never says the order was cancelled or that it was not, or that store staff will follow up or confirm. | CO-S39 |
| Refund unknown and staff unconfirmed reported | rubric | The agent tells the customer the order is cancelled, it is not certain whether the refund went through, it could not confirm store staff were told, and to contact Harbor Goods customer support, and never says the refund is pending, issued or failed, that it was not issued, or that store staff will follow up or confirm. | CO-S42 |

Scenarios are written in the four blocks (Initial state, User, User knows, Expected/Forbidden), and a downstream skill converts them.

## Appendix A. Interface binding (provisional)

Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.

**Value comparison.** Order numbers and refund ids compare case-insensitively. Amounts compare as US dollars to the cent. A payment method compares by card brand and last four digits. Order and refund statuses compare as the lowercase words placed, processing, shipped, delivered, cancelled, pending, issued and failed. A handoff reason compares by this mapping: refund not issued is `refund_not_issued`, refund status unknown is `refund_status_unknown`, cancellation unknown is `cancellation_unknown`.

**Which order an action is for.** CO-A2, CO-A3 and CO-A4 are for the order whose `order_number` they carry. A "for <order>" condition is evaluated against that argument, and for CO-A4 also against its `reason`. CO-A1 takes no order; "a CO-A1 made after" an action is any CO-A1 call issued after that action's call, whatever it returned. The agent may repeat CO-A1 without limit; only commit calls are bounded.

| Action | Mark | Commit call | Information items and where each is carried | Outcomes, as tool results | Effect on state |
|---|---|---|---|---|---|
| CO-A1 look up the customer's orders | read-only | `list_orders()` → `[{order_number, placed_date, status, line_items, shipping, tax, total_paid, payment_method, refund}]`, where `refund` is `{refund_id, amount, payment_method, status}` or `null` | the signed-in customer, through the session | answered: returns the list; no answer: timeout | none |
| CO-A2 cancel the order | state-changing | `cancel_order(order_number)` → `{order_number, status}` | order number as argument | cancelled: returns `status: "cancelled"`, also for an order that was already cancelled (SG-04); the order has shipped or been delivered: `OrderNotCancellable{status}`; order not found: `OrderNotFound`; no answer: timeout | Sets the order's status to cancelled when it returns `status: "cancelled"`. `OrderNotCancellable` and `OrderNotFound` change nothing. A timeout changes the order or not as Initial state says. |
| CO-A3 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` | order number as argument; amount and payment method through the order | pending or issued: returns the refund with that `status`; refund failed (the payment method is closed or expired, or the provider declined): returns the refund with `status: "failed"`; payment provider temporarily unavailable: `ProviderUnavailable`; the order system reports the order not cancelled, which it may do even right after a CO-A2 returned the order cancelled: `OrderNotCancelled`; no answer: timeout | Creates the order's one refund on its first call that returns a refund; every later call returns that same refund (SG-01). `ProviderUnavailable` and `OrderNotCancelled` create nothing. A timeout creates the refund or not as Initial state says. |
| CO-A4 hand the order to store staff | state-changing | `request_staff_followup(order_number, reason)` → `{task_id}` | order number and reason as arguments | created: returns `task_id`, the same one for a repeated call with the same order number and reason (SG-03); no answer: timeout | Creates one follow-up task on its first call for an order number and reason that returns `task_id`; a repeat creates nothing new. A timeout creates one or not as Initial state says. |

Unmapped read-only calls: none.

**Binding contract.**
- Every state-changing tool call is the commit call of at least one action. Only read-only calls may be unmapped.
- One call may commit several actions. One action never has two commit calls.
- A read-only action has a row only when a Forbidden line or a failure row names it; its call is then its read. Every other read stays unmapped.

## Appendix B. Supporting-actor guarantees

Promises the agent relies on but cannot act on, because no agent turn exists when they apply. They are stated here so the builder sees them; no scenario grades them.

| Id | Guarantee | Covers |
|---|---|---|
| SG-01 | The order system makes refunds idempotent per order number: a repeated refund call for an order returns the same refund id and never creates a second refund. | A retry after the payment provider was temporarily unavailable or reported the order not cancelled, and the retry G-05 requires after a refund call got no answer. |
| SG-02 | Store staff work every follow-up task the order system holds, completing the refund or settling the cancellation by hand. | Every failure row that ends in CO-A4. |
| SG-03 | The order system makes follow-up tasks idempotent per order number and reason: a repeated handoff call with the same order number and reason returns the same task id and never creates a second task. | A retry after a handoff call got no answer. |
| SG-04 | The order system makes cancellation idempotent: cancelling an order that is already cancelled returns it cancelled and changes nothing. | The retry G-05 requires after a cancellation call got no answer, including when the first call took effect late. |
