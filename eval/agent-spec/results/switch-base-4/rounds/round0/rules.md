# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them. An *open order* is one whose status is placed or processing. A *read* is a call that only looks at orders; the cancel, refund and follow-up calls change something.

## R-01 Only orders that have not shipped are cancelled

The agent cancels an order only while it is placed or processing, however long ago it was placed. For a shipped or delivered order it says it cannot cancel, tells the customer returns are a separate process, sends no cancel call and changes nothing. When the cancel call answers not cancellable, or a read after a cancel call with no answer shows the order shipped, the agent tells the customer the same and issues no refund.

Rests on: C-05, C-08, C-09, C-10, C-11, C-29, C-42

## R-02 An order already cancelled is not changed

For an order that is already cancelled, the agent says so and changes nothing.

Rests on: C-02, C-12

## R-03 Only the customer's own orders

The agent acts only on the orders the order system lists for the signed-in customer. For an order number that matches none of them, it says so and changes nothing.

Rests on: C-01, C-03, C-13

## R-04 The customer says which order

When the customer has more than one open order and does not say which one to cancel, the agent asks which, and its proposal names the order number. It never picks an order for the customer.

Rests on: C-14

## R-05 Cancel only after a yes to the full proposal

The agent states one proposal: cancel this whole order, and refund its total paid to the order's payment method. It cancels only after the customer clearly says yes to that proposal. A question about an order, or saying they want to cancel, is not a yes. The one yes covers both the cancel and the refund. When the customer says no, the agent changes nothing. The agent does not cancel part of an order, and offers no store credit and no other payment method for the refund; there is no cancellation fee.

Rests on: C-15, C-17, C-27, C-33, C-50, C-51, C-53

## R-06 A changed proposal needs a new yes

When the customer changes any part of the proposal after saying yes, the earlier yes no longer counts. The agent states the changed proposal and asks again.

Rests on: C-16, C-38

## R-07 A cancelled order is refunded

Once the cancel call answers cancelled, or a read after a cancel call with no answer shows the order cancelled, the agent issues the refund for that order, without asking again.

Rests on: C-17, C-42

## R-08 At most two refund calls, never a second refund

After a refund call that answers with an error or gets no answer, the agent sends the refund call once more; it sends at most two refund calls for one order. After a failed refund, or an answer that the order is not cancelled, it sends none. When the second call gets no answer, it reads the order and its refund again and tells the customer what it finds. An order gets at most one refund.

Rests on: C-18, C-19, C-20, C-22, C-28, C-31, C-32, C-37, C-40, C-45, C-48, C-49, C-52

## R-09 The customer is told what happened

The agent says the order is cancelled and refunded only when a refund for the confirmed amount is pending or issued, and then gives the amount, the payment method, the refund id and whether it is pending or issued. It promises nothing about when the money arrives. What it last tells the customer matches the refund's last status: after the second refund call and a read that shows a failed refund or no refund, it says the refund is not confirmed yet; when that read fails, it says the refund's status is unknown. It never says nothing was changed when it may have been.

Rests on: C-06, C-07, C-21, C-23, C-35, C-49, C-54

## R-10 What the agent could not finish goes to staff

When the refund was not issued, the refund amount differs, or the agent cannot tell whether the order was cancelled or the refund issued, it asks staff to follow up on the order with the reason, does not claim success, and tells the customer staff will follow up. When the follow-up call gets no answer it sends it once more; when that gets no answer too, it tells the customer to contact Harbor Goods support.

Rests on: C-21, C-24, C-25, C-26, C-36, C-39, C-47

## R-11 After a cancel call with no answer, read before cancelling again

When the cancel call gets no answer, the agent does not just send it again: it reads the order first. Cancelled, it goes on to the refund. Still placed or processing, it sends the cancel once more under the same yes. Shipped, it says so and issues no refund. When the read fails, it says the outcome is unknown, issues no refund, and asks staff to follow up. When the second cancel call also gets no answer, it sends no third cancel call and no refund call, says the outcome is unknown, and asks staff to follow up. When the cancel call answers order not found, it sends no refund call, says the order could not be cancelled, and asks staff to follow up.

Rests on: C-29, C-30, C-41, C-42, C-43, C-44

## R-12 A refund amount that differs is not acted on

When the refund the order system returns is for an amount other than the one the customer said yes to, the agent makes no further change, tells the customer the amount the order system returned, and asks staff to follow up.

Rests on: C-34, C-39

## R-13 A read with no answer is sent again

When a read gets no answer, the agent sends it again; the owner set no limit on reads. Only a read that fails with an error counts as a failed read.

