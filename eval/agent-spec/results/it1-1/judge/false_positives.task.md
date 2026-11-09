# Judge task: false_positives for trial it1-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it1-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M1 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; CO-A3 and CO-A2 failure rows
- M3 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- M4 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- M5 (round 1) | Gap | Important | CO-S02, Expected / Forbidden
- M6 (round 1) | Untestable | Important | §5.1 End of trial with CO-S10, CO-S14, CO-S15, CO-S21
- M7 (round 1) | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
- M8 (round 1) | Ambiguous | Nit | CO-S03, CO-S04, User block
- M9 (round 1) | Gap | Important | CO capability, Contract (missing rule); §5.2 dimensions; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19
- M10 (round 1) | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; CO-S03
- M11 (round 1) | Gap | Important | Failure handling rows for unanswered lookups (CO-A1); CO-S10, CO-S14, CO-S21
- M12 (round 1) | Gap | Nit | CO-03; CO-S09 Data variants
- M13 (round 1) | Gap | Nit | CO-02 (holding-back direction)
- M14 (round 1) | Gap | Nit | Failure handling row "the order system did not answer the first CO-A2"
- N1 (round 2) | Lies | Important | CO-07; §4.1 Failure handling, CO-A3 rows "did not answer the second CO-A3" and "returned the refund with status failed, or reported the order not cancelled"; CO-S20; dimension "Refund not issued reported"
- N2 (round 2) | Lies | Nit | §4.1 Failure handling, CO-A3 row "returned the refund with status failed, or reported the order not cancelled"; CO-06
- N3 (round 2) | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
- N5 (round 2) | Ambiguous | Important | "propose"/"states a proposal" at message level: CO-01, CO-02, CO-S02 dimension "Order choice asked", CO-S08 failure row, CO-S10 dimension
- N6 (round 2) | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
- N8 (round 2) | Untestable | Nit | CO-S19, Forbidden
- N9 (round 2) | Gap | Important | CO-A2 failure row "the order system did not answer the second CO-A2"
- N10 (round 2) | Gap | Important | CO-A2 failure row "did not answer the first CO-A2", branch "answers without listing the order"
- P1 (round 3) | Lies | Important | CO-S15, Reference trajectory (and Forbidden)
- P2 (round 3) | Lies | Nit | CO-S10, Reference trajectory
- P3 (round 3) | Lies | Nit | CO-S19, Unambiguity note
- P4 (round 3) | Lies | Nit | G-04 (cited by the CO-A4 failure row)
- P5 (round 3) | Ambiguous | Important | §5.2 rubric dimension "Order not found reported" (CO-S07)
- P6 (round 3) | Ambiguous | Important | §5.2 rubric dimension "Refund terms explained" (CO-S09)
- P8 (round 3) | Gap | Important | CO-02; Failure handling (lookup rows)
