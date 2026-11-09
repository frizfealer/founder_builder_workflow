# Round 3 merged findings

12 findings: 7 Important, 5 Nit (merged from 15 raw: faithfulness 5, verdicts 6, coverage 4).

Decisions: 7 kept, 5 dropped, 0 Pre-existing. Important findings went to one adversarial verifier (eval/agent-spec/run-e4-base-3/round3-verifier.md is the scratch copy; its full report is reproduced at the end). Nits went straight to 4.5.

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

## R3-03 | Ambiguous | Important | KEPT | fixed

- Verifier: Real | Important
- Decision: Kept on the Gap half, which the verifier could not refute; the Ambiguous half is refuted by SG-04 (a late second cancel can still land, so the agent cannot tell). Behaviour in that branch also listed as an open question.

Reported by the faithfulness finder as F3:

```
F3 | Ambiguous | Important | Failure row CO-A2 "did not answer the second CO-A2"; G-03; CO-07
Quote: "If it shows the order placed or processing, or the lookup does not answer, make no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown."
Evidence: G-03 says "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." CO-07 allows CO-A4 only "when the agent cannot tell whether the order was cancelled ... CO-A4 occurs in no other situation." A lookup showing placed or processing does tell the agent the order was not cancelled. So under G-03 and CO-07 the agent should report "not cancelled" and must not make CO-A4, while this row requires "unknown" and CO-A4. The inputs (round 3 Q4) set behavior only for the first unanswered cancel. Following the rules and following the row lead to opposite verdicts on the same trajectory.
Pattern: a failure-row branch that contradicts a global or capability rule about what the agent may say and when it may hand off.
```

Reported by the coverage finder as F1:

```
F1 | Gap | Important | Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"
Quote: "If it shows the order placed or processing, or the lookup does not answer, make no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown."
Evidence: The R2-01 fix (answered.md, Round 2) added scenarios for three of this row's four lookup branches. The cancelled branch is CO-S13 row 3, the shipped branch is CO-S25, and the no-answer branch is CO-S15, whose Initial state says "The order system does not answer any CO-A1 the agent makes after its second CO-A2." No scenario has the lookup after the second unanswered CO-A2 come back with the order still placed or processing. That branch has its own wrong runs, and nothing catches them: a third CO-A2 (forbidden only by CO-06), telling the customer "your order was not cancelled" (the lookup seems to show that, but the row requires "not known"), or ending with no CO-A4. The row's outcome is a CO-A4, so leaving that branch untested lets an agent skip the handoff. The fix is incomplete.
Pattern: When a failure row branches on what a lookup shows, each branch that leads to a different action or message needs a scenario whose Initial state produces that lookup result.
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

## R3-05 | Ambiguous | Important | KEPT | fixed

- Verifier: Not real | Important
- Decision: Kept. The verifier called its refutation its weakest and conceded the tension with §5.1 "A question with the right form and one wrong value is not the confirmation question"; I read that sentence as applying here (the HG-10482 question has the form and values unequal to the only pair), so the clause does not refute the finding. The defect was introduced by the R1-13 fix.

Reported by the verdicts finder as F1:

```
F1 | Ambiguous | Important | CO-S03 User block, CO-S04 User block
Quote: "Turn 2, in reply to the agent's first confirmation question for HG-10482, in place of a confirmation: "<Turn 2>""
Evidence: §5.1 (agent-spec.md line 1528) defines the confirmation question by a matching pair: "in User knows it is a pair whose question has that form... Each proposal value the question states must equal that value in the confirmation-form pair it matches... a question whose values equal none of them is a wrong-value question" that the simulated user deflects. In CO-S03 the only confirmation-form pair is for HG-10511 (line 255), and CO-S04 has "User knows: none." (line 316). Under §5.1, no "confirmation question for HG-10482" can exist in either scenario, so the trigger names an event that cannot happen. One harness reading fires Turn 2 on a confirmation-shaped HG-10482 question, matched on meaning. The other treats that question as a wrong-value question, deflects it and never says Turn 2. Under the second reading a correct CO-S03 agent never gets the switch and fails "CO-A2 occurs exactly once, for HG-10511". evaluation-checklist.md, "A User turn's trigger is a defined event", requires a trigger that §5.1 defines. This is the R1-13 fix, and it is incomplete: it replaced an undefined term with one whose §5.1 definition rules the event out.
Pattern: A scripted User turn is triggered by "the confirmation question" for a proposal that has no confirmation-form pair in User knows. Either define in §5.1 a confirmation-form question for a named order that has no matching pair, or anchor the turn on a defined event.
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

