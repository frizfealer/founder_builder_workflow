# Input ledger, step 1

Inputs read: `eval/agent-spec/run-switch-base-2/product/product-idea.md` (the only product document).

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." Goal: the order is cancelled and the money is back. Trigger: the customer asks, in conversation, to cancel an order they placed. |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | The inputs name no system and no tool. Step 2 asks which systems the tools reach; step 3.4 proposes the tool set. |
| 3 | Data: the records and fields the rules depend on | yes | missing | Nothing supplied: no order record, no order status, no payment or refund record, no way to tell the customer placed the order. |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing supplied on what lets the agent cancel or refund, or what voids it. |
| 5 | Domain rules | no | missing | product-idea.md says the store has "cancellation and refund rules" and forms "for their situation", but gives none of them. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |

Use-case checklist, row 1: go-home-happy holds (the order is cancelled and the money is back); one sitting holds (one customer, one conversation); one trigger the agent can perceive (the customer asks to cancel an order); two exits (cancelled and refunded, or not cancelled and told why).
