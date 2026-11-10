# Round 2 merged findings

9 findings: 4 Important, 5 Nit. (11 raw: faithfulness 4, verdicts 4, coverage 3.) 8 kept, 1 dropped.

Severity as the finders gave it; status is fixed / answered / open / dropped / Pre-existing (none Pre-existing: whole-spec scope). Verifier verdicts are from the one adversarial verifier; Nits went straight to 4.5 unverified, as the skill states.

## N1 — DROPPED — dropped

Severity: finder Important; final Important. Sources: faithfulness F1.

Verifier: N1 | Not real | Important | G-03 'Otherwise it tells the customer the action was not done' requires saying no refund was made in CO-S14/CO-S15 (no CO-A3); §2 'wants to be told truthfully whether the order was cancelled' supports 'the order is cancelled' in CO-S19, where CO-A2 returned cancelled; the reference trajectories match the rubrics

Decision / fix: Dropped. I read G-03 and §2 and agree: G-03 obliges the agent to say the refund was not done when no refund call was made, and the §2 interest supports stating the cancellation in CO-S19, so neither clause is unsupported.

Finder text (faithfulness F1), verbatim:
```
F1 | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported" (CO-S14, CO-S15) and "Refund status reported" (CO-S19)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, ..." and "| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it. |"
Evidence: Each of these rubrics requires the agent to say something that neither the failure row it grades nor the inputs ask for. An agent that follows the row exactly fails the judge.
- CO-S14 and CO-S15 are graded under the CO-A2 failure rows "did not answer the first CO-A2" (agent-spec.md line 103) and "did not answer the second CO-A2" (line 104). Both rows give the message for a lookup that does not answer as "tell the customer it is not known whether the order was cancelled and store staff will follow up". Neither row mentions the refund. The input, review-packet.md Round 3 Q4 ("Re-read fails, say outcome unknown, issue no refund, hand off"), makes "issue no refund" an action, not something to say. The added clause "that no refund was issued" appears only in the rubric (line 1631) and in the reference steps CO-S14 step 8 (line 879) and CO-S15 step 10 (line 940).
- CO-S19 is graded under the CO-A3 row "did not answer the second CO-A3" (line 108): "If the lookup shows the refund pending or issued, tell the customer that status and the refund id". The input, review-packet.md Round 3 Q3 ("pending or issued, report that status"), and CO-08 (line 83, "the agent tells the customer the refund id") also do not require saying the order is cancelled. The rubric (line 1635) adds "tells the customer the order is cancelled".
Pattern: a rubric dimension requires the agent to say more than the failure row or rule it grades, so an agent that follows the row fails. Every "tells the customer" clause in a dimension should match the "Tell the customer" clause of the failure row or rule it grades, or the row should gain that clause.
```

## N2 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: faithfulness F2, verdicts F4.

Verifier: Nit (not verified)

Decision / fix: Fixed (incomplete fix of M5): CO-S17, CO-S22 and CO-S23 Reference trajectory step 6 now read '→ refund RF-5531, failed.'. The cause stays in Initial state as a world fact.

