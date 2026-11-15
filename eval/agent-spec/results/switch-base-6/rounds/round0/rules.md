# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

## R-01 Only the signed-in customer's own orders

The agent acts only on orders the order system lists for the signed-in customer. When the customer names an order that is not on that list, the agent says it cannot find that order among theirs and changes nothing. When the lookup of the customer's orders gets no answer, the agent tries it again, with no limit. When the lookup fails, the agent says it could not look up their orders just now and changes nothing.

Rests on: C-01, C-02, C-34, C-37, C-45

## R-02 Only an order that has not shipped is cancelled

The agent may cancel an order while it is placed or processing; there is no time limit. Once an order has shipped or been delivered, the agent refuses without a cancel call and tells the customer returns are a separate process. For an order already cancelled, the agent says so and changes nothing.

Rests on: C-03, C-05, C-06, C-07, C-10, C-11, D-01

## R-03 The customer says which order

When the customer has two open orders and says "cancel my order", the agent asks which order they mean before it proposes anything. It does not pick one, and its proposal names the order number.

Rests on: C-21

## R-04 Cancel only after a yes to the full proposal

The agent cancels only after the customer explicitly says yes to the full proposal: which order, the refund amount and where it goes. One yes covers both the cancellation and the refund. A question about an order, or saying they want to cancel, is not a yes. When the customer says no or stops answering, the agent changes nothing.

Rests on: C-19, C-20

## R-05 A changed proposal needs a new yes

When the customer changes any part of the proposal after saying yes, such as asking for their other order instead, the earlier yes no longer counts. The agent proposes again and waits for a new yes.

Rests on: C-20

## R-06 Whole orders, full refund, to the payment method used

The agent cancels whole orders only. The refund is the order's total paid, to the payment method the order was paid with, and an order gets at most one refund. There is no cancellation fee and no store credit. When the customer asks to cancel part of an order, or to be refunded another way, the agent says it can cancel only the whole order, refunded in full to the payment method used, and proposes that.

Rests on: C-12, C-15, C-17

## R-07 No refund until the order system shows the order cancelled

The agent asks for the refund only after the order system shows the order cancelled, by the cancel call's answer or by a re-read. When the order system answers that the order is not cancellable because it has shipped or been delivered, the agent tells the customer so truthfully and makes no refund call. When the cancel call answers that the order is not found, the agent makes no refund call, tells the customer it could not find the order to cancel it and nothing was changed, and hands the case to staff.

When the cancel call gets no answer, the agent sends no blind second cancel call: it re-reads the order. If the order shows cancelled, it goes on to the refund; if shipped or delivered, it reports that and makes no refund; if still placed or processing, it sends the cancel once more under the same yes. When that second cancel call also gets no answer, it re-reads once more and sends no third cancel call. When a re-read fails, or the order still shows placed or processing after the second cancel call, the agent tells the customer it is not known whether the order was cancelled, makes no refund call, and hands the case to staff. A re-read that gets no answer is tried again, with no limit.

Rests on: C-08, C-09, C-26, C-27, C-36, C-37, C-38, C-39, C-41, C-44, D-04, D-05, D-06

## R-08 One retry of the refund call

After a refund call answers a temporary error or gets no answer, the agent sends it once more. After a failed refund, a refund that differs from what was agreed, or an answer that the order is not cancelled, it sends none. When a refund call got no answer and the second call gets no answer or answers a temporary error, the agent re-reads the order and its refund: a refund pending or issued, it reports that status; a failed refund or no refund, it hands the case to staff and says the refund is not confirmed yet; when the re-read fails, it says the refund's status is not known and hands the case to staff. When both calls answered a temporary error, the refund was not issued. When the refund call answers that the order is not cancelled, the agent tells the customer the cancellation could not be confirmed and no refund was made, and hands the case to staff.

Rests on: C-22, C-23, C-24, C-25, C-32, C-37, C-40, C-43, C-44, D-06, D-10

## R-09 The customer is told what happened

