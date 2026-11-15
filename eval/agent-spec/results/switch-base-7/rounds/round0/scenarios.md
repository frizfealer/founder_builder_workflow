# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 The lookup gets no answer
Kind: model path
Rules: R-01
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup gets no answer

## SC-02 A shipped or delivered order
Kind: model path
Rules: R-03
World:
1. The order has shipped or been delivered
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders

## SC-03 An order already cancelled
Kind: model path
Rules: R-03
World:
1. The order is already cancelled
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders

## SC-04 The number matches none of the customer's orders
Kind: model path
Rules: R-01
World:
1. No order of the customer's has that number
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders

## SC-05 Two open orders, and the lookup gets no answer
Kind: model path
Rules: R-01
World:
1. The customer has two open orders
2. customer asks to cancel "my order" without saying which
3. lookup gets no answer

## SC-06 The customer leaves at the proposal
Kind: model path
Rules: R-04, R-05
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer stops answering

## SC-07 Two open orders, the customer leaves when asked which
Kind: model path
Rules: R-02
World:
1. The customer has two open orders
2. customer asks to cancel "my order" without saying which
3. lookup answers with the customer's orders
4. customer stops answering

## SC-08 The order ships before the cancel
Kind: model path
Rules: R-04, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers the order cannot be cancelled (shipped or delivered)

## SC-09 The customer changes the proposal, then leaves
Kind: model path
Rules: R-04
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes and changes part of the proposal
5. customer stops answering

## SC-10 The customer says no
Kind: model path
Rules: R-04
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says no

## SC-11 Two open orders, the customer names one, then leaves at the proposal
Kind: model path
Rules: R-02, R-04
World:
1. The customer has two open orders
2. customer asks to cancel "my order" without saying which
3. lookup answers with the customer's orders
4. customer names one of the open orders
5. customer stops answering

## SC-12 Cancelled and refunded
Kind: model path
Rules: R-04, R-05, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns the refund for the confirmed amount

## SC-13 The cancel call does not find the order
Kind: model path
Rules: R-01
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers the order is not found

## SC-14 The cancel call times out but cancelled the order, then refunded
Kind: model path
Rules: R-07, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call times out (order cancelled)
6. lookup shows the order cancelled
7. refund call returns the refund for the confirmed amount

## SC-15 The cancel call times out and the order has shipped
Kind: model path
Rules: R-07, R-06
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call times out (nothing changed)
6. lookup shows the order shipped

## SC-16 A refund for a different amount goes to staff
Kind: model path
Rules: R-09, R-10, R-11
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. follow-up call answers created

## SC-17 A failed refund goes to staff
Kind: model path
Rules: R-08, R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a failed refund
7. follow-up call answers created

## SC-18 A transient refund error, then the retry refunds
Kind: model path
Rules: R-08, R-11
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a transient error (no refund created)
7. refund call returns the refund for the confirmed amount

## SC-19 The refund call says the order is not cancelled
Kind: model path
Rules: R-06, R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers the order is not cancelled
7. follow-up call answers created

## SC-20 The refund call times out after creating the refund; the retry returns it
Kind: model path
Rules: R-08, R-11
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (refund created)
7. refund call returns the existing refund

## SC-21 The refund call times out after creating a refund for a different amount
Kind: model path
Rules: R-08, R-09, R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (refund created for a different amount)
7. refund call returns the existing refund
8. follow-up call answers created

## SC-22 The refund call times out with no refund; the retry refunds
Kind: model path
Rules: R-08, R-11
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (no refund created)
7. refund call returns the refund for the confirmed amount

## SC-23 The cancel call times out and the lookup gets no answer
Kind: model path
Rules: R-07, R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call times out (order cancelled)
6. lookup gets no answer
7. follow-up call answers created

## SC-24 The cancel call times out, the order is still open, and the second cancel is refused
Kind: model path
Rules: R-07, R-06
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call times out (nothing changed)
6. lookup shows the order still placed or processing
7. cancel call answers the order cannot be cancelled (shipped or delivered)

## SC-25 The follow-up call times out once (task created), then answers created
Kind: model path
Rules: R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. follow-up call times out (task created)
8. follow-up call answers created

## SC-26 The follow-up call times out once (no task created), then answers created
Kind: model path
Rules: R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. follow-up call times out (no task created)
8. follow-up call answers created

## SC-27 The refund call times out twice, and the lookup shows the refund
Kind: model path
Rules: R-08, R-11
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (refund created)
7. refund call times out (nothing new created)
8. lookup shows the refund pending or issued

## SC-28 A transient refund error, a time-out, and a lookup with no answer
Kind: model path
Rules: R-08, R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a transient error (no refund created)
7. refund call times out (refund created)
8. lookup gets no answer
9. follow-up call answers created

## SC-29 A transient refund error, a time-out, and no refund
Kind: model path
Rules: R-08, R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a transient error (no refund created)
7. refund call times out (no refund created)
8. lookup shows no refund
9. follow-up call answers created

## SC-30 A refund for a different amount, and the follow-up call times out twice
Kind: model path
Rules: R-09, R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. follow-up call times out (task created)
8. follow-up call times out (task created)

## SC-31 A failed refund, and the follow-up call times out twice
Kind: model path
Rules: R-08, R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a failed refund
7. follow-up call times out (task created)
8. follow-up call times out (task created)

## SC-32 The order is not cancelled, and the follow-up call times out twice
Kind: model path
Rules: R-06, R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers the order is not cancelled
7. follow-up call times out (task created)
8. follow-up call times out (task created)

## SC-33 The cancellation is unknown, and the follow-up call times out twice
Kind: model path
Rules: R-07, R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call times out (order cancelled)
6. lookup gets no answer
7. follow-up call times out (task created)
8. follow-up call times out (task created)

## SC-34 The refund status is unknown, and the follow-up call times out twice
Kind: model path
Rules: R-08, R-10
World:
1. The order is placed or processing
2. customer asks to cancel an order by its number
3. lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a transient error (no refund created)
7. refund call times out (refund created)
8. lookup gets no answer
9. follow-up call times out (task created)
10. follow-up call times out (task created)

## SC-35 Two orders in one message
Kind: conversational
Rules: R-12, R-04
Why not a path: the model holds one order; a message naming two orders needs a proposal and a yes for each, one at a time.

## SC-36 A second order after the first is done
Kind: conversational
Rules: R-12, R-04
Why not a path: a second order named after this one is done starts a new run of the model, with its own proposal and its own yes.

## SC-37 The customer asks to cancel part of the order, or for store credit
Kind: conversational
Rules: R-05
Why not a path: the model's proposal is always the whole order refunded to its payment method; what the customer asks for instead is wording the model does not hold.

## SC-38 The customer asks when the money will arrive
Kind: conversational
Rules: R-11
Why not a path: the model does not hold what the agent says about timing; the agent promises nothing about when the money arrives.
