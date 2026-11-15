# Input ledger (step 1)

Inputs read: run-switch-smoke-1/product/product-idea.md (the only product document).

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | partial | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." Goal and trigger (customer asks to cancel) are stated; which orders can be cancelled, and what "get their money back" means (full, partial, to which method), are not. Passes go-home-happy and one-sitting tests if the refund is issued in the same conversation. |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | No systems or tools named. Step 3.4 proposes the tool set. |
| 3 | Data: the records and fields the rules depend on | yes | missing | Nothing on order records, statuses, payment, or how a customer is identified. |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing supplied. |
| 5 | Domain rules | no | missing | product-idea.md refers to "the store's cancellation and refund rules" but does not state them. |
| 6 | Known failure cases or transcripts | no | missing | Nothing supplied. |
