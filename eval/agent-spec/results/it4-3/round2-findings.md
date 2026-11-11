# Round 2 merged findings

16 merged findings: 10 Important, 6 Nit.

## R2-01 | Ambiguous | Important | sources: faithfulness:F1, verdicts:F1, verdicts:F6

[faithfulness F1]
F1 | Ambiguous | Important | CO-S03 User, CO-S04 User (fix for R1-17); also CO-S02 User
Quote: "Turn 2, in reply to the agent's first confirmation question (§5.1) for HG-10482: "<Turn 2>"" (CO-S03 line 252, CO-S04 line 313)
Evidence: §5.1 "Confirmation question" (agent-spec.md line 1592) defines the confirmation question as one whose values each "must equal that value in the confirmation-form pair it matches ... and that pair must be in scope", and says "A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it." In CO-S03 the only User-knows pair is "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?" (line 255), so under §5.1 a proposal for HG-10482 / $86.40 / Visa ending 4242 is a wrong-value question that gets deflected, not "the confirmation question for HG-10482". In CO-S04 User knows is "none." (line 316), so no confirmation-form pair exists and §5.1 never yields a confirmation question. In both scenarios the event that makes Turn 2 due cannot happen as §5.1 defines it. One harness never says Turn 2 and deflects the proposal; another reads "confirmation question" loosely and says Turn 2. The verdicts differ. Weaker instance of the same pattern, from the R1-11 fix: CO-S02 line 190, "Turn 2, in reply to the agent's first question that asks which order the customer wants to cancel". §5.1 does not define that trigger event, but the evaluation checklist requires one: "A User turn's trigger names an event §5.1 defines ... never 'a proposal' or 'an offer'" (.claude/skills/agent-spec/references/evaluation-checklist.md, Scenario design).
Pattern: A scripted User turn's trigger must be an event §5.1 defines, and that event must be able to occur in that scenario under §5.1's definition. A trigger that names a §5.1 term whose definition excludes the case (no pair, or a pair with other values) leaves the turn's timing to judgment.

[verdicts F1]
F1 | Ambiguous | Important | CO-S03 and CO-S04, User block (R1-17 fix incomplete)
Quote: "Turn 2, in reply to the agent's first confirmation question (§5.1) for HG-10482: \"<Turn 2>\"" (CO-S03 l.252; CO-S04 l.313, same line)
Evidence: §5.1 (l.1592) defines the confirmation question by its match to a pair: "Each proposal value the question states must equal that value in the confirmation-form pair it matches ... and that pair must be in scope ... A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it." CO-S03's only pair is for HG-10511 (l.255), and CO-S04 has no User-knows pairs ("none.", l.316). So under §5.1, a question proposing HG-10482 can never be "the confirmation question", and §5.1 tells the simulator to deflect it. A simulator that follows §5.1 literally never says Turn 2. In CO-S03 the agent then never hears about the switch and never cancels HG-10511, so a correct agent fails "CO-A2 occurs exactly once, for HG-10511". In CO-S04 no withdrawal ever arrives and no confirmation is possible, so the scenario passes every agent and never tests withdrawal. A simulator that reads "confirmation question" by its form alone says Turn 2 and the scenarios work. The two readings give different verdicts.
Pattern: A User-turn trigger points to the §5.1 confirmation question for a proposal that no in-scope pair matches, while §5.1 makes being the confirmation question depend on matching such a pair. Define the trigger by form only (a question stating every proposal value for the named order and asking to go ahead), apart from pair matching.

[verdicts F6]
F6 | Ambiguous | Nit | CO-S02, User block and Unambiguity note
Quote: "Turn 2, in reply to the agent's first question that asks which order the customer wants to cancel: \"<Turn 2>\""
Evidence: The evaluation checklist says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." §5.1 defines no which-order question. Suppose the agent guesses and asks "Shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?". One simulator treats that as asking which order and says Turn 2; another deflects it, since the pair is "(after Turn 2)". Under either reading the guessing agent then recovers and passes, so the Unambiguity note's "a proposal that guesses the order before asking is deflected" (l.234) settles nothing. CO-02's "proposes nothing until the customer names one" is not checked by any line.
Pattern: A scripted turn triggered by a kind of agent message that §5.1 does not define, and a hold-back clause that the scenario's lines cannot detect.

