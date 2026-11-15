# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 Lookup fails
Kind: model path
Rules: R-01
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup fails

## SC-02 Order already shipped or delivered
Kind: model path
Rules: R-02
World:
1. The customer has one order, already shipped or delivered
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders

## SC-03 Order already cancelled
Kind: model path
Rules: R-02
World:
1. The customer has one order, already cancelled
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders

## SC-04 Two or more open orders, one named, lookup fails
Kind: model path
Rules: R-01
World:
1. The customer has two or more orders, none shipped
2. customer asks to cancel an order, naming its number
3. lookup fails

## SC-05 No order named, lookup fails
Kind: model path
Rules: R-01
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel their order without naming one
3. lookup fails

## SC-06 Customer names an order that is not theirs
Kind: model path
Rules: R-01
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order number that is not one of theirs
3. lookup answers with the customer's orders

## SC-07 Lookup gets no answer, then fails
Kind: model path
Rules: R-01
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup gets no answer
4. lookup fails

## SC-08 Customer leaves at the proposal
Kind: model path
Rules: R-04, R-06
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer stops answering

## SC-09 Two or more open orders, none named, customer leaves when asked which
Kind: model path
Rules: R-03
World:
1. The customer has two or more orders, none shipped
2. customer asks to cancel their order without naming one
3. lookup answers with the customer's orders
4. customer stops answering

## SC-10 Order ships between the lookup and the cancel call
Kind: model path
Rules: R-07, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers not cancellable because the order has shipped or been delivered

## SC-11 Customer says no to the proposal
Kind: model path
Rules: R-04, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says no

## SC-12 Customer asks to cancel part of the order
Kind: model path
Rules: R-06, R-05
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer asks to cancel only some items, or to be refunded another way
5. customer stops answering

## SC-13 Customer says yes, then switches to their other order
Kind: model path
Rules: R-05, R-04
World:
1. The customer has two or more orders, none shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes, then asks to cancel their other order instead
5. customer stops answering

## SC-14 Two or more open orders, customer names one when asked
Kind: model path
Rules: R-03, R-04
World:
1. The customer has two or more orders, none shipped
2. customer asks to cancel their order without naming one
3. lookup answers with the customer's orders
4. customer names an order not yet shipped
5. customer stops answering

## SC-15 Cancelled and refunded as agreed
Kind: model path
Rules: R-04, R-07, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund as agreed, pending or issued

## SC-16 Cancel call unanswered, re-read shows it cancelled
Kind: model path
Rules: R-07, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. re-read shows the order cancelled
7. refund call answers with a refund as agreed, pending or issued

## SC-17 Cancel call answers order not found
Kind: model path
Rules: R-07, R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers order not found
6. task call answers created

## SC-18 Cancel call unanswered, re-read shows it shipped
Kind: model path
Rules: R-07, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (not cancelled)
6. re-read shows the order shipped or delivered

## SC-19 Refund differs from what was agreed
Kind: model path
Rules: R-10, R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund whose amount or payment method differs
7. task call answers created

## SC-20 Refund failed
Kind: model path
Rules: R-08, R-11, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a failed refund
7. task call answers created

## SC-21 Temporary refund error, retry succeeds
Kind: model path
Rules: R-08, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error, no refund made
7. refund call answers with a refund as agreed, pending or issued

## SC-22 Refund call answers the order is not cancelled
Kind: model path
Rules: R-08, R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers that the order is not cancelled
7. task call answers created

## SC-23 Refund call unanswered though made, retry returns it
Kind: model path
Rules: R-08, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund made)
7. refund call answers with the refund that exists

## SC-24 Refund call unanswered, a failed refund was made
Kind: model path
Rules: R-08, R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (failed refund made)
7. refund call answers with the refund that exists
8. task call answers created

## SC-25 Refund call unanswered, nothing made, retry succeeds
Kind: model path
Rules: R-08, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (no refund made)
7. refund call answers with a refund as agreed, pending or issued

## SC-26 Re-read of the order unanswered, then shows it cancelled
Kind: model path
Rules: R-07
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. re-read of the order gets no answer
7. re-read shows the order cancelled
8. refund call answers with a refund as agreed, pending or issued

## SC-27 Re-read of the order fails after an unanswered cancel
Kind: model path
Rules: R-07, R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. re-read of the order fails
7. task call answers created

## SC-28 Task call unanswered once, then created
Kind: model path
Rules: R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers order not found
6. task call gets no answer (task created)
7. task call answers created

## SC-29 Task call unanswered with no task made, then created
Kind: model path
Rules: R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers order not found
6. task call gets no answer (no task created)
7. task call answers created

## SC-30 Second cancel call after a re-read, order has shipped
Kind: model path
Rules: R-07, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (not cancelled)
6. re-read shows the order still placed or processing
7. cancel call answers not cancellable because the order has shipped or been delivered