## R3-08 | Lies | Nit | KEPT | fixed

- Verifier: Nit, not verified

Reported by the faithfulness finder as F5:

```
F5 | Lies | Nit | CO-S05, Unambiguity note
Quote: "The order is past the cutoff in every row, so any cancellation, refund or handoff fails in the action log"
Evidence: Packet round 2 Q1 answer: "Cancellable while placed or processing, no time limit." CO-01 makes cancellability depend on status only. No cutoff exists in the inputs.
Pattern: a note that states a domain fact the inputs contradict.
```

## R3-09 | Gap | Nit | KEPT | answered

- Verifier: Nit, not verified
- Decision: CO-03's acting side is CO-S09; CO-S08 is the hold-back.

Reported by the coverage finder as F3:

```
F3 | Gap | Nit | CO-03; Failure handling row "any | the customer asked to cancel only some of an order's items"
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence: This is an "act only when" clause: propose only once the customer asks for the whole order. The only scenario for it is CO-S08, which holds back: the customer declines with "No, I'll keep it." No scenario has the customer, after a partial-items request, ask to cancel the whole order, with the agent then proposing and making CO-A2 and CO-A3. An agent that refuses any cancellation for the rest of the conversation once the customer asks for partial items passes the suite. The evaluation checklist says: "For every rule that says 'act only when', one scenario shows the agent acting when it should and one shows it holding back."
Pattern: Each "propose nothing until X" clause needs an acting scenario in which X happens and the agent goes on to the confirmed write.
```

## R3-10 | Gap | Nit | KEPT | open

- Verifier: Nit, not verified
- Decision: Inputs do not say what the agent tells a customer with no open order who names none.

Reported by the coverage finder as F4:

```
F4 | Gap | Nit | CO-01 / CO-02; Failure handling
Quote: absent
Evidence: The cockburn checklist brainstorm lists "the lookup returns more than one plausible match, or none (ambiguous match)". The spec handles more than one open order (CO-02, CO-S02) and a named number matching none of the customer's orders (CO-02 row, CO-S07). It has no rule or row for a customer who names no order (CO-S01 row 4 wording, "I need to cancel my order, please.") when the answered lookup shows no orders, or no order with status placed or processing. The precondition only guarantees that the customer is signed in, not that they have an order. The agent can detect this case, and what it tells the customer is left for the builder to invent.
Pattern: Each lookup result the agent can observe (several matches, one, none) needs a row that says what the agent tells the customer.
```

## R3-11 | Ambiguous | Nit | KEPT | fixed

- Verifier: Nit, not verified

Reported by the verdicts finder as F5:

```
F5 | Ambiguous | Nit | §5.2 dimension "Shipped order explained", used by CO-S05
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: In CO-S05 the agent never attempts a cancellation. CO-01 (line 62) and the failure row (line 95) require "has shipped and cannot be cancelled". CO-S05's own Unambiguity note (line 400) says the dimension checks "has shipped and cannot be cancelled". The shared definition asks for "was not cancelled", which fits CO-S11 and CO-S25 but not CO-S05. A literal judge could fail a CO-S05 agent that said only "cannot be cancelled". evaluation-checklist.md, "A shared rubric dimension has one definition."
Pattern: A shared dimension's wording fits some of its scenarios' failure rows but not others. Write wording that holds in every scenario, or split the dimension.
```

## R3-12 | Gap | Nit | KEPT | open

- Verifier: Nit, not verified
- Decision: Fix changes CO-03's rule text; proposed to the user.

Reported by the verdicts finder as F6:

```
F6 | Gap | Nit | CO-03; CO-S08
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: For a partial-item request, CO-03 requires both statements. The failure row (line 97) keeps only the first: "Tell the customer only the whole order can be cancelled". CO-S08's dimension "Whole order only explained" (line 1569) checks only "only the whole order can be cancelled". For a payment-method request, CO-S09's "Refund terms explained" (line 1570) checks only the refund-terms half. Neither scenario asserts the other half of the rule's statement.
Pattern: A rule makes one compound statement mandatory for several triggers, but each scenario's dimension asserts only part of it. Narrow the rule per trigger to match the rows, or extend the dimensions.
```

## Verifier report, verbatim

