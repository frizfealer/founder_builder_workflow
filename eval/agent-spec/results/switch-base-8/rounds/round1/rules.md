# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

An *open order* is an order whose status is placed or processing: one the agent may cancel. A *read* is a call that only looks at the customer's orders and changes nothing.

## R-01 Only the customer's own orders

The agent acts only on an order in the signed-in customer's order list. When an order number matches none of the customer's orders, the agent says so and changes nothing.

Rests on: C-01, C-33

## R-02 The order is named before the proposal

When the customer has more than one open order and does not say which one, the agent asks which order and proposes nothing until the customer names it. The proposal names the order number.

Rests on: C-34, C-30

## R-03 Only placed or processing orders are cancelled

The agent cancels an order only while its status is placed or processing, with no time limit. Once an order has shipped, or has been delivered, the agent refuses without a cancel call and tells the customer returns are a separate process. For an order that is already cancelled, the agent says so and changes nothing.

Rests on: C-05, C-22, C-23, C-24, C-25

## R-04 Cancel and refund only after a yes to the full proposal

The agent states one proposal: which order is cancelled, the refund amount and the payment method it goes back to. It cancels the order and issues the refund only after the customer explicitly says yes to that proposal; that one yes covers both. A question about an order, or saying they want to cancel, is not a yes.

Rests on: C-30, C-32

## R-05 A changed proposal needs a new yes

When the customer changes any part of the proposal after saying yes, such as naming a different order, the earlier yes no longer counts. The agent states the changed proposal and asks again.

Rests on: C-31

## R-06 The whole order, the total paid, the payment method paid with

The agent cancels whole orders only. The refund is the order's total paid, back to the payment method the customer paid with. There is no cancellation fee and no store credit.

Rests on: C-26, C-27, C-29, C-19

## R-07 No refund unless the order is cancelled

The agent issues the refund only after the order system has answered, or a new read has shown, that the order is cancelled. When the order system rejects the cancel because the order has shipped or been delivered since the agent read it, the agent tells the customer so truthfully and issues no refund. When the cancel call answers that the order was not found, the agent sends no refund call, tells the customer the order could not be cancelled and that nothing was changed, and asks staff to follow up with the reason cancellation unknown.

Rests on: C-09, C-45, C-48, D-12

## R-08 After a cancel timeout, read the order before anything else

When the cancel call times out, the agent sends no blind second cancel call; it reads the order again. When the order is cancelled, it goes on to the refund. When the order is still placed or processing, it sends the cancel once more under the same yes. When the order has shipped, it tells the customer and issues no refund. When the read fails, it tells the customer the outcome is unknown, issues no refund, and asks staff to follow up. When the second cancel call also times out, it sends no further cancel call and no refund call, tells the customer it is not known whether the order was cancelled and that no refund was made, and asks staff to follow up with the reason cancellation unknown.

Rests on: C-10, C-41, C-46, C-47, C-51, D-08, D-13

## R-09 At most one refund per order

An order gets at most one refund. Repeated refund calls for an order return the same refund and never create a second one, so the agent may retry the refund call.

Rests on: C-28, C-14

## R-10 A refund that is not issued goes to staff

When the refund call returns an error, the agent reports it, does not claim the refund was issued, and asks staff to issue it by the store's manual refund process. After an error the order system will not recover from, the agent sends no second refund call. When the refund call answers that the order is not cancelled, the agent sends no second refund call, tells the customer the refund was not issued, and asks staff to follow up with the reason refund not issued.

Rests on: C-11, C-35, C-36, C-49, C-50, C-16, D-14, D-15

## R-11 One retry, and a new read after a timeout

The agent sends at most one second refund call for an order: after a short-lived error or a timeout. After any refund call that timed out, the agent reads the order and its refund again once the retry is used, and reports what that read shows. When that read fails, the agent asks staff to follow up because the refund status is unknown.

Rests on: C-13, C-36, C-37, C-03, D-04

## R-12 The customer is told what happened

The agent's last message matches the final refund status: it says a refund was made only when the order system showed a refund with status pending or issued for the amount the customer said yes to, and gives that status. It says nothing was changed only when it made no change.

Rests on: C-38, C-12, C-21

## R-13 A refund amount that differs goes to staff

When the refund the order system returns, or shows on a new read, has an amount that differs from the amount the customer said yes to, the agent makes no further change with the new amount, tells the customer the amount the order system returned, and asks staff to follow up with the reason refund status unknown.

Rests on: C-27, C-39, C-52, D-06, D-16

## R-14 A staff request is sent at most twice

When a request for staff follow-up times out, the agent sends it once more; that creates no second task. When the second request times out too, the agent tells the customer what happened to the order and the refund, and to contact Harbor Goods support.

Rests on: C-15, C-42, D-10

## R-15 A read that times out is read again

A read that times out may be retried without limit; only calls that change something are bounded. While a read keeps timing out, the agent tells the customer once that it is still checking, and reads again until the read answers, fails, or the customer leaves. When the read of the customer's orders fails with an error at the start of the conversation, the agent changes nothing and tells the customer it cannot see their orders right now.

Rests on: C-08, C-44, C-43, C-53, D-11, D-17, D-18

## R-16 One order at a time

The customer may cancel more than one order in a conversation, one order at a time, each with its own proposal and its own yes. It ends when the customer asks for nothing more or has no open order left.

Rests on: C-40, D-07

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asked to cancel an order, and the agent has not read the order list | reads the customer's order list | R-01 |
| a read timed out for the first time in the conversation | tells the customer it is still checking, and reads again | R-15 |
| a read timed out again | reads again | R-15 |
| the order list read failed with an error | says it cannot see the customer's orders right now and that nothing was changed | R-15 |
| the order number the customer gave matches none of their orders | says no order of theirs has that number and that nothing was changed | R-01 |
| the customer named no order and has more than one open order | asks which order, and proposes nothing | R-02 |
| the customer named no order and has no open order | says none of their orders can be cancelled, gives each order's status, and changes nothing | R-03 |
| the order has shipped or been delivered | says the order has shipped and cannot be cancelled, and that returns are a separate process | R-03 |
| the order is already cancelled | says the order is already cancelled and that nothing was changed | R-03 |
| the order is open and no proposal is waiting | states the proposal: the order number, the refund amount and the payment method, and asks for a yes | R-02, R-04, R-06 |
| the customer said yes and named a different open order | states the changed proposal and asks for a yes again | R-05 |
| a proposal is waiting and the customer names a different order before saying yes | states the proposal for the order the customer named and asks for a yes | R-04, R-16 |
| the customer asks to cancel more than one order, in one message or later in the conversation | takes the orders one at a time: finishes the current order, then states the proposal for the next one and asks for its own yes | R-16 |
| the customer asks to cancel part of an order, or for the refund as store credit or to another payment method | says the store cancels whole orders only and refunds the total paid to the payment method paid with, with no store credit, and states the full proposal | R-06 |
| the customer said no to the proposal | says nothing was changed | R-04, R-12 |
| the customer said yes to the proposal | cancels the order | R-04, R-03 |
| the cancel call answered that the order is cancelled | issues the refund | R-07, R-06 |
| the cancel call answered that the order cannot be cancelled because it has shipped or been delivered | says the order shipped before it could be cancelled, that it was not cancelled and no refund was made, and that returns are a separate process | R-07, R-12 |
| the cancel call answered that the order was not found | asks staff to follow up because it is not known whether the order was cancelled | R-07 |
| the first cancel call timed out | reads the order again | R-08 |
| the new read after a cancel timeout shows the order cancelled | issues the refund | R-08 |
| the new read after a cancel timeout shows the order still placed or processing | sends the cancel once more | R-08 |
| the new read after a cancel timeout shows the order shipped | says the order shipped before it could be cancelled, that it was not cancelled and no refund was made, and that returns are a separate process | R-08 |
| the new read after a cancel timeout failed, or the second cancel call timed out | asks staff to follow up because it is not known whether the order was cancelled | R-08 |
| the refund call returned a refund, pending or issued, for the amount the customer said yes to, and no refund call timed out | says the order is cancelled and the refund was made, with its amount, payment method and status | R-12 |
| the refund call returned a refund for a different amount, and no refund call timed out | asks staff to follow up with the reason refund status unknown, because the refund amount differs | R-13 |
| the refund call returned a failed refund, and no refund call timed out | asks staff to issue the refund by the manual refund process | R-10 |
| the refund call answered that the order is not cancelled, and no refund call timed out | asks staff to follow up because the refund was not issued | R-10 |
| the refund call had a short-lived error or timed out, and no second refund call was sent | sends the refund call again | R-11, R-09 |
| the second refund call had a short-lived error, and no refund call timed out | asks staff to issue the refund by the manual refund process | R-10, R-11 |
| a refund call timed out and the retry is used | reads the order and its refund again | R-11 |
| the new read shows a refund, pending or issued, for the amount the customer said yes to | says the order is cancelled and the refund was made, with its amount, payment method and status | R-11, R-12 |
| the new read shows a refund for a different amount | asks staff to follow up with the reason refund status unknown, because the refund amount differs | R-13 |
| the new read shows a failed refund, or no refund | asks staff to issue the refund by the manual refund process | R-10, R-11 |
| the new read after a refund timeout failed | asks staff to follow up because the refund status is unknown | R-11 |
| the staff request timed out the first time | sends the staff request once more | R-14 |
| the staff task was created | tells the customer what happened to the order and the refund, and that staff will follow up | R-12, R-14 |
| the second staff request timed out | tells the customer what happened to the order and the refund, and to contact Harbor Goods support | R-14 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | Only orders that are placed or processing can be cancelled, with no time limit; a shipped order is refused and the customer is told returns are a separate process. | the owner | Returns are out of scope for this agent. |
| D-02 | Whole orders only, refunded in full to the payment method paid with, with no fee and no store credit. | the owner | The owner's rules for cancellation and refund. |
| D-03 | One proposal naming the order, the refund amount and where it goes, and one yes, authorize both the cancel and the refund; any change voids the yes. | the owner | A cancel and a refund the customer did not agree to cannot be undone in the conversation. |
| D-04 | A refund call is retried once after a short-lived error or a timeout, never after an error the order system will not recover from; after a timeout the agent reads the order again and reports what it finds. | the owner | The final message must match the final refund status. |
| D-05 | A refund that is not issued is handed to staff for the store's manual refund process. | the owner | The agent must not claim success. |
| D-06 | When the refund's amount differs from the amount the customer said yes to, the agent makes no further change, tells the customer the amount returned, and asks staff to follow up. | the owner, accepting the recommendation | The customer said yes to one amount; another amount needs a person. |
| D-07 | The customer may cancel more than one order in one conversation, one at a time, each with its own proposal and yes. | the owner, accepting the recommendation | Each order's cancel and refund rests on its own yes. |
| D-08 | After a cancel timeout the agent reads the order again instead of resending; it cancels once more only when the order is still placed or processing. | the owner | A blind resend could act on an order whose state the agent does not know. |
| D-09 | The tools are: list the customer's orders, cancel an order, issue the refund for an order, and create a staff follow-up task, with the owner's four changes: the cancel call is safe to repeat and has the outcomes in C-45, the refund call can answer that the order is not cancelled, the staff request is safe to repeat and is sent once more after a timeout, and reads may be retried on timeout without limit. | the owner | Every write has one call and every fact the agent needs before it acts has a read. |
| D-10 | A staff request that times out is sent once more; after a second timeout the customer is told to contact Harbor Goods support. | the owner | The staff request creates no second task when repeated. |
| D-11 | A read that times out may be retried without limit. | the owner | Only calls that change something are bounded. |
| D-12 | When the cancel call answers that the order was not found, the agent sends no refund call, says the order could not be cancelled and nothing was changed, and asks staff to follow up. | the owner, accepting the recommendation | The agent cancels only orders in the customer's list, so a person must look at the mismatch. |
| D-13 | When the second cancel call also times out, the agent stops, issues no refund, says the outcome is not known, and asks staff to follow up. | the owner, accepting the recommendation | Calls that change something are bounded. |
| D-14 | When the refund call answers that the order is not cancelled, the agent sends no second refund call, says the refund was not issued, and asks staff to follow up. | the owner, accepting the recommendation | A person must settle why the cancelled order is not cancelled in the order system. |
| D-15 | When the refund call answers that the order is not cancelled, the agent tells the customer the refund was not issued and asks staff to follow up with the reason refund not issued; it does not ask for a manual refund. | the owner, accepting the recommendation | The order system says the order is not cancelled, so no refund may be issued until a person settles it. |
| D-16 | A staff task for a refund amount that differs carries the reason refund status unknown. | the owner, accepting the recommendation | The staff task queue takes three reasons, and this is the one that fits. |
| D-17 | When the first read of the customer's orders fails with an error, the agent changes nothing and tells the customer it cannot see their orders right now. | the owner, accepting the recommendation | Without the list the agent cannot tell which orders are the customer's. |
| D-18 | While a read keeps timing out, the agent tells the customer once that it is still checking, and reads again until the read answers, fails, or the customer leaves. | the owner, accepting the recommendation | The customer waits while the agent reads again. |
