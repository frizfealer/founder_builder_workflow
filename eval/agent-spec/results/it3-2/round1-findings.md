# Round 1 findings

Merged findings, verbatim as sent to the verifier, each with the verifier's line and the main thread's decision.

Merged count line: 19 findings: 10 Important, 9 Nit.
Decisions: 16 kept, 3 dropped.

R1-01 | Lies | Important | CO-S17 Data variants row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-S24 Initial state; dimensions "Refund not issued reported", "Order not cancelled reported" (FA-F1, VE-F1, CV-F8)
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
Evidence: Appendix A CO-A3 row defines `OrderNotCancelled` as "the order is not cancelled". In CO-S17 the preceding CO-A2 returned cancelled (Reference trajectory step 5) and Final state asserts "HG-10482 has status cancelled", so the injected outcome cannot be true at that call. The failure row and the dimension "Refund not issued reported" still require the agent to say "the order is cancelled" right after the system said it is not; CO-07 ("when the agent cannot tell whether the order was cancelled") gives a second reading (reason cancellation unknown) that fails the Required CO-A4 reason. In CO-S24 Initial state says "Order <order> belongs to the customer" and the lookup returned it, yet CO-A2 returns `OrderNotFound`; the required message "could not be found" contradicts what the agent has just seen. The adversarial verifier brief: an injected outcome "must still describe something that can be true of the scenario at that call, given its Initial state and the results of the calls before it."
Pattern: an Initial-state injected tool outcome that contradicts the scenario's own state or earlier call results, so the required report is undecidable.

Verifier: R1-01 | Real | Important | Not refuted. Appendix A defines OrderNotCancelled as "the order is not cancelled", but CO-S17 row 3 injects it right after step 5 returned cancelled, and Final state says "HG-10482 has status cancelled". CO-S24 Initial state says the order "belongs to the customer", yet its CO-A2 returns OrderNotFound after the lookup showed it. §5.1 "answers every call normally unless an Initial-state line says otherwise" only permits the injection; it does not make the outcome true at that call.
Decision: kept; severity Important; status fixed (part open). Verifier could not refute. Fixed: CO-S17 row 3 removed; CO-S24 order leaves the order system at the first CO-A2. Open: what the agent says when OrderNotCancelled follows a cancelled CO-A2 (only the user can decide).

R1-02 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-S15 (FA-F2, CV-F4)
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. |"
Evidence: review-packet.md Round 3 Q4 (confirmed "Yes to all"): "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." That covers every cancel timeout. The row for the second timeout skips the re-read, rules out CO-A3 even when a lookup would show the order cancelled, and calls the cancellation unknown when a lookup could settle it; CO-07 hands off as cancellation unknown only "when the agent cannot tell whether the order was cancelled"; Appendix A and tool confirmation change 4 allow unlimited reads. CO-S15's Initial state makes every lookup after the second CO-A2 unanswered and its reference trajectory goes straight to CO-A4 without a CO-A1. cockburn-checklist.md Failure handling: "A failure row that branches on a lookup covers every result of the lookup".
Pattern: a confirmed recovery rule (re-read after a commit timeout, then branch on the result) applied only to the first occurrence.

Verifier: R1-02 | Real | Important | Not refuted. The row "did not answer the second CO-A2" goes straight to "Make no further CO-A2 and no CO-A3 ... cancellation unknown" with no lookup. The first-timeout row branches on a lookup, Round 3 Q4 says to re-read after a cancel timeout, and Appendix A says CO-A1 is unlimited. CO-07 hands off as unknown only when "the agent cannot tell", which a lookup could settle. The cockburn-checklist line "covers every result of the lookup" applies. CO-S15 hides this by making every later CO-A1 unanswered.
Decision: kept; severity Important; status fixed. Verifier could not refute. Second-CO-A2 failure row now re-reads and branches; CO-S15 gains the lookup; CO-S13 row 3; new CO-S25, CO-S26.

R1-03 | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported" (FA-F3)
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md Round 3 Q3 (confirmed): "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet". The spec replaces "the refund is not confirmed yet" with "the refund has not been issued", and CO-S20 is graded on that by "Refund not issued reported". An agent that says what the user specified can fail the rubric.
Pattern: a message the user confirmed for a failure path is reworded into a different claim, and the rubric grades the reworded claim.

