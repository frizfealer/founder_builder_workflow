# Harbor Goods order-support agent

The agent lets a signed-in Harbor Goods customer cancel an unshipped order and get the order's
total paid back to its payment method.

Read in this order:

1. [Claims](claims.md): what the spec relies on about the order system, the payment provider, the staff task queue and Harbor Goods.
2. [Rules](rules.md): the rules, what the agent does in each situation, and the decisions behind them.
3. [Policy](policy.md): the chart, and each rule break as its shortest path.
