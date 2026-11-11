# Round 2 findings (merged, verbatim)

11 findings: 7 Important, 4 Nit.

Each finding is the merged text sent to the verifier, then the verifier's line, then the decision.

R2-01 | Lies | Important | Failure handling (CO-A3, second CO-A3 unanswered), CO-S20 Reference trajectory and dimension "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md, Round 3 Q3, confirmed with "Yes to all": "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet." The user decided the message for this branch is "not confirmed yet". The spec swaps in the firmer claim "has not been issued". Other instances:
- agent-spec.md line 1244 (CO-S20 Reference trajectory step 10): "Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
- line 1248 (CO-S20 Unambiguity note): "rubric dimension 'Refund not issued reported' checks the agent said ... the refund has not been issued"
- line 1659: dimension "Refund not issued reported" requires "the refund has not been issued" and lists CO-S20 under Used by.

An agent that follows the confirmed decision and says "your refund is not confirmed yet; store staff will follow up" can fail CO-S20 on the rubric.
Pattern: The required customer message for a branch differs from the wording the user confirmed for that branch. Check every failure row, reference trajectory step and rubric definition that states what the agent tells the customer against the interview's confirmed wording for that case.
(Source: faithfulness finder)

**Verifier (sonnet):** Not real | Important | Review-packet round 2 Q4 case 2 (confirmed with "Yes to all") supports the spec's wording: "Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success". The confirmed handoff reason is also `refund_not_issued`. In CO-S20 variant 1 the lookup shows a failed refund, the same known state as case 2. So "the refund has not been issued" is supported by an input and is true under G-03. The only part I could not close is variant 2 (lookup shows no refund). There Q3's "not confirmed yet" is a softer wording, but "no refund exists" still makes "not issued" true. I would keep this as a Nit-level wording note at most.

**Decision:** kept | severity Important | status: fixed | Verifier Not real, quoting packet Round 2 Q4 case 2 ("refund not issued, state known"). Not dropped: that clause is about a refund call that returned an error, while the branch is case 3 (timeout, then re-read), for which Round 3 Q3 confirmed "say the refund is not confirmed yet"; the verifier itself could not close row 2. Wording changed in the row, CO-S20 and a new dimension.

---

R2-02 | Lies | Important | Failure handling, CO-A3 row "returned the refund with status failed, or reported the order not cancelled"
Quote: "Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md, tool confirmation turn, change 2: "issue_refund adds outcome OrderNotCancelled." agent-spec.md line 1681 (Appendix A) defines that outcome as "the order is not cancelled: `OrderNotCancelled`". When the order system answers CO-A3 with OrderNotCancelled, its latest word is that the order is not cancelled. No input supports telling the customer "the order is cancelled" at that point. The packet's shared-understanding summary also gives the cancellation-uncertain case its own handoff reason ("One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument"; reason cancellation_unknown). This row instead files it under refund not issued. This is not the same as R1-01: R1-01 removed the CO-S17 row that injected this outcome, but the failure row's instruction is unchanged. No scenario grades it now, so it would surface as production behavior: the customer is told the order is cancelled right after the store said it is not, and staff get the wrong reason.
Pattern: A failure row merges two outcomes under one required message, but the message is true for only one of them. Split the outcome or word the message so it holds for each.
Duplicates merged into this finding (same defect, or an instance of it, reported by other finders):
- coverage finder: R2-02 | Gap | Nit | Failure handling, CO-A3 row "returned the refund with status failed, or reported the order not cancelled"; CO-06
  Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |"
  Evidence: The OrderNotCancelled outcome (packet, tool confirmation change 2) has no scenario since answered.md R1-01 removed CO-S17 row 3. CO-06's clause "never after the order system ... reported the order not cancelled" is also unexercised. R1-01's fix is incomplete: the row still requires the agent to "tell the customer the order is cancelled" right after the order system said the order is not cancelled. That breaks G-03 (line 24): "tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled". No consistent Initial state can trigger the branch without the agent first breaking CO-05, so it can never get a scenario as written.
  Pattern: a tool outcome kept in a merged failure row with no reachable trigger and with handling that contradicts a global rule. Either split it into its own row with G-03-true wording (order not confirmed cancelled), or record how it can arise as an open question.
(Source: faithfulness, coverage finder)