**Verifier:** R2-01 | Real | Important | Cannot refute. §5.1 defines the confirmation question by matching an in-scope pair: "Each proposal value the question states must equal that value in the confirmation-form pair it matches ... and that pair must be in scope ... A question with the right form and one wrong value is not the confirmation question". CO-S03's only pair is for HG-10511 (l.255) and CO-S04's User knows is "none." (l.316). So "the agent's first confirmation question (§5.1) for HG-10482" can never happen under §5.1. §5.2's "When an agent message makes a scripted User turn due, the simulated user says the User turn" decides which response wins once a turn is due, not whether it is due. The CO-S02 part also stands: "first question that asks which order" is not a §5.1 event, and evaluation-checklist.md requires one ("A User turn's trigger names an event §5.1 defines").

**Decision:** kept (Important) — status: fixed

## R2-02 | Lies | Important | sources: faithfulness:F2

[faithfulness F2]
F2 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15); also "Refund status reported" (CO-S19)
Quote: "In its messages after its last CO-A2, the agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows this dimension grades require only "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown" (agent-spec.md lines 103 and 104, the "does not answer" branch). CO-07 (line 80) and G-03 (line 24) add nothing about saying no refund was issued. The input says only "Re-read fails, say outcome unknown, issue no refund, hand off" (review-packet.md, Round 3 Q4). "Issue no refund" is an action, not something the agent must say. An agent that obeys every rule and says "I can't tell whether your order was cancelled; store staff will follow up" fails CO-S14 and CO-S15 on this dimension. Same pattern in "Refund status reported" (line 1641), which requires "the order is cancelled and the refund's status is ...", while its failure row says only "tell the customer that status and the refund id" (line 108).
Pattern: A rubric dimension's required statements must match the failure row or rule it grades, adding no requirement that the inputs and rules do not give. Otherwise an agent that obeys the contract fails the scenario.

**Verifier:** R2-02 | Real | Nit | Partly refuted. For CO-S14/CO-S15, G-03 (l.24) supports requiring "no refund was issued": "tells the customer a refund is pending or issued only when ... Otherwise it tells the customer the action was not done". So the claim that an agent "that obeys every rule" fails there is wrong, and that part does not stand. The "Refund status reported" part (l.1641, CO-S19) stands. Its requirement that the agent say "the order is cancelled" is only permitted by G-03, not required. Failure row l.108 requires only "that status and the refund id", and CO-08 requires only the refund id. Downgraded to Nit because only that one dimension in one scenario remains.

**Decision:** kept (Nit) — status: fixed. Reason: Kept at the verifier's Nit. The CO-S14/CO-S15 part is refuted by G-03 ('Otherwise it tells the customer the action was not done'), which I read and agree with; the 'Refund status reported' part stands and is fixed.

## R2-03 | Ambiguous | Important | sources: verdicts:F4

[verdicts F4]
F4 | Ambiguous | Important | §5.2 dimensions "Cancellation not done reported" and "Cancellation outcome unknown reported" (R1-16 fix)
Quote: "In its messages after its last CO-A2, the agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up" (l.1636; l.1635 has the same "In its messages after its last CO-A2")
Evidence: §5.1 (l.1594): "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one." §5.2 (l.1624): "A rubric judge reads every text the agent sends, including text sent alongside a tool call." Take CO-S14 or CO-S15. The agent writes "I couldn't confirm whether the cancellation went through and no refund was made, so I'm creating a task for our staff" alongside its CO-A4 call, and its final message says "Store staff will follow up." One judge counts only §5.1 messages and fails the run, because the required statements are missing from them. Another reads all text, as §5.2 directs, and passes it. The same split applies to the "never says" clauses.
Pattern: A rubric definition uses the §5.1 term "messages", which excludes tool-call text, in a judge that §5.2 tells to read all text. Say which text the window covers.

**Verifier:** R2-03 | Real | Important | Cannot refute. The dimension's window "In its messages after its last CO-A2" (l.1635-1636) uses §5.1's defined term, and §5.1 excludes tool-call text: "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one" (l.1594). §5.2 tells the judge to read all text: "A rubric judge reads every text the agent sends, including text sent alongside a tool call" (l.1624). No clause says which one governs a windowed dimension.

**Decision:** kept (Important) — status: fixed

