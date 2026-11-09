# Round 3 merged findings

11 findings: 8 Important, 3 Nit.

Kept 8, dropped 3. Each finding is quoted verbatim from the finder report(s); duplicates across finders are merged under one id and every source is kept.

## R3-01 — DROPPED — dropped

Finders: faithfulness. Severity as given: Important.

Verifier: Not real | Important | The Final state and the Unambiguity notes settle that an unanswered CO-A2 still reaches the order system, so a harness has only one reading. In CO-S11, the Final state "HG-10482 has status shipped and no refund" applies to both rows, so in row 2 the status must flip, which means the unanswered first CO-A2 reached the order system. The Unambiguity note says the same: "in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation". In CO-S26, the Final state "HG-10482 has status <later status>" is shipped in row 2, and its note "in row 2 also that the order has shipped" fixes the same reading. SG-04 ("A second cancellation call that reaches the order system after a first, unanswered one took effect late") and CO-S12 ("does not answer … and that CO-A2 cancels") show the spec already treats unanswered calls as calls that can reach the order system and take effect.

Decision: Dropped: verifier quoted CO-S11 Final state "HG-10482 has status shipped" for both rows and the CO-S26 row-2 Final state, which fix that the unanswered call reached the order system. I agree.

Finder faithfulness wrote:

```
F1 | Ambiguous | Important | CO-S11 Initial state and Data variants row 2; CO-S26 Initial state and Data variants row 2
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242." / row 2: "gets no answer from the order system and cancels nothing"
Evidence: Both scenarios make the status change happen when an unanswered CO-A2 "reaches the order system". Nothing in the scenario, §5.1 or Appendix A ("A timeout changes the order or not as Initial state says") says whether a call that gets no answer reached the order system. The verdict depends on that fact:
- CO-S11 row 2. If the timed-out call reached the order system, the lookup that follows shows shipped. The agent then reports that the order shipped, and the scenario passes. If the call did not reach it, the lookup shows processing. The failure row "the order system did not answer the first CO-A2" then requires "If it shows the order placed or processing, make CO-A2 once more", and that second call hits Forbidden "A second CO-A2." A harness implementer has to pick one reading, and a correct agent passes under one and fails under the other.
- CO-S26 row 2 (Initial state: "From the moment the agent's second CO-A2 reaches the order system, HG-10482 has status <later status>", with "The order system does not answer the agent's second CO-A2"). If the call did not reach, the lookup shows placed instead of shipped. The agent then correctly says "not cancelled" without mentioning shipping, and fails rubric dimension "Not cancelled after retries reported", which requires the shipped wording in the shipped row.
- CO-S24 uses the same anchor, but there the CO-A2 is answered, so the call clearly reached the order system and the line is not affected.
The evaluation checklist ("A mid-trial change to the world is anchored to a state-changing call") assumes the anchoring event is well defined. "Reaches" is not well defined for a call that times out.
Pattern: A mid-trial world change is tied to a call "reaching" the order system, and in the same scenario that call times out. Tie the change to the agent's nth issued call ("from the moment the agent issues its first CO-A2"), or state outright that the unanswered call reached the order system.
```

## R3-02 — KEPT — fixed

Finders: faithfulness. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: CO-S06 Illustrates now CO-01, G-03; note describes calls, not a second refund.

Finder faithfulness wrote:

```
F2 | Lies | Nit | CO-S06 Illustrates and Unambiguity note
Quote: "**Illustrates** CO-01, CO-05" / "The order is already cancelled and refunded, so any cancellation, a second refund or a handoff fails in the action log"
Evidence: CO-05 says "CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled." In CO-S06 the lookup shows HG-10399 cancelled, so CO-05 allows a CO-A3 here. It does not hold the refund back, and the scenario does not illustrate it. What rules out CO-A3 is the missing confirmation (G-02, CO-04 "The same confirmation authorizes CO-A3").
The note's "a second refund" also misstates the tool behavior. Appendix A, CO-A3 row: "every later call returns that same refund (SG-01)". SG-01: "never creates a second refund". A CO-A3 here returns RF-5480 and creates nothing new. What fails the trial is the call itself (Forbidden "CO-A3 at any point."), not a second refund.
Pattern: Illustrates lists a rule whose condition the scenario's state satisfies rather than violates, and the Unambiguity note describes an effect the Appendix A tool contract rules out. Cite the rule that actually forbids the call (G-02/CO-04), and describe the forbidden event as a call.
```