## SC-31 Temporary error, then no answer, re-read shows the refund
Kind: model path
Rules: R-08, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error, no refund made
7. refund call gets no answer (refund made)
8. re-read shows the refund, pending or issued

## SC-32 Task call unanswered twice after order not found
Kind: model path
Rules: R-11, R-07
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers order not found
6. task call gets no answer (task created)
7. task call gets no answer (task created)

## SC-33 Re-read of the refund unanswered, then shows it
Kind: model path
Rules: R-08, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error, no refund made
7. refund call gets no answer (refund made)
8. re-read of the refund gets no answer
9. re-read shows the refund, pending or issued

## SC-34 Re-read of the refund fails
Kind: model path
Rules: R-08, R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error, no refund made
7. refund call gets no answer (refund made)
8. re-read of the refund fails
9. task call answers created

## SC-35 Re-read shows the refund failed
Kind: model path
Rules: R-08, R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error, no refund made
7. refund call gets no answer (failed refund made)
8. re-read shows the refund failed
9. task call answers created

## SC-36 Re-read shows no refund
Kind: model path
Rules: R-08, R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error, no refund made
7. refund call gets no answer (no refund made)
8. re-read shows no refund
9. task call answers created

## SC-37 Refund differs and the task call is unanswered twice
Kind: model path
Rules: R-10, R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund whose amount or payment method differs
7. task call gets no answer (task created)
8. task call gets no answer (task created)

## SC-38 Refund failed and the task call is unanswered twice
Kind: model path
Rules: R-11, R-09
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a failed refund
7. task call gets no answer (task created)
8. task call gets no answer (task created)

## SC-39 Order not cancelled per the refund call, task call unanswered twice
Kind: model path
Rules: R-11, R-08
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers that the order is not cancelled
7. task call gets no answer (task created)
8. task call gets no answer (task created)

## SC-40 Cancellation unknown, task call unanswered twice
Kind: model path
Rules: R-11, R-07
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. re-read of the order fails
7. task call gets no answer (task created)
8. task call gets no answer (task created)

## SC-41 Refund status unknown, task call unanswered twice
Kind: model path
Rules: R-11, R-08
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error, no refund made
7. refund call gets no answer (refund made)
8. re-read of the refund fails
9. task call gets no answer (task created)
10. task call gets no answer (task created)

## SC-42 Refund not confirmed, task call unanswered twice
Kind: model path
Rules: R-11, R-08
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error, no refund made
7. refund call gets no answer (failed refund made)
8. re-read shows the refund failed
9. task call gets no answer (task created)
10. task call gets no answer (task created)

## SC-43 Customer cancels a second order after the first
Kind: conversational
Rules: R-12, R-04
Why not a path: the model is one order per run; a second order named after the first is done starts a new run with its own proposal and yes.

## SC-44 Two orders named in one message
Kind: conversational
Rules: R-12, R-03, R-04
Why not a path: the model has the customer ask about one order at a time; asking to cancel two orders in one message needs the agent to take them one per proposal.

## SC-45 A question about cancelling is not a yes
Kind: conversational
Rules: R-04
Why not a path: the model's customer steps are a yes, a no or a change; it cannot express a message that asks whether an order can be cancelled, or says the customer wants to, without saying yes.

## SC-46 Customer asks when the money will arrive
Kind: conversational
Rules: R-09
Why not a path: the model does not hold what the agent says about timing; the agent must promise nothing about when the money arrives.

## SC-47 Customer asks for store credit or to waive a fee
Kind: conversational
Rules: R-06
Why not a path: the model has no store credit or fee; the agent offers neither and keeps to the full refund to the payment method used.

## SC-48 Open and shipped order, one named, lookup fails
Kind: model path
Rules: R-01
World:
1. The customer has one order not yet shipped and one shipped
2. customer asks to cancel an order, naming its number
3. lookup fails

## SC-49 Customer has no orders
Kind: model path
Rules: R-03
World:
1. The customer has no orders
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders

## SC-50 Open and shipped order, none named, customer picks the shipped one
Kind: model path
Rules: R-03, R-02
World:
1. The customer has one order not yet shipped and one shipped
2. customer asks to cancel their order without naming one
3. lookup answers with the customer's orders
4. customer names the shipped order

## SC-51 Refund call unanswered, a refund that differs was made
Kind: model path
Rules: R-08, R-10, R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund that differs made)
7. refund call answers with the refund that exists
8. task call answers created

## SC-52 Re-read shows a refund that differs
Kind: model path
Rules: R-08, R-10, R-11
World:
1. The customer has one order, not yet shipped
2. customer asks to cancel an order, naming its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error, no refund made
7. refund call gets no answer (refund that differs made)
8. re-read shows a refund whose amount or payment method differs
9. task call answers created
