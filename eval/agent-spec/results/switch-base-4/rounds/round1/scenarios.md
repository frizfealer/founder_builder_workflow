# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 Order list fails at the start
Kind: model path
Rules: R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call fails with an error

## SC-02 Second open order, order list fails
Kind: model path
Rules: R-09
World:
1. The order is placed or processing, and the customer has a second open order
2. customer asks to cancel the order, naming it
3. order list call fails with an error

## SC-03 Order has shipped
Kind: model path
Rules: R-01
World:
1. The order has shipped or been delivered
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders

## SC-04 Order already cancelled
Kind: model path
Rules: R-02
World:
1. The order is already cancelled
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders

## SC-05 No order named, order list fails
Kind: model path
Rules: R-09
World:
1. The order is placed or processing
2. customer asks to cancel an order without naming it
3. order list call fails with an error

## SC-06 Order number matches none of the customer's orders
Kind: model path
Rules: R-03
World:
1. The order is placed or processing
2. customer asks to cancel an order number that matches none of their orders
3. order list call answers with the customer's orders

## SC-07 Order list gets no answer, then fails
Kind: model path
Rules: R-13, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call gets no answer
4. order list call fails with an error

## SC-08 Customer leaves at the proposal
Kind: model path
Rules: R-05
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer stops answering

## SC-09 Two open orders, none named, customer leaves
Kind: model path
Rules: R-04
World:
1. The order is placed or processing, and the customer has a second open order
2. customer asks to cancel an order without naming it
3. order list call answers with the customer's orders
4. customer stops answering

## SC-10 Yes, but the order shipped before the cancel
Kind: model path
Rules: R-05, R-01
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers not cancellable: the order has shipped or been delivered

## SC-11 Customer changes the proposal after the yes, then leaves
Kind: model path
Rules: R-06
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes and then changes the proposal
5. customer stops answering

## SC-12 Customer says no
Kind: model path
Rules: R-05, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says no

## SC-13 Customer names the order after being asked, then leaves
Kind: model path
Rules: R-04, R-05
World:
1. The order is placed or processing, and the customer has a second open order
2. customer asks to cancel an order without naming it
3. order list call answers with the customer's orders
4. customer names the order
5. customer stops answering

## SC-14 Order cancelled and refunded
Kind: model path
Rules: R-05, R-07, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund for the confirmed amount

## SC-15 Cancel call answers order not found
Kind: model path
Rules: R-11, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers order not found
6. follow-up call answers created

## SC-16 Cancel call unanswered, read shows it cancelled
Kind: model path
Rules: R-11, R-07, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. order list shows the order cancelled
7. refund call answers with a refund for the confirmed amount

## SC-17 Cancel call unanswered, still open, second cancel refused
Kind: model path
Rules: R-11, R-01
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing cancelled)
6. order list shows the order still placed or processing
7. cancel call answers not cancellable: the order has shipped or been delivered

## SC-18 Cancel call unanswered, read shows the order shipped
Kind: model path
Rules: R-11, R-01
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing cancelled, the order has shipped)
6. order list shows the order shipped

## SC-19 Refund for a different amount
Kind: model path
Rules: R-12, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund for a different amount
7. follow-up call answers created

## SC-20 Failed refund
Kind: model path
Rules: R-08, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a failed refund (a lasting error)
7. follow-up call answers created

## SC-21 Passing refund error, second call refunds
Kind: model path
Rules: R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a passing error, and creates no refund
7. refund call answers with a refund for the confirmed amount

## SC-22 Refund call answers order not cancelled
Kind: model path
Rules: R-08, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers order not cancelled
7. follow-up call answers created

## SC-23 Refund call unanswered though refunded, second call returns the refund
Kind: model path
Rules: R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created)
7. refund call answers with the refund that exists, for the confirmed amount

## SC-24 Refund call unanswered, refund for a different amount
Kind: model path
Rules: R-08, R-12, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created, different amount)
7. refund call answers with the refund that exists, for a different amount
8. follow-up call answers created

## SC-25 Refund call unanswered, refund failed
Kind: model path
Rules: R-08, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (failed refund created)
7. refund call answers with the refund that exists, failed
8. follow-up call answers created

## SC-26 Refund call unanswered, nothing created, second call refunds
Kind: model path
Rules: R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (nothing created)
7. refund call answers with a refund for the confirmed amount

## SC-27 Follow-up unanswered once, then created
Kind: model path
Rules: R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers order not found
6. follow-up call gets no answer
7. follow-up call answers created

