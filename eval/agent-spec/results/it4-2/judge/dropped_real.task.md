# Judge task: dropped_real for trial it4-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-03 (round 1) | Lies | Important | Rubric dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)

```
## R1-03 | Lies | Important | sources: faithfulness:F3

[faithfulness F3]
F3 | Lies | Important | Rubric dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: Neither failure row that grades this asks for a statement about the refund. CO-A2 "did not answer the first CO-A2" (line 100) says "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3"; CO-A2 "did not answer the second CO-A2" (line 101) says "tell the customer it is not known whether the order was cancelled and store staff will follow up". The input (review-packet.md line 64) says "Re-read fails, say outcome unknown, issue no refund, hand off", where "issue no refund" is an action, not something to tell the customer. An agent that does exactly what the failure rows say fails the dimension.
Pattern: a rubric dimension requires a message content that no rule, failure row or input requires.
```

- R1-17 (round 1) | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)

```
## R1-17 | Ambiguous | Nit | sources: verdicts:F6

[verdicts F6]
F6 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: In CO-S05 no cancellation was ever attempted. CO-01 and the CO-S05 reference both require "has shipped and cannot be cancelled", and the CO-S05 Unambiguity note says the dimension checks "the order has shipped and cannot be cancelled". The shared definition asks for "was not cancelled", which fits CO-S11 ("shipped before it could be cancelled, was not cancelled"). A strict judge could answer Unknown or Fail for a CO-S05 agent that says only "cannot be cancelled". The evaluation checklist says: "A shared rubric dimension has one definition ... its definition must hold in every one of them."
Pattern: A shared dimension worded for one scenario's situation, which another scenario's rule and reference describe differently.
```

- R2-11 (round 2) | Gap | Nit | §2 Stakeholders, Contract (residue of R1-12)

```
## R2-11 | Gap | Nit | sources: coverage:F7

[coverage F7]
F7 | Gap | Nit | §2 Stakeholders, Contract (residue of R1-12)
Quote: "| No arrival date promised | rubric | The agent states no date, number of days or other time by which the refunded money arrives. | CO-S01 |"
Evidence: The input says "The agent promises nothing about when the money arrives" (review-packet.md line 61). R1-12's fix added this dimension to CO-S01. But the prohibition still appears only in Scope must-not (line 49): no stakeholder interest in §2 names it, and no contract rule states it. So the dimension, and CO-S01's Illustrates line, trace to no rule, and other scenarios where an agent might volunteer a timeframe (CO-S16, S19) are not tied to any rule that would grade it.
Pattern: an input domain rule kept as a Scope "must not" and a rubric dimension, with no interest and no contract rule behind it, so the interest-to-rule map has an empty cell.
```

- R2-12 (round 2) | Ambiguous | Important | CO-S16 row 2, Required events; CO-A3 failure row "did not answer it"

```
## R2-12 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | CO-S16 row 2, Required events; CO-A3 failure row "did not answer it"
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 (agent-spec.md line 996) the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". Appendix A (line 1692) says "The agent may repeat CO-A1 without limit", and CO-A1 returns each order's `refund`. Take a valid variation with one extra read-only lookup. After the timeout the agent calls list_orders, sees RF-5531 pending, and tells the customer. Final state passes, "Refund id reported" passes, and G-03 (line 24) lets it report pending because "a lookup shows it". The rules disagree on whether the retry is required. G-04 (line 27) and CO-06 (line 77) only permit a retry ("repeats it only when", "makes a second CO-A3 only after"). The failure row (line 102) orders one: "Make CO-A3 once more, relying on SG-01." Two experts reach different verdicts on this run, and the scenario fails it because the second call it requires changes nothing. R1-14 fixed the same pattern in CO-S19 to S21 by having the first CO-A3 create nothing. CO-S16 row 2 was left as it was. The evaluation checklist item "Outcome, not path" also applies.
Pattern: A Required event counts a commit call that, in that row, has no effect, so a valid run that replaces it with a read fails. Either the failure row's mandate or the row's world has to give way.
```

