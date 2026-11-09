# Round 1 findings

21 merged findings: 10 Important, 11 Nit. Kept 18, dropped 3, Pre-existing 0.

Finder reports verbatim: eval/agent-spec/run-e4-base-2/round1-findings-faithfulness.md, -verdicts.md, -coverage.md. Verifier report verbatim: eval/agent-spec/run-e4-base-2/round1-verifier.md.

## R1-01 (Important; from faithfulness F1, coverage F3)

[faithfulness F1]
F1 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2" (also CO-S15)
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: Round 3 Q4 in review-packet.md, which the user confirmed with "Yes to all", covers any cancel timeout: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." The row for the second timeout drops the re-read. It forbids CO-A3 even when a lookup would show the order cancelled, and it requires the agent to say the outcome is unknown when a lookup could settle it. The spec also contradicts itself. CO-07 allows CO-A4 only "when the agent cannot tell whether the order was cancelled ... CO-A4 occurs in no other situation". G-03 requires reporting a cancellation that "a lookup shows". CO-S15 hides the conflict: its Initial state line "The order system does not answer any CO-A1 the agent makes after its second CO-A2" means no lookup can answer, and its Forbidden line "CO-A3 at any point" only holds because of that.
Pattern: A failure row for a repeated unanswered commit call drops the input's "re-read, then branch on what the lookup shows" handling, which the inputs apply to every timeout of that call. It replaces that handling with an unconditional "unknown" handoff, and the matching scenario's Initial state rigs the lookup so the gap never shows.

[coverage F3]
F3 | Gap | Important | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
Quote: "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown."
Evidence: packet Round 3 Q4: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." The row after the second timeout does not branch on a lookup. CO-S15's Initial state (line 892) makes every CO-A1 after the second CO-A2 go unanswered, so no scenario covers a lookup after the second timeout that shows cancelled, shipped or still placed. If a lookup shows cancelled, the row requires "not known" and forbids the refund. That conflicts with G-03 and with the input's "Cancelled, continue to refund".
Pattern: a failure row after an unseen result does not cover every lookup result (nothing found, match, mismatch, no answer). Its only scenario fixes the lookup to "no answer".

**Decision:** kept. **Verifier:** R1-01 | Real | Important | I could not refute it. Packet Round 3 Q4 gives the handling for a cancel timeout: "re-read the order. Cancelled, continue to refund … Re-read fails, say outcome unknown". The row "the order system did not answer the second CO-A2" requires "Make no further CO-A2 and no CO-A3 … not known … make CO-A4" whatever a lookup would show. No input supports skipping the refund when a lookup shows the order cancelled, so this is a valid Lies finding: showing that no input contradicts the line does not refute it. The Gap half also holds. Cockburn: "A failure row that branches on a lookup covers every result of the lookup". CO-S15 line 892 makes every CO-A1 after the second CO-A2 go unanswered, so the missing branch never shows. One sub-claim is weak and does not change the verdict: that the row contradicts CO-07 or G-03. Without a lookup the agent "cannot tell", and G-03 is only an "only when" rule.

**Status:** fixed. Verifier could not refute; I agree.

## R1-02 (Important; from faithfulness F2, coverage F7)

[faithfulness F2]
F2 | Lies | Important | CO-S17 data variant row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; dimension "Refund not issued reported"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Appendix A, CO-A3 outcomes, says `OrderNotCancelled` is returned when "the order is not cancelled". In CO-S17 the order is cancelled when CO-A3 runs. The Reference trajectory has "Agent → CO-A2 (HG-10482) → cancelled", and the Final state says "HG-10482 has status cancelled." So row 3's tool result contradicts the scenario's own world state and the tool contract. Row 3 then requires the agent to tell the customer "the order is cancelled". The failure row says so ("tell the customer the order is cancelled, the refund has not been issued"), and so does the rubric "Refund not issued reported" ("The agent tells the customer the order is cancelled"). That is the opposite of the order system's latest answer. An agent that reports the conflict or says the cancellation is uncertain fails the rubric, even though G-03 would back it. The packet (tool confirmation turn, change 2) only adds the outcome. Nothing in it says how to handle the outcome after a successful cancel, or that the order should then be reported as cancelled.
Pattern: A scenario injects a tool outcome whose own definition contradicts the scenario's world state, and the Expected message then asserts a fact the injected result denies.

[coverage F7]
F7 | Ambiguous | Important | CO-S17, Data variants row 3
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: in CO-S17 the CO-A2 answers normally (§5.1 "Supporting actors"), so per Appendix A it "Sets the order's status to cancelled". Final state asserts "HG-10482 has status cancelled". Then the first CO-A3 returns OrderNotCancelled. Initial state leaves open what a lookup after that shows. The rubric "Refund not issued reported" requires the agent to say "the order is cancelled" right after the order system said it is not. By G-03, an agent that looks up and reports what it sees, or that reports the rejection truthfully, could be graded either way.
Pattern: an Initial-state failure injection contradicts the world state that the scenario's own earlier call established. The fact the verdict depends on (what the order system says the status is) is left open.

**Decision:** kept. **Verifier:** R1-02 | Not real | Important | The failure row settles the case: "| CO-A3 | … returned the refund with status failed, or reported the order not cancelled | … tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up." The input supports it. Packet Round 2 Q4 case 2 says "Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off". G-03 allows saying "cancelled" because "the order system returned it cancelled" when CO-A2 answered. The injected outcome is allowed by §5.1: "A supporting actor answers every call normally unless an Initial-state line says otherwise." F7's claim that "Initial state leaves open what a lookup after that shows" is false. CO-A2 answered normally, which per Appendix A "Sets the order's status to cancelled". OrderNotCancelled "create[s] nothing". The Final state asserts "HG-10482 has status cancelled". So any lookup shows cancelled. CO-06 also forbids a retry: "never after the order system … reported the order not cancelled".

**Status:** open. Verifier cites the failure row and input case 2. Not accepted: Appendix A defines OrderNotCancelled as "the order is not cancelled", and the scenario's own state has the order cancelled, so the injected outcome contradicts the tool contract; the failure row the verifier quotes is the line under question. Row 3 removed; the handling of OrderNotCancelled after a returned cancellation goes to the user.

## R1-03 (Important; from verdicts F1, coverage F2)

[verdicts F1]
F1 | Ambiguous | Important | CO-S02, Expected/Forbidden blocks (with CO-02)
Quote: "Forbidden - CO-A2 before the user's confirmation turn. - CO-A2 or CO-A3 for any order other than <order>. - A second CO-A2. - CO-A4 at any point."
Evidence: CO-02 (agent-spec.md line 65) says the agent "asks which and proposes nothing until the customer names one". The Unambiguity note (line 230) says the confirmation turn "follows the which-order answer". Nothing in the Expected block or the Forbidden block checks that. Neither User-knows pair is scoped (§5.2, line 1481, offers only "(after Turn n)"/"(before Turn n)" scoping). Interaction recall is "never folded into the score" (line 1489). Take this wrong run: the agent guesses, skips the which-order question and asks "Shall I cancel HG-10511 and refund $23.75 to Mastercard ending 8810?". In rows 1 and 3 the values equal the confirmation pair, so the simulated user says "Yes", and CO-A2/CO-A3 on HG-10511 pass every line. In row 2 the guess is a wrong-value question, which is deflected, and proposing HG-10482 next then passes. So an agent that never asks which order passes all three rows. A reader going by CO-02 and the note fails that run; a reader going by the Expected block passes it.
Pattern: when a scenario tests a required clarification, no line fails a run that skips it. The order "which-order answer before confirmation" lives only in the rule and the Unambiguity note, not in an event line or a pair scope.

[coverage F2]
F2 | Gap | Important | CO-02 / CO-S02
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: Known failure case 1 (packet Round 2 Q4): "agent must disambiguate and get a confirmation naming the order number before the cancel call." CO-S02 checks the agent's words only with "Refund id reported" (spec line 230). Under §5.2 the simulated user deflects a confirmation question with a wrong value. Interaction recall is "never folded into the score". Here is a run that passes: the agent guesses, proposes HG-10482, is deflected, then asks which order and finishes correctly. No rubric dimension asserts that the agent asked which order, or that it proposed nothing before the which-order answer.
Pattern: a rule clause that requires the agent to ask and to hold back a proposal has no scenario asserting it by a rubric dimension. A proposal is a message, not an event, so Forbidden lines cannot catch it.

