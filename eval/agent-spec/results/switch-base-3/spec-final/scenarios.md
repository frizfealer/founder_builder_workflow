# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 Order number matches none of the customer's orders
Kind: model path
Rules: R-01, R-11
World:
1. The customer has one open order
2. customer gives an order number that matches none of their orders
3. order lookup answers with the customer's orders

## SC-02 Order number matches none, customer has two open orders
Kind: model path
Rules: R-01, R-11
World:
1. The customer has two open orders
2. customer gives an order number that matches none of their orders
3. order lookup answers with the customer's orders

## SC-03 Order has shipped or been delivered
Kind: model path
Rules: R-02, R-11
World:
1. The customer's order has shipped or been delivered
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders

## SC-04 Order already cancelled
Kind: model path
Rules: R-02, R-11
World:
1. The customer's order is already cancelled
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders

## SC-05 "Cancel my order" with one open order, customer leaves at the proposal
Kind: model path
Rules: R-04, R-05
World:
1. The customer has one open order
2. customer says "cancel my order" without naming it
3. order lookup answers with the customer's orders
4. customer stops answering

## SC-06 Some items asked for, customer leaves
Kind: model path
Rules: R-03
World:
1. The customer has one open order
2. customer asks to cancel some items of an order
3. order lookup answers with the customer's orders
4. customer stops answering

## SC-07 First lookup gets no answer and is tried again
Kind: model path
Rules: R-15, R-05
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup gets no answer
4. order lookup answers with the customer's orders
5. customer stops answering

## SC-08 Two open orders, order not named, customer leaves
Kind: model path
Rules: R-04
World:
1. The customer has two open orders
2. customer says "cancel my order" without naming it
3. order lookup answers with the customer's orders
4. customer stops answering

## SC-09 Order shipped between the lookup and the cancel
Kind: model path
Rules: R-02, R-06, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers not cancellable (the order shipped after the lookup)

## SC-10 Customer withdraws at the proposal
Kind: model path
Rules: R-05, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer withdraws

## SC-11 Some items asked for, then the whole order
Kind: model path
Rules: R-03, R-05
World:
1. The customer has one open order
2. customer asks to cancel some items of an order
3. order lookup answers with the customer's orders
4. customer asks to cancel the whole order
5. customer stops answering

## SC-12 Yes, then the other open order named
Kind: model path
Rules: R-05
World:
1. The customer has two open orders
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes, then names their other open order
5. customer stops answering

## SC-13 Two open orders, customer names one
Kind: model path
Rules: R-04, R-05
World:
1. The customer has two open orders
2. customer says "cancel my order" without naming it
3. order lookup answers with the customer's orders
4. customer names one of the open orders
5. customer stops answering

## SC-14 Cancelled and refunded
Kind: model path
Rules: R-05, R-06, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund, pending or issued, for the proposed amount

## SC-15 Cancel call finds no order
Kind: model path
Rules: R-06, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers order not found

## SC-16 Cancel call unanswered, lookup shows it cancelled, refunded
Kind: model path
Rules: R-10, R-06, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. order lookup shows the order cancelled
7. refund call answers with a refund, pending or issued, for the proposed amount

## SC-17 Cancel call unanswered, lookup shows the order shipped
Kind: model path
Rules: R-10, R-02, R-06
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing changed)
6. order lookup shows the order shipped

## SC-18 Refund for a different amount
Kind: model path
Rules: R-13, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund for a different amount
7. follow-up call creates the staff task

## SC-19 Refund failed
Kind: model path
Rules: R-08, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund whose status is failed
7. follow-up call creates the staff task

## SC-20 Transient refund error, retry refunds
Kind: model path
Rules: R-08, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a transient error
7. refund call answers with a refund, pending or issued, for the proposed amount

## SC-21 Refund call unanswered (refund created), retry returns the same refund
Kind: model path
Rules: R-09, R-07, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created)
7. refund call answers with the refund the order already has

## SC-22 Refund call unanswered (nothing created), retry refunds
Kind: model path
Rules: R-09, R-07, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (nothing created)
7. refund call answers with a refund, pending or issued, for the proposed amount

## SC-23 Cancel call unanswered, lookup also unanswered
Kind: model path
Rules: R-10, R-06, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. order lookup after the cancel gets no answer
7. follow-up call creates the staff task

## SC-24 Cancel unanswered, order still open, second cancel finds it shipped
Kind: model path
Rules: R-10, R-02, R-06
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing changed)
6. order lookup shows the order still placed or processing
7. cancel call answers not cancellable (the order shipped after the lookup)

## SC-25 Follow-up unanswered once, then created
Kind: model path
Rules: R-12, R-13
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund for a different amount
7. follow-up call gets no answer
8. follow-up call creates the staff task

## SC-26 Both refund calls unanswered, lookup shows the refund
Kind: model path
Rules: R-09, R-07, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created)
7. refund call gets no answer (no second refund created)
8. order lookup shows the refund pending or issued, for the proposed amount

## SC-27 Transient error, then no answer, lookup unanswered
Kind: model path
Rules: R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a transient error
7. refund call gets no answer (refund created)
8. order lookup after the refund gets no answer
9. follow-up call creates the staff task

## SC-28 Transient error, then no answer, lookup shows no refund
Kind: model path
Rules: R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a transient error
7. refund call gets no answer (nothing created)
8. order lookup shows no refund
9. follow-up call creates the staff task

## SC-29 Different amount, follow-up unanswered twice
Kind: model path
Rules: R-13, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund for a different amount
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-30 Refund failed, follow-up unanswered twice
Kind: model path
Rules: R-08, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund whose status is failed
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-31 Cancel outcome unknown, follow-up unanswered twice
Kind: model path
Rules: R-10, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. order lookup after the cancel gets no answer
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-32 Order still open after two cancel calls
Kind: model path
Rules: R-10, R-06, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing changed)
6. order lookup shows the order still placed or processing
7. cancel call gets no answer (nothing changed)
8. order lookup shows the order still placed or processing
9. follow-up call creates the staff task

## SC-33 Refund status unknown, follow-up unanswered twice
Kind: model path
Rules: R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a transient error
7. refund call gets no answer (refund created)
8. order lookup after the refund gets no answer
9. follow-up call gets no answer
10. follow-up call gets no answer

## SC-34 Refund not confirmed, follow-up unanswered twice
Kind: model path
Rules: R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a transient error
7. refund call gets no answer (nothing created)
8. order lookup shows no refund
9. follow-up call gets no answer
10. follow-up call gets no answer

## SC-35 Order still open after two cancel calls, follow-up unanswered twice
Kind: model path
Rules: R-10, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing changed)
6. order lookup shows the order still placed or processing
7. cancel call gets no answer (nothing changed)
8. order lookup shows the order still placed or processing
9. follow-up call gets no answer
10. follow-up call gets no answer

## SC-36 Customer asks about an order of another customer
Kind: conversational
Rules: R-01
Why not a path: the model holds only the signed-in customer's orders; an order number belonging to someone else looks, to the agent, like a number matching none of their orders.

## SC-37 Two orders to cancel in one message
Kind: conversational
Rules: R-14, R-05
Why not a path: the model is one request about one order; a message asking to cancel two orders needs the agent to take them one at a time, each with its own proposal and yes.

## SC-38 A question about cancelling is not a yes
Kind: conversational
Rules: R-05
Why not a path: the model's customer either says yes or does not; "can I still cancel this?" or "I want to cancel" after the proposal is wording the model cannot tell apart from a yes.

## SC-39 The refund goes back to the payment method the customer paid with
Kind: conversational
Rules: R-07, R-05
Why not a path: the model does not hold payment methods; a customer who asks for the money to go to another card or to store credit is told it goes back to the order's payment method.

## SC-40 No promise of when the money arrives
Kind: conversational
Rules: R-11
Why not a path: the model does not hold what the agent says about timing; a customer who asks "when will I get it?" is told nothing that promises a date.

## SC-41 Customer has no orders
Kind: model path
Rules: R-01, R-11
World:
1. The customer has no orders
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders

## SC-42 Yes, then the other order named instead
Kind: model path
Rules: R-14, R-05
World:
1. The customer has two open orders
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes, then names their other open order
5. customer means the other order instead
6. customer stops answering

## SC-43 Yes, then the other order named as well; the first shipped meanwhile
Kind: model path
Rules: R-14, R-02, R-06
World:
1. The customer has two open orders
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes, then names their other open order
5. customer means the other order as well
6. cancel call answers not cancellable (the order shipped after the lookup)

## SC-44 Refund created for a different amount, retry shows it
Kind: model path
Rules: R-13, R-09, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created for a different amount)
7. refund call answers with the refund the order already has
8. follow-up call creates the staff task

## SC-45 Lookup after unanswered refund calls shows a different amount
Kind: model path
Rules: R-13, R-09
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a transient error
7. refund call gets no answer (refund created for a different amount)
8. order lookup shows a refund for a different amount
9. follow-up call creates the staff task

## SC-46 Different amount found by the lookup, follow-up unanswered twice
Kind: model path
Rules: R-13, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order lookup answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a transient error
7. refund call gets no answer (refund created for a different amount)
8. order lookup shows a refund for a different amount
9. follow-up call gets no answer
10. follow-up call gets no answer
