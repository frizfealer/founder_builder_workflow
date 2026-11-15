# Round 1 findings

Finder report, verbatim, then each finding's verifier verdict, the decision and its status.

```
10 findings: 6 Important, 4 Nit.

F1 | Lies | Important | rules.md R-08; rules.md "What the agent does" row "the refund read again answered an error, and the retry answered pending or issued"
Quote: "When that read fails but the retry answered pending or issued, the agent tells the customer what the retry answered."
Evidence: review-packet.md Question 10, owner's reply: "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off." The owner set no exception for a failed re-read. Claim C-53 and decision D-07 carry the owner's rule without the exception, and no decision records the added branch. Under the spec, when the re-read fails the agent reports success and creates no staff task. The owner said it should say the status is unknown and hand off.
Pattern: a rule adds a branch to the owner's case list that the owner never gave, and no decision records it.

F2 | Gap | Important | rules.md R-12 and "What the agent does"; policy.md chart steps
Quote: absent (R-12: "It handles at most 3 orders in one conversation; for a fourth it tells the customer to start a new conversation." has no row)
Evidence: review-packet.md Question 8 (accepted): "The agent handles one order at a time ... It handles at most 3 orders in one conversation; for a fourth it tells the customer to start a new conversation." The only multi-order row in "What the agent does" is "the customer said yes and switched to their other open order". Three cases have no row: (a) one message asking to cancel two orders, (b) a second order asked for after the first is settled, (c) a fourth order. In policy.md every "Conversation over" state is final and no arrow returns to "Customer asked". The spec's own scenarios.md SC-46 and SC-47 admit the model cannot show these, but the table that tells the agent what to do does not cover them either.
Pattern: a rule the owner gave has no row in "What the agent does" because the policy model cannot reach the case.

F3 | Gap | Important | rules.md R-03 and row "the customer has two open orders and did not say which"; policy.md A1, A6
Quote: "When the customer has two open orders and does not say which one to cancel, the agent asks which one and proposes nothing until the customer names it."
Evidence: review-packet.md Question 6, failure case 1: "customer has two open orders and says 'cancel my order'; agent must disambiguate". The owner gave two orders as the example of the case: an ambiguous request. Nothing in the inputs limits a customer to two open orders, yet R-03, the row, A1 ("The customer has two orders placed or processing") and A6 ("asks which of the two orders") only cover exactly two. No rule or row says what the agent does with three or more open orders and no order number.
Pattern: the owner's example is written as the rule's limit, so the general case has no rule.

F4 | Lies | Important | rules.md R-02 (last sentence), R-07, row "the order read again shows it shipped"
Quote: R-02: "When the cancel call answers that the order is not cancellable, or the order read again shows it shipped, the agent says the order can no longer be cancelled and issues no refund." R-07: "Shipped, it says the order can no longer be cancelled and issues no refund." Row: "says the order can no longer be cancelled and no refund was issued"
Evidence: review-packet.md Question 3, owner: "Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1)." The spec is inconsistent about this message. The row "the cancel call answered not cancellable" includes "and that returns are a separate process", even though the R-02 sentence it cites does not. policy.md A13 includes it for both cases. R-02's last sentence, R-07 and row 105 drop it. An agent built from R-07 or row 105 leaves out the owner's message about returns when the order shipped after the yes.
Pattern: what the owner said the agent tells the customer is kept in some places and dropped in others for the same situation.

F5 | Gap | Important | rules.md R-08, row "the refund call answered failed or order not cancelled, and no refund call timed out"; policy.md A3
Quote: R-08: "After a terminal one ..., or an answer that the order is not cancelled, it sends none and hands the case to staff as refund not issued." Policy A3: "agent tells the customer: the order is cancelled but the refund was not issued; staff will follow up"
Evidence: review-packet.md Question 9, owner change 2: "issue_refund adds outcome OrderNotCancelled"; claims.md C-45. When the refund call says the order is not cancelled, the only message the policy has for "refund not issued" tells the customer "the order is cancelled". That contradicts what the order system just said. No rule says what the agent tells the customer about the order's state in this case. C-38 and R-09 only make the final message match the refund's status.
Pattern: a tool outcome is mapped to a staff reason, but the message to the customer is borrowed from a different outcome and states something the tool denied.

F6 | Gap | Important | rules.md R-04, R-06, R-08; row "the order is placed or processing and nothing is proposed yet"
Quote: absent (the row reads: "proposes cancelling that order and refunding its total paid to the payment method it was paid with, and asks for a yes")
Evidence: review-packet.md Question 5 (accepted recommendation) lists "whether a refund has already been issued for it" as a field the rules depend on. claims.md C-04 says the order list returns each order with its refund. C-32 and the owner's words say "at most one refund per order". C-44 says a repeated refund call returns the existing refund. No rule reads an open order's existing refund before proposing. So for an open order that already has a refund, the agent proposes and gets a yes for a refund of the full total, cancels the order, and only learns of the existing refund when the refund call returns it.
Pattern: a field the owner said the rules depend on is read but no rule uses it before the agent commits.

F7 | Gap | Nit | rules.md R-07, row "the order read again shows it shipped"
Quote: "Shipped, it says the order can no longer be cancelled and issues no refund."
Evidence: claims.md C-03 lists the statuses placed, processing, shipped, delivered, cancelled. R-07 and row 105 cover only a re-read showing shipped. A re-read showing delivered has no rule or row, though policy.md A13 already reads "the order has shipped or been delivered". review-packet.md Question 3: "for a shipped or delivered order the agent says it cannot cancel".
Pattern: a branch on a status lists only some of the statuses that lead to the same outcome.

F8 | Gap | Nit | rules.md R-09, R-11
Quote: R-09: "either way it gives the amount and the payment method and creates no staff task."
Evidence: review-packet.md Question 4: the yes covers "which order, the refund amount and where it goes". claims.md C-09 says the refund the tool returns carries its own payment method. R-11 covers a refund amount that differs from the yes, but nothing covers a refund payment method that differs. R-09 also does not say whether the payment method given to the customer comes from the proposal or from the refund. C-13 (from the Stripe docs) makes a mismatch unlikely, which is why this is a Nit.
Pattern: a value passed on from a tool, covered by the yes, with nothing said about a mismatch.

F9 | Lies | Nit | claims.md C-56; rules.md R-01
Quote: C-56: "A read can answer with an error, which the owner calls a read that fails, as well as time out." R-01: "When the order list answers with an error, it says it cannot look up the orders right now and changes nothing."
Evidence: review-packet.md Question 9: the confirmed tool set gives the order list only "the call can get no answer", with no error outcome. The owner never defined "fails" as an error answer, as opposed to a timeout. The wording "cannot look up the orders right now" comes from the Question 13 recommendation, which the owner did not accept (reply: "Reads may be retried on timeout without limit; only commit calls are bounded."). C-56 is marked "spec only", but its wording tells the reader the owner made the distinction.
Pattern: a spec-only inference is worded as the owner's own term, and its customer wording comes from a recommendation the owner did not accept.

F10 | Unclear | Nit | claims.md C-30
Quote: "The agent proposes the total paid the order list shows; when the refund comes back with another amount, C-39 applies."
Evidence: The "if it differs" column of C-30 hands the owner a claim id instead of saying what happens. C-39's own column spells it out: "No further change with the new amount; the customer is told the amount the order system returned; the case goes to staff."
Pattern: an id stands in for a sentence the owner needs to read.
```

## Verifier verdicts, verbatim

```
F1 | Real | Important | I could not refute it. The owner's Q10 rule has no exception: "re-read fails, say status unknown and hand off." C-53 and D-07 ("reads the refund again and reports what it finds") carry that rule without the added branch, and no decision records the branch. So when the re-read fails after a retry that answered pending or issued, row 117 tells the customer what the retry answered and creates no staff task. The owner said: status unknown, hand off.
F2 | Real | Nit (finder said Important) | Part answered: R-12 "one order at a time, each with its own proposal and its own yes … for a fourth it tells the customer to start a new conversation" says what the agent does in cases (a) and (c). For (b), SC-47 says "a second order in the same conversation starts a new run of the model". Part that stands: the Gap class in verification.md counts "a case an agent will meet that no row of 'What the agent does' covers, such as two requests in one message", and no row covers any of the three cases. Because R-12 already states the behavior, I rate it Nit.
F3 | Real | Important | I could not refute it. R-03, row 91, A1 ("two orders placed or processing") and A6 ("which of the two orders") all say exactly two. Row 95 "proposes cancelling that order" assumes there is only one. No rule or row says what the agent does with three or more open orders and no order number. R-04 (a yes that names the order number) guards the cancel but does not say "ask which one", which the owner's case 1 requires ("agent must disambiguate").
F4 | Real | Nit (finder said Important) | Part answered: the owner's Q10 answer for this exact case is "Shipped, report it and issue no refund." That supports R-07 and row 105 leaving out the returns message when the order read again shows it shipped. Parts that stand: R-02's last sentence also drops "returns are a separate process" for a cancel call that answers not cancellable, while row 100, which cites R-02, includes it. And A13 includes it for the re-read-shipped case that row 105 leaves it out of. So the spec gives two different messages for the same situation.
F5 | Real | Important | I could not refute it. The owner added the OrderNotCancelled outcome (Q9 change 2, C-45), so it is possible at that point. Row 119 and R-10 say only "tells the customer what happened to the order and the refund", which does not say what the customer hears. The only A3 wording for "refund not issued" is "the order is cancelled but the refund was not issued", which states something the refund call just denied.
F6 | Not real | Important | The case cannot arise from what the packet and the spec say. C-45: "The refund call can also answer that the order is not cancelled, and then creates no refund." So a refund exists only for a cancelled order, and R-02 covers that: "For an order that is already cancelled it says so and changes nothing." Nothing in the packet says an open order can carry a refund. The refund field is also used: R-08 reads the refund again, and C-11 says "The order list shows a refund as soon as it is made." Even if the case did happen, C-44 returns the same refund and R-11 covers another amount, so nothing would go against the owner.
F7 | Real | Nit | Part answered: R-02 "For a shipped or delivered order it says it cannot cancel, tells the customer returns are a separate process, and sends no cancel call" and R-07 "sends the refund call only once the cancel call answered cancelled, or the order read again shows it cancelled" say what the agent does. A13 gives the message ("the order has shipped or been delivered … no refund was issued"). So the "no rule" part is refuted. Part that stands: no row of "What the agent does" covers an order read again that shows delivered.
F8 | Not real | Nit | C-13 (Stripe docs): "Refunds can only be sent back to the original payment method used in a charge." C-31 says the refund goes to "the payment method the order was paid with". A refund that comes back with a different payment method cannot happen. Since the proposal's method and the refund's method are the same, which one R-09 reads from changes no behavior. The Gap class example is about an amount passed on from a tool, not a payment method.
F9 | Style only | Nit | Answer to the C-56 part: the owner says reads that time out are retried without limit ("Reads may be retried on timeout without limit") and also says "Re-read fails, say outcome unknown" and "re-read fails, say status unknown". So a failed read is something other than a timeout, which is what C-56 says. C-56 is honestly marked "spec only", and "fails" is the owner's own word. Answer to the R-01 part: "changes nothing" already follows from R-01 "acts only on an order in the signed-in customer's own order list" and R-04. What is left is the wording of a message for a case the owner gave no wording for. It changes no behavior the owner set, and the owner would not misread it.
F10 | Real | Nit | Arguably Style only (no behavior changes, and C-39 sits nine rows below in the same table). But verification.md lists exactly this pattern as Unclear: "a rule id standing in for a sentence the owner would need to read." Here a claim id, C-39, stands in for that sentence in C-30's "if it differs" column.
Count: 7 Real (F1, F2, F3, F4, F5, F7, F10), 2 Not real (F6, F8), 1 Style only (F9).
```

## Decisions and status

| finding | finder severity | verifier | decision | kept severity | status | what was done |
|---|---|---|---|---|---|---|
| F1 | Important | Real, Important | kept | Important | fixed | R-08's added sentence put to the owner (turn 5, question 17); owner replied with the record ("re-read fails, say status unknown and hand off"); sentence deleted, row merged, model changed; D-15 logged. Side effect: break R-11 (a retry that answered another amount, then a failed read, now ends "status unknown"), listed on policy.md as open. |
| F2 | Important | Real, Nit | kept | Nit | fixed | Three rows added to "What the agent does": more than one order in one message, another order after the first is settled, a fourth order. R-12's text unchanged. |
| F3 | Important | Real, Important | kept | Important | fixed | R-03 change put to the owner (question 18), accepted; R-03 text, its row, model labels and scenario labels now say "more than one open order"; D-16 logged. |
| F4 | Important | Real, Nit | kept | Nit | fixed | R-02's last sentence and R-07's shipped branch put to the owner with F7 (question 19), accepted; both now add "tells the customer returns are a separate process"; row changed; D-17 logged. |
| F5 | Important | Real, Important | kept | Important | fixed | New row and model message for a refund call that answers order not cancelled: the agent says the order system did not confirm the order is cancelled and the refund was not issued (no "the order is cancelled"); SC-25 and SC-52 cite R-09. No rule text changed. |
| F6 | Important | Not real, Important | dropped | | dropped | Refutation: "C-45: 'The refund call can also answer that the order is not cancelled, and then creates no refund.' ... Even if the case did happen, C-44 returns the same refund and R-11 covers another amount, so nothing would go against the owner." I read C-44 and agree: a repeated refund call returns the existing refund, so an open order with a refund can get no second refund and the customer is told that refund's real status. |
| F7 | Nit | Real, Nit | kept | Nit | fixed | With F4 (question 19): R-07's branch and the row now say "shipped or delivered"; model label "order read again shows it shipped or delivered". |
| F8 | Nit | Not real, Nit | dropped | | dropped | Refutation: "C-13 (Stripe docs): 'Refunds can only be sent back to the original payment method used in a charge.'" I read C-13 and agree: the refund's payment method cannot differ from the order's. |
| F9 | Nit | Style only, Nit | dropped | | dropped | Verifier: "'fails' is the owner's own word ... What is left is the wording of a message for a case the owner gave no wording for." I read F9's quote and evidence and agree it is a preference about phrasing: C-56 is marked spec only, and the owner uses "re-read fails" next to "retried on timeout", so the distinction is the owner's. |
| F10 | Nit | Real, Nit | kept | Nit | fixed | C-30's "if it differs" cell now states the handling in words instead of "C-39 applies". |

Count: 10 merged, 7 kept (3 Important, 4 Nit), 3 dropped. Fixed 7, answered 0, open 0, pre-existing 0. Open after the round: break R-11 on policy.md (a side effect of the F1 fix).
