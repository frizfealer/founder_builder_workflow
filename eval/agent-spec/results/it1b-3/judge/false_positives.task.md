# Judge task: false_positives for trial it1b-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it1b-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1b-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1b-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M1 (round 1) | Lies | Important | CO-S17 Initial state / Data variants row 3; CO-S24 Initial state; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
- M2 (round 1) | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"
- M3 (round 1) | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
- M4 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- M5 (round 1) | Gap | Important | CO-S02, User knows / Forbidden
- M7 (round 1) | Gap | Important | G-02 / failure row "the customer changed the order or another proposal term in the confirming turn or after confirming"
- M8 (round 1) | Gap | Important | Scope & Authority "must not" / Contract
- M10 (round 1) | Gap | Nit | CO-02 (clarify rule, holding-back direction)
- M11 (round 1) | Gap | Nit | Failure handling, CO-A3
- M12 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state (and CO-S16 row 2)
- M14 (round 1) | Ambiguous | Important | CO-S09, rubric dimension "Refund terms explained"
- M15 (round 1) | Ambiguous | Nit | CO-S03 and CO-S04, User block
- M16 (round 1) | Ambiguous | Nit | CO-07
- M17 (round 1) | Gap | Nit | CO-03; dimensions "Whole order only explained" and "Refund terms explained"
- N1 (round 2) | Lies | Nit | G-04, with CO-06 and the CO-A4 retry row
- N2 (round 2) | Lies | Nit | Failure handling, row "CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it"
- N3 (round 2) | Lies | Nit | CO-S06, Illustrates
- N4 (round 2) | Ambiguous | Important | Forbidden lines of the form "<action> before a CO-A1 made after <earlier action>" in CO-S12, CO-S13, CO-S14, CO-S15, CO-S20, CO-S21, CO-S25, CO-S26
- N5 (round 2) | Ambiguous | Important | Failure row "the order system did not answer the second CO-A2" (the M2 fix), CO-S15 row 2, dimension "Cancellation outcome unknown reported"; CO-S20 row 1, dimension "Refund not confirmed reported"
- N6 (round 2) | Ambiguous | Important | Undefined term "proposal"; dimensions "Order choice asked" (CO-S02) and "Orders unavailable reported" (CO-S10)
- N7 (round 2) | Untestable | Nit | CO-S17 Data variants, CO-S22 and CO-S23 Initial state, the reference trajectories of CO-S17, CO-S22 and CO-S23 (left over from the M4 fix)
- N8 (round 2) | Untestable | Nit | CO-S19 Forbidden
- N10 (round 2) | Gap | Important | CO-01 (no rule or scenario for the confirmed "no time limit")
- N11 (round 2) | Gap | Nit | Failure handling, rows "the lookup shows the named order with status shipped or delivered" / "... with status cancelled"; CO-02
- P1 (round 3) | Lies | Important | §5.2 rubric dimension "Refund not confirmed reported" (used by CO-S20)
- P2 (round 3) | Gap | Important | CO-A3 failure row "first CO-A3 provider unavailable or unanswered" (§4.1 Failure handling)
- P3 (round 3) | Gap | Important | Failure row "the customer asked to cancel only some of an order's items" (CO-03) and CO-S08
- P4 (round 3) | Ambiguous | Nit | CO-09; dimension "No arrival time promised" (CO-S01)
- P5 (round 3) | Ambiguous | Important | CO-02; CO-S07 (dimension "Order not found reported")
- P6 (round 3) | Ambiguous | Nit | Forbidden "CO-A2 before the user's confirmation turn." in CO-S01, CO-S02, CO-S03, CO-S09
- P7 (round 3) | Ambiguous | Nit | Dimension "Shipped order explained" (CO-S05, CO-S11, CO-S26)
