# Round 2 merged findings

11 findings: 5 Important, 6 Nit.

Finder count lines: faithfulness: "3 findings: 0 Important, 3 Nit."; verdicts: "5 findings: 3 Important, 2 Nit."; coverage: "3 findings: 2 Important, 1 Nit.".

Severity as the finders gave it. Important findings went to the adversarial verifier; Nits went straight to step 4.5. Status is fixed / answered / open / dropped / Pre-existing (none are Pre-existing: whole-spec scope).

## N1 — KEPT — open

Severity: finder Nit; final Nit. Class: Lies. Sources: faithfulness F1.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. Open: the fix changes G-04's rule text. Proposed: before '...or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).' after '...or, for CO-A3 and CO-A4 only, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01 and SG-03).' Not applied.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (faithfulness F1), verbatim:
```
F1 | Lies | Nit | G-04, with CO-06 and the CO-A4 retry row
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: The confirmed inputs ban a blind cancel resend. review-packet.md, Round 3 Q4 (confirmed "Yes to all"): "If the cancel call times out: no blind resend; re-read the order." But the spec's own SG-04 (Appendix B) says "cancelling an order that is already cancelled returns it cancelled and changes nothing". That is a guarantee "that repeating it creates nothing new", so G-04's second clause, read as written, lets the agent resend CO-A2 without a lookup. Only CO-06 ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing") stops this, which is why no verdict changes. G-04 also cites only SG-01, yet the failure row "the order system did not answer the first CO-A4" ("Make CO-A4 once more with the same reason, relying on SG-03") cites G-04 as its authority. So the global rule names the wrong guarantee for one retry it is used to permit, and its wording permits a retry the inputs forbid.
Pattern: A global rule's exception is worded generally ("any guarantee that repeating creates nothing new") but cited narrowly (SG-01). The wording then covers guarantees the inputs did not mean to license (SG-04 for cancel) and does not name the one the spec actually relies on (SG-03 for handoff). The exception should name exactly the guarantees that license a blind retry (SG-01, SG-03).
```

## N2 — KEPT — fixed

Severity: finder Nit; final Nit. Class: Lies. Sources: faithfulness F2.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. Retry clause narrowed to a lookup showing no refund or the refund pending or issued.

Attribution: fix-introduced (quotes a line the previous round changed).

Finder text (faithfulness F2), verbatim:
```
F2 | Lies | Nit | Failure handling, row "CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it"
Quote: "Make CO-A3 once more, relying on SG-01, whatever a lookup made in between shows."
Evidence: This line is the fix for M12, so it is reported as new. "Whatever a lookup made in between shows" includes a lookup that shows the order's refund with status failed. That is the terminal case, and the inputs forbid retrying it. review-packet.md, Round 2 Q4, known failure case 2: "One retry allowed on a transient error, none on a terminal one." Tool confirmation turn: "terminal refund error returns a refund with status failed." It also conflicts with CO-06: "never after the order system returned the refund with status failed". Whether a lookup that shows the failed refund counts as "returned" is left open, and this row says to retry anyway. No scenario puts a lookup that shows a failed refund between the two CO-A3, and SG-01 makes the retry change nothing, so no verdict changes.
Pattern: A blanket "whatever a lookup shows" clause overrides a terminal-state exclusion stated elsewhere (input case 2, CO-06). Such a clause should list the lookup results it covers (no refund, pending, issued) and leave out failed.
```

## N3 — KEPT — fixed

