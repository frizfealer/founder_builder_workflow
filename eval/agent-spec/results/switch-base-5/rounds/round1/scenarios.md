# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 Order list answers an error
Kind: model path
Rules: R-01
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers an error

## SC-02 Shipped order is refused
Kind: model path
Rules: R-02
World:
1. The customer's order has shipped
2. customer asks to cancel the order by its number
3. order list answers

## SC-03 Delivered order is refused
Kind: model path
Rules: R-02
World:
1. The customer's order has been delivered
2. customer asks to cancel the order by its number
3. order list answers

## SC-04 Order already cancelled
Kind: model path
Rules: R-02
World:
1. The customer's order is already cancelled
2. customer asks to cancel the order by its number
3. order list answers

## SC-05 More than one open order, order list answers an error
Kind: model path
Rules: R-01
World:
1. The customer has more than one order placed or processing
2. customer asks to cancel the order by its number
3. order list answers an error

## SC-06 Order number matches none of the customer's orders
Kind: model path
Rules: R-01
World:
1. The customer's order is placed or processing
2. customer asks to cancel an order number that matches none of their orders
3. order list answers

## SC-07 Order without a number, order list answers an error
Kind: model path
Rules: R-01
World:
1. The customer's order is placed or processing
2. customer asks to cancel their order without giving a number
3. order list answers an error

## SC-08 Order list gets no answer, then an error
Kind: model path
Rules: R-13, R-01
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list gets no answer
4. order list answers an error

## SC-09 Customer leaves at the proposal
Kind: model path
Rules: R-04, R-06
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer stops answering

## SC-10 More than one open order, agent asks which, customer leaves
Kind: model path
Rules: R-03
World:
1. The customer has more than one order placed or processing
2. customer asks to cancel their order without giving a number
3. order list answers
4. customer stops answering

## SC-11 Order shipped between the read and the cancel
Kind: model path
Rules: R-04, R-02
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers not cancellable

## SC-12 Customer says no
Kind: model path
Rules: R-04
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says no

## SC-13 Customer asks for part of the order, store credit or another card
Kind: model path
Rules: R-06
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer asks for part of the order, store credit or another payment method
5. customer stops answering

## SC-14 Customer says yes and switches to another open order
Kind: model path
Rules: R-05, R-12
World:
1. The customer has more than one order placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes and switches to another of their open orders
5. customer stops answering

## SC-15 Customer names one of the open orders, then leaves
Kind: model path
Rules: R-03, R-04
World:
1. The customer has more than one order placed or processing
2. customer asks to cancel their order without giving a number
3. order list answers
4. customer names one of the open orders
5. customer stops answering

## SC-16 Cancelled and refunded
Kind: model path
Rules: R-04, R-07, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers issued

## SC-17 Cancel call answers order not found
Kind: model path
Rules: R-01
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers order not found

## SC-18 Cancel call unanswered though it cancelled, read again shows it cancelled
Kind: model path
Rules: R-07, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call gets no answer (cancelled)
6. order read again shows it cancelled
7. refund call answers issued

## SC-19 Cancel call unanswered, still open, second cancel not cancellable
Kind: model path
Rules: R-07, R-02
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call gets no answer (not cancelled)
6. order read again shows it still placed or processing
7. cancel call answers not cancellable

## SC-20 Cancel call unanswered, the order shipped meanwhile
Kind: model path
Rules: R-07, R-02
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call gets no answer (not cancelled, the order has shipped)
6. order read again shows it shipped or delivered

## SC-21 Refund pending
Kind: model path
Rules: R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers pending

## SC-22 Refund issued with another amount
Kind: model path
Rules: R-11, R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers issued with another amount
7. staff task call answers created

## SC-23 Refund failed
Kind: model path
Rules: R-08, R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers failed
7. staff task call answers created

## SC-24 Transient refund error, retry issued
Kind: model path
Rules: R-08, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call answers issued

## SC-25 Refund call answers order not cancelled
Kind: model path
Rules: R-08, R-10, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers order not cancelled
7. staff task call answers created

## SC-26 Refund call unanswered (issued), retry unanswered, read shows issued
Kind: model path
Rules: R-08, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (issued)
7. refund call gets no answer (no second refund)
8. refund read again shows it issued

## SC-27 Refund call unanswered (pending), read shows pending
Kind: model path
Rules: R-08, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (pending)
7. refund call gets no answer (no second refund)
8. refund read again shows it pending

## SC-28 Refund call unanswered (failed), read shows failed
Kind: model path
Rules: R-08, R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (failed)
7. refund call gets no answer (no second refund)
8. refund read again shows it failed
9. staff task call answers created

## SC-29 Refund call unanswered (nothing created), retry issued, read shows issued
Kind: model path
Rules: R-08, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (nothing created)
7. refund call gets no answer (issued)
8. refund read again shows it issued

## SC-30 Order read again after a cancel answers an error
Kind: model path
Rules: R-07, R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call gets no answer (cancelled)
6. order read again answers an error
7. staff task call answers created

## SC-31 Order read again gets no answer, then shows it cancelled
Kind: model path
Rules: R-13, R-07, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call gets no answer (cancelled)
6. order read again gets no answer
7. order read again shows it cancelled
8. refund call answers issued

## SC-32 Staff task unanswered (created), second call created
Kind: model path
Rules: R-10, R-11
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers issued with another amount
7. staff task call gets no answer (created)
8. staff task call answers created

## SC-33 Staff task unanswered (not created), second call created
Kind: model path
Rules: R-10, R-11
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers issued with another amount
7. staff task call gets no answer (not created)
8. staff task call answers created

## SC-34 Refund failed, staff task sent once more
Kind: model path
Rules: R-10, R-08
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers failed
7. staff task call gets no answer (created)
8. staff task call answers created

## SC-35 Cancellation unknown, staff task sent once more
Kind: model path
Rules: R-10, R-07
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call gets no answer (cancelled)
6. order read again answers an error
7. staff task call gets no answer (created)
8. staff task call answers created

## SC-36 Refund retry unanswered, read answers an error
Kind: model path
Rules: R-08, R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (issued)
8. refund read again answers an error
9. staff task call answers created

## SC-37 Refund read again gets no answer, then shows issued
Kind: model path
Rules: R-13, R-08, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (issued)
8. refund read again gets no answer
9. refund read again shows it issued

## SC-38 Refund read again shows no refund
Kind: model path
Rules: R-08, R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (nothing created)
8. refund read again shows no refund
9. staff task call answers created

## SC-39 Refund read again shows another amount
Kind: model path
Rules: R-08, R-11, R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (nothing created)
7. refund call answers issued with another amount
8. refund read again shows it issued with another amount
9. staff task call answers created

## SC-40 Another amount, staff task unanswered twice
Kind: model path
Rules: R-11, R-10
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers issued with another amount
7. staff task call gets no answer (created)
8. staff task call gets no answer (created)

## SC-41 Refund failed, staff task unanswered twice
Kind: model path
Rules: R-10, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers failed
7. staff task call gets no answer (created)
8. staff task call gets no answer (created)

## SC-42 Cancellation unknown, staff task unanswered twice
Kind: model path
Rules: R-10, R-07
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call gets no answer (cancelled)
6. order read again answers an error
7. staff task call gets no answer (created)
8. staff task call gets no answer (created)

## SC-43 Refund status unknown, staff task sent once more
Kind: model path
Rules: R-10, R-08
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (issued)
8. refund read again answers an error
9. staff task call gets no answer (created)
10. staff task call answers created

## SC-44 Refund status unknown, staff task unanswered twice
Kind: model path
Rules: R-10, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (issued)
8. refund read again answers an error
9. staff task call gets no answer (created)
10. staff task call gets no answer (created)

## SC-45 Refund not confirmed yet, staff task unanswered twice
Kind: model path
Rules: R-10, R-08
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (failed)
8. refund read again shows it failed
9. staff task call gets no answer (created)
10. staff task call gets no answer (created)

## SC-46 Two orders in one message
Kind: conversational
Rules: R-12, R-04
Why not a path: the model holds one request about one order; a message asking to cancel two orders at once needs the agent to take them one at a time, each with its own proposal and yes.

## SC-47 A fourth order in one conversation
Kind: conversational
Rules: R-12
Why not a path: a second order in the same conversation starts a new run of the model, so the model cannot count orders across a conversation.

## SC-48 A question or a wish is not a yes
Kind: conversational
Rules: R-04
Why not a path: the model's customer either says yes or does not; a question about the refund, or "I want to cancel", is wording the agent must not read as a yes.

## SC-49 The customer asks when the money arrives
Kind: conversational
Rules: R-09
Why not a path: what the agent says about timing is wording, not a step; the agent must promise nothing about when the money arrives.

## SC-50 The customer changes the payment method after saying yes
Kind: conversational
Rules: R-05, R-06
Why not a path: the model lets the customer change the proposal only by switching orders; a yes followed by a request to refund to another card must void the yes, and the agent must say the refund goes only to the payment method the order was paid with.

## SC-51 A read that never answers
Kind: conversational
Rules: R-13
Why not a path: the model folds repeated reads with no answer into one state, so it cannot show a conversation that waits on reads forever; nothing in the inputs ends it.

## SC-52 Refund call answers order not cancelled, staff task unanswered twice
Kind: model path
Rules: R-08, R-10, R-09
World:
1. The customer's order is placed or processing
2. customer asks to cancel the order by its number
3. order list answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers order not cancelled
7. staff task call gets no answer (created)
8. staff task call gets no answer (created)
