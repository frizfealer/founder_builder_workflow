# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

## R-01 Only the customer's own orders

The agent reads and acts on only the signed-in customer's orders. When an order number matches none of them, it says so and changes nothing. When the order list call times out, it sends it again; the owner set no limit on this.

Rests on: C-01, C-04, C-14

## R-02 Only orders that have not shipped

The agent cancels an order only while it is placed or processing. When the order has shipped or been delivered, it sends no cancel call and tells the customer returns are a separate process. When the order is already cancelled, it says so and changes nothing.

Rests on: C-06, C-09, C-10, C-11, C-13

## R-03 Whole orders only

The agent cancels only a whole order. When the customer asks to cancel some items, it says only the whole order can be cancelled.

Rests on: C-12

## R-04 The order is clear before the proposal

When the customer could mean more than one order, the agent asks which one before it proposes anything. The proposal names the order number.

Rests on: C-37

## R-05 Cancel only after a yes to the full proposal

The agent cancels an order only after the customer says yes to one proposal naming the order, the refund amount and the payment method the refund goes back to. That one yes covers both the cancellation and the refund. A question, or saying they want to cancel, is not a yes. Any change after the yes voids it, and the agent asks again.

Rests on: C-35, C-36, C-42

## R-06 One full refund, to the payment method paid with

The refund is the order's total paid, back to the payment method the order was paid with, with no fee and no store credit. An order gets at most one refund: once the order system has returned a refund, the agent sends no further refund call.

Rests on: C-19, C-21, C-23, C-24, C-28, C-29

## R-07 No refund without a cancellation

The agent sends the refund call only after the cancel call answered cancelled. When the cancel call answers that the order has shipped since it was read, the agent says so, and sends no refund call.

Rests on: C-15, C-16

## R-08 A cancellation with no answer

When the cancel call gets no answer, the agent does not simply send it again: it reads the order again. When the order shows cancelled, it goes on to the refund. When it is still placed or processing, the agent sends the cancel call once more under the same yes. When it has shipped or been delivered, the agent says so and makes no refund. When the read fails, the agent says the outcome is unknown, makes no refund, and asks staff to follow up with the reason cancellation unknown. When the second cancel call also gets no answer and the order still shows placed or processing, the agent sends no third cancel call and no refund call, asks staff to follow up with the reason cancellation unknown, and tells the customer the order is not cancelled yet and store staff will follow up.

Rests on: C-17, C-18, C-38, C-46, C-51, C-57

## R-09 At most two refund calls

After a passing error or no answer, the agent sends the refund call once more. After a lasting error, which returns a refund with status failed, it sends none.

Rests on: C-29, C-30, C-31, C-32, C-54, C-56

## R-10 A refund not made, or not known, goes to staff

When the order is cancelled but the refund was not issued (a lasting error, or a passing error twice), the agent asks staff to follow up with the reason refund not issued and tells the customer the refund was not issued. When the refund call answers order not cancelled, the agent sends no further call, asks staff to follow up with the reason refund not issued, and tells the customer the refund is not confirmed yet. When a refund call got no answer, the agent sends it once more and then reads the refund again: pending or issued, it reports that status; failed or no refund, it asks staff to follow up with the reason refund not issued and says the refund is not confirmed yet; the read fails, it asks staff to follow up with the reason refund status unknown and says the status is unknown. When the staff follow-up call times out, the agent sends it once more; when that also times out, it tells the customer to contact Harbor Goods support.

Rests on: C-31, C-33, C-38, C-39, C-40, C-41, C-44, C-48, C-50, C-52, C-53, C-55, C-57

## R-11 A refund amount that differs

When the refund call returns an amount that differs from the amount the customer confirmed, the agent makes no further change with it, tells the customer the amount the refund call returned, and hands the case to staff with the reason refund status unknown.

Rests on: C-19, C-20, C-47

## R-12 The customer is told what happened

The agent says the order is cancelled only when a cancel call answered cancelled or the order read again shows it cancelled, and states the refund as the order system shows it: its amount, the payment method and its status. It promises nothing about when the money arrives. When it cannot tell, it says so.