Finder text (faithfulness F2), verbatim:
```
F2 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory step 6 (incomplete fix of M5)
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: The M5 fix (answered.md) removed `failure_reason` from Appendix A. The CO-A3 result is now `{refund_id, amount, payment_method, status}`, and "refund failed: returns the refund with `status: \"failed\"`" (agent-spec.md line 1655). The Refund data model in review-packet.md Round 2 Q3 plus the user's change has no field that carries the cause either. issue_refund therefore cannot return "card closed", yet three reference trajectories still show it as part of the tool result: CO-S17 step 6 (line 1051), CO-S22 step 6 (line 1344) and CO-S23 step 6 (line 1402). In CO-S23 the rows differ only in a cause (closed vs expired, lines 1393-1394) that no tool result exposes.
Pattern: a reference trajectory shows a tool result value that the Appendix A return shape cannot carry. Reference outcomes should name only fields the commit call returns.
```

Finder text (verdicts F4), verbatim:
```
F4 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory (incomplete fix of answered M5)
Quote: "Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: M5 (answered.md) removed `failure_reason` from Appendix A. The CO-A3 commit call now returns only `{refund_id, amount, payment_method, status}` (agent-spec.md line 1655). Three Reference trajectories still show the failure cause as part of the tool result: CO-S17 step 6 (line 1051), CO-S22 step 6 (line 1344) and CO-S23 step 6 (line 1402). The cause also survives in Initial state ("with status failed because the card has been closed", lines 1304 and 1364, and the CO-S17 and CO-S23 data-variant columns). There it is a world fact the agent can never observe, so the CO-S17 rows 1/2 and CO-S23 rows 1/2 differ in nothing the agent or a grader can see. No verdict changes.
Pattern: a tool-result field was removed from Appendix A, but Reference trajectories and Initial-state wording still present it as returned. Remove the field from every place that shows it as part of a tool result.
```

## N3 — KEPT — fixed

Severity: finder Important (verdicts F2); Nit (faithfulness F3); final Important. Sources: verdicts F2, faithfulness F3.

Verifier: N3 | Real | Important | could not refute ('propose' undefined in §5.1; CO-S08 row conflicts with its reference; CO-S03/CO-S04 triggers name 'a question that proposes', against evaluation-checklist.md)

Decision / fix: Kept. The four holding-back dimensions now read 'asks no question that offers to cancel an order' (CO-S05, CO-S06, CO-S07, CO-S10, CO-S11 notes match); CO-S08's failure row now 'propose nothing other than cancelling the whole order', agreeing with CO-03 and the reference; CO-S03/CO-S04 Turn 2 triggers name 'the agent's first question in the confirmation-question form (§5.1) for cancelling HG-10482'. CO-01/CO-02 rule text still says 'proposes nothing' (rule text not edited).

Finder text (verdicts F2), verbatim:
```
F2 | Ambiguous | Important | §5.2 dimensions "Order not found reported", "Already cancelled reported", "Shipped order explained", "Orders unavailable reported"; CO-S07 Unambiguity note; CO-S08 failure row and Reference trajectory; CO-S03 and CO-S04 User Turn 2 trigger
Quote: "| Order not found reported | rubric | The agent tells the customer no order with the number they gave is on their account, never says an order was cancelled or a refund issued, and proposes no cancellation of any order. | CO-S07 |"
Evidence: §5.1 defines "Confirmation question" (line 1588) and "Confirmed proposal" (line 1598). Neither the rules nor §5.1 define what counts as "proposing" a cancellation. The spec uses the word in two incompatible ways:
- In CO-S08, the failure row (line 97) says "propose nothing until the customer asks to cancel the whole order". Yet the Reference trajectory step 3 (line 546) "asks whether they want to cancel the whole order", and User knows (line 518) scripts "Would you like to cancel the whole order HG-10530 instead?". So a question of the form "would you like to cancel X?" is treated as not a proposal.
- The M12 fix adds "proposes no cancellation of any order" to the dimensions at lines 1625, 1626 and 1627 (1630 already had it). The CO-S07 Unambiguity note (line 500) says "proposed no cancellation of any order, HG-10482 included".
In CO-S07 rows 1 and 3 (HG-10428 and HG-10483, near misses of HG-10482), take an agent that says "No order HG-10428 is on your account. Did you mean HG-10482? Would you like to cancel that one?". Read by CO-S08's precedent, it proposes nothing and passes. Read by the CO-S07 note, it proposes HG-10482 and fails. The must-not at line 46, "guess which order the customer means", does not settle whether asking counts as a guess. The same undefined term is the trigger for the scripted turn in CO-S03 (line 252) and CO-S04 (line 313): "in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead". evaluation-checklist.md requires that "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'."
Pattern: a judgment term ("propose", "proposal") decides a rubric verdict or when a User turn is due, but §5.1 never defines it. Define a proposal in §5.1 (for example, any agent question that offers to cancel a named order, with or without the refund terms), make CO-S08's failure row and Reference trajectory agree with that definition, and give the CO-S03 and CO-S04 triggers a §5.1-defined event.
```

Finder text (faithfulness F3), verbatim:
```
F3 | Lies | Nit | CO-S08 Reference trajectory step 3 and User knows; failure row "asked to cancel only some of an order's items"
Quote: "3. Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order."
Evidence: The failure row (agent-spec.md line 97) says: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order." In CO-S08 the customer never asks to cancel the whole order. Even so, the reference trajectory (line 546) and the optional User-knows pair "Q: Would you like to cancel the whole order HG-10530 instead?" (line 518) have the agent offer it first. CO-03 (line 68, "proposes nothing else") seems to allow that offer, which the failure row forbids. The rule and the row disagree, and the reference sides with the rule. No dimension grades the offer ("Whole order only explained", line 1628), so no verdict changes.
Pattern: a reference trajectory does what its failure row says not to do. The row, the rule and the reference should agree on whether the agent may offer the whole-order cancellation.
```

## N4 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: faithfulness F4.

Verifier: Nit (not verified)

Decision / fix: Fixed: CO-S20's final-state line is now 'HG-10482 has exactly <refund count> refunds, and none of them has status pending or issued.' (refund count 1 / 0); CO-S17's whole-line column replaced with its literal line (same pattern).

Finder text (faithfulness F4), verbatim:
```
F4 | Untestable | Nit | CO-S20 Final state assertions / Data variants
Quote: "- <refund final state>"
Evidence: The column holds a whole assertion, and its rows have different shapes: row 1 is "Exactly one refund exists for HG-10482: RF-5531, status failed." and row 2 is "No refund exists for HG-10482." (agent-spec.md lines 1213-1214). SKILL.md step 3.6 (line 114) requires "identical Required events and final-state lines after substituting row values, so the lines differ only in the values their <column> placeholders take". Here the final-state line becomes two different propositions, which one Then step cannot express without rewording. CO-S17 (line 1031) uses the same whole-line column, but both of its rows hold the same line, so only CO-S20 actually diverges.
Pattern: a data-variant column holds a whole assertion line instead of a value, so the rows' final-state lines differ in shape. Either keep the line's shape fixed and vary only values, or split the scenario.
```

## N5 — KEPT — fixed

Severity: finder Important; final Important. Sources: verdicts F1.

Verifier: N5 | Real | Important | could not refute (the CO-S02 confirmation pair is in scope from Turn 1; no Forbidden line or dimension fails a proposal before the which-order answer)

Decision / fix: Kept. New rubric dimension 'Asked which order first' ('Before its first question that offers to cancel an order, the agent asks the customer which of their open orders they mean.') used by CO-S02; the Unambiguity note's false claim removed.

Finder text (verdicts F1), verbatim:
```
F1 | Gap | Important | CO-S02, User knows / Forbidden / Unambiguity note (CO-02 "asks which and proposes nothing until the customer names one")
Quote: "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes."
Evidence: CO-02 (agent-spec.md line 65) and the failure row at line 93 say that with two open orders and no order named, the agent must "Ask which order; propose nothing until the customer names one." In CO-S02 the confirmation pair (line 193) has no scope marker, so it is in scope from Turn 1. No Forbidden line or dimension checks that the agent asked which order before proposing. Plausible wrong run (a guessed value): after the lookup the agent says "Shall I cancel HG-10511 and refund $23.75 to Mastercard ending 8810?" without asking which order. In rows 1 and 3 the simulated user matches the confirmation pair and answers "Yes." The agent then cancels and refunds HG-10511, and every Required event, Final state line, Forbidden line and "Refund id reported" passes. In row 2 that guess has the wrong values and is deflected (§5.1 line 1588). The agent then proposes HG-10482, gets "Yes.", and passes too. So an agent that proposes each open order in turn passes every row. The only signal is interaction recall, which §5.2 line 1616 says is "never folded into the score". The Unambiguity note (line 234) says a cancellation fails if it comes "before the confirmation turn, which follows the which-order answer". Nothing makes the confirmation turn follow the which-order answer, so that claim is false. This is known failure case 1 in the packet (review-packet.md, round 2 Q4: "customer has two open orders and says 'cancel my order'; agent must disambiguate"). A real customer can say yes to the wrong guessed order.
Pattern: the holding-back clause of an "ask before proposing" rule depends on the order of User-knows answers, but the confirmation pair is in scope from the start and no line asserts the order. The §5.2 scope markers, (after Turn n), cover only scripted turns, not User-knows answers. The fix needs a line that fails a proposal made before the which-order answer, for example a rubric dimension "Asked which order before proposing", or a way to scope the confirmation pair to after the which-order answer.
```

## N6 — KEPT — open

Severity: finder Nit; final Nit. Sources: verdicts F3.

Verifier: Nit (not verified)

Decision / fix: Stands: the fix ('when no confirmation turn occurs, every action is before it') belongs in §5.1 fixed text, which step 4 never edits. Open; proposed as a template line.

Finder text (verdicts F3), verbatim:
```
F3 | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden; §5.1 Turn anchors
Quote: "CO-A2 before the user's confirmation turn."
Evidence: §5.1 (line 1586) defines "the user's confirmation turn" and picks the first when there are several. It does not say how a line anchored on that turn is read in a trial that has none, for example when the agent cancels without ever asking a full-form confirmation question, or asks only a partial one that the simulated user deflects. One reader takes the Forbidden line as vacuously not violated, since nothing comes before a turn that does not exist. Another takes every CO-A2 as coming before it. Instances: line 148 (CO-S01), line 208 (CO-S02), line 272 (CO-S03, "CO-A2 for HG-10511 before the user's confirmation turn"), line 585 (CO-S09). The scenario verdict does not change, because the Required line "CO-A2 occurs exactly once … after the user's confirmation turn" fails either way. The two readings do change the trial score (0 under §5.2 "Any Forbidden event scores the trial 0", partial credit otherwise). They also change the Forbidden pass^k reported for the authorization guardrail, which could show clean for an agent that cancelled without any confirmation.
Pattern: a Forbidden line is anchored on a labeled turn that may not occur in a trial, and the spec does not say how to read it then. State in §5.1 that when no confirmation turn occurs, every action is before it.
```

## N7 — KEPT — fixed

Severity: finder Important; final Important. Sources: coverage F1.

Verifier: N7 | Real | Important | could not refute (no scenario for a cancelled order whose refund is failed or null; CO-07 pulls the other way)

Decision / fix: Kept. Following the confirmed input 'An already cancelled order: the agent reports that and changes nothing', the cancelled failure row now adds 'make no CO-A3 and no CO-A4'; CO-S06 gains column refund status (row 1 issued, row 2 failed) and 'Already cancelled reported' checks no refund status other than the lookup's is stated. Whether a failed or missing refund on an already-cancelled order should go to store staff, and the no-refund case, left as an open question.

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | CO-01 / CO-07, Failure handling row "...with status cancelled"; CO-S06
Quote: "| any | the lookup shows the order the customer asked about, or their only order when they named none, with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |"
Evidence: The cancelled branch never looks at the order's refund, and the only scenario for it (CO-S06, line 412: "Exactly one refund exists for <order>: <existing refund>, ... status issued") has an issued refund. The inputs say a cancelled order can have a failed refund or no refund at all. list_orders "returns each order with its refund or null" (review-packet.md, tool confirmation turn; Appendix A line 1653 "`refund` is `{...}` or `null`"), and "list_orders includes cancelled orders" (user's change 4). Refund status includes failed (round 2, Q3 answer). The spec's own exits leave orders in exactly this state: CO-S17 (line 1042, refund failed), CO-S18 (line 1086, "cancelled and no refund"), CO-S20 (lines 1213-1214) and CO-S23 (line 1382, where the customer is told to contact support). The trigger (line 57) includes "to get their money back for an order", so a customer who comes back with "I still haven't got my refund for HG-10482" lands on this branch. For that case, two spec lines give different verdicts. CO-07 (line 80): "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4". CO-05 (line 73) allows CO-A3 "for an order ... a lookup shows cancelled". But CO-01 (line 62) and the packet's shared-understanding item ("An already cancelled order: the agent reports that and changes nothing") call for no action. No failure row or scenario settles whether the agent hands off, refunds or does nothing, or what it tells the customer about the refund.
Pattern: A failure row branches on a lookup's order status but ignores the refund record the same lookup returns. Split the cancelled branch by refund state (pending or issued, failed, none) and give each branch that changes the outcome its own scenario.
```

