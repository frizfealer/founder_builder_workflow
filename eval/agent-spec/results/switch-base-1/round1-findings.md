# Round 1 findings

Finder count line: "11 findings: 6 Important, 5 Nit."
Verifier count line: "Real 3 (F3, F4, F5); Not real 5 (F1, F2, F6, F7, F11); Style only 3 (F8, F9, F10)."
Decision: 5 kept (F3, F4, F5, F9, F10), 6 dropped (F1, F2, F6, F7, F8, F11). Pre-existing: 0.

Each finding below is the finder's text verbatim, then the verifier's line verbatim, then the decision and status.

---

F1 | Gap | Important | claims.md C-04, C-25; rules.md R-07, R-09, D-10, rows "the cancel call got no answer, or the list after it got no answer" and "a refund call got no answer, and the second refund call has returned, or the list after it got no answer"
Quote: "A list call that gets no answer may be tried again, with no limit." / what ends it: "nothing: the owner set no limit on retrying a list call"; R-07 "trying the list again as often as it gets no answer"
Evidence: Q13 asked what ends a list call that keeps getting no answer. The owner did not accept the three-try recommendation and repeated "Reads may be retried on timeout without limit" (review-packet Q13; also Q9 change 4, Q11, Q12). The owner also said "Re-read fails, say outcome unknown, issue no refund, hand off" (Q7) and "re-read fails, say status unknown and hand off" (Q12), so the owner expects a re-read to end. The spec repeats the owner's words but leaves a list call that never answers looping forever, at the start, after an unanswered cancel, and after an unanswered refund. The customer is never told anything. C-25's "what ends it" says "the second refund call, then one more list", which contradicts R-09's unlimited retry.
Pattern: a repeated read with no end. The spec records "no limit" instead of putting the conflict between the two owner answers back to the owner, and one claim names an end the rule does not have.

Verifier: F1 | Not real | Important | The owner was asked this exact question and answered it. Q13 laid out the conflict: "Nothing then ends a list call that keeps getting no answer, and you also said that when the re-read fails..." The owner turned down the three-try recommendation and replied "Reads may be retried on timeout without limit; only commit calls are bounded." D-10 logs that as the owner's decision, in the owner's words: "A list call that gets no answer is tried again with no limit; only cancel, refund and follow-up calls are bounded." The cockburn checklist asks for exactly this: "When the owner chooses not to protect one, log that as a decision." R-07 and R-09 say what the agent does ("trying the list again as often as it gets no answer"). The owner's two answers do not conflict, because the owner uses "re-read fails" and "timeout" as separate outcomes. One sub-point is at most Style only. C-25's "what ends it: the second refund call, then one more list" reads as one re-read step whose no-answer retries fall under C-04, and R-09 spells out the unlimited retry.

Decision: dropped. Refutation: Q13 reply "Reads may be retried on timeout without limit; only commit calls are bounded." and D-10. Status: dropped.

---

F2 | Unclear | Important | claims.md C-04, C-34; rules.md R-07, R-09, R-10, rows "the first list call failed", "the list after an unanswered cancel failed", "the list of the order and its refund failed"
Quote: "A call to list the orders answers, fails, or gets no answer."; "When the first call to list the orders fails, the agent tells the customer it cannot look up their orders right now"
Evidence: The tool set confirmed in Q9 gives the list call two outcomes, an answer or "may get no answer". It has no separate failure. Since no answer is retried without limit (D-10), the agent's whole choice between retrying and telling the customer or handing to staff turns on "fails", and the spec never says what a failure is or how it differs from no answer. "The first list call" is also unclear: after retries, it could mean the very first call or the start-of-conversation lookup. C-34 is "spec only". It comes from the Q13 recommendation, which the owner did not accept.
Pattern: a coined outcome ("fails") with no one-line definition, and the agent's behavior depends on it.

Verifier: F2 | Not real | Important | "Fails" is the owner's own word. The owner uses it apart from timeout: Q12 says "re-read fails, say status unknown and hand off" and, in the same reply, "Reads may be retried on timeout without limit." The spec's "fails" vs "gets no answer" follows that line exactly, so the owner would not misread it. "The first list call" is settled two ways. The row "the customer asked to cancel, and the orders are not listed yet, or the list call got no answer | lists the customer's orders" covers it, and SC-08 ("First list unanswered, tried again, then fails", Rules: R-10) shows that it means the opening lookup, not only the very first call. C-34 is honestly labeled "spec only". That is not an Unclear defect.

