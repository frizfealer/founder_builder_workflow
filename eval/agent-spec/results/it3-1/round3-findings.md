# Round 3 merged findings

12 merged findings: 6 Important, 6 Nit.

## R3-01 | Lies | Important | sources: faithfulness:F1

[faithfulness F1]
F1 | Lies | Important | CO-S15, Reference trajectory
Quote: "7. Agent → CO-A2 (HG-10482) → no answer.
8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created."
Evidence: CO-S15's own Forbidden block says "CO-A4 before a CO-A1 made after the second CO-A2." (agent-spec.md line 923). Its Initial state says "The order system does not answer any CO-A1 the agent makes after its second CO-A2." (line 901). Its Unambiguity note says "a handoff before a lookup made after the second cancellation fails" (line 946). The failure row "the order system did not answer the second CO-A2" says "no CO-A3 or CO-A4 before a lookup made after it" (line 105). The reference trajectory goes straight from the second unanswered CO-A2 (step 7) to CO-A4 (step 8) with no CO-A1 between them, so it breaks a Forbidden line of its own scenario. Every sibling trajectory includes the lookup before acting: CO-S14 step 6, CO-S19 step 8, CO-S20 step 8, CO-S21 step 8, CO-S25 step 8, CO-S26 step 8. If the reference is replayed to check the harness, or used as the passing example for the conversion, it scores 0. The fix is to add "Agent → CO-A1 → no answer." between steps 7 and 8.
Pattern: A reference trajectory leaves out a step that one of its own scenario's Forbidden lines or failure rows requires before a later action.

**Verifier:** R3-01 | Real | Important | Could not refute. CO-S15 Reference trajectory goes from step 7 "Agent → CO-A2 (HG-10482) → no answer." to step 8 "Agent → CO-A4 (HG-10482, cancellation unknown) → task created." with no CO-A1 between. Its own Forbidden says "CO-A4 before a CO-A1 made after the second CO-A2." The failure row for the second unanswered CO-A2 says "no CO-A3 or CO-A4 before a lookup made after it."

**Decision:** kept (Important) — status: fixed

## R3-02 | Lies | Nit | sources: faithfulness:F2

[faithfulness F2]
F2 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 (agent-spec.md line 740) says cancelling an already-cancelled order "returns it cancelled and changes nothing", which is exactly "repeating it creates nothing new". As written, G-04's second clause therefore allows a blind resend of cancel_order after a timeout. The input forbids that: review-packet.md round 3 Q4, accepted with "Yes to all", says "If the cancel call times out: no blind resend; re-read the order." The CO-A4 retry row (line 111) also leans on G-04's general clause through SG-03, so the clause is not limited to SG-01. CO-06 and the Forbidden lines in CO-S12, CO-S13 and CO-S15 still require the lookup before a second CO-A2, so no verdict changes. The global rule still states a permission the inputs deny.
Pattern: A global rule's exception is written as a general class of supporting-actor guarantees, and a later guarantee (SG-04) falls into that class for an action the inputs exclude from the exception.

**Verifier:** R3-02 | Style only | Nit | G-04 names its exception in the clause itself: "creates nothing new (Appendix B, SG-01)". CO-06 ("makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing") and the Forbidden lines in CO-S12, S13 and S15 already bind the agent to the lookup. No verdict or agent behavior changes.

**Decision:** kept (Nit) — status: open. Reason: Not a wording matter: the finding is that a global rule's exception admits an action the inputs exclude (round 3 Q4 "no blind resend"). Kept; the fix is to G-04's rule text, so it is a proposed rule change.

## R3-03 | Lies | Nit | sources: faithfulness:F3

[faithfulness F3]
F3 | Lies | Nit | CO-S08, User knows and Reference trajectory (against the partial-items failure row)
Quote: "Q: Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)" and "3. Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order."
Evidence: The failure row for "the customer asked to cancel only some of an order's items" says "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order." (agent-spec.md line 98). CO-01 uses "proposes cancelling an order" for putting one order forward to be cancelled (line 62). The CO-S08 pair and trajectory have the agent offer to cancel HG-10530 before the customer has asked for the whole order. CO-S27 handles the same row and the same Turn 1 the other way: step 3 is only "Agent tells the customer only the whole order can be cancelled." and the customer asks for the whole order in Turn 2 (line 1577). The spec models opposite behavior for one failure row. No dimension penalizes the offer, and the pair is optional, so no verdict changes. This is related to the open R1-18 ("propose" undefined) but is a separate conflict: the scenario contradicts the row's own wording.
Pattern: A scenario's User-knows pair or reference trajectory shows behavior that the failure row it exercises explicitly holds back, and a sibling scenario on the same row shows the held-back version.

**Verifier:** R3-03 | Style only | Nit | CO-04 defines a proposal as "order number, refund amount and payment method". The CO-S08 question "Would you like to cancel the whole order HG-10530 instead?" gives only the order number, so it is not a proposal. The pair is marked (optional), and CO-S08 Forbidden (no CO-A2, CO-A3 or CO-A4) fails any action. No verdict changes.

**Decision:** kept (Nit) — status: fixed. Reason: Not a wording matter: the reference trajectory models behavior the failure row it exercises holds back, and CO-S27 models the opposite. Kept.

## R3-04 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | CO-S27, User block
Quote: "- Turn 2, in reply to the agent's first agent message: "<Turn 2>""
Evidence: The trigger fires on whatever the first agent message is, including a full confirmation question. An agent can explain "only the whole order can be cancelled" and then ask "Shall I cancel HG-10530 and refund $53.50 to Amex ending 1007?" in that same first message. The sibling scenario CO-S08 does nearly this in its reference step 3: "Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order." In that case the scripted Turn 2 arrives as the reply to the confirmation question: row 1 "OK, then cancel the whole order.", row 2 "Fine, cancel all of HG-10530 then." §5.2 says that when a message makes a scripted turn due, the simulated user "gives no User-knows answer", so that turn is never labelled the confirmation turn. A CO-A2 after it therefore hits Forbidden "CO-A2 before the user's confirmation turn, or in a trial with no confirmation turn." Two readings decide this trajectory differently:
- G-02 (line 21) only asks that the customer "explicitly confirmed the exact proposal". "OK, then cancel" in reply to a proposal that states every value reads as that confirmation, so the trial should pass.
- CO-04 (line 71) says "a statement that the customer wants to cancel ... is not confirmation". Failure row line 98 says "propose nothing until the customer asks to cancel the whole order", which would make the early proposal itself the error. But no CO-S27 line names that error, and the Unambiguity note ("confirms only after it") does not settle whether a reply to a full proposal is a confirmation.
Pattern: A scripted reply is triggered by an event broader than the message it was written to answer. When the triggering message is a confirmation question, the reply's wording reads as a confirmation, and whether the agent may act on it is left to judgment.

**Verifier:** R3-04 | Not real | Nit | §5.1 defines "the user's confirmation turn" as a turn in which the simulated user gives a User-knows answer, and the harness labels it. CO-S27's pair is scoped "(after Turn 2)", so a question in the first agent message matches no pair. §5.2 says that when a message makes a scripted turn due, the simulated user "gives no User-knows answer". The Turn 2 reply is therefore never the confirmation turn. A CO-A2 right after it hits Forbidden "CO-A2 before the user's confirmation turn, or in a trial with no confirmation turn." The verdict is fixed by the labels, not by judgment.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: §5.1 "'The user's confirmation turn' is the user turn in which the simulated user gives a User-knows answer to a confirmation question" and §5.2 "When an agent message makes a scripted User turn due, the simulated user says the User turn, and gives no User-knows answer" make Turn 2 never the confirmation turn, so a CO-A2 after it hits CO-S27's Forbidden line by the harness labels, with no judgment left.

## R3-05 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | §5.1 Agent message / §5.2 Graders and dimension definitions
Quote: "A rubric judge reads every text the agent sends, including text sent alongside a tool call."
Evidence: §5.1 (line 1655) says: "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one." The dimension definitions are written in terms of messages:
- "No arrival time promised" (line 1692): "No agent message promises or estimates a date..."
- "Cancellation outcome unknown reported", "Refund not issued reported", "Refund not confirmed reported" and "Refund status unknown reported" (lines 1699-1701, 1704): "in an agent message sent after a CO-A4 returned its task id, that store staff will follow up; it says store staff will follow up in no message before then".
Take an agent that writes "I've passed this to our store staff, who will follow up" alongside its request_staff_followup call, before the task id returns. Under §5.1 that text is not a message, so the dimension passes. The judge reads that text, so it can fail the dimension. The same split applies to "your money arrives in 5-10 business days" written alongside the issue_refund call, which CO-09 forbids. That text reaches the customer, yet the definition excludes it. This affects CO-S01, CO-S14, CO-S15, CO-S16, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21 and CO-S22. This is not R2-09, which is about the tool log, turn labels and data-variant rows that the judge cannot see. This finding is about which agent texts count at all.
Pattern: Rubric definitions limit themselves to "agent messages" as §5.1 defines them, while §5.2 has the judge read all agent text. Text sent alongside a tool call can pass or fail the same dimension depending on which clause the judge follows.

**Verifier:** R3-05 | Real | Important | Could not refute. §5.1 says "text sent alongside a tool call is not one" (an agent message). §5.2 says the judge reads "every text the agent sends, including text sent alongside a tool call." Dimensions such as "No arrival time promised" and the four "...reported" dimensions say "no agent message...", so text alongside a call can pass or fail depending on which clause the judge follows.

**Decision:** kept (Important) — status: fixed

## R3-06 | Untestable | Important | sources: verdicts:F3

[verdicts F3]
F3 | Untestable | Important | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A (line 1715) says "The agent may repeat CO-A1 without limit; only commit calls are bounded." The packet's tool confirmation turn agrees: "Reads may be retried on timeout without limit". Four Initial states make CO-A1 never answer:
- CO-S10 (line 624): "does not answer any CO-A1 the agent makes"
- CO-S14 (line 843): after the first CO-A2
- CO-S15 (line 901): after the second CO-A2
- CO-S21 (line 1247): after the second CO-A3
Failure rows lines 92, 104, 105 and 110 act on "the lookup does not answer", but nothing says after how many unanswered retries the agent should treat a lookup as not answering. An agent that keeps calling list_orders never sends a message, so by §5.1 the trial never ends and gets no verdict. Any step limit the harness adds is unstated, and the verdict then depends on it.
Pattern: A tool may be retried without limit against a supporting actor scripted never to answer, and trial end is bounded only by agent messages. The spec bounds neither tool calls nor the number of read retries before the "lookup does not answer" branch.

**Verifier:** R3-06 | Real | Nit | Could not refute. Appendix A says "The agent may repeat CO-A1 without limit", and §5.1 bounds the trial only by agent messages. CO-S10, S14, S15 and S21 script CO-A1 never answering, and no clause says after how many unanswered reads the lookup counts as "does not answer". Only the endless-looping case is open: a single lookup already satisfies the Forbidden lines.

**Decision:** kept (Nit) — status: open

## R3-07 | Ambiguous | Important | sources: verdicts:F4

[verdicts F4]
F4 | Ambiguous | Important | CO-S01, Data variants row 3 / Appendix A Value comparison
Quote: "| 3 | cancel my order hg-10530 | HG-10530 | placed | $53.50 | Amex ending 1007 | RF-5533 |"
Evidence: CO-S01 carries the tag "canonicalization" (line 119). Appendix A (line 1713) says "Order numbers and refund ids compare case-insensitively." It does not say whether this applies only to grading or also to the order system's handling of cancel_order and issue_refund. The CO-A2 outcome "order not found: `OrderNotFound`" does not say whether "hg-10530" finds HG-10530. Take an agent that passes the customer's lowercase text to cancel_order:
- Harness A (case-insensitive order system): cancelled, and the trial passes.
- Harness B (exact match): OrderNotFound, so Final state "<order> has status cancelled" fails, while the Required event "for <order>" still passes under case-insensitive comparison.
Under reading A, row 3 cannot fail on canonicalization, despite the tag.
Pattern: A comparison rule written for grading is silent on whether the simulated supporting actor accepts the same variants. A row built to test a surface form then gets a verdict that depends on how the harness builder reads that rule.

**Verifier:** R3-07 | Real | Important | Could not refute. Appendix A says "Order numbers and refund ids compare case-insensitively" under "Value comparison", which is a grading rule. Neither it nor the CO-A2 outcome "order not found: OrderNotFound" says whether the order system accepts "hg-10530". §5.1's "answers every call normally" does not say what is normal for that input. CO-S01 row 3 is tagged canonicalization, and its verdict can differ by harness.

**Decision:** kept (Important) — status: open

## R3-08 | Untestable | Nit | sources: verdicts:F5

[verdicts F5]
F5 | Untestable | Nit | CO-S17, CO-S22, CO-S23, Initial state / Data variants
Quote: "- The agent's first CO-A3 creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because <failure reason>."
Evidence: R1-11 (answered.md) removed the invented `failure_reason` field from Appendix A's CO-A3 outcome. The Refund data model confirmed in the packet (round 2 Q3) has only refund id, order number, amount, payment method and status. So no world state or tool result can carry "because the card has been closed / has expired / the payment provider declined it". Instances:
- CO-S17 "first refund outcome" column, rows 1 and 2
- CO-S22 Initial state line 1306 ("because the card has been closed")
- CO-S23 line 1366 and its "failure reason" column
None of these can become a Given step without dropping the clause. Once it is dropped, CO-S17's two rows and CO-S23's two rows are identical. The R1-11 fix is incomplete.
Pattern: An Initial-state line states a cause that the data model and tool result have no field for. The Given step cannot set it up, and data-variant rows that differ only in that cause test nothing different.

**Verifier:** R3-08 | Style only | Nit | Appendix A's CO-A3 outcome "refund failed: returns the refund with status failed" has no cause field, and the agent sees only the status. The "because the card has been closed / the payment provider declined it" clause changes no tool result and no agent behavior, so dropping it changes no verdict. The duplicate rows are redundant but not wrong.

**Decision:** kept (Nit) — status: answered. Reason: Not a wording matter: the finding is about Initial-state lines a Given step cannot set. Kept; answered: the causes are the input's named terminal causes and the Given step sets status failed.

## R3-09 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | CO-01 / CO-08, Initial state of every cancellable scenario
Quote: "absent"
Evidence: The user's answer in review-packet.md l.43 (round 2 Q1) says: "Cancellable while placed or processing, no time limit." The packet also says, l.47: "No final-sale or non-cancellable flag." No rule in the spec says there is no time limit. CO-01 (agent-spec.md l.62) states a necessary condition only: "proposes cancelling an order only after a lookup shows it with status placed or processing". No scenario has an open order placed long before today (2026-11-05). Only CO-S02 (l.186) gives placed dates at all, and both are recent: 2026-11-03 and 2026-11-04. Every other cancellable scenario (CO-S01, S03, S09, S11–S28) leaves the order's placed date unset, although `list_orders` returns `placed_date` (Appendix A, l.1719). So a harness default, not the spec, decides what the agent sees. Take an agent that invents an age cutoff, for example refusing orders placed more than 30 days ago. It passes every scenario, and in production it turns away customers whose orders the store allows them to cancel. Input map: domain rule "no time limit" has no scenario. Initial-state map: placed_date is left open where the contract turns on it.
Pattern: A domain rule from the inputs that removes a limit (no time limit, no non-cancellable flag) has no scenario whose Initial state sits where an invented limit would bite. The value that rule depends on (placed date) is left out of Initial state.

**Verifier:** R3-09 | Real | Important | Could not refute. The packet records "Cancellable while placed or processing, no time limit." CO-01 gives only a necessary condition ("only after a lookup shows it with status placed or processing"). No rule states there is no time limit. Only CO-S02 sets placed dates, and both are recent (2026-11-03 and 2026-11-04). No scenario asserts that an old open order is cancellable.

**Decision:** kept (Important) — status: fixed

## R3-10 | Gap | Nit | sources: coverage:F2

[coverage F2]
F2 | Gap | Nit | CO-02, holding-back side (CO-S03)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: The rule holds back only when two conditions are both true: more than one open order, and no order named. The one-open-order side is tested: CO-S01 row 4 with rubric dimension "No order question asked" (l.1690, used by CO-S01 only). The other side is not: two open orders where the customer has already named one. CO-S03 (l.238–300) is the only scenario with two open orders and a named order ("Please cancel order HG-10482."), and it uses no dimension that fails a "which order?" question. Its User knows has no which-order pair, so the simulated user deflects that question and the agent goes on to pass. The only remaining signal is interaction precision, which §5.2 (l.1681) says is "never folded into the score". An agent that always asks "which order?" whenever two orders are open passes everything. evaluation-checklist.md, "Both directions are covered": "test only 'asks when unsure' and you get an agent that always asks."
Pattern: An "act only when A and B" rule has a holding-back scenario for "not A" but none for "A and not B".

**Verifier:** R3-10 | Real | Nit | Could not refute. CO-S03 is the only scenario with two open orders and a named order. No dimension or Forbidden line in it fails an unneeded "which order?" question. Interaction precision is "never folded into the score" (§5.2), and a rule settling the case is not a refutation unless a scenario or dimension asserts it.

**Decision:** kept (Nit) — status: fixed

## R3-11 | Gap | Nit | sources: coverage:F3

[coverage F3]
F3 | Gap | Nit | CO-03; failure rows l.99 and l.100
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: Three places name a request for a different refund amount as a trigger:
- CO-03 (l.68): "or for a different amount".
- The failure row at l.99: "or in a different amount".
- The changed-term row at l.100: "or in another amount".
No scenario row asks for a different amount:
- CO-S09 rows (l.596–598): Mastercard, store credit, PayPal.
- CO-S28 rows (l.1629–1630): Mastercard, store credit.
- CO-S08 and CO-S27: items only.
So rubric dimension "Refund terms explained" (l.1697) never grades the agent's answer to an amount request such as "just refund the items, not shipping", or "refund me $50 and keep the rest as credit". Input l.48 states the rule this protects: "refund amount = order total paid".
Pattern: A rule or failure-row condition that lists several triggers joined by "or" has scenario rows for only some of them.

**Verifier:** R3-11 | Style only | Nit | CO-03, the row at line 99 and the row at line 100 give one required behavior for all of "different payment method, store credit, different amount". CO-S09 and CO-S28 exercise that row, and the dimension "Refund terms explained" already says "offers no other payment method, amount or store credit". An extra variant for the amount trigger is a "one more scenario would be nice" preference.

**Decision:** dropped (Nit) — status: dropped. Reason: Agreed, preference: the finding's own Evidence shows one failure row gives one behavior for every trigger ("different payment method, as store credit, or in a different amount"), CO-S09 and CO-S28 exercise that row, and the dimension already says "offers no other payment method, amount or store credit"; asking for an amount row is "one more scenario would be nice".

## R3-12 | Gap | Nit | sources: coverage:F4

[coverage F4]
F4 | Gap | Nit | Failure handling, row "the order system did not answer a lookup of the customer's orders made before any CO-A2" (l.92); CO-S10
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: The user's change 4 (review-packet.md l.85) says: "Reads may be retried on timeout without limit; only commit calls are bounded." Appendix A (l.1715) repeats it: "The agent may repeat CO-A1 without limit". The row covers only the case where the lookup does not answer. It has no branch for a retried lookup that then answers. As written it fires whenever any lookup went unanswered and says "propose nothing", which conflicts with CO-01 (l.62): "When no lookup of the customer's orders has answered, it proposes nothing." CO-S10 (l.624) has "The order system does not answer any CO-A1", so no scenario has a lookup that fails once and then answers. cockburn-checklist.md: "A failure row that branches on a lookup covers every result of the lookup ... A missing branch is the else-branch a coder will invent."
Pattern: When an input makes a call retryable, the failure row for that call's timeout must cover the retry's possible results. The retry-then-success path also needs a scenario if its outcome differs from giving up.

**Verifier:** R3-12 | Real | Nit | Could not refute. The row at line 92 fires on "the order system did not answer a lookup ... made before any CO-A2" and says "propose nothing". Appendix A allows unlimited CO-A1 repeats, and CO-01 says only "When no lookup ... has answered, it proposes nothing." No branch covers a lookup that is unanswered once and then answered, and no scenario has one (CO-S10 never answers).

**Decision:** kept (Nit) — status: fixed