**Decision:** kept. **Verifier:** R1-03 | Real | Important | I could not refute it. CO-S02's Expected and Forbidden blocks have no line that orders the confirmation after the which-order answer. Neither User-knows pair is scoped. §5.2 says interaction recall is "never folded into the score". CO-S02 uses no rubric dimension, only "Refund id reported". The Unambiguity note's "which follows the which-order answer" describes the reference run and is not an assertion. So an agent that guesses and proposes HG-10511 straight away passes rows 1 and 3. It also passes row 2 after one deflection. CO-02's "asks which and proposes nothing until the customer names one" is never asserted, which fits the Gap class: "a rule that requires the agent to tell the user something, with no scenario asserting it".

**Status:** fixed. Verifier could not refute.

## R1-04 (Important; from coverage F1)

[coverage F1]
F1 | Gap | Important | §4.1 Scope & Authority (must not), no matching rule or dimension
Quote: "promise a date by which the refunded money arrives."
Evidence: review-packet.md Round 3 Q1, which the user confirmed with "Yes to all": "The agent promises nothing about when the money arrives." Round 2 Q2 had first proposed "money arrives in 5 to 10 business days", so an agent prompt could easily carry that promise. No CO or G rule states this, and no §5.2 dimension checks it. Every success scenario (CO-S01, S02, S03, S09, S12, S13, S16, S19) checks the agent's words only with the message check "Refund id reported". An agent that says "you'll have it in 5–10 business days" passes every scenario.
Pattern: a confirmed domain rule exists only as a must-not bullet. No contract rule protects it and no rubric dimension asserts it in any scenario.

**Decision:** kept. **Verifier:** R1-04 | Real | Important | I could not refute it. "promise a date by which the refunded money arrives" appears only as a must-not bullet. No CO or G rule carries it. No §5.2 dimension checks it: "Refund terms explained" covers only "payment method, amount or store credit". Packet Round 3 Q1, which the user confirmed, says "The agent promises nothing about when the money arrives". Per the brief, a rule that settles the behavior is no refutation unless a scenario or dimension asserts it, and none does.

**Status:** fixed. Verifier could not refute.

## R1-05 (Important; from coverage F4)

[coverage F4]
F4 | Gap | Important | Failure handling row "CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3"; CO-S18
Quote: "Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Known failure case 3 (packet Round 2 Q4): "refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds." Round 3 Q3: "For case 3, after the retry the agent re-reads the refund record." Appendix A's issue_refund row says a timeout "creates the refund or not as Initial state says", and CO-S16 row 2 shows a timed-out first call that created RF-5531. The row does not ask whether the first CO-A3 was unanswered. After "first unanswered, second ProviderUnavailable" the refund may exist, yet the row prescribes "has not been issued" and no lookup. CO-S18 covers only ProviderUnavailable twice. No scenario covers first-timeout-then-ProviderUnavailable.
Pattern: the second-call rows assume the first call left no effect. The combination of an unseen first result and a definite second failure has no row branch and no scenario.

**Decision:** dropped. **Verifier:** R1-05 | Not real | Important | Appendix B SG-01 rules out the case the finding fears: "a repeated refund call for an order returns the same refund id". Appendix A agrees: "every later call returns that same refund (SG-01)". If the unanswered first CO-A3 had created a refund, the second call would return that refund. Then the "returned the refund with status failed" row or the success path applies, not ProviderUnavailable. So "second CO-A3 ProviderUnavailable" means no refund exists, and "the refund has not been issued" is true. A re-read, as case 3 in the input asks, would find no refund and lead to the same CO-A4 with "refund not issued". No verdict or final state changes. CO-S18 triggers the row.

**Status:** dropped. Dropped: I read Appendix A "every later call returns that same refund (SG-01)" and SG-01; a second ProviderUnavailable means no refund was created, so "the refund has not been issued" is true and the verdict does not change.

