# Round 3 findings (merged, verbatim) — r2-new-3

Count line: 3 kept findings: 2 Important, 1 Nit (1 dropped). Finder reports: faithfulness 2 (1 Important, 1 Nit); coverage 4 (2 Important, 2 Nit); verdicts (Codex) 2 (2 Important). 8 finder findings merged to 4.

Merge map: faithfulness F1 + coverage F1 + Codex F1 -> N1; coverage F2 + Codex F2 -> N2; faithfulness F2 + coverage F3 -> N3; coverage F4 -> N4.

Pre-existing (reported): rubric row "No open order reported" (context block) said "because they have shipped or been delivered" while the no-open-order row says "shipped, been delivered or been cancelled" (faithfulness finder). The N4 fix rewrote that rubric row as part of its pattern, which also settles this note.

Round 3 is the last round: the skill stops after round 3 even with findings left; the open part of N1 goes to the report as open.

## N1

N1 | Ambiguous | Important | failure rows "CO-A2 | the order system did not answer a CO-A2", "CO-A3 | the order system did not answer the second CO-A3", "any | every lookup made after an unanswered CO-A2 did not answer ..."; CO-S12 row 3, CO-S19 row 3
Quote: "Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it, repeating the lookup while it does not answer; then act on the row below that matches the first lookup after it that answers with the order, or on the row for no such lookup when the agent stops looking up." / "Make no further CO-A3; look up the order's refund, repeating the lookup while it does not answer. … If no lookup answers and the agent stops looking up, make CO-A4 with reason refund status unknown…" / CO-S12 row "| 3 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 | does not answer |" with its note "in row 3 the first lookup goes unanswered and a repeat shows the order cancelled, so a handoff after one unanswered lookup fails in the action log"
Evidence: No line says how many unanswered lookups must come before the agent may stop and hand off; the packet sets no minimum ("Reads may be retried on timeout without limit", review-packet.md, Tool confirmation turn, change 4), and Round 3 Q3/Q4 say a failed re-read leads to the handoff ("re-read fails, say status unknown and hand off"; "Re-read fails, say outcome unknown, issue no refund, hand off"). The scenarios disagree: CO-S14 (reference steps 6-7 "CO-A1 → no answer" then "CO-A4"; Forbidden "CO-A4 before a CO-A1 made after the first CO-A2."), CO-S15 (steps 8-9) and CO-S21 (steps 8-9; Forbidden "CO-A4 before a CO-A1 made after the second CO-A3.") pass a handoff after one unanswered lookup, while CO-S12 row 3 and CO-S19 row 3 fail the same trajectory under "CO-A4 at any point." Up to the handoff the agent sees the same thing in CO-S14 and CO-S12 row 3 (CO-A2 unanswered, one CO-A1 unanswered), and in CO-S21 row 1 and CO-S19 row 3 (same refund RF-5531 pending).
Pattern: A "repeat while it does not answer / when the agent stops" clause sets no stopping point while scenarios assume different stopping points; state an observable retry budget or make the retry optional with the same permitted outcome after every timeout, and align every scenario.

Verifier verdicts:
- V1: Real | Important | The CO-A2 row lets the agent act "when the agent stops looking up" but never says when that is. In CO-S14 (steps 5-7: CO-A2 no answer, CO-A1 no answer, CO-A4) a handoff after one unanswered lookup passes. In CO-S12 row 3 the agent has seen exactly the same thing at that point, yet "CO-A4 at any point" is Forbidden. CO-S21 (steps 6-9) and CO-S19 row 3 split the same way, so one agent policy cannot pass both scenarios of either pair.
- V2: Real | Important | The revised CO-A2 row says "repeating the lookup while it does not answer ... or on the row for no such lookup when the agent stops looking up" and never says when the agent may stop. Up to the handoff, the agent sees the same thing in CO-S14 and CO-S12 row 3. CO-S14's reference hands off at that point (steps 6-7), and so do CO-S15 (steps 8-9) and CO-S21 (steps 8-9). CO-S12 row 3 and CO-S19 row 3 fail that same trajectory under "CO-A4 at any point." Round 3 Q3/Q4 support the one-lookup handoff, and "Reads may be retried on timeout without limit" only permits retries; it sets no minimum.
- V3: Real | Important | The CO-A2-unanswered row lets the agent stop retrying at any point ("or on the row for no such lookup when the agent stops looking up"), and so does the CO-A3-unanswered row ("If no lookup answers and the agent stops looking up, make CO-A4"). CO-S14 (steps 6-7, Forbidden only "CO-A4 before a CO-A1 made after the first CO-A2") and CO-S21 (steps 8-9) pass a handoff after one unanswered lookup. CO-S12 row 3 and CO-S19 row 3 fail the same handoff under "CO-A4 at any point". Up to the handoff the agent sees the same thing in each pair, so one policy cannot pass both. The packet only allows retries ("Reads may be retried on timeout without limit"), and Round 3 Q4 says "Re-read fails, say outcome unknown, issue no refund, hand off", so no input sets a minimum number of lookups.

