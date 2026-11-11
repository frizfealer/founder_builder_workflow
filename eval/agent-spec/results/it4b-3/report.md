# Agent Spec report: Harbor Goods order-support agent (trial it4b-3)

## File written

`eval/agent-spec/run-it4b-3/agent-spec.md` (copied to `results/it4b-3/agent-spec-final.md`). This was a verification-only run: it started at step 4.1 on the round-0 spec and ran step 4 to its round cap.

| Capability | Mark | Scenarios |
|---|---|---|
| 4.1 Cancel Order (CO) | state-changing | 29 (CO-S01 to CO-S29) |

Verification added CO-S25 to CO-S29 and added data-variant rows to CO-S01 (rows 4, 5), CO-S03 (row 4), CO-S04 (row 4), CO-S05 (row 4) and CO-S06 (row 3).

## Merges (step 3.9)

None. The run started at step 4.1, and step 3.9 is outside step 4. The checker still prints these merge-candidate WARNING groups, none of which was acted on: CO-S01/S02/S03/S12; CO-S01/S02/S09/S12/S28; CO-S01/S29; CO-S11/S24; CO-S13/S25; CO-S16/S19; CO-S18/S20; CO-S22/S23; CO-S26/S27. No rows were dropped.

## Input ledger (final, from the review packet)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied by the user; the rest proposed and confirmed with changes | interview round 2 Q3, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found (default accepted) | round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases, no transcripts | round 2 Q4 |

The user accepted one default (round 1 Q4): the agent cancels only after the customer explicitly confirms the full proposal (order, refund amount and destination), and any change after confirmation voids that confirmation.

## Tools (Appendix A is provisional)

- `list_orders()`: read-only, proposed
- `cancel_order(order_number)`: proposed
- `request_staff_followup(order_number, reason)`: proposed
- `issue_refund(order_number)`: supplied by the user

Each proposed tool was confirmed with the user's changes. Appendix A is the part of the spec that architecture notes may change. Verification changed one cell in it: the invented `failure_reason` field was removed from the CO-A3 outcomes (R1-03).

## Checker (final run)

```
0 errors
```

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S28 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S26, CO-S27 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26, CO-S27 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S28, CO-S29 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S28, CO-S29 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S24, CO-S25, CO-S27 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26, CO-S27 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S26 |
| CO-08 | CO-S01, CO-S16, CO-S19 |

## Findings

**42 findings verified: 24 Important, 18 Nit. 35 kept (22 Important, 13 Nit); 7 dropped (2 Important, 5 Nit). Of the kept findings, 28 are fixed and 7 open, 0 were answered with a reason, and 0 are Pre-existing. 3 rounds ran; the run stopped at the round cap.**

Per round, as merged, kept and dropped:
- Round 1: 18 merged (9 Important, 9 Nit), 14 kept, 4 dropped.
- Round 2: 15 merged (9 Important, 6 Nit), 12 kept, 3 dropped.
- Round 3: 9 merged (6 Important, 3 Nit), 9 kept, 0 dropped.

The finders' own count lines summed to 20, 16 and 9 before duplicates were merged. Each finding's full text, the verifier's line and the decision are in `round<N>-findings.md`.

### Status of each finding

**Round 1**
- **Fixed:**
  - R1-02: refund "not confirmed yet" wording.
  - R1-03: invented `failure_reason`.
  - R1-04: no-date promise was unchecked.
  - R1-05: change inside the confirming turn; a question in reply.
  - R1-06: second unanswered CO-A2 now branches on the lookup.
  - R1-07: success-path refund status was unchecked.
  - R1-08: CO-S02 passed a guessed proposal.
  - R1-10: the result of a lookup between two unanswered CO-A3 was undefined.
  - R1-12: one open order with an unnamed request.
  - R1-13: unnamed request with no open order.
  - R1-15: Turn 2 trigger was undefined.
  - R1-16: "Shipped order explained" wording.
- **Open:**
  - R1-01: injected OrderNotCancelled / OrderNotFound contradict the scenario.
  - R1-11: CO-03 rule-text change, proposed.
- **Dropped:** R1-09, R1-14, R1-17, R1-18.

