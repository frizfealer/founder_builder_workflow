# Round 1 findings (merged; one finder)

10 findings: 6 Important, 4 Nit.

F1 | Gap | Important | rules.md "What the agent does" row "the re-read shows a refund, pending or issued"; policy.md A18
Quote: "| the re-read shows a refund, pending or issued | says the order is cancelled and the refund is pending or issued | R-07 |" and A18 "agent tells the customer: the order is cancelled and the refund of the total paid is pending or issued to the order's payment method"
Evidence: Q12 (accepted): when the refunded amount differs from the total paid the customer said yes to, the agent "makes no further change with the new amount, tells the customer the amount the refund call returned, and asks staff to follow up". C-07 says a refund shows its amount. The amount is checked only on the refund call's own answer (rows 102/103). On the timeout path (Q6 case 3: the refund call times out, then the agent re-reads), the refund read back is never compared with the amount confirmed. A18 then tells the customer "the total paid" whatever the amount. model.py `recheck_refund` has no "differs" outcome (lines 170-177, 211-212).
Pattern: an amount the agent passes on from a tool, here the re-read of the refund, has no rule for a mismatch. Every path that reports a refund to the customer needs the R-11 check.

Verifier: F1 | Real | Important | R-11 covers only part of this. It says "When the refund the order system returns is for a different amount than the customer said yes to, the agent makes no further change, tells the customer the amount the order system returned, and hands the case to staff", and C-04 says the order list "returns each order with its refund". So a rule does say what to do when a re-read shows a different amount. What stands: no row of "What the agent does" covers a re-read with a different amount. Row 103 is only for "the refund call answered with a refund for a different amount". Row 109 ("the re-read shows a refund, pending or issued") and A18 ("the refund of the total paid") send that case to the success message, and model.py's recheck_refund has no "differs" outcome. The Gap definition names a case no row covers, and cockburn-checklist.md says "A row that branches on a lookup covers every result: ... a record that does not match".
Decision: kept (Important) | fixed: re-read "different amount" outcome, row, model steps, SC-40

F2 | Lies | Important | rules.md row "the refund call answered that the order is not cancelled"; policy.md A3; R-07
Quote: "| the refund call answered that the order is not cancelled | asks staff to follow up (refund not issued) | R-06, R-10 |", which leads to A3 "agent tells the customer: the order is cancelled, but the refund is not issued or not confirmed; store staff will follow up"
Evidence: C-13 / Q9 change 2: the refund call answers OrderNotCancelled. R-07: "What the agent tells the customer last matches what the order system shows". Q6 case 3: "Final message must match the final refund status." On this path the order system has just said the order is not cancelled, and the customer is told "the order is cancelled". model.py lines 209 and 70 confirm the refund_not_issued wording is used for `not_cancelled`.
Pattern: one customer message is reused for an outcome whose facts contradict it. Each follow-up reason needs a message that is true for every outcome that leads to it.

Verifier: F2 | Real | Important | I could not refute it. Nothing makes the OrderNotCancelled answer impossible: the owner added it as an outcome (Q9 change 2). R-06 ("It asks for a refund only for an order it knows is cancelled") does not say what the customer is told when the refund call answers anyway. Row 107 sends this outcome to refund_not_issued, and model.py line 71 words that as "the order is cancelled, but the refund is not issued or not confirmed". That contradicts what the order system just answered and R-07 ("What the agent tells the customer last matches what the order system shows"). The model never reaches this step, because the agent refunds only after it sees "cancelled", which is why the checker did not flag it.
Decision: kept (Important) | fixed: own customer wording for the "order not cancelled" refund answer

F3 | Lies | Important | policy.md A3 (and the refund_not_issued wording); rules.md row "the re-read shows the refund failed, or no refund"
Quote: "agent tells the customer: the order is cancelled, but the refund is not issued or not confirmed; store staff will follow up"
Evidence: Q7 record: "For case 3, after the retry the agent re-reads the refund record: ... failed or no refund, hand off and say the refund is not confirmed yet". Q6 case 2 (refund error) is a different case: "agent reports it, does not claim success". The spec merges both into "not issued or not confirmed". So the agent may tell a timeout-path customer "not issued" where the owner said "not confirmed yet", and the "yet" (the refund may still come) is lost.
Pattern: the owner's wording for what the agent tells the customer is replaced by a merged paraphrase. Keep the owner's words for each case.

Verifier: F3 | Real | Important | I could not refute it. For the timeout path the owner gave the words to tell the customer: "failed or no refund, hand off and say the refund is not confirmed yet" (Q7). C-38 ("handed to staff as not confirmed") and A3 ("the refund is not issued or not confirmed") drop "yet" and add "not issued". That departs from the owner's wording in the way the Lies class names. Nothing in the spec words the timeout case separately from the refund-error case (Q6 case 2).
Decision: kept (Important) | fixed: "was not issued" after a refund error; "is not confirmed yet" after the re-read; C-38 updated