Decision: dropped. Refutation: Q12 reply "re-read fails, say status unknown and hand off" beside "Reads may be retried on timeout without limit"; row "the customer asked to cancel, and the orders are not listed yet, or the list call got no answer | lists the customer's orders". Status: dropped. (C-34 stays spec only and is reported as an open question.)

---

F3 | Gap | Important | rules.md R-04, rows "a customer with two open orders said "cancel my order"" and "the customer said yes but switched to their other open order"; claims.md C-22
Quote: "When a customer with two open orders says "cancel my order", the agent asks which one first."
Evidence: Q5 and Q7 give "customer has two open orders" as one example of the failure "Wrong order cancelled", where the agent must "disambiguate and get a confirmation naming the order number". No row covers three or more open orders, or "cancel my order" from a customer with one open order and other shipped or delivered orders. Those are the same ambiguity. "Their other open order" also assumes exactly two.
Pattern: the owner's example count written as the rule's limit, which narrows a disambiguation rule to exactly two.

Verifier: F3 | Real | Important | I could not refute it. R-04 and its row say only "When a customer with two open orders says 'cancel my order', the agent asks which one first." No rule or row says the agent asks when there are three or more open orders, or when one open order sits beside shipped or delivered ones. The model's starting situations top out at "two open orders". R-04's "confirms the full proposal: which order, by its order number" makes a wrong cancel less likely, but it does not require the agent to ask. The owner's Q5/Q7 words were "agent must disambiguate".

Decision: kept, Important. The fix changes R-04's text, so it went to the owner as a proposal (question 17). The owner (stand-in) accepted it ("Yes, I accept your recommendation."). Following the skill's rule that a fix changing a rule's text stops at that rule, R-04's text was not changed in this run. Status: open (rule-change proposal, accepted by the owner, to apply).

---

F4 | Gap | Important | rules.md R-13 and "What the agent does"; policy.md chart steps A1 to A18
Quote: "The agent handles one order at a time, each with its own proposal and its own yes, finishing one before starting the next." / row: absent
Evidence: Q16 (accepted) expects a customer to cancel more than one order in one conversation. No row and no arrow covers: (a) two orders named in one message ("cancel HG-1 and HG-2"); (b) a different order named while a proposal waits for a yes (the only switch row is "said yes but switched"; A6 to A8 leave "Proposal waiting for yes" only on no, yes, or silence); (c) asking for the next order after the first is finished. Every "customer told" state in policy.md is terminal, with no arrow back to "Finding the order".
Pattern: a rule with no row or path that carries it out. These are cases the agent will meet: a second order in the same message, mid-proposal, or after the first is finished.

Verifier: F4 | Real | Important | This is a partial refutation only. Parts (a) and (c) are settled by R-13, "handles one order at a time, each with its own proposal and its own yes, finishing one before starting the next", together with SC-49 ("Two orders to cancel in one message"), SC-50, and the model docstring "A request to cancel a second order after the first is done starts a new run." Part (b) stands: a different order named while a proposal waits for a yes. The only switch row is "the customer said yes but switched to their other open order". Arrows A6 to A8 leave "Proposal waiting for yes" only on no, yes or silence. R-13 does not say whether the first proposal is dropped or finished first.

Decision: kept, Important, for part (b). Fix: the row now reads "the customer said yes but switched to their other open order, or named their other open order while the proposal waited for a yes | drops the waiting proposal, which has no yes, and proposes the newly named order, asking for a yes again | R-04, R-13"; model.py gained the customer step "customer names their other open order instead"; SC-53 covers it. Status: fixed.

---

F5 | Lies | Important | rules.md row "the refund came back ... issued for the confirmed amount"
Quote: "says the order is cancelled and the total paid is refunded to the payment method, and nothing about when the money arrives"
Evidence: The owner's words are "The agent promises nothing about when the money arrives" (Q6). R-10 and C-27 copy them correctly. The row widens "promises nothing" to "says nothing", which would stop the agent from answering "how long does it usually take?" with something that is not a promise, such as Stripe's "approximately 5-10 business days ... depending upon the bank" (docs.stripe.com/refunds, C-12). No row covers a customer asking when the money arrives.
Pattern: a row's customer wording widens the owner's wording in the rule it cites.

Verifier: F5 | Real | Nit | I could not refute the main point. The row "says the order is cancelled and the total paid is refunded to the payment method, and nothing about when the money arrives" widens R-10's "It promises nothing about when the money arrives". verification.md lists this very pattern as a Lies example ("promises nothing about when" written as "names no date"). I rate it Nit, not Important, because an agent that says nothing about timing still keeps the owner's rule. The claim that "No row covers a customer asking" is answered by R-10 and SC-51: "the agent's answer must promise nothing about when the money arrives."

Decision: kept, at the verifier's severity, Nit. Fix: the row now says "and promises nothing about when the money arrives"; the pattern was searched ("nothing about when") and this was the only instance. Status: fixed.

---

F6 | Unclear | Important | rules.md row "a refund call got no answer, and the second refund call has returned, or the list after it got no answer"
Quote: "the second refund call has returned"
Evidence: Q12's own path is a refund call with no answer, then a retry with no answer. Q7 case 3 says "agent retries once, then re-reads". If "returned" means "answered", that path matches no row: the row above needs "only one refund call has been sent". A builder could then send a third refund call, against "retries once" (Q7, C-24, C-25). The same holds for a first call with a transient error followed by a retry with no answer.
Pattern: an everyday word ("returned") used in a narrower sense the reader cannot see, at a branch point.

Verifier: F6 | Not real | Important | R-09 settles the no-answer-twice path whatever "returned" means: "When a refund call gets no answer, the agent retries once, then lists the order and its refund again." SC-31 ("Unanswered refund, retry unanswered, list shows it issued") is that exact path. For a transient error followed by no answer, C-24's "what ends it: the second refund call" rules out a third call. SC-37, SC-38 and SC-39 ("Transient error, then unanswered refund, list ...") show the list following.

Decision: dropped. Refutation: R-09 "When a refund call gets no answer, the agent retries once, then lists the order and its refund again" and C-24's "what ends it: the second refund call". Status: dropped.

---

F7 | Gap | Nit | rules.md R-11, R-10; claims.md C-07, C-20
Quote: absent
Evidence: The customer confirms "where it goes" as part of the proposal (Q5, C-20), and the refund call returns a payment method (C-07, Q9). R-11 covers only an amount that differs. Nothing covers a returned refund whose payment method differs from the confirmed one. C-11 (Stripe: "Refunds can only be sent back to the original payment method") makes this unlikely, but the order system has no docs (Q1). The "issued" and "pending" rows would then tell the customer the confirmed method.
Pattern: a value passed on from a tool that the customer confirmed, with nothing said about a mismatch.

Verifier: F7 | Not real | Nit | Under the spec's own claims the case cannot arise. C-11 says "A refund goes back only to the payment method the order was paid with", quoting Stripe: "You can't send a refund to a different destination, such as another card or bank account." The finding admits as much. The Gap example covers an amount passed on from a tool, not a field the claims fix.

Decision: dropped. Refutation: C-11 "A refund goes back only to the payment method the order was paid with" (docs.stripe.com/refunds). Status: dropped.

---

F8 | Lies | Nit | rules.md row "the cancel call answered that the order is not cancellable ..., or the orders listed again show it shipped"
Quote: "or the orders listed again show it shipped"
Evidence: R-07, which the row cites, says "If it shows shipped or delivered, it says so and issues no refund". Q9 change 1 says OrderNotCancellable "covers shipped and delivered". The row leaves out delivered for the re-list branch.
Pattern: a row narrower than the rule it cites.

Verifier: F8 | Style only | Nit | The row's own action already says "says the order has shipped or been delivered and could not be cancelled". R-07, which the row cites, says "If it shows shipped or delivered, it says so and issues no refund." The agent behaves the same, and the owner would not misread it.

Decision: dropped (Style only Nit; read its Quote and Evidence: the row's action already says "shipped or been delivered", so the situation cell's wording is a phrasing preference). Status: dropped.

---

