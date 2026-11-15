# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 First list fails, one open order
Kind: model path
Rules: R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call fails

## SC-02 First list fails, two open orders
Kind: model path
Rules: R-10
World:
1. The customer has two open orders
2. customer asks to cancel an order by its number
3. list call fails

## SC-03 Order has shipped: refused, returns are a separate process
Kind: model path
Rules: R-02
World:
1. The customer's order has shipped or been delivered
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders

## SC-04 Order already cancelled: nothing changed
Kind: model path
Rules: R-02
World:
1. The customer's order is already cancelled
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders

## SC-05 "Cancel my order", first list fails
Kind: model path
Rules: R-10
World:
1. The customer has one open order
2. customer asks to cancel my order
3. list call fails

## SC-06 Unknown order number, first list fails
Kind: model path
Rules: R-10
World:
1. The customer has one open order
2. customer asks to cancel an order number that matches none of their orders
3. list call fails

## SC-07 Some items asked for, first list fails
Kind: model path
Rules: R-10, R-03
World:
1. The customer has one open order
2. customer asks to cancel some items of an order
3. list call fails

## SC-08 First list unanswered, tried again, then fails
Kind: model path
Rules: R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call gets no answer
4. list call fails

## SC-09 Proposal made, customer leaves
Kind: model path
Rules: R-04
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer stops answering

## SC-10 Order number matches none, customer leaves
Kind: model path
Rules: R-01
World:
1. The customer has one open order
2. customer asks to cancel an order number that matches none of their orders
3. list call answers with the customer's orders
4. customer stops answering

## SC-11 Some items asked for: only whole orders
Kind: model path
Rules: R-03
World:
1. The customer has one open order
2. customer asks to cancel some items of an order
3. list call answers with the customer's orders
4. customer stops answering

## SC-12 Two open orders and "cancel my order": agent asks which
Kind: model path
Rules: R-04
World:
1. The customer has two open orders
2. customer asks to cancel my order
3. list call answers with the customer's orders
4. customer stops answering

## SC-13 Yes, then the order shipped before the cancel
Kind: model path
Rules: R-06, R-04
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers the order is not cancellable: shipped

## SC-14 Customer says no: nothing changed
Kind: model path
Rules: R-04
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says no

## SC-15 Unknown number, then one of the customer's orders
Kind: model path
Rules: R-01, R-04
World:
1. The customer has one open order
2. customer asks to cancel an order number that matches none of their orders
3. list call answers with the customer's orders
4. customer names one of their orders by its number
5. customer stops answering

## SC-16 Two order numbers that match none
Kind: model path
Rules: R-01
World:
1. The customer has one open order
2. customer asks to cancel an order number that matches none of their orders
3. list call answers with the customer's orders
4. customer names another order number that matches none of their orders
5. customer stops answering

## SC-17 Some items, then the whole order
Kind: model path
Rules: R-03, R-04
World:
1. The customer has one open order
2. customer asks to cancel some items of an order
3. list call answers with the customer's orders
4. customer asks to cancel the whole order
5. customer stops answering

## SC-18 Yes, but switches to the other open order
Kind: model path
Rules: R-04
World:
1. The customer has two open orders
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes but switches to their other open order
5. customer stops answering

## SC-19 Cancelled and refunded
Kind: model path
Rules: R-04, R-05, R-06, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund issued for the confirmed amount

## SC-20 Cancel answers order not found: staff follow up
Kind: model path
Rules: R-07, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers the order was not found
6. follow-up call answers created

## SC-21 Unanswered cancel that did cancel, then refunded
Kind: model path
Rules: R-07, R-06, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. list call shows the order cancelled
7. refund call returns a refund issued for the confirmed amount

## SC-22 Unanswered cancel, order still open, resent, then shipped
Kind: model path
Rules: R-07, R-06
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing changed)
6. list call shows the order still open
7. cancel call answers the order is not cancellable: shipped

## SC-23 Unanswered cancel, order shipped meanwhile
Kind: model path
Rules: R-07, R-06
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order shipped meanwhile)
6. list call shows the order shipped

## SC-24 Third order number that matches none: sent to support
Kind: model path
Rules: R-01
World:
1. The customer has one open order
2. customer asks to cancel an order number that matches none of their orders
3. list call answers with the customer's orders
4. customer names another order number that matches none of their orders
5. customer names another order number that matches none of their orders

## SC-25 Refund pending
Kind: model path
Rules: R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund pending for the confirmed amount

## SC-26 Refund for a different amount: staff follow up
Kind: model path
Rules: R-11, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. follow-up call answers created

## SC-27 Refund failed: staff follow up
Kind: model path
Rules: R-08, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund with status failed
7. follow-up call answers created

