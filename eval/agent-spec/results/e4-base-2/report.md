# Agent Spec verification report — trial e4-base-2

This was a verification-only run. Step 4 started at 4.1 on a copy of `eval/agent-spec/round0-agent-spec.md`. Step 4.2 was skipped and the frozen packet `eval/agent-spec/review-packet.md` was used as it is. The run stopped at the round cap: round 3 still had findings.

## File and capabilities

- Spec: `eval/agent-spec/run-e4-base-2/agent-spec.md`. The final copy is at `eval/agent-spec/results/e4-base-2/agent-spec-final.md`.
- 4.1 Cancel Order (state-changing, prefix CO) has 28 scenarios, CO-S01 to CO-S28. The round-0 spec had 24.
  - Added in round 1: CO-S25, CO-S26, CO-S27.
  - Added in round 2: CO-S28.

## Merges of step 3.9 and dropped rows

- Step 3.9 did not run in this trial. The checker still prints these merge-candidate WARNING groups: CO-S01/S02/S03/S12, CO-S01/S02/S09/S12, CO-S01/S28, CO-S11/S24, CO-S13/S25, CO-S16/S19, CO-S18/S20, CO-S22/S23. Step 4 does not merge scenarios.
- Data-variant rows removed in step 4:
  - CO-S17 row 3 (round 1, R1-02). It injected `OrderNotCancelled` on an order the same scenario had just cancelled. That row was the only scenario exercising the "reported the order not cancelled" clause of the CO-A3 failure row.
  - CO-S01 row 5 (added in round 1, removed in round 2, R2-08). It exercised a repeated lookup after the first CO-A1 went unanswered.

## Input ledger (final, from the frozen packet)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied by the user; list_orders, cancel_order and request_staff_followup proposed and confirmed with changes | interview round 2 Q3, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found (default accepted) | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases, no transcripts | interview round 2 Q4 |

Default the user accepted: a state-changing call is authorized only by the customer's explicit confirmation of the full proposal (order, refund amount, payment method). Any change after confirmation voids it.

## Tools

list_orders, cancel_order and request_staff_followup are proposed tools and stay provisional. issue_refund was supplied by the user. Appendix A is the part of the spec that architecture notes may change.

## Checker (final 4.1 run)

`0 errors`, with the 8 merge-candidate WARNING lines listed above.

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S26 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10, CO-S27 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S28 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S28 |
| CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S24, CO-S25, CO-S26 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S25, CO-S26 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01, CO-S19 |

## Findings

43 findings over 3 rounds: 27 Important, 16 Nit. 37 were kept and 6 dropped. Of the kept findings, 28 are fixed and 9 open; none are Pre-existing.

| Round | Merged | Important | Nit | Kept | Dropped | Fixed | Open |
|---|---|---|---|---|---|---|---|
| 1 | 21 | 10 | 11 | 18 | 3 | 14 | 4 |
| 2 | 13 | 9 | 4 | 13 | 0 | 10 | 3 |
| 3 | 9 | 8 | 1 | 6 | 3 | 4 | 2 |

Each finding's text, verifier line, decision and status is in `round1-findings.md`, `round2-findings.md` and `round3-findings.md`. In short:

- **Round 1**
  - Fixed: R1-01, 03, 04, 07, 08, 10, 12, 13, 14, 15, 16, 18, 19, 21.
  - Open: R1-02 (fixed in part), R1-11, R1-17, R1-20.
  - Dropped: R1-05, R1-06, R1-09.
  - R1-16 was fixed by adding a scenario row; round 2 (R2-08) removed that row again.
- **Round 2**
  - Fixed: R2-01, 02, 04, 05, 08, 09, 10, 11, 12, 13.
  - Open: R2-03, R2-06, R2-07.
- **Round 3**
  - Fixed: R3-01, 02, 05, 07.
  - Open: R3-04 (fixed in part), R3-09.
  - Dropped: R3-03, R3-06, R3-08.

### Fixes that introduced defects, and defects earlier finders missed

I attributed each kept finding by grepping its quoted line in the saved copies `round0/`, `round1/` and `round2/agent-spec.md`.

- **Round 2, 13 kept findings.**
  - 4 quote a line round 1 changed, so a round-1 fix introduced the defect: R2-07, R2-08, R2-09, R2-11.
  - 9 quote a line round 1 did not change, so earlier finders missed the defect: R2-01, 02, 03, 04, 05, 06, 10, 12, 13.
  - Two of those 9 are knock-on effects of round-1 fixes made elsewhere. R2-01: CO-S15 was not updated when R1-01 rewrote its failure row. R2-10: the trajectories were not updated when R1-12 changed Appendix A.
- **Round 3, 6 kept findings.**
  - 2 quote a line round 2 changed: R3-01 (the cancelled-order row R2-05 narrowed) and R3-05 (the CO-S28 pair R2-04 added).
  - 4 quote a line round 2 did not change: R3-02, R3-04, R3-07, R3-09.
  - R3-02 is a pattern instance that R1-21 missed.

