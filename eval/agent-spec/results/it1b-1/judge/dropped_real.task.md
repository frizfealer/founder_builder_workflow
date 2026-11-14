# Judge task: dropped_real for trial it1b-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1b-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1b-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M7 (round 1) | Gap | Important | G-03 / CO-08, success-path scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16

```
## M7
F2 | Gap | Important | G-03 / CO-08, success-path scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
Quote: "The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: On every success path, the only check on the agent's words is the code message check "Refund id reported" (§5.2 line 1497). The refund status the agent states is never checked. In all of these scenarios the refund is pending, and an agent that says "your refund has been issued" passes. The dimension "Refund status reported" (line 1507) exists but only CO-S19 uses it. Known failure case 3 in the packet (review-packet.md line 54: "Cancel succeeded, refund call timed out ... Final message must match the final refund status") is exactly CO-S16 rows 2 and 3, where the first refund call times out and the retry returns pending. Those rows assert only the refund id, so the known case's own pass condition goes untested there. The customer's interest "to be told truthfully ... where the refund stands" (§2 line 9) has no assertion on any success exit.
Pattern: A truthfulness rule is asserted by rubric only on failure exits. Every exit where the agent reports a status (pending or issued) needs a dimension that checks the stated status against the tool result.
```

- N1 (round 2) | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported" (CO-S14, CO-S15) and "Refund status reported" (CO-S19)

```
## N1
F1 | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported" (CO-S14, CO-S15) and "Refund status reported" (CO-S19)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, ..." and "| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it. |"
Evidence: Each of these rubrics requires the agent to say something that neither the failure row it grades nor the inputs ask for. An agent that follows the row exactly fails the judge.
- CO-S14 and CO-S15 are graded under the CO-A2 failure rows "did not answer the first CO-A2" (agent-spec.md line 103) and "did not answer the second CO-A2" (line 104). Both rows give the message for a lookup that does not answer as "tell the customer it is not known whether the order was cancelled and store staff will follow up". Neither row mentions the refund. The input, review-packet.md Round 3 Q4 ("Re-read fails, say outcome unknown, issue no refund, hand off"), makes "issue no refund" an action, not something to say. The added clause "that no refund was issued" appears only in the rubric (line 1631) and in the reference steps CO-S14 step 8 (line 879) and CO-S15 step 10 (line 940).
- CO-S19 is graded under the CO-A3 row "did not answer the second CO-A3" (line 108): "If the lookup shows the refund pending or issued, tell the customer that status and the refund id". The input, review-packet.md Round 3 Q3 ("pending or issued, report that status"), and CO-08 (line 83, "the agent tells the customer the refund id") also do not require saying the order is cancelled. The rubric (line 1635) adds "tells the customer the order is cancelled".
Pattern: a rubric dimension requires the agent to say more than the failure row or rule it grades, so an agent that follows the row fails. Every "tells the customer" clause in a dimension should match the "Tell the customer" clause of the failure row or rule it grades, or the row should gain that clause.
```

- P4 (round 3) | Ambiguous | Important | §5.1 "Confirmation question"; Appendix A "Value comparison"; every scenario with a confirmation-form User-knows pair (CO-S01–S03, CO-S09, CO-S11–S26)

```
## P4
F4 | Ambiguous | Important | §5.1 "Confirmation question"; Appendix A "Value comparison"; every scenario with a confirmation-form User-knows pair (CO-S01–S03, CO-S09, CO-S11–S26)
Quote: "A payment method compares by card brand and last four digits."
Evidence: §5.1 (line 1588) defines the confirmation question as "a question that states every value of the proposal". It also says "Each proposal value the question states must equal that value in the confirmation-form pair it matches... A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it." The spec does not say what counts as stating the payment method. Take the valid phrasing "Shall I cancel HG-10482 and refund $86.40 to your card ending 4242?". It gives no brand, so by line 1648 it may not equal "Visa ending 4242". One reader calls it a wrong-value question and the simulated user deflects. Another reads it as stating the payment method and the user confirms. The same split applies to "refund $86.40 to your original payment method". CO-04 (line 71) requires confirming "order number, refund amount and payment method", and the input (packet Round 1 Q4) requires "where it goes". Whether the simulated user says "Yes" decides whether any of CO-A2's and CO-A3's Required events can occur, so the same trajectory can pass or fail depending on the reader.
Pattern: A value comparison that gates the simulated user's confirmation does not say how a partly written value compares (here, a payment method without its brand, or named only generically). State the minimum form that counts as stating each proposal value, for example "a card's last four digits suffice when the customer has one card with them", or require both brand and last four and say a question without them is a partial question.
```