F9 | Lies | Nit | rules.md D-03
Quote: "A blind resend could act on an order that has since shipped."
Evidence: C-05 (Q9 change 1, Q6 race) says the cancel call rejects an order that shipped after the agent read it ("OrderNotCancellable{status}"), and that cancel_order is idempotent. A resend cannot act on a shipped order. The owner gave no reason, only "no blind resend; re-read the order" (Q7).
Pattern: a decision's reason that the inputs contradict, recorded beside the owner's decision.

Verifier: F9 | Style only | Nit | The decision itself is the owner's (Q7: "no blind resend; re-read the order"). The reason column, unlike other rows, does not claim to be the owner's words. Changing the reason changes no behavior. I concede the reason is wrong as stated: C-05 says a shipped order's cancel is rejected. The main thread may prefer Real Nit.

Decision: kept, Nit (Style only, but not a preference about phrasing: the reason states a fact C-05 contradicts). Fix: D-03's reason now reads "The owner's words: "no blind resend; re-read the order."" Pattern searched across the Decisions table; no other reason contradicts an input. Status: fixed.

---

F10 | Lies | Nit | claims.md C-02, C-04, C-07, C-13, C-29, C-38
Quote: C-29 quote: "Q8. The agent tells the customer the amount to be refunded ... what does the agent do?"; C-38 quote: "Yes, this tool set, with the new reason "refund amount differs"."
Evidence: C-29's quote is the question, not the answer. C-38's quote is the recommended answer, not the owner's reply ("Confirmed, with four changes", Q9). C-02 claims "the order's refund or none" and "Cancelled orders are listed too"; its quote holds neither. C-04 claims "fails"; its quote holds no such outcome. C-07's quote is only "issue_refund adds outcome OrderNotCancelled", not the fields and statuses the claim lists. C-13's quote has no "answers "created" or gets no answer".
Pattern: a claim says more than its quote, or quotes the question or the recommendation instead of the owner's reply.

Verifier: F10 | Style only | Nit | Every part of each claim's content is backed by an owner answer elsewhere. Only the quote cell is wrong: - C-02: Q4 says "returns each order with its refund or null" and "4. list_orders includes cancelled orders". - C-04: Q7 and Q12 say "re-read fails". - C-07: Q4 says "terminal refund error returns a refund with status failed, transient error creates none", and the Q9 tool list was confirmed. - C-13: the Q9 tool list says "answers 'created' or gets no answer", and it was confirmed. - C-29: the Q8 recommended answer plus "Yes, I accept your recommendation". - C-38: the Q9 recommendation. The owner confirmed it with four changes, none touching the reasons. C-30, C-33 and C-35 quote recommendations the same way. No behavior changes. If the main thread holds quote fidelity to Lies strictly, this is Real Nit.

Decision: kept, Nit, for C-02, C-04, C-07 and C-13 (a claim saying more than its quote is a Lies defect by definition, not phrasing). C-29 and C-38 are refuted: the claims template says a "proposed, accepted" quote is "the question the owner accepted", which C-29 quotes; C-38 quotes the accepted recommendation, as the café example does. Fix: the quotes of C-02, C-04, C-07 and C-13 now carry the owner's passages that hold each part of the claim; C-13's source is now "proposed, accepted", quoting the confirmed tool-set line and the owner's "Confirmed, with four changes:". Status: fixed.

---

F11 | Gap | Nit | rules.md R-05, "What the agent does"
Quote: absent
Evidence: The owner said "No cancellation fee, no store-credit option" (Q3) and "refund payment method = order's payment method" (Q3). R-05 states this, but no row says what the agent tells a customer who asks for store credit or a refund to a different card. The owner also said "Any change after confirmation voids it" (Q5). After a yes, the only change any row covers is switching to another order.
Pattern: an owner rule with no row for the customer request it answers.

Verifier: F11 | Not real | Nit | Both halves are settled. - After the yes: R-04 says what the agent does for any change, not only a switch: "Any change after the yes voids it, and the agent asks again." - Store credit or a different card: R-05 says what the agent offers: "The refund is the order's total paid, to the payment method the order was paid with, with no cancellation fee and no store credit." C-11 rules out another card, and SC-52 ("The customer asks for store credit...", Rules: R-05, R-03) covers the request.

Decision: dropped. Refutation: R-04 "Any change after the yes voids it, and the agent asks again." and R-05 "The refund is the order's total paid, to the payment method the order was paid with, with no cancellation fee and no store credit." Status: dropped.