Result: kept, Important (3 Real)
Status: fixed, with an open question: repeating an unanswered lookup is now optional in the CO-A2-unanswered row ("the agent may repeat a lookup that does not answer. Then act on ... the row for no such lookup when the agent makes no further lookup.") and in the second-CO-A3-unanswered row; CO-S12 and CO-S19 restored to their round-1 text (row 3 and the "first lookup" column removed), so every scenario now accepts a handoff after one unanswered lookup. Open: how many lookups the agent must try before handing off (the inputs allow unlimited read retries but set no minimum); until the user decides, the retry-then-answers branch has no scenario.

## N2

N2 | Gap | Important | CO-S12, Forbidden (row 3)
Quote: "CO-A3 before a CO-A1 made after the first CO-A2."
Evidence: In row 3 ("The order system <first lookup> the first CO-A1 the agent makes after its first CO-A2." with first lookup = "does not answer"), an unanswered CO-A1 still counts as "a CO-A1 made after the first CO-A2" (Appendix A: "a CO-A1 made after an action is any CO-A1 call issued after that action's call, whatever it returned"). An agent that makes one unanswered lookup and then sends CO-A3 blind gets RF-5531 pending, because the order really was cancelled, and so satisfies the Final state, Required events, the message check "Refund id reported" and every Forbidden line. CO-05 says "CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled", and the revised CO-A2 row says to act only on "the first lookup after it that answers with the order".
Pattern: A Forbidden line keyed on "a CO-A1 made after X" in a row where that CO-A1 can go unanswered lets an unanswered read authorize the action; key it on a lookup that answered with the authorizing state.

Verifier verdicts:
- V1: Real | Important | Spec Appendix A (line 1845) says "a CO-A1 made after an action is any CO-A1 call issued after that action's call, whatever it returned". So in CO-S12 row 3 an agent can make one unanswered CO-A1, then send CO-A3 blind. It still passes "CO-A3 before a CO-A1 made after the first CO-A2", gets RF-5531 pending, and meets the Required events and Final state. That breaks CO-05.
- V2: Real | Important | Appendix A (spec line 1845): "'a CO-A1 made after' an action is any CO-A1 call issued after that action's call, whatever it returned". So in CO-S12 row 3, one unanswered CO-A1 satisfies "CO-A3 before a CO-A1 made after the first CO-A2." A blind CO-A3 then returns RF-5531 pending and meets the Required events, the Final state and "Refund id reported". That breaks CO-05 and the CO-A2 row's "first lookup after it that answers with the order".
- V3: Real | Important | Appendix A (spec line 1845) says "a CO-A1 made after an action is any CO-A1 call issued after that action's call, whatever it returned". So in CO-S12 row 3 the sequence CO-A2 (no answer), CO-A1 (no answer), CO-A3 satisfies "CO-A3 before a CO-A1 made after the first CO-A2", returns RF-5531 pending, and meets the Required events, Final state, "Refund id reported" and every Forbidden line, though it breaks CO-05. It also contradicts the scenario's own Unambiguity note.

Result: kept, Important (3 Real)
Status: fixed: the only instance was CO-S12 row 3, removed under N1; in rows 1-2 the lookup answers, so the Forbidden line keys on an answered lookup.

## N3

N3 | Ambiguous | Nit | failure: any | every lookup made after an unanswered CO-A2 did not answer or answered without the order, and the agent makes no further lookup
Quote: "| any | every lookup made after an unanswered CO-A2 did not answer or answered without the order, and the agent makes no further lookup | Tell the customer it is not known whether the order was cancelled, ... make CO-A4 with reason cancellation unknown. | CO-07, G-03 |"
Evidence: In CO-S15 the lookup made after the first unanswered CO-A2 answers with the order (reference step 6 "Agent → CO-A1 → HG-10482 still processing"). Read literally, "every lookup made after an unanswered CO-A2 did not answer" is false there, yet CO-S15 requires this row's action ("CO-A4 occurs exactly once, for <order>, reason cancellation unknown, after the second CO-A2 for <order>"). The neighbouring row is bounded ("after the first CO-A2 went unanswered, and before any second CO-A2"); this one does not say which CO-A2 when there are two. CO-07 ("cannot tell whether its own CO-A2 cancelled the order") still settles the verdict.
Pattern: A failure-row condition over "an unanswered CO-A2" does not say which one when two can occur; scope it to the most recent unanswered CO-A2.

Verifier verdicts:
- V1: Style only | Nit | The indefinite "an unanswered CO-A2" reads as "some unanswered CO-A2". In CO-S15 that is the second CO-A2, after which every lookup failed (step 8 "CO-A1 → no answer"), so the row fires as CO-S15 requires. In CO-S25 the lookup after the second CO-A2 answers, so the row does not fire. Neither reading changes a verdict, and CO-07 settles it anyway.
- V2: Style only | Nit | The existential reading ("there is an unanswered CO-A2 after which every lookup failed") holds in CO-S15 for the second CO-A2. It is the same construction the sibling row "a lookup made after an unanswered CO-A2 shows the order cancelled" uses. CO-07 requires the same handoff either way, so no verdict or behavior changes.
- V3: Real | Nit | "every lookup made after an unanswered CO-A2" has two readings; read as the second it holds in CO-S15, read as the first or any it is false (step 6 "CO-A1 → HG-10482 still processing"). The neighbouring rows name which CO-A2; this row does not. CO-07 still requires the same handoff under both readings, so no verdict changes.

Result: dropped (V3 Real; V1 and V2 Style only: the existential reading 'some unanswered CO-A2' fits CO-S15 and CO-07 settles the verdict)
Status: n/a

## N4

N4 | Gap | Nit | failure: any | the customer named no order, has at least one order, and none of the customer's orders has status placed or processing
Quote: "Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing."
Evidence: The only scenario that triggers this row is CO-S29, whose Initial state has only a shipped order (HG-10466) and a delivered order (HG-09977), and its rubric dimension "No open order reported" checks "because they have shipped or been delivered". No scenario covers a customer who named no order and whose non-open orders include a cancelled one, so the row's "been cancelled" alternative is never asserted. CO-01 says something different for a cancelled order ("tells the customer the order is already cancelled").
Pattern: A failure-row tell clause with alternatives where only some alternatives get a scenario and a rubric.

Verifier verdicts:
- V1: Real | Nit | The row's "or been cancelled" clause is never tested: CO-S29 has only HG-10466 shipped and HG-09977 delivered, and "No open order reported" checks only "because they have shipped or been delivered". The row also tells a customer whose order was cancelled that "returns are a separate process", which differs from CO-01. No current verdict changes.
- V2: Real | Nit | CO-S29 is the only scenario for this row; its Initial state has only HG-10466 shipped and HG-09977 delivered, and "No open order reported" checks "because they have shipped or been delivered". No scenario has a customer who named no order and owns a cancelled order, so the "been cancelled" alternative is never asserted. (The claim that CO-01 says something different is weak, but the coverage gap stands.)
- V3: Real | Nit | The only scenario that triggers the row is CO-S29 (HG-10466 shipped, HG-09977 delivered); its rubric checks only "because they have shipped or been delivered", so "been cancelled" is never tested. The case can happen: list_orders includes cancelled orders (packet, tool confirmation change 4). No existing verdict changes.

Result: kept, Nit (3 Real)
Status: fixed: CO-S29 gains order HG-09940 (cancelled, total paid $19.60, Visa ending 3519) with refund RF-5490 issued; final state asserts it unchanged; reference trajectory, Unambiguity note and rubric "No open order reported" now say "shipped, been delivered or been cancelled" and "never says it cancelled an order or issued a refund in this conversation".
