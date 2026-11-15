# Input ledger, step 1 (shown to the user)

Sources read: eval/agent-spec/run-build-base-2/product/product-idea.md (the only product document). No code exists for this product.

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | Capabilities, each marked state-changing or read-only | yes | partial | product-idea.md names one goal: a customer cancels an order they placed and gets their money back (state-changing). Missing: which orders are cancellable, whole order vs items, whether cancel and refund are one goal. |
| 2 | Tools: name, parameters, return values, failure modes | yes | proposed | The product document defines no tools; step 3.8 proposes the tool set. Read-only vs state-changing: none supplied yet. |
| 3 | Data model: entities and fields | yes | missing | No entities or fields supplied (order, refund implied by "cancel an order" and "get their money back"). |
| 4 | Authorization policy: what counts as permission to act, what invalidates it | no | missing | Nothing says how the customer is identified or what authorizes a cancellation. |
| 5 | Domain rules | no | missing | "the store's cancellation and refund rules" are referenced but not stated. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |
