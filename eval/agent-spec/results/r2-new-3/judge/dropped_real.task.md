# Judge task: dropped_real for trial r2-new-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round1-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. Do NOT open the round*-findings.md files: they carry the verifier's refutation, and you are judging the finding against the spec and the inputs, not the refutation. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/r2-new-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/r2-new-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M18 (round 2) | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28

```
## M18

M18 | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28
Quote: "absent"
Evidence: CO-01 requires a lookup showing placed or processing before a proposal. None of these scenarios checks for that initial lookup. Their reference trajectories perform CO-A1, but their Expected and Forbidden checks let an agent guess the proposal values and still pass. (CO-S11 and CO-S15 at bundle lines 54-172; CO-S25 and CO-S26 at 173-288; CO-S27 and CO-S28 at 289-463; CO-01 in bundle §4.)
Pattern: A scenario checks that the agent reached the correct proposal or outcome but omits the observable lookup the contract requires before the agent may know it.
```

- N3 (round 3) | Ambiguous | Nit | failure: any | every lookup made after an unanswered CO-A2 did not answer or answered without the order, and the agent makes no further lookup

```
## N3

N3 | Ambiguous | Nit | failure: any | every lookup made after an unanswered CO-A2 did not answer or answered without the order, and the agent makes no further lookup
Quote: "| any | every lookup made after an unanswered CO-A2 did not answer or answered without the order, and the agent makes no further lookup | Tell the customer it is not known whether the order was cancelled, ... make CO-A4 with reason cancellation unknown. | CO-07, G-03 |"
Evidence: In CO-S15 the lookup made after the first unanswered CO-A2 answers with the order (reference step 6 "Agent → CO-A1 → HG-10482 still processing"). Read literally, "every lookup made after an unanswered CO-A2 did not answer" is false there, yet CO-S15 requires this row's action ("CO-A4 occurs exactly once, for <order>, reason cancellation unknown, after the second CO-A2 for <order>"). The neighbouring row is bounded ("after the first CO-A2 went unanswered, and before any second CO-A2"); this one does not say which CO-A2 when there are two. CO-07 ("cannot tell whether its own CO-A2 cancelled the order") still settles the verdict.
Pattern: A failure-row condition over "an unanswered CO-A2" does not say which one when two can occur; scope it to the most recent unanswered CO-A2.
```

