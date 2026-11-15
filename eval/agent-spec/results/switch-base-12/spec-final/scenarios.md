# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 Order list fails at the start
Kind: model path
Rules: R-01
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call fails with an error

## SC-02 Shipped or delivered order
Kind: model path
Rules: R-03
World:
1. The order has shipped or been delivered
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders

## SC-03 Order already cancelled
Kind: model path
Rules: R-03
World:
1. The order is already cancelled
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders

## SC-04 Two open orders, list fails
Kind: model path
Rules: R-01
World:
1. The customer has two open orders
2. customer asks to cancel the order by its number
3. list call fails with an error

## SC-05 Order number that is none of the customer's
Kind: model path
Rules: R-01
World:
1. The order is placed or processing
2. customer asks to cancel an order number that is none of theirs
3. list call answers with the customer's orders

## SC-06 Some items only, list fails
Kind: model path
Rules: R-01
World:
1. The order is placed or processing
2. customer asks to cancel only some items of the order
3. list call fails with an error

## SC-07 "My order" with two open orders, list fails
Kind: model path
Rules: R-01
World:
1. The customer has two open orders
2. customer asks to cancel "my order" without saying which
3. list call fails with an error

## SC-08 Order list unanswered, then fails
Kind: model path
Rules: R-01
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call gets no answer
4. list call fails with an error

## SC-09 Customer leaves at the proposal
Kind: model path
Rules: R-04, R-05
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer stops answering

## SC-10 Some items only, customer leaves
Kind: model path
Rules: R-03
World:
1. The order is placed or processing
2. customer asks to cancel only some items of the order
3. list call answers with the customer's orders
4. customer stops answering

## SC-11 Two open orders, agent asks which, customer leaves
Kind: model path
Rules: R-02
World:
1. The customer has two open orders
2. customer asks to cancel "my order" without saying which
3. list call answers with the customer's orders
4. customer stops answering

## SC-12 Order shipped before the cancel went through
Kind: model path
Rules: R-04, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers the order cannot be cancelled: it has shipped

## SC-13 Customer changes the proposal after the yes, then leaves
Kind: model path
Rules: R-04, R-05
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes, then asks for a different refund amount or payment method
5. customer stops answering

## SC-14 Customer says no
Kind: model path
Rules: R-04
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says no

## SC-15 Some items, then the whole order, customer leaves at the proposal
Kind: model path
Rules: R-03, R-04
World:
1. The order is placed or processing
2. customer asks to cancel only some items of the order
3. list call answers with the customer's orders
4. customer asks to cancel the whole order
5. customer stops answering

## SC-16 Two open orders, customer names one, leaves at the proposal
Kind: model path
Rules: R-02, R-04
World:
1. The customer has two open orders
2. customer asks to cancel "my order" without saying which
3. list call answers with the customer's orders
4. customer names the order to cancel
5. customer stops answering

## SC-17 Cancelled and refund issued
Kind: model path
Rules: R-04, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers issued

## SC-18 Cancel call answers order not found
Kind: model path
Rules: R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers the order was not found

## SC-19 Cancel unanswered, re-read shows cancelled, refund issued
Kind: model path
Rules: R-07, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. list call answers with the customer's orders
7. refund call answers issued

## SC-20 Cancel unanswered, nothing changed, second cancel finds it shipped
Kind: model path
Rules: R-07, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (nothing changed)
6. list call answers with the customer's orders
7. cancel call answers the order cannot be cancelled: it has shipped

## SC-21 Cancel unanswered, re-read shows it shipped
Kind: model path
Rules: R-07, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (the order shipped meanwhile)
6. list call answers with the customer's orders

## SC-22 Cancelled and refund pending
Kind: model path
Rules: R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers pending

## SC-23 Refund amount differs from the confirmed total
Kind: model path
Rules: R-10, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with an amount that differs from the confirmed total
7. follow-up task call answers created

## SC-24 Refund failed
Kind: model path
Rules: R-08, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers failed
7. follow-up task call answers created

## SC-25 Transient refund error, then issued
Kind: model path
Rules: R-08, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call answers issued

## SC-26 Refund call answers the order is not cancelled
Kind: model path
Rules: R-06, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers the order is not cancelled
7. follow-up task call answers created

## SC-27 Refund unanswered (created), second call answers pending
Kind: model path
Rules: R-09, R-05, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund created)
7. refund call answers pending

