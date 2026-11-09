# Report: agent-spec verification trial it1-1

Skill commit 29e7be1. The run started at step 4.1 on a copy of eval/agent-spec/round0-agent-spec.md. Three rounds ran, and the run stopped at the round cap.

## File written

`eval/agent-spec/run-it1-1/agent-spec.md` (copied to `results/it1-1/agent-spec-final.md`).

- Capability 4.1 Cancel Order (state-changing, prefix CO): 25 scenarios, CO-S01 to CO-S25. Round 2 added CO-S25. There were 24 before the run.

## Merges of step 3.9

None. The run started at step 4, so step 3.9 did not run. The checker's WARNING groups (merge candidates) were left as they were:

- CO-S01/S02/S03/S12
- CO-S01/S02/S09/S12
- CO-S11/S24
- CO-S16/S19
- CO-S18/S20
- CO-S22/S23

No rows were dropped by a merge. Rows the verification fixes removed:

- CO-S17 row 3 (OrderNotCancelled after a cancelled CO-A2). It exercised the OrderNotCancelled half of the CO-A3 failure row.

## Input ledger (final, from the review packet; unchanged)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied, the rest proposed and confirmed with changes | interview round 2 Q3, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found (default accepted: a state-changing call only after explicit confirmation of the full proposal; any change voids it) | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases, no transcripts | interview round 2 Q4 |

## Proposed tools

`list_orders()`, `cancel_order(order_number)` and `request_staff_followup(order_number, reason)` are proposed tools that the user confirmed with changes. `issue_refund(order_number)` was supplied by the user. The proposed tools are provisional. Appendix A is the part of the spec that architecture notes may change. Round 1 removed `failure_reason` from the `issue_refund` result, because no input defines it.

## Checker

Final run: `uv run python .claude/skills/agent-spec/scripts/check_spec.py eval/agent-spec/run-it1-1/agent-spec.md`. It printed **0 errors**, plus the 6 merge-candidate WARNINGs above.

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S25 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09 |
| CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S24, CO-S25 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S25 |
| CO-08 | CO-S01, CO-S16, CO-S19 |

## Findings

34 merged findings over 3 rounds: 23 Important, 11 Nit (finder severity). 28 were kept and 6 dropped. No finding was Pre-existing (the whole spec was in scope).

| Round | Count line | Kept | Dropped | Important kept |
|---|---|---|---|---|
| 1 | 14 findings: 8 Important, 6 Nit. | 13 | 1 | 7 |
| 2 | 11 findings: 9 Important, 2 Nit. | 8 | 3 | 5 |
| 3 | 9 findings: 6 Important, 3 Nit. | 7 | 2 | 4 |

Status of every finding (the full text is in round1/2/3-findings.md):

- **Round 1**
  - Fixed: M1, M3, M4, M5, M7, M8, M9, M10, M11, M12, M13, M14.
  - Open: M6 (template §5.1 text).
  - Dropped: M2.
  - Also open: M1's OrderNotCancelled handling and M9's rule.
- **Round 2**
  - Fixed: N1, N3, N5, N6, N8, N9, N10.
  - Open: N2 (kept, verifier severity Nit).
  - Dropped: N4, N7, N11.
- **Round 3**
  - Fixed: P1, P2, P3, P5, P6, P8.
  - Open: P4 (rule text).
  - Dropped: P7, P9.

Round 3 changed the spec, and the cap stopped the run before a confirming round. Its fixes have not been reviewed.

**Attribution** (each kept finding's quoted line compared against the previous round's snapshot with diff):

- **Round 2:** 2 of 8 kept findings quote a line round 1 changed:
  - N5 quotes the new "Order choice asked" dimension.
  - N10 quotes the M14 branch.

  6 quote lines round 1 did not change. Of those, N2 and N3 describe defects that round-1 fixes caused: M1 left the OrderNotCancelled row without a scenario, and M3 left "card closed" in the trajectories.
- **Round 3:** 1 of 7 kept findings quotes a line round 2 changed:
  - P5 quotes the "Order not found reported" fix.

  6 quote unchanged lines. P2 and P3 come from earlier fixes: M11 made CO-S10's single lookup wrong, and N8 made the CO-S19 note stale.

**Verifier drop rate:** 6 of 23 Important findings verified were dropped (26%). The refutations, quoted:

- M2: "G-04 is a necessary condition, not a permission: 'the agent repeats it **only when** ...'. It never allows a resend. CO-06 adds a stricter condition that applies alongside it ... G-04 also cites only '(Appendix B, SG-01)', not SG-04."
- N4: "The CO-A3 failure row decides it: 'the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01.' The input requires the same thing: case 3 ... 'agent retries once, then re-reads'."
- N7: "The CO-S23 dimension already settles the timing for any text the agent sends: 'never says … that staff will follow up' ... In CO-S14, S15, S17, S18, S20 and S22 the task is always created, so the early statement ends up true and no verdict changes."
- N11: "G-01 already has holding-back state checks: CO-S02 'The customer's other order is unchanged and has no refund' and CO-S03 'HG-10482 has status processing and no refund' ... the remaining request is 'one more scenario would be nice'."
- P7: "The input lets the agent hand off after one failed re-read: round 3 Q4 says 'Re-read fails, say outcome unknown, issue no refund, hand off' ... 'Reads **may** be retried on timeout without limit' permits retries and does not require them."
- P9: "The standard the finding relies on ('Each trigger form the spec lists needs at least one scenario') is not in the references, the packet or the spec ... CO-05 has both sides covered."

### Rule changes proposed for the user (not applied; step 4 stops at rule text)

- **New rule for M9 (no arrival date).**
  - Before: absent. The ban appears only in Scope & Authority: "promise a date by which the refunded money arrives."
  - After (proposed): **CO-09 — No arrival date** [minimal guarantee]. "The agent states no date, number of days or time frame by which refunded money arrives."
  - The rubric dimension "No arrival date promised" (CO-S01, CO-S19) was added either way.
- **G-04 for P4.**
  - Before: "... or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
  - After (proposed): "... or, for CO-A3 and CO-A4 only, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03)."
- **CO-06, related to N2.**
  - The clause "never after the order system ... reported the order not cancelled" settles OrderNotCancelled handling before the user has decided it. Keep it or change it depending on the answer to open question 1.

## Open questions

1. What if `issue_refund` reports OrderNotCancelled right after `cancel_order` returned cancelled? The inputs name the outcome but give no handling. The row now has the agent hand off with "refund not issued" and claim the order is cancelled only if a lookup shows it. No scenario can make this outcome true. (M1, N2)
2. What if a lookup never answers? §5.1 ends a trial only on agent messages, and reads may be retried without limit. Should §5.1 or the harness cap tool calls per trial? (M6)
3. What if the customer asks to cancel a second order in the same conversation? G-01 says "the one order the current request is about", and CO-06 caps calls per conversation. (N11)
4. What if a lookup after the second unanswered cancellation shows the order still placed or processing? The spec now says "tell the customer it was not cancelled, no refund, no handoff" (CO-S25 row 1). This follows from G-03 and CO-07, and the user has not confirmed it.
5. What if an order the lookup listed is gone when `cancel_order` runs? CO-S24 now builds OrderNotFound this way. Is that a real case for Harbor Goods?
6. The rule changes proposed above (CO-09, G-04).

## What verification cannot catch

Whether these rules are Harbor Goods' real cancellation and refund rules, and whether the stakeholder list (customer, order system, store staff, Harbor Goods, support team, other customers) is complete. Only the user can confirm these.

## Checklist lines proposed

These kept findings' patterns are not covered by any checklist:

- evaluation-checklist: "A rubric dimension shared by several scenarios uses wording that holds in every one of them." (M7)
- evaluation-checklist: "A 'reported' rubric dimension asks the agent to say exactly what the matching failure row tells it to say, no more." (N6, N1)
- evaluation-checklist: "When a fix removes a Forbidden line or check, every Unambiguity note that named it is updated." (P3)
- cockburn-checklist: "A failure row that branches on a lookup states that at least one lookup must be tried before its no-answer branch." (P1)
- evaluation-checklist: "A rubric clause that forbids an 'offer' or a 'proposal' defines it, and says whether a clarifying question counts." (N5, P5)

## Interview

This run started at step 4, so no interview ran. The review packet records the original interview as direct question-and-answer rounds.
