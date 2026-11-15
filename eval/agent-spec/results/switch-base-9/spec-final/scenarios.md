# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 Order list unanswered, one open order
Kind: model path
Rules: R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call gets no answer

## SC-02 Order list unanswered, two open orders
Kind: model path
Rules: R-07
World:
1. The customer has two open orders
2. customer asks to cancel an order, naming it
3. order list call gets no answer

## SC-03 Shipped order is refused without a cancel call
Kind: model path
Rules: R-02, R-12
World:
1. The customer's order has shipped or been delivered
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders

## SC-04 Already cancelled order is reported, nothing changed
Kind: model path
Rules: R-02
World:
1. The customer's order is already cancelled
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders

## SC-05 Order number that is not the customer's
Kind: model path
Rules: R-01
World:
1. The customer has one open order
2. customer asks to cancel an order number that is not theirs
3. order list call answers with the customer's orders

## SC-06 Two open orders, no order named, order list unanswered
Kind: model path
Rules: R-03, R-07
World:
1. The customer has two open orders
2. customer asks to cancel their order without saying which
3. order list call gets no answer

## SC-07 Customer leaves at the proposal
Kind: model path
Rules: R-04, R-06
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer stops answering

## SC-08 Customer leaves when asked which order
Kind: model path
Rules: R-03
World:
1. The customer has two open orders
2. customer asks to cancel their order without saying which
3. order list call answers with the customer's orders
4. customer stops answering

## SC-09 Order shipped between the proposal and the cancel
Kind: model path
Rules: R-04, R-02, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers that the order cannot be cancelled, with its status shipped or delivered

## SC-10 Customer withdraws at the proposal
Kind: model path
Rules: R-04
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer withdraws

## SC-11 Customer says yes, then switches to the other order
Kind: model path
Rules: R-05, R-03
World:
1. The customer has two open orders
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes, then asks to cancel their other open order instead
5. customer stops answering

## SC-12 Customer names one of two open orders, then leaves
Kind: model path
Rules: R-03, R-04
World:
1. The customer has two open orders
2. customer asks to cancel their order without saying which
3. order list call answers with the customer's orders
4. customer names one of their open orders
5. customer stops answering

## SC-13 Cancelled and refunded
Kind: model path
Rules: R-04, R-06, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund, pending or issued, for the amount confirmed

## SC-14 Cancel call cannot find the order
Kind: model path
Rules: R-02, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers that the order is not found

## SC-15 Cancel unanswered but done; re-read shows it cancelled
Kind: model path
Rules: R-09, R-06, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. re-read shows the order cancelled
7. refund call answers with a refund, pending or issued, for the amount confirmed

## SC-16 Cancel unanswered; re-read shows the order shipped
Kind: model path
Rules: R-09, R-02
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order shipped)
6. re-read shows the order shipped

## SC-17 Cancel unanswered, order still open; resent cancel finds it shipped
Kind: model path
Rules: R-09, R-02
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing cancelled)
6. re-read shows the order still placed or processing
7. cancel call answers that the order cannot be cancelled, with its status shipped or delivered

## SC-18 Refund for a different amount, staff follow up
Kind: model path
Rules: R-11, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund for a different amount
7. follow-up call answers that the task is created

## SC-19 Refund failed, staff follow up
Kind: model path
Rules: R-08, R-10, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund whose status is failed
7. follow-up call answers that the task is created

## SC-20 Temporary refund error, second refund call works
Kind: model path
Rules: R-08, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a temporary error, no refund created
7. refund call answers with a refund, pending or issued, for the amount confirmed

## SC-21 Refund unanswered but made; second call returns the same refund; re-read shows it
Kind: model path
Rules: R-08, R-06, R-09, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created)
7. refund call answers with the same refund, pending or issued
8. re-read shows a refund, pending or issued

## SC-22 Refund unanswered and not made; second call works; re-read shows it
Kind: model path
Rules: R-08, R-06, R-09, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (nothing created)
7. refund call answers with a refund, pending or issued, for the amount confirmed
8. re-read shows a refund, pending or issued

## SC-23 Cancel outcome unknown, staff follow up
Kind: model path
Rules: R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. re-read of the order gets no answer
7. follow-up call answers that the task is created

