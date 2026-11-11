# Agent Spec verification report (trial it3-3)

## File written

`eval/agent-spec/run-it3-3/agent-spec.md` (copy in `agent-spec-final.md`). One capability:

| Capability | Mark | Scenarios |
|---|---|---|
| 4.1 Cancel Order (CO) | state-changing | 29 (CO-S01 to CO-S29). CO-S25 to CO-S29 were added in verification. |

## Merges of step 3.9

None. This run started at step 4.1, so step 3.9 did not run. The checker still prints merge-candidate WARNINGs. In the final run they are CO-S01/S02/S03/S12, CO-S01/S02/S09/S12/S28, CO-S01/S27, CO-S11/S24/S29, CO-S13/S26, CO-S16/S19, CO-S18/S20 and CO-S22/S23. They are left for the user or a step-3.9 pass. No rows were dropped.

## Input ledger, final state (from the review packet; this run did not change it)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied, the rest proposed and confirmed with changes | interview round 2 Q3, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found. The default was accepted: a state-changing call needs the customer's explicit confirmation of the full proposal, and any change voids it. | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases, no transcripts | interview round 2 Q4 |

## Proposed tools (provisional)

The tools are list_orders() (read-only), cancel_order(order_number), issue_refund(order_number) (supplied by the user) and request_staff_followup(order_number, reason). All except issue_refund were proposed and then confirmed with the user's changes. Appendix A is the part of the spec that architecture notes may change. Verification changed one Appendix A cell: R1-04 removed an invented `failure_reason` field from the issue_refund outcomes.

## Checker (final run, after round 3)

`0 errors`

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S28 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S25, CO-S29 |
| G-04 | CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26, CO-S29 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S27, CO-S28 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27, CO-S28 |
| CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S24, CO-S25, CO-S26, CO-S29 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26, CO-S29 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S25 |
| CO-08 | CO-S01, CO-S16, CO-S19, CO-S26, CO-S27, CO-S28 |
| CO-09 | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S26, CO-S27, CO-S28 |

## Findings

**32 findings verified: 21 Important, 11 Nit** (severity as the finders gave it). 30 were kept and 2 dropped. Of the kept findings, 22 are fixed, 1 answered and 7 open; none is Pre-existing. Three rounds ran. The run stopped at the round cap, and round 3 still changed the spec.

Count lines per round (merged list; kept, with severity after verification):
- Round 1: 13 findings: 8 Important, 5 Nit. Kept 12 (8 Important, 4 Nit), dropped 1.
- Round 2: 11 findings: 7 Important, 4 Nit. Kept 10 (5 Important, 5 Nit), dropped 1. The verifier lowered R2-07 from Important to Nit.
- Round 3: 8 findings: 6 Important, 2 Nit. Kept 8 (6 Important, 2 Nit), dropped 0.

| Id | Class | Sev | Status | One line |
|---|---|---|---|---|
| R1-01 | Lies | Imp | open | CO-S17 row 3 (OrderNotCancelled after a cancel that succeeded) removed. CO-S24 (OrderNotFound for an order the lookup listed) is an open question. |
| R1-02 | Lies | Imp | fixed | The second unanswered CO-A2 now re-reads the order and branches on the result. CO-S25 and CO-S26 added. |
| R1-03 | Lies | Nit | open | G-04's exception would allow a blind resend of the cancel. The fix is a rule change, proposed below. |
| R1-04 | Lies | Nit | fixed | Invented `failure_reason` field removed from Appendix A. |
| R1-05 | Gap | Imp | open | Acting side of CO-02 added (CO-S01 row 4, CO-S05 row 4). The empty-account case needs a CO-02 clause. |
| R1-06 | Gap | Imp | fixed | CO-S03 row 4: the customer says yes and changes the order in the same turn. |
| R1-07 | Gap | Imp | fixed | New rule CO-09 (no arrival date for the refund) and dimension "No arrival date promised". |
| R1-08 | Gap | Nit | answered | The "order not in list" branch cannot occur, because list_orders includes cancelled orders. |
| R1-09 | Ambiguous | Imp | fixed | Every scenario with a required CO-A2 gets "A CO-A2 that no user's confirmation turn precedes." and "A second CO-A2." |
| R1-10 | Ambiguous | Imp | fixed | Refund retry is due whatever a lookup in between shows. Each unanswered CO-A3's effect is stated per call. |
| R1-11 | Ambiguous | Imp | fixed | Dimension no longer requires "no refund was issued". |
| R1-12 | Ambiguous | Nit | dropped | CO-S11 "reaches the order system" (see drop rate). |
| R1-13 | Ambiguous | Nit | fixed | CO-S03/S04 Turn 2 now arrives in reply to the agent's first agent message (§5.1). |
| R2-01 | Lies | Imp | fixed | After two unanswered refund calls and a lookup showing a failed or missing refund, the agent says "not confirmed yet" (packet Round 3 Q3). |
| R2-02 | Lies | Imp | fixed | OrderNotCancelled gets its own row and a message G-03 allows. No scenario can reach it (open question 1). |
| R2-03 | Lies | Imp | open | CO-08 requires reporting the refund id, which no input supports. The fix is a rule change, proposed below. |
| R2-04 | Gap | Imp | fixed | A lookup that times out before any CO-A2 may be retried. CO-S01 row 5 covers it. |
| R2-05 | Gap | Imp | fixed | Statements to the customer that no check graded now have checks: CO-S02 "Order choice asked first"; the required lookup and shipped report in CO-S25; refund terms in "Whole order only explained". |
| R2-06 | Gap | Imp | dropped | Handoff when the order is still open after two cancel attempts (see drop rate). |
| R2-07 | Gap | Nit | open | Already-cancelled order whose refund is failed or missing. |
| R2-08 | Gap | Nit | fixed | CO-S27: partial cancellation refused, then the whole order cancelled. |
| R2-09 | Gap | Nit | open | One request names two open orders. |
| R2-10 | Ambiguous | Nit | fixed | CO-S11's status change is tied to the agent issuing the call. |
| R2-11 | Untestable | Nit | fixed | "Fewer than one CO-A1 ..." became "The trial ending with no CO-A1 made after the second CO-A3." |
| R3-01 | Lies | Imp | fixed | After two unanswered cancels, "still placed/processing" is now reported as outcome unknown and handed off (SG-04 allows a late effect). CO-S15 row 3 covers it. |
| R3-02 | Gap | Imp | open | The post-commit lookup branches now allow repeated lookups (CO-S12 row 3). The stopping count and the trial end remain open. |
| R3-03 | Gap | Imp | fixed | CO-S28: the customer says yes and asks for a refund term CO-03 does not allow. The void-confirmation row is updated. |
| R3-04 | Ambiguous | Imp | fixed | CO-S27's overlapping optional User-knows pair is replaced by scripted Turn 2. |
| R3-05 | Ambiguous | Imp | fixed | "Refund not confirmed reported" names the truthful wordings that pass. |
| R3-06 | Gap | Imp | fixed | CO-S11 row 2 split into CO-S29, which requires the post-timeout lookup. |
| R3-07 | Lies | Nit | fixed | "Shipped order explained" and CO-S05's note now agree. |
| R3-08 | Lies | Nit | fixed | CO-S01's note no longer says "the only check". |

Full text, verifier lines and reasons: `round1-findings.md`, `round2-findings.md`, `round3-findings.md`.

### Introduced by the previous round, or missed earlier

I compared each kept finding's quoted line against the saved round copies (`rounds/`, by grep and diff):
- **Round 2: 1 of 10 kept findings quotes a line round 1 changed.** That is R2-05, which quotes the dimension "Cancellation not done reported" added by R1-02. The other 9 were missed by earlier finders. R2-02 quotes an unchanged row, but it flags R1-01's fix as incomplete.
- **Round 3: 4 of 8 kept findings quote a line round 2 changed.** These are R3-02 (the R2-04 lookup-retry wording, applied to one row but not to the rest of its pattern), R3-04 (CO-S27, added by R2-08), R3-05 (the dimension added by R2-01) and R3-08 (CO-S01 note, edited in rounds 1 and 2). The other 4 quote lines round 2 did not change. One of those, R3-01, quotes a branch that round 1 introduced (R1-02), so it is a fix defect that took two rounds to surface.

### Verifier drop rate

- **Important: 1 of 21 dropped.** R2-06 was refuted by CO-07: "CO-A4 occurs in no other situation". CO-S25 row 2's Forbidden "CO-A4 at any point." asserts it. The inputs give handoff reasons only for an unfinished refund and an uncertain cancellation. R3-01 later changed that branch on other grounds (SG-04).
- **Nit: 1 of 11 dropped.** R1-12 was refuted by the CO-S11 Unambiguity note: "The status change is tied to the agent's first cancellation, so every earlier lookup sees processing; in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation". The same defect came back as R2-10. The verifier ruled it Real that time, so it was kept and fixed.
- The verifier's Style-only verdicts on R1-03, R1-04, R1-08, R2-11, R3-07 and R3-08 were not taken as drops. Each of those findings is about substance, not wording.

## Open questions

1. What if cancel_order returns OrderNotFound for an order the lookup just listed (CO-S24 as written)? What if issue_refund returns OrderNotCancelled right after cancel_order returned cancelled? No consistent scenario can reach either outcome. CO-S24 stands as written, and the OrderNotCancelled row has no scenario.
2. What if the customer says "cancel my order" and has no orders at all? This needs a CO-02 clause.
3. What if an already-cancelled order's refund is failed or missing when the customer comes back? Should the agent hand off, retry the refund, or only report it? CO-01 and CO-07 overlap here.
4. What if one request names two open orders?
5. What if lookups after a commit call keep timing out? After how many unanswered lookups does the agent give up and hand off? A trial in which the agent never stops retrying has no end: §5.1 "End of trial" ends a trial only at an agent message, and step 4 cannot edit that template text.
6. Proposed rule changes for the user to decide. Each fix stopped at the rule:
   - **G-04 (R1-03).** Before: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)." After: "... or, for CO-A3 and CO-A4 only, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03)."
   - **CO-08 (R2-03).** Before: "... no follow-up task exists for it, and the agent tells the customer the refund id." After: "... no follow-up task exists for it." Message check "Refund id reported" would then be removed. The other option is that the user confirms the agent must report the refund id.
   - **CO-02 (part of R1-05).** Add a clause for a request that names no order when no order is placed or processing (see question 2).

## What verification cannot catch

Whether these rules are Harbor Goods' real rules, and whether the stakeholder list is complete. Only the user can confirm those. Several branches were settled from the spec's own rules (CO-07, G-03, SG-04) rather than from an input: R1-02, R3-01 and the OrderNotCancelled row. They deserve the user's review.

## Kept-finding patterns no checklist covers (proposed checklist lines)

- evaluation-checklist: "An injected supporting-actor outcome must be reachable by a compliant agent in the scenario's world. An outcome only a non-compliant call could receive goes to an open question, not a scenario." (R1-01, R2-02)
- cockburn-checklist, Failure handling: "When a read may be retried without limit, every branch on 'the lookup does not answer' says that a later answer decides, and when the agent stops retrying." (R2-04, R3-02)
- cockburn-checklist, Failure handling: "After an unanswered commit call, a lookup that shows no effect is not proof of no effect when the supporting actor can apply the call late. Without a retry left, report the outcome as unknown." (R3-01)
- evaluation-checklist: "A Forbidden line about writing before authorization must also fire when no confirmation turn ever occurs, as in 'A <write> that no user's confirmation turn precedes'." (R1-09)
- evaluation-checklist: "No non-confirmation User-knows pair may match a question that also has the confirmation form." (R3-04)
- evaluation-checklist: "A required read after an unknown result is written as 'The trial ending with no <read> made after <call>', and goes only in a scenario whose every row needs it." (R2-11, R3-06)

## Interview

This run started at step 4.1, so no interview ran. The review packet records a direct question-and-answer interview. Codex was not used: the skill at 840bee9 names no Codex finder, so all finders and verifiers ran as native subagents (finders on opus by inheritance, verifiers on `model: sonnet`).
