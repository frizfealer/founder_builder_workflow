# Round 3 findings

10 merged findings (10 in the to-verify file): kept 7, dropped 3. Finder reports: round3-faithfulness.md, round3-verdicts.md, round3-coverage.md in eval/agent-spec/run-it2-3/.

## R3-01 | Lies | Important

Merged from: faithfulness F1.

### As reported by the faithfulness finder (F1)

F1 | Lies | Important | CO-01..CO-09 Failure handling, row "any | the customer changed the order or another proposal term ..."
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: CO-04 (agent-spec.md line 71) lists the proposal terms as "order number, refund amount and payment method". The order is the only one of those the customer can change. The inputs fix the other two: review-packet.md, Round 2 Q3 answer: "refund amount = order total paid; refund payment method = order's payment method". CO-03 (line 68) repeats this: when the customer asks "for a different amount, a different payment method or store credit, the agent ... proposes nothing else". The failure row two lines up (line 99) also says "propose only that". This row tells the agent to "propose the changed proposal" whenever the customer changes "another proposal term", so a customer who confirms and then says "actually, refund it to my Mastercard" gets a proposal of a Mastercard refund. That proposal cannot be carried out. CO-A3 takes only `order_number` (Appendix A, line 1764: `issue_refund(order_number)`, "amount and payment method through the order"), so the refund still goes to the order's own card. If the customer confirms the changed proposal, the agent runs an action the customer never confirmed, which breaks G-02 (line 21: "occurs only when the customer has explicitly confirmed the exact proposal it executes"). No scenario tests a refund-term change after confirmation (CO-S09 puts the request in Turn 1, before any proposal), so nothing catches it. An agent built from this row misbehaves in production.
Pattern: a failure row's required behavior covers a wider class ("another proposal term") than the inputs and the other rules allow. For part of that class, the inputs and CO-03 forbid what the row requires. Here, a change to the amount or payment method has to go to CO-03 handling (state the fixed term and propose only the order's total paid to the order's payment method), not "propose the changed proposal".

**Verifier:** `R3-01 | Real | Important | Could not refute. No spec line or input supports "propose the changed proposal" when the changed term is the amount or payment method: CO-03 ("Every proposal cancels the whole order and refunds its total paid to its payment method") and the row above it ("Tell the customer the refund is the order's total paid, to the order's payment method; propose only that.") contradict the row rather than support it, and G-02 ("Any change to a proposal term after confirmation voids that confirmation") supports only the voiding half. No scenario puts a refund-term change after a proposal (CO-S09 has it in Turn 1), so a builder following this row can propose a Mastercard refund that CO-A3 (`issue_refund(order_number)`) cannot carry out.`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R3-02 | Lies | Important

Merged from: faithfulness F2.

### As reported by the faithfulness finder (F2)

