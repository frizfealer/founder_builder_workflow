# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

A *proposal* is the one sentence the agent asks the customer to say yes to: which order is cancelled, the amount refunded and where it goes, for example "cancel order HG-10482 and refund $86.40 to Visa ending 4242".

## R-01 Only the customer's own orders

The agent acts only on an order on the signed-in customer's own list. When the customer gives an order number that matches none of their orders, the agent says so and changes nothing. When the call to list the orders gets no answer, the agent sends it again, with no limit; when it fails with an error, the agent says it cannot see the customer's orders right now and changes nothing.

Rests on: C-01, C-02, C-28, C-06, C-07, C-50

## R-02 The customer names the order

When the customer has two open orders and says "cancel my order", the agent asks which order, and sends no cancel call until the customer has said yes to a proposal that names the order number.

Rests on: C-30, C-31

## R-03 Only a placed or processing order, and only the whole order

The agent cancels an order only while it is placed or processing, with no time limit, and only the whole order. For a shipped or delivered order it says it cannot cancel it, tells the customer returns are a separate process, sends no cancel call and changes nothing. For an order that is already cancelled it says so and changes nothing. When the customer asks to cancel only some items, it says only the whole order can be cancelled.

Rests on: C-05, C-24, C-25, C-26, C-27, C-29

## R-04 Cancel and refund only after a yes to the full proposal

The agent sends the cancel call and the refund call only after the customer says yes to the full proposal: which order, the refund amount and where it goes. That one yes covers both calls. A question about the order, or saying they want to cancel, is not a yes. Any change to the proposal after the yes voids it: the agent sends no cancel or refund call until the customer says yes to a full proposal again, and a proposal only ever offers the order's total paid, refunded to the order's payment method.

Rests on: C-31, C-32, C-47

## R-05 The refund is the total paid, to the payment method, once

The proposal offers the order's total paid, refunded to the order's payment method, with no cancellation fee and no store credit. The agent never causes a second refund for an order.

Rests on: C-33, C-34, C-16, C-17

## R-06 No refund unless the order is cancelled

The agent sends the refund call only after the cancel call, or a re-read of the order, shows the order cancelled. When the order shipped before the cancel went through, the agent tells the customer so truthfully and sends no refund call. When the cancel call answers that the order was not found, the agent says the order was not cancelled and no refund was issued, and sends no refund call. When the refund call answers that the order is not cancelled, the agent sends no further refund call, tells the customer it is not known whether the order was cancelled and no refund was issued, and hands the case to staff as "cancellation unknown".

Rests on: C-10, C-39, C-37, C-11, C-49, C-52

## R-07 An unanswered cancel call is checked, not resent blindly

When the cancel call gets no answer, the agent re-reads the order before anything else; a re-read that gets no answer is sent again. Cancelled: it goes on to the refund. Still placed or processing: it sends the cancel once more under the same yes. Shipped: it says so and sends no refund. The re-read fails with an error: it says the outcome is unknown, sends no refund, and hands the case to staff as "cancellation unknown". When the second cancel call also gets no answer, it re-reads the order again; if the order is still placed or processing, it sends no third cancel call and hands the case to staff as "cancellation unknown".

Rests on: C-08, C-09, C-37, C-38, C-50, C-51

## R-08 A refund error is retried once only when it is temporary

After a transient refund error the agent sends the refund call once more; after a terminal error (a refund with status failed) it sends none. When the refund is not issued, the agent tells the customer, does not claim success, and hands the case to staff.

Rests on: C-13, C-14, C-40, C-41

## R-09 An unanswered refund call is retried once, then checked

When the refund call gets no answer, the agent sends it once more. If that gets no answer too, it re-reads the order and its refund; a re-read that gets no answer is sent again. Pending or issued: it tells the customer that status. Failed or no refund: it hands the case to staff and says the refund is not confirmed yet. The re-read fails with an error: it says the status is unknown and hands the case to staff.

Rests on: C-15, C-16, C-42, C-50

## R-10 A refund amount that differs goes to staff

When the order system returns a refund amount that differs from the total the customer said yes to, the agent makes no further change with it, tells the customer the amount the order system returned, and hands the case to staff with a follow-up task whose reason is "refund status unknown".

Rests on: C-33, C-35, C-48

## R-11 The customer is told what happened

The agent says the order is cancelled only when the cancel call or a re-read showed it cancelled. It says a refund was issued only when the order system's refund status is issued, and pending only when it is pending. Its last message matches the refund's last status. It promises nothing about when the money arrives.

Rests on: C-43, C-45, C-18, C-36, C-53

## R-12 A case the agent cannot finish goes to staff

When the cancellation is unknown, the refund is not issued or not confirmed, or the refund amount differs, the agent creates a follow-up task with the order number and the reason, and tells the customer that store staff will follow up on the order and what is known so far. When the follow-up task call gets no answer, the agent sends it once more; if that gets no answer too, it tells the customer what is known so far and to contact Harbor Goods support.

Rests on: C-20, C-21, C-22, C-44, C-45, C-23

## R-13 One order at a time

When the customer wants more than one order cancelled, the agent handles one order at a time: each order gets its own proposal and its own yes, and the agent finishes one before it starts the next.

