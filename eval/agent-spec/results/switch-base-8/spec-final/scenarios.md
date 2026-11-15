# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 Order list read fails
Kind: model path
Rules: R-15
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read fails with an error

## SC-02 Order list read fails, customer with two open orders
Kind: model path
Rules: R-15
World:
1. The customer's order is placed or processing, and they have another open order
2. customer asks to cancel the order by its number
3. order list read fails with an error

## SC-03 Shipped order is refused
Kind: model path
Rules: R-03
World:
1. The customer's order is shipped or delivered
2. customer asks to cancel the order by its number
3. order list read answers with the orders

## SC-04 Shipped order is refused, customer with another open order
Kind: model path
Rules: R-03
World:
1. The customer's order is shipped or delivered, and they have another open order
2. customer asks to cancel the order by its number
3. order list read answers with the orders

## SC-05 Order already cancelled
Kind: model path
Rules: R-03
World:
1. The customer's order is already cancelled
2. customer asks to cancel the order by its number
3. order list read answers with the orders

## SC-06 Order already cancelled, customer with another open order
Kind: model path
Rules: R-03
World:
1. The customer's order is already cancelled, and they have another open order
2. customer asks to cancel the order by its number
3. order list read answers with the orders

## SC-07 Order number that is none of the customer's
Kind: model path
Rules: R-01
World:
1. The customer's order is placed or processing
2. customer asks to cancel an order number that is none of theirs
3. order list read answers with the orders

## SC-08 Unnamed order, order list read fails
Kind: model path
Rules: R-15
World:
1. The customer's order is placed or processing
2. customer asks to cancel "my order" without a number
3. order list read fails with an error

## SC-09 Order list read times out, then fails
Kind: model path
Rules: R-15
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read times out
4. order list read fails with an error

## SC-10 Customer leaves at the proposal
Kind: model path
Rules: R-04
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer stops answering

## SC-11 Two open orders, no number, customer leaves when asked which
Kind: model path
Rules: R-02
World:
1. The customer's order is placed or processing, and they have another open order
2. customer asks to cancel "my order" without a number
3. order list read answers with the orders
4. customer stops answering

## SC-12 Order ships between the read and the cancel
Kind: model path
Rules: R-07, R-12
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers the order cannot be cancelled: it has shipped since the read

## SC-13 Customer says no to the proposal
Kind: model path
Rules: R-04, R-12
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says no

## SC-14 Customer names the other order with the yes, then leaves
Kind: model path
Rules: R-05
World:
1. The customer's order is placed or processing, and they have another open order
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes and names their other open order
5. customer stops answering

## SC-15 Two open orders, customer names one, then leaves at the proposal
Kind: model path
Rules: R-02, R-04
World:
1. The customer's order is placed or processing, and they have another open order
2. customer asks to cancel "my order" without a number
3. order list read answers with the orders
4. customer names the order
5. customer stops answering

## SC-16 Cancelled and refunded
Kind: model path
Rules: R-04, R-06, R-07, R-12
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for the confirmed amount

## SC-17 Cancel call answers the order was not found
Kind: model path
Rules: R-07, R-14
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers the order was not found
6. staff task is created

## SC-18 Cancel times out, new read shows it cancelled, refunded
Kind: model path
Rules: R-08, R-07, R-12
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call times out (cancelled)
6. new read shows the order cancelled
7. refund call returns a refund for the confirmed amount

## SC-19 Cancel times out, order still open, second cancel finds it shipped
Kind: model path
Rules: R-08, R-07
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call times out (not cancelled)
6. new read shows the order still placed or processing
7. cancel call answers the order cannot be cancelled: it has shipped since the read

## SC-20 Cancel times out, new read shows the order shipped
Kind: model path
Rules: R-08
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call times out (not cancelled; the order shipped meanwhile)
6. new read shows the order shipped

## SC-21 Refund for a different amount
Kind: model path
Rules: R-13
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. staff task is created

## SC-22 Refund fails
Kind: model path
Rules: R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a failed refund
7. staff task is created

## SC-23 Refund call answers the order is not cancelled
Kind: model path
Rules: R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers the order is not cancelled
7. staff task is created

## SC-24 Short-lived refund error, retry refunds
Kind: model path
Rules: R-11, R-12
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call has a short-lived error (no refund made)
7. refund call returns a refund for the confirmed amount

## SC-25 Refund times out twice, new read shows the refund
Kind: model path
Rules: R-11, R-09, R-12
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (refund made)
7. refund call times out (refund already made)
8. new read shows a refund for the confirmed amount

## SC-26 Refund times out, retry times out after refunding, new read shows the refund
Kind: model path
Rules: R-11, R-09, R-12
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (no refund made)
7. refund call times out (refund made)
8. new read shows a refund for the confirmed amount

## SC-27 Staff request times out once, then is created
Kind: model path
Rules: R-14
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers the order was not found
6. staff request times out
7. staff task is created

## SC-28 Cancel times out, new read times out and is read again
Kind: model path
Rules: R-08, R-15
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call times out (cancelled)
6. new read of the order times out
7. new read shows the order cancelled
8. refund call returns a refund for the confirmed amount

