# Round 1 findings (merged, verbatim)

Merged count line: 15 findings: 9 Important, 6 Nit.

## R1-01 — kept — fixed

```
R1-01 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"
Source: faithfulness F2, coverage F1
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: review-packet.md line 64 (round 3 Q4, confirmed "Yes to all") says: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." The row skips the re-read. It forbids CO-A3 and requires the "cancellation unknown" handoff and message even when a lookup would show the order cancelled or shipped. That contradicts CO-07 ("when the agent cannot tell whether the order was cancelled ... CO-A4 occurs in no other situation") and G-03, the truthful outcome rule. The spec itself expects a late effect: SG-04's Covers cell is "a first, unanswered one took effect late". And CO-S15's Initial state adds "does not answer any CO-A1 the agent makes after its second CO-A2", a line that only matters if a lookup comes next. In production, a cancelled order would get no refund and a handoff with a false reason.
Pattern: a failure row for a repeated unanswered commit call drops the lookup-then-branch step that the input prescribes for an unanswered call. It goes straight to the "unknown" outcome even when a lookup could settle the outcome.
Merged duplicate (coverage F1), verbatim:
  F1 | Gap | Important | 4.1 Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
  Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
  Evidence: Interview round 3 Q4 (review-packet.md line 64), confirmed "Yes to all", says that after a cancel timeout the agent does "no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." That re-read applies to any cancel timeout. Known failure case 3 (line 54) has the same shape: after the retry, re-read and "report what it finds". The spec's row for the second unanswered CO-A2 has no lookup and no branches. It sends every such case to a "cancellation unknown" handoff, which conflicts with two spec lines. CO-07 (line 80) allows CO-A4 only "when the agent cannot tell whether the order was cancelled", but a lookup can tell. CO-05 (line 74) allows CO-A3 when "a lookup shows cancelled". The cockburn checklist (line 74) says "A failure row that branches on a lookup covers every result of the lookup". CO-S15's Initial state (line 892, "does not answer any CO-A1 the agent makes after its second CO-A2") assumes a lookup but tests only the unanswered branch. No row or scenario covers a lookup after the second unanswered CO-A2 that shows the order cancelled (refund owed), shipped, or still open. In production, a customer whose order was in fact cancelled gets no refund and a wrong "unknown" report.
  Pattern: A row for a repeated unanswered commit call skips the post-timeout lookup that the inputs require for every timeout, so the lookup's answered results have no branch and no scenario.
```

Verifier: `R1-01 | Real | Important | Could not refute. Round 3 Q4 (packet), confirmed "Yes to all", says "If the cancel call times out: no blind resend; re-read the order ... Re-read fails, say outcome unknown". That covers any cancel timeout. The second-timeout row goes straight to "make CO-A4 with reason cancellation unknown", with no lookup and no branches. That conflicts with CO-07, which allows CO-A4 only "when the agent cannot tell whether the order was cancelled", and with CO-05's "a lookup shows cancelled". CO-S15's step 8 also skips the lookup. No spec line supports going straight to "unknown" when a lookup could settle the outcome.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. Second-unanswered-CO-A2 row now looks up and branches; CO-S15 makes the lookup; new CO-S25, CO-S26, CO-S27 cover the cancelled, shipped and still-open branches.

## R1-02 — kept — fixed

```
R1-02 | Gap | Important | 4.1 Failure handling, row "any | the customer changed the order or another proposal term in the confirming turn or after confirming"; G-02
Source: coverage F2
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: The only change-of-mind scenario is CO-S03. Its Turn 2 (line 248) is said "in place of a confirmation", and none of its variants (lines 275-277) contains a confirmation. Its Unambiguity note (line 292) says the turn "confirms nothing". No scenario has a turn that confirms and changes a term together (e.g. "Yes, but cancel HG-10511 instead"), or a change after a confirmation. So G-02's "Any change to a proposal term after confirmation voids that confirmation" (line 21) and this row's trigger condition never come up in any Initial state or User block. An agent that hears "yes" and then cancels the changed order without asking again passes every scenario.
Pattern: A failure row that changes the outcome (it voids an authorization) has no scenario that sets off its exact condition. A nearby scenario covers a weaker condition instead.
```

Verifier: `R1-02 | Real | Important | Could not refute. CO-S03's Turn 2 is said "in place of a confirmation", and its note says it "confirms nothing". No scenario confirms and changes a term in the same turn, or changes a term after confirming. So the row's trigger, "in the confirming turn or after confirming, before CO-A2", never occurs in any scenario. That is a failure row that changes the outcome (it voids the confirmation) with no scenario.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. CO-S03 rows 4 and 5 carry a yes together with a changed order; 'in place of a confirmation' removed from CO-S03 Turn 2.

