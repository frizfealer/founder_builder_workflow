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
- M14 "Order not cancelled reported" lost "could not be found" for CO-S24: CO-S24 now uses its own dimension "Cancellation not found reported", which keeps that clause; the shared one covers CO-S25 only.
- M15 race variants went placed → shipped: CO-S11 and CO-S26 now start every row at processing, the only flip the inputs name; status column removed.
- M16 CO-02 "may propose" vs the row's "Propose that order": stands as a proposed rule change for the user (CO-02 "the agent may propose that order" → "the agent proposes that order without asking which"); rule text unchanged.
- M17 CO-S25 and CO-S26 did not require the lookup after the unanswered CO-A2: added "Fewer than one CO-A1 after the second CO-A2." (CO-S25) and "Fewer than one CO-A1 after the first CO-A2." (CO-S26) to Forbidden.
- M19 one unanswered lookup triggered the handoff despite unlimited read retries: the CO-A2-unanswered row and the second-CO-A3-unanswered row now repeat the lookup while it does not answer and act on the first that answers; the cancellation-unknown row fires only when every lookup failed and the agent stops looking up; CO-S12 and CO-S19 gained a row 3 where the first lookup is unanswered and a repeat answers.
- M20 no-open-order row covered a customer with no orders: the row now requires at least one order; CO-02's "When none has" clause is a proposed rule change, and what to tell a customer with no orders is an open question.
- M21 "after the first CO-A2 went unanswered" overlapped the second-attempt row: now bounded "and before any second CO-A2".
- M22 "Refund not issued reported" accepted "not confirmed yet" for known failures: restored to "has not been issued" for CO-S17, CO-S18, CO-S22; CO-S20 uses new dimension "Refund not confirmed reported".

Already answered in round 3 (do not report again):
- N1 no stopping point for repeated lookups; CO-S12/CO-S19 row 3 contradicted CO-S14/CO-S15/CO-S21: repeating an unanswered lookup is now optional ("the agent may repeat a lookup that does not answer"; the no-answer branch applies "when the agent makes no further lookup"); CO-S12 and CO-S19 restored to their round-1 text (row 3 and the "first lookup" column removed). How many lookups the agent must try before handing off is an open question for the user.
- N2 CO-S12 row 3 let an unanswered lookup authorize a blind CO-A3: resolved by removing row 3 (N1).
- N4 the no-open-order row's "been cancelled" alternative was never asserted: CO-S29 gains cancelled order HG-09940 with issued refund RF-5490; its final state, reference trajectory, Unambiguity note and rubric "No open order reported" now cover "been cancelled".
