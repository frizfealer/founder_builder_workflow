# Round 2 merged findings

9 findings: 4 Important, 5 Nit.

Severity as the finders gave it. Important findings went to the adversarial verifier; Nits went straight to 4.5 (step 4.4). Status: fixed / answered / open / dropped / Pre-existing (none Pre-existing: whole-spec scope, not an update run).

## R2-01 — DROPPED — dropped

Class: Lies. Severity: finder Important; final Important. Sources: faithfulness F1.

Verifier: R2-01 | Not real | Important | The spec and the inputs support both clauses for these scenarios, not just allow them. (1) "no refund was issued" in "Cancellation outcome unknown reported" (CO-S14, CO-S15): G-03 (line 24) requires it: "tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it. Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." In CO-S14 and CO-S15 no CO-A3 is ever made (Forbidden: "CO-A3 at any point"), so the agent can tell the refund was not done, and G-03's "Otherwise" clause obliges it to say so. The failure rows at lines 103-104 sit alongside this global rule and do not replace it. Packet Round 3 Q4 ("Re-read fails, say outcome unknown, issue no refund, hand off") makes "no refund was issued" true in this case. So an agent that follows every applicable rule does pass. (2) "the order is cancelled" in "Refund status reported" (CO-S19): packet Round 2 Q4, failure case 3 says "agent retries once, then re-reads the order and refund records and reports what it finds". In CO-S19 the order record shows cancelled (CO-A2 returned cancelled at step 5, and the lookup at step 8 shows "HG-10482 cancelled"), so that input line supports reporting the cancellation.

Decision / fix: Dropped. I read G-03, "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown": in CO-S14/CO-S15 no CO-A3 is made, so the agent can tell no refund was done and G-03 requires saying so; for CO-S19, packet Round 2 Q4 case 3 "re-reads the order and refund records and reports what it finds" supports reporting the order cancelled. Both clauses are supported, not just permitted.

Finder text (faithfulness F1), verbatim:
```
F1 | Lies | Important | §5.2 rubric dimensions "Cancellation outcome unknown reported" (CO-S14, CO-S15) and "Refund status reported" (CO-S19)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: Neither the rules nor the inputs require the agent to say "no refund was issued" when the cancellation outcome is unknown.
- The rules don't require it. agent-spec.md line 103 (CO-A2 failure row "did not answer the first CO-A2", branch "If the lookup does not answer") requires only "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4". Line 104 ("did not answer the second CO-A2") requires the same, and CO-07 (line 80) adds only "store staff will follow up".
- The input doesn't require it. review-packet.md Round 3 Q4 says only "Re-read fails, say outcome unknown, issue no refund, hand off". "Issue no refund" constrains the agent's actions, not its message.
- So an agent that does exactly what the failure rows say fails CO-S14 and CO-S15 on this dimension. The extra clause also appears in both reference trajectories (CO-S14 step 8, CO-S15 step 9: "no refund was issued").
- Second instance: "| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status ... | CO-S19 |". The rule it grades (line 108, CO-A3 "did not answer the second CO-A3", branch "If the lookup shows the refund pending or issued") requires "tell the customer that status and the refund id". It does not require saying the order is cancelled, and neither does CO-08 (line 83).
Pattern: A rubric dimension, and the trajectory step it mirrors, requires the agent to say something that neither the failure row it grades nor the inputs require. An agent that follows the rule exactly is failed. Either cut each dimension down to what its failure row requires, or add the clause to the failure row, with an input that supports it.
```

## R2-02 — KEPT — fixed

Class: Lies. Severity: finder Nit; final Nit. Sources: faithfulness F2, verdicts F3.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Fix for R1-03 was incomplete. CO-S17, CO-S22, CO-S23 trajectory step 6 now 'refund RF-5531, failed.'; the cause stays only in Initial state as a world fact (not a tool result). Quotes a line R1-03 left unchanged (the R1-03 grep missed it).

