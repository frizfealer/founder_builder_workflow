# Step-5 report (full-new-3)

Verification-only trial: step 4 run from 4.1 on eval/verify-test/round0-agent-spec.md, with the given review packet (step 4.2 skipped). Wall clock: 2026-11-08T15:23:37Z (first 4.1 run) to 15:50:05Z = 26 min 28 s. Round 1: 11 min 38 s. Round 2: 7 min 07 s. Round 3: 7 min 43 s.

## File and capabilities

- File: eval/verify-test/run/agent-spec.md (copy: results/full-new-3/agent-spec-final.md).
- One capability: 4.1 Cancel Order (CO), state-changing. 27 scenarios (CO-S01 to CO-S27), up from 24 in round 0. Round 1 added CO-S25, CO-S26 and CO-S27.

## Step 3.9 merges

Not run: this trial starts at step 4, and step 4 does not merge. The checker prints 8 WARNING groups (below). Two of them are new in this run, and each stays apart for a stated reason:
- CO-S13 / CO-S25: CO-S25 needs the Forbidden line "CO-A3 before a CO-A1 made after the second CO-A2.", which does not hold for CO-S13's flow.
- CO-S26 / CO-S27: each uses a different rubric dimension ("Shipped order explained" / "Cancellation not done reported").

The other 6 groups were already in round 0. No rows dropped.

## Input ledger (final; from the review packet, unchanged)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied, the rest proposed and confirmed with changes | interview round 2 Q3 answer, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found, default accepted: a state-changing call is authorized only by the customer's explicit confirmation of the full proposal (order, refund amount, payment method); any change voids it | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases, no transcripts | interview round 2 Q4 |

## Tools

Proposed, so provisional: list_orders(), cancel_order(order_number) and request_staff_followup(order_number, reason). Supplied by the user: issue_refund(order_number). Appendix A is the part of the spec that architecture notes may change. Verification changed Appendix A in two places (R1-16, R1-17).

## Checker

Final 4.1 run: **0 errors**, 8 WARNING lines (merge candidates; no effect on the exit code).

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S26, CO-S27 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26, CO-S27 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S06, CO-S09 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S24, CO-S25, CO-S26 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26, CO-S27 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S27 |
| CO-08 | CO-S01, CO-S16, CO-S19, CO-S25 |
| CO-09 | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S25 |
| CO-10 | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25 |

## Findings

**43 findings: 31 Important, 12 Nit**, merged across 3 rounds from 46 raw finder findings. Merging removed 3 duplicates within rounds.

- **Dropped:** 12, all Important.
- **Kept:** 31 (19 Important, 12 Nit). Of these, 24 fixed, 1 answered, 6 open, 0 Pre-existing.
- **Rounds:** 3 of 3. The run stopped at the round cap: round 3 still changed the spec.

| Round | Merged | Important to verifier | Nit to fix | Dropped | Fixed | Answered | Open |
|---|---|---|---|---|---|---|---|
| 1 | 18 | 15 | 3 | 4 | 13 | 0 | 1 |
| 2 | 13 | 8 | 5 | 5 | 6 | 1 | 1 |
| 3 | 12 | 8 | 4 | 3 | 5 | 0 | 4 |

Per finding, with source text, verifier line, decision and status: round1-findings.md, round2-findings.md, round3-findings.md.

- Fixed (24): R1-02, R1-03, R1-04, R1-05, R1-06, R1-08, R1-10, R1-11, R1-12, R1-13, R1-16, R1-17, R1-18; R2-02, R2-05, R2-08, R2-09, R2-10, R2-12; R3-03, R3-07, R3-10, R3-11, R3-12.
- Answered (1): R2-13. It stands because CO-04 defines a proposal as the full proposal (order number, amount, payment method). CO-S08's whole-order question states none of those terms, and no verdict depends on it.
- Open (6): R1-01, R2-11, R3-01, R3-02, R3-08, R3-09 (see Open questions).

**Defects introduced by fixes vs defects missed.** These counts cover kept findings, compared against the saved round copies with diff:
- **Round 2 vs round 1's changes:** 2 kept findings quote a line round 1 changed: R2-02 (CO-09) and R2-05 ("Refund not confirmed reported"). 6 quote a line round 1 did not change. One of those, R2-09, is still a fix defect: a leftover of the incomplete R1-16 fix, on a trajectory line round 1 did not touch.
- **Round 3 vs round 2's changes:** 1 kept finding quotes a line round 2 changed: R3-09 (the shipped/cancelled row condition from R2-12). 8 quote a line round 2 did not change. One of those, R3-07, quotes a round-1 fix (R1-12).

**Verifier drop rate: 12 / 31 Important findings verified (39%).** Round 1: 4/15. Round 2: 5/8. Round 3: 3/8. Each dropped finding's refutation, quoted from the verifier:
- R1-07: "SG-01 already settles the case: 'a repeated refund call for an order returns the same refund id'. Appendix A agrees: 'every later call returns that same refund'."
- R1-09: "CO-S11's Unambiguity note settles it: 'in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation'."
- R1-14: "G-04 is an 'only when' condition: it sets a requirement and grants no permission. CO-06 adds a further requirement ... G-04's clause cites SG-01, not SG-04."
- R1-15: "§5.2 says 'A rubric judge reads every text the agent sends, including text sent alongside a tool call'. The CO-S23 dimension says 'never says … that staff will follow up'."
- R2-01: "G-03 already requires the statement the finding says no rule asks for: '... Otherwise it tells the customer the action was not done'."
- R2-03: "The checklist item it quotes, 'the lookup returns more than one plausible match, or none (ambiguous match)', covers ambiguity, and the spec already handles that ... The 'cancel both of my orders' request is the finder's own invention."
- R2-04: "§5.2 Graders says 'A rubric judge reads every text the agent sends, including text sent alongside a tool call,' and the dimension says 'never says ... that staff will follow up.'"
- R2-06: "For a first CO-A3 that 'did not answer', the required behavior is 'Make CO-A3 once more, relying on SG-01.' That has no condition attached."
- R2-07: "Appendix A says 'The agent may repeat CO-A1 without limit; only commit calls are bounded,' and the packet's tool confirmation turn, change 4, says 'Reads may be retried on timeout without limit.' So both runs pass."
- R3-04: "The Unambiguity note already settles which reading applies: 'The status change is tied to the agent's first cancellation ...'."
- R3-05: "G-04 is an 'only when' rule. It sets a condition a repeat must meet but does not permit a repeat on its own ... G-04's parenthetical cites only '(Appendix B, SG-01)'."
- R3-06: "The failure row ... requires 'Make CO-A3 once more, relying on SG-01' without condition, so the agent must make the second call whatever an extra lookup shows."

Re-reports: 4 of round 3's 8 Important findings repeated findings dropped earlier: R3-04 (= R1-09), R3-05 (= R1-14), R3-06 (= R2-06), and R3-08 (close to R2-07). answered.md lists only kept findings, so the finders had no record of the drops. Each re-report cost a verifier pass, and the verifier dropped three of them again. R3-08 was kept this time, reframed as Untestable.

## Proposed rule changes (not applied; for the user)

- **CO-08 (R3-01).** No input asks the agent to tell the customer the refund id.
  - Before: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id."
  - After: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, and no follow-up task exists for it."
  - Lines left unchanged until you decide, so CO-08 as written stays asserted: message check "Refund id reported" (9 scenarios) and "and the refund id" in the second-CO-A3 failure row. If you accept the change, they go too.
- **CO-07 (R3-02).**
  - Before: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, ..."
  - After: "When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows, ..."
  - It would come with a CO-S06 row where the already-cancelled order's refund has failed.

## Open questions

- R1-01: What if issue_refund returns OrderNotCancelled right after cancel_order returned the order cancelled? Should the agent report the refund as not issued, or look up and hand off as cancellation unknown?
- R2-11: What if the first refund call timed out and the retry answers? Should the agent still re-read before reporting, as known case 3's "retries once, then re-reads" suggests? The spec re-reads only after two unanswered calls.
- R3-01: What if the agent tells the customer the order is cancelled and the refund pending, but gives no refund id? Is that a failure?
- R3-02: What if the customer asks about an order that is already cancelled but whose refund failed or never existed? Leave it, or hand it to staff?
- R3-08: What if the order system never answers a lookup? After how many unanswered lookups does the agent stop and report? The inputs allow unlimited reads, and a trial ends only on an agent message.
- R3-09: What if the customer has several orders, none placed or processing, and names none? What does the agent tell them?

## What verification cannot catch

Whether these rules are Harbor Goods' real cancellation and refund rules, and whether the stakeholder list is complete. Only you can confirm both.

## Proposed checklist lines (patterns no checklist covers)

- evaluation-checklist.md: "A [minimal guarantee] rule about what the agent says is checked by a dimension in every scenario whose exit it covers, failure exits included, not only the success scenarios." (R1-04, R2-02)
- evaluation-checklist.md: "A message the inputs dictate keeps the inputs' words in the failure row and the rubric, and the rubric lists the truthful equivalent forms that count." (R1-03, R2-05, R3-07)
- evaluation-checklist.md: "Every confirm scenario forbids the commit call before the confirmation turn; 'exactly N, after X' in Required events does not cover a call before X." (R2-08)
- evaluation-checklist.md: "A disclosure the agent must make (an id, a status) traces to an input; a message check never adds one." (R3-01)
- cockburn-checklist.md: "Every unanswered commit call, including the last allowed retry, is followed by a read before the agent reports or hands off, and the row branches on that read." (R1-02)
- cockburn-checklist.md: "A state the capability can leave behind (cancelled, refund failed, no task) is tested as an Initial state of the same capability." (R3-02)
- Process (not a checklist): list dropped findings and their refutations in answered.md too, so later finders do not re-report them (4 re-reports in round 3).

## Interview

The packet does not record which interview skill ran. The interview is given only as its verbatim Q&A rounds, so this trial cannot tell whether grilling ran or the interview was direct.