Rests on: C-35, C-46

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asked to cancel an order | reads the customer's orders | R-03 |
| a read got no answer | sends the same read again | R-13 |
| the order list call failed with an error | says it cannot see the orders right now and that nothing was changed | R-09 |
| the customer named an order number that matches none of their orders | says no order of theirs has that number, and changes nothing | R-03 |
| the customer named no order and has more than one open order | asks which order to cancel | R-04 |
| the order has shipped or been delivered | says it cannot be cancelled and that returns are a separate process, and changes nothing | R-01 |
| the order is already cancelled | says so, and changes nothing | R-02 |
| the order is open and the agent knows which one the customer means | proposes: cancel this whole order and refund its total paid to its payment method, and asks for a yes | R-05, R-04 |
| the customer changed the proposal | states the changed proposal and asks for a yes again | R-06 |
| the customer said no | says nothing was changed | R-05 |
| the customer said yes to the current proposal | cancels the order | R-05 |
| the cancel call answered not cancellable | says the order has shipped and cannot be cancelled, that returns are a separate process, and issues no refund | R-01 |
| the cancel call answered order not found | asks staff to follow up (cancellation unknown), then says the order could not be cancelled | R-11, R-10 |
| the first cancel call got no answer | reads the order again | R-11 |
| the read after the cancel call shows the order still placed or processing | cancels the order once more | R-11 |
| the read after the cancel call shows the order shipped | says the order has shipped and cannot be cancelled, that returns are a separate process, and issues no refund | R-01, R-11 |
| the read after the cancel call failed with an error | asks staff to follow up (cancellation unknown), then says the outcome is unknown | R-11, R-10 |
| the second cancel call got no answer | asks staff to follow up (cancellation unknown), then says the outcome is unknown | R-11, R-10 |
| the cancel call answered cancelled, or the read after it shows the order cancelled | issues the refund | R-07 |
| the refund call, or the read after the second one, shows a refund for the confirmed amount | says the order is cancelled and gives the refund amount, payment method, refund id and whether it is pending or issued | R-09 |
| the refund call, or the read after the second one, shows a refund for a different amount | asks staff to follow up (refund amount differs), then tells the customer the amount the order system returned | R-12, R-10 |
| the refund call answered with a failed refund, or order not cancelled | asks staff to follow up (refund not issued), then says the refund was not issued | R-08, R-10 |
| the first refund call answered with an error or got no answer | issues the refund once more | R-08 |
| the second refund call answered with an error | asks staff to follow up (refund not issued), then says the refund was not issued | R-08, R-10 |
| the second refund call got no answer | reads the order and its refund again | R-08 |
| the read after the second refund call shows a failed refund or no refund | asks staff to follow up (refund not issued), then says the refund is not confirmed yet | R-09, R-10 |
| the read after the second refund call failed with an error | asks staff to follow up (refund status unknown), then says the refund's status is unknown | R-09, R-10 |
| the first follow-up call got no answer | asks staff to follow up once more | R-10 |
| a follow-up call answered created | tells the customer what happened and that staff will follow up | R-10, R-09 |
| the second follow-up call got no answer | tells the customer what happened and to contact Harbor Goods support | R-10, R-09 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | Only orders that are placed or processing can be cancelled; there is no time limit and no final-sale exception. | the owner | Returns of shipped orders are a separate process. |
| D-02 | The customer's one yes to the proposal covers both the cancel and the refund. | the owner | The customer agrees to the whole outcome once. |
| D-03 | After a passing refund error, or a refund call with no answer, the agent sends the refund call once more; after a lasting error it sends none. | the owner | A lasting error means the payment method can no longer receive money or the provider declined. |
| D-04 | When the second refund call gets no answer, the agent reads the order and its refund again and tells the customer what it finds. | the owner | The final message must match the refund's last status. |
| D-05 | A follow-up call with no answer is sent once more; after that the customer is told to contact Harbor Goods support. | the owner | The follow-up call is safe to repeat. |
| D-06 | After a cancel call with no answer, the agent reads the order before it sends the cancel again. | the owner | No blind resend. |
| D-07 | The refund is the order's total paid, and a refund amount that differs from it is not acted on: the agent tells the customer the returned amount and asks staff to follow up. | the owner, accepting the recommendation | A different amount from the one the customer said yes to is not the agreed outcome. |
| D-08 | At most two refund calls per order in all; when the second answers with an error, staff follow up. | the owner, accepting the recommendation | Without it, an answer with no reply followed by a passing error had no end. |
| D-09 | One proposal cancels one order; another order needs its own proposal and yes. | the owner, accepting the recommendation | Each order can be cancelled only once, so this ends. |
| D-10 | When the second cancel call also gets no answer, the agent stops, says the outcome is unknown, and asks staff to follow up. | the owner, accepting the recommendation | Without it, cancel and read could repeat with no end. |
| D-11 | When the cancel call answers order not found, the agent issues no refund, says the order could not be cancelled, and asks staff to follow up. | the owner, accepting the recommendation | The order list showed the order, so the store must look at it. |
| D-12 | When the refund call answers order not cancelled, the agent sends no further refund call, says the refund was not issued, and asks staff to follow up. | the owner, accepting the recommendation | A second call would get the same answer. |
| D-13 | Reads with no answer are sent again with no limit. | the owner | Only calls that change something are bounded. |
