# Report: agent-spec verification-only trial it1b-3

Skill at commit 9b7479f. The run started at step 4.1 on a copy of eval/agent-spec/round0-agent-spec.md and ran step 4 through the three-round cap. Every round changed the spec, so the stop came from the cap, not from a round that changed nothing.

## File written

- eval/agent-spec/run-it1b-3/agent-spec.md (copied here as agent-spec-final.md).
- Capability 4.1 Cancel Order (state-changing, prefix CO): 25 scenarios. CO-S01 to CO-S23, plus CO-S25 and CO-S26.
  - CO-S24 was removed in round 1 (M1) and its id is left unused.
  - CO-S25 and CO-S26 were added in round 1 (M2).
- Rules: G-01 to G-04 and CO-01 to CO-10.
  - CO-09 "No arrival time promised" was added in round 1 (M8).
  - CO-10 "No age limit" was added in round 2 (N10).

## Merges of step 3.9

None. The run started at step 4, so step 3.9 did not run and no rows were dropped. The checker's six merge-candidate WARNINGs (below) were left as they were.

## Input ledger, final state

Unchanged from the review packet:

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied, the rest proposed and confirmed with changes | interview round 2 Q3, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found (default accepted) | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases, no transcripts | interview round 2 Q4 |

Accepted default: a state-changing call is authorized only by the customer's explicit confirmation of the full proposal it executes, and any change voids it (round 1 Q4).

## Proposed tools

These are provisional:
- list_orders(), proposed.
- cancel_order(order_number), proposed.
- request_staff_followup(order_number, reason), proposed.
- issue_refund(order_number), supplied by the user.

Appendix A is the part of the spec that architecture notes may change. In round 1 the unsupported `failure_reason` field was removed from issue_refund's outcomes (M4). Round 3 added a reading rule for "before the user's confirmation turn" lines (P6).

## Checker

Final run:

```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S13, CO-S25: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S26 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S06, CO-S09 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S25, CO-S26 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01 |
| CO-10 | CO-S01 |
```

The checker printed "0 errors" on every run (4.1 before round 1, and after the fixes of rounds 1, 2 and 3).

## Findings

**35 findings: 20 Important, 15 Nit.** These are the final severities. The finders gave 21 Important and 14 Nit; the verifier lowered P4 to Nit.

By status:
- 25 fixed;
- 1 answered;
- 5 open;
- 4 dropped;
- 0 Pre-existing (the whole spec was in scope).

3 rounds were run.

| Round | Merged (finder count lines summed) | Important / Nit | Kept | Dropped | Fixed | Answered | Open |
|---|---|---|---|---|---|---|---|
| 1 | 17 (22) | 11 / 6 | 14 | 3 | 11 | 1 | 2 |
| 2 | 11 (11) | 5 / 6 | 10 | 1 | 8 | 0 | 2 |
| 3 | 7 (9) | 5 / 2 (final 4 / 3) | 7 | 0 | 6 | 0 | 1 |

Each finding, verbatim, with its verifier line and decision, is in round1-findings.md, round2-findings.md and round3-findings.md.

**Round 1.**
- Fixed:
  - M1: impossible injected outcomes. CO-S17 row 3 was removed, and CO-S24 was removed.
  - M2: the second cancel timeout now re-reads and branches. CO-S15 was extended, and CO-S25 and CO-S26 were added.
  - M3: case 3 now uses the confirmed wording "not confirmed yet".
  - M4: `failure_reason` was dropped.
  - M5: dimension "Order choice asked".
  - M7: CO-S03 row 4, a "yes" with a change in the same turn.
  - M8: CO-09 and dimension "No arrival time promised".
  - M12: refund timeouts are tied to the nth call.
  - M14: "Refund terms explained".
  - M15: Turn 2 triggers.
  - M17: both halves of CO-03.
- Answered: M11, a wrong refund amount. No input defines it, and Appendix A carries the amount through the order.
- Open: M10, M16.
- Dropped: M6, M9, M13.

**Round 2.**
- Fixed:
  - N2: retry clause narrowed.
  - N3: CO-S06 Illustrates.
  - N4: ten Forbidden lines rewritten as "with no CO-A1 between".
  - N5: "Refund not confirmed reported" (the second instance).
  - N6: "proposal" in two dimensions.
  - N7: failure causes in reference results.
  - N8: CO-S19 absence line.
  - N10: CO-10 and an old order in CO-S01 row 3.
- Open: N1, N11.
- Dropped: N9.

**Round 3.**
- Fixed:
  - P1: the relaxation of "Refund not confirmed reported" was narrowed.
  - P3: the items row now matches CO-03.
  - P4: vague timing in "No arrival time promised".
  - P5: near-match order in "Order not found reported".
  - P6: confirmation-turn anchor when no confirmation turn happens.
  - P7: "cannot be or was not cancelled".
- Open: P2.

The round-3 fixes were not reviewed again, because round 3 is the cap.

**Attribution.** A kept finding counts as fix-introduced when the line it quotes is in the previous round's snapshot but not in the one before. This was checked with the saved round copies.
- Round 2: 10 kept.
  - 3 quote a line round 1 changed: N2, N5, N6.
  - 7 quote a line it did not change: N1, N3, N4, N7, N8, N10, N11.
  - N7 quotes an unchanged Initial-state line, but the defect it names was created by the M4 fix.
- Round 3: 7 kept.
  - 2 quote a line round 2 changed: P1, P2. Both quote the N5 and N2 fixes.
  - 5 quote a line it did not change: P3, P4, P5, P6, P7.
  - P3 quotes a row that round 1 changed (M17) and round 2 missed.

**Verifier drop rate: 4 of 21 Important findings verified were dropped.** In each case I read the quoted clause and agreed:
- M6, Not real: "CO-S19's 'Refund status reported' reads: 'The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it.' That is the known-failure-case-3 scenario … The coverage map needs a scenario that asserts the clause, not one in every success scenario."
- M9, Not real: "G-03 says 'Otherwise it tells the customer the action was not done', and in CO-S14 and CO-S15 the agent knows it made no CO-A3, so G-03 requires telling the customer the refund was not done."
- M13, Not real: "CO-S11's Unambiguity note settles the timing: 'The status change is tied to the agent's first cancellation, so every earlier lookup sees processing; in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation'."
- N9, Not real: "CO-S06 (… 'CO-A2 at any point. / CO-A3 at any point. / CO-A4 at any point.') forbids a refund and a handoff for an already-cancelled order … The confirmed input ('An already cancelled order: the agent reports that and changes nothing') makes no distinction by refund status."

Two findings were verified but not dropped:
- P4: the verifier said "Not real". It was kept at Nit, because the refutation relies on the Scope must-not line, which the rubric judge never reads.
- N5: the verifier refuted one of its two instances (CO-S15 row 2, citing SG-04's late effect), and I agreed. The other instance was fixed.

## Open questions

- What if issue_refund reports OrderNotCancelled? A correct agent refunds only an order the system returned or showed as cancelled, so no consistent scenario reaches this outcome. The failure row also tells the agent to say "the order is cancelled" right after the system said it is not (M1).
- What if cancel_order reports OrderNotFound for an order the lookup just returned? The failure row exists but now has no scenario (M1).
- What if the customer names no order and exactly one order is open? Is proposing that order a guess under the must-not "guess which order the customer means" (M10)?
- What if the customer names no order and no order is open? No row says how the agent answers (N11).
- What if CO-07's "tells the customer store staff will follow up once the order system has created the task" is meant as timing? This is a proposed rule change, not applied:
  - before: "…and tells the customer store staff will follow up once the order system has created the task."
  - after: "…and, only after the order system has returned the task, tells the customer store staff will follow up." (M16)
- What if G-04's guarantee clause covers SG-04 and so licenses a blind cancel resend? It also does not name SG-03, which the handoff retry relies on. This is a proposed rule change, not applied:
  - before: "…or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
  - after: "…or, for CO-A3 and CO-A4 only, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01 and SG-03)." (N1)
- What if, after a first refund call that timed out, a lookup shows the refund failed? Should the agent still retry, as "retries once, then re-reads" says, or stop and hand off, as "none on a terminal one" says? No scenario can pin either answer while a blind retry is allowed (P2).

## What verification cannot catch

Only the user can confirm two things:
- whether these rules are Harbor Goods' real cancellation and refund rules;
- whether the stakeholder list (the customer, the order system, store staff, Harbor Goods, the support team, other customers) is complete.

## Proposed checklist lines

These are for kept findings whose pattern no checklist names:
- Use-case checklist, Contract: "A confirmed input that removes a constraint ('no time limit', 'no fee') becomes a rule, and one scenario sits on the far side of the constraint an agent might invent." (N10)
- Use-case checklist, Failure handling: "A retry bound limits the number of commit calls; it never drops the re-read branches of the user's recovery procedure after the last allowed attempt." (M2)
- Evaluation checklist, Forbidden lines: "An ordering line anchored on an event that may never occur ('before a lookup made after X', 'before the confirmation turn') says how it reads when that event never occurs." (N4, P6)
- Evaluation checklist, Graders: "When the inputs fix what the agent must say in a case, the dimension for that case requires that claim and accepts no stronger claim the scenario's results do not show." (M3, P1)
- Evaluation checklist, Graders: "A rubric dimension that turns on 'proposal' or 'offer' says what counts as one, given what Scope lets the agent tell the customer." (N6)

## Interview

None ran. This was a verification-only run that started at step 4, and no questions were asked.
