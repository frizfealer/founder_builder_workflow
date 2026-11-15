# Report: Harbor Goods order-support agent (cancel an order and refund it)

## What was written

- Folder: `eval/agent-spec/run-switch-base-12/product/agent-spec/`. Start at [index.md](../../run-switch-base-12/product/agent-spec/index.md) (copied to `results/switch-base-12/spec-final/`).
- Scenarios: 47 in all. 42 are model paths and 5 are conversational: SC-41 (two orders in one message), SC-42 (a question at the proposal is not a yes), SC-43 (the customer asks when the money arrives), SC-44 (the customer asks for store credit instead), SC-45 (a second order named partway through).
- Interview log: `run-switch-base-12/product/interview-log.json`, 18 questions.

## Checker, final output

```
0 errors
States: 9351  steps: 11163  self-test: pass
Breaks: 0
Listed on policy.md: 0; not listed: 0
Scenarios: 47 (42 model path); one-path share 1.0
Chart: 13 states, 20 arrows
Steps no scenario takes: 0
```

## Breaks on policy.md

None. The one break the first check found had no next step for the agent: the follow-up task call got no answer. It went to the owner in the decision turn (question 11). The owner's confirmed tool set settles it: "On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support." (D-04).

## Claims put to the owner

9 claims were put to the owner (the limit is 10): C-06, C-07, C-11, C-23, C-36, C-38, C-47, C-48, C-49.

- Answered from the owner's record: C-23 (retry the follow-up task call once), C-36 (promise nothing about when the money arrives), C-38 (re-read after a second unanswered cancel call), C-49 (the refund call can answer that the order is not cancelled).
- Recommendation accepted: C-11 (order not found), C-48 (a differing amount goes to staff as "refund status unknown"), C-47 (a change after the yes, accepted in its narrowed form in step 4.5).
- Recommendation rejected, and nothing replaced it: C-07 (the first list call fails). C-06 (the list call's outcomes) was rejected for the same reason. The owner answered "Reads may be retried on timeout without limit; only commit calls are bounded." Both are now *spec only*. See the open questions.

No claim is left with kind `missing`. Three claims are *spec only*, written by the spec without an owner's answer: C-06 (a list call can also fail with an error), C-07 (what the agent says when the first list call fails), and C-51 (no third cancel call when a re-read after the second cancel call still shows the order open).

## Input ledger, final state

| # | Input | Status | Source |
|---|---|---|---|
| 1 | The capability | found | product-idea.md: cancel an order the customer placed and get the money back |
| 2 | Systems and tools | found (proposed in the interview, confirmed by the owner with four changes) | order system (Harbor Goods, no docs); payment provider (an outside service like Stripe, docs.stripe.com, reached only through the order system); staff task queue (Harbor Goods, no docs). Four calls: list the customer's orders, cancel an order, issue the refund, create a follow-up task. |
| 3 | Data | found | order fields and statuses; refund fields; refund status pending, issued or failed |
| 4 | Authorization | found | the customer is signed in and sees only their own orders; a yes to the full proposal covers both calls; any change voids it |
| 5 | Domain rules | found | from the owner's record |
| 6 | Known failure cases | found | three known failure cases, no transcripts |

The owner accepted these defaults:

- D-01 (a differing refund amount goes to staff);
- D-02 (one order at a time);
- D-03 (what the agent says when it hands a case to staff);
- D-07 (order not found);
- D-08 (the order is not cancelled at the refund);
- D-09 (the reason "refund status unknown" for a differing amount);
- D-10 (the narrowed rule for a change after the yes).

The tools are provisional. Architecture notes may change them.

## Findings (one verification round)

9 findings: 5 Important, 4 Nit. The finder's own count line said "8 findings: 5 Important, 3 Nit", but its report lists F1 to F9.

| finding | class | severity kept | status |
|---|---|---|---|
| F1: the first list call failing with an error has no owner answer (C-06, C-07, R-01) | Lies | Important | open: only the owner can say what the agent does when the first list call fails with an error. The error outcome itself is supported by the owner's "re-read fails" answers. |
| F2: unlimited read retries, and nothing said to the customer while they repeat | Gap | Nit | answered and open: the owner chose no limit (D-06, C-50). What the customer is told while reads repeat is open. |
| F3: the agent asking for a yes again after a change had no owner support (C-47, R-04) | Lies | Important | fixed: the owner accepted the narrowed R-04 text (D-10) |
| F4: R-13 (one order at a time) had no row in "What the agent does" | Gap | Nit | fixed: row added |
| F5: the agent's words left out the returned amount, and merged "status unknown" into "not confirmed yet" | Lies | Important | fixed: both messages corrected |
| F6: "what is known so far" in R-12 | Lies | Nit | dropped |
| F7: the some-items row added a question | Lies | Nit | fixed: row and model step |
| F8: a delivered order at the cancel call | Gap | Nit | dropped |
| F9: the refund's payment method could differ from the confirmed one | Gap | Nit | dropped |

Drop rate:

- Important: 0 of 5 dropped.
- Nit: 3 of 4 dropped.

The refutations quoted for each dropped finding:

- F6: C-43 "Final message must match the final refund status." and the owner's "Re-read fails, say outcome unknown, issue no refund, hand off".
- F8: C-26 "For a shipped or delivered order the agent says it cannot cancel and changes nothing."
- F9: C-17, from docs.stripe.com/refunds: "Refunds can only be sent back to the original payment method used in a charge."

One rule change went to the owner, and the owner accepted it: R-04, log question 18. No rule change is left as a proposal.

## Open questions

- What if the first call to list the customer's orders fails with an error rather than getting no answer? The spec has the agent say it cannot see the orders right now and change nothing (C-07, spec only). The owner has not said this.
- What if the call to list the orders, or a re-read, keeps getting no answer? The owner set no limit (D-06), so the agent keeps sending it. Nothing says what the customer hears meanwhile, or what happens if they leave.
- What if a re-read after the second cancel call still shows the order placed or processing? The spec sends no third cancel call and hands the case to staff as "cancellation unknown" (C-51, spec only).
- What if the customer changes the proposal after the yes? The yes is void and no call goes out until a new yes (owner-accepted R-04). The agent then offers the proposal again (model step). Whether it should offer again or end the conversation is not in the owner's answers.

## What verification cannot catch

The lint, the checker and the reviewers test whether the spec matches the owner's answers. They cannot test two things:

- whether these are Harbor Goods' real rules;
- whether the claims about the systems without docs are true: the order system and the staff task queue. That covers the call outcomes, retries that do the work once, and the race between processing and shipped.

Only the owner can confirm those.