## SC-29 Cancel times out, new read fails
Kind: model path
Rules: R-08
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call times out (cancelled)
6. new read of the order fails with an error
7. staff task is created

## SC-30 Refund times out, retry returns the same refund, new read shows it
Kind: model path
Rules: R-11, R-09, R-12
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (refund made)
7. refund call returns the refund already made
8. new read shows a refund for the confirmed amount

## SC-31 Order not found, staff request times out twice
Kind: model path
Rules: R-07, R-14
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers the order was not found
6. staff request times out
7. staff request times out

## SC-32 Short-lived error, retry times out, new read times out and is read again
Kind: model path
Rules: R-11, R-15, R-12
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call has a short-lived error (no refund made)
7. refund call times out (refund made)
8. new read of the refund times out
9. new read shows a refund for the confirmed amount

## SC-33 Short-lived error, retry times out, new read fails
Kind: model path
Rules: R-11
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call has a short-lived error (no refund made)
7. refund call times out (refund made)
8. new read of the refund fails with an error
9. staff task is created

## SC-34 Short-lived error, retry times out with no refund, new read shows none
Kind: model path
Rules: R-11, R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call has a short-lived error (no refund made)
7. refund call times out (no refund made)
8. new read shows no refund
9. staff task is created

## SC-35 Refund times out, retry returns a different amount
Kind: model path
Rules: R-11, R-13
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (no refund made)
7. refund call returns a refund for a different amount
8. new read shows a refund for a different amount
9. staff task is created

## SC-36 Refund times out, retry returns a failed refund
Kind: model path
Rules: R-11, R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (no refund made)
7. refund call returns a failed refund
8. new read shows a failed refund
9. staff task is created

## SC-37 Different amount, staff request times out twice
Kind: model path
Rules: R-13, R-14
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. staff request times out
8. staff request times out

## SC-38 Failed refund, staff request times out twice
Kind: model path
Rules: R-10, R-14
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a failed refund
7. staff request times out
8. staff request times out

## SC-39 Cancel times out, new read fails, staff request times out twice
Kind: model path
Rules: R-08, R-14
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call times out (cancelled)
6. new read of the order fails with an error
7. staff request times out
8. staff request times out

## SC-40 Refund status unknown, staff request times out twice
Kind: model path
Rules: R-11, R-14
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call has a short-lived error (no refund made)
7. refund call times out (refund made)
8. new read of the refund fails with an error
9. staff request times out
10. staff request times out

## SC-41 Two orders in one conversation
Kind: conversational
Rules: R-16, R-04
Why not a path: the model holds one order per run; a second order starts a new run, so it cannot show each order getting its own proposal and yes.

## SC-42 Two orders named in one message
Kind: conversational
Rules: R-16, R-04, R-02
Why not a path: the model's customer names one order per message; it cannot express one message asking to cancel two orders at once.

## SC-43 A question about an order or a wish to cancel is not a yes
Kind: conversational
Rules: R-04
Why not a path: the model's customer only says yes, no, changes the order or leaves; it cannot express a message that sounds like agreement but is not an explicit yes.

## SC-44 The proposal states the total paid and the payment method paid with
Kind: conversational
Rules: R-06
Why not a path: the model abstracts amounts to same or different; it cannot check that the proposal's amount is the order's total paid with shipping and tax, back to the payment method paid with.

## SC-45 Customer asks for the refund to another card, store credit or part of the order
Kind: conversational
Rules: R-06, R-05
Why not a path: the model has no amounts, payment methods or line items, so it cannot express a request to refund elsewhere or to cancel part of an order.

## SC-46 Customer names a different order before saying yes
Kind: conversational
Rules: R-04, R-16
Why not a path: the model's customer changes the order only together with a yes; it cannot express naming another order while the proposal waits.

## SC-47 "Cancel my order" with several orders, none of them open
Kind: conversational
Rules: R-03
Why not a path: the model holds one order the customer means; it cannot express several orders that are all shipped, delivered or cancelled.

## SC-48 Order list read times out twice, then fails
Kind: model path
Rules: R-15
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read times out
4. order list read times out
5. order list read fails with an error

## SC-49 Cancel times out, new read times out twice, then shows it cancelled
Kind: model path
Rules: R-08, R-15, R-12
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call times out (cancelled)
6. new read of the order times out
7. new read of the order times out
8. new read shows the order cancelled
9. refund call returns a refund for the confirmed amount

## SC-50 Order system says the order is not cancelled, staff request times out twice
Kind: model path
Rules: R-10, R-14
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers the order is not cancelled
7. staff request times out
8. staff request times out

## SC-51 Refund new read times out twice, then shows the refund
Kind: model path
Rules: R-11, R-15, R-12
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list read answers with the orders
4. customer says yes
5. cancel call answers cancelled
6. refund call has a short-lived error (no refund made)
7. refund call times out (refund made)
8. new read of the refund times out
9. new read of the refund times out
10. new read shows a refund for the confirmed amount