## SC-28 Cancel call unanswered, re-read unanswered, then shows it cancelled
Kind: model path
Rules: R-11, R-13, R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. order list call gets no answer on the re-read
7. order list shows the order cancelled
8. refund call answers with a refund for the confirmed amount

## SC-29 Cancel call unanswered, re-read fails
Kind: model path
Rules: R-11, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. order list call fails with an error on the re-read
7. follow-up call answers created

## SC-30 Both refund calls unanswered, read shows the refund
Kind: model path
Rules: R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created)
7. refund call gets no answer (no second refund)
8. order list shows a refund for the confirmed amount

## SC-31 Order not found, follow-up unanswered twice
Kind: model path
Rules: R-11, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers order not found
6. follow-up call gets no answer
7. follow-up call gets no answer

## SC-32 Refund error, then no answer, re-read unanswered, then shows the refund
Kind: model path
Rules: R-08, R-13, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a passing error, and creates no refund
7. refund call gets no answer (refund created)
8. order list call gets no answer on the re-read
9. order list shows a refund for the confirmed amount

## SC-33 Refund error, then no answer, re-read fails
Kind: model path
Rules: R-08, R-09, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a passing error, and creates no refund
7. refund call gets no answer (refund created)
8. order list call fails with an error on the re-read
9. follow-up call answers created

## SC-34 Refund error, then no answer, read shows a different amount
Kind: model path
Rules: R-08, R-12, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a passing error, and creates no refund
7. refund call gets no answer (refund created, different amount)
8. order list shows a refund for a different amount
9. follow-up call answers created

## SC-35 Refund error, then no answer, read shows a failed refund
Kind: model path
Rules: R-08, R-09, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a passing error, and creates no refund
7. refund call gets no answer (failed refund created)
8. order list shows a failed refund
9. follow-up call answers created

## SC-36 Refund error, then no answer, read shows no refund
Kind: model path
Rules: R-08, R-09, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a passing error, and creates no refund
7. refund call gets no answer (nothing created)
8. order list shows no refund
9. follow-up call answers created

## SC-37 Different amount, follow-up unanswered twice
Kind: model path
Rules: R-12, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a refund for a different amount
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-38 Failed refund, follow-up unanswered twice
Kind: model path
Rules: R-08, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a failed refund (a lasting error)
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-39 Cancel outcome unknown, follow-up unanswered twice
Kind: model path
Rules: R-11, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. order list call fails with an error on the re-read
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-40 Refund status unknown, follow-up unanswered twice
Kind: model path
Rules: R-09, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a passing error, and creates no refund
7. refund call gets no answer (refund created)
8. order list call fails with an error on the re-read
9. follow-up call gets no answer
10. follow-up call gets no answer

## SC-41 Refund not confirmed, follow-up unanswered twice
Kind: model path
Rules: R-09, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with a passing error, and creates no refund
7. refund call gets no answer (failed refund created)
8. order list shows a failed refund
9. follow-up call gets no answer
10. follow-up call gets no answer

## SC-42 Second cancel call also unanswered
Kind: model path
Rules: R-11, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing cancelled)
6. order list shows the order still placed or processing
7. cancel call gets no answer (nothing cancelled)
8. follow-up call answers created

## SC-43 Customer asks to cancel part of an order
Kind: conversational
Rules: R-05
Why not a path: the model holds the whole order as one thing, so it cannot ask to cancel only some of its items.

## SC-44 Customer asks for the refund as store credit or to another card
Kind: conversational
Rules: R-05
Why not a path: the model's proposal always refunds to the order's payment method; a request for another destination is words in the conversation the model does not hold.

## SC-45 Customer asks when the money will arrive
Kind: conversational
Rules: R-09
Why not a path: what the agent promises about timing is wording, which the model does not hold.

## SC-46 Customer asks to cancel two orders in one message
Kind: conversational
Rules: R-04, R-05
Why not a path: one run of the model is one order; two requests in one message need two proposals, each with its own yes.

## SC-47 Customer only says they want to cancel, or asks about an order
Kind: conversational
Rules: R-05
Why not a path: the model has one "customer says yes" step; telling a statement of intent or a question apart from a yes happens in the words.

## SC-48 Customer asks about an order number that belongs to someone else
Kind: conversational
Rules: R-03
Why not a path: the order system lists only the signed-in customer's orders, so the model sees such a number only as one that matches none of their orders.
