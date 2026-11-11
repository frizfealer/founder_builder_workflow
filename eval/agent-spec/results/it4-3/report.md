# agent-spec verification report — it4-3

Verification-only run (step 4.1 onward) of the agent-spec skill at commit 58cdc2f, on `eval/agent-spec/run-it4-3/agent-spec.md` (copy of `eval/agent-spec/round0-agent-spec.md`). Reviewers got `eval/agent-spec/run-it4-3/review-packet.md`. Three rounds ran; the run stopped at the round cap with findings left.

## File and capabilities

- File: `eval/agent-spec/run-it4-3/agent-spec.md` (final copy: `agent-spec-final.md` here).
- 4.1 Cancel Order (state-changing, prefix CO): 29 scenarios, CO-S01 to CO-S29. Round 0 had 24; verification added CO-S25 and CO-S26 (round 1), CO-S27 and CO-S28 (round 2), CO-S29 (round 3). Rule CO-09 (no arrival date) was added in round 1.

## Merges (step 3.9) and dropped rows

- No step-3.9 merges: the run started at step 4.1. The checker's nine WARNING groups (identical Required events) were left as they are.
- Dropped data-variant row: CO-S17 row 3 ("is answered by the order system with the order not cancelled, and creates no refund"), removed in round 1 (R1-01). It exercised the CO-A3 failure row branch "reported the order not cancelled"; no scenario now exercises that branch (open question 1).
- Rows added: CO-S01 row 4 (unnamed request, one open order), CO-S03 row 4 (yes taken back in the same turn), CO-S06 rows 3 and 4 (already-cancelled order, refund failed / no refund).

## Input ledger (final, from the review packet)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied, the rest proposed and confirmed with changes | interview round 2 Q3, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found (default accepted) | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases, no transcripts | interview round 2 Q4 |

Default the user accepted: a state-changing call is authorized only by the customer's explicit confirmation of the full proposal it executes (order, refund amount, payment method), and any change after confirmation voids it.

## Tools

`list_orders()`, `cancel_order(order_number)` and `request_staff_followup(order_number, reason)` were proposed and are provisional; `issue_refund(order_number)` was supplied by the user. Appendix A is the part of the spec that architecture notes may change. Verification changed Appendix A in three places: the CO-A3 outcome no longer names a `failure_reason` field (R1-06), and two reading rules were added under "Which order an action is for" (R2-06: "<action> with no CO-A1 between <earlier action> and it"; R3-08: what "<action> occurs exactly n times, for <order>" counts).

## Checker

Final run: `0 errors`, with 9 WARNING merge-candidate groups (step 3.9 does not apply to this run). Coverage table:

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S27, CO-S29 |
| G-03 | CO-S01, CO-S06, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S26, CO-S28 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S27, CO-S29 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27, CO-S29 |
| CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S24, CO-S25, CO-S28 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26, CO-S28 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S26 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01, CO-S19 |

## Findings

**45 findings verified over 3 rounds: 33 Important, 12 Nit (merged, at finder severity). 39 kept (22 Important, 17 Nit at the verifier's severity where lower): 30 fixed, 9 open, 0 Pre-existing. 6 dropped.**

| Round | Finder count lines (raw) | Merged | Kept | Dropped | Fixed | Open |
|---|---|---|---|---|---|---|
| 1 | 21 (17 I, 4 N) | 17 (14 I, 3 N) | 15 | 2 | 12 | 3 |
| 2 | 18 (11 I, 7 N) | 16 (10 I, 6 N) | 14 | 2 | 8 | 6 |
| 3 | 12 (9 I, 3 N) | 12 (9 I, 3 N) | 10 | 2 | 9 | 1 |

Each finding, verbatim, with its verifier line and decision, is in `round1-findings.md`, `round2-findings.md` and `round3-findings.md`.

- Round 1. Fixed: R1-02, R1-04, R1-06, R1-07, R1-08, R1-09, R1-10, R1-11, R1-13, R1-15, R1-16, R1-17. Open: R1-01 (partly fixed), R1-05 (proposed rule change), R1-12. Dropped: R1-03, R1-14.
- Round 2. Fixed: R2-01, R2-02, R2-03, R2-04, R2-05, R2-06, R2-09, R2-13, R2-15. Open: R2-08, R2-10, R2-12, R2-14, R2-16. Dropped: R2-07, R2-11.
- Round 3. Fixed: R3-02, R3-03, R3-04, R3-05, R3-08, R3-09, R3-10, R3-11, R3-12. Open: R3-06. Dropped: R3-01, R3-07.

Attribution (diff of the saved round copies, `attribute.py`: a kept finding counts as "changed line" when a 12+ character piece of its Quote is in a line the previous round added):
- Round 2: 14 kept. 7 quote a line round 1 changed (a fix that introduced or left a defect: R2-01, R2-02, R2-03, R2-05, R2-13, R2-14, R2-15). 7 quote lines round 1 did not change (defects earlier finders missed: R2-04, R2-06, R2-08, R2-09, R2-10, R2-12, R2-16). R2-06 and R2-09 were partly set off by round-1 fixes, although their quotes are older lines.
- Round 3: 10 kept. 1 quotes a line round 2 changed (R3-09). 9 quote lines round 2 did not change (R3-02, R3-03, R3-04, R3-05, R3-06, R3-08, R3-10, R3-11, R3-12). R3-10 quotes a round-1 line.

Verifier drop rate: Important 5 of 33 (15%), Nit 1 of 12 (8%). Each dropped finding's refutation, quoted:
- R1-03 (Important; verifier Not real): "CO-06 settles the whole case: 'It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing.' The Forbidden lines enforce it: CO-S12 'A second CO-A2' and CO-S13 'A second CO-A2 before a CO-A1 made after the first CO-A2'."
- R1-14 (Important; Not real): "Failure row 102 settles the whole case: its 'Required behavior' for 'the order system... did not answer [the first CO-A3]' is 'Make CO-A3 once more, relying on SG-01'. The row has no lookup condition, so the second CO-A3 is required whatever a lookup shows."
- R2-07 (Important; Not real): "The CO-S11 Unambiguity note settles it: 'in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation'. Final state for both rows also says 'HG-10482 has status shipped and no refund'."
- R2-11 (Nit; Not real): "§5.2 Interaction metrics computes precision for CO-S01 ... 'never folded into the score'. ... The evaluation checklist says to report precision 'to catch over-asking, but do not score on it, since a reasonable extra question is not a failure'."
- R3-01 (Important; Not real): "G-04 does not say that its exception list is closed. Its condition is general: 'or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)'. SG-03 is that kind of guarantee."
- R3-07 (Important; Not real): "'Order numbers and refund ids compare case-insensitively.' ... §5.1 says 'A supporting actor answers every call normally unless an Initial-state line says otherwise', and CO-S01 has no such line, so cancel_order and issue_refund on 'hg-10530' return cancelled and the refund."

Five Style only verdicts on Nits were not taken as drops (R1-06, R1-17, R2-09, R3-11, R3-12). Each finding is about content, not wording: a field the inputs do not define, an undefined trigger, a tool result the tool cannot return, a value with no column, and a Forbidden line that is not an event. All five were fixed.

Proposed rule changes, not applied (step 4.5 stops at a rule's text):
- CO-08 (R1-05). Before: "...no follow-up task exists for it, and the agent tells the customer the refund id." After: "...no follow-up task exists for it, and the agent tells the customer the refund's status." No input asks for the refund id. The message check "Refund id reported" stands with the rule until the user decides.
- CO-07 (R1-07, R2-14). Before: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, ..." After: "When an order cancelled in this conversation has a refund that is not shown pending or issued after the retries CO-06 allows, ...". As written, the rule reaches an order that was already cancelled before the conversation, which the input says the agent leaves unchanged.

## Open questions

1. What if `issue_refund` reports OrderNotCancelled, or `cancel_order` reports OrderNotFound, for an order the agent's own lookup or cancellation just showed? In what world does that happen, and what does the agent tell the customer? (R1-01; CO-S24 and the CO-A3 "order not cancelled" branch stand as written.)
2. Should a successful cancellation tell the customer the refund id? (R1-05, proposed CO-08 change.)
3. What if a customer with no orders at all asks to cancel one? (R1-12)
4. What if the lookup after an unanswered cancellation answers but no longer lists the order? (R1-02 part b)
5. What if the second cancellation goes unanswered and the lookup still shows the order open? The spec now says the outcome is unknown and hands off, based on its own rules and SG-04, because no input covers a second cancellation timeout. (R2-05; please confirm.)
6. What if the customer asks to cancel a second order in the same conversation? G-01's "current request" and CO-06's per-conversation counts give two readings. (R2-12)
7. What if an already-cancelled order has a failed refund or no refund? The input says the agent "reports that and changes nothing", and §2 says the support team wants every unfinished refund handed to it. What does the agent tell the customer, and does it hand the order off? (R2-14, R1-07 / CO-07)
8. What if `issue_refund` returns a refund whose amount or payment method differs from the confirmed proposal? (R2-16)
9. What if both handoff calls time out after a cancellation-unknown or refund-status-unknown result? No scenario asserts the message. (R3-06)
10. Template text, which step 4 never edits: §5.1 does not define "the user's confirmation turn" when no confirmation turn occurs (R2-08), and the end-of-trial rule never fires for an agent that retries an unanswered lookup forever (R2-10).

## What verification cannot catch

Verification cannot tell whether these rules are the business's real rules (full-order only, refund to the original payment method, one retry per call, the handoff reasons) or whether the stakeholder list is complete. Only the user can confirm those.

## Checklist lines proposed for kept patterns no checklist covers

- Evaluation checklist: "A scripted User turn's trigger must be able to occur in its scenario. When the trigger is the confirmation question for a proposal that no in-scope pair matches, define it by form ('a question that states every value of a proposal for X and asks to go ahead'), not by §5.1's pair-matched term." (R2-01)
- Evaluation checklist: "A rubric dimension with a window says which text it reads, agent messages (§5.1) or all text, and a 'never says X' clause is bounded to the text after the last event that could make X briefly true." (R1-16, R2-03, R2-04, R3-09)
- Use-case checklist, Failure handling: "When a supporting-actor guarantee lets an unanswered commit take effect late, a lookup after the last allowed attempt cannot show 'not done'; handle that branch as outcome unknown." (R2-05)
- Evaluation checklist: "An ordering Forbidden line over a repeatable read names its quantifier: '<action> with no <read> between <earlier action> and it'." (R2-06)
- Evaluation checklist: "Every scenario where the agent reports an outcome has a dimension that checks the stated status, including success paths, not only failure paths." (R3-04)
- Use-case checklist, Failure handling: "A row that applies the input's procedure for one failure (retry, then re-read, then report) covers every outcome of the retry, not only the outcome that repeats the first failure." (R1-02, R3-03)

## Interview

No interview ran. The run started at step 4.1 on a frozen spec and packet. The packet records the original interview as direct.
