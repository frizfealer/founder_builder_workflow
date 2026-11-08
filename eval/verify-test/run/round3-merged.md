# Round 3 merged findings

## R3-01 (Important)
Sources: faithfulness F1

R3-01 | Lies | Important | failure rows "any | the customer named no order, and none of their orders has status placed or processing" and "CO-A2 | the order system did not answer the second CO-A2", §3 failure table
Quote: "Tell the customer none of their orders can be cancelled, and, when any of them has shipped or been delivered, that returns are a separate process; propose nothing."
Evidence:
- Instance 1, the no-order-named row (rewritten for R2-06/R2-07). This row says the agent only has to say "none can be cancelled" and, when an order has shipped, that returns are separate. It never has the agent say that an order has shipped or been delivered. Two other spec lines require exactly that. CO-01, the rule the row cites, says: "For an order with status shipped or delivered, it tells the customer the order has shipped and cannot be cancelled ... for an order with status cancelled, it tells the customer the order is already cancelled." CO-S05 row 4 ("I want to cancel my order.", only order HG-10466 delivered) is the scenario that runs this row. It is graded by the rubric "Shipped order explained", which needs "the order has shipped (or been delivered) and was not cancelled". The CO-S05 Unambiguity note says the same: "checks the agent said the order has shipped and cannot be cancelled". So an agent that follows the row exactly ("None of your orders can be cancelled; returns are a separate process.") fails CO-S05 row 4. The row also drops CO-01's "already cancelled" message for a customer whose orders are all cancelled. The R2-06 fix took out the per-order clause but did not replace what CO-01 and the rubric still require.
- Instance 2, the second-CO-A2 row, lookup-fails branch (rewritten in this round). Quote: "If the lookup does not answer, make no CO-A3, make CO-A4 with reason cancellation unknown, and tell the customer it is not known whether the order was cancelled and store staff will follow up." CO-S15 runs this branch (no CO-A1 after the second CO-A2 answers). It is graded by "Cancellation outcome unknown reported", which needs the agent to say "that no refund was issued". CO-S15 reference trajectory step 10 also says "no refund was issued". The row never asks for that clause, so an agent that follows the row can fail CO-S15.
Pattern: a failure row's required customer message leaves out a clause that the cited rule, or the rubric dimension of the scenario that runs the row, requires. The fix is to make each row's message include every clause that its cited rule and its scenario's dimension check, or to drop those clauses from the rule and dimension.

Pre-existing: failure row "CO-A2 | the order system did not answer the first CO-A2", lookup-fails branch, leaves out "no refund was issued", which CO-S14's "Cancellation outcome unknown reported" dimension requires (same pattern as F1 instance 2).

Checked with no Lies found:
- **CO-S26:** the Initial state race, the timeout effects matched against Appendix A CO-A2, and a replay of the trajectory to the Final state (shipped, no refund, no task). Also row 1 substitution, the row 2 Required events and final state, the Forbidden lines against CO-06 and G-04, Illustrates, and 2026-11-05 being a Thursday.
- **Second-CO-A2 row:** checked against round 3 Q4, CO-06 and CO-07.
- **Other blocks:** the CO-S03 and CO-S04 Turn 2 anchors against their trajectories; the cause-free CO-A3 failed results in CO-S17, CO-S22 and CO-S23 against Appendix A; and the "No follow-up task exists." pattern line against every scenario's Final state and CO-S22's ST-2207 setup.

## R3-02 (Nit)
Sources: coverage F1

R3-02 | Gap | Nit | failure row "any | the customer named no order, and none of their orders has status placed or processing" (section 3)
Quote: "| any | the customer named no order, and none of their orders has status placed or processing | Tell the customer none of their orders can be cancelled, and, when any of them has shipped or been delivered, that returns are a separate process; propose nothing. | CO-01 |"
Evidence: The rewritten row has two message branches: the returns clause is said only when some order has shipped or been delivered. The findings list (R2-07) also says the row now covers a customer with no orders. Only one scenario triggers the row: CO-S05 row 4 (agent-spec.md line 398, "I want to cancel my order." | delivered). There the customer's only order is delivered, so only the "some order shipped" branch is tested. No scenario's Initial state gives a customer with no orders, a customer whose orders are all cancelled, or a customer with several orders none of which is open. Every scenario has at least one order plus "The customer has no other orders." (lines 127, 251, 314, 368 ... 1620). So nothing tests the "none of their orders can be cancelled" message without the returns clause, or the propose-nothing outcome when no order has shipped. CO-S05 row 4 scores the message with "Shipped order explained" (a single shipped order "was not cancelled", plus returns). It never checks "none of their orders can be cancelled" across several orders.
Pattern: A failure row with a conditional message branch, or an extension added in a fix (here R2-07's no-orders case), gets a scenario only for the branch the existing scenario already triggers. Each branch the row defines needs an Initial state that triggers it and a rubric dimension that checks its message.

Pre-existing (section 4, failure row "CO-A4 | the order system did not answer the second CO-A4"): no scenario triggers this row with reason cancellation unknown or refund status unknown. Only CO-S23 (refund not issued) does, so the "tell what it knows under G-03" message is untested for those reasons.

Checked and found complete (no finding):
- All four lookup branches of the rewritten "second CO-A2 unanswered" row have a scenario whose Initial state triggers them, with matching message checks: cancelled is CO-S25; shipped is CO-S26 ("Shipped order explained"); placed or processing is CO-S27 ("Cancellation not made reported"); lookup does not answer is CO-S15 ("Cancellation outcome unknown reported").
- The row's two wait-before-acting conditions are each tested both ways:
  - "no CO-A3 until a lookup … answers": CO-S25 acts, CO-S15 and CO-S26/27 hold back.
  - "no CO-A4 until a lookup has been made": CO-S15 acts and has a Forbidden line for CO-A4 before that lookup.
- CO-S26's User-knows pair is used at trajectory steps 3–4.
- CO-S26's Initial-state values sit inside the contract: processing changes to shipped only on the second CO-A2; row 2 HG-10530/$53.50/Amex ending 1007 matches CO-S01 row 3; 2026-11-05 is a Thursday.
- The "No follow-up task exists." pattern edit agrees with every scenario's Final state. Success scenarios assert no task (CO-08). Handoff scenarios assert exactly one task.
- CO-S22's extra Initial-state line about ST-2207 does not conflict with the pattern edit.
- The CO-S03/CO-S04 Turn 2 anchors and the CO-S17/22/23 trajectory edits are consistent with each scenario's Initial state and data rows.
