# Judge task: dropped_real for trial e4-base-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. Do NOT open the round*-findings.md files: they carry the verifier's refutation, and you are judging the finding against the spec and the inputs, not the refutation. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/e4-base-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/e4-base-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-02 (round 1) | Ambiguous | Important | CO-S17 row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-06

```
## R1-02 | Ambiguous | Important | DROPPED | dropped

- Verifier: Not real | Important
- Decision: Dropped. Refutation quoted: line 103 "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up." and line 99 "Tell the customer the order could not be found and was not cancelled". I read both: the failure rows fix the report and the handoff reason for each contradictory answer, G-03 allows 'cancelled' because CO-A2 returned it, and the dimensions match the rows word for word, so two experts reach the same verdict; the OrderNotCancelled outcome was added by the user (tool confirmation change 2).

Reported by the faithfulness finder as F1:

```
F1 | Lies | Important | CO-S17 row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-06
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" together with the failure row's "make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: In CO-S17 the CO-A2 returns cancelled (Reference trajectory step 5, "Agent → CO-A2 (HG-10482) → cancelled") and Final state asserts "HG-10482 has status cancelled". Appendix A defines the outcome as "the order is not cancelled: `OrderNotCancelled`". So in row 3 the order system says the order is not cancelled about an order that is cancelled. No tool behaviour in the inputs produces that world (packet, tool confirmation turn change 2: "issue_refund adds outcome OrderNotCancelled"). CO-05 already stops any CO-A3 unless the order was returned cancelled or a lookup shows it cancelled, so this outcome only reaches the agent when two order-system answers contradict each other. The failure row then has the agent tell the customer "the order is cancelled" when the latest result says it is not. It also files reason refund_not_issued, although the packet's handoff reasons include `cancellation_unknown` for exactly this doubt (round 3 Q4, tool confirmation turn), and G-03 says "when it cannot tell, that the outcome is unknown". Two domain experts could reach different verdicts on whether the right handoff reason is refund not issued or cancellation unknown. They could also differ on whether the "Refund not issued reported" rubric (which requires saying "the order is cancelled") is a correct requirement.
Pattern: A data variant or failure row that has a supporting actor return an outcome its own tool definition contradicts, given the scenario's state. The spec then requires a report or handoff reason that rests on one of the two conflicting answers.
```

Reported by the verdicts finder as F3:

```
F3 | Ambiguous | Important | CO-S17 row 3, CO-S24; dimensions "Refund not issued reported" and "Order not cancelled reported"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
Evidence: In CO-S17 row 3, CO-A2 has already returned cancelled and the Final state is "HG-10482 has status cancelled", yet CO-A3 returns OrderNotCancelled. The rubric still requires the agent to tell the customer "the order is cancelled". G-03 says cancelled may be reported only when "the order system returned it cancelled or a lookup shows it", and here the system's latest answer says the opposite. An agent that truthfully reports "the system now says the order is not cancelled" fails the rubric.
In CO-S24, the agent's CO-A1 showed the order on the account, and a lookup after the rejection (a valid variation) shows it still placed or processing. The dimension still requires "the order could not be found and was not cancelled". An agent that reports "the cancellation did not go through; your order is still processing" is truthful under G-03 but may fail. Whether the agent should report the tool's error or the state its lookups show is left to the judge.
Pattern: When a scenario's supporting-actor answer contradicts the world state a lookup shows, the rule and the dimension must say which source the agent reports. Otherwise the world must not contradict itself.
```
```

- R1-04 (round 1) | Gap | Important | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15

