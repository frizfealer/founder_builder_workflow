# Agent Spec verification report — it4b-1

Verification-only run of the agent-spec skill at 9fe669b: step 4 from 4.1, on eval/agent-spec/round0-agent-spec.md. The 4.2 packet was supplied, and steps 1–3 did not run in this trial.

## File written

`eval/agent-spec/run-it4b-1/agent-spec.md` (copy: `results/it4b-1/agent-spec-final.md`).

- **4.1 Cancel Order (CO), state-changing:** 27 scenarios, CO-S01 to CO-S28. The id CO-S24 is unused because round 1 removed that scenario.
- **New in verification:** CO-S25 (second cancel unanswered, order shipped meanwhile), CO-S26 (partial request, then the whole order), CO-S27 (cancellation unknown, handoff unanswered twice) and CO-S28 (refund status unknown, handoff unanswered twice).
- **New rule:** CO-09 (no promise about when the money arrives).

## Step 3.9 merges and dropped rows

Step 3.9 did not run, because this trial starts at step 4. The checker's merge WARNINGs are listed below; each group stays apart:

| Group | Why it stays apart |
|---|---|
| CO-S01, S02, S03, S12 | Different User and User-knows blocks, different Initial-state failures (S12) and different Forbidden lines. |
| CO-S01, S02, S09, S12 | Same as above. |
| CO-S01, S26 | CO-S26 has an extra which-whole-order pair and a partial-items request. |
| CO-S16, S19 | Different final state checks (refund status column) and different lookups. |
| CO-S18, S20 | S20 requires a lookup before the handoff, and its final refunds differ. |
| CO-S22, S23 | S22 ends with a task. S23 ends with none and a different report. |

Rows removed during verification, each with what it exercised:

| Removed | What it exercised | Why removed |
|---|---|---|
| CO-S17 row 3 | `issue_refund` → `OrderNotCancelled` right after `cancel_order` returned cancelled | That outcome cannot be true at that call (R1-02). |
| CO-S24, all rows | `cancel_order` → `OrderNotFound` for an order `list_orders` had just returned | Same reason (R1-02). |

Both outcomes keep their failure rows. They now have no scenario (open question 3).

## Input ledger (final, from the review packet)

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial: `issue_refund` supplied, the rest proposed and confirmed with changes |
| 3 | Data model | found |
| 4 | Authorization policy | found. Default accepted: a state-changing call is authorized only by the customer's explicit confirmation of the full proposal, and any change voids it. |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases, no transcripts |

## Tools

These are provisional:

- `list_orders()`: read, proposed.
- `cancel_order(order_number)`: proposed.
- `request_staff_followup(order_number, reason)`: proposed.
- `issue_refund(order_number)`: supplied by the user.

Appendix A is the part of the spec that architecture notes may change. Verification changed Appendix A once: the `issue_refund` return is now `{refund_id, order_number, amount, payment_method, status}`, and the `failure_reason` field, which no input supplied, is gone (R1-05).

## Checker

Final run: **0 errors**, 6 WARNING groups (listed above).

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S25, CO-S27, CO-S28 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S27 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S26 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S26 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S13, CO-S25 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S27, CO-S28 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S27, CO-S28 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01 |

## Findings

**38 findings: 23 Important, 15 Nit.** 3 rounds ran; the run stopped at the round cap, and round 3 still changed the spec.

| Round | Count line | Raw | Kept | Dropped | Verifier |
|---|---|---|---|---|---|
| 1 | 18 findings: 10 Important, 8 Nit. | 22 | 17 | 1 | Real 11, Not real 2, Style only 5 |
| 2 | 11 findings: 8 Important, 3 Nit. | 14 | 11 | 0 | Real 10, Style only 1 |
| 3 | 9 findings: 5 Important, 4 Nit. | 11 | 8 | 1 | Real 8, Style only 1 |

**Outcome:** 30 fixed, 6 open, 2 dropped, 0 answered outright, 0 Pre-existing. Several findings were fixed in part, and the rest of each stands as listed:

- R1-01: two lookup branches are open questions.
- R1-02: no scenario can inject the two outcomes.
- R1-03: part (a) answered, because G-03 requires it.
- R1-13: the after-confirmation case is answered; no scripted turn can arrive there.
- R2-03, R2-05, R3-01: each also proposes a rule change.

Every finding is in `round<N>-findings.md` with its verifier line and decision.

**Round 1**

| Finding | Status | What it was and what changed |
|---|---|---|
| R1-01 | fixed in part, open | The second unanswered cancel skipped the re-read. That row now re-reads and branches; CO-S13 row 2 and CO-S25 cover it. |
| R1-02 | fixed, open | `OrderNotCancelled` and `OrderNotFound` were injected where they cannot be true. CO-S17 row 3 and CO-S24 removed. |
| R1-03 | fixed (b) | After the re-read, a refund still unfinished is reported as "not confirmed yet", per the input. |
| R1-04 | open, rule proposal | The input never asks for the refund id. Rule CO-08 would change. |
| R1-05 | fixed | Invented `failure_reason` field removed. |
| R1-06 | fixed | The must-not line was narrower than the input ("a date by which"). |
| R1-07 | fixed | No rule or dimension forbade promising when the money arrives. Added CO-09 and "No arrival time promised". |
| R1-08 | open, rule proposal | G-04 names only SG-01. |
| R1-09 | fixed | A data-variant column held a whole Expected line. |
| R1-10 | fixed | CO-S06 listed CO-05 under Illustrates without exercising it. |
| R1-11 | fixed | The lookup failure row fired on a single timeout. |
| R1-12 | fixed | The which-order question was not graded. |
| R1-13 | fixed in part | A change inside the confirming turn had no scenario. Added CO-S03 row 4. |
| R1-14 | fixed | Initial state did not say which unanswered refund call created the refund. |
| R1-15 | dropped | See the verifier drop rate below. |
| R1-16 | open | Unbounded reads mean a trial need never end. |
| R1-17 | fixed | A scripted-turn trigger was not a §5.1 event. |
| R1-18 | fixed | Dimensions did not grade when "staff will follow up" may be said. |

**Round 2**

| Finding | Status | What it was and what changed |
|---|---|---|
| R2-01 | fixed | CO-S15's trajectory and Forbidden block still followed the old row. |
| R2-02 | fixed | An answered retry after an unanswered first refund call skipped the re-read. CO-S20 rows 3 and 4 added. |
| R2-03 | fixed, open | "Refund not confirmed reported" now accepts either statement. G-03 rule change proposed. |
| R2-04 | fixed | Stale "card closed" left in tool results. |
| R2-05 | fixed in part, open | Added CO-S09 row 4 for a different amount. CO-03 rule change proposed. |
| R2-06 | fixed | An already-cancelled order with a failed refund or no refund had no scenario. Added CO-S06 rows 2 and 3. |
| R2-07 | fixed | One dimension was missing the timing clause. |
| R2-08 | open | An order described by item or date that matches none of the customer's orders has no row. |
| R2-09 | fixed | A dimension relied on "proposal", which the spec never defines. It now uses the §5.1 confirmation question. |
| R2-10 | fixed | CO-S05 shared a dimension whose wording fits only an attempted cancellation. New dimension "Shipped order refused". |
| R2-11 | fixed | CO-S19's status report was not tied to the lookup. |

**Round 3**

| Finding | Status | What it was and what changed |
|---|---|---|
| R3-01 | fixed in part, open | CO-07, §2 and §1 contradicted the already-cancelled row. §1, §2 and CO-S06's Illustrates fixed. CO-07 rule change proposed. |
| R3-02 | dropped | See the verifier drop rate below. |
| R3-03 | fixed | Nothing graded the refund status the agent reports on the direct path. New dimension "Refund pending reported" on 8 scenarios. |
| R3-04 | fixed | A partial request followed by a request for the whole order had no scenario. Added CO-S26. |
| R3-05 | fixed | `OrderNotCancelled` on a retry fell in no row. |
| R3-06 | fixed | Two unanswered handoffs were graded for only one of the three reasons. Added CO-S27 and CO-S28. |
| R3-07 | fixed | "message" left out text sent alongside a tool call. |
| R3-08 | fixed | The "Refund terms explained" dimension could not tell an agent that explained the terms from one that silently ignored the request. |
| R3-09 | fixed | The anchor "before the user's confirmation turn" had no reading when no confirmation turn occurs. |

**Did a kept finding quote a line the previous round changed?** Compared with diff of the saved round copies:

- **Round 2:** 3 of 11 quote a line round 1 changed: R2-03, R2-09, R2-10. R2-10's defect is older; round 1 only added CO-S25 to that row. The other 8 quote unchanged lines. Of those 8, R2-01, R2-04 and R2-07 are leftovers of round-1 fixes that did not reach every instance of their pattern. The other 5 are defects the round-1 finders missed.
- **Round 3:** 2 of 8 quote a line round 2 changed: R3-01 (CO-S06 Illustrates) and R3-05 (a CO-A3 row). The other 6 quote unchanged lines. Of those 6, R3-07 is a defect introduced by the round-1 fix R1-18; round 2 copied it into a fourth dimension. R3-03, R3-04, R3-06, R3-08 and R3-09 were missed earlier.

**Verifier drop rate:** Important 1 of 23 dropped; Nit 1 of 15 dropped.

- **R1-15 (Important)**, dropped on the verifier's Not real. Its refutation: "Row 102 settles the case: for an unanswered first CO-A3, 'Make CO-A3 once more, relying on SG-01'. That is a requirement with no condition, not a permission." Packet case 3 also says "agent retries once".
- **R3-02 (Nit)**, dropped on a Style only verdict. The finding's own Quote was: "3. Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation." Reason for the drop: it concerns the wording of a described agent turn that no grader reads, and the ambiguity it points to is R3-08, which was kept and fixed.

Kept against a refuting verdict:

- R1-03: the refutation answered part (a) only; part (b) stands on the input's "not confirmed yet".
- R1-05, R1-08, R1-09, R1-10, R1-17 and R2-04: each got Style only, but each is about content, not wording.

## Open questions

1. What if a lookup after the second unanswered `cancel_order` shows the order still placed or processing? The cancel limit is spent, and CO-07 allows a handoff only when the agent cannot tell whether the order was cancelled.
2. What if a lookup after an unanswered `cancel_order` answers but no longer lists the order?
3. What if `cancel_order` returns `OrderNotFound` for an order `list_orders` just returned, or `issue_refund` returns `OrderNotCancelled` after `cancel_order` returned cancelled? The tool set declares both outcomes, but no Initial state consistent with the spec reaches them for a correct agent. Do they stay as failure rows with no scenario?
4. What if `list_orders` keeps timing out? Reads may be retried without limit, but a trial ends only on an agent message or at the 12-message cap. How many retries before the agent tells the customer the orders cannot be checked?
5. What if the customer describes an order by item or date, and the description matches none of their orders?
6. What if the customer changes a proposal term after confirming but before `cancel_order` goes out? No scripted turn can arrive at that point unless the agent yields there.
7. Proposed rule changes, held back because a fix that changes a rule's text stops at the rule. Before and after for each is in runner-notes.md:
   - **CO-08:** report the refund status instead of the refund id (R1-04).
   - **G-04:** name SG-03 for a handoff, and repeat a cancellation only after a lookup (R1-08).
   - **G-03:** allow "not confirmed yet" after a retried refund (R2-03).
   - **CO-03:** one statement per trigger (R2-05).
   - **CO-07:** limit the handoff trigger to an order the agent cancelled in this conversation (R3-01).

## What verification cannot catch

Whether these rules are Harbor Goods' real rules, and whether the stakeholder list is complete. Only the user can confirm those.

## Proposed checklist lines

These patterns from kept findings are not covered by any checklist:

- **evaluation checklist:** "An injected outcome is one a correct agent can meet: its Appendix A condition holds at that call, given Initial state and the results of earlier calls." (R1-02)
- **evaluation checklist, Graders:** "A timing limit in a rubric definition covers any text the agent sends, not only agent messages." (R3-07)
- **evaluation checklist, Graders:** "A rubric 'tells the customer' clause names what the agent must say beyond the values the proposal already states." (R3-08)
- **evaluation checklist:** "An event line anchored on a labelled turn says how it reads when that turn never occurs." (R3-09)
- **use-case checklist, Failure:** "A fix that narrows a failure row is checked against the rule, the stakeholder interest and the purpose lines that state the wider behavior." (R3-01, R2-01)
- **use-case checklist, Failure:** "After an unanswered commit call is retried, every way the retry can resolve leads back to the re-read the inputs require." (R1-01, R2-02)

## Interview

None ran. This trial starts at step 4, so steps 1 and 2 were not run.
