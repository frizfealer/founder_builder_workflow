# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

An *open* order is an order whose status is placed or processing. To *hand the case to staff* is to ask the staff task queue for a follow-up task that names the order and what happened.

## R-01 Only the customer's own open orders are cancelled

The agent cancels only an order in the signed-in customer's own list whose status is placed or processing. For an order that has shipped or been delivered, it issues no cancel call and tells the customer it cannot cancel it and that returns are a separate process. For an order that is already cancelled, it says so and changes nothing. For an order number that matches none of the customer's orders, it says so and changes nothing. When listing the orders gets no answer, it lists them again; when the listing fails, it tells the customer it cannot see their orders right now, changes nothing, and asks them to try again later.

Rests on: C-01, C-02, C-03, C-04, C-05, C-06, C-15, C-37, C-41

## R-02 The proposal names the order

When the customer has more than one open order and does not say which, the agent asks which one. The proposal always names the order number, and no cancel call comes before the customer confirms it.

Rests on: C-10, C-12

## R-03 Cancel only after a yes to the full proposal

The agent cancels an order only after the customer explicitly confirms the full proposal: which order, the refund amount and where it goes. The one yes covers both the cancellation and the refund. A question about an order, or saying they want to cancel, is not a yes.

Rests on: C-11, C-12

## R-04 A changed proposal needs a new yes

Any change to the proposal after the customer confirmed it voids the confirmation. The agent states the changed proposal and asks again.

Rests on: C-11

## R-05 Whole orders, the full amount, one refund

The agent cancels only a whole order. It proposes a refund of the order total the customer paid, back to the order's payment method, with no fee and no store credit, and an order gets at most one refund. When the customer asks to cancel only some items, it says only the whole order can be cancelled.

Rests on: C-07, C-08, C-09, C-24, C-31, C-34

## R-06 No refund without a cancellation

The agent issues the refund only after the order system shows the order cancelled. When the cancel call answers that the order is not cancellable because it has shipped or been delivered, the agent tells the customer so truthfully and issues no refund call. When the cancel call answers that the order is not found, the agent tells the customer it cannot find that order, changes nothing, and issues no refund.

Rests on: C-14, C-17, C-19, C-40

## R-07 A cancel call with no answer is not sent again blind

When the cancel call gets no answer, the agent reads the order again before anything else. If the read shows it cancelled, the agent goes on to the refund; if it shows it shipped, the agent says it was not cancelled and issues no refund. If it shows the order still placed or processing, the agent sends the cancel call once more under the same yes; if that one also gets no answer and a read again shows the order still open, the agent sends no third cancel call, tells the customer the order was not cancelled and no refund was issued, and hands the case to staff. If the read fails, the agent says the outcome is unknown, issues no refund, and hands the case to staff. A read with no answer is read again.

Rests on: C-17, C-18, C-37, C-38, C-39, D-02

## R-08 The refund call is sent at most twice

The agent sends the refund call a second time only after a temporary error or no answer, and never a third time. After a final error it sends no second call: it hands the case to staff and tells the customer the refund was not issued, without claiming success.

Rests on: C-19, C-20, C-21, C-24, D-01

## R-09 After a refund call with no answer, read before telling

After a refund call with no answer, the agent sends it once more and then reads the order and its refund again, and tells the customer what that read shows. Pending or issued: it says that status. Failed or no refund: it hands the case to staff and says the refund is not confirmed yet. The read fails: it says the refund status is unknown and hands the case to staff. A read with no answer is read again. When the second call answers a refund whose amount differs from the confirmed one, the agent acts on that answer at once instead, as the next rule says, without reading the refund again.

Rests on: C-22, C-24, C-37, C-42

## R-10 The customer is told what happened

The agent says the order is cancelled only when the order system showed it cancelled, and states the refund only as the order system reported it, so its final message matches the final refund status. It promises nothing about when the money arrives.

Rests on: C-13, C-23, C-32, C-33

## R-11 A refund amount that differs stops the agent

When the refund the order system reports differs from the amount the customer said yes to, the agent makes no further change with the new amount, tells the customer the amount the order system returned, and hands the case to staff.

Rests on: C-25, C-42

## R-12 Staff follow up on what the agent could not finish

The agent hands the case to staff when a cancel or refund call fails or gets no answer, or the refund differs from what the customer confirmed, and tells the customer that staff will follow up. When the follow-up call gets no answer it sends it once more; if that gets no answer too, it tells the customer to contact Harbor Goods support.

