# Round 3 findings (merged), with verifier verdicts

Count: 4 merged findings from 4 finder findings (faithfulness 2, verdicts/Codex 1, coverage 1; no duplicates). Kept 4: 1 Important, 3 Nit. Dropped 0.

Kept when at least two verifiers say Real; severity is the majority.

| Id | Verifier A | Verifier B | Verifier C | Kept/dropped | Severity | Disposition | Quotes a line round 2 changed? |
|---|---|---|---|---|---|---|---|
| R3-1 | Real, Important | Real, Important | Real, Important | kept | Important | fixed (not re-reviewed: round 3 is the last) | yes (Forbidden lines added in round 2) |
| R3-2 | Real, Nit | Real, Nit | Real, Nit | kept | Nit | fixed (not re-reviewed) | yes (failure row rewritten in round 2) |
| R3-3 | Real, Nit | Real, Nit | Real, Nit | kept | Nit | fixed (not re-reviewed) | yes (failure row reason changed in round 2) |
| R3-4 | Real, Nit | Real, Nit | Real, Nit | kept | Nit | fixed (not re-reviewed) | no (CO-S17 data variants unchanged since round 0; residue of round 1's failure_reason removal) |

## Fixes

- R3-1 lookup-count guards did not tie the report to the lookup: the dimensions "Shipped order explained", "Already cancelled reported", "Order not found reported", "Orders unavailable reported", "Order not cancelled reported" and "No open order reported" now also check that the agent states the outcome only in text sent after the tool result that shows it.
- R3-2 cancellation-unknown row put the follow-up promise before CO-A4: reordered to make CO-A4 first, then tell.
- R3-3 "No open order reported" and the CO-S29 note did not accept the row's reason: both now accept "because none is placed or processing" or "because they have shipped or been delivered".
- R3-4 failure causes no field or tool result carries: removed from CO-S17, CO-S22, CO-S23; CO-S17 rows 2-3 replaced by one row with refund id RF-5540; CO-S23's "failure reason" column became "refund id" (RF-5531, RF-5540).

Dropped data-variant rows: CO-S17 row 2 (refund failed because the payment provider declined it) and row 3 (because the card has expired), replaced by one values-only row with refund id RF-5540; CO-S23 row 2 (failure reason: the card has expired), replaced by a row with refund id RF-5540. Each dropped row exercised a terminal refund cause that no field or tool result distinguishes.

## Merged findings, verbatim (as sent to the verifiers)

R3-1 | Gap | Important | CO-S05, CO-S06, CO-S07, CO-S10, CO-S25, CO-S26, CO-S29, Forbidden
Quote: "- Fewer than one CO-A1." / "- Fewer than one CO-A1 after the second CO-A2." / "- Fewer than one CO-A1 after the first CO-A2."
Evidence: The round-2 fix meant to guard state-dependent replies (bundle §1 and §3, CO-S25, CO-S26). The new lines constrain only the lookup count and, in CO-S25/CO-S26, its position relative to CO-A2. None requires the lookup to precede the customer-facing report, though every reference trajectory has that order. A question-bearing agent message does not end the trial (§5.1 End of trial), so an agent can report a guessed outcome while asking an extra question, then do the lookup, and satisfy every added line.
Pattern: A minimum-count lookup guard that does not enforce that the state-dependent report follows the lookup that supports it.
(Verdicts finder F1, via Codex.)

R3-2 | Ambiguous | Nit | failure row "any | no lookup made after an unanswered CO-A2 answered with the order (the agent may repeat the lookup first)"
Quote: "Tell the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; make no further CO-A2 and no CO-A3; make CO-A4 with reason cancellation unknown."
Evidence: CO-07 says the agent "tells the customer store staff will follow up once the order system has created the task", and the row "CO-A4 | the order system did not answer the second CO-A4" requires "it could not confirm store staff were told" instead. The sibling rows put CO-A4 before the tell ("CO-A3 | ... status failed", "CO-A3 | ... temporarily unavailable for the second CO-A3", the edited "CO-A3 | ... did not answer the second CO-A3": "make CO-A4 ... and tell the customer"). This row puts the promise first, so one reader lets the agent promise follow-up before CO-A4 returns and another does not. No scenario combines cancellation-unknown with two unanswered CO-A4; CO-S14 and CO-S15 do not change verdict.
Pattern: A failure row that makes a handoff and tells the customer staff will follow up, with the promise placed ahead of the call instead of depending on the handoff returning a task.
(Faithfulness finder F1.)

R3-3 | Ambiguous | Nit | failure row "any | the customer has not said which order they mean, and none of the customer's orders has status placed or processing", against dimension "No open order reported" (CO-S29)
Quote: "Tell the customer none of their orders can be cancelled, because none is placed or processing, and, when any has shipped or been delivered, that returns are a separate process; propose nothing."
Evidence: The R2-7 fix changed the row's reason to "because none is placed or processing". The rubric dimension "No open order reported" that CO-S29 uses still requires "none of their orders can be cancelled because they have shipped or been delivered", and so does CO-S29's Unambiguity note. An agent that gives the reason as the row words it can be failed by a literal grader. CO-01 separately requires "the order has shipped" for each shipped or delivered order.
Pattern: A fix that rewords a failure row's required behavior without updating the rubric dimension and Unambiguity note of the scenario that tests it.
(Faithfulness finder F2.)

R3-4 | Untestable | Nit | CO-S17 Data variants, CO-S22 Initial state, CO-S23 Data variants
Quote: "| 1 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has been closed | Exactly one refund exists for HG-10482: RF-5531, status failed. |"
Evidence: R2-11 removed "card closed" from the reference trajectories because the tool returns no reason. The cause is still world state in CO-S17 rows 1-3 ("because the card has been closed" / "because the payment provider declined it" / "because the card has expired"), CO-S22 Initial state ("with status failed because the card has been closed") and CO-S23 rows 1 and 2 (column "failure reason"). Appendix A CO-A3 returns only `{refund_id, amount, payment_method, status}`; refund fields per review-packet.md round 2 Q3 are refund id, order number, amount, payment method, status; failure_reason was removed (answered M4). The harness cannot set up a "because ..." clause, so CO-S17's three rows and CO-S23's two rows build the same world and the same tool results: separate variants testing one case.
Pattern: A data-variant column or Initial-state clause giving a cause that no world-state field and no tool result carries; variants differing only in it are duplicates.
(Coverage finder F1.)

## Finder reports, verbatim

### faithfulness

```
2 findings: 0 Important, 2 Nit.

F1 | Ambiguous | Nit | failure row "any | no lookup made after an unanswered CO-A2 answered with the order" (bundle §2, spec line 107)
Quote: "Tell the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; make no further CO-A2 and no CO-A3; make CO-A4 with reason cancellation unknown."
Evidence: CO-07 (bundle line 187) says the agent "tells the customer store staff will follow up once the order system has created the task". The row "CO-A4 | the order system did not answer the second CO-A4" (bundle line 243) says the agent must instead tell the customer "it could not confirm store staff were told". The sibling rows put CO-A4 before the tell: "CO-A3 | ... status failed" (bundle line 231), "CO-A3 | ... temporarily unavailable for the second CO-A3" (line 235), and the edited "CO-A3 | ... did not answer the second CO-A3" (line 43, "make CO-A4 ... and tell the customer"). The new row puts the promise first, so one reader lets the agent promise follow-up before CO-A4 returns and another does not. No scenario combines cancellation-unknown with two unanswered CO-A4, so a premature promise is never caught. CO-S14 and CO-S15 do not change verdict, because their CO-A4 succeeds and the rubric "Cancellation outcome unknown reported" does not check order.
Pattern: When a failure row both makes a handoff and tells the customer staff will follow up, it must make the tell depend on the handoff returning a task, matching CO-07, and not put the promise ahead of the call.

F2 | Ambiguous | Nit | failure row "any | the customer has not said which order they mean, and none of the customer's orders has status placed or processing" (bundle §2, spec line 93)
Quote: "Tell the customer none of their orders can be cancelled, because none is placed or processing, and, when any has shipped or been delivered, that returns are a separate process; propose nothing."
Evidence: The R2-7 fix changed the row's reason to "because none is placed or processing". Rubric dimension "No open order reported" (bundle line 1278), which CO-S29 uses, still requires "none of their orders can be cancelled because they have shipped or been delivered". So does CO-S29's Unambiguity note (spec, CO-S29 block). An agent that gives the reason exactly as the row words it can be failed by a grader reading the rubric literally. CO-01 separately requires "the order has shipped" for each shipped or delivered order, which is why this is a Nit and not Important.
Pattern: When a fix rewords the required behavior in a failure row, the rubric dimension and Unambiguity note of the scenario that tests that row must accept the same wording.

Also checked, no defects found: pattern edit "Fewer than one CO-A1." in CO-S05, CO-S06, CO-S07, CO-S10, CO-S29; the other new rows (orders-lookup-failed row, one-open-order row, "Refund not confirmed reported" and "Order not found at cancellation reported"); the edited CO-A3 second-unanswered row against round 3 Q3; CO-S17, CO-S22, CO-S23 trajectories; CO-S20 and CO-S24 dimension names; new Forbidden lines in CO-S25, CO-S26; edited "Refund not issued reported" and "Order not cancelled reported" rows; replays of CO-S17, CO-S20, CO-S22, CO-S23, CO-S24, CO-S25, CO-S26 against Final state and every Data variants row.

Files read: rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (lines 29-117; CO-S05, CO-S06, CO-S07, CO-S10, CO-S17, CO-S20, CO-S22 to CO-S26, CO-S29; grep of headings and dimension names)
```

### verdicts-codex

```
1 finding: 1 Important, 0 Nit.

F1 | Gap | Important | CO-S05, CO-S06, CO-S07, CO-S10, CO-S25, CO-S26, CO-S29
Quote: "- Fewer than one CO-A1.
- Fewer than one CO-A1 after the second CO-A2.
- Fewer than one CO-A1 after the first CO-A2."
Evidence: The fix explicitly intends to guard state-dependent replies (rereview-r3.md, lines about 1343-1346). The new assertions constrain only the lookup count and, in CO-S25/CO-S26, its position relative to CO-A2 (grep 'Fewer than one CO-A1' in agent-spec.md). They never require the lookup to precede the customer-facing report, although the reference trajectories consistently use that ordering (agent-spec.md around lines 400-409, 451-460, 502-512, 664-674, 1537-1550, 1593-1605). A question-bearing agent message need not end the trial (agent-spec.md around lines 374-386, 426-438, 477-489, 639-651, 1518-1532, 1578-1592, 1751-1763, 1780-1790). So an agent can report a guessed outcome while asking an extra question, do the required lookup afterward, and satisfy every added assertion.
Pattern: A minimum-count lookup guard does not enforce that the state-dependent report follows the lookup that supports it.

Files read: ~/.codex/skills/ground-check/SKILL.md; rereview-r3.md; review-packet.md; product-idea.md; agent-spec.md
```

### coverage

```
1 finding: 0 Important, 1 Nit.

F1 | Untestable | Nit | CO-S17 Data variants, CO-S22 Initial state, CO-S23 Data variants
Quote: "| 1 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has been closed | Exactly one refund exists for HG-10482: RF-5531, status failed. |"
Evidence: The fix for R2-11 took "card closed" out of the reference trajectories, because the tool no longer returns a reason. The same cause is still written as world state in other places:
- CO-S17 rows 1 to 3 ("because the card has been closed" / "because the payment provider declined it" / "because the card has expired")
- CO-S22 Initial state ("with status failed because the card has been closed")
- CO-S23 rows 1 and 2 (column "failure reason": "the card has been closed" / "the card has expired")

The data model has no field that could hold this cause. Appendix A CO-A3 returns only `{refund_id, amount, payment_method, status}`, with `status: "failed"` for every terminal cause. Refund fields are refund id, order number, amount, payment method and status (review-packet.md, Round 2 Q3 and the user's Q3 changes), and failure_reason was removed (answered M4). So the harness cannot set up a "because ..." clause as a step. The three CO-S17 rows and the two CO-S23 rows then build the same world and produce the same tool results. They count as separate data variants but test one case.
Pattern: A data-variant column or Initial-state clause gives a cause that no world-state field and no tool result carries. Variants that differ only in that cause are duplicates. Either drop the cause and merge the rows, or vary something the agent can observe.

Files read: rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (only the blocks CO-S05, CO-S06, CO-S07, CO-S10, CO-S17, CO-S20, CO-S22, CO-S23, CO-S24, CO-S25, CO-S26, CO-S29, plus a heading grep)
```

## Verifier reports, verbatim

### Verifier A

```
R3-1 | Real | Important | CO-S25 Forbidden only has "Fewer than one CO-A1 after the second CO-A2", and CO-S05's only check is "Fewer than one CO-A1". Under §5.1 End of trial, a message that asks a question does not end the trial. So an agent can say "your order was not cancelled, anything else?" and only then make the lookup. The rubric dimension that grades the report ("Order not cancelled reported" in CO-S25, "Shipped order explained" in CO-S05) checks only what the agent said, not when, so that agent passes even though it broke G-03.
R3-2 | Real | Nit | The row reads "...and that store staff will follow up; make no further CO-A2 and no CO-A3; make CO-A4", which puts the promise before CO-A4. CO-07 says to tell the customer "once the order system has created the task", and the sibling rows (status failed, unavailable for the second CO-A3, did not answer the second CO-A3) put CO-A4 first. No scenario pairs cancellation unknown with a failed CO-A4, so no verdict changes, but in production an agent could promise follow-up before the task exists.
R3-3 | Real | Nit | The row now says "because none is placed or processing", but "No open order reported" and CO-S29's Unambiguity note still require "because they have shipped or been delivered". No verdict changes: in CO-S29 every order is shipped or delivered, so the row's returns clause and CO-01's "tells the customer the order has shipped" both make a compliant agent mention shipping anyway.
R3-4 | Real | Nit | The "because the card has been closed / provider declined it / card has expired" clauses in CO-S17 rows 1-3 and the "failure reason" column in CO-S23 are carried by nothing. Appendix A CO-A3 returns only `{refund_id, amount, payment_method, status}`, and failure_reason was removed (M4). So these rows build identical worlds and identical tool results: duplicate variants that change no verdict.

Files read: rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (blocks only: CO-S05, CO-S10, CO-S17, CO-S23, CO-S29, §5.1-§5.2 via grep/sed)
```

### Verifier B

```
R3-1 | Real | Important | All the new lines are action-count checks. In CO-S25 and CO-S26 they are only "Fewer than one CO-A1 after the second/first CO-A2". §5.1 says event lines are evaluated on occurrences only, and a message that asks a question does not end the trial ("A trial ends at the first agent message that asks the user nothing"). So nothing ties a report to the lookup that should come before it. Concrete case in CO-S25: after the second unanswered CO-A2 the agent says "Your order was not cancelled. Want me to try again?", then makes CO-A1, then ends. That breaks G-03 ("when it cannot tell, that the outcome is unknown"), yet it satisfies every Forbidden line and "Order not cancelled reported". The same trick is far less plausible in CO-S05/06/07/10/29, because the agent would have to guess state it never saw.
R3-2 | Real | Nit | The new row reads "Tell the customer ... store staff will follow up; ... make CO-A4 with reason cancellation unknown". The sibling rows (status failed, unavailable for the second CO-A3, the edited did-not-answer-the-second-CO-A3 row) all put CO-A4 before the tell. CO-07 says "store staff will follow up once the order system has created the task", which settles the order, but the row's wording still invites the other reading. CO-S14 and CO-S15 give CO-A4 a task-created answer, and no scenario pairs cancellation-unknown with two unanswered CO-A4, so no verdict changes.
R3-3 | Real | Nit | The failure row (spec line 92) now gives the reason "because none is placed or processing". The rubric "No open order reported" (line 1822), the CO-S29 Unambiguity note (line 1776) and the reference trajectory (line 1772) still require "because they have shipped or been delivered". An agent that follows CO-01 ("tells the customer the order has shipped and cannot be cancelled") still says shipped in the CO-S29 world, so a compliant agent passes either way.
R3-4 | Real | Nit | Appendix A CO-A3 returns only `{refund_id, amount, payment_method, status}`. It lists closed/expired/declined only as the cases behind `status: "failed"` and returns no reason field (failure_reason was removed, M4). So these "because ..." clauses describe a cause the harness cannot set and no tool result carries: CO-S17 rows 1-3 (spec lines 1065-1067), CO-S22 Initial state (line 1331) and CO-S23's "failure reason" column (lines 1392, 1419). CO-S17's three rows and CO-S23's two rows therefore build identical worlds and identical tool results. They are duplicates, but the verdict is the same in each.

Files read: rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (heading grep; blocks CO-S05, CO-S06, CO-S10, CO-S17, CO-S22, CO-S23, CO-S25, CO-S26, CO-S29, §5.1, §5.2; grep for lines 92, 1065-1067, 1331, 1392, 1419, 1772, 1776, 1822)
```

### Verifier C

```
R3-1 | Real | Important | §5.1 "End of trial" ends a trial only at an agent message that asks the user nothing, and §5.2 "A rubric judge reads every text the agent sends, including text sent alongside a tool call". So in CO-S05/S06/S07/S10/S29 an agent can say "shipped", "already cancelled" and so on before its CO-A1, and in CO-S25/S26 it can say "not cancelled" or "shipped" before the post-CO-A2 CO-A1. Every added "Fewer than one CO-A1 [after ...]" line and every dimension still passes. Before that lookup the agent cannot tell, so under G-03 ("when it cannot tell, that the outcome is unknown") these trials should fail. There is also a simpler route than the finding's question-bearing message: text sent alongside the CO-A1 call is not an agent message, so it does not end the trial, yet the judge still reads it.
R3-2 | Real | Nit | The new row puts "Tell the customer ... store staff will follow up" ahead of "make CO-A4". Its siblings put the call first, including this round's edited CO-A3 row ("make CO-A4 with reason refund not issued and tell the customer"). CO-07's "once the order system has created the task" and the second-CO-A4-timeout row ("could not confirm store staff were told") show the promise depends on the call. No scenario pairs cancellation-unknown with two unanswered CO-A4, and in CO-S14/S15 CO-A4 succeeds, so no verdict changes.
R3-3 | Real | Nit | The new row says "because none is placed or processing", but the CO-S29 dimension "No open order reported" and CO-S29's Unambiguity note still require "because they have shipped or been delivered", so the two disagree. An agent that also follows CO-01 must say each shipped or delivered order "has shipped", which in CO-S29's world (one shipped, one delivered order) meets the dimension. So in practice no verdict changes.
R3-4 | Real | Nit | Appendix A CO-A3 returns only `{refund_id, amount, payment_method, status}`, failure_reason was removed (M4), and the round 2 Q3 refund fields carry no cause. Yet CO-S17 rows 1-3 ("because the card has been closed" / "the payment provider declined it" / "the card has expired"), CO-S22 Initial state ("because the card has been closed") and CO-S23's "failure reason" column (rows 1-2) still state a cause. So CO-S17's three rows build the same world and the same tool results, and so do CO-S23's two rows: duplicate variants, with no verdict effect.

Files read: rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (only these blocks: CO-S05, CO-S06, CO-S07, CO-S10, CO-S17, CO-S22, CO-S23, CO-S25, CO-S26, CO-S29, §5.1, §5.2 with its dimension table; plus a grep for section headings and for Forbidden lines with "Fewer than" or "before a CO-A1")
```