## N8 — KEPT — open

Severity: finder Nit; final Nit. Sources: coverage F2.

Verifier: Nit (not verified)

Decision / fix: Stands: no input says what the agent tells a customer who names no order and has no orders, or several orders none open; only the user can decide (open question).

Finder text (coverage F2), verbatim:
```
F2 | Gap | Nit | CO-01 / CO-02, Failure handling rows for an unnamed request (lines 93-96)
Quote: "| any | the lookup shows the order the customer asked about, or their only order when they named none, with status shipped or delivered | Tell the customer the order has shipped and cannot be cancelled, and that returns are a separate process; propose nothing for it. | CO-01 |"
Evidence: The M9 fix covers an unnamed request only in two cases: the customer has exactly one order (lines 95-96), or more than one order is placed or processing (line 93). Two results of the lookup still have no row. First, the customer names no order and has no orders, so list_orders returns an empty list. CO-02's not-on-the-account clause (line 65) covers only a number the customer named. Second, the customer names no order and has two or more orders, none of them placed or processing (for example one delivered and one cancelled), so "their only order" does not apply. The brainstorm list in cockburn-checklist.md names this ("the lookup returns more than one plausible match, or none"), and so does the line "A failure row that branches on a lookup covers every result of the lookup: nothing found, ...". It is Nit because no write is possible in either case; only what the agent says is undefined.
Pattern: The lookup branches for an unnamed request handle "exactly one order" and "several open orders" but not "no orders" or "several orders, none open". Every result of the lookup needs a row.
```

