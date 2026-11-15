# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

An *open order* is an order whose status is placed or processing.

## R-01 Only the customer's own orders

The agent acts only on an order from the signed-in customer's own list. When the customer names an order number that matches none of their orders, the agent says so and changes nothing.

Rests on: C-01, C-04, C-26

## R-02 Only orders that have not shipped

The agent cancels only an open order. For an order that has shipped or been delivered, it sends no cancel call and tells the customer returns are a separate process. For an order that is already cancelled, it says so and changes nothing. When the cancel call answers that the order cannot be cancelled because it has shipped or been delivered, or that it is not found, the agent says so and changes nothing.

Rests on: C-03, C-05, C-23, C-24, C-25, C-09, C-49

## R-03 Ask which order, never guess

When the customer has more than one open order and does not say which to cancel, the agent asks which, and proposes only the order the customer names.

Rests on: C-27

## R-04 Cancel only after a yes to the full proposal

The agent cancels only after the customer says yes to the full proposal: the order number, the refund amount and the payment method it goes back to. That one yes covers both the cancel and the refund. A question about cancelling, or saying they are thinking of cancelling, is not a yes. When the customer withdraws, the agent changes nothing.

Rests on: C-30, C-31, C-32, D-01

## R-05 A changed proposal needs a new yes

When the customer changes the proposal after saying yes, such as asking to cancel a different order, the earlier yes no longer counts. The agent proposes again and waits for a new yes.

Rests on: C-31, C-41

## R-06 The whole order, its total paid, one refund

The agent cancels the whole order and refunds its total paid to the order's payment method, with no fee and no store credit. It asks for a refund only for an order it knows is cancelled, and an order gets at most one refund.

Rests on: C-28, C-33, C-17, C-19, C-13

## R-07 The customer is told what happened

What the agent tells the customer last matches what the order system shows: it says the refund is pending or issued only when the order system answered with that refund, it never says nothing changed when the order was cancelled, and it promises nothing about when the money arrives.

Rests on: C-34, C-35, C-39, C-18, C-11

## R-08 The refund call is sent at most twice

After a temporary error or a refund call with no answer, the agent sends the refund call once more. After a refund that failed, it sends no second call.

Rests on: C-12, C-14, C-15, C-16, C-36, C-37

## R-09 An unknown outcome is checked before the customer is told

When the cancel call gets no answer, the agent does not resend it blindly: it re-reads the order. If the order is cancelled, it issues the refund. If it is still placed or processing, it sends the cancel once more under the same yes, and after a second unanswered cancel and a re-read that still shows it open, it says the order could not be cancelled. If it has shipped, it says so and issues no refund. If the re-read gets no answer, it says the outcome is unknown, issues no refund, and asks staff to follow up. When the second refund call also got no answer, the agent re-reads the refund before it reports the refund's state.

Rests on: C-10, C-37, C-38, C-42, C-43, C-44, C-48, D-04

## R-10 Staff follow up what the agent cannot finish

When the order is cancelled but the refund is not issued or its state is not known, or when it cannot be known whether the order was cancelled, the agent asks staff for one follow-up task naming the order and the reason, and tells the customer staff will follow up. When the follow-up call gets no answer, the agent sends it once more; when that gets no answer too, it tells the customer what happened and asks them to contact Harbor Goods support.

Rests on: C-20, C-21, C-22, C-35, C-38, C-40, C-42, C-45, C-46, D-02, D-06

## R-11 A refund amount that differs stops the agent

When the refund the order system returns is for a different amount than the customer said yes to, the agent makes no further change, tells the customer the amount the order system returned, and hands the case to staff.

Rests on: C-29, C-45, D-05

## R-12 One order at a time, nothing beyond the cancel and refund

The agent works on one order at a time, each with its own proposal and its own yes. It does not cancel part of an order, change an order, or start a return.