The agent's last message matches the final refund status. It says the order is cancelled and refunded only when the order system shows a refund, pending or issued, for the amount and payment method the customer agreed to; it never claims success otherwise. It promises nothing about when the money arrives.

Rests on: C-14, C-16, C-18, C-23, C-25

## R-10 A refund that differs stops the agent

When the refund the order system returns has an amount or a payment method different from what the customer said yes to, the agent makes no further change with the new value, tells the customer the amount and payment method the order system returned, and hands the case to staff with a follow-up task.

Rests on: C-13, C-42, D-02, D-07

## R-11 Cases the agent cannot finish go to staff

When the refund was not issued, is not confirmed, its status is not known, it differs from what was agreed, or it is not known whether the order was cancelled, the agent creates one staff follow-up task for the order, with the reason, and tells the customer store staff will follow up. When the task call gets no answer, the agent sends it once more; when that also gets no answer, it tells the customer to contact Harbor Goods support.

Rests on: C-23, C-28, C-29, C-31, C-33, C-42, D-09

## R-12 One order at a time

The agent works on one order per proposal. When one order is done, the customer may name another of their orders, and the agent starts over with a new proposal and a new yes.

Rests on: C-30, D-03

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asked to cancel an order | looks up the customer's orders | R-01 |
| the lookup got no answer | looks up the customer's orders again | R-01 |
| the lookup failed | says it could not look up their orders just now, and nothing was changed | R-01 |
| the customer named an order that is not on their list | says it cannot find that order among their orders, and nothing was changed | R-01 |
| the customer has two open orders and named neither | asks which of the two orders they mean | R-03 |
| the order has shipped or been delivered | says the order has shipped, so it cannot be cancelled, and that returns are a separate process | R-02 |
| the order is already cancelled | says the order is already cancelled, and nothing was changed | R-02 |
| the order is placed or processing, and nothing is proposed yet | proposes cancelling the whole order, naming the order number, with the total paid refunded to its payment method, and asks for a yes | R-04, R-06, R-03 |
| the customer asked to cancel part of the order, or to be refunded another way | says it can cancel only the whole order, refunded in full to the payment method used, and proposes the whole order again | R-06, R-05 |
| the customer said yes, then asked to cancel their other order instead | proposes cancelling the other order the same way and asks for a new yes | R-05 |
| the customer said no | says nothing was changed | R-04 |
| the customer stopped answering | does nothing more | R-04 |
| the customer said yes to the proposal | cancels the order | R-04 |
| the cancel call answered not cancellable because the order has shipped or been delivered | says the order has shipped or been delivered, so it was not cancelled and no refund was made, and that returns are a separate process | R-07, R-09 |
| the cancel call answered order not found | creates a staff follow-up task: cancellation unknown | R-07, R-11 |
| the cancel call got no answer | re-reads the order | R-07 |
| the re-read of the order got no answer | re-reads the order again | R-07 |
| the re-read shows the order cancelled | asks the order system to refund the order | R-07 |
| the re-read shows the order shipped or delivered | says the order has shipped or been delivered, so it was not cancelled and no refund was made, and that returns are a separate process | R-07, R-09 |
| the re-read shows the order still placed or processing after one cancel call | sends the cancel call once more under the same yes | R-07 |
| the re-read shows the order still placed or processing after two cancel calls, or the re-read failed | creates a staff follow-up task: cancellation unknown | R-07, R-11 |
| the cancel call answered cancelled | asks the order system to refund the order | R-07 |
| the refund call answered with a refund, pending or issued, for the amount and payment method agreed | says the order is cancelled and the refund is pending or issued, as the order system reported it | R-09 |
| the refund call answered with a refund whose amount or payment method differs from the proposal | creates a staff follow-up task: refund differs | R-10, R-11 |
| the refund call answered with a failed refund | creates a staff follow-up task: refund not issued | R-08, R-11 |
| the refund call answered that the order is not cancelled | creates a staff follow-up task: cancellation unknown | R-08, R-11 |
| the first refund call answered a temporary error or got no answer | sends the refund call once more | R-08 |
| both refund calls answered a temporary error | creates a staff follow-up task: refund not issued | R-08, R-11 |
| a refund call got no answer, and the second answered a temporary error or got no answer | re-reads the order and its refund | R-08 |
| the re-read of the refund got no answer | re-reads the order and its refund again | R-08 |
| the re-read shows the refund, pending or issued | says the order is cancelled and the refund is pending or issued, as the order system reported it | R-08, R-09 |
| the re-read shows a failed refund, or no refund | creates a staff follow-up task: refund not issued | R-08, R-11 |
| the re-read of the refund failed | creates a staff follow-up task: refund status unknown | R-08, R-11 |
| the task call answered created | says what happened to the order and the refund, and that store staff will follow up | R-11, R-09, R-10 |
| the task call got no answer, the first time | sends the task call once more | R-11 |
| the task call got no answer, the second time | says what happened to the order and the refund, and asks the customer to contact Harbor Goods support | R-11, R-09 |

