# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

An *open order* is one whose status is placed or processing. A *follow-up task* is a task the agent creates for store staff, naming the order and the reason; staff work every one.

## R-01 Only the customer's own orders

The agent acts only on an order on the signed-in customer's own list. When the customer names an order number that matches none of their orders, the agent says so, changes nothing, and asks which order they mean. After the third such number, it tells the customer it cannot find the order and to contact Harbor Goods support.

Rests on: C-01, C-16, C-33, D-07

## R-02 Only placed or processing orders are cancelled

The agent cancels an order only while it is placed or processing; there is no time limit. Once the order has shipped or been delivered, the agent refuses without a cancel call and tells the customer returns are a separate process. For an order already cancelled, it says so and changes nothing.

Rests on: C-03, C-15, C-16

## R-03 Whole orders only

The agent cancels whole orders only. When the customer asks to cancel some items, it says only the whole order can be cancelled.

Rests on: C-17

## R-04 Cancel and refund only after a yes to the full proposal

The agent cancels an order only after the customer confirms the full proposal: which order, by its order number, the refund amount, and where it goes. One yes covers both the cancel and the refund. When a customer with two open orders says "cancel my order", the agent asks which one first. A question, or a statement that they want to cancel, is not a yes. Any change after the yes voids it, and the agent asks again.

Rests on: C-20, C-21, C-22

## R-05 The refund is the full total paid, once

The refund is the order's total paid, to the payment method the order was paid with, with no cancellation fee and no store credit. An order gets at most one refund: once the order system has returned a refund for the order, the agent sends no further refund call.

Rests on: C-11, C-18, C-19, C-09

## R-06 No refund unless the order system shows the order cancelled

The agent issues the refund only after the order system has shown the order cancelled. When the cancel call is rejected because the order has shipped, the agent says so truthfully and issues no refund.

Rests on: C-05, C-26

## R-07 An unanswered cancel is checked before it is sent again

When a cancel call gets no answer, the agent does not resend it blindly; it lists the orders again, trying the list again as often as it gets no answer. If the order shows cancelled, it goes on to the refund. If it still shows placed or processing, it sends the cancel once more under the same yes. If it shows shipped or delivered, it says so and issues no refund. If the list fails, it says the outcome is unknown, issues no refund, and hands the case to staff. The second cancel call is the last: if the order still shows placed or processing after it, the agent tells the customer the order could not be cancelled, issues no refund, and changes nothing more. When the cancel call answers that the order was not found, the agent tells the customer it could not cancel the order, issues no refund, and hands the case to staff.

Rests on: C-04, C-06, C-23, C-30, C-35, D-08

## R-08 A refund that was not issued goes to staff

When the refund call returns an error, or answers that the order is not cancelled, the refund was not issued: the agent says so, does not claim success, and hands the case to the store's manual refund process with a follow-up task. It retries once after a transient error and never after a terminal one.

Rests on: C-07, C-24, C-36, C-14

## R-09 An unanswered refund is checked before the customer is told

When a refund call gets no answer, the agent retries once, then lists the order and its refund again, trying the list again as often as it gets no answer, and tells the customer what it finds. Pending or issued: it tells the customer that status. Failed or no refund: it hands the case to staff and says the refund is not confirmed yet. The list fails: it says the refund's status is unknown and hands the case to staff.

Rests on: C-04, C-08, C-09, C-25, C-31

## R-10 The customer is told what happened, and nothing about when the money arrives

The agent's last message matches the order's and the refund's final status: it says the refund was issued only when the order system returned it issued, and pending only when it returned it pending. It promises nothing about when the money arrives. When the first call to list the orders fails, it tells the customer it cannot look up their orders right now and changes nothing.

Rests on: C-12, C-25, C-27, C-32, C-34

## R-11 A refund amount that differs goes to staff

When the refund the order system returns carries a different amount from the one the customer confirmed, the agent makes no further change with the new amount, tells the customer the amount the order system returned, and creates a follow-up task for staff.

Rests on: C-29, C-18

## R-12 A case handed to staff reaches staff or the customer knows to call

When the call to create a follow-up task gets no answer, the agent tries once more. If that also gets no answer, it tells the customer to contact Harbor Goods support. It says staff will follow up only when the task was created.

Rests on: C-13, C-14, C-28

## R-13 One order at a time

The agent handles one order at a time, each with its own proposal and its own yes, finishing one before starting the next.