```
## R1-04 | Gap | Important | DROPPED | dropped

- Verifier: Not real | Important
- Decision: Dropped. Refutation quoted: line 101 "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown." I read it: the row prescribes one behaviour for every lookup result and CO-S15 asserts it; the inputs give a lookup branch only for the first cancel timeout (round 3 Q4), so no branch the inputs require is missing. The verifier's residual (an agent that saw 'cancelled' in a voluntary lookup) goes to the report as an open question.

Reported by the coverage finder as F3:

```
F3 | Gap | Important | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence:
- The packet says reads "may be retried on timeout without limit" (tool confirmation turn, change 4), and Appendix A says "The agent may repeat CO-A1 without limit."
- Round 3 Q4 sets the pattern for an unanswered cancel: "re-read the order. Cancelled, continue to refund … Shipped, report it."
- The first-CO-A2 row branches on that lookup (line 100). The second-CO-A2 row has no lookup branch, so it says nothing about a lookup that shows the order cancelled, shipped or still open. As written, it still requires "no CO-A3" and "not known whether the order was cancelled".
- That contradicts G-03 (line 24): the agent says the outcome is unknown only "when it cannot tell".
- SG-04 (line 1544) itself expects a late-landing cancellation.
- The use-case checklist (cockburn-checklist.md, Failure handling) says: "A failure row that branches on a lookup covers every result of the lookup … A missing branch is the else-branch a coder will invent."
- CO-S15's Initial state (line 892: "does not answer any CO-A1 the agent makes after its second CO-A2") makes this case unreachable in tests.
In production, the order is cancelled, no refund is issued, the customer is told the outcome is unknown, and staff get the wrong reason.
Pattern: A row for an unknown result that ends the capability without a lookup branch, while a sibling row for the same unknown result does branch on one.
```
```

- R1-07 (round 1) | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)

```
## R1-07 | Ambiguous | Important | DROPPED | dropped

- Verifier: Not real | Important
- Decision: Dropped. Refutation quoted: G-03 "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." I read it: in CO-S14 and CO-S15 the agent made no CO-A3, so G-03 requires telling the customer no refund was issued; the dimension asks for what G-03 requires and the reference trajectories agree.

Reported by the verdicts finder as F2:

```
F2 | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows this dimension grades require only "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown" (CO-A2 first unanswered, lookup unanswered, line 100) and "tell the customer it is not known whether the order was cancelled and store staff will follow up" (CO-A2 second unanswered, line 101). Neither row, nor CO-07, requires the agent to say no refund was issued. The source, round 3 Q4, says "issue no refund", which is an action, not something to tell the customer. An agent that follows the failure row word for word fails the rubric. One expert grading against the rule passes it, another grading against the dimension fails it.
Pattern: A rubric dimension must require exactly the statements its failure rows require. Either add the clause to the rows and to CO-07, or drop it from the dimension.
```
```

- R2-02 (round 2) | Lies | Important | CO failure handling, row "CO-A3 | ... or reported the order not cancelled"; CO-S17 row 3; §5.2 "Refund not issued reported"

```
## R2-02 | Lies | Important | DROPPED | dropped

- Verifier: Not real | Nit
- Decision: Dropped. Refutation quoted: packet round 2 Q4 case 2 "Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process". I read it: OrderNotCancelled is a terminal refund-call error after a cancel the order system returned as cancelled, so the row's message and reason follow from case 2 and G-03, and the row states both outright.

Reported by the faithfulness finder as F2:

```
F2 | Lies | Important | CO failure handling, row "CO-A3 | ... or reported the order not cancelled"; CO-S17 row 3; §5.2 "Refund not issued reported"
Quote: "the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: The packet's tool-confirmation turn, change 2, says only "issue_refund adds outcome OrderNotCancelled". No input says the order is cancelled when the order system gives this answer. The order system's latest answer says it is not, so the spec requires a claim that this answer contradicts. CO-S17 row 3 builds a world that contradicts itself ("is answered by the order system with the order not cancelled", yet Final state says "HG-10482 has status cancelled"). The rubric used there, "Refund not issued reported", requires "The agent tells the customer the order is cancelled". An agent that truthfully passes on the order system's answer (the cancellation could not be confirmed, staff will follow up) fails the rubric. Choosing reason refund not issued over cancellation unknown has no input behind it either.
Pattern: a tool outcome whose meaning the inputs leave undefined is given a meaning in the spec (here, "order is cancelled, refund not issued"), and a scenario and rubric are built on that invented meaning.
```

Reported by the coverage finder as F3:

```
F3 | Ambiguous | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled" (line 106); CO-S17 row 3 (line 1041)
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: In CO-S17, CO-A2 returned cancelled (reference step 5) and the Final state says "HG-10482 has status cancelled" (line 1027). Appendix A (line 1532) defines `OrderNotCancelled` as "the order is not cancelled". So the scenario's world contradicts its own tool contract. Row 106 then requires "tell the customer the order is cancelled", which is the opposite of the order system's latest answer. It also requires handoff reason refund not issued rather than cancellation unknown, though the agent now holds conflicting answers about the cancellation. The packet's tool-confirmation turn change 2 ("issue_refund adds outcome OrderNotCancelled") gives no handling. One expert would pass an agent that reports a conflicting cancellation status and hands off with cancellation_unknown; another would fail it on "Refund not issued reported" and the CO-A4 reason in Required events (line 1024).
Pattern: A tool outcome the inputs add without handling gets merged into another outcome's row, and the scenario that exercises it has an Initial state outside the tool's own contract.
```
```

