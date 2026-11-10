# Report — agent-spec verification-only trial it1b-2

Skill under test: agent-spec at 9b7479f. The run started at step 4.1 on a copy of eval/agent-spec/round0-agent-spec.md. Step 4.2 was skipped (the review packet was supplied) and the template re-sync was not run (a run that starts at step 4 does not re-sync). Rounds run: 3, stopped at the round cap with open findings. Wall clock: 2026-11-10T01:34:40Z to 02:08:16Z, 2016 s (33m36s).

## File written and scenarios

- eval/agent-spec/run-it1b-2/agent-spec.md (final copy: results/it1b-2/agent-spec-final.md).
- Capability 4.1 Cancel Order (CO, state-changing): 28 scenarios, CO-S01 to CO-S28. Four of them are new in verification: CO-S25 (R2-03), CO-S26 (R3-09), CO-S27 (R3-06) and CO-S28 (R3-11). CO-S17 lost one data-variant row (R1-01). CO-S03 gained one row (R1-06).
- New rule: CO-09 "No arrival date" (R1-05). New rubric dimensions: "No arrival date promised", "Which order asked" and "Refund not confirmed reported".

## Merges (step 3.9)

Not run. This trial starts at step 4, and step 3.9 merges before any reviewer reads the spec. No rows were dropped. The checker prints 8 merge-candidate WARNINGs. Those on CO-S01/02/03/09/12, CO-S11/24, CO-S16/19, CO-S18/20 and CO-S22/23 were present at round 0. The new scenarios add three more, and each stays apart for a stated reason:
- CO-S13/CO-S25: the second CO-A2 has a different outcome, and CO-S25 forbids a refund before a lookup made after the second CO-A2. CO-S13 rows cannot carry that line.
- CO-S01/CO-S27: CO-S27 has a scripted Turn 2 and a scoped confirmation pair.
- CO-S09/CO-S28: CO-S28 has a scripted Turn 2 and a scoped confirmation pair.

## Input ledger (final, from the review packet; unchanged by this run)

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial: issue_refund supplied; list_orders, cancel_order, request_staff_followup proposed and confirmed with the user's four changes |
| 3 | Data model | found |
| 4 | Authorization policy | found. The default was accepted: a state-changing call is authorized only by the user's explicit confirmation of the full proposal, and any change voids it |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases, no transcripts |

## Tools

The proposed tools (list_orders, cancel_order, request_staff_followup) are provisional. issue_refund was supplied by the user. Appendix A is the part of the spec that architecture notes may change. Verification changed Appendix A in one place: `failure_reason` was removed from the CO-A3 outcomes (R1-03), because the confirmed data model has no such field.

## Checker (final run)

    0 errors
    WARNING CO-S01, CO-S02, CO-S03, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
    WARNING CO-S01, CO-S02, CO-S09, CO-S12, CO-S28: identical Required events after substitution; merge candidates (skill step 3.9)
    WARNING CO-S01, CO-S27: identical Required events after substitution; merge candidates (skill step 3.9)
    WARNING CO-S11, CO-S24: identical Required events after substitution; merge candidates (skill step 3.9)
    WARNING CO-S13, CO-S25: identical Required events after substitution; merge candidates (skill step 3.9)
    WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
    WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
    WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)
    
    | Rule | Scenarios |
    |---|---|
    | G-01 | CO-S01, CO-S02, CO-S03 |
    | G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S28 |
    | G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S26 |
    | G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
    | CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
    | CO-02 | CO-S02, CO-S07 |
    | CO-03 | CO-S01, CO-S08, CO-S09, CO-S27, CO-S28 |
    | CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27, CO-S28 |
    | CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S24, CO-S25, CO-S26 |
    | CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26 |
    | CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23 |
    | CO-08 | CO-S01, CO-S16, CO-S19 |
    | CO-09 | CO-S01 |

## Findings

33 findings over 3 rounds: 20 Important, 13 Nit.
- By status: 22 fixed, 1 answered, 6 open, 4 dropped, 0 Pre-existing (whole-spec scope).
- By round: round 1 had 13 (8 Important, 5 Nit), round 2 had 9 (4 Important, 5 Nit), round 3 had 11 (8 Important, 3 Nit).

The full findings, with finder text verbatim and verifier lines, are in results/it1b-2/round<N>-findings.md.

