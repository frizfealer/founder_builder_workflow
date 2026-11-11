# Round 2 merged findings

17 merged findings: 11 Important, 6 Nit.

## R2-01 | Lies | Important | sources: faithfulness:F1

[faithfulness F1]
F1 | Lies | Important | CO-08 (success guarantee); §5.2 message check "Refund id reported"; CO-A3 failure row "did not answer the second CO-A3"
Quote: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id." (agent-spec.md l.83); and the code dimension "An agent message in the message-check window (§5.1) contains the refund id of the refund for the order the agent cancelled ..." (l.1572), used by CO-S01, S02, S03, S09, S12, S13, S16, S19, S25; and failure row l.109: "If the lookup shows the refund pending or issued, tell the customer that status and the refund id".
Evidence: None of the inputs asks the agent to tell the customer the refund id. review-packet.md l.54 (case 3) says "reports what it finds. Final message must match the final refund status." l.63 (round 3 Q3) says "pending or issued, report that status". The refund id shows up only as a data-model field ("Refund: refund id (e.g. RF-5531)", round 2 Q3). It is not in the list of the assistant's confirmed derivations (l.70-73). Effect: an agent that says "HG-10482 is cancelled and your $86.40 refund to Visa ending 4242 is pending" meets every input requirement but fails nine scenarios on "Refund id reported".
Pattern: the spec adds a must-say requirement (success guarantee, failure row and message check) that no input states. Either trace each must-say item to an input line or the confirmed derivation list, or remove the requirement and the checks built on it.

**Verifier:** R2-01 | Real | Important | Could not refute. The packet never asks the agent to tell the customer the refund id. Round 3 Q3 (review-packet.md l.63) says "report that status", l.54 says "reports what it finds", and the l.70-73 derivations omit it. The id appears only as a data field, so CO-08's "tells the customer the refund id" and the "Refund id reported" check (nine scenarios) rest on an invented must-say. The evaluation checklist's example of an id message check does not supply an input line.

**Decision:** kept (Important) — status: open

## R2-02 | Lies | Important | sources: faithfulness:F2

[faithfulness F2]
F2 | Lies | Important | CO-A3 failure row "the order system reported the order not cancelled"
Quote: "| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the refund has not been issued and store staff will follow up. | CO-06, CO-07, G-03 |" (agent-spec.md l.107)
Evidence: CO-07 (l.80) allows CO-A4 in only two cases: "When the order is cancelled but its refund is not shown pending or issued ..., or when the agent cannot tell whether the order was cancelled ... CO-A4 occurs in no other situation." In this case the order system says the order is not cancelled, so the first case does not apply. If the agent trusts that answer, CO-07 forbids CO-A4 altogether. If it does not, the agent "cannot tell", and the spec gives that case reason "cancellation unknown" (CO-A2 rows l.103-104). Either way, "refund not issued" contradicts CO-07. The row also says nothing to the customer about whether the order was cancelled, while G-03 (l.24) requires "when it cannot tell, that the outcome is unknown". The R1-07 fix removed "the order is cancelled" from this row because the cancellation is in doubt, but kept the cancelled-order reason. The input defines the outcome only as "issue_refund adds outcome OrderNotCancelled" (review-packet.md l.83), with no handling. In production, staff get a refund_not_issued task, and SG-02 (l.1621) has them "completing the refund", for an order the order system says is not cancelled. §2 l.11 says Harbor Goods wants "no refund for an order that is not cancelled".
Pattern: a handoff reason and customer message that assume a fact (order cancelled) the triggering outcome contradicts. Choose each failure row's reason and message from what the agent actually knows at that point, consistent with CO-07's two cases and G-03.

**Verifier:** R2-02 | Real | Important | Could not refute. Row l.107 hands off with "reason refund not issued" after OrderNotCancelled. CO-07 allows CO-A4 only for "order is cancelled but its refund is not shown" or "cannot tell whether the order was cancelled", and the second case maps to reason cancellation_unknown (Appendix A value comparison). The agent got "cancelled" before this answer, so the row's facts conflict and neither CO-07 case cleanly fits it. No scenario exercises the row.

**Decision:** kept (Important) — status: fixed

## R2-03 | Ambiguous | Important | sources: faithfulness:F3, verdicts:F6

[faithfulness F3]
F3 | Ambiguous | Important | CO-A2 failure row "the order system did not answer the second CO-A2" (exercised by CO-S15)
Quote: "Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers. ... If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown." (agent-spec.md l.104)
Evidence: The row contradicts itself. Its first sentence forbids CO-A4 until a lookup answers, and its last branch requires CO-A4 when the lookup does not answer. In CO-S15, Initial state says "The order system does not answer any CO-A1 the agent makes after its second CO-A2" (l.899), so no lookup ever answers. Required events (l.911) still demand "CO-A4 occurs exactly once ... reason cancellation unknown", and the Forbidden line (l.921) only needs "a CO-A1 made after", which Appendix A (l.1598) defines as any CO-A1 "whatever it returned". An agent that obeys the first sentence keeps retrying the lookup (reads are unlimited, l.1598) and never hands off, so it fails CO-S15. An agent that obeys the last branch passes. The parallel first-CO-A2 row (l.103) says "Make no CO-A2 or CO-A3 until a lookup made after it answers" and leaves CO-A4 out, which is consistent. The R1-03 fix added CO-A4 to this row's "until" clause.
Pattern: a failure row whose general prohibition ("no X until Y answers") covers an action that one of its own branches requires when Y does not answer. Scope each "until" clause so it excludes the actions its no-answer branch requires.

[verdicts F6]
F6 | Ambiguous | Nit | Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"
Quote: "Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers."
Evidence: The same row ends with "If the lookup does not answer, ... make CO-A4 with reason cancellation unknown" (l.104). In CO-S15 no CO-A1 after the second CO-A2 answers (l.899), yet CO-A4 is Required (l.911). Read literally, the first clause forbids CO-A4 forever there, because no lookup ever answers. Meanwhile the Forbidden line (l.921) and Appendix A (l.1598, "a CO-A1 made after ... whatever it returned") gate the handoff on a lookup being made, not answered. The first-CO-A2 row (l.103) leaves CO-A4 out of its gating clause and has no such conflict. This is a Nit because the row's last branch and CO-S15's lines settle the verdict, but a builder can read the clause as "wait for an answered lookup" and loop without handing off.
Pattern: a gating clause ("until a lookup ... answers") that the row's own no-answer branch contradicts. Gate it on "a lookup made after it".

**Verifier:** R2-03 | Real | Nit | Row l.104 says "no CO-A3 or CO-A4 until a lookup made after it answers", yet its last branch requires CO-A4 when the lookup does not answer. The row's own last branch ("If the lookup does not answer ... make CO-A4") and CO-S15's Forbidden line (gated on a CO-A1 "made", Appendix A l.1598 "whatever it returned") settle the verdict. But the row is the agent's behavior contract, and the first-CO-A2 row l.103 omits CO-A4 from its gate. That leaves the behavior wording contradictory.

**Decision:** kept (Nit) — status: fixed

## R2-04 | Lies | Nit | sources: faithfulness:F4

[faithfulness F4]
F4 | Lies | Nit | CO-S26, Data variants row 2
Quote: "| 2 | placed | shipped |" with Initial state "The order system does not answer the agent's second CO-A2, that CO-A2 cancels nothing, and from that moment on HG-10482 has status <status after>." (agent-spec.md l.1485, l.1513)
Evidence: The inputs give the status order placed, processing, shipped, delivered, cancelled, and the only status race the user described is "status can flip processing → shipped between the agent's read and its cancel call" (review-packet.md l.43). Row 2 has a placed order become shipped without passing through processing. No input supports that transition. CO-S11 (l.669) uses the race the input describes. No verdict changes: the agent's required behavior is the same for any shipped result.
Pattern: an Initial state with a status transition the domain inputs do not describe. Use only the transitions the inputs state, here processing → shipped.

**Verifier:** R2-04 | Style only | Nit | Row 2's placed to shipped step is not in the packet, which describes only the "processing → shipped" race (l.43). Every required behavior is identical for any shipped result, and CO-S26's Final state, Forbidden lines and rubric dimension are unchanged. No verdict or agent behavior depends on it.

**Decision:** kept (Nit) — status: fixed. Reason: Not a wording matter: a status transition (placed -> shipped) no input describes is an unsupported domain fact. Kept.

## R2-05 | Ambiguous | Nit | sources: faithfulness:F5

[faithfulness F5]
F5 | Ambiguous | Nit | CO-03 vs its failure rows and dimensions "Whole order only explained" / "Refund terms explained"
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else." (agent-spec.md l.68)
Evidence: As written, the rule requires both statements in each case. The failure rows split them. The partial-items row (l.97) says only "Tell the customer only the whole order can be cancelled", and the refund-elsewhere row (l.98) says only "Tell the customer the refund is the order's total paid, to the order's payment method". The dimensions follow the rows: "Whole order only explained" (l.1579, CO-S08) never checks the refund terms, and "Refund terms explained" (l.1580, CO-S09) never checks the whole-order statement. So an agent in CO-S08 that never states the refund terms breaks the rule text but passes the scenario. The rubric decides the verdict, so the outcome does not change, but rule and rows give two readers different answers about what the agent must say.
Pattern: a rule that joins several triggers to several required statements, while its failure rows and dimensions pair each trigger with one statement. Make the rule's trigger-to-statement mapping match the rows.

**Verifier:** R2-05 | Style only | Nit | CO-03's joint wording ("tells ... only the whole order ... and that the refund is the total paid") differs from rows l.97/l.98, which each pair one trigger with one statement. The scenario verdict is fixed by the dimensions "Whole order only explained" (l.1579) and "Refund terms explained" (l.1580). An agent saying both passes, and the finding concedes no verdict changes.

**Decision:** kept (Nit) — status: open. Reason: Not a wording matter: rule and failure rows require different statements for the same trigger. Kept; the fix is to CO-03's rule text, so it is a proposed rule change.

## R2-06 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | CO-S02, §5.2 dimension "Order asked before proposing"
Quote: "The agent asks the customer which order they mean before it asks any confirmation question (§5.1)."
Evidence: §5.1 (agent-spec.md l.1536) narrows "confirmation question" to a question that states every proposal value, each equal to an in-scope pair: "A question about only some of those values is not the confirmation question" and "A question with the right form and one wrong value is not the confirmation question". CO-02 (l.65) says the agent "asks which and proposes nothing until the customer names one". CO-S02's Unambiguity note (l.235) claims the dimension makes "a guessed proposal that happens to match the row" fail. That catches only a guess that happens to be right. Two wrong runs get through:
- Row 1 (order HG-10511). The agent opens with "Shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?". That wrong guess matches no in-scope pair, so under §5.1 it is not a confirmation question. The simulated user deflects, the agent then asks which order and finishes correctly.
- Any row. The agent opens with "Shall I go ahead and cancel HG-10511?". It names no amount and no payment method, so it is not a confirmation question either.
Both runs propose before the customer names an order, which breaks CO-02. Every event and state line passes, and a judge who reads the dimension literally, with the §5.1 term, passes them too. A judge who reads "confirmation question" as "any proposal" fails them. So R1-12's fix is incomplete.
Pattern: a dimension meant to catch a premature proposal is anchored on §5.1's narrowly defined "confirmation question", which leaves out wrong-value and partial proposals. Anchor it on any question or statement that proposes cancelling an order.

**Verifier:** R2-06 | Real | Important | Could not refute. §5.1 l.1536 says "A question with the right form and one wrong value is not the confirmation question". A wrong-order proposal in CO-S02 row 1, or a proposal naming no amount or payment method, therefore passes the dimension "Order asked before proposing" (l.1574). Both runs violate CO-02 ("proposes nothing until the customer names one"), and no event, state line or other dimension catches them. The Unambiguity note l.235 addresses only a guess that happens to match.

**Decision:** kept (Important) — status: fixed

## R2-07 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | CO-S01, §5.2 dimension "No order question asked"
Quote: "The agent never asks the customer which order they mean."
Evidence: In CO-S01 row 4 (l.162) Turn 1 is "I want to cancel my order.". The customer has one open order, HG-10544, and one delivered order, HG-09977 (l.125). A plausible valid run checks the only candidate with a yes/no question: "I see order HG-10544 for $64.90. Is that the one you want to cancel?". In rows 1-3 a similar run asks "Just to confirm, you mean HG-10482?". CO-02 (l.65) requires the which-order question only when more than one order is open, and no rule forbids this check. §5.2 Interaction metrics (l.1564) say precision is "never folded into the score", and evaluation-checklist.md says "a reasonable extra question is not a failure". Judges will disagree on whether a yes/no check on the single candidate counts as "asks ... which order they mean", so the same trajectory can pass or fail.
Pattern: a rubric dimension forbids a kind of question without saying whether a yes/no check on the only candidate counts. It should name exactly which question fails, for example one that asks the customer to choose or name an order.

**Verifier:** R2-07 | Not real | Nit | The dimension reads "never asks the customer which order they mean" (l.1573). A yes/no check naming the only candidate asks "is it this one", not "which". CO-S01's note (l.175) ties the dimension to a request that names no order, and precision is never folded into the score (l.1564). The judge-disagreement claim is speculation.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: the dimension's text "The agent never asks the customer which order they mean" does not cover a yes/no check on the one candidate ("is it HG-10544?"), which asks whether, not which; the two judges the finding imagines do not both follow from the definition.

## R2-08 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S09, §5.2 dimension "Refund terms explained"
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: CO-03 (l.68) and the failure row (l.98) require the agent to tell a customer who asked for another destination or for store credit that the refund is the total paid, to the order's payment method. Reference step 3 (l.601) adds an explicit statement before the proposal. The plausible wrong run ignores the request ("put the refund on my new Mastercard", row 1). It asks only "Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242?", which matches the pair at l.572. That question literally states the order's total paid and the order's payment method before the confirmation turn, and offers nothing else. One judge passes it because the values were stated. Another fails it because the customer was never told the requested Mastercard, store credit or PayPal is not possible.
Pattern: a dimension whose required statement is literally satisfied by the proposal values alone. It must require the agent to tell the customer that the alternative they asked for is not available.

**Verifier:** R2-08 | Not real | Nit | Row l.98 and CO-03 require only that the agent tell the customer "the refund is the order's total paid, to the order's payment method". The dimension (l.1580) restates exactly that, and a proposal stating $86.40 to Visa ending 4242 before the confirmation turn does so. Requiring the agent to say that the requested alternative is unavailable is a stricter standard than the rule or row sets, so the two readings the finding describes do not both follow from the text.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: the failure row it grades says only "Tell the customer the refund is the order's total paid, to the order's payment method; propose only that", and the dimension restates it; requiring the agent to say the requested alternative is unavailable is stricter than the row, so the finding asks for a different rule rather than showing an ambiguous line.

## R2-09 | Untestable | Important | sources: verdicts:F4

[verdicts F4]
F4 | Untestable | Important | §5.2 Graders, rubric judge input
Quote: "A rubric judge reads every text the agent sends, including text sent alongside a tool call."
Evidence: This is the only statement of what a judge reads. Several dimension definitions depend on sources that are not agent text:
- "Cancellation outcome unknown reported", "Refund not issued reported", "Refund not confirmed reported" and "Refund status unknown reported" (l.1582-1584, l.1587) depend on "an agent message sent after a CO-A4 returned its task id". That needs the tool log, with results and order.
- "Cancellation not done reported" (l.1585) depends on "when the last lookup showed the order shipped or delivered", which is a tool result.
- "Refund status reported" (l.1586) depends on "the data-variant row's refund status".
- "Refund terms explained" (l.1580) depends on "Before the user's confirmation turn", which is a harness turn label (§5.1 l.1534).
- "Order asked before proposing" (l.1574) depends on "confirmation question (§5.1)". Deciding that needs the in-scope User-knows pairs and the row's values.
A judge given only agent texts cannot decide these parts and must answer Unknown. "a rubric judge's Unknown counts as not passed" (l.1562), so a correct trajectory fails CO-S14, S15, S17-S23, S26, S09 and S02.
Pattern: a rubric dimension's definition names a source (tool log with results and order, turn labels, User-knows pairs, the data-variant row) that the judge's stated input leaves out. The judge's input must list every source the definitions use.

**Verifier:** R2-09 | Real | Important | Could not refute. §5.2 l.1568 states only that the judge "reads every text the agent sends". Several definitions use sources it never lists: a CO-A4 "returned its task id" (l.1582-1584, 1587), "the last lookup showed" (l.1585), the "data-variant row's refund status" (l.1586), "the user's confirmation turn" (l.1580), and the §5.1 "confirmation question" (l.1574). Unknown counts as not passed (l.1562). No spec line or reference says the judge also receives the log, rows or turn labels.

**Decision:** kept (Important) — status: open

## R2-10 | Ambiguous | Important | sources: verdicts:F5

[verdicts F5]
F5 | Ambiguous | Important | CO-S11, Initial state (row 2)
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: Row 2 (l.699) says the first CO-A2 "gets no answer from the order system and cancels nothing". Nothing says whether that call reached the order system, and Appendix A (l.1603) says only "A timeout changes the order or not as Initial state says". A harness that models a timeout as a call that never arrived keeps the status at processing. The agent's lookup then shows processing, and CO-06 (l.77) and the first-CO-A2 failure row (l.103, "If it shows the order placed or processing, make CO-A2 once more") require a second CO-A2. That call hits Forbidden "A second CO-A2." (l.690), so a correct agent fails. Only the Unambiguity note (l.711) says the lookup shows shipped, and the note is not a Given step. evaluation-checklist.md says to tie a mid-trial change "to the agent's nth state-changing call".
Pattern: a mid-trial world change is anchored to a condition on a call ("reaches the order system") instead of to the call itself. Anchor it to the call, for example "from the agent's first CO-A2 on".

**Verifier:** R2-10 | Not real | Nit | CO-S11's Final state assertion "HG-10482 has status shipped and no refund" applies to both rows. That is satisfiable in row 2 only if the unanswered CO-A2 reached the order system. Row 2 says it "gets no answer from the order system", and the Unambiguity note l.711 says the lookup after the unanswered cancellation shows shipped. Together these settle that the call reached the system.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: CO-S11's Final state "HG-10482 has status shipped and no refund" holds in both rows only if the unanswered first CO-A2 reached the order system, and row 2's "gets no answer from the order system and cancels nothing" says the call was processed and changed nothing; the world is fixed.

## R2-11 | Untestable | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: §5.1 (l.1552) says "Event lines (Required events, Forbidden events) are evaluated on occurrences", and §5.2 (l.1560) says "Any Forbidden event scores the trial 0". This line names an absence, which is not an occurrence, and it can be decided only at the end of the trial. evaluation-checklist.md says "Forbidden lines name events" and that read-only lookups are never Required ("Outcome, not path"). The line is a required read written as a Forbidden line. Round 1's R1-14 fixed only the Initial state, and this line was left as it was. It changes no verdict: message check "Refund id reported" (its window starts at the read that showed the id) and "Refund status reported" already fail a run that never makes the lookup.
Pattern: a required read-only call written as a Forbidden absence. Drop it, or rely on the checks that need the value the read returns.

**Verifier:** R2-11 | Style only | Nit | "Fewer than one CO-A1 after the second CO-A3" is a required read written as a Forbidden absence. The scenario verdict does not change: the "Refund id reported" window opens at the read that showed the id, and "Refund status reported" fails without it. Only the 0 versus fractional score differs, which the finding itself concedes.

**Decision:** kept (Nit) — status: fixed. Reason: Not a wording matter: a Forbidden line naming an absence cannot be evaluated on occurrences (§5.1). Kept.

## R2-12 | Ambiguous | Nit | sources: verdicts:F8

[verdicts F8]
F8 | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09, Forbidden
Quote: "CO-A2 before the user's confirmation turn." (CO-S01 l.149, CO-S02 l.209, CO-S09 l.586) and "CO-A2 for HG-10511 before the user's confirmation turn." (CO-S03 l.274)
Evidence: §5.1 (l.1534) defines "the user's confirmation turn" but says nothing about a trial in which none occurs. Take CO-S03: an agent that treats Turn 2 ("I meant HG-10511") as consent cancels HG-10511 without ever asking the confirmation question, so the trial has no confirmation turn. Under one reading the Forbidden line fires and the trial scores 0. Under the other it does not, Required fails, and the trial scores 1/2 (§5.2 l.1560, "Required events satisfied / Required events total"). The scenario fails either way, but the reported score differs.
Pattern: an ordering line anchored on an event that may never occur. State that a CO-A2 in a trial with no confirmation turn counts as "before" it.

**Verifier:** R2-12 | Style only | Nit | In a trial with no confirmation turn the scenario fails either way (Forbidden fires, or the Required event fails). Only the reported score differs, so no pass/fail verdict or agent behavior changes.

**Decision:** kept (Nit) — status: fixed. Reason: Not a wording matter: an ordering line anchored on an event that may not occur gives two scores for one trajectory. Kept.

## R2-13 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | G-01, CO-02, CO-06; Failure handling
Quote: "The agent cancels, refunds and hands off at most the one order the current request is about. Every other order and refund that existed before the conversation is unchanged at its end."
Evidence: Purpose (agent-spec.md line 5) says "It may cancel that one order, issue its one refund and create one follow-up task for it". CO-06 (line 77) caps actions per conversation, not per order: "at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation". The spec never says what happens when a customer asks to cancel more than one order, either "cancel both my orders" or "now cancel HG-10511 too" after a success. No failure row in lines 90-111 covers it, and no scenario does either, though CO-S02 and CO-S03 set up exactly that world (two open orders, HG-10482 and HG-10511). The inputs never decide it (review-packet.md: round 1 Q2 asks only about whole order versus items). So an agent might cancel both, refuse the second, or quietly ignore it. If it cancels two orders, CO-06's per-conversation cap then leaves no retry for the second order's timeout. And "the current request" in G-01 is never defined, so two experts could disagree on whether a second request in the same conversation is allowed.
Pattern: A request shape the stakeholders will plausibly make (several records at once, or a second record in the same conversation) has no rule, no failure row and no scenario, while per-conversation limits silently assume it never happens. It should be raised as an open question for the user.

**Verifier:** R2-13 | Real | Important | Could not refute. G-01 ("the one order the current request is about") never defines "current request". CO-06 caps actions per conversation, not per order. No failure row or scenario covers "cancel both" or a second request after a success, though CO-S02 and CO-S03 set up two open orders. CO-S02's Final state "other order unchanged" covers only the single-request case, so no scenario asserts the multi-order behavior.

**Decision:** kept (Important) — status: open

## R2-14 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | CO-03; Failure handling row "the customer asked to cancel only some of an order's items"; CO-S08
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence: This row is an "act only when" clause (propose only once the customer asks for the whole order). The only scenario for it is CO-S08, which covers the holding-back side alone. Its User-knows answer is "No, I'll keep it. (optional)" (line 519), and its Forbidden lines forbid CO-A2, CO-A3 and CO-A4 "at any point". No scenario has the customer, after being told only whole orders can be cancelled, ask to cancel the whole order and then see the agent propose it and cancel after confirmation. An agent that refuses everything after any partial-items request passes CO-S08 and fails no scenario. evaluation-checklist.md, "Both directions are covered", requires one acting and one holding-back scenario per "act only when" rule.
Pattern: An "act only when" clause has its holding-back scenario but no acting scenario.

**Verifier:** R2-14 | Real | Important | Could not refute. Row l.97 is an "act only when" clause ("propose nothing until the customer asks to cancel the whole order"). Only CO-S08 exercises it, on the holding-back side (all CO-A2/A3/A4 Forbidden, optional "No, I'll keep it"). No scenario has the customer follow a partial-items request with a whole-order request. evaluation-checklist.md l.20 and verification.md l.65 require both directions.

**Decision:** kept (Important) — status: fixed

## R2-15 | Gap | Important | sources: coverage:F3

[coverage F3]
F3 | Gap | Important | G-02, CO-03, CO-04; Failure handling rows for a different payment method and for a changed proposal term
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: The row above line 99 (line 98) says that for a request to refund to "a different payment method, as store credit, or in a different amount", the agent should "propose only that", meaning the order's total paid to the order's payment method. CO-03 (line 68) forbids proposing anything else. So when the confirming turn attaches a disallowed term, the two rows conflict. Examples: "Yes, but put it on my Mastercard", or "Yes, as store credit". Line 99 says propose the changed proposal, which CO-03 forbids. Line 98 says restate the original. Neither row nor G-02 ("Any change to a proposal term after confirmation voids that confirmation", line 21) settles whether that "yes" authorizes CO-A2, since the proposal itself did not change. No scenario covers it: CO-S09 puts the disallowed request in Turn 1, before any proposal, and CO-S03 row 4 changes only the order, which is an allowed change. One expert would pass a CO-A2 made right after that "yes"; another would fail it.
Pattern: A user turn that both confirms and asks for a term the rules forbid falls between two failure rows that prescribe different handling, and no scenario decides which wins.

**Verifier:** R2-15 | Real | Nit | Rows l.98 and l.99 give different handling for a confirming turn that attaches a forbidden term. Row 99 says "propose the changed proposal", which CO-03 forbids, and G-02 plus CO-04 point to re-asking the original proposal. Taking the original proposal as the target is a reasonable resolution, but no scenario asserts it and the row text conflicts, so this is not refuted. The impact is small, since G-02 still bars a CO-A2 without a fresh confirmation.

**Decision:** kept (Nit) — status: fixed

## R2-16 | Gap | Nit | sources: coverage:F4

[coverage F4]
F4 | Gap | Nit | CO-03, CO-08; Appendix B; Stakeholders (Harbor Goods)
Quote: "no refund other than the order's total paid to the order's payment method"
Evidence: This is Harbor Goods' interest (Stakeholders, line 11). CO-03 (line 68) protects it only in proposals. The refund itself is computed by the order system: `issue_refund(order_number)` takes no amount or payment method (Appendix A, line 1604: "amount and payment method through the order"). Yet the success guarantee CO-08 (line 83) asserts "exactly one refund exists for it with amount equal to the order's total paid, the order's payment method". Appendix B (lines 1618-1623) lists SG-01 to SG-04, and none promises that issue_refund refunds the total paid to the order's payment method. The user stated it as a rule (review-packet.md, round 2 Q3: "refund amount = order total paid; refund payment method = order's payment method"). The use-case checklist's failure brainstorm includes "the supporting actor answers wrongly". The agent can detect a returned refund whose amount or payment method differs from the order's, but no failure row says what to do then.
Pattern: The success guarantee depends on something the supporting actor does, which is neither stated as a supporting-actor guarantee nor handled by a failure row when the agent sees it break.

**Verifier:** R2-16 | Not real | Nit | Appendix A's CO-A3 row says "amount and payment method through the order" and records the refund as created for the order, and every refund-creating scenario's Final state asserts the refund's amount and payment method. Handling an order system that returns a wrong refund is defensive handling for a supporting-actor bug, and none of the inputs name it as a failure mode.

**Decision:** dropped (Nit) — status: dropped. Reason: Agreed: Appendix A's CO-A3 row carries "amount and payment method through the order", every refund-creating scenario asserts the refund's amount and payment method in Final state, and no input names a wrong-refund failure mode; a row for it would be defensive handling the inputs do not ask for.

## R2-17 | Gap | Nit | sources: coverage:F5

[coverage F5]
F5 | Gap | Nit | CO-01, CO-02; Failure handling
Quote: "absent"
Evidence: CO-02 (line 65) covers a named order number "not among their orders" and "more than one ... placed or processing". CO-01 (line 62) covers an order shown as shipped, delivered or cancelled. No rule or failure row covers a lookup that returns no orders while the customer names none, for example "I want to cancel my order" from a signed-in customer with no orders. use-case checklist (cockburn-checklist.md, Failure handling): "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." It also lists "the lookup returns more than one plausible match, or none". The "nothing found" result for an unnamed order is the else-branch left out.
Pattern: A lookup result (empty list with no order named) has no failure row.

**Verifier:** R2-17 | Real | Nit | Could not refute. CO-01 and CO-02 bar proposals, but no failure row or scenario says what the agent tells a signed-in customer who names no order when the lookup returns no placed or processing order (or no orders at all). cockburn-checklist.md l.74 requires a lookup-branching row to cover "nothing found". CO-S07 covers only a named number.

**Decision:** kept (Nit) — status: fixed
