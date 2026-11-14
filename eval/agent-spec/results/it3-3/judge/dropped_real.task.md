# Judge task: dropped_real for trial it3-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it3-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it3-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-12 (round 1) | Ambiguous | Nit | CO-S11 Initial state

```
R1-12 | Ambiguous | Nit | CO-S11 Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: Row 2's first CO-A2 "gets no answer from the order system and cancels nothing". Whether a timed-out call "reached" the order system is not stated. If the status does not flip, the later lookup shows processing, and a correct agent sends a second CO-A2 under the failure row (line 100), which hits Forbidden "A second CO-A2". Only the Unambiguity note ("in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation") settles the intent. The evaluation checklist asks that a mid-trial change be tied to "the agent's nth state-changing call", not to a network event.
Pattern: a mid-trial world change anchored on whether a call arrived, rather than on the call being issued.
(Source: verdicts finder)
```

- R2-06 (round 2) | Gap | Important | Failure row "the order system did not answer the second CO-A2", branch "placed or processing"; CO-S25 row 2

```
R2-06 | Gap | Important | Failure row "the order system did not answer the second CO-A2", branch "placed or processing"; CO-S25 row 2
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4."
Evidence: §2 (line 10) says store staff "receive a follow-up task for each order the agent could not finish". The primary actor (line 9) "wants the order they mean cancelled". In CO-S25 row 2 the order is still processing after two unanswered cancellations. The agent could not finish it, yet CO-S25 forbids "CO-A4 at any point" (line 1522). No rule tells the customer what to do next, such as trying later or contacting support. CO-07 (line 80) covers only an unfinished refund or an uncertain cancellation. No input decides this branch: packet round 3 Q4 stops at "send the cancel once more", and the user listed no handoff reason for it ("refund_not_issued, refund_status_unknown, cancellation_unknown"). The branch came from the R1-02 fix and has no input support. A correct agent that hands off here, as §2 suggests, fails CO-S25 row 2.
Pattern: a branch the inputs leave undecided, settled in the spec without the user. Record it as an open question for the user, and make §2's interest list, CO-07 and the scenario agree.
(Source: coverage finder)
```