## SC-28 Transient refund error, retried, refunded
Kind: model path
Rules: R-08, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a transient error
7. refund call returns a refund issued for the confirmed amount

## SC-29 Refund answers order not cancelled: staff follow up
Kind: model path
Rules: R-08, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers the order is not cancelled
7. follow-up call answers created

## SC-30 Two unanswered refund calls, list shows it issued
Kind: model path
Rules: R-09, R-05, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund issued)
7. refund call gets no answer (refund exists)
8. list call shows the refund issued

## SC-31 Unanswered refund, retry unanswered, list shows it issued
Kind: model path
Rules: R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (no refund created)
7. refund call gets no answer (refund issued)
8. list call shows the refund issued

## SC-32 Follow-up call unanswered once, then created
Kind: model path
Rules: R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers the order was not found
6. follow-up call gets no answer
7. follow-up call answers created

## SC-33 Unanswered cancel, list fails: staff follow up
Kind: model path
Rules: R-07, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. list call fails
7. follow-up call answers created

## SC-34 Unanswered cancel, list unanswered then shows it cancelled
Kind: model path
Rules: R-07, R-06, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. list call gets no answer
7. list call shows the order cancelled
8. refund call returns a refund issued for the confirmed amount

## SC-35 Unanswered refund, retry returns it, list confirms
Kind: model path
Rules: R-09, R-05, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund issued)
7. refund call returns the refund that exists
8. list call shows the refund issued

## SC-36 Order not found and both follow-up calls unanswered: sent to support
Kind: model path
Rules: R-07, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers the order was not found
6. follow-up call gets no answer
7. follow-up call gets no answer

## SC-37 Transient error, then unanswered refund, list fails
Kind: model path
Rules: R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a transient error
7. refund call gets no answer (refund issued)
8. list call fails
9. follow-up call answers created

## SC-38 Transient error, unanswered refund, list unanswered then shows it issued
Kind: model path
Rules: R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a transient error
7. refund call gets no answer (refund issued)
8. list call gets no answer
9. list call shows the refund issued

## SC-39 Transient error, unanswered refund, list shows no refund
Kind: model path
Rules: R-09, R-08, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a transient error
7. refund call gets no answer (no refund created)
8. list call shows no refund
9. follow-up call answers created

## SC-40 Unanswered refund, retry pending, list shows it pending
Kind: model path
Rules: R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (no refund created)
7. refund call returns a refund pending for the confirmed amount
8. list call shows the refund pending

## SC-41 Unanswered refund, retry for a different amount, list shows it
Kind: model path
Rules: R-09, R-11, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (no refund created)
7. refund call returns a refund for a different amount
8. list call shows a refund for a different amount
9. follow-up call answers created

## SC-42 Unanswered refund, retry failed, list shows it failed
Kind: model path
Rules: R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (no refund created)
7. refund call returns a refund with status failed
8. list call shows the refund failed
9. follow-up call answers created

## SC-43 Different amount and both follow-up calls unanswered
Kind: model path
Rules: R-11, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund for a different amount
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-44 Refund failed and both follow-up calls unanswered
Kind: model path
Rules: R-08, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund with status failed
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-45 Cancel outcome unknown and both follow-up calls unanswered
Kind: model path
Rules: R-07, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. list call fails
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-46 Two unanswered cancels, order still open: could not be cancelled
Kind: model path
Rules: R-07
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing changed)
6. list call shows the order still open
7. cancel call gets no answer (nothing changed)
8. list call shows the order still open

## SC-47 Refund status unknown and both follow-up calls unanswered
Kind: model path
Rules: R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a transient error
7. refund call gets no answer (refund issued)
8. list call fails
9. follow-up call gets no answer
10. follow-up call gets no answer

## SC-48 Refund not confirmed and both follow-up calls unanswered
Kind: model path
Rules: R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a transient error
7. refund call gets no answer (no refund created)
8. list call shows no refund
9. follow-up call gets no answer
10. follow-up call gets no answer

## SC-49 Two orders to cancel in one message
Kind: conversational
Rules: R-13, R-04
Why not a path: the model holds one request about one order; a message naming two orders, each needing its own proposal and yes, is outside it.

## SC-50 After one order is done, the customer asks to cancel another
Kind: conversational
Rules: R-13
Why not a path: a request about a second order after the first is finished starts a new run of the model.

## SC-51 The customer asks when the money will arrive
Kind: conversational
Rules: R-10
Why not a path: the model has no customer questions after the refund; the agent's answer must promise nothing about when the money arrives.

## SC-52 The customer asks for store credit, or a smaller refund kept on the order
Kind: conversational
Rules: R-05, R-03
Why not a path: the model's proposal always carries the total paid to the payment method; a customer asking for another amount or for store credit is outside it.