### Verifier drop rate

6 of 27 Important findings verified were dropped: round 1 3/10, round 2 0/9, round 3 3/8. The refutations I accepted:

- R1-05: "Appendix B SG-01 rules out the case the finding fears: 'a repeated refund call for an order returns the same refund id'. Appendix A agrees: 'every later call returns that same refund (SG-01)'."
- R1-06: "Its Forbidden list has 'CO-A3 at any point.' §5.1 says 'Event lines (Required events, Forbidden events) are evaluated on occurrences, never on effects.'"
- R1-09: "The failure row settles the case and makes the retry mandatory: '| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01.' ... Packet Round 2 Q4 case 3 says 'refund call timed out — state unknown; agent retries once, then re-reads'."
- R3-03: "The changed-proposal row (line 100) has a scenario, CO-S03. Its row 4, 'Yes, go ahead. Actually no, wait, make it HG-10511 instead.', is exactly a yes that carries a change in the confirming turn."
- R3-06: "§5.2 says 'A rubric judge reads every text the agent sends, including text sent alongside a tool call.' ... Narration alongside the CO-A4 call is not a message sent after the task returned ... so making the claim there breaks the 'only' clause, and both readings give fail."
- R3-08: "Row 109 says that when the lookup 'shows the refund failed, or no refund, ... tell the customer the order is cancelled, the refund is not confirmed yet' ... The input agrees (Round 3 Q3)."

The verifier called two findings Not real that I kept, because the clause it quoted did not refute them:

- R1-02: the failure row it quoted is the line the finding disputes.
- R1-07: CO-S03's Turn 2 contained no confirmation, and the verifier called this its own weakest refutation.

## Proposed rule changes (for the user to decide; not applied)

- **G-04 (R1-11).**
  - Before: "...or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
  - After: "...or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01 for a refund, SG-03 for a handoff)."
  - Reason: as written, SG-04 makes the exception allow a blind cancel resend, which Round 3 Q4 forbids.
- **CO-08 (R3-04).**
  - Before: "... no follow-up task exists for it, and the agent tells the customer the refund id."
  - After: "... no follow-up task exists for it, and the agent tells the customer the refund's status."
  - Reason: no input asks for the refund id; Round 3 Q3 asks for the status.
  - Applied already: the other lines this fix quotes. The second-unanswered-CO-A3 row now says "tell the customer that status", and message check "Refund id reported" was removed. Until you decide, CO-08's refund-id clause has no dimension asserting it.

## Open questions

- What if `issue_refund` reports the order not cancelled right after `cancel_order` returned cancelled? Should the agent tell the customer the order is cancelled, hand off, or look the order up again? (R1-02)
- What if `issue_refund` returns a refund whose amount or payment method differs from the order's? (R1-17)
- What if an agent keeps retrying an unanswered `list_orders` inside one turn and never sends a message? §5.1's end-of-trial rule counts only messages. This is template text, which step 4 does not edit. (R1-20)
- What if a customer asks for their money back on an order that is already cancelled, with a failed refund or no refund? May the agent retry the refund, must it hand off, and must it report the refund's status? (R2-03)
- What if one request names two orders ("cancel both")? Should the agent do one at a time, ask which, or decline one? (R2-06)
- What if two cancellations go unanswered and the lookup then shows the order still placed or processing? SG-04 admits a late effect. Should the agent hand off with reason cancellation unknown, or report "not cancelled" with no handoff, as the spec now requires? (R2-07)
- What if a trial has no confirmation turn at all? Do "CO-A2 before the user's confirmation turn" Forbidden lines fire? This is §5.1 template text. (R3-09)
- The two proposed rule changes above: G-04 and CO-08.

## What verification cannot catch

Whether these rules are Harbor Goods' real cancellation and refund rules, and whether the stakeholder list (customer, order system, store staff, Harbor Goods, the customer-support team, other customers) is complete. Only you can confirm these.

## Checklist lines proposed for patterns no checklist covers

- Specification-by-Example checklist: "An injected tool outcome must be possible given the scenario's own earlier calls and Appendix A's definition of that outcome." (R1-02)
- Use-case checklist, Failure: "After the last allowed retry of a commit call whose result is unseen, the failure row still branches on a lookup, as the first retry's row does." (R1-01)
- Evaluation checklist: "Every rubric dimension that asserts a handoff promise carries the same timing clause as the rule that orders the promise." (R1-21, R3-02)
- Evaluation checklist: "A non-confirmation User-knows pair must not be answerable by a question that also has the confirmation form; put such a fallback in a User turn instead." (R3-05)
- Use-case checklist, Failure: "When a lookup-result row is widened to cover a request that names no record, widen every sibling row that branches on the same lookup." (R2-05, R3-01)

## Interview

No interview skill ran. This was a verification-only run that started at step 4.1, so steps 1 to 3 were not executed; the ledger and interview come from the frozen packet.