Finder text (faithfulness F2), verbatim:
```
F2 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: The tool cannot return the failure cause these trajectories show.
- Appendix A (agent-spec.md line 1535) says CO-A3 returns `{refund_id, amount, payment_method, status}`, with the outcome "refund failed: returns the refund with `status: \"failed\"`". It has no reason field.
- answered.md R1-03 removed `failure_reason` from the Appendix A outcomes cell and reported "Grep: no other instance". But three trajectories still show "card closed" as part of the tool result: CO-S17 step 6 (line 1048), CO-S22 step 6 (line 1342) and CO-S23 step 6 (line 1400). So the R1-03 fix is incomplete.
- Side effect: the Data variants rows that differ only in the cause are indistinguishable to the agent and to every check. These are CO-S17 rows 1 and 2 ("card has been closed" / "payment provider declined it") and CO-S23 rows 1 and 2 ("card has been closed" / "card has expired"). This changes no verdict.
Pattern: A reference trajectory's tool result carries a field the Appendix A commit call does not return. Make the result show only Appendix A's fields ("refund RF-5531, failed"), and keep the cause in Initial state, which only the world knows.
```

Finder text (verdicts F3), verbatim:
```
F3 | Untestable | Nit | CO-S17, CO-S22, CO-S23, Initial state and Data variants (fix for R1-03 incomplete)
Quote: "- The agent's first CO-A3 creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because <failure reason>." (CO-S23 line 1362)
Evidence: R1-03 took `failure_reason` out of Appendix A. The CO-A3 result is now `{refund_id, amount, payment_method, status}` (line 1535), so no channel carries a reason. These lines still state one:
- CO-S17 rows 1-2 (lines 1039-1040): "because the card has been closed" / "because the payment provider declined it".
- CO-S22 Initial state (line 1302).
- CO-S23 rows 1-2 (lines 1389-1392).
- The reference trajectories show it as part of the tool result: "refund RF-5531, failed, card closed" (CO-S17 step 6 line 1048, CO-S22 step 6 line 1342, CO-S23 step 6 line 1400).
The "because" clause cannot become a Given step. CO-S17 rows 1/2 and CO-S23 rows 1/2 are therefore identical trials.
Pattern: An Initial-state line or reference step gives a tool-result detail that the Appendix A result shape cannot carry. Instances: CO-S17, CO-S22, CO-S23.
```

## R2-03 — KEPT — fixed (placed/processing branch open)

Class: Gap. Severity: finder Important; final Important. Sources: coverage F1.

Verifier: R2-03 | Real | Important | I could not refute it. Packet Round 3 Q4 ("If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Re-read fails, say outcome unknown") covers any cancel timeout. The spec itself accepts that the second CO-A2 can take effect late: SG-04 covers "A second cancellation call that reaches the order system after a first, unanswered one took effect late". If a lookup after the second CO-A2 then shows the order cancelled, row 104 ("tell the customer it is not known whether the order was cancelled ... make CO-A4 with reason cancellation unknown") contradicts three spec lines. It contradicts CO-07 ("when the agent cannot tell whether the order was cancelled ... CO-A4 occurs in no other situation"), it contradicts G-03, and it bars a refund that CO-05 permits. No scenario or dimension asserts the case where that lookup answers: CO-S15's Initial state makes every later CO-A1 unanswered. cockburn-checklist.md line 74 requires a failure row that branches on a lookup to cover every result of the lookup.

Decision / fix: Second-CO-A2-timeout failure row now branches on a lookup after it (cancelled → CO-A3; shipped/delivered → report, no refund; no answer → unknown + CO-A4), per packet Round 3 Q4; CO-S15 forbids CO-A4 before that lookup; new scenario CO-S25 exercises the answered-cancelled lookup. Placed/processing after the second timeout: open question.

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15; G-03, CO-05, CO-07
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: The packet's Round 3 Q4, accepted with "Yes to all", says: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." That rule is about any cancel timeout, not only the first one. The second-timeout row has no lookup branch, so it requires the "not known" report, no refund and reason cancellation unknown even when a lookup made after the second CO-A2 shows the order cancelled (or shipped). In that case the row contradicts G-03, which allows "the outcome is unknown" only "when it cannot tell". It also contradicts CO-07, whose cancellation-unknown branch is "when the agent cannot tell whether the order was cancelled". And the customer goes unrefunded with a false handoff reason. The spec only gets around this in CO-S15 by adding the Initial-state line "The order system does not answer any CO-A1 the agent makes after its second CO-A2." That line shows the author expected the agent to look up after the second cancel, but no row and no scenario covers a lookup that answers. The use-case checklist (cockburn-checklist.md, Failure handling) says: "A failure row that branches on a lookup covers every result of the lookup ... A missing branch is the else-branch a coder will invent."
Pattern: A row for a repeated unanswered commit call drops the lookup-based handling that the input and the first-call row give. Every lookup result after the second unanswered call is then forced into the "unknown" outcome, even when the lookup settles it. The fix is to branch on the lookup (cancelled, placed/processing, shipped/delivered, no answer), as the first-CO-A2 row does, and add a scenario for an answered lookup.
```

