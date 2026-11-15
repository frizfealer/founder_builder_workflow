# Input ledger, step 1

Inputs read: `product/product-idea.md` (the only document passed).

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." Goal: the order is cancelled and the money is refunded. Trigger: the customer asks, in conversation, to cancel an order. |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | The idea names no system and no tool. Which systems hold orders and take refunds, who owns them and where their docs are is the first interview question; step 3.4 proposes the tool set. |
| 3 | Data: the records and fields the rules depend on | yes | missing | Nothing says what an order record holds (status, amount paid, payment, the customer it belongs to). |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing says how the agent knows the customer owns the order, or what counts as the customer's yes to cancel and refund. |
| 5 | Domain rules | no | missing | The idea refers to "the store's cancellation and refund rules" but does not state them (which orders can be cancelled, how much is refunded, by when). |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |

Row 1 against the use-case checklist: go-home-happy holds (the order is cancelled and the money is on its way back); one sitting holds (one customer, one conversation); the trigger is perceivable (the customer asks to cancel an order); the exits are success (cancelled and refunded) and failure (not cancelled, or refund not made, customer told).
