# Agent Spec verification report: Harbor Goods order-support agent (trial it4b-2)

## File and capabilities

- File written: `eval/agent-spec/run-it4b-2/agent-spec.md` (copy at `results/it4b-2/agent-spec-final.md`).
- One capability: **4.1 Cancel Order (CO)**, state-changing, with 30 scenarios. The ids run CO-S01 to CO-S31; CO-S24 is unused. Verification added CO-S25 to CO-S31. Rows added to existing scenarios: CO-S01 row 4, CO-S03 row 4 and CO-S05 row 4.

## Merges (step 3.9) and dropped rows

This run started at step 4.1, so step 3.9 did not run and no merges were made. The checker still prints seven merge-candidate WARNING groups. The added scenarios stay apart from their candidates because their Forbidden lines and dimensions differ: CO-S27 vs CO-S01/02/09/12, CO-S29 vs CO-S01, CO-S25 vs CO-S13.

Verification dropped these rows (both under R1-01):
- **CO-S17 row 3** ("is answered by the order system with the order not cancelled, and creates no refund"). It exercised the CO-A3 `OrderNotCancelled` failure row. The outcome cannot be true right after CO-A2 returned cancelled.
- **CO-S24, the whole scenario, rows 1 and 2** (HG-10482 processing; HG-10511 placed). It exercised the CO-A2 `OrderNotFound` failure row and CO-05's "order system reports the order not found" clause. The outcome cannot be true for an order the lookup has just listed. Its dimension "Order not cancelled reported" was removed with it.

## Input ledger (final, unchanged by this run)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied, the rest proposed and confirmed with changes | interview round 2 Q3, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found, **default accepted**: a state-changing call is authorized only by explicit confirmation of the full proposal; any change voids it | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases, no transcripts | interview round 2 Q4 |

## Tools

The tools `list_orders`, `cancel_order` and `request_staff_followup` are proposed and therefore provisional; `issue_refund` was supplied. Appendix A is the part of the spec that architecture notes may change. This run changed only one Appendix A outcome cell: CO-A3's failed-refund outcome no longer names a `failure_reason` field (R1-04).

## Checker (final run)

```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12, CO-S27: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S29: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S13, CO-S25: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)
```

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S27 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S26, CO-S30, CO-S31 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10, CO-S28 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S27, CO-S29 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27, CO-S29 |
| CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S25, CO-S26, CO-S28 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26, CO-S30, CO-S31 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S25, CO-S26, CO-S28, CO-S30, CO-S31 |
| CO-08 | CO-S01, CO-S16, CO-S19 |

## Findings

**39 findings verified: 24 Important, 15 Nit. 34 kept (20 Important, 14 Nit), 5 dropped. Of the kept: 27 fixed, 1 answered, 6 open, 0 Pre-existing.** All 3 rounds ran, and the run stopped at the round cap with findings still open.

Per round (merged after dropping duplicates):
- Round 1: 16 findings (11 Important, 5 Nit); 14 kept, 2 dropped.
- Round 2: 15 findings (8 Important, 7 Nit); 13 kept, 2 dropped.
- Round 3: 8 findings (5 Important, 3 Nit); 7 kept, 1 dropped.

Round 3 fixes were checked by the checker only; no later finder round saw them.

### Each finding

