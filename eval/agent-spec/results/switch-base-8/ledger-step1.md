# Input ledger, step 1

Inputs read: `product/product-idea.md` (the only document passed).

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | partial | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." Trigger: the customer asks to cancel an order. Missing: which orders can be cancelled, how the agent knows the order is the customer's, and what "get their money back" covers (full or partial amount). |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | No system or tool is named. The store must hold orders and take payments; step 3.4 proposes the tool set. |
| 3 | Data: the records and fields the rules depend on | yes | missing | No order record, status, amount or payment fields are given. |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Not supplied. |
| 5 | Domain rules | no | missing | product-idea.md says the store has "cancellation and refund rules" and forms "for their situation", but does not state them. |
| 6 | Known failure cases or transcripts | no | missing | Not supplied. |

Row 1 against the user-goal tests: go-home-happy holds (the order is cancelled and the refund is issued); one sitting holds if issuing the refund, not its arrival in the customer's account, is the end; one trigger (the customer asks to cancel an order), two exits (cancelled and refunded, or not cancelled and told why).
