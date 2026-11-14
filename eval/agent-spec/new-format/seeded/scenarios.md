# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 Open order cancelled and refunded
Kind: model path
Rules: R-01, R-03, R-04, R-05, R-08
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call returns the refund pending or issued

## SC-02 Two open orders, customer does not say which
Kind: model path
Rules: R-02
World:
1. The order is placed or processing, and a second open order exists
2. customer asks to cancel 'my order' without saying which
3. lookup shows the order placed or processing
4. customer names the order
5. customer says yes
6. cancel call returns cancelled
7. refund call returns the refund pending or issued

## SC-03 Customer switches orders in reply to the proposal
Kind: model path
Rules: R-04
World:
1. The order is placed or processing, and a second open order exists
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer names the other open order instead
5. customer says yes
6. cancel call returns cancelled
7. refund call returns the refund pending or issued

## SC-04 Customer withdraws after the proposal
Kind: model path
Rules: R-04
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer withdraws

## SC-05 Shipped or delivered order
Kind: model path
Rules: R-01
World:
1. The order has shipped or been delivered
2. customer asks to cancel the order by its number
3. lookup shows the order shipped

## SC-06 Order already cancelled
Kind: model path
Rules: R-01
World:
1. The order is already cancelled, refund pending or issued
2. customer asks to cancel the order by its number
3. lookup shows the order cancelled, refund pending or issued

## SC-06b Order already cancelled, its refund failed
Kind: model path
Rules: R-01, R-07
World:
1. The order is already cancelled, its refund failed
2. customer asks to cancel the order by its number
3. lookup shows the order cancelled, refund failed

## SC-07 Order number not on the account
Kind: model path
Rules: R-02
World:
1. The order is placed or processing
2. customer gives an order number not on the account
3. lookup shows the order placed or processing

## SC-08 Customer asks to cancel only some items
Kind: model path
Rules: R-03
World:
1. The order is placed or processing
2. customer asks to cancel only some items
3. lookup shows the order placed or processing
4. customer keeps the order

## SC-09 Customer asks for the refund elsewhere
Kind: model path
Rules: R-03
World:
1. The order is placed or processing
2. customer asks for the refund to go to another payment method
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call returns the refund pending or issued

## SC-10 Orders cannot be looked up
Kind: model path
Rules: R-01
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup gets no answer

## SC-11 Order ships before the cancellation lands
Kind: model path
Rules: R-05
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. order ships
6. cancel call rejected: the order has shipped

## SC-11b Order ships, cancellation unanswered
Kind: model path
Rules: R-05
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. order ships
6. cancel call times out (nothing changed)
7. lookup shows the order shipped

## SC-12 Cancellation unanswered, but the order was cancelled
Kind: model path
Rules: R-05, R-06
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call times out (it did cancel)
6. lookup shows the order cancelled
7. refund call returns the refund pending or issued

## SC-13 Cancellation unanswered and nothing happened
Kind: model path
Rules: R-06
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call times out (nothing changed)
6. lookup shows the order placed or processing
7. cancel call returns cancelled
8. refund call returns the refund pending or issued

## SC-14 Cancellation and the lookup both unanswered
Kind: model path
Rules: R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call times out (nothing changed)
6. lookup gets no answer
7. follow-up task created

## SC-15 Second cancellation also unanswered
Kind: model path
Rules: R-06, R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call times out (nothing changed)
6. lookup shows the order placed or processing
7. cancel call times out (nothing changed)
8. follow-up task created

## SC-16 Refund retried after the payment provider was unavailable
Kind: model path
Rules: R-06
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call: payment provider temporarily unavailable
7. refund call returns the refund pending or issued

## SC-16b Refund unanswered once, it went through
Kind: model path
Rules: R-06
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call times out (refund created, pending or issued)
7. refund call returns the refund pending or issued

## SC-16c Refund unanswered once, nothing created
Kind: model path
Rules: R-06
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call times out (nothing created)
7. refund call returns the refund pending or issued

## SC-17 Refund fails
Kind: model path
Rules: R-06, R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call returns the refund failed
7. follow-up task created

## SC-17b Refund refused: order not cancelled
Kind: model path
Rules: R-06, R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call: the order is not cancelled
7. follow-up task created

## SC-18 Payment provider unavailable twice
Kind: model path
Rules: R-06, R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call: payment provider temporarily unavailable
7. refund call: payment provider temporarily unavailable
8. follow-up task created

## SC-19 Refund unanswered twice, lookup shows it went through
Kind: model path
Rules: R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call times out
7. refund call times out
8. lookup shows the order's refund pending or issued

## SC-20 Refund unanswered twice, lookup shows it failed
Kind: model path
Rules: R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call times out
7. refund call times out
8. lookup shows the order's refund failed
9. follow-up task created

## SC-20b Refund unanswered twice, lookup shows no refund
Kind: model path
Rules: R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call times out
7. refund call times out
8. lookup shows no refund for the order
9. follow-up task created

## SC-21 Refund unanswered twice, lookup unanswered
Kind: model path
Rules: R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call times out
7. refund call times out
8. lookup gets no answer
9. follow-up task created

## SC-22 Hand-off unanswered once, retried
Kind: model path
Rules: R-06, R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call returns the refund failed
7. follow-up call times out (no task)
8. follow-up task created

## SC-23 Hand-off unanswered twice
Kind: model path
Rules: R-06, R-07
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call returns cancelled
6. refund call returns the refund failed
7. follow-up call times out (no task)
8. follow-up call times out (no task)

## SC-24 Cancellation reports the order not found
Kind: model path
Rules: R-05
World:
1. The order is placed or processing
2. customer asks to cancel the order by its number
3. lookup shows the order placed or processing
4. customer says yes
5. cancel call reports the order not found

## SC-25 Order number typed in lower case
Kind: conversational
Rules: R-02
Why not a path: the model has no order numbers.
The customer writes "cancel my order hg-10530" for order HG-10530, which is placed. The agent
proposes HG-10530 and, after "yes", cancels and refunds it.

## SC-26 What counts as a confirmation
Kind: conversational
Rules: R-04
Why not a path: the model has one "customer says yes" step and no customer words.
After the proposal the customer asks "will the refund go to my Visa?". The agent answers and
makes no cancel call until the customer says yes to the full proposal.
