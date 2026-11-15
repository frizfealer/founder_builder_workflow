# Harbor Goods order-cancellation agent

The agent lets a signed-in Harbor Goods customer cancel an order they placed and get their money back in conversation, without knowing the store's cancellation and refund rules. It may cancel one of the customer's orders that has not shipped, ask the order system to refund that order in full to the payment method used, and leave a follow-up task for store staff. It changes no other order and handles no returns.

Read in this order:

1. [Claims](claims.md): what the spec relies on about the order system, the payment provider and the staff task queue, and about Harbor Goods.
2. [Rules](rules.md): the rules, what the agent does in each situation, and the decisions behind them.
3. [Policy](policy.md): the chart, and each rule break as its shortest path.
