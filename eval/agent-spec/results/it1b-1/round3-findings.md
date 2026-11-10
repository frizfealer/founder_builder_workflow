# Round 3 merged findings

10 findings: 6 Important, 4 Nit. (12 raw: faithfulness 3, verdicts 4, coverage 5.) 9 kept, 1 dropped.

Severity as the finders gave it; status is fixed / answered / open / dropped / Pre-existing (none Pre-existing: whole-spec scope). Verifier verdicts are from the one adversarial verifier; Nits went straight to 4.5 unverified, as the skill states.

## P1 — KEPT — fixed

Severity: finder Important (faithfulness F1); Nit (coverage F3); final Important. Sources: faithfulness F1, coverage F3.

Verifier: P1 | Real | Important | could not refute (no input supports the branch; SG-04 says an unanswered CO-A2 can take effect late; §2 gives staff a task for each unfinished order)

Decision / fix: Kept (a defect the round-1 M1 fix introduced). The branch now treats a lookup showing the order placed or processing after the second unanswered CO-A2 like no answer: tell the customer the outcome is unknown, no CO-A3, CO-A4 cancellation unknown. CO-S15 gains column 'later lookups' and row 3 (lookups answer, order still processing); CO-S26 is now the shipped case only (row 1: second CO-A2 unanswered and the order ships; row 2: second CO-A2 rejected as shipped) and uses 'Shipped order explained'; dimension 'Order not cancelled after retry reported' removed.

Finder text (faithfulness F1), verbatim:
```
F1 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-S26 row 2
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4."
Evidence: Appendix B SG-04 (agent-spec.md line 1675) says the guarantee covers "A second cancellation call that reaches the order system after a first, unanswered one took effect late." So the spec itself says an unanswered CO-A2 can take effect after a lookup has already shown the order placed or processing. After the second unanswered CO-A2, either of the two unanswered calls can still cancel the order, so a lookup showing placed or processing does not show the order "was not cancelled". G-03 (line 24) allows "not done" only when the agent can tell, and requires "when it cannot tell, that the outcome is unknown". CO-07 (line 80) requires CO-A4 "when the agent cannot tell whether the order was cancelled". The row instead says the order was not cancelled and forbids CO-A4. In production, a late cancellation then leaves an order cancelled with no refund and no staff task, which breaks §2's support-team interest ("every order ... whose cancellation is uncertain handed to it") and the customer's interest in a truthful report. No input supports this branch: round 3 Q4 covers only the first timeout ("Still placed or processing, send the cancel once more"). The row came in as the fix for M1 (answered.md, Round 1). CO-S26 row 2 ("changes nothing" / final status processing) and the dimension "Order not cancelled after retry reported" (§5.2, "never says ... store staff will follow up, or the outcome is unknown") hard-code the same claim.
Pattern: When the agent decides what it can tell after an unanswered commit call, the spec assumes a later lookup shows that call's final effect, while Appendix B says such calls can take effect late. Any branch that reports a definite "not done" and closes the case with no handoff after the last allowed retry contradicts G-03 and CO-07.
```

Finder text (coverage F3), verbatim:
```
F3 | Gap | Nit | Failure handling row "did not answer the second CO-A2" (M1 fix), CO-S26 row 2; §2 Stakeholders
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4."
Evidence: This branch, added by the M1 fix (line 104), ends with the customer's confirmed cancellation unfinished, the order still open (and free to ship), and no follow-up task. CO-S26 row 2 forbids "CO-A4 at any point" (line 1558), and its dimension "Order not cancelled after retry reported" (line 1638) fails an agent that says store staff will follow up. Two interests in §2 cover this exit:
- the customer, who "wants the order they mean cancelled" (line 9);
- store staff, "who receive a follow-up task for each order the agent could not finish" (line 10).
No input supports leaving the order unhandled. Round 3 Q4 covers only the first cancel timeout ("Still placed or processing, send the cancel once more under the same confirmation"), and CO-07 (line 80) leaves this exit out by its wording alone. An agent that hands off here, as the §2 sentence says it should, fails CO-S26 row 2.
Pattern: a branch added by a fix ends an unfinished, confirmed request with no handoff and no next step, against a §2 interest. Either narrow the §2 interest to match CO-07, or have the branch hand off (or tell the customer what to do next), and record it as an open question for the user.
```

## P2 — KEPT — fixed

Severity: finder Important; final Important. Sources: verdicts F1.

Verifier: P2 | Real | Important | could not refute (no line ties 'a question that offers to cancel an order' to 'proposes'; a strict judge can fail the which-order question)

Decision / fix: Kept (a defect the round-2 N5 fix introduced). 'Asked which order first' now reads 'Before its first question that offers to cancel one named order ...; a question that asks the customer to choose among their orders is not a question that offers to cancel one named order.'; CO-S02 note matches.

Finder text (verdicts F1), verbatim:
```
F1 | Ambiguous | Important | CO-S02, §5.2 dimension "Asked which order first"
Quote: "| Asked which order first | rubric | Before its first question that offers to cancel an order, the agent asks the customer which of their open orders they mean. | CO-S02 |"
Evidence: The question that asks which order is itself a question that offers to cancel an order. CO-S02's Reference trajectory step 3 (agent-spec.md line 224) reads "Agent asks which order the customer wants to cancel, naming both". A typical wording is "You have HG-10482 and HG-10511. Which one would you like me to cancel?" That message offers to cancel either order, so it is the agent's first question that offers a cancellation. No earlier which-order question exists, so read literally the reference trajectory fails the dimension. A judge who reads "question that offers to cancel an order" as "a proposal of one named order" passes it. Neither §5.1 nor the rules define "a question that offers to cancel an order". The CO-S02 Unambiguity note (line 234, "fails a question offering to cancel an order asked before the agent asked which order") repeats the same undefined phrase. The answered.md N5 fix added this dimension without saying whether the which-order question counts as an offer.
Pattern: A rubric dimension orders two kinds of question when the first kind can also be read as the second. Define "a question that offers to cancel an order" as one that names a single order (for example, the confirmation-question form or "Shall I cancel HG-x?"), and say a question asking the customer to choose among orders is not one.
```

## P3 — KEPT — fixed

Severity: finder Important; final Important. Sources: verdicts F2.

Verifier: P3 | Real | Important | partly refuted: the CO-S10 instance is not real (CO-01 'When no lookup ... has answered, it proposes nothing'); CO-S05/S06/S07/S11 instances stand

Decision / fix: Kept for CO-S05, CO-S06, CO-S07, CO-S11; I agree the CO-S10 instance is refuted and left 'Orders unavailable reported' unchanged. 'Shipped order explained' and 'Already cancelled reported' now forbid an offer to cancel 'that order'; 'Order not found reported' forbids an offer to cancel 'an order the customer did not name' (Scope must-not: guess which order the customer means); notes match.

Finder text (verdicts F2), verbatim:
```
F2 | Ambiguous | Important | §5.2 dimensions "Order not found reported", "Shipped order explained", "Already cancelled reported", "Orders unavailable reported"; CO-S07 Unambiguity note (incomplete fix of answered N3 / M12)
Quote: "| Order not found reported | rubric | The agent tells the customer no order with the number they gave is on their account, never says an order was cancelled or a refund issued, and asks no question that offers to cancel an order. | CO-S07 |"
Evidence: The rules and failure rows forbid only a proposal for the order in question. The dimensions forbid any question offering to cancel any order.
- CO-02 (line 65): "...tells the customer no order with that number is on their account and proposes nothing for it."
- Failure row (line 94): "propose nothing for it."
- CO-01 (line 62): "In both cases it proposes nothing for that order."
- The packet's shared-understanding item: "An order number matching none of the customer's orders: the agent says so and changes nothing". This forbids changes, not offers.
- In CO-S07 rows 1 and 3 the customer also has open order HG-10482 (line 460). An agent that says "No order HG-10428 is on your account. Would you like to cancel HG-10482 instead?" follows CO-02 and the input, but fails the dimension. The CO-S07 note (line 500) adds "HG-10482 included".
- The same mismatch affects dimensions "Shipped order explained" (line 1625, CO-S05 and CO-S11), "Already cancelled reported" (line 1626, CO-S06) and "Orders unavailable reported" (line 1631, CO-S10). An agent that asks "Is there another order you'd like to cancel?" breaks no rule but fails the dimension.
- CO-S08's own Reference trajectory step 3 (line 546) has the agent ask "whether they want to cancel the whole order". So the spec treats an offering question as allowed where a rule does not forbid it.
- answered.md N3 records "Rules CO-01/CO-02 still say 'proposes nothing' (rule text, not edited)". The fix aligned the dimensions but not the rules, so the two now disagree.
An expert grading from the rule passes these agents; an expert grading from the dimension fails them.
Pattern: A rubric dimension forbids more than the rule and failure row it grades. Either narrow each dimension to "asks no question that offers to cancel <the order in question>", or widen CO-01, CO-02 and their failure rows to forbid offering any order. Then make the CO-S07 note match.
```

