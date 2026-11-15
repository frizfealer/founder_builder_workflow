# Input ledger (step 1)

Inputs read: `eval/agent-spec/run-switch-base-3/product/product-idea.md` (the only product document).

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." Trigger: the customer asks, in conversation, to cancel an order. Passes the go-home-happy and one-sitting tests: once the order is cancelled and the refund issued, the customer can stop. |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | No system, owner, docs or tool is named. The systems are asked first in step 2; the tool set is proposed in step 3.4. |
| 3 | Data: the records and fields the rules depend on | yes | missing | Nothing says what an order record holds (status, shipped or not, amount paid, payment method) or how the agent finds the customer's order. |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing says how the agent knows the person owns the order, or what counts as the customer's go-ahead to cancel and refund. |
| 5 | Domain rules | no | missing | product-idea.md refers to "the store's cancellation and refund rules" and "the right form for their situation" but does not state them. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |
