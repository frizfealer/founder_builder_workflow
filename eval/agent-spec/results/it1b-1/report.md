# Agent-spec verification report: it1b-1

Verification-only trial of the agent-spec skill at commit 9b7479f. Step 4 ran from 4.1 on `eval/agent-spec/round0-agent-spec.md` (copied to `eval/agent-spec/run-it1b-1/agent-spec.md`), with the frozen review packet. Step 4.2 was skipped, as instructed. The run stopped at the round cap (3 rounds), and every round changed the spec.

## File written and scenario counts

- `eval/agent-spec/run-it1b-1/agent-spec.md`, copied as `results/it1b-1/agent-spec-final.md`.
- One capability, **4.1 Cancel Order (CO), state-changing**. It now has 27 scenarios (CO-S01..CO-S27); it had 24 before the run.
  - Added in round 1: CO-S25 (second cancel goes unanswered, a lookup shows the order cancelled, refund issued) and CO-S26 (second cancel goes unanswered or is rejected, and the order has shipped).
  - Added in round 3: CO-S27 (a "yes, but refund it elsewhere" turn in reply to the proposal).
- Rules: G-01..G-04 and CO-01..CO-09. CO-09 ("No promised arrival date") was added in round 1. The text of every existing rule is unchanged.

## Merges (step 3.9) and dropped rows

The run started at step 4, so step 3.9 did not run and no scenarios were merged. The checker prints seven merge-candidate WARNING groups. Step 4 does not merge, so they are left as they are. Two of the groups involve scenarios this run added: CO-S13/CO-S25 (Forbidden lines and trajectory differ) and CO-S01/S02/S09/S12/S27.

Two rows were dropped by fixes in step 4:

| Dropped row | What it exercised | Why it was dropped |
|---|---|---|
| CO-S16 row 2 (first CO-A3 unanswered but created RF-5531, retry returns it) | A late-landing refund plus an SG-01-safe retry | M13: a lookup between the two refund calls would show the refund, so a compliant agent could stop and fail "exactly twice" |
| CO-S17 row 3 (CO-A3 answered OrderNotCancelled) | The OrderNotCancelled clause of the CO-A3 failure row | M2: impossible right after a CO-A2 that returned cancelled. The clause now has no scenario (open question 2) |

## Input ledger (final, unchanged from the packet)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied by the user, the rest proposed and confirmed with changes | interview round 2 Q3, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found (**default accepted**: a state-changing call needs explicit confirmation of the full proposal; any change voids it) | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases named by the user, no transcripts | interview round 2 Q4 |

## Tools

- **Supplied:** `issue_refund(order_number)`.
- **Proposed and confirmed with the user's changes:** `list_orders()`, `cancel_order(order_number)`, `request_staff_followup(order_number, reason)`.

The proposed tools are provisional. Appendix A is the part of the spec that architecture notes may change. This run changed Appendix A in one place: it removed `failure_reason` from the CO-A3 outcomes (M5).

## Checker (final run, round 3 after fixes)

`0 errors`. Seven WARNING merge-candidate groups (see `run.log`). Coverage table:

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S27 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S25, CO-S26 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S27 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S24, CO-S25, CO-S26 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01 |

## Findings

**33 findings: 18 Important, 15 Nit.** 3 rounds run. 30 kept, 3 dropped. Of the kept findings, 23 were fixed, 7 are open, 0 were answered, and 0 are Pre-existing (the scope was the whole spec).

| Round | Count line | Kept | Dropped | Fixed | Open |
|---|---|---|---|---|---|
| 1 | 14 findings: 8 Important, 6 Nit | 13 | 1 (M7) | 11 | 2 (M4, M10) |
| 2 | 9 findings: 4 Important, 5 Nit | 8 | 1 (N1) | 5 | 3 (N6, N8, N9) |
| 3 | 10 findings: 6 Important, 4 Nit | 9 | 1 (P4) | 7 | 2 (P5, P9) |

Each finding's text, its verifier line and its fix are in `round1-findings.md`, `round2-findings.md` and `round3-findings.md`. In short:

- **Round 1.** Fixed:
  - M1: the second cancel timeout skipped the re-read;
  - M2: injected outcomes were impossible at their call (CO-S17 row 3, CO-S24);
  - M3: CO-S20 said "has not been issued" where the user said "not confirmed yet";
  - M5: `failure_reason` is not in the data model;
  - M6: no scenario for a change in the confirming turn;
  - M8: the no-arrival-date promise was not asserted;
  - M9: unnamed requests with one or zero open orders;
  - M11: the timing of "staff will follow up" was not graded;
  - M12: "proposes nothing" was not asserted in the infeasible scenarios;
  - M13: "together they create" left the refund's origin open;
  - M14: a Forbidden line written as "fewer than one".

  Open: M4 (a G-04 rule change, proposed below) and M10. Dropped: M7.
- **Round 2.** Fixed:
  - N2: the failure cause was still shown as a tool result;
  - N3: "propose" was undefined in the dimensions and triggers;
  - N4: a final-state column held a whole assertion line;
  - N5: CO-S02 passed a guessed proposal;
  - N7: the already-cancelled branch ignored a failed refund.

  Open: N6 (needs §5.1 fixed text), N8, N9. Dropped: N1.
- **Round 3.** Fixed:
  - P1: the M1 fix's "not cancelled, no handoff" branch contradicts SG-04's late effect;
  - P2: the which-order question counted as an offer;
  - P3: the no-offer clauses were wider than the rules;
  - P6: CO-S06 named CO-05 under Illustrates;
  - P7: CO-S05's note misquoted its dimension;
  - P8: a "yes, but" in the confirming turn for a fixed refund term;
  - P10: CO-03's two-part statement was split across rows and dimensions.

  Open: P5 (unbounded unanswered lookups) and P9. Dropped: P4.