**Verifier (sonnet):** Real | Important | I could not refute it. Appendix A defines the outcome as "the order is not cancelled: `OrderNotCancelled`". The row then requires the agent to "tell the customer the order is cancelled", which contradicts G-03 ("tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled"). No Initial-state line or earlier call result can make that outcome true of the scenario. Because the row is not covered by a scenario, §5.1's "answers every call normally" does not help.

**Decision:** kept | severity Important | status: fixed | Verifier Real. OrderNotCancelled split into its own row with a G-03-true message and reason cancellation unknown; no consistent scenario reaches it (carried in the R1-01 open question).

---

R2-03 | Lies | Important | CO-08 and message check "Refund id reported"
Quote: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id."
Evidence: Nothing in the packet requires the agent to tell the customer the refund id.
- Round 2 Q3 lists the refund id only as a data field.
- The only confirmed requirements on the success message are in Q4 case 3 ("Final message must match the final refund status") and Round 3 Q1 ("The agent promises nothing about when the money arrives").
- The shared-understanding summary lists every derivation the assistant made and the user confirmed. Reporting the refund id is not among them.

The spec still makes it a pass condition: agent-spec.md line 1651, message check "Refund id reported", is used by CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 and CO-S26. An agent that says "Order HG-10482 is cancelled and your $86.40 refund to Visa ending 4242 is pending" meets every confirmed input but fails all nine scenarios.
Pattern: The spec turns an unconfirmed derivation into a guarantee and a grader. Either trace each success-guarantee clause and message check to a packet passage, or list it as an open question for the user.
(Source: faithfulness finder)

**Verifier (sonnet):** Real | Important | I could not refute it. CO-08 says "the agent tells the customer the refund id". Nothing in the packet requires that. The "Shared-understanding summary" does not list it either. The check "Refund id reported" is a pass condition for 9 scenarios, so it changes verdicts and is not Style only.

**Decision:** kept | severity Important | status: open | Verifier Real. The fix changes CO-08's text, so it stops at the rule: proposed to the user.

---

R2-04 | Gap | Important | Failure handling, row "the order system did not answer a lookup of the customer's orders made before any CO-A2"; CO-S10
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: Packet, tool confirmation turn, user change 4: "Reads may be retried on timeout without limit; only commit calls are bounded." Appendix A (agent-spec.md line 1675) agrees: "The agent may repeat CO-A1 without limit". CO-01 (line 62) only forbids proposing "When no lookup of the customer's orders has answered". The row's condition is "did not answer a lookup", so it fires after one timed-out read even when a retry then answers, and in that case it requires the agent to propose nothing. The row has no branch for "a retried lookup answers". The only scenario, CO-S10 (line 623), makes every CO-A1 fail ("does not answer any CO-A1 the agent makes"). So no scenario has a first read time out and a retry succeed, and a coder who follows the row literally gives up after one blip. That goes against the user's instruction.
Pattern: a failure row on a retryable read must branch on the retry's result (it answers, or it never answers) and needs a scenario for the branch that continues. Instance: row 92 / CO-S10.
(Source: coverage finder)

**Verifier (sonnet):** Real | Important | This is a Gap finding. CO-01 ("When no lookup of the customer's orders has answered") and Appendix A ("The agent may repeat CO-A1 without limit") settle the behavior by rule. But no scenario asserts a retried lookup that answers, because CO-S10 fails every CO-A1. The row text "did not answer a lookup ... propose nothing" fires on a single timeout. The packet's user change 4 says "Reads may be retried on timeout without limit".

**Decision:** kept | severity Important | status: fixed | Verifier Real. Row now retries the lookup; CO-S01 row 5 has a first lookup unanswered and a later one answered.

---

