# Round 1 findings (merged, verbatim)

Finder count line: "8 findings: 5 Important, 3 Nit." (the report lists 9: F1 to F9, 5 Important, 4 Nit).
Verifier count line: 4 Real (F1, F3, F5, F7), 5 Not real (F2, F4, F6, F8, F9), 0 Style only.

Result: 9 merged, 6 kept, 3 dropped. Important: 5 verified, 0 dropped (drop rate 0/5). Nit: 4 verified, 3 dropped (drop rate 3/4). Pre-existing: 0.

```
F1 | Lies | Important | claims.md C-06, C-07; rules.md R-01, R-07, R-09; rows "the list call failed with an error", "the re-read after a cancel call failed with an error", "the refund re-read failed with an error"
Quote: "C-06 | A call to list the customer's orders answers with the orders, gets no answer, or fails with an error. | system | order system | spec only" / "C-07 | When the first list call fails with an error, the agent tells the customer it cannot see their orders right now and changes nothing. | policy | | spec only" / R-01: "when it fails with an error, the agent says it cannot see the customer's orders right now and changes nothing"
Evidence: Question 10 described the list call to the owner as returning the orders "; it can also get no answer". It named no error outcome. The owner confirmed the call and changed only "4. list_orders includes cancelled orders. Reads may be retried on timeout without limit". C-07 was put to the owner in Question 13(a) as the case where the first list call gets no answer. The owner answered "No. The record says: ... Reads may be retried on timeout without limit". The spec then kept the id C-07 and moved it to a new outcome, "fails with an error", which no input mentions. C-06 is tagged kind "system", so it states how Harbor Goods' order system behaves, but it has no source. Every "re-read fails with an error" branch in R-07 and R-09 (and the owner's "re-read fails ... hand off" handling) now depends on this made-up outcome.
Pattern: A system claim about tool behavior with no source, made up to settle a conflict in the owner's answers (unlimited read retries against "re-read fails, hand off") instead of asking the owner. This includes reusing a claim id the owner rejected for a different statement.
```

Verifier: F1 | Real | Important | This is only partly refuted. The owner's record does say re-reads can fail, apart from timeouts: "Re-read fails, say outcome unknown, issue no refund, hand off" (Q9/Q13/Q14/Q17) and "re-read fails, say status unknown and hand off" (Q9 Q3). "Reads may be retried on timeout without limit" means that failure can only be something other than a timeout. That supports the third outcome in C-06 and the "re-read fails with an error" branches in R-07 and R-09. What stands is the first list call failing with an error: C-07 and that clause of R-01 ("says it cannot see the customer's orders right now and changes nothing"). No owner text supports that message. The owner answered "No" to the same message in Q13(a). "Derive any further cases yourself" (Q6) only permits derived cases, so it does not refute. The reused C-07 id changes no behavior.

