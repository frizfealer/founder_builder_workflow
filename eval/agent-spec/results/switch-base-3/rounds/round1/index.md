# Harbor Goods order-cancellation agent

The agent lets a signed-in Harbor Goods customer cancel an order they placed and get their money back, in conversation, without knowing the store's cancellation and refund rules. It may look up the customer's orders, cancel a whole order that has not shipped, issue that order's refund to the payment method it was paid with, and hand a case to store staff when a cancel or refund does not go through. It changes no other order and handles no returns.

Read in this order:

1. [Claims](claims.md): what the spec relies on about the order system, the payment provider, the staff task queue and Harbor Goods.
2. [Rules](rules.md): the rules, what the agent does in each situation, and the decisions behind them.
3. [Policy](policy.md): the chart, and each rule break as its shortest path.
