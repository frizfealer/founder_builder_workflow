# Judge task: dropped_real for trial it4b-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4b-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4b-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-02 (round 1) | Lies | Important | CO-A3 failure row "reported the payment provider temporarily unavailable for the second CO-A3"

```
### R1-02 (from faithfulness F2)

R1-02 | Lies | Important | CO-A3 failure row "reported the payment provider temporarily unavailable for the second CO-A3"
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
Evidence: The row before it (line 102) sends the agent to a second CO-A3 when the first "reported the payment provider temporarily unavailable ... or did not answer it". So this row also fires when the first CO-A3 timed out. Appendix A says "A timeout creates the refund or not as Initial state says", and CO-S16 row 2 shows a timed-out first call that did create refund RF-5531 pending. The input for a timed-out refund is: "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds" (packet, round 2 Q4 answer, case 3). Round 3 Q3 adds: "For case 3, after the retry the agent re-reads the refund record". This row skips the re-read and states as fact "the refund has not been issued", even though a pending refund may exist. That also breaks G-03 ("when it cannot tell, that the outcome is unknown"). With reason `refund_not_issued`, store staff (SG-02, "completing the refund ... by hand") could pay a second refund.
Pattern: A failure row is keyed only on the second call's result and ignores the first call's unknown result. A path the inputs require to end in a re-read ends in an unverified claim instead.
```

- R1-11 (round 1) | Ambiguous | Important | CO-S16 (row 2), CO-S19–CO-S21, Required events; CO-A3 failure row

```
### R1-11 (from verdicts F2)

R1-11 | Ambiguous | Important | CO-S16 (row 2), CO-S19–CO-S21, Required events; CO-A3 failure row
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: agent-spec.md line 962 (CO-S16). Row 2 (line 979): the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". Take a valid variation: after the unanswered first CO-A3, the agent runs CO-A1 (lookups are unlimited, line 1519), sees RF-5531 pending, reports it and does not retry. G-04 (line 27) only permits a repeat ("repeats it only when ... or when the order system guarantees ..."); it does not require one. CO-08 (line 83) is fully met. But the failure row (line 102), "did not answer it | Make CO-A3 once more", does not say whether a lookup that already shows the outcome removes the retry, and the Required event fails this agent. One expert passes it on outcome; another fails it on the row. evaluation-checklist.md line 16 says "Outcome, not path ... agents find valid paths the author did not anticipate, and a path assertion punishes them." The same exposure applies to CO-S19/S20/S21 (lines 1132, 1189, 1249) whenever the harness resolves F1 so that the first call created the refund. In CO-S19 it then also leaves "after the second CO-A3" (line 1141) without a referent.
Pattern: a retry required after an unknown result must say what happens when a lookup made in between already shows the outcome. Either the failure row branches on that lookup, or the Required count accepts both paths.
```

- R2-01 (round 2) | Lies | Important | CO-A2 failure rows "did not answer the first CO-A2" and "did not answer the second CO-A2" vs §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)

```
### R2-01 (from faithfulness F1)

R2-01 | Lies | Important | CO-A2 failure rows "did not answer the first CO-A2" and "did not answer the second CO-A2" vs §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: The failure rows that CO-S14 and CO-S15 trigger only require the agent to say the outcome is unknown and that staff will follow up. Neither asks it to say anything about the refund. The first-CO-A2 row (agent-spec.md line 100) and the second-CO-A2 row (line 101) both read: "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown." The input does not require a refund statement either. Round 3 Q4 (review-packet.md) says: "Re-read fails, say outcome unknown, issue no refund, hand off." That is an action ("issue no refund"), not something to tell the customer. The clause "no refund was issued" appears only in the CO-A3 "reported the order not cancelled" row (line 104), and no scenario triggers that row. So an agent that does exactly what the CO-A2 rows say fails the dimension, and therefore fails CO-S14 and CO-S15. The reference trajectories (CO-S14 step 8, CO-S15 step 10) also include "no refund was issued", which the rows do not support.
Pattern: A rubric dimension requires the agent to tell the customer something that the failure row the scenario triggers (and the inputs) never requires. Either add the clause to the row or drop it from the dimension and the trajectory.
```

- R2-14 (round 2) | Untestable | Nit | CO-S02, Final state assertions

```
### R2-14 (from verdicts F6)

R2-14 | Untestable | Nit | CO-S02, Final state assertions
Quote: "- The customer's other order is unchanged and has no refund."
Evidence: The order this line refers to changes by row: HG-10482 in rows 1 and 3, HG-10511 in row 2 (Data variants, lines 214-216). It has no column and is not written as one. SKILL.md step 3.6 says "Every value that differs between rows gets a column". To become a step, the line must be reworded to name the order, as CO-S01 does with "HG-09977 is unchanged and has no refund." (line 141).
Pattern: A final-state line points to a record by its relation to a column value ("the other order") instead of naming it. Add a column, such as <other order>, and write the line with it.
```

- R3-02 (round 3) | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory

```
### R3-02 (from faithfulness F2)

R3-02 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A gives CO-A3's result shape as `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` (line 1891), with no field for why it failed. The R1-04 fix removed `failure_reason` from Appendix A on purpose (answered.md R1-04: "Appendix A CO-A3 outcome no longer names a `failure_reason` field"). The three trajectories still show a tool result that carries the cause:
- CO-S17 step 6 (line 1050)
- CO-S22 step 6 (line 1343)
- CO-S23 step 6 (line 1401)
No dimension needs the cause, so no verdict changes. A builder reading the trajectories would still expect the tool to return a reason it does not return.
Pattern: A reference trajectory's tool result contains a value that the bound tool's result shape does not have. Trim each such result to the fields Appendix A lists (here "refund RF-5531, failed"), and leave the cause in Initial state only.
```

