# Findings already answered

## Round 1
- R1-01 fixed: the "second CO-A2 unanswered" failure row now waits for a lookup and branches on it (cancelled: CO-A3; shipped or delivered: shipped report, no CO-A3/CO-A4; placed or processing: not-cancelled report, no CO-A3/CO-A4; no answer: CO-A4 cancellation unknown); the "second CO-A3 provider unavailable" row is limited to two provider-unavailable answers, and a provider-unavailable answer after an unanswered first CO-A3 now goes to the lookup row; new CO-S25, CO-S26, CO-S27, new CO-S20 row 3, CO-S15 now requires the lookup.
- R1-02 open: what the agent does when issue_refund reports OrderNotCancelled for an order the order system returned cancelled is not in the inputs (the user only added the outcome name); only the user can decide, so the row and CO-S17 row 3 are left as they are and the question is in the report.
- R1-03 fixed: the failed-or-no-refund branch after the refund retry now says "the refund is not confirmed yet" (round 3 Q3 wording); CO-S20 uses the new dimension "Refund not confirmed reported".
- R1-04 fixed: new rule CO-09 (no promised arrival date), new dimension "No arrival date promised" on CO-S01, new CO-S01 row 4 in which the customer asks how many days the money takes.
- R1-05 fixed: new CO-S03 row 4, in which the customer confirms and changes the order in the same turn.
- R1-06 open: whether a customer may cancel more than one order in one conversation, and what the agent says when asked to, is a business decision the inputs do not make; in the report as an open question.
- R1-07 answered (stands): the packet's confirmed derivation "An already cancelled order: the agent reports that and changes nothing" is what the row and CO-S06 assert.
- R1-08 open: the fix changes G-04's text, so it stops at that rule and is reported as a proposed rule change (G-04 to name SG-03 and to exclude CO-A2 from the guarantee clause).
- R1-09 fixed: Appendix A's CO-A3 failed outcome no longer carries the invented `failure_reason` field.
- R1-10 fixed: new failure row for a customer who names no order and has no order placed or processing; new CO-S05 row 4 exercises it.

## Round 2
- R2-01 fixed: the "second CO-A2 unanswered" row now gates CO-A3 on a lookup that answers and CO-A4 only on a lookup having been made, so the lookup-fails branch can hand off.
- R2-02 open: what next step, if any, the agent offers when both cancellations went unanswered and the lookup shows the order still open (try later, contact support, or a handoff) is a business decision the inputs do not make.
- R2-03 fixed: CO-S26 now uses only the processing-to-shipped race; row 2 is a second order (HG-10530) instead of a jump to delivered.
- R2-04 fixed: CO-S17, CO-S22 and CO-S23 trajectories show CO-A3 returning "refund RF-5531, failed" with no cause.
- R2-05 fixed: in the new "second CO-A2 unanswered" row the lookup-fails branch makes CO-A4 before telling the customer staff will follow up (the same order in the first-CO-A2 row is Pre-existing and left as is).
- R2-06 fixed: the "no order named, none open" row no longer has a per-order clause; it says none can be cancelled and, for shipped or delivered orders, that returns are separate.
- R2-07 fixed: the same row's message is now defined for a customer with no orders.
- R2-L1 duplicate of R1-06 (open).
- R2-L2 fixed: every scenario's Initial state now states "No follow-up task exists."
- R2-L3 fixed: CO-S03 and CO-S04 Turn 2 is anchored on a question that states every proposal value for HG-10482.

## Round 3
- R3-01 fixed: the "no order named, none open" row now tells, for a shipped or delivered order, that it has shipped and cannot be cancelled and returns are separate, and for a cancelled order that it is already cancelled; the "second CO-A2 unanswered" row's lookup-fails branch now says no refund was issued (the same gap in the first-CO-A2 row is Pre-existing and left as is).
- R3-02 fixed in part: new CO-S06 row 3 (no order named, only order already cancelled) exercises the cancelled branch of that row; a customer with several non-open orders or with no orders is still not exercised.
