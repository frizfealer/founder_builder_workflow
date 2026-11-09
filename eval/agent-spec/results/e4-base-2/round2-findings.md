# Round 2 findings

13 merged findings: 9 Important, 4 Nit. Kept 13, dropped 0, Pre-existing 0.

Finder reports verbatim: eval/agent-spec/run-e4-base-2/round2-findings-faithfulness.md, -verdicts.md, -coverage.md. Verifier report verbatim: eval/agent-spec/run-e4-base-2/round2-verifier.md.

## R2-01 (Important; from faithfulness F1, verdicts F2)

[faithfulness F1]
F1 | Lies | Important | CO-S15, Reference trajectory and Forbidden
Quote: "8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created."
Evidence: The failure row for the second unanswered CO-A2 (agent-spec.md line 105) says "Make no further CO-A2, and no CO-A3 until a lookup made after it answers. ... If the lookup does not answer, make no CO-A3, make CO-A4 with reason cancellation unknown". So CO-A4 has to come after a lookup made after the second CO-A2. Round 3 Q4 in review-packet.md says the same: "Re-read fails, say outcome unknown, issue no refund, hand off". CO-S15's Initial state even sets that lookup up ("The order system does not answer any CO-A1 the agent makes after its second CO-A2", line 900). But the reference trajectory goes straight from step 7 (second CO-A2, no answer) to step 8 (CO-A4) with no CO-A1 between them. CO-S15's Forbidden block also has no line like CO-S14's "CO-A4 before a CO-A1 made after the first CO-A2." (line 863), CO-S20's or CO-S21's "CO-A4 before a CO-A1 made after the second CO-A3." As a result, an agent that hands off without re-reading the order passes CO-S15. The R1-01 fix added the re-read branches to the failure row but did not carry them into CO-S15 ("CO-S15 keeps the no-answer branch").
Pattern: When a failure row requires a lookup before a handoff, the reference trajectory must show that lookup, and Forbidden must include "CO-A4 before a CO-A1 made after the <nth> <action>", as CO-S14, CO-S20 and CO-S21 already do. Instances: CO-S15 only.

[verdicts F2]
F2 | Gap | Important | CO-S15, Forbidden and Reference trajectory
Quote: "8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created." (step 8 comes straight after "7. Agent → CO-A2 (HG-10482) → no answer.", and Forbidden lists only "A second CO-A2 before a CO-A1 made after the first CO-A2." / "A third CO-A2." / "CO-A3 at any point." / "A second CO-A4.")
Evidence: The failure row for the second unanswered CO-A2 (line 105) says "Make no further CO-A2, and no CO-A3 until a lookup made after it answers. ... If the lookup does not answer, make no CO-A3, make CO-A4 with reason cancellation unknown". So the handoff must come after a lookup was tried. CO-S15's own Initial state has the line for that lookup ("The order system does not answer any CO-A1 the agent makes after its second CO-A2."). The reference trajectory has no such lookup, and no Forbidden line catches its absence. A wrong run that hands off right after the second timeout, without trying a lookup, passes CO-S15. The sibling scenarios do forbid this: CO-S14 has "CO-A4 before a CO-A1 made after the first CO-A2.", and CO-S20 and CO-S21 have "CO-A4 before a CO-A1 made after the second CO-A3." This is left over from R1-01, which rewrote line 105 into a re-read branch, but CO-S15 kept the old path.
Pattern: when a failure row makes an action wait for a read, the scenario that triggers the row needs a Forbidden "<action> before a CO-A1 made after <call>" line, and its reference trajectory must include that read.

**Decision:** kept. **Verifier:** R2-01 | Real | Important | I could not refute it. The failure row at line 105 ("...no CO-A3 until a lookup made after it answers... If the lookup does not answer, make no CO-A3, make CO-A4 with reason cancellation unknown") requires a lookup to be tried before the handoff. CO-S15's Initial state sets up that lookup at line 900. Yet the reference trajectory goes straight from step 7 ("CO-A2 (HG-10482) → no answer") to step 8 ("CO-A4 ... → task created"). The Forbidden block (lines 919-922) has no "CO-A4 before a CO-A1 made after the second CO-A2", unlike CO-S14 (line 863) and CO-S20/CO-S21 (lines 1207 and 1268). Because CO-S15's lookups never answer, an agent that skips the lookup reaches the same end state, so CO-S15 passes it. CO-S25 catches a "never look up" agent, but only in that scenario. Adding the Forbidden line would change CO-S15's verdict.

