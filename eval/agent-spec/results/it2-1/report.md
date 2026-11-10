# Report: agent-spec verification, trial it2-1

Verification-only run of the agent-spec skill at a5e1880, starting at step 4.1 on the frozen round-0 spec. Three rounds ran; round 3 hit the round cap, so the run stopped with findings still open.

## File written

- `eval/agent-spec/run-it2-1/agent-spec.md`, the spec under review. A copy is at `results/it2-1/agent-spec-final.md`.
- Capability Cancel Order (CO, state-changing): 28 scenarios, CO-S01 to CO-S28. The round-0 spec had 24. The run added these:
  - CO-S25: second cancellation unanswered, order shipped.
  - CO-S26: second cancellation unanswered, order still open.
  - CO-S27: second cancellation unanswered, but the order was cancelled.
  - CO-S28: customer asks to cancel some items, then the whole order.
- New data-variant rows:
  - CO-S01 row 4: one open order, and the request names no order.
  - CO-S01 row 5: the first lookup goes unanswered and a repeated lookup answers.
  - CO-S03 row 4: the customer confirms and changes the order in the same turn.
- Removed data-variant row: CO-S13 row 3, added in round 1, became CO-S27 in round 2.
- New rule: CO-09, no arrival date promised (round 1).

## Merges of step 3.9

None. The run started at step 4, so it made no consolidation merges and dropped no rows. The checker's WARNING groups stay apart, each for a stated reason:
- From round 0: CO-S01/02/03/12, CO-S01/02/09/12, CO-S11/24, CO-S16/19, CO-S18/20, CO-S22/23.
- Added by this run:
  - CO-S25/CO-S26: the final status lines and the dimensions differ.
  - CO-S13/CO-S27: CO-S27 needs a lookup-guard Forbidden line that CO-S13's rows must not carry (R2-01).
  - CO-S01/CO-S28: the final state and the dimensions differ.

## Input ledger, final state

The ledger is unchanged from the review packet:

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial: issue_refund supplied, the rest proposed and confirmed with the user's changes |
| 3 | Data model | found |
| 4 | Authorization policy | found, with the default accepted: a cancellation runs only after explicit confirmation of the full proposal, and any change voids the confirmation |
| 5 | Domain rules | found |
| 6 | Known failure cases | three cases, no transcripts |

## Proposed tools

These are provisional. `list_orders()`, `cancel_order(order_number)` and `request_staff_followup(order_number, reason)` were proposed and confirmed with changes. `issue_refund(order_number)` was supplied by the user. Appendix A is the part of the spec that architecture notes may change.

Verification changed Appendix A once: R1-04 removed the `failure_reason` field and its enum values, which no input supports.

## Checker

Final run, after the round-3 fixes:

```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S28: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S11, CO-S24: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S13, CO-S27: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S25, CO-S26: identical Required events after substitution; merge candidates (skill step 3.9)

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S25, CO-S26 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26, CO-S27 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S28 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S28 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S24, CO-S25, CO-S27 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26, CO-S27 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S26 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01 |
```

## Findings

32 findings: 19 Important, 13 Nit. That is 32 merged from 36 raw over 3 rounds (15, 12, 9).
- 26 kept: 19 fixed, 1 answered, 6 open.
- 6 dropped: 4 Important, 2 Nit.
- 0 Pre-existing.

Per round count lines (merged; kept; dropped):
- Round 1: 14 findings: 9 Important, 5 Nit. 11 kept, 3 dropped (3 Important).
- Round 2: 9 findings: 5 Important, 4 Nit. 8 kept, 1 dropped (1 Nit).
- Round 3: 9 findings: 5 Important, 4 Nit. 7 kept, 2 dropped (1 Important, 1 Nit).

Round attribution, from diffs of the saved round copies:
- **Round 2:** 2 kept findings quote a line round 1 changed, so a round-1 fix introduced the defect:
  - R2-01: CO-S13 row 3, added by the R1-02 fix, had no lookup guard.
  - R2-06: the Turn 2 trigger rewritten by R1-09 named a confirmation question that had no pair.

  The other 6 quote lines round 1 did not touch, so earlier finders missed them: R2-02, R2-03, R2-04, R2-05, R2-07, R2-08.
- **Round 3:** 0 kept findings quote a line round 2 changed. All 7 quote lines round 2 left alone, so they are defects earlier finders missed. R3-03 and R3-04 quote lines added in round 1 (CO-09 and "Refund not confirmed reported"), not in round 2.

Verifier drop rate:
- Important: 4 dropped of 19 verified (21%).
- Nit: 2 dropped of 13 verified (15%).
- Overall: 6 of 32.

