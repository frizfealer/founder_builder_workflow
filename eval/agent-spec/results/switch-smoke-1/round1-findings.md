# Round 1 findings (merged, verbatim from the finder), with verifier verdicts and decisions

Finder count line: 10 findings: 7 Important, 3 Nit.
Verifier count line: 9 Real, 0 Not real, 1 Style only.

F1 | Lies | Important | policy.md A18 (rows at lines 38, 40, 41, 42, 45, 46); rules.md R-10
Quote: "agent tells the customer: the order could not be cancelled, and no refund was issued; staff will follow up; please contact Harbor Goods support"
Evidence: Q7/Q9 change 3: "On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support." After two follow-up calls with no answer, the agent has not seen a task created, so "staff will follow up" is a success it did not see. R-09 forbids that: "It never claims success it did not see". The rules.md row "the follow-up call got no answer, the second time" says only "tells the customer what happened and to contact Harbor Goods support". The six policy messages add the staff promise.
Pattern: a customer message after a failed hand-off promises the hand-off happened. Every "...; please contact Harbor Goods support" line in A18 also says "staff will follow up". All six need the staff promise removed.
Verifier: F1 | Real | Important | I could not refute it. ...
Decision: kept
Status: fixed

F2 | Lies | Important | rules.md R-09; "What the agent does" row "the refund re-read shows it pending or issued"
Quote: "The agent says the refund is issued only when the order system showed it pending or issued" / "says the order is cancelled and the refund is issued; promises no date"
Evidence: answer 7 (Q3 Proposed): "after the retry the agent re-reads the refund record: pending or issued, report that status". C-19 says the same: "pending or issued, it reports that". The owner asked the agent to report the actual status. The rule tells the customer "issued" when the refund is only pending. Answer 6 gives pending as a status of its own (pending, issued, failed).
Pattern: two different tool statuses are folded into one customer message, which overstates the outcome. Instances: R-09 and the re-read row (rules.md line 106). The policy A16 message "the refund ... is issued" is the same.
Verifier: F2 | Real | Important | I could not refute it. ...
Decision: kept
Status: fixed (R-09 change accepted by the owner, question 16)

F3 | Gap | Important | rules.md "What the agent does" rows "the refund call answered issued, for the total confirmed", "...for a different amount", "the refund re-read shows it pending or issued"; R-11
Quote: "the refund call answered issued, for the total confirmed" / "the refund call answered issued, for a different amount" / "the refund re-read shows it pending or issued | says the order is cancelled and the refund is issued"
Evidence: C-16 and Q9: the refund call "answers the refund, pending or issued, with its amount". (1) No row covers a first refund call that answers pending. (2) The amount check from R-11/Q10 ("when that amount differs from the total the customer said yes to") appears only on the "answered issued" rows. A pending refund, or a refund found on the re-read after no answer, is reported as a success whatever its amount.
Pattern: an amount passed on from a tool is checked against the confirmed total on only one path. Every path that ends in reporting a refund (first-call pending, second-call answer, re-read pending/issued) needs the amount check and its own row.
Verifier: F3 | Real | Important | One part is refuted (the different-amount row is not limited to the first call); the rest stands: no row for a first refund call answering pending, and no amount condition on the re-read row.
Decision: kept
Status: fixed (R-11 change accepted, question 16)

F4 | Gap | Important | rules.md R-10, R-11, row "the refund call answered issued, for a different amount"; D-05
Quote: "it creates one follow-up task for staff naming the order and the reason" / D-05 "One follow-up call, with a reason, covers every case the agent cannot finish."
Evidence: C-26 and answer 6/7 allow exactly three reasons: refund_not_issued, refund_status_unknown, cancellation_unknown. No rule maps each hand-off case to its reason. Only C-33 and C-34 name one, and neither carries into R-06, R-08 or R-10. The amount-mismatch hand-off (R-11, accepted in Q10) fits none of the three reasons. D-05 also widens what the owner said: "One handoff call covers both the failed-refund case and the unknown-cancellation case" (answer 7).
Pattern: a tool argument the agent must choose has no rule that picks it. Instances: hand-off from cancel not found, cancel unknown, second cancel no answer, refund failed or order-not-cancelled, refund not confirmed, refund status unknown, and amount mismatch (no valid reason at all).
Verifier: F4 | Real | Important | I could not refute it.
Decision: kept
Status: fixed (R-10 reason mapping and fourth reason accepted, question 17)