Rests on: C-26, C-27, C-28, C-29, C-30, C-43

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asked to cancel an order | lists the customer's orders | R-01 |
| listing the orders got no answer | lists the orders again | R-01 |
| listing the orders failed | says it cannot see their orders right now, changes nothing, and asks them to try again later | R-01 |
| the customer asked to cancel only some items | says only the whole order can be cancelled | R-05 |
| the order number matches none of the customer's orders | says so and changes nothing | R-01 |
| the order has shipped or been delivered | says it cannot cancel it and that returns are a separate process, and issues no cancel call | R-01 |
| the order is already cancelled | says so and changes nothing | R-01 |
| the customer has more than one open order and did not say which | asks which order | R-02 |
| one open order is the one the customer means | proposes: cancel this order number and refund the order total to the order's payment method, and asks for a yes | R-02, R-03, R-05 |
| the customer said yes to the proposal | sends the cancel call | R-03 |
| the customer said yes and changed which order | states the changed proposal and asks again | R-04 |
| the customer withdrew | says nothing was changed | R-03 |
| the cancel call answered "cancelled" | sends the refund call | R-06 |
| the cancel call answered "not cancellable" because the order has shipped or been delivered | says the order has shipped and was not cancelled, that returns are a separate process, and issues no refund call | R-06, R-10 |
| the cancel call answered "order not found" | says it cannot find that order, changes nothing, and issues no refund | R-06 |
| the cancel call got no answer | reads the order again | R-07 |
| the read of the order got no answer | reads the order again | R-07 |
| the read after the cancel call shows the order cancelled | sends the refund call | R-07, R-06 |
| the read after the cancel call shows the order shipped | says the order has shipped and was not cancelled, and issues no refund call | R-07, R-06 |
| the read after the first cancel call shows the order still open | sends the cancel call once more under the same yes | R-07 |
| the read after the second cancel call shows the order still open | sends no third cancel call and hands the case to staff: the order was not cancelled and no refund was issued | R-07, R-12 |
| the read after the cancel call failed | hands the case to staff: the cancellation is unknown and no refund was issued | R-07, R-12 |
| the refund call answered a pending or issued refund for the confirmed amount, with no unanswered refund call before it | says the order is cancelled and the refund of that amount to that payment method is pending or issued, and promises nothing about when it arrives | R-10 |
| a refund call answered a refund whose amount differs from the confirmed one | makes no further change and hands the case to staff: the refund differs | R-11, R-12 |
| the refund call answered "failed" | hands the case to staff: the refund was not issued | R-08, R-12 |
| the refund call answered a temporary error, the first time | sends the refund call again | R-08 |
| the refund call answered a temporary error, the second time | hands the case to staff: the refund was not issued | R-08, R-12 |
| the refund call got no answer, the first time | sends the refund call again | R-08, R-09 |
| the second refund call has answered the confirmed amount, or got no answer, after an unanswered one, or got no answer after a temporary error | reads the order and its refund again | R-09 |
| the read of the refund got no answer | reads the order and its refund again | R-09 |
| the read shows a pending or issued refund for the confirmed amount | says the order is cancelled and the refund is pending or issued | R-09, R-10 |
| the read shows a refund whose amount differs from the confirmed one | makes no further change and hands the case to staff: the refund differs | R-11, R-12 |
| the read shows a failed refund or no refund | hands the case to staff: the refund is not confirmed yet | R-09, R-12 |
| the read of the refund failed | hands the case to staff: the refund status is unknown | R-09, R-12 |
| the follow-up call answered | tells the customer what happened and that staff will follow up | R-12, R-10 |
| the follow-up call got no answer, the first time | sends the follow-up call again | R-12 |
| the follow-up call got no answer, the second time | tells the customer what happened and to contact Harbor Goods support | R-12, R-10 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | After a temporary refund error the agent tries once more; after a final error it does not. | the owner | One retry allowed on a transient error, none on a terminal one. |
| D-02 | When the read after an unanswered cancel call fails, the agent issues no refund and hands the case to staff. | the owner | A refund without a known cancellation could pay for an order that ships. |
| D-03 | The agent asks staff to follow up when a cancel or refund call fails or gets no answer, or the refund differs from what the customer confirmed. | the owner, accepting the recommendation | Without it, a cancelled order could be left with no refund and nobody told. |
| D-04 | When the refund amount differs from the confirmed one, the agent makes no further change, tells the customer the amount returned, and hands the case to staff. | the owner, accepting the recommendation | The customer said yes to one amount; a different one needs a person. |
| D-05 | When listing the orders fails, the agent tells the customer it cannot see their orders right now, changes nothing, and asks them to try again later. | the owner, accepting the recommendation | With no list the agent cannot tell which orders are the customer's. |
| D-06 | When the cancel call answers "order not found", the agent says it cannot find that order, changes nothing, and issues no refund. | the owner, accepting the recommendation | Without a cancelled order there is nothing to refund. |
| D-07 | After the cancel call is sent a second time and the order is still open, the agent sends no third call and hands the case to staff. | the owner, accepting the recommendation | Without a bound, the agent could resend the cancel forever. |
| D-08 | When the second refund call answers a different amount, the agent acts on it at once instead of reading the refund again. | the owner, accepting the recommendation | Otherwise a failed read would hide the different amount from the customer. |
| D-09 | Reads that get no answer are tried again with no limit. | the owner | Reads may be retried on timeout without limit; only commit calls are bounded. |
