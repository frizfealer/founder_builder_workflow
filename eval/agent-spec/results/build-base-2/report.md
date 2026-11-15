# Agent Spec report: Harbor Goods order-support agent (build-base-2)

## File written
`eval/agent-spec/run-build-base-2/product/agent-spec.md` (copy: `results/build-base-2/agent-spec-final.md`).

One capability, **4.1 Cancel Order and Refund (state-changing), prefix CO**, with rules G-01 to G-04 and CO-01 to CO-08 and **16 scenarios**:
- CO-S01 to CO-S07, CO-S09, CO-S11 to CO-S14 and CO-S16 to CO-S19.
- Ids CO-S08, CO-S10 and CO-S15 are unused (merged).
- 49 data-variant rows in all.

## Step 3.9 merges and dropped rows
- **CO-S08 into CO-S01 (row 4).** CO-S08 is "cancellation got no answer; a read shows it went through". Dropped source row: CO-S08 row 2 ("Cancel HG-10482, please." with the unanswered cancellation). It was only a wording variant of the read-then-refund path (CO-06, G-04).
- **CO-S10 into CO-S07 (row 3).** CO-S10 is "cancellation got no answer; a read shows the order shipped". Dropped source row: CO-S10 row 2 ("Please cancel HG-10482 and refund it." with the unanswered cancellation). It was only a wording variant of CO-06's shipped branch.
- **CO-S15 into CO-S13 (rows 4 and 5).** CO-S15 is "both refund calls got no answer; a read shows the refund". No row dropped.
- **CO-S02 and CO-S03 stay apart.** Their final-state lines differ, and their User and User-knows blocks differ in kind (a required which-order question versus a scripted Turn 2 change), which data-variant rows cannot express.
- **CO-S01 and CO-S19 not merged.** Round-1 fixes added CO-S19 after step 3.9, and the checker now warns on CO-S01/CO-S19. Step 4 does not re-run 3.9, and CO-S19 has a scripted Turn 2, so they stay apart.

## Input ledger, final

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md; round 1 Q1, Q2 |
| 2 | Tools | found (confirmed) | issue_refund supplied by the user; list_orders, cancel_order, request_staff_followup proposed and confirmed with the user's four changes |
| 3 | Data model | found | round 2 Q3 with the user's changes |
| 4 | Authorization policy | found, default accepted | round 1 Q3 (signed-in customer, precondition); default accepted in round 1 Q4; extended by round 3 Q1 |
| 5 | Domain rules | found | rounds 2 and 3; shared-understanding summary |
| 6 | Known failure cases | found | three cases, round 2 Q4; no transcripts |

Default accepted (round 1 Q4): an explicit confirmation of the full proposal (order, refund amount, destination) authorizes the action, and any change voids it. Round 3 Q1 extends it: one confirmation covers both the cancellation and the refund.

## Proposed tools (provisional)
- `list_orders()` (read-only), `cancel_order(order_number)` and `request_staff_followup(order_number, reason)` were proposed and are provisional.
- `issue_refund(order_number)` was supplied by the user.
- These outcome names were proposed and are not from the inputs: `RefundServiceUnavailable`, and the return shapes of `cancel_order` and `request_staff_followup`.
- Supporting-actor guarantees SG-01 to SG-04 are in Appendix B.
- **Appendix A is the part of the spec that architecture notes may change.**

## Checker
Final count line: **0 errors** (WARNING lines: CO-S01/CO-S19 and CO-S02/CO-S03).

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S05, CO-S07, CO-S11, CO-S12, CO-S13, CO-S14, CO-S16, CO-S18 |
| G-02 | CO-S01, CO-S05, CO-S06 |
| G-03 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S19 |
| G-04 | CO-S01, CO-S07, CO-S09, CO-S11, CO-S12, CO-S13, CO-S14, CO-S16, CO-S17 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S07 |
| CO-02 | CO-S02 |
| CO-03 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S19 |
| CO-04 | CO-S01, CO-S07, CO-S09 |
| CO-05 | CO-S13, CO-S14, CO-S16, CO-S17 |
| CO-06 | CO-S01, CO-S07, CO-S09, CO-S11, CO-S12 |
| CO-07 | CO-S11, CO-S17, CO-S18 |
| CO-08 | CO-S01, CO-S02, CO-S13, CO-S19 |

## Findings
**28 findings: 17 Important, 11 Nit.** 3 rounds ran, which is the round cap. Each round changed the spec, and no fourth round reviewed round 3's fixes.

Status: 21 fixed, 3 open (R1-05, R1-10, R2-03), 2 answered (R1-06, R1-11), 2 dropped (R2-04, R3-07), 0 Pre-existing. R2-06, R2-07 and R3-01 are fixed in the failure rows and dimensions, but their rule-text parts are proposed below.

| Round | Findings | Fixed | Open | Answered | Dropped |
|---|---|---|---|---|---|
| 1 | 11: 7 Important, 4 Nit | 7 | 2 | 2 | 0 |
| 2 | 10: 5 Important, 5 Nit | 8 | 1 | 0 | 1 |
| 3 | 7: 5 Important, 2 Nit | 6 | 0 | 0 | 1 |

Detail for every finding, verbatim with verifier verdicts, is in `round<N>-findings.md`.

Answered:
- **R1-06:** the Turn 2 trigger in CO-S03 and CO-S04 changes no verdict. It is the same form the skill's café example uses, and §5.1's fixed text is not edited in step 4.
- **R1-11:** when the customer goes silent there is no agent turn, and the simulated user cannot script silence. The resulting state is the one CO-S04 asserts.

Attribution, by diff of the saved round copies:
- **Round 2:** 9 kept findings. 3 quote a line round 1 changed, so a fix introduced the defect (R2-02, R2-05, R2-10). 6 quote lines round 1 did not change, so earlier finders missed them.
- **Round 3:** 6 kept findings. 1 quotes a line round 2 changed (R3-05). 5 quote lines round 2 did not change.

Verifier drop rate: Important 0/17 dropped. Nit 2/11 dropped:
- **R2-04** was refuted by the Appendix A heading "Interface binding (provisional)" and "Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios."
- **R3-07** was refuted by the evaluation checklist: "Precision ... report it to catch over-asking, but do not score on it, since a reasonable extra question is not a failure". CO-02 does not forbid asking when one order fits.
- Four findings with a Style-only verdict were kept because they are not about wording: R1-06, R1-11, R2-03, R3-06.

## Open questions
- **What if a read keeps timing out?** (R1-05) The user allowed read retries "without limit", but a trial ends only on an agent message. A bound on read retries needs the user's decision.
- **What if the refund the store issues differs from the proposal?** (R1-10) Proposed change to CO-08.
  - Before: "exactly one refund exists for it, with status pending or issued"
  - After: "exactly one refund exists for it, for the order's total paid to the order's payment method, with status pending or issued"
  - A rule is also needed for a refund-service result with the wrong amount or payment method.
- **What if the handoff needs its own consent?** (R2-03) CO-03 says the one confirmation "also authorizes ... any CO-A3". The inputs say only that it covers cancel and refund. The user should decide whether to keep that, or drop it and exempt CO-A3 from G-03.
- **What if the follow-up queue never answers?** (R2-07) Proposed change to CO-05. The failure rows already say this.
  - Before: "...tells the customer the refund is not confirmed and staff will follow up."
  - After: "...and, once the handoff returned a task, that staff will follow up."
- **What if the retry after a refund timeout returns a result?** (R3-01) Proposed change to CO-05's last sentence. The rows and scenarios already require this.
  - Before: "After a second CO-A2 got no answer, the agent reads the refund record before it reports or hands off."
  - After: "After a CO-A2 that got no answer, the agent reads the refund record once the retry returns, before it reports or hands off."
- **What if a commit call times out after an earlier read?** (R2-06) Proposed clarification to G-01: an unanswered commit call leaves its record's status unknown until a later read shows it. The rubric already says this.
- **What if both cancellation attempts time out and the order is still open?** No input covers this. CO-S12 is my derivation: the agent reports that the order is not cancelled and sends nothing more. Should staff get a follow-up task instead?

## What verification cannot catch
Whether these rules are Harbor Goods' real rules, and whether the stakeholder list is complete, can only be confirmed by the user. The list is: the customer, the order system, the refund service, the follow-up queue, Harbor Goods, store staff, and the customer's other orders.

## Patterns no checklist covers (proposed lines)
- **Evaluation checklist:** a rubric definition says whether text sent alongside a tool call counts (R3-02).
- **Evaluation checklist:** don't grade "the final message", because a closing line can follow the report. Grade a message after the agent's last call (R2-05).
- **Use-case checklist, failure handling:** a row for the retry of a timed-out commit call depends on what the first call returned, and a "nothing happened" report after a timeout needs a read first (R1-01, R3-01).
- **Evaluation checklist:** a dimension's exclusion clause must not forbid a fact the row's own Initial state makes true (R2-01).
- **Evaluation checklist:** a must-not about what the agent offers needs a rubric dimension that fails the offer (R3-04).

## Interview
The interview was direct, replayed from the recording. No interview skill ran, because replay rule 6 forbids grilling and grill-with-docs.
