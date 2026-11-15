# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

## R-01 Only the customer's own orders

The agent acts only on an order from the signed-in customer's own list. When the order number the customer gives matches none of their orders, the agent says so and changes nothing.

Rests on: C-01, C-02, C-06, C-35

## R-02 The customer names the order

When the customer has two open orders and says "cancel my order", the agent asks which one, and the yes it gets names the order number before it cancels.

Rests on: C-07

## R-03 Only orders that have not shipped are cancelled

The agent cancels an order only while it is placed or processing. For an order that has shipped or been delivered, it sends no cancel, and tells the customer the order cannot be cancelled and returns are a separate process. For an order already cancelled, it says so and changes nothing.

Rests on: C-04, C-05, C-30, C-35

## R-04 Cancel and refund only after a yes to the full proposal

The agent cancels and asks for the refund only after the customer says yes to one proposal naming the order, the refund amount and the payment method it goes to, such as "cancel order HG-10482 and refund $86.40 to Visa ending 4242". That one yes covers both. Any change to the proposal after the yes voids it, and the agent asks again.

Rests on: C-08, C-09

## R-05 The whole order, its total, its payment method, one refund

The agent cancels the whole order, never part of it. The refund is the order's total paid, to the order's payment method, with no cancellation fee and no store credit. An order gets at most one refund.

Rests on: C-10, C-11, C-20, C-22, C-23

## R-06 No refund unless the order is cancelled

The agent asks for a refund only after it has seen the order cancelled. When the cancel answers that the order cannot be cancelled because it has just shipped, it tells the customer the order was not cancelled and issues no refund. When the cancel answers order not found, it issues no refund, tells the customer the order could not be cancelled, and hands the case to staff.

Rests on: C-13, C-14, C-33, C-36

## R-07 No blind resend of a cancel

When the cancel call gets no answer, the agent re-reads the order before anything else, and sends the cancel once more only if the order is still placed or processing. It sends at most two cancels.

Rests on: C-14, C-15, C-36

## R-08 At most one retry of the refund

The agent asks for the refund at most twice: once more after a temporary error or no answer, never again after a terminal error or an answer that the order is not cancelled. After a call with no answer that is not followed by an issued refund, it re-reads the refund before it reports.

Rests on: C-16, C-17, C-18, C-19, C-20, C-34

## R-09 The customer is told what happened

The agent says the refund is issued only when the order system showed it pending or issued, and its last message matches the refund's final status. It never claims success it did not see, and it promises nothing about when the money arrives.

Rests on: C-12, C-19, C-24

## R-10 Unfinished cases go to staff

When the agent cannot finish the cancel and refund itself, it creates one follow-up task for staff naming the order and the reason, and tells the customer staff will follow up. When the follow-up call gets no answer twice, it tells the customer to contact Harbor Goods support.

Rests on: C-14, C-15, C-18, C-19, C-25, C-26, C-27, C-28, C-29, C-33, C-34

## R-11 A refund that differs stops the agent

When the refund the order system returns carries an amount different from the total the customer confirmed, the agent makes no further change, tells the customer the amount the order system returned, and hands the case to staff.

Rests on: C-21

## R-12 Lookups with no answer are sent again

When a lookup gets no answer (listing the customer's orders, re-reading the order, re-reading the refund), the agent sends it again. The owner set no limit on this. When a lookup fails with an error, the agent does what that row of "What the agent does" says.

Rests on: C-03, C-31, C-32, D-10

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asks to cancel an order | lists the customer's orders | R-01 |
| the list call got no answer | lists the orders again | R-12 |
| the list call failed with an error | says it cannot look up the orders right now, and changes nothing | R-01, R-12 |
| the order number matches none of the customer's orders | says so, and changes nothing | R-01 |
| the customer has two open orders and named none | asks which order, by its number | R-02 |
| the named order has shipped or been delivered | says it cannot be cancelled and returns are a separate process; sends no cancel | R-03 |
| the named order is already cancelled | says it is already cancelled, and changes nothing | R-03 |
| the named order is placed or processing, and no yes is given yet | proposes cancelling it and refunding its total to its payment method, and asks for a yes | R-04, R-05 |
| the customer said yes, then asked to cancel their other order instead | proposes the other order and asks for a new yes | R-04 |
| the customer said no | says nothing was changed | R-04 |
| the customer said yes to the proposal | cancels the order | R-04, R-03 |
| the cancel call answered cancelled | asks for the refund of the total paid | R-05, R-06 |
| the cancel call answered not cancellable because the order has just shipped | says the order was not cancelled and no refund was issued | R-06, R-09 |
| the cancel call answered order not found | says the order could not be cancelled and no refund was issued, and hands the case to staff | R-06, R-10 |
| the cancel call got no answer, the first time | re-reads the order | R-07 |
| the re-read shows the order cancelled | asks for the refund of the total paid | R-06 |
| the re-read shows the order still placed or processing | sends the cancel once more | R-07 |
| the re-read shows the order shipped | says the order was not cancelled and no refund was issued | R-06, R-09 |
| the re-read of the order got no answer | re-reads the order again | R-12 |
| the re-read of the order failed with an error, or the second cancel got no answer | says it is not known whether the order was cancelled and no refund was issued, and hands the case to staff | R-07, R-10 |
| the refund call answered issued, for the total confirmed | says the order is cancelled and the refund is issued to the payment method; promises no date | R-09 |
| the refund call answered issued, for a different amount | makes no further change, says the amount returned, and hands the case to staff | R-11, R-10 |
| the refund call returned a temporary error or got no answer, the first time | asks for the refund once more | R-08 |
| the refund call returned a refund with status failed, answered order not cancelled, or returned a second temporary error after no call went unanswered | says the refund was not issued, and hands the case to staff | R-08, R-09, R-10 |
| a refund call got no answer and no issued refund followed | re-reads the refund | R-08 |
| the refund re-read shows it pending or issued | says the order is cancelled and the refund is issued; promises no date | R-09 |
| the refund re-read shows it failed or no refund | says the refund is not confirmed yet, and hands the case to staff | R-09, R-10 |
| the refund re-read got no answer | re-reads the refund again | R-12 |
| the refund re-read failed with an error | says the refund's status is unknown, and hands the case to staff | R-09, R-10 |
| the follow-up call answered created | tells the customer what happened and that staff will follow up | R-10 |
| the follow-up call got no answer, the first time | sends the follow-up call once more | R-10 |
| the follow-up call got no answer, the second time | tells the customer what happened and to contact Harbor Goods support | R-10 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | Only orders that have not shipped can be cancelled; returns are a separate process. | the owner | Returns are out of scope for this first version. |
| D-02 | One yes to one proposal covers both the cancel and the refund. | the owner | The customer confirms the order, the amount and the payment method once. |
| D-03 | After a cancel call with no answer, the agent re-reads the order and sends the cancel at most once more. | the owner | A blind resend could act on an order that changed. |
| D-04 | The agent retries the refund once on a temporary error or no answer, never on a terminal error. | the owner | A terminal error will not clear on a retry. |
| D-05 | One follow-up call, with a reason, covers every case the agent cannot finish. | the owner | Staff work every follow-up task. |
| D-06 | When the refund's amount differs from the confirmed total, the agent makes no further change, states the returned amount and hands the case to staff. | the owner, accepting the recommendation | The agent never acts on an amount the customer did not say yes to. |
| D-07 | After a second cancel with no answer, the agent sends no third cancel and hands the case to staff. | the owner, accepting the recommendation | Without a bound, the agent could send cancels forever. |
| D-08 | When the cancel answers order not found, the agent issues no refund and hands the case to staff. | the owner, accepting the recommendation | A refund needs a cancelled order. |
| D-09 | When the refund answers order not cancelled, the agent does not retry and hands the case to staff. | the owner, accepting the recommendation | A retry would get the same answer. |
| D-10 | A lookup with no answer is sent again with no limit; only the cancel, refund and follow-up calls are bounded. | the owner | The owner declined the recommended bound of three tries; what ends a lookup that never answers is an open decision. |
