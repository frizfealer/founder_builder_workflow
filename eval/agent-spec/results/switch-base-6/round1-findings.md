# Round 1 findings

Merged findings of the round-1 faithfulness finder, verbatim, each with the adversarial verifier's verdict line, the keep/drop decision and the outcome.

Finder count line: 8 findings: 6 Important, 2 Nit.
Verifier count line: 5 Real (3 Important, 2 Nit), 3 Not real, 0 Style only.

## Findings, verbatim

F1 | Gap | Important | rules.md R-01, R-07, R-08, D-08; claims.md C-37; rules.md "What the agent does" rows "the lookup got no answer", "the re-read of the order got no answer", "the re-read of the refund got no answer"
Quote: "When the lookup of the customer's orders gets no answer, the agent tries it again, with no limit." / "A re-read that gets no answer is tried again, with no limit." / C-37 what ends it: "nothing: the owner set no limit on a read with no answer; a read that fails ends it"
Evidence: Q13 asked the owner exactly this: "Nothing then ends a lookup or a re-read that keeps getting no answer, and the customer waits for ever. What ends it?" The owner did not answer it. The reply only repeats the earlier line: "Reads may be retried on timeout without limit; only commit calls are bounded." The spec's own "what ends it" column says "nothing". Per the tool contract the owner confirmed (Q9), a read that keeps getting no answer never reaches the "fails" exit. So the lookup (R-01), the order re-read (R-07) and the refund re-read (R-08) can each loop for ever. D-08 logs "the owner kept no limit" as a decision, but the owner gave no answer to what ends it, which is the question that was open.
Pattern: a repeated call with no end. Each of the three read loops needs a bound or an exit the owner confirms. Until then, the question should be recorded as unanswered, not logged as a decision.

F2 | Unclear | Important | rules.md R-01, R-07, R-08; claims.md C-34, C-44, C-45; rules.md rows "the lookup failed", "...or the re-read failed", "the re-read of the refund failed"
Quote: "When the lookup fails, the agent says it could not look up their orders just now and changes nothing." / C-44: "A re-read of the order or its refund can fail rather than get no answer." / C-45: "The lookup of the customer's orders can fail rather than get no answer." (spec only)
Evidence: The read tool the owner confirmed in Q9 has two outcomes. It "returns each of the signed-in customer's orders ... or gets no answer". No "fails" outcome exists. The owner's only words on this are "Re-read fails, say outcome unknown, issue no refund, hand off" (Q11) and "re-read fails, say status unknown and hand off" (Q12). Neither says a failure is different from no answer. C-44 adds "rather than get no answer", which its quote does not support. C-45 has no source at all. The spec never defines what a failed read looks like. It also uses "failed" for a refund whose status is failed, a second meaning in the same rules. An agent cannot tell a read that should be retried without limit from a read that has "failed" and should go to staff.
Pattern: a coined outcome ("a read fails") with no one-line definition and no tool answer behind it. It also overlaps the everyday sense of "failed" that the spec uses for refunds.

F3 | Gap | Important | rules.md R-08, R-10; rules.md row "the re-read shows the refund, pending or issued"
Quote: "a refund pending or issued, it reports that status" / row: "the re-read shows the refund, pending or issued | says the order is cancelled and the refund is pending or issued, as the order system reported it"
Evidence: The row for the refund call itself checks the amount: "the refund call answered with a refund, pending or issued, for the amount and payment method agreed". The re-read row has no such check, and no row covers a re-read that shows a refund for a different amount or payment method. In Q7 the owner accepted that a refund differing from what the customer agreed is handed to staff. The model has no such state either: in model.py the outcomes of a refund call with no answer set refund only to "ok", "failed" or "none", never "differs". So after a timeout the agent passes on whatever amount the re-read shows.
Pattern: an amount passed on from a tool with nothing said about a mismatch. Every path that reports a refund needs the same agreed-amount and payment-method check.

F4 | Gap | Important | rules.md R-12, D-03; rules.md "What the agent does" (absent); policy.md chart
Quote: "When one order is done, the customer may name another of their orders, and the agent starts over with a new proposal and a new yes." / for the rows: absent
Evidence: Q8 recommendation, accepted by the owner: "After one order is done, the customer may name another of their orders, and the agent starts over ... It ends when the customer names no other order to cancel." R-12 leaves out the ending ("It ends when ..."). No row covers a second order named after the first one ends, and no row covers two orders asked for in one message ("cancel both my orders"). In policy.md every end state is under "Conversation over" and no arrow leads back to "Customer asked". In model.py, tell() sets loc="end".
Pattern: a case the owner accepted that has no row in "What the agent does" and no path in the policy. The same holds for a repeated thing (one order after another) whose end is missing from the rule.