Decision: KEPT (Important). OPEN. The error outcome of C-06 is supported by the owner's "re-read fails" answers (the verifier's partial refutation); what stands is what the agent does when the first list call fails with an error (C-07, R-01's last clause). No answer covers it and the decision turns are spent, so only the owner can decide it: open question in the report. C-07 stays spec only.

```
F2 | Gap | Important | claims.md C-50; rules.md R-01, R-07, R-09; rows "the list call got no answer", "a re-read got no answer"
Quote: "C-50 | ... | none: the owner set no limit |" / R-01: "When the call to list the orders gets no answer, the agent sends it again, with no limit"
Evidence: Question 14 asked what ends a list call that keeps getting no answer. The owner answered "No. The record says: Reads may be retried on timeout without limit". The spec carries the owner's choice faithfully, but nothing ends the loop. No row or chart step says what the customer is told while it runs, or what happens if the customer leaves while the agent is still in "Looking up orders". The chart gives "Customer left" only for the waiting states (A11, A13, A15). After a cancel or refund call, an unanswered re-read loops the same way, so the owner's "re-read fails, hand off" can never fire on timeouts.
Pattern: A repeated call with no end and no message to the customer while it repeats. Either record it as an open risk for the owner, or give the customer a message and an exit.
```

Verifier: F2 | Not real | Nit | The owner was asked exactly this in Q14 ("the conversation could go on forever. What ends it?") and answered "Reads may be retried on timeout without limit; only commit calls are bounded." The spec logs that as the owner's decision, D-06 ("may be sent again with no limit … the owner"), and C-50 records "what ends it: none: the owner set no limit". That is what the checklist asks for: "When the owner chooses not to protect one, log that as a decision." It also meets the finding's own remedy ("record it"). "Re-read fails can never fire on timeouts" is the owner's own design, and the R-07/R-09 error branches still fire. Weakest point if the main thread disagrees: no row says what the customer is told while the list call keeps repeating.

Decision: KEPT (Nit, verifier's severity). ANSWERED / OPEN. The verifier's lines (D-06, C-50) refute the "no end" part: the owner chose no limit. They do not cover what the customer is told while reads repeat, or the customer leaving mid-retry, which the verifier names as standing. Only the owner can decide that: open question in the report.

```
F3 | Lies | Important | claims.md C-47; rules.md R-04; row "the customer said yes, then asked for a different refund amount or payment method"; policy.md A4/A9
Quote: "C-47 | When the customer changes the proposal after saying yes, the agent says the refund is the order's total paid to its payment method and asks for a yes to the proposal again. | policy | | spec only" / R-04: "the agent then says the refund is the order's total paid to its payment method and asks for a yes to the proposal again."
Evidence: Question 17(b) put this exact behavior to the owner (C-47), with the alternative "otherwise it would end the conversation without cancelling". The recommendation was "Yes to both". The owner replied "No. The record says:" and quoted only "any change after confirmation voids it" and the refund-amount rule. The quotes say nothing about restating and asking again. The spec adopted the recommendation the owner turned down, and records no decision showing which half of the "No" applied to (a) and which to (b).
Pattern: A rule carries a recommendation the owner answered "No" to, with no owner text supporting it. The question needs to go back to the owner, or the rule should be limited to what the record says.
```

Verifier: F3 | Real | Important | The Q17(b) reply is "No. The record says:". The quotes it gives ("any change after confirmation voids it", "refund amount = order total paid; refund payment method = order's payment method") support only half of C-47/R-04: the yes is void, and any proposal can only offer the total paid to the order's payment method. Nothing supports asking for a yes again rather than ending without cancelling. The owner also dropped "and the agent asks again" from the Q4 recommendation. C-47 is tagged "spec only".

Decision: KEPT (Important). FIXED. R-04's text change went to the owner as a proposal (log question 18) and was accepted; applied, logged as D-10, C-47 now carries the accepted text.

```
F4 | Gap | Important | rules.md R-13; "What the agent does" table; policy.md chart steps
Quote: "absent" (R-13 has no row in "What the agent does" and no arrow in the policy)
Evidence: Question 8 (accepted): "each order gets its own proposal and its own yes, and the agent finishes one before it starts the next." No row covers a customer who asks to cancel two orders in one message. None covers a second order named partway through, for example while a proposal is waiting or after the yes ("cancel HG-10482 ... actually HG-10490 too"). The policy has no arrow from a terminal state (Cancelled and refunded, Handed to staff, Nothing changed) back to "Looking up orders", so the "start the next" step cannot happen. The A9 row covers a changed amount or payment method only, not a changed order, though C-31 says "Any change after the confirmation voids it" and the proposal includes "which order".
Pattern: A rule with no row and no path in the policy. Cases with two requests in one message, or a second order named partway through, are not handled.
```

Verifier: F4 | Not real | Nit | R-13 says what the agent does in exactly these cases: "the agent handles one order at a time: each order gets its own proposal and its own yes, and the agent finishes one before it starts the next". That covers two orders in one message and a second order added while a proposal waits or after the yes. The policy-path point is settled by model.py: "A second order in the same conversation starts a new run (R-13)". SC-41 and SC-45 give the same handling ("the earlier yes covers nothing for it"). An order changed after the yes is voided by R-04: "Any change to the proposal after the yes voids it".

Decision: KEPT (Nit, verifier's severity). FIXED. I read R-13; it says what the agent does, but the Gap class names a case "no row of 'What the agent does' covers, such as two requests in one message", and there was no row. Added the row "the customer asked to cancel more than one order, in one message or one after another" citing R-13; SC-41 and SC-45 stay as its conversational scenarios.

```
F5 | Lies | Important | policy.md A3; rules.md R-10, R-09
Quote: A3: "agent tells the customer: the order is cancelled and the order system returned a refund amount that differs from the one you agreed; store staff will follow up on the order" / A3: "agent tells the customer: the order is cancelled but the refund is not confirmed yet; store staff will follow up on the order"
Evidence: R-10 and the owner's accepted Question 7 answer say the agent "tells the customer the amount the order system returned". None of the A3 messages for the amount mismatch gives the amount. Question 9 / Q3 record: "failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off". R-09 keeps the difference ("The re-read fails with an error: it says the status is unknown"). A3 has no "status unknown" message, so the re-read-error case can only use "not confirmed yet".
Pattern: The policy's wording for what the customer is told departs from the rule and the owner's words. It drops a detail the owner said to give (the amount returned) and merges two messages the owner kept separate.
```

Verifier: F5 | Real | Important (borderline Nit) | Only the first half is refuted. The missing amount in A3 comes from the model's abstraction: model.py says "The model does not carry amounts", and R-10 still says the agent "tells the customer the amount the order system returned". What stands is the refund re-read error. The owner said "re-read fails, say status unknown", and R-09 keeps that ("it says the status is unknown"). But model.py sends refund_reread == "error" to handoff "refund_status_unknown", which says "the order is cancelled but the refund is not confirmed yet". A3 has no "status unknown" message, so the policy merges two messages the owner kept separate.

Decision: KEPT (Important). FIXED. The amount-differs message now states the returned amount ("the order system returned a refund of <the amount it returned>, which differs from the total you agreed"), and a refund re-read that fails with an error now tells the customer "the refund's status is unknown" (new message in model.py and the row). Searched every other message against the owner's wording; no other instance.

```
F6 | Lies | Nit | rules.md R-12; row "the second follow-up task call got no answer"; policy.md A3 "please contact Harbor Goods support" steps
Quote: R-12: "if that gets no answer too, it tells the customer what is known so far and to contact Harbor Goods support."
Evidence: The owner's words (Question 10 change 3, quoted again in Question 11): "On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support." The "what is known so far" part comes from the Question 11 recommendation, and the owner did not accept it: the reply was only the record. D-04 states the owner's wording without it.
Pattern: The spec adds recommendation text to the owner's wording for what the customer is told.
```

Verifier: F6 | Not real | Nit | In every handoff case the owner's own words say to tell the customer the state, whether or not the task call succeeds: cancellation unknown: "Re-read fails, say outcome unknown, issue no refund, hand off"; refund status unknown: "re-read fails, say status unknown and hand off"; refund not issued: "agent reports it, does not claim success"; amount differs: "tells the customer the amount the order system returned" (Q7, accepted); in general: "Final message must match the final refund status" (C-43). So "what is known so far" in R-12 is supported in this case, not added by the recommendation. The Q11 reply is not a "No" either.

Decision: DROPPED. Refutation: C-43 "Final message must match the final refund status." and the owner's "Re-read fails, say outcome unknown, issue no refund, hand off". I read them and agree: the owner asks for the state to be told in each hand-off case, so "what is known so far" is supported.

```
F7 | Lies | Nit | rules.md row "the customer asked to cancel only some items"
Quote: "says only the whole order can be cancelled, and asks whether to cancel the whole order | R-03"
Evidence: R-03 and the owner's record (Question 3): "A request to cancel only some items: the agent says only the whole order can be cancelled." Neither says the agent asks whether to cancel the whole order.
Pattern: A row of "What the agent does" adds a step that the rule it cites does not contain.
```

Verifier: F7 | Real | Nit | R-03 ("When the customer asks to cancel only some items, it says only the whole order can be cancelled") and the owner's record ("A request to cancel only some items: the agent says only the whole order can be cancelled") have no step that asks. No spec line or answer supports "and asks whether to cancel the whole order". "Derive any further cases yourself" only permits it. It adds a question, not a write, so it is a Nit.

Decision: KEPT (Nit). FIXED. The row now reads "says only the whole order can be cancelled", and the model step no longer asks a question ("agent tells the customer only the whole order can be cancelled"); the customer may then ask for the whole order.

```
F8 | Gap | Nit | rules.md rows "the cancel call answered that the order cannot be cancelled because it shipped", "the re-read shows the order shipped"; R-06, R-07
Quote: "the cancel call answered that the order cannot be cancelled because it shipped" / "the re-read shows the order shipped"
Evidence: C-08 and the owner's Question 10 change 1: "OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered)". No row covers a cancel reply, or a re-read after an unanswered cancel, that shows the status delivered.
Pattern: A tool outcome the owner listed with two values is handled for only one of them.
```

Verifier: F8 | Not real | Nit | A delivered order has shipped. R-06 says what the agent does: "When the order shipped before the cancel went through, the agent tells the customer so truthfully and sends no refund call". The owner's C-26 covers both statuses: "for a shipped or delivered order the agent says it cannot cancel and changes nothing". The existing row message, "the order shipped before it could be cancelled, so nothing was cancelled or refunded", is also true of a delivered order.

Decision: DROPPED. Refutation: C-26 "For a shipped or delivered order the agent says it cannot cancel and changes nothing." and R-06's "When the order shipped before the cancel went through, the agent tells the customer so truthfully and sends no refund call." I read them and agree: the delivered case gets the same handling and the same true message.

```
F9 | Gap | Nit | rules.md R-10, R-11; row "the refund call answered issued or pending, with the total the customer said yes to"
Quote: "says the order is cancelled and the refund of that amount to that payment method is issued or pending, with its refund id"
Evidence: The customer's yes covers "where it goes" (Question 4: "which order, the refund amount and where it goes"). The refund record returns a payment method (C-12, Question 10: "returns the refund (refund id, amount, payment method, status ...)"). R-10 checks only the amount against what was confirmed. Nothing says what the agent does when the returned payment method differs from the one the customer said yes to. C-17 (Stripe sends only to the original method) makes this unlikely but does not rule it out for the order system's record.
Pattern: A confirmed value is passed on from a tool with nothing said about a mismatch (the payment method; the amount is covered).
```

Verifier: F9 | Not real | Nit | No claim lets the refund record show a different payment method, and C-17 rules it out: "Refunds can only be sent back to the original payment method used in a charge. You can't send a refund to a different destination" (docs.stripe.com/refunds). The owner's C-33 adds "refund payment method = order's payment method". The Gap class names only an amount passed on from a tool, and the amount is covered (R-10). Weakest point: the checklist's brainstorm item "the system answers wrongly" could be read as covering this.

Decision: DROPPED. Refutation: C-17 (docs.stripe.com/refunds) "Refunds can only be sent back to the original payment method used in a charge." I read it and agree: the refund cannot go to another payment method, so there is no mismatch to handle.