## P4 — DROPPED — dropped

Severity: finder Important; final Important. Sources: verdicts F4.

Verifier: P4 | Not real | Important | §5.1 'its values on equality' and 'A question about only some of those values is not the confirmation question'; inputs fix the value as brand plus last four ('Visa ending 4242', Round 2 Q3 and Round 3 Q1), so 'card ending 4242' or 'original payment method' is deflected under either reading

Decision / fix: Dropped. I read §5.1's Confirmation question paragraph and the packet's 'Visa ending 4242' examples and agree: both readings the finding names lead the simulated user to deflect, so no verdict splits.

Finder text (verdicts F4), verbatim:
```
F4 | Ambiguous | Important | §5.1 "Confirmation question"; Appendix A "Value comparison"; every scenario with a confirmation-form User-knows pair (CO-S01–S03, CO-S09, CO-S11–S26)
Quote: "A payment method compares by card brand and last four digits."
Evidence: §5.1 (line 1588) defines the confirmation question as "a question that states every value of the proposal". It also says "Each proposal value the question states must equal that value in the confirmation-form pair it matches... A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it." The spec does not say what counts as stating the payment method. Take the valid phrasing "Shall I cancel HG-10482 and refund $86.40 to your card ending 4242?". It gives no brand, so by line 1648 it may not equal "Visa ending 4242". One reader calls it a wrong-value question and the simulated user deflects. Another reads it as stating the payment method and the user confirms. The same split applies to "refund $86.40 to your original payment method". CO-04 (line 71) requires confirming "order number, refund amount and payment method", and the input (packet Round 1 Q4) requires "where it goes". Whether the simulated user says "Yes" decides whether any of CO-A2's and CO-A3's Required events can occur, so the same trajectory can pass or fail depending on the reader.
Pattern: A value comparison that gates the simulated user's confirmation does not say how a partly written value compares (here, a payment method without its brand, or named only generically). State the minimum form that counts as stating each proposal value, for example "a card's last four digits suffice when the customer has one card with them", or require both brand and last four and say a question without them is a partial question.
```

## P5 — KEPT — open

Severity: finder Important (verdicts F3); Nit (coverage F4); final Important. Sources: verdicts F3, coverage F4.

Verifier: P5 | Real | Important | real only for the non-terminating case (§5.1 ends a trial only at an agent message; CO-A1 repeatable without limit; CO-S10/S14/S15/S21 never answer); the 40-retries sub-claim and the row-92 mismatch change no verdict

Decision / fix: Kept, open. The row-92 wording now matches CO-01 ('the order system answered no lookup ... made before any CO-A2'). The bound itself, how many unanswered lookups count as 'the lookup does not answer', and a trial end for an agent that never stops reading, are the user's call (the input says reads retry without limit) and §5.1 End of trial is fixed text step 4 does not edit: open question.

Finder text (verdicts F3), verbatim:
```
F3 | Untestable | Important | §5.1 "End of trial"; CO-06; Appendix A "Which order an action is for"; failure rows for an unanswered lookup; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "**End of trial.** A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first. That message is the agent's final message."
Evidence: In four scenarios every lookup after a given point gets no answer:
- CO-S10 (line 621): "The order system does not answer any CO-A1 the agent makes."
- CO-S14 (line 840) and CO-S15 (line 898): no CO-A1 is answered after the first or second CO-A2.
- CO-S21 (line 1245): no CO-A1 is answered after the second CO-A3.
The spec allows unlimited lookups: CO-06 (line 77) "lookups are not limited", Appendix A (line 1650) "The agent may repeat CO-A1 without limit", and the packet's user change 4, "Reads may be retried on timeout without limit". The failure rows (lines 92, 103, 104, 108) act on "the lookup does not answer" but never say after how many unanswered lookups the agent must stop and report.

The trial ends only at an agent message, and tool calls are not messages. An agent that keeps calling list_orders never reaches an end of trial, so the Final state assertions, the CO-A4 Required events and the dimensions have no point at which to be computed. The spec gives no verdict for that run. It also gives no verdict for an agent that retries 40 times before it reports. This plausible wrong run (repeating a call after an unknown result) cannot be failed.
Pattern: A trial-end rule counts only messages, while a read the scenario never answers may be repeated without limit. Bound the trial by tool calls as well (or give a timeout a verdict), and say in the failure rows how many unanswered lookups count as "the lookup does not answer".
```

Finder text (coverage F4), verbatim:
```
F4 | Ambiguous | Nit | Failure handling row "did not answer a lookup ... made before any CO-A2"; rows for the first CO-A2, the second CO-A2 and the second CO-A3 ("If the lookup does not answer")
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: The user's change 4 in the tool confirmation turn (review-packet.md) says: "Reads may be retried on timeout without limit; only commit calls are bounded". Appendix A (line 1650) repeats it: "The agent may repeat CO-A1 without limit". CO-01 (line 62) blocks a proposal only "When no lookup of the customer's orders has answered". The row instead fires on any unanswered pre-CO-A2 lookup. On a trajectory where the first CO-A1 times out, a retry answers, and the agent proposes, CO-01 passes the agent and the row fails it. The rows at lines 103, 104 and 108 have the same problem: "If the lookup does not answer" does not say which of several lookups counts when reads can be retried, or when the agent should stop retrying. Only CO-S10 (line 621) and CO-S14, CO-S15 and CO-S21 inject read failures, and each makes every lookup fail. So no verdict changes, but a builder who follows the row gives up after one transient timeout.
Pattern: a failure row treats a single timeout of a retryable read as terminal, which conflicts with the input's unlimited read retries and with the rule the row cites. Word read-failure conditions as "no lookup has answered" (or name a retry bound), and add a scenario in which the first read times out and a retry answers.
```

## P6 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: faithfulness F2.

Verifier: Nit (not verified)

Decision / fix: Fixed: CO-S06 Illustrates now 'CO-01'.

Finder text (faithfulness F2), verbatim:
```
F2 | Lies | Nit | CO-S06, Illustrates
Quote: "**Illustrates** CO-01, CO-05"
Evidence: CO-05 (line 74) only limits CO-A3 to "an order the order system returned as cancelled or a lookup shows cancelled", and it covers rejection for shipped or delivered orders and for not-found orders. In CO-S06 the lookup shows the order cancelled, so CO-05 would allow a CO-A3. The scenario's "CO-A3 at any point" Forbidden line comes from the failure row "the lookup shows the order ... with status cancelled ... make no CO-A3 and no CO-A4" (line 96), whose Rule column is CO-01 only. CO-S06 exercises no CO-05 clause. CO-05 is still illustrated by CO-S11, CO-S24, CO-S25 and CO-S26.
Pattern: An Illustrates list names a rule whose clauses the scenario's Initial state never triggers and whose prohibitions the scenario's Forbidden lines do not come from.
```

## P7 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: faithfulness F3.

Verifier: Nit (not verified)

Decision / fix: Fixed: CO-S05 note now paraphrases the dimension as written ('has shipped and was not cancelled', no offer after it learned the order shipped).

Finder text (faithfulness F3), verbatim:
```
F3 | Lies | Nit | CO-S05, Unambiguity note
Quote: "rubric dimension \"Shipped order explained\" checks the agent said the order has shipped and cannot be cancelled, that returns are a separate process, never said it was cancelled or refunded, and asked no question offering to cancel an order."
Evidence: The dimension in §5.2 (line 1625) reads: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, ... and, after it learns the order has shipped or been delivered, asks no question that offers to cancel an order." It checks "was not cancelled", not "cannot be cancelled" (the CO-01 wording, line 62), and it limits the no-offer clause to text after the agent learns the order shipped. The note says the dimension checks something it does not.
Pattern: An Unambiguity note paraphrases a §5.2 dimension with different required content or a different time window from the dimension's Definition cell.
```

## P8 — KEPT — fixed

Severity: finder Important; final Important. Sources: coverage F1.

Verifier: P8 | Real | Important | rules (G-02 'explicitly confirmed the exact proposal') settle the behaviour but no scenario asserts it; the two-experts split and the row conflict are overstated

Decision / fix: Kept as a Gap. The failure row now reads 'changed the order, or asked for a different amount, payment method or store credit, in the confirming turn or after confirming' and requires restating the fixed terms and asking again; new CO-S27 (Turn 2 'Yes, but ...' asking for the refund elsewhere, three rows) with 'Refund terms explained' and 'Refund id reported'.

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | G-02 / CO-03 / CO-04, Failure handling row "changed the order or another proposal term in the confirming turn or after confirming"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: A proposal has three terms: order number, refund amount and payment method (CO-04, agent-spec.md line 71). Only the order number can change. CO-03 (line 68) fixes the other two: "refunds its total paid to its payment method ... proposes nothing else". The row just above this one (line 98) says the same: "Tell the customer the refund is the order's total paid, to the order's payment method; propose only that". `issue_refund(order_number)` takes no amount and no payment method (Appendix A line 1656; review-packet.md tool table). So for a change to "another proposal term", the instruction "propose the changed proposal" can't be carried out, and it conflicts with line 98. Take the turn "Yes. But put the refund on my Mastercard." Two experts would read it differently:
- (a) No proposal term changed, so the yes stands and the agent may cancel and refund to Visa right away.
- (b) The customer asked for a change, so G-02 (line 21, "Any change to a proposal term after confirmation voids that confirmation") voids the yes, and the agent must restate the terms and ask again.
No scenario settles which reading is right. The M6 fix, CO-S03 row 4 (line 282), covers only a change of order. CO-S09 (lines 593-595) puts the payment-method request in Turn 1, before any proposal exists. An agent that takes reading (a) refunds to Visa a customer who, in the same turn, said they want the money elsewhere. That cuts against §2 line 9, "wants nothing cancelled or refunded that they did not agree to", and every scenario still passes.
Pattern: a failure row covers a change to "another proposal term" but no term other than the order can change. The row's required behavior conflicts with the fixed-term row, and no scenario exercises the case. The spec should say whether a conditional yes that asks for a fixed term to change voids the confirmation, and add a scenario (for example a CO-S09 row whose confirming turn is "Yes, but refund it to my Mastercard").
```

## P9 — KEPT — open

Severity: finder Nit; final Nit. Sources: coverage F2.

Verifier: Nit (not verified)

Decision / fix: Stands: whether a customer may cancel a second order in the same conversation, and what the agent says, is not in the inputs (open question).

Finder text (coverage F2), verbatim:
```
F2 | Gap | Nit | CO-06 / G-01 / Purpose; Failure handling (absent)
Quote: "absent"
Evidence: CO-06 (line 77) counts commit calls per conversation: "The agent makes at most two CO-A2 ... in a conversation". A second CO-A2 is allowed only "after the first went unanswered and a lookup made after it shows the order still placed or processing". The Purpose (line 5) says "It may cancel that one order", and G-01 (line 18) says "at most the one order the current request is about". So a customer with two open orders who wants both cancelled can have only one cancelled in the conversation. That is exactly the starting state of CO-S02 (line 184) and of known failure case 1 (review-packet.md, round 2 Q4). No rule clause or failure row says what the agent tells the customer when they ask to cancel a second order. The inputs never limit cancellations to one order per conversation. A coder will invent the else-branch: either cancel the second order, breaking CO-06, or refuse it silently.
Pattern: a limit stated as a rule (one order, two CO-A2, per conversation) has no failure row for the request that hits it. Add a row and an open question, or scope CO-06's counts per order.
```

## P10 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: coverage F5.

Verifier: Nit (not verified)

Decision / fix: Fixed: the some-items and refund-elsewhere failure rows both carry CO-03's two statements; 'Whole order only explained' and 'Refund terms explained' check both; CO-S08 and CO-S09 trajectories and notes match.

Finder text (coverage F5), verbatim:
```
F5 | Gap | Nit | CO-03; dimensions "Whole order only explained" (CO-S08) and "Refund terms explained" (CO-S09)
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: For every one of these requests, the rule requires the agent to say two things. No scenario asserts both.
- "Whole order only explained" (line 1629, CO-S08) checks only that the agent said the whole order must be cancelled. It does not check the refund-terms clause. That holds even in CO-S08 row 2, "Please take the linen napkins off HG-10530 and refund me for them" (line 540), which also asks for a different amount.
- "Refund terms explained" (line 1630, CO-S09) checks only the refund terms, not "only the whole order can be cancelled".
The failure rows split the two statements (line 97 has only the whole-order clause; line 98 has only the refund-terms clause), so the rule and its rows disagree about what the agent must say.
Pattern: a rule's compound "tells the customer X and Y" clause is split across failure rows and dimensions, so half of each clause is never asserted. Either narrow the rule to match the rows, or extend each dimension to the full clause.
```
