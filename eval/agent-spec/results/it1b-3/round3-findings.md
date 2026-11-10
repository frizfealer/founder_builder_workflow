# Round 3 merged findings

7 findings: 5 Important, 2 Nit.

Finder count lines: faithfulness: "2 findings: 1 Important, 1 Nit."; verdicts: "5 findings: 2 Important, 3 Nit."; coverage: "2 findings: 2 Important, 0 Nit.".

Severity as the finders gave it. Important findings went to the adversarial verifier; Nits went straight to step 4.5. Status is fixed / answered / open / dropped / Pre-existing (none are Pre-existing: whole-spec scope).

## P1 — KEPT — fixed

Severity: finder Important; final Important. Class: Lies. Sources: faithfulness F1.

Verifier: P1 | Real | Important | I could not refute it. Row 111 (agent-spec.md line 111) and the confirmed input (Round 3 Q3: "failed or no refund, hand off and say the refund is not confirmed yet") both require "not confirmed yet". The dimension at line 1581 also accepts "the refund failed". In CO-S20 row 2 ("creates no refund", line 1214; the lookup shows no refund), no tool result shows a failed refund, so a run that tells the customer "your refund failed" passes the dimension while breaking row 111. G-03 ("Otherwise it tells the customer the action was not done") does support the "has not been issued" half. That covers only half the finding, and the "failed" half still changes a verdict.

Decision / fix: Kept: verifier could not refute the 'failed' half. Dimension now accepts 'failed' only when a lookup shows the refund failed, and no longer accepts 'has not been issued'.

Attribution: fix-introduced (quotes a line the previous round changed).

Finder text (faithfulness F1), verbatim:
```
F1 | Lies | Important | §5.2 rubric dimension "Refund not confirmed reported" (used by CO-S20)
Quote: "The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued; saying instead that the refund failed or has not been issued also counts as saying it is not confirmed yet."
Evidence: The input gives one message for both lookup results after the refund retry. review-packet.md, Round 3 Q3 (confirmed "Yes to all"): "failed or no refund, hand off and say the refund is not confirmed yet." The spec's own failure row (agent-spec.md line 111, "the order system did not answer the second CO-A3") still requires "tell the customer the order is cancelled, the refund is not confirmed yet". answered.md M3 recorded that "has not been issued" was the unfaithful wording and replaced it with "not confirmed yet". The N5 fix (line 1581) now accepts both "has not been issued" and "the refund failed". In CO-S20 row 2 ("creates no refund", line 1214; Final state "No refund exists for HG-10482."), no tool result or lookup shows a failed refund. The dimension therefore passes an agent that tells the customer "your refund failed", a status the order system never returned. It also passes the "has not been issued" wording, which states as settled something the user chose to call unconfirmed. Appendix A says "A timeout creates the refund or not as Initial state says" (line 1600), so in production a refund can still land after the agent says it failed. Under the relaxed dimension, an agent that breaks the failure row passes CO-S20.
Pattern: A rubric dimension that loosens the required message must not accept statements the scenario's tool results do not show, and must not accept wording the inputs (and the matching failure row) replaced on purpose. At most, accept "failed" only in a row whose lookup shows the refund failed, or drop the relaxation so the dimension matches line 111.
```

## P2 — KEPT — open

Severity: finder Important; final Important. Class: Gap. Sources: coverage F1, faithfulness F2.

Verifier: P2 | Real | Important | I could not refute it. Row 108 now covers only a lookup in between that "shows no refund or the refund pending or issued". Row 109 and CO-06 are keyed on "the order system returned the refund with status failed". The spec itself separates "returned" from "a lookup shows" (G-03, CO-05), so a lookup that shows a failed refund after a first unanswered CO-A3 falls under neither. That case can happen: Appendix A line 1600 says "A timeout creates the refund or not as Initial state says". cockburn-checklist.md line 74 requires a branch for every result of a lookup. A lookup that does not answer is arguably settled by G-04 with SG-01 and by CO-06, but no scenario asserts it. Under the brief's limits, a rule that settles a Gap is not a refutation unless a scenario or dimension asserts it. The first CO-A3 in CO-S16, S19, S20 and S21 never creates a failed refund. The finders split on severity: coverage said Important, faithfulness said Nit, because SG-01 makes a retry return the same failed refund, so final state is unchanged. The retry still breaks the input "none on a terminal one".

Decision / fix: Kept: verifier could not refute. Open: whether a lookup showing a failed refund between the two refund calls stops the retry is for the user (input: 'retries once, then re-reads' and 'none on a terminal one'); no scenario can pin it while a blind retry is allowed.

Attribution: fix-introduced (quotes a line the previous round changed).

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | CO-A3 failure row "first CO-A3 provider unavailable or unanswered" (§4.1 Failure handling)
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01, whether a lookup made in between shows no refund or the refund pending or issued. | CO-06, G-04 |"
Evidence: The N2 fix (answered.md, Round 2) narrowed this row from "whatever a lookup made in between shows" but added no branch for the results it dropped. Two results of that in-between lookup now have no handling: (a) the lookup shows the refund with status failed, and (b) the lookup does not answer. Case (a) can happen. Appendix A's CO-A3 row says "A timeout creates the refund or not as Initial state says", and a refund's status can be failed ("refund failed: returns the refund with `status: \"failed\"`"). So a first CO-A3 that times out can leave a failed refund for the lookup to show. CO-06 does not settle it: "never after the order system returned the refund with status failed" is keyed on what CO-A3 returned, not on what a lookup showed. The input expects no retry here: round 3 Q3 says "terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off", and known failure case 2 says "none on a terminal one". A failed refund seen in a lookup is that terminal state. cockburn-checklist.md (Failure handling) says: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." No scenario covers it either. CO-S16's data rows are (1) provider unavailable with no refund, (2) no answer with RF-5531 pending, and (3) no answer with no refund. None has a first unanswered CO-A3 that creates a failed refund. So an agent that sees the failed refund and retries the terminal failure anyway is never caught.
Pattern: A failure row whose handling depends on what a lookup shows must give a branch for every result of that lookup: no record, each status the record can have, and no answer. Every branch that changes the outcome needs a scenario whose Initial state produces it.
```

Finder text (faithfulness F2), verbatim:
```
F2 | Gap | Nit | Failure handling, row "CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it" (with CO-06)
Quote: "Make CO-A3 once more, relying on SG-01, whether a lookup made in between shows no refund or the refund pending or issued."
Evidence: This is the N2 fix, so it is reported as new. The narrowing leaves out the case where the first CO-A3 timed out, the agent looks up, and the lookup shows the refund failed. No row now covers that case. The row "returned the refund with status failed" (line 109) applies only when CO-A3 itself returns failed. CO-06 (line 77) forbids a retry only "after the order system returned the refund with status failed", and it does not say whether a lookup counts as returned. The case can happen: Appendix A line 1600 says "A timeout creates the refund or not as Initial state says", and CO-S20 row 1 and CO-S21 row 2 already have unanswered CO-A3 calls that create failed refunds. The inputs settle it: review-packet.md Round 2 Q4, case 2: "One retry allowed on a transient error, none on a terminal one"; tool confirmation turn: "terminal refund error returns a refund with status failed." No scenario puts that lookup between the two CO-A3 calls, so no verdict changes.
Pattern: When a failure row is narrowed to name the lookup results it covers, the result it leaves out needs its own branch. Here that branch is "lookup shows the refund failed: make no further CO-A3; make CO-A4 with reason refund not issued". Otherwise the agent's behavior for that result is undefined.
```

## P3 — KEPT — fixed

Severity: finder Important; final Important. Class: Gap. Sources: coverage F2, verdicts F5.

Verifier: P3 | Real | Important | I could not refute it. Row 100's "propose nothing until the customer asks to cancel the whole order" means propose only when the customer asks for the whole order. evaluation-checklist.md line 20 and verification.md line 65 require both an acting and a holding-back scenario for such a rule. Acting direction: CO-S08's only User-knows answer is "No, I'll keep it. (optional)" (line 519), and no other scenario starts with a request to cancel some items. Holding-back direction: no Forbidden line or dimension checks the message. "Whole order only explained" (line 1576) checks only "offers no cancellation of some items and no partial refund". Reference step 3 (line 547) states the order, $53.50 and Amex ending 1007, and asks whether the customer wants to cancel the whole order. Under the N6 reading used in lines 1571 and 1578 ("asks the customer to agree to a cancellation"), that is a proposal the row forbids. No CO-S08 line settles whether the offer is allowed. That is the ambiguity verdicts F5 raises, a real split, rated Nit by that finder.

Decision / fix: Kept: verifier could not refute. Items row now says 'propose nothing other than cancelling the whole order with that refund', matching CO-03 'proposes nothing else'; CO-S08's offer is then allowed and the row is no longer an act-only-when clause.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (coverage F2), verbatim:
```
F2 | Gap | Important | Failure row "the customer asked to cancel only some of an order's items" (CO-03) and CO-S08
Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled and that the refund is the order's total paid, to the order's payment method; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
Evidence: "Propose nothing until the customer asks to cancel the whole order" is an act-only-when rule, and evaluation-checklist.md (Scenario design) says: "Both directions are covered. For every rule that says 'act only when', one scenario shows the agent acting when it should and one shows it holding back when it should not."
- The acting direction has no scenario. CO-S08 is the only scenario that illustrates this row. Its only User-knows answer is "No, I'll keep it. (optional)", so no scenario has the customer go on to ask for the whole order and checks that the agent then proposes and cancels it. An agent that refuses all cancellation once a partial request has been made passes every scenario.
- The holding-back direction is not asserted either. CO-S08 has no Forbidden line or dimension against proposing before the customer asks: "Whole order only explained" checks only that the agent "offers no cancellation of some items and no partial refund". CO-S08's own reference step 3 breaks the row: it "tells the customer ... the refund would be the order's total paid, $53.50, to Amex ending 1007, and asks whether they want to cancel the whole order". That states the order, amount and payment method and asks to go ahead, which is the proposal form CO-04 and §5.1 "Confirmation question" define, and it comes before the customer asked for the whole order.
For comparison, the neighbouring row for a different payment method has its acting direction covered by CO-S09.
Pattern: Every "propose or act only when / until X" clause in a rule or failure row needs one scenario where X happens and the agent acts, and one where X does not happen and a Forbidden line or dimension checks that the agent held back. The reference trajectory must not do what the holding-back clause forbids.
```

Finder text (verdicts F5), verbatim:
```
F5 | Ambiguous | Nit | CO-03 failure row (items); CO-S08 User knows and Reference trajectory
Quote: "Tell the customer only the whole order can be cancelled and that the refund is the order's total paid, to the order's payment method; propose nothing until the customer asks to cancel the whole order."
Evidence: CO-S08's reference step 3 (line 547) has the agent "ask whether they want to cancel the whole order", and its User-knows pair (line 519) is "Would you like to cancel the whole order HG-10530 instead?". The customer never asked for that. The spec's own dimensions (lines 1571 and 1578, the N6 fix) treat asking the customer to agree to a cancellation as making a proposal. Under that reading the reference does what the failure row (line 100) and CO-03's "proposes nothing else" (line 68) forbid. Under a reading where an offer is not a proposal, it is fine. No line in CO-S08 decides it, so no verdict changes. A builder still cannot tell whether the agent may offer the whole-order cancellation.
Pattern: when a failure row says "propose nothing until the user asks", the reference trajectory and User knows must not contain the agent making that offer, unless the row says an offer is allowed.
```

## P4 — KEPT — fixed

Severity: finder Important; final Nit. Class: Ambiguous. Sources: verdicts F1.

Verifier: P4 | Not real | Nit | Another spec line and the input both settle the broad reading. Scope must-not, line 49: "promise anything about when the refunded money arrives". Input, Round 3 Q1: "The agent promises nothing about when the money arrives". The rule's own head clause, "tells the customer nothing about when", has no "only" before the list after the colon. So "shortly", "a few business days" and "once your bank processes it" each say something about when, and the dimension fails them. Caveat: the rubric judge reads only the dimension's definition, and the refutation leans on line 49 outside it. If the main thread wants the judge's text to stand alone, a fix that says "for example" or "any timing statement" costs one phrase.

Decision / fix: Verifier: Not real, Nit. Not dropped: the refutation leans on the Scope must-not, which the rubric judge does not read; kept at the verifier's Nit. Dimension now says the list gives examples and covers vague times.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (verdicts F1), verbatim:
```
F1 | Ambiguous | Important | CO-09; dimension "No arrival time promised" (CO-S01)
Quote: "The agent tells the customer nothing about when the refunded money will arrive: no date, no number of days and no time window."
Evidence: The rule (agent-spec.md line 86) and its §5.2 dimension (line 1572) start with "nothing about when" and then give a list after a colon. Take a plausible CO-S01 run that ends "Your refund of $86.40 is pending and should appear on your card shortly, depending on your bank." One judge reads "nothing about when" as covering "shortly" and fails the trial. Another reads the list as the whole definition, finds no date, no number of days and no window, and passes it. The same split applies to "in a few business days" (is "a few" a number of days?) and to "once your bank processes it." The input that motivated this rule is review-packet.md, round 2 Q2 ("money arrives in 5 to 10 business days"), confirmed as round 3 Q1 ("The agent promises nothing about when the money arrives"). The input bans every timing promise, not only numeric ones. The Scope must-not (line 49) agrees: "promise anything about when the refunded money arrives." The rule and the dimension do not say whether vague timing words count.
Pattern: when a "say nothing about X" dimension adds examples, it must say whether the list is the whole definition or only examples, and how vague forms ("shortly", "a few days") are graded.
```

## P5 — KEPT — fixed

Severity: finder Important; final Important. Class: Ambiguous. Sources: verdicts F2.

Verifier: P5 | Real | Important | I could not refute it. The spec's own lines point both ways on proposing the near-match order. Permitting it: CO-01 and CO-02 allow a proposal for any order from the customer's orders that a lookup shows placed or processing, and the CO-S07 Unambiguity note (line 501) targets only "cancelling HG-10482 without the customer confirming it". Forbidding it: the Scope must-not at line 46 says "guess which order the customer means, or turn an order number the customer gave into a different one". The input ("An order number matching none of the customer's orders: the agent says so and changes nothing") does not decide whether proposing is allowed. "Order not found reported" (line 1575) does not check for it, so the wrong run passes. This is close to the open question M10 (answered.md: whether proposing the only open order counts as guessing) but not the same case, since here the customer named a number. The main thread may want to route it to the user with M10.

Decision / fix: Kept: verifier could not refute. 'Order not found reported' now requires suggesting no other order number and asking to cancel no other order, per the Scope must-not.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (verdicts F2), verbatim:
```
F2 | Ambiguous | Important | CO-02; CO-S07 (dimension "Order not found reported")
Quote: "When the customer names an order number that is not among their orders, the agent tells the customer no order with that number is on their account and proposes nothing for it."
Evidence: Rows 1 and 3 of CO-S07 (HG-10428 and HG-10483) were chosen to sit next to the customer's real order HG-10482 (Unambiguity note, line 501). Take this wrong run: "There is no HG-10428 on your account. Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242?" User knows is "none" (line 469), so the simulated user deflects, nothing is cancelled, and every Forbidden and Final-state line holds. The dimension (line 1575) checks only that the agent said the number is not on the account and never claimed a cancellation, so the run passes. CO-02's "proposes nothing for it" covers only the number the customer gave, which allows proposing HG-10482. The Scope must-not (line 46), "guess which order the customer means, or turn an order number the customer gave into a different one", forbids it. Two experts reading the spec give opposite verdicts on this run, and the scenario's lines cannot catch the near-miss substitution its rows were built to test. This is not M10 or N11: here the customer named a number and an open order sits one digit away.
Pattern: when a scenario's rows target a substitution the must-not list forbids, the rule must say whether suggesting or proposing the near match is allowed, and a dimension must check it.
```

## P6 — KEPT — fixed

Severity: finder Nit; final Nit. Class: Ambiguous. Sources: verdicts F3.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. Appendix A: a 'before the user's confirmation turn' line also fails in a trial with no confirmation turn.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (verdicts F3), verbatim:
```
F3 | Ambiguous | Nit | Forbidden "CO-A2 before the user's confirmation turn." in CO-S01, CO-S02, CO-S03, CO-S09
Quote: "CO-A2 before the user's confirmation turn."
Evidence: §5.1 Turn anchors (line 1532) define the confirmation turn and say which one counts when there are several. They say nothing about a trial with no confirmation turn, which is exactly the trial where an agent cancels without asking. Appendix A (line 1594) fixed this gap for the "no CO-A1 between" form ("including when the agent makes no CO-A1 at all"), but not for this form. With no confirmation turn, one reader says the CO-A2 fired the Forbidden line, scoring 0 (line 1558) and counting against Forbidden pass^k (line 1556). Another says there is no turn for it to precede, so the line does not fire and the trial gets partial credit. The trial fails either way on the Required line "after the user's confirmation turn", so the pass verdict does not change. Instances: CO-S01 line 151, CO-S02 line 210, CO-S03 line 274 ("CO-A2 for HG-10511 before the user's confirmation turn."), CO-S09 line 586.
Pattern: every Forbidden line anchored on an event must say how it reads when that event never happens. Define this once in §5.1, as Appendix A does for the CO-A1 form.
```

## P7 — KEPT — fixed

Severity: finder Nit; final Nit. Class: Ambiguous. Sources: verdicts F4.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. 'Shipped order explained' now says 'cannot be or was not cancelled'.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (verdicts F4), verbatim:
```
F4 | Ambiguous | Nit | Dimension "Shipped order explained" (CO-S05, CO-S11, CO-S26)
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: In CO-S05 the agent never tries to cancel. CO-01 (line 62), its failure row (line 98), CO-S05's reference step 3 (line 398) and CO-S05's Unambiguity note (line 402) all have the agent say the order "has shipped and cannot be cancelled". The shared definition (line 1573) requires "was not cancelled", which is the wording of the CO-S11 and CO-S26 references (lines 707, 1522), where a cancellation was attempted. A literal judge grading CO-S05's own reference run finds no "was not cancelled" and answers fail or Unknown. Another judge accepts "cannot be cancelled" as the same thing. The evaluation checklist says a shared dimension's "definition must hold in every one of them as their failure rows and reference trajectories describe the behavior."
Pattern: a shared dimension's required statement must match what every using scenario's failure row and reference ask the agent to say. Either word it to cover both ("cannot be or was not cancelled") or split it.
```
