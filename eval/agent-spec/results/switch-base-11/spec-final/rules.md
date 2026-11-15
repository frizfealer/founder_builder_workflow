# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

An *open* order is one whose status is placed or processing. A *handoff* is the agent creating a follow-up task for store staff. A *re-read* is the agent reading the order or its refund again, to see what a call with no answer did.

## R-01 Only open orders are cancelled

The agent cancels an order only when it is placed or processing, with no time limit. It never cancels an order the signed-in customer did not place.

Rests on: C-03, C-05

## R-02 Shipped, delivered, cancelled or unknown orders change nothing

For a shipped or delivered order, the agent says it cannot cancel it, sends no cancel call, and tells the customer returns are a separate process. For an order that is already cancelled, it reports that and changes nothing. For an order number that matches none of the customer's orders, it says so and changes nothing. When it cannot read the customer's orders, it says so and changes nothing.

Rests on: C-06, C-07, C-34, C-35, C-15

## R-03 Only the whole order

The agent cancels whole orders only. When the customer asks to cancel only some items, it says only the whole order can be cancelled.

Rests on: C-28, C-29

## R-04 Cancel only after a yes to the full proposal

The agent states one proposal: which order, that it will be cancelled, the refund amount and where it goes, as in "cancel order HG-10482 and refund $86.40 to Visa ending 4242". It cancels only after the customer explicitly confirms that proposal; the one yes covers both the cancel and the refund. Any change after the yes voids it. When the customer's words fit more than one open order, the agent asks which one, and the yes must name the order number.

Rests on: C-36, C-37, C-38

## R-05 The refund is the order's total paid, to its payment method, once

The agent issues the refund only after the order is cancelled. The refund is the order's total paid, to the order's payment method, with no cancellation fee and no store credit. An order gets at most one refund.

Rests on: C-30, C-31, C-33, C-39, C-16

## R-06 A cancel with no answer is checked, not resent

When the cancel call gets no answer, the agent does not resend it blindly. It re-reads the order. Cancelled: it goes on to the refund. Still placed or processing: it sends the cancel once more under the same yes; if that call also gets no answer and the order is still placed or processing, it sends no third cancel call, tells the customer the order could not be cancelled right now and that no refund was issued, and hands the case to staff. Shipped: it says so and issues no refund. The re-read fails: it says the outcome is unknown, issues no refund, and hands the case to staff. When the cancel call answers that the order shipped, or that the order was not found, the agent says so truthfully and issues no refund.

Rests on: C-08, C-09, C-10, C-11, C-12, C-13, C-52

## R-07 A refund error is retried once only when it is transient

When the refund call answers a transient error, the agent sends it once more. When it answers a terminal error (a failed refund), or order not cancelled, it sends no further refund call, tells the customer the refund was not issued, does not claim success, and hands the case to staff. When the refund call gets no answer, the agent sends it once more, then re-reads the refund: pending or issued, it reports that status; failed or no refund, it hands the case to staff and says the refund is not confirmed yet; the re-read fails, it says the status is unknown and hands the case to staff.

Rests on: C-19, C-20, C-21, C-22, C-23, C-24, C-25, C-26

## R-08 No promise about when the money arrives

The agent promises nothing about when the money arrives.

Rests on: C-40, C-50

## R-09 The customer is told what happened

When the cancel and the refund both succeed, the agent tells the customer the order is cancelled, and the refund as the order system returned it: its amount, payment method, status (pending or issued) and refund id. The agent's last message matches the final refund status, and it never says a refund was made, or that nothing changed, when that is not what the order system showed.

Rests on: C-27, C-41, C-17

## R-10 A refund that differs from the yes is not acted on

When the refund the order system returns has a different amount or payment method from the ones the customer said yes to, the agent makes no further change with the new value, tells the customer the amount and payment method the refund call returned, and hands the case to staff with the reason refund status unknown.

Rests on: C-32, C-30, C-31, C-54

## R-11 What the agent cannot settle goes to staff

The agent hands the case to staff, with the order number and the reason (refund not issued, refund status unknown, or cancellation unknown), whenever the refund was not issued, its status is not known, or it is not known whether the order was cancelled. When the handoff call gets no answer, the agent sends it once more; if that also gets no answer, it tells the customer to contact Harbor Goods support.

Rests on: C-43, C-44, C-45, C-46, C-47, C-53, C-55

## R-12 Each order gets its own yes

The customer may cancel more than one order in one conversation, one at a time. Each order gets its own proposal and its own yes, and a yes for one order never covers another.

Rests on: C-42

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asks to cancel an order | reads the customer's orders | R-01 |
| the read of the orders got no answer | reads the orders again | R-01 |
| the read of the orders failed | says it cannot see their orders right now, and changes nothing | R-02 |
| the order number matches none of the customer's orders | says so, and changes nothing | R-02 |
| the customer's words fit two open orders | asks which order to cancel | R-04 |
| the order has shipped or been delivered | says it cannot be cancelled here and that returns are a separate process; sends no cancel call | R-02 |
| the order is already cancelled | says so, and changes nothing | R-02 |
| the order is open and named | proposes: cancel this order and refund its total paid to its payment method, and asks for a yes | R-04, R-05 |
| the customer said no to the proposal | says nothing was changed | R-04 |
| the customer said yes with a change to the proposal (another order, some items only, another payment method) | treats the yes as void and sends no cancel call; for some items, says only the whole order can be cancelled; for another payment method, says the refund goes to the order's payment method; for another order, takes that order instead; then states the proposal again and asks for a new yes | R-04, R-03, R-05 |
| the customer names another order while a proposal waits for a yes | sends no cancel call for the waiting proposal, and takes the orders one at a time, each with its own proposal and its own yes | R-12, R-04 |
| the customer asks to cancel two or more orders in one message | takes them one at a time: proposes the first and asks for its yes; once that order is settled, proposes the next | R-12, R-04 |
| one order is settled and the customer asks to cancel another | reads the customer's orders again and starts over for that order, with its own proposal and its own yes | R-12, R-04 |
| the customer said yes to the proposal | cancels the order | R-04, R-01 |
| the cancel call answered cancelled | issues the refund | R-05 |
| the cancel call answered that the order has shipped | says it shipped before it could be cancelled; issues no refund | R-06 |
| the cancel call answered order not found | says it could not find that order and that no refund was issued; cancels nothing more | R-06 |
| the cancel call got no answer | re-reads the order | R-06 |
| the re-read of the order got no answer | re-reads the order again | R-06 |
| the re-read shows the order cancelled | issues the refund | R-06, R-05 |
| the re-read shows the order still open, after the first cancel call | sends the cancel once more under the same yes | R-06 |
| the re-read shows the order still open, after the second cancel call | hands the case to staff (cancellation unknown), then says the order could not be cancelled right now and that no refund was issued | R-06, R-11 |
| the re-read shows the order shipped | says it shipped before it could be cancelled; issues no refund | R-06 |
| the re-read of the order failed | hands the case to staff (cancellation unknown), then says it is not known whether the order was cancelled and that no refund was issued | R-06, R-11 |
| the refund call returned a pending or issued refund for the confirmed amount and payment method | tells the customer the order is cancelled, with the refund's amount, payment method, status and refund id | R-09, R-08 |
| the refund call returned a refund with a different amount or payment method | hands the case to staff (refund status unknown), then tells the customer the amount and payment method the refund call returned | R-10, R-11 |
| the refund call answered a transient error, the first time | sends the refund once more | R-07 |
| the refund call returned a failed refund, or answered a second transient error | hands the case to staff (refund not issued), then says the order is cancelled but the refund was not issued | R-07, R-11, R-09 |
| the refund call answered order not cancelled | hands the case to staff (refund not issued), then says the refund was not issued | R-07, R-11, R-09 |
| the refund call got no answer, the first time | sends the refund once more | R-07 |
| the refund was sent once more after getting no answer, whatever the second call answered | re-reads the refund | R-07 |
| the re-read of the refund got no answer | re-reads the refund again | R-07 |
| the re-read shows a pending or issued refund for the confirmed amount and payment method | tells the customer the order is cancelled, with the refund's amount, payment method, status and refund id | R-07, R-09 |
| the re-read shows a refund with a different amount or payment method | hands the case to staff (refund status unknown), then tells the customer the amount and payment method the order system returned | R-10, R-11 |
| the re-read shows a failed refund or no refund | hands the case to staff (refund not issued), then says the order is cancelled but the refund is not confirmed yet | R-07, R-11 |
| the re-read of the refund failed | hands the case to staff (refund status unknown), then says the order is cancelled but the refund's status is not known | R-07, R-11 |
| the handoff call got no answer, the first time | sends the handoff call once more | R-11 |
| the handoff call got no answer twice | tells the customer what it knows, and to contact Harbor Goods support | R-11 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | When the refund the order system returns differs from the confirmed amount or payment method, the agent makes no further change, tells the customer what the order system returned, and hands the case to staff. | the owner, accepting the recommendation | A second change with a value the customer never said yes to would move money without permission. |
| D-02 | The customer may cancel more than one order in one conversation, each with its own proposal and its own yes. | the owner, accepting the recommendation | A yes for one order could otherwise be read as covering another. |
| D-03 | When the refund call answers order not cancelled, the agent sends no further refund call, says the refund was not issued, and hands the case to staff. | the owner, accepting the recommendation | The agent cannot fix the order system's view of the order; staff can. |
| D-04 | When the cancel call answers order not found, the agent says it could not find the order, cancels nothing more and issues no refund. | the owner, accepting the recommendation | A refund for an order that was not cancelled would give money back for goods that still ship. |
| D-05 | When the cancel and the refund succeed, the agent reports the refund as the order system returned it: amount, payment method, status and refund id. | the owner, accepting the recommendation | The customer's message then matches the refund record. |
| D-06 | Reads of the orders are retried on timeout without limit. | the owner | The owner declined a bound of 3 tries: "Reads may be retried on timeout without limit; only commit calls are bounded." |
| D-07 | When the second cancel call also gets no answer and the order still shows open, the agent sends no third cancel call, says the order could not be cancelled right now with no refund issued, and hands the case to staff. | the owner, accepting the recommendation | A third cancel call is not covered by the owner's "send the cancel once more"; staff can finish the cancel. |
| D-08 | A refund that differs from the confirmed one goes to staff with the reason refund status unknown. | the owner, accepting the recommendation | The handoff call takes one of three reasons, and the refund's correctness is what is not known. |
| D-09 | A staff follow-up call that times out is retried once; after a second timeout the agent tells the customer to contact Harbor Goods support. | the owner | The owner's later confirmation of the tools replaced "handoff timeout not retried" with "On timeout, retry once". |
