# Input ledger, step 1

Inputs read: `product/product-idea.md` (the only document passed).

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | partial | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." The trigger (the customer asks to cancel an order) is implied. Missing: which orders can be cancelled (which order states), and what "get their money back" means (full refund, to the original payment method, when). |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | No system, tool or doc is named. Missing: the order system, the payment / refund system, their owners and docs. Step 3.4 will propose the tool set. |
| 3 | Data: the records and fields the rules depend on | yes | missing | Nothing supplied: order id, order status (placed / shipped / delivered / already cancelled), amount paid, who placed the order, how the customer is identified. |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing supplied: how the agent knows the person is the one who placed the order, and what counts as the customer's yes to cancel and refund. |
| 5 | Domain rules | no | missing | product-idea.md says the store has "cancellation and refund rules" and "the right form for their situation", but gives none of them. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |

Row 1 against the user-goal tests of the use-case checklist:

- Go-home-happy: passes. When the order is cancelled and the refund is issued, the customer can stop satisfied.
- One sitting: passes. One customer, one conversation, one order.
- One trigger, two exits: the trigger is the customer asking to cancel an order (perceivable); exits are cancelled and refunded, or not cancelled with the reason. Partial until the order states that allow a cancel are known.