## R1-03 — kept — fixed

```
R1-03 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 (success-path messages)
Source: verdicts F2, coverage F3
Quote: "absent"
Evidence: G-03 (line 24) says the agent "tells the customer a refund is pending or issued only when the order system returned that refund with that status". Scope & Authority (line 49) says "must not ... promise a date by which the refunded money arrives". Packet round 3 Q1 says "The agent promises nothing about when the money arrives." In every success-path scenario the only check on the agent's words is message check "Refund id reported" (CO-S01 note, line 170: "the only check on the agent's words"). In each of these scenarios the refund is pending. A final message such as "Refund RF-5531 has been issued and will reach your Visa in 5-10 business days" contains the id, so it passes every line. That message breaks G-03 by calling the refund issued, and it breaks the no-date rule; the date wording is a common LLM default. A dimension that checks the status exists ("Refund status reported"), but only CO-S19 uses it. No scenario asserts the no-date rule.
Pattern: a rule limits what the agent may tell the customer on the success path, but the success scenarios check only one verbatim value. A false status or a forbidden promise in the same message passes.
Merged duplicate (coverage F3), verbatim:
  F3 | Gap | Important | 4.1 Contract (no rule); 5.2 dimensions
  Quote: "absent" (the only mention is the Scope & Authority line "- promise a date by which the refunded money arrives.")
  Evidence: Interview round 3 Q1 (review-packet.md line 61), confirmed "Yes to all": "The agent promises nothing about when the money arrives." This is a confirmed domain rule. Round 2 Q2's "5 to 10 business days" was dropped. No contract rule protects it: CO-01..CO-08 and G-01..G-04 (spec lines 17-83) never mention arrival timing. No scenario or rubric dimension asserts it either (dimension table, lines 1497-1509). An agent that says "your refund will arrive in 5-7 business days" passes CO-S01, CO-S09, CO-S16 and CO-S19.
  Pattern: A must-not or domain rule from the inputs that sits only in Scope & Authority has no contract rule and no scenario or dimension that checks it.
```

Verifier: `R1-03 | Real | Important | Could not refute. CO-S01's note says message check "Refund id reported" is "the only check on the agent's words", and the same holds in every success scenario except CO-S19, which adds "Refund status reported". A message that calls a pending refund "issued", which G-03 forbids, still passes. So does one that promises "5-10 business days", which Scope & Authority forbids ("promise a date by which the refunded money arrives") and round 3 Q1 rules out. No dimension checks the no-date rule anywhere.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. Dimensions 'Refund status reported' (generalised) and 'No arrival date promised' added to the nine success scenarios. A contract rule for the no-date promise would change rule text; proposed to the user as an open question.

## R1-04 — dropped — dropped

```
R1-04 | Gap | Important | CO-02; CO-S01, CO-S02
Source: coverage F4
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-02 is an "ask only when" rule. CO-S02 covers the asking side (two open orders, "I want to cancel my order."). No scenario covers the other side, where the request names no order and exactly one order is placed or processing, so the agent should propose without asking. Every CO-S01 Turn 1 names the order (lines 155-157), and so does every other scenario's Turn 1. evaluation-checklist.md, "Both directions are covered": "test only 'asks when unsure' and you get an agent that always asks." product-idea.md: "The customer should not need to know the store's ... rules." An agent that will not propose until the customer gives an order number passes every scenario.
Pattern: An "act only when" rule is tested only on the side where the condition holds.
```

Verifier: `R1-04 | Not real | Important | Both directions of CO-02 already have a scenario. CO-S02 is the asking side. CO-S01 is the side where the condition is false: Turn 1 "Please cancel order HG-10482." names the order, and the reference trajectory goes from CO-A1 straight to the proposal (steps 2-3) without asking which. The checklist asks for one acting and one holding-back scenario, and both exist. The finding wants one more boundary (a request that names no order, with a single open order), which is "one more scenario would be nice". Also, §5.2 never scores over-asking ("never folded into the score"), so an always-asking agent would pass the proposed scenario too.`

Decision: dropped. Verifier Not real, quoting CO-S01 ('Please cancel order HG-10482.', trajectory steps 2-3 propose without asking) as the scenario where CO-02's condition is false. I read it and agree: CO-02 has an asking scenario (CO-S02) and a not-asking one (CO-S01), which is what the 'act only when' coverage condition asks; the finding asks for one more boundary scenario.

Status: dropped. 

## R1-05 — kept — open

```
R1-05 | Gap | Important | 4.1 Failure handling (no row); G-01, CO-06
Source: coverage F5
Quote: "absent"
Evidence: The cockburn brainstorm (cockburn-checklist.md line 64, "the lookup returns more than one plausible match") covers a request that is about more than one open order, such as "cancel both my orders". The agent can detect this, but no failure row covers it. The spec's lines pull in different directions. G-01 (line 18) allows "at most the one order the current request is about". Purpose (line 5) says "It may cancel that one order". CO-06 (line 77) caps CO-A2 at two "in a conversation", so cancelling two orders one after the other would use up the retry allowance. Nothing says whether the agent cancels one, asks the customer to pick one, or handles them one at a time. No scenario covers it, so the coder will invent the behavior for a money-moving action.
Pattern: A detectable "more than one match" case in the brainstorm has no failure row, and the per-conversation limits imply an answer that no rule states.
```

Verifier: `R1-05 | Not real | Important | The evidence does not say what the finding claims. The brainstorm item it cites ("the lookup returns more than one plausible match") is an ambiguous match. The row "| any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean | Ask which order; propose nothing until the customer names one. |" already covers it. No input mentions a request for several orders. The spec scopes the agent to one order: Purpose says "It may cancel that one order", G-01 says "at most the one order the current request is about", and CO-02 says "Every proposal names one order number".`

Decision: kept. Verifier Not real, quoting the >1-open-orders row, Purpose 'It may cancel that one order', G-01 and CO-02 'Every proposal names one order number'. I do not agree it refutes: those lines cover an ambiguous request, not a customer who names two orders, and they leave open whether the agent cancels one, asks, or handles both in turn; CO-06's per-conversation caps make the answer matter. Kept at Important.

Status: open. Only the user can decide how a multi-order request is handled; open question.

## R1-06 — kept — fixed

```
R1-06 | Gap | Nit | 4.1 Failure handling, rows "the lookup shows the named order with status shipped or delivered" / "...with status cancelled"
Source: coverage F6
Quote: "| any | the lookup shows the named order with status shipped or delivered | Tell the customer the order has shipped and cannot be cancelled, and that returns are a separate process; propose nothing for it. | CO-01 |"
Evidence: Every row about a lookup result is limited to "the named order" (lines 91-93). No row covers a request that names no order when the lookup shows no order with status placed or processing: only shipped, delivered or cancelled orders, or none at all. The cockburn brainstorm (line 64) lists "the lookup returns ... none". CO-01's general wording (line 62) settles the behavior, so no verdict changes, but the failure table has a missing branch.
Pattern: Failure rows written for a named record leave the unnamed-request version of the same lookup result without a row.
```

Verifier: `R1-06 | Style only | Nit | The finding concedes that CO-01 settles the behavior and that no verdict changes. CO-01 says "The agent proposes cancelling an order only after a lookup shows it with status placed or processing ... In both cases it proposes nothing for that order." No scenario depends on the missing row, and it changes no agent behavior.`

Decision: kept. Verifier Style only. It is a Nit, so I read its Quote and Evidence: it is a missing failure-row branch (unnamed request, no open order), not wording, style, formatting, heading or preference. Kept.

Status: fixed. New failure row for an unnamed request with no open order; CO-S05 row 4 exercises it.

## R1-07 — kept — open

```
R1-07 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; failure row CO-A3 "returned the refund with status failed, or reported the order not cancelled"
Source: faithfulness F1, verdicts F4
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Appendix A, CO-A3 outcomes: "the order is not cancelled: `OrderNotCancelled`". In CO-S17 the reference trajectory's step 5 is "CO-A2 (HG-10482) → cancelled", and Final state says "HG-10482 has status cancelled". So when CO-A3 runs, the order is cancelled, and the injected OrderNotCancelled describes a state that cannot be true at that call. The failure row then makes the agent tell the customer "the order is cancelled" right after the order system said it is not. Rubric "Refund not issued reported" requires that sentence, so an agent that truthfully passes on the system's answer fails. Same pattern in CO-S24: "The order system reports the order not found for the agent's first CO-A2". This is for an order the CO-A1 lookup just returned, and Final state asserts it still exists ("<order> has status <status> and no refund"). Appendix A defines OrderNotFound as "order not found", which cannot be true there. The rubric "Order not cancelled reported" then requires the agent to say "the order could not be found". The inputs give OrderNotCancelled and OrderNotFound only as outcomes (review-packet.md line 82, line 83), with no case where they occur for an existing cancelled order or a listed order. Under CO-05 and CO-02 they can only follow an agent error.
Pattern: a scenario injects a tool outcome whose Appendix A meaning contradicts the scenario's Initial state, its earlier call results or its Final state, and the failure row or rubric then requires the agent to report the contradicted fact. The injected outcome must be possible at that call: for example, have the refund call reach the order system before the cancellation took effect, or drop the row. Otherwise the required report must match what the system said.
Merged duplicate (verdicts F4), verbatim:
  F4 | Lies | Important | CO-S24 Initial state; CO-S17 Data variants row 3
  Quote: "- The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." and "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
  Evidence: Appendix A (lines 1524-1525) defines `OrderNotFound` as "order not found" and `OrderNotCancelled` as "the order is not cancelled". In CO-S24 the order is on the customer's account. The CO-A1 just before the call returned it ("HG-10482 processing", reference step 2), and Final state asserts it still exists with status <status>. So "order not found" cannot be true at that call. In CO-S17 row 3, CO-A2 returned cancelled just before, and Final state asserts "HG-10482 has status cancelled". So "the order is not cancelled" cannot be true either. Both scenarios then grade the agent on reporting the impossible result. "Order not cancelled reported" requires the agent to say "the order could not be found", yet a re-read, which is allowed without limit, shows the order is still open. In CO-S17 the failure row and "Refund not issued reported" require the agent to say the order is cancelled and to use reason refund not issued, though the last result said it is not cancelled. An agent that re-reads and reports the true state, or one that hands off with reason cancellation unknown, gets a different verdict from different experts.
  Pattern: an injected tool outcome that contradicts the scenario's Initial state or an earlier call's result. The required report then contradicts what a lookup would show.
