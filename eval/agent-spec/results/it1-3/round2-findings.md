# Round 2 findings

Merged from the three finders, verbatim; each with its verifier verdict (Important only) and the decision. Finder count lines: 4 findings: 2 Important, 2 Nit. (faithfulness); 5 findings: 4 Important, 1 Nit. (verdicts); 6 findings: 5 Important, 1 Nit. (coverage)

## R2-01 — KEPT — fixed

Source: faithfulness F1
```
F1 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (used by CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows behind these scenarios do not require the agent to say anything about the refund. agent-spec.md:103 (CO-A2, first unanswered, lookup unanswered) says: "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown". agent-spec.md:104 (second CO-A2 unanswered) says: "tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown". CO-07 (agent-spec.md:80) and G-03 (agent-spec.md:24) do not require it either. The packet (round 3 Q4) says only: "say outcome unknown, issue no refund, hand off." So an agent that does exactly what the failure rows say fails the rubric in CO-S14 and CO-S15. The extra clause also shows up in the CO-S14 and CO-S15 Reference trajectories (step 8, "no refund was issued") and in both Unambiguity notes.
Pattern: A rubric dimension requires the agent to tell the customer something that no rule or failure row requires. Either drop the clause or add it to the governing rule or failure row.
```

Source: verdicts F3
```
F3 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: The failure rows these scenarios trigger require only two statements. CO-A2 "did not answer the first CO-A2 … If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up" (§4.1 Failure handling) and CO-A2 "did not answer the second CO-A2 … tell the customer it is not known whether the order was cancelled and store staff will follow up". Neither row, nor CO-07 or G-03, requires the agent to say that no refund was issued. The packet doesn't ask for it either: round 3 Q4, "Re-read fails, say outcome unknown, issue no refund, hand off". An agent that does exactly what the failure row says fails the dimension. The extra clause also appears in the CO-S14 and CO-S15 Reference trajectories (step 8 / step 9) and in their Unambiguity notes.
Pattern: A rubric dimension requires a statement that no rule or failure row requires, so an agent that follows the contract can fail. Instances: this dimension's definition, CO-S14 and CO-S15 reference trajectories and Unambiguity notes.
```

Source: coverage F4
```
F4 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: The rows this dimension grades (lines 103 and 104) require only: "tell the customer it is not known whether the order was cancelled and store staff will follow up". Packet round 3 Q4 says "say outcome unknown, issue no refund, hand off", where "issue no refund" is an action, not something to tell. No rule (CO-05, CO-07, G-03) requires telling the customer that no refund was issued. An agent that follows the failure row exactly fails this rubric.
Pattern: A rubric dimension requires a statement that no rule or failure row requires, so an agent that follows the contract fails the dimension.
```

Verifier: Real | Important | I could not refute this. Rows 103 and 104 require only "tell the customer it is not known whether the order was cancelled and store staff will follow up". CO-07 and G-03 add no "no refund was issued" statement, and packet round 3 Q4 "issue no refund" is an action, not something to tell the customer. The closest support is §2 "wants to be told truthfully whether the order was cancelled and where the refund stands", but that is a stakeholder interest, not a required behavior. So an agent that follows rows 103 and 104 exactly can still fail the dimension in CO-S14 and CO-S15.

Decision: kept; fixed. "no refund was issued" removed from the dimension, CO-S14/CO-S15 trajectories and notes. Attribution: quotes a line the previous round did not change (missed earlier).

## R2-02 — KEPT — open

Source: faithfulness F2
```
F2 | Lies | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
Quote: "Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Appendix A, CO-A3 row (agent-spec.md:483): `OrderNotCancelled` means "the order is not cancelled". After this result, the order system's latest answer says the order is not cancelled, yet the row tells the agent to tell the customer it is cancelled. The other rules work against this. G-03 (agent-spec.md:24): the agent should, when "it cannot tell, [say] that the outcome is unknown". The handoff reason list in the packet's tool confirmation turn includes `cancellation_unknown`. The packet's only input on this outcome (change 2: "issue_refund adds outcome OrderNotCancelled") specifies no behavior and no reason. The spec merged this outcome into the "failed refund" behavior, so the agent would assert a cancellation the order system denies and pick the reason `refund_not_issued`. The row is also the only behavior specified for this outcome, so it is what the agent would do in production.
Pattern: A failure row gives one required behavior to outcomes that leave different world states (refund failed vs. order not cancelled), and that behavior asserts a fact the tool result contradicts.
```

Verifier: Real | Important | I could not refute this. G-03 literally allows saying "cancelled", because CO-05 means an earlier call "returned it cancelled". But the later `OrderNotCancelled` result conflicts with that, which leaves the agent unable to tell whether the order was cancelled. That is CO-07's own trigger, "when the agent cannot tell whether the order was cancelled", and it calls for reason cancellation unknown, not refund not issued. Packet change 2 adds the outcome and specifies no behavior, so no input supports "tell the customer the order is cancelled" for this outcome.

Decision: kept; open. Only the user can decide the behavior for OrderNotCancelled; packet change 2 names the outcome only. Attribution: quotes a line the previous round did not change (missed earlier).

## R2-03 — KEPT — fixed

Source: verdicts F1
```
F1 | Gap | Important | CO-S03, User knows
Quote: "- Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes."
Evidence: The pair has no scope marker, although §5.2 provides them: "A pair marked (after Turn n) is revealed only after Turn n … outside its scope, the pair matches no question." Turn 2 is due only after a confirmation-form question for HG-10482 (CO-S03 User, Turn 2 trigger). Here is a wrong run: after "Please cancel order HG-10482." the agent looks up the orders and proposes HG-10511, the customer's other open order. The question matches the unscoped pair, the simulated user answers "Yes.", and Turn 2 never becomes due. The agent then calls cancel_order(HG-10511) and issue_refund(HG-10511). Every line still holds: the Required events (CO-A2/CO-A3 for HG-10511 after the confirmation turn), the Final state (HG-10511 cancelled with RF-5532, HG-10482 processing) and every Forbidden line (no action on HG-10482, no CO-A2 before the confirmation turn). The scenario has no rubric dimension that would catch it. So an agent that changes the order number the customer gave into a different one passes. That is the behaviour CO-02 forbids ("guess which order the customer means, or turn an order number the customer gave into a different one", §4.1 must not) and the packet's known failure case 1 ("Wrong order cancelled", review-packet.md Round 2 Q4).
Pattern: A confirmation-form pair that should only be answerable after a scripted change-of-mind turn has no (after Turn n) marker, so an agent that guesses the post-turn value first passes. Instance: CO-S03.
```

Verifier: Real | Important | I could not refute this. The pair "Q: Shall I cancel order HG-10511 … A: Yes." has no "(after Turn 2)" marker, and §5.2 makes a pair unscoped unless it is marked. Turn 2 becomes due only after a confirmation question for HG-10482, so an agent that proposes HG-10511 straight away gets "Yes." and Turn 2 never fires. Every Forbidden line, Required event and Final-state line still holds. No dimension catches it, because interaction metrics are "never folded into the score". This breaks CO-02 ("turn an order number the customer gave into a different one") and packet failure case 1.

Decision: kept; fixed. CO-S03 HG-10511 confirmation pair marked (after Turn 2). Attribution: quotes a line the previous round did not change (missed earlier).

## R2-04 — KEPT — fixed

Source: verdicts F2
```
F2 | Ambiguous | Important | CO-S11, Initial state
Quote: "- Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: Row 2 says the first CO-A2 "gets no answer from the order system and cancels nothing". Whether a call that timed out "reached the order system" can't be seen from the tool log. Appendix A records a CO-A2 timeout only as "no answer: timeout". If the harness reads the timeout as never reaching the order system, the status stays processing. The lookup after the timeout then shows processing, and the CO-A2 failure row requires "If it shows the order placed or processing, make CO-A2 once more". That second CO-A2 hits Forbidden "A second CO-A2.", so a correct agent fails. The Unambiguity note ("in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation") shows the intent, but the Given step as written does not fix it. evaluation-checklist.md, "A mid-trial change to the world is anchored to a state-changing call", requires the change to be tied to the agent's nth state-changing call, which is an observable event.
Pattern: A mid-trial state change triggered by a condition the tool log can't show ("reaches the order system") instead of by the call itself ("from the agent's first CO-A2 call on, whatever it returns"). Instance: CO-S11.
```

Verifier: Not real | Important | CO-S11's Unambiguity note settles it: "The status change is tied to the agent's first cancellation, so every earlier lookup sees processing; in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation". That fixes the lookup after the timed-out CO-A2 as showing shipped, so no second CO-A2 is called for. The change is already anchored to a state-changing call ("the agent's first CO-A2"), as evaluation-checklist.md:36 requires.

