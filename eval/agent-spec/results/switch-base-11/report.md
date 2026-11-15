# Agent spec report: Harbor Goods order-support agent

## Folder

- Written: `eval/agent-spec/run-switch-base-11/product/agent-spec/`. Start at [index.md](../../run-switch-base-11/product/agent-spec/index.md).
- Scenarios: 53. 46 are model paths and 7 are conversational (SC-45 to SC-51).
- Model: `eval/agent-spec/run-switch-base-11/product/agent-spec/model.py`. One run is one signed-in customer and one order.
- Interview log: `eval/agent-spec/run-switch-base-11/product/interview-log.json` (17 questions).

## Checker, final output

```
0 errors
States: 5976  steps: 7338  self-test: pass
Breaks: 0
Listed on policy.md: 0; not listed: 0
Scenarios: 53 (46 model path); one-path share 1.0
Chart: 13 states, 20 arrows
Steps no scenario takes: 0
```

## Breaks on policy.md

None. The first check found one break, a state with no step: the second cancel call also gets no answer, and the order still shows placed or processing. The owner settled it in step 3.4 (Q14, accepting the recommendation): the agent sends no third cancel call, tells the customer the order could not be cancelled right now and that no refund was issued, and hands the case to staff with the reason "cancellation unknown" (D-07).

## Claims put to the owner under the decision filter

1 claim: C-12, "A cancel call that times out may have cancelled the order." The owner accepted it (Q15).

No claim is left `missing`.

## Input ledger, final

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capability | found | product idea; Q2, Q4, Q5 |
| 2 | Systems and tools | found | Q1 (order system, payment provider behind it, staff task queue); Q16 (four tools confirmed) |
| 3 | Data | found | Q3 |
| 4 | Authorization | found | Q3, Q4 |
| 5 | Domain rules | found | Q2, Q5 |
| 6 | Known failure cases | found | Q10: no transcripts, three known cases plus the race where an order ships between the read and the cancel |

Defaults the owner accepted (the record said nothing, so the recommendation stood):
- Q7 / D-01: what the agent does when a refund's amount or payment method is different.
- Q9 / D-02: one order at a time, each with its own yes.
- Q11 / D-03: "order not cancelled" from the refund call.
- Q12 / D-04: "order not found" from the cancel call.
- Q13 / D-05: the success message.
- Q14 / D-07: a second cancel call that also gets no answer.
- Q15: C-12.
- Q16 / D-08: the tool set, and the handoff reason "refund status unknown" for a refund that is different.

The tools came from the owner's record and were confirmed in Q16. They are still provisional, and architecture notes may change them.

## Findings

6 findings: 3 Important, 3 Nit (one verification round).

| id | class | severity | status | note |
|---|---|---|---|---|
| F1 | Lies | Important | fixed | Two customer messages said more than the tool's answer. When the refund call answers "order not cancelled", the message now says only "the refund was not issued". When the cancel call answers "not found", the message is now "it could not find that order; no refund was issued". |
| F2 | Unclear | Important | dropped | Refutation: "agent must disambiguate and get a confirmation naming the order number before the cancel call." R-04 says the same thing. |
| F3 | Gap | Important | fixed | Added rows to "What the agent does" for: a yes that comes with a change; another order named while a proposal waits; several orders in one message; another order after one is settled. Added a model step for a yes with a change. |
| F4 | Lies | Nit | dropped | Refutation: Q16 "answers the orders, times out, or fails" and Q10 "Derive any further cases yourself." |
| F5 | Lies | Nit | fixed (C-49, C-51); answered (C-47) | C-49 and C-51 are trimmed to their Stripe sentences. C-47 stays "spec only", because the agent handles the case the same way whichever answer holds. |
| F6 | Unclear | Nit | dropped | Refutation (Style only): R-02's next sentence says what the case is: "For an order number that matches none of the customer's orders". |

Drop rate (findings dropped over findings verified):
- Important: 1 of 3.
- Nit: 2 of 3.

No fix changed a rule's text, so no rule change went to the owner.

## Open questions

- **What if the order system stays silent?** Reads are retried on timeout with no limit. This is the owner's choice (D-06): "Reads may be retried on timeout without limit; only commit calls are bounded." Nothing ends a run of read timeouts, before or after the cancel.
- **What if the second refund call gives a clear answer?** The agent still re-reads the refund, because the record says "after the retry the agent re-reads the refund record". If that re-read then fails, the agent says the status is not known, even though the second call answered.
- **What if the first refund call answers a transient error and the second one times out?** The record covers neither case on its own. The spec sends it to the refund re-read.
- **What if the customer's card is expired or cancelled?** The owner counts this as a terminal refund error. Stripe's docs say such refunds "in most cases" reach the replacement card (C-51). Only the owner can say whether the order system's refund call really answers "failed" here.
- **What if a refund fails after the conversation ends?** Stripe's docs say this can happen (C-49). The agent reports "pending" and nothing in the spec follows the refund up.
- **What does the agent say when a handoff succeeds?** The owner's record gives a message for each case ("outcome unknown", "refund is not confirmed yet", "status unknown"). It gives none for the handoff itself. The spec says only what is known.
- **What does the agent say when a yes comes with a change?** The rows added for F3 (whole order only, refund to the order's payment method, take the other order instead) follow from the owner's rules. They are not in the owner's words.

## What verification cannot catch

The checker and the reviewers can confirm only that the spec says what the interview record says. Two things only the owner can confirm:
- Whether these rules are Harbor Goods' real rules.
- Whether the claims about the order system and the staff task queue are true. Neither system has docs (C-09, C-12, C-16, C-19, C-21, C-43, C-44, C-47).