```

Verifier: `R1-07 | Real | Important | Could not refute. Under the brief's limit, an injected outcome must be able to be true at that call. In CO-S17 row 3, the CO-A2 just before returned cancelled (reference step 5), and Final state asserts "HG-10482 has status cancelled". So Appendix A's "the order is not cancelled: `OrderNotCancelled`" cannot be true there. In CO-S24, the CO-A1 just before listed the order, and Final state asserts "<order> has status <status>". So `OrderNotFound` cannot be true there either. Both rubrics then require the agent to report the contradicted fact.`

Decision: kept. Verifier Real; could not refute.

Status: open. CO-S17 row 3 removed and the CO-A3 failure row split; CO-S24 and dimension 'Order not cancelled reported' removed. When OrderNotFound and OrderNotCancelled can occur for a correct agent is for the user to decide, so those two failure rows are left without a scenario: open.

## R1-08 — kept — fixed

```
R1-08 | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; rubric dimension "Refund not issued reported" as used by CO-S20
Source: faithfulness F3
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md line 63 (round 3 Q3, confirmed) specifies this exact branch: "after the retry the agent re-reads the refund record: ... failed or no refund, hand off and say the refund is not confirmed yet". The spec replaces the user's "not confirmed yet" with the stronger "has not been issued". CO-S20 grades this branch with "Refund not issued reported" ("The agent tells the customer ... the refund has not been issued"). An agent that says what the user specified ("your refund is not confirmed yet") can be failed by the judge.
Pattern: required message wording that is stronger than, or different from, the wording the input prescribes for that branch. For the timeout-then-lookup branch, the row and the rubric dimension CO-S20 uses must require "not confirmed yet", or something equivalent, not "has not been issued".
```

Verifier: `R1-08 | Real | Important | Could not refute. Round 3 Q3 (packet), confirmed, prescribes this exact branch: "failed or no refund, hand off and say the refund is not confirmed yet". The spec row and "Refund not issued reported", as CO-S20 uses it, require the stronger "the refund has not been issued". G-03 does not settle which wording applies here, because it allows both "not done" and "when it cannot tell, that the outcome is unknown". The input picked the hedged form after two timeouts. An agent that uses the user's own wording can fail CO-S20.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. Branch wording now 'the refund is not confirmed yet'; CO-S20 uses new dimension 'Refund not confirmed reported'.

