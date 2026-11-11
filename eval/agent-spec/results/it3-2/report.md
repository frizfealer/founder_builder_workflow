# Agent Spec verification report (trial it3-2)

## File written

`eval/agent-spec/run-it3-2/agent-spec.md` (copy: `results/it3-2/agent-spec-final.md`). It has one capability:

- **Cancel Order (CO), state-changing**: 29 scenarios, CO-S01 to CO-S29. The run added five of them: CO-S25, CO-S26, CO-S27, CO-S28 and CO-S29.

## Merges (step 3.9) and dropped rows

This run started at step 4, so step 3.9 did not run and nothing was merged.

The checker printed 8 merge-candidate WARNING groups. Each stays apart because the scenarios differ in their final state or in the dimensions they use.

One data-variant row was dropped in round 1 (R1-01):
- **CO-S17 row 3.** It had issue_refund answer `OrderNotCancelled` right after cancel_order returned cancelled. That is the CO-A3 failure row's "reported the order not cancelled" branch. That branch now has no scenario, and what it should do is an open question.

## Input ledger, final state

No changes from the review packet:

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial |
| 3 | Data model | found |
| 4 | Authorization policy | found, with the default the user accepted |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases, no transcripts |

Input 2 detail: issue_refund was supplied by the user. The other tools were proposed and then confirmed with the user's changes.

The accepted default for input 4: a state-changing call is authorized only by the customer's explicit confirmation of the full proposal (order, refund amount, payment method). Any change after confirmation voids it.

## Tools (provisional)

| Tool | Effect | Source |
|---|---|---|
| `list_orders()` | read-only | proposed |
| `cancel_order(order_number)` | state-changing | proposed |
| `issue_refund(order_number)` | state-changing | supplied by the user |
| `request_staff_followup(order_number, reason)` | state-changing | proposed |

These are provisional. Appendix A is the part of the spec that architecture notes may change.

Round 1 removed the invented `failure_reason` field from issue_refund's outcomes (R1-04).

## Checker

The last 4.1 run, after the round-3 fixes, printed: `0 errors`, 8 WARNING merge-candidate groups.

Coverage table:

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S28 |
| G-03 | CO-S01, CO-S02, CO-S03, CO-S09, CO-S10, CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S25, CO-S26, CO-S28, CO-S29 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10, CO-S27 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S28, CO-S29 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S06, CO-S09, CO-S28, CO-S29 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S13, CO-S24, CO-S26 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S25, CO-S26 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01 |

## Findings

**39 findings verified across 3 rounds: 19 Important, 20 Nit (finder severities). 32 kept, 7 dropped.**

| Round | Merged (count line) | Kept | Dropped |
|---|---|---|---|
| 1 | 19: 10 Important, 9 Nit | 16 | 3 |
| 2 | 11: 4 Important, 7 Nit | 7 | 4 |
| 3 | 9: 5 Important, 4 Nit | 9 | 0 |

Round 3 hit the cap, so its fixes were applied after the last review round and no finder checked them. Each finding's full text, the verifier's line and the decision are in `round1-findings.md`, `round2-findings.md` and `round3-findings.md`.

Status of the 32 kept findings:

**Fixed (24):**
- Round 1: R1-02, R1-03, R1-04, R1-06, R1-07, R1-08, R1-10, R1-12, R1-13, R1-16, R1-17, R1-19.
- Round 2: R2-04, R2-07, R2-08, R2-09, R2-11.
- Round 3: R3-02, R3-03, R3-05, R3-06, R3-07, R3-08, R3-09.

**Fixed, with a part left open (3):**
- R1-01: CO-S17 row 3 removed; CO-S24 made consistent. Open: the OrderNotCancelled branch.
- R2-06: unnamed request on an account with several orders and none open. Fixed with a new failure row and CO-S27. Open: a customer with no orders.
- R3-04: dimension "No needless order question" removed. Open: a possible CO-02 rule change.

**Fixed, with a part answered (1):**
- R2-02: "card closed" removed from the trajectories' tool results. The Initial-state failure reasons stand, because review-packet Round 3 Q3 names them as world facts.

**Open (4):**
- R1-09: a lookup that answers without the order.
- R1-11: cancelling more than one order in one conversation.
- R1-15: proposed rule change to CO-03.
- R3-01: proposed rule change to CO-08.

Pre-existing: 0, since this was not an update run. Rounds run: 3, stopped at the round cap.

### Which round introduced the defects

I compared the saved round copies (`attribute.py`, output in run.log):

- **Round 2:** 2 kept findings quote a line round 1 changed: R2-06 and R2-09. Those are defects the fix introduced. 5 quote a line round 1 did not change: R2-02, R2-04, R2-07, R2-08 and R2-11. Those are defects earlier finders missed. Three of the five (R2-02, R2-07, R2-08) are incomplete fixes of a round-1 pattern, even though the line they quote predates round 1.
- **Round 3:** 2 kept findings quote a line round 2 changed: R3-05 and R3-07. 7 quote a line round 2 did not change. Three of those seven (R3-04, R3-06, R3-08) quote lines that round 1's fixes added: the dimension "No needless order question", the dimension "Cancellation not made reported", and CO-S03 row 4. So 5 of round 3's 9 findings trace to this run's own fixes. 4 (R3-01, R3-02, R3-03, R3-09) quote round-0 lines that earlier finders missed.

### Verifier drop rate

- **Important:** 2 dropped of 19 verified (11%).
  - R2-01. Refutation: failure row "the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01." The retry is mandatory whatever a lookup shows.
  - R2-05. Refutation: G-03 "or a lookup shows it" and G-04 "a lookup made after that action shows it took no effect" make a lookup authoritative. Review-packet Round 3 Q4 draws the same inference for the first timeout: "Still placed or processing, send the cancel once more".
- **Nit:** 5 dropped of 20 verified (25%).
  - R1-05. Refutation: CO-06 "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing."
  - R1-14. Style only. The finding's own Quote, "The agent tells the customer the order has shipped (or been delivered) and was not cancelled", against "has shipped and cannot be cancelled". These are the same fact in different wording.
  - R1-18. Refutation: CO-S11 Final state "HG-10482 has status shipped" in both rows, plus the Unambiguity note "in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation".
  - R2-03. Style only. The finding's own Quote, "The order is past the cutoff in every row", restates the status boundary CO-01 draws and decides no verdict.
  - R2-10. Refutation: CO-04 "the full proposal: order number, refund amount and payment method". CO-S08's "Would you like to cancel the whole order HG-10530 instead?" is therefore not a proposal.

Six findings the verifier marked Style only were kept, because they are not about wording, style, formatting, heading choice or preference: R1-03, R1-04, R1-15, R2-02, R2-09 and R3-02. R1-03 and R1-11 were kept at the verifier's lower severity, Nit.

### Proposed rule changes (not applied; for the user to decide)

**1. CO-03 (R1-15).** The rule asks for both statements whatever the request, but each of its failure rows asks for only one.
- Before: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
- After: "When the customer asks to cancel only some items, the agent tells the customer that only the whole order can be cancelled; when the customer asks for a different amount, a different payment method or store credit, the agent tells the customer that the refund is the total paid to the order's payment method. In both cases it proposes nothing else."

**2. CO-08 (R3-01).** No input asks for the refund id to be reported.
- Before: "... no follow-up task exists for it, and the agent tells the customer the refund id."
- After: "... no follow-up task exists for it, and the agent tells the customer the order is cancelled and the refund's status."
- If accepted, also drop "and the refund id" from the failure row "the order system did not answer the second CO-A3". Then remove message check "Refund id reported" from CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S28 and CO-S29.

**3. CO-02 (R3-04), optional.** Add: "When exactly one of the customer's orders has status placed or processing and the customer names none, the agent proposes that order without asking which one they mean." Only with this rule can a scenario fail an agent that always asks which order is meant.

## Open questions

- What if the order system returns an order cancelled, and then refuses that order's refund with `OrderNotCancelled`? What does the agent tell the customer? (R1-01)
- What if a lookup made during recovery answers without the order the agent is working on? (R1-09)
- What if the customer asks to cancel two orders, or a second order after the first is done? The CO-06 per-conversation caps would cut the second one short. (R1-11)
- What if a signed-in customer with no orders at all asks to cancel "my order"? (R2-06)
- What if the customer is not told the refund id: is the cancellation still a success? (R3-01)
- What if exactly one order is open and the request names none: may the agent check which order is meant? (R3-04)
- What if two cancellation calls go unanswered and the lookup still shows the order open? The spec now says "tell the customer the order was not cancelled, no handoff". I derived that from CO-06, CO-07 and G-03, and kept it after the verifier refuted R2-05. A late-landing cancellation (SG-04) would leave a cancelled order with no refund and no staff task. Only the user can confirm the business accepts that.

## What verification cannot catch

Two things only the user can confirm:
- whether these rules are Harbor Goods' real cancellation and refund rules;
- whether the stakeholder list (customer, order system, store staff, Harbor Goods, the customer-support team, other customers) is complete.

## Patterns no checklist covers (proposed checklist lines)

For the evaluation checklist:
- "A 'never says X' or 'no other status' clause in a rubric dimension is scoped to the text sent after the event that settles X, because the judge reads text sent alongside tool calls too." (R2-08, R3-06)
- "An injected tool outcome must be true at that call, given Initial state and the results of earlier calls. An order the lookup just showed cannot be 'not found', and an order just returned cancelled cannot be 'not cancelled'." (R1-01; today this rule exists only in the verifier brief)
- "A failure row whose condition joins several triggers with 'or' gets a scenario, or a data-variant row, for each trigger." (R2-07, R3-08)
- "When a scenario injects an effect across several unanswered calls, tie the effect to one numbered call, never 'together'." (R1-12, R2-01)

For the cockburn checklist, Contract:
- "Every 'must not' about what the agent tells the customer, and every rule that comes from it, has a contract rule and a rubric dimension that asserts it." (R1-06)

## Interview and reviewers

- **Interview:** none ran. This verification-only trial started at step 4.
- **Finders:** all nine (three per round) ran as native general-purpose subagents on the session model.
- **Verifiers:** all three ran as native general-purpose subagents with `model: sonnet`.
- **Codex:** no reviewer ran through Codex. SKILL.md at 840bee9 names no Codex reviewer, and the harness required native subagents.
