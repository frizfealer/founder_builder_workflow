# Judge task: dropped_real for trial it2-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it2-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it2-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-06 (round 1) | Ambiguous | Important | CO-S16, Required events / Data variants row 2

```
## R1-06 (from verdicts F2)

R1-06 | Ambiguous | Important | CO-S16, Required events / Data variants row 2
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Row 2 (line 979) says the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". A valid variation calls CO-A1 after that unanswered call (lookups are unlimited, line 1519) and sees RF-5531 pending. At that point CO-08's success guarantee (line 83) already holds. G-04 (line 27) only permits a repeat; it does not require one. A reasonable agent reports RF-5531 and stops. It then fails "exactly twice", even though the failure row for an unanswered first CO-A3 (line 102, "Make CO-A3 once more") never anticipated a lookup in between. Two experts would disagree on whether skipping the now-pointless retry is a failure. The brief requires that a scenario pass a variation with different read-only lookups.
Pattern: A Required count on retries fails an agent whose extra lookup shows the first call already took effect. Either require the retry only when no lookup between the calls showed the effect, or state in Initial state what the lookup shows.
```

- R1-07 (round 1) | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)

```
## R1-07 (from verdicts F4)

R1-07 | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows this dimension grades require only "tell the customer it is not known whether the order was cancelled and store staff will follow up". These are the CO-A2 "did not answer the first CO-A2" row (line 100, lookup-unanswered branch) and the "did not answer the second CO-A2" row (line 101). No rule or failure row requires saying "no refund was issued". An agent that follows those rows to the letter fails the dimension in CO-S14 and CO-S15. One grader goes by the rules, another by the dimension, and the verdicts differ.
Pattern: A rubric dimension must ask for exactly what the rule or failure row it grades requires. Add the clause to the failure rows, or drop it from the dimension.
```

- R1-12 (round 1) | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 (success scenarios), against G-03 and the customer's interest

```
## R1-12 (from coverage F3)

R1-12 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 (success scenarios), against G-03 and the customer's interest
Quote: "message check \"Refund id reported\" matches the row's refund id." (CO-S01 Unambiguity note; the same single check closes each listed scenario)
Evidence: G-03 says the agent "tells the customer a refund is pending or issued only when the order system returned that refund with that status" (line 24). The primary actor "wants to be told truthfully whether the order was cancelled and where the refund stands" (line 9). Known failure case 3 says "Final message must match the final refund status" (review-packet.md line 54). In the listed scenarios the refund ends in status pending, and the only check on the agent's words is the code message check for the refund id (§5.2 line 1497). Nothing checks that the agent says the order is cancelled or that the refund is pending rather than issued or already back on the card. Only CO-S19 has "Refund status reported" (line 1507). This matters most in CO-S16 row 2, where the first refund call timed out but still created a pending refund (line 979). An agent that reports "your refund has been issued" passes all of these scenarios.
Pattern: A truthfulness rule about reporting a status (G-03) is asserted on the failure paths and in one success-after-lookup scenario, but on the ordinary success path the only check is the verbatim id. No rubric dimension checks the reported cancellation and refund status.
```

- R2-09 (round 2) | Ambiguous | Nit | G-04 (with CO-06, Appendix B SG-04)

```
## R2-09 (from verdicts F6)

R2-09 | Ambiguous | Nit | G-04 (with CO-06, Appendix B SG-04)
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1672) guarantees that cancelling an already cancelled order "changes nothing". Under G-04's second clause, that would allow a blind second CO-A2 after an unanswered one. CO-06 (line 77) allows a second CO-A2 "only after ... a lookup made after it shows the order still placed or processing". The interview (review-packet.md, round 3 Q4) says "no blind resend; re-read the order". CO-S12 forbids "A second CO-A2". CO-S22 cites G-04 for a retry that rests on SG-03, so the parenthetical "SG-01" reads as an example, not a limit. Two readers of G-04 disagree on whether a blind CO-A2 retry is allowed. The scenarios are explicit, so no verdict changes.
Pattern: A global retry rule that allows any idempotent repeat must exclude the actions whose capability rule forbids a blind repeat, or name exactly which guarantees qualify.
```

- R3-01 (round 3) | Lies | Important | §5.2 rubric dimensions "Cancellation outcome unknown reported" (CO-S14, CO-S15) and "Refund status reported" (CO-S19)

```
## R3-01 (from faithfulness F1)

R3-01 | Lies | Important | §5.2 rubric dimensions "Cancellation outcome unknown reported" (CO-S14, CO-S15) and "Refund status reported" (CO-S19)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; it never says the order was cancelled, and its final message does not say the order was not cancelled."
Evidence: Neither the inputs nor the spec's own rules ask the agent to say these things. Round 3 Q4 (review-packet.md, "Round 3"), confirmed by the user, says: "Re-read fails, say outcome unknown, issue no refund, hand off." There, "issue no refund" is an action limit, not something the agent must tell the customer. The failure rows for that case (agent-spec.md lines 103 and 104, "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4") only require saying "not known whether cancelled" and "staff will follow up". So an agent that does exactly what the row says fails CO-S14 and CO-S15. The same thing happens with "Refund status reported" (line 1757: "The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status"). Its failure row (line 108, "If the lookup shows the refund pending or issued, tell the customer that status and the refund id") does not require saying the order is cancelled. An agent that reports only "refund RF-5531 is pending" follows CO-S19's row but fails the dimension. Every other rubric dimension's required statements match its failure row or rule.
Pattern: A rubric dimension requires the agent to say something that no rule or failure row requires, so it adds an obligation the contract and inputs do not support. Each dimension's required statements should match its failure row's "tell the customer" clause exactly, or the failure row and rule should be changed to require the statement.
```

- R3-09 (round 3) | Gap | Nit | CO-S08 and CO-S28, Initial state

```
## R3-09 (from coverage F4)

R3-09 | Gap | Nit | CO-S08 and CO-S28, Initial state
Quote: "- Order HG-10530 belongs to the customer, with status placed, items 1 × Stoneware mug set at $28.00 and 1 × Linen napkins, set of 4, at $16.00, total paid $53.50, payment method Amex ending 1007."
Evidence: Appendix A (line 1775) has list_orders return `shipping` and `tax` for each order. The packet's round 2 Q2 proposes "the full amount paid (items, shipping and tax)", and Q3 lists the fields "shipping cost, tax, total paid". The line items add up to $44.00 against $53.50 total paid, and neither scenario states shipping or tax (lines 510 and 1652). The harness has to invent $9.50 of shipping and tax for the record to hold together, and the reader cannot see that the total satisfies the contract's total-paid relation. The evaluation checklist ("Concrete initial state") and the Specification-by-Example checklist ("State every attribute the rule depends on") both call for these values.
Pattern: when Initial state gives some of the values that make up a derived field (the line items of total paid), it must give all of them (shipping and tax) so that the stated total follows from them.
```

