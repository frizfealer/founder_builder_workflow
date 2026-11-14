# Owner brief: the systems behind the Harbor Goods agent

Frozen fixture for the build2 kind (HARNESS-PLAN.md step 7, owner ruling 1, 2026-11-14). It
holds the facts the recorded interview does not: which systems the agent calls, who owns each,
and where their docs are. The owner stand-in answers from this file and from the recorded
interview in `review-packet.md`.

| System | What it does for the agent | Owner | Docs |
|---|---|---|---|
| Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
| Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs. |
| Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |
