Input ledger (step 1), from eval/agent-spec/run-standin-1/product/product-idea.md, the only input passed.

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | Capabilities, each marked state-changing or read-only | yes | partial | product-idea.md: "cancel an order they placed and get their money back" (state-changing). Gap: whether partial cancellation, order lookup or refund-status questions are in scope; which order states can be cancelled. |
| 2 | Tools: name, parameters, return values, failure modes | yes | proposed | No tools defined in the inputs; step 3.8 proposes the tool set. Read-only: none known. State-changing: none known. |
| 3 | Data model: entities and fields | yes | missing | No entities or fields given (order, line items, payment, refund, customer identity). |
| 4 | Authorization policy: what counts as permission to act, what invalidates it | no | missing | Nothing on how the customer is identified or what counts as permission to cancel and refund. |
| 5 | Domain rules | no | missing | product-idea.md says the store has "cancellation and refund rules" and "forms" per situation, but states none of them. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |
