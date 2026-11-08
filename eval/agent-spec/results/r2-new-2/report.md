# Report: Harbor Goods order-support agent spec, verification rounds 2 and 3 (r2-new-2)

## File written

eval/verify-test/run-r2-new-2/agent-spec.md (copy: results/r2-new-2/agent-spec-final.md). One capability, 4.1 Cancel Order (state-changing, prefix CO), 29 scenarios (CO-S01 to CO-S29). Data-variant rows changed this run: CO-S29 gained row 3 (an already cancelled order); CO-S14 row 3, added in round 2, was removed in round 3. CO-S28 gained one optional User-knows pair.

## Merges (step 3.9)

None in this run. Rounds 2 and 3 change no scenario ids, so no merges. The checker's six WARNING groups were present after round 1 and are still there; they are left as they are.

## Input ledger, final state

Unchanged from the review packet: 1 Capabilities, found; 2 Tools, partial (issue_refund supplied, the rest proposed and confirmed with the user's four changes); 3 Data model, found; 4 Authorization policy, found (the default was accepted: a state-changing call is authorized only by explicit confirmation of the full proposal, and any change voids it); 5 Domain rules, found; 6 Known failure cases, found (three cases, no transcripts).

## Proposed tools

list_orders(), cancel_order(order_number) and request_staff_followup(order_number, reason) were proposed and confirmed with changes. issue_refund(order_number) was supplied by the user. The proposed tools are provisional. Appendix A is the part of the spec that architecture notes may change.

## Checker

```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12, CO-S27, CO-S28: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12, CO-S28: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S11, CO-S24, CO-S26: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)

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
```

## Findings

Rounds 2 and 3, after verification: 17 kept findings: 6 Important, 11 Nit. 1 more was dropped (M18), and 2 Pre-existing findings were reported and left untouched (P1, P2). Two rounds were run in this trial; round 1 had already happened. The skill's limit stopped the run after round 3.

| Id | Round | Severity | Status |
|---|---|---|---|
| M14 | 2 | Important | fixed: CO-S25 and CO-S26 forbid ending without a lookup after the last unanswered cancellation |
| M15 | 2 | Important | fixed: CO-S24 has its own dimension "Cancellation not found reported" |
| M16 | 2 | Important | fixed: "Refund not issued reported" requires "has not been issued" again; CO-S20 uses "Refund not confirmed reported" |
| M17 | 2 | Nit | open: proposed rule change to CO-03 (below) |
| M19 | 2 | Nit | fixed: the CO-S17, CO-S22 and CO-S23 trajectories no longer show a failure reason |
| M20 | 2 | Nit | open: next step after the second unanswered cancellation, with the order still open |
| M21 | 2 | Nit | answered: stands until the user answers round 1's M10 open question |
| M22 | 2 | Nit | fixed (rubric, CO-S29 row 3); the customer-with-no-orders case is open |
| M23 | 2 | Nit | answered after M30: the confirmed list_orders contract cannot return a list without an order the customer owns, so no scenario injects that case; open whether it can happen |
| M24 | 2 | Nit | fixed: CO-S11 and CO-S26 row 2 race from processing |
| M25 | 2 | Nit | fixed: the failure row allows asking; completed by M28 |
| M26 | 2 | Nit | open: proposed rule change to CO-02 (below) |
| M27 | 2 | Nit | open: the round-2 fix was reverted under M29 |
| M28 | 3 | Important | fixed: optional which-order pair in CO-S28 |
| M29 | 3 | Important | fixed by revert: the OrderNotCancelled row is back to its round-1 text; its handling is open |
| M30 | 3 | Nit | fixed by revert: CO-S14 is back to its round-1 block |
| M31 | 3 | Important | fixed: "No open order reported" now forbids only claiming the agent cancelled an order in this conversation |
| P1 | 2 | - | Pre-existing: G-04 cites only SG-01, but the CO-A4 retry relies on SG-03 |
| P2 | 3 | - | Pre-existing: "Shipped order explained" asks for a past "was not cancelled" that CO-S05's reference does not state |

Count lines by round: round 2, 13 kept findings: 3 Important, 10 Nit (1 dropped, 1 Pre-existing). Round 3, 4 kept findings: 3 Important, 1 Nit (0 dropped, 1 Pre-existing).

Where each kept finding came from:
- Round 2: all 13 kept findings quote a line that round 1 changed (a fix that introduced a defect), and 0 quote a line round 1 left alone (a defect earlier finders missed). None fell in a bundle context block.
- Round 3: all 4 kept findings quote a line that round 2 changed, and 0 quote an unchanged line. None fell in a bundle context block. Three of the four (M28, M29, M30) are defects introduced by round-2 fixes (M25, M27, M23).

### Proposed rule changes (not applied; for the user to decide)

- CO-03 (M17). Before: "The agent states no date or time frame by which the refunded money arrives." After: "The agent promises no date or time frame by which the refunded money arrives." The confirmed input is "The agent promises nothing about when the money arrives." If this is accepted, the dimension "No arrival date promised" and its Unambiguity-note mentions would change the same way.
- CO-02 (M26). Before: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order. ... When none has, ..." After: "When the customer has not said which order they mean and exactly one of the customer's orders has status placed or processing, the agent may propose that order. ... When none has, ...". This makes clear that describing an order (by item or by date) counts as saying which order. The two "named no order" failure rows would follow.

## Reviewers

- Verdicts finder, both rounds: through Codex, using the codex:codex-rescue agent type.
- Faithfulness and coverage finders, both rounds: general-purpose subagents.
- All six verifiers (three per round): general-purpose subagents.

## Open questions

- What if the second cancellation goes unanswered and a lookup shows the order still open? Should the agent hand off to staff, tell the customer to contact support, or only say it was not cancelled? (M20)
- What if an order cancelled before this conversation has a failed or missing refund? (round 1 M10, M21)
- What if issue_refund reports the order not cancelled right after cancel_order returned it cancelled? Hand off to staff under CO-07, or not? (round 1 M2, M27, M29)
- What if list_orders answers but leaves out the order the agent just tried to cancel? Can that happen? (M23, M30)
- What if a customer with no orders at all asks to cancel "my order"? (M22)
- Should CO-03 forbid only promising an arrival date, or stating one at all? (M17)
- Does describing an order count as naming it under CO-02? (M26)

## What verification cannot catch

Whether these rules are the business's real rules, and whether the stakeholder list is complete. Only the user can confirm either.

## Proposed checklist lines (kept findings no checklist covers)

These are for the evaluation checklist unless noted.
- Every permitted alternative needs an answer. When a rule or failure row allows the agent to ask instead of act, every scenario that triggers it has a User-knows pair, marked optional, that answers that question (M28).
- The outcome report waits for its lookup. When a scenario's outcome report depends on a lookup made after an unanswered call, and no write follows that would order it, a Forbidden line requires the lookup ("Fewer than one <read> after <call>") (M14).
- Injected tool results must be possible. An Initial-state tool result is one the confirmed tool contract can return (M30).
- For the Specification-by-Example checklist: a rubric that reports a pre-existing status separates it from the agent's own action ("never says it cancelled ... in this conversation") (M31).
- For the use-case checklist: a failure row's action holds against every rule it cites, including "in no other situation" clauses (M27, M29).

M15 and M16 fall under the existing line "A shared rubric dimension has one definition".

## Interview

None ran in this trial. It started after round 1, and nothing was asked of the user.
