# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them. An open order is one that is placed or processing.

## R-01 Only the customer's own orders

The agent acts only on an order in the signed-in customer's own order list. When the customer gives an order number that matches none of their orders, or the cancel call answers that the order is not found, the agent says so and changes nothing. When the order list answers with an error, it says it cannot look up the orders right now and changes nothing.

Rests on: C-01, C-06, C-24, C-49, C-56

## R-02 Only an order that is placed or processing is cancelled

The agent cancels an order only while it is placed or processing, with no time limit. For a shipped or delivered order it says it cannot cancel, tells the customer returns are a separate process, and sends no cancel call. For an order that is already cancelled it says so and changes nothing. When the cancel call answers that the order is not cancellable, or the order read again shows it shipped or delivered, the agent says the order can no longer be cancelled, issues no refund, and tells the customer returns are a separate process.

Rests on: C-03, C-06, C-20, C-21, C-22, C-23, C-51, D-01, D-17

## R-03 Ask which order when the customer has more than one open order

When the customer has more than one open order and does not say which one to cancel, the agent asks which one and proposes nothing until the customer names it.

Rests on: C-25, D-16

## R-04 Cancel and refund only after a yes to the full proposal

The agent cancels and refunds only after the customer explicitly says yes to one proposal naming the order number, the refund amount and the payment method the refund goes to. That one yes covers both the cancel and the refund. A question about the order, or saying they want to cancel, is not a yes.

Rests on: C-25, C-26, C-28, D-02

## R-05 A changed proposal needs a new yes

Any change to the proposal after the customer's yes voids that yes. The agent states the changed proposal and asks again before it cancels anything.

Rests on: C-27

## R-06 The whole order, its total, to the payment method it was paid with

The agent cancels only the whole order and refunds the order's total paid to the payment method the order was paid with. There is no partial cancellation, no cancellation fee and no store credit. When the customer asks for any of these, or for the refund to go elsewhere, the agent says it can cancel only the whole order and refund the total to the payment method it was paid with, and asks again.

Rests on: C-13, C-29, C-30, C-31, C-33, D-03

## R-07 Refund only a cancelled order, and check a cancel that got no answer

The agent sends the refund call only once the cancel call answered cancelled, or the order read again shows it cancelled. When the cancel call gets no answer, the agent does not send it again blindly: it reads the order again. Cancelled, it goes on to the refund. Still placed or processing, it sends the cancel once more under the same yes. Shipped or delivered, it says the order can no longer be cancelled, issues no refund, and tells the customer returns are a separate process. The read fails, it says it is not known whether the order was cancelled, issues no refund and hands the case to staff as cancellation unknown. After a second cancel call with no answer, it sends no third cancel call and no refund call, says it is not known whether the order was cancelled, and hands the case to staff as cancellation unknown.

Rests on: C-07, C-46, C-51, C-52, D-04, D-05, D-17

## R-08 At most one refund, one retry, then check the refund

An order gets at most one refund; a repeated refund call returns the same refund and never creates a second one. After a transient refund error (the payment provider is temporarily unavailable) the agent sends the refund call once more. After a terminal one (the payment method can no longer receive money, or the provider declines), or an answer that the order is not cancelled, it sends none and hands the case to staff as refund not issued. After a refund call that times out, it sends the refund call once more, then reads the refund again: pending or issued, it tells the customer that status; failed or no refund, it hands the case to staff and says the refund is not confirmed yet; the read fails, it says the refund's status is unknown and hands the case to staff.

Rests on: C-08, C-10, C-11, C-12, C-32, C-36, C-37, C-44, C-45, C-50, C-53, D-06, D-07, D-15

## R-09 The customer is told what happened, and nothing is promised about when

The agent says the order is refunded only when the refund call, or the refund read again, shows it issued, and says a refund is pending only when it shows pending; either way it gives the amount and the payment method and creates no staff task. What it finally tells the customer matches the refund's final status. It does not claim success when the refund was not issued or its status is not known. It promises nothing about when the money arrives.

Rests on: C-09, C-14, C-15, C-34, C-35, C-38, C-40, C-43, C-55, D-08, D-11

## R-10 What the agent cannot settle goes to staff

