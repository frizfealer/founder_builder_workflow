# Judge task: false_positives for trial it2-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it2-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it2-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it2-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; failure rows CO-A3 "reported the order not cancelled" and CO-A2 "reported the order not found"
- R1-02 (round 1) | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2" (and CO-S15 reference trajectory step 8)
- R1-03 (round 1) | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; dimension "Refund not issued reported" as used by CO-S20
- R1-04 (round 1) | Lies | Nit | Appendix A, CO-A3 row "Outcomes, as tool results"
- R1-05 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- R1-08 (round 1) | Untestable | Nit | §5.1 End of trial (CO-S10, CO-S14, CO-S15, CO-S21)
- R1-09 (round 1) | Ambiguous | Nit | CO-S03, CO-S04, User block
- R1-10 (round 1) | Gap | Important | G-02 / Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
- R1-11 (round 1) | Gap | Important | Section 2 Stakeholders / Section 4.1 Contract (no rule); Scope & Authority "must not"
- R1-13 (round 1) | Gap | Nit | Failure handling row "CO-A2 | the order system did not answer the first CO-A2"
- R1-14 (round 1) | Gap | Nit | G-01 / Failure handling (no row) / Scenarios (none)
- R2-01 (round 2) | Gap | Important | CO-S13 row 3 and CO-S26, Forbidden (failure row "the order system did not answer the second CO-A2")
- R2-02 (round 2) | Gap | Important | CO-S02, User knows / Expected (CO-02)
- R2-03 (round 2) | Lies | Nit | CO-S06, Illustrates
- R2-04 (round 2) | Gap | Important | CO-S08 / Failure handling row "the customer asked to cancel only some of an order's items" (CO-03)
- R2-05 (round 2) | Gap | Nit | CO-02, Scenarios
- R2-06 (round 2) | Ambiguous | Important | CO-S03 User Turn 2; CO-S04 User Turn 2
- R2-07 (round 2) | Ambiguous | Important | Evaluation dimension "Cancellation outcome unknown reported" (used by CO-S15)
- R2-08 (round 2) | Untestable | Nit | CO-S19, Forbidden
- R3-02 (round 3) | Lies | Nit | §2 Stakeholders & Interests, Offstage stakeholders
- R3-03 (round 3) | Ambiguous | Important | CO-09, §5.2 dimension "No arrival date promised" (used by CO-S01)
- R3-04 (round 3) | Ambiguous | Important | CO-S20, §5.2 dimension "Refund not confirmed reported"; CO-A3 failure row "did not answer the second CO-A3"
- R3-05 (round 3) | Ambiguous | Important | CO-03 failure row "the customer asked to cancel only some of an order's items"; CO-02; scenarios CO-S07, CO-S08, CO-S28
- R3-06 (round 3) | Gap | Important | CO-05 / CO-01, Scenarios (no scenario has a cancelled order with no refund or a failed refund)
- R3-07 (round 3) | Gap | Nit | CO-02 / CO-01, Failure handling
- R3-08 (round 3) | Gap | Nit | Failure handling, lookup rows (lines 92, 103, 104, 108)