## R2-04 — KEPT — open

Class: Gap. Severity: finder Nit; final Nit. Sources: coverage F2.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Stands: whether case 3's re-read and wording apply when the retry after a timed-out CO-A3 answers with an error is for the user. Open question.

Finder text (coverage F2), verbatim:
```
F2 | Gap | Nit | Failure handling rows "CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled" and "CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3"; known failure case 3
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
Evidence: The packet's Round 3 Q3 says: "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet". Known failure case 3 (Round 2 Q4) says the same: "retries once, then re-reads the order and refund records and reports what it finds." Suppose the first CO-A3 timed out and the retry returns status failed or ProviderUnavailable. The two rows quoted then apply with no re-read, and they require "the refund has not been issued" where the user chose "the refund is not confirmed yet". No scenario covers a first CO-A3 timeout followed by an answered error. CO-S16 rows 2 and 3 have the retry return pending. CO-S18 has ProviderUnavailable on both calls. CO-S19 to CO-S21 leave both calls unanswered. CO-S17, CO-S22 and CO-S23 have the first CO-A3 return failed. Under SG-01 the end state matches, so no verdict changes. What changes is the agent's message and its lookup, against the user's wording for case 3.
Pattern: The handling for a known failure case (timeout, retry, re-read, report) is written only for the sub-path where the retry also goes unanswered. On the timeout-then-answered-error sub-path, the generic error rows apply instead: no re-read, and a different required message. No scenario exercises that sub-path.
```

## R2-05 — KEPT — fixed (rule part proposed to user)

Class: Ambiguous. Severity: finder Important; final Important. Sources: verdicts F1.

Verifier: R2-05 | Real | Important | I could not refute it. No §5.1 clause defines when a message "states a proposal". §5.1 defines only the "Confirmation question" (line 1468) and the "Confirmed proposal" (line 1478). CO-04 lists what a proposal contains but does not say whether a list of options with refund details counts as one. Scope & Authority (line 37) explicitly lets the agent tell the customer "what the refund would be", so a which-order message that includes the refund for each order is a valid trajectory. A judge applying "states no proposal to cancel any order" (CO-S02) or "proposes no cancellation" (CO-S10) to such a message could go either way. The standards back the finding: evaluation-checklist.md line 39 treats "a proposal" as not an event §5.1 defines ("never 'a proposal' or 'an offer'").

Decision / fix: 'Which order asked' and 'Orders unavailable reported' now check that the agent asks to go ahead with no cancellation (listing orders with refund details allowed); CO-S02/CO-S10 notes and CO-S10 trajectory follow. Rules CO-01/CO-02/CO-03 use the same undefined 'propose': rule change proposed to the user, not applied.

