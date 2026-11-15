# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 The orders cannot be read
Kind: model path
Rules: R-01, R-02
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list fails

## SC-02 A shipped or delivered order is refused
Kind: model path
Rules: R-01, R-02
World:
1. The order has shipped or been delivered
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders

## SC-03 An already cancelled order is reported
Kind: model path
Rules: R-01, R-02
World:
1. The order is already cancelled
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders

## SC-04 An order number that matches none of the customer's orders
Kind: model path
Rules: R-01, R-02
World:
1. The order is placed or processing
2. customer gives an order number that matches none of their orders
3. order list returns the customer's orders

## SC-05 Two open orders, and the orders cannot be read
Kind: model path
Rules: R-01, R-02, R-04
World:
1. The order is placed or processing
2. customer says cancel my order, and has two open orders
3. order list fails

## SC-06 The order list times out, then fails
Kind: model path
Rules: R-01, R-02
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list times out
4. order list fails

## SC-07 Customer leaves at the proposal
Kind: model path
Rules: R-01, R-04
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer stops answering

## SC-08 Two open orders, customer leaves when asked which
Kind: model path
Rules: R-01, R-04
World:
1. The order is placed or processing
2. customer says cancel my order, and has two open orders
3. order list returns the customer's orders
4. customer stops answering

## SC-09 The order shipped before the cancel call
Kind: model path
Rules: R-01, R-04, R-06
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers not cancellable: the order has shipped

## SC-10 Customer says no to the proposal
Kind: model path
Rules: R-01, R-04
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says no

## SC-11 Two open orders, customer names one, then leaves
Kind: model path
Rules: R-01, R-04
World:
1. The order is placed or processing
2. customer says cancel my order, and has two open orders
3. order list returns the customer's orders
4. customer names the order
5. customer stops answering

## SC-12 Order cancelled and refunded
Kind: model path
Rules: R-01, R-04, R-05, R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a pending or issued refund for the confirmed amount and payment method

## SC-13 The cancel call answers order not found
Kind: model path
Rules: R-01, R-04, R-06
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers order not found

## SC-14 Cancel unanswered but done, re-read shows it cancelled, refund made
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call times out (order cancelled)
6. order re-read shows the order cancelled
7. refund call returns a pending or issued refund for the confirmed amount and payment method

## SC-15 Cancel unanswered, order still open, second cancel finds it shipped
Kind: model path
Rules: R-01, R-04, R-06
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call times out (nothing cancelled)
6. order re-read shows the order placed or processing
7. cancel call answers not cancellable: the order has shipped

## SC-16 Cancel unanswered while the order shipped
Kind: model path
Rules: R-01, R-04, R-06
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call times out (the order shipped meanwhile)
6. order re-read shows the order shipped

## SC-17 The refund differs from the confirmed one
Kind: model path
Rules: R-01, R-04, R-05, R-10, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund with a different amount or payment method
7. handoff call creates the staff task

## SC-18 The refund call returns a failed refund
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-09, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a failed refund
7. handoff call creates the staff task

## SC-19 A transient refund error, then the refund is made
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. second refund call returns a pending or issued refund for the confirmed amount and payment method

## SC-20 The refund call answers order not cancelled
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers order not cancelled
7. handoff call creates the staff task

## SC-21 Refund unanswered twice, re-read shows the refund made
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (refund made)
7. second refund call times out (refund exists)
8. refund re-read shows a pending or issued refund for the confirmed amount and payment method

## SC-22 Refund unanswered twice, re-read shows a failed refund
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-09, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (failed refund made)
7. second refund call times out (refund exists)
8. refund re-read shows a failed refund
9. handoff call creates the staff task

## SC-23 Refund unanswered, made on the second call, re-read shows it
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (no refund made)
7. second refund call times out (refund made)
8. refund re-read shows a pending or issued refund for the confirmed amount and payment method

## SC-24 The order re-read times out, then shows the order cancelled
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call times out (order cancelled)
6. order re-read times out
7. order re-read shows the order cancelled
8. refund call returns a pending or issued refund for the confirmed amount and payment method

## SC-25 Cancel unanswered and the re-read fails
Kind: model path
Rules: R-01, R-04, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call times out (order cancelled)
6. order re-read fails
7. handoff call creates the staff task

## SC-26 Handoff unanswered once (task created), then created
Kind: model path
Rules: R-01, R-04, R-05, R-10, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund with a different amount or payment method
7. handoff call times out (task created)
8. handoff call creates the staff task

## SC-27 Handoff unanswered once (no task), then created
Kind: model path
Rules: R-01, R-04, R-05, R-10, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund with a different amount or payment method
7. handoff call times out (no task created)
8. handoff call creates the staff task

## SC-28 A transient error, then a refund that differs
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-10, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. second refund call returns a refund with a different amount or payment method
8. handoff call creates the staff task

## SC-29 A transient error, then a failed refund
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-09, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. second refund call returns a failed refund
8. handoff call creates the staff task

## SC-30 Two transient refund errors
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. second refund call answers a transient error
8. handoff call creates the staff task

