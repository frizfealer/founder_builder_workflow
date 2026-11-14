# Judge task: dropped_real for trial it4-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. Do NOT open the round*-findings.md files: they carry the verifier's refutation, and you are judging the finding against the spec and the inputs, not the refutation. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-15 (round 1) | Untestable | Nit | CO-S19, Forbidden

```
## R1-15 | Untestable | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: This is not a forbidden event. It is a required read-only call phrased as a Forbidden line, so it gets past the script's check for read-only actions in Required events. The evaluation checklist says "Forbidden lines name events. Each Forbidden line is a tool call pattern ... or a timing violation" and "A tool call that only reads is never Required". The behavior is already enforced elsewhere: message check "Refund id reported" cannot pass without that lookup, because its window opens at "the read that showed it" (line 1467). CO-S20 and CO-S21 use the proper timing form "CO-A4 before a CO-A1 made after the second CO-A3" (lines 1199, 1259).
Pattern: A required read must not be phrased as a Forbidden "fewer than one" line. Use a timing violation on a write, or rely on the message check that needs the read.
```

- R1-17 (round 1) | Ambiguous | Nit | CO-S03, CO-S04, User block

```
## R1-17 | Ambiguous | Nit | sources: verdicts:F9

[verdicts F9]
F9 | Ambiguous | Nit | CO-S03, CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: The checklist says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'". "A question that proposes cancelling HG-10482" is not a §5.1 event. It leaves open whether a partial question such as "Do you want me to cancel HG-10482?", with no amount or payment method, makes Turn 2 due. In CO-S03 a full HG-10482 proposal is a wrong-value question under §5.1 (line 1461), so "confirmation question" could not be used directly. Both readings appear to lead to the same verdict.
Pattern: A User turn's trigger must be an event §5.1 defines, or one the scenario defines exactly.
```

- R3-06 (round 3) | Ambiguous | Important | CO-S16 row 2, Required events

```
## R3-06 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | CO-S16 row 2, Required events
Quote: "| 2 | gets no answer from the order system, and creates refund RF-5531 with status pending |" together with "- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first, unanswered CO-A3 creates RF-5531 (line 990). Lookups are unlimited (CO-06, line 77; Appendix A, line 1716).
Valid variation: after the timeout, the agent calls list_orders and sees RF-5531 pending. It tells the customer the order is cancelled and refund RF-5531 is pending, and stops. This run is allowed by every rule:
- G-03 (line 24) allows reporting pending "when ... a lookup shows it".
- G-04 (line 27) and CO-06 (line 77) allow a second CO-A3 but do not require one.
- The success guarantee CO-08 (line 83) holds in full.
- The message check "Refund id reported" passes, because its window opens at "the read that showed it" (line 1659).
Only failure row 106 ("Make CO-A3 once more, relying on SG-01.") requires the retry. The Required line "exactly twice" fails this run.
The evaluation checklist ("Outcome, not path ... agents find valid paths the author did not anticipate, and a path assertion punishes them") says a correct agent should pass. One expert reads row 106 as binding and fails the run; another reads the outcome rules and passes it. R1-12 removed the same in-between-read problem from CO-S19, S20 and S21, where the first CO-A3 now creates nothing. CO-S16 row 2 still has it.
Pattern: when an unanswered commit call takes effect and a read before the retry can show that effect, either let the scenario accept the agent stopping on that read (for example, CO-A3 once or twice) or make the effect land on the second call. Instance: CO-S16 row 2. CO-S12 and CO-S22 row 2 are not affected: in CO-S12 the row requires the lookup, and in CO-S22 no read shows follow-up tasks.
```

- R3-07 (round 3) | Ambiguous | Nit | G-04

```
## R3-07 | Ambiguous | Nit | sources: verdicts:F4

[verdicts F4]
F4 | Ambiguous | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Read either way, G-04 contradicts another rule:
- Broad reading: "a guarantee that repeating creates nothing new" also covers SG-04 (line 1741: "cancelling an order that is already cancelled returns it cancelled and changes nothing"). G-04 then allows a blind second cancel_order. CO-06 (line 77) and failure row 104 (line 104) forbid that, and so does the input: round 3 Q4, "If the cancel call times out: no blind resend; re-read the order" (review-packet.md, Round 3).
- Narrow reading: the guarantee is SG-01 only, as the parenthetical names. Then the blind second CO-A4 that row 110 requires ("relying on SG-03", citing G-04) and CO-S22 requires ("CO-A4 occurs exactly twice", line 1325) breaks G-04. No lookup can show a follow-up task, because list_orders returns no tasks (Appendix A, line 1720).
The Forbidden lines in CO-S12, CO-S13 and CO-S25 ("A second CO-A2 before a CO-A1 made after the first CO-A2") settle the scenario verdicts. In production, though, an agent reading G-04 could resend a timed-out cancellation blindly.
Pattern: a global rule's exception must name exactly the guarantees it covers (here SG-01 and SG-03, not SG-04), so it agrees with the per-action retry rules.
```

