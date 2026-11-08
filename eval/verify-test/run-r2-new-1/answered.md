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
- R2-1 CO-S25/CO-S26 did not require the lookup after the unanswered CO-A2: added "Fewer than one CO-A1 after the second CO-A2." (CO-S25) and "Fewer than one CO-A1 after the first CO-A2." (CO-S26).
- R2-2 "Order not cancelled reported" dropped "could not be found" for CO-S24: CO-S24 now uses its own dimension "Order not found at cancellation reported"; "Order not cancelled reported" is CO-S25 only.
- R2-3 "not cancelled" after the second unanswered CO-A2 although a late effect is possible: stands as an open question for the user (the inputs decide only the first timeout; changing it changes CO-07).
- R2-4 "names no order" undefined in CO-02: the two failure rows now say "has not said which order they mean", matching the sibling row; the CO-02 rule text change is proposed to the user, not applied.
- R2-5 CO-02 "may propose" vs failure row "Propose that order.": rule change ("proposes") proposed to the user, not applied.
- R2-6 "a lookup did not answer" rows overlapped retried lookups: the three such conditions now read "no lookup ... answered (the agent may repeat the lookup first)".
- R2-7 none-open row misdescribed a customer with no orders: reason now "because none is placed or processing", and returns are mentioned only when an order has shipped or been delivered.
- R2-8 no lookup guard for state-dependent replies with no commit call: "Fewer than one CO-A1." added to CO-S05, CO-S06, CO-S07, CO-S10, CO-S29.
- R2-10 "Refund not issued reported" accepted "not confirmed yet" for known failures: restored to "has not been issued" for CO-S17, CO-S18, CO-S22; CO-S20 now uses "Refund not confirmed reported".
- R2-11 reference trajectories carried "card closed" the tool no longer returns: removed from CO-S17, CO-S22, CO-S23.

Already answered in round 3:
- R3-1 lookup-count guards did not tie the report to the lookup: the dimensions "Shipped order explained", "Already cancelled reported", "Order not found reported", "Orders unavailable reported", "Order not cancelled reported" and "No open order reported" now also check that the agent states the outcome only in text sent after the tool result that shows it.
- R3-2 cancellation-unknown row put the follow-up promise before CO-A4: reordered to make CO-A4 first, then tell.
- R3-3 "No open order reported" and the CO-S29 note did not accept the row's reason: both now accept "because none is placed or processing" or "because they have shipped or been delivered".
- R3-4 failure causes no field or tool result carries: removed from CO-S17, CO-S22, CO-S23; CO-S17 rows 2-3 replaced by one row with refund id RF-5540; CO-S23's "failure reason" column became "refund id" (RF-5531, RF-5540).
