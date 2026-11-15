# Input ledger, step 1

Inputs read: `product/product-idea.md` (the only product document). No code, no tool definitions, no docs.

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | partial | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." The trigger (the customer asks, in conversation, to cancel an order) is perceivable. Gap: what "get their money back" means by the end of the one conversation (refund issued, how much, to where). |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | No system, owner, docs or tool is named; the idea says only "an online store". The systems are asked first in step 2; step 3.4 proposes the tool set. |
| 3 | Data: the records and fields the rules depend on | yes | missing | Nothing names the order record or its fields (status, items, amount paid, payment, owner of the order). |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing says who may cancel an order or what counts as the customer's go-ahead. |
| 5 | Domain rules | no | partial | product-idea.md says the store has "cancellation and refund rules" and forms "for their situation", but states none of them. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |

Use-case checklist, row 1: go-home-happy holds (the order is cancelled and the money is on its way back); one sitting holds (one customer, one conversation about one order); the trigger is perceivable (the customer asks to cancel); the exits are success (cancelled and refunded, customer told) and failure (not cancelled, customer told why).