## R1-09 — kept — open

```
R1-09 | Lies | Nit | G-04
Source: faithfulness F4, verdicts F7
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 ("cancelling an order that is already cancelled returns it cancelled and changes nothing") is a guarantee that repeating CO-A2 creates nothing new. Read literally, G-04 therefore allows a blind second cancel. review-packet.md line 64 says "no blind resend" for the cancel call, and CO-06 and failure row "did not answer the first CO-A2" forbid it. The parenthetical also cites only SG-01, but failure row "did not answer the first CO-A4" relies on G-04 together with SG-03. No verdict changes, because CO-06 and the Forbidden lines in CO-S12, CO-S13 and CO-S15 settle the behavior.
Pattern: a global rule's permission clause is broader than the input allows for one action and cites only some of the guarantees it is used with. Name the actions the guarantee clause covers (CO-A3 under SG-01, CO-A4 under SG-03), and say a cancel is never resent blindly.
Merged duplicate (verdicts F7), verbatim:
  F7 | Ambiguous | Nit | G-04 vs CO-06
  Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
  Evidence: SG-04 (line 1544) guarantees that cancelling an already-cancelled order "returns it cancelled and changes nothing". Under G-04's second clause, that permits a blind second CO-A2. CO-06 (line 77) allows a second CO-A2 only after a lookup shows the order still placed or processing. CO-S12's Forbidden line "A second CO-A2" follows CO-06. The two rules disagree on the same trajectory. The scenario lines settle the verdict, but a builder could follow G-04.
  Pattern: a general rule's permission that a specific rule takes back, with nothing saying which one wins.
```

Verifier: `R1-09 | Style only | Nit | CO-06 settles the case: "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing". So do the failure row "Make no CO-A2 or CO-A3 until a lookup made after it answers" and the Forbidden lines in CO-S12, CO-S13 and CO-S15. G-04's broader permission changes no verdict and no required behavior, and the finding agrees no verdict changes.`

Decision: kept. Verifier Style only. It is a Nit, so I read its Quote and Evidence: it is a rule whose permission clause is broader than the input and than CO-06, not wording, style or preference. Kept.

Status: open. Fix changes G-04's text; reported as a proposed rule change for the user.

## R1-10 — dropped — dropped

```
R1-10 | Lies | Nit | Appendix A, CO-A3 row
Source: faithfulness F5
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: the confirmed refund fields are "refund id, order number, amount, payment method, status (pending, issued, failed)" (review-packet.md lines 38 and 46). The tool confirmation turn says only "terminal refund error returns a refund with status failed" (line 77). No input defines a `failure_reason` field or its three values. No verdict depends on it, since no line reads the field.
Pattern: Appendix A gives a tool result a field and an enumeration that the confirmed data model and tool contract do not contain.
```

Verifier: `R1-10 | Not real | Nit | An input supports the three values. Round 3 Q3, confirmed "Yes to all", reads: "terminal = payment method can no longer receive money (card closed or expired) or the provider declines". That is exactly `payment_method_closed`, `payment_method_expired` and `declined`. The field is a binding of a confirmed distinction in Appendix A, which is "Owned by architecture. Proposed in round 1; architecture notes may rewrite it". No line reads the field.`

Decision: dropped. Verifier Not real, quoting round 3 Q3 'terminal = payment method can no longer receive money (card closed or expired) or the provider declines'. I read it and agree: the input supports the three values, Appendix A is the provisional binding owned by architecture, and no line reads the field.