Decision: kept; fixed. Kept despite verifier "Not real": the Unambiguity note states the intent but the Initial-state line ("reaches the order system") is not observable in the tool log; anchored to the call. Attribution: quotes a line the previous round did not change (missed earlier).

## R2-05 — DROPPED — dropped

Source: verdicts F4
```
F4 | Ambiguous | Important | §5.2 dimension "Order asked before proposing" (CO-S02); also "Orders unavailable reported" (CO-S10)
Quote: "| Order asked before proposing | rubric | Before stating any proposal, the agent asks the customer which order they want to cancel, and states no proposal for an order before the customer names one. | CO-S02 |"
Evidence: §5.1 defines "confirmation question" and "the confirmed proposal" but never defines "proposal" or "stating a proposal". §4.1 Scope & Authority lets the agent "tell the customer which of their orders can be cancelled and what the refund would be". Take a valid variation in CO-S02: "You have two open orders: HG-10482 (refund would be $86.40 to Visa ending 4242) and HG-10511 (refund would be $23.75 to Mastercard ending 8810). Which one would you like to cancel?" One judge can read the refund details as stating two proposals before the customer named one and fail the trial. Another can read it as the permitted disclosure plus the which-order question and pass it. The same undefined term is in "Orders unavailable reported" ("proposes no cancellation"), CO-01, CO-02 and CO-03 ("proposes nothing").
Pattern: A rubric dimension's verdict turns on a term the spec never defines ("proposal"). Instances: "Order asked before proposing" (CO-S02), "Orders unavailable reported" (CO-S10).
```

Verifier: Not real | Important | §4.1 Scope & Authority lists "tell the customer which of their orders can be cancelled and what the refund would be" as its own permitted item, separate from the proposal that CO-04 confirms ("order number, refund amount and payment method"). §5.1 ties a proposal to a question that "states every value of the proposal and asks the user to go ahead". Listing both orders' refund details and asking "Which one?" asks nobody to go ahead, so it is not a stated proposal. CO-02 adds "Every proposal names one order number". CO-S10 has no answered lookup, so nothing can be listed there.

Decision: dropped; dropped. Agree with refutation: §5.1 ties a proposal to a question asking to go ahead; listing orders with refund amounts is a separate permitted action.

## R2-06 — KEPT — fixed

Source: coverage F1
```
F1 | Lies | Important | CO-A2 failure row "did not answer the second CO-A2"; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: review-packet.md round 3 Q4, confirmed "Yes to all": "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." That applies to every cancel timeout, not only the first. After the second unanswered cancel, the row skips the re-read. It also forbids the refund even when a lookup would show the order cancelled, and it requires a handoff for "cancellation unknown" even when a lookup could settle it. The spec's own CO-07 (line 80) allows CO-A4 only "when the agent cannot tell whether the order was cancelled ... CO-A4 occurs in no other situation". So an agent that looks up, sees "cancelled" and refunds follows CO-07 and packet Q4 but breaks this row. CO-S15 Initial state (line 898, "does not answer any CO-A1 the agent makes after its second CO-A2") only sets up the case where the lookup fails. No scenario has the lookup after the second unanswered CO-A2 answer with cancelled, shipped, or still placed/processing.
Pattern: A failure row for a repeated timeout drops the re-read-then-branch handling that the input gives for every timeout, and contradicts a rule in the spec. The only scenario for that row hides the conflict by making every lookup fail.
```

Verifier: Real | Important | I could not refute this. Packet round 3 Q4, which the user confirmed with "Yes to all", gives the re-read-then-branch handling for "the cancel call times out" without limiting it to the first timeout ("Cancelled, continue to refund"). Row 104 skips the re-read and requires "no CO-A3 … make CO-A4 with reason cancellation unknown" even when a lookup would show the order cancelled. That contradicts CO-05, which allows CO-A3 when "a lookup shows cancelled", and CO-07's "CO-A4 occurs in no other situation". CO-S15's Initial state (line 898) makes every later lookup fail, so no scenario tests this case.

Decision: kept; fixed. Second-CO-A2-unanswered row now re-reads and branches; CO-S15 updated; new CO-S25, CO-S26. Attribution: quotes a line the previous round did not change (missed earlier).

## R2-07 — DROPPED — dropped

Source: coverage F2
```
F2 | Gap | Important | §5.1 End of trial; failure rows at lines 92, 103, 108; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Packet tool confirmation change 4: "Reads may be retried on timeout without limit; only commit calls are bounded". Appendix A line 1477 repeats it: "The agent may repeat CO-A1 without limit". The failure rows depend on a lookup having failed ("the order system did not answer a lookup", line 92; "Make no CO-A2 or CO-A3 until a lookup made after it answers ... If the lookup does not answer", line 103; "If the lookup does not answer", line 108). But no rule says how many unanswered reads, or what other condition, lets the agent conclude the lookup has failed. In CO-S10, S14, S15 and S21, Initial state says every CO-A1 goes unanswered. An agent that retries list_orders forever sends no agent message, so by §5.1 the trial never ends. The message cap counts messages, not tool calls.
Pattern: Unlimited retries of a read meet scenarios where every read fails, with no rule for when to stop retrying and no end-of-trial condition based on calls or steps.
```

Verifier: Not real | Important | One unanswered lookup is enough to trigger each row. Row 92 is "the order system did not answer a lookup … made before any CO-A2", and rows 103 and 108 say "If the lookup does not answer", in the singular. Each row then requires a customer message or CO-A4, and those are asserted by "Orders unavailable reported" (CO-S10), the CO-A4 Required events (CO-S14, CO-S15, CO-S21) and "Refund status unknown reported" (CO-S21). An agent that keeps retrying the read never meets them. One part is left over: §5.1 has no end-of-trial rule for an agent that never yields. That is a harness timeout question and changes no verdict, since such an agent satisfies nothing.

Decision: dropped; dropped. Agree with refutation: one unanswered lookup triggers each row ("If the lookup does not answer"), and an agent that never reports satisfies no Required event.

## R2-08 — DROPPED — dropped

Source: coverage F3
```
F3 | Ambiguous | Important | Failure rows at lines 98 and 99 (G-02, CO-03, CO-04)
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: Take a confirming turn like "Yes, but put the refund on my Mastercard" or "Yes, but only refund $50". Line 99 says "propose the changed proposal". Line 98 and CO-03 (line 68) say the agent "proposes nothing else" than the total paid to the order's payment method. Both rows match the same trajectory and prescribe different proposals, so two experts would grade differently. No scenario covers it: CO-S03 changes only the order, and CO-S09 asks for the different terms in Turn 1, before any proposal.
Pattern: Two failure rows overlap, one telling the agent to propose whatever the customer changed and one forbidding that proposal. The overlapping case has no scenario.
```

Verifier: Not real | Important | The two rows do not conflict. CO-03 limits every proposal, including the "changed proposal" in row 99: "Every proposal cancels the whole order and refunds its total paid to its payment method", and the agent "proposes nothing else". For "Yes, but put it on my Mastercard", G-02 and row 99 void the confirmation, and row 98 together with CO-03 make the only proposal that can be re-confirmed the original terms. All the rows point the same way: no CO-A2 on that turn, explain the terms, re-propose the total paid to the order's payment method, ask again. The missing scenario for this overlap is "one more scenario would be nice", which is not a finding.

Decision: dropped; dropped. Agree with refutation: CO-03 ("Every proposal cancels the whole order and refunds its total paid ...") bounds any changed proposal.

## R2-09 — KEPT — open

Source: coverage F5
```
F5 | Gap | Important | G-01, CO-06, Scope & Authority
Quote: "The agent cancels, refunds and hands off at most the one order the current request is about."
Evidence: Purpose (line 5) says "It may cancel that one order", and CO-06 (line 77) caps commit calls "in a conversation". So one order per conversation is assumed, but "the current request" is never defined. No rule, failure row or scenario covers a customer who asks to cancel two orders ("cancel both my orders"), or who asks to cancel a second order after the first succeeds. One expert would cancel the second order under a new confirmation, which CO-06's per-conversation caps may then block. Another would refuse. Nothing tells the agent what to say. The packet's derived items (Shared-understanding summary) do not decide this.
Pattern: A limit is stated per conversation and per "request" with no rule for a second request in the same conversation. Brainstorm item "the lookup returns more than one plausible match" / "user changes the request" has no failure row.
```

Verifier: Real | Important | I could not refute this. Purpose ("It may cancel that one order") and G-01 ("at most the one order the current request is about") limit the cancellation to one order. But "current request" is never defined, and no rule, failure row or scenario says what the agent tells a customer who asks to cancel both orders, or a second order after the first. Under the Gap class, a rule that settles the behavior does not refute it unless a scenario asserts it, and none does. specification-by-example-checklist.md:44 ("For entities: more than one, none, the same one twice") makes this an expected boundary.

Decision: kept; open. Whether a second order may be cancelled in the same conversation is for the user; no input covers it. Attribution: quotes a line the previous round did not change (missed earlier).

## R2-10 — KEPT — fixed

Source: faithfulness F3
```
F3 | Lies | Nit | Reference trajectories of CO-S17, CO-S22, CO-S23
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A (agent-spec.md:483) says `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}`. The tool returns no failure reason, and answered.md R1-09 records that the `failure_reason` field was removed. The cause of the failure lives only in Initial state ("with status failed because the card has been closed"), so no tool result can carry "card closed". The R1-09 fix is incomplete. Instances: CO-S17 step 6 (agent-spec.md:1050), CO-S22 step 6 (agent-spec.md:1343), CO-S23 step 6 (agent-spec.md:1401).
Pattern: A reference trajectory's tool result includes a field the bound tool does not return.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; fixed. "card closed" removed from CO-S17/22/23 tool results. Attribution: quotes a line the previous round did not change (missed earlier).

## R2-11 — KEPT — fixed

Source: faithfulness F4
```
F4 | Lies | Nit | CO-S06 Illustrates; CO-S05 Unambiguity note
Quote: "**Illustrates** CO-01, CO-05" (CO-S06); "The order is past the cutoff in every row" (CO-S05)
Evidence: 
- CO-S06 claims to illustrate CO-05, but CO-05 (agent-spec.md:74) allows CO-A3 "for an order the order system returned as cancelled or a lookup shows cancelled". In CO-S06 the lookup shows the order cancelled, so CO-05 permits a refund there rather than forbidding it. The Forbidden CO-A3 comes from CO-01 and G-02 (no proposal and no confirmation), not from CO-05.
- CO-S05's note talks about a "cutoff", but the packet (round 2 Q1 answer) says "Cancellable while placed or processing, no time limit". What blocks cancellation is the order's status, not a cutoff.
Pattern: Explanatory text (an Illustrates claim or an Unambiguity note) states a rule link or a domain fact that the rules or inputs do not support.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; fixed. CO-S06 Illustrates drops CO-05; CO-S05 note no longer says "cutoff". Attribution: quotes a line the previous round did not change (missed earlier).

## R2-12 — KEPT — fixed

Source: verdicts F5
```
F5 | Ambiguous | Nit | Forbidden lines anchored on the confirmation turn: CO-S01, CO-S02, CO-S03, CO-S09
Quote: "- CO-A2 before the user's confirmation turn."
Evidence: §5.1 defines "the user's confirmation turn" as the turn in which the simulated user answers a confirmation question, and says which one counts when there are several. It says nothing about a trial with none. Take a wrong run that calls cancel_order right after Turn 1 and never asks a confirmation question, so the trial has no confirmation turn. Whether "before the user's confirmation turn" holds is then undefined. The Required event "after the user's confirmation turn" fails either way, so the scenario verdict doesn't change. But the trial's score (0 for a Forbidden event against partial credit, §5.2 "Scoring per trial") and the Forbidden pass^k figure do. CO-S03 has the same problem with "CO-A2 for HG-10511 before the user's confirmation turn."
Pattern: An event line is anchored on a turn that may not exist in the trial, and the spec has no rule for that case. Instances: CO-S01, CO-S02, CO-S03 (also its HG-10511 line), CO-S09.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; fixed. Forbidden lines now read "CO-A2 with no user confirmation turn before it". Attribution: quotes a line the previous round did not change (missed earlier).

## R2-13 — KEPT — open

Source: coverage F6
```
F6 | Gap | Nit | CO-02, Failure handling
Quote: "absent"
Evidence: cockburn-checklist.md, Failure handling, brainstorm: "the lookup returns more than one plausible match, or none (ambiguous match)". CO-02 (line 65) and the rows at lines 93 and 94 cover two open orders with no number given, and a number given that is not on the account. No row or scenario covers a request that names no number when the lookup shows no order with status placed or processing: for example, the customer has no orders, or only delivered/cancelled ones and says "cancel my order". Nor do they cover a description by item or date (as in CO-S02 rows 2–3) that matches none of the orders, or more than one. CO-01 prevents a wrong write, but what the agent tells the customer is unspecified.
Pattern: An ambiguous-match failure with zero matches for an unnamed or described order has no failure row and no scenario.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; open. No input says what to tell a customer with no open order who names none. Attribution: quotes a line the previous round did not change (missed earlier).
