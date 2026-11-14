# Judge task: dropped_real for trial it1-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M2 (round 1) | Lies | Important | G-04

```
## M2
F2 | Lies | Important | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 says "cancelling an order that is already cancelled returns it cancelled and changes nothing". Appendix A CO-A2 says the same: "also for an order that was already cancelled (SG-04)". So G-04's second clause lets the agent resend a timed-out cancel_order without a lookup. The packet, Round 3 Q4 (accepted with "Yes to all"), says: "If the cancel call times out: no blind resend; re-read the order." CO-06 and CO-S13's Forbidden line "A second CO-A2 before a CO-A1 made after the first CO-A2" carry the user's rule. The global rule says the opposite. The same clause also lets the agent resend CO-A4 without a lookup (SG-03), which matches the input there. Only the cancel case contradicts it.
Pattern: A global rule's permission must not cover an action that the inputs explicitly bar from blind retry. Scope the guarantee clause to the actions the user allowed to be retried (issue_refund, request_staff_followup), or exclude CO-A2.
```

- N4 (round 2) | Ambiguous | Important | CO-S16, Required events (row 2)

```
## N4
F1 | Ambiguous | Important | CO-S16, Required events (row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (CO-S16 Data variants row 2). Take an agent that, after that timeout, makes a CO-A1 (lookups are unlimited, CO-06 and Appendix A). The lookup shows RF-5531 pending. The agent then tells the customer the order is cancelled and RF-5531 is pending. G-03 allows that report ("or a lookup shows it"). CO-06 only allows a second call: "It makes a second CO-A3 only after the first … went unanswered". The world ends in exactly the Final state assertions. This run makes one CO-A3, so it fails "exactly twice". The CO-A3 failure row ("did not answer it | Make CO-A3 once more") says to retry, while G-03 and CO-06 accept the lookup-and-report path. Two experts could give this trajectory opposite verdicts. evaluation-checklist.md, "Outcome, not path": "agents find valid paths the author did not anticipate, and a path assertion punishes them."
Pattern: An exact retry count is Required in a row where a read-only lookup after the unanswered call already shows the call took effect, so a valid lookup-then-report path fails. Either require the retry only in rows where nothing is created (rows 1 and 3), or say outright that the retry is required even when a lookup shows the refund.
```

- N7 (round 2) | Ambiguous | Important | CO-07; CO-S23 dimension "Staff contact unconfirmed reported"

```
## N7
F4 | Ambiguous | Important | CO-07; CO-S23 dimension "Staff contact unconfirmed reported"
Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
Evidence: "once the order system has created the task" can be read two ways: as when staff follow up, or as a limit on when the agent may say so. No dimension used in CO-S14, S15, S17, S18, S20 or S22 checks that the statement comes after a returned task_id, so an early announcement passes there. In CO-S23 the dimension says "never says … that staff will follow up", and §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call". An agent that writes "I'm asking store staff to follow up on your refund" next to its first CO-A4 call, and then correctly reports that it could not confirm staff were told, may pass or fail depending on how the judge reads that earlier text.
Pattern: The timing of a required statement relative to a commit call's result is stated only in an ambiguous clause and checked only in one scenario. Rewrite CO-07 so it says plainly that the agent says staff will follow up only after CO-A4 returns a task. Then add that ordering to every dimension that grades the handoff message, or say that text sent before the call's result does not count.
```

- N11 (round 2) | Gap | Important | G-01 / §4.1 Contract (customer asks for a second order)

```
## N11
F4 | Gap | Important | G-01 / §4.1 Contract (customer asks for a second order)
Quote: absent
Evidence: G-01: "The agent cancels, refunds and hands off at most the one order the current request is about." The Purpose says: "It may cancel that one order, issue its one refund and create one follow-up task for it." CO-06 counts calls "in a conversation" ("at most two CO-A2 ... in a conversation"), which reads as one order per conversation. The packet says Q1 "Which orders can the agent cancel?" was answered by status only, and CO-S02 shows a customer can have two open orders (HG-10482, HG-10511). No rule, failure row or scenario says what the agent does or tells the customer when they ask to cancel both orders, or ask for a second order after the first is cancelled. The use-case checklist brainstorm ("the user ... changes the request mid-way"; "more than one plausible match") and the Specification-by-Example check ("'What if' questions become examples ... Record it as an open question") both point at this case. Under the spec, an agent can either cancel the second order (does G-01 forbid that?) or silently do nothing, and no scenario tells these apart.
Pattern: A limiting rule (one order per request or per conversation) with no rule or failure row saying how the agent declines the request it limits, and no holding-back scenario for it.
```

- P7 (round 3) | Gap | Important | CO-A2 timeout rows, second-CO-A3 timeout row; CO-S14, CO-S15, CO-S21

```
## P7
F1 | Gap | Important | CO-A2 timeout rows, second-CO-A3 timeout row; CO-S14, CO-S15, CO-S21
Quote: "If the agent stops looking up before any lookup made after the CO-A2 answers, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: These rows let the agent hand off only after it stops looking up. Before that, they require it to keep looking up: "Make no CO-A2 or CO-A3 until a lookup made after it answers" (agent-spec.md:100, also :101 and :106). The packet says reads are retried without limit: "Reads may be retried on timeout without limit; only commit calls are bounded" (review-packet.md:85). Every scenario that tests the hand-off-after-unanswered-lookup branch makes every later lookup go unanswered: CO-S14 "does not answer any CO-A1 the agent makes after its first CO-A2" (:843), CO-S15 (:901) and CO-S21 (:1247). No scenario has a lookup after an action go unanswered and then answer on a retry. An agent that hands off after one unanswered lookup, with no retry, therefore passes CO-S14, CO-S15 and CO-S21, and no scenario fails it. The round-1 fix M11 (answered.md:14) added that holding-back case only for the lookup before any CO-A2 (CO-S01 row 5). It did not add it for the lookups after CO-A2 or after the second CO-A3, so that fix is incomplete.
Pattern: An "act only when the agent stops looking up" branch is tested only on its acting side. Each such branch (after the first CO-A2, after the second CO-A2, after the second CO-A3) needs a holding-back row: the first lookup after the action times out, a later one answers, and the agent continues from that answer with no CO-A4 for cancellation unknown or refund status unknown.
```

- P9 (round 3) | Gap | Important | Cancel Order, Preconditions and Trigger

```
## P9
F3 | Gap | Important | Cancel Order, Preconditions and Trigger
Quote: "The customer asks to cancel an order or to get their money back for an order."
Evidence: Every scenario's opening turn asks to cancel. Examples: CO-S01 rows 1–5 (:157–161), CO-S05 row 2 "Cancel HG-10466 and refund me, please." (:390), and CO-S09 rows 1–4 (:592–595). No scenario starts with a money-back request alone for an open order, such as "I'd like a refund for HG-10482." That form carries the specific risk CO-05 guards against: the agent calls CO-A3 before any CO-A2 ("CO-A3 occurs only for an order the order system returned as cancelled", :73), or it refuses because no cancellation was asked for. Neither failure is tested. The product idea makes the money-back goal central: "cancel an order they placed and get their money back" (product-idea.md:5–6).
Pattern: A trigger branch with no scenario. Each trigger form the spec lists needs at least one scenario whose opening turn uses it. Here that means a refund-only request for an open order, where the required events are one CO-A2 and then one CO-A3, and a CO-A3 before CO-A2 is forbidden.
```

