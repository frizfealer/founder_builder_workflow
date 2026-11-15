# Harbor Goods order-support agent

The agent lets a signed-in Harbor Goods customer cancel an order that has not shipped and get their money back, in conversation, without knowing the store's cancellation and refund rules. It may cancel the order the customer said yes to, ask the order system for the refund of that order's total, and create a follow-up task for store staff when it cannot finish. It changes no other order.

Read in this order:

1. [Claims](claims.md): what the spec relies on about the order system, the payment provider, the staff task queue and about Harbor Goods.
2. [Rules](rules.md): the rules, what the agent does in each situation, and the decisions behind them.
3. [Policy](policy.md): the chart, and each rule break as its shortest path.
