# Seeded fixture: where each defect sits

`seeded/` is `round0-agent-spec.md` and `review-packet.md` rewritten by hand in the format of
`FORMAT.md`, with round0's defects kept. `seeded-clean/` is the same spec with every
program-check defect fixed. Both test the frozen grader in `grader/`; no skill trial runs on
them. `grader/tests/` asserts every row below.

Regenerate the policy pages after changing a model:
`python3 grader/check.py seeded --write` and `python3 grader/check.py seeded-clean --write`.

## The 13 program-check defects (HARNESS-PLAN.md section 4)

| Defect | Where it sits in `seeded/` | What reports it | Fixed in `seeded-clean/` by |
|---|---|---|---|
| M2 | `scenarios.md:231` SC-17b has the refund refused as "order not cancelled" right after the cancel returned cancelled. `claims.md:33` C-17 lets that answer come only for an order that is not cancelled. | replay: SC-17b, no path | dropping SC-17b |
| M7 | `rules.md:94` has a row for a change made in the confirming turn; `model.py:227` gives the customer that step; no scenario takes it. | uncovered step: "customer says yes but names the other open order" | SC-27 |
| M8 | `model.py:307` proposes the only open order after an unnamed request; SC-02 (`scenarios.md:17`) has two open orders only. | uncovered step: "agent proposes the only open order" | SC-28 |
| M10 | `model.py:402` counts an order seen cancelled before any proposal as cancelled for R-07 (`rules.md:41`); the agent row for an already-cancelled order makes no hand-off. | checker: R-07 break, 5 steps | D-05: R-07 covers only an order this conversation cancelled |
| M11 | `model.py:336`: after the first cancel goes unanswered, a lookup that answers without the order has no row. `claims.md:47` C-31 says nobody rules this case out. | checker: no-step break, 10 steps | a branch in the row for the first unanswered cancel |
| P1 | `scenarios.md:337` SC-24 has the cancel report the order not found for an order the lookup just showed. `claims.md:27` C-11 allows "not found" only for a number not on the account. | replay: SC-24, no path | dropping SC-24 |
| P2 | `scenarios.md:256`, `:269`, `:297`: SC-19, SC-20 and SC-21 write "refund call times out" twice without saying which call created the refund. | replay: ambiguous (2, 2 and 5 paths) | naming the hidden part in each world line |
| P6 | the customer step "asks to cancel the whole order" (`model.py:219`) after the whole-order-only message; SC-08 (`scenarios.md:82`) only keeps the order. | uncovered step | SC-29 |
| P11 | `rules.md:94` says to propose the changed proposal; `model.py:303` then proposes a refund to the other payment method, against R-03. | checker: R-03 break, 7 steps | a row giving the refund terms and proposing only the original method |
| P12 | `rules.md:47` R-08 (tell the refund id) has an empty `Rests on:` line (`rules.md:51`). | lint: "R-08 rests on nothing" | C-45, sourced "spec only" |
| P18 | `model.py:84`: a request for a different refund amount; SC-09 (`scenarios.md:91`) covers another payment method only. | uncovered step: "customer asks for a different refund amount" | SC-30 |
| P29 | `claims.md:19` C-03 quotes "Cancellable while placed or processing" and no row quotes the owner's "no time limit". | lint, uncited answer: U-07 | C-44 |
| F5 | `scenarios.md:66` SC-06b, an already-cancelled order with a failed refund, cites R-07, which breaks on its own path. Seeded here: round0 has no such scenario; F5 came from a trial's fix. | replay: SC-06b, cited rule R-07 breaks on its path | D-05, as for M10 |

The plan's two items that need proposal terms in the model, P11 and P18, are both expressible:
the model tracks the refund destination of the current proposal and the kind of request.

## Draft-key defects present in the text

These are for the key_recall judge (step 6). No program reports them.

| Defect | Where |
|---|---|
| M1 | `rules.md:99`: after the second unanswered cancel, the agent hands off without re-reading the order. |
| M3 | `rules.md:101-103`: "the refund has not been issued" where the owner said "not confirmed yet". |
| P7 | No claim or row says what happens when the customer names a second order. |
| P10 | `claims.md:42` C-26: lookups are not limited and "what ends it" is blank; `rules.md:87` acts on the first unanswered lookup. Also lowers guard_none_limits to 0.75. |
| P21 | `rules.md:101`: a failed refund after a timed-out first refund call hands off without the re-read. |
| P25 | No claim says how the order system reads an order number typed in another case; SC-25 is conversational. |
| P26 | `rules.md:95` covers withdrawing only before confirming. |
| F8 | `rules.md:79` R-13 bans only a date, not every promise about when the money arrives. |

F2 is not present: the seeded model has no late cancellations.

## Other measured values on `seeded/`

guard_money is 0.0: C-06 and C-30 (`claims.md:22`, `:46`) say nothing about a value that differs
from what the customer confirmed. unsourced_claims is 2 (C-11, C-31). Steps no scenario takes:
22 in `seeded/`, 15 in `seeded-clean/`.
