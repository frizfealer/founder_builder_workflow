# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 An order number that matches none of the customer's orders
Kind: model path
Rules: R-01
World:
1. The customer has one order that has not shipped
2. customer names an order number that matches none of their orders
3. order list call answers with the customer's orders

## SC-02 An order number that matches none, while two orders are open
Kind: model path
Rules: R-01
World:
1. The customer has two orders that have not shipped
2. customer names an order number that matches none of their orders
3. order list call answers with the customer's orders

## SC-03 A shipped order is refused
Kind: model path
Rules: R-02
World:
1. The customer's order has shipped or been delivered
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders

## SC-04 An order that is already cancelled
Kind: model path
Rules: R-02
World:
1. The customer's order is already cancelled
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders

## SC-05 Some items only, then the customer leaves
Kind: model path
Rules: R-03
World:
1. The customer has one order that has not shipped
2. customer asks to cancel only some items of an order
3. order list call answers with the customer's orders
4. customer stops answering

## SC-06 Unclear which of two orders, then the customer leaves
Kind: model path
Rules: R-04
World:
1. The customer has two orders that have not shipped
2. customer asks to cancel "my order" without saying which
3. order list call answers with the customer's orders
4. customer stops answering

## SC-07 The customer leaves at the proposal
Kind: model path
Rules: R-05
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer stops answering

## SC-08 The order ships between the read and the cancel
Kind: model path
Rules: R-05, R-07
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers not cancellable: the order shipped since it was read

## SC-09 The customer says no
Kind: model path
Rules: R-05
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says no

## SC-10 Some items, then the whole order
Kind: model path
Rules: R-03, R-05
World:
1. The customer has one order that has not shipped
2. customer asks to cancel only some items of an order
3. order list call answers with the customer's orders
4. customer asks to cancel the whole order
5. customer stops answering

## SC-11 The customer switches to their other order
Kind: model path
Rules: R-04, R-05
World:
1. The customer has two orders that have not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes, but for their other order
5. customer stops answering

## SC-12 The customer names one of two orders
Kind: model path
Rules: R-04
World:
1. The customer has two orders that have not shipped
2. customer asks to cancel "my order" without saying which
3. order list call answers with the customer's orders
4. customer names one of the orders
5. customer stops answering

## SC-13 Cancelled and refunded
Kind: model path
Rules: R-05, R-06, R-07, R-12
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns the refund, issued, for the confirmed amount

## SC-14 The cancel call answers order not found
Kind: model path
Rules: R-12
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers order not found

## SC-15 Cancel unanswered; the order read shows it cancelled; refunded
Kind: model path
Rules: R-07, R-08, R-12
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. order read shows the order cancelled
7. refund call returns the refund, issued, for the confirmed amount

## SC-16 Cancel unanswered; the order read shows it shipped
Kind: model path
Rules: R-08, R-12
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing cancelled)
6. order read shows the order shipped or delivered

## SC-17 The refund is pending
Kind: model path
Rules: R-06, R-12
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns the refund, pending, for the confirmed amount

## SC-18 The refund amount differs
Kind: model path
Rules: R-11
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. staff follow-up call answers created

## SC-19 The refund fails with a lasting error
Kind: model path
Rules: R-09, R-10
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund with status failed (a lasting error)
7. staff follow-up call answers created

## SC-20 The refund call answers order not cancelled
Kind: model path
Rules: R-10
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers order not cancelled
7. staff follow-up call answers created

## SC-21 A passing error, then the refund
Kind: model path
Rules: R-09, R-12
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a passing error (no refund created)
7. refund call returns the refund, issued, for the confirmed amount

## SC-22 Two refund calls unanswered; the refund read shows the refund
Kind: model path
Rules: R-09, R-10, R-12
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created)
7. refund call gets no answer (refund exists)
8. refund read shows the refund

## SC-23 A refund call unanswered with nothing made, then one unanswered that made it
Kind: model path
Rules: R-09, R-10, R-12
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (no refund created)
7. refund call gets no answer (refund created)
8. refund read shows the refund

## SC-24 Cancel unanswered; the order read fails
Kind: model path
Rules: R-08
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. order read fails
7. staff follow-up call answers created

## SC-25 Cancel unanswered; the order is still open; the second cancel finds it shipped
Kind: model path
Rules: R-07, R-08
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing cancelled)
6. order read shows the order still placed or processing
7. cancel call answers not cancellable: the order shipped since it was read

