# Judge task: dropped_real for trial it4-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-03 (round 1) | Ambiguous | Important | G-04 vs CO-06 / CO-A2 failure rows / SG-04

```
## R1-03 | Ambiguous | Important | sources: verdicts:F2, faithfulness:F6

[verdicts F2]
F2 | Ambiguous | Important | G-04 vs CO-06 / CO-A2 failure rows / SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (Appendix B) says the order system makes cancellation idempotent: repeating a cancellation "returns it cancelled and changes nothing". G-04's second clause therefore allows a blind second CO-A2 after a timeout. CO-06 ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing"), the CO-A2 no-answer failure row, CO-S12 (Forbidden "A second CO-A2") and CO-S13 (Forbidden "A second CO-A2 before a CO-A1 made after the first CO-A2") all forbid it. The input agrees with CO-06: review-packet round 3 Q4, "If the cancel call times out: no blind resend; re-read the order." Under G-04 a blind cancel retry is allowed; under CO-06 it is forbidden. An agent built to G-04 fails CO-S12 and CO-S13.
Pattern: A global rule's general exception (any idempotency guarantee) is wider than the capability rule. This spec cites four idempotency guarantees, so G-04 must either name the actions its exception covers or exclude CO-A2.

[faithfulness F6]
F6 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 (line 1544) gives exactly such a guarantee for cancellation: "cancelling an order that is already cancelled returns it cancelled and changes nothing". So G-04 as worded permits a blind resend of CO-A2 after a timeout. The input forbids that: round 3 Q4, "If the cancel call times out: no blind resend; re-read the order." The user's later change, making cancel_order idempotent, did not withdraw that rule. CO-06 and the Forbidden lines in CO-S12 and S13 still forbid the blind resend, so no verdict changes.
Pattern: A global permission is written as a general condition, and a supporting-actor guarantee added later makes it license behavior the input forbids. Name the guarantees it covers (SG-01, SG-03) instead.

Checked with no defect found: tool names and parameters against the confirmed tool set; dates (2026-11-05 is a Thursday, and "placed yesterday" resolves to HG-10511); every Reference trajectory against its Data variants row 1; Required events and Final state for every other row; the refund and task idempotency effects in CO-S16, S19, S21 and S22.
```

- R1-14 (round 1) | Ambiguous | Important | CO-S16 row 2 (and CO-S19, CO-S20, CO-S21 once F3 is settled with the refund created by the first call), Required events

```
## R1-14 | Ambiguous | Important | sources: verdicts:F4

[verdicts F4]
F4 | Ambiguous | Important | CO-S16 row 2 (and CO-S19, CO-S20, CO-S21 once F3 is settled with the refund created by the first call), Required events
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: CO-S16 row 2 says the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". An agent that looks up after the unanswered call sees RF-5531 pending. Reporting it without a second refund call satisfies G-03 ("or a lookup shows it"), CO-08 and every Final state line, and CO-06 is only permissive ("It makes a second CO-A3 only after ..."). It still fails the Required line. Only the failure row "Make CO-A3 once more, relying on SG-01" makes the retry mandatory, and the evaluation checklist says "Outcome, not path ... a path assertion punishes them". One reviewer reads the failure row as binding; another reads CO-06, G-03 and the checklist as allowing the lookup path. They reach different verdicts on the same run.
Pattern: An exact count on a retry the agent may correctly skip once a read shows the first call took effect. Either state that the retry is required whatever a lookup shows, or assert the outcome (one refund, reported) and bound the count with "at most two".
```

- R2-07 (round 2) | Ambiguous | Important | CO-S11, Initial state

```
## R2-07 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: Row 2 makes that CO-A2 time out: "gets no answer from the order system and cancels nothing" (l.700). Nothing defines whether a timed-out call "reaches the order system". §5.1 anchors occurrence to issuing the call ("An action occurs when the agent issues that action's commit call", l.1606). The evaluation checklist says a mid-trial change must be "anchored to a state-changing call", meaning the agent's nth call, not its arrival. If a harness treats a timed-out call as not having reached the order system, the status stays processing and the lookup after the timeout shows processing. The failure row (l.103) then requires "make CO-A2 once more", and that trips Forbidden "A second CO-A2" (l.691). A correct agent fails row 2.
Pattern: A mid-trial state change tied to a supporting actor receiving a call, where the call itself may time out. Tie it to the agent issuing its nth call.
```

