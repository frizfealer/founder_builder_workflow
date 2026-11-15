# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

An *open order* is an order whose status is placed or processing: one the store still lets the customer cancel. A *follow-up* is a task the agent creates for store staff, with the order number and a reason; it is the store's way of handing a case to staff.

## R-01 Only the signed-in customer's orders

The agent looks up, proposes and cancels only orders of the customer who is signed in. When the order number the customer gives matches none of their orders, it says so and changes nothing.

Rests on: C-01, C-02, C-29

## R-02 Cancel only an open order

The agent cancels an order only while it is placed or processing. For a shipped or delivered order it says it cannot cancel it, tells the customer returns are a separate process, and changes nothing, with no cancel call. For an order that is already cancelled it says so and changes nothing. When the order system shows the order has shipped since the lookup, the agent tells the customer so and issues no refund.

Rests on: C-05, C-08, C-09, C-20, C-21, C-22, C-28

## R-03 The whole order or nothing

The agent cancels whole orders only. When the customer asks to cancel some of an order's items, it says only the whole order can be cancelled, and goes on only if the customer then asks to cancel the whole order.

Rests on: C-23, C-24, D-01

## R-04 The customer names the order

When the customer could mean more than one open order, the agent asks which one before it proposes anything. The proposal names the order number.

Rests on: C-30

## R-05 Cancel and refund only after a yes to the full proposal

