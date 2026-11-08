Already answered in round 1 (do not report again):
- M1 second unanswered cancellation skipped the re-read: rows now branch on a lookup after any unanswered CO-A2; CO-S15 requires the lookup; CO-S25 covers "still open after two attempts".
- M2 OrderNotCancelled handling invented / CO-S17 row 3 contradicted its own world: row 3 removed; the outcome has its own row (no further refund, no handoff, tell no refund was issued). The right handling is an open question for the user; in a consistent world the outcome arises only after an agent breaks CO-05, so no scenario injects it.
- M3 "not confirmed yet" wording: the lookup-failed branch and CO-S20 now use it; the shared dimension accepts either wording.
- M4 failure_reason field: removed.
- M5 CO-S11 row 2 switched rules: split into CO-S26.
- M6 CO-S06 Illustrates CO-05: changed to CO-01, G-01.
- M7 no scenario for a change inside the confirming turn: CO-S27 added.
- M8 one or zero open orders with no order named: CO-02 clauses, two failure rows, CO-S28, CO-S29 added.
- M9 no-arrival-date promise untested: added to CO-03 and as rubric dimension "No arrival date promised".
- M10 a cancelled order with a failed or missing refund when a later conversation starts: CO-07 scoped to orders the agent cancelled in this conversation; the confirmed summary ("An already cancelled order: the agent reports that and changes nothing") supports CO-01; whether the agent should do more is an open question for the user.
- M11 lookup answered without the order: merged into the unknown-cancellation row.
- M12 follow-up task set not stated: "No follow-up task exists." added to every Initial state.
- M13 Turn 2 anchors: now anchored on the §5.1 confirmation-question form with the proposal values.

Already answered in round 2 (do not report again):
- M14 CO-S25 and CO-S26 did not require the lookup after the last unanswered cancellation: Forbidden "Fewer than one CO-A1 after the second CO-A2" (CO-S25) and "... after the first CO-A2" (CO-S26) added.
- M15 shared "Order not cancelled reported" dropped "could not be found" for CO-S24: CO-S24 now uses its own dimension "Cancellation not found reported".
- M16 shared "Refund not issued reported" accepted "not confirmed yet" for known failures: restored to "has not been issued" for CO-S17, CO-S18, CO-S22; CO-S20 uses new dimension "Refund not confirmed reported".
- M17 CO-03 "states no date or time frame" is stronger than the confirmed "promises nothing about when the money arrives": rule change proposed to the user (open); spec unchanged.
- M19 reference trajectories showed a refund failure reason CO-A3 no longer returns: "failed, card closed" changed to "failed" in CO-S17, CO-S22, CO-S23.
- M20 no next step for the customer after the second unanswered cancellation with the order still open: open question for the user; spec unchanged.
- M21 no holding-back scenario on the excluded side of CO-07's "cancelled in this conversation" scope: stands until the user answers the M10 open question.
- M22 "none open" row covered cancelled orders but its rubric and scenario did not: rubric now says "each has shipped, been delivered or been cancelled"; CO-S29 row 3 has an already cancelled order; a customer with no orders at all is an open question.
- M23 "lookup answered without the order" had no scenario: CO-S14 row 3 added, lookup returns a list without the order.
- M24 placed-to-shipped race not in the inputs: CO-S11 and CO-S26 row 2 status changed to processing.
- M25 CO-02 "may propose" versus failure row "Propose that order.": row now "Propose that order, or ask which order and propose it once the customer names it."
- M26 "names no order" undefined against "has not said which one they mean": rule change to CO-02 proposed to the user (open); spec unchanged.
- M27 OrderNotCancelled row forbade the CO-A4 that CO-07 requires: row now makes CO-A4 with reason refund not issued and tells the customer staff will follow up; whether that handling is right stays the M2 open question.

Already answered in round 3:
- M28 the M25 fix allowed asking which order, but CO-S28 had no answer for that question: optional pair "Which order would you like to cancel? A: <order>." added to CO-S28.
- M29 the M27 fix made a CO-A4 that CO-07 forbids ("occurs in no other situation"): row reverted to its round-1 text (no CO-A4); how to handle OrderNotCancelled, given CO-07, is an open question for the user.
- M30 CO-S14 row 3 injected a list_orders result the confirmed contract cannot produce: CO-S14 reverted to its round-1 block; whether list_orders can omit an owned order is an open question.
- M31 "No open order reported" both required and forbade saying an order was cancelled: now "never says it cancelled an order in this conversation", and the CO-S29 note matches.
