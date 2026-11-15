# Round 1 findings (merged, verbatim) with verifier verdicts and decisions

Finder count line: 7 findings: 4 Important, 3 Nit.
Verifier count line: 5 Real (F1, F2, F5, F6, F7), 2 Not real (F3, F4), 0 Style only.
Decision: 5 kept (2 Important, 3 Nit), 2 dropped (F3, F4). Pre-existing: 0.

F1 | Gap | Important | rules.md R-01, R-08, R-10; claims.md C-04, C-45; rules.md "What the agent does" row "the order list call timed out"
Quote: "When the order list call times out, it sends it again; the owner set no limit on this." (R-01); "When the read fails, the agent says the outcome is unknown, makes no refund, and asks staff to follow up" (R-08); "the read fails, it asks staff to follow up with the reason refund status unknown" (R-10)
Evidence: The owner turned down the 3-try bound (packet Q13, "Reads may be retried on timeout without limit"), and the spec records that nothing ends it (C-04 "none set", C-45 "missing"). But the owner's own words also give branches for a read that fails: "Re-read fails, say outcome unknown, issue no refund, hand off" (Q10/Q11/Q13 record, Q4) and "re-read fails, say status unknown and hand off" (Q9/Q13 record, Q3). If a read that times out is always sent again, then "the read fails" in R-08 and R-10 never happens, or it means something the spec never defines. So nothing ends a re-read loop after a cancel or refund call that got no answer, and the customer waits forever. C-04 also says the list call can "fail", but no row says what the agent does when a read fails before any proposal.
Pattern: A read sent again with no end, while other rules depend on that read "failing". Either define what counts as a failed read (an error that is not a timeout, or a bound) or go back to the owner, because the owner's answers contradict each other.

Verifier: F1 | Real | Important | Partly answered. C-04 says "The order list call can time out or fail", so a failure is something other than a timeout. And R-01 ("When the order list call times out, it sends it again") covers a re-read that times out, since the list call is the only read tool. So "the read fails" in R-08 and R-10 can still happen and is not undefined. Two parts stand. (1) The resend after a timeout has no end: the owner declined the bound in Q13, C-45 records it as "missing" and SC-40 admits "the owner set no end to it". The checklist names "a repeated thing with no end" as a Gap. (2) No row of "What the agent does" covers a list call that fails, as distinct from timing out, before any proposal. The owner's Q12 reply did not answer that case either.

Decision: KEPT (Important). Status: fixed in part, open in part. Part (2) fixed: R-01 change put to the owner (question 20), accepted; row, model step, C-58, C-59, SC-45 and D-10 added. Part (1) open: the owner declined a bound on read retries (question 13); C-45 stays missing; reported as an open question.

F2 | Lies | Important | rules.md R-07
Quote: "The agent sends the refund call only after the cancel call answered cancelled."
Evidence: The owner said that after a cancel call with no answer, if a re-read shows the order "Cancelled, continue to refund" (packet Q10/Q11, record Q4). Q16 states the condition as "only after the cancel call answered cancelled or a re-read showed the order cancelled". R-08 and R-12 allow the refund after a re-read, and the row "the order read again shows it cancelled | refunds the order | R-07, R-08" cites R-07 even though R-07, read literally, forbids that refund.
Pattern: A rule narrows the owner's condition. Its own row and its sibling rules then contradict it.

Verifier: F2 | Real | Important | I could not refute it. R-08 ("When the order shows cancelled, it goes on to the refund") and R-12 ("only when a cancel call answered cancelled or the order read again shows it cancelled") follow what the owner said. But R-07, read alone, still forbids the refund after a re-read, so it narrows the owner's Q4 answer ("Cancelled, continue to refund"). Severity is open to argument: because R-08 states the specific case, an agent may well refund anyway, which would make this a Nit.

Decision: KEPT (Important). Status: fixed. R-07 change put to the owner (question 17); the owner's recorded answer ("Cancelled, continue to refund") supports the new text; applied, D-07 logged.

F3 | Gap | Important | policy.md chart (states in "Conversation over"; A7, A20); rules.md D-02, R-04; claims.md C-42
Quote: "Each order is handled on its own, with its own proposal and its own yes; nothing else bounds how many orders one conversation cancels." (D-02) The chart puts "Cancelled and refunded, customer told" and "Nothing changed, customer told" in "Conversation over", with no arrow back out.
Evidence: Packet Q8 (accepted): the conversation ends "when no order of the customer's is left that can be cancelled, or when the customer stops asking". In the spec, the conversation ends after the first order reaches any outcome, even if a second order is already cancelled, already done or still open. No row covers a customer who asks for a second order after the first is finished, and none covers two requests in one message ("cancel both"). For that message R-04 has the agent "ask which one", which does not answer it.
Pattern: The owner said the conversation repeats per order, but the policy stops after one. Add a path back after each outcome, plus a row for several orders named in one message.

Verifier: F3 | Not real | Important | D-02 settles both cases: "Each order is handled on its own, with its own proposal and its own yes; nothing else bounds how many orders one conversation cancels" (reason: "A conversation ends when no order is left that can be cancelled, or when the customer stops asking"). C-42 gives the same end in its "what ends it" column. For a second order after the first is done, the row "the customer asks to cancel an order | reads the customer's orders" applies, and SC-39 says it "starts again from reading the orders, with its own proposal and yes". For "cancel both", D-02 gives each order its own proposal and yes (SC-38: "each must get its own proposal and its own yes"). R-04 is about an unclear order, which "cancel both" is not. The chart ends after one order because the model is scoped that way: model.py says "A customer who asks to cancel a second order starts a new run". One thing left over: the chart's group name "Conversation over" could be raised as a separate Unclear Nit, but it is not this Gap.