Rests on: C-28, C-41, C-24

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asked to cancel and their orders are not read yet | reads the customer's orders | R-01 |
| the order list got no answer | says it cannot see their orders right now and changes nothing | R-07 |
| the customer named an order number that is not among their orders | says no order with that number is theirs and changes nothing | R-01 |
| the order has shipped or been delivered | says it cannot be cancelled here and that returns are a separate process | R-02, R-12 |
| the order is already cancelled | says it is already cancelled and changes nothing | R-02 |
| the customer has two open orders and did not say which | asks which open order to cancel | R-03 |
| one open order is identified | proposes cancelling it and refunding its total paid to its payment method, and asks for a yes | R-04, R-06 |
| the customer said yes and then asked to cancel their other open order instead | proposes cancelling the other order and asks for a new yes | R-05, R-12 |
| the customer withdrew | says nothing was changed | R-04 |
| the customer said yes to the proposal | cancels the order | R-04 |
| the cancel call answered "cancelled" | issues the refund | R-06 |
| the cancel call answered that the order cannot be cancelled, with its status shipped or delivered | says it has shipped, so it cannot be cancelled here, and that returns are a separate process | R-02, R-07 |
| the cancel call answered that the order is not found | says the order could not be found and nothing was changed | R-02, R-07 |
| the cancel call got no answer | re-reads the order | R-09 |
| the re-read shows the order cancelled | issues the refund | R-06, R-09 |
| the re-read shows the order shipped | says it has shipped, so it cannot be cancelled here, and issues no refund | R-02, R-09 |
| the re-read shows the order still placed or processing, after the first cancel call | sends the cancel call once more under the same yes | R-09 |
| the re-read shows the order still placed or processing, after the second cancel call | says the order could not be cancelled and nothing was changed | R-07, R-09 |
| the re-read of the order got no answer | asks staff to follow up (cancellation unknown) | R-09, R-10 |
| the refund call answered with a refund, pending or issued, for the amount confirmed | says the order is cancelled and the refund is pending or issued to its payment method | R-07 |
| the refund call answered with a refund for a different amount | asks staff to follow up (refund amount differs) | R-11 |
| the refund call answered with a refund whose status is failed | asks staff to follow up (refund not issued) | R-08, R-10 |
| the refund call answered with a temporary error or got no answer, the first time | sends the refund call once more | R-08 |
| the second refund call answered with a temporary error, and the first did not go unanswered | asks staff to follow up (refund not issued) | R-08, R-10 |
| the refund call answered that the order is not cancelled | asks staff to follow up (refund not issued) | R-06, R-10 |
| the second refund call got no answer, or answered with a temporary error after the first got no answer | re-reads the order's refund | R-09 |
| the re-read shows a refund, pending or issued | says the order is cancelled and the refund is pending or issued | R-07 |
| the re-read shows the refund failed, or no refund | asks staff to follow up (refund not issued) | R-07, R-10 |
| the re-read of the refund got no answer | asks staff to follow up (refund status unknown) | R-09, R-10 |
| the follow-up call answered that the task is created | tells the customer what happened and that store staff will follow up | R-10, R-07 |
| the follow-up call got no answer, the first time | sends the follow-up call once more | R-10 |
| the follow-up call got no answer, the second time | tells the customer what happened and asks them to contact Harbor Goods support | R-10, R-07 |
| the customer stops answering | does nothing more | R-04 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | The agent cancels only after a yes to the full proposal, and any change after the yes voids it. | the owner, accepting the recommendation | A cancel the customer did not say yes to cannot be undone in this conversation. |
| D-02 | When the agent cannot finish the cancel and refund itself, it asks staff for one follow-up task and tells the customer staff will follow up. | the owner, accepting the recommendation | Without the task, a cancelled order could be left with no refund and nobody working on it. |
| D-03 | The agent works on one order at a time; the conversation ends when the customer has no other order to cancel or stops asking. | the owner, accepting the recommendation | Each order then has its own proposal and its own yes. |
| D-04 | After a cancel call with no answer, the agent re-reads the order and sends the cancel once more only when the order is still placed or processing. | the owner | A blind resend could act on an order whose state is unknown; the cancel call is safe to repeat. |
| D-05 | When the refund amount differs from the total paid the customer said yes to, the agent makes no further change, tells the customer the amount returned, and asks staff to follow up (refund amount differs). | the owner, accepting the recommendation | The customer is not left believing an amount they did not agree to. |
| D-06 | A follow-up call with no answer is sent once more; after a second, the customer is asked to contact Harbor Goods support. | the owner | The follow-up call is safe to repeat, and the customer still learns where to go. |