- R2-11 (round 2) | Gap | Nit | CO-S01 row 4 (R1-10 fix incomplete)

```
## R2-11 | Gap | Nit | sources: verdicts:F10

[verdicts F10]
F10 | Gap | Nit | CO-S01 row 4 (R1-10 fix incomplete)
Quote: "| 4 | I'd like to cancel my order, please. | HG-10547 | processing | $64.00 | Visa ending 6021 | RF-5535 |"
Evidence: The Unambiguity note says "the agent has nothing to ask" (l.174). But no User-knows deflection and no dimension scores an unneeded "which order?" question, and §5.2 says precision is "never folded into the score" (l.1620). An agent that always asks which order gets deflected, then proposes HG-10547 and passes. Row 4 catches only an agent that refuses to propose. The evaluation checklist asks for "a deflection for questions the agent should not ask when the scenario tests over-asking" and warns "test only 'asks when unsure' and you get an agent that always asks."
Pattern: The holding-back side of an "act only when" clarification rule catches the refusal to act but not the unneeded question.
```

- R3-01 (round 3) | Lies | Important | G-04, Global Contract (and the CO-A4 failure row, CO-S22)

```
## R3-01 | Lies | Important | sources: faithfulness:F1

[faithfulness F1]
F1 | Lies | Important | G-04, Global Contract (and the CO-A4 failure row, CO-S22)
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: The input requires a blind retry of the handoff. Review packet, tool confirmation turn, change 3: "request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once." G-04's exception names only SG-01, and the round-1 decision (decisions-round1.json R1-03: "G-04's exception cites only SG-01") reads that list as closed, so G-04 does not cover SG-03. Its first clause cannot apply to CO-A4 either: `list_orders()` returns orders and refunds but no follow-up tasks (Appendix A, CO-A1 row, line 1775), so no lookup can show that a handoff took no effect. Read this way, G-04 forbids the second CO-A4 that the failure row "CO-A4 | the order system did not answer the first CO-A4 | Make CO-A4 once more with the same reason, relying on SG-03 | CO-06, CO-07, G-04" (line 109) requires, and that CO-S22 requires ("CO-A4 occurs exactly twice", line 1323; Illustrates G-04, line 1353). An agent built to G-04 fails CO-S22, and in production it drops the handoff retry the user asked for.
Pattern: A global rule's list of exceptions names fewer supporting-actor guarantees than the failure rows and scenarios rely on. Here the blind retry rests on SG-03 but G-04 cites only SG-01.
```

- R3-07 (round 3) | Ambiguous | Important | CO-S01, Data variants row 3; Appendix A Value comparison / CO-A2 row

```
## R3-07 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | CO-S01, Data variants row 3; Appendix A Value comparison / CO-A2 row
Quote: "| 3 | cancel my order hg-10530 | HG-10530 | placed | $53.50 | Amex ending 1007 | RF-5533 |"
Evidence: In row 3 the customer types the order number in lowercase. Appendix A (agent-spec.md l.1769) says "Order numbers and refund ids compare case-insensitively". That clause covers grading comparisons. Nothing in the spec says what the order system does when `cancel_order("hg-10530")` or `issue_refund("hg-10530")` arrives. The CO-A2 row (l.1776) lists the outcomes cancelled, `OrderNotCancellable`, `OrderNotFound` and timeout, and §5.1 (l.1718) says only that a supporting actor "answers every call normally". Take an agent that passes the lowercase string through. Under the case-insensitive reading, the Required line "CO-A2 occurs exactly once, for <order>" passes it. Whether the Final state "<order> has status cancelled" and the refund line pass depends on whether the harness's order system treats "hg-10530" as HG-10530 or returns `OrderNotFound`. Two harness builders following the spec could reach opposite verdicts on the same run. The row is tagged canonicalization, which suggests the agent must normalize. The Value comparison clause suggests it need not.
Pattern: A data-variant row that tests canonicalization of a value passed as a tool argument, where the spec defines how graders compare the value but not how the supporting actor treats the non-canonical form.
```

