# Input ledger, step 1 (build-base-3)

Sources read: eval/agent-spec/run-build-base-3/product/product-idea.md (the only product document). No code exists for this product.

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | Capabilities, each marked state-changing or read-only | yes | partial | product-idea.md names one goal: "cancel an order they placed and get their money back" (state-changing). Missing: which orders are cancellable, whole order or items, whether refund is part of the same capability. |
| 2 | Tools: name, parameters, return values, failure modes | yes | proposed | No tools defined in the inputs; step 3.8 proposes the tool set. Read-only vs state-changing: none supplied. |
| 3 | Data model: entities and fields | yes | missing | Orders and refunds are implied ("order they placed", "money back") but no entity has fields. |
| 4 | Authorization policy: what counts as permission to act, what invalidates it | no | missing | Nothing on identity/ownership or what counts as permission to cancel. |
| 5 | Domain rules | no | missing | "the store's cancellation and refund rules" are referenced but not stated. |
| 6 | Known failure cases or transcripts | no | missing | None supplied. |