F5 | Gap | Important | rules.md R-03; rules.md row "the customer has two open orders and named neither"; policy.md A1, A5
Quote: "When the customer has two open orders and says \"cancel my order\", the agent asks which order they mean before it proposes anything."
Evidence: Q5 failure case 1 ("Wrong order cancelled — customer has two open orders and says 'cancel my order'; agent must disambiguate") gives two orders as an example of the general danger. The rule and the row cover exactly two. No row covers three or more open orders, an open order plus a shipped one, or a customer with no orders who names none. model.py only has the starting situations one_open, two_open, one_shipped and one_cancelled, and ambiguous() is true only for "two_open". A customer with three open orders who says "cancel my order" hits no rule, which is the wrong-order failure the owner named.
Pattern: an owner's example was turned into a rule that covers only that example. Here the rule should cover "more than one order the customer could mean".

F6 | Lies | Important | rules.md R-05
Quote: "When the customer changes any part of the proposal after saying yes, such as asking for their other order instead, the earlier yes no longer counts."
Evidence: The owner's words in Q5 are "any change after confirmation voids it", with no limit on who makes the change. The owner quoted that same sentence again in reply to Q7, which is about the order system returning a different refund. That reply shows the owner counts changes on the system side too. R-05 narrows this to changes the customer makes. R-07 then has the agent re-read the order and "send the cancel once more under the same yes" with no check that the re-read order still matches the proposal (same total paid, same payment method).
Pattern: a rule narrows what the owner said, here "any change" became "the customer changes".

F7 | Lies | Nit | rules.md R-09
Quote: "It says the order is cancelled and refunded only when the order system shows a refund, pending or issued, for the amount and payment method the customer agreed to"
Evidence: Q12, owner: "pending or issued, report that status". Q6: "Final message must match the final refund status." claims.md C-18 (Stripe docs): a refund can still fail after it is accepted. Saying "refunded" while the refund is pending departs from the owner's wording. The rows ("the refund is pending or issued, as the order system reported it") follow the owner, so only the rule's sentence is off.
Pattern: the rule's wording for what the agent tells the customer departs from the owner's wording.

F8 | Lies | Nit | claims.md C-13, C-30
Quote: C-13: "The refund the order system returns carries an amount and a payment method, which the agent passes on to the customer." / C-30 quote: "How many orders may the agent cancel in one conversation, and what ends it?"
Evidence: C-13's quote (Q4: "Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued).") lists fields only. Nothing in it says the agent passes them on. C-30's quote is the question, not the answer that was accepted. The text it relies on is the Q8 recommendation: "One order per proposal. After one order is done, ... It ends when the customer names no other order to cancel."
Pattern: a claim whose quote does not support what it says. Quote the passage that holds the claim, and keep the claim to what that passage says.

## Verdicts and decisions

| finding | verifier | severity (verifier) | decision | outcome |
|---|---|---|---|---|
| F1 | Not real | Important | dropped | dropped |
| F2 | Not real | Important | dropped | dropped |
| F3 | Real | Important | kept | fixed |
| F4 | Real | Nit (finder: Important) | kept, at the verifier's lower severity | fixed |
| F5 | Real | Important | kept | fixed |
| F6 | Not real | Important | dropped | dropped |
| F7 | Real | Nit | kept | fixed |
| F8 | Real | Nit | kept | fixed |

Pre-existing: none.

### Verifier lines, verbatim

F1 | Not real | Important | This is an owner decision, logged the way the checklist asks, so it is not a gap. Asked "What ends it?" in Q13, against a recommendation of three tries, the owner replied "Reads may be retried on timeout without limit; only commit calls are bounded." That reply turns down the bound, so "nothing ends it" is the owner's answer, not a missing one. D-08 records it: "The agent proposed three tries; the owner kept no limit." The checklist (cockburn-checklist.md) says "When the owner chooses not to protect one, log that as a decision." R-01, R-07 and R-08 each say what the agent does in the case: it retries. C-37 states the end honestly: "nothing: the owner set no limit".

F2 | Not real | Important | The owner draws this line in their own words and would not misread it. The owner names two different outcomes for a read: "Reads may be retried on timeout without limit" (Q9 reply) and "Re-read fails, say outcome unknown, issue no refund, hand off" (Q11). The spec keeps them apart in the same way: rows say "got no answer" (retry) or "failed" (hand off). "Failed" is the owner's word in its everyday sense, not one the spec coined. The two senses of "failed" also come from the owner, in one sentence (Q12): "failed or no refund, hand off ... re-read fails, say status unknown and hand off". C-45 is labelled "spec only" openly, and an unsourced claim is not an Unclear defect.

F3 | Real | Important | R-10 covers part of this: "When the refund the order system returns has an amount or a payment method different from what the customer said yes to, the agent makes no further change ... and hands the case to staff". R-09 adds "it never claims success otherwise". Together they settle the behavior at the level of the rules. What stands: the row "the re-read shows the refund, pending or issued | says the order is cancelled and the refund is pending or issued" has no agreed-amount or payment-method check; no row covers a re-read that shows a different refund, so an agent that follows the table reports it as a success; model.py never sets refund="differs" on a call with no answer, so the checker never reaches that state. The case can happen: the refund call can answer "differs" (Q9), and a call with no answer may have made that refund.

F4 | Real | Nit | Parts of this are settled. R-12 says what the agent does with a second order: "the agent starts over with a new proposal and a new yes". The end of the series is in D-03 ("the conversation ends when the customer names no other order") and in C-30's "what ends it" column. For two orders in one message, SC-44 says the agent takes them "one per proposal". What stands: no row of "What the agent does" covers either case, and verification.md names exactly this as a Gap ("two requests in one message or a second order named mid-conversation"). Behavior is settled elsewhere, so this is a Nit, not Important.

F5 | Real | Important | I could not refute this. R-03 and ambiguous() cover only "two_open". No rule or row says what the agent does in these cases: three or more open orders and "cancel my order"; one open order plus one shipped order, with no order named; a customer with no orders who names none. R-03's "It does not pick one" applies only to the two-order case. The checklist requires "A row that branches on a lookup covers every result: nothing found, a match ..." and treats a guess about "which record" as a must-not.

F6 | Not real | Important | The owner's own answers support each scope. Change made by the order system: the owner accepted Q7, "makes no further change with the new value, tells the customer ..., and hands the case to staff". That is not "propose again", so a system-side change goes to R-10, not R-05. R-05's limit to changes the customer makes therefore matches the owner. The cancel retry: the owner said in Q11 "Still placed or processing, send the cancel once more under the same confirmation." That directly supports R-07. A re-read order whose total or payment method no longer matches: nothing in the packet or the spec says an order's total or payment method can change, so this part has no evidence.

F7 | Real | Nit | R-09's first sentence, "The agent's last message matches the final refund status", together with the rows ("the refund is pending or issued, as the order system reported it"), settles what the agent says for a pending refund. What stands: R-09's own sentence calls a pending refund "refunded". That departs from the owner's "pending or issued, report that status" (Q12). verification.md lists a departure from the owner's wording as a Lies defect. No behavior changes, so it is a Nit.

F8 | Real | Nit | Each claim is only partly supported. C-13: Q7 (accepted) supports "passes on" only when the refund differs ("tells the customer the amount and payment method the order system returned"). C-13's quote is a list of fields and does not support the general claim that the agent passes these on. C-30: the Q8 recommendation supports the claim, but the quote given is the question ("How many orders may the agent cancel ...?"), not that recommendation. Both are a claim saying more than its quote. Neither changes behavior.

### Drop reasons

- F1 dropped. Refuting line, read in the packet: Q13 reply "Reads may be retried on timeout without limit; only commit calls are bounded." and rules.md D-08. The owner was asked what ends a read and declined a bound; the spec logs that as the owner's decision. It stays an open "what if" in the report.
- F2 dropped. Refuting lines: Q11 reply "Re-read fails, say outcome unknown, issue no refund, hand off." and Q13 reply "Reads may be retried on timeout without limit". "No answer" (timeout) and "fails" are the owner's two outcomes, in their own words. The pattern part about C-44 saying "rather than get no answer" was still trimmed under F8's pattern (claim saying more than its quote).
- F6 dropped. Refuting lines: Q7 (accepted) "The agent makes no further change with the new value, tells the customer the amount and payment method the order system returned, and hands the case to staff" (system-side change goes to staff, not to a new proposal) and Q11 "send the cancel once more under the same confirmation". No input says an order's total or payment method can change between reads.

### Fixes

- F3 fixed: model.py now lets a refund call with no answer make a refund that differs, and the re-read can show it; new row "the re-read shows a refund whose amount or payment method differs" (staff task, refund differs); the re-read row now checks the agreed amount and payment method; R-08's text changed by proposal, accepted (D-12). New scenarios SC-51, SC-52.
- F4 fixed: rows for a second order named after the first, two or more orders in one message, and the end of a run; R-12's text changed by proposal, accepted (D-14).
- F5 fixed: R-03's text changed by proposal, accepted (D-11): more than one order the customer could mean, and no orders. model.py setups now include two or more open orders, an open and a shipped order, and no orders. Rows updated; scenarios SC-48 to SC-50.
- F7 fixed: R-09's text changed by proposal, accepted (D-13).
- F8 fixed: C-13 now says only what its quote says; C-30 quotes the accepted recommendation. Pattern search found and fixed C-18 (claimed "accepted ... later"), C-24 (quote extended to "The agent may retry it.") and C-44 (dropped "rather than get no answer").
