# Answered findings

## Round 1
- R1-01 fixed: the "second CO-A2 unanswered" failure row now waits for a lookup and branches on it (cancelled: CO-A3; shipped/delivered: report, no CO-A3/CO-A4; still placed/processing: report not cancelled, no CO-A3/CO-A4; no answer: CO-A4 cancellation unknown); new CO-S13 row 3, CO-S25, CO-S26.
- R1-02 fixed: OrderNotCancelled from CO-A3 has its own failure row (lookup first; cancelled: CO-A4 refund not issued; otherwise: CO-A4 cancellation unknown); CO-S17 row 3 now requires the lookup (conditional Forbidden line); new CO-S27 for the unanswered-lookup branch.
- R1-03 fixed: the "second CO-A3 unanswered" row's failed-or-no-refund branch now says "the refund is not confirmed yet" (round 3 Q3 wording); CO-S20 uses new dimension "Refund not confirmed reported".
- R1-04 fixed: "Cancellation outcome unknown reported" no longer requires "that no refund was issued" (CO-S14/S15 trajectories and notes too); "Refund status reported" no longer requires "the order is cancelled".
- R1-05 fixed: removed the invented `failure_reason` field from Appendix A's CO-A3 outcomes.
- R1-06 fixed: new rule CO-09 (no arrival date or time span for the refund); rubric dimension "No arrival date promised" on CO-S01.
- R1-07 fixed: CO-S03 row 4, a confirming turn that also changes the order ("Yes, but make it HG-10511 instead, not that one.").
- R1-08 fixed: rubric "Refund status reported" (status as Final state gives it, no other) now used by CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19.
- R1-09 open: no input says what to do when the lookup after an unanswered cancellation no longer lists the order; left for the user.
- R1-10 open: an unnamed request with no open orders is settled by CO-01 (propose nothing, report each status); a customer with no orders at all has no input; left for the user.
- R1-11 dropped (adversarial refutation: inputs ask the writer to derive further cases; no input contradicts reporting the id).
- R1-12 open: G-04's general "guarantees nothing new" clause also covers SG-04 (cancel) although the input forbids a blind resend; fixing it changes rule text, so it is a proposed rule change for the user.
- R1-13 fixed: CO-S06 rows 3 and 4, an already cancelled order with no refund and with a failed refund; nothing may change.
- R1-14 open: whether one conversation may cancel more than one order is a product decision no input makes; left for the user.
- R1-15 fixed: CO-S01 row 4, an unnamed request with exactly one open order (agent proposes it without asking); CO-S01 now illustrates CO-02.
- R1-16 stands: SG-01 (user-supplied) makes a repeated refund call return the existing refund, so a provider-unavailable answer to the second call means no refund exists.
- R1-17 dropped (adversarial refutation: §5.1 reads Final state against Initial state, which creates no follow-up task).
- R1-18 dropped (adversarial refutation: §5.2 has the simulated user deliver scripted turns judged on meaning; the trigger follows §5.1's confirmation-question form).

## Round 2
- R2-01 fixed: CO-S15 now forbids "CO-A4 before a CO-A1 made after the second CO-A2" and its trajectory makes that (unanswered) lookup before the handoff.
- R2-02 fixed: CO-S25 and CO-S26 forbid "Fewer than one CO-A1 after the second CO-A2", so a guessed report without the lookup fails.
- R2-03 fixed: the OrderNotCancelled row gains a shipped-or-delivered branch (CO-05 report, no CO-A4); placed/processing stays "cannot tell" (CO-A4 cancellation unknown), as both verifiers held; new scenario CO-S28 exercises the new branch.
- R2-04 dropped (both verifiers: the row had two outcomes and CO-S27 covers the second).
- R2-05 fixed: Appendix A's CO-A3 outcome now reads "the order system reports the order not cancelled"; §5.1 "Supporting actors" lets Initial state inject an answer that contradicts the order's status.
- R2-06 fixed: CO-S17, CO-S22 and CO-S23 trajectories show a failed refund without a failure cause the tool no longer returns.
- R2-07 fixed: CO-S26's Unambiguity note states both CO-07 conditions.
- R2-08 fixed: CO-09 (a rule added in this run) and its rubric now forbid any promise about when the money arrives, including words such as soon or shortly.
- R2-09 dropped (both verifiers: "states no other status" needs judgment, so §5.2 requires a rubric).
- R2-L1 fixed: CO-S19, CO-S20 and CO-S21 give each unanswered refund call its own effect (the first creates no refund, the second creates the row's refund or none).

## Round 3
- R3-01 fixed: new scenario CO-S29 for the OrderNotCancelled row's placed/processing branch (CO-A2 answered cancelled, the lookup after the refund call shows the order open; CO-A4 cancellation unknown).
- R3-02 unverified, not applied (late round-3 Codex verdicts finder; no next round).
- R3-03 Pre-existing, unverified, not applied (late round-3 Codex verdicts finder).