F5 | Gap | Important | rules.md R-12, D-10; claims.md C-32; rows "the list call got no answer", "the re-read of the order got no answer", "the refund re-read got no answer"
Quote: "When a lookup gets no answer ..., the agent sends it again. The owner set no limit on this." / D-10 "what ends a lookup that never answers is an open decision."
Evidence: Q13 asked what ends it. The owner's reply only repeated "Reads may be retried on timeout without limit". The spec records the question as open, but the agent will still meet a read that never answers, and nothing ends that loop. The customer gets no message and the case never reaches staff.
Pattern: a repeated call with no end. Three instances: the list call, the order re-read after a cancel with no answer, and the refund re-read.
Verifier: F5 | Real | Important | I could not refute it. ... The spec follows the owner's "without limit" faithfully, but the loop still has no end.
Decision: kept
Status: open (only the owner can decide; the owner set no bound in questions 11 and 13)

F6 | Gap | Important | rules.md R-06; rows "the cancel call answered not cancellable because the order has just shipped" and "the re-read shows the order shipped"
Quote: "When the cancel answers that the order cannot be cancelled because it has just shipped, it tells the customer the order was not cancelled and issues no refund." / "the re-read shows the order shipped | says the order was not cancelled and no refund was issued"
Evidence: Q9 change 1: "OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered)". (a) The rule and the row say only "just shipped", and no re-read row covers "delivered". (b) Answer 2: "Once shipped, the agent refuses ... and tells the customer returns are a separate process". R-03 carries that message, but on these two shipped-late paths the customer is not told about returns.
Pattern: a case the owner defined by status set (shipped or delivered) is narrowed to one status, and the owner's message for that status is dropped on the late-discovery paths.
Verifier: F6 | Real | Important | Part (b) is refuted (Q8, answer 7 Q4 ask for no returns message on the late-discovery path). Part (a) stands.
Decision: kept
Status: fixed, part (a) (R-06 change accepted, question 18)

F7 | Gap | Important | rules.md "What the agent does" (absent); policy.md A16/A18 (terminal states)
Quote: absent
Evidence: the only multi-order row is "the customer said yes, then asked to cancel their other order instead". Answer 5 is about a customer with two open orders. No row covers a customer who asks to cancel both orders in one message, or who asks to cancel a second order after the first finished. In policy.md every path ends at "Cancelled and refunded, customer told" or "Outcome unclear" with no way back to "Customer asked". Per R-04, each cancel needs its own yes to a proposal naming one order, but nothing says whether the agent proposes them one at a time or ends the conversation.
Pattern: a second request in the same conversation (in the same message, or after a terminal state) has no row.
Verifier: F7 | Real | Important | The only partial answer is SC-39, a scenario rather than a rule or row.
Decision: kept
Status: fixed (new R-13 accepted, question 19)

F8 | Gap | Nit | rules.md R-02; row "the customer has two open orders and named none"
Quote: "When the customer has two open orders and says \"cancel my order\", the agent asks which one"
Evidence: answer 5 names two orders as the failure case it saw ("customer has two open orders"). The rule it backs is to disambiguate whenever the order is ambiguous. Three or more open orders match no row as written.
Pattern: a number from the owner's example is written into a rule as the condition.
Verifier: F8 | Real | Nit | I could not refute it.
Decision: kept
Status: fixed (R-02 change accepted, question 18)

F9 | Unclear | Nit | rules.md row "...or returned a second temporary error after no call went unanswered"
Quote: "returned a second temporary error after no call went unanswered"
Evidence: this means "both refund calls returned temporary errors and neither had no answer", which the owner would have to work out. R-08 and C-18 say it as "after a temporary error the agent asks for the refund once more".
Pattern: a row condition written as a double negative the owner could misread.
Verifier: F9 | Real | Nit | Not refuted.
Decision: kept
Status: fixed

F10 | Lies | Nit | claims.md C-02, C-16, C-26
Quote: C-02 "The list call returns each of the customer's orders with its order number, status, total paid and payment method, and the order's refund or none." (quote: "list_orders() (returns each order with its refund or null) ...") ; C-16 "...answers order not cancelled..." (quote is the same tool-set line, which has no "order not cancelled" and no "pending or issued, with its amount"); C-26 "...a reason: the refund was not issued, the refund's status is unknown, or the cancellation is unknown" (quote: "One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.")
Evidence: the missing parts are in other answers: Q9 tool confirmation and change 2 ("issue_refund adds outcome OrderNotCancelled"), and answer 6's reason list. Each claim says more than its own quote.
Pattern: a claim cites one quote but rests on several answers. Each instance should cite the answer that carries each part (Q9 for C-02 and C-16, the answer 6/7 tool-set line for C-26).
Verifier: F10 | Style only | Nit | Each extra part of the three claims is supported by another answer in the packet ... Only the citation is off.
Decision: kept (a claim saying more than its quote is a Lies defect, not a phrasing preference)
Status: fixed