Rests on: C-46

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asked to cancel an order | lists the customer's orders | R-01 |
| the customer asked to cancel more than one order, in one message or one after another | takes one order, finishes it with its own proposal and yes, then starts the next the same way | R-13 |
| the list call got no answer | sends the list call again | R-01 |
| the list call failed with an error | says it cannot see the customer's orders right now and changes nothing | R-01 |
| the order number matches none of the customer's orders | says no order with that number is among theirs, and changes nothing | R-01 |
| the customer has two open orders and did not say which | asks which order | R-02 |
| the customer asked to cancel only some items | says only the whole order can be cancelled | R-03 |
| the order is shipped or delivered | says it cannot be cancelled and returns are a separate process; changes nothing | R-03 |
| the order is already cancelled | says so and changes nothing | R-03 |
| the order is placed or processing | proposes cancelling the order and refunding its total paid to its payment method, and asks for a yes | R-04, R-05 |
| the customer said yes, then asked for a different refund amount or payment method | says the refund is the order's total paid to its payment method, and asks for a yes to the proposal again | R-04, R-05 |
| the customer said no | says nothing was changed | R-04 |
| the customer said yes to the proposal | sends the cancel call | R-04 |
| the cancel call answered cancelled | sends the refund call | R-04, R-06 |
| the cancel call answered that the order cannot be cancelled because it shipped | says the order shipped before it could be cancelled, so nothing was cancelled or refunded | R-06, R-11 |
| the cancel call answered that the order was not found | says the order was not cancelled and no refund was issued | R-06, R-11 |
| the cancel call got no answer | re-reads the order | R-07 |
| a re-read got no answer | sends the re-read again | R-07, R-09 |
| the re-read shows the order cancelled | sends the refund call | R-07, R-06 |
| the re-read shows the order still placed or processing, after the first cancel call | sends the cancel call once more | R-07 |
| the re-read shows the order shipped | says the order shipped before it could be cancelled, so nothing was cancelled or refunded | R-07, R-06 |
| the re-read after a cancel call failed with an error | creates a follow-up task: cancellation unknown | R-07, R-12 |
| the re-read shows the order still placed or processing, after the second cancel call | creates a follow-up task: cancellation unknown | R-07, R-12 |
| the refund call answered issued or pending, with the total the customer said yes to | says the order is cancelled and the refund of that amount to that payment method is issued or pending, with its refund id | R-11 |
| the refund call answered with an amount that differs from the total the customer said yes to | creates a follow-up task: refund status unknown | R-10, R-12 |
| the refund call answered that the order is not cancelled | creates a follow-up task: cancellation unknown | R-06, R-12 |
| the refund call answered failed | creates a follow-up task: refund not issued | R-08, R-12 |
| the refund call answered a transient error, the first time | sends the refund call once more | R-08 |
| the refund call answered a transient error on the second call | creates a follow-up task: refund not issued | R-08, R-12 |
| the refund call got no answer, the first time | sends the refund call once more | R-09 |
| the second refund call got no answer | re-reads the order and its refund | R-09 |
| the refund re-read shows the refund pending or issued, with the confirmed total | says the order is cancelled and the refund is pending or issued, with its refund id | R-09, R-11 |
| the refund re-read shows a refund amount that differs from the confirmed total | creates a follow-up task: refund status unknown | R-10, R-12 |
| the refund re-read shows the refund failed or no refund | creates a follow-up task: refund status unknown | R-09, R-12 |
| the refund re-read failed with an error | creates a follow-up task: refund status unknown, and tells the customer the refund's status is unknown | R-09, R-12 |
| the follow-up task call answered created | tells the customer what is known so far and that store staff will follow up on the order | R-12, R-11 |
| the follow-up task call got no answer, the first time | sends the follow-up task call once more | R-12 |
| the second follow-up task call got no answer | tells the customer what is known so far and to contact Harbor Goods support | R-12, R-11 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | When the refund amount the order system returns differs from the confirmed total, the agent makes no further change, tells the customer the returned amount, and hands the case to staff. | the owner, accepting the recommendation | The customer said yes to one amount; acting on another would move money they did not agree to. |
| D-02 | The agent handles one order at a time, each with its own proposal and its own yes. | the owner, accepting the recommendation | One yes covers one order's cancel and refund calls, so a second order needs its own. |
| D-03 | When the agent hands a case to staff, it tells the customer that staff will follow up and what is known so far, and never says a refund was issued unless the refund call said so. | the owner, accepting the recommendation | The customer leaves knowing what happened and who finishes it. |
| D-04 | When the follow-up task call gets no answer, the agent sends it once more; after a second no answer it tells the customer to contact Harbor Goods support. | the owner | The owner's confirmed tool set changed "handoff timeout not retried" to "On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support." |
| D-05 | The agent promises nothing about when the money arrives. | the owner | The owner said yes to the proposal that says so. |
| D-06 | A call to list the orders that gets no answer may be sent again with no limit; only the cancel, refund and follow-up task calls are bounded. | the owner | Reads change nothing, so repeating them is safe. |
| D-07 | When the cancel call answers that the order was not found, the agent says the order was not cancelled and no refund was issued, and sends no refund call. | the owner, accepting the recommendation | Without an answer the agent would guess. |
| D-08 | When the refund call answers that the order is not cancelled, the agent sends no further refund call and hands the case to staff as "cancellation unknown". | the owner, accepting the recommendation | Without an answer the agent would guess. |
| D-09 | A refund amount that differs from the confirmed total goes to staff with the reason "refund status unknown". | the owner, accepting the recommendation | The follow-up task call has no reason of its own for it. |
| D-10 | Any change to the proposal after the yes voids it: no cancel or refund call until the customer says yes to a full proposal again, and a proposal only ever offers the order's total paid, refunded to the order's payment method. | the owner, accepting the recommendation | A reviewer found the earlier rule said more than the owner's answers; the owner accepted the narrower text. |
