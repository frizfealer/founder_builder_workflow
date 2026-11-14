# Judge task: dropped_real for trial full-new-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/full-new-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/full-new-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-11 (round 1) | Lies | Important | CO-08; dimension "Refund id reported" (CO-S01, S02, S03, S09, S12, S13, S16, S19)

```
## R1-11 (Important)
Sources: B-faithfulness F3

R1-11 | Lies | Important | CO-08; dimension "Refund id reported" (CO-S01, S02, S03, S09, S12, S13, S16, S19)
Quote: "The order has status cancelled, exactly one refund exists for it ... and the agent tells the customer the refund id."
Evidence: No input requires the agent to tell the customer the refund id. The packet's only reporting requirement for the success and timeout paths is "Final message must match the final refund status" (line 54) and "pending or issued, report that status" (line 63). The refund id is not among the confirmed derivations either (lines 70-73). Because of this, an agent that reports "order cancelled, your $86.40 refund to Visa ending 4242 is pending" without the id fails eight scenarios, although the inputs call that behavior correct.
Pattern: A success guarantee adds a reporting requirement the inputs do not state, and a pass condition across many scenarios is built on it.
```

- R1-17 (round 1) | Ambiguous | Important | CO-S01–CO-S21, CO-S23–CO-S24, Initial state / Final state assertions

```
## R1-17 (Important)
Sources: A-verdicts-codex F1

R1-17 | Ambiguous | Important | CO-S01–CO-S21, CO-S23–CO-S24, Initial state / Final state assertions
Quote: "- No follow-up task exists."
Evidence: Each affected scenario makes an exact final assertion about the number of follow-up tasks, at these lines of agent-spec.md: CO-S01:141, CO-S02:201, CO-S03:263, CO-S04:320, CO-S05:372, CO-S06:422, CO-S07:471, CO-S08:521, CO-S09:576, CO-S10:630, CO-S11:680, CO-S12:735, CO-S13:792, CO-S14:850, CO-S15:908, CO-S16:967, CO-S17:1025, CO-S18:1081, CO-S19:1137, CO-S20:1195, CO-S21:1255, CO-S23:1375 and CO-S24:1429. Only CO-S22 constrains the pre-existing task population; CO-S23 merely says its two calls create none. The evaluation checklist (evaluation-checklist.md, lines 34-42) requires every fact needed by a grader to have a value in Initial state.
Pattern: An exact final-state cardinality is asserted for an entity whose starting population is unspecified, so the verdict depends on whether the test author assumes an unstated empty set.
```

- R1-18 (round 1) | Untestable | Important | CO-S03 and CO-S04, User block

```
## R1-18 (Important)
Sources: A-verdicts-codex F2, B-verdicts-codex F1 (late, duplicate)

R1-18 | Untestable | Important | CO-S03 and CO-S04, User block
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: The line occurs at agent-spec.md:248 and :308. Section 5.1 defines and labels a "confirmation question" at agent-spec.md:1459-1461, but does not define or label a question that merely "proposes cancelling … and asks to go ahead." The scenario checklist (evaluation-checklist.md, lines 34-42) expressly requires a scripted User turn to be triggered by a §5.1-defined event and says never to use "a proposal".
Pattern: A scripted user turn is anchored to an undefined semantic description rather than a harness-recognizable event; it must be reworded to a defined event before it can become one deterministic step.
```

- R2-04 (round 2) | Gap | Important | failure: CO-A3 | the order system reported the order not cancelled (new)

```
## R2-04 (Important)
Sources: coverage F4

R2-04 | Gap | Important | failure: CO-A3 | the order system reported the order not cancelled (new)
Quote: "absent"
Evidence: This row has three outcomes. Two have scenarios: the lookup shows cancelled (CO-S17 row 3, unambiguity note at line 523) and the lookup does not answer (CO-S27, Initial state line 339). No scenario's Initial state makes the lookup after OrderNotCancelled answer with a status other than cancelled. That branch changes the outcome (CO-A4 with a different reason, a different message, and possibly a further CO-A2), so a scenario should trigger it.
Pattern: Each branch of a failure row that leads to a different action or message needs a scenario whose Initial state triggers that branch.
Changed-line tag: quotes a line round 1 added.
```

- R2-09 (round 2) | Untestable | Important | Refund status reported

```
## R2-09 (Important)
Sources: verdicts-codex F3

R2-09 | Untestable | Important | Refund status reported
Quote: "| Refund status reported | rubric | The agent tells the customer the refund's status is the status the scenario's Final state assertions give the refund, and states no other status for it. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 |"
Evidence: The review criterion classifies a rubric dimension as untestable when a verbatim-value message check would suffice. Here the expected value is the literal refund-status enum in the confirmed model (pending, issued, or failed), so this can be a deterministic message check. Instances: CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19.
Pattern: A rubric grader is used to judge reporting of a literal enum value that can be checked directly in the message window.
Changed-line tag: quotes a line round 1 changed.
```