### Proposed rule change (M4, for the user to decide)

G-04, before:
> After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).

Proposed after:
> After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or, for CO-A3 and CO-A4 only, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03).

The reason: SG-04 makes cancellation idempotent, so the guarantee clause as written also licenses a blind resend of CO-A2. Round 3 Q4 forbids that resend ("no blind resend; re-read the order").

### Attribution (each kept finding's quoted line checked against the previous round's change, by comparing the saved round snapshots)

- **Round 2:** 8 kept findings.
  - 3 quote a line round 1 changed (fix-introduced): N3 (the verdicts quote of the rewritten "Order not found reported"), N7 and N8 (the cancelled and shipped failure rows reworded by M9).
  - 5 quote a line round 1 did not change (missed earlier): N2, N4, N5, N6, N9.
  - Caveats: N2's defect was caused by the M5 fix even though its quoted trajectory line is unchanged. N7's defect (the refund is ignored on the cancelled branch) predates M9's rewording.
- **Round 3:** 9 kept findings.
  - 3 quote a line round 2 changed (fix-introduced): P2 (the "Asked which order first" dimension added by N5), P3 (the dimensions rewritten by N3) and P7 (the CO-S05 note rewritten by N3).
  - 6 quote a line round 2 did not change: P1, P5, P6, P8, P9, P10.
  - Caveat: P1 quotes a branch that round 1's M1 fix introduced and round 2's finders missed. By quote it counts as "not changed by the previous round", but its cause is a fix two rounds back.

### Verifier drop rate

**3 / 18** Important findings dropped over Important findings verified (round 1: 1/8, round 2: 1/4, round 3: 1/6). Each dropped finding, with its refutation:

- **M7** (success paths never assert the stated refund status). Refutation: "A dimension asserts the rule, so the case falls outside the Gap class. The refund-status clause of G-03 is asserted by 'Refund status reported' (line 1507: 'states no other status for it', used by CO-S19). The failure dimensions also assert it: 'never says a refund is pending or issued'... Known failure case 3 ... maps to CO-S19, CO-S20 and CO-S21, not to CO-S16."
- **N1** (rubrics require "no refund was issued" and "the order is cancelled" beyond their rows). Refutation: "G-03 says the agent 'tells the customer a refund is pending or issued only when ... Otherwise it tells the customer the action was not done'. In both scenarios no CO-A3 is made, so G-03 requires the agent to say the refund was not done ... §2 says the primary actor 'wants to be told truthfully whether the order was cancelled and where the refund stands'."
- **P4** (a payment method stated without its brand). Refutation: "§5.1 (line 1588) says 'its values on equality' and 'A question about only some of those values is not the confirmation question' ... The inputs fix the value itself as brand plus last four ... Whether such a question counts as partial or as wrong-value, the simulated user deflects it, so the verdict is the same for both readers."

One finding was kept against a Not real verdict. **M3**: the verifier pointed to known failure case 3, "Final message must match the final refund status". I did not agree that this refutes the finding. Round 3 Q3 is the user's specific wording for exactly this branch ("failed or no refund, hand off and say the refund is not confirmed yet"), and the rubric grades the wording.

## Open questions

1. What if the order is still placed or processing after two unanswered cancellations? The spec now treats this as "unknown" and hands off (P1). Should the customer be told something else, such as "not cancelled"?
2. What if `issue_refund` returns OrderNotCancelled? A rule-following agent cannot meet this outcome, so the CO-A3 failure-row clause has no scenario (M2). Should the outcome stay, and what should the agent say?
3. What if a lookup after an unanswered call no longer lists the order (M10)?
4. What if the customer asks about an already-cancelled order whose refund failed, or that has no refund (N7)? Should the agent hand it to store staff? The spec follows "reports that and changes nothing".
5. What if the customer names no order and has no orders, or has several orders and none is open (N8)?
6. What if `issue_refund` returns a refund whose amount or payment method differs from the order's (N9)?
7. What if a lookup never answers? How many unanswered lookups count as "the lookup does not answer", and when does a trial end for an agent that keeps reading (P5)? §5.1 End of trial is fixed text.
8. What if the customer wants to cancel a second order in the same conversation (P9)? CO-06 and G-01 limit one conversation to one order.
9. What if no confirmation turn ever occurs? How is "CO-A2 before the user's confirmation turn" read then (N6)? The fix belongs in the template's §5.1.
10. Should G-04's guarantee clause be limited to CO-A3 and CO-A4 (M4, the proposed rule change above)?

## What verification cannot catch

Verification cannot show whether these rules are Harbor Goods' real business rules, or whether the stakeholder list (customer, order system, store staff, Harbor Goods, support team, other customers) is complete. Only the user can confirm either.

## Proposed checklist lines (kept findings whose pattern no checklist covers)

- **Specification-by-Example checklist:** "A Reference trajectory shows only fields the commit call returns; a world fact the tool does not return stays in Initial state." (N2)
- **Evaluation checklist:** "A rubric dimension forbids exactly what the rule and failure row it grades forbid, no wider." (P3) Also: "A phrase that orders two kinds of agent question says which kind the earlier question is." (P2)
- **Use-case checklist (Failure handling):** "After the last allowed retry of an unanswered commit call, a lookup that shows no effect does not show the call will not take effect late; report unknown and hand off." (P1)
- **Evaluation checklist:** "A data-variant column holds a value, never a whole assertion line." (N4)

## Interview

No interview ran in this verification-only run. The packet records that the original interview was direct.
