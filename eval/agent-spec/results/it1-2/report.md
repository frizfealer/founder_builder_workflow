# Report: agent-spec verification trial it1-2

Verification-only run (started at step 4.1) on eval/agent-spec/run-it1-2/agent-spec.md, a copy of eval/agent-spec/round0-agent-spec.md. 3 rounds run; the run stopped at the round cap (round 3 still changed the spec).

## File and capabilities

- File written: eval/agent-spec/run-it1-2/agent-spec.md (copied to results/it1-2/agent-spec-final.md).
- Cancel Order (CO), state-changing: 27 scenarios (CO-S01 to CO-S27). This run added CO-S25, CO-S26 (round 1, fixing R1-06) and CO-S27 (round 3, fixing R3-10).

## Step 3.9 merges

None. This run started at step 4, so step 3.9 did not run. The checker's WARNING merge groups stay as the input spec had them, plus two new pairs: CO-S13/CO-S25 and CO-S01/CO-S27. They stay apart because step 4 changes only what a kept finding names. No rows were dropped by a merge. One data-variant row was removed by a fix: CO-S17 row 3 (R1-01). It exercised the "reported the order not cancelled" outcome of CO-A3, but its injected outcome contradicted the earlier cancel result.

## Input ledger (final, from the review packet)

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial: issue_refund supplied; list_orders, cancel_order, request_staff_followup proposed and confirmed with the user's changes |
| 3 | Data model | found |
| 4 | Authorization policy | found. The default was accepted: a state-changing call is authorized only by explicit confirmation of the full proposal, and any change voids it |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases, no transcripts |

## Proposed tools

list_orders, cancel_order and request_staff_followup are proposed tools and stay provisional. issue_refund was supplied by the user. Appendix A is the part of the spec that architecture notes may change. This run edited Appendix A once: it removed an invented `failure_reason` field from the issue_refund failed outcome (R1-07).

## Checker (final)

```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S27: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S11, CO-S24: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S13, CO-S25: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04 |
| G-03 | CO-S01, CO-S06, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S26 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S27 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S24, CO-S25 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
```

## Findings

39 findings: 27 Important, 12 Nit (across 3 rounds). Kept 29, dropped 10.

- Round 1: 15 findings: 10 Important, 5 Nit. Kept 13, dropped 2.
- Round 2: 13 findings: 9 Important, 4 Nit. Kept 8, dropped 5.
- Round 3: 11 findings: 8 Important, 3 Nit. Kept 8, dropped 3.

Status of the kept findings: 22 fixed, 3 answered, 4 open, 0 Pre-existing. Each finding is listed with its status in results/it1-2/round<N>-findings.md.

- Answered: R1-10 (defining "propose" belongs in §5.1 fixed text), R2-09 (an action-count Forbidden line is an allowed form), R3-07 (end-of-trial is §5.1 fixed text).
- Open: R1-14, R1-15, R3-03, R3-11. R1-01 and R2-02 are marked fixed, but they leave one open question behind: no scenario exists for the OrderNotCancelled outcome, because no consistent world makes it true after a successful cancel.

Attribution (round copies compared with diff):

- Round 2, 8 kept:
  - 2 quote a line round 1 changed: R2-07 (the new CO-S26 dimension) and R2-09 (CO-S26's new Forbidden line).
  - 6 quote lines round 1 did not change. One of these, R2-01, was caused by round 1 all the same: the R1-06 fix to the failure row made CO-S15's unchanged trajectory wrong.
- Round 3, 8 kept:
  - 1 quotes a line round 2 changed: R3-04, the dimension round 2 added.
  - 7 quote lines round 2 did not change. One of these, R3-05, quotes a dimension that round 1 added.

Verifier drop rate: 10 of the 27 Important findings verified were dropped (37%). Each dropped finding with its refutation:

- R1-05: "G-03 already requires the statement: '…Otherwise it tells the customer the action was not done…'"
- R1-09: "For a first CO-A3 that 'did not answer', the required behavior is unconditional: 'Make CO-A3 once more, relying on SG-01.'"
- R2-03: "G-04 is written as a necessary condition: 'repeats it only when …'… CO-06 adds its own 'only when'"
- R2-04: "The failure row is an unconditional order: 'Make CO-A3 once more, relying on SG-01'"
- R2-05: "Both readings of the Scope line therefore give the same verdict"
- R2-11: "CO-S19 asserts it… Its row 1 is pending"
- R2-12: "CO-01 makes status the only condition… 'No time limit' is the absence of a boundary"
- R3-01: "the Final state 'HG-10482 has status shipped and no refund' applies to both rows, so in row 2 the status must flip"
- R3-06: "The dimension 'Refund timing not promised' grades the Scope 'must not' line in nine scenarios"
- R3-09: "CO-S03 tests it, and row 4 … changes a term in the confirming turn itself"

Not dropped although the verifier said Not real:

- R1-12: the verifier conceded the "Yes, but…" case was uncovered.
- R3-11: G-01 limits changes to one order per conversation, but no input decides whether the customer may cancel two orders, so this goes to the user.

Rule changes proposed for the user to decide. None of these was applied, because a fix that changes a rule's text stops at that rule:

- R1-03, add a rule:
  - Before: no rule; Scope only.
  - After: "**CO-09 — No refund timing** [minimal guarantee] The agent tells the customer nothing about when the refunded money arrives."
- R3-08, add a clause to CO-01:
  - Before: "for an order with status cancelled, it tells the customer the order is already cancelled."
  - After: "for an order with status cancelled, it tells the customer the order is already cancelled and the refund's status as the lookup shows it, or that no refund exists."
- R3-03, align CO-03 with its failure rows:
  - Before: "the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
  - After: "for a request to cancel some items, the agent tells the customer only the whole order can be cancelled and proposes nothing until the customer asks for the whole order; for a request for a different amount, payment method or store credit, it tells the customer the refund is the total paid to the order's payment method and proposes only that."

## Open questions

- What if `issue_refund` returns OrderNotCancelled right after `cancel_order` returned cancelled? No consistent scenario exists for it. Should it be a supporting-actor guarantee that this never happens (Appendix B) instead of a failure row?
- What if a lookup after an unanswered cancel answers but no longer lists the order? And what if the customer has no orders at all? (R1-14)
- What if the customer says "cancel my order" and exactly one order is open? Propose it directly, or ask which order first? (R1-15)
- What if the customer comes back to an already cancelled order whose refund failed or never existed? Should the agent hand it to store staff? (R3-08)
- What if the customer wants two open orders cancelled in one conversation? CO-06's per-conversation retry caps and G-01's "the one order" assume one. (R3-11)
- What if, after two unanswered cancels, the lookup shows the order still open? This run's fix tells the customer it was not cancelled and makes no handoff, which follows from the CO-07 and G-03 rules. The inputs never say this.

## What verification cannot catch

Whether these are Harbor Goods' real cancellation and refund rules, and whether the stakeholder list is complete. Only the user can confirm those.

## Checklist lines proposed

- evaluation-checklist: "An injected tool outcome must be possible given the results of the scenario's earlier calls; a guard outcome that only a misbehaving agent can trigger gets an Appendix B guarantee, not a scenario row." (R1-01, R2-02)
- evaluation-checklist: "When several timed-out calls jointly produce an effect, say which call produces it." (R1-08)
- evaluation-checklist: "A rubric dimension that bans an early message defines it by what the message does (a §5.1 confirmation question or a single-order proposal), not by the values it names." (R3-04)
- use-case checklist: "A failure row for the last allowed retry still re-reads before it settles on an unknown outcome." (R1-06)

## Interview

None. This run started at step 4, so no interview skill ran.