## SC-26 The staff call is unanswered though the task was made, and is sent again
Kind: model path
Rules: R-10, R-11
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. staff follow-up call gets no answer (task created)
8. staff follow-up call answers created

## SC-27 The staff call is unanswered with no task, and is sent again
Kind: model path
Rules: R-10, R-11
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. staff follow-up call gets no answer (no task)
8. staff follow-up call answers created

## SC-28 The second refund call returns the refund the first one made
Kind: model path
Rules: R-06, R-09, R-10
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created)
7. refund call returns the existing refund
8. refund read shows the refund

## SC-29 The refund read fails
Kind: model path
Rules: R-10
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a passing error (no refund created)
7. refund call gets no answer (refund created)
8. refund read fails
9. staff follow-up call answers created

## SC-30 The refund read shows no refund
Kind: model path
Rules: R-10
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a passing error (no refund created)
7. refund call gets no answer (no refund created)
8. refund read shows no refund
9. staff follow-up call answers created

## SC-31 The refund amount differs, and staff cannot be reached
Kind: model path
Rules: R-10, R-11
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. staff follow-up call gets no answer (task created)
8. staff follow-up call gets no answer (task created)

## SC-32 The refund fails, and staff cannot be reached
Kind: model path
Rules: R-10
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund with status failed (a lasting error)
7. staff follow-up call gets no answer (task created)
8. staff follow-up call gets no answer (task created)

## SC-33 The refund call answers order not cancelled, and staff cannot be reached
Kind: model path
Rules: R-10
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers order not cancelled
7. staff follow-up call gets no answer (task created)
8. staff follow-up call gets no answer (task created)

## SC-34 The cancellation outcome is unknown, and staff cannot be reached
Kind: model path
Rules: R-08, R-10
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. order read fails
7. staff follow-up call gets no answer (task created)
8. staff follow-up call gets no answer (task created)

## SC-35 Two cancel calls unanswered while the order stays open
Kind: model path
Rules: R-08
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing cancelled)
6. order read shows the order still placed or processing
7. cancel call gets no answer (nothing cancelled)
8. order read shows the order still placed or processing
9. staff follow-up call answers created

## SC-36 The refund status is unknown, and staff cannot be reached
Kind: model path
Rules: R-10
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a passing error (no refund created)
7. refund call gets no answer (refund created)
8. refund read fails
9. staff follow-up call gets no answer (task created)
10. staff follow-up call gets no answer (task created)

## SC-37 Two cancel calls unanswered, and staff cannot be reached
Kind: model path
Rules: R-08, R-10
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing cancelled)
6. order read shows the order still placed or processing
7. cancel call gets no answer (nothing cancelled)
8. order read shows the order still placed or processing
9. staff follow-up call gets no answer (task created)
10. staff follow-up call gets no answer (task created)

## SC-38 Two orders in one message
Kind: conversational
Rules: R-04, R-05
Why not a path: the model is one order per conversation; here the customer asks to cancel two orders at once, and each must get its own proposal and its own yes.

## SC-39 A second order after the first is done
Kind: conversational
Rules: R-05
Why not a path: the model ends after one order; the customer then asks to cancel another order, which starts again from reading the orders, with its own proposal and yes.

## SC-40 The order list call keeps timing out
Kind: conversational
Rules: R-01
Why not a path: the model lets the read time out and be sent again; it cannot show a customer left waiting while every read times out, because the owner set no end to it.

## SC-41 The customer asks for store credit, part of the refund, or a refund to another card
Kind: conversational
Rules: R-05, R-06
Why not a path: the model has no step for a counter-offer; the agent offers only the full total paid, back to the payment method paid with, with no fee and no store credit, and a change to the proposal needs a new yes.

## SC-42 The customer asks when the money will arrive
Kind: conversational
Rules: R-12
Why not a path: the model does not hold the agent's wording; the agent promises nothing about when the money arrives.

## SC-43 The customer asks to return a shipped order
Kind: conversational
Rules: R-02
Why not a path: returns are a separate process the model does not hold; the agent sends no cancel call and says returns are a separate process.

## SC-44 The order list call times out and is sent again
Kind: model path
Rules: R-01
World:
1. The customer has one order that has not shipped
2. customer asks to cancel an order, naming it
3. order list call times out
4. order list call answers with the customer's orders
5. customer stops answering