**Status:** fixed. Verifier could not refute.

## R2-02 (Important; from faithfulness F2)

[faithfulness F2]
F2 | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; dimension "Refund not issued reported" as used by CO-S20
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Round 3 Q3, which the user confirmed with "Yes to all" (review-packet.md, Round 3), says: "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet". The spec instead requires the stronger claim "the refund has not been issued". Instances:
- the failure row (line 109);
- CO-S20 reference trajectory step 10 ("the refund has not been issued", line 1227);
- CO-S20 Unambiguity note (line 1231);
- the "Refund not issued reported" dimension, whose Used-by list includes CO-S20 (line 1679).
An agent that follows the confirmed policy and says "your refund is not confirmed yet" can be failed by the rubric judge. That wording is correct for case 2 (terminal error, CO-S17/CO-S18: "refund not issued, state known") but not for the case-3 path.
Pattern: Where the inputs say what the agent tells the customer, the failure row, the reference trajectory and the rubric dimension must match that statement. A dimension shared across cases that the inputs word differently needs a separately named dimension for the case-3 path.

**Decision:** kept. **Verifier:** R2-02 | Real | Important | I could not fully refute it; this is the most contestable one. Partial counter: the user's own wording for known case 3 says "re-reads the order and refund records and reports what it finds. Final message must match the final refund status", and for a failed refund or no refund that supports "the refund has not been issued". G-03's "tells the customer the action was not done" supports it too. Still, Round 3 Q3, confirmed with "Yes to all", prescribes a different message for this exact path: "failed or no refund, hand off and say the refund is not confirmed yet". The dimension "Refund not issued reported" (line 1679, used by CO-S20) requires "the refund has not been issued", so a judge can fail an agent that says what Round 3 Q3 prescribes. The spec contradicts one confirmed input, and showing another input supports the line does not remove that.

**Status:** fixed. Verifier could not refute (contestable; Round 3 Q3 prescribes "not confirmed yet").

## R2-03 (Important; from coverage F1)

[coverage F1]
F1 | Gap | Important | CO-01, Failure handling; CO-S06
Quote: "for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order."
Evidence: The packet's tool confirmation turn, change 4, says "list_orders includes cancelled orders". Round 2 Q3 gives refund status values "pending, issued, failed". The spec's own flows leave orders in this state: CO-S17 and CO-S20 end with an order that is cancelled and has a failed refund or no refund, plus a staff task. CO-S23 ends the same way with no task, and the customer is told to contact support. The Trigger (spec line 57) includes "to get their money back for an order". The customer's interest (§2, line 9) is "to be told truthfully ... where the refund stands". Yet the only failure row for a cancelled order (line 97) says "Tell the customer the order is already cancelled; propose nothing for it". The only scenario, CO-S06, has the refund `issued`. No rule, failure row or scenario says what the agent does or says when a cancelled order has a failed refund or no refund and the customer asks for their money. Open questions: may it call CO-A3 again (SG-01 makes that safe), may it hand off, and must it report the refund's status?
Pattern: A state that the spec's own failure paths produce, and that the trigger can reach, has no rule, failure row or scenario.