R2-05 | Gap | Important | CO-S25 (Cancellation not done reported), CO-S08 (Whole order only explained), CO-S02 (CO-02 "asks which")
Quote: "| Cancellation not done reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled, that whether it was cancelled is unknown, or that a refund was issued. | CO-S25 |"
Evidence: In each instance below, a rule or failure-row clause tells the agent to say something, and the scenario that triggers it asserts nothing about it:
- CO-S25 row 1 (status after = shipped). CO-05 (line 74) says that when "a lookup shows the order shipped or delivered, the agent tells the customer the order shipped and was not cancelled, and that returns are a separate process". Failure row 104 says the same. CO-S25's only dimension checks "not cancelled". An agent that never says the order shipped, or that returns are a separate process, passes row 1. CO-S11 does check this with "Shipped order explained".
- CO-S08. CO-03 (line 68): when the customer asks to cancel only some items, the agent tells the customer "that only the whole order can be cancelled and that the refund is the total paid to the order's payment method". "Whole order only explained" (line 1655) checks only the first half. No scenario asserts the refund-terms half for a partial-item request.
- CO-S02. CO-02 (line 65): "the agent asks which and proposes nothing until the customer names one". No Forbidden line or dimension asserts this. Asking is measured only by interaction recall, which §5.2 says is "never folded into the score" (line 1643). The confirmation pair has no scope marker, so an agent that skips the which-order question and proposes the right order outright (HG-10511 in rows 1 and 3) passes those rows. The Unambiguity note's "the confirmation turn, which follows the which-order answer" is not enforced. This is known failure case 1 in the packet ("agent must disambiguate").
Pattern: each clause in a rule or failure row that requires the agent to tell or ask the user something needs a dimension, or a Forbidden line, in a scenario that triggers it. A shared dimension must cover every row's required content, or the row needs its own dimension.
Duplicates merged into this finding (same defect, or an instance of it, reported by other finders):
- verdicts finder: R2-05 | Gap | Important | CO-S02, Expected/Forbidden (CO-02 holding-back clause)
  Quote: "absent" (no line orders the proposal or the CO-A2 after the which-order answer; the Unambiguity note asserts it: "so a cancellation before the confirmation turn, which follows the which-order answer, or of the other order fails in the action log")
  Evidence: CO-02 says "the agent asks which and proposes nothing until the customer names one." In CO-S02, the confirmation pair "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes." has no scope marker. Under §5.2 the simulated user reveals that pair whenever a question matches it, and §5.2 Interaction metrics says recall is "never folded into the score". Here is a wrong run that guesses the order. In rows 1 and 3, the agent skips the which-order question and proposes HG-10511, the most recent order. The user answers "Yes.", CO-A2 and CO-A3 run for HG-10511, and every Required, Final-state, Forbidden, message-check and rubric line passes. In row 2 the same guess becomes a wrong-value question that the user deflects (§5.1). The agent then asks which order, gets "The one with the linen throw blanket.", proposes HG-10482 and passes. An agent that guesses first and asks only after a deflection passes every row, although it broke CO-02 and the must-not "guess which order the customer means". Nothing makes the confirmation turn come after the which-order answer, because the harness labels only confirmation turns and scripted turns (§5.1 Turn anchors).
  Pattern: A rule that says "ask, and propose nothing until answered" is enforced only by interaction recall, which is not scored. The scenario needs a scored line that the agent cannot pass by guessing, such as a dimension or an ordering line anchored to the answer turn.
- verdicts finder: R2-05 | Gap | Important | CO-S25, Forbidden and rubric dimension "Cancellation not done reported"
  Quote: "| Cancellation not done reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled, that whether it was cancelled is unknown, or that a refund was issued. | CO-S25 |"
  Evidence: After the second unanswered CO-A2, the failure row says "Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers or goes unanswered", and for shipped it requires "tell the customer the order shipped and was not cancelled, and that returns are a separate process". G-03 allows "not done" only when the agent can tell. Otherwise it must say the outcome is unknown. CO-S25 has no line that requires a CO-A1 after the second CO-A2. CO-S19 has one for its case: "Fewer than one CO-A1 after the second CO-A3." The dimension also does not check the shipped report or the returns process in row 1 (status after = shipped). Here is a plausible wrong run in both rows: confirm, CO-A2 times out, CO-A1 shows processing, CO-A2 times out, and the agent ends with "I wasn't able to cancel your order." with no lookup. It makes no CO-A3 and no CO-A4, and the dimension passes. That guess about an unknown result passes, contradicting the Unambiguity note: "The lookup after the second unanswered cancellation answers and shows the order not cancelled in both rows, so the agent can tell the outcome". Rows 1 and 2 also need different reports: shipped plus returns in row 1, plain "not cancelled" in row 2. One dimension covers both, and it checks only what the two have in common.
  Pattern: The scenario requires a report that must wait for a read, but no scored line requires that read or the part of the report only the read can supply. The agent can pass by guessing the outcome. One dimension shared by rows that need different reports checks only their common part.
(Source: coverage, verdicts, verdicts finder)

**Verifier (sonnet):** Real | Important | This is a Gap finding with three instances, and each is only settled by a rule with no scenario assertion.

