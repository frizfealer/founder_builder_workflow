# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 One open order, and the order list fails
Kind: model path
Rules: R-01, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call fails with an error

## SC-02 Two open orders, the customer names one, and the order list fails
Kind: model path
Rules: R-01, R-12
World:
1. The customer has two open orders
2. customer asks to cancel an order, naming its number
3. list call fails with an error

## SC-03 The order has shipped and is not cancelled
Kind: model path
Rules: R-01, R-03
World:
1. The customer's order has shipped
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders

## SC-04 The order is already cancelled and nothing changes
Kind: model path
Rules: R-01, R-03
World:
1. The customer's order is already cancelled
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders

## SC-05 The customer names an order number that is not theirs
Kind: model path
Rules: R-01
World:
1. The customer has one open order
2. customer asks to cancel an order number that is not theirs
3. list call answers with the customer's orders

## SC-06 Two open orders, the customer says "my order", and the order list fails
Kind: model path
Rules: R-01, R-02, R-12
World:
1. The customer has two open orders
2. customer asks to cancel "my order" without a number
3. list call fails with an error

## SC-07 The order list gets no answer, then fails
Kind: model path
Rules: R-01, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call gets no answer
4. list call fails with an error

## SC-08 The agent proposes the cancel and refund
Kind: model path
Rules: R-01
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer stops answering

## SC-09 Two open orders and the agent asks which one
Kind: model path
Rules: R-01, R-02
World:
1. The customer has two open orders
2. customer asks to cancel "my order" without a number
3. list call answers with the customer's orders
4. customer stops answering

## SC-10 The customer says yes and the order is cancelled
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-09
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers not cancellable: the order has just shipped

## SC-11 The customer says no and nothing changes
Kind: model path
Rules: R-01, R-04
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says no

## SC-12 The customer switches to their other order after saying yes
Kind: model path
Rules: R-01, R-04, R-05
World:
1. The customer has two open orders
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes, then asks to cancel their other order instead
5. customer stops answering

## SC-13 The customer names one of two open orders
Kind: model path
Rules: R-01, R-02
World:
1. The customer has two open orders
2. customer asks to cancel "my order" without a number
3. list call answers with the customer's orders
4. customer names one order by its number
5. customer stops answering

## SC-14 The cancel goes through and the refund is asked for
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers issued, for the total confirmed

## SC-15 The cancel answers order not found
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers order not found
6. follow-up call answers created

## SC-16 The cancel gets no answer but did cancel the order
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-07, R-08, R-09
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. re-reading the order shows it cancelled
7. refund call answers issued, for the total confirmed

## SC-17 The cancel gets no answer and did not cancel the order
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-07, R-09
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (not cancelled)
6. re-reading the order shows it still open
7. cancel call answers not cancellable: the order has just shipped

## SC-18 The cancel gets no answer while the order ships
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-07, R-09
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (the order has just shipped)
6. re-reading the order shows it shipped

## SC-19 The refund comes back with a different amount
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers issued, for a different amount
7. follow-up call answers created

## SC-20 The refund gets a temporary error
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a temporary error (no refund)
7. refund call answers issued, for the total confirmed

## SC-21 The refund answers order not cancelled
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers order not cancelled
7. follow-up call answers created

## SC-22 The refund fails with a terminal error
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a refund with status failed
7. follow-up call answers created

## SC-23 The refund gets no answer but was created
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created)
7. refund call answers issued, for the total confirmed

## SC-24 The refund gets no answer and was not created
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (no refund)
7. refund call answers issued, for the total confirmed

## SC-25 The follow-up task gets no answer
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers order not found
6. follow-up call gets no answer
7. follow-up call answers created

## SC-26 The order re-read gets no answer
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-07, R-08, R-09, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. re-reading the order gets no answer
7. re-reading the order shows it cancelled
8. refund call answers issued, for the total confirmed

## SC-27 The order re-read fails with an error
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-07, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. re-reading the order fails with an error
7. follow-up call answers created

## SC-28 The agent re-reads the refund
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a temporary error (no refund)
7. refund call gets no answer (refund created)
8. re-reading the refund shows the refund pending or issued

## SC-29 Order not found, and the follow-up task gets no answer twice
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers order not found
6. follow-up call gets no answer
7. follow-up call gets no answer

## SC-30 The refund re-read gets no answer
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10, R-12
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a temporary error (no refund)
7. refund call gets no answer (refund created)
8. re-reading the refund gets no answer
9. re-reading the refund shows the refund pending or issued

## SC-31 The refund re-read fails with an error
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a temporary error (no refund)
7. refund call gets no answer (refund created)
8. re-reading the refund fails with an error
9. follow-up call answers created

## SC-32 The refund re-read shows no refund
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a temporary error (no refund)
7. refund call gets no answer (no refund)
8. re-reading the refund shows no refund
9. follow-up call answers created

## SC-33 The refund re-read shows the refund failed
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (no refund)
7. refund call returns a refund with status failed
8. re-reading the refund shows the refund failed
9. follow-up call answers created

## SC-34 A different refund amount, and the follow-up task gets no answer twice
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10, R-11
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers issued, for a different amount
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-35 The refund not issued, and the follow-up task gets no answer twice
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers order not cancelled
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-36 Cancellation unknown, and the follow-up task gets no answer twice
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-07, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (cancelled)
6. re-reading the order fails with an error
7. follow-up call gets no answer
8. follow-up call gets no answer

## SC-37 Refund status unknown, and the follow-up task gets no answer twice
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a temporary error (no refund)
7. refund call gets no answer (refund created)
8. re-reading the refund fails with an error
9. follow-up call gets no answer
10. follow-up call gets no answer

## SC-38 Refund not confirmed, and the follow-up task gets no answer twice
Kind: model path
Rules: R-01, R-04, R-05, R-06, R-08, R-09, R-10
World:
1. The customer has one open order
2. customer asks to cancel an order, naming its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call returns a temporary error (no refund)
7. refund call gets no answer (no refund)
8. re-reading the refund shows no refund
9. follow-up call gets no answer
10. follow-up call gets no answer

## SC-39 Two orders cancelled in one message
Kind: conversational
Rules: R-02, R-04
Why not a path: The model handles one cancel request per conversation. A customer who asks to cancel two orders in one message must get one proposal per order, and each order is cancelled only after its own yes.

## SC-40 A request about another kind of change
Kind: conversational
Rules: R-03, R-05
Why not a path: The model has no step for a request to return part of an order, change its address or get store credit. The agent changes nothing for such a request; it cancels only whole orders that have not shipped and refunds only to the order's payment method.

## SC-41 The customer asks when the money arrives
Kind: conversational
Rules: R-09
Why not a path: What the agent says about timing is wording, which the model does not hold. The agent promises nothing about when the money arrives.