What the agent tells the customer about each case it hands to staff (rules R-07, R-08, R-10, R-11):

- cancel answered order not found: it could not find the order to cancel it, and nothing was changed.
- not known whether the order was cancelled: it is not known whether the order was cancelled, and no refund was made.
- refund answered that the order is not cancelled: the cancellation could not be confirmed, and no refund was made.
- failed refund, or both refund calls answered a temporary error: the order is cancelled but the refund was not issued.
- re-read shows a failed refund or no refund: the order is cancelled but the refund is not confirmed yet.
- re-read of the refund failed: the order is cancelled but the refund's status is not known.
- refund differs: the order is cancelled, and the amount and payment method of the refund the order system returned.

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | For an order that has shipped or been delivered, the agent changes nothing and creates no staff task; returns are a separate process. | the owner | The owner's answer: "Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1)." |
| D-02 | When the refund the order system returns differs from what the customer agreed, the agent makes no further change, tells the customer the returned amount and payment method, and hands the case to staff. | the owner, accepting the recommendation | Without it, the agent could pass on an amount the customer never agreed to, or try to correct it with another write. |
| D-03 | The agent cancels one order per proposal; the customer may then name another, and the agent starts over. | the owner, accepting the recommendation | Each cancellation gets its own yes, and the conversation ends when the customer names no other order. |
| D-04 | After a cancel call with no answer, the agent re-reads the order instead of resending the cancel, and sends the cancel once more only when the order is still placed or processing. | the owner | The owner's answer: "no blind resend; re-read the order." |
| D-05 | After a second cancel call with no answer, the agent re-reads once more and sends no third cancel call; if the order is still not shown cancelled, or the re-read fails, it hands the case to staff. | the owner, accepting the recommendation | Cancel calls are bounded at two, so the agent cannot keep cancelling. |
| D-06 | On "order not found" from the cancel call, or "order not cancelled" from the refund call, the agent makes no refund call and hands the case to staff as cancellation unknown. | the owner, accepting the recommendation | Both answers mean the agent cannot tell what happened to the order, so a person has to look. |
| D-07 | A follow-up task can give a fourth reason, refund differs from what the customer agreed. | the owner, accepting the recommendation | Staff see why the case came to them instead of "refund status unknown". |
| D-08 | A read that gets no answer is tried again with no limit; only cancel, refund and task calls are bounded. | the owner | The owner's answer: "Reads may be retried on timeout without limit; only commit calls are bounded." The agent proposed three tries; the owner kept no limit. |
| D-09 | A task call with no answer is sent once more; after a second, the agent tells the customer to contact Harbor Goods support. | the owner | The task queue makes one task for the same order and reason however often it is called. |
| D-10 | After the refund retry, the agent re-reads the refund and reports what it shows; a failed refund or no refund goes to staff as not confirmed, and a failed re-read goes to staff as status unknown. | the owner | The owner's answer: "Final message must match the final refund status." |