Decision: DROPPED. Refutation read and agreed: D-02 "Each order is handled on its own, with its own proposal and its own yes; nothing else bounds how many orders one conversation cancels", with SC-38 and SC-39 saying what the agent does for two orders in one message and for a second order afterwards.

F4 | Unclear | Important | rules.md "What the agent does", row "a refund call went unanswered, and the second refund call has answered"
Quote: "a refund call went unanswered, and the second refund call has answered | reads the refund again"
Evidence: Everywhere else the spec sets "answered" against "got no answer" (for example "the refund call answered a passing error or got no answer, the first time"). Read that way, no row covers the owner's own case 3: both refund calls get no answer. The owner said "agent retries once, then re-reads the order and refund records and reports what it finds" (packet Q6, case 3). model.py re-reads whenever `refund_unanswered and refund_calls >= 2`, whatever the second call returned. The row's wording leaves out the case the model covers.
Pattern: A row's condition uses a word ("answered") that the spec uses elsewhere in a narrower sense, so the row seems to leave out a case the owner named.

Verifier: F4 | Not real | Nit | R-10 settles the case of both refund calls getting no answer, with no condition on what the second call returned: "When a refund call got no answer, the agent sends it once more and then reads the refund again". C-55 says the same: "After a refund call with no answer and its second call, the agent reads the refund again". The row's word "answered" is loose, but R-10 fixes the behavior, so this is Nit at most, not Important.

Decision: DROPPED. Refutation read and agreed: R-10 "When a refund call got no answer, the agent sends it once more and then reads the refund again" states the behavior for both calls unanswered; the row's condition does not change it.

F5 | Unclear | Nit | claims.md C-30 (first use), C-32; rules.md R-09, R-10
Quote: "On a lasting error the refund call returns a refund with status failed; on a passing error it creates no refund." (C-30)
Evidence: The owner said "transient" and "terminal" (packet Q6 case 2; Q9 record Q3). The spec's own terms "passing error" and "lasting error" are first used in C-30 and defined only at C-54, 24 rows later. R-09 defines "lasting error" in part, but never says what a "passing error" is.
Pattern: A term the spec coined, with no one-line definition where it first appears.

Verifier: F5 | Real | Nit | I could not refute it. C-30 is the first use of "passing error" and "lasting error", and their definitions only come at C-54. R-09 defines only "lasting error" ("which returns a refund with status failed"). references/verification.md names exactly this as Unclear: "A term the spec coins with no one-line definition where it first appears".

Decision: KEPT (Nit). Status: fixed. C-30 now defines both terms where they first appear.

F6 | Lies | Nit | claims.md C-26, C-04
Quote: "A refund can fail after it is issued, when the customer's bank or card issuer cannot process it." (C-26); "The order list call can time out or fail." (C-04)
Evidence: C-26's quote is "A refund can fail if the customer's bank or card issuer can't process it." (packet, Docs pages read). It says nothing about "after it is issued". C-04's quote is "Reads may be retried on timeout without limit; only commit calls are bounded." It says nothing about the call failing apart from a timeout.
Pattern: A claim says more than the passage it quotes.

Verifier: F6 | Real | Nit | Partly answered. C-04's "fail" has support in the owner's words: packet Q10/Q11/Q13 record "Re-read fails, say outcome unknown" and Q9/Q13 record "re-read fails, say status unknown". So the claim is true even though its own quote column leaves the failure out. C-26 stands: no sentence the packet lists from the Stripe page says "after it is issued", and its quote is "A refund can fail if the customer's bank or card issuer can't process it."

Decision: KEPT (Nit). Status: fixed. C-26 drops "after it is issued"; C-04 says only "can time out"; the read failure is its own claim C-58 quoting "Re-read fails, say outcome unknown, issue no refund, hand off."

F7 | Lies | Nit | rules.md "What the agent does" rows citing R-12, R-10 and R-04
Quote: "the cancel call answered order not found | says the order was not found, and changes nothing | R-12"; "the staff follow-up call answered created | tells the customer what it knows and that store staff will follow up | R-10, R-12"; "the customer has two orders that have not shipped and did not say which | lists them and asks which one | R-04"
Evidence: R-12 says nothing about a cancel call answering order not found. That behavior is only in C-49, which R-12 lists under "Rests on". R-10 never says the agent tells the customer that store staff will follow up. R-04 says "When the customer could mean more than one order", but the row (and policy A1) narrows that to "two orders", so no row covers three or more.
Pattern: A row in "What the agent does" says something the rule it cites does not, or narrows that rule. Put the behavior in the rule's text, or match the row to the rule.

Verifier: F7 | Real | Nit | I could not refute any of the three rows. (a) R-12's text never mentions a cancel call answering order not found. Only C-49, which is "spec only", says it, and R-01's no-match sentence is about the customer's number, not the cancel answer. (b) R-10 never says "store staff will follow up". That wording is in R-08, C-51 and C-52, and R-08 is not cited on that row. (c) The row says "two orders" where R-04 says "more than one order", so the row narrows the rule it cites. Agent behavior is likely unchanged because R-04 governs, so Nit.

Decision: KEPT (Nit). Status: fixed. (a) R-12 change put to the owner (question 19), accepted, D-09; C-49 now proposed, accepted. (b) R-10 change put to the owner (question 18), accepted, D-08. (c) Row now reads "more than one order that has not shipped".