Each dropped finding, with the refutation I read and agreed with:
- R1-06 (Important): "Make CO-A3 once more, relying on SG-01". The failure row requires the retry whatever a lookup shows.
- R1-07 (Important): G-03 "Otherwise it tells the customer the action was not done". The "no refund was issued" clause in the dimension traces to G-03.
- R1-12 (Important): "Refund status reported" (CO-S19) asserts G-03's status clause, "the refund's status is the data-variant row's refund status, and states no other status for it".
- R2-09 (Nit): G-04's "repeats it only when" is a necessary condition. CO-06 adds the stricter rule, "It makes a second CO-A2 only after ... a lookup made after it shows the order still placed or processing".
- R3-01 (Important): G-03 "Otherwise it tells the customer the action was not done", and packet failure case 3, "re-reads the order and refund records and reports what it finds".
- R3-09 (Nit): CO-03 "refunds its total paid", and the user's rule "refund amount = order total paid". No rule depends on shipping or tax.

The verifier rated two Nits Style only, and I kept both. Under step 4.4 I read each finding's Quote and Evidence, and neither is about wording or preference:
- R2-03 is a factual Illustrates mislabel against the Specification-by-Example checklist.
- R2-08 is a Forbidden-line form that the evaluation checklist rules out.

Each finding with its status (verbatim text in round1-findings.md, round2-findings.md and round3-findings.md):
- R1-01 | Lies | Important | open: Verifier could not refute. Only the user can say when OrderNotCancelled (after a CO-A2 that returned cancelled) and OrderNotFound (for an order the lookup listed) can occur; lines left unchanged and reported as an open question.
- R1-02 | Lies | Important | fixed: Second-unanswered-CO-A2 failure row now re-reads and branches on the lookup; CO-S15 gains the lookup step and guard; CO-S13 row 3 (later CO-S27), CO-S25 and CO-S26 exercise the new branches.
- R1-03 | Lies | Important | fixed: Timeout-then-lookup branch now says the refund 'is not confirmed yet' (input wording); CO-S20 uses new dimension 'Refund not confirmed reported'.
- R1-04 | Lies | Nit | fixed: Removed failure_reason from Appendix A and 'card closed' from three reference trajectories.
- R1-05 | Ambiguous | Important | fixed: CO-S19, CO-S20, CO-S21 Initial state now name which unanswered CO-A3 creates the refund. The CO-S19 sub-bullet the verifier refuted is moot after the fix.
- R1-06 | Ambiguous | Important | dropped: Read failure row 'did not answer [the first CO-A3] | Make CO-A3 once more, relying on SG-01': it requires the retry with no lookup condition, so an agent that stops fails by the row; agree it refutes.
- R1-07 | Ambiguous | Important | dropped: Read G-03 'Otherwise it tells the customer the action was not done' and that rows 100-101 cite G-03; the refund was not done, so the dimension's clause traces to G-03 and the trajectories; agree it refutes.
- R1-08 | Untestable | Nit | answered: Stands: the fix belongs to §5.1 'End of trial', fixed template text that step 4 never edits; reported as a template proposal.
- R1-09 | Ambiguous | Nit | fixed: CO-S03 and CO-S04 Turn 2 anchored on the agent's first confirmation question (§5.1) for the HG-10482 proposal (completed in round 2 by R2-06).
- R1-10 | Gap | Important | fixed: CO-S03 row 4 confirms and changes the order in the same turn.
- R1-11 | Gap | Important | fixed: New rule CO-09, Harbor Goods interest, CO-S01 dimension 'No arrival date promised'.
- R1-12 | Gap | Important | dropped: Read 'Refund status reported' (CO-S19) 'the refund's status is the data-variant row's refund status, and states no other status': a scenario asserts G-03's status clause, so the Gap class (rule with no scenario asserting it) does not fit; agree it refutes.
- R1-13 | Gap | Nit | open: Inputs do not say what the agent does when the lookup after an unanswered CO-A2 answers without the order; open question.
- R1-14 | Gap | Nit | open: Inputs do not say what the agent does when one request asks to cancel more than one order; open question.
- R2-01 | Gap | Important | fixed: CO-S13 row 3 became CO-S27 with the lookup guard; CO-S25 and CO-S26 gain a final-message-before-lookup Forbidden line.
- R2-02 | Gap | Important | fixed: CO-S02 uses new dimension 'Asked which order first'.
- R2-03 | Lies | Nit | fixed: Style only verdict on a Nit: read the Quote and Evidence; the finding is a factual mislabel against the Specification-by-Example checklist, not wording, style or preference, so kept. CO-05 removed from CO-S06 Illustrates.
- R2-04 | Gap | Important | fixed: New scenario CO-S28 (partial request, then the whole order).
- R2-05 | Gap | Nit | fixed: CO-S01 row 4: one open order, request names none.
- R2-06 | Ambiguous | Important | fixed: CO-S03 and CO-S04 gain the HG-10482 confirmation-form pair marked (before Turn 2).
- R2-07 | Ambiguous | Important | fixed: Dimension limits the 'was not cancelled' clause to the final message; CO-S14, CO-S15 notes match.
- R2-08 | Untestable | Nit | fixed: Style only verdict on a Nit: read the Quote and Evidence; the finding is about a Forbidden line form the evaluation checklist rules out, not wording or preference, so kept. Rewritten as a timing violation.
- R2-09 | Ambiguous | Nit | dropped: Read G-04 '...repeats it only when...' (a necessary condition) and CO-06 'It makes a second CO-A2 only after ... a lookup made after it shows the order still placed or processing': the two hold together and no blind CO-A2 is allowed; agree it refutes.
- R3-01 | Lies | Important | dropped: Read G-03 'Otherwise it tells the customer the action was not done' and packet case 3 '...re-reads the order and refund records and reports what it finds': both required statements trace to them; agree it refutes.
- R3-02 | Lies | Nit | fixed: Customer-support team interest now has unfinished orders handed to store staff.
- R3-03 | Ambiguous | Important | open: Dimension 'No arrival date promised' now counts any timing statement, hedged or not. The matching change to rule CO-09's text is a rule change, so it stops at the rule and is proposed to the user (before/after in report.md).
- R3-04 | Ambiguous | Important | fixed: 'Refund not confirmed reported' accepts the more specific truthful report (failed, or not issued).
- R3-05 | Ambiguous | Important | fixed: Kept at the verifier's partial refutation: CO-S08/CO-S28 instances refuted (CO-04 and §5.1 define a proposal as stating every value; agree), CO-S07 instance stands. 'Order not found reported' now checks no proposal for any other order.
- R3-06 | Gap | Important | open: Only the user can decide whether a cancelled order with no or a failed refund, plus a money-back request, is handed off (CO-07) or only reported (CO-01); open question.
- R3-07 | Gap | Nit | open: Inputs do not say what the agent tells a customer who names no order when no order is open; open question.
- R3-08 | Gap | Nit | fixed: First failure row covers a repeated lookup that answers; lookup-unanswered branches read 'If no lookup made after it answers'; CO-S01 row 5.
- R3-09 | Gap | Nit | dropped: Read CO-03 'refunds its total paid' and the user's Round 2 Q3 rule 'refund amount = order total paid': no rule depends on shipping or tax; agree it refutes.

## Proposed rule change, for the user to decide (R3-03)

A fix that changes a rule's text stops at that rule. I updated the dimension "No arrival date promised" but left the rule as it was.

- **CO-09 before:** "The agent tells the customer no date or time span by which refunded money arrives."
- **CO-09 proposed:** "The agent says nothing about when refunded money arrives: no date, no time span and no estimate, however hedged."

The input, Round 3 Q1, says: "The agent promises nothing about when the money arrives."

## Open questions

- R1-01: When can `issue_refund` return OrderNotCancelled for an order that `cancel_order` has just returned as cancelled (CO-S17 row 3)? And when can `cancel_order` return OrderNotFound for an order the lookup just listed (CO-S24)? If neither can happen, should those rows and scenarios go?
- R1-13: What should the agent do if the lookup after an unanswered cancellation answers but no longer lists the order?
- R1-14: What should the agent do if the customer asks to cancel two orders at once ("cancel both")? Handle them one at a time, each with its own confirmation, or refuse the second?
- R3-03: Should CO-09 be widened to forbid any statement about when the money arrives, hedged or not? (See the proposed change above.)
- R3-06: What should happen when the customer asks for their money back on an order that is already cancelled but has no refund, or a failed one? Report it as already cancelled (CO-01), or hand it to store staff (CO-07)?
- R3-07: What should the agent tell a customer who names no order when none of their orders is open: none at all, or only shipped, delivered or cancelled ones, possibly several?
- From the R1-02 fix: after two unanswered cancellations, if the lookup shows the order still open, the existing rules (CO-06, CO-07, G-03) say the agent reports "not cancelled" and makes no handoff. CO-S26 now asserts this. Is that the business's intent, or should store staff follow up?

## What verification cannot catch

Verification cannot tell whether these rules are Harbor Goods' real cancellation and refund rules, or whether the stakeholder list is complete (customer, order system, store staff, Harbor Goods, customer-support team, other customers). Only the user can confirm those.

## Proposed checklist lines

These patterns from kept findings are not covered by any checklist:
- **Evaluation checklist:** a data-variant row that turns a call's answered outcome into an unanswered one needs the lookup-before-next-commit Forbidden line. When the other rows cannot carry that line, the row is its own scenario (R2-01).
- **Evaluation checklist:** a User turn that replaces a confirmation is triggered by a confirmation-form pair in User knows, scoped (before Turn n), so that the trigger is a defined §5.1 event (R1-09, R2-06).
- **Evaluation checklist:** a rubric "never says X" clause names the messages it covers whenever X is true at an earlier point in the trajectory (R2-07).
- **Use-case checklist, Failure handling:** an Initial-state line for a call that may or may not take effect names which call took effect, so every lookup between calls has a defined result (R1-05).
- **Template, §5.1 "End of trial":** when reads may be retried without limit, the trial also ends at a cap on tool calls, not only on agent messages (R1-08; step 4 cannot edit this fixed text).

## Interview

No interview ran in this trial. It started at step 4.1 from the frozen spec and review packet, and asked the user nothing. The packet does not record which interview skill produced its answers.

## Reviewers

All 12 reviewers ran as native subagents (general-purpose), with no Codex. Each round had 3 finders and 1 verifier. The skill at a5e1880 names no Codex verdicts finder, so none was dispatched.