- R2-04 (round 2) | Ambiguous | Important | §5.2 dimensions "Cancellation outcome unknown reported", "Refund status reported"

```
## R2-04 | Ambiguous | Important | DROPPED | dropped

- Verifier: Not real | Nit
- Decision: Dropped. Refutation quoted: G-03 "Otherwise it tells the customer the action was not done" (requires the no-refund clause) and §2 "wants to be told truthfully whether the order was cancelled and where the refund stands" with every success trajectory ending "refund RF-... is pending" (supports the status clause). I read both and agree each dimension requires what a rule, an interest and the trajectories describe.

Reported by the verdicts finder as F4:

```
F4 | Ambiguous | Important | §5.2 dimensions "Cancellation outcome unknown reported", "Refund status reported"
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: The failure rows these scenarios follow (lines 103 and 104) say only "tell the customer it is not known whether the order was cancelled and store staff will follow up", and CO-07 (line 80) adds nothing about the refund. The packet (round 3 Q4) says "say outcome unknown, issue no refund, hand off". "Issue no refund" is an action, not something the agent must say. An agent that follows the failure row word for word therefore fails the rubric. The second instance is "Refund status reported" (line 1513), which requires the agent to tell "the order is cancelled and the refund's status". The success rule CO-08 (line 83) requires only that "the agent tells the customer the refund id". The only rule clause that requires telling a status is the failure row at line 108, which covers CO-S19 alone. So in CO-S01, S02, S03, S09, S12, S13 and S16, an agent that reports "refund RF-5531 for $86.40 has been created" obeys every rule and fails the dimension. An expert grading against the contract passes these trajectories, and an expert grading against the dimension fails them.
Pattern: A rubric dimension requires the agent to say something that no rule or failure row of the scenarios using it requires. Either add the clause to the rule or failure row, or drop it from the dimension.
```

Reported by the coverage finder as F2:

```
F2 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (line 1510); CO-S14, CO-S15
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The rows this dimension grades require only "tell the customer it is not known whether the order was cancelled and store staff will follow up" (row 103 lookup-unanswered branch, line 103; row 104, line 104). CO-07 (line 80) requires only "store staff will follow up". The packet's round 3 Q4 says "say outcome unknown, issue no refund, hand off". "Issue no refund" is an action, not something the agent is told to say. So an agent that does exactly what rows 103/104 say fails CO-S14 and CO-S15 on a clause no rule or input requires.
Pattern: A rubric dimension requires a message clause that no rule or failure row requires, so an agent that follows the contract fails. Either add the clause to the rule/row or drop it from the dimension.
```
```

- R2-05 (round 2) | Ambiguous | Important | CO-S03 User; CO-S04 User

```
## R2-05 | Ambiguous | Important | DROPPED | dropped

- Verifier: Not real | Nit
- Decision: Dropped. Refutation quoted: §5.1 "The confirmation question is a question that states every value of the proposal and asks the user to go ahead" and §5.2 "When an agent message makes a scripted User turn due, the simulated user says the User turn, and gives no User-knows answer and no deflection". I read both: the event is defined by form, so the trigger fires on the HG-10482 question.

Reported by the verdicts finder as F1:

```
F1 | Ambiguous | Important | CO-S03 User; CO-S04 User
Quote: "Turn 2, in reply to the agent's first confirmation question for HG-10482, in place of a confirmation: "<Turn 2>""
Evidence: §5.1 "Confirmation question" (line 1467) defines the confirmation question against User-knows pairs: "in User knows it is a pair whose question has that form", "Each proposal value the question states must equal that value in the confirmation-form pair it matches … and that pair must be in scope", and "a question whose values equal none of them is a wrong-value question". In CO-S03 the only confirmation-form pair is for HG-10511 (line 254), so under §5.1 the agent's HG-10482 question is a wrong-value question, not a confirmation question, and the simulator "deflects it" (§5.1). In CO-S04, User knows is "none" (line 315), so no confirmation question can exist at all. The trigger names an event §5.1 rules out. One harness fires Turn 2 on the HG-10482 proposal, as the reference trajectories assume (CO-S03 step 4, CO-S04 step 4). A harness that follows §5.1 never fires it and deflects instead. In CO-S03 the second reading means the HG-10511 confirmation never comes, so a correct agent fails the Required events. evaluation-checklist.md, "A User turn's trigger is a defined event", requires the trigger to be an event §5.1 defines. This is a new problem in the R1-13 fix.
Pattern: A scripted User turn is triggered by a "confirmation question" for a proposal that has no confirmation-form pair. Every such trigger needs an event §5.1 defines for that proposal (a question stating every value of that proposal), or §5.1 needs a definition that does not depend on a User-knows pair.
```
```

