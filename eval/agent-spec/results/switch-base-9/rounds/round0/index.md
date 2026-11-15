# Harbor Goods order-support agent

The agent lets a signed-in Harbor Goods customer cancel an order in conversation and get their money
back, without knowing the store's cancellation and refund rules. It may cancel an order that has not
shipped once the customer says yes, ask the order system to refund the order's total paid, and ask
store staff to follow up when it cannot finish. It changes no other order.

Read in this order:

1. [Claims](claims.md): what the spec relies on about the order system, the payment provider and the staff task queue, and about Harbor Goods.
2. [Rules](rules.md): the rules, what the agent does in each situation, and the decisions behind them.
3. [Policy](policy.md): the chart, and each rule break as its shortest path.
