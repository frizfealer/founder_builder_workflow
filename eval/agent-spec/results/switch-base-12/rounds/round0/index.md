# Harbor Goods order-support agent: cancel an order and refund it

The agent lets a signed-in Harbor Goods customer cancel an order they placed, in conversation, and get their money back, without knowing the store's cancellation and refund rules. It may cancel one of the customer's own orders that is placed or processing, issue the refund for that order through the order system, and create a follow-up task for store staff when it cannot finish a case. It changes nothing else.

Read in this order:

1. [Claims](claims.md): what the spec relies on about the order system, the payment provider behind it, the staff task queue, and about Harbor Goods.
2. [Rules](rules.md): the rules, what the agent does in each situation, and the decisions behind them.
3. [Policy](policy.md): the chart, and each rule break as its shortest path.

[Scenarios](scenarios.md) and [model.py](model.py) are for programs and later stages.