## N9 — KEPT — open

Severity: finder Nit; final Nit. Sources: coverage F3.

Verifier: Nit (not verified)

Decision / fix: Stands: a refund returned with a different amount or payment method is checklist-derived and named by no input; only the user can decide the handling (open question).

Finder text (coverage F3), verbatim:
```
F3 | Gap | Nit | CO-A3 Failure handling; CO-03 / CO-08
Quote: "absent"
Evidence: issue_refund returns `{refund_id, amount, payment_method, status}` (Appendix A, line 1655), and the agent already knows the order's total_paid and payment_method from CO-A1 (line 1653). So the agent can see when the order system returns a refund whose amount is not the total paid, or whose payment method is not the order's. That is the brainstorm item "the supporting actor answers wrongly" (cockburn-checklist.md, Failure handling). Harbor Goods wants "no refund other than the order's total paid to the order's payment method" (§2, line 11), and CO-08 (line 83) requires that amount and payment method. No failure row covers a mismatched refund. G-03 only asks whether the status was shown, so it would let the agent report such a refund as pending. CO-07 triggers only when the refund is not shown pending or issued, so no handoff happens either. It is Nit because the inputs never name this failure; it comes only from the checklist.
Pattern: A detectable failure from the use-case checklist's brainstorm list, here a supporting actor that answers wrongly, has no failure row. Add a row (or record an open question) for a commit result that contradicts a value the agent read earlier.
```