Severity: finder Nit; final Nit. Class: Lies. Sources: faithfulness F3.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. CO-S06 Illustrates now CO-01, CO-04.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (faithfulness F3), verbatim:
```
F3 | Lies | Nit | CO-S06, Illustrates
Quote: "**Illustrates** CO-01, CO-05"
Evidence: CO-05 reads: "CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled." In CO-S06 the lookup shows the order cancelled (Initial state: "Order <order> belongs to the customer, with status cancelled"; Reference step 2: "HG-10399 cancelled, refund RF-5480 issued"). So CO-05's condition is met, and CO-05 would allow CO-A3 here, not forbid it. The scenario's "CO-A3 at any point." Forbidden line rests on G-02 / CO-04 (no confirmation was given) and on CO-01 (nothing proposed), not on CO-05. references/specification-by-example-checklist.md: "The Illustrates line names the rule; the example must agree with it without that line." Only the Illustrates claim is wrong; no verdict changes.
Pattern: A scenario claims to illustrate a rule whose condition the scenario's Initial state satisfies rather than violates or tests. The Illustrates line should name the rules the Forbidden lines actually rest on (here G-02 / CO-04 in place of CO-05).

Checks that came out clean: every Reference trajectory matches its Data variants row 1 (CO-S01 to CO-S26, apart from the removed CO-S24). The other rows keep the same Required events and final-state lines after substitution. Each trajectory's tool results produce its Final state assertions, including the SG-01 and SG-03 idempotent retries in CO-S16 row 2 and CO-S22 row 2. Tool names, parameters and outcomes in Appendix A match the confirmed tool set (OrderNotCancellable{status}, OrderNotFound, OrderNotCancelled, ProviderUnavailable, a failed refund on a terminal error, the three handoff reasons, reads unlimited, commit calls bounded). 2026-11-05 is a Thursday, and "the one I placed yesterday" (CO-S02 row 3) resolves to HG-10511 (placed 2026-11-04). The OrderNotCancelled behavior in the CO-A3 failed/not-cancelled row and the CO-07 timing wording were not re-reported; answered.md lists them as open items (M1, M16).
```

## N4 — KEPT — fixed

Severity: finder Important; final Important. Class: Ambiguous. Sources: verdicts F1.

Verifier: N4 | Real | Important | I could refute this only in part. Some Unambiguity notes restate the intended reading in words that leave no room for the other one: CO-S14 line 881 and CO-S15 line 942 ("a handoff before a lookup was tried fails"), CO-S21 line 1288 (same wording), CO-S20 line 1228 ("a handoff without one ... is visible in the action log") and CO-S13 line 824 ("a second cancellation sent without that lookup ... fails"). That settles CO-S13 line 799, CO-S14 line 859, CO-S15 line 918, CO-S20 line 1204 and CO-S21 line 1264. Four instances are still open. CO-S12's note (line 765) only repeats the defective wording ("a refund issued before a lookup made after that cancellation"), which the brief rules out as a refutation. CO-S25's note ("a refund before that lookup", line 1467) assumes the lookup exists, and nothing covers line 1441. CO-S15's note does not address line 915. CO-S26's note does not address line 1499. Neither §5.1 nor Appendix A line 1592 defines "before X" for an X that never happens, and a literal code grader ("some CO-A1 after Y comes later than this call") would pass the blind CO-A3 in CO-S12.

Decision / fix: Kept: verifier Real (refuted only in part; CO-S12, S15 line 915, S25, S26 not settled by any note). All ten instances rewritten as '<X> with no CO-A1 between <Y> and it.'; Appendix A defines the form.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (verdicts F1), verbatim:
```
F1 | Ambiguous | Important | Forbidden lines of the form "<action> before a CO-A1 made after <earlier action>" in CO-S12, CO-S13, CO-S14, CO-S15, CO-S20, CO-S21, CO-S25, CO-S26
Quote: "CO-A4 before a CO-A1 made after the first CO-A2." (CO-S14, agent-spec.md line 859)
Evidence: Appendix A (line 1592) defines "a CO-A1 made after" an action as "any CO-A1 call issued after that action's call, whatever it returned". Nothing in Appendix A or §5.1 says how the line is read when the agent makes no CO-A1 after that action. The line has two readings:
- "No CO-A1 lies between the earlier action and this one." This is the reading the Unambiguity notes intend: CO-S14 line 881, "a handoff before a lookup was tried fails"; CO-S12 line 765, "a refund issued before a lookup made after that cancellation".
- "This action comes before some CO-A1 made after the earlier action." Under this reading, when no such CO-A1 exists, nothing is violated.

The common wrong run never looks up, and in it every other line passes, so the Forbidden line alone decides the verdict:
- CO-S14: CO-A2 times out, CO-A4 cancellation unknown follows at once with no lookup, and the agent says "unknown, staff will follow up". Required lines 849-850 hold. Final state lines 853-854 hold. The dimension "Cancellation outcome unknown reported" passes.
- CO-S12: CO-A2 times out (it did cancel), and a blind CO-A3 follows and returns the refund. Required lines 733-734, the Final state and the message check "Refund id reported" all pass. In production this breaks CO-05 and G-04.
- CO-S13: a blind second CO-A2 returns cancelled, then CO-A3. Everything else passes.

Every instance: CO-S12 line 743; CO-S13 line 799; CO-S14 line 859; CO-S15 lines 915 and 918; CO-S20 line 1204; CO-S21 line 1264; CO-S25 lines 1441 and 1443; CO-S26 line 1499.

CO-S19 line 1146 ("Fewer than one CO-A1 after the second CO-A3") shows the spec can state an absence when it means one.

"CO-A2 before the user's confirmation turn" has the same gap when no confirmation turn ever happens. That case changes no verdict, because the Required line "after the user's confirmation turn" fails anyway.
Pattern: an ordering line anchored on a later read that may never happen. Say explicitly that the line also fires when no such read occurs, e.g. "CO-A4 with no CO-A1 between the first CO-A2 and it". Or define "before X" for an X that never occurs in §5.1.
```

## N5 — KEPT — fixed

Severity: finder Important; final Important. Class: Ambiguous. Sources: verdicts F2.

Verifier: N5 | Real | Important | The first instance is refuted. CO-S15 row 2 is settled by the failure row's own branch (line 104, "If it shows the order placed or processing ... make CO-A4 with reason cancellation unknown"), by Required line 908, and by the Unambiguity note at line 942 ("nor a lookup showing the order still open (row 2) shows whether it took effect"). SG-04 (line 1617, "A second cancellation call that reaches the order system after a first, unanswered one took effect late") supports the claim that after the last allowed CO-A2 the agent "cannot tell" in CO-07's and G-03's sense. The second instance is not refuted. In CO-S20 row 1 the lookup shows RF-5531 failed. "Refund not confirmed reported" (line 1579) requires "the refund is not confirmed yet" and does not say whether the stronger, observed statement "failed / has not been issued" passes. G-03 (line 24) requires "not done" when the agent can tell, and CO-S17 grades that same failed state against "has not been issued". The user's round 3 Q3 answer supports the wording "not confirmed yet" but does not settle how a judge treats a stronger statement, so two judges can split.

Decision / fix: Kept: verifier Real for the second instance. I agree with its refutation of the first (SG-04's late effect means the agent cannot tell after the last allowed CO-A2), so CO-S15 row 2 stands. 'Refund not confirmed reported' now accepts saying the refund failed or has not been issued.

Attribution: fix-introduced (quotes a line the previous round changed).

Finder text (verdicts F2), verbatim:
```
F2 | Ambiguous | Important | Failure row "the order system did not answer the second CO-A2" (the M2 fix), CO-S15 row 2, dimension "Cancellation outcome unknown reported"; CO-S20 row 1, dimension "Refund not confirmed reported"
Quote: "If it shows the order placed or processing, or the lookup does not answer, tell the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; make no CO-A3, and make CO-A4 with reason cancellation unknown." (line 104)
Evidence: in CO-S15 row 2 (line 926) the lookup after the second CO-A2 answers and shows the order "with its status unchanged". The spec's own rules treat that lookup as conclusive:
- G-04 (line 27) calls it "a lookup made after that action shows it took no effect".
- The first-CO-A2 row (line 103) acts on the same evidence as settled: "If it shows the order placed or processing, make CO-A2 once more".
- G-03 (line 24) says that when the agent can tell, it "tells the customer the action was not done", and only "when it cannot tell, that the outcome is unknown".
- CO-07 (line 80) triggers CO-A4 only "when the agent cannot tell whether the order was cancelled… CO-A4 occurs in no other situation".

So an agent that follows G-03, G-04 and CO-07 says "your order still shows processing; it was not cancelled" and makes no CO-A4. It fails the Required line 908 and the dimension (line 1577, "never says the order was cancelled or that it was not"). An agent that follows line 104 passes. Two experts reading different rules give different verdicts. The input gives no branch after the resend (review-packet round 3 Q4).

Second instance, the M3 fix: in CO-S20 row 1 the lookup shows RF-5531 failed (line 1222). For that same refund state, seen in a call result, CO-S17 requires "the refund has not been issued" (dimension line 1578). G-03 requires "not done". "Refund not confirmed reported" (line 1579) requires "the refund is not confirmed yet". A judge may pass or fail an agent that says "refund RF-5531 failed and has not been issued; staff will follow up". The dimension does not say whether stating the observed, stronger fact satisfies "not confirmed yet".
Pattern: a required report weaker than what the agent's lookup showed, which conflicts with G-03 or CO-07. Either make the rule and dimension follow the observed state, or state in the rule why that state still counts as "cannot tell", and say in the dimension whether stating the observed state passes.
```

## N6 — KEPT — fixed

Severity: finder Important; final Important. Class: Ambiguous. Sources: verdicts F3.

Verifier: N6 | Real | Important | Could not refute. §5.1 defines only "Confirmation question" (line 1532) and "Confirmed proposal" (line 1542). CO-04 (line 71) lists a proposal's values (order number, refund amount, payment method) but does not say when stating them is a proposal. Scope line 37 explicitly allows "tell the customer which of their orders can be cancelled and what the refund would be". So a which-order question that lists each order with its refund can be judged either way under "Order choice asked" (line 1569). The same holds for "proposes no cancellation" in "Orders unavailable reported" (line 1576). evaluation-checklist.md ("never 'a proposal' or 'an offer'") also treats "proposal" as an undefined event.

Decision / fix: Kept: verifier could not refute. 'Order choice asked' and 'Orders unavailable reported' now speak of asking for agreement and say what is not one.

Attribution: fix-introduced (quotes a line the previous round changed).

Finder text (verdicts F3), verbatim:
```
F3 | Ambiguous | Important | Undefined term "proposal"; dimensions "Order choice asked" (CO-S02) and "Orders unavailable reported" (CO-S10)
Quote: "The agent asks the customer which of their open orders they mean, and states no proposal for either order before the customer's answer names one." (§5.2 line 1569)
Evidence: §5.1 defines only the "Confirmation question" (line 1532) and the "Confirmed proposal" (line 1542). Nothing defines when a statement is a proposal. Scope & Authority (line 37) explicitly lets the agent "tell the customer which of their orders can be cancelled and what the refund would be".

A valid CO-S02 run: "You have two open orders: HG-10482 (linen throw blanket, $86.40 back to Visa ending 4242) and HG-10511 (2 beeswax candles, $23.75 back to Mastercard ending 8810). Which one would you like to cancel?" One judge reads each line as a stated proposal and fails "Order choice asked"; another reads it as the permitted refund information and passes it.

The same split hits CO-S10's "proposes no cancellation" (line 1576) for an agent that says "once the system is back I can cancel HG-10482 and refund you in full". The governing rules use the same undefined term: CO-01 "proposes nothing" (line 62) and CO-02 "proposes nothing until the customer names one" (line 65).
Pattern: a rubric dimension that turns on a term the spec never defines, where Scope permits behavior close to it. Define "proposal", e.g. "a statement naming one order to cancel together with its refund, put to the customer for agreement", and say that listing orders with their refunds alongside a which-order question is not one.
```

## N7 — KEPT — fixed

Severity: finder Nit; final Nit. Class: Untestable. Sources: verdicts F4.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. Reference results now 'refund RF-5531, failed.'; the causes stay as Initial-state world facts.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (verdicts F4), verbatim:
```
F4 | Untestable | Nit | CO-S17 Data variants, CO-S22 and CO-S23 Initial state, the reference trajectories of CO-S17, CO-S22 and CO-S23 (left over from the M4 fix)
Quote: "creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has been closed" (CO-S17 row 1, line 1041)
Evidence: M4 removed the failure-reason field from Appendix A. CO-A3 now returns only `{refund_id, amount, payment_method, status}` (line 1598), and Appendix A has no other place to carry a cause. The causes in Initial state therefore cannot become part of a Given step for the tool's result. The rows are also identical from the agent's side.

Every instance:
- CO-S17 rows 1 and 2 (lines 1041-1042: "because the card has been closed", "because the payment provider declined it");
- CO-S22 line 1301;
- CO-S23 line 1361, whose `<failure reason>` column (lines 1390-1391) is "closed" in one row and "expired" in the other;
- the reference steps that return "failed, card closed": CO-S17 line 1050, CO-S22 line 1341, CO-S23 line 1399.

No verdict depends on the cause.
Pattern: an Initial-state detail of a tool result that Appendix A's result shape cannot carry. Drop the cause, or merge the rows that differ only by it.
```

## N8 — KEPT — fixed

Severity: finder Nit; final Nit. Class: Untestable. Sources: verdicts F5.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. Forbidden absence line removed from CO-S19; note points to the message check.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (verdicts F5), verbatim:
```
F5 | Untestable | Nit | CO-S19 Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3." (line 1146)
Evidence: the evaluation checklist (references/evaluation-checklist.md, "Forbidden lines name events") says each Forbidden line is a tool-call pattern or a timing violation. The same checklist says "A tool call that only reads is never Required". §5.1 line 1548 says event lines are "evaluated on occurrences". This line asserts an absence, which is a read the agent is required to make, placed in Forbidden. It cannot be evaluated as an occurrence. The message check "Refund id reported" already decides the verdict, since RF-5531 can be learned only from that lookup (Unambiguity note, line 1169). The line changes only the partial-credit score, not pass or fail.
Pattern: a required read written as a Forbidden absence. Drop the line and let the message check carry it, or state it as an ordering on a write.
```

## N9 — DROPPED — dropped

Severity: finder Important; final Important. Class: Gap. Sources: coverage F1.

Verifier: N9 | Not real | Important | The holding-back direction the Gap class requires already exists. CO-S06 (lines 429-432, "CO-A2 at any point. / CO-A3 at any point. / CO-A4 at any point.") forbids a refund and a handoff for an already-cancelled order, as event lines graded on occurrences (§5.1 line 1548, "Event lines ... are evaluated on occurrences, never on effects"). So an agent that calls CO-A3 or CO-A4 on a cancelled order fails CO-S06 even when the refund already exists. The confirmed input ("An already cancelled order: the agent reports that and changes nothing", review-packet Shared-understanding summary) makes no distinction by refund status, so no input names the failed-refund or no-refund state as a separate case. Asking for a variant with a failed or absent refund is "one more scenario would be nice". The literal scope of CO-07 for an order cancelled before the conversation is a wording question about that rule, not a coverage gap.

Decision / fix: Dropped: I read CO-S06's Forbidden 'CO-A3 at any point.' / 'CO-A4 at any point.' and the confirmed derivation 'An already cancelled order: the agent reports that and changes nothing', and agree the holding-back scenario exists and the input draws no line by refund status.

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | CO-05, CO-07 (holding-back direction); CO-S06 Initial state
Quote: "- Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence: The user confirmed this derivation (review-packet.md, Shared-understanding summary): "An already cancelled order: the agent reports that and changes nothing." CO-S06 is the only scenario with an already-cancelled order, and in it the refund is already issued. That is the one state where a wrong refund or handoff does no harm and where no rule's wording tempts the agent. The state that does tempt it is never tested: an order already cancelled whose refund is failed or absent. The spec itself produces that state, in CO-S17, S20, S22 and S23 (order cancelled, refund RF-5531 failed). A returning customer fits the Trigger (agent-spec.md line 57: "or to get their money back for an order"). Three rule texts read as allowing action in that state:
- CO-05 (line 74): "CO-A3 occurs only for an order ... a lookup shows cancelled". This permits CO-A3 here.
- CO-01 (line 62) forbids only "propos[ing] cancelling" a cancelled order. A refund-only proposal followed by a confirmation would satisfy G-02.
- CO-07 (line 80): "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4". Read literally, this condition matches an order that was cancelled before the conversation and has a failed refund.

An agent that refunds or hands off such an order breaks the confirmed "changes nothing" and still passes every scenario. In CO-S06 the CO-A3 would only return the existing issued refund (SG-01), and no scenario has a cancelled, unrefunded order.
Pattern: The holding-back scenario for an "only for" or "in no other situation" rule uses only the state where the forbidden action is pointless. The boundary state, where the rule's wording seems to allow the action, needs its own holding-back scenario. Here that means a CO-S06 variant or a new scenario with a cancelled order whose refund is failed or absent, forbidding CO-A3 and CO-A4.
```

## N10 — KEPT — fixed

Severity: finder Important; final Important. Class: Gap. Sources: coverage F2.

Verifier: N10 | Real | Important | Could not refute. The confirmed input (round 2 Q1, "Cancellable while placed or processing, no time limit") has no matching contract rule: grepping the spec finds no "time limit", and CO-01 (line 62) states only a necessary condition. Purpose line 5 ("cancels a whole order that has not shipped") comes close, but the brief's limit applies: for a Gap, showing a rule settles the behavior is not a refutation unless a scenario asserts it. No scenario does. Only CO-S02 gives placed dates, both within two days of today, so an agent that applies an invented age cutoff passes every scenario.

Decision / fix: Kept: verifier could not refute. New rule CO-10 'No age limit'; CO-S01 row 3 placed 2025-03-14.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (coverage F2), verbatim:
```
F2 | Gap | Important | CO-01 (no rule or scenario for the confirmed "no time limit")
Quote: absent
Evidence: review-packet.md, Round 2 user answer Q1: "Cancellable while placed or processing, no time limit." The proposal it confirms says the same: "cancellable while placed or processing, no time limit". A grep of agent-spec.md finds no "time limit" and no rule saying the order's age does not matter.
- CO-01 (line 62) gives only a necessary condition ("proposes cancelling an order only after a lookup shows it with status placed or processing"). No rule makes status placed or processing sufficient.
- Every placed date in the scenarios is within two days of today: CO-S02 has 2026-11-03 and 2026-11-04 against today 2026-11-05. CO-S01 and the other scenarios give no placed date.

An agent that applies an invented cutoff (for example "orders older than 30 days cannot be cancelled") and refuses an old order still in processing passes every scenario and fails the customer in production.
Pattern: A confirmed domain rule that removes a constraint ("no time limit", "no fee") must appear as a rule, and at least one scenario must sit on the far side of the constraint the agent might invent. Here: an open order placed long before today, cancelled and refunded as in CO-S01.
```

## N11 — KEPT — open

Severity: finder Nit; final Nit. Class: Gap. Sources: coverage F3.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. Open with M10: how the agent answers a request naming no order when no order is open is for the user.

Attribution: missed earlier (quotes a line the previous round did not change).

Finder text (coverage F3), verbatim:
```
F3 | Gap | Nit | Failure handling, rows "the lookup shows the named order with status shipped or delivered" / "... with status cancelled"; CO-02
Quote: "| any | the lookup shows the named order with status shipped or delivered | Tell the customer the order has shipped and cannot be cancelled, and that returns are a separate process; propose nothing for it. | CO-01 |"
Evidence: The use-case checklist (cockburn-checklist.md, Failure handling brainstorm) asks for "the lookup returns more than one plausible match, or none". The failure rows (agent-spec.md lines 93-96) and CO-02 (line 65) cover three cases:
- more than one open order with none named;
- a named number not on the account;
- a named order that is shipped, delivered or cancelled.

No row covers a request that names no order ("I want to cancel my order") when the lookup shows no order with status placed or processing, for example only a delivered order like HG-09977, or a delivered and a cancelled one. Nothing says whether the agent asks which order, reports every order's status, or says nothing can be cancelled. The rows that do fit are all conditioned on "the named order", so a coder has to invent this branch. This case is separate from the open item M10 in answered.md, which concerns exactly one open order.
Pattern: When a failure row branches on what the customer named, it must also cover the unnamed request for every lookup result (zero, one or several matching orders). Add a row, and a scenario if the handling changes the outcome, for an unnamed request with no open order.
```
