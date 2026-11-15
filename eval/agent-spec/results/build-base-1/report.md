# Agent Spec report: Harbor Goods order-support agent (build-base-1)

## File written

/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-build-base-1/product/agent-spec.md

There is one capability: **4.1 Cancel an Order and Refund It (state-changing), prefix CO, with 17 scenarios.** These are CO-S01 to CO-S07 and CO-S10 to CO-S19. CO-S08 and CO-S09 are unused because they were merged away. The rules are G-01 to G-04 and CO-01 to CO-11. Actions: CO-A1 cancel, CO-A2 refund, CO-A3 staff follow-up, CO-A4 look-up (read-only, bound because Forbidden lines and failure rows name it).

## Merges in step 3.9

- CO-S08 (unanswered cancellation, look-up shows it cancelled) was merged into CO-S01 as row 3.
  - Dropped row: CO-S08 row 2. It was a placed order whose unanswered cancellation did cancel, with refund RF-5571 issued and Turn 1 "I want to cancel HG-10482 and get my money back." It exercised CO-06's "cancelled: go on to the refund" branch with an issued refund. It differed from the kept row only in values and wording.
- CO-S09 (unanswered cancellation, look-up shows it shipped) was merged into CO-S06 as row 4.
  - Dropped row: CO-S09 row 2. The order turned out delivered behind an unanswered cancellation. It exercised the CO-A4 row "after an unanswered CO-A1, the look-up shows the order shipped or delivered" for delivered. It differed from row 4 only in value.
- CO-S02 and CO-S05 (and later CO-S18 and CO-S19, which share Required events with CO-S01 or CO-S02) were kept apart. Their User blocks and User-knows pairs differ: a clarify pair, a scripted change of mind, the partial-items fallback, and an unnamed single order. Their final-state lines differ too.

## Input ledger (final)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md; round 1 Q1, Q2 |
| 2 | Tools | partial, confirmed: issue_refund supplied; list_orders, cancel_order, request_staff_followup proposed and confirmed with the user's four changes | round 2 Q3; tool confirmation turn |
| 3 | Data model | found | round 2 Q1, Q3 with the user's changes |
| 4 | Authorization policy | found, **default accepted**: a state-changing call only after explicit confirmation of the full proposal (order, refund amount, destination); any change voids it; one confirmation covers cancel and refund | round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | rounds 2 and 3; shared-understanding summary |
| 6 | Known failure cases | found: three cases, no transcripts | round 2 Q4 |

## Proposed tools

`list_orders()`, `cancel_order(order_number)` and `request_staff_followup(order_number, reason)` were proposed. `issue_refund(order_number)` was supplied. All are bound in Appendix A. The proposed tools and the outcome name `PaymentProviderUnavailable` are provisional. **Appendix A is the part of the spec that architecture notes may change.** Supporting-actor guarantees are SG-01 to SG-04.

## Checker (final run)

```
0 errors
WARNING CO-S01, CO-S02, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S02, CO-S05, CO-S18: identical Required events after substitution; merge candidates (skill step 3.9)

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S05 |
| G-02 | CO-S01, CO-S02, CO-S04, CO-S05, CO-S07, CO-S16, CO-S17, CO-S18, CO-S19 |
| G-03 | CO-S01, CO-S03, CO-S06, CO-S10, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16 |
| G-04 | CO-S01, CO-S06, CO-S07, CO-S11, CO-S12, CO-S13, CO-S14, CO-S15 |
| CO-01 | CO-S01, CO-S03, CO-S19 |
| CO-02 | CO-S04, CO-S18 |
| CO-03 | CO-S02, CO-S03, CO-S05, CO-S19 |
| CO-04 | CO-S01, CO-S02, CO-S16, CO-S17 |
| CO-05 | CO-S01, CO-S06, CO-S10 |
| CO-06 | CO-S01, CO-S06, CO-S07, CO-S10, CO-S15 |
| CO-07 | CO-S11, CO-S12, CO-S13 |
| CO-08 | CO-S11, CO-S12 |
| CO-09 | CO-S10, CO-S12, CO-S13, CO-S14 |
| CO-10 | CO-S06 |
| CO-11 | CO-S01, CO-S11, CO-S18 |
```

## Findings

**25 findings verified over 3 rounds: 19 Important, 6 Nit.** 19 were kept: 15 Important, 4 Nit. 6 were dropped: 4 Important, 2 Nit.
- Fixed: 17.
- Open: 2 (R3-01, R3-05).
- Answered with a reason: none outside the fixed ones. R1-01's two failure rows have no consistent scenario, and the after-confirmation part of R2-03 has none either; both are explained in answered.md.
- Pre-existing: 0, because this is a build run.

By round:
- Round 1: 13 merged (10 Important, 3 Nit). Kept 11, all fixed. Dropped R1-08 and R1-09.
- Round 2: 7 merged (5 Important, 2 Nit). Kept 5, all fixed. Dropped R2-02 and R2-07.
  - Kept findings that quote a line round 1 changed (fixes that introduced a defect): **3**. They are R2-04 (the R1-13 trigger fix), R2-05 (the new CO-S18) and R2-06 (mostly the rewritten CO-S02 rows and the new CO-S16 and CO-S17).
  - Kept findings that quote a line round 1 did not change (missed earlier): **2**, R2-01 and R2-03.
- Round 3: 5 merged (4 Important, 1 Nit). Kept 3: R3-02 fixed, R3-01 open, R3-05 open. Dropped R3-03 and R3-04.
  - Kept findings that quote a line round 2 changed: **0**.
  - Kept findings that do not: **3**.

The round cap was reached. Round 3 still changed the spec (it added CO-S19), so verification did not converge.

**Verifier drop rate:**
- Important: 4 dropped of 19 verified (21%).
- Nit: 2 dropped of 6 verified (33%).

The refutations of the dropped findings:
- R1-08 (Important): Appendix A CO-A2 Effect says "Creates the order's refund on the first call that creates one; a later call for the same order returns that refund and creates none (SG-01)."
- R1-09 (Nit): Appendix A CO-A4 returns "the signed-in customer's orders, cancelled ones included", and no action removes an order.
- R2-02 (Important): the evaluation checklist says interaction precision is reported "but do not score on it, since a reasonable extra question is not a failure". §5.2 says interaction metrics are "never folded into the score".
- R2-07 (Important): CO-08 says "failed or no refund, it tells the customer the refund is not confirmed yet". Its failure row and packet round 3 Q3 say the same.
- R3-03 (Nit, Style only; the finding's own Quote was "The payment provider answers the first CO-A2 with: <first_refund_answer>."): §2 says "the payment provider, which receives the refund through the store, may be temporarily unavailable, may decline ... and may not answer". Every CO-A2 is bound to issue_refund, so the actor named in the line changes no injected result.
- R3-04 (Important): §5.2 says "The agent's messages tell the customer every fact in the data-variant row's outcome told column". The amounts and card appear in the proposal step of each trajectory cited.

Three findings were kept even though the verifier rated them lower:
- R1-04 and R1-13 (Style only): each cites a defect the evaluation checklist names.
- R1-06 (Not real): the verifier's citation of CO-S04 covers a neighbouring case.

Per-finding detail is in round1-findings.md, round2-findings.md and round3-findings.md.

## Open questions

- **R3-01:** What if the customer asks about an order that is already cancelled but has no refund, or has a failed refund? CO-01 says "it says the order is already cancelled ... changes nothing". CO-09 says to ask staff to follow up when an order the store reported cancelled has no pending or issued refund. Choosing one means changing one of those rules, so the user decides.
- **R3-05:** What makes an agent message "ask the user nothing" (§5.1 End of trial)? For example, "Let me know if you'd like me to cancel it." §5.1 is fixed template text, so this goes to the template owner.
- **Proposed rule change (CO-10):** CO-10 still says the store may reject a cancellation "because it finds no such order". After R1-01, no consistent scenario reaches that outcome. The same holds for CO-A2's OrderNotCancelled: a correct agent never reaches it. The proposal is to keep the failure rows as defensive handling and drop the clause from CO-10. Rule text was not changed in step 4.
- What if the second cancellation also gets no answer and the look-up then shows the order still open? This is a derived case, not one from the inputs. The spec ends with no further cancellation, no refund and no follow-up, and tells the customer the order could not be cancelled (CO-S15). The user did not say whether staff should follow up here.
- How many times may the agent repeat an unanswered look-up before it says the outcome is unknown? Reads may be retried "without limit", and the spec writes this case as "however often the agent repeats it".
- G-04 reads "one retry" as at most two sends of the same action per order. A transient error followed by a timeout, or the reverse, still counts toward that cap.

## What verification cannot catch

Verification cannot tell whether these rules are Harbor Goods' real cancellation and refund rules, or whether the stakeholder list (customer, order system, payment provider, store staff, Harbor Goods, other orders, manual refund process) is complete. Only the user can confirm both.

## Checklist proposals (kept findings whose pattern no checklist covers)

- **R1-12 / R2-01** (proposed for the evaluation checklist): "When a commit call in Initial state gets no answer, state what that call did to the world, because a read the agent may make before its next call exposes it. Write a tool result only with the fields the Appendix A result shape carries."
- **R1-01** (proposed for the evaluation checklist): "An injected outcome that only an agent error could cause, such as OrderNotFound for an order the look-up showed, has no consistent scenario. Keep its failure row as defensive handling and say so, rather than injecting it against the Initial state."
- **R2-06** (proposed for the evaluation checklist, under Graders): "An outcome-told or expected-report column holds only the facts a rule requires the agent to tell; an unchanged-record fact belongs in Final state assertions."

## Interview

The interview was direct. It was replayed from the recorded review packet, three rounds plus the shared-understanding summary. No interview skill (grilling, grill-with-docs) was invoked. The tool set was confirmed in one recorded turn with four changes.
