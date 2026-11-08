# Agent-spec verification report (full-new-2)

Verification-only trial of agent-spec step 4 (4.1, then 4.3 to 4.5; 4.2 skipped per the trial prompt, round0 copy saved). Run 2026-11-07T19:21:59Z to 19:49:37Z for the three rounds; the run ends when the last subagent has reported (see run.log).

## File written and capabilities

- Spec under review: eval/verify-test/run/agent-spec.md (final copy: results/full-new-2/agent-spec-final.md). Nothing under examples/ was touched.
- One capability: **4.1 Cancel Order (CO), state-changing**: 27 scenarios (CO-S01 to CO-S27). Rounds added CO-S25, CO-S26 and CO-S27 and these data-variant rows: CO-S01 r4, CO-S03 r4, CO-S05 r4, CO-S06 r3, CO-S20 r3.
- Rules: G-01 to G-04 and CO-01 to CO-09 (CO-09 "No promised arrival date" added in round 1).

## Step 3.9 merges and dropped rows

- Step 3.9 did not run, because this trial starts at step 4.1. The checker's merge-candidate WARNINGs are listed below. Groups created by this run stay apart for these reasons:
  - CO-S13 and CO-S25: CO-S25 forbids CO-A3 before a lookup made after the second CO-A2, and CO-S13 allows it. This spec's §5.1 defines no conditional Forbidden lines.
  - CO-S26 and CO-S27: the final status and the rubric dimension differ ("Shipped order explained" vs "Cancellation not made reported").
- Dropped row: the round-1 CO-S26 row 2 (final status delivered, which jumped processing to delivered), replaced in round 2 (R2-03). The delivered branch of the "second CO-A2 unanswered" row is still covered by its shipped-or-delivered clause, which row 1 exercises with shipped.

## Input ledger (final state, from the review packet; unchanged by this run)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied, the rest proposed and confirmed with changes | interview round 2 Q3, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found (default accepted) | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases, no transcripts | interview round 2 Q4 |

The user accepted one default: the authorization policy (an order is cancelled only after the customer explicitly confirms the full proposal, and any change after confirmation voids it). Defaults kept: 5 trials and a 12-message cap. No metric changes.

## Proposed tools (provisional)

list_orders() (read-only, proposed), cancel_order(order_number) (proposed), issue_refund(order_number) (supplied by the user), request_staff_followup(order_number, reason) (proposed). All are bound in Appendix A. Appendix A is the part of the spec that architecture notes may change. This run edited Appendix A once: R1-09 removed an invented `failure_reason` field.

## Checker (final 4.1 run)

```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S11, CO-S24: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S13, CO-S25: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S26, CO-S27: identical Required events after substitution; merge candidates (skill step 3.9)

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S26, CO-S27 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26, CO-S27 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09 |
| CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S24, CO-S25, CO-S26 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26, CO-S27 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S27 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01 |
```

## Findings

**Count line, all rounds (kept findings after verification, final severities): 21 findings: 8 Important, 13 Nit.** On top of these: 3 Pre-existing, 1 duplicate (R2-L1 = R1-06), and the unverified Codex findings listed below.

- **Rounds run: 3** (the round cap). Every round changed the spec, so the run stopped at the cap, not on a round that changed nothing.
- **Per round (merged count lines):**
  - Round 1: "10 findings: 7 Important, 3 Nit."
  - Round 2: "7 findings: 2 Important, 5 Nit." (plus 2 late Important findings from round 1's Codex finder)
  - Round 3: "2 findings: 1 Important, 1 Nit."
- **By status:**
  - Fixed, 15: R1-01, R1-03, R1-04, R1-05, R1-09, R1-10; R2-01, R2-03, R2-04, R2-05, R2-06, R2-07, R2-L2, R2-L3; R3-01.
  - Fixed in part, 1: R3-02 (the rest is open).
  - Answered, 1: R1-07. It stands because the confirmed derivation "An already cancelled order: the agent reports that and changes nothing" supports the line.
  - Open, 4: R1-02, R1-06, R2-02, and R1-08 (a proposed rule change, below). R2-L1 is open with R1-06.
  - Pre-existing, 3: the first-CO-A2 row tells the customer staff will follow up before it makes CO-A4 (round 2). The same row leaves out "no refund was issued" (round 3; both verifiers judged it Real, Important). The second-CO-A4-unanswered row has no scenario for the reasons cancellation unknown or refund status unknown (round 3).
- **Every finding with its status:** see round1-findings.md, round2-findings.md and round3-findings.md in this directory.

**Rounds after the first (what the previous round's changes caused):**
- Round 2: 7 kept findings from round-2 finders quote a line round 1 changed: a fix that introduced a defect, or one left incomplete (R2-01 to R2-07). 0 quote a line round 1 did not change. The 2 late round-1 Codex findings (R2-L2, R2-L3) quote round-0 lines, so they are defects the earlier finders missed. Kept findings in a bundle context block: 0 (1 Pre-existing line).
- Round 3: 2 kept findings quote a line round 2 changed (R3-01, R3-02). 0 quote a line it did not change. Kept findings in a bundle context block: 0 (2 Pre-existing lines).

**Verifier drop rate: 0/12** (round 1 0/7, round 2 0/4, round 3 0/1). No Important finding was dropped, so there is no refutation to quote for a drop. Split verdicts were kept at the lower severity, with the adversarial refutation recorded in the round files: R1-07, R2-02, R2-L2, R2-L3.

**Proposed rule change, not applied (R1-08).** The rule-change limit stops this fix at the rule; the user decides.
- Before (G-04): "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
- After: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or, for CO-A3 and CO-A4, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03)."

**Unverified, not applied.** These are Codex verdicts-finder findings that arrived after the last round's verification, so no next round exists to verify them:
- **Round 3 Codex F1** (Gap, Important; reported in full in eval/verify-test/run/reports/r3-verdicts-codex.md). CO-S05, CO-S06, CO-S10, CO-S11 row 2, CO-S26 and CO-S27 do not require the CO-A1 lookup that their required message depends on. CO-S26 and CO-S27 do not require the lookup after the second unanswered CO-A2. So an agent that guesses the outcome without looking it up can pass. No Claude finder raised this.
- **Round 2 Codex verdicts finder: no findings.** Its Codex job (task-mw6szlw5-otc7sg) wrote nothing after 19:36:05Z and was still in the "verifying" phase when last checked. It was not cancelled.

## Reviewers: subagents and Codex

- These ran as subagents (general-purpose, Opus 5.5) every round: the faithfulness finder, the coverage finder, the standard verifier and the adversarial verifier.
- The verdicts finder ran through Codex (codex:codex-rescue) every round:
  - Round 1's report arrived after 4.4 began and was folded into round 2.
  - Round 2's first hand-back had no report. Two SendMessage follow-ups were needed; see the unverified list above and run.log.
  - Round 3's report arrived after round 3 ended.
- Per 4.3, the run never waited for the Codex finder before 4.4. Per the trial instructions, the run did not end until every subagent had reported. See subagent-stats.md.

## Open questions (what the inputs could not answer)

1. **R1-02.** What if issue_refund reports OrderNotCancelled for an order that cancel_order (or a lookup) returned as cancelled? Should the agent treat the order as cancelled (hand off with refund_not_issued and say the order is cancelled, as the spec does now) or as uncertain (hand off with cancellation_unknown)? Should it look up the order first?
2. **R1-06 / R2-L1.** What if the customer asks to cancel two orders in one conversation, together ("cancel both") or one after the other? May the agent do both, should it do one and say so, or should it refuse the second?
3. **R2-02.** What if both cancel calls go unanswered and the lookup shows the order still placed or processing? The agent can make no third cancel call. Should it tell the customer to try again later, tell them to contact Harbor Goods support, or hand the order to store staff?
4. **R1-08.** Should G-04 be narrowed as proposed above, so it no longer reads as allowing a blind resend of a cancel call under SG-04?
5. **R3-02 remainder.** What should the agent tell a signed-in customer who has no orders at all, or several orders none of which is open? The row covers these cases, but no scenario exercises them.

## What verification cannot catch

Two things only the user can confirm: whether these rules are Harbor Goods' real business rules, and whether the stakeholder list (customer, order system, store staff, Harbor Goods, support team, other customers) is complete.

## Patterns no checklist covers (proposed checklist lines)

- cockburn-checklist.md, Failure: "A row for the last allowed retry of a commit call that timed out still re-reads state before reporting or handing off, as the row for the first retry does." (R1-01)
- evaluation-checklist.md: "A failure row's customer message holds every clause that the rule it cites and the rubric dimension of every scenario that runs it require." (R3-01. The shared-dimension line covers dimension against dimension, not row against dimension.)
- evaluation-checklist.md: "A must-not bullet that comes from a confirmed input has a contract rule and a scenario or dimension that asserts it." (R1-04)
- specification-by-example-checklist.md: "When a fix removes a field from a tool result, every reference trajectory and data-variant row that shows or varies that field changes with it." (R2-04)
- verification.md, Finder: verdicts: "A gate of the form 'no X until a lookup answers' names no action that a later branch requires when the lookup does not answer." (R2-01)

## Interview

No interview ran in this trial: it starts at step 4 and uses the existing review packet. The packet records a direct interview in three rounds, plus a summary of the shared understanding and a turn confirming the tools.
