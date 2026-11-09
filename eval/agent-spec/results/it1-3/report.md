# Agent Spec verification report — trial it1-3

## File and capabilities
- File: eval/agent-spec/run-it1-3/agent-spec.md (copy at results/it1-3/agent-spec-final.md).
- One capability: 4.1 Cancel Order (CO, state-changing), 27 scenarios: CO-S01 to CO-S23, CO-S25 to CO-S28. CO-S24 was removed in round 1. CO-S25 and CO-S26 were added in round 2, CO-S27 and CO-S28 in round 3.

## Merges (step 3.9)
None. The run started at step 4.1, so step 3.9 did not run. The checker's merge WARNINGs are listed below and were not acted on.
Dropped rows (from verification fixes, not merges): CO-S17 row 3 (exercised the CO-A3 OrderNotCancelled outcome right after a cancel that returned cancelled; R1-01). The whole of CO-S24 (exercised CO-A2 OrderNotFound for an order the lookup had just listed, and the CO-05 not-found clause; R1-01).

## Input ledger (final, from the review packet)
1 Capabilities found. 2 Tools partial: issue_refund supplied, list_orders, cancel_order and request_staff_followup proposed and confirmed with changes. 3 Data model found. 4 Authorization policy found; the **default was accepted** (an explicit confirmation of the full proposal, voided by any change). 5 Domain rules found. 6 Known failure cases found: three cases, no transcripts.

## Proposed tools
list_orders, cancel_order and request_staff_followup are proposed tools and stay provisional. Appendix A is the part of the spec that architecture notes may change. In round 1, Appendix A lost an invented failure_reason field (R1-09).

## Checker (final run)
```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12, CO-S27: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S28: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S13, CO-S26: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S27 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S25 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S27, CO-S28 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27, CO-S28 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S25, CO-S26 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S25 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01, CO-S19 |
```

## Findings
37 findings over 3 rounds (the cap; the run stopped there): 22 Important, 15 Nit. Of these, 23 fixed, 1 answered, 7 open, 6 dropped, 0 Pre-existing.

Round 1 (15 merged: 8 Important, 7 Nit):
- fixed: R1-01, R1-03, R1-04, R1-05, R1-06, R1-08, R1-09, R1-10, R1-11, R1-12, R1-13, R1-15.
- answered: R1-14. It stands because list_orders always lists every order of the customer.
- dropped: R1-02, R1-07.

Round 2 (13 merged: 9 Important, 4 Nit):
- fixed: R2-01, R2-03, R2-04, R2-06, R2-10, R2-11, R2-12.
- open: R2-02, R2-09, R2-13.
- dropped: R2-05, R2-07, R2-08.

Round 3 (9 merged: 5 Important, 4 Nit):
- fixed: R3-01, R3-03, R3-04, R3-06.
- open: R3-02, R3-07, R3-08, R3-09.
- dropped: R3-05.

Attribution, from diffs of the round copies:
- Round 2: 0 kept findings quote a line round 1 changed, and 10 quote lines round 1 left unchanged (6 Important, 4 Nit). These are defects earlier finders missed.
- Round 3: 2 kept findings quote lines round 2 added (R3-01 on CO-S26 and R3-06 on CO-S25: a fix introduced a defect). The other 6 quote unchanged lines (R3-02, R3-03, R3-04, R3-07, R3-08, R3-09).

Verifier drop rate: 6 of the 22 verified Important findings were dropped (27%). Each refutation, quoted:
- R1-02: "G-04 only restricts. It reads "the agent repeats it **only when** … or when …", which sets a necessary condition and grants no permission." The CO-A2 failure row also says "Make no CO-A2 or CO-A3 until a lookup made after it answers."
- R1-07: "The failure row settles it without condition: "CO-A3 | … for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01.""
- R2-05: "§5.1 ties a proposal to a question that "states every value of the proposal and asks the user to go ahead". Listing both orders' refund details and asking "Which one?" asks nobody to go ahead."
- R2-07: "One unanswered lookup is enough to trigger each row … rows 103 and 108 say "If the lookup does not answer", in the singular."
- R2-08: "CO-03 limits every proposal, including the "changed proposal" in row 99: "Every proposal cancels the whole order and refunds its total paid to its payment method"." R3-03 later found that the row's wording still conflicted with CO-03, and that was fixed.
- R3-05: ""Refund status reported" (CO-S19 …) requires that the agent "tells the customer … the refund's status is the data-variant row's refund status, and states no other status for it"."

One finding was kept against the verifier: the verifier rated R2-04 Not real, but its refutation cited the Unambiguity note, not a testable line, so the finding was kept and fixed.

## Open questions (what if…)
- What if issue_refund reports OrderNotCancelled for an order the agent believes is cancelled? What should the agent do, and what should it say? (R1-01, R2-02.) The current row says "the order is cancelled" and hands off as refund not issued. No consistent scenario can trigger this outcome, nor cancel_order's OrderNotFound for a listed order.
- What if the customer asks to cancel a second order in the same conversation, or both orders at once? (R2-09.)
- What if the customer names no order and has no placed or processing order? (R2-13.)
- What if every lookup goes unanswered and the agent retries list_orders without limit? The packet allows unlimited read retries, and the trial has no tool-call bound. (R3-02.)
- What if the refund retry answers (failed, provider unavailable, or pending) after a first call that timed out? Does packet round 3 Q3 still require a re-read and the "not confirmed yet" wording? (R3-07.)
- What if issue_refund returns a refund with the wrong amount or payment method? (R3-09.)
- Proposed rule change, CO-03 (R3-08). Rule text changes stop at the rule, so this needs the user's decision.
  - Before: "…the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
  - After (proposed): "When the customer asks to cancel only some items, the agent tells the customer only the whole order can be cancelled and proposes nothing until the customer asks to cancel the whole order; when the customer asks for a different amount, a different payment method or store credit, the agent tells the customer the refund is the total paid to the order's payment method and proposes only that."

## What verification cannot catch
Verification cannot show whether these are Harbor Goods' real rules, or whether the stakeholder list is complete. Only the user can confirm both.

## Checklist lines proposed
- evaluation-checklist: "An Initial-state line that injects an outcome must name which of several unanswered calls has the effect; never 'together they'." (R1-06)
- evaluation-checklist: "A confirmation-form pair that must only be answerable after a scripted change-of-mind turn carries (after Turn n)." (R2-03)
- cockburn-checklist: "A failure row for a repeated timeout keeps the same re-read-then-branch handling as the first." (R2-06)
- evaluation-checklist: "A rubric dimension requires no statement that its scenario's failure rows do not require." (R2-01)
- evaluation-checklist: "An injected outcome must be possible given the scenario's own earlier call results; an outcome no consistent world produces gets an open question, not a scenario." (R1-01)

## Interview
The run started at step 4.1, so no interview ran. The packet records a direct interview.