## SC-28 Refund unanswered (failed), second call answers failed
Kind: model path
Rules: R-09, R-08, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (refund failed)
7. refund call answers failed
8. follow-up task call answers created

## SC-29 Refund unanswered (nothing created), second call answers issued
Kind: model path
Rules: R-09, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call gets no answer (no refund created)
7. refund call answers issued

## SC-30 Cancel unanswered, re-read unanswered then answers cancelled
Kind: model path
Rules: R-07, R-06, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. list call gets no answer
7. list call answers with the customer's orders
8. refund call answers issued

## SC-31 Cancel unanswered, re-read fails
Kind: model path
Rules: R-07, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call gets no answer (order cancelled)
6. list call fails with an error
7. follow-up task call answers created

## SC-32 Follow-up task call unanswered (created), second call created
Kind: model path
Rules: R-12, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with an amount that differs from the confirmed total
7. follow-up task call gets no answer (task created)
8. follow-up task call answers created

## SC-33 Follow-up task call unanswered (not created), second call created
Kind: model path
Rules: R-12, R-10
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with an amount that differs from the confirmed total
7. follow-up task call gets no answer (no task created)
8. follow-up task call answers created

## SC-34 Transient refund error, second refund call unanswered, re-read shows pending
Kind: model path
Rules: R-08, R-09, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (refund created)
8. list call answers with the customer's orders

## SC-35 Refund re-read unanswered, then answers
Kind: model path
Rules: R-09, R-11
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (refund created)
8. list call gets no answer
9. list call answers with the customer's orders

## SC-36 Refund re-read fails
Kind: model path
Rules: R-09, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (refund created)
8. list call fails with an error
9. follow-up task call answers created

## SC-37 Amount differs, follow-up task call unanswered twice
Kind: model path
Rules: R-10, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers with an amount that differs from the confirmed total
7. follow-up task call gets no answer (task created)
8. follow-up task call gets no answer (task created)

## SC-38 Refund failed, follow-up task call unanswered twice
Kind: model path
Rules: R-08, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers failed
7. follow-up task call gets no answer (task created)
8. follow-up task call gets no answer (task created)

## SC-39 Order not cancelled at refund, follow-up task call unanswered twice
Kind: model path
Rules: R-06, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers the order is not cancelled
7. follow-up task call gets no answer (task created)
8. follow-up task call gets no answer (task created)

## SC-40 Refund re-read fails, follow-up task call unanswered twice
Kind: model path
Rules: R-09, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (refund created)
8. list call fails with an error
9. follow-up task call gets no answer (task created)
10. follow-up task call gets no answer (task created)

## SC-41 Two orders in one message
Kind: conversational
Rules: R-13, R-04
Why not a path: the model holds one order per conversation, so it cannot hold a request that names two orders; the agent must take one order, finish it with its own proposal and yes, then start the next.

## SC-42 A question at the proposal is not a yes
Kind: conversational
Rules: R-04
Why not a path: the model's customer answers the proposal only with yes, a change, no or silence; a question such as "will I get all my money back?" must be answered without sending the cancel call.

## SC-43 The customer asks when the money arrives
Kind: conversational
Rules: R-11
Why not a path: the model does not hold what the agent says about time; the agent must name no date or number of days.

## SC-44 The customer asks for store credit instead
Kind: conversational
Rules: R-05
Why not a path: the model does not carry the refund's form; the agent must offer only a refund of the total paid to the order's payment method.

## SC-45 A second order named mid-conversation
Kind: conversational
Rules: R-13, R-01
Why not a path: the model has one order; when the customer names another of their orders after the proposal, the agent must treat it as a new request with its own proposal and yes, and the earlier yes covers nothing for it.

## SC-46 Refund re-read shows the refund failed, staff will follow up
Kind: model path
Rules: R-08, R-09, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (refund failed)
8. list call answers with the customer's orders
9. follow-up task call answers created

## SC-47 Refund re-read shows the refund failed, follow-up task call unanswered twice
Kind: model path
Rules: R-09, R-12
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. list call answers with the customer's orders
4. customer says yes
5. cancel call answers cancelled
6. refund call answers a transient error
7. refund call gets no answer (refund failed)
8. list call answers with the customer's orders
9. follow-up task call gets no answer (task created)
10. follow-up task call gets no answer (task created)

