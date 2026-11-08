# Report (full-new-1): verification of the Harbor Goods order-support Agent Spec

## File written
- eval/verify-test/run/agent-spec.md (copy: results/full-new-1/agent-spec-final.md). Nothing under examples/ was touched.
- Capability 4.1 Cancel Order (CO): 29 scenarios, CO-S01 to CO-S29 (24 at the start; this run added CO-S25 to CO-S29). Data-variant rows were also added to CO-S01 (row 4), CO-S03 (row 4), CO-S06 (rows 3 and 4) and CO-S13 (row 3).

## Step 3.9 merges
- None. This trial started at step 4.1, so step 3.9 did not run. The checker's WARNING groups are listed below. CO-S25/CO-S26 and CO-S27/CO-S29 were added in this run, and each pair stays apart because the final status and the rubric dimension (or the lookup behaviour) differ, and every dimension would have to pass for every row. No rows were dropped.

## Input ledger, final state (from the review packet; unchanged in this run)
| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial: issue_refund supplied; list_orders, cancel_order and request_staff_followup proposed and confirmed with the user's four changes |
| 3 | Data model | found |
| 4 | Authorization policy | found (the user accepted the default: explicit confirmation of the full proposal; any change voids it) |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases, no transcripts |

## Proposed tools
list_orders, cancel_order and request_staff_followup were proposed (issue_refund was supplied). They are provisional. Appendix A is the part of the spec that architecture notes may change. This run edited Appendix A only to remove the invented `failure_reason` field (R1-05) and to reword the OrderNotCancelled outcome as something the order system reports (R2-05).

## Checker (final run)
```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12, CO-S28: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S11, CO-S24: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S25, CO-S26: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S27, CO-S29: identical Required events after substitution; merge candidates (skill step 3.9)

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09 |
| CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S13, CO-S24, CO-S25, CO-S28 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S26, CO-S27, CO-S29 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01 |
```

## Findings
Count line: 31 findings: 22 Important, 9 Nit (severity as the finders gave it, deduplicated within each round). Round 1 had 18, round 2 had 10 (including 1 late round-1 finding), and round 3 had 3.
- Fixed: 19. R1-01, R1-02, R1-03, R1-04, R1-05, R1-06, R1-07, R1-08, R1-13, R1-15; R2-01, R2-02, R2-03, R2-05, R2-06, R2-07, R2-08, R2-L1; R3-01.
- Answered (stands): 1. R1-16 stands because SG-01, which the user supplied, makes a repeated refund call return the existing refund. A provider-unavailable answer to the second call therefore means no refund exists, so "refund not issued" is true.
- Open: 5. R1-09, R1-10, R1-12 and R1-14 (see open questions), and R3-02 (unverified, below).
- Pre-existing: 1. R3-03 (unverified, below).
- Dropped by verification: 5 (R1-11, R1-17, R1-18, R2-04, R2-09).

Rounds run: 3. The run stopped at the round cap and did not converge, because round 3 changed the spec (it added CO-S29).

Fix-introduced defects vs earlier misses:
- Round 2: 8 kept findings. 6 quote a line round 1 changed or added (R2-01, R2-02, R2-03, R2-05, R2-07, R2-08), meaning a fix introduced a defect. 2 quote lines round 1 did not change: R2-06 (an incomplete carry-through of fix R1-05 into unchanged trajectories) and R2-L1 (a defect earlier finders missed, reported late by a round-1 finder).
- Round 3: 1 kept finding (R3-01). It quotes a line round 2 changed, an incomplete R2-03 fix.
- Kept findings in a bundle context block rather than a changed block: round 2 had 0 whole findings, but R2-06's CO-S22 and CO-S23 instances sat in section-4 context. Round 3 had 0 kept; the unverified Pre-existing R3-03 is in context block CO-S11.

Verifier drop rate: 5 of 20 Important findings verified were dropped (round 1: 3/12; round 2: 2/7; round 3: 0/1). The refutations:
- R1-11 (refund id not in the inputs): "The packet asks the spec writer to derive: \"Derive any further cases yourself\" (line 55). No input forbids or contradicts reporting the id."
- R1-17 (no initial follow-up-task population): "§5.1 line 1477 says Final state assertions \"are read against Initial state\", and no Initial state creates any follow-up task, so the starting set is empty by construction."
- R1-18 (Turn 2 trigger not a §5.1 event): "§5.2 line 1481 makes the simulated user an LLM that \"says the User turns on its own, at the points they state\", judged on meaning ... The trigger ... closely follows §5.1's confirmation-question form."
- R2-04 (OrderNotCancelled branch without a scenario): "The row has two outcomes, not three: \"Otherwise, including when the lookup does not answer, make CO-A4 with reason cancellation unknown ...\" ... CO-S27 covers that." (Round 2's fix made the branches explicit, and R3-01 then reopened the same gap and was kept.)
- R2-09 (status check should be a message check): "§5.2 Graders: ... \"a check with any part that needs judgment ... is a rubric dimension in full, however exact its other parts\". The dimension includes \"and states no other status for it\"."

Where the two verifiers disagreed, the decision was recorded with the finding (R1-03, R1-13, R1-14, all kept as Nit). Full verdicts are in round1-findings.md, round2-findings.md and round3-findings.md.

Unverified (late verdicts finder in round 3, the last round; not applied):
- R3-02: lookup-dependent customer reports are not anchored after the lookup. An agent could send its guessed report alongside the CO-A1 call, which rubric judges read (CO-S15, CO-S20, CO-S21, CO-S25, CO-S26, CO-S28).
- R3-03 (Pre-existing): CO-S11 row 2 does not require the lookup after the unanswered CO-A2.

Late finder in round 1: set B's Codex verdicts finder returned without a report, and its report was collected with SendMessage. Its F1 duplicated R1-18. Its F2 was folded into round 2 as R2-L1, verified there and fixed.

## Proposed rule change, not applied
The skill stops a fix that changes a rule's text at that rule, so this one needs the user's decision:
- **G-04 (R1-12).** Before: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)." Proposed: "... or, for CO-A3 and CO-A4, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03)." As written, SG-04 makes the general clause allow a blind CO-A2 resend, which the input forbids. CO-06 and the scenarios already enforce the input, so no verdict changes.

New rule added in this run: CO-09 (R1-06), which forbids any promise about when the refunded money arrives. It was widened in round 2 (R2-08). Because CO-09 is a rule this run added and the user never approved it, I edited its text directly rather than treating the change as a proposal. The user should confirm both the rule and that choice.

## Reviewers
- Subagents (general-purpose, Opus 5.5): every faithfulness and coverage finder (4 in round 1, 2 in each later round) and every verifier (2 per round).
- Through Codex (codex:codex-rescue): every verdicts finder (2 in round 1, 1 in each later round).

## Open questions
- What if the lookup after an unanswered cancellation no longer lists the order at all? No input says what the agent does or tells the customer (R1-09).
- What if a customer with no orders at all asks to cancel "my order"? CO-01 covers a customer whose orders are all shipped, delivered or cancelled. No input covers a customer with no orders (R1-10).
- What if a customer wants two orders cancelled in one conversation ("cancel both")? G-01 and CO-06 allow one order per conversation, but no input chose that limit or says what the agent tells the customer (R1-14).
- What if, after two unanswered cancellations, the lookup shows the order still open? The spec now has the agent report "not cancelled" with no handoff (derived from G-03 and CO-07). Should store staff be asked to cancel it instead? (Raised while fixing R1-01.)
- What if the order system answers a cancellation "cancelled" and the refund call then says "not cancelled"? The spec now has the agent look the order up and hand off when it cannot tell (derived from CO-07). The inputs give no handling for OrderNotCancelled (R1-02, R2-03, R3-01).
- G-04 proposed change above (R1-12).

## What verification cannot catch
Verification cannot tell whether these rules are the business's real rules, or whether the stakeholder list is complete. Only the user can confirm those. The two derived handlings in the open questions above most need that confirmation.

## Checklist proposals (kept findings whose pattern no checklist covers)
- evaluation-checklist: "A rubric dimension requires only what the rule or failure row it grades requires; it adds no clause." (R1-04)
- cockburn-checklist, Contract: "A constraint written only in 'The agent must not' that limits what the agent says has a Contract rule and a dimension that checks it." (R1-06)
- evaluation-checklist: "When several calls to one action go unanswered, Initial state gives each call's effect separately, so a lookup between them has one result." (R2-L1)
- evaluation-checklist: "When the right final report could be guessed without a lookup the failure row requires, a Forbidden line requires that lookup." (R2-01, R2-02). This is in tension with "Outcome, not path", which the checklist could resolve explicitly.
- cockburn-checklist, Failure handling (extends "covers every result of the lookup"): "each branch of a lookup-dependent row that changes the action or the message has its own scenario, including a branch that shares an action with another." (R3-01)

## Interview
No interview ran in this trial (verification only). The packet records the original interview as direct.