## R1-06 (Important; from coverage F5)

[coverage F5]
F5 | Gap | Important | CO-01 / CO-05 / CO-S06
Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence: the Trigger includes "The customer asks ... to get their money back for an order". CO-05 allows CO-A3 "for an order ... a lookup shows cancelled". Appendix A says a CO-A3 on an order that already has a refund "returns that same refund (SG-01)", so in CO-S06 a wrongful CO-A3 moves no money. The one tempting case has no scenario: an already-cancelled order with no refund, or with a failed refund, where a CO-A3 really would move money without a confirmed proposal (G-02) and could double a refund staff are doing by hand (SG-02). Packet shared-understanding: "An already cancelled order: the agent reports that and changes nothing."
Pattern: the holding-back scenario for a rule uses a state where the forbidden action has no effect. The state where it would cause harm is never tested.

**Decision:** dropped. **Verifier:** R1-06 | Not real | Important | CO-S06 is the holding-back scenario, and it catches a wrongful refund by the call itself, whatever the call's effect. Its Forbidden list has "CO-A3 at any point." §5.1 says "Event lines (Required events, Forbidden events) are evaluated on occurrences, never on effects." So the finding's premise does not change any verdict: "in CO-S06 a wrongful CO-A3 moves no money". CO-01 settles the behavior: "for an order with status cancelled, it tells the customer the order is already cancelled … proposes nothing". What is left is "one more scenario would be nice", which the class definitions exclude.

**Status:** dropped. Dropped: CO-S06 Forbidden "CO-A3 at any point." and §5.1 "Event lines ... are evaluated on occurrences, never on effects" catch the wrongful refund call whatever its effect; what is left is "one more scenario would be nice".

## R1-07 (Important; from coverage F6)

[coverage F6]
F6 | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; G-02
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: packet Round 1 Q4: "any change after confirmation voids it". The only scenario on this row, CO-S03, scripts Turn 2 "in place of a confirmation" (line 248), with variants such as "Oh wait, sorry, I meant HG-10511", which contain no "yes". So no confirmation is ever given and then changed. No scenario has a turn that confirms and changes in the same breath (e.g. "Yes — actually make it HG-10511"). That is the condition this row and G-02's void clause name.
Pattern: a failure row that changes the outcome is matched to a scenario whose trigger is a nearby but different condition. The row's own trigger is never set up.

**Decision:** kept. **Verifier:** R1-07 | Not real | Important | The row's trigger reads "changed the order or another proposal term in the confirming turn or after confirming". It does not require a prior "yes". CO-S03 sets up the first disjunct: Turn 2 is the reply to the proposal's confirmation question, "in place of a confirmation", and it changes the order. CO-S03's Expected checks exactly the Required behavior: "propose the changed proposal and ask for confirmation of it". So the row has a scenario. The quoted line does not say what the finding claims ("That is the condition this row … name[s]"). This is the weakest refutation in the set. A "Yes — actually HG-10511" turn is untested, and the main thread may judge that worth a variant.

**Status:** fixed. Verifier says CO-S03's Turn 2 sets up "in the confirming turn". Not accepted: CO-S03's Turn 2 is "in place of a confirmation" and contains no confirmation, so the confirm-and-change case the row names was never set up; the verifier itself calls this its weakest refutation.

## R1-08 (Important; from verdicts F2)

[verdicts F2]
F2 | Ambiguous | Important | CO-S19, CO-S20 row 1, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: Same wording in CO-S19 (line 1120), CO-S20 (line 1177, "together they <refund effect>") and CO-S21 (line 1236). Initial state never says which call creates the refund, so a CO-A1 made between the first and second CO-A3 has no defined result. Such a lookup is allowed: Appendix A line 1519 says "The agent may repeat CO-A1 without limit". In CO-S21 only lookups after the second CO-A3 fail (line 1237), so this one answers. If the harness puts the refund in place after the first call, the lookup shows RF-5531. The agent then has no reason to resend, and with status failed (CO-S20 row 1, CO-S21 row 2) CO-06 line 77 even forbids a second CO-A3 after a failed refund. It then fails "CO-A3 occurs exactly twice". If the harness creates the refund on the second call, the same agent passes. The verdict depends on a fact Initial state leaves open. evaluation-checklist.md says "A mid-trial change to the world is anchored to a state-changing call" (to the nth call).
Pattern: a world change tied to several unanswered calls together rather than to one numbered call, which leaves the state between them undefined.

**Decision:** kept. **Verifier:** R1-08 | Real | Important | I could not refute it. CO-S19 line 1120, CO-S20 line 1177 and CO-S21 line 1236 say "together they create". They tie the world change to two calls instead of one numbered call. The rules allow a lookup between the two calls: "The agent may repeat CO-A1 without limit". What that lookup returns depends on how the harness reads the line. evaluation-checklist.md requires "tie the change to the agent's nth state-changing call", and "The agent must not be able to fail because the scenario left a fact open." Neither holds.

**Status:** fixed. Verifier could not refute.

## R1-09 (Important; from verdicts F3)

[verdicts F3]
F3 | Ambiguous | Important | CO-S16 row 2 (and CO-S19/CO-S20/CO-S21 under F2), Required events
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: CO-S16 row 2 (line 979): the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". Take a valid variation: after the unanswered call the agent makes one extra lookup, which shows RF-5531 pending. It tells the customer RF-5531 is pending and makes no second CO-A3. The world state and the message check "Refund id reported" are identical to the reference run, but the Required event fails. The failure row (line 102, "Make CO-A3 once more") reads as a mandate. G-04 (line 27) is about "an action whose result the agent cannot see", and after the lookup the result is visible. CO-06 (line 77) only bounds a second CO-A3 ("only after"). Two experts can therefore disagree on whether that trial should pass. evaluation-checklist.md, "Outcome, not path": "agents find valid paths the author did not anticipate, and a path assertion punishes them."
Pattern: an exact count on a retry in a row where an allowed lookup can show the first call already took effect, so the count asserts a path rather than an outcome.

**Decision:** dropped. **Verifier:** R1-09 | Not real | Important | The failure row settles the case and makes the retry mandatory: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01." The input supports it. Packet Round 2 Q4 case 3 says "refund call timed out — state unknown; agent retries once, then re-reads". So the trajectory with one lookup and no second CO-A3 breaks a rule, and "CO-A3 occurs exactly twice" asserts an outcome the input requires. It does not assert an optional path. evaluation-checklist "Ordering only where required … or when a rule orders the agent's own calls" covers it.

**Status:** dropped. Dropped: the failure row "Make CO-A3 once more, relying on SG-01" and input case 3 "agent retries once, then re-reads" make the second CO-A3 required, so the exact count asserts required behavior, not an optional path.

## R1-10 (Important; from verdicts F4)

[verdicts F4]
F4 | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported" and "Refund status reported"
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not." / "The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it."
Evidence: The failure rows these dimensions grade require less. Line 100 (lookup does not answer) says only "tell the customer it is not known whether the order was cancelled and store staff will follow up". Line 101 (second CO-A2 unanswered) says the same. Line 105 (lookup shows pending/issued) says "tell the customer that status and the refund id". No rule or input requires "no refund was issued" (CO-S14, CO-S15) or "the order is cancelled" (CO-S19). The input (packet, round 3 Q4) says only "say outcome unknown, issue no refund, hand off". An agent that follows these failure rows word for word fails the rubric.
Pattern: a rubric dimension that requires statements beyond the failure row or rule it grades. Each dimension's required statements should equal the Required-behavior cell of its row.

**Decision:** kept. **Verifier:** R1-10 | Real | Important | I could refute it only in part. For "Refund status reported", the input supports adding "the order is cancelled". Packet case 3 says the agent "re-reads the order and refund records and reports what it finds", and "Final message must match the final refund status". That half is not real. For "Cancellation outcome unknown reported" (CO-S14, CO-S15), it holds. Failure rows 100 and 101 require only "tell the customer it is not known whether the order was cancelled and store staff will follow up". The input says only "say outcome unknown, issue no refund, hand off". No rule or input requires telling the customer "that no refund was issued". An agent that follows those rows word for word fails the dimension. evaluation-checklist says a shared dimension's definition "must hold in every one of them as their failure rows … describe the behavior." §2's "where the refund stands" is an interest the spec states itself, not an input, so it does not support the requirement.