```
R3-01 | Not real | Important | The inputs support this scenario. Packet Q4 failure case 2 reads: "Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process ... none on a terminal one." Row 3 is exactly that case: CO-A2 returned cancelled, then issue_refund returned an error outcome. The scripted outcome is allowed by §5.1 "A supporting actor answers every call normally unless an Initial-state line says otherwise." Saying "the order is cancelled" is allowed by G-03 "tells the customer an order was cancelled only when the order system returned it cancelled", and step 5's CO-A2 did return it cancelled. The Final state "status cancelled" follows from Appendix A, CO-A2 effect: "Sets the order's status to cancelled when it returns status: "cancelled"".

R3-02 | Not real | Important | Blind handoff is already caught. CO-S25 has Forbidden "CO-A4 at any point." and the rubric "Shipped order explained", so an agent that hands off after the second unanswered CO-A2 without a lookup fails CO-S25. The finding itself concedes this ("would cancel nothing on a shipped order in CO-S25"). The row "Make no further CO-A2, and no CO-A3 until a lookup made after it answers" restricts only CO-A2 and CO-A3. CO-07 allows CO-A4 "when the agent cannot tell whether the order was cancelled". So the CO-S15 trajectory breaks no rule. specification-by-example-checklist.md says the Reference trajectory "is an example of a passing run, not a requirement", and the CO-S15 trajectory passes every CO-S15 line.

R3-03 | Real | Important | I could not refute the Gap half (coverage F1). The row's branch "If it shows the order placed or processing ... make CO-A4 with reason cancellation unknown" has no scenario. The other branches do: CO-S13 row 3 is cancelled, CO-S25 is shipped, CO-S15 is the lookup with no answer. No Initial state has the lookup after the second unanswered CO-A2 come back placed or processing. So an agent that skips the handoff, or says "not cancelled", in that branch passes every scenario. The Ambiguous half (faithfulness F3) can be refuted. SG-04 "Covers: A second cancellation call that reaches the order system after a first, unanswered one took effect late" means a placed or processing lookup does not prove the unanswered cancel will not land, so the agent "cannot tell" under G-03 and CO-07. Also, no scenario verdict depends on that branch.

R3-04 | Not real | Important | The single-lookup wording comes from the inputs. Round 3 Q4: "Re-read fails, say outcome unknown, issue no refund, hand off." Round 3 Q3: "re-read fails, say status unknown and hand off." The packet's "Reads may be retried on timeout without limit; only commit calls are bounded" allows retries but does not require them. So an agent that hands off after one failed re-read follows the inputs and is not a wrong run that needs a scenario. Appendix A "a CO-A1 made after an action is any CO-A1 call issued after that action's call, whatever it returned" and the Initial states ("does not answer any CO-A1 ...") make every verdict independent of how many reads the agent makes. The F4 Nit half admits "no verdict changes".

R3-05 | Not real | Important | My weakest refutation. §5.1 defines the event by its form, without reference to any pair: "The confirmation question is a question that states every value of the proposal and asks the user to go ahead." The trigger "the agent's first confirmation question for HG-10482" names the proposal by its order, and Initial state fixes that order's values. The value-equality clauses only govern when the simulated user gives a confirmation answer: "the simulated user does not give the confirmation answer to it". The "wrong-value question" clause applies only "When more than one confirmation-form pair is in scope", which holds in neither CO-S03 (one pair) nor CO-S04 (none). §5.2 decides which comes first: "When an agent message makes a scripted User turn due, the simulated user says the User turn, and gives ... no deflection to any question in that message." Some tension remains with "A question with the right form and one wrong value is not the confirmation question", so if the main thread reads that sentence as global, this finding stands.

R3-06 | Not real | Important | The failure row settles the case without conditions: "the order system ... did not answer it | Make CO-A3 once more, relying on SG-01." The input supports that row: packet failure case 3 says "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads". So the lookup-only path breaks the row, and experts reach the same fail verdict. evaluation-checklist.md "Outcome, not path" allows asserting "the state-changing calls that produced it", and CO-A3 is state-changing.

R3-07 | Not real | Important | A rule does require the statement. G-03: "tells the customer a refund is pending or issued only when the order system returned that refund with that status ... Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." In CO-S14 and CO-S15 no CO-A3 is made, so the refund action was not done, and G-03 requires telling the customer so. The input behind G-03 is round 2 Q1: "the agent must report that truthfully and issue no refund call". §2 also states the primary actor "wants to be told truthfully whether the order was cancelled and where the refund stands." The dimension matches the reference trajectories: CO-S14 step 8 and CO-S15 step 9 both say "no refund was issued".

Count: Real 1, Not real 6, Style only 0.
```