F4 | Gap | Important | claims.md C-47 (cited by no rule); rules.md rows "the order list got no answer", "the re-read of the order got no answer", "the re-read of the refund got no answer"
Quote: C-47 what ends it: "nothing set: an open question for the owner; the model treats a read with no answer as one still unanswered after the agent stops retrying"
Evidence: Q9 change 4: "Reads may be retried on timeout without limit; only commit calls are bounded." No rule carries this: C-47 and C-06 appear in no "Rests on" line. No rule says whether or how many times the agent retries a read. The rows act on the first "got no answer", and the row for the order list cites R-07, which says nothing about it. The spec calls the read's end "an open question for the owner", but neither rules.md nor any decision records or raises that question.
Pattern: a repeated thing (the read retry) has no end, and a recorded owner answer is carried by a claim but by no rule.

Verifier: F4 | Real | Nit | One part is refuted. C-47 carries the Q9 answer ("Reads ... may be retried on timeout without limit; only cancel, refund and follow-up calls are bounded"), so "a recorded answer that no rule and no claim carries" does not hold. What stands: no rule says whether or how long the agent retries a read. C-47's "what ends it" is "nothing set: an open question for the owner", and no decision records or raises that question. That fits "a repeated thing with no end". I rate it Nit: the rows act on the first read with no answer, and that is within what the owner allowed ("may be retried"), so a built agent does not go against the answer.
Decision: kept (Nit, verifier lowered from Important) | open: bound of three read tries proposed to the owner (question 15); the reply kept reads unbounded

F5 | Gap | Important | rules.md R-12, D-03, "What the agent does"; policy.md chart (all end states in "Conversation over")
Quote: absent. No rule sentence or row covers the customer asking to cancel another order after one is done, or asking for two orders in one message.
Evidence: Q8 (accepted): "After one order is done, the customer may ask to cancel another of their orders; the conversation ends when they have no other order to cancel or stop asking." D-03 records the decision, but R-12 says only "one order at a time". Every end state in the chart is in "Conversation over". scenarios.md SC-33 and SC-34 describe both cases as "conversational", yet no row tells the agent what to do. An agent built from the rules table ends after the first order.
Pattern: a case the agent will meet (a second order named after or alongside the first) has no row in "What the agent does".

Verifier: F5 | Real | Nit | Partly answered. R-12 says "The agent works on one order at a time, each with its own proposal and its own yes". D-03 and C-41 say "the conversation ends when the customer has no other order to cancel or stops asking". Together they say what the agent does for a second order and for two orders in one message. What stands: no row of "What the agent does" covers either case, and the Gap definition gives exactly these as examples. Every end state in the chart also sits in "Conversation over". I rate it Nit rather than Important because R-12, C-41 and D-03 all state the behavior.
Decision: kept (Nit, verifier lowered from Important) | fixed: rows for a second order and for two orders in one message

F6 | Lies | Important | scenarios.md SC-38
Quote: "the customer asks when the refund will reach them, and the agent promises no date."
Evidence: Q4 record: "The agent promises nothing about when the money arrives." (C-34, R-07). "Promises no date" is narrower. A reply such as "about 5-10 business days" (the wording in docs.stripe.com/refunds, packet line 30) names no date, so it would pass this scenario while breaking the owner's rule.
Pattern: a test's wording narrows the owner's rule. Use the owner's words: "promises nothing about when the money arrives".

Verifier: F6 | Real | Nit | I could not refute it. SC-38's "promises no date" narrows the owner's rule in exactly the way the Lies definition gives as its example ("promises nothing about when" written as "names no date"). The agent's own behavior is carried right by R-07, which SC-38 cites: "it promises nothing about when the money arrives". Only the scenario's wording is narrowed, so a test built from it could pass "about 5-10 business days". That is why I rate it Nit.
Decision: kept (Nit, verifier lowered from Important) | fixed: SC-38 uses the owner's words

F7 | Gap | Nit | rules.md "What the agent does"
Quote: absent. There are no rows for: the customer asks to cancel part of an order; asks for store credit or a refund to another card; asks a question about cancelling while a proposal waits; changes to a different order before saying yes (R-05 covers only "after saying yes"); asks when the money arrives.
Evidence: R-04, R-06, R-12 and C-32, C-33, C-34 state the limits (Q4: "full-order cancellation only (no partial)", "No cancellation fee, no store-credit option", "The agent promises nothing about when the money arrives"; Q5: "A question about cancelling ... is not a yes"). scenarios.md SC-35, SC-36, SC-37 and SC-38 name these cases, but no row says what the agent replies. The chart's "Proposal waiting for yes" has no arrow for a non-yes reply or a change of order.
Pattern: a rule states a limit, but no row says what the agent does when the customer meets it.