F2 | Lies | Important | CO-07; CO-S06 rows 2 and 3 (Forbidden, Unambiguity note)
Quote: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation."
Evidence: The fix for R2-10 (answered.md, Round 2) added CO-S06 row 2 (line 441: "Exactly one refund exists for HG-10405: RF-5486, ... status failed.") and row 3 (line 442: "No refund exists for HG-10412."), both for an order whose status is already cancelled. In both rows CO-07's condition holds as written: the order is cancelled, and the lookup shows its refund failed or missing, so it is "not shown pending or issued". CO-06 allows no CO-A3 for an order nobody proposed, so no retries remain. CO-07 then requires CO-A4 with reason refund not issued. CO-S06 forbids it ("CO-A4 at any point.", line 434), and its Unambiguity note (line 451) bases the ban on the input: "An already cancelled order: the agent reports that and changes nothing" (review-packet.md, Shared-understanding summary). That input contradicts CO-07 for an order that was cancelled before the conversation. Scope & Authority agrees with the input ("must not: cancel, refund or hand off any order other than the one the customer confirmed", line 43), and in CO-S06 the customer confirmed nothing. An agent that follows CO-07 fails CO-S06 rows 2 and 3, and the rule text gives the builder no way to tell this case apart. The §2 support-team interest ("wants every order whose refund is unfinished ... handed to it", line 11) is worded just as broadly, so the inputs alone do not settle whether a cancelled order with an unfinished refund should be handed off. Two fixes fit the input: narrow CO-07 to an order the agent cancelled (or confirmed) in this conversation, or ask the user whether such an order should be handed off.
Pattern: a fix adds data-variant rows that meet the trigger of a rule written for another flow (here, CO-07 is written for the agent's own cancel-then-refund flow). The scenario's Forbidden line then contradicts that rule's literal text, and the rule claims more than the input supports ("changes nothing").

**Verifier:** `R3-02 | Not real | Important | Scope & Authority, line 43: "The agent must not: cancel, refund or hand off any order other than the one the customer confirmed". In CO-S06 the customer confirmed nothing, so this must-not forbids CO-A4 there, and CO-07's "the order" is the order of the agent's own cancel-then-refund flow: its trigger "after the retries CO-06 allows" means the agent's own CO-A3 attempts, which CO-04 allows only under a confirmation ("The same confirmation authorizes CO-A3 for that order"), and Purpose (line 5) limits the handoff the same way ("create one follow-up task for it", meaning the order it cancels). Read this way CO-07 does not say an already cancelled order is handed off, and CO-S06's Forbidden "CO-A4 at any point." and its input-based Unambiguity note agree with the rule. (Closest call of the round: it rests on reading CO-07 together with line 43, which the finder considered and rejected.)`

**Decision:** dropped (Important). Verifier Not real, quoting Scope & Authority line 43 "The agent must not: cancel, refund or hand off any order other than the one the customer confirmed" and CO-07's "after the retries CO-06 allows". I read both and agree: read together, CO-07 covers the order of the agent's own confirmed flow, so CO-S06's ban on CO-A4 is consistent with the rules and the input.

**Status:** dropped

---

## R3-03 | Lies | Nit

Merged from: faithfulness F3.

### As reported by the faithfulness finder (F3)

F3 | Lies | Nit | CO-S08, Reference trajectory step 3 and User knows
Quote: "3. Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order."
Evidence: The failure row for this case (agent-spec.md line 98) reads: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order." The spec defines a proposal in "Which order asked first" (line 1740): "A proposal is a question asking the customer to go ahead with cancelling one particular order." Step 3, and the matching User-knows pair "Q: Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)" (line 519), have the agent ask exactly that kind of question before the customer has asked to cancel the whole order. The input says only "A request to cancel only some items: the agent says only the whole order can be cancelled" (review-packet.md, Shared-understanding summary). It does not mention an offer to cancel the whole order. The verdict does not change, because the pair is optional and no Forbidden line or dimension covers the offer.
Pattern: a reference trajectory, and a User-knows pair written to match it, show a step that the scenario's own failure row forbids.

**Verifier:** `R3-03 | Not real | Nit | CO-04: "CO-A2 occurs only after the customer confirms the full proposal: order number, refund amount and payment method", and CO-03: "Every proposal cancels the whole order and refunds its total paid to its payment method". A proposal states the refund amount and destination. Step 3 ("asks whether they want to cancel the whole order") and the optional pair "Would you like to cancel the whole order HG-10530 instead?" state neither, so they are not a proposal and the failure row's "propose nothing until the customer asks to cancel the whole order" is not broken. The definition the finding cites ("A proposal is a question asking the customer to go ahead with cancelling one particular order") sits in the "Which order asked first" row, which only CO-S02 uses. Also changes no verdict, as the finding says.`

**Decision:** kept (Nit). Verifier Not real (a proposal states amount and destination per CO-04). Kept: the spec's own definition in "Which order asked first" ("A proposal is a question asking the customer to go ahead with cancelling one particular order") fits the CO-S08 question, so I do not agree the quoted clause refutes the finding.

**Status:** fixed

---

## R3-04 | Ambiguous | Important

Merged from: verdicts F1.

### As reported by the verdicts finder (F1)

