# Input ledger, step 1

Inputs read: `eval/agent-spec/run-switch-base-6/product/product-idea.md` (the only product document).

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." Trigger: the customer asks, in conversation, to cancel an order. Passes the user-goal tests: go-home-happy (order cancelled, money back), one sitting, one trigger, two exits (cancelled and refunded / not cancelled). |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | The idea names no system and no tool, only "an online store". Systems go to the owner first in step 2; the tool set is proposed in step 3.4. |
| 3 | Data: the records and fields the rules depend on | yes | missing | Nothing says what an order record holds (status, items, amount paid, payment method, who placed it). |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing says how the agent knows the customer placed the order, or what counts as the customer's go-ahead to cancel. |
| 5 | Domain rules | no | partial | The idea refers to "the store's cancellation and refund rules" and "the right form for their situation" but does not state them: which orders can be cancelled, how much is refunded, and to where. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |
