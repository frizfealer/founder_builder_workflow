# Round 3 findings (merged)

8 findings: 5 Important, 3 Nit.

### R3-01 (from faithfulness F1; duplicate: verdicts F3)

R3-01 | Lies | Important | CO-07 (Contract), against CO-S28 Forbidden and Illustrates, §1 Purpose, §2 Offstage stakeholders
Quote: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation."
Evidence: The fix for R2-06 added CO-S28 but did not change CO-07, so the fix is incomplete (answered.md R2-06: "new CO-S28, an already cancelled order with no refund ... refund, cancel and handoff are forbidden").
- CO-S28 Initial state (agent-spec.md lines 1595-1596): "Order HG-10420 belongs to the customer, with status cancelled ..." and "No refund exists for HG-10420." The lookup therefore shows the order cancelled with no refund pending or issued. CO-01 and CO-04 bar any CO-A3, so CO-06 allows no retries at all. CO-07's first clause is met as written and requires a CO-A4.
- CO-S28 says the opposite. Forbidden (line 1618): "CO-A4 at any point." Its Illustrates line (1632) lists CO-07. Row 2's Turn 1 (line 1625) is "I cancelled HG-10420 last week but never got my money back. Can you refund it?", which is exactly a cancelled order whose refund is unfinished.
- The input backs the scenario, not the rule. review-packet.md, shared-understanding summary: "An already cancelled order: the agent reports that and changes nothing."
- The same unqualified trigger appears in two more places:
  - §1 Purpose (line 5): "it hands the order to store staff when it cannot finish the refund"
  - §2 Offstage stakeholders (line 11): the customer-support team "wants every order whose refund is unfinished or whose cancellation is uncertain handed to it"
- An agent that follows CO-07 fails CO-S28. A builder who implements CO-07 as written ships a handoff that the input forbids.
Pattern: A rule's trigger, and the stakeholder or purpose lines that state it, cover a state the inputs say must change nothing. Limit CO-07's first clause to an order cancelled by this conversation's CO-A2 for which the agent made at least one CO-A3, and word §1 and §2 to match.

Duplicate report (verdicts F3), kept for its evidence:
R3-01-dup | Ambiguous | Important | CO-07; CO-S28 (Illustrates, Forbidden)
Quote: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation."
Evidence: CO-S28's Initial state (lines 1595-1596) has "HG-10420 ... status cancelled" and "No refund exists for HG-10420". Read literally, CO-07's trigger holds: the order is cancelled, and its refund is not shown pending or issued after the CO-A3 retries CO-06 allows, which here are none. Yet CO-S28 forbids "CO-A4 at any point." (line 1618) and lists CO-07 under Illustrates (line 1632). Its Unambiguity note decides the case from the shared-understanding summary ("An already cancelled order: the agent reports that and changes nothing", review-packet.md, Shared-understanding summary), not from CO-07. The same reading applies to a returning customer whose order ended as in CO-S23 (cancelled, refund RF-5531 failed, no follow-up task): CO-07 reads as requiring a handoff, while the input says change nothing, and no scenario decides it. One builder reads "the order" as the order this conversation cancelled and "after the retries" as retries actually made, and hands off nothing. Another hands off and fails CO-S28. R2-06 was fixed by adding CO-S28, but CO-07's text was not changed.
Pattern: A rule's trigger is stated on world state ("the order is cancelled") rather than on the agent's own actions in this conversation, so it also fires for records that were already in that state. Anchor CO-07 to "an order the agent cancelled in this conversation (CO-A2 returned cancelled or a lookup after its CO-A2 shows cancelled) whose refund ... after the CO-A3 calls CO-06 allows".

Verifier: R3-01 | Real | Important | Partial refutation only. Scope must-not (line 44) says "cancel, refund or hand off any order other than the one the customer confirmed". In CO-S28 the customer confirmed nothing, so this line settles CO-S28's verdict: a handoff is barred. It does not change what CO-07 says. CO-07's trigger, "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4", still literally covers an order that was already cancelled with no refund, and "CO-A4 occurs in no other situation" does not exclude that order. So two rules conflict, and an agent following CO-07 fails CO-S28. The same unqualified trigger in §1 ("hands the order to store staff when it cannot finish the refund") and §2's support-team interest still stands, as does the duplicate's returning-customer case like CO-S23. No clause limits CO-07 to an order cancelled in this conversation.
Decision: kept | Status: open | The fix changes CO-07's text, so it stops at the rule: proposed rule change for the user. The verifier's partial refutation (Scope must-not 'hand off any order other than the one the customer confirmed') settles CO-S28's verdict but not CO-07's conflicting text.

### R3-02 (from faithfulness F2)

R3-02 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A gives CO-A3's result shape as `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` (line 1891), with no field for why it failed. The R1-04 fix removed `failure_reason` from Appendix A on purpose (answered.md R1-04: "Appendix A CO-A3 outcome no longer names a `failure_reason` field"). The three trajectories still show a tool result that carries the cause:
- CO-S17 step 6 (line 1050)
- CO-S22 step 6 (line 1343)
- CO-S23 step 6 (line 1401)
No dimension needs the cause, so no verdict changes. A builder reading the trajectories would still expect the tool to return a reason it does not return.
Pattern: A reference trajectory's tool result contains a value that the bound tool's result shape does not have. Trim each such result to the fields Appendix A lists (here "refund RF-5531, failed"), and leave the cause in Initial state only.

Verifier: R3-02 | Style only | Nit | The finding concedes that no dimension needs the cause and no verdict changes. The trajectory is not an input to the agent, so agent behavior does not change either. Trajectory arrows in this spec give the outcome in the words of Appendix A's Outcomes cell, not literal fields: line 994 has "→ payment provider temporarily unavailable" for `ProviderUnavailable`, and line 1051 has "→ task created" for `{task_id}`. Appendix A's outcome is "refund failed (the payment method is closed or expired, or the provider declined): returns the refund with `status: \"failed\"`". So "failed, card closed" names that outcome and does not add a result field.
Decision: dropped | Status: dropped | Style-only Nit. The finding's own Quote, '6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed.', describes the outcome in the words of Appendix A's outcome cell, which includes the cause in parentheses. Other arrows do the same ('→ payment provider temporarily unavailable', '→ task created'). The finding is about how the arrow is phrased, not a returned field, so it is wording; dropped.

### R3-03 (from coverage F1)

R3-03 | Gap | Important | CO-S28 (row 2), §5.2 dimension "Already cancelled reported"; G-03 refund clause; Failure handling row "the lookup shows the named order with status cancelled"
Quote: "| Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06, CO-S28 |"
Evidence: In CO-S28 row 2 the customer asks directly about the refund: "I cancelled HG-10420 last week but never got my money back. Can you refund it?" (agent-spec.md line 1625). Initial state: "No refund exists for HG-10420." (line 1596).
- G-03 (line 24) says the agent "tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it." The scope must-not list (line 48) says the same, and so does the offstage interest (line 11): the support team "wants no customer told a refund is on its way when it is not".
- The only dimension CO-S28 uses forbids just two claims: that the agent cancelled the order, or that it "issued a refund in this conversation". A run that says "Your refund is already being processed and should reach your Visa in 5 to 10 business days" fails no line of CO-S28. That one sentence breaks G-03, the must-not list and round 3 Q1 ("The agent promises nothing about when the money arrives"). "No arrival date promised" is used only by CO-S01 (line 1870).
- The rule side is open too. Row 93 (line 93) requires only "Tell the customer the order is already cancelled". No rule or row says what the agent tells a customer whose cancelled order has no refund. So nothing protects the primary-actor interest "wants to be told truthfully ... where the refund stands" (line 9) in the one scenario where the customer asks that question.
Pattern: when the user asks about the refund directly and no refund exists, no dimension in that scenario asserts G-03's refund-status clause, and the scenario's dimension forbids only the agent's own new actions, not false claims about the existing state.

Verifier: R3-03 | Real | Important | Could not refute. "Already cancelled reported" (line 1860, used by CO-S06 and CO-S28) forbids only "says it cancelled the order or issued a refund in this conversation". That covers claims of new actions, not a false claim that a refund already exists or is pending, which is the case CO-S28 row 2 ("never got my money back. Can you refund it?") invites. G-03 and the must-not line "tell the customer a refund is pending or issued when the order system has not shown it" settle the rule. But no scenario or dimension asserts that rule when an order is cancelled and has no refund ("No arrival date promised" and the refund-status dimensions are not used by CO-S28). So a run that says "your refund is being processed" passes CO-S28.
Decision: kept | Status: fixed | 'Already cancelled reported' extended; 'No arrival date promised' added to CO-S28.

### R3-04 (from coverage F2)

R3-04 | Gap | Important | §4.1 Failure handling; Scenarios; G-01, CO-02, CO-06
Quote: "absent"
Evidence: Nothing in the spec covers a customer who asks to cancel more than one order, either in one request ("cancel both HG-10482 and HG-10511") or by asking for a second order after the first is done. Three spec lines make this the spec's own problem:
- CO-06 (line 77): "The agent makes at most two CO-A2 ... in a conversation ... It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing". Read literally, this bars cancelling a second open order in the same conversation.
- G-01 (line 18): "at most the one order the current request is about".
- CO-02 (line 65): "Every proposal names one order number".

The inputs set no one-order-per-conversation limit. Round 1 Q1/Q2 and round 2 Q1 limit only status and whole-versus-partial. Known failure case 1 has a customer with two open orders (review-packet.md, Round 2 Q4). No failure row says what the agent tells a customer who asks for two orders: cancel one and refuse the other, ask which one first, or tell them to start again. No scenario has such a request. The use-case checklist's brainstorm list (cockburn-checklist.md, "Failure handling") includes "the user goes silent or changes the request mid-way" and "the lookup returns more than one plausible match". Its "Each interest maps to at least one rule" item applies to the primary actor, who "wants the order they mean cancelled" (line 9) and here means two. A coder will invent the branch: either silently drop the second order or cancel both against CO-06.
Pattern: a limit the spec sets on how many orders one conversation may act on has no failure row and no scenario for a request that goes over it.

Verifier: R3-04 | Real | Important | Could not refute. CO-06 (line 77) says "makes at most two CO-A2 ... It makes a second CO-A2 only after the first went unanswered". With G-01's "at most the one order the current request is about", that settles that a second order is not cancelled. But it is a rule, and no failure row or scenario asserts what the agent does or says when a customer asks to cancel two orders. The inputs set no one-order-per-conversation limit (packet rounds 1 to 3). cockburn-checklist.md's Failure handling list includes "the user ... changes the request mid-way".
Decision: kept | Status: open | Whether one conversation may cancel several orders is not in the inputs; only the user can decide.

### R3-05 (from coverage F3)

R3-05 | Gap | Nit | §4.1 Failure handling rows "more than one of the customer's orders has status placed or processing ...", "the lookup shows the named order with status shipped or delivered", "the lookup shows the named order with status cancelled"
Quote: "| any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean | Ask which order; propose nothing until the customer names one. | CO-02 |"
Evidence: When the request names no order, the spec covers only some lookup results:
- more than one open order: row 90 and CO-S02;
- exactly one open order: CO-S01 row 4 ("Can you cancel my order? I don't need it anymore.", line 159).

No row covers a request that names no order when the lookup shows no open order. That includes a customer with no orders at all, the "nothing found" result, and one whose orders are all shipped, delivered or cancelled. Rows 92 and 93 apply only to "the named order", and CO-01 (line 62) says what to tell the customer per order, not which of several closed orders the request is about. cockburn-checklist.md, "Failure handling": "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." No verdict changes, because CO-01 already forbids any proposal in this case. The agent's reply is left for a coder to invent.
Pattern: the lookup results for a request that names no order are covered only for one and for several open orders. The zero-open-order result (none at all, or only closed orders) has no row.

Verifier: R3-05 | Real | Nit | Could not refute. CO-01 (line 62) says "proposes cancelling an order only after a lookup shows it with status placed or processing", which settles that nothing is proposed. Rows 92 and 93 apply only to "the named order", and row 90 needs more than one open order. No rule or row says what the agent tells a customer who names no order and has no open order: no orders at all, or only shipped, delivered or cancelled ones. cockburn-checklist.md: "A failure row that branches on a lookup covers every result of the lookup". This changes no verdict but leaves the reply for a coder to invent, so it is not Style only.
Decision: kept | Status: fixed | New failure row for no open order when none is named; CO-S05 row 4.

### R3-06 (from verdicts F1)

R3-06 | Ambiguous | Important | §5.2 dimension "Refund status reported" (CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25, CO-S27, CO-S29); G-03
Quote: "| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the refund status the data-variant row gives, or pending when the row has no refund status column, and states no other status for it. |"
Evidence: The spec uses "issue" and "issued" for two things.
- As the action: Scope line 39 "CO-A3 issue the refund for the cancelled order"; Appendix A line 1891 "`issue_refund(order_number)`"; "Already cancelled reported" (line 1860) "never says it ... issued a refund in this conversation"; "Cancellation outcome unknown reported" (line 1865) "that no refund was issued"; "Shipped order explained" (line 1859) "never says ... a refund was issued".
- As a refund status: G-03 (line 24) "tells the customer a refund is pending or issued only when the order system returned that refund with that status"; Appendix A value comparison (line 1883) lists "issued" as a status word.
Take a plausible CO-S01 row 1 final message after RF-5531 comes back pending: "I've cancelled HG-10482 and issued refund RF-5531 for $86.40 to your Visa ending 4242; it's pending." One judge reads "issued" as the action the agent took and passes the run. Another reads it as stating status issued, which is a second status, and fails it under "states no other status for it" and under G-03. The same wording question comes up in "Refund status unknown reported" (line 1872, "never says the refund is pending, issued or failed"), where the run says "I couldn't confirm whether the refund was issued", and in "Refund not issued reported" (line 1866), which requires "the refund has not been issued" and also forbids saying it is "issued".
Pattern: A word that names both a tool action and a status value is used in a rubric that bans other status values. Say in §5.2 that "issued" counts as a status only when the message says the refund's status or state is issued, or rename the action ("create the refund") everywhere the spec means the call.

Verifier: R3-06 | Real | Important | Could not refute. No §5.1 or §5.2 clause says that "issued" used as a verb for the action is not a status statement. Appendix A's value comparison (line 1883) lists "issued" among the status words, which supports the finding. So "I've ... issued refund RF-5531 ...; it's pending" can be graded either way under "states no other status for it" in "Refund status reported".
Decision: kept | Status: fixed | The status dimensions now say how 'issued' as a verb is read.

### R3-07 (from verdicts F2)

R3-07 | Ambiguous | Important | CO-S29, User knows / Required events; Failure handling row "the customer asked to cancel only some of an order's items"
Quote: "- Q: Would you like to cancel the whole order HG-10530 instead? A: Yes, cancel the whole order."
Evidence: The customer's wish to cancel the whole order reaches the agent only as a User-knows answer, and §5.2 (line 1842) says the simulated user "reveals a User-knows answer only when the agent asks the matching question". No rule tells the agent to ask that question. Row 94 says only "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order", and CO-03 (line 68) adds "proposes nothing else". In CO-S08 the same question is "(optional)" (line 516), so an agent that only states the rule passes there. Take a rule-compliant run in CO-S29: "Only the whole order can be cancelled, not single items. Let me know if you'd like to cancel all of HG-10530." That message asks nothing, so under §5.1 "End of trial" (line 1826) the trial ends. Both Required events (CO-A2 and CO-A3 for HG-10530) are then missing and the run fails. The identical behavior passes CO-S08. The agent cannot know from the inputs which of the two customers it is facing, so the CO-S29 verdict depends on a question the contract never requires. This is a gap left by the R2-07 fix (new CO-S29).
Pattern: A scenario's acting branch is reachable only through a User-knows answer to a question no rule requires. Either make the question a rule (row 94: "ask whether the customer wants to cancel the whole order"), or script the customer's whole-order request as a User turn triggered by a defined event.

Verifier: R3-07 | Real | Important | Could not refute. Row 94 says only "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order", and CO-03 says "proposes nothing else". Neither requires the agent to ask the whole-order question. CO-S29 makes that question a required User-knows pair, while CO-S08 marks the same question "(optional)". CO-S29 row 2 and CO-S08 row 2 have the identical Turn 1 ("Please take the linen napkins off HG-10530 and refund me for them."), so the agent cannot tell the two cases apart. Under §5.1's End of trial ("the first agent message that asks the user nothing"), a run that follows the rules but does not ask the question ends and fails CO-S29's Required events. Whether "Let me know if..." counts as a question also needs judgment.
Decision: kept | Status: fixed | CO-S29's whole-order request is now a scripted Turn 2 after the agent's first agent message.

### R3-08 (from verdicts F4)

R3-08 | Ambiguous | Nit | Scope & Authority must-not; §5.2 "No arrival date promised" (CO-S01)
Quote: "- promise a date by which the refunded money arrives."
Evidence: The dimension (line 1870) checks something broader: "The agent says nothing about when, or within how many days, the refunded money arrives." The input agrees with the dimension. Round 3 Q1 says "The agent promises nothing about when the money arrives", after round 2 Q2 had proposed "money arrives in 5 to 10 business days". Take a run that says "Refunds usually show up within 5 to 10 business days." By the Scope line it promises no date and passes. By the dimension it fails. The dimension is the CO-S01 grader, so the verdict there is fixed. The Scope line still tells a builder that a day-range estimate is allowed, and no other success scenario uses the dimension to catch it.
Pattern: A rule states a narrower ban than the input and the rubric that grades it. Reword the Scope line to match the input: "say anything about when, or within how many days, the refunded money arrives."

Verifier: R3-08 | Real | Nit | Partial refutation only. "No arrival date promised" (line 1870), "says nothing about when, or within how many days", fixes CO-S01's verdict, as the finding concedes. The Scope line "promise a date by which the refunded money arrives" is still narrower than round 3 Q1's "promises nothing about when the money arrives". A promised day range ("within 5 to 10 business days", which round 2 Q2 proposed and round 3 Q1 dropped) is a promise about when but not a promise of a date. So the rule a builder implements allows what the input bars. One thing weakens the finding: its example says "usually", which may not be a "promise" under the input's own verb either.
Decision: kept | Status: fixed | Scope line widened to match round 3 Q1 and the dimension.

Verifier count line: Count: 7 Real, 0 Not real, 1 Style only.