Rests on: C-25, C-26, C-27, C-34, C-49

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asks to cancel an order | reads the customer's orders | R-01 |
| the order list call timed out | sends it again; the owner set no limit | R-01 |
| the order number matches none of the customer's orders | says so, and changes nothing | R-01 |
| the customer asked to cancel some items of an order | says only the whole order can be cancelled | R-03 |
| the order has shipped or been delivered | says it cannot be cancelled and that returns are a separate process, and sends no cancel call | R-02 |
| the order is already cancelled | says so, and changes nothing | R-02 |
| the customer has two orders that have not shipped and did not say which | lists them and asks which one | R-04 |
| the order is clear, and it is placed or processing | proposes: cancel this order and refund its total paid to the payment method it was paid with, and asks for a yes | R-04, R-05, R-06 |
| the customer said yes, but for their other order | proposes the other order and asks for a new yes | R-05 |
| the customer said no | says nothing was changed | R-05 |
| the customer said yes to the proposal | cancels the order | R-05 |
| the cancel call answered that the order shipped since it was read | says the order shipped before it could be cancelled, so nothing is cancelled and no refund is made | R-07, R-12 |
| the cancel call answered order not found | says the order was not found, and changes nothing | R-12 |
| the cancel call got no answer | reads the order again | R-08 |
| the order read again shows it cancelled | refunds the order | R-07, R-08 |
| the order read again shows it still placed or processing, after the first cancel call | sends the cancel call again | R-08 |
| the order read again shows it still placed or processing, after the second cancel call | asks staff to follow up: cancellation unknown; will tell the customer the order is not cancelled yet | R-08 |
| the order read again shows it shipped or delivered | says the order shipped before it could be cancelled, so nothing is cancelled and no refund is made | R-08, R-12 |
| the order read again failed | asks staff to follow up: cancellation unknown; will tell the customer the outcome is unknown and no refund was made | R-08 |
| the cancel call answered cancelled | refunds the order | R-06, R-07 |
| the refund call returned the refund, issued or pending, for the confirmed amount | says the order is cancelled and gives the refund's amount, payment method and status, with no promise of when the money arrives | R-12 |
| the refund call returned a refund for a different amount | asks staff to follow up: refund status unknown; will tell the customer the amount the refund call returned | R-11 |
| the refund call returned a refund with status failed | asks staff to follow up: refund not issued; will tell the customer the refund was not issued | R-09, R-10 |
| the refund call answered order not cancelled | asks staff to follow up: refund not issued; will tell the customer the refund is not confirmed yet | R-10 |
| the refund call answered a passing error or got no answer, the first time | sends the refund call again | R-09 |
| the second refund call answered a passing error, and no refund call went unanswered | asks staff to follow up: refund not issued; will tell the customer the refund was not issued | R-09, R-10 |
| a refund call went unanswered, and the second refund call has answered | reads the refund again | R-10 |
| the refund read again shows the refund, issued or pending | says the order is cancelled and gives the refund's amount, payment method and status | R-10, R-12 |
| the refund read again shows a refund for a different amount | asks staff to follow up: refund status unknown; will tell the customer the amount the refund call returned | R-11 |
| the refund read again shows no refund, or a failed one | asks staff to follow up: refund not issued; will tell the customer the refund is not confirmed yet | R-10 |
| the refund read again failed | asks staff to follow up: refund status unknown; will tell the customer the refund status is unknown, or the amount the second refund call returned when it differed | R-10, R-11 |
| the staff follow-up call answered created | tells the customer what it knows and that store staff will follow up | R-10, R-12 |
| the staff follow-up call got no answer, the first time | sends the staff follow-up call again | R-10 |
| the staff follow-up call got no answer, the second time | tells the customer what it knows and to contact Harbor Goods support | R-10, R-12 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | When the refund call returns an amount that differs from the confirmed one, the agent makes no further change, tells the customer the amount returned, and hands the case to staff. | the owner, accepting the recommendation | The customer said yes to one amount; staff settle any other. |
| D-02 | Each order is handled on its own, with its own proposal and its own yes; nothing else bounds how many orders one conversation cancels. | the owner, accepting the recommendation | A conversation ends when no order is left that can be cancelled, or when the customer stops asking. |
| D-03 | A cancel call with no answer may have cancelled the order, and the order list shows a refund as soon as the refund call made it. | the owner, accepting the recommendation | The agent never refunds an order whose cancellation it has not seen, and a refund read that shows no refund means none was made. |
| D-04 | After the second cancel call gets no answer and the order still shows placed or processing, the agent stops, makes no refund, and asks staff to follow up with the reason cancellation unknown. | the owner, accepting the recommendation | The cancel call is a change, so it is bounded at two. |
| D-05 | A refund amount that differs goes to staff with the reason refund status unknown. | the owner, accepting the recommendation | With refund not issued, staff could issue a second refund on top of the one made. |
| D-06 | When the refund call answers order not cancelled, the agent stops, asks staff to follow up with the reason refund not issued, and says the refund is not confirmed yet. | the owner, accepting the recommendation | The order system's two answers disagree; staff settle it. |
