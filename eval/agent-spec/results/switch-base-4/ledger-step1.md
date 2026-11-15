# Input ledger (step 1)

Inputs read: `run-switch-base-4/product/product-idea.md` (the only document passed). No code, no tool definitions, no docs.

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." Trigger: the customer asks, in conversation, to cancel an order they placed. Exits: the order is cancelled and refunded (success), or it is not (failure). Passes go-home-happy (order cancelled, money on its way) and one sitting (one conversation). |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | The idea names an online store and a refund but no system, owner, docs or tool. The systems are asked first in step 2; the tool set is proposed in step 3.4. |
| 3 | Data: the records and fields the rules depend on | yes | missing | Nothing says what an order record holds (status, items, amount paid, payment, who placed it). |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing says how the customer shows the order is theirs, or what counts as a yes to cancel. |
| 5 | Domain rules | no | partial | The idea says the store has "cancellation and refund rules" and "forms" for different situations, but does not give them. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |
