# Input ledger (step 1)

Inputs read: `product/product-idea.md` (the only input).

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: "A customer should be able to use natural-language conversation to cancel an order they placed and get their money back." Trigger: the customer asks, in conversation, to cancel an order they placed. Exits: the order is cancelled and refunded, or it is not. |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed | The idea names no system and no tool. Step 3.4 proposes the tool set; the interview asks which systems the tools reach. |
| 3 | Data: the records and fields the rules depend on | yes | missing | Nothing says which order records, statuses, amounts or customer identity fields the cancellation and refund rules depend on. |
| 4 | Authorization: what counts as permission to act, what voids it | no | missing | Nothing says what counts as the customer's permission to cancel and refund, or how the agent knows the customer placed the order. |
| 5 | Domain rules | no | partial | The idea says the store has "cancellation and refund rules" and more than one form "for their situation", but gives none of them. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |

Row 1 against the user-goal tests of the use-case checklist:

- Go-home-happy: when the order is cancelled and the money is on its way back, the customer can stop satisfied. Pass.
- One sitting: one customer, one conversation, one order. Pass.
- One trigger, two exits: trigger is the customer asking to cancel an order (perceivable); exits are cancelled-and-refunded, or not cancelled. Pass.