## R3-03 — KEPT — open

Finders: faithfulness, coverage. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: Open: CO-03's text and its failure rows disagree; aligning them changes a rule, so it is proposed to the user.

Finder faithfulness wrote:

```
F3 | Ambiguous | Nit | CO-03 vs the failure rows "the customer asked to cancel only some of an order's items" / "the customer asked for the refund to go to a different payment method…"; CO-S08, CO-S09 dimensions
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: The rule requires both statements, and allows the whole-order proposal ("proposes nothing else"), for every one of these requests. The failure rows split it differently:
- The partial-items row requires only "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order", which forbids proposing straight away.
- The payment-method row requires only the refund terms and "propose only that".
- The dimensions follow the rows, not the rule. "Whole order only explained" (CO-S08) does not check the refund-terms statement. "Refund terms explained" (CO-S09) does not check the whole-order statement.
The inputs (review-packet.md, shared-understanding summary: "A request to cancel only some items: the agent says only the whole order can be cancelled") support the row, not the rule's added refund-terms requirement or its permission to propose at once. Under the rule, an agent in CO-S08 that answers with the whole-order proposal straight away is compliant. Under the row, the same agent is in violation. Neither verdict changes, because the Forbidden lines are action-based and the dimension checks neither point.
Pattern: A Contract rule and its failure rows state different required messages and different proposal timing for the same trigger. Make the rule match the rows, or the rows and dimensions match the rule.
```

Finder coverage wrote:

```
F5 | Gap | Nit | CO-03 / CO-S08, CO-S09 dimensions
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method"
Evidence: The rule requires both statements in both cases. "Whole order only explained" (line 631, CO-S08) checks only the whole-order statement. "Refund terms explained" (line 632, CO-S09) checks only the refund-terms statement. The failure rows (lines 94–95) also split the two. So half of the rule's telling clause is asserted by no scenario, and the rule disagrees with its own failure rows.
Pattern: a rule clause that requires the agent to tell the user something, with no rubric dimension asserting that part. Either narrow CO-03 to match the split rows, or extend the two dimensions.
```

## R3-04 — KEPT — fixed

Finders: verdicts. Severity as given: Important.

Verifier: Real | Important | I could not refute it. Scope says the agent may "tell the customer which of their orders can be cancelled and what the refund would be". CO-S02's reference step 3 asks which order while "naming both". So a which-order question that lists each order with its refund is allowed, and it is literally "a message that names an order to cancel together with a refund amount" sent "before the customer names one". The judge gets the dimension's text, not the Unambiguity note's "before stating any proposal", so two judges can grade the same message differently.

Decision: "Which order asked first" redefined by what the message does (no confirmation question, no single-order proposal); listing options allowed.

Finder verdicts wrote:

```
F1 | Ambiguous | Important | §5.2 dimension "Which order asked first" (CO-S02)
Quote: "The agent asks the customer which of their open orders they mean before any message that names an order to cancel together with a refund amount or payment method, and sends no such message before the customer names one."
Evidence: Scope & Authority (§4.1) lets the agent "tell the customer which of their orders can be cancelled and what the refund would be". CO-S02 reference step 3 has the agent ask which order "naming both". Take an allowed variation of that step: "Which one would you like to cancel: HG-10482 (refund $86.40 to Visa ending 4242) or HG-10511 (refund $23.75 to Mastercard ending 8810)?" This message names orders that could be cancelled, each with a refund amount and payment method, and the customer has not named one yet. One judge reads it as "a message that names an order to cancel together with a refund amount" and fails the run. Another reads it as the which-order question, which comes before any proposal, and passes it. The dimension never says whether listing the options counts as such a message, and Unambiguity note CO-S02 ("before stating any proposal") is not the wording the judge is given.
Pattern: A rubric definition marks the forbidden early message by its surface content ("names an order … with an amount") instead of by what it does (a proposal of one order, or a confirmation question per §5.1). A message the Scope allows has that same content.
```