Verifier: R1-03 | Style only | Nit | The CO-A3 row's "tell the customer the order is cancelled, the refund has not been issued" is true in both lookup results (failed refund or no refund), and it matches the failure-case-2 wording "refund not issued" and G-03. It changes only the phrasing of a truthful statement, not what the agent does.
Decision: kept; severity Nit; status fixed. Verifier said Style only; I do not agree its line refutes it: the user confirmed "say the refund is not confirmed yet" and the rubric grades a different claim, so an agent following the input can fail. Kept at the verifier's lower severity, Nit. Fixed: row wording, CO-S20, new dimension "Refund not confirmed reported".

R1-04 | Lies | Nit | Appendix A, CO-A3 row (FA-F4)
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The confirmed refund fields (review-packet.md Round 2 Q3 and the user's changes) are refund id, order number, amount, payment method, status. No failure-reason field appears in the inputs, and the row's own return shape `{refund_id, amount, payment_method, status}` leaves it out. No verdict depends on it.
Pattern: a tool result field invented beyond the confirmed data model, inconsistent with the spec's own return signature.

Verifier: R1-04 | Style only | Nit | The finding itself says "No verdict depends on it". failure_reason appears only in Appendix A's outcome cell and in Initial-state prose; no rule, check or dimension reads it.
Decision: kept; severity Nit; status fixed. Verifier said Style only; the finding is an invented tool-result field (a Lies about the tool contract), not wording, style, formatting, heading choice or preference, so it is not dropped. Fixed: failure_reason removed from Appendix A.

R1-05 | Lies | Nit | G-04 (FA-F5)
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 guarantees a repeated cancellation changes nothing, so the general clause would permit a blind CO-A2 retry. review-packet.md Round 3 Q4: "If the cancel call times out: no blind resend; re-read the order." CO-06 and CO-S13 Forbidden enforce the input, so no verdict changes.
Pattern: a global rule's general exception covers a case the user explicitly excluded.

Verifier: R1-05 | Not real | Nit | CO-06: "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing." Rules apply together, so G-04's broader "or" clause cannot license a blind second CO-A2. CO-S13 Forbidden "A second CO-A2 before a CO-A1 made after the first CO-A2" and the CO-A2 first-timeout row enforce this.
Decision: dropped; severity Nit; status dropped. Refutation read and agreed: CO-06 "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing." binds alongside G-04, so no blind CO-A2 retry is permitted.

R1-06 | Gap | Important | CO Scope & Authority "must not"; Contract; Scenarios; §5.2 (CV-F1, VE-F10)
Quote: "promise a date by which the refunded money arrives."
Evidence: review-packet.md Round 3 Q1 (confirmed "Yes to all"): "The agent promises nothing about when the money arrives." Round 2 Q2 had floated "money arrives in 5 to 10 business days". The ban exists only in the Scope "must not" list; no §2 interest, no G or CO rule, no Forbidden line and no §5.2 dimension asserts it. An agent telling the customer "back in 5-10 business days" passes every scenario.
Pattern: a confirmed must-not about what the agent tells the customer with no rule and no scenario or dimension asserting it.

Verifier: R1-06 | Real | Important | Not refuted. The ban exists only in the Scope "must not" list ("promise a date by which the refunded money arrives."). No §2 interest, G or CO rule, Forbidden line or §5.2 dimension asserts it, and Round 3 Q1 confirms it. A rule alone does not refute a Gap finding.
Decision: kept; severity Important; status fixed. Verifier could not refute. Fixed: new rule CO-09, §2 interest, dimension "No arrival date promised" on CO-S01.

R1-07 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 Unambiguity notes / dimensions; CO-08; G-03 (CV-F2)
Quote: "the only check on the agent's words, message check \"Refund id reported\", is a match on one exact value, the row's refund id." (CO-S01 Unambiguity note)
Evidence: §2 primary actor "wants to be told truthfully whether the order was cancelled and where the refund stands"; known failure case 3 (packet Round 2 Q4): "Final message must match the final refund status"; G-03 allows "pending or issued only when the order system returned that refund with that status". In every success-path scenario the only message check is the refund id substring; the refund is pending, and nothing checks the agent said the order is cancelled or did not call the refund "issued". CO-S16 rows 2-3 are known failure case 3 itself. Only CO-S19 has "Refund status reported".
Pattern: success and retry-success scenarios assert only the verbatim id; the status the agent must report truthfully is unasserted.

Verifier: R1-07 | Real | Important | Not refuted. Every success-path scenario's only message check is "Refund id reported", a verbatim match. No dimension checks the agent said the order is cancelled or the refund's status. Only CO-S19 has "Refund status reported". CO-S16 rows 2 and 3 are failure case 3 from Round 2 Q4 ("Final message must match the final refund status"), and G-03 is not asserted there.
Decision: kept; severity Important; status fixed. Verifier could not refute. Fixed: "Refund status reported" redefined and added to CO-S01, S02, S03, S09, S12, S13, S16.

R1-08 | Gap | Important | Failure handling row "changed ... in the confirming turn or after confirming" (CV-F3)
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: This row changes the outcome (no CO-A2 may follow a "yes" carrying a change), but no scenario triggers it: CO-S03 Turn 2 is "in place of a confirmation"; CO-S09 asks for another payment method in Turn 1, before any proposal. G-02's "Any change to a proposal term after confirmation voids that confirmation" has no holding-back scenario.
Pattern: a failure row that changes the outcome has no scenario.

Verifier: R1-08 | Real | Important | Not refuted. The row "changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" changes the outcome, but no scenario triggers it. CO-S03 Turn 2 is "in place of a confirmation", and CO-S09 changes terms in Turn 1, before any proposal.
Decision: kept; severity Important; status fixed. Verifier could not refute. Fixed: CO-S03 row 4 changes the order inside a "yes".

R1-09 | Gap | Nit | Failure rows "did not answer the first CO-A2" and "did not answer the second CO-A3" (CV-F5)
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
Evidence: Appendix A gives cancel_order an `OrderNotFound` outcome (tool confirmation change 1), so the inputs admit an order absent from the order system. Neither lookup-branching row covers a lookup that answers without the order. cockburn-checklist.md requires the "nothing found" branch.
Pattern: lookup-branching rows omit the "answered, record absent" result.

Verifier: R1-09 | Real | Nit | Not refuted. Both lookup-branching rows list cancelled, placed or processing, shipped or delivered, and no answer, but not "answered, order absent". The cockburn-checklist requires the nothing-found branch, and Appendix A admits OrderNotFound. It is narrow because Initial state puts the order on the account.
Decision: kept; severity Nit; status open. Verifier could not refute. Stands as an open question: no input says an order can vanish between lookups or what the agent does then; only the user can decide.

R1-10 | Gap | Important | CO-02; failure rows for shipped/cancelled ("the named order") (CV-F6)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-02 is an ask-only-when rule; its holding-back side is CO-S02, but no scenario has an unnamed request ("cancel my order") with exactly one open order; every CO-S01 row names the order. An agent that always asks "which order?" passes. evaluation-checklist.md "Both directions are covered". The rows for shipped/delivered and cancelled apply only to "the named order"; no row covers an unnamed request when the account has no open order.
Pattern: the acting side of an ask-only-when rule is untested; unnamed-request branches of the first lookup are missing.

Verifier: R1-10 | Real | Important | Not refuted. Every CO-S01 row names the order, and CO-S02 is the only unnamed request, with two open orders. No scenario has an unnamed request with exactly one open order, so an always-ask agent passes (evaluation-checklist "Both directions are covered"). The shipped and cancelled failure rows are worded for "the named order" only.
Decision: kept; severity Important; status fixed. Verifier could not refute. Fixed: CO-S01 row 4 + "No needless order question"; CO-S05 row 4; failure rows reworded from "the named order".

R1-11 | Gap | Important | G-01; Failure handling (no row) (CV-F7)
Quote: absent
Evidence: G-01: "The agent cancels, refunds and hands off at most the one order the current request is about". CO-06 caps CO-A2/CO-A3 per conversation. CO-S02 already gives a customer two open orders. No failure row, scenario or open question covers a customer who asks to cancel both, or a second order after the first is done; the CO-06 caps would truncate a second order's cancel and refund. Nothing in the packet settles it. specification-by-example-checklist.md: an unanswerable "what if" "marks an undecided rule. Record it as an open question."
Pattern: a detectable user request that the spec's own limits forbid or truncate has no failure row, scenario or open question.

Verifier: R1-11 | Real | Nit | Not refuted. G-01 and the CO-06 caps settle the outcome (one order only), but no failure row, scenario or open question covers a customer asking to cancel two orders. Nothing in the packet requires it. Importance looks closer to Nit than Important.
Decision: kept; severity Nit; status open. Verifier lowered it to Nit. Open question: cancelling more than one order in one conversation; only the user can decide.

R1-12 | Ambiguous | Important | CO-S19, CO-S20, CO-S21 Initial state (VE-F2)
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: "Together" does not say which call creates the refund, so a CO-A1 between the two CO-A3 (lookups unlimited, Appendix A; S21's outage only covers CO-A1 "after its second CO-A3") sees a harness-dependent state. S20 row 1: if the lookup shows RF-5531 failed, CO-06 ("never after the order system returned the refund with status failed") may forbid the second CO-A3, failing Required "CO-A3 occurs exactly twice". S21: if the lookup shows RF-5531 pending, G-03 lets the agent report pending and CO-07 needs no handoff, failing Required CO-A4 and "Refund status unknown reported". evaluation-checklist.md: a mid-trial change is anchored to the agent's nth state-changing call.
Pattern: an Initial-state effect shared across several calls leaves open the state a read between them sees.

Verifier: R1-12 | Real | Important | Not refuted. "together they create refund RF-5531" does not say which unanswered CO-A3 creates the refund, and CO-S19 and CO-S20 allow CO-A1 lookups between the two calls. An agent whose between-call lookup shows the refund pending is correct to stop under G-03 and CO-07 (CO-06 only permits a second CO-A3), yet it fails Required "CO-A3 occurs exactly twice". The Appendix A timeout cell defers to "Initial state", which leaves this open.
Decision: kept; severity Important; status fixed. Verifier could not refute. Fixed: CO-S19/S20/S21 tie the refund effect to the second CO-A3.

R1-13 | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15) (VE-F3)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows for this case ("did not answer the first CO-A2" lookup-unanswered branch, "did not answer the second CO-A2") require "tell the customer it is not known whether the order was cancelled and store staff will follow up", with no statement about the refund; CO-07 requires only the follow-up statement. Only the reference trajectories add "no refund was issued". An agent that does exactly what the failure row says fails the dimension.
Pattern: a rubric dimension requires a statement that the failure row's Required behavior does not list.

Verifier: R1-13 | Real | Important | Not refuted. The dimension requires "that no refund was issued". The first-CO-A2 lookup-unanswered row and the second-CO-A2 row require only "not known whether the order was cancelled and store staff will follow up". CO-07 adds nothing on the refund. An agent that does exactly what the rows say fails the dimension.
Decision: kept; severity Important; status fixed. Verifier could not refute. Fixed: cancellation-unknown branches now include "that no refund was issued".

R1-14 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11) (VE-F4)
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process"
Evidence: In CO-S05 the agent never tries to cancel; CO-01, the shipped/delivered failure row, the reference trajectory and the Unambiguity note all require "has shipped and cannot be cancelled". The shared definition requires "was not cancelled", which fits CO-S11's attempted cancellation. evaluation-checklist.md: "A shared rubric dimension has one definition."
Pattern: a shared dimension's definition fits one scenario's failure row but not the other's.

