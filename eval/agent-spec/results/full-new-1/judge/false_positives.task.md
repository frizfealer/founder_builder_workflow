# Judge task: false_positives for trial full-new-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/full-new-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/full-new-1/agent-spec-final.md` is the end state.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO failure handling, row "CO-A2 | the order system did not answer the second CO-A2"
- R1-02 (round 1) | Lies | Important | CO failure handling row "CO-A3 | ... or reported the order not cancelled"; CO-07; CO-S17 row 3
- R1-03 (round 1) | Lies | Important | CO failure handling row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20
- R1-04 (round 1) | Lies | Important | §5.2 rubric dimensions "Cancellation outcome unknown reported" and "Refund status reported"
- R1-05 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-06 (round 1) | Gap | Important | §4.1 Contract (no rule); §5.2 dimension table
- R1-07 (round 1) | Gap | Important | Failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" (line 96); G-02, CO-04
- R1-08 (round 1) | Gap | Important | G-03; success-path scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16; CO-08
- R1-09 (round 1) | Gap | Nit | Failure row "the order system did not answer the first CO-A2" (line 100)
- R1-10 (round 1) | Gap | Nit | §4.1 Failure handling (rows at lines 90-93); CO-01, CO-02
- R1-12 (round 1) | Lies | Nit | G-04; Appendix B SG-04
- R1-13 (round 1) | Gap | Important | CO-01 / CO-S06; row "the lookup shows the named order with status cancelled"
- R1-14 (round 1) | Gap | Important | G-01 / CO-06 / CO-02
- R1-15 (round 1) | Gap | Nit | CO-02 (act-only-when, holding-back side)
- R1-16 (round 1) | Gap | Nit | CO-A3 failure row "payment provider temporarily unavailable for the second CO-A3"
- R2-01 (round 2) | Gap | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (with CO-S15)
- R2-02 (round 2) | Gap | Important | CO-S26, Required events / Forbidden
- R2-03 (round 2) | Lies | Important | failure: CO-A3 | the order system reported the order not cancelled (new)
- R2-05 (round 2) | Lies | Nit | CO-S27 Initial state (also CO-S17 row 3)
- R2-06 (round 2) | Lies | Nit | scenario: CO-S17, Reference trajectory step 6 (same line in CO-S22 and CO-S23)
- R2-07 (round 2) | Lies | Nit | scenario: CO-S26, Unambiguity note
- R2-08 (round 2) | Gap | Important | CO-09; No arrival date promised
- R2-L1 (round 2) | Ambiguous | Important | CO-S19, CO-S20 and CO-S21, Initial state
- R3-01 (round 3) | Gap | Important | failure row CO-A3 "the order system reported the order not cancelled" (section 3), placed-or-processing branch
- R3-02 (round 3) | Gap | Important | CO-S15, CO-S20, CO-S21, CO-S25, CO-S26, CO-S28