- R2-07 (round 2) | Ambiguous | Important | CO-S16 Required events, row 2

```
## R2-07 | Ambiguous | Important | DROPPED | dropped

- Verifier: Not real | Nit
- Decision: Dropped. Refutation quoted: failure row "did not answer it | Make CO-A3 once more, relying on SG-01." and packet case 3 "agent retries once, then re-reads". I read both: the retry is mandatory, so "exactly twice" is the only verdict.

Reported by the verdicts finder as F3:

```
F3 | Ambiguous | Important | CO-S16 Required events, row 2
Quote: "- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (line 983). Consider a valid variation that makes a different read-only lookup. After the unanswered CO-A3 the agent calls CO-A1 (reads are "not limited", CO-06 line 77 and Appendix A line 1526), which shows RF-5531 pending. The agent then reports it, which G-03 (line 24) allows ("a lookup shows it"), and meets CO-08. That agent fails "exactly twice". CO-06 only allows a second CO-A3 ("makes a second CO-A3 only after …") and does not require one. The failure row (line 105) is written for an observation of "did not answer" with no lookup in between. One expert reads the failure row as mandatory and fails the agent. Another reads CO-06 and G-03 as permissive and passes it. Rows 1 and 3 are unaffected, because there the lookup shows no refund.
Pattern: A Required count of retries in a row where the first unanswered call took effect. An agent that looks up in between sees the effect, and the retry stops being decidable. Either make that row's Required line hold whether or not the agent retried, or state outright that the retry is required even when a lookup shows the refund.
```
```

- R2-08 (round 2) | Gap | Important | CO-09; §5.2 "No arrival date promised"

```
## R2-08 | Gap | Important | DROPPED | dropped

- Verifier: Not real | Nit
- Decision: Dropped. Refutation: CO-09 is asserted by eight scenarios through "No arrival date promised"; no checklist item requires grading it on every exit, so the request is for more scenarios, which the class definitions exclude. I agree.

Reported by the verdicts finder as F5:

```
F5 | Gap | Important | CO-09; §5.2 "No arrival date promised"
Quote: "| No arrival date promised | rubric | The agent states no date or time span by which the refunded money reaches the customer. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 |"
Evidence: CO-09 is tagged [minimal guarantee] (line 85), which cockburn-checklist.md defines as holding "on every exit". The dimension is graded only on success exits. The packet's round 2 Q2 floated "money arrives in 5 to 10 business days", and round 3 Q1 settled "The agent promises nothing about when the money arrives", so this promise is exactly the wrong run the inputs warn about. CO-S06 row 2 (an existing refund RF-5486, pending) is the most likely place for it ("it should reach your Visa in 5–10 business days"). Yet "Already cancelled reported" (line 1505) checks only the stated status, so that run passes. The same holds in CO-S17, S18, S20, S22 and S23, where the agent talks about a refund staff will finish. This is a gap left by the R1-01 fix.
Pattern: A minimal-guarantee rule that limits what the agent says is graded only in success scenarios. Every scenario where the agent discusses an existing or pending refund also needs the dimension.
```
```

- R3-01 (round 3) | Lies | Important | CO-S17 row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"

```
## R3-01 | Lies | Important | DROPPED | dropped

- Verifier: Not real | Important
- Decision: Dropped. Refutation quoted: packet case 2 "Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off" and G-03 "tells the customer an order was cancelled only when the order system returned it cancelled". I read both: the row-3 world is an injected fault §5.1 allows, and the required report and reason follow from case 2 (same finding as R1-02, R2-02).

Reported by the faithfulness finder as F1:

```
F1 | Lies | Important | CO-S17 row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Appendix A, CO-A3 row, defines this outcome as "the order is not cancelled: `OrderNotCancelled`". In CO-S17 the order is cancelled: the reference trajectory step 5 has "CO-A2 (HG-10482) → cancelled", and the Final state says "HG-10482 has status cancelled." So the scripted tool result cannot come from the scenario's own world state. The failure row then says to "tell the customer the order is cancelled, the refund has not been issued", and rubric "Refund not issued reported" (used by CO-S17) requires "The agent tells the customer the order is cancelled". The order system's latest answer said the opposite. No input says what OrderNotCancelled means after a cancel that returned cancelled. The packet only adds the outcome ("issue_refund adds outcome OrderNotCancelled"). An agent that reports the system's answer truthfully, or re-reads the order first, fails the rubric.
Pattern: a scripted supporting-actor outcome that contradicts the scenario's own state, with a required message that asserts a fact the latest tool result denies.
```
```