## SC-24 Follow-up unanswered once, then created
Kind: model path
Rules: R-10, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund for a different amount
7. follow-up call gets no answer
8. follow-up call answers that the task is created

## SC-25 Second refund call unanswered; re-read shows the refund
Kind: model path
Rules: R-09, R-08, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a temporary error, no refund created
7. refund call gets no answer (refund created)
8. re-read shows a refund, pending or issued

## SC-26 Refund re-read unanswered, staff follow up
Kind: model path
Rules: R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a temporary error, no refund created
7. refund call gets no answer (refund created)
8. re-read of the refund gets no answer
9. follow-up call answers that the task is created

## SC-27 Refund re-read shows no refund, staff follow up
Kind: model path
Rules: R-09, R-10, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a temporary error, no refund created
7. refund call gets no answer (nothing created)
8. re-read shows no refund
9. follow-up call answers that the task is created

## SC-28 Refund amount differs and follow-up twice unanswered
Kind: model path
Rules: R-11, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund for a different amount
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-29 Refund failed and follow-up twice unanswered
Kind: model path
Rules: R-10, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund whose status is failed
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-30 Cancel outcome unknown and follow-up twice unanswered
Kind: model path
Rules: R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. re-read of the order gets no answer
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-31 Cancel unanswered twice, order still open
Kind: model path
Rules: R-09, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing cancelled)
6. re-read shows the order still placed or processing
7. cancel call gets no answer (nothing cancelled)
8. re-read shows the order still placed or processing

## SC-32 Refund status unknown and follow-up twice unanswered
Kind: model path
Rules: R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a temporary error, no refund created
7. refund call gets no answer (refund created)
8. re-read of the refund gets no answer
9. follow-up call gets no answer
10. follow-up call gets no answer

## SC-33 A second order in the same conversation
Kind: conversational
Rules: R-12, R-05, R-04
Why not a path: the model covers one order per run; after one order is done the customer asks to cancel another of their open orders, and the agent makes a new proposal and waits for a new yes for it.

## SC-34 Two requests in one message
Kind: conversational
Rules: R-03, R-12
Why not a path: the model has one request per message; the customer asks in one message to cancel two orders, and the agent works on one at a time, each with its own proposal and yes.

## SC-35 A part of an order
Kind: conversational
Rules: R-12, R-06
Why not a path: the model has no partial cancel; the customer asks to cancel one item of an order, and the agent says only a whole order can be cancelled, with its total paid refunded.

## SC-36 A question about cancelling is not a yes
Kind: conversational
Rules: R-04
Why not a path: the model cannot tell a question from a yes; the customer asks "can I still cancel?" or says they are thinking of cancelling, and the agent answers and proposes, and cancels nothing.

## SC-37 Store credit or a return instead
Kind: conversational
Rules: R-02, R-06, R-12
Why not a path: the model has no return or store-credit request; the customer asks for store credit instead, or to return a delivered order, and the agent offers neither.

## SC-38 When will the money arrive
Kind: conversational
Rules: R-07
Why not a path: the model has no question after the refund; the customer asks when the refund will reach them, and the agent promises nothing about when the money arrives.

## SC-39 Customer switches to the other order before saying yes
Kind: model path
Rules: R-05, R-04
World:
1. The customer has two open orders
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer asks to cancel their other open order instead, before saying yes
5. customer stops answering

## SC-40 Refund unanswered twice; re-read shows a different amount
Kind: model path
Rules: R-09, R-11, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created for a different amount)
7. refund call gets no answer (refund created)
8. re-read shows a refund for a different amount
9. follow-up call answers that the task is created

## SC-41 Refund unanswered, then failed; re-read shows it failed
Kind: model path
Rules: R-09, R-08, R-10, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (nothing created)
7. refund call answers with a refund whose status is failed
8. re-read shows the refund failed
9. follow-up call answers that the task is created

## SC-42 Refund not confirmed yet and follow-up twice unanswered
Kind: model path
Rules: R-09, R-10, R-07
World:
1. The customer has one open order
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a temporary error, no refund created
7. refund call gets no answer (nothing created)
8. re-read shows no refund
9. follow-up call gets no answer
10. follow-up call gets no answer