The agent states one proposal: the order number, the refund amount (the order's total paid) and the payment method it goes back to, such as "cancel order HG-10482 and refund $86.40 to Visa ending 4242". It cancels and refunds only after the customer says yes to that proposal. A question about cancelling, or saying they want to cancel, is not a yes. When the customer changes any part of the proposal after the yes, the yes no longer counts and the agent proposes again.

Rests on: C-25, C-26, C-31, C-32, D-02

## R-06 Refund only a cancelled order

The agent issues the refund only after the order system has shown the order cancelled: the cancel call answered "cancelled", or a lookup after an unanswered cancel call shows it cancelled. When the cancel is rejected, finds no order, or its outcome stays unknown, the agent issues no refund.

Rests on: C-09, C-10, C-25, C-35

## R-07 At most one refund per order

No order gets more than one refund. The refund goes back only to the order's payment method.

Rests on: C-13, C-14, C-25

## R-08 A refund error: one retry, then staff

After a refund call answers with a transient error, the agent tries once more. After a refund with status failed, a second error, or an answer that the order is not cancelled, it makes no further refund call, tells the customer the refund was not issued, and hands the case to staff as "refund not issued". It never says the refund succeeded.

Rests on: C-11, C-17, C-18, C-33, D-04

## R-09 A refund call with no answer: one retry, then look again

After a refund call gets no answer, the agent tries once more. If that call also gets no answer, or answers with an error, it looks up the order and its refund again and tells the customer what it finds. A pending or issued refund: it reports that status. A failed refund or none: it says the refund is not confirmed yet and hands the case to staff. The lookup fails: it says the refund status is unknown and hands the case to staff.

Rests on: C-12, C-13, C-34, C-39, D-05

## R-10 A cancel call with no answer: look before anything else

When the cancel call gets no answer, the agent does not resend it blindly; it looks the order up. Cancelled: it goes on to the refund. Still placed or processing: it sends the cancel once more under the same yes, and never a third time. Shipped: it tells the customer and issues no refund. The lookup fails, or the order is still not cancelled after the second cancel call: it says the outcome is unknown, issues no refund, and hands the case to staff as "cancellation unknown".

Rests on: C-08, C-10, C-35, C-41, D-07

## R-11 The customer is told what happened

The agent says the order is cancelled only when the order system showed it cancelled, and says a refund is pending or issued only when a refund call or a lookup showed that refund, with that status. It says nothing was changed only when nothing was. It promises nothing about when the money arrives.

Rests on: C-06, C-15, C-16, C-27, C-34

## R-12 Every handed-on case reaches staff, or the customer is sent to support

Each case R-08, R-09, R-10 and R-13 hand to staff gets a follow-up with its reason. When the follow-up call gets no answer, the agent tries once more; when that also gets no answer, it tells the customer what happened to the order and the refund, that it could not reach store staff, and to contact Harbor Goods support.

Rests on: C-17, C-18, C-19, C-36, D-03

## R-13 When the refund amount differs from the proposal

When the refund call answers with an amount different from the one the customer said yes to, the agent makes no further change with the new amount, tells the customer the amount the refund call returned, and hands the case to staff as "refund amount differs".

Rests on: C-25, C-40, D-08

## R-14 One order at a time

The agent works on one order at a time. A request to cancel another order gets its own proposal and its own yes.

Rests on: C-37, D-09

## R-15 Lookups may be tried again

When the first lookup of the customer's orders gets no answer, the agent tries it again; the owner set no limit on lookups. Calls that change something (cancel, refund, follow-up) are each sent at most twice.

Rests on: C-07, C-42

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the customer asks to cancel an order | looks up the customer's orders | R-01 |
| the lookup got no answer | looks up the customer's orders again | R-15 |
| the order number matches none of the customer's orders | says so, and changes nothing | R-01 |
| the order has shipped or been delivered | says it cannot cancel it and returns are a separate process, and changes nothing | R-02 |
| the order is already cancelled | says so, and changes nothing | R-02 |
| the customer asked to cancel some items of an open order | says only the whole order can be cancelled, and asks whether to cancel the whole order | R-03 |
| the customer has two open orders and did not say which | asks which order | R-04 |
| the customer named one open order, or has only one | proposes: cancel order <number> and refund <total paid> to <payment method>, and asks for a yes | R-04, R-05 |
| the customer said yes and then named a different order | proposes again for the order now named, and asks for a yes | R-05 |
| the customer withdrew before saying yes | says the order was not cancelled and nothing changed | R-05, R-11 |
| the customer said yes to the proposal | cancels the order | R-05, R-02 |
| the cancel call answered "not cancellable" | says the order has shipped and cannot be cancelled, and that returns are a separate process; no refund | R-02, R-06 |
| the cancel call answered "order not found" | says it could not find the order, and that nothing changed | R-06, R-11 |
| the cancel call got no answer | looks up the order | R-10 |
| the lookup after the cancel shows the order cancelled | issues the refund | R-06, R-10 |
| the lookup after the first cancel call shows the order still placed or processing | cancels the order once more | R-10 |
| the lookup shows the order shipped | says the order has shipped and cannot be cancelled, and that returns are a separate process; no refund | R-02, R-10 |
| the lookup after the cancel got no answer, or the order is still not cancelled after the second cancel call | hands the case to staff as "cancellation unknown", saying the outcome is unknown and no refund was issued | R-10, R-12 |
| the cancel call answered "cancelled" | issues the refund | R-06 |
| the refund call answered with a refund, pending or issued, for the amount proposed | says the order is cancelled and the refund of that amount to that payment method is pending or issued, with no promise of when it arrives | R-11 |
| the refund call answered with an amount different from the proposal | hands the case to staff as "refund amount differs", stating the amount returned | R-13 |
| the refund call answered with a refund whose status is failed, or that the order is not cancelled | hands the case to staff as "refund not issued" | R-08 |
| the first refund call answered with a transient error, and no earlier call got no answer | issues the refund again | R-08 |
| the first refund call got no answer | issues the refund again | R-09 |
| the second refund call answered with a transient error, and no call got no answer | hands the case to staff as "refund not issued" | R-08 |
| the second refund call got no answer, or answered with an error after a call that got no answer | looks up the order and its refund again | R-09 |
| the new lookup shows the refund pending or issued | says the order is cancelled and the refund is pending or issued, with no promise of when it arrives | R-09, R-11 |
| the new lookup shows a failed refund or no refund | hands the case to staff as "refund not issued", saying the refund is not confirmed yet | R-09 |
| the new lookup got no answer | hands the case to staff as "refund status unknown", saying the refund status is unknown | R-09 |
| the follow-up call created the task | tells the customer what happened to the order and the refund, and that store staff will follow up | R-12 |
| the first follow-up call got no answer | sends the follow-up once more | R-12 |
| the second follow-up call got no answer | tells the customer what happened to the order and the refund, that it could not reach store staff, and to contact Harbor Goods support | R-12 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | Only whole orders are cancelled; there is no partial cancellation. | the owner, accepting the recommendation | Recorded: "Q2 Whole order only, or individual items? Recommended: whole order only." |
| D-02 | One yes to one proposal allows both the cancel and the refund. | the owner, accepting the recommendation | The customer confirms once, and the proposal names the order, the amount and where the money goes. |
| D-03 | A handoff to staff is a call that creates a staff task with a reason; a follow-up with no answer is tried once more, then the customer is sent to Harbor Goods support. | the owner | Recorded: "On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support." |
| D-04 | After a refund call answers with a transient error the agent retries once; after a terminal error it does not retry. | the owner | Recorded: "One retry allowed on a transient error, none on a terminal one." |
| D-05 | After a refund call gets no answer the agent retries once, then looks up the order again and reports what it finds. | the owner | Recorded: "agent retries once, then re-reads the order and refund records and reports what it finds." |
| D-06 | A shipped or delivered order is refused with no cancel call; returns are a separate process this agent does not handle. | the owner | Recorded: "returns are a separate process (out of scope for v1)." |
| D-07 | After a cancel call gets no answer the agent looks the order up before anything else, and sends the cancel at most once more. | the owner | Recorded: "no blind resend; re-read the order." |
| D-08 | When the refund amount differs from the proposal, the agent changes nothing more and hands the case to staff. | the owner, accepting the recommendation | A different amount means the customer's yes did not cover what happened. |
| D-09 | The agent works on one order at a time; each order gets its own proposal and yes. | the owner, accepting the recommendation | Each order can be cancelled only once, so the customer's open orders bound the conversation. |
