# Judge task: false_positives for trial it1b-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it1b-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1b-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1b-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M1 (round 1) | Lies | Important | CO-A2 failure row "did not answer the second CO-A2" (§4.1 Failure handling); CO-S15
- M2 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state
- M3 (round 1) | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20 Reference trajectory step 10; dimension "Refund not issued reported" as used by CO-S20
- M4 (round 1) | Lies | Nit | G-04
- M5 (round 1) | Lies | Nit | Appendix A, CO-A3 row "Outcomes, as tool results"
- M6 (round 1) | Gap | Important | G-02 / CO-04, Failure handling row "changed ... in the confirming turn or after confirming"
- M8 (round 1) | Gap | Important | Scope & Authority "must not" / Contract (no rule)
- M9 (round 1) | Gap | Nit | CO-02 / Failure handling (unnamed request)
- M10 (round 1) | Gap | Nit | Failure handling row "did not answer the first CO-A2"
- M11 (round 1) | Gap | Nit | CO-07 "once the order system has created the task" / CO-S22
- M12 (round 1) | Gap | Important | CO-S05, CO-S06, CO-S07 (§5.2 rubric dimensions "Shipped order explained", "Already cancelled reported", "Order not found reported")
- M13 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21 Initial state; CO-S16 row 2; Required events "CO-A3 occurs exactly twice"
- M14 (round 1) | Untestable | Nit | CO-S19 Forbidden
- N2 (round 2) | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory step 6 (incomplete fix of M5)
- N3 (round 2) | Ambiguous | Important | §5.2 dimensions "Order not found reported", "Already cancelled reported", "Shipped order explained", "Orders unavailable reported"; CO-S07 Unambiguity note; CO-S08 failure row and Reference trajectory; CO-S03 and CO-S04 User Turn 2 trigger
- N4 (round 2) | Untestable | Nit | CO-S20 Final state assertions / Data variants
- N5 (round 2) | Gap | Important | CO-S02, User knows / Forbidden / Unambiguity note (CO-02 "asks which and proposes nothing until the customer names one")
- N6 (round 2) | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden; §5.1 Turn anchors
- N7 (round 2) | Gap | Important | CO-01 / CO-07, Failure handling row "...with status cancelled"; CO-S06
- N8 (round 2) | Gap | Nit | CO-01 / CO-02, Failure handling rows for an unnamed request (lines 93-96)
- N9 (round 2) | Gap | Nit | CO-A3 Failure handling; CO-03 / CO-08
- P1 (round 3) | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-S26 row 2
- P2 (round 3) | Ambiguous | Important | CO-S02, §5.2 dimension "Asked which order first"
- P3 (round 3) | Ambiguous | Important | §5.2 dimensions "Order not found reported", "Shipped order explained", "Already cancelled reported", "Orders unavailable reported"; CO-S07 Unambiguity note (incomplete fix of answered N3 / M12)
- P5 (round 3) | Untestable | Important | §5.1 "End of trial"; CO-06; Appendix A "Which order an action is for"; failure rows for an unanswered lookup; CO-S10, CO-S14, CO-S15, CO-S21
- P6 (round 3) | Lies | Nit | CO-S06, Illustrates
- P7 (round 3) | Lies | Nit | CO-S05, Unambiguity note
- P8 (round 3) | Gap | Important | G-02 / CO-03 / CO-04, Failure handling row "changed the order or another proposal term in the confirming turn or after confirming"
- P9 (round 3) | Gap | Nit | CO-06 / G-01 / Purpose; Failure handling (absent)
- P10 (round 3) | Gap | Nit | CO-03; dimensions "Whole order only explained" (CO-S08) and "Refund terms explained" (CO-S09)
