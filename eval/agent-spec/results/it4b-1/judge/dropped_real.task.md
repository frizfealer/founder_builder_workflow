# Judge task: dropped_real for trial it4b-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4b-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4b-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-15 (round 1) | Ambiguous | Important | CO-S16 row 2, Required events

```
R1-15 | Ambiguous | Important | CO-S16 row 2, Required events
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (line 979). A valid variant does a CO-A1 after that timeout and sees RF-5531 pending. The rules permit reporting it and stopping:
- G-03 (line 24): the agent may report a status "a lookup shows".
- CO-06 (line 77): "It makes a second CO-A3 only after…" is a permission, not a duty.
- G-04 (line 27) is also a permission.
- The CO-08 success guarantee (line 83) is fully met.
But the failure row (line 102) says "Make CO-A3 once more" with no condition, and the Required line fails an agent that stops. One expert reading the rules passes that trajectory and another reading the failure row fails it. The checklist's "Outcome, not path" (evaluation-checklist.md line 16) warns against punishing a valid path, and the brief lists "different read-only lookups" as a valid variant.
Pattern: A Required call count for a retry that the rules only permit fails an agent whose lookup has already made the retry unnecessary. Either the rule must make the retry mandatory, or the count must allow one or two calls.
Source: verdicts F3.
```

- R3-02 (round 3) | Lies | Nit | CO-S09, Reference trajectory step 3

```
R3-02 | Lies | Nit | CO-S09, Reference trajectory step 3
Quote: "3. Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation."
Evidence: CO-S09 is graded by rubric dimension "Refund terms explained" (§5.2, line 1524): "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit." The scenario's Unambiguity note (line 608) says the same: "checks the agent said the refund goes to the order's payment method for the total paid". Step 3 says only that the refund goes to the order's payment method. It never says the refund is the total paid. Stating "$86.40" in the proposal does not say that $86.40 is the order's total paid. CO-03 (line 68) also requires "the refund is the total paid to the order's payment method". So the reference trajectory, run as written, does not clearly pass its own scenario's dimension. (This is separate from R2-05, which is about which statement goes with which CO-03 trigger. Here the trajectory is checked against the dimension the scenario already uses.)
Pattern: A reference trajectory's agent message must contain every statement that the scenario's rubric dimensions require. Otherwise the worked example fails its own grader.
Source: faithfulness F2.
```

