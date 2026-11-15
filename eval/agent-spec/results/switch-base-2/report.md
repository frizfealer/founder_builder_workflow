# Report: Harbor Goods order-cancellation agent spec

## Folder

Written: `eval/agent-spec/run-switch-base-2/product/agent-spec/`. Start at [index.md](spec-final/index.md) (copy in `results/switch-base-2/spec-final/`).

Scenarios: 48 in all. 42 are model paths and 6 are conversational. Model: `agent-spec/model.py`.

## Checker, final output

```
0 errors
States: 8254  steps: 10063  self-test: pass
Breaks: 0
Listed on policy.md: 0; not listed: 0
Scenarios: 48 (42 model path); one-path share 1.0
Chart: 12 states, 16 arrows
Steps no scenario takes: 0
```

## Breaks on policy.md

None. The checker found six cases during the run, and the owner settled every one in the step-3.4 decision turns:
- listing the orders gets no answer
- a re-read shows the order still open
- the cancel call answers "order not found"
- the order is still open after a second cancel call
- a second refund call could have made a second refund
- the retry's different amount was hidden by a failed re-read

## Claims put to the owner under the decision filter

1 claim: C-24, whether a second refund call can create a second refund. The owner answered from the record: "issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund." No claim is left `missing`.

## Input ledger, final state

| # | Input | Status | Source |
|---|---|---|---|
| 1 | The capability | found | product-idea.md: a signed-in customer cancels an order they placed and gets their money back |
| 2 | Systems and tools | found (proposed, confirmed with four changes) | Q1 systems; Q10 tool set: list orders, cancel an order, issue the refund, ask staff to follow up |
| 3 | Data | found | Q2, Q3, Q4, Q10: order number, status (placed, processing, shipped, delivered, cancelled), total paid, payment method, refund and its status (pending, issued, failed) |
| 4 | Authorization | found | Q5: an explicit yes to the full proposal (which order, the refund amount and where it goes); any change voids it |
| 5 | Domain rules | found | Q2, Q4, Q8: only placed or processing orders, whole orders only, full total to the order's payment method, one refund, no fee, no store credit |
| 6 | Known failure cases | found | Q6: no transcripts; three failure cases (wrong order, refund error, refund timeout) and the ship-before-cancel race |

The owner accepted 10 of the 21 questions as recommended defaults:
- Q7: when to hand a case to staff
- Q9: a refund amount that differs from the confirmed one
- Q11: the listing fails
- Q15: the cancel call answers "order not found"
- Q16: the order is still open after a second cancel
- Q17: act at once on a different amount from the retry
- Q18 to Q20: the R-12, R-08 and R-02 rule changes from round 1
- Q21: the fifth hand-off reason, "order not cancelled"

The tools are proposed, and the owner confirmed them in Q10, but they are provisional. Architecture notes may change them.

## Findings

10 findings: 6 Important, 4 Nit. The verifier ruled 7 Real, 3 Not real and 0 Style only. 7 were kept and 3 dropped.

| id | class | severity (kept at) | status |
|---|---|---|---|
| F1 | Gap | Important | fixed: a row and a model step for the refund call answering "order not cancelled" |
| F2 | Gap | Important | fixed: each refund row now names which call it is about; the R-08 text change was accepted by the owner |
| F3 | Lies | Nit (finder said Important) | fixed: the R-12 text change was accepted by the owner |
| F4 | Gap | Important | fixed: the hand-off after a read showing no refund now sends "refund not issued"; the owner accepted a fifth reason, "order not cancelled" |
| F5 | Gap | Important | fixed: the R-02 text change (one order at a time, each with its own yes) was accepted, and a row was added |
| F6 | Gap | Important | dropped |
| F7 | Lies | Nit | open: a re-read that shows "delivered" has no row. Proposed change to R-07: "if it shows it shipped" becomes "if it shows it shipped or delivered". The one step-4.5 owner turn was full, so this goes to the owner as a proposal |
| F8 | Lies | Nit | fixed: C-27 now says only what its quote says. The C-15 part is answered: Q10 confirms the fields and that cancelled orders are listed |
| F9 | Gap | Nit | dropped |
| F10 | Unclear | Nit | dropped |

Drop rate: Important 1 of 6 verified (F6). Nit 2 of 4 verified (F9, F10).

Refutations quoted for the dropped findings:
- **F6:** D-09, "Reads that get no answer are tried again with no limit. | the owner | Reads may be retried on timeout without limit; only commit calls are bounded."
- **F9:** R-05, "It proposes a refund of the order total the customer paid, back to the order's payment method, with no fee and no store credit", together with R-03's "explicitly confirms the full proposal: which order, the refund amount and where it goes".
- **F10:** R-01, "When listing the orders gets no answer, it lists them again; when the listing fails, ...", and R-09, "The read fails: ... A read with no answer is read again."

## Open questions

- **A read that never answers.** What if a read never answers? The owner set no limit on reads (C-37, D-09). An order system that stays silent leaves the customer waiting, with nothing said and no hand-off.
- **A re-read that shows "delivered".** What if the re-read after an unanswered cancel call shows the order delivered? R-07 names only shipped (F7, proposal above).
- **A refund that fails later.** What if a refund the provider accepted fails days later (C-33)? The conversation is over by then, and nothing says who tells the customer.
- **"Order not cancelled" from the refund call.** What if the refund call answers "order not cancelled" after the cancel call answered "cancelled"? The spec hands the case to staff as "refund not issued". The two systems' answers disagree, and the inputs do not say which one is right.

## What verification cannot catch

Verification cannot tell whether these rules are Harbor Goods' real rules. It also cannot tell whether the claims about the two systems without docs are true; only the owner can confirm them. Those systems are the order system and the staff task queue. The claims include what each call can answer, that cancelling and refunding are idempotent, and that the follow-up call is idempotent.
