# Input ledger, step 1

Inputs read: `product/product-idea.md` (the only document passed).

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | partial | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." Trigger: the customer asks, in conversation, to cancel an order. Missing: which orders can be cancelled (by status, by age), and what "get their money back" covers (full or partial refund, to which payment method). Checklist: passes go-home-happy (order cancelled, refund issued) and one trigger, two exits (cancelled and refunded / not cancelled); one sitting holds if the refund is issued in the conversation, even when the money lands later. |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | No system or tool is named. Step 3.4 proposes the tool set; the systems question asks which systems exist, who owns them and where their docs are. |
| 3 | Data: the records and fields the rules depend on | yes | missing | Nothing supplied about the order record (status, items, amount paid, payment method, owner of the order) or how the agent identifies the customer's order. |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing supplied: how the agent knows the customer placed the order, and what counts as the customer's go-ahead to cancel and refund. |
| 5 | Domain rules | no | partial | product-idea.md names "the store's cancellation and refund rules" and "the right form for their situation" but does not state them. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |
