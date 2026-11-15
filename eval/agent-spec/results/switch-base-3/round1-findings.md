# Round 1 findings

Finder count line: 12 findings: 6 Important, 6 Nit.
Verifier count line: 8 Real (F1, F3, F4, F5, F6, F8, F9, F12), 3 Not real (F2, F7, F11), 1 Style only (F10).

Kept 10, dropped 2 (F2, F11). Pre-existing: 0.

## F1

```
F1 | Lies | Important | rules.md R-05
Quote: "When the customer changes any part of the proposal after the yes, the yes no longer counts and the agent proposes again."
Evidence: In review-packet.md, Question 4, the owner's reply is: "any change after confirmation voids it". The recommended answer, also under Question 4, is: "any change to the proposal voids that yes". The owner did not limit this to changes the customer makes. C-32 says it correctly ("Any change after the confirmation voids it"), but R-05 narrows it to changes the customer makes. Changes on the system's side, such as the order's total paid or payment method being different when the agent next looks, do not void the yes under R-05.
Pattern: A rule turns the owner's general condition ("any change") into one cause of it ("the customer changes").
```

Verifier: F1 | Real | Nit | The finding fits Lies: R-05 narrows the owner's "any change after confirmation voids it" to "When the customer changes any part of the proposal". Two lines cover the system-side changes at the refund call. For the amount, R-13 says "When the refund call answers with an amount different from the one the customer said yes to, the agent makes no further change with the new amount... hands the case to staff". For the method, C-14 says "Refunds can only be sent back to the original payment method used in a charge", so the payment method cannot differ. What still stands is the narrowed wording, and an amount shown by a later lookup (that part is F3). By then the refund already exists, so voiding the yes would change nothing further. So I rate this Nit, not Important.

Decision: KEPT at Nit (verifier's lower severity). Status: fixed. R-05 now reads "Any change to the proposal after the yes voids the yes. When the customer changes any part of it, the agent proposes again." (owner accepted in question 14).

## F2

```
F2 | Gap | Important | rules.md R-05, R-07; "What the agent does"; claims.md C-26
Quote: "absent" (R-05 says only "the agent proposes again")
Evidence: In Question 2 the owner says: "No cancellation fee, no store-credit option." and "refund amount = order total paid; refund payment method = order's payment method". C-26 records this, and R-05 lists C-26 under "Rests on", but no rule text or row says what the agent does when the customer asks for store credit, a different card or a different amount. Only one row covers a change to the proposal: "the customer said yes and then named a different order". R-05's "proposes again" suggests the customer can change the amount or the destination, which the owner ruled out.
Pattern: An owner answer is carried only by a claim. No rule or row covers the case where the customer asks for what that answer rules out.
```

Verifier: F2 | Not real | Important | Payment method and store credit: R-07 says "The refund goes back only to the order's payment method", and SC-39 (scenarios.md) says "a customer who asks for the money to go to another card or to store credit is told it goes back to the order's payment method." Amount: R-05 fixes the proposal's amount as "the refund amount (the order's total paid)", so "proposes again" can only offer the total paid again. The customer cannot change the amount or where it goes. One soft spot: no line spells out what the agent says to a customer who asks for a different amount, beyond proposing the total paid again.

Decision: DROPPED. Refutation read and agreed: R-07 "The refund goes back only to the order's payment method" and R-05 "the refund amount (the order's total paid)" fix the amount and where the money goes, so the customer cannot change either; SC-39 states the store-credit and other-card case. Status: dropped.

## F3

```
F3 | Gap | Important | rules.md R-09, R-13, "What the agent does" row "the new lookup shows the refund pending or issued"; policy.md A8
Quote: "the new lookup shows the refund pending or issued | says the order is cancelled and the refund is pending or issued, with no promise of when it arrives" and A8 "the refund of the total paid to the payment method is pending or issued"
Evidence: Question 9 is about the refund amount the agent passes on from a tool. The owner accepted: "tells the customer the amount the refund call returned, and hands the case to store staff (reason: refund amount differs)". R-13 checks the amount only when "the refund call answers". It does not check the refund found by the new lookup after an unanswered refund call (R-09). A8 still tells the customer "the total paid", whatever amount the lookup shows. No rule anywhere checks whether the refund's payment method matches the confirmed one. In Question 4 the owner made "where it goes" part of what the customer confirms, and C-04 shows that a refund record holds its own payment method.
Pattern: A value passed on from a tool is compared with what the customer confirmed on one path only, and not on the other paths that pass it on.
```

Verifier: F3 | Real | Important | The payment-method part is refuted. C-14 says "Refunds can only be sent back to the original payment method used in a charge", and issue_refund takes only the order number, so a refund cannot go to another method. The amount part stands. R-13 checks only "When the refund call answers with an amount different". R-09 says only "A pending or issued refund: it reports that status". A8 says "the refund of the total paid", whatever amount the new lookup shows. The model never draws a different amount on the lookup path (refund_look is only ok, failed or nothing). No line covers a mismatch there.

Decision: KEPT, Important. Status: fixed. The payment-method part is refuted by C-14; the amount part stood. R-13 now covers "a refund call or a lookup" (owner accepted in question 14); the model draws a refund for a different amount on the no-answer and lookup paths, with a row for the lookup case (SC-44, SC-45, SC-46).

## F4

```
F4 | Gap | Important | rules.md R-15, "What the agent does" row "the lookup got no answer"; claims.md C-07, C-42
Quote: "When the first lookup of the customer's orders gets no answer, the agent tries it again; the owner set no limit on lookups."
Evidence: In Questions 6 and 12 the owner says: "Reads may be retried on timeout without limit; only commit calls are bounded." The owner's word is "may", and the owner turned down the recommendation that the agent tell the customer it cannot look up their orders. Nothing ends the loop, and nothing tells the customer anything while it runs. C-07 admits this: "nothing ends repeated lookups that keep getting no answer (C-42)". R-15 also applies the retry only to "the first lookup", but the owner's sentence covers every read. R-09 and R-10 treat a failed re-read after an unanswered cancel or refund as final after one try, and the spec leaves that question open as C-42 ("nobody").
Pattern: A repeated call has no end and no message to the customer, and a permission the owner gave for all reads is applied to one read only.
```

Verifier: F4 | Real | Important | The second part is partly refuted. The owner's own answers make a failed re-read final: Q8 says "Re-read fails, say outcome unknown, issue no refund, hand off", and Q13 says "re-read fails, say status unknown and hand off". R-09 and R-10 follow these. The main point stands. R-15's lookup has no end and no message to the customer, and C-07 admits it: "nothing ends repeated lookups that keep getting no answer (C-42)". C-42 is still an open question (owner "nobody"). verification.md lists "a repeated thing with no end" as a Gap.

Decision: KEPT, Important. Status: open. Put to the owner as a rule change with a bound of 3 lookups (question 15); the owner's reply kept "Reads may be retried on timeout without limit; only commit calls are bounded." R-15 is unchanged; what ends repeated lookups, and what the customer hears meanwhile, stays open (C-42).

## F5

```
F5 | Gap | Important | rules.md R-14, "What the agent does"; policy.md chart steps
Quote: "A request to cancel another order gets its own proposal and its own yes." / row "the customer said yes and then named a different order | proposes again for the order now named"
Evidence: In Question 11 the owner accepted: "a request to cancel another order gets its own proposal and its own yes. It ends when the customer makes no further request". These cases have no row:
- two orders named in one message ("cancel HG-1 and HG-2"), including which order goes first;
- a second request after the first order ends. Every end state in policy.md ("Cancelled and refunded, customer told", "Handed to staff, customer told", "Nothing changed, customer told") has no arrow back to "Looking up orders";
- a second order named while a proposal waits for a yes.
The one row that does cover another order treats it as a replacement ("proposes again for the order now named"), not as an extra request.
Pattern: A case the agent will meet (several requests in one conversation) is stated as a rule but has no row or path for its main forms.
```

Verifier: F5 | Real | Important | One part is covered. For two orders in one message, R-14 says "The agent works on one order at a time. A request to cancel another order gets its own proposal and its own yes", and SC-37 says the agent must "take them one at a time, each with its own proposal and yes". For a second request after the first order ends, the model.py docstring says it "starts a new run", but no rule, row or arrow says so. Still uncovered: which order goes first; a second order named while a proposal waits for a yes; and the clash between R-14 (an extra request) and the row "the customer said yes and then named a different order | proposes again for the order now named", which treats the new order as a replacement. verification.md names exactly these cases as a Gap.

Decision: KEPT, Important. Status: fixed. R-14 now says the order goes in the order named, a second order named at the proposal is asked about (instead or as well), and a later request starts with a lookup (owner accepted in question 16); rows added; the model has the instead-or-as-well step (SC-42, SC-43).

## F6

```
F6 | Gap | Nit | rules.md "What the agent does" rows for an order the customer has not named
Quote: "the customer has two open orders and did not say which | asks which order" / "the customer named one open order, or has only one"
Evidence: R-04 says "more than one open order", but the row says "two". No row covers a customer who did not name an order and has no open orders, or no orders at all. The owner gave the case "customer has two open orders" (Question 5, case 1) as one example of disambiguation, not as the only one.
Pattern: The rows list the owner's example rather than the class it stands for, which leaves its neighbours (none, three or more) uncovered.
```

Verifier: F6 | Real | Nit | Three or more open orders are covered: R-04 says "When the customer could mean more than one open order, the agent asks which one", so the row's "two" is only narrower wording. One case stands. A customer who names no order and has no orders at all matches no row; the rows assume a named order, a shipped or cancelled order, or one or two open orders.

Decision: KEPT, Nit. Status: fixed. The row says "more than one open order"; a row and a starting situation cover a customer with no order to cancel (C-44, spec only; SC-41).

## F7

```
F7 | Unclear | Important | rules.md R-10, "What the agent does" row "the lookup after the cancel got no answer, or the order is still not cancelled after the second cancel call"
Quote: "The lookup fails, or the order is still not cancelled after the second cancel call: it says the outcome is unknown, issues no refund, and hands the case to staff as \"cancellation unknown\"."
Evidence: A second cancel call can answer "not cancellable" with status shipped (C-08, C-09). Read literally, that leaves the order "still not cancelled", so R-10 tells the customer "the outcome is unknown", even though the outcome is known. Two rows then match the same situation: this one and "the cancel call answered \"not cancellable\"". In Question 2 the owner says that when the order flips to shipped, "the store rejects the cancel and the agent must report that truthfully and issue no refund call."
Pattern: A catch-all condition ("still not cancelled") also catches an outcome that another rule handles with a different message.
```

Verifier: F7 | Not real | Important | R-02 says "When the order system shows the order has shipped since the lookup, the agent tells the customer so and issues no refund". R-10 itself says "Shipped: it tells the customer and issues no refund". The row "the cancel call answered \"not cancellable\"" holds for any cancel call. SC-24 ("second cancel finds it shipped", Rules R-10, R-02, R-06) ends on "not cancellable", not on "cancellation unknown". In model.py, cancel_steps checks not_cancellable before the cancellation-unknown branch. "Still not cancelled" therefore applies only when the order is still placed or processing after the second call, as SC-32 shows.

Decision: KEPT, Important (the verifier said Not real; the runner did not agree the cited lines refute an Unclear finding about R-10's own wording, which literally includes a shipped answer). Status: fixed. R-10 now says "the lookup after the second cancel call still shows the order placed or processing" (owner accepted in question 17).

## F8

```
F8 | Lies | Nit | rules.md R-03 and row "the customer asked to cancel some items of an open order"; policy.md A12; rules.md R-12 and row "the second follow-up call got no answer"
Quote: "says only the whole order can be cancelled, and asks whether to cancel the whole order" / "tells the customer what happened to the order and the refund, that it could not reach store staff, and to contact Harbor Goods support"
Evidence: In Question 2 the owner's words are only: "the agent says only the whole order can be cancelled." R-03's own text says the agent "goes on only if the customer then asks", so the row's "asks whether to cancel the whole order" departs even from R-03. In Question 10 the owner did not accept the recommendation and replied only: "tell the customer to contact Harbor Goods support". "That it could not reach store staff" comes from the unaccepted recommendation, yet D-03 is logged as "the owner".
Pattern: What the agent tells the customer adds content the owner did not give.
```

Verifier: F8 | Real | Nit | Neither part is refuted. The owner's only words are "the agent says only the whole order can be cancelled". R-03 says "goes on only if the customer then asks", yet the row and A12 add "asks whether to cancel the whole order". For the unreachable staff case, the owner replied only "tell the customer to contact Harbor Goods support", yet R-12 adds "that it could not reach store staff". One sub-point does not hold. D-03 does not contain the added content; it reads "then the customer is sent to Harbor Goods support", which matches the owner's words.

Decision: KEPT, Nit. Status: fixed. The R-03 row now says only "says only the whole order can be cancelled", with a separate row for the customer then asking for the whole order; R-12 no longer adds "that it could not reach store staff" (owner accepted in question 17); the model's message is "please contact Harbor Goods support".

## F9

```
F9 | Lies | Nit | claims.md C-11, C-16, C-17
Quote: C-11 "A refund call answers with a refund whose status is pending or issued; on a terminal error ... or it gets no answer." (quote: "2. issue_refund adds outcome OrderNotCancelled."); C-16 "A refund can still fail after it is issued" (quote: "A refund can fail if the customer's bank or card issuer can't process it."); C-17 "...refund not issued, refund status unknown, cancellation unknown, or refund amount differs." (the quote lists only the first three reasons and contains "handoff timeout not retried")
Evidence: Each claim says more than its quote:
- C-11: the extra outcomes come from the Question 6 proposal, which is not quoted.
- C-16: "after it is issued" is not in Stripe's sentence.
- C-17: "refund amount differs" is not in the quoted line. That line is the superseded proposal, whose "handoff timeout not retried" the owner overturned in Question 6, change 3: "On timeout, retry once".
Pattern: A claim's quote does not support the whole claim, or quotes text the owner later changed.
```

Verifier: F9 | Real | Nit | Most of C-11 and C-17 is supported elsewhere in the packet, though not by their own quotes. For C-11, the Q6 reply itself says "terminal refund error returns a refund with status failed, transient error creates none" and "Confirmed, with four changes". For C-17, Q9's accepted recommendation gives "(reason: refund amount differs)". C-16's "after it is issued" has no support: Stripe's quoted sentence does not say it. C-17's quote is still the line whose "handoff timeout not retried" the owner overturned, and verification.md lists "a claim says more than its quote" as a Lies defect.

Decision: KEPT, Nit. Status: fixed. C-11 now quotes the tool-set line and states only its outcomes; the not-cancelled outcome is C-43 with its own quote; C-16 drops "after it is issued"; C-17 states only the three recorded reasons and points to C-40 for the fourth.

## F10

```
F10 | Lies | Nit | claims.md C-38
Quote: "The customer has no transcripts or known incidents"
Evidence: In Question 5 the owner says: "Q4: No transcripts or known incidents." That is the owner's statement about the store, not about the customer.
Pattern: A claim names the wrong party.
```

Verifier: F10 | Style only | Nit | C-38's "The customer has no transcripts" names the wrong party, but the claim's content matches the owner's "No transcripts or known incidents". No rule depends on who holds the transcripts, so no behavior changes, and the owner would not misread it.

Decision: KEPT at Nit (the verifier said Style only; the runner did not agree a wrong party is a preference about phrasing). Status: fixed. C-38 now reads "Harbor Goods has no transcripts or known incidents".

## F11

```
F11 | Lies | Nit | rules.md R-08
Quote: "After a refund with status failed, a second error, or an answer that the order is not cancelled, it makes no further refund call, tells the customer the refund was not issued, and hands the case to staff as \"refund not issued\"."
Evidence: For this outcome the owner said only "2. issue_refund adds outcome OrderNotCancelled." (Question 6). How the agent handles it has no owner answer, no decision and no "spec only" claim. D-04, which R-08 rests on, covers only transient and terminal errors. The message it leads to (A7, "the order is cancelled and the refund was not issued") also says the order is cancelled when the order system has just answered that it is not.
Pattern: A rule's handling of an outcome is the spec's own choice, but it is not recorded as a decision or a "spec only" claim.
```

Verifier: F11 | Not real | Nit | The owner's Q5 answer covers how a refund-call error is handled: "Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process... none on a terminal one". C-33 carries it, and R-08 rests on C-33. The A7 message point needs a state that cannot occur. R-06 says "The agent issues the refund only after the order system has shown the order cancelled", so a "not cancelled" answer is impossible at that point. model.py draws that outcome only "for an order the order system has not cancelled", which is why no A7 line covers it.

Decision: DROPPED. Refutation read and agreed: C-33 carries the owner's answer for a refund-call error ("refund not issued, state known; agent reports it, does not claim success, hands off"), R-08 rests on it, and R-06 "The agent issues the refund only after the order system has shown the order cancelled" makes a not-cancelled answer impossible at that point. Status: dropped.

## F12

```
F12 | Unclear | Nit | rules.md R-12
Quote: "Each case R-08, R-09, R-10 and R-13 hand to staff gets a follow-up with its reason."
Evidence: To learn which cases reach staff, the owner has to look up four rules. The rule could name them in one sentence: a refund that failed or was not issued, a refund whose status is unknown, a cancellation whose outcome is unknown, and a refund amount that differs.
Pattern: Rule ids stand in for a sentence the owner needs to read.
```

Verifier: F12 | Real | Nit | Only partly mitigated. The reasons are spelled out elsewhere, in C-17's list and in the rows "hands the case to staff as ...". R-12 itself still uses "R-08, R-09, R-10 and R-13" in place of the sentence the owner needs, which verification.md lists as an Unclear defect: "a rule id standing in for a sentence the owner would need to read".

Decision: KEPT, Nit. Status: fixed. R-12 now names the four cases in a sentence (owner accepted in question 17).