## SC-31 A transient error, then order not cancelled
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. second refund call answers order not cancelled
8. handoff call creates the staff task

## SC-32 A transient error, then the second refund call times out with a failed refund
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-09, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. second refund call times out (failed refund made)
8. refund re-read shows a failed refund
9. handoff call creates the staff task

## SC-33 A transient error, then the second refund call times out with no refund
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. second refund call times out (no refund made)
8. refund re-read shows no refund
9. handoff call creates the staff task

## SC-34 Refund unanswered, the second call returns the refund made
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (refund made)
7. second refund call returns the refund it already made
8. refund re-read shows a pending or issued refund for the confirmed amount and payment method

## SC-35 The refund re-read times out, then shows the refund made
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-08, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. second refund call times out (refund made)
8. refund re-read times out
9. refund re-read shows a pending or issued refund for the confirmed amount and payment method

## SC-36 The refund re-read fails
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. second refund call times out (refund made)
8. refund re-read fails
9. handoff call creates the staff task

## SC-37 Refund unanswered, then a refund that differs on the second call and the re-read
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-10, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call times out (no refund made)
7. second refund call returns a refund with a different amount or payment method
8. refund re-read shows a refund with a different amount or payment method
9. handoff call creates the staff task

## SC-38 A refund that differs, and the handoff gets no answer twice
Kind: model path
Rules: R-01, R-04, R-05, R-10, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund with a different amount or payment method
7. handoff call times out (task created)
8. handoff call times out (task created)

## SC-39 A failed refund, and the handoff gets no answer twice
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-09, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a failed refund
7. handoff call times out (task created)
8. handoff call times out (task created)

## SC-40 Cancel outcome unknown, and the handoff gets no answer twice
Kind: model path
Rules: R-01, R-04, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call times out (order cancelled)
6. order re-read fails
7. handoff call times out (task created)
8. handoff call times out (task created)

## SC-41 Two cancel calls unanswered, order still open
Kind: model path
Rules: R-01, R-04, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call times out (nothing cancelled)
6. order re-read shows the order placed or processing
7. cancel call times out (nothing cancelled)
8. order re-read shows the order placed or processing
9. handoff call creates the staff task

## SC-42 Refund status unknown, and the handoff gets no answer twice
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. second refund call times out (refund made)
8. refund re-read fails
9. handoff call times out (task created)
10. handoff call times out (task created)

## SC-43 Refund not confirmed, and the handoff gets no answer twice
Kind: model path
Rules: R-01, R-04, R-05, R-07, R-09, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. second refund call times out (failed refund made)
8. refund re-read shows a failed refund
9. handoff call times out (task created)
10. handoff call times out (task created)

## SC-44 Two cancel calls unanswered, and the handoff gets no answer twice
Kind: model path
Rules: R-01, R-04, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call times out (nothing cancelled)
6. order re-read shows the order placed or processing
7. cancel call times out (nothing cancelled)
8. order re-read shows the order placed or processing
9. handoff call times out (task created)
10. handoff call times out (task created)

## SC-45 Customer asks to cancel only some items
Kind: conversational
Rules: R-03
Why not a path: the model cancels whole orders only, so it has no request for part of an order; the agent must say only the whole order can be cancelled.

## SC-46 Customer changes the proposal after saying yes
Kind: conversational
Rules: R-04
Why not a path: the model has one step for a yes with a change; which change it is (another order, some items only, another payment method) and what the agent says for each is wording the model cannot express. Each must void the yes, and the agent proposes again.

## SC-47 A question about cancelling is not a yes
Kind: conversational
Rules: R-04
Why not a path: the model has one "yes" step; whether "can I still cancel?" or "I might want to cancel" counts as a yes is a matter of wording the model cannot express.

## SC-48 Customer cancels a second order in the same conversation
Kind: conversational
Rules: R-12, R-04
Why not a path: one run of the model is one order; the second order needs its own proposal and its own yes, and the first yes must not cover it.

## SC-49 Customer asks when the money will arrive
Kind: conversational
Rules: R-08
Why not a path: the model has no step for the customer's question about timing; the agent promises nothing about when the money arrives.

## SC-50 Customer asks about an order they did not place
Kind: conversational
Rules: R-01, R-02
Why not a path: the agent sees only the signed-in customer's orders, so the model has no other customer's order; the agent says the number matches none of their orders and changes nothing.

## SC-51 Two requests in one message
Kind: conversational
Rules: R-12, R-04
Why not a path: the model takes one request per run; "cancel HG-10482 and HG-10490" must become two proposals with two yeses, one at a time.

## SC-52 Customer says yes with a change, then leaves
Kind: model path
Rules: R-04, R-01
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes with a change to the proposal
5. customer stops answering

## SC-53 Order not cancelled at the refund, and the handoff gets no answer twice
Kind: model path
Rules: R-04, R-05, R-07, R-11, R-09
World:
1. The order is placed or processing
2. customer asks to cancel the order, naming it
3. order list returns the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers order not cancelled
7. handoff call times out (task created)
8. handoff call times out (task created)
