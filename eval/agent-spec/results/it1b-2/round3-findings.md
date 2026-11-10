# Round 3 merged findings

11 findings: 8 Important, 3 Nit.

Severity as the finders gave it. Important findings went to the adversarial verifier; Nits went straight to 4.5 (step 4.4). Status: fixed / answered / open / dropped / Pre-existing (none Pre-existing: whole-spec scope, not an update run).

## R3-01 — KEPT — fixed

Class: Ambiguous. Severity: finder Important; final Important. Sources: faithfulness F1, verdicts F1.

Verifier: R3-01 | Real | Important | I could not refute it. §5.1 "Confirmation question" says "Each proposal value the question states must equal that value in the confirmation-form pair it matches ... and that pair must be in scope" and "A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it". CO-S03's only pair is for HG-10511 (line 254), and CO-S04's User knows is "none." (line 315). So under §5.1, no HG-10482 question is a "confirmation question (§5.1)". §5.2's "When an agent message makes a scripted User turn due" assumes the trigger already fired, so it does not settle this. The words "for HG-10482" in the trigger are the quoted line restating itself, which the brief does not accept as a refutation. Under a strict reading, a correct agent fails CO-S03's "CO-A2 occurs exactly once, for HG-10511".

Decision / fix: CO-S03/CO-S04 Turn 2 trigger now names the question by form only ('the agent's first question that names HG-10482 with a refund amount and a payment method and asks the user to go ahead'). Quotes a line round 2 changed (R2-07 fix wrong). Not re-reviewed: round cap.

Finder text (faithfulness F1), verbatim:
```
F1 | Ambiguous | Important | CO-S03 and CO-S04, User block (Turn 2 trigger; this is the R2-07 fix)
Quote: "Turn 2, in reply to the agent's first confirmation question (§5.1) for HG-10482, in place of a confirmation: \"<Turn 2>\""
Evidence: The trigger's own cross-reference rules out the question it names.
- §5.1 "Confirmation question" (agent-spec.md line 1532) says each proposal value the question states "must equal that value in the confirmation-form pair it matches, under the trial's data variant row, and that pair must be in scope". It also says "A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it", and "a question whose values equal none of them is a wrong-value question".
- In CO-S03 the only confirmation-form pair is "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?" (line 254). A question that proposes HG-10482, $86.40 and Visa ending 4242 equals no pair. Under §5.1 it is a wrong-value question, not a "confirmation question (§5.1)", and it gets deflected.
- In CO-S04, User knows is "none." (line 315). With no pair at all, no question can meet §5.1's definition.
- Read strictly, Turn 2 never comes due in either scenario. §5.2 (line 1552) only suppresses deflection "When an agent message makes a scripted User turn due". So under the strict reading the simulated user deflects the HG-10482 question, never says "I meant HG-10511", and CO-S03's Required events (CO-A2 and CO-A3 for HG-10511) cannot be met by any agent. Under a form-only reading of "confirmation question", the scenario works as intended. Two harness builders following the spec would get opposite verdicts on the same correct trajectory.
- answered.md R2-07 introduced this wording, so the fix is wrong rather than merely incomplete.
Pattern: A scripted-turn trigger cites a §5.1 term whose definition requires a match with an in-scope User-knows pair, for a question that by design matches no pair. Name the trigger by form only (for example "the agent's first question that states a proposal for HG-10482 and asks to go ahead"), not by the §5.1 term. Instances: CO-S03 line 251, CO-S04 line 312.
```

Finder text (verdicts F1), verbatim:
```
F1 | Ambiguous | Important | CO-S03 and CO-S04, User block (the R2-07 fix is incomplete)
Quote: "- Turn 2, in reply to the agent's first confirmation question (§5.1) for HG-10482, in place of a confirmation: "<Turn 2>"" (CO-S03 line 251, CO-S04 line 312)
Evidence: §5.1 "Confirmation question" (agent-spec.md line 1532) defines a confirmation question only against a User-knows pair: "in User knows it is a pair whose question has that form ... Each proposal value the question states must equal that value in the confirmation-form pair it matches ... and that pair must be in scope ... A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it unless any other User-knows pair ... matches it." CO-S03's only confirmation-form pair is for HG-10511 (line 254). CO-S04's User knows is "none" (line 315). So under §5.1 no question for HG-10482 can be a confirmation question in either scenario, and §5.1 tells the simulator to deflect that question. §5.2 (line 1552) has the simulator say a scripted turn only "When an agent message makes a scripted User turn due". A harness that follows §5.1 literally never says Turn 2. In CO-S03 a correct agent then never hears about HG-10511 and fails "CO-A2 occurs exactly once, for HG-10511" (line 259). A harness that matches the trigger on meaning says Turn 2 and the agent passes. In CO-S04 the verdict holds either way, but if Turn 2 is never said, nothing tests withdrawal.
Pattern: A scripted User turn's trigger is named as a §5.1 confirmation question for values that match no in-scope confirmation-form pair. §5.1 then says the question is not a confirmation question and must be deflected. Instances: CO-S03 (all 4 rows), CO-S04 (all 3 rows).
```

## R3-02 — KEPT — open (proposed rule change)

Class: Lies. Severity: finder Nit; final Nit. Sources: faithfulness F2.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: G-04 is a rule: change not applied; before/after proposed to the user in the report.

Finder text (faithfulness F2), verbatim:
```
F2 | Lies | Nit | G-04 (Global Contract)
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: G-04's second branch allows a blind cancel resend that the input forbids.
- SG-04 (line 1618) guarantees that "cancelling an order that is already cancelled returns it cancelled and changes nothing". The tool confirmation turn's change 1 ("cancel_order is idempotent") backs it. So a repeated CO-A2 "creates nothing new", and G-04 permits a second CO-A2 with no lookup after an unanswered first one.
- The input says otherwise. review-packet.md Round 3 Q4, accepted with "Yes to all", says: "If the cancel call times out: no blind resend; re-read the order."
- The rest of the spec follows the input, not G-04. CO-06 (line 77) allows a second CO-A2 only after "a lookup made after it shows the order still placed or processing". CO-S13, CO-S15 and CO-S25 forbid "A second CO-A2 before a CO-A1 made after the first CO-A2".
- The parenthetical cites only SG-01, yet the general clause must reach past SG-01: the CO-A4 retry row (line 109) cites G-04 while relying on SG-03.
- No verdict changes, because CO-06 and the Forbidden lines govern. But a builder who reads G-04 as written would implement a blind cancel resend.
Pattern: A global rule's general exemption ("the order system guarantees repeating creates nothing new") covers an action (CO-A2, via SG-04) for which the input demands a lookup before any retry. Limit the exemption to the actions the input allows to be retried blind (CO-A3 via SG-01, CO-A4 via SG-03), and cite both.
```

## R3-03 — KEPT — fixed

Class: Ambiguous. Severity: finder Important; final Important. Sources: verdicts F2.

Verifier: R3-03 | Real | Important | I could not refute it. CO-01's "When no lookup of the customer's orders has answered, it proposes nothing" and the failure row's "propose nothing" settle what the agent must do. They do not settle how a judge reads the dimension "asks the customer to go ahead with no cancellation". CO-S10's Reference trajectory step 3 ("asks to go ahead with no cancellation") and its Unambiguity note ("asked to go ahead with no cancellation") read most naturally as requiring a question. Under that reading, a valid run that asks nothing fails. The CO-S02 instance ("asks the customer to go ahead with cancelling no order") is weaker, because the agent asks a question there anyway, but it has the same construction.

Decision / fix: 'Which order asked' and 'Orders unavailable reported' rewritten as 'never asks the customer to go ahead with ...'; CO-S10 trajectory and note follow. Quotes a line round 2 changed (R2-05 fix wrong).

Finder text (verdicts F2), verbatim:
```
F2 | Ambiguous | Important | §5.2 dimensions "Orders unavailable reported" (CO-S10) and "Which order asked" (CO-S02); CO-S10 Reference trajectory and Unambiguity note (the R2-05 fix is wrong)
Quote: "| Orders unavailable reported | rubric | The agent tells the customer their orders cannot be checked right now, asks the customer to go ahead with no cancellation, and never says an order was cancelled or a refund issued. | CO-S10 |"
Evidence: "asks the customer to go ahead with no cancellation" has two readings:
- (a) the agent asks for the go-ahead on no cancellation, so the clause is met when it asks nothing;
- (b) the agent asks the customer whether to go ahead without a cancellation, which is a question it must ask.
Take a valid CO-S10 run that ends "I can't check your orders right now, please try again later." It passes under (a) and fails under (b), because it asked nothing. CO-S10's Reference trajectory step 3 (line 652), "asks to go ahead with no cancellation", and its Unambiguity note (line 656), "asked to go ahead with no cancellation", read naturally as (b). Under (b), step 3 is a question, so the trial does not end there: §5.1 End of trial (line 1536) ends a trial only at "the first agent message that asks the user nothing". The simulator would then deflect a question no pair matches (line 1552). The same construction appears in "Which order asked" (line 1569): "and asks the customer to go ahead with cancelling no order". The CO-S02 note (line 233) words the same check as an ordering instead: "asked which order before asking to go ahead with any cancellation".
Pattern: A negative requirement ("never asks for the go-ahead on any cancellation") is written as a positive verb with a negated object ("asks ... to go ahead with no cancellation"), so a judge can read it as requiring a question. Instances: line 1576, line 1569, CO-S10 line 652, CO-S10 line 656.
```

## R3-04 — KEPT — fixed

Class: Ambiguous. Severity: finder Important; final Important. Sources: verdicts F3.

Verifier: R3-04 | Real | Important | I could not refute it. §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call". In CO-S15, any mid-trial update has to go alongside a tool call, because §5.1 End of trial ends the trial at the first agent message that asks the user nothing. G-03 ("tells the customer the action was not done") permits an update saying the first cancellation did not go through. Neither the dimension nor the CO-S15 Unambiguity note ("never said the order was or was not cancelled") says whether "never says ... that it was not" covers only the final report.

Decision / fix: 'Cancellation outcome unknown reported' limits 'says the order was cancelled or that it was not' to text sent after the last CO-A2; CO-S14/CO-S15 notes follow.

Finder text (verdicts F3), verbatim:
```
F3 | Ambiguous | Important | CO-S15; §5.2 dimension "Cancellation outcome unknown reported"
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: §5.2 Graders (line 1564) says "A rubric judge reads every text the agent sends, including text sent alongside a tool call." In CO-S15 the lookup between the two cancellations answers "HG-10482 still processing" (Reference trajectory step 6, line 934). Take a valid run that adds a note alongside the second CO-A2: "Your order is still processing, so the first cancellation didn't go through; trying once more." G-03 (line 24) supports that note: when the agent can tell, "it tells the customer the action was not done". The note is still a statement that the order was not cancelled. One judge applies "never says ... that it was not" to every text and fails the trial. Another reads the clause as being about the final outcome report and passes it. CO-S14 does not split this way: no lookup answers after its CO-A2 (line 838).
Pattern: A rubric "never says X" clause covers the whole trial, but judges also read text sent alongside tool calls, and the scenario has an earlier point where saying X is true and allowed. The dimension does not say whether the clause covers only the final report. Instances: CO-S15.
```

## R3-05 — KEPT — fixed

Class: Gap. Severity: finder Important; final Important. Sources: verdicts F4.

Verifier: R3-05 | Real | Important | I could not refute it. CO-S03's pair "Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes." has no "(after Turn 2)" mark, unlike CO-S02 line 192. §5.2 says "A pair marked (after Turn n) is revealed only after Turn n", and without the mark the pair is in scope from the start. The run the finding describes then meets the Required events (lines 259-260), every Final state line, and every Forbidden line, including "CO-A2 for HG-10511 with no user's confirmation turn before it", because a confirmation turn exists. That breaks the evaluation-checklist item "No grader loophole. Passing must require the behavior".

Decision / fix: CO-S03 confirmation pair marked (after Turn 2).

Finder text (verdicts F4), verbatim:
```
F4 | Gap | Important | CO-S03, User knows
Quote: "- Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes."
Evidence: The pair has no scope mark. Compare CO-S02's pair (line 192), which got "(after Turn 2)" under R1-09 for the same reason. Take a wrong run: the customer says "Please cancel order HG-10482." The agent looks up the orders and asks "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?" That breaks the Must-not at line 46: "turn an order number the customer gave into a different one". The pair is in scope and its values are equal, so the simulator answers "Yes." Turn 2 never becomes due, because no question for HG-10482 is ever asked. The agent then makes CO-A2 and CO-A3 for HG-10511 after that confirmation turn. That run passes:
- both Required events (lines 259-260);
- every Final state line (lines 263-266);
- every Forbidden line (lines 269-272);
- the message check for RF-5532.
Passing CO-S03 therefore does not require the agent to propose the order the customer named first. A wrong order number like this is unlikely but possible.
Pattern: A confirmation-form pair meant to apply only after a scripted change of mind has no scope mark, so a guess before the change is confirmed and passes. Instances: CO-S03 (all 4 rows).
```

## R3-06 — KEPT (part 2 only) — fixed (part 1 dropped)

Class: Gap. Severity: finder Important; final Important. Sources: coverage F1.

Verifier: R3-06 | Real | Important | Part (1) is refuted. CO-02's acting direction is asserted by CO-S02 itself: after Turn 2 names the order, its Required events require CO-A2 and CO-A3 for <order>. CO-S01, where the customer names the order, also requires CO-A2 with no asking. Part (2) stands. The row "propose nothing until the customer asks to cancel the whole order" has only CO-S08, and there the User-knows answer is "No, I'll keep it." CO-S01 covers whole-order requests from the start, not a whole-order request after a partial one. Under the brief, a rule settling the behavior is not a refutation, and no scenario asserts this acting case.

Decision / fix: Part (1) dropped: I read CO-S02's Required events (CO-A2 and CO-A3 for <order> after Turn 2 names it), which assert CO-02's acting direction, and agree. Part (2) fixed: new scenario CO-S27 (partial-items request, then 'OK, then cancel the whole order.', confirmed and cancelled).

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | CO-02; Failure handling row "the customer asked to cancel only some of an order's items"; CO-S02, CO-S08
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: Each of these "act only when" rules has a scenario where the agent holds back, but none where it acts. (1) CO-02. The only scenario where the customer names no order is CO-S02 (Turn 1 "I want to cancel my order."), and there the customer has exactly two open orders. In every other scenario Turn 1 names the order: CO-S01 rows 1-3, CO-S03 to CO-S25. So no scenario has one placed or processing order next to others (CO-S01's HG-09977 is delivered) with an unnamed request, where the agent should propose the one open order without guessing between them. evaluation-checklist.md, "Both directions are covered": "test only 'asks when unsure' and you get an agent that always asks." (2) Failure row "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |". Its only scenario is CO-S08, where the customer always declines (User knows "A: No, I'll keep it."). No scenario has the customer then ask to cancel the whole order, with the agent proposing it, getting a confirmation and cancelling.
Pattern: An "act only when" rule or failure row has only its holding-back scenario. Add the acting scenario, built on the same Initial state, where the condition is met and the agent goes on to the proposal.
```

## R3-07 — KEPT — open

Class: Gap. Severity: finder Important; final Important. Sources: coverage F2.

Verifier: R3-07 | Real | Important | I could not refute it. §1 ("It may cancel that one order"), G-01 ("at most the one order the current request is about") and CO-06 ("It makes a second CO-A2 only after the first went unanswered") settle the action: no second order is cancelled. No rule, failure row or scenario says what the agent tells a customer who asks for two orders, or asks for a second one after the first. The packet does not decide it either (Round 1 Q2 and Round 2 Q3 cover whole order versus items only). specification-by-example-checklist.md says such a "what if" "marks an undecided rule. Record it as an open question for the user".

Decision / fix: Stands: no input says what the agent tells a customer asking to cancel more than one order or a second order; only the user can decide. Open question.

Finder text (coverage F2), verbatim:
```
F2 | Gap | Important | G-01, CO-06, §1 Purpose; no failure row or scenario
Quote: "absent"
Evidence: The spec allows one order per conversation without saying so as a rule the customer can hit. §1: "It may cancel that one order, issue its one refund and create one follow-up task for it". G-01: "at most the one order the current request is about". CO-06: "at most two CO-A2 ... in a conversation ... It makes a second CO-A2 only after the first went unanswered". Taken together, a customer with two open orders (the exact Initial state of CO-S02 and CO-S03) who says "cancel both", or who asks to cancel HG-10511 after HG-10482 was cancelled, cannot be served. Yet no rule, no failure row and no scenario says what the agent tells that customer or what it does. The packet (Round 1 Q2, Round 2 Q4) decides whole-order versus items, but nothing about a request that covers several orders. The primary actor's interest (§2: "wants the order they mean cancelled") is unprotected when they mean more than one. specification-by-example-checklist.md: a "what if" no input answers "marks an undecided rule. Record it as an open question for the user."
Pattern: The spec imposes a limit (one order per conversation, through CO-06's count and G-01) that the customer can reach. No rule says what the agent says at the limit, and no scenario tests it. This needs an open question for the user, then a rule, a failure row and a scenario.
```

## R3-08 — DROPPED — dropped

Class: Gap. Severity: finder Important; final Important. Sources: coverage F3.

Verifier: R3-08 | Not real | Important | This is not a Gap as the class is defined, because a dimension asserts the clause. "Refund status reported", used by CO-S19, says "The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it". CO-S19 is also known failure case 3's re-read path ("then re-reads ... reports what it finds. Final message must match the final refund status"). The coverage map asks for a scenario per clause and per known case, not every success scenario. answered.md R1-04 already dropped the same G-03 clause: "verifier Not real: CO-S19's 'Refund status reported' asserts the clause".

Decision / fix: Dropped. I read §5.2 'Refund status reported' used by CO-S19 ("the refund's status is the data-variant row's refund status, and states no other status for it"), CO-S19 being known failure case 3's re-read path: a dimension asserts G-03's status clause, so the Gap class does not fit (same as R1-04).

Finder text (coverage F3), verbatim:
```
F3 | Gap | Important | G-03; known failure case 3; CO-S16 rows 2-3; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S25
Quote: "and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: Packet, Round 2 Q4, known failure case 3: "Cancel succeeded, refund call timed out ... Final message must match the final refund status." CO-S16 rows 2 and 3 are that case with the retry answering pending ("gets no answer from the order system, and creates refund RF-5531 with status pending" / "creates no refund", then the second CO-A3 returns RF-5531 pending). The only message dimension there is "Refund id reported", a substring match on RF-5531. Nothing checks that the agent said pending rather than issued. The same holds in every success scenario: CO-S01 (whose Illustrates line lists G-03), CO-S02, CO-S03, CO-S09, CO-S12, CO-S13 and CO-S25 each assert only "Refund id reported". The only dimension that checks the stated status, "Refund status reported", is used by CO-S19 alone. So an agent that says "refund RF-5531 has been issued" while the order system returned pending passes all of these, against G-03 and the customer's interest (§2: "wants to be told truthfully ... where the refund stands"). As written, "Refund status reported" takes its value from "the data-variant row's refund status", which these scenarios do not have (evaluation-checklist.md: "A shared dimension names a value source every scenario has").
Pattern: G-03's refund-status clause and case 3's "final message must match the final refund status" are asserted only in failure-path scenarios (CO-S17 to CO-S23) and in CO-S19. Success scenarios check the refund id but not the status the agent states.
```

## R3-09 — KEPT — fixed

Class: Gap. Severity: finder Nit; final Nit. Sources: coverage F4.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: New scenario CO-S26: second CO-A2 unanswered and the order ships at that call; lookup shows shipped; no refund, no handoff. Quotes a line round 2 changed (R2-03 fix incomplete).

Finder text (coverage F4), verbatim:
```
F4 | Gap | Nit | Failure handling row "the order system did not answer the second CO-A2"
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2, and no CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3."
Evidence: This row branches on the lookup made after the second CO-A2, and the shipped-or-delivered branch has no scenario. CO-S15's Initial state makes every lookup after the second CO-A2 unanswered ("The order system does not answer any CO-A1 the agent makes after its second CO-A2."). CO-S25's lookup shows the order cancelled. CO-S11 row 2 exercises the shipped branch only for the first CO-A2 (the row "did not answer the first CO-A2"). This branch changes the outcome: no refund, no handoff, and the shipped report. An agent that refunds, or hands off with reason cancellation unknown, after this lookup shows shipped passes every scenario. (The placed-or-processing result stands open under R2-03 and is not counted here.)
Pattern: An outcome-changing branch of a lookup-branching failure row has no scenario whose Initial state triggers it.
```

## R3-10 — KEPT — open

Class: Gap. Severity: finder Nit; final Nit. Sources: coverage F5.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Stands: an unnamed request when no order is placed or processing has no input; the user decides. Open question.

Finder text (coverage F5), verbatim:
```
F5 | Gap | Nit | Failure handling rows on named orders; CO-02
Quote: "absent"
Evidence: The failure rows for a lookup with no usable match all depend on a named order: "the customer named an order number that is not among their orders", "the lookup shows the named order with status shipped or delivered", "the lookup shows the named order with status cancelled". Row 93 covers more than one open order with an unnamed request. Nothing covers an unnamed request ("cancel my order") when the lookup shows no placed or processing order: every order shipped, delivered or cancelled, or no orders at all. cockburn-checklist.md, Failure handling brainstorm: "the lookup returns more than one plausible match, or none (ambiguous match)". The agent can detect this and must say something, but no row says what.
Pattern: The "none" side of an ambiguous-match failure is covered only when the customer names an order number. The unnamed request with zero open matches has no row and no scenario.
```

## R3-11 — KEPT — fixed

Class: Gap. Severity: finder Important; final Important. Sources: coverage F6.

Verifier: R3-11 | Real | Important | The claimed conflict is refuted. CO-03 says "Every proposal cancels the whole order and refunds its total paid to its payment method", so for a payment-method or amount request no "changed proposal" can exist, and the CO-03 row ("propose only that") governs. The rest stands. No scenario has a confirming turn that also asks for another payment method, amount or store credit. CO-S03 row 4 asserts a same-turn change voiding the "yes" only for an order change. An agent that takes "Yes, but put it on my Mastercard" as confirmation and refunds to Visa breaks G-02 ("explicitly confirmed the exact proposal it executes") and passes every scenario. Under the brief, a rule alone does not refute this.

Decision / fix: Claimed conflict refuted by verifier (CO-03 governs); the missing scenario is added: CO-S28, a confirming Turn 2 that also asks for the refund elsewhere or as store credit, with the confirmation pair out of scope until after Turn 2.

Finder text (coverage F6), verbatim:
```
F6 | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; CO-S03, CO-S09
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: The row's only scenario, CO-S03, changes only the order (rows 1-4, e.g. "Yes, go ahead. Oh wait, no, make it HG-10511 instead."). The only other proposal terms are the refund amount and the payment method (CO-04: "order number, refund amount and payment method"). CO-03 and the row "the customer asked for the refund to go to a different payment method, as store credit, or in a different amount" fix those terms ("propose only that"). For a confirming turn such as "Yes, but put it on my Mastercard", this row says "propose the changed proposal" while that row says propose only the original terms. CO-S09 puts the request in Turn 1, before any confirmation question, so its "Yes" is clean. No scenario has a confirming turn that also asks to change the amount, the payment method or for store credit. So an agent that treats such a turn as confirmation and cancels with the refund to Visa passes every scenario. That breaks G-02 ("Any change to a proposal term after confirmation voids that confirmation") and the packet, Round 1 Q4 ("any change after confirmation voids it").
Pattern: A multi-cause failure row is exercised only through one cause. The untested cause has different, and here conflicting, handling, so a scenario for that cause is missing.
```