**Status:** fixed. Kept for the "Cancellation outcome unknown reported" half (verifier: Real); the "Refund status reported" half refuted by input case 3 "reports what it finds", which I accept.

## R1-11 (Nit; from faithfulness F3)

[faithfulness F3]
F3 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 says "cancelling an order that is already cancelled returns it cancelled and changes nothing". That is a guarantee that repeating CO-A2 creates nothing new, so G-04's second clause allows a blind resend of cancel_order. The user ruled this out (Round 3 Q4: "no blind resend; re-read the order"), and so do CO-06 ("a second CO-A2 only after ... a lookup made after it shows the order still placed or processing") and CO-S12/CO-S13 ("A second CO-A2 before a CO-A1 made after the first CO-A2"). CO-06 and the scenarios settle the verdicts, so this is a Nit.
Pattern: A global rule's general exception, read with an idempotency guarantee added later (SG-04), allows something the inputs and the capability rules forbid. The exception should name only the guarantees it covers (SG-01, SG-03).

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** open. Fix changes G-04's rule text; proposed to the user.

## R1-12 (Nit; from faithfulness F4)

[faithfulness F4]
F4 | Lies | Nit | Appendix A, CO-A3 row (also Initial state wording in CO-S17, CO-S22, CO-S23)
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The packet's data model for Refund is "refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued, failed)" (Round 2 Q3 and the user's changes). The tool confirmation turn says only "terminal refund error returns a refund with status failed". No input defines a `failure_reason` field or its three values. The causes appear only in prose (Round 3 Q3: "card closed or expired ... or the provider declines"). No verdict depends on the field.
Pattern: A tool result field and its enum values are invented beyond the confirmed data model.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. 

## R1-13 (Nit; from faithfulness F5)

[faithfulness F5]
F5 | Lies | Nit | CO-A2 failure rows "did not answer the first CO-A2" (lookup-unanswered branch) and "did not answer the second CO-A2", against CO-07
Quote: "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown." and "tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown."
Evidence: CO-07 says "tells the customer store staff will follow up once the order system has created the task". The CO-A4 row "did not answer the second CO-A4" requires telling the customer the agent "could not confirm store staff were told". So the promise may be made only after CO-A4 returns a task. Both CO-A2 rows put the promise before CO-A4. The CO-A3 rows use the correct order ("Make CO-A4 ...; tell the customer ..."). If both CO-A4 calls then time out, an agent that followed the CO-A2 rows has already made a promise the spec calls untrue. CO-S14/CO-S15 have CO-A4 succeed, so no verdict changes.
Pattern: A failure row promises the result of a handoff before the handoff call has returned, which contradicts the rule that makes the promise wait for the order system to create the task.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. 

## R1-14 (Nit; from coverage F8)

[coverage F8]
F8 | Gap | Nit | Failure handling: lookup branches
Quote: "absent"
Evidence: cockburn-checklist.md: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer", and the brainstorm item "the lookup returns ... none". Two cases have no row:
(a) The customer names no order and the answered CO-A1 returns no orders at all. CO-02's not-found clause covers only a named number.
(b) A lookup after the unanswered first CO-A2 (row at line 100) or the second CO-A3 (line 105) answers but no longer lists the order.
Pattern: the lookup branches leave out the "nothing found" result.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. (a) fixed; (b) answered: list_orders includes every order.

## R1-15 (Nit; from coverage F9)

[coverage F9]
F9 | Gap | Nit | CO-02 boundary
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which"
Evidence: every scenario except CO-S02 names the order in Turn 1. CO-S01 even sets up a distractor, delivered HG-09977, beside the open order, but its Turn 1 always names the order. No scenario has the customer name no order while exactly one order is placed or processing. That is the other side of CO-02's threshold, where the must-not "guess which order the customer means" and CO-02's "more than one" trigger must both be shown to hold.
Pattern: an "ask only when" rule has a holding-back scenario but no scenario at its boundary showing the agent proceeds without asking.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. 

## R1-16 (Nit; from coverage F10)

[coverage F10]
F10 | Gap | Nit | Failure handling row 1 / CO-01 / CO-S10
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: packet tool confirmation change 4: "Reads may be retried on timeout without limit". Appendix A: "The agent may repeat CO-A1 without limit". CO-S10 makes every CO-A1 go unanswered (line 615). No scenario has an initial lookup time out and a retry answer. The acting side of CO-01's "When no lookup of the customer's orders has answered, it proposes nothing" is never shown, and the row as written reads as giving up after one timeout.
Pattern: a rule with a "when no X has answered" hold-back has no acting scenario where X answers on a retry.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. 

## R1-17 (Nit; from coverage F11)

[coverage F11]
F11 | Gap | Nit | Failure handling, CO-A3
Quote: "absent"
Evidence: cockburn-checklist.md brainstorm item: "the supporting actor answers wrongly or late". CO-A3 returns `{refund_id, amount, payment_method, status}` (Appendix A), so the agent can detect a refund whose amount is not the order's total paid, or whose payment method is not the order's. CO-08 and CO-03 require both to match. No failure row says what the agent tells the customer or whether it hands off when they do not match.
Pattern: a detectable wrong answer from a supporting actor, against a success-guarantee field, has no failure row.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** open. Handling of a refund with the wrong amount or payment method is for the user to decide.

## R1-18 (Nit; from verdicts F5)

[verdicts F5]
F5 | Ambiguous | Nit | CO-S03 and CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: §5.1 defines only "the confirmation question", as one that "states every value of the proposal" (line 1461). "A question that proposes cancelling HG-10482" is not a defined event, and no confirmation-form pair for HG-10482 exists. So it is open whether, for example, "Do you want me to cancel HG-10482?" (no amount, no payment method) makes Turn 2 due. evaluation-checklist.md: "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." No verdict changes that I could construct, since the agent re-asks either way.
Pattern: a scripted-turn trigger written as an undefined agent act ("proposes") instead of an event §5.1 defines.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. 

## R1-19 (Nit; from verdicts F6)

[verdicts F6]
F6 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: A Forbidden line must be "a tool call pattern (name plus the argument condition) or a timing violation" (evaluation-checklist.md, "Forbidden lines name events"). This line is the absence of a read: it can only be checked at end of trial and must be reworded as "at least one CO-A1 occurs after the second CO-A3" to become a Then step. That is a required read-only call, which the checklist rules out ("A tool call that only reads is never Required"). It changes no verdict, because the message check "Refund id reported" already fails an agent that never looks up.
Pattern: a required read written as a negated Forbidden line to avoid the rule against reads in Required events.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. 

## R1-20 (Nit; from verdicts F7)

[verdicts F7]
F7 | Untestable | Nit | §5.1 End of trial, with CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: These scenarios make every lookup (or every lookup after a given call) go unanswered (lines 615, 834, 892, 1237). Appendix A line 1519 and CO-06 line 77 allow "CO-A1 without limit". An agent that keeps retrying list_orders inside one turn never sends a message, so the trial never ends under §5.1 and no verdict is defined. In practice any harness cut-off would fail the trial on Required events or the rubric, so the verdict is unchanged.
Pattern: the trial bound counts only agent messages, while the spec allows unlimited tool calls that never answer.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** open. §5.1 template text; step 4 does not edit it.

## R1-21 (Nit; from verdicts F8)

[verdicts F8]
F8 | Gap | Nit | CO-07 / CO-S22
Quote: "absent"
Evidence: CO-07 (line 80) says the agent "tells the customer store staff will follow up once the order system has created the task". The dimension CO-S22 uses, "Refund not issued reported" (line 1505), has no timing part. The rubric judge "reads every text the agent sends, including text sent alongside a tool call" (line 1493). So an agent that tells the customer staff will follow up alongside the first, unanswered CO-A4, before any task exists, passes CO-S22. No scenario checks the "once the task is created" part.
Pattern: a timing condition on something the agent must tell the user, with no dimension that checks the timing.

**Decision:** kept. **Verifier:** not verified: Nit findings go straight to 4.5

**Status:** fixed. 