| id | class | severity | status | one line |
|---|---|---|---|---|
| R1-01 | Lies | Important | fixed | CO-S17 row 3 removed. CO-S24 now removes the order when the first CO-A2 is issued, so OrderNotFound can be true. The OrderNotCancelled handling is open (Q1). |
| R1-02 | Lies | Important | fixed | The timeout re-read branch now says "not confirmed yet" (packet Round 3 Q3), with a new dimension for CO-S20. |
| R1-03 | Lies | Nit | fixed | `failure_reason` removed from Appendix A. |
| R1-04 | Gap | Important | dropped | Success-path refund status unasserted. |
| R1-05 | Gap | Important | fixed | No-arrival-date promise: added a §2 interest, CO-09 and a dimension on CO-S01. |
| R1-06 | Gap | Important | fixed | CO-S03 row 4: a confirming turn that also changes the order. |
| R1-07 | Gap | Nit | open | A lookup after an unanswered first CO-A2 that answers without the order (Q2). |
| R1-08 | Gap | Nit | open | What to say about the refund of an already cancelled order whose refund failed or is missing (Q3). |
| R1-09 | Gap | Important | fixed | CO-S02: which-order answer is now scripted Turn 2, confirmation pair scoped (after Turn 2), new dimension "Which order asked". |
| R1-10 | Ambiguous | Important | fixed | CO-S19/20/21: one Initial-state line per unanswered CO-A3. |
| R1-11 | Ambiguous | Important | dropped | Retry still owed after a lookup shows the effect. |
| R1-12 | Ambiguous | Nit | fixed | CO-S11 anchored on the agent issuing its first CO-A2. |
| R1-13 | Ambiguous | Nit | fixed | "Shipped order explained" now has one wording, "is not cancelled". |
| R2-01 | Lies | Important | dropped | Dimensions said to require more than the failure rows. |
| R2-02 | Lies | Nit | fixed | Failure cause removed from three trajectories (completes R1-03). |
| R2-03 | Gap | Important | fixed | The second-CO-A2-timeout row now branches on a lookup, and new CO-S25 covers it. The placed/processing branch is open (Q4). |
| R2-04 | Gap | Nit | open | Case 3 wording when the retry after a refund timeout answers with an error (Q5). |
| R2-05 | Ambiguous | Important | fixed | Dimensions no longer turn on "proposal". The same word in rules CO-01/02/03 is a proposed rule change (below). |
| R2-06 | Ambiguous | Important | fixed | "Refund not confirmed reported" accepts "not confirmed yet" or "has not been issued". |
| R2-07 | Ambiguous | Nit | fixed | CO-S03/S04 trigger reworded. This fix was wrong, see R3-01. |
| R2-08 | Ambiguous | Nit | fixed | Confirmation-anchored Forbidden lines now also fire when no confirmation turn occurs. |
| R2-09 | Ambiguous | Nit | answered | Unlimited reads: the input supports it (tool confirmation, change 4). |
| R3-01 | Ambiguous | Important | fixed | CO-S03/S04 trigger is now named by form only. |
| R3-02 | Lies | Nit | open | G-04 exemption covers CO-A2 via SG-04. This is a rule change, proposed below. |
| R3-03 | Ambiguous | Important | fixed | "never asks the customer to go ahead with ..." wording. |
| R3-04 | Ambiguous | Important | fixed | "Cancellation outcome unknown reported" is limited to text sent after the last CO-A2. |
| R3-05 | Gap | Important | fixed | CO-S03 confirmation pair is scoped (after Turn 2). |
| R3-06 | Gap | Important | fixed | Part (2) fixed with new CO-S27. Part (1) was refuted. |
| R3-07 | Gap | Important | open | A request covering more than one order (Q6). |
| R3-08 | Gap | Important | dropped | Success-path refund status (same as R1-04). |
| R3-09 | Gap | Nit | fixed | New CO-S26: the order ships at the second CO-A2. |
| R3-10 | Gap | Nit | open | An unnamed request when no order is open (Q7). |
| R3-11 | Gap | Important | fixed | New CO-S28: a confirming turn that also asks for the refund elsewhere. |

The round-3 fixes were not reviewed by another round, because the round cap was reached.

### Fix-introduced defects vs defects missed earlier

These were attributed by matching each kept finding's quote against the saved round copies:
- Round 2 had 8 kept findings. 2 quote a line round 1 changed (R2-05 and R2-06, both dimensions round 1 added). 6 quote a line round 1 did not change.
- Round 3 had 10 kept findings. 3 quote a line round 2 changed (R3-01 is the R2-07 trigger, R3-03 is the R2-05 dimension wording, R3-09 is the R2-03 failure row). 7 quote a line round 2 did not change (R3-07 and R3-10 quote "absent").

### Verifier drop rate

4 of 20 Important findings verified were dropped (20%): round 1 2/8, round 2 1/4, round 3 1/8. R3-06 was kept because the verifier refuted only its part (1). The refutations, quoted:
- R1-04: "a scenario does assert the clause. CO-S19 uses \"Refund status reported\": \"the refund's status is the data-variant row's refund status, and states no other status for it\"."
- R1-11: "Failure row 102 settles the case ... \"| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. |\". That is an unconditional instruction".
- R2-01: "G-03 (line 24) requires it: \"... Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown.\" In CO-S14 and CO-S15 no CO-A3 is ever made". For CO-S19: "packet Round 2 Q4, failure case 3 says \"agent retries once, then re-reads the order and refund records and reports what it finds\"".
- R3-08: "a dimension asserts the clause. \"Refund status reported\", used by CO-S19 ... CO-S19 is also known failure case 3's re-read path".

### Proposed rule changes (not applied; for the user to decide)

**R2-05: "propose" is undefined in CO-01, CO-02 and CO-03.** The failure rows that mirror these rules ("propose nothing ...") would follow.
- Before (CO-02): "... the agent asks which and proposes nothing until the customer names one."
- After (CO-02): "... the agent asks which and asks the customer to go ahead with no cancellation until the customer names one."
- CO-01 ("proposes cancelling an order only after a lookup shows it ...", "proposes nothing") and CO-03 ("proposes nothing else") would change the same way, or the spec would define "proposal" as a question that names an order, its refund amount and its payment method and asks the customer to go ahead.

**R3-02: G-04's exemption also covers CO-A2, through SG-04.** The packet says "If the cancel call times out: no blind resend; re-read the order."
- Before: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
- After: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or, for CO-A3 and CO-A4 only, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01 and SG-03)."

## Open questions

- Q1 (R1-01): What if the refund call reports the order not cancelled? When can that happen, and what does the agent tell the customer? The failure row tells it to say "the order is cancelled", and no scenario exercises the branch now.
- Q2 (R1-07): What if the lookup after an unanswered first cancellation answers without the order in it?
- Q3 (R1-08): What if the customer asks about an order that is already cancelled and whose refund failed or was never created? What is the agent required to tell them about the refund?
- Q4 (R2-03): What if the lookup after the second unanswered cancellation shows the order still placed or processing? No third cancellation is allowed, so what does the agent say, and which handoff reason does it use?
- Q5 (R2-04): What if the refund retry after a timeout answers with status failed or "provider unavailable"? Does case 3's re-read and "not confirmed yet" wording still apply, or the answered-error handling?
- Q6 (R3-07): What if the customer asks to cancel two orders, or a second order after the first is done in the same conversation?
- Q7 (R3-10): What if the customer says "cancel my order" and none of their orders is placed or processing, or they have no orders?
- The two proposed rule changes above.

## What verification cannot catch

Whether these rules are Harbor Goods' real rules, and whether the stakeholder list is complete. Only the user can confirm either. CO-S24 now assumes an order can leave the order system at the moment of cancellation, so that "order not found" is possible. The user should confirm that this world can occur (Q1 asks the same about OrderNotCancelled).

## Checklist lines proposed (patterns no checklist covers)

- evaluation-checklist.md: "A scripted turn's trigger never cites a §5.1 term whose definition needs a matching User-knows pair, when the question it names matches no pair; name it by form." (R2-07/R3-01)
- evaluation-checklist.md: "A rubric line that forbids an action is written as 'never asks ...', not 'asks ... no ...'." (R3-03)
- evaluation-checklist.md: "A 'never says X' clause names the window it covers when X is true and allowed earlier in the trial." (R3-04)
- evaluation-checklist.md: "A confirmation pair that must follow a clarifying answer or a scripted change of mind is scoped after that turn, and the clarifying answer is a scripted turn when the pair must wait for it." (R1-09, R3-05)
- cockburn-checklist.md: "A row for a repeated unanswered commit call keeps the lookup branches of the first-call row." (R2-03)
- evaluation-checklist.md: "An injected outcome's Appendix A meaning is true at that call; when it needs the world to change, anchor the change to a state-changing call." (R1-01; verification.md's verifier brief already says this, but no writing checklist does)

## Interview

No interview ran in this trial; it started at step 4 from the frozen packet. The packet's interview rounds were run before this trial and the packet does not name an interview skill.