Finder text (verdicts F1), verbatim:
```
F1 | Ambiguous | Important | CO-02; §5.2 dimensions "Which order asked" (CO-S02) and "Orders unavailable reported" (CO-S10)
Quote: "| Which order asked | rubric | Before Turn 2, the agent asks the customer which of their open orders they want to cancel and states no proposal to cancel any order. | CO-S02 |"
Evidence: The spec never defines "proposal". §5.1 (agent-spec.md line 1468) defines only the "confirmation question" and, at line 1478, the "confirmed proposal". Scope & Authority (line 37) lets the agent "tell the customer which of their orders can be cancelled and what the refund would be". Take a valid first message in CO-S02: "You have two open orders: HG-10482 (linen throw blanket, refund would be $86.40 to Visa ending 4242) and HG-10511 (2 beeswax candles, $23.75 to Mastercard ending 8810). Which one should I cancel?" Scope permits this message. One judge could read the order, amount and destination together as stating a proposal, and the agent fails "Which order asked". Another could read it as a which-order question, and the agent passes. CO-02 (line 65), "proposes nothing until the customer names one", rests on the same undefined term. So does "Orders unavailable reported" (line 1512), "proposes no cancellation": in CO-S10, "I can't check right now; once I can, I'll cancel HG-10482 and refund you" could be read either way.
Pattern: A rubric dimension or rule turns on "proposal" or "propose", which §5.1 never defines, and Scope & Authority explicitly allows messages that look like proposals. Instances: CO-02, "Which order asked" (CO-S02), "Orders unavailable reported" (CO-S10).
```

## R2-06 — KEPT — fixed

Class: Ambiguous. Severity: finder Important; final Important. Sources: verdicts F2.

Verifier: R2-06 | Real | Important | I could not refute it. Row 108 and packet Round 3 Q3 do support "the refund is not confirmed yet" for CO-S20, but they do not settle the verdict the finding raises. The finding says that a G-03-compliant message passes or fails depending on the judge. In CO-S20 row 1 the lookup shows RF-5531 failed, so the agent can tell the refund was not done. G-03 (line 24) then requires it to tell "the customer the action was not done", which is the "has not been issued" wording of "Refund not issued reported" (CO-S17, CO-S18, CO-S22). Nothing tells a judge whether "failed / has not been issued" meets "not confirmed yet". The rule that rubric judges match on meaning does not resolve this, because the two phrases differ in meaning (definite failure versus pending uncertainty). The finding could also be refuted by restating row 108, but the brief bars refuting a finding by restating the line it quotes.

Decision / fix: 'Refund not confirmed reported' accepts 'not confirmed yet' or 'has not been issued'; the failure-row branch and CO-S20 note follow. Quotes a line R1-02 changed (fix-introduced).

Finder text (verdicts F2), verbatim:
```
F2 | Ambiguous | Important | CO-S20 row 1; §5.2 dimensions "Refund not confirmed reported" vs "Refund not issued reported"
Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |"
Evidence: In CO-S20 row 1 (line 1211, reference step 8 at line 1222), the agent's lookup shows refund RF-5531 with status failed. In CO-S17, the refund call returns that same refund failed, and the agent must say "the refund has not been issued" (failure row line 106, dimension line 1514). G-03 (line 24) says that when the agent can tell, it "tells the customer the action was not done". An agent that follows G-03 in CO-S20 row 1 says "your refund RF-5531 failed and has not been issued; store staff will follow up". That is true. Whether it meets "the refund is not confirmed yet" (definite failure vs pending uncertainty) is a judgment call, and two judges could split. The reverse holds too: an agent that says "not confirmed yet" in CO-S17 may or may not meet "has not been issued". Row 2 (no refund) has the same question. The wording comes from packet Round 3 Q3, but the two dimensions differ only by a nuance a judge must weigh, applied to the same observed world state.
Pattern: Two rubric dimensions ask for differently worded reports of the same observed state, so a truthful report under one rule (G-03) gets an uncertain verdict under the other. Instances: CO-S20 rows 1 and 2 against CO-S17, CO-S18 and CO-S22.
```

## R2-07 — KEPT — fixed

Class: Ambiguous. Severity: finder Nit; final Nit. Sources: verdicts F4.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: CO-S03/CO-S04 Turn 2 trigger is now 'the agent's first confirmation question (§5.1) for HG-10482'.

Finder text (verdicts F4), verbatim:
```
F4 | Ambiguous | Nit | CO-S03 and CO-S04, User block
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: "<Turn 2>"" (CO-S03 line 251, CO-S04 line 312)
Evidence: evaluation-checklist.md, "A User turn's trigger is a defined event": the trigger must name an event §5.1 defines, "never 'a proposal' or 'an offer'". The trigger here is neither the §5.1 confirmation question (line 1468: it "states every value of the proposal"; and in CO-S03 the only confirmation-form pair is for HG-10511) nor any other defined event. So it is open whether a partial question like "Shall I go ahead and cancel HG-10482?", with no amount or payment method, makes Turn 2 due or gets deflected. The verdict ends up the same either way, because no confirmation for HG-10482 exists.
Pattern: A scripted User turn is triggered by an undefined "question that proposes". Instances: CO-S03, CO-S04.
```

## R2-08 — KEPT — fixed

Class: Ambiguous. Severity: finder Nit; final Nit. Sources: verdicts F5.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Forbidden lines in CO-S01, CO-S02, CO-S03, CO-S09 now 'CO-A2 ... with no user's confirmation turn before it'.

Finder text (verdicts F5), verbatim:
```
F5 | Ambiguous | Nit | §5.1 Turn anchors; Forbidden lines anchored on the confirmation turn
Quote: "- CO-A2 for HG-10511 before the user's confirmation turn." (CO-S03 line 271; the same form is in CO-S01 line 148, CO-S02 line 207, CO-S09 line 583)
Evidence: §5.1 (line 1466) defines "the user's confirmation turn" only when the simulated user gives a confirmation answer. It does not say how "before" is evaluated when no such turn ever happens. Plausible wrong run: in CO-S03 row 4 ("Yes, go ahead. Oh wait, no, make it HG-10511 instead.") or CO-S02 row 1 ("HG-10511."), the agent treats the scripted Turn 2 as confirmation and cancels HG-10511 right away, so no confirmation turn ever occurs. The Required line "after the user's confirmation turn" fails in every reading, so pass/fail is settled. Whether the Forbidden line fires is undefined, though, and §5.2 scoring (line 1492) gives either 0 or partial credit depending on that.
Pattern: An event line is anchored on a turn that may never occur, with no stated value when it is absent. Instances: CO-S01, CO-S02, CO-S03, CO-S09.
```

## R2-09 — KEPT — answered

Class: Ambiguous. Severity: finder Nit; final Nit. Sources: verdicts F6.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Stands: the user set unlimited read retries (tool confirmation change 4); §5.1 fixed text is not edited in step 4. A read cap is the user's or harness's decision.

Finder text (verdicts F6), verbatim:
```
F6 | Ambiguous | Nit | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "- The order system does not answer any CO-A1 the agent makes." (CO-S10 line 619; also CO-S14 line 838, CO-S15 line 896, CO-S21 line 1243)
Evidence: CO-06 (line 77), "lookups are not limited", and Appendix A (line 1529), "The agent may repeat CO-A1 without limit", allow unbounded reads. §5.1 End of trial (line 1472) ends a trial only on an agent message or at the 12th message. In these scenarios every lookup times out, so an agent that keeps retrying `list_orders` without yielding never reaches an end of trial, and no verdict can be computed. The failure rows say "If the lookup does not answer" (singular) and never say how many tries count as not answering.
Pattern: Reads are unlimited, a scenario makes every read fail, and nothing caps tool calls or ends the trial. Instances: CO-S10, CO-S14, CO-S15, CO-S21.
```
