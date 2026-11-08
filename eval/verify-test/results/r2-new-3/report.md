# Step 5 report: Harbor Goods order-support agent spec (trial r2-new-3, rounds 2 and 3)

## File written

- Live spec: `eval/verify-test/run-r2-new-3/agent-spec.md`. The final copy is `results/r2-new-3/agent-spec-final.md`. Nothing under `examples/` was touched.
- Capability **4.1 Cancel Order (CO), state-changing**: 29 scenarios (CO-S01 to CO-S29). This trial added no scenario. It changed CO-S11, CO-S20, CO-S24, CO-S25, CO-S26 and CO-S29. CO-S12 and CO-S19 changed in round 2 and were restored to their round-1 text in round 3.

## Merges (step 3.9) and dropped rows

- This trial ran no step 3.9 merge, because it starts after round 1. The checker still prints six merge-candidate WARNING groups that the round-1 spec already had: CO-S01/02/03/12/27/28, CO-S01/02/09/12/28, CO-S11/24/26, CO-S16/19, CO-S18/20, CO-S22/23. They are warnings, not errors.
- Dropped data-variant rows: CO-S11 and CO-S26 lost their status column, and their row 2 (HG-10511) now starts at processing instead of placed (M15). CO-S12 row 3 and CO-S19 row 3 were added in round 2 and removed in round 3 (N1, N2). They exercised "the first lookup after the unanswered call goes unanswered, and a repeat answers".
- Added: CO-S29 now has a third order, HG-09940 (cancelled, with refund RF-5490 issued). It exercises the "been cancelled" part of the no-open-order row (N4).

## Input ledger (final state, from the review packet)

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial: `issue_refund` supplied by the user; `list_orders`, `cancel_order` and `request_staff_followup` proposed and confirmed with the user's four changes |
| 3 | Data model | found |
| 4 | Authorization policy | found, **default accepted**: cancel only after the customer explicitly confirms the full proposal; any change voids the confirmation |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases from the user, no transcripts |

## Tools

`list_orders()`, `cancel_order(order_number)` and `request_staff_followup(order_number, reason)` are proposed tools, so they are provisional. `issue_refund(order_number)` was supplied by the user. Appendix A is the part of the spec that architecture notes may change.

## Checker (final run)

```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12, CO-S27, CO-S28: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12, CO-S28: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S11, CO-S24, CO-S26: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)
```

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03, CO-S06 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S27 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S25, CO-S26 |
| G-04 | CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10, CO-S29 |
| CO-02 | CO-S02, CO-S07, CO-S28, CO-S29 |
| CO-03 | CO-S01, CO-S08, CO-S09 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27, CO-S28 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S24, CO-S26 |
| CO-06 | CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S25 |
| CO-08 | CO-S01, CO-S16, CO-S19 |

## Findings

**Rounds 2 and 3: 11 kept findings, 7 Important and 4 Nit (2 dropped by verifiers). 3 rounds run in total (round 1 came with the inputs and answered M1 to M13).**

- Round 2: 8 kept (5 Important, 3 Nit) and 1 dropped (M18).
- Round 3: 3 kept (2 Important, 1 Nit) and 1 dropped (N3).

| Id | Class, severity | Summary | Status |
|---|---|---|---|
| M14 | Gap, Important | "Order not cancelled reported" lost the "could not be found" check for CO-S24 | fixed: CO-S24 has its own dimension, "Cancellation not found reported" |
| M15 | Lies, Nit | race variants went placed → shipped, a transition the inputs do not give | fixed: every race row starts at processing |
| M16 | Ambiguous, Important | CO-02 says "may propose" while the row and CO-S28 require it | **open**: proposed rule change (below) |
| M17 | Gap, Important | CO-S25 and CO-S26 did not require the lookup after the unanswered cancellation | fixed: "Fewer than one CO-A1 after the second/first CO-A2." added to Forbidden |
| M19 | Gap, Important | one unanswered lookup forced a handoff even though reads may be retried | fixed in round 2, reworked in round 3 (N1): a repeat is optional |
| M20 | Gap, Nit | the no-open-order row also covered a customer with no orders | fixed in part: the row now requires at least one order. **Open**: the CO-02 clause is a proposed rule change, and what to tell a customer with no orders is the user's call |
| M21 | Ambiguous, Nit | the first-retry row overlapped the second-attempt row | fixed: "and before any second CO-A2" |
| M22 | Lies, Important | "Refund not issued reported" accepted "not confirmed yet" for known failures | fixed: restored for CO-S17, CO-S18 and CO-S22; CO-S20 has its own dimension, "Refund not confirmed reported" |
| N1 | Ambiguous, Important | repeated lookups had no stopping point; CO-S12/S19 row 3 contradicted CO-S14/S15/S21 | fixed: a repeat is optional and the row-3 variants are removed. **Open**: how many lookups to try |
| N2 | Gap, Important | in CO-S12 row 3 an unanswered lookup could authorize a blind refund | fixed: row 3 removed |
| N4 | Gap, Nit | the "been cancelled" part of the no-open-order row was never asserted | fixed: CO-S29 has a cancelled order, and its rubric covers it |
| Pre-existing | n/a | (a) G-04's idempotency clause also covers SG-04, which would permit a blind second CO-A2; (b) the row for an unanswered lookup before any CO-A2 fires on one unanswered read even though reads may be retried; (c) the "No open order reported" wording | (a) and (b) reported and left untouched; (c) settled by the N4 fix |

