# Report: Harbor Goods order-support agent spec

## The folder

- Folder written: `eval/agent-spec/run-switch-smoke-1/product/agent-spec/`. Start at [index.md](../../run-switch-smoke-1/product/agent-spec/index.md).
- Scenarios: 44 in all. 41 are model paths and 3 are conversational (SC-39 two orders in one message, SC-40 another kind of change, SC-41 when the money arrives).

## Checker, final output

```
0 errors
States: 2231  steps: 2339  self-test: pass
Breaks: 0
Listed on policy.md: 0; not listed: 0
Scenarios: 44 (41 model path); one-path share 1.0
Chart: 12 states, 18 arrows
Steps no scenario takes: 0
```

## Breaks listed on policy.md

None. No rule breaks in any reachable state, so policy.md has no open decision listed.

## Claims put to the owner under the decision filter

3 claims: C-20, C-30, C-31 (question 12).
- C-20: the refund call is idempotent. Settled by the owner's words.
- C-30: an already-cancelled order is reported and nothing changes. Settled by the owner's words.
- C-31: when the list call fails with an error, the agent says it cannot look up the orders and changes nothing. The owner's reply did not address it, so it stays `spec only`.

No claim is left as kind `missing`.

## Input ledger, final state

| # | Input | Status | Source |
|---|---|---|---|
| 1 | The capability | found | product-idea.md; answers 2 to 5 |
| 2 | Systems and tools | found | answers 1, 6, 7, 9, 12 to 15; Stripe docs (refunds, idempotent requests) |
| 3 | Data | found | answer 6 |
| 4 | Authorization | found | answer 5 |
| 5 | Domain rules | found | answers 2, 3, 6, 12 |
| 6 | Known failure cases | found | answer 8: no transcripts, three failure cases named |

Defaults the owner accepted, each given by the stand-in as "Yes, I accept your recommendation":
- a refund whose amount differs from the confirmed total (C-21, D-06);
- no third cancel after a second cancel with no answer (C-15, D-07);
- a cancel that answers order not found (C-33, D-08);
- a refund that answers order not cancelled (C-34, D-09);
- the four rule changes from the review (D-11 to D-14).

The tools (list orders, cancel order, issue refund, create staff follow-up) were proposed and the owner confirmed them with four changes. They are provisional, and the architecture notes may change them.

## Findings

10 findings: 7 Important, 3 Nit. 10 kept, 0 dropped.

Drop rate: Important 0/7, Nit 0/3. Nothing was dropped, so there is no refutation to quote.

| # | Class, severity | Finding | Status |
|---|---|---|---|
| F1 | Lies, Important | When the follow-up call fails twice, the agent's message still said "staff will follow up". | fixed: that message now only tells the customer to contact support |
| F2 | Lies, Important | A pending refund was reported as issued. | fixed: R-09 change, accepted by the owner |
| F3 | Gap, Important | No row for a refund that answers pending; the amount was checked on only some paths. | fixed: R-11 change accepted; rows and model added |
| F4 | Gap, Important | No rule said which follow-up reason goes with which case; the amount mismatch fit no reason. | fixed: R-10 change accepted, with a fourth reason "refund amount differs" |
| F5 | Gap, Important | A lookup that keeps getting no answer has no end. | open: the owner set no bound (questions 11 and 13) |
| F6 | Gap, Important | "Just shipped" left out "delivered". | fixed: R-06 change accepted. The verifier refuted part (b), the returns message; nothing was changed for it. |
| F7 | Gap, Important | No rule for two orders in one message, or a second order after the first. | fixed: new R-13, one order at a time, accepted |
| F8 | Gap, Nit | R-02 covered exactly two open orders. | fixed: "two or more", accepted |
| F9 | Unclear, Nit | A row condition was a double negative. | fixed: reworded |
| F10 | Lies, Nit | C-02, C-16 and C-26 said more than their quotes. | fixed: quotes re-cited, and new C-37 for "order not cancelled". The verifier rated it Style only. It was kept because a claim that says more than its quote is a Lies defect, not a phrasing preference. |

## Open questions

- What if a lookup never answers? The owner said "Reads may be retried on timeout without limit". So if listing the orders, re-reading an order or re-reading a refund keeps timing out, nothing ends the conversation, the customer gets no message, and no staff task is created.
- What if listing the customer's orders fails with an error rather than a timeout? The spec has the agent say it cannot look up the orders and change nothing (C-31, `spec only`). The owner has not confirmed this.
- What if a refund that was reported pending fails later, after the conversation? The payment provider's docs say this can happen (C-25). The spec has no step for it, so staff must find it some other way.

## What verification cannot catch

Verification cannot show whether these rules are Harbor Goods' real rules. It also cannot show whether the claims about the order system and the staff task queue are true. Neither system has docs, and only the owner can confirm them.