| id | sev | class | status | one line |
|---|---|---|---|---|
| R1-01 | Important | Lies | fixed (+ open question) | Injected `OrderNotCancelled` after a cancelled result (CO-S17 row 3) and `OrderNotFound` for a listed order (CO-S24) cannot be true. Row and scenario dropped; the OrderNotCancelled row now hands off with reason cancellation unknown. |
| R1-02 | Important | Lies | dropped | Second CO-A3 ProviderUnavailable after a timed-out first. |
| R1-03 | Important | Lies | fixed | The failed/no-refund branch after the re-read now says "not confirmed yet" (round 3 Q3); new dimension for CO-S20. |
| R1-04 | Nit | Lies | fixed | `failure_reason` field removed from Appendix A. |
| R1-05 | Important | Gap | fixed | No-arrival-date ban asserted by a new dimension on CO-S01. |
| R1-06 | Important | Gap | fixed | Confirmation that carries a change: CO-S03 row 4. |
| R1-07 | Important | Gap | fixed | Second CO-A2 timeout now looks up and branches; CO-S15 updated; CO-S25 and CO-S26 added. |
| R1-08 | Important | Gap | fixed | "Refund status reported" now on every success scenario. |
| R1-09 | Nit | Gap | answered | Order absent from an answered lookup: list_orders returns every order, cancelled ones too (tool confirmation change 4). |
| R1-10 | Important | Ambiguous | fixed | CO-S19/S20/S21 say which unanswered CO-A3 creates the refund. |
| R1-11 | Important | Ambiguous | dropped | Retry still required after a lookup shows the outcome. |
| R1-12 | Important | Gap | fixed | Guessed proposal: new dimension on CO-S02; CO-S07 dimension extended. |
| R1-13 | Important | Ambiguous | fixed | CO-07 "once ... created": the CO-S23 dimension says how a statement of intent is read. |
| R1-14 | Nit | Untestable | fixed | "Fewer than one CO-A1 ..." Forbidden line removed. |
| R1-15 | Nit | Ambiguous | open | "The user's confirmation turn" when none occurs: §5.1 fixed text. |
| R1-16 | Nit | Ambiguous | fixed | Turn 2 triggers now name the confirmation question, backed by a (before Turn 2) pair. |
| R2-01 | Important | Lies | dropped | "No refund was issued" in "Cancellation outcome unknown reported". |
| R2-02 | Important | Lies | fixed | The row now proposes only a newly named order; a term change goes to the CO-03 row, at any point; CO-S27 added. |
| R2-03 | Nit | Lies | open | G-04's guarantee clause covers CO-A2 (SG-04) and omits SG-03. Proposed rule change. |
| R2-04 | Important | Gap | fixed | One open order and a request naming none: CO-S01 row 4. |
| R2-05 | Nit (lowered from Important) | Gap | fixed | The first failure row now reads "no lookup ... has answered". |
| R2-06 | Important | Gap | fixed | Already cancelled order with no refund: CO-S28. |
| R2-07 | Important | Gap | fixed | Partial request, then the whole order: CO-S29. |
| R2-08 | Nit | Gap | open | CO-03 joins two statements per trigger while its rows split them. Proposed rule change. |
| R2-09 | Nit | Gap | fixed | Second unanswered CO-A4 on the other two paths: CO-S30, CO-S31. |
| R2-10 | Important | Ambiguous | fixed | "Proposal" defined in the dimensions that turn on it. |
| R2-11 | Important | Ambiguous | fixed | "Not issued" and "not confirmed" dimensions accept each other's wording. |
| R2-12 | Nit | Ambiguous | fixed | "Shipped order explained" accepts "cannot be / was not cancelled". |
| R2-13 | Nit | Untestable | fixed | CO-S20 whole-sentence final-state column replaced by one fixed line. |
| R2-14 | Nit | Untestable | dropped | CO-S02 "the customer's other order". |
| R2-15 | Nit | Untestable | open | Unlimited read retries vs the end-of-trial rule: §5.1 fixed text. |
| R3-01 | Important | Lies | open | CO-07's trigger covers an order already cancelled with no refund, against CO-S28 and the input. Proposed rule change. |
| R3-02 | Nit | Lies | dropped | "failed, card closed" in trajectories. |
| R3-03 | Important | Gap | fixed | CO-S28: no false refund-status claim and no arrival date. |
| R3-04 | Important | Gap | open | Request to cancel more than one order. |
| R3-05 | Nit | Gap | fixed | No open order and no order named: new failure row, CO-S05 row 4. |
| R3-06 | Important | Ambiguous | fixed | "Issued" as verb vs status, defined in the status dimensions. |
| R3-07 | Important | Ambiguous | fixed | CO-S29's whole-order request is now a scripted Turn 2. |
| R3-08 | Nit | Ambiguous | fixed | Scope arrival-date line widened to match round 3 Q1. |

### Fix-introduced vs missed (compared with the saved round copies)

- **Round 2**: 13 kept. **2** quote a line round 1 changed: R2-10 on the new "Order asked before any proposal" dimension and R2-11 on the new "Refund not confirmed reported" dimension. Those are defects the fixes introduced. **11** quote lines round 1 did not change; those are defects earlier finders missed.
- **Round 3**: 7 kept. **3** quote a line round 2 changed: R3-03 ("Already cancelled reported"), R3-06 ("Refund status reported") and R3-07 (the CO-S29 pair). **4** quote unchanged lines: R3-01, R3-04, R3-05, R3-08. R3-01 quotes the unchanged CO-07, but the round-2 CO-S28 fix is what exposed it.

### Verifier drop rate

- **Important: 3 dropped of 24 verified (12.5%).**
  - R1-02. Refutation: SG-01 "repeated calls return the same refund id and never create a second refund", and Appendix A "every later call returns that same refund (SG-01)". A second CO-A3 answered ProviderUnavailable therefore means no refund exists.
  - R1-11. Refutation: the failure row "did not answer it | Make CO-A3 once more, relying on SG-01" is unconditional, and input case 3 says "agent retries once, then re-reads the order and refund records".
  - R2-01. Refutation: G-03 "tells the customer a refund is pending or issued only when ... Otherwise it tells the customer the action was not done".
- **Nit: 2 dropped of 15 verified (13.3%).**
  - R2-14. Refutation: CO-S02 Initial state "The customer's orders are exactly two: HG-10482 ... and HG-10511 ..." fixes "the other order" per row.
  - R3-02, dropped on a Style only verdict. The finding's own Quote, "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed.", words the outcome as Appendix A's outcome cell does ("refund failed (the payment method is closed or expired, or the provider declined)"). Other arrows do the same ("→ payment provider temporarily unavailable"). The finding is about how the arrow is phrased.
- **Not dropped:** R1-04 got a Style only verdict but was kept. It is about a return field no input defines, not about wording.

## Proposed rule changes (rule text unchanged; for the user to decide)

**G-04 (R2-03).**
- Before: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
- After: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or, for CO-A3 and CO-A4, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03)."

**CO-03 (R2-08).**
- Before: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
- After: "When the customer asks to cancel only some items, the agent tells the customer that only the whole order can be cancelled; when the customer asks for a different amount, a different payment method or store credit, the agent tells the customer that the refund is the total paid to the order's payment method; in both cases it proposes nothing else."

**CO-07 (R3-01).**
- Before: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 ..."
- After: "When an order the agent cancelled in this conversation has no refund shown pending or issued after the CO-A3 calls CO-06 allows, or when the agent cannot tell whether the order it tried to cancel in this conversation was cancelled, the agent makes CO-A4 ..."
- The rest of the rule is unchanged. §1 Purpose and the §2 support-team interest would then be worded to match.

## Open questions

- **What if** `issue_refund` returns `OrderNotCancelled`, or `cancel_order` returns `OrderNotFound`, for an order the agent has just seen open or cancelled? The inputs give no cause that an Initial state can set. The two failure rows stand without a scenario, and CO-05's not-found clause has none either (R1-01).
- **What if** a customer asks to cancel two orders in one conversation? Should the agent cancel both, refuse the second, or ask which first? CO-06's "at most two CO-A2 ... in a conversation" and G-01 read as one order (R3-04).
- **What if** a returning customer's order is cancelled but its refund failed or never happened? The input says "changes nothing", while CO-07 as written requires a handoff (R3-01; CO-S28 now asserts "changes nothing").
- **What if** a lookup times out once? Should the agent retry it before taking the no-answer branch, and how many times? The inputs only permit read retries.
- **What if** a trial has no confirmation turn at all? How do "before the user's confirmation turn" lines score? This is §5.1 fixed text (R1-15).
- **What if** the agent keeps retrying a lookup the scenario never answers? §5.1 "End of trial" counts only agent messages (R2-15).
- The three proposed rule changes above.

## What verification cannot catch

Two things only the user can confirm:
- whether these rules are Harbor Goods' real rules;
- whether the stakeholder list (customer, order system, store staff, Harbor Goods, the support team, other customers) is complete.

## Proposed checklist lines (kept findings whose pattern no checklist covers)

- evaluation-checklist: **A term a dimension turns on is defined.** A rubric dimension that turns on a word the spec also uses for something else ("proposal" vs informing; "issued" as the action vs the status) defines the word in the dimension (R2-10, R3-06).
- evaluation-checklist: **An acting branch needs a required question or a scripted turn.** When a scenario's acting branch depends on a customer turn that no rule makes the agent ask for, script it as a User turn on a defined event instead of a User-knows answer (R3-07).
- evaluation-checklist: **Confirmed wording wins, and parallel dimensions agree.** A failure row's required message uses the wording the inputs confirmed for that branch. Two dimensions for the same visible fact accept each other's wording (R1-03, R2-11).
- cockburn-checklist: **Triggers anchor to this conversation.** A rule whose trigger is a world-state condition ("the order is cancelled") names the agent's own actions in this conversation whenever an existing record can already be in that state (R3-01).
- cockburn-checklist: **A retried call's timeout row branches too.** The timeout row for a retried commit call carries the same lookup branches as the first-timeout row (R1-07).
- template §5.1: define how a line anchored on "the user's confirmation turn" reads when no confirmation turn occurs, and when a trial ends if the agent never sends a message (R1-15, R2-15).

## Interview

This run started at step 4.1 and ran no interview. The review packet records the interview rounds verbatim but does not say which interview skill produced them.
