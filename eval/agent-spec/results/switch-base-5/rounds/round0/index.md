# Harbor Goods order-cancellation agent

The agent lets a signed-in Harbor Goods customer cancel an order they placed and get their money back, in conversation, without knowing the store's cancellation and refund rules or finding the right form. It may cancel a whole order that is placed or processing, issue the refund of the order's total paid to the payment method it was paid with, and create a follow-up task for store staff when it cannot settle the case. It changes nothing else.

Read in this order:

1. [Claims](claims.md): what the spec relies on about the order system, the payment provider and the staff task queue, and about Harbor Goods.
2. [Rules](rules.md): the rules, what the agent does in each situation, and the decisions behind them.
3. [Policy](policy.md): the chart, and each rule break as its shortest path.