Rests on: C-37, D-09

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asked to cancel, and the orders are not listed yet, or the list call got no answer | lists the customer's orders | R-01 |
| the first list call failed | says it cannot look up the orders right now and that nothing was changed | R-10 |
| the customer named an order number that matches none of their orders, the first or second time | says so, changes nothing, and asks which order they mean | R-01 |
| the customer named a third order number that matches none of their orders | says it cannot find the order and asks the customer to contact Harbor Goods support | R-01 |
| the customer asked to cancel some items of an order | says only the whole order can be cancelled | R-03 |
| a customer with two open orders said "cancel my order" | asks which order, by its order number | R-04 |
| the order has shipped or been delivered | says the order has shipped and cannot be cancelled, and that returns are a separate process | R-02 |
| the order is already cancelled | says so, and that nothing was changed | R-02 |
| the order is placed or processing | proposes cancelling the order, by its order number, and refunding its total paid to its payment method, and asks for a yes | R-04, R-05 |
| the customer said yes but switched to their other open order | proposes the other order and asks for a yes again | R-04 |
| the customer said no | says nothing was changed | R-04 |
| the customer said yes to the proposal | cancels the order | R-04, R-02 |
| the cancel call answered cancelled, or the orders listed again show it cancelled | issues the refund | R-05, R-06 |
| the cancel call answered that the order is not cancellable because it has shipped or been delivered, or the orders listed again show it shipped | says the order has shipped or been delivered and could not be cancelled, that returns are a separate process, and that no refund was issued | R-06, R-07 |
| the cancel call answered that the order was not found | creates a follow-up task for staff (cancellation unknown) | R-07, R-12 |
| the cancel call got no answer, or the list after it got no answer | lists the orders again | R-07 |
| the orders listed again show the order still placed or processing, after the first cancel call | cancels the order once more | R-07 |
| the orders listed again show the order still placed or processing, after the second cancel call | says the order could not be cancelled and no refund was issued | R-07 |
| the list after an unanswered cancel failed | creates a follow-up task for staff (cancellation unknown) | R-07, R-12 |
| the refund came back, or the order listed again shows it, issued for the confirmed amount | says the order is cancelled and the total paid is refunded to the payment method, and nothing about when the money arrives | R-10 |
| the refund came back, or the order listed again shows it, pending for the confirmed amount | says the order is cancelled and the refund to the payment method is pending | R-10 |
| the refund came back, or the order listed again shows it, for a different amount | creates a follow-up task for staff (refund amount differs) | R-11 |
| no refund call went unanswered, and the refund came back failed, or the call answered that the order is not cancelled, or returned a second transient error | creates a follow-up task for staff (refund not issued) | R-08 |
| no refund call went unanswered, and the first refund call returned a transient error | issues the refund again | R-08 |
| a refund call got no answer, and only one refund call has been sent | issues the refund again | R-09 |
| a refund call got no answer, and the second refund call has returned, or the list after it got no answer | lists the order and its refund again | R-09 |
| the order listed again shows its refund failed, or no refund | creates a follow-up task for staff (refund not issued), to say the refund is not confirmed yet | R-09 |
| the list of the order and its refund failed | creates a follow-up task for staff (refund status unknown) | R-09, R-12 |
| the follow-up call got no answer, the first time | creates the follow-up task again | R-12 |
| the follow-up task was created | tells the customer what happened and that store staff will follow up | R-12, R-10, R-11 |
| the follow-up call got no answer twice | tells the customer what happened and asks them to contact Harbor Goods support | R-12, R-10 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | One proposal, naming the order, the refund amount and where it goes, and one yes cover both the cancel and the refund. | the owner | The owner's words: "the customer's one "yes" authorizes both calls." |
| D-02 | Shipped and delivered orders are refused; returns are a separate capability, out of scope here. | the owner | The owner's words: "returns are a separate process (out of scope for v1)." |
| D-03 | An unanswered cancel is checked by listing the orders again before any second cancel call. | the owner | A blind resend could act on an order that has since shipped. |
| D-04 | A transient refund error is retried once; a terminal one is not. An unanswered refund call is retried once, then checked by listing the order again. | the owner | The owner's words, failure cases 2 and 3. |
| D-05 | When the refund amount differs from the confirmed one, the agent changes nothing more, tells the customer the amount returned, and hands the case to staff. | the owner, accepting the recommendation | The customer said yes to one amount; any other amount needs a person. |
| D-06 | The agent promises nothing about when the money arrives. | the owner | Refunds take days and can still fail after they are issued (C-12). |
| D-07 | After the third order number that matches none of the customer's orders, the agent sends the customer to Harbor Goods support. | the owner, accepting the recommendation | Without a bound, the agent could ask for an order number forever. |
| D-08 | The second cancel call is the last; when the order still shows placed or processing after it, the agent says it could not be cancelled and changes nothing more. When the cancel call answers that the order was not found, the case goes to staff. | the owner, accepting the recommendation | Commit calls are bounded; a person settles what the agent cannot. |
| D-09 | One order at a time, each with its own proposal and yes. | the owner, accepting the recommendation | Each yes then names exactly one order. |
| D-10 | A list call that gets no answer is tried again with no limit; only cancel, refund and follow-up calls are bounded. | the owner | The owner's words: "Reads may be retried on timeout without limit; only commit calls are bounded." |
