# Judge task: dropped_real for trial it3-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it3-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it3-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-05 (round 1) | Lies | Nit | G-04 (FA-F5)

```
R1-05 | Lies | Nit | G-04 (FA-F5)
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 guarantees a repeated cancellation changes nothing, so the general clause would permit a blind CO-A2 retry. review-packet.md Round 3 Q4: "If the cancel call times out: no blind resend; re-read the order." CO-06 and CO-S13 Forbidden enforce the input, so no verdict changes.
Pattern: a global rule's general exception covers a case the user explicitly excluded.
```

- R1-14 (round 1) | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11) (VE-F4)

```
R1-14 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11) (VE-F4)
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process"
Evidence: In CO-S05 the agent never tries to cancel; CO-01, the shipped/delivered failure row, the reference trajectory and the Unambiguity note all require "has shipped and cannot be cancelled". The shared definition requires "was not cancelled", which fits CO-S11's attempted cancellation. evaluation-checklist.md: "A shared rubric dimension has one definition."
Pattern: a shared dimension's definition fits one scenario's failure row but not the other's.
```

- R1-18 (round 1) | Ambiguous | Nit | CO-S11 Initial state (VE-F8)

```
R1-18 | Ambiguous | Nit | CO-S11 Initial state (VE-F8)
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: In row 2 the first CO-A2 "gets no answer from the order system and cancels nothing"; nothing says whether a timed-out call "reaches" the order system. If not, the lookup shows processing and the agent may legitimately send a second CO-A2 (CO-06), which hits Forbidden "A second CO-A2". evaluation-checklist.md: a mid-trial change is anchored to the agent's nth state-changing call.
Pattern: a mid-trial world change anchored on a condition undefined for a timed-out call.
```

- R2-01 (round 2) | Ambiguous | Important | CO-S16 Data variants row 2 and Required events (FA-F1, VE-F1)

```
R2-01 | Ambiguous | Important | CO-S16 Data variants row 2 and Required events (FA-F1, VE-F1)
Quote: "| 2 | gets no answer from the order system, and creates refund RF-5531 with status pending |" (with Required "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482.")
Evidence: In row 2 the first, unanswered CO-A3 creates the refund. Appendix A: "The agent may repeat CO-A1 without limit", and `list_orders` returns each order's `refund`, so a lookup between the two refund calls shows RF-5531 pending. G-03 ("or a lookup shows it") then lets the agent report it pending, and CO-06 only permits a second CO-A3 ("It makes a second CO-A3 only after..."); the Unambiguity note says "One retry is allowed". An agent that looks up, sees the pending refund and reports it meets CO-08 but fails "CO-A3 occurs exactly twice". Only the failure row "Make CO-A3 once more" makes the retry mandatory. Same defect as R1-12, whose fix (answered.md) covered CO-S19, CO-S20, CO-S21 but not CO-S16 row 2.
Pattern: a Required line counts a retry as mandatory while the effect that makes the retry pointless is tied to an earlier call an allowed lookup can see.
```

- R2-03 (round 2) | Lies | Nit | CO-S05 Unambiguity note (FA-F3)

```
R2-03 | Lies | Nit | CO-S05 Unambiguity note (FA-F3)
Quote: "The order is past the cutoff in every row, and in row 4, which names no order, it is the only order on the account, ..."
Evidence: review-packet.md Round 2 Q1 user answer: "Cancellable while placed or processing, no time limit. Once shipped, the agent refuses". CO-01 states the condition by status only. "Past the cutoff" implies a time limit the inputs rule out. No verdict depends on it.
Pattern: an explanatory note states a domain fact the inputs do not support.
```

- R2-05 (round 2) | Gap | Important | Failure row "the order system did not answer the second CO-A2" (still-open branch); CO-S25; CO-07 (CV-F2)

```
R2-05 | Gap | Important | Failure row "the order system did not answer the second CO-A2" (still-open branch); CO-S25; CO-07 (CV-F2)
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4."
Evidence: Appendix B SG-04 Covers: "A second cancellation call that reaches the order system after a first, unanswered one took effect late." Appendix A CO-A2: "A timeout changes the order or not as Initial state says", with no timing bound. After the second, final unanswered CO-A2 a lookup showing the order still open does not show the cancellation will not land; if it lands later, the order is cancelled with no refund and no follow-up task and the customer was told "the order was not cancelled". §2: the support team "wants every order whose refund is unfinished or whose cancellation is uncertain handed to it"; G-03 "when it cannot tell, that the outcome is unknown". CO-S25 Forbids CO-A4 and its dimension "Cancellation not made reported" fails an agent that says the outcome is unknown or that staff will follow up. The branch was added in R1-02 as a derivation (answered.md); Round 3 Q4 defines re-read branches only for the first cancel timeout.
Pattern: a branch treats a lookup after an unanswered final commit call as settling the outcome although the spec admits the call landing late.
```

- R2-10 (round 2) | Ambiguous | Nit | CO-03 failure row (partial items); CO-S08 Reference trajectory and User knows; dimension "Orders unavailable reported" (CO-S10) (VE-F5)

```
R2-10 | Ambiguous | Nit | CO-03 failure row (partial items); CO-S08 Reference trajectory and User knows; dimension "Orders unavailable reported" (CO-S10) (VE-F5)
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence: The failure row forbids proposing until the customer asks, but CO-S08 Reference step 3 has the agent ask "whether they want to cancel the whole order" and User knows scripts "Would you like to cancel the whole order HG-10530 instead?". The spec does not settle whether offering whole-order cancellation is a proposal; the same undefined term is graded in CO-S10's dimension "proposes no cancellation", and CO-01 and CO-02 use "proposes nothing" without a definition.
Pattern: "propose"/"proposal" used as a graded boundary without a definition, and a Reference trajectory crosses the boundary a failure row draws.
```