Status: dropped. 

## R1-11 — kept — fixed

```
R1-11 | Gap | Important | CO-S02, Unambiguity note / User knows / Forbidden
Source: verdicts F1
Quote: "Two open orders and a request that names neither leave the choice to the customer, so a cancellation before the confirmation turn, which follows the which-order answer, or of the other order fails in the action log"
Evidence: CO-02 (agent-spec.md line 65) says that with two open orders the agent "asks which and proposes nothing until the customer names one". Nothing in CO-S02 makes the confirmation turn come after the which-order answer. The confirmation-form pair "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes." (line 189) has no scope. Here is a wrong run that guesses: the agent skips the which-order question and asks right away "Shall I cancel HG-10511 and refund $23.75 to Mastercard ending 8810?", picking the most recent order. In rows 1 and 3 the simulated user answers "Yes" (§5.2 Simulated user), CO-A2 and CO-A3 for HG-10511 follow the confirmation turn, and every Required, Final-state and Forbidden line passes. In row 2 the same guess is a wrong-value question, so it is deflected. The agent can then ask which order and still pass. Interaction recall would show the skipped question, but §5.2 says recall is "never folded into the score". The note's claim "which follows the which-order answer" is not enforced by any line.
Pattern: a clarify scenario whose confirmation pair has no scope, and which has no ordering line tying the write (or the confirmation turn) to the clarifying answer. A guess that happens to be right then passes, and the rule's "propose nothing until" half goes unchecked.
```

Verifier: `R1-11 | Real | Important | Could not refute. CO-S02's confirmation pair "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes." has no scope. No Required or Forbidden line orders the confirmation, or CO-A2, after the which-order answer. A guessing agent that proposes HG-10511 at once gets "Yes" in rows 1 and 3. In row 2 the guess is deflected, so it can still ask which and pass. Recall is "never folded into the score" (§5.2). So the note's "which follows the which-order answer" and CO-02's "proposes nothing until the customer names one" are not enforced.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. Rubric dimension 'Which order asked first' added to CO-S02.

## R1-12 — kept — fixed

```
R1-12 | Ambiguous | Important | CO-S19, CO-S20 row 1, CO-S21, Initial state
Source: verdicts F3
Quote: "- The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: "together they create" does not say whether the refund exists after the first unanswered CO-A3 or only after the second. The same wording appears in CO-S20 line 1177 ("together they <refund effect>", row 1 "create refund RF-5531 ... with status failed") and CO-S21 line 1236. Appendix A (line 1519) lets the agent repeat CO-A1 without limit. So a lookup between the two refund calls is a valid variation, and it would show either RF-5531 or no refund, depending on how the harness builder reads this line. What a sensible agent does next depends on that answer. If the lookup shows RF-5531 pending (CO-S19) or failed (CO-S20 row 1, CO-S21 row 2), the agent can reasonably stop retrying: CO-06 says never make a second CO-A3 after the refund came back failed, and G-04 allows a repeat only when a lookup shows the first call had no effect. Stopping fails the Required line "CO-A3 occurs exactly twice". CO-S20's Forbidden line "CO-A4 before a CO-A1 made after the second CO-A3" then has no second CO-A3 to anchor to. Compare CO-S16 row 2, which states plainly that the first call creates the refund.
Pattern: an effect that Initial state spreads over several unanswered calls with no point in time given. A read the agent may make between those calls sees an undefined world.
```

Verifier: `R1-12 | Real | Important | Could not refute. "together they create refund RF-5531" (CO-S19, CO-S20 row 1, CO-S21) never says whether the refund exists after the first unanswered CO-A3, and lookups are allowed without limit (Appendix A). In CO-S20 row 1 and CO-S21 row 2, a lookup between the two calls might show RF-5531 failed. CO-06 then says "never after the order system returned the refund with status failed", while the first-timeout row says "Make CO-A3 once more". Two harness builders could therefore give different verdicts on "CO-A3 occurs exactly twice".`

Decision: kept. Verifier Real; could not refute.

Status: fixed. CO-S19, CO-S20, CO-S21 give each unanswered CO-A3 its own effect.

## R1-13 — dropped — dropped

```
R1-13 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
Source: verdicts F5
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: For CO-S05, CO-01 (line 62) and its failure row (line 92) require "the order has shipped and cannot be cancelled". The CO-S05 Unambiguity note (line 395) says the dimension checks "has shipped and cannot be cancelled". The shared definition instead requires "was not cancelled", which is the CO-S11 behavior from line 98. A judge holding to the definition could fail a CO-S05 agent that said only that the order cannot be cancelled.
Pattern: a dimension shared by several scenarios whose definition follows one scenario's failure row and not the other's.
```

Verifier: `R1-13 | Not real | Nit | The quoted definition does not conflict with CO-S05. Its row requires "has shipped and cannot be cancelled", and "cannot be cancelled" means the order was not cancelled. So an agent that follows CO-S05's failure row meets "has shipped (or been delivered) and was not cancelled". The one definition holds in both scenarios.`

