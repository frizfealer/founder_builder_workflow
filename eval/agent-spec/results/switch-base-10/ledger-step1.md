# Input ledger (step 1)

Inputs read: `product/product-idea.md` (the only document passed).

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | partial | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." Trigger: the customer asks to cancel an order. Gap: which orders can be cancelled (by order state, e.g. shipped or not), and whether "get their money back" means a full refund issued in the same conversation. |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | No system or tool is named. The idea implies an order system (look up and cancel an order) and a payment or refund system (return the money). Owners and docs unknown. Step 3.4 proposes the tool set. |
| 3 | Data: the records and fields the rules depend on | yes | missing | No records or fields are given. Needed: how the agent knows who the customer is and which orders are theirs, the order's state, the amount paid. |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing supplied. |
| 5 | Domain rules | no | missing | The idea says the store has "cancellation and refund rules" and forms "for their situation", but states none of them. |
| 6 | Known failure cases or transcripts | no | missing | Nothing supplied. |

Row 1 against the user-goal tests:

- Go-home-happy: yes, if the order is cancelled and the refund is issued, the customer can stop.
- One sitting: cancelling and issuing a refund fits one conversation; the money reaching the customer's account later is outside the conversation.
- One trigger, two exits: trigger is the customer asking to cancel an order they placed (perceivable). Exits: order cancelled and refund issued; or order not cancelled, with the reason.
- Gap: which orders qualify, and the refund's amount and timing, are not stated.