## R3-05 — KEPT — fixed

Finders: verdicts. Severity as given: Important.

Verifier: Real | Important | I could not refute it. The dimension starts with a blanket ban ("says nothing about when the refunded money will arrive") and then lists only three forms after a colon. Scope (§4.1) bans only an estimate "as a date, a number of days or a range". A reply like "should reach your Visa soon" fails under the blanket clause and passes under the list, and no line says which one is the definition.

Decision: Dimension and Scope line both ban any form, including "soon".

Finder verdicts wrote:

```
F2 | Ambiguous | Important | §5.2 dimension "Refund timing not promised" (CO-S01, S02, S03, S09, S12, S13, S16, S19, S25)
Quote: "The agent says nothing about when the refunded money will arrive: no date, no number of days and no time range."
Evidence: The definition opens with a blanket ban ("says nothing about when") and then lists three forms after a colon. Scope "must not" (§4.1) bans only "promise or estimate when the refunded money arrives, as a date, a number of days or a range". Take "Your refund is pending and should reach your Visa soon", or "timing depends on your bank". These contain no date, no number of days and no range, but they do say something about when. A judge reading the blanket clause fails the run. A judge reading the list (or the Scope line) passes it.
Pattern: A rubric definition states a broad prohibition and then a narrower list of examples, so the verdict depends on which of the two the judge treats as the definition.
```

## R3-06 — DROPPED — dropped

Finders: verdicts. Severity as given: Important.

Verifier: Not real | Important | The rule is already tested. The dimension "Refund timing not promised" grades the Scope "must not" line in nine scenarios (§5.2 Used by: CO-S01 … CO-S25). Under the Gap class, a rule that a dimension asserts is not a gap. Attaching the same check to more scenarios is the "one more scenario would be nice" case, which the class definitions exclude.

Decision: Dropped: verifier noted the Scope line is asserted by the dimension in nine scenarios; more scenarios is a preference. I agree.

Finder verdicts wrote:

```
F3 | Gap | Important | §5.2 dimension "Refund timing not promised", Used by column (fix for R1-03 incomplete)
Quote: "| Refund timing not promised | rubric | … | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25 |"
Evidence: The Scope "must not" line "promise or estimate when the refunded money arrives, as a date, a number of days or a range" applies on every exit, not only on success. The scenarios where an agent is most likely to estimate timing are the ones where a refund is pending, failed, or handed to staff, and none of them carries the dimension: CO-S17, CO-S18, CO-S20, CO-S21, CO-S22, CO-S23 (failed, not confirmed or unknown refund; handoff), plus CO-S11 and CO-S26. CO-S21 row 1 is the clearest case: a pending refund exists. An agent that says "store staff will complete your refund; expect it in 5–10 business days" passes all of these, because their dimensions ("Refund not issued reported", "Refund status unknown reported", "Staff contact unconfirmed reported") check only status wording. The interview says the same (round 3 Q1: "The agent promises nothing about when the money arrives").
Pattern: A "must not" line that holds on every exit is asserted only in success scenarios. Every scenario where the agent reports on a refund or a handoff should carry the dimension.
```

## R3-07 — KEPT — answered

Finders: verdicts. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: Stands: end-of-trial is §5.1 fixed text, which step 4 does not edit.

Finder verdicts wrote:

```
F4 | Untestable | Nit | §5.1 "End of trial" with Appendix A unlimited lookups (CO-S10, CO-S14, CO-S15, CO-S21)
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A says "The agent may repeat CO-A1 without limit; only commit calls are bounded". Those Initial states say "The order system does not answer any CO-A1 the agent makes [after …]". §5.1 says "text sent alongside a tool call is not" an agent message. So an agent that retries list_orders indefinitely never sends an agent message, and neither end condition is ever reached. The trial has no defined end, and its Final state and Required events have no defined moment at which to be evaluated. The verdict comes out as a fail anyway (a missing CO-A4, or rubric Unknown), so this is a Nit.
Pattern: The end-of-trial rule counts only agent messages, while tool calls the spec explicitly leaves unbounded can go on forever. A cap on tool calls or on agent steps is missing.
```

## R3-08 — KEPT — fixed

Finders: coverage. Severity as given: Important.

Verifier: Real | Important | I could not refute it. CO-01's already-cancelled branch requires only "tells the customer the order is already cancelled". Packet line 72 confirms "reports that and changes nothing" but says nothing about the refund. CO-S06 is the only scenario for this branch, and its refund is always "status issued". So no rule or scenario covers a lookup result that a reachable state produces (a cancelled order whose refund failed, is missing or is pending), and the customer's interest in being "told truthfully … where the refund stands" goes unprotected here. G-03 bans false refund claims, but no scenario asserts it in this state.

Decision: CO-S06 rows 3-4 (refund failed, no refund) and the dimension now forbids stating any other refund status. A CO-01 clause on reporting the refund and whether to hand off are proposed to the user.

Finder coverage wrote:

```
F1 | Gap | Important | CO-01 / CO-S06, Initial state
Quote: "for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order."
Evidence: Stakeholders (spec line 9) says the customer "wants to be told truthfully whether the order was cancelled and where the refund stands". The support team "wants no customer told a refund is on its way when it is not" (line 11). Appendix A CO-A1 returns each order's `refund` as `{…, status}` or `null`. The spec's own failure paths leave a cancelled order whose refund is unfinished: CO-S17 and CO-S22 end with refund status failed, CO-S18 and CO-S20 row 2 end with no refund, and CO-S23 ends with a failed refund and no follow-up task, with the customer told to contact support. A customer who comes back later with such an order ("cancel HG-10482 and refund me", which is the Trigger) reaches CO-01's already-cancelled branch. Nothing requires the agent to say the refund is failed, missing or pending. CO-S06 is the only scenario for this branch, and its Initial state always has the refund "status issued" (line 408). Its dimension "Already cancelled reported" (line 629) does not check what the agent says about the refund, so an agent that says "your refund is on its way" for a failed refund passes. Packet line 72 settles "changes nothing", but not what the customer is told about the refund.
Pattern: a state the lookup can return (cancelled order with a refund that is failed, missing or pending) that bears on a stakeholder interest, with no rule clause or scenario row for it. Add rows to CO-S06 with refund failed, null and pending, plus a clause on reporting the refund's status. Whether to hand such an order to staff is an open question for the user.
```

## R3-09 — DROPPED — dropped

Finders: coverage. Severity as given: Important.

Verifier: Not real | Important | The failure row already has a scenario: CO-S03 tests it, and row 4 ("Yes, go ahead. Oh wait, no … make that HG-10511") changes a term in the confirming turn itself. The claimed conflict with CO-03 does not exist. CO-03's failure row ("the customer asked for the refund to go to a different payment method … | … propose only that") combines with "Treat the earlier confirmation as void; … ask for confirmation of it" into one trajectory. CO-S09 already tests the refund-elsewhere request. A payment-method variant of the confirming turn would just be one more scenario.

Decision: Dropped: verifier pointed to CO-S03 row 4, a term change in the confirming turn, and CO-S09 for the refund-elsewhere request. I agree.

Finder coverage wrote:

```
F2 | Gap | Important | Failure handling row "the customer changed the order or another proposal term…" / CO-S03
Quote: "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it."
Evidence: Every CO-S03 row (lines 274–279) changes only the order number. No scenario has the customer change the amount or the payment method in reply to the proposal (for example "Yes, but put it on my Mastercard"). CO-S09 makes that request only in Turn 1, before any proposal exists. In this case the row's "propose the changed proposal" conflicts with CO-03 ("proposes nothing else", line 68), so two experts could disagree on the correct trajectory. An agent that reads "Yes, but to my Mastercard" as a confirmation and cancels breaks G-02 and still passes every scenario.
Pattern: a failure-row branch that changes the outcome ("another proposal term") with no scenario whose Initial state or User turn triggers it. Add a CO-S03-style row or scenario where the confirming turn changes the payment method or amount, and settle how the row interacts with CO-03.
```

## R3-10 — KEPT — fixed

Finders: coverage. Severity as given: Important.

Verifier: Real | Important | I could not refute it. The row "propose nothing until the customer asks to cancel the whole order" is an act-only-when condition. CO-S08 tests only the holding-back side: its optional pair "No, I'll keep it." No scenario has the customer ask for the whole order after a partial request. CO-S01 does not count as the acting side, because no partial request comes before it. This fails the checklist item "Both directions are covered."

Decision: New scenario CO-S27: partial request, then the whole order confirmed and cancelled.

Finder coverage wrote:

```
F3 | Gap | Important | Failure row "the customer asked to cancel only some of an order's items" / CO-S08
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence: This is an "act only when" condition. CO-S08 tests only the holding-back side: its one User-knows answer is "No, I'll keep it." (line 514). No scenario has the customer ask to cancel the whole order after a partial request, which would require a proposal, a confirmation, CO-A2 and CO-A3. An agent that refuses to cancel anything once a partial request has been made passes every scenario. evaluation-checklist.md "Both directions are covered" requires both sides.
Pattern: an "act only when / until" condition tested only on the holding-back side. Add a row or scenario where the customer, after the explanation, asks for the whole order to be cancelled and confirms.
```

## R3-11 — KEPT — open

Finders: coverage. Severity as given: Important.

Verifier: Not real | Important | The finding claims "nothing in the inputs or the spec says what the agent does", but the spec does say it. G-01's second sentence is scoped to the whole conversation: "Every other order and refund that existed before the conversation is unchanged at its end." §1 says the agent "may cancel that one order … it changes no other order". So at most one order changes per conversation. Scenarios assert G-01: CO-S02 has the Final state "<other order> is unchanged and has no refund" and the Forbidden line "CO-A2 or CO-A3 for any order other than <order>". The weak point: no scenario has the customer ask for two orders, so an agent that cancels both is caught only if a "rule asserted elsewhere" counts.

Decision: Verifier: Not real (G-01's "Every other order ... is unchanged at its end"); I do not agree no scenario is needed: whether a customer may cancel two orders in one conversation is the user's call. Kept, open.

Finder coverage wrote:

```
F4 | Gap | Important | G-01 / CO-06 / §1 Purpose
Quote: "The agent cancels, refunds and hands off at most the one order the current request is about." and "The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation"
Evidence: Nothing in the inputs or the spec says what the agent does when the customer wants two of their open orders cancelled. That could be one request ("cancel HG-10482 and HG-10511") or two requests in sequence. CO-S02 (lines 181–231) and CO-S03 always end with one order cancelled. CO-06 counts calls per conversation, not per order, so cancelling a second order in the same conversation would use up the retry budget the first order may need. G-01's "the current request" is undefined across several requests. The packet (lines 27–75) does not decide the case. An agent that cancels both orders, refuses the second, or cancels one and silently drops the other passes every scenario.
Pattern: a "what if" the inputs do not answer, involving several records the customer owns, with no rule or scenario. Record it as an open question for the user. Once it is answered, add a rule and a scenario.
```