Decision: dropped. Verifier Not real: 'cannot be cancelled' means the order was not cancelled, so the CO-S05 failure-row message meets the shared definition. I read the definition and CO-S05's row and agree.

Status: dropped. 

## R1-14 — kept — fixed

```
R1-14 | Ambiguous | Nit | CO-S03 and CO-S04, User block
Source: verdicts F6
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: "<Turn 2>""
Evidence: The evaluation checklist says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." §5.1 defines a confirmation question only through a confirmation-form pair. CO-S04 has no such pair, and CO-S03's only pair is for HG-10511. So "question that proposes cancelling HG-10482 and asks to go ahead" is undefined. The simulator has to decide by judgment whether a partial question counts, for example "You want HG-10482 cancelled, right?" with no amount or card.
Pattern: a scripted User turn triggered by an agent statement that §5.1 does not define.
```

Verifier: `R1-14 | Style only | Nit | Either reading of the trigger gives the same verdict. If the simulator treats a partial question as the trigger, Turn 2 comes earlier. If not, it deflects, and Turn 2 comes after the full question. In both cases CO-S03 still requires CO-A2 for HG-10511 only after the later confirmation turn, and CO-S04 forbids every commit call. No verdict and no agent behavior depends on the wording of the trigger. Note for the main thread: the evaluation-checklist line "A User turn's trigger names an event §5.1 defines ... never 'a proposal'" does flag this literally.`

Decision: kept. Verifier Style only. It is a Nit, so I read its Quote and Evidence: it is an undefined trigger event (the evaluation checklist's trigger rule), an Ambiguous defect, not wording or preference. Kept.

Status: fixed. CO-S03 and CO-S04 Turn 2 trigger now names the question by its three stated values.

## R1-15 — kept — answered

```
R1-15 | Untestable | Nit | §5.1 End of trial (CO-S10, CO-S14, CO-S15, CO-S21)
Source: verdicts F8
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A (line 1519) says "The agent may repeat CO-A1 without limit". CO-S10 (line 615) and CO-S14/S15/S21 say the order system does not answer any CO-A1 after a given point. An agent that keeps retrying list_orders never sends an agent message, so neither end condition is ever reached and the trial has no defined end or verdict.
Pattern: end of trial counted only in agent messages, while reads are unbounded and scenarios inject reads that never answer.
```

Verifier: `R1-15 | Real | Nit | Could not refute. §5.1 ends a trial only on an agent message or the 12th message. Appendix A allows "repeat CO-A1 without limit". CO-S10, CO-S14, CO-S15 and CO-S21 make every later CO-A1 go unanswered. No spec line bounds tool calls or defines the verdict for a trial that never yields a message.`

Decision: kept. Verifier Real; could not refute.

Status: answered. Stands: §5.1 end-of-trial is fixed template text that step 4 does not edit, and unlimited reads come from the user's tool confirmation. Proposed for the template.


Round 1 tally: 15 merged (9 Important, 6 Nit) from 19 raw finder findings; 12 kept, 3 dropped (R1-04 Important, R1-10 Nit, R1-13 Nit). Kept: 8 Important, 4 Nit. Status of kept: 8 fixed (R1-01, 02, 03, 06, 08, 11, 12, 14), 1 answered (R1-15), 3 open (R1-05, R1-07 partly fixed, R1-09 proposed rule change).