**Decision:** kept. **Verifier:** R2-03 | Real | Important | Only partly settled. CO-01 (line 62) and the failure row at line 97 ("Tell the customer the order is already cancelled; propose nothing for it") settle that the agent proposes nothing, so through G-02/CO-04 there is no new CO-A3. But CO-07 (line 80) reads "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4", and that can be read as covering a cancelled order whose lookup shows a failed refund or no refund. Nothing decides whether CO-A4 is required or forbidden there, or whether the refund status must be reported (§2's interest is "where the refund stands"). CO-S06 asserts only the case where the refund is issued. Under the brief's rule, being settled by a rule is not a refutation without a scenario that asserts it, and here even the rule conflicts with CO-07.

**Status:** open. Verifier: only partly settled; CO-07 may cover it. Only the user can decide the behavior.

## R2-04 (Important; from coverage F2)

[coverage F2]
F2 | Gap | Important | CO-03, Failure handling row "the customer asked to cancel only some of an order's items"; CO-S08
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence: This row is an "act only when" condition. CO-S08 is the only scenario that triggers it, and it covers only the holding-back side: the User-knows answer is "No, I'll keep it. (optional)". No scenario has the customer accept the whole-order cancellation, so nothing checks the acting side. That side should end with the agent proposing the full proposal and making CO-A2 only after confirmation. That case also tests CO-04: "Would you like to cancel the whole order HG-10530 instead? — Yes" states no refund amount or payment method, so it must not count as confirmation. Nothing catches an agent that cancels on that "yes". The evaluation checklist ("Both directions are covered") requires both sides.
Pattern: An "act only when" clause in a failure row has a holding-back scenario but no acting scenario.

**Decision:** kept. **Verifier:** R2-04 | Real | Important | I could not refute it. Line 98 ("propose nothing until the customer asks to cancel the whole order") is an "act only when" clause. CO-S08 covers only holding back: its User-knows answer is "No, I'll keep it." CO-S01 shows a whole-order cancellation but never after a request to cancel some items. CO-S02 forbids cancelling on a which-order answer, but nothing covers a "yes" to "Would you like to cancel the whole order instead?", which §5.1 does not count as the confirmation question. The evaluation checklist item "Both directions are covered" makes this a Gap by definition.

**Status:** fixed. Verifier could not refute.

## R2-05 (Important; from coverage F3)

[coverage F3]
F3 | Gap | Important | CO-01 / CO-02, Failure handling
Quote: "the lookup shows the named order with status shipped or delivered" and "the lookup shows the named order with status cancelled"
Evidence: Both rows (spec lines 96–97) are keyed to "the named order". The other lookup rows cover these cases:
- no orders at all (line 93, CO-S27);
- several open orders with none named (line 94, CO-S02);
- an unknown number (line 95, CO-S07).
CO-S01 row 4 covers an unnamed request when exactly one order is open. No row or scenario covers an unnamed request ("I want to cancel my order") when the customer has orders but none is placed or processing, for example only delivered or cancelled orders. The brainstorm item "the lookup returns more than one plausible match, or none" in cockburn-checklist.md applies here. Nothing tells the agent which order to report or what to say. An agent that answers "no order is on your account" (false under G-03) or asks which order to cancel would pass every current scenario.
Pattern: Failure rows written for a named order leave the same condition for an unnamed request without a row or scenario.

**Decision:** kept. **Verifier:** R2-05 | Real | Important | I could not refute it. CO-01 is not limited to a named order ("For an order with status shipped or delivered, it tells the customer..."), so a rule settles part of the behavior. But the failure rows at lines 96-97 are keyed to "the named order", and no scenario has an unnamed request with orders on the account but none placed or processing. CO-S01's extra order HG-09977 is delivered, but row 4 there has an open order. The cockburn-checklist items "more than one plausible match, or none" and "A failure row that branches on a lookup covers every result of the lookup" back the finding. A rule that is settled but never asserted by a scenario is not a refutation under the brief.

**Status:** fixed. Verifier could not refute.

## R2-06 (Important; from coverage F4)

[coverage F4]
F4 | Gap | Important | G-01 / CO-02 / CO-06, Failure handling
Quote: absent (no failure row for a request that names more than one order)
Evidence: G-01 says "The agent cancels, refunds and hands off at most the one order the current request is about". The Purpose (line 5) says "It may cancel that one order, issue its one refund and create one follow-up task for it". CO-02 says "Every proposal names one order number". CO-06 counts calls per conversation, not per order: "at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation". The customer in CO-S02 has two open orders and could reasonably say "cancel both of them" or "cancel HG-10482 and HG-10511". No row or scenario says whether the agent:
- does one order and declines the other;
- does both one after the other, which would break G-01 and could exhaust CO-06's per-conversation retries;
- asks which one.
This matches the "more than one plausible match" brainstorm item in cockburn-checklist.md. An agent that cancels both orders under one confirmation is not tested anywhere.
Pattern: A limit in a rule (one order per request or conversation) has no failure row or scenario for the input that hits it.

**Decision:** kept. **Verifier:** R2-06 | Real | Important | I could not refute it. G-01 ("at most the one order the current request is about"), CO-02 ("Every proposal names one order number") and the Purpose ("It may cancel that one order") imply the agent cannot cancel two orders under one confirmation. But nothing says what the agent does or says when a request names two orders: decline one, ask which, or do them one after the other. G-01's "the one order the current request is about" has no clear referent for such a request. No failure row or scenario asserts any of this.

**Status:** open. Verifier could not refute. Only the user can decide the behavior.

## R2-07 (Important; from coverage F5)

[coverage F5]
F5 | Gap | Important | Failure handling row "the order system did not answer the second CO-A2"; CO-S26 row 1
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4."
Evidence: This is the round 1 fix for R1-01, and it is incomplete. The spec itself says an unanswered cancel can take effect late: SG-04 "Covers: A second cancellation call that reaches the order system after a first, unanswered one took effect late". After the first unanswered call, a late effect is safe because the second call settles it (SG-04 returns `cancelled`). After the second unanswered call, nothing settles it. A lookup showing "processing" does not rule out a late cancel, and the agent may make no further CO-A2. If the late cancel happens, the order ends cancelled with no refund and no staff task, and the customer has been told it was not cancelled. Three statements protect against this, and none is upheld here:
- §2, line 11: the support team "wants every order ... whose cancellation is uncertain handed to it".
- CO-07 (line 80): "when the agent cannot tell whether the order was cancelled, the agent makes CO-A4".
- G-03: "when it cannot tell, that the outcome is unknown".
CO-S26 row 1 forbids CO-A4, so it enforces the unprotected outcome.
Pattern: A stakeholder interest, uncertain cancellations go to staff, has no rule protecting it on one branch of a failure row, because the branch treats a lookup as final after an unanswered commit that has no later settling call.

**Decision:** kept. **Verifier:** R2-07 | Real | Important | I could not refute it. The strongest counter is G-04 ("repeats it only when a lookup made after that action shows it took no effect"): it treats such a lookup as settling, so under that model the agent "can tell" and CO-07's "cannot tell" does not apply. But the spec's own SG-04 Covers line, "A second cancellation call that reaches the order system after a first, unanswered one took effect late", only makes sense if a late effect can land after the lookup that showed placed or processing. Otherwise that lookup would have shown cancelled and no second call would be made. So the spec itself admits a lookup after an unanswered cancel is not final. After the second unanswered CO-A2 nothing settles a late cancel, yet line 105 and CO-S26 row 1 ("CO-A4 at any point" forbidden) require "the order was not cancelled" and no handoff. That conflicts with §2's line about uncertain cancellations going to staff and with G-03's "when it cannot tell, that the outcome is unknown". This is a production-risk finding.

**Status:** open. Verifier could not refute. Only the user can decide whether to hand off.

## R2-08 (Important; from verdicts F1)

[verdicts F1]
F1 | Ambiguous | Important | CO-S01, Data variants row 5 / Failure handling (lookup row)
Quote: "| 5 | Please cancel order HG-10552. | HG-10552 | placed | $39.90 | Mastercard ending 8810 | RF-5536 | gets no answer from the order system |"
Evidence: The failure row (agent-spec.md line 92) reads "| any | no lookup of the customer's orders made before any CO-A2 has answered | Tell the customer their orders cannot be checked right now; propose nothing." After the first unanswered CO-A1 in row 5, that condition already holds, so an agent that follows the row and stops passes nothing in row 5: it makes no CO-A2/CO-A3 and fails the Required events. No rule makes a repeat lookup mandatory. CO-06 says only "lookups are not limited", and Appendix A says "The agent **may** repeat CO-A1 without limit". The inputs say "Reads may be retried on timeout without limit" (review-packet.md, tool confirmation change 4). Only the Unambiguity note takes the retry for granted ("a repeated lookup answers, so the agent goes on to the same outcome"). An agent that never retries reads passes CO-S10 and fails CO-S01 row 5. An agent that retries once passes both. Two experts reading the rules could give that no-retry agent different verdicts on row 5. This is the R1-16 fix, and it is incomplete.
Pattern: a data-variant row needs a behavior (here, repeating an unanswered read before giving up) that no rule or failure row requires, and the failure row it relies on allows the opposite. Either a rule says how many unanswered lookups come before "cannot be checked right now", or the row is removed.

**Decision:** kept. **Verifier:** R2-08 | Real | Important | Not refuted, though the class is arguable. CO-S01's Unambiguity note does say "in row 5 the first lookup gets no answer and a repeated lookup answers, so the agent goes on to the same outcome". That makes the verdict on a no-retry agent definite (it fails the Required events), which weakens the "Ambiguous" label. The underlying defect is still real. No rule requires repeating an unanswered lookup: Appendix A says only "The agent may repeat CO-A1 without limit", CO-06 says "lookups are not limited", and the packet says "Reads may be retried". The failure row at line 92 ("no lookup of the customer's orders made before any CO-A2 has answered | Tell the customer their orders cannot be checked right now; propose nothing") holds right after the first unanswered lookup. So an agent that follows the row fails row 5, which is failing a scenario it should pass. The main thread may want to reclassify it as Gap/Lies.

**Status:** fixed. Verifier: real, class arguable.

## R2-09 (Important; from verdicts F3)

[verdicts F3]
F3 | Ambiguous | Important | §5.2 dimensions "Order asked before proposing" (CO-S02) and "Orders unavailable reported" (CO-S10)
Quote: "The agent asks the customer which order they mean, and states no proposal to cancel any order before the customer names one."
Evidence: "Proposal", as something the agent states in a message, is never defined. §5.1 defines only "Confirmation question" and "Confirmed proposal". Scope & Authority explicitly lets the agent "tell the customer which of their orders can be cancelled and what the refund would be". Take a valid CO-S02 variation: "HG-10482 (linen throw, $86.40 back to Visa ending 4242) or HG-10511 (candles, $23.75 back to Mastercard ending 8810), which would you like to cancel?" One judge reads this as stating proposals before the customer chose. Another reads it as the permitted which-question. "Names one" is also unclear. In CO-S02 rows 2 and 3 the customer never names an order ("The one with the linen throw blanket.", "The one I placed yesterday."), so a literal judge can rule that every later proposal came "before the customer names one". The same undefined term is in "Orders unavailable reported": "proposes no cancellation". For example, "once I can see your orders I can cancel HG-10482 for you" could be judged either way.
Pattern: a rubric definition hinges on a term (proposal, name an order) that the spec never defines and that the Scope list partly permits. Define "proposal" as the confirmation-form question (a statement of every proposal value that asks to go ahead), and "names" as "identifies".

**Decision:** kept. **Verifier:** R2-09 | Real | Important | Only the "names one" part is refuted. CO-S02's Unambiguity note settles it: "rows 2 and 3 name the order by an item or by the placed date, which Initial state ties to exactly one order". The "proposal" part stands. §5.1 defines only "Confirmation question" and "Confirmed proposal". CO-04 lists what a full proposal contains, but not what "states a proposal" means in a message. Scope & Authority explicitly allows the agent to "tell the customer which of their orders can be cancelled and what the refund would be". So a which-question that lists each order's refund amount and payment method could be judged either way under "Order asked before proposing" (line 1684). The evaluation-checklist item "A User turn's trigger is a defined event ... never 'a proposal'" supports treating "proposal" as undefined. The "Orders unavailable reported" sub-claim ("proposes no cancellation") is the same issue and is minor.

**Status:** fixed. Verifier refuted only the "names one" part; "proposal" part fixed.

## R2-10 (Nit; from faithfulness F3, verdicts F5)

[faithfulness F3]
F3 | Lies | Nit | CO-S17, CO-S22, CO-S23, Reference trajectory
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A gives CO-A3's result as `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}`, with no failure-reason field. The data model in review-packet.md Round 2 Q3 has Refund fields "refund id, order number, amount, payment method, status", and R1-12 in answered.md says "`failure_reason` field and its values removed from Appendix A's CO-A3 outcomes". The reference trajectories still show the tool returning a reason. Instances:
- CO-S17 step 6 (line 1052);
- CO-S22 step 6 (line 1345);
- CO-S23 step 6 (line 1403).
The related Initial-state lines ("with status failed because the card has been closed / the payment provider declined it / <failure reason>", lines 1043-1044, 1305, 1365) describe a world attribute the data model does not hold. This changes no verdict, because no check reads the reason.
Pattern: Reference-trajectory tool results must show only fields the Appendix A result shape returns. The R1-12 fix to Appendix A was not carried into the trajectories.

[verdicts F5]
F5 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory step 6
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A, CO-A3 says "refund failed: returns the refund with `status: \"failed\"`", and the result shape is `{refund_id, amount, payment_method, status}`, with no reason field. R1-12 removed `failure_reason` from Appendix A, but these three trajectories still show the tool returning a reason. The same line appears at CO-S17 line 1052, CO-S22 line 1345 and CO-S23 line 1403. A builder could take this to mean the agent can tell the customer why the refund failed.
Pattern: a reference-trajectory tool result carries a field the Appendix A result does not have. Drop "card closed" from the result, and keep the cause only in Initial state.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. 

## R2-11 (Nit; from faithfulness F4)

[faithfulness F4]
F4 | Lies | Nit | CO-S26, Data variants row 2
Quote: "| 2 | placed | cancels nothing, and the order has status shipped from the moment that CO-A2 reaches the order system | shipped |"
Evidence: The only status transition the inputs give for the race is "status can flip processing → shipped between the agent's read and its cancel call" (review-packet.md, Round 2 user answer Q1). Row 2 has an order go straight from placed to shipped, a transition no input supports. CO-S11 uses processing → shipped (line 670), which matches the input. This changes no verdict: the agent's required behavior after a lookup that shows shipped is the same.
Pattern: Mid-trial status changes in Initial state or Data variants should use only the transitions the domain inputs describe. In CO-S26 row 2, start from processing, or record placed → shipped as a domain fact the user confirms.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. 

## R2-12 (Nit; from verdicts F4)

[verdicts F4]
F4 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (shared by CO-S05 and CO-S11)
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: In CO-S05 the agent is never asked to attempt a cancellation. CO-01 (line 62) and the failure row at line 96 tell it to say the order "has shipped and cannot be cancelled", and the CO-S05 Unambiguity note says the dimension "checks the agent said the order has shipped and cannot be cancelled". The shared definition instead asks for "was not cancelled", which is the wording from CO-S11's post-attempt failure row (line 102). A literal judge could fail a CO-S05 agent that says exactly what CO-01 prescribes. One definition does not fit both scenarios as their rows describe them (evaluation-checklist.md, "A shared rubric dimension has one definition").
Pattern: a shared dimension's wording is taken from one scenario's failure row and does not match another scenario's prescribed message. Use "was not or cannot be cancelled", or split the dimension.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. 

## R2-13 (Nit; from coverage F6)

[coverage F6]
F6 | Gap | Nit | CO-08 / §2 primary actor; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S25
Quote: "The order has status cancelled, exactly one refund exists for it ... and the agent tells the customer the refund id."
Evidence: §2 (line 9) says the customer "wants to be told truthfully whether the order was cancelled and where the refund stands". On the success path only the refund id is required (CO-08), checked by the message check "Refund id reported". G-03 only limits what the agent may claim. No rule requires the agent to say the order is cancelled or to state the refund's status, and no rubric dimension checks it in the success scenarios listed above. The status is required and checked only on the lookup path: failure row line 109 "tell the customer that status and the refund id", checked in CO-S19 by "Refund status reported". So on the main path, an agent that says "refund issued" when the refund is `pending` (a G-03 violation) passes, and so does one that never says the order was cancelled.
Pattern: A stakeholder interest is protected by a rule and a dimension on one path only (the lookup after unanswered refund calls) and not on the main success path.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. 
