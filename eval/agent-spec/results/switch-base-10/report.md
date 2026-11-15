# Report: Harbor Goods order-support agent spec

## The folder

- Written: `eval/agent-spec/run-switch-base-10/product/agent-spec/` (copy in `results/switch-base-10/spec-final/`).
- Start here: [index.md](../../run-switch-base-10/product/agent-spec/index.md). Then claims.md, rules.md, policy.md.
- Scenarios: 45 in all. 39 are model paths and 6 are conversational: two orders in one message, a second order after the first, the order list call that keeps timing out, a counter-offer (store credit, part of the refund, another card), when the money arrives, and a return of a shipped order.
- Model: `model.py` (one signed-in customer, one order, one conversation). 12 rules, 59 claims, 10 decisions.

## Checker, final output

```
0 errors
States: 6623  steps: 7800  self-test: pass
Breaks: 0
Listed on policy.md: 0; not listed: 0
Scenarios: 45 (39 model path); one-path share 1.0
Chart: 14 states, 21 arrows
Steps no scenario takes: 0
```

## Breaks on policy.md

None. The one break the checker found during writing was a `no-step` after the order list call fails before anything is proposed. It was closed in step 4.5, when the owner accepted the R-01 change (decision D-10).

## Claims put to the owner under the decision filter

2 claims, both accepted (decision D-03):

- C-18: a cancel call with no answer may or may not have cancelled the order.
- C-44: the order list shows a refund as soon as the refund call made it.

Left `missing`, source nobody:

- C-45: what ends the order list call being sent again when it keeps timing out. The owner said "Reads may be retried on timeout without limit" and turned down a bound of 3 tries (question 13).

Still spec only:

- C-41: the staff follow-up call answers created or gets no answer.

## Input ledger, final state

| # | Input | Status | Source |
|---|---|---|---|
| 1 | The capability | found | product-idea.md; questions 2 and 3 |
| 2 | Systems and tools | proposed, confirmed with changes | questions 1 and 9: the order system (list orders, cancel order, issue refund), the payment provider (called by the order system; Stripe docs read), the staff task queue (staff follow-up) |
| 3 | Data | found | question 5 |
| 4 | Authorization | found | questions 3 and 7 |
| 5 | Domain rules | found | questions 2, 3 and 6 |
| 6 | Known failure cases | found | question 6: no transcripts; three failure cases and the shipped-in-between race |

Defaults the owner accepted from a recommendation:

- D-01: when the refund amount differs from the confirmed one, the agent makes no further change, tells the customer the amount, and hands the case to staff.
- D-02: each order gets its own proposal and its own yes.
- D-03: C-18 and C-44.
- D-04: two unanswered cancel calls with the order still open go to staff as cancellation unknown.
- D-05: an amount that differs goes to staff as refund status unknown.
- D-06: the refund call answering "order not cancelled" goes to staff as refund not issued.
- D-08 to D-10: the R-10, R-12 and R-01 changes from step 4.5.

The tool set (list orders, cancel order, issue refund, staff follow-up) was proposed by this spec. It is provisional, and architecture notes may change it.

## Findings

7 findings: 4 Important, 3 Nit. Kept 5 (2 Important, 3 Nit). Dropped 2 (both reported as Important).

| id | class, severity | status |
|---|---|---|
| F1 | Gap, Important: reads sent again with no end, and no row for a list call that fails before a proposal | Partly fixed. The owner accepted the R-01 change (D-10), so a list call that fails before a proposal now has a rule. Open: nothing ends a read that keeps timing out. The owner turned down a bound in question 13. C-45 stays missing. |
| F2 | Lies, Important: R-07 allowed the refund only after the cancel call itself answered cancelled | Fixed. R-07 now also allows the refund after the order read again shows it cancelled (D-07, the owner's recorded answer). |
| F3 | Gap, Important: the conversation stops after one order | Dropped. The verifier: "D-02 settles both cases: 'Each order is handled on its own, with its own proposal and its own yes; nothing else bounds how many orders one conversation cancels'", plus SC-39 "starts again from reading the orders, with its own proposal and yes" and SC-38. |
| F4 | Unclear, Important (verifier: Nit): the re-read row's "has answered" | Dropped. The verifier: R-10 "When a refund call got no answer, the agent sends it once more and then reads the refund again", and C-55 "After a refund call with no answer and its second call, the agent reads the refund again". |
| F5 | Unclear, Nit: "passing error" and "lasting error" are not defined where they first appear | Fixed. C-30 now defines both where they first appear. |
| F6 | Lies, Nit: C-26 and C-04 said more than their quotes | Fixed. C-26 no longer says "after it is issued". C-04 now says only "can time out". The read failure got its own claim, C-58, with the owner's passage as its quote. |
| F7 | Lies, Nit: rows said more than the rules they cite | Fixed. R-12 now covers "order not found" (D-09). R-10 now says what the customer hears once the staff task is created (D-08). The row "two orders" now reads "more than one order". |

Drop rate (dropped over verified):

- Important: 2 of 4 (50%).
- Nit: 0 of 3 (0%).

## Open questions

- What if the order list call keeps timing out? The owner set no end to resending reads. The customer could wait indefinitely before anything is proposed. After a cancel or refund call with no answer, the re-read only ends when it answers or fails.
- What if a refund the agent reported as issued or pending later fails at the customer's bank? Stripe says "A refund can fail if the customer's bank or card issuer can't process it." Nothing says who tells the customer once the conversation is over.
- What if the customer has three or more open orders? The rules say "more than one". The model holds two.
- The record has two answers about a staff follow-up that times out: "handoff timeout not retried" and the later "On timeout, retry once". The spec follows the later answer (C-39, C-48).

## What verification cannot catch

Verification cannot say whether these are Harbor Goods' real cancellation and refund rules. It also cannot say whether the claims about the undocumented systems are true: the order system and the staff task queue have no docs, and C-18, C-44 and C-41 rest on the owner's word or on this spec. Only the owner can confirm these.
