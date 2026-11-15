# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 The order list cannot be read
Kind: model path
Rules: R-01
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers an error

## SC-02 Two open orders, the order list cannot be read
Kind: model path
Rules: R-01
World:
1. The customer has two open orders
2. customer asks to cancel an order by its number
3. listing the orders answers an error

## SC-03 The order has already shipped
Kind: model path
Rules: R-01
World:
1. The customer's order has shipped
2. customer asks to cancel an order by its number
3. listing the orders answers

## SC-04 The order is already cancelled
Kind: model path
Rules: R-01
World:
1. The customer's order is already cancelled
2. customer asks to cancel an order by its number
3. listing the orders answers

## SC-05 No order number given, the order list cannot be read
Kind: model path
Rules: R-01, R-02
World:
1. The customer has one open order
2. customer asks to cancel their order without a number
3. listing the orders answers an error

## SC-06 The order number matches none of the customer's orders
Kind: model path
Rules: R-01
World:
1. The customer has one open order
2. customer asks to cancel an order number that matches none of their orders
3. listing the orders answers

## SC-07 The customer asks to cancel only some items
Kind: model path
Rules: R-05
World:
1. The customer has one open order
2. customer asks to cancel only some items of an order
3. listing the orders answers

## SC-08 The order list answers late, then fails
Kind: model path
Rules: R-01
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders gets no answer
4. listing the orders answers an error

## SC-09 The customer leaves at the proposal
Kind: model path
Rules: R-03
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer stops answering

## SC-10 Two open orders and no number: the agent asks which, the customer leaves
Kind: model path
Rules: R-02, R-03
World:
1. The customer has two open orders
2. customer asks to cancel their order without a number
3. listing the orders answers
4. customer stops answering

## SC-11 The order ships before the cancel call
Kind: model path
Rules: R-03, R-06, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers not cancellable: the order has shipped or been delivered

## SC-12 The customer withdraws at the proposal
Kind: model path
Rules: R-03
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer withdraws

## SC-13 The customer says yes and names the other order
Kind: model path
Rules: R-03, R-04
World:
1. The customer has two open orders
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes and names the other open order
5. customer stops answering

## SC-14 The customer names which of two orders, then leaves
Kind: model path
Rules: R-02, R-03
World:
1. The customer has two open orders
2. customer asks to cancel their order without a number
3. listing the orders answers
4. customer names one of the open orders
5. customer stops answering

## SC-15 Cancelled and refunded
Kind: model path
Rules: R-03, R-05, R-06, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a pending or issued refund for the confirmed amount

## SC-16 The cancel call cannot find the order
Kind: model path
Rules: R-03, R-06
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers order not found

## SC-17 The cancel call gets no answer but cancelled the order
Kind: model path
Rules: R-03, R-05, R-07, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call gets no answer (cancelled)
6. read shows the order cancelled
7. refund call answers a pending or issued refund for the confirmed amount

## SC-18 The cancel call gets no answer, sent once more, the order has shipped
Kind: model path
Rules: R-03, R-06, R-07, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call gets no answer (nothing cancelled)
6. read shows the order still open
7. cancel call answers not cancellable: the order has shipped or been delivered

## SC-19 The cancel call gets no answer and the order had shipped
Kind: model path
Rules: R-03, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call gets no answer (the order had shipped)
6. read shows the order shipped

## SC-20 The refund is for a different amount
Kind: model path
Rules: R-03, R-06, R-11, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a refund whose amount differs from the confirmed one
7. follow-up call answers task created

## SC-21 The refund fails for good
Kind: model path
Rules: R-03, R-06, R-08, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers failed
7. follow-up call answers task created

## SC-22 The refund hits a temporary error, then succeeds
Kind: model path
Rules: R-03, R-05, R-06, R-08, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error
7. refund call answers a pending or issued refund for the confirmed amount

## SC-23 The refund call gets no answer twice but made the refund
Kind: model path
Rules: R-03, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created)
7. refund call gets no answer (a refund already exists)
8. read shows a pending or issued refund for the confirmed amount

## SC-24 The refund call gets no answer, then makes the refund
Kind: model path
Rules: R-03, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (nothing created)
7. refund call gets no answer (refund created)
8. read shows a pending or issued refund for the confirmed amount

## SC-25 The read after an unanswered cancel call fails
Kind: model path
Rules: R-03, R-07, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call gets no answer (cancelled)
6. read of the order answers an error
7. follow-up call answers task created

## SC-26 The read after an unanswered cancel call answers late
Kind: model path
Rules: R-03, R-05, R-07, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call gets no answer (cancelled)
6. read of the order gets no answer
7. read shows the order cancelled
8. refund call answers a pending or issued refund for the confirmed amount

## SC-27 The follow-up call gets no answer once
Kind: model path
Rules: R-03, R-06, R-11, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a refund whose amount differs from the confirmed one
7. follow-up call gets no answer (task created)
8. follow-up call answers task created

## SC-28 The follow-up call gets no answer once and made no task
Kind: model path
Rules: R-03, R-06, R-11, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a refund whose amount differs from the confirmed one
7. follow-up call gets no answer (nothing created)
8. follow-up call answers task created

## SC-29 The second refund call answers with the refund that exists
Kind: model path
Rules: R-03, R-05, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created)
7. refund call answers with the refund that already exists
8. read shows a pending or issued refund for the confirmed amount

## SC-30 The read of the refund fails
Kind: model path
Rules: R-03, R-06, R-08, R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error
7. refund call gets no answer (refund created)
8. read of the refund answers an error
9. follow-up call answers task created

## SC-31 The read of the refund answers late
Kind: model path
Rules: R-03, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error
7. refund call gets no answer (refund created)
8. read of the refund gets no answer
9. read shows a pending or issued refund for the confirmed amount

## SC-32 After a temporary error and no answer, no refund exists
Kind: model path
Rules: R-03, R-06, R-08, R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error
7. refund call gets no answer (nothing created)
8. read shows no refund
9. follow-up call answers task created

## SC-33 After no answer, the second refund call fails for good
Kind: model path
Rules: R-03, R-06, R-08, R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (nothing created)
7. refund call answers failed
8. read shows a failed refund
9. follow-up call answers task created

## SC-34 Different refund amount and no follow-up answer: contact support
Kind: model path
Rules: R-03, R-06, R-11, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a refund whose amount differs from the confirmed one
7. follow-up call gets no answer (task created)
8. follow-up call gets no answer (task created)

## SC-35 Failed refund and no follow-up answer: contact support
Kind: model path
Rules: R-03, R-06, R-08, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers failed
7. follow-up call gets no answer (task created)
8. follow-up call gets no answer (task created)

## SC-36 Unknown cancellation and no follow-up answer: contact support
Kind: model path
Rules: R-03, R-07, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call gets no answer (cancelled)
6. read of the order answers an error
7. follow-up call gets no answer (task created)
8. follow-up call gets no answer (task created)

## SC-37 Two cancel calls with no answer, the order is still open
Kind: model path
Rules: R-03, R-07, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call gets no answer (nothing cancelled)
6. read shows the order still open
7. cancel call gets no answer (nothing cancelled)
8. read shows the order still open
9. follow-up call answers task created

## SC-38 Unknown refund status and no follow-up answer: contact support
Kind: model path
Rules: R-03, R-06, R-08, R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error
7. refund call gets no answer (refund created)
8. read of the refund answers an error
9. follow-up call gets no answer (task created)
10. follow-up call gets no answer (task created)

## SC-39 Refund not confirmed and no follow-up answer: contact support
Kind: model path
Rules: R-03, R-06, R-08, R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a temporary error
7. refund call gets no answer (nothing created)
8. read shows no refund
9. follow-up call gets no answer (task created)
10. follow-up call gets no answer (task created)

## SC-40 Order still open after two cancel calls, no follow-up answer: contact support
Kind: model path
Rules: R-03, R-07, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. listing the orders answers
4. customer says yes
5. cancel call gets no answer (nothing cancelled)
6. read shows the order still open
7. cancel call gets no answer (nothing cancelled)
8. read shows the order still open
9. follow-up call gets no answer (task created)
10. follow-up call gets no answer (task created)

## SC-41 Two orders cancelled in one message
Kind: conversational
Rules: R-02, R-03
Why not a path: the model follows one order per conversation; a message that asks to cancel two orders needs a proposal naming each order and a yes to each.

## SC-42 A second cancellation after the first is done
Kind: conversational
Rules: R-01, R-03
Why not a path: a request to cancel another order after the first is finished starts a new run of the model; the earlier yes does not cover it.

## SC-43 The customer asks when the money arrives
Kind: conversational
Rules: R-10
Why not a path: the model has no step for what the agent says about timing; the agent promises nothing about when the money arrives.

## SC-44 The customer asks for store credit, a fee waiver or part of the money
Kind: conversational
Rules: R-05
Why not a path: the model holds no amounts or refund options; the agent offers only the full order total back to the order's payment method.

## SC-45 A question about cancelling is not a yes
Kind: conversational
Rules: R-03
Why not a path: the model has no free text; "can I still cancel this?" or "I want to cancel" before the proposal must not count as the yes.

## SC-46 Only some items, then the whole order
Kind: conversational
Rules: R-05, R-03
Why not a path: the model ends the run once the agent says only the whole order can be cancelled; a customer who then asks to cancel the whole order starts a new request with its own proposal and yes.