Verifier: R1-14 | Style only | Nit | The CO-S05 Reference trajectory ("has shipped and cannot be cancelled") entails "was not cancelled", and rubric judges read on meaning. The dimension's clause "never says the order was cancelled or a refund was issued" is the decisive part in both scenarios, so no verdict changes.
Decision: dropped; severity Nit; status dropped. Style only on a Nit; its Quote and Evidence read and agreed to be about wording: "has shipped and cannot be cancelled" and "was not cancelled" state the same fact, and a meaning-based judge reaches the same verdict.

R1-15 | Ambiguous | Nit | CO-03 (VE-F5)
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: The rule requires both statements for every listed request; the failure rows split them (partial items: only "only the whole order can be cancelled"; other destination/amount: only the refund terms), and the dimensions "Whole order only explained" and "Refund terms explained" follow the rows.
Pattern: a rule's required statements differ from its failure rows and dimensions.

Verifier: R1-15 | Style only | Nit | The CO-03 rule is the superset and the rows and dimensions are the checked minimum. An agent that states both facts violates no row, no Forbidden line and no dimension, and an agent that states only one fails nothing. The Scope and CO-03 text is not graded beyond the dimensions.
Decision: kept; severity Nit; status open. Verifier said Style only; the finding is a mismatch between a rule's required statements and its failure rows, not wording, so it is not dropped. The fix changes CO-03's text, so it stops at the rule and is reported as a proposed rule change for the user.

R1-16 | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden (VE-F6)
Quote: "CO-A2 before the user's confirmation turn."
Evidence: §5.1 defines the confirmation turn only when one exists. In a wrong run where the simulated user deflects a wrong-value proposal and the agent cancels anyway, no confirmation turn exists, so whether a CO-A2 is "before" it is undecided; under §5.2 scoring that decides 0 versus partial credit.
Pattern: an event line anchored on a turn that may never occur.

Verifier: R1-16 | Real | Nit | Not refuted. §5.1 defines the confirmation turn only when a User-knows answer is given to a confirmation question. A CO-A2 with no such turn is neither "before" nor "after" a turn that does not exist. The effect is the score (0 versus partial). The trial fails either way, because Required "after the user's confirmation turn" is unmet.
Decision: kept; severity Nit; status fixed. Verifier could not refute. Fixed: four Forbidden lines add "or in a trial with no confirmation turn".

R1-17 | Ambiguous | Nit | CO-S03, CO-S04 User (VE-F7)
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: The trigger is not an event §5.1 defines; §5.1 defines only "the confirmation question", which states every value of the proposal. evaluation-checklist.md: "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'."
Pattern: a scripted User turn triggered by an undefined kind of agent message.

Verifier: R1-17 | Real | Nit | Not refuted. The trigger "the agent's first question that proposes cancelling HG-10482 and asks to go ahead" is not the §5.1 "confirmation question", which must state every value (evaluation-checklist "A User turn's trigger is a defined event"). It is close in meaning, so the effect is small.
Decision: kept; severity Nit; status fixed. Verifier could not refute. Fixed: CO-S03/CO-S04 Turn 2 trigger anchored on the §5.1 confirmation-question form.

