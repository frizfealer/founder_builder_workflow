# Round 1 findings (merged, verbatim) with verifier verdicts and decisions

Finder count line: "10 findings: 6 Important, 4 Nit."
Verifier count line: "Count: 7 Real (F1, F2, F3, F4, F5, F7, F8), 3 Not real (F6, F9, F10), 0 Style only."

Kept 7 (F1, F2, F3, F4, F5, F7, F8), dropped 3 (F6, F9, F10). Pre-existing: 0.

---

F1 | Gap | Important | rules.md "What the agent does" (refund-call rows), R-06, R-08, R-09; claims.md C-19
Quote: absent. C-19 lists the outcome ("answers \"order not cancelled\""), but no rule and no row says what the agent does when the refund call gives that answer.
Evidence: review-packet.md Q10 reply, change 2: "issue_refund adds outcome OrderNotCancelled." The refund-call rows (rules.md lines 105-116) cover pending/issued, a different amount, failed, a temporary error and no answer. None covers "order not cancelled". It can come back after the cancel call answered "cancelled", or after a re-read showed the order cancelled (R-07). The agent then has no next step and no customer wording, and no staff reason fits.
Pattern: a tool outcome the owner added and the claims list has no row and no rule.

Verifier: F1 | Real | Important | I could not refute it. C-19 lists "answers \"order not cancelled\"", taken from the owner's Q10 change 2: "issue_refund adds outcome OrderNotCancelled." No row of "What the agent does" covers that answer (rules.md 105-116), no rule does, and model.py's refund system steps leave it out. The checklist says "Each outcome gets a row of 'What the agent does'". R-06's "issues the refund only after the order system shows the order cancelled" says when the call is sent. It does not say what the agent does when this answer comes back.
Decision: kept (Important). Status: fixed. Added the row "the first refund call answered \"order not cancelled\"" (hand the case to staff with reason refund not issued; tell the customer the refund was not issued without saying the order is cancelled), the system step in model.py, and scenarios SC-47 and SC-48. Pattern check: every other tool outcome in claims.md has a row.

---

F2 | Gap | Important | rules.md rows "the refund call answered a temporary error, the first time" / "the second time" / "the second refund call has answered the confirmed amount, or got no answer, after an unanswered one, or got no answer after a temporary error"; R-08, R-09
Quote: "| the refund call answered a temporary error, the second time | hands the case to staff: the refund was not issued | R-08, R-12 |"
Evidence: review-packet.md Q6 case 3: "refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status." Take the path where the first refund call gets no answer and the second answers a temporary error. Row 111 lists three cases that lead to a re-read, and this path is not one of them. That leaves two rows, and either one breaks a rule:
(a) If "the first time" means the first temporary error, row 108 applies. The agent sends a third refund call, against R-08's "never a third time".
(b) If "the second time" means the second call, row 109 applies. The agent hands off and tells the customer "the refund was not issued" without re-reading. But the first, unanswered call may have created the refund (C-19: "a call with no answer may or may not have created the refund"). This contradicts R-09, which says that after no answer the agent sends once more and then reads.
A second instance: the first call gets no answer and the second answers "failed". Row 107 hands off with "the refund was not issued". The owner's case 3 says to re-read and, for failed, "say the refund is not confirmed yet".
Pattern: a retry after no answer whose answer is not success. The rows say "first time / second time" without saying first or second of what, and the owner's "then re-read" step is skipped.

Verifier: F2 | Real | Important | R-09 settles the action for the temporary-error instance: "After a refund call with no answer, the agent sends it once more and then reads the order and its refund again". model.py does the same (`if s.refund_timeout and s.refund_calls == 2` re-reads), and so does SC-33 (no answer, then failed, then "read shows a failed refund"). The rest stands. Row 111 does not list "second call answered a temporary error after an unanswered one". Row 109 ("temporary error, the second time | hands the case to staff: the refund was not issued") and row 107 ("the refund call answered \"failed\" | hands the case to staff: the refund was not issued") apply literally to this path. So does R-08's "After a final error it sends no second call: it hands the case to staff and tells the customer the refund was not issued". Each of those gives a hand-off with no re-read and different customer wording, against R-09 and Q6 case 3.
Decision: kept (Important). Status: fixed. Rewrote every refund row to say which call (first, or second after a temporary error, or second after no answer) it is about. R-08's text change went to the owner (packet Q19) and was accepted (stand-in default); applied with D-11.

---

F3 | Lies | Important | rules.md R-12; claims.md C-26; rules.md D-03
Quote: "The agent hands the case to staff when a cancel or refund call fails or gets no answer, or the refund differs from what the customer confirmed, and tells the customer that staff will follow up."
Evidence: As written, R-12 sends every unanswered cancel or refund call to staff. The owner's later answers narrow that:
- Q12 reply: "Still placed or processing, send the cancel once more under the same confirmation."
- Q6 case 3: retry once, then re-read; "pending or issued, report that status" with no hand-off.
R-07 ("If the read shows it cancelled, the agent goes on to the refund") and R-09 ("Pending or issued: it says that status") follow those answers, and contradict R-12's unconditional trigger. An agent or owner reading R-12 alone would expect a staff task on every timeout.
Pattern: a rule copied from an early accepted recommendation that later owner answers narrowed. It keeps the wider wording.

Verifier: F3 | Real | Nit | The case-by-case lines settle the behavior: row 98 "the cancel call got no answer | reads the order again", row 110 "the refund call got no answer, the first time | sends the refund call again", row 113 "the read shows a pending or issued refund ... | says the order is cancelled and the refund is pending or issued", and R-07 and R-09. An agent following the table will not hand off on every timeout. The defect stands only in the wording. R-12 and D-03 keep the unconditional trigger from Q7 ("when a cancel or refund call fails or gets no answer"). Q12 and Q6 case 3 later narrowed it, and the owner could read R-12 that way.
Decision: kept, at the verifier's lower severity (Nit). Status: fixed. R-12's text change went to the owner (packet Q18) and was accepted (stand-in default); applied with D-10. C-26 and D-03 keep the owner's Q7 answer as recorded.

---

F4 | Gap | Important | policy.md A12, A15; rules.md rows "the read after the second cancel call shows the order still open" and "the read shows a failed refund or no refund"; claims.md C-43
Quote: "| A12 | Cancelling | Handing to staff | agent asks staff to follow up: cancellation unknown |" and "| A15 | ... | agent asks staff to follow up: refund not confirmed |"
Evidence: C-43 and Q10 give the follow-up call exactly four reasons: "refund not issued, refund status unknown, cancellation unknown, refund amount differs". Two hand-offs fit none of them:
(a) After the second cancel call, the order is known to be still open (Q16, accepted: "the order was not cancelled and no refund was issued"). The only Cancelling→staff step, A12, sends "cancellation unknown", so staff get a task that misstates the case.
(b) A15 sends a fifth reason, "refund not confirmed", which the tool does not take.
C-26 says "The task names the order and what happened", which neither of these does.
Pattern: a hand-off with no mapping to one of the tool's confirmed reason values.

Verifier: F4 | Real | Important | I could not refute it. Two hand-offs have no tool reason that fits. Row 103 ("the order was not cancelled and no refund was issued") maps only to A12 "cancellation unknown" (model.py: `hand_off(s, "cancellation_unknown", "not_cancelled")`), but the read has shown the order still open. A15 "refund not confirmed" (model.py `refund_not_confirmed`) is none of C-43's four reasons. No rule says which reason value the agent sends in either case.
Decision: kept (Important). Status: fixed. (b) the hand-off after a read showing a failed or no refund now sends "refund not issued" (the customer is still told the refund is not confirmed yet). (a) put to the owner (packet Q21): accepted a fifth reason, "order not cancelled" (C-44, D-13); model and row changed.

---

F5 | Gap | Important | rules.md "What the agent does"; policy.md chart steps; claims.md C-35
Quote: "Each order is cancelled at most once, so the number of the customer's open orders bounds how many cancellations one conversation makes." (C-35, spec only)
Evidence: C-35 assumes one conversation can cancel several orders. But no row covers a customer who asks to cancel two orders in one message ("cancel both my orders"). No row covers a second order named after the first is done, or added after a proposal. Row 93 covers only "the customer said yes and changed which order". In policy.md no step leaves the end states ("Handed to staff, customer told", "Cancelled and refund pending or issued, customer told", "Nothing changed, customer told"), so a second request has nowhere to go. The rules also don't say whether two orders need one yes or two. The owner's own failure case (Q5/Q6 case 1: "customer has two open orders") makes such a customer likely.
Pattern: two requests in one message, or a second order mid-conversation, with no row.