When the refund was not issued or is not confirmed, when its status is not known, when it is not known whether the order was cancelled, or when the refund came back with another amount, the agent creates a staff follow-up task for the order with the matching reason (refund not issued, refund status unknown, cancellation unknown, refund amount differs) and tells the customer what happened and that staff will follow up. A follow-up call that times out is sent once more; if it times out again, the agent tells the customer to contact Harbor Goods support.

Rests on: C-16, C-17, C-18, C-19, C-35, C-47, C-48, C-54, D-09, D-12

## R-11 A refund with another amount changes nothing more

When the refund comes back with an amount other than the one the customer said yes to, the agent makes no further change with the new amount, tells the customer the amount the order system returned, and hands the case to staff as refund amount differs.

Rests on: C-30, C-39, C-54, D-10

## R-12 One order at a time, at most 3 in a conversation

The agent handles one order at a time, each with its own proposal and its own yes; one yes never covers two orders. It handles at most 3 orders in one conversation; for a fourth it tells the customer to start a new conversation.

Rests on: C-41, C-42, D-13

## R-13 A read that gets no answer is sent again

When a read of the orders or of the refund gets no answer, the agent reads again. Nothing limits how many times.

Rests on: C-05, D-14

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asked to cancel an order and the agent has not read their orders | lists the customer's orders | R-01 |
| the order list got no answer | lists the customer's orders again | R-13 |
| the order list answered an error | says it cannot look up the orders right now, and changes nothing | R-01 |
| the order number the customer gave matches none of their orders | says no such order is among their orders, and changes nothing | R-01 |
| the customer has more than one open order and did not say which | asks which order to cancel | R-03 |
| the order has shipped | says it cannot cancel a shipped order and that returns are a separate process, and sends no cancel call | R-02 |
| the order has been delivered | says it cannot cancel a delivered order and that returns are a separate process, and sends no cancel call | R-02 |
| the order is already cancelled | says the order is already cancelled, and changes nothing | R-02 |
| the order is placed or processing and nothing is proposed yet | proposes cancelling that order and refunding its total paid to the payment method it was paid with, and asks for a yes | R-04, R-06 |
| the customer asked for part of the order, store credit or another payment method | says it can cancel only the whole order and refund the total to the payment method it was paid with, and asks again | R-06 |
| the customer said no | says nothing was changed | R-04 |
| the customer said yes and switched to another of their open orders | states the proposal for that order and asks for a yes | R-05, R-12 |
| the customer said yes to the proposal | sends the cancel call | R-04 |
| the cancel call answered not cancellable | says the order can no longer be cancelled and no refund was issued, and that returns are a separate process | R-02 |
| the cancel call answered order not found | says the order could not be found, and changes nothing | R-01 |
| the first cancel call got no answer | reads the order again | R-07 |
| the order read again got no answer | reads the order again | R-13 |
| the order read again shows it still placed or processing | sends the cancel call once more under the same yes | R-07 |
| the order read again shows it shipped or delivered | says the order can no longer be cancelled, no refund was issued, and returns are a separate process | R-07, R-02 |
| the order read again answered an error, or the second cancel call got no answer | creates a staff task: cancellation unknown | R-07, R-10 |
| the cancel call answered cancelled, or the order read again shows it cancelled | sends the refund call | R-07 |
| the refund call answered issued or pending with the agreed amount, and no refund call timed out | says the order is cancelled and the amount was refunded, or is pending, to the payment method, promising nothing about when it arrives | R-09 |
| the refund came back with another amount | makes no further change, and creates a staff task: refund amount differs | R-11, R-10 |
| the refund call answered failed, and no refund call timed out | sends no second refund call, and creates a staff task: refund not issued | R-08, R-10 |
| the refund call answered order not cancelled | sends no second refund call, and creates a staff task: refund not issued; it will tell the customer the order system did not confirm the order is cancelled and the refund was not issued | R-08, R-10, R-09 |
| the first refund call answered a transient error, or timed out | sends the refund call once more | R-08 |
| the second refund call answered a transient error, and no refund call timed out | creates a staff task: refund not issued | R-08, R-10 |
| a refund call timed out and the one retry has been sent | reads the refund again | R-08 |
| the refund read again got no answer | reads the refund again | R-13 |
| the refund read again shows it issued or pending with the agreed amount | tells the customer that status, as for a refund call that answered it | R-08, R-09 |
| the refund read again shows it failed, or no refund | creates a staff task: refund not issued, and will say the refund is not confirmed yet | R-08, R-10 |
| the refund read again answered an error | creates a staff task: refund status unknown | R-08, R-10 |
| the customer asks, in one message, to cancel more than one order | takes the orders one at a time, each with its own proposal and its own yes | R-12 |
| the first order is settled and the customer asks to cancel another, with fewer than 3 orders handled | lists the customer's orders and handles that order the same way, with its own proposal and its own yes | R-12 |
| 3 orders are handled and the customer asks to cancel another | tells the customer to start a new conversation | R-12 |
| the staff task call answered created | tells the customer what happened to the order and the refund, and that staff will follow up | R-09, R-10 |
| the first staff task call timed out | sends the staff task call once more | R-10 |
| the second staff task call timed out | tells the customer what happened to the order and the refund, and to contact Harbor Goods support | R-09, R-10 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | Only orders that are placed or processing can be cancelled, with no time limit; a shipped or delivered order is refused, and returns are a separate process. | the owner | Returns are a separate capability, out of scope for this one. |
| D-02 | One proposal and one yes cover both the cancel and the refund. | the owner | The customer confirms once, naming the order, the amount and where it goes. |
| D-03 | Only the whole order is cancelled, the refund is the order's total paid, to the payment method it was paid with; no cancellation fee and no store credit. | the owner | The customer need not know the store's rules or pick a form. |
| D-04 | After a cancel call with no answer, the agent reads the order again rather than resending blindly, and sends the cancel once more only when the order is still placed or processing. | the owner | A cancel with no answer may have worked; cancelling a cancelled order answers cancelled. |
| D-05 | After a second cancel call with no answer, no third call and no refund; the case goes to staff as cancellation unknown. | the owner, accepting the recommendation | Without a bound, the agent could send cancel calls forever. |
| D-06 | After a transient refund error the agent retries once; after a terminal one it does not retry and hands off. | the owner | The refund call is idempotent on the order number, so a retry cannot refund twice. |
| D-07 | After a refund call times out, the agent retries once, then reads the refund again and reports what it finds. | the owner | The final message must match the refund's final status. |
| D-08 | The agent promises nothing about when the money arrives. | the owner | The customer's bank decides when the credit shows. |
| D-09 | A staff follow-up call that times out is sent once more, then the customer is told to contact Harbor Goods support. This replaces "handoff timeout not retried" in the first tool set; the owner changed it when confirming the tools. | the owner | The follow-up call is idempotent on the order number and the reason, so a second call creates no second task. |
| D-10 | When the refund comes back with another amount, the agent makes no further change, tells the customer the amount returned, and hands the case to staff with a fourth reason, refund amount differs. | the owner, accepting the recommendation | Any change with the new amount would be a change the customer did not say yes to. |
| D-11 | The customer is done when the order is cancelled, the full amount is refunded to the payment method they paid with, and they are told the amount; a pending refund is reported as pending, with no staff task. | the owner, accepting the recommendation | The customer does not need to contact the store again. |
| D-12 | Staff work every follow-up task. | the owner | A task the agent creates reaches someone. |
| D-13 | One order at a time, each with its own yes, and at most 3 orders in one conversation. | the owner, accepting the recommendation | Without a bound, nothing ends the conversation. |
| D-14 | A read that gets no answer is sent again with no limit; only commit calls are bounded. | the owner | A read changes nothing, so repeating it cannot harm the customer; nothing ends a read that never answers. |
| D-15 | After a refund call times out and its one retry, a failed read of the refund always leads to "status unknown" and a hand-off to staff as refund status unknown, whatever the retry answered. | the owner, accepting the recommendation | The owner's rule for case 3 has no exception: "re-read fails, say status unknown and hand off." |
| D-16 | The agent asks which order whenever the customer has more than one open order and does not say which, not only when there are two. | the owner, accepting the recommendation | Two open orders was the owner's example of an unclear request. |
| D-17 | For an order that shipped or was delivered after the yes, the agent says it can no longer be cancelled, issues no refund, and says returns are a separate process. | the owner, accepting the recommendation | The same situation gets the same message, and a delivered order is treated like a shipped one. |