**Decision:** kept | severity Important | status: fixed | Verifier Real. CO-S02 dimension 'Order choice asked first'; CO-S25 trial-end lookup line and row-1 shipped report; 'Whole order only explained' checks the refund terms.

---

R2-06 | Gap | Important | Failure row "the order system did not answer the second CO-A2", branch "placed or processing"; CO-S25 row 2
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4."
Evidence: §2 (line 10) says store staff "receive a follow-up task for each order the agent could not finish". The primary actor (line 9) "wants the order they mean cancelled". In CO-S25 row 2 the order is still processing after two unanswered cancellations. The agent could not finish it, yet CO-S25 forbids "CO-A4 at any point" (line 1522). No rule tells the customer what to do next, such as trying later or contacting support. CO-07 (line 80) covers only an unfinished refund or an uncertain cancellation. No input decides this branch: packet round 3 Q4 stops at "send the cancel once more", and the user listed no handoff reason for it ("refund_not_issued, refund_status_unknown, cancellation_unknown"). The branch came from the R1-02 fix and has no input support. A correct agent that hands off here, as §2 suggests, fails CO-S25 row 2.
Pattern: a branch the inputs leave undecided, settled in the spec without the user. Record it as an open question for the user, and make §2's interest list, CO-07 and the scenario agree.
(Source: coverage finder)

**Verifier (sonnet):** Not real | Important | CO-07 says "CO-A4 occurs in no other situation" than an unfinished refund or an uncertain cancellation. §1 says the same: it hands off "when it cannot finish the refund or cannot tell whether the order was cancelled". The failure row for the second unanswered CO-A2 says "make no CO-A3 and no CO-A4". CO-S25 row 2 asserts it with the Forbidden line "CO-A4 at any point" and the final-state line "No follow-up task exists". In that branch the agent can tell the order was not cancelled, so §2's "could not finish" refers to the refund or uncertain-cancellation cases. Telling the customer what to do next is a Style point.

**Decision:** dropped | severity Important | status: dropped | Verifier Not real, quoting CO-07 "CO-A4 occurs in no other situation" and CO-S25 row 2's Forbidden "CO-A4 at any point". I read them and agree: the inputs list handoff reasons only for an unfinished refund and an uncertain cancellation, and CO-07 with a scenario asserts the no-handoff branch.

---

R2-07 | Gap | Important | CO-01 / CO-07; CO-S06
Quote: "for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order."
Evidence: The Trigger (line 57) includes "to get their money back for an order". The data model allows refund status failed, and list_orders returns each order's refund. So a customer can come back about an already-cancelled order whose refund is failed (left from an earlier conversation like CO-S17) or missing. Two rules give different instructions for that order:
- CO-01 and row 96 say: report it as already cancelled and propose nothing.
- CO-07 (line 80) says: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4". Zero retries were made, so this can be read as requiring a handoff.
The customer's interest "told truthfully ... where the refund stands" (line 9) is not asserted for this state. The shared understanding says only "An already cancelled order: the agent reports that and changes nothing." CO-S06, the only already-cancelled scenario, has the refund issued, so the boundary is never tested. Two experts could disagree on whether CO-A4, or CO-A3 under SG-01, is allowed.
Pattern: an Initial-state boundary (cancelled order with refund failed or absent) where two rules overlap. It needs a data variant or scenario that settles which rule wins and what the agent says about the refund.
(Source: coverage finder)

**Verifier (sonnet):** Real | Nit | I could not fully refute it. CO-05 permits CO-A3 for "a lookup shows cancelled". CO-07 permits CO-A4 when "the order is cancelled but its refund is not shown pending or issued". CO-01 and the row for a cancelled order say "propose nothing". The packet's "reports that and changes nothing" points toward CO-01, but CO-S06 only covers an issued refund. No scenario asserts the failed-refund or no-refund boundary.

**Decision:** kept | severity Nit | status: open | Verifier Real at Nit (lower than the finder's Important). Only the user can decide what happens to an already-cancelled order with a failed or missing refund.

---

R2-08 | Gap | Nit | CO-03 / failure row "the customer asked to cancel only some of an order's items"; CO-S08
Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
Evidence: This is an "act only when" row: propose only once the customer asks for the whole order. CO-S08 is the holding-back side; its optional pair answers "No, I'll keep it." No scenario covers the acting side, where after a partial-item request the customer asks to cancel the whole order and the agent proposes HG-10530 for $53.50 to Amex ending 1007 and completes it. An agent that refuses to cancel anything once a partial request was made would pass every scenario. (Evaluation checklist: "Both directions are covered.")
Pattern: an act-only-when condition with a holding-back scenario and no acting scenario. Instance: the partial-item row and CO-S08.
(Source: coverage finder)

**Verifier (sonnet):** Real | Nit | The row says "propose nothing until the customer asks to cancel the whole order". CO-S08 tests only the holding-back side, and no scenario has the customer then asking for the whole order. The checklist item "Both directions are covered" applies.

**Decision:** kept | severity Nit | status: fixed | Verifier Real. New CO-S27.

---

R2-09 | Gap | Nit | G-01 / CO-02; no row or scenario
Quote: "absent"
Evidence: G-01 (line 18): "The agent cancels, refunds and hands off at most the one order the current request is about". §1 (line 5): "It may cancel that one order". No rule, failure row or scenario says what the agent does when one request names two of the customer's open orders (for example "cancel HG-10482 and HG-10511" with the CO-S02 Initial state). Any of these could pass under G-01: one proposal at a time, refusing the second, or asking which. No input decides it; the use-case checklist says to record such a "what if" as an open question.
Pattern: a request shape the capability's own rules make ambiguous (several orders in one request), with no rule and no scenario.
(Source: coverage finder)

**Verifier (sonnet):** Real | Nit | G-01 and CO-02 ("Every proposal names one order number") bound the behavior, but no scenario or row covers a request naming two open orders. Several behaviors would pass.

**Decision:** kept | severity Nit | status: open | Verifier Real. No input decides a request naming two open orders.

---

R2-10 | Ambiguous | Nit | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: Row 2 says the first CO-A2 "gets no answer from the order system and cancels nothing". Initial state does not say whether an unanswered call "reaches" the order system. If the harness treats a timed-out call as not reaching it, the status stays processing. The lookup then shows processing, and the failure row ("If it shows the order placed or processing, make CO-A2 once more") requires a second CO-A2. That call is forbidden ("A second CO-A2."), and the Final state "HG-10482 has status shipped" fails. CO-S25 anchors the same kind of change to an event the harness can see: "status processing until the agent issues its second CO-A2". The Unambiguity note ("in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation") shows the intended reading, so this is a Nit.
Pattern: A world change mid-trial is anchored to whether a call reached the supporting actor, which is unclear for a call that timed out. The anchor should be the agent issuing the call.
(Source: verdicts finder)

**Verifier (sonnet):** Real | Nit | The checklist requires a mid-trial change to be tied to "the agent's nth state-changing call". CO-S11 ties it to the CO-A2 "reaches the order system". Row 2 ("gets no answer ... and cancels nothing") leaves open whether an unanswered call reaches it. The Unambiguity note shows the intended reading, so this is a Nit.

**Decision:** kept | severity Nit | status: fixed | Verifier Real this round (it called R1-12, the same defect, Not real in round 1). Kept and fixed: CO-S11 status change tied to the agent issuing its first CO-A2.

---

R2-11 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: §5.2 Scoring says "Any Forbidden event scores the trial 0", and evaluation-checklist.md says "Forbidden lines name events. Each Forbidden line is a tool call pattern (name plus the argument condition) or a timing violation". It also says "A tool call that only reads is never Required". This line names no event. It is a required read written as a Forbidden line, and it cannot become a "Then no … occurs" step without rewording. It changes no verdict: an agent that skips the lookup cannot learn RF-5531, so message check "Refund id reported" and "Refund status reported" already fail it. CO-S20 and CO-S21 express the same need as a timing violation instead: "CO-A4 before a CO-A1 made after the second CO-A3."
Pattern: A Forbidden line that asserts a read is missing, instead of naming a forbidden call or a timing violation.
(Source: verdicts finder)

**Verifier (sonnet):** Style only | Nit | The line "Fewer than one CO-A1 after the second CO-A3" is a required read written as a Forbidden line, which the checklist disallows. But it changes no verdict. An agent that skips the lookup cannot learn RF-5531, so "Refund id reported" and "Refund status reported" already fail it.

**Decision:** kept | severity Nit | status: fixed | Verifier Style only; not dropped: a Forbidden line that names no event is an Untestable form defect, not wording. Rewritten as 'The trial ending with no CO-A1 made after the second CO-A3.'

---