**Round 2**
- **Fixed:**
  - R2-01: CO-S15 lookup.
  - R2-03: already cancelled with a failed refund.
  - R2-04: a fixed refund term changed in the confirming turn.
  - R2-06: no-date clause off the success path.
  - R2-08: "Which order asked first" anchor.
  - R2-09: CO-S09 "total paid".
  - R2-10: CO-S06 Illustrates.
  - R2-11: partial request, then the whole order.
- **Open:**
  - R2-02: is a lookup after a timed-out cancel final?
  - R2-05: two orders in one request.
  - R2-12: an unanswered re-check after confirmation.
  - R2-13: §5.1 anchor with no confirmation turn, which is template text.
- **Dropped:** R2-07, R2-14, R2-15.

**Round 3**
- **Fixed:**
  - R3-01: remaining no-date gaps.
  - R3-03: CO-S03 pair scope.
  - R3-04: CO-S29 pair conflict.
  - R3-05: negative rubric clauses over mid-run text.
  - R3-06: "not confirmed yet" against a true "failed".
  - R3-07: "no time limit" scenario.
  - R3-08: per-order clause.
  - R3-09: "Orders unavailable" anchor.
- **Open:**
  - R3-02: a read that fails once, then answers.

### Rule changes proposed, not applied (rule-text stop)

**CO-03 (R1-11)**

- Before: "Every proposal cancels the whole order and refunds its total paid to its payment method, with no fee and no store credit. When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
- After: "Every proposal cancels the whole order and refunds its total paid to its payment method, with no fee and no store credit. When the customer asks to cancel only some items, the agent tells the customer only the whole order can be cancelled; when the customer asks for a different amount, a different payment method or store credit, the agent tells the customer the refund is the total paid to the order's payment method. In both cases it proposes nothing else."

**CO-07 (R2-03, part b)**

- Before: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation."
- After: "When the agent cancelled the order in this conversation but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether its cancellation took effect, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation; for an order cancelled before the conversation the agent makes no CO-A4."

CO-S06 row 3 already forbids CO-A4. That follows the confirmed shared-understanding item, "An already cancelled order: the agent reports that and changes nothing."

### Kept findings in rounds 2 and 3, split by what they quote

This split compares each finding's quoted line with the saved round copies (`round<N-1>` against `round<N-2>`).

**Round 2: 12 kept.**
- 2 quote a line that round 1 changed, so a round-1 fix introduced the defect:
  - R2-02: CO-S26, from the R1-06 fix.
  - R2-08: "Which order asked first", from the R1-08 fix.
- 10 quote a line round 1 did not change, so these are defects earlier finders missed.
- Two of those 10 still stem from incomplete round-1 fixes:
  - R2-01: CO-S15 was left without the lookup that the rewritten R1-06 row requires.
  - R2-06: the R1-04 no-date clause reached only the success dimensions.

**Round 3: 9 kept.**
- 2 quote a line that round 2 changed:
  - R3-04: the CO-S29 pairs, from the R2-11 fix.
  - R3-06: "Refund not confirmed reported", touched by the R2-06 fix and first written in R1-02.
- 7 quote lines round 2 did not change.
- One of those 7 is an incomplete round-2 pattern fix: R3-01, the no-date clause again.

### Verifier drop rate

- **Important:** 2 dropped of 24 verified, 8%.
- **Nit:** 5 dropped of 18 verified, 28%.

**Refutations of the dropped findings**

- R1-09 (Important, Not real): "CO-S11's Unambiguity note says 'in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation'. The scenario's own lines can only hold together if the unanswered first CO-A2 reached the system: Required 'CO-A2 occurs exactly once' with Final state 'HG-10482 has status shipped'."
- R1-14 (Nit, Not real): "`issue_refund(order_number)` takes only the order number, and Appendix A carries the 'amount and payment method through the order'. The confirmed outcome list ... names no refund with a different amount or payment method."
- R1-17 (Nit, Style only): "'Fewer than one CO-A1 after the second CO-A3' can be computed as one count over the tool log. A run without that lookup already fails message check 'Refund id reported'."
  - The finding's own Quote, "Fewer than one CO-A1 after the second CO-A3.", is about how the line is phrased.
- R1-18 (Nit, Not real): "G-04's exception names its guarantee: '(Appendix B, SG-01)'. CO-06 says 'It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing'."
- R2-07 (Important, Not real): "§5.2 'Scenario pass' says 'A trial passes when ... every dimension the scenario uses passes' ... §2 line 9: the customer 'wants to be told truthfully whether the order was cancelled and where the refund stands' ... Round 2 Q4 case 3 adds 'Final message must match the final refund status'."
- R2-14 (Nit, Style only): "Each row's substituted line is one step that needs no rewording and is a plain state check ... The whole-sentence placeholder affects only step-definition reuse."
  - The finding's Quote is "- <refund final state>".
- R2-15 (Nit, Style only): this repeats R1-17. "Appendix A defines the count ... so the line can be computed from the tool log ... The finding concedes it 'decides no verdict'."

**Style only verdicts on Nits that were rejected (the findings were kept)**

These were about content, not wording:
- R1-03: a tool field that no input supplies.
- R1-15: a trigger that names an event §5.1 does not define.
- R2-10: a wrong rule id in Illustrates, which feeds the checker's coverage table.

## Open questions

- **What if** the order system answers CO-A3 with OrderNotCancelled right after CO-A2 returned the order cancelled? Or answers CO-A2 with OrderNotFound for an order the lookup just returned? When can these happen, and what does the agent tell the customer? (R1-01: CO-S17 row 3 and CO-S24 stand as written.)
- **What if** CO-03 is meant to require both statements in both cases, rather than one statement per case? (R1-11: the proposed CO-03 text above.)
- **What if** a cancel that timed out lands after a later lookup showed the order still open? SG-04's Covers line says this can happen.
  - After the second timed-out cancel, should the agent hand off as "cancellation unknown" instead of reporting "not cancelled"? (R2-02: CO-S26 assumes the lookup is final.)
- **What if** the customer names two orders, or asks to cancel "all my open orders"? Which order does the agent act on: one, both, or does it ask? (R2-05)
- **What if** the agent re-checks the order after confirmation, and that read goes unanswered? Does the confirmed cancellation still proceed? (R2-12)
- **What if** a scenario's anchoring confirmation turn never occurs? How is "before the user's confirmation turn" evaluated then? This is §5.1 fixed template text, which step 4 does not edit. (R2-13)
- **What if** a read times out once and then answers on retry? How many unanswered reads count as "the lookup does not answer" before the agent hands off or proposes nothing? (R3-02)
- **What if** an order was cancelled before the conversation and its refund is unfinished? Should CO-07's handoff apply? (R2-03 part b: the proposed CO-07 text above.)

## What verification cannot catch

Two things only the user can confirm:
- whether these rules are Harbor Goods' real business rules;
- whether the stakeholder list is complete.

The reviewers checked the spec against the review packet only.

## Checklist proposals (kept patterns no checklist covers)

- **evaluation-checklist.md:** "A User-knows confirmation pair for a value the user switches to in a later scripted turn is scoped (after Turn n), so a guessed proposal before the switch is not confirmed." (R3-03, R3-04)
- **evaluation-checklist.md:** "A rubric dimension's 'never says' clause is limited to the final message when a correct run says the forbidden thing mid-run, since the judge reads text sent alongside tool calls." (R3-05)
- **evaluation-checklist.md:** "A rubric dimension that asks for a hedged statement says whether a stronger statement that is also true meets it." (R3-06)
- **cockburn-checklist.md:** "A read the inputs make retriable has a row for a read that fails and then answers, and states how many failures count as 'no answer'." (R3-02)
- **cockburn-checklist.md:** "A lookup made after a timed-out commit is treated the same way everywhere: as final in the failure rows and scenarios, or as possibly stale in Appendix B, not both." (R2-02)
- **evaluation-checklist.md:** "A restriction on what the agent tells the user (such as no arrival date) is carried by a dimension in every scenario where the agent talks about that subject, not only on the success path." (R1-04, R2-06, R3-01)

## Interview

No interview ran in this trial. It started at step 4.1 from a fixed review packet, and the packet's interview record does not name an interview skill.
