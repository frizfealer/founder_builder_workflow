# Input ledger after step 1 (build-base-1)

Source read: eval/agent-spec/run-build-base-1/product/product-idea.md (the only product document; no code exists).

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | Capabilities, each marked state-changing or read-only | yes | partial | product-idea.md names one goal: cancel an order the customer placed and get the money back (state-changing). Gap: which orders are cancellable, whole order or items, whether refund is part of the same capability. |
| 2 | Tools: name, parameters, return values, failure modes | yes | proposed | No tools are defined in the inputs; step 3.8 proposes the set. Read-only vs state-changing: none supplied. |
| 3 | Data model: entities and fields | yes | missing | "order" and "money back" (a refund) are named, with no fields, statuses or identifiers. |
| 4 | Authorization policy: what counts as permission to act, what invalidates it | no | missing | Nothing says how the agent knows the order is the customer's, or what counts as permission to cancel. |
| 5 | Domain rules | no | missing | product-idea.md says the store has "cancellation and refund rules" but does not state them. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |
