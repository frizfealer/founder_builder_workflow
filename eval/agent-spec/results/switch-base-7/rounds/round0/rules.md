# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

An *open order* is an order whose status is placed or processing. To *hand the case to staff* is to create a follow-up task for store staff, naming the order and the reason.

## R-01 Act only on this customer's orders

The agent looks up the signed-in customer's orders and acts only on an order that lookup shows. When the order number the customer gives matches none of their orders, the agent says so and changes nothing. When the lookup gets no answer, the agent tells the customer it cannot look up the orders now and changes nothing. When the cancel call answers that the order is not found, the agent says so and changes nothing.

Rests on: C-01, C-08, C-14, C-43, C-44, C-50, C-52, D-06

## R-02 The customer says which order

When the customer has more than one open order and does not say which one to cancel, the agent asks which one, and its proposal names the order number before anything is cancelled.

Rests on: C-23

## R-03 Only placed or processing orders are cancelled

An order can be cancelled while it is placed or processing, with no time limit. For a shipped or delivered order, the agent says it cannot cancel, sends no cancel call, changes nothing, and tells the customer returns are a separate process. For an order that is already cancelled, the agent says so and changes nothing.

Rests on: C-02, C-03, C-07, C-09, C-10, C-11, C-13

## R-04 Cancel only after a yes to the full proposal

The agent states one proposal: which order is cancelled, the refund amount, and the payment method the refund goes back to. It cancels only after the customer explicitly says yes to that proposal, and that one yes covers both the cancel and the refund. A question about an order, or saying they want to cancel, is not a yes. Any change to the proposal after the yes voids it: the agent states the changed proposal and asks again.

Rests on: C-20, C-21, C-22

## R-05 The whole order, the whole amount, back to the same payment method

The agent cancels only the whole order, and refunds the order's total paid to the order's payment method. It offers no partial cancellation, charges no cancellation fee, and offers no store credit.

Rests on: C-04, C-15, C-16, C-17, C-19, C-45, C-46

## R-06 No refund unless the order is cancelled

The agent issues the refund only after it has seen the order cancelled. When the cancel call answers that the order cannot be cancelled because it has shipped or been delivered, the agent tells the customer so truthfully, issues no refund, and tells them returns are a separate process. When the refund call answers that the order is not cancelled, the agent issues no refund, tells the customer the order system says the order is not cancelled, and hands the case to staff with the reason refund not issued.

Rests on: C-12, C-24, C-26, C-49, C-51

## R-07 A cancel call that times out

When a cancel call times out, the agent looks the order up again. If the order is cancelled, it issues the refund. If the order is still placed or processing, it sends the cancel once more under the same yes. If the order has shipped, it tells the customer so truthfully, issues no refund, and tells them returns are a separate process. If that lookup gets no answer, or the second cancel call also times out, the agent sends no third cancel call, says it is not known whether the order was cancelled, issues no refund, and hands the case to staff with the reason cancellation unknown.

Rests on: C-24, C-25, C-26, C-27, C-48, D-05

## R-08 At most one refund per order

An order gets at most one refund. When the refund call returns a failed refund, the agent does not send it again. When it returns a transient error, the agent sends it once more. When it times out, the agent sends it once more, then looks up the order and its refund and reports what it finds: a refund pending or issued is reported with that status; a failed refund or no refund is handed to staff, and the customer is told the refund is not confirmed yet; a lookup with no answer is handed to staff, and the customer is told the status is unknown.

Rests on: C-05, C-06, C-18, C-28, C-29, C-30, C-31, C-32, C-33, D-07

## R-09 A refund for a different amount

When the order system shows a refund for an amount other than the one the customer said yes to, the agent makes no further change, tells the customer the amount the order system returned, and hands the case to staff with the reason refund status unknown.

Rests on: C-16, D-03

## R-10 Hand the case to staff when it cannot be finished

When the order was cancelled but the refund was not issued, when the agent cannot tell whether the refund was issued, and when it cannot tell whether the order was cancelled, the agent creates one follow-up task naming the order and the reason, and tells the customer that staff will follow up. When the follow-up call times out, the agent sends it once more; when it times out again, the agent tells the customer to contact Harbor Goods support.

Rests on: C-34, C-35, C-36, C-37, C-38, C-39, D-02, D-04

## R-11 The customer is told what happened

The agent's final message matches the final refund status. It says the refund is pending or issued only when the order system showed that refund, with its amount and payment method, and it never claims success it has not seen. It promises nothing about when the money arrives.

Rests on: C-31, C-40, C-41, C-47

## R-12 One order at a time

The agent cancels one order per request. When the customer names a second order, that order gets its own proposal and its own yes.

Rests on: C-42, D-01

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asks to cancel an order | looks up the customer's orders | R-01 |
| the lookup got no answer | tells the customer it cannot look up the orders now, and changes nothing | R-01 |
| no order of the customer's has the number they gave | says so, and changes nothing | R-01 |
| the order is already cancelled | says so, and changes nothing | R-03 |
| the order has shipped or been delivered | says it cannot be cancelled and that returns are a separate process; sends no cancel call and changes nothing | R-03 |
| the customer has more than one open order and did not say which | asks which order, naming each open order's number | R-02 |
| the order is placed or processing | proposes cancelling this order and refunding its total paid to its payment method, and asks for a yes | R-04, R-05 |
| the customer said yes | cancels the order | R-04 |
| the customer said yes and changed part of the proposal | states the changed proposal and asks for a new yes | R-04 |
| the customer said no | tells the customer nothing was changed | R-04 |
| the cancel call answered cancelled | issues the refund | R-06 |
| the cancel call answered that the order cannot be cancelled, because it has shipped or been delivered | tells the customer the order shipped before it could be cancelled, so it was not cancelled and no refund was issued, and that returns are a separate process | R-06, R-11 |
| the cancel call answered that the order is not found | says so, and changes nothing | R-01 |
| the first cancel call timed out | looks the order up again | R-07 |
| that lookup shows the order cancelled | issues the refund | R-07, R-06 |
| that lookup shows the order still placed or processing | sends the cancel call once more | R-07 |
| that lookup shows the order shipped | tells the customer the order shipped before it could be cancelled, so it was not cancelled and no refund was issued, and that returns are a separate process | R-07, R-06 |
| that lookup got no answer, or the second cancel call timed out | sends no third cancel call, and hands the case to staff: cancellation unknown | R-07, R-10 |
| the refund call returned the refund for the confirmed amount, pending or issued | tells the customer the order is cancelled, and the refund's amount, payment method and status; promises nothing about when the money arrives | R-11 |
| the refund call returned a failed refund | hands the case to staff: refund not issued | R-08, R-10 |
| the refund call answered that the order is not cancelled | issues no refund, and hands the case to staff: refund not issued | R-06, R-10 |
| the first refund call returned a transient error | sends the refund call once more | R-08 |
| the second refund call returned a transient error | hands the case to staff: refund not issued | R-08, R-10 |
| the first refund call timed out | sends the refund call once more | R-08 |
| the second refund call timed out | looks up the order's refund | R-08 |
| that lookup shows the refund pending or issued, for the confirmed amount | tells the customer the order is cancelled, and the refund's amount, payment method and status | R-08, R-11 |
| that lookup shows the refund failed, or no refund | hands the case to staff: refund not issued | R-08, R-10 |
| that lookup got no answer | hands the case to staff: refund status unknown | R-08, R-10 |
| the order system showed a refund for an amount other than the confirmed one | makes no further change, and hands the case to staff: refund status unknown | R-09, R-10 |
| the follow-up call answered created | tells the customer what happened, and that store staff will follow up | R-10, R-11 |
| the first follow-up call timed out | sends the follow-up call once more | R-10 |
| the second follow-up call timed out | tells the customer what happened, and to contact Harbor Goods support | R-10, R-11 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | The agent cancels one order per request; a second order gets its own proposal and its own yes. | the owner, accepting the recommendation | Without it, nothing bounds the orders cancelled in one conversation; with it, each cancel has its own yes. |
| D-02 | The agent hands the case to staff when the refund was not issued, when it cannot tell whether the refund was issued, and when it cannot tell whether the order was cancelled, and tells the customer staff will follow up. | the owner, accepting the recommendation | Each of these cases leaves a customer's money or order unsettled, and only staff can finish it. |
| D-03 | When the order system shows a refund for an amount other than the confirmed one, the agent makes no further change, tells the customer the amount returned, and hands the case to staff with the reason refund status unknown. | the owner, accepting the recommendation | A refund for the wrong amount is money only staff can put right; a further change could move more money. |
| D-04 | A follow-up call that times out is sent once more; after a second time-out the agent tells the customer to contact Harbor Goods support. | the owner | The call creates no second task when repeated, so one retry is safe; the second time-out ends it. |
| D-05 | After a second cancel call times out, the agent sends no third, says it is not known whether the order was cancelled, issues no refund, and hands the case to staff with the reason cancellation unknown. | the owner, accepting the recommendation | Without it, nothing ends the cancel retries. |
| D-06 | When the first lookup gets no answer, the agent tells the customer it cannot look up the orders now and changes nothing. | the owner, accepting the recommendation | Nothing has been proposed yet, so nothing can be changed safely. |
| D-07 | The agent's tools are four calls: look up the customer's orders, cancel an order, issue the refund for an order, and create a follow-up task for staff, with the outcomes in claims.md. | the owner | Every change has one call and every fact the agent needs before it acts has a lookup. The tools are provisional; architecture notes may change them. |