Verifier: F7 | Real | Nit | Partly answered. Each limit has a rule: R-12 "It does not cancel part of an order"; R-06 "with no fee and no store credit"; R-04 "A question about cancelling, or saying they are thinking of cancelling, is not a yes"; R-07 "it promises nothing about when the money arrives". What stands: no row of "What the agent does" says what the agent replies in these cases. No rule at all covers a change of order before the yes; R-05 is only for a change "after saying yes". SC-35 to SC-38 describe the replies only as conversational scenarios.
Decision: kept (Nit) | fixed: rows for part of an order, store credit or another card, a question while a proposal waits, a switch before the yes, when the money arrives; R-05 widened (accepted, question 16)

F8 | Lies | Nit | rules.md rows at lines 84, 108, 115
Quote: "| the order list got no answer | says it cannot see their orders right now and changes nothing | R-07 |"; "| the second refund call got no answer, or answered with a temporary error after the first got no answer | re-reads the order's refund | R-09 |"; "| the customer stops answering | does nothing more | R-04 |"
Evidence: R-07 says nothing about an unanswered order list. R-09 re-reads only "When the second refund call also got no answer", not after a temporary error that follows a timeout. R-04 covers withdrawing, not going silent.
Pattern: a row of "What the agent does" states behavior the rule it cites does not contain.

Verifier: F8 | Style only | Nit | Row 115 ("the customer stops answering | does nothing more") is supported by the rule it cites, R-04: "The agent cancels only after the customer says yes to the full proposal". Row 84 is consistent with R-07 ("matches what the order system shows"; the system showed nothing), and R-04 covers "changes nothing". Row 108 goes beyond R-09's last sentence, but R-09 rests on C-37: "After a refund call times out, the agent sends it once more, then re-reads the order and refund records". The behavior in all three rows is what the owner asked for (Q6 case 3). Only the cited rule ids are loose, so no agent behavior changes and the owner would not misread the rows.
Decision: kept (Nit; verifier said Style only, not dropped: a row citing a rule that lacks its behavior is not a phrasing preference) | fixed: order-list row cites R-04; re-read row matches R-09 after the F9 change

F9 | Lies | Nit | rules.md R-09 (last sentence), R-08; claims.md C-37
Quote: "When the second refund call also got no answer, the agent re-reads the refund before it reports the refund's state."
Evidence: Q6 case 3: "agent retries once, then re-reads the order and refund records and reports what it finds." Q7 record: "after the retry the agent re-reads the refund record". The owner puts the re-read after the retry whatever the retry answers, and re-reads both the order and the refund. The spec re-reads only when the retry is also unanswered (or a temporary error), and re-reads only the refund. Because the refund call is idempotent (C-16), the outcomes match, so behavior barely changes.
Pattern: a rule narrows the owner's condition ("then re-reads") to a subset of cases.

Verifier: F9 | Real | Nit | One part is refuted. The order list "returns each order with its refund" (C-04), so re-reading the refund also re-reads the order. "re-reads only the refund" does not hold. What stands: R-09 re-reads only "When the second refund call also got no answer", while the owner said "retries once, then re-reads ... and reports what it finds" whatever the retry answers. Because of C-16 ("returns the same refund and never creates a second refund"), the outcomes match, so I rate it Nit.
Decision: kept (Nit) | fixed: R-09 change put to the owner (question 14); the reply restated the owner's words, which match the "After" text; applied, D-07

F10 | Lies | Nit | claims.md C-10
Quote: "A cancel call that times out may or may not have cancelled the order, so the agent does not resend it blindly and re-reads the order first." (quote: "If the cancel call times out: no blind resend; re-read the order.")
Evidence: The owner's Q11 reply gives the instruction only. "may or may not have cancelled the order" comes from the question text (Q11), not the reply, yet the source is marked "owner's words".
Pattern: a claim says more than its quote, here by taking the question's premise as the owner's words.

Verifier: F10 | Style only | Nit | The owner's own reply to Q11 states both possibilities: "Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation." C-44 quotes that line. So "may or may not have cancelled the order" is supported by the owner's words, just not by the part C-10 quotes. No behavior changes, and the owner would not misread it.
Decision: kept (Nit; verifier said Style only, not dropped: a claim saying more than its quote is not a phrasing preference) | fixed: C-10 narrowed to its quote; premise moved to C-50

Verifier count: Count: 8 Real, 0 Not real, 2 Style only (F8, F10).