Verifier: F5 | Real | Important | scenarios.md answers part of it. SC-41: "a message that asks to cancel two orders needs a proposal naming each order and a yes to each". SC-42: "a request to cancel another order after the first is finished starts a new run of the model; the earlier yes does not cover it". That covers the one-yes-or-two question and the second order after the first is done, but only in scenarios, not in a rule or a row. The rest stands. No row covers either case, which verification.md names as a Gap ("two requests in one message or a second order named mid-conversation"). A second order added after a proposal is covered nowhere. No policy step leaves the end states.
Decision: kept (Important). Status: fixed. R-02's text change (one order at a time, each with its own proposal and yes) went to the owner (packet Q20) and was accepted (stand-in default); applied with D-12 and a new row "the customer asked to cancel more than one order".

---

F6 | Gap | Important | claims.md C-37, C-22; rules.md R-01, R-07, R-09, D-09; rows "listing the orders got no answer", "the read of the order got no answer", "the read of the refund got no answer"
Quote: "nothing: the owner set no limit, so a read that never answers is tried until the customer leaves" (C-37, what ends it)
Evidence: Q14 asked what ends a read that never answers, and the owner replied "Reads may be retried on timeout without limit". So no end exists. The spec's "until the customer leaves" is not the owner's words. It is also not an event the policy can see: "Customer left" is reachable only from "Proposal waiting for yes" and "Asked which order" (A9, A11). Reading the orders, Cancelling and Refunding have no way out, and nothing tells the customer anything while the reads repeat. C-22's own end, "then one read of the refund", also contradicts C-37's unlimited reads.
Pattern: a repeated read with no end. The spec writes in an end the owner never gave, and one the agent cannot observe. Record it plainly as the owner's accepted risk, or put the question to the owner again.

Verifier: F6 | Not real | Nit | D-09 records the owner's choice, which was made twice: once at Q10 and again at Q14 after being told the customer "would wait forever". D-09: "Reads that get no answer are tried again with no limit. | the owner | Reads may be retried on timeout without limit; only commit calls are bounded." The checklist asks for exactly that ("When the owner chooses not to protect one, log that as a decision"), and it is the fix the finding asks for. What is left is Style only and changes no behavior: C-37's "until the customer leaves" opens with "nothing: the owner set no limit", and C-22's "what ends it" says "then one read". R-09 and row 112 state plainly that "A read with no answer is read again".
Decision: dropped. Refutation: D-09 "Reads that get no answer are tried again with no limit. | the owner | Reads may be retried on timeout without limit; only commit calls are bounded." The owner chose no limit twice and the spec logs it as the owner's decision, which is what the finding asks for. The unbounded read stays an open question in the report.

---

F7 | Lies | Nit | rules.md R-06, R-07, row "the read after the cancel call shows the order shipped"
Quote: "| the read after the cancel call shows the order shipped | says the order has shipped and was not cancelled, and issues no refund call | R-07, R-06 |"
Evidence: Q2 reply: "Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1)." Row 96 and policy.md A13 include "returns are a separate process". R-06 ("tells the customer so truthfully") and R-07 / row 101 ("says it was not cancelled") leave it out. R-07 and row 101 also cover only a read that shows "shipped". A read showing "delivered" (C-02, C-17) has no row.
Pattern: the owner's customer wording for a shipped order is dropped from some of the paths that reach it.

Verifier: F7 | Real | Nit | The returns-wording part is refuted by the owner's wording for the race: "the store rejects the cancel and the agent must report that truthfully and issue no refund call" (Q6/Q8). R-06's "tells the customer so truthfully" and R-07 / row 101 follow it. The owner's "returns are a separate process" line (Q2) is about refusing "without issuing a cancel call". The delivered part stands. R-07 ("if it shows it shipped") and row 101 name only "shipped", but Q10 change 1 says the not-cancellable status "covers shipped and delivered". No row covers a read that shows delivered.
Decision: kept (Nit), for the "delivered" part only; the returns-wording part is refuted by the quoted race answer, which I read and agree with. Status: open. The fix changes R-07's text ("if it shows it shipped" to "if it shows it shipped or delivered"); the one owner turn of step 4.5 was full (4 questions), so it is reported as a proposal for the owner.

---

F8 | Lies | Nit | claims.md C-15, C-27
Quote: C-15: "returns each of the customer's orders, cancelled ones included, with its number, status, total paid, payment method and its refund, or no refund". C-27: "One follow-up call covers every hand-off, with a reason: the refund was not issued, the refund status is unknown, or the cancellation is unknown."
Evidence:
- C-15's quote is the "Proposed set shown to the user" line, which says only "list_orders() (returns each order with its refund or null)". "Cancelled ones included" is from Q10 change 4. The fields are from the Q10 question text.
- C-27's quote says "covers both the failed-refund case and the unknown-cancellation case". It does not say "every hand-off". The three reasons C-27 lists contradict C-43's four, which add "refund amount differs".
Pattern: a claim that says more than its quote, sourced from other lines that it does not cite.

Verifier: F8 | Real | Nit | The C-15 part is Style only. Its content is all owner-confirmed: Q10 "Confirmed, with four changes", "4. list_orders includes cancelled orders", and the fields in the Q10 tool proposal. The C-27 part stands. Its quote ("covers both the failed-refund case and the unknown-cancellation case") does not say "every hand-off". It also lists three reasons, while C-43 lists four ("or the refund amount differs"). That contradiction bears on which reason the agent sends (see F4).
Decision: kept (Nit). Status: fixed for C-27 (rewritten to say only what its quote says: "One follow-up call covers both the failed-refund case and the unknown-cancellation case, with a reason."; the reasons live in C-43 and C-44). The C-15 part is answered: Q10's reply confirms the listed fields and "list_orders includes cancelled orders".

---

F9 | Gap | Nit | rules.md R-04, row "the customer said yes and changed which order"
Quote: "| the customer said yes and changed which order | states the changed proposal and asks again | R-04 |"
Evidence: Q5 reply: "any change after confirmation voids it". Q4: "refund payment method = order's payment method ... No cancellation fee, no store-credit option." No row covers a customer who asks, before or after the yes, for the refund to go to another card or as store credit. R-05 forbids both, but no row gives the agent's reply or says whether the proposal stands.
Pattern: a change to the proposal other than the order, with no row.

Verifier: F9 | Not real | Nit | R-05 fixes the proposal whatever the customer asks: "It proposes a refund of the order total the customer paid, back to the order's payment method, with no fee and no store credit". C-31 backs it ("Refunds can only go back to the original payment method"). R-03 makes a yes count only when it confirms "where it goes", so a yes that asks for another card or store credit authorizes nothing. SC-44 states the case outright: "the agent offers only the full order total back to the order's payment method". The owner gave no reply wording, and the checklist forbids inventing it.
Decision: dropped. Refutation: R-05 "It proposes a refund of the order total the customer paid, back to the order's payment method, with no fee and no store credit" with R-03's "explicitly confirms the full proposal: which order, the refund amount and where it goes". I read both: the proposal cannot change to another card or store credit, and a yes to anything else is not a yes to the proposal.

---

F10 | Unclear | Nit | rules.md R-01, R-07, R-09; rows "listing the orders failed", "the read after the cancel call failed", "the read of the refund failed"
Quote: "When listing the orders gets no answer, it lists them again; when the listing fails, it tells the customer it cannot see their orders right now"
Evidence: The spec separates a read that "fails" (an error answer, C-16: "answers, answers an error, or gets no answer") from one that "gets no answer". rules.md never defines "fails". The owner uses "fails" for timeouts: Q7 reply says "re-read fails, say status unknown and hand off", in a passage about the refund call timing out. So the owner could read R-09's "The read fails: it says the refund status is unknown" as covering a re-read that times out. Under the spec, that path instead loops (see F6).
Pattern: a term the spec uses in a narrower sense than the owner's, with no definition where it first appears.

Verifier: F10 | Not real | Nit | Every rule that uses "fails" for a read sets the no-answer case apart in the same place. R-09: "The read fails: it says the refund status is unknown and hands the case to staff. A read with no answer is read again." R-07: "If the read fails, ... hands the case to staff. A read with no answer is read again." R-01: "When listing the orders gets no answer, it lists them again; when the listing fails ...". C-16 defines the three outcomes ("answers, answers an error, or gets no answer"). The misreading the finding names, a timeout counted as "fails", is ruled out by the sentence next to it.
Decision: dropped. Refutation: R-01 "When listing the orders gets no answer, it lists them again; when the listing fails, ..." and R-09 "The read fails: ... A read with no answer is read again." I read them: each "fails" sits beside the sentence that sends a no-answer read back, so the owner cannot read "fails" as a timeout there.