Dropped: M18 (Not real ×3). §5.1 lets only a question with the exact proposal values count as confirmation, and only CO-A1 supplies those values. N3 (Style only ×2, Real ×1).

**Whether a kept finding quotes a line the previous round changed:**
- Round 2: all 8 kept findings quote a line round 1 changed, so each is a fix that introduced a defect. None quotes an unchanged line. None fell in a bundle context block.
- Round 3: 2 kept findings (N1, N4) quote a line round 2 changed. 1 (N2) quotes a line round 2 did not change ("CO-A3 before a CO-A1 made after the first CO-A2."), but the defect came from row 3, which round 2 added to that scenario. None fell in a bundle context block.
- Every kept finding in both rounds traces to the previous round's fixes. The fixes need more care; the earlier finders did not miss defects in the original text.

## Reviewers

- Subagents (general-purpose, Claude): the faithfulness and coverage finders in rounds 2 and 3, and all six verifiers.
- Through Codex (`codex:codex-rescue`): the verdicts finder in rounds 2 and 3. In round 3 the Codex job outlived its wrapper agent. The result was fetched with `codex-companion.mjs result` and the agent was resumed with SendMessage, which then delivered the same report (see run.log).

## Open questions

- **What if** the customer named no order and exactly one order is open: must the agent propose it without asking which? This is M16, a proposed rule change. CO-02 now says "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order." The proposal is "... the agent proposes that order without asking which."
- **What if** a signed-in customer with no orders at all asks to cancel? This is M20. The proposed CO-02 clause is "When the customer has at least one order and none has, the agent tells the customer none of their orders can be cancelled and proposes nothing." What to say when there are no orders is the user's call.
- **What if** the lookup after an unanswered cancellation or refund call times out? This is N1 and M19. How many lookups must the agent try before handing off? The inputs say reads "may be retried on timeout without limit" and "re-read fails ... hand off", but set no minimum. A repeat is now optional, so no scenario covers a repeat that answers.
- Carried from round 1: the right handling of `OrderNotCancelled` (M2), and whether the agent should do more for an order that is already cancelled with a failed or missing refund (M10).

## What verification cannot catch

Verification cannot tell whether these rules are Harbor Goods' real rules, or whether the stakeholder list (customer, order system, store staff, Harbor Goods, the support team, other customers) is complete. Only the user can confirm that.

## Proposed checklist lines (patterns no checklist covers)

- evaluation-checklist: "When a new scenario reuses a rubric dimension, do not widen its definition. If the new scenario needs a different statement, give it its own dimension, so no existing scenario loses a clause it asserts." (M14, M22)
- evaluation-checklist: "When a scenario's correct ending depends on a read after an unanswered action and no write follows, Forbidden carries 'Fewer than one <read> after <action>'." (M17)
- evaluation-checklist: "An ordering line that gates an action on a lookup ('X before a <read> made after Y') must not be satisfiable by an unanswered read in any row; key it on a read that answered with the authorizing state." (N2)
- use-case checklist (Failure): "Failure-row conditions on retries name which attempt they follow, are bounded so that no two rows match one moment, and any retry of a read either has a stated budget or is optional with the same permitted outcome." (M21, N1)

## Interview

No interview ran in this trial: it started at round 2, and the packet records the original interview.
