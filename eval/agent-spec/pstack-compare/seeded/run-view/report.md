# SeededPolicy

TLC reached 10,477 states, more than the chart budget of 500, so the chart draws only the bug paths: 6 states and 10 arrows.

## R07 breaks
The shortest path has 5 steps:
0. Start
1. The order is already cancelled, its refund failed: Start
2. customer asks to cancel the order by its number: Before the cancel call / Looking up orders
3. agent looks up the customer's orders: Before the cancel call / Looking up orders
4. lookup shows the order cancelled, refund failed: Before the cancel call / Looking up orders
5. agent tells the customer: the order is already cancelled: Conversation over / Nothing cancelled, customer told

## R03 breaks
The shortest path has 7 steps:
0. Start
1. The order is placed or processing: Start
2. customer asks to cancel the order by its number: Before the cancel call / Looking up orders
3. agent looks up the customer's orders: Before the cancel call / Looking up orders
4. lookup shows the order placed or processing: Before the cancel call / Looking up orders
5. agent proposes: cancel the whole order, refund the total to its payment method: Before the cancel call / Proposal waiting for yes
6. customer asks for the refund to go to another payment method instead: Before the cancel call / Proposal waiting for yes
7. agent proposes the changed proposal: refund to the other payment method: Before the cancel call / Proposal waiting for yes

## NoDeadlock breaks
The shortest path has 10 steps:
0. Start
1. The order is placed or processing: Start
2. customer asks to cancel the order by its number: Before the cancel call / Looking up orders
3. agent looks up the customer's orders: Before the cancel call / Looking up orders
4. lookup shows the order placed or processing: Before the cancel call / Looking up orders
5. agent proposes: cancel the whole order, refund the total to its payment method: Before the cancel call / Proposal waiting for yes
6. customer says yes: After the customer says yes / Cancelling
7. agent sends the cancel: After the customer says yes / Cancelling
8. cancel call times out (it did cancel): After the customer says yes / Cancel unanswered, checking
9. agent looks up the customer's orders: After the customer says yes / Cancel unanswered, checking
10. lookup answers without the order: After the customer says yes / Cancel unanswered, checking

## Rules that hold
R01, R02, R04, R05, R06