R1-18 | Ambiguous | Nit | CO-S11 Initial state (VE-F8)
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: In row 2 the first CO-A2 "gets no answer from the order system and cancels nothing"; nothing says whether a timed-out call "reaches" the order system. If not, the lookup shows processing and the agent may legitimately send a second CO-A2 (CO-06), which hits Forbidden "A second CO-A2". evaluation-checklist.md: a mid-trial change is anchored to the agent's nth state-changing call.
Pattern: a mid-trial world change anchored on a condition undefined for a timed-out call.

Verifier: R1-18 | Not real | Nit | CO-S11 Final state asserts "HG-10482 has status shipped" in both variants, and the Unambiguity note says "in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation". Together these make the timed-out first CO-A2 reach the order system. The change is also anchored to the first CO-A2, as evaluation-checklist requires.
Decision: dropped; severity Nit; status dropped. Refutation read and agreed: CO-S11 Final state "HG-10482 has status shipped" in both rows and the Unambiguity note settle that the timed-out first CO-A2 triggers the change.

R1-19 | Untestable | Nit | CO-S19 Forbidden (VE-F9)
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: §5.2: "Any Forbidden event scores the trial 0"; this line describes the absence of an event, decidable only at trial end, and needs rewording into a positive step. It is redundant with message check "Refund id reported", since RF-5531 is visible only through that lookup (Unambiguity note).
Pattern: a required action disguised as a Forbidden absence line.

Verifier: R1-19 | Real | Nit | Not refuted. §5.1 says "Event lines ... are evaluated on occurrences". "Fewer than one CO-A1 after the second CO-A3" is an absence, not an occurrence. It is mostly redundant with message check "Refund id reported" (RF-5531 is visible only through the lookup), so the effect is small.
Decision: kept; severity Nit; status fixed. Verifier could not refute. Fixed: replaced with "Ending the trial without a CO-A1 made after the second CO-A3." (template's conditional form).

