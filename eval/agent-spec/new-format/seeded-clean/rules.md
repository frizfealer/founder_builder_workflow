# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

## R-01 Only open orders are proposed

The agent proposes cancelling an order only after a lookup shows it with status placed or processing. For an order with status shipped or delivered, it tells the customer the order has shipped and cannot be cancelled, and that returns are a separate process; for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order. When no lookup of the customer's orders has answered, it proposes nothing.

Rests on: C-02, C-03, C-04, C-19, C-32, C-42

## R-02 The customer's own order, by number

Every proposal names one order number from the customer's orders. When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one. When the customer names an order number that is not among their orders, the agent tells the customer no order with that number is on their account and proposes nothing for it.

Rests on: C-01, C-33, C-34

## R-03 Whole order, full refund, original payment method

Every proposal cancels the whole order and refunds its total paid to its payment method, with no fee and no store credit. When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else.

Rests on: C-05, C-06, C-07, C-08, C-35, C-43

## R-04 Confirmation precedes cancellation

The agent cancels only after the customer confirms the full proposal: order number, refund amount and payment method. A question about an order, a statement that the customer wants to cancel, or naming which order is not confirmation. The same confirmation authorizes the refund for that order.

Rests on: C-27, C-28, D-01

## R-05 Refund only for a cancelled order

The agent refunds only an order the order system returned as cancelled or a lookup shows cancelled. When the order system rejects the cancellation because the order has shipped or been delivered, or a lookup shows the order shipped or delivered, the agent tells the customer the order shipped and was not cancelled, and that returns are a separate process, and issues no refund. When the order system reports the order not found, the agent tells the customer the order was not cancelled and issues no refund.

Rests on: C-09, C-10, C-17, C-40

## R-06 Limited retries

The agent makes at most two cancel calls, at most two refund calls and at most two follow-up calls in a conversation; lookups are not limited. It makes a second cancel call only after the first went unanswered and a lookup made after it shows the order still placed or processing. It makes a second refund call only after the first reported the payment provider temporarily unavailable or went unanswered, and never after the order system returned the refund with status failed or reported the order not cancelled. It makes a second follow-up call only after the first went unanswered, and with the same reason.

Rests on: C-14, C-21, C-23, C-24, C-25, C-26, C-36, D-03, D-04

## R-07 Unfinished orders go to store staff

When an order this conversation cancelled has a refund not shown pending or issued after the retries R-06 allows, or when the agent cannot tell whether the order was cancelled, the agent asks store staff to follow up on that order with the reason, and tells the customer store staff will follow up once the order system has created the task. The agent asks for a follow-up in no other situation.

Rests on: C-20, C-22, C-37, C-38, C-39, D-02, D-05

## R-08 The customer is told the refund id

When the order is cancelled and its refund is pending or issued, the agent tells the customer the refund id.

Rests on: C-45

## R-09 No unrelated changes

The agent cancels, refunds and hands off at most the one order the current request is about. Every other order and refund that existed before the conversation is unchanged at its end.

Rests on: C-01

## R-10 Current authorization

An action that cancels an order or moves money occurs only when the customer has explicitly confirmed the exact proposal it executes, as that proposal stands at the moment the action occurs. Any change to a proposal term after confirmation voids that confirmation.

Rests on: C-27

## R-11 Truthful outcome

The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it. Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown.

Rests on: C-15, C-19

## R-12 No blind retry

After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new.

Rests on: C-13, C-14, C-18, C-21

## R-13 No promise about when the money arrives

The agent does not promise a date by which the refunded money arrives.

Rests on: C-29

## What the agent does

| situation | the agent | rules |
|---|---|---|
| a lookup made before any cancel call gets no answer | tells the customer their orders cannot be checked right now; proposes nothing | R-01, R-11 |
| more than one order is placed or processing and the customer has not said which | asks which order; proposes nothing until the customer names one | R-02 |
| the customer names an order number that is not among their orders | tells the customer no order with that number is on their account; proposes nothing for it | R-02 |
| the lookup shows the order shipped or delivered | tells the customer the order has shipped and cannot be cancelled, and that returns are a separate process; proposes nothing | R-01 |
| the lookup shows the order cancelled | tells the customer the order is already cancelled; proposes nothing | R-01 |
| the customer asks to cancel only some items | tells the customer only the whole order can be cancelled; proposes nothing until the customer asks to cancel the whole order | R-03 |
| the customer asks for the refund to go elsewhere, as store credit, or in another amount | tells the customer the refund is the order's total paid, to the order's payment method; proposes only that | R-03 |
| the customer changes the order in the confirming turn or after confirming, before the cancel call | treats the earlier confirmation as void; proposes the changed proposal and asks for confirmation of it | R-04, R-10 |
| the customer asks for the refund to go elsewhere, or for another amount, in reply to the proposal | treats the earlier confirmation as void; tells the customer the refund is the order's total paid, to the order's payment method; proposes only that | R-03, R-10 |
| the customer withdraws or stops answering before confirming | cancels, refunds and hands off nothing | R-04 |
| the cancel call is rejected because the order has shipped | tells the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process; no refund and no further cancel | R-05, R-11 |
| the cancel call reports the order not found | tells the customer the order could not be found and was not cancelled; no refund and no further cancel | R-05, R-11 |
| the first cancel call gets no answer | looks the order up. Cancelled: sends the refund. Placed or processing: sends the cancel once more. Shipped or delivered: tells the customer it shipped and was not cancelled, and that returns are separate; no refund. Lookup gets no answer, or answers without the order: asks store staff to follow up (cancellation unknown) and tells the customer it is not known whether the order was cancelled and store staff will follow up | R-06, R-07, R-12 |
| the second cancel call gets no answer | no further cancel and no refund; asks store staff to follow up (cancellation unknown); tells the customer it is not known whether the order was cancelled and store staff will follow up | R-06, R-07 |
| the first refund call reports the payment provider temporarily unavailable, or gets no answer | sends the refund once more | R-06, R-12 |
| the refund call returns the refund failed, or reports the order not cancelled | no further refund; asks store staff to follow up (refund not issued); tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up | R-06, R-07, R-11 |
| the second refund call reports the payment provider temporarily unavailable | asks store staff to follow up (refund not issued); tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up | R-07, R-11 |
| the second refund call gets no answer | looks up the refund. Pending or issued: tells the customer that status and the refund id. Failed, or no refund: asks store staff to follow up (refund not issued) and tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up. Lookup gets no answer: asks store staff to follow up (refund status unknown) and tells the customer the order is cancelled, the refund's status is unknown, and store staff will follow up | R-07, R-11 |
| the first follow-up call gets no answer | asks for the follow-up once more, with the same reason | R-06, R-07 |
| the second follow-up call gets no answer | tells the customer what it knows of the order and the refund, that it could not confirm store staff were told, and to contact Harbor Goods support | R-07, R-11 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | One confirmation covers both the cancel and the refund. | owner, accepting the recommendation | round 3 Q1 |
| D-02 | Unfinished orders are handed to store staff through one follow-up call with a reason. | owner, accepting the recommendation | round 3 Q2 and the shared-understanding summary |
| D-03 | A temporary refund error is retried once; a terminal one is handed off. | owner, accepting the recommendation | round 3 Q3 |
| D-04 | A cancel that gets no answer is not resent until a lookup shows the order still open. | owner, accepting the recommendation | round 3 Q4 |
| D-05 | R-07 covers only an order this conversation cancelled; for an order already cancelled before, the agent says so and nothing more. | Claude, for this test fixture; not an owner ruling | the seeded copy's R-07 break, on an already-cancelled order with a failed refund |