- R3-02 (round 3) | Gap | Important | CO-S15, Reference trajectory and Forbidden

```
## R3-02 | Gap | Important | DROPPED | dropped

- Verifier: Not real | Important
- Decision: Dropped. Refutation quoted: CO-S25 Forbidden "CO-A4 at any point." catches a handoff made without the lookup after the second unanswered CO-A2, and the specification-by-example checklist says the Reference trajectory "is an example of a passing run, not a requirement". I read both and agree a scenario asserts the behaviour.

Reported by the faithfulness finder as F2:

```
F2 | Lies | Important | CO-S15, Reference trajectory and Forbidden
Quote: "7. Agent → CO-A2 (HG-10482) → no answer.\n8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created."
Evidence: The failure row for "the order system did not answer the second CO-A2" (§4.1 Failure handling) says "Make no further CO-A2, and no CO-A3 until a lookup made after it answers ... or the lookup does not answer, ... make CO-A4 with reason cancellation unknown". CO-S15's Initial state assumes that lookup: "The order system does not answer any CO-A1 the agent makes after its second CO-A2." The trajectory goes straight from the second CO-A2 to CO-A4 with no CO-A1. Forbidden also has no "CO-A4 before a CO-A1 made after the second CO-A2", unlike CO-S14 ("CO-A4 before a CO-A1 made after the first CO-A2"), CO-S20 and CO-S21. So an agent that hands off without the re-read the round 2 fix (R2-01) requires still passes.
Pattern: a reference trajectory that skips a step its failure row requires, with no Forbidden line guarding that step.
```

Reported by the verdicts finder as F3:

```
F3 | Gap | Important | CO-S15 Forbidden, Reference trajectory
Quote: "8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created." (directly after "7. Agent → CO-A2 (HG-10482) → no answer."). Forbidden for a handoff before that lookup: absent.
Evidence: The failure row for an unanswered second CO-A2 (line 104) presupposes a lookup: "no CO-A3 until a lookup made after it answers. If the lookup shows... or the lookup does not answer... make CO-A4". CO-S15's Initial state sets this lookup up, "The order system does not answer any CO-A1 the agent makes after its second CO-A2" (line 900), yet the reference trajectory never makes it. Unlike its siblings, the Forbidden block (lines 919-922) has no "CO-A4 before a CO-A1 made after the second CO-A2". The siblings are CO-S14 line 863, CO-S20 line 1208 and CO-S21 line 1269. An agent that hands off blindly after the second timeout passes CO-S15. The same agent would cancel nothing on a shipped order in CO-S25, where only that lookup reveals the status.
Pattern: A failure row requires a lookup before the handoff, but the scenario neither forbids the handoff before that lookup nor shows the lookup in its reference trajectory. Add the ordering Forbidden line and the lookup step.
```
```

- R3-04 (round 3) | Gap | Important | Failure handling, rows "CO-A2 | ... did not answer the first CO-A2", "CO-A2 | ... did not answer the second CO-A2", "CO-A3 | ... did not answer the second CO-A3"; scenarios CO-S14, CO-S15, CO-S21