## Verifier report, verbatim

F1 | Real | Important | I could not refute it. The owner's only words for this case are Q9 change 3: "On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support." Nothing the agent saw shows a task was created. C-29 ("Store staff work every follow-up task") assumes a task exists, so it does not apply. The rules.md row says only "tells the customer what happened and to contact Harbor Goods support". All four "...; please contact Harbor Goods support" lines in A18 still add "staff will follow up", which is the success R-09 forbids: "It never claims success it did not see".

F2 | Real | Important | I could not refute it. Answer 7 (Q3) says "pending or issued, report that status", and answer 6 lists pending and issued as separate refund statuses. No answer lets a pending refund be reported to the customer as issued. R-09, the re-read row ("says the order is cancelled and the refund is issued") and the A16 message all do that.

F3 | Real | Important | One part is refuted: the "refund call answered issued, for a different amount" row is not limited to the first call, so a second refund call that returns a different amount is covered. R-11 ("When the refund the order system returns carries an amount different ... hands the case to staff") arguably covers the amount on the re-read and pending paths too. The rest stands. (1) No row covers a first refund call that answers pending, even though C-16 lists that answer. (2) The re-read row "pending or issued | says the order is cancelled and the refund is issued" has no amount condition, so the table states no mismatch handling on that path.

F4 | Real | Important | I could not refute it. Only C-33 and C-34 name a reason, and no rule or row maps the other hand-off cases to one of the three reasons in answer 6 (refund_not_issued, refund_status_unknown, cancellation_unknown). The amount-mismatch hand-off accepted in Q10 fits none of the three. On D-05, the acceptances in Q10, Q14 and Q15 support handing those three cases to staff, but they still give no reason to use.

F5 | Real | Important | I could not refute it. D-10 says "what ends a lookup that never answers is an open decision", and C-32's "what ends it" column says "nothing: the owner set no bound". Neither says what the agent does. The class definition lists "a repeated thing with no end" as a Gap. The spec follows the owner's "without limit" faithfully, but the loop still has no end.

F6 | Real | Important | Part (b) is refuted. For the late-discovery shipped case the owner's own words are Q8, "the store rejects the cancel and the agent must report that truthfully and issue no refund call", and answer 7 (Q4), "Shipped, report it and issue no refund". Neither asks for the returns message, which answer 2 attaches to refusing without a cancel call. Part (a) stands. Q9 change 1 ("OrderNotCancellable{status} ... covers shipped and delivered") is carried by C-36, but R-06 and the rows say only "just shipped", and no row covers a cancel or re-read that answers delivered.

F7 | Real | Important | The only partial answer is SC-39, a scenario rather than a rule or row: "A customer who asks to cancel two orders in one message must get one proposal per order, and each order is cancelled only after its own yes." It answers the case of two orders in one message. The class definition asks for a row of "What the agent does" for that case, and none exists. A second request after a terminal state has nothing at all, and the policy has no arrow back from the terminal states.

F8 | Real | Nit | I could not refute it. R-02 and its row are conditioned on exactly "two open orders". No rule or row covers three or more open orders with no number named. The model also allows the "my order" request only when there are two orders. This may affect behavior, since the agent could guess which order to propose, so the Nit label may understate it.

F9 | Real | Nit | Not refuted. The next row ("a refund call got no answer and no issued refund followed | re-reads the refund") and R-08 make the meaning recoverable by elimination. The double negative "after no call went unanswered" is still a line the owner could misread.

F10 | Style only | Nit | Each extra part of the three claims is supported by another answer in the packet. For C-02 and C-16: the Q9 tool text the owner answered "Confirmed, with four changes" includes "returning each order's number, status, total paid, payment method, and its refund or none" and "answers the refund, pending or issued, with its amount", and change 2 says "issue_refund adds outcome OrderNotCancelled". For C-26: the answer 6/7 tool-set line gives "reasons refund_not_issued, refund_status_unknown, cancellation_unknown". Only the citation is off, so no agent behavior changes and the owner would not misread the claims.

Count: 9 Real, 0 Not real, 1 Style only.
