# Policy

The chart is in [chart.mmd](chart.mmd). Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Breaks

### R-07: order cancelled with no refund shown, or cancellation unknown, and no hand-off made

1. The order is already cancelled, its refund failed
2. customer asks to cancel the order by its number
3. agent looks up the customer's orders
4. lookup shows the order cancelled, refund failed
5. agent tells the customer: the order is already cancelled

### R-03: proposed a refund to another payment method

1. The order is placed or processing
2. customer asks to cancel the order by its number
3. agent looks up the customer's orders
4. lookup shows the order placed or processing
5. agent proposes: cancel the whole order, refund the total to its payment method
6. customer asks for the refund to go to another payment method instead
7. agent proposes the changed proposal: refund to the other payment method

### no-step: the agent has no step here

1. The order is placed or processing
2. customer asks to cancel the order by its number
3. agent looks up the customer's orders
4. lookup shows the order placed or processing
5. agent proposes: cancel the whole order, refund the total to its payment method
6. customer says yes
7. agent sends the cancel
8. cancel call times out (it did cancel)
9. agent looks up the customer's orders
10. lookup answers without the order