## R2-04 | Ambiguous | Important | sources: verdicts:F5

[verdicts F5]
F5 | Ambiguous | Important | CO-S19, dimension "Refund status reported" (same pattern as R1-16, new instance)
Quote: "The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it." (l.1641)
Evidence: After the R1-13 fix, CO-S19's first CO-A3 "creates no refund" (l.1129), and lookups are unlimited (CO-06). In a valid variation, the agent looks up between the two refund calls, sees no refund, and truthfully says alongside the second CO-A3 "the refund hasn't gone through yet, trying again". The dimension has no window, and the judge reads all text (§5.2 l.1624). One judge counts "hasn't gone through" as a stated status other than the row's pending or issued and fails the run. Another treats it as interim narration and passes it.
Pattern: A shared rubric clause "states no other X", applied over the whole trial in a scenario where a different X is briefly true and visible to the agent. Bound it to messages after the last read, or to the final message.

**Verifier:** R2-04 | Real | Nit | Cannot refute. "Refund status reported" (l.1641) has no window, and the judge reads all text (l.1624). The interim case is valid: failure row l.105 does not forbid a lookup between the two CO-A3 calls, and CO-S19's first CO-A3 "creates no refund" (l.1129). Nit because the split needs an extra lookup plus narration in tool-call text, and whether "hasn't gone through" counts as a status of a refund that does not yet exist is borderline.

**Decision:** kept (Nit) — status: fixed

## R2-05 | Lies | Important | sources: faithfulness:F3

[faithfulness F3]
F3 | Lies | Important | Failure row "CO-A2 | the order system did not answer the second CO-A2", placed-or-processing branch; CO-S26 (fix for R1-02)
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 and no CO-A4."
Evidence: The spec's own Appendix B says an unanswered cancellation can take effect after a later lookup. SG-04 "Covers: A second cancellation call that reaches the order system after a first, unanswered one took effect late." (line 1678). Under CO-06 (line 77), a second CO-A2 happens only after a lookup shows the order still placed or processing. So the case SG-04 covers is exactly one where an unanswered call took effect after a lookup showed the order open. By the same model, the second unanswered CO-A2 can also cancel the order after the lookup that shows it open. The agent then tells the customer "not cancelled", the order ends up cancelled with no refund, and no follow-up task exists. That contradicts G-03 ("when it cannot tell, that the outcome is unknown", line 24), CO-07 ("when the agent cannot tell whether the order was cancelled, the agent makes CO-A4", line 80), and the support team's interest in "every order ... whose cancellation is uncertain handed to it" (§2, line 11). The inputs never cover a second cancel timeout. Round 3 Q4 treats a lookup showing the order open only as grounds to resend once, which SG-04 makes safe, not as proof that the cancellation will never land. CO-S26's Forbidden "CO-A4 at any point." (line 1562) and its dimension "Cancellation not done reported" (line 1635) build the unsupported claim into the verdict.
Pattern: When the spec's own guarantees allow an unanswered commit to take effect after a lookup, a lookup made after the last allowed attempt cannot support telling the customer the action was not done, or skipping the handoff. Either state that a lookup after an unanswered call settles its effect (and drop SG-04's late-effect Covers line), or treat that branch as cancellation unknown.

Checked and found consistent (no finding): every Reference trajectory against Data variants row 1 (CO-S01 to CO-S26); tool results replayed against Final state assertions; Required events identical across rows; Appendix A tool names, parameters and outcomes against the tool confirmation turn (OrderNotCancellable{status}, OrderNotFound, OrderNotCancelled, idempotency SG-01/03/04, unlimited read retries); retry limits against case 2, case 3 and Round 3 Q3/Q4; terminal reasons (card closed or expired, provider declined) in CO-S17 and CO-S23; "Today is 2026-11-05, a Thursday" (correct; HG-10511 placed 2026-11-04 is "yesterday" for CO-S02 row 3); trial count 5 and message cap 12. Findings answered or left open in answered.md (R1-01, R1-05, R1-07, R1-12) were not reported again.

Files read: /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4-3/review-packet.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/product-idea.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4-3/agent-spec.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4-3/answered.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/ (verification.md, evaluation-checklist.md, specification-by-example-checklist.md). No files edited or created.

