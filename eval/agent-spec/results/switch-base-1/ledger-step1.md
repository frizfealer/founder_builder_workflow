# Input ledger, step 1

Inputs read: `product/product-idea.md` (the only product document). No code paths were passed.

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | partial | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." The trigger (the customer asks, in conversation, to cancel an order) and the goal (the order cancelled and the money returned) are given. Missing: which orders can be cancelled, and what "get their money back" means (full or partial amount, to which payment method, when). |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | The idea names no system and no tool. Step 3.4 will propose the tool set. Missing: the order system, the payment or refund system, who owns each, and where their docs are. |
| 3 | Data: the records and fields the rules depend on | yes | missing | Nothing supplied. Needed: the order record (status, items, amount paid, whether it has shipped), how the customer is identified as the order's owner, and the refund record. |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing supplied: what shows the customer owns the order, and what counts as their yes to cancel and refund. |
| 5 | Domain rules | no | missing | The idea refers to "the store's cancellation and refund rules" and "the right form for their situation" but does not give them. |
| 6 | Known failure cases or transcripts | no | missing | Nothing supplied. |

## Row 1 against the use-case checklist

- Go-home-happy: passes. When the order is cancelled and the refund issued, the customer can stop satisfied.
- One sitting: passes for the agent's part. One customer, one conversation; the refund may take days to reach the customer's account, but the agent's work (cancel, issue the refund, tell the customer) ends in the conversation.
- One trigger, two exits: the trigger is perceivable ("the customer asks to cancel an order"). Success: the order is cancelled and the refund issued. Failure: the order is not cancelled (not eligible, not the customer's, a system failure), or the outcome is handed to staff.
- Open: whether "cancel" and "refund" are one goal or two (for example, an order that has shipped may need a return, which is a different capability). The interview asks.
