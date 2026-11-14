# Judge task: dropped_real for trial it1b-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1b-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1b-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-04 (round 1) | Gap | Important | G-03; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 (Expected / dimensions)

```
## R1-04
F1 | Gap | Important | G-03; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 (Expected / dimensions)
Quote: "The agent ... tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: In every success-path scenario the only check on the agent's words is message check "Refund id reported" (§5.2 table, "Used by CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19"). That check only matches the id. In CO-S01 the refund comes back `status: pending` (Initial state: "The order system will give refund id <refund_id>, with status pending"), so an agent that says "refund RF-5531 has been issued" breaks G-03 and still passes. The same holds for a claim of "cancelled" in CO-S12/CO-S13, where the cancellation was unanswered and only a lookup can show it. Only CO-S19 carries a status-truthfulness rubric ("Refund status reported"). The failure-path rubrics ("never says a refund is pending or issued") do not apply on the success path. The input asks for this outright: packet, Round 2 Q4 answer, case 3: "Final message must match the final refund status."
Pattern: a rule clause about what the agent tells the user is asserted on its failure paths but not on its success path. The success scenarios need a rubric dimension (or an extended one) that checks the reported cancellation and refund status match what the order system returned.
```

- R1-11 (round 1) | Ambiguous | Important | CO-S16 row 2 (and CO-S19, CO-S20 row 1, CO-S21 once F2 is fixed), Required events

```
## R1-11
F3 | Ambiguous | Important | CO-S16 row 2 (and CO-S19, CO-S20 row 1, CO-S21 once F2 is fixed), Required events
Quote: "- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482." (CO-S16 line 962, and the same line in CO-S19 line 1132, CO-S20 line 1189, CO-S21 line 1249)
Evidence: In CO-S16 row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (line 979). Suppose the agent makes one extra lookup after that timeout. It sees RF-5531 pending, reports it and stops. The world matches every Final state line (lines 965-967) and the message check is met, but the trial fails "CO-A3 occurs exactly twice". G-04 (line 27) is worded as a permission ("repeats it only when ..."). The failure row (line 102) says "Make CO-A3 once more" and gives no exception for a lookup that has already shown the result. The checklist (evaluation-checklist.md, "Outcome, not path") says exact call sequences are not Required. Here the second call changes nothing in row 2. Two experts could split on whether this agent passes.
The same split happens when the lookup shows a failed refund (CO-S20 row 1, CO-S21 row 2, if the first call created it). CO-06 (line 77) bars a second CO-A3 only after the order system "returned the refund with status failed". It does not say what happens when a lookup shows it failed. So both of these are defensible: an agent that skips the retry and hands off, and one that retries.
Pattern: A Required count on a retried commit call does not say whether the retry is still owed after a lookup between the calls has shown the first call's effect. A reasonable extra read then flips the verdict. Instances: CO-S16 row 2; CO-S19 rows 1-2, CO-S20 row 1 and CO-S21 rows 1-2 whenever the first call is the one that creates the refund.
```

- R2-01 (round 2) | Lies | Important | §5.2 rubric dimensions "Cancellation outcome unknown reported" (CO-S14, CO-S15) and "Refund status reported" (CO-S19)

```
## R2-01
F1 | Lies | Important | §5.2 rubric dimensions "Cancellation outcome unknown reported" (CO-S14, CO-S15) and "Refund status reported" (CO-S19)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: Neither the rules nor the inputs require the agent to say "no refund was issued" when the cancellation outcome is unknown.
- The rules don't require it. agent-spec.md line 103 (CO-A2 failure row "did not answer the first CO-A2", branch "If the lookup does not answer") requires only "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4". Line 104 ("did not answer the second CO-A2") requires the same, and CO-07 (line 80) adds only "store staff will follow up".
- The input doesn't require it. review-packet.md Round 3 Q4 says only "Re-read fails, say outcome unknown, issue no refund, hand off". "Issue no refund" constrains the agent's actions, not its message.
- So an agent that does exactly what the failure rows say fails CO-S14 and CO-S15 on this dimension. The extra clause also appears in both reference trajectories (CO-S14 step 8, CO-S15 step 9: "no refund was issued").
- Second instance: "| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status ... | CO-S19 |". The rule it grades (line 108, CO-A3 "did not answer the second CO-A3", branch "If the lookup shows the refund pending or issued") requires "tell the customer that status and the refund id". It does not require saying the order is cancelled, and neither does CO-08 (line 83).
Pattern: A rubric dimension, and the trajectory step it mirrors, requires the agent to say something that neither the failure row it grades nor the inputs require. An agent that follows the rule exactly is failed. Either cut each dimension down to what its failure row requires, or add the clause to the failure row, with an input that supports it.
```

- R3-08 (round 3) | Gap | Important | G-03; known failure case 3; CO-S16 rows 2-3; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S25

```
## R3-08
F3 | Gap | Important | G-03; known failure case 3; CO-S16 rows 2-3; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S25
Quote: "and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: Packet, Round 2 Q4, known failure case 3: "Cancel succeeded, refund call timed out ... Final message must match the final refund status." CO-S16 rows 2 and 3 are that case with the retry answering pending ("gets no answer from the order system, and creates refund RF-5531 with status pending" / "creates no refund", then the second CO-A3 returns RF-5531 pending). The only message dimension there is "Refund id reported", a substring match on RF-5531. Nothing checks that the agent said pending rather than issued. The same holds in every success scenario: CO-S01 (whose Illustrates line lists G-03), CO-S02, CO-S03, CO-S09, CO-S12, CO-S13 and CO-S25 each assert only "Refund id reported". The only dimension that checks the stated status, "Refund status reported", is used by CO-S19 alone. So an agent that says "refund RF-5531 has been issued" while the order system returned pending passes all of these, against G-03 and the customer's interest (§2: "wants to be told truthfully ... where the refund stands"). As written, "Refund status reported" takes its value from "the data-variant row's refund status", which these scenarios do not have (evaluation-checklist.md: "A shared dimension names a value source every scenario has").
Pattern: G-03's refund-status clause and case 3's "final message must match the final refund status" are asserted only in failure-path scenarios (CO-S17 to CO-S23) and in CO-S19. Success scenarios check the refund id but not the status the agent states.
```