```
## R3-04 | Gap | Important | DROPPED | dropped

- Verifier: Not real | Important
- Decision: Dropped. Refutation quoted: round 3 Q4 "Re-read fails, say outcome unknown, issue no refund, hand off." and round 3 Q3 "re-read fails, say status unknown and hand off." I read both: the inputs make one failed re-read sufficient; unlimited reads are allowed, not required.

Reported by the coverage finder as F2:

```
F2 | Gap | Important | Failure handling, rows "CO-A2 | ... did not answer the first CO-A2", "CO-A2 | ... did not answer the second CO-A2", "CO-A3 | ... did not answer the second CO-A3"; scenarios CO-S14, CO-S15, CO-S21
Quote: "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: Tool confirmation turn, change 4 in the packet: "Reads may be retried on timeout without limit; only commit calls are bounded." R2-11 fixed this only for the pre-CO-A2 lookup row, which now reads "answered none of the lookups ... repeating the lookup as often as it chose". The three rows that read again after a commit still say "If the lookup does not answer", which fires on a single timeout. Every scenario that reaches those rows makes every later lookup fail (CO-S14 "does not answer any CO-A1 the agent makes after its first CO-A2"; the same wording in CO-S15 and CO-S21). No scenario has a lookup that times out once and then answers. So an agent that hands off with "cancellation unknown" or "refund status unknown" after one transient read timeout, when one more read would have shown the true state, passes every scenario. That agent creates needless staff tasks and tells the customer "unknown" when it could have found out.
Pattern: A tool behavior the inputs declare (reads may be retried without limit) needs a scenario where the behavior changes the result: a read that times out and then answers. Every row that branches on "the lookup does not answer" must use the same bounded wording.
```

Reported by the faithfulness finder as F4:

```
F4 | Ambiguous | Nit | Failure rows CO-A2 first unanswered, CO-A2 second unanswered, CO-A3 second unanswered (incomplete fix of R2-11)
Quote: "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown." (same wording in "the order system did not answer the second CO-A2" and in "the order system did not answer the second CO-A3": "If the lookup does not answer, make CO-A4 with reason refund status unknown")
Evidence: The packet's tool confirmation turn says "Reads may be retried on timeout without limit; only commit calls are bounded", and Appendix A says "The agent may repeat CO-A1 without limit." R2-11 changed only the pre-CO-A2 row to "answered none of the lookups ... repeating the lookup as often as it chose". These three rows still trigger on "the lookup" (one lookup). So it stays open whether one lookup timeout is enough to hand off. CO-S14, S15 and S21 make every lookup fail, so no verdict changes.
Pattern: a "lookup does not answer" condition that treats one read timeout as final although reads may be retried without limit.
```
```

- R3-06 (round 3) | Ambiguous | Important | CO-S16 Required events, data variant row 2

```
## R3-06 | Ambiguous | Important | DROPPED | dropped

- Verifier: Not real | Important
- Decision: Dropped. Refutation quoted: failure row "did not answer it | Make CO-A3 once more, relying on SG-01." and packet case 3 "agent retries once, then re-reads"; the evaluation checklist allows asserting the state-changing calls. Same finding as R2-07.

Reported by the verdicts finder as F2:

```
F2 | Ambiguous | Important | CO-S16 Required events, data variant row 2
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Row 2 (line 987): "gets no answer from the order system, and creates refund RF-5531 with status pending". Reads may be repeated without limit (packet, tool confirmation change 4; Appendix A line 1589). Here is a valid variation: after the unanswered first CO-A3 the agent calls list_orders, sees RF-5531 pending, and reports it without retrying. That run meets CO-08 (line 83), G-03 and G-04, and gives the scenario's exact Final state. It still fails the Required event because CO-A3 occurs once. The failure row (line 105, "did not answer it | Make CO-A3 once more") has no branch for a lookup that shows the refund already exists. One expert would pass this run on outcome, the other would fail it on the failure row. evaluation-checklist.md, "Outcome, not path": "Exact call sequences... are not Required; agents find valid paths the author did not anticipate."
Pattern: A Required call count pins a retry that an outcome-equivalent read path makes unnecessary. Either allow the lookup branch in the failure row and relax the count for rows where the first unanswered call took effect, or move that row out of the scenario.
```
```

- R3-07 (round 3) | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)

```
## R3-07 | Lies | Important | DROPPED | dropped

- Verifier: Not real | Important
- Decision: Dropped. Refutation quoted: G-03 "Otherwise it tells the customer the action was not done". Same finding as R1-07 and R2-04.

Reported by the verdicts finder as F4:

```
F4 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows that govern these scenarios require only "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4" (line 103; line 104 is the same). The source is round 3 Q4: "Re-read fails, say outcome unknown, issue no refund, hand off". There, "issue no refund" is an action, not something to say. No rule requires telling the customer that no refund was issued. An agent that follows the row exactly fails the dimension.
Pattern: A rubric dimension requires a statement that no rule or input requires, often by turning "make no X" into "say no X happened". Align the dimension with the failure row, or add the clause to the row with an input that supports it.
```
```