**Verifier:** R2-05 | Real | Important | Cannot refute in full. G-04 ("repeats it only when a lookup made after that action shows it took no effect", l.27) and Round 3 Q4 ("Still placed or processing, send the cancel once more") treat a lookup as showing the effect, but only for the first timeout. No input covers a second cancel timeout. The spec's own SG-04 Covers line, "A second cancellation call that reaches the order system after a first, unanswered one took effect late" (l.1678), says a lookup showing the order open does not rule out a late effect. That contradicts the l.104 branch's "tell the customer the order was not cancelled ... make no CO-A4" and CO-S26's Forbidden "CO-A4 at any point."

**Decision:** kept (Important) — status: fixed. Reason: Fixed on the spec's own rules (G-03 'when it cannot tell', CO-07, SG-04's late-effect line): after the second unanswered CO-A2, a lookup showing the order open now leads to 'outcome unknown' and CO-A4 cancellation unknown. No input covers a second cancel timeout, so the user should confirm this reading (open question).

## R2-06 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | Forbidden lines "<action> before a CO-A1 made after <action>"; Appendix A "Which order an action is for"
Quote: "CO-A4 before a CO-A1 made after the first CO-A2." (CO-S14 l.863)
Evidence: Appendix A (l.1653) defines only the noun phrase: "'a CO-A1 made after' an action is any CO-A1 call issued after that action's call". It does not say whether "X before a CO-A1 made after Y" means "no such CO-A1 comes before X" (universal) or "some such CO-A1 comes after X" (existential). The two readings give opposite verdicts on both test runs:
- Wrong run, CO-S14: CO-A2 times out and the agent hands off at once with no lookup. Under the existential reading no CO-A1 exists, so the line does not fire, and every Required, Final-state and rubric line can still pass.
- Wrong run, CO-S13: a blind second CO-A2 with no lookup (the input's "no blind resend") passes under the existential reading.
- Valid run, CO-S14 and CO-S15: the agent hands off, then retries the unanswered lookup ("Reads may be retried on timeout without limit"; CO-06 "lookups are not limited"). Under the existential reading it fails.
Instances: CO-S12 l.747 "CO-A3 before a CO-A1 made after the first CO-A2."; CO-S13 l.803; CO-S14 l.863; CO-S15 l.919 and l.922; CO-S20 l.1210; CO-S21 l.1271; CO-S25 l.1500 and l.1502; CO-S26 l.1559.
Pattern: An ordering Forbidden line whose quantifier over a repeatable read is left open. State it as "<action> with no CO-A1 between <earlier action> and it".

**Verifier:** R2-06 | Real | Nit | Partly refuted. The Unambiguity notes fix the intended reading (no lookup between the two actions) for several instances. CO-S13: "a second cancellation sent without that lookup". CO-S14 and CO-S21: "a handoff before a lookup was tried". CO-S20: "a handoff without one". CO-S15 (l.922 only): "a handoff before that lookup". These settle CO-S13 l.803, CO-S14 l.863, CO-S15 l.922, CO-S20 l.1210 and CO-S21 l.1271. No note settles CO-S12 l.747 (its note repeats the same open wording, "a refund issued before a lookup made after that cancellation"), CO-S15 l.919, CO-S25 l.1500 and l.1502, or CO-S26 l.1559. Nit because the line shape is shared and the notes pin its step definition.

**Decision:** kept (Nit) — status: fixed

## R2-07 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: Row 2 makes that CO-A2 time out: "gets no answer from the order system and cancels nothing" (l.700). Nothing defines whether a timed-out call "reaches the order system". §5.1 anchors occurrence to issuing the call ("An action occurs when the agent issues that action's commit call", l.1606). The evaluation checklist says a mid-trial change must be "anchored to a state-changing call", meaning the agent's nth call, not its arrival. If a harness treats a timed-out call as not having reached the order system, the status stays processing and the lookup after the timeout shows processing. The failure row (l.103) then requires "make CO-A2 once more", and that trips Forbidden "A second CO-A2" (l.691). A correct agent fails row 2.
Pattern: A mid-trial state change tied to a supporting actor receiving a call, where the call itself may time out. Tie it to the agent issuing its nth call.

**Verifier:** R2-07 | Not real | Important | The CO-S11 Unambiguity note settles it: "in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation" (l.712). Final state for both rows also says "HG-10482 has status shipped and no refund" (l.687). So in row 2 the status flips even though the CO-A2 timed out, and the lookup after it shows shipped.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: CO-S11's Unambiguity note 'in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation' and the Final state 'HG-10482 has status shipped and no refund' for both rows fix the reading that the status flips even when the first CO-A2 times out.

## R2-08 | Ambiguous | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Ambiguous | Nit | §5.1 Turn anchors; every "before/after the user's confirmation turn" line
Quote: "CO-A2 before the user's confirmation turn." (CO-S01 l.148)
Evidence: §5.1 (l.1590) defines the anchor for one or for several confirmation turns ("If a trial has more than one ... the first") but not for a trial with none. Take an agent that cancels without ever asking a confirmation question. Whether this Forbidden line fires is undefined. That changes the trial score ("Any Forbidden event scores the trial 0" versus partial Required credit) and the Forbidden pass^k number. The Required "after the user's confirmation turn" fails either way, so scenario pass is unchanged. Instances: CO-S01 l.148, CO-S02 l.208, CO-S03 l.272, CO-S09 l.587, plus the Required lines of every confirm scenario.
Pattern: A turn anchor with no defined value when the anchoring turn never occurs.

**Verifier:** R2-08 | Real | Nit | Cannot refute. §5.1 Turn anchors (l.1590) defines "the user's confirmation turn" for one or for several confirmation turns, not for none. No Unambiguity note says what "CO-A2 before the user's confirmation turn" means when no confirmation turn occurs. The finding itself grants that scenario pass is unchanged; the trial score and the Forbidden pass^k differ.

**Decision:** kept (Nit) — status: open. Reason: The defect is in §5.1 fixed text (Turn anchors), which step 4 never edits; left for the user / template.

## R2-09 | Untestable | Nit | sources: verdicts:F8

[verdicts F8]
F8 | Untestable | Nit | CO-S17, CO-S22, CO-S23, Initial state and Reference trajectory (R1-06 fix incomplete)
Quote: "creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has been closed" (CO-S17 row 1, l.1045)
Evidence: After the R1-06 fix, Appendix A's CO-A3 result is `{refund_id, amount, payment_method, status}` (l.1659), with no field for the reason. The "because ..." part cannot become a tool result, so CO-S17 rows 1 and 2 (closed versus declined) and CO-S23 rows 1 and 2 (closed versus expired, l.1397-1398) look the same to the agent. The reference trajectories still show a result the tool cannot return: "refund RF-5531, failed, card closed" (CO-S17 l.1054, CO-S22 l.1348, CO-S23 l.1406). CO-S22's Initial state (l.1308) has the same clause.
Pattern: An Initial-state outcome, and a reference result, that carry a detail the bound tool does not return.

**Verifier:** R2-09 | Style only | Nit | Changes no verdict and no agent behavior. Appendix A's CO-A3 result is `{refund_id, amount, payment_method, status}` (l.1659), so the agent sees the same `status: "failed"` result in CO-S17 rows 1/2 and CO-S23 rows 1/2. Every Required, Final-state and dimension line ("Refund not issued reported", "Staff contact unconfirmed reported") is the same whatever the reason. The "because ..." clause and "card closed" in the reference steps are descriptive text a harness drops.

**Decision:** kept (Nit) — status: fixed. Reason: Style only rejected: a reference result that the bound tool cannot return is a content mismatch between the trajectory and Appendix A, not wording, style or preference.

## R2-10 | Untestable | Nit | sources: verdicts:F9

[verdicts F9]
F9 | Untestable | Nit | §5.1 End of trial, for scenarios where lookups never answer
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A (l.1653) says "The agent may repeat CO-A1 without limit". CO-S10 (l.623), CO-S14 (l.842), CO-S15 (l.900) and CO-S21 (l.1249) make every such lookup go unanswered. An agent that keeps retrying the lookup never sends an agent message (§5.1 l.1594: tool-call text is not one), so neither end condition is ever reached and no verdict can be computed.
Pattern: The trial-end rule counts only messages, while a tool can be called without limit and is scripted to fail forever. Add a tool-call or step cap.

**Verifier:** R2-10 | Real | Nit | Cannot refute. §5.1 End of trial (l.1596) counts only agent messages. Appendix A says "The agent may repeat CO-A1 without limit" (l.1653), and CO-S10, S14, S15 and S21 script every lookup to go unanswered. No step or tool-call cap exists anywhere in §5.

**Decision:** kept (Nit) — status: open. Reason: The defect is in §5.1 fixed text (End of trial), which step 4 never edits; left for the user / template.

## R2-11 | Gap | Nit | sources: verdicts:F10

[verdicts F10]
F10 | Gap | Nit | CO-S01 row 4 (R1-10 fix incomplete)
Quote: "| 4 | I'd like to cancel my order, please. | HG-10547 | processing | $64.00 | Visa ending 6021 | RF-5535 |"
Evidence: The Unambiguity note says "the agent has nothing to ask" (l.174). But no User-knows deflection and no dimension scores an unneeded "which order?" question, and §5.2 says precision is "never folded into the score" (l.1620). An agent that always asks which order gets deflected, then proposes HG-10547 and passes. Row 4 catches only an agent that refuses to propose. The evaluation checklist asks for "a deflection for questions the agent should not ask when the scenario tests over-asking" and warns "test only 'asks when unsure' and you get an agent that always asks."
Pattern: The holding-back side of an "act only when" clarification rule catches the refusal to act but not the unneeded question.

**Verifier:** R2-11 | Not real | Nit | The case is settled by the spec's own standard. §5.2 Interaction metrics computes precision for CO-S01, which has a User-knows set, and it is "reported beside pass/fail and ... never folded into the score" (l.1620). The simulated user already "deflects any other question" (§5.2, l.1612). The evaluation checklist says to report precision "to catch over-asking, but do not score on it, since a reasonable extra question is not a failure". No rule (CO-02 included) forbids asking when only one order is open, so nothing the contract needs is missing.

**Decision:** dropped (Nit) — status: dropped. Reason: Agreed: §5.2 Interaction metrics reports precision 'beside pass/fail and ... never folded into the score', the evaluation checklist says to report precision 'to catch over-asking, but do not score on it, since a reasonable extra question is not a failure', and no rule forbids asking when one order is open, so nothing the contract needs is missing.

## R2-12 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | G-01 / CO-06 / Failure handling (a request covering a second order)
Quote: "The agent cancels, refunds and hands off at most the one order the current request is about. Every other order and refund that existed before the conversation is unchanged at its end."
Evidence: The spec has no failure row, rule clause or scenario for a customer who asks to cancel two orders ("cancel both my orders"), or who asks for a second one after the first is done ("now cancel HG-10511 too"). The rules that touch this case disagree:
- G-01's first sentence scopes the limit to "the current request", so a new request could count as a new current request.
- G-01's second sentence, and §1 ("It may cancel that one order, issue its one refund and create one follow-up task for it"), forbid any second order in the conversation.
- CO-06 counts per conversation, not per order: "at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation". So after one retried cancellation, no CO-A2 is left for another order.
No input limits a conversation to one order. Known failure case 1 (review-packet.md, Round 2 Q4) is a customer with two open orders, and CO-S02 and CO-S03 set up exactly that customer. The use-case checklist's brainstorm list includes "the user goes silent or changes the request mid-way" (cockburn-checklist.md, Failure handling). As written, nothing tests whether the agent refuses the second order, cancels it, or what it tells the customer. An agent that cancels both orders, or silently ignores the second, passes every scenario.
Pattern: A limit on how many orders one conversation may touch is stated in Purpose and G-01 but has no failure row, no required message and no scenario. Its wording ("current request" against "in a conversation") gives two readings.

**Verifier:** R2-12 | Real | Important | Cannot refute. No failure row, scenario or dimension covers a request for a second order. G-01's "the one order the current request is about" (l.18) and CO-06's "in a conversation" (l.77) give two readings. G-01's second sentence and §1 do forbid a second order, but no scenario asserts it. Under the brief, a rule alone does not refute a Gap finding.

**Decision:** kept (Important) — status: open. Reason: Whether one conversation may cancel a second order turns on G-01 ('the one order the current request is about') and CO-06's per-conversation counts, both rule text, and no input decides it; open question for the user.

## R2-13 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | Failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; CO-S03 row 4 (fix for R1-09 is incomplete)
Quote: "| 4 | Yes, go ahead. Oh wait, no, I meant HG-10511, not that one. |"
Evidence: R1-09 named two cases of a confirming turn that also changes a term: "Yes, but put it on my Mastercard" and "Yes, cancel HG-10511 instead". The fix added only the order-change case (CO-S03 row 4). The row covers "the order or another proposal term", but no scenario has a confirming turn that changes the refund destination or amount. CO-S09 asks for another payment method in Turn 1, before any proposal exists. The outcome differs from CO-S03: the changed term cannot be granted, so the agent must restate the Visa proposal and ask again (CO-03, G-02). It must not cancel on the "Yes". An agent that reads "Yes, but put it on my Mastercard" as confirmation, then makes CO-A2 and refunds to Visa, breaks G-02 ("the exact proposal it executes") and still passes every scenario.
Pattern: A failure row that covers several terms is triggered by a scenario for only one of them. The term whose correct handling differs (a change that cannot be granted, inside the confirming turn) has no scenario.

**Verifier:** R2-13 | Real | Important | Cannot refute in full. CO-S03 row 4 (l.282) covers the order changed inside the confirming turn and answers only that part. Failure row l.99 ("the order or another proposal term in the confirming turn") has no scenario for a term that cannot be granted, such as "Yes, but put it on my Mastercard". CO-S09 puts that request in Turn 1, before any proposal, which is a different Initial state. CO-04 and G-02 settle the behavior, but no scenario asserts it.

**Decision:** kept (Important) — status: fixed

## R2-14 | Gap | Important | sources: coverage:F3

[coverage F3]
F3 | Gap | Important | CO-01 / failure row "the lookup shows the named order with status cancelled"; dimension "Already cancelled reported"; CO-S06 rows 3 and 4 (fix for R1-07 is incomplete)
Quote: "| Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, never says it cancelled the order or issued a refund in this conversation, and never says the order's refund is pending or issued unless the lookup showed it with that status. | CO-S06 |"
Evidence: CO-S06 rows 3 and 4 now hold a cancelled order whose refund is failed, or that has no refund, with no follow-up task. Final state says "No follow-up task exists" and the row forbids CO-A4. R1-07's pattern was that "no rule says what to tell the customer about them". The fix added only a ban on false claims. The cells that stay empty:
- The primary actor wants "to be told truthfully whether the order was cancelled and where the refund stands" (§2).
- No rule (CO-01 says only "tells the customer the order is already cancelled") and no dimension requires the agent to tell this customer that the refund failed or does not exist, or where to turn.
- The support team's interest, "every order whose refund is unfinished ... handed to it" (§2), is protected by no rule for this order. The row's "make no CO-A4" also contradicts that interest. The row follows the input ("reports that and changes nothing", Shared-understanding summary), so the stakeholder line or the rule has to give way.
An agent that says only "your order is already cancelled" to a customer whose money never came back passes rows 3 and 4. In production that customer is left with no refund, no task and no pointer to support.
Pattern: An infeasible-path scenario covers a record in a bad state (refund failed or missing), but the only check on it bans false claims. No rule or dimension requires the true status or a next step, and a stakeholder interest that names this case has no rule. This is an open question for the user: whether the agent tells the customer to contact support, or the CO-07 extension already proposed for R1-07 is applied.

**Verifier:** R2-14 | Real | Important | Cannot refute. "Already cancelled reported" (l.1630) only bans false claims. CO-01 requires only "tells the customer the order is already cancelled". No rule or dimension requires telling the customer, in CO-S06 rows 3 and 4, that the refund failed or does not exist, or where to turn. That leaves §2's "where the refund stands" and the support team's "every order whose refund is unfinished ... handed to it" unprotected. The row's "make no CO-A4" is backed by the input ("reports that and changes nothing"), so this is a conflict for the user to decide, not a spec slip.

**Decision:** kept (Important) — status: open. Reason: The input ('reports that and changes nothing') and §2's support-team interest conflict for an already-cancelled order with a failed or missing refund; only the user can decide what the agent tells that customer and whether it hands off.

## R2-15 | Gap | Nit | sources: coverage:F4

[coverage F4]
F4 | Gap | Nit | Failure row "CO-A2 | the order system did not answer the second CO-A2", branch "shipped or delivered"
Quote: "If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3."
Evidence: The other three branches of this row each have a scenario: cancelled in CO-S25, placed or processing in CO-S26, no answer in CO-S15. The shipped-or-delivered branch has none. Every scenario whose lookup follows a second unanswered CO-A2 holds the order unchanged or cancelled. The same branch in the first-unanswered-CO-A2 row is covered by CO-S11 row 2. This branch can be reached: the status flip only has to be tied to the second CO-A2, as CO-S11 ties it to the first. Its outcome differs from CO-S26's: the final status is shipped, and the agent must say the order shipped and that returns are a separate process. An agent that hands off with reason cancellation unknown here, or says only "not cancelled", is untested. The action outcome (no CO-A3, no CO-A4) matches CO-S26, so the risk sits mainly in the message, and I rate it Nit.
Pattern: A lookup-branching failure row with one branch that no scenario's Initial state reaches.

**Verifier:** R2-15 | Real | Nit | Cannot refute. CO-S11 row 2 tests the same shipped branch after the first unanswered CO-A2 (failure row l.103). That is a neighboring case with a different Initial state. No scenario's Initial state reaches the shipped branch of l.104, after the second unanswered CO-A2.

**Decision:** kept (Nit) — status: fixed

## R2-16 | Gap | Nit | sources: coverage:F5

[coverage F5]
F5 | Gap | Nit | §2 Offstage stakeholders / Appendix B; CO-A3 failure handling
Quote: "Harbor Goods, which wants ... no refund other than the order's total paid to the order's payment method"
Evidence: CO-A3 is `issue_refund(order_number)`. The agent passes no amount or payment method (Appendix A: "amount and payment method through the order"). The user stated "refund amount = order total paid; refund payment method = order's payment method" as "Rules, not fields" (review-packet.md, Round 2 Q3 answer). Only the order system can enforce that, yet Appendix B holds no guarantee for it. SG-01 covers only "at most one refund per order". CO-03 binds only the agent's proposal, and CO-08 asserts an outcome the agent cannot produce. The checklist calls for naming each supporting actor "with what it must receive from the agent and what it can fail to deliver", and lists "the supporting actor answers wrongly" in the brainstorm (cockburn-checklist.md). A CO-A3 result whose amount or payment method differs from the confirmed proposal is detectable from the tool result. No failure row covers it. G-03 governs only the refund status, so the agent may still report the confirmed $86.40 to Visa ending 4242.
Pattern: A stakeholder interest that only the supporting actor can enforce has no supporting-actor guarantee. The detectable "answered wrongly" result has no failure row.

Maps built with no empty cell:
- Stakeholder interests, apart from F3 and F5.
- Every tool outcome in the confirmed tool set: list_orders timeout; cancel_order cancelled, OrderNotCancellable, OrderNotFound and timeout (first and second); issue_refund pending or issued, failed, ProviderUnavailable and timeout (first and second); request_staff_followup timeout (first and second). The OrderNotCancelled and OrderNotFound questions stay open under R1-01.
- The "act only when" rules CO-01, CO-02, CO-04, CO-05, CO-06 (each retry clause), CO-07 and G-04: each has an acting and a holding-back scenario.
- Every required User-knows pair is used in its reference trajectory.
- Every tell-the-user clause has a rubric dimension. The refund-status message on success paths is left under R1-05.
- Known failure cases 1 to 3, the processing-to-shipped race and the round 3 Q3 and Q4 branches each have a scenario.
- Initial-state values: 2026-11-05 is a Thursday, "placed yesterday" resolves to HG-10511, all statuses are in the enum, refund amounts equal total paid, and CO-S11's status flip is tied to a state-changing call.

Not reported, already answered: R1-01, R1-02(b), R1-05 and R1-12.

**Verifier:** R2-16 | Real | Nit | Partly refuted. The missing-SG part is Style only: Appendix B says "no scenario grades them" (l.1671), so adding a guarantee changes no verdict. The missing failure row for a CO-A3 result whose amount or payment method differs from the proposal stands. Such a result is detectable (Appendix A l.1659 returns both fields), and cockburn-checklist.md's brainstorm lists "the supporting actor answers wrongly". G-03 covers only the refund's status.

**Decision:** kept (Nit) — status: open. Reason: Kept at Nit; the SG part is refuted as changing no verdict. What the agent does when CO-A3 returns a refund whose amount or payment method differs from the confirmed proposal is not in the inputs; open question for the user.