F1 | Ambiguous | Important | §5.2 Graders and rubric dimensions "Cancellation outcome unknown reported", "No wrong refund status", "Refund status reported", "Staff contact unconfirmed reported"; CO-07; CO-S15, CO-S16, CO-S19, CO-S23
Quote: "A rubric judge reads every text the agent sends, including text sent alongside a tool call."
Evidence: That line makes every "never says" or "states no other status" clause apply to the agent's narration while it is still working. The spec never says whether a statement that is true when made, about an attempt that has not finished, counts against the final-outcome clause. Instances where a plausible run says such a thing:
(1) CO-S15. After reference step 6 ("Agent → CO-A1 → HG-10482 still processing"), the failure row for the first unanswered CO-A2 says "If it shows the order placed or processing, make CO-A2 once more". An agent that sends the second CO-A2 with the text "The first try didn't go through; your order is still processing, so I'm trying again" says something true at that moment. "Cancellation outcome unknown reported" requires the agent "never says the order was cancelled or that it was not". One judge fails the run because it said the order was not cancelled. Another passes it, reading the clause as about the final outcome.
(2) CO-S16 rows 1 and 3, and CO-S19. When the agent makes the second CO-A3 after a ProviderUnavailable or a timeout, it may say "The refund didn't go through, retrying." "No wrong refund status" requires "The agent states no status for the refund other than the status it ends with" (pending). "Refund status reported" in CO-S19 requires that it "states no other status for it". Whether "didn't go through" states a status (failed, or not issued) is left to the judge. The R2-04 carve-out covers only describing the act ("saying the agent requested or issued the refund describes the action and states no status"), not a report that an attempt failed.
(3) CO-S23. An agent may send the first CO-A4 with the text "I'm passing this to our store staff, who will follow up with you." "Staff contact unconfirmed reported" requires it "never says ... that staff will follow up". CO-07 can be read two ways: "tells the customer store staff will follow up once the order system has created the task" either limits when the agent may say it (only after CO-A4 returned task_id) or describes what it says ("staff will follow up once the task exists"). On the first reading the CO-S23 run correctly fails, but the same narration then also breaks CO-07 in CO-S14, CO-S15, CO-S17, CO-S18, CO-S20, CO-S21 and CO-S22, and their dimensions pass it ("Refund not issued reported", "Cancellation outcome unknown reported", "Refund not confirmed reported", "Refund status unknown reported" only require that the statement is made). On the second reading the CO-S23 failure is unfair. The same text gets opposite verdicts depending on the scenario.
Pattern: A rubric judge that reads text sent mid-trial needs a stated rule for statements about an unfinished attempt: either the "never says" clauses cover only what the agent says about the final outcome, or interim statements count and the rule (CO-07's "once" clause) says when each statement may first be made. Every dimension that shares the clause should then read it the same way.

**Verifier:** `R3-04 | Real | Important | Could not refute. §5.2 "A rubric judge reads every text the agent sends, including text sent alongside a tool call" settles that mid-trial text is read, which removes the finder's "final outcome only" reading. But the problem the finding raises remains: no line says whether a true statement about an unfinished attempt ("still processing, so I'm trying again" in CO-S15; "the refund didn't go through, retrying" in CO-S16/CO-S19) counts as saying the order "was not" cancelled or as stating a refund status. The R2-04 carve-out ("saying the agent requested or issued the refund describes the action and states no status") covers describing the act, not reporting that an attempt failed. CO-07's "once the order system has created the task" can still be read either as a timing limit or as the content of the statement (CO-S23 vs the other handoff scenarios). Judges can reach different verdicts, or a correct agent can fail.`

**Decision:** kept (Important). Verifier Real; could not refute. Fix needs §5.2 fixed text or CO-07 rule text; open question for the user.

**Status:** open

---

## R3-05 | Ambiguous | Important

Merged from: verdicts F2.

### As reported by the verdicts finder (F2)

F2 | Ambiguous | Important | §5.1 "Agent message" and "Message-check window"; message check "Refund id reported" (§5.2); CO-08
Quote: "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one."
Evidence: CO-08 requires that "the agent tells the customer the refund id". The message check "Refund id reported" reads only agent messages ("A message check reads every agent message from the event that made its value available ... to the end of the trial"), so text sent alongside a tool call does not count as telling the customer. §5.2, though, says "A rubric judge reads every text the agent sends, including text sent alongside a tool call", so for every rubric dimension that text does count as said to the customer. Take a valid variation of CO-S01 row 1 that adds one read-only lookup. After CO-A3 returns RF-5531, the agent calls CO-A1 to check the order, with the text "Your refund RF-5531 for $86.40 to Visa ending 4242 is pending; let me confirm the order shows cancelled". Its final message is "Confirmed: HG-10482 is cancelled." The customer saw the id, but "Refund id reported" fails, so the scenario fails. Had the same alongside-call text said "issued", "No wrong refund status" would fail the run, treating that text as told to the customer. Either the text reaches the customer and the message check punishes a correct run, or it does not and the rubric judges punish text the customer never saw. Same exposure in every user of the check: CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25.
Pattern: Every grader, code or rubric, should share one definition of what the customer was told. Either message checks also read text sent alongside tool calls, or rubric judges read only agent messages.

**Verifier:** `R3-05 | Not real | Important | §5.1: "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one." and "A message check reads every agent message from the event that made its value available ... to the end of the trial." With §5.2's "A rubric judge reads every text the agent sends, including text sent alongside a tool call", every grader's input is defined exactly, so the finder's example run gets one computed verdict (message check "Refund id reported" fails; a wrong status in alongside text fails "No wrong refund status") whoever grades it. Two experts cannot reach different verdicts, so it is not Ambiguous. The two definitions also fit together: a required value must reach the customer in a yielded message, and a forbidden statement counts wherever it appears.`

**Decision:** dropped (Important). Verifier Not real, quoting §5.1 "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one." and §5.2 "A rubric judge reads every text the agent sends, including text sent alongside a tool call". I read both and agree: each grader's input is defined exactly, so the example run gets one computed verdict; it is not Ambiguous.

**Status:** dropped

---

## R3-06 | Ambiguous | Important

Merged from: verdicts F3.

### As reported by the verdicts finder (F3)

F3 | Ambiguous | Important | §5.2 rubric dimensions "Refund not issued reported" and "Staff contact unconfirmed reported"; CO-S17 row 1, CO-S22, CO-S23
Quote: "The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued (pending and issued read as defined for No wrong refund status)."
Evidence: In CO-S17 row 1, CO-S22 and CO-S23, CO-A3 returns the refund with status failed (reference trajectories: "Agent → CO-A3 (HG-10482) → refund RF-5531, failed."). The CO-A4 second-unanswered failure row even tells the agent to say "what it knows of the order and the refund under G-03", which is that the refund failed. So "Your order is cancelled, but refund RF-5531 failed; store staff will follow up" is a likely truthful report. Whether it meets "the refund has not been issued" is judgment. The sibling dimension, rewritten by the R2-06 fix, lists "failed" explicitly: "Refund not confirmed reported": "that the refund is not confirmed (saying it is not confirmed yet, has not been issued, or failed each meets this)". "Refund not issued reported" (CO-S17, CO-S18, CO-S22) and "Staff contact unconfirmed reported" (CO-S23, "the refund has not been issued") have no such list. A judge comparing the two definitions may conclude that "failed" is accepted in one and not the other, while another judge reads "failed" as entailing "not issued" (issued = "the money has been sent"). The verdict on the same report differs by judge.
Pattern: When several dimensions require the same proposition about the refund, each must say which truthful wordings meet it, or none should. Here that means accepting "failed" wherever the tool result was a failed refund.

**Verifier:** `R3-06 | Not real | Important | The dimension itself defines the term: "Refund not issued reported" says "(pending and issued read as defined for No wrong refund status)", and that definition reads "issued when the money has been sent". A report that the refund failed says the money was not sent, so under the dimension's own definition it says the refund has not been issued. "Staff contact unconfirmed reported" carries the same parenthetical. The explicit list in "Refund not confirmed reported" was needed because "not confirmed yet" is a different proposition (R2-06); it does not make "failed" fail "has not been issued" here.`

**Decision:** dropped (Important). Verifier Not real, quoting the dimension's own "(pending and issued read as defined for No wrong refund status)" and that definition "issued when the money has been sent". I read them and agree: saying the refund failed says the money was not sent, which meets "has not been issued".

**Status:** dropped

---

## R3-07 | Untestable | Nit

Merged from: verdicts F4.

### As reported by the verdicts finder (F4)

F4 | Untestable | Nit | §5.1 "End of trial"; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Both end conditions are counted in agent messages, and reads are unbounded: Appendix A says "The agent may repeat CO-A1 without limit; only commit calls are bounded", and the input says "Reads may be retried on timeout without limit" (review-packet.md, tool confirmation turn, change 4). CO-S10 sets "The order system does not answer any CO-A1 the agent makes", and CO-S14, CO-S15 and CO-S21 set "The order system does not answer any CO-A1 the agent makes after its ...". An agent that retries list_orders on every timeout never yields a message, so neither end condition is ever met. The harness must invent its own cut-off before it can grade the trial. Every such run fails anyway (no report, or no CO-A4), so no verdict changes.
Pattern: When a scenario makes a tool fail on every call and the spec allows unlimited retries of that call, the end-of-trial rule must also bound tool calls (or the time within one agent turn), and say how a trial cut off that way is scored.

**Verifier:** `R3-07 | Real | Nit | Could not refute. §5.1 bounds a trial only by agent messages ("at the agent's 12th message (the message cap)"), and Appendix A ("The agent may repeat CO-A1 without limit") and the input ("Reads may be retried on timeout without limit") leave tool calls within a turn unbounded, while CO-S10 ("does not answer any CO-A1 the agent makes") and CO-S14/S15/S21 make every later read time out. No line gives the harness a cut-off or says how a cut-off trial is scored. Changes no verdict and no agent behavior, but it is a missing termination bound the harness needs, not wording or preference, so I do not class it Style only.`

**Decision:** kept (Nit). Verifier Real (Nit). Fix belongs in §5.1 fixed text, which step 4 does not edit; open.

**Status:** open

---

## R3-08 | Gap | Important

Merged from: coverage F1.

### As reported by the coverage finder (F1)

F1 | Gap | Important | CO-02 / Failure handling; Scenarios
Quote: "absent"
Evidence: CO-02 asks which order only "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean". The Failure handling table covers an unnamed request when more than one order is open ("more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean") and when none is open ("the customer named no order, and none of their orders has status placed or processing", added for R2-11). Nothing covers the third count: the customer names no order and exactly one order is open, for example beside a delivered or cancelled order. Both scenarios with the unnamed Turn 1 "I want to cancel my order." have zero open orders (CO-S28: "HG-09977, status delivered ... HG-10399, status cancelled"; "The customer has no orders.") or two (CO-S02: HG-10482 processing and HG-10511 placed). In every row of CO-S01, the one scenario with a single open order next to a non-open one (HG-09977 delivered), Turn 1 names the open order ("Please cancel order HG-10482.", "... cancel HG-10511 ...", "cancel my order hg-10530"). references/cockburn-checklist.md, Failure handling brainstorm: "the lookup returns more than one plausible match, or none (ambiguous match)". references/evaluation-checklist.md, "Both directions are covered": CO-02's ask-which clause has an acting scenario (CO-S02) but no scenario where it must hold back, that is, where the agent must propose the one open order without asking which. That case is the most common form of the request, and the unnamed form of known failure case 1 (review-packet.md, Round 2 Q4: "customer has two open orders and says 'cancel my order'"). Each of these agents passes every scenario: one that answers "cancel my order" by picking the most recent order (HG-09977, delivered) and saying it cannot be cancelled while HG-10482 is open; one that demands an order number and stops when the simulated user deflects; one that asks which order when only one can be cancelled.
Pattern: For a request that names no record, each count of eligible records the lookup can return (none, one, more than one) needs a failure row or a rule clause and a scenario whose Initial state has that count. The "one" count also needs non-eligible records beside it, so that picking the wrong record can be seen.

**Verifier:** `R3-08 | Real | Important | Could not refute. CO-02's ask-which clause applies only "When more than one of the customer's orders has status placed or processing"; no failure row covers an unnamed request with exactly one open order, and no scenario has that Initial state (CO-S02 has two open orders, CO-S28 none, every CO-S01 row names the order in Turn 1). CO-01 allows proposing the one open order, but a rule that settles the behavior does not refute a Gap when no scenario or dimension asserts it, and evaluation-checklist "Both directions are covered" requires the holding-back scenario for CO-02.`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R3-09 | Gap | Important

Merged from: coverage F2.

### As reported by the coverage finder (F2)

F2 | Gap | Important | Failure handling, rows that branch on an unanswered lookup; CO-01; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: review-packet.md, Tool confirmation turn, the user's change 4: "Reads may be retried on timeout without limit; only commit calls are bounded." Appendix A: "The agent may repeat CO-A1 without limit". No failure row has a branch for a lookup that goes unanswered and then answers when the agent retries it, and no scenario's Initial state makes one lookup fail and a later one answer. Every lookup-outage scenario fails every read: CO-S10 "The order system does not answer any CO-A1 the agent makes."; CO-S14 "does not answer any CO-A1 the agent makes after its first CO-A2"; CO-S15 "... after its second CO-A2"; CO-S21 "... after its second CO-A3". The rows read as if one unanswered lookup settles the outcome:
(1) the row quoted above: its condition stays true after a retried lookup answers, so it reads as "propose nothing" even then. CO-01 instead says "When no lookup of the customer's orders has answered, it proposes nothing", which allows a proposal once any lookup has answered;
(2) the first-CO-A2-unanswered row: "Make no CO-A2 or CO-A3 until a lookup made after it answers. ... If the lookup does not answer, tell the customer it is not known whether the order was cancelled ... and make CO-A4 with reason cancellation unknown.";
(3) the second-CO-A2-unanswered row: the same "If the lookup does not answer ..." branch;
(4) the second-CO-A3-unanswered row: "If the lookup does not answer, make CO-A4 with reason refund status unknown".
None of these says whether the agent may or must retry the read before acting on "no answer", or how many tries count as "does not answer". Two runs can both pass every scenario. In the first, the agent gives up after one read timeout. It tells the customer their orders cannot be checked, or hands a cancelled order to staff with reason cancellation unknown when one more read would have shown it cancelled and let it refund. In the second, the agent retries and finishes the cancellation. Two domain experts could grade the second run differently against row (1). references/cockburn-checklist.md: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer. A missing branch is the else-branch a coder will invent."
Pattern: Every failure-row branch on "the lookup does not answer" must say whether reads are retried before that branch applies, consistent with the input that reads may be retried without limit. At least one scenario must make a lookup go unanswered and then answer on a retry, so that the retry-then-proceed path has a verdict.

**Verifier:** `R3-09 | Real | Important | Could not refute. CO-01 ("When no lookup of the customer's orders has answered, it proposes nothing") and Appendix A ("The agent may repeat CO-A1 without limit") allow retry-then-proceed, but the first failure row's condition ("did not answer a lookup ... made before any CO-A2") stays true after a later lookup answers, and the "If the lookup does not answer" branches in the CO-A2 and second-CO-A3 rows do not say whether reads are retried first. No scenario makes a lookup time out and then answer (CO-S10, S14, S15, S21 fail every later read), so no scenario or dimension asserts the path. cockburn-checklist.md line 74 ("A failure row that branches on a lookup covers every result of the lookup ... and no answer") supports the finding.`

**Decision:** kept (Important). Verifier Real; could not refute. Whether a read must be retried before acting on no answer, and how many times, only the user can decide; open question.

**Status:** open

---

## R3-10 | Gap | Nit

Merged from: coverage F3.

### As reported by the coverage finder (F3)

F3 | Gap | Nit | CO-03; §5.2 dimensions "Whole order only explained", "Refund terms explained"; CO-S08, CO-S09
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: As written, CO-03 requires both statements whatever the customer asked for. The failure rows split them: a partial-items request gets "Tell the customer only the whole order can be cancelled"; a different-refund request gets "Tell the customer the refund is the order's total paid, to the order's payment method". The dimensions follow the rows, not the rule. "Whole order only explained" (CO-S08) asserts only "only the whole order can be cancelled". "Refund terms explained" (CO-S09) asserts only "for the refund term the customer asked to change". The reference trajectories give one statement each: CO-S08 step 3 "Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order."; CO-S09 step 3 "Agent tells the customer the refund can only go to the order's payment method, states the proposal ...". So no scenario asserts CO-03's second clause in CO-S08 or its first clause in CO-S09, and both reference trajectories break the rule as written. references/verification.md, Gap: "a rule that requires the agent to tell the user something, with no scenario asserting it." No verdict changes as the scenarios stand: the dimensions follow the rows, and the CO-A2 checks do not depend on what is said.
Pattern: When a rule's "tells the customer" clause lists several statements across several causes, either the rule assigns each statement to its cause, as the failure rows do, or every scenario for each cause asserts every statement. The rule, the failure rows, the dimensions and the reference trajectories must agree on which statements each cause requires.

**Verifier:** `R3-10 | Not real | Nit | The Gap class is "a rule that requires the agent to tell the user something, with no scenario asserting it". Each of CO-03's statements has an asserting scenario: "Whole order only explained" (CO-S08: "only the whole order can be cancelled") and "Refund terms explained" (CO-S09: "the refund goes to the order's payment method ... or that it is the order's total paid"). The failure rows assign each statement to its cause ("Tell the customer only the whole order can be cancelled" and "Tell the customer the refund is the order's total paid, to the order's payment method"). CO-S09's reference step 3 does give both statements, since the proposal it states ("cancel HG-10482, refund $86.40 to Visa ending 4242") names the whole order and its total paid. Changes no verdict, as the finding says.`

**Decision:** kept (Nit). Verifier Not real (each statement has an asserting scenario; the rows assign statements). Kept: CO-03's text requires both statements for the partial-items cause and CO-S08 asserts only one, so the refutation covers each statement, not each cause. The fix changes CO-03's rule text, so it is a proposed rule change for the user.

**Status:** open

---
