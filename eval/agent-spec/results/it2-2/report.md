# Step-5 report — trial it2-2 (verification-only, skill commit a5e1880)

## File written

`eval/agent-spec/run-it2-2/agent-spec.md` (copy in this folder as `agent-spec-final.md`). One capability:

- **4.1 Cancel Order (state-changing), prefix CO: 27 scenarios.** CO-S01 to CO-S23 and CO-S25 to CO-S28. Id CO-S24 is unused because it was removed in round 1 (R1-07).

Scenarios added by verification: CO-S25, CO-S26, CO-S27 (round 1, R1-01) and CO-S28 (round 3, R3-03). Data-variant rows added: CO-S01 row 4 (R3-04), CO-S03 rows 4–5 (R1-02), CO-S05 row 4 (R1-06) and CO-S06 row 3 (R2-05).

## Merges of step 3.9 and dropped rows

This run started at step 4.1, so no step-3.9 consolidation ran and no WARNING groups were merged. The final checker prints eight merge-candidate WARNINGs. Each group stays apart because its scenarios differ in Forbidden lines, Initial-state failures or dimensions.

Rows and scenarios that verification removed:
- **CO-S17 row 3** exercised `OrderNotCancelled` from CO-A3 right after a CO-A2 that returned cancelled. That outcome could not be true at that call (R1-07).
- **CO-S24, whole scenario** exercised `OrderNotFound` from CO-A2 for an order the lookup had just listed. It went with its dimension "Order not cancelled reported" (R1-07).

## Input ledger, final state

The ledger is unchanged from the review packet:

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial: `issue_refund` was supplied; the rest were proposed and confirmed with the user's changes |
| 3 | Data model | found |
| 4 | Authorization policy | found, default accepted: a cancellation happens only after explicit confirmation of the full proposal; any change voids the confirmation |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases, no transcripts |

## Proposed tools

The tools are `list_orders()`, `cancel_order(order_number)` and `request_staff_followup(order_number, reason)`, all proposed and confirmed, plus `issue_refund(order_number)`, which the user supplied.

They are provisional. Appendix A is the part of the spec that architecture notes may change. Verification changed Appendix A once: round 2 removed the invented `failure_reason` field from the CO-A3 result (R2-04).

## Checker

Final run, after round 3: **0 errors**, with 8 merge-candidate WARNINGs (full output in run.log). Coverage table:

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S26, CO-S27 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S28 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S28 |
| CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S25, CO-S26 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26, CO-S27 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S27 |
| CO-08 | CO-S01, CO-S16, CO-S19 |

## Findings

**36 findings verified: 21 Important, 15 Nit. 26 kept (15 Important, 11 Nit), 10 dropped. 3 rounds run (cap reached, not converged).**

Round count lines (merged; finder severity; the verifier lowered no severity):
- Round 1: 15 findings: 9 Important, 6 Nit. 12 kept (8 Important, 4 Nit), 3 dropped.
- Round 2: 9 findings: 8 Important, 1 Nit. 6 kept (5 Important, 1 Nit), 3 dropped.
- Round 3: 12 findings: 4 Important, 8 Nit. 8 kept (2 Important, 6 Nit), 4 dropped.

Status of the 26 kept findings: 20 fixed, 1 answered, 5 open. None were Pre-existing, because this is not an update run.

### Kept findings, by round

| Id | Class / severity | Status | Fix or reason |
|---|---|---|---|
| R1-01 | Lies/Gap, Important | fixed | The second-unanswered-CO-A2 row now looks up and branches. Added CO-S25, CO-S26, CO-S27. |
| R1-02 | Gap, Important | fixed | CO-S03 rows 4–5 carry a "yes" together with a changed order. |
| R1-03 | Gap, Important | fixed | Added dimensions "Refund status reported" and "No arrival date promised" to the 9 success scenarios. The contract rule is proposed below. |
| R1-05 | Gap, Important | open | A request to cancel several orders is for the user to decide. |
| R1-06 | Gap, Nit | fixed | New failure row for an unnamed request with no open order. Exercised by CO-S05 row 4. |
| R1-07 | Lies, Important | open | Partly fixed: CO-S17 row 3 and CO-S24 removed, and the not-cancelled row no longer claims the order is cancelled. When the two outcomes can really occur is for the user to decide. |
| R1-08 | Lies, Important | fixed | The CO-S20 branch now says "not confirmed yet", as round 3 Q3 has it. New dimension "Refund not confirmed reported". |
| R1-09 | Lies/Ambiguous, Nit | open | Proposed rule change to G-04 (below). |
| R1-11 | Gap, Important | fixed | Added dimension "Which order asked first" to CO-S02. |
| R1-12 | Ambiguous, Important | fixed | CO-S19, CO-S20 and CO-S21 now give each unanswered CO-A3 its own effect. |
| R1-14 | Ambiguous, Nit | fixed | The Turn 2 trigger in CO-S03 and CO-S04 is now named by its three stated values. |
| R1-15 | Untestable, Nit | answered | The end-of-trial rule is §5.1 fixed text, which step 4 does not edit. Unlimited reads are the user's own rule. |
| R2-01 | Lies, Important | fixed | When the lookup still shows the order open after the second unanswered cancel, the agent now hands off as "cancellation unknown". CO-S27 was rewritten. |
| R2-04 | Lies, Nit | fixed | `failure_reason` removed from Appendix A. |
| R2-05 | Gap, Important | fixed | CO-S06 row 3: an already cancelled order with a failed refund changes nothing, per the packet. A CO-07 clarification is proposed below. |
| R2-06 | Ambiguous, Important | fixed | Added "A second CO-A3." to CO-S02 and CO-S03. |
| R2-08 | Ambiguous, Important | fixed | "Refund not confirmed reported" now also accepts "has not been issued" or "failed". |
| R2-09 | Ambiguous, Important | fixed | The two dimensions now say "asks to go ahead with cancelling" in place of the undefined "propose". |
| R3-02 | Lies, Nit | fixed | Removed the unsupported SG-04 citation from the row and from the CO-S27 note. |
| R3-03 | Gap, Important | fixed | New CO-S28: the customer asks to cancel some items, then the whole order. |
| R3-04 | Gap, Nit | fixed | The unanswered-lookup row now retries. CO-S01 row 4 exercises it. |
| R3-05 | Gap, Nit | open | A refund returned with the wrong amount or payment method is for the user to decide. |
| R3-06 | Gap, Nit | fixed | Added "A second CO-A2." to 9 scenarios. |
| R3-08 | Ambiguous, Important | fixed | "Refund terms explained" now says that stating the amount counts. |
| R3-09 | Untestable, Nit | fixed | "before the user's confirmation turn" is now "with no user's confirmation turn before it" in the 4 Forbidden lines that used it, and CO-S28 uses the same form. |
| R3-12 | Ambiguous, Nit | open | Defining "propose" in CO-01 to CO-03 is a proposed rule change. |

### Fix-introduced versus missed defects

Each kept finding was attributed by diffing `round<N-1>/agent-spec.md` against `round<N>/agent-spec.md`:

- **Round 2:** 3 of 6 kept findings quote a line round 1 changed, so a fix introduced the defect: R2-01 (R1-01 branch), R2-08 (R1-08 wording) and R2-09 (R1-11 dimension). The other 3 quote lines round 1 did not change, so earlier finders missed them: R2-04, R2-05 and R2-06.
- **Round 3:** 1 of 8 kept findings quotes a line round 2 changed: R3-02, on the R2-01 row. The other 7 quote lines round 2 did not change: R3-03, R3-04, R3-05, R3-06, R3-08, R3-09 and R3-12. R3-06 and R3-09 follow patterns that round 1 and 2 fixes had touched nearby: the R2-06 Forbidden lines and the CO-S03 rows round 1 added.

### Verifier drop rate

- **Important: 6 dropped of 21 verified (29%).**
- **Nit: 4 dropped of 15 verified (27%).**

Dropped findings and the refutations quoted:
- **R1-04 (Important).** "CO-S01 is the side where the condition is false: Turn 1 'Please cancel order HG-10482.' names the order, and the reference trajectory goes from CO-A1 straight to the proposal." I agreed: CO-02 has both an acting scenario and a holding-back one.
- **R1-10 (Nit).** "Round 3 Q3 ... 'terminal = payment method can no longer receive money (card closed or expired) or the provider declines'. That is exactly `payment_method_closed`, `payment_method_expired` and `declined`." The verifier later ruled the same defect Real as R2-04, and it was fixed.
- **R1-13 (Nit).** "'cannot be cancelled' means the order was not cancelled. So an agent that follows CO-S05's failure row meets 'has shipped (or been delivered) and was not cancelled'."
- **R2-02 (Important).** "G-03 ... 'Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown.' In CO-S14 and CO-S15 the agent made no CO-A3, so it knows the refund was not done, and G-03 requires it to say so."
- **R2-03 (Important).** "CO-03 settles the case: 'Every proposal cancels the whole order and refunds its total paid to its payment method ... and proposes nothing else.'"
- **R2-07 (Important).** "The failure row that governs CO-S16 row 2 makes the retry required: 'Make CO-A3 once more, relying on SG-01.' A run that looks up and stops without the retry breaks that row."
- **R3-01 (Important).** The same G-03 refutation as R2-02: "the 'Otherwise' covers the refund action as well as the cancellation."
- **R3-07 (Important).** "The CO-A3 row at line 103 is a requirement, not a permission ... 'Make CO-A3 once more, relying on SG-01.', with no exception for a lookup made in between."
- **R3-10 (Nit).** "An order the agent says 'has shipped and cannot be cancelled' ... is an order the agent says was not cancelled."
- **R3-11 (Nit).** "A refund the order system returned as 'failed' is a refund that 'has not been issued', so a report that it failed meets the definition on meaning."

Three rounds re-reported a defect that an earlier round had dropped: R2-07 then R3-07, R2-02 then R3-01, and R1-13 then R3-10. answered.md lists only kept findings, so the later finders could not see the drops.

The verifier also returned "Not real" on R1-05, but I kept the finding. The clause it quoted covers an ambiguous request, not a customer who names two orders.

## Proposed rule changes

The skill stops a fix at rule text, so each of these is for the user to decide:

1. **G-04 (R1-09).**
   - Before: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
   - After: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or, for CO-A3 and CO-A4, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01 for CO-A3, SG-03 for CO-A4). It never repeats CO-A2 without such a lookup."
2. **No arrival date (R1-03).**
   - Before: no rule. The only statement is the Scope & Authority line "must not ... promise a date by which the refunded money arrives".
   - After: append to CO-03: "The agent states no date or time span by which the refunded money arrives."
3. **CO-07 (R2-05).**
   - Before: "... CO-A4 occurs in no other situation."
   - After: "... CO-A4 occurs in no other situation; an order already cancelled before the conversation is reported under CO-01 and gets no CO-A4."
4. **"Propose" (R3-12).**
   - Before: undefined.
   - After: add to CO-01: "To propose is to ask the customer to go ahead with cancelling a particular order; telling the customer which orders can be cancelled and what each refund would be is not proposing."

## Open questions

- **R1-05.** What if the customer asks to cancel two of their open orders in one conversation? Does the agent handle one, ask which one, or do both? CO-06's per-conversation caps assume one order.
- **R1-07.** What if `cancel_order` returns `OrderNotFound`, or `issue_refund` returns `OrderNotCancelled`, for an order the lookup showed? Can either really happen to an agent that follows CO-02 and CO-05? Until you answer, those two failure rows, and CO-05's not-found clause, have no scenario.
- **R2-01.** What if the second cancellation goes unanswered and the lookup still shows the order open? The spec now hands this off as "cancellation unknown". Should store staff follow up here, or should the agent report "not cancelled"?
- **R2-05.** What if a customer comes back about an order that is already cancelled but whose refund failed or never ran? The spec now says nothing changes, per the packet. Should store staff get a task?
- **R3-05.** What if `issue_refund` returns a refund whose amount or payment method differs from the order's?
- The four proposed rule changes above.

## What verification cannot catch

Verification cannot tell whether these rules are Harbor Goods' real cancellation and refund rules. It also cannot tell whether the stakeholder list is complete: the customer, the order system, store staff, Harbor Goods, the customer-support team and other customers. Only the user can confirm both.

## Proposed checklist lines

These kept-finding patterns are not covered by any checklist:

- **cockburn-checklist, Failure.** "A row for a repeated unanswered commit call looks up and branches like the row for the first, and does not go straight to 'unknown'." (R1-01)
- **evaluation-checklist.** "When several unanswered calls share an effect, Initial state gives each call its own effect, so a read between them sees a defined world." (R1-12)
- **evaluation-checklist.** "A rubric definition says whether stating a value, or a truthful stronger statement, meets a required statement." (R2-08, R3-08)
- **evaluation-checklist.** "A Forbidden line anchored on a turn that may never occur is written so it is decidable when the turn is absent ('with no confirmation turn before it')." (R3-09)
- **evaluation-checklist.** "Every scenario that requires a commit call 'exactly N times' also forbids an N+1th, so partial credit is uniform." (R2-06, R3-06)
- **Template §5.1.** End of trial does not handle an agent that keeps calling a read that never answers (R1-15). §5.1 needs a bound on tool calls, or a verdict for a trial that never yields a message.

## Interview

No interview ran in this trial: it was a verification-only run that started at step 4.1. The review packet does not say which interview skill ran when the spec was written.
