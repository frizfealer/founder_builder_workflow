# Round 1 findings, with verifier verdicts and decisions

18 findings: 10 Important, 8 Nit. Merged from three finder reports (faithfulness 10, coverage 5, verdicts 7; 22 raw). Each finding is quoted verbatim from the finder that reported it; duplicates are named under "Also reported by".

---

R1-01 | Gap | Important | CO failure rows for CO-A2 unanswered (second, and first)
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence:
- The second-timeout row does not branch on a lookup at all. The packet's Round 3 Q4 rule for a cancel timeout is "re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." CO-S15's Initial state (line 892, "does not answer any CO-A1 the agent makes after its second CO-A2") expects a lookup after the second CO-A2 but only covers the "no answer" result.
- Suppose a lookup after the second CO-A2 shows the order cancelled. The row then forbids CO-A3 and tells the customer the outcome is "not known". That conflicts with CO-05 (line 74, a refund is allowed when "a lookup shows cancelled"). It also conflicts with CO-07 (line 80), whose handoff applies only when the agent "cannot tell whether the order was cancelled" and which says "CO-A4 occurs in no other situation". If the lookup shows shipped or still placed/processing, no row says what to tell the customer or which handoff reason applies; "cancellation unknown" would be false.
- The first-timeout row (line 100) branches on cancelled, placed/processing, shipped/delivered and no answer. It has no branch for a lookup that answers without the order. The spec itself treats OrderNotFound for a listed order as possible (CO-S24).
- cockburn-checklist.md line 74: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer. A missing branch is the else-branch a coder will invent."
Pattern: A failure row after an unknown commit result either skips the re-read the inputs require, or covers only some of the lookup's results. That leaves answered-lookup branches (cancelled, shipped, still open, order absent) with no required behavior.
Source: coverage F4. Also reported by: faithfulness F1 (Lies, Important, same quote: "a failure row for the nth unanswered commit call drops a re-read step the inputs require after every timeout. The bound on commit calls is applied to reads and to the decision that follows them." It adds: "In production, an agent that follows the row leaves an order it could confirm as cancelled unrefunded, sends it to staff as 'cancellation unknown', and tells the customer something a lookup would disprove.")

Verifier: R1-01 | Real | Important | Could not refute. Row 101 ("Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled ... make CO-A4 with reason cancellation unknown") has no re-read, but the input requires one after every cancel timeout (packet R3 Q4: "re-read the order. Cancelled, continue to refund ... Shipped, report it ... Re-read fails, say outcome unknown"). If a lookup after the second CO-A2 shows the order cancelled, the row contradicts G-03 ("tells the customer an order was cancelled only when ... a lookup shows it cancelled"), CO-05 and CO-07 ("CO-A4 occurs in no other situation"). CO-S15 line 892 covers only an unanswered lookup. The missing order-absent branch of row 100 also stands, backed by cockburn-checklist.md line 74.
Decision: kept. Real; no refutation offered.
Status: fixed (in part); open for the still-open-after-two-cancels and order-absent branches

---

R1-02 | Lies | Important | CO-S17 row 3; CO-S24 Initial state; CO-A3 failure row "reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
Evidence: Appendix A line 1525 defines `OrderNotCancelled` as "the order is not cancelled". In CO-S17 the CO-A2 just before it returned cancelled and set the status (Appendix A line 1524, "Sets the order's status to cancelled"), and Final state asserts "HG-10482 has status cancelled" (line 1023). So the injected result says something false about the world at that call. In CO-S24, Appendix A defines `OrderNotFound` as "order not found", but Initial state line 1411 says "Order <order> belongs to the customer", CO-A1 has just returned it (reference step 2), and Final state still asserts it has status <status>. Neither outcome can be true of its scenario. A harness that derives tool results from state cannot produce them, and an agent that re-reads (allowed without limit) sees state that contradicts the result. Related problem: the failure row at line 103 tells the agent to "tell the customer the order is cancelled" right after the order system said it is not. No input supports that statement, and G-03 (line 24) bases a "cancelled" claim on what the order system returned.
Pattern: an injected supporting-actor outcome whose Appendix A meaning contradicts the scenario's Initial state or the result of an earlier call.
Source: faithfulness F2. Also reported by: coverage F5 (Lies, Important, adds: "The rubric 'Refund not issued reported' (line 1505) then requires the agent to say 'the order is cancelled' right after the order system said it is not. An agent that reports the conflict truthfully and calls the cancellation uncertain would fail."; cites verification.md lines 91–94); verdicts F4 (Lies, Important, adds: "Under G-03 (line 24), an agent that reports the contradiction, or says the cancellation is unconfirmed, may pass or fail depending on the judge.").

Verifier: R1-02 | Real | Important | Could not refute. Appendix A's outcome list ("the order is not cancelled: `OrderNotCancelled`"; "order not found: `OrderNotFound`") only permits these kinds of result. It does not make them true at that call. In CO-S17 row 3, the CO-A2 just before returned cancelled and set the status (Appendix A line 1524, Final state line 1023). In CO-S24, line 1411 says "Order <order> belongs to the customer", CO-A1 returned it, and Final state still asserts it exists. Neither injected outcome can be true of its scenario. Row 103 then tells the customer "the order is cancelled" right after the order system said it is not.
Decision: kept. Real; no refutation offered.
Status: fixed (CO-S17 row 3 and CO-S24 removed); open: the OrderNotFound and OrderNotCancelled failure-row clauses have no scenario consistent with the spec

---

R1-03 | Lies | Important | §5.2 "Cancellation outcome unknown reported" (CO-S14, CO-S15); "Refund not issued reported" with CO-S20 and the CO-A3 failure row "did not answer the second CO-A3"
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, ..." and "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: (a) The CO-A2 failure rows at lines 100–101 require the agent to say only "it is not known whether the order was cancelled and store staff will follow up". The input (packet line 64) says "say outcome unknown, issue no refund, hand off", where "issue no refund" is an action, not something to tell the customer. The rubric, and the reference trajectories at lines 873 and 932, add a required statement "that no refund was issued" that no rule and no input requires. An agent that follows the failure row exactly fails CO-S14 and CO-S15. (b) For a refund still unconfirmed after the retry and the re-read, the input (packet line 63) says "failed or no refund, hand off and say the refund is not confirmed yet". The spec requires the firmer "the refund has not been issued", in the failure row at line 105, the rubric at line 1505 and CO-S20's trajectory at line 1219. An agent that says what the input specifies can fail the CO-S20 rubric.
Pattern: a rubric dimension or failure row requires a customer statement that differs from the statement the inputs specify, or adds one to it.
Source: faithfulness F3.

Verifier: R1-03 | Not real | Important | Part (a): G-03 (line 24), "tells the customer a refund is pending or issued only when ... Otherwise it tells the customer the action was not done", requires "no refund was issued" in CO-S14 and CO-S15, where no CO-A3 was made. So following every rule, not only rows 100 and 101, gives that statement. Part (b): the same G-03 clause, plus packet R2 Q4 case 2 ("refund not issued, state known; agent reports it"), supports "the refund has not been issued" once the lookup in row 105 and CO-S20 shows the refund failed or absent.
Decision: kept. Refutation read and accepted for part (a) only: G-03 makes "no refund was issued" a required statement. For part (b) the cited input, case 2, is the refund-error case, not the timeout-then-re-read case; for this case the input (Round 3 Q3) names the statement "say the refund is not confirmed yet", and G-03 is a spec line, not an input. The refutation answers part of the finding, so the finding stands for (b).
Status: fixed (part b); part (a) answered: G-03 requires it

---

R1-04 | Lies | Important | CO-08; §5.2 "Refund id reported"
Quote: "The order has status cancelled, exactly one refund exists for it ... no follow-up task exists for it, and the agent tells the customer the refund id."
Evidence: For a finished refund the inputs ask only that "Final message must match the final refund status" (packet line 54) and "pending or issued, report that status" (packet line 63). No input asks for the refund id. The shared-understanding summary (packet lines 69–73) lists every derivation the assistant marked as its own, and this one is not there. Even so, message check "Refund id reported" decides CO-S01, S02, S03, S09, S12, S13, S16 and S19 (line 1497). An agent that says "your order is cancelled and the $86.40 refund to Visa ending 4242 is pending" meets every input yet fails eight scenarios.
Pattern: a success guarantee requires telling the customer something no input or confirmed derivation requires, and a grader enforces it.
Source: faithfulness F4.

Verifier: R1-04 | Real | Important | Could not refute. No input or confirmed derivation asks the agent to tell the customer the refund id. The inputs ask only "Final message must match the final refund status" and "pending or issued, report that status", and the shared-understanding list does not include it. Yet CO-08 and message check "Refund id reported" (line 1497) decide 8 scenarios on it.
Decision: kept. Real; no refutation offered.
Status: open: the fix changes CO-08's text, proposed to the user

---

R1-05 | Lies | Nit | Appendix A, CO-A3 row
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The confirmed refund fields are "refund id, order number, amount, payment method, status" (packet line 38, with the user's change to the statuses at line 47). The tool confirmation turn says only "terminal refund error returns a refund with status failed" (packet line 77). No input names a `failure_reason` field or its values. The return shape also leaves out the confirmed `order_number` field. No scenario grades the field.
Pattern: a tool result field, or an enumerated value set, that is not in the confirmed data model or tool set.
Source: faithfulness F5.

Verifier: R1-05 | Style only | Nit | The finding concedes "No scenario grades the field". The failure_reason values match packet R3 Q3 ("card closed or expired ... or the provider declines"), and every failed refund gets the same handling (row 103). So the field and the missing order_number change no verdict and no agent behavior.
Decision: kept. Style only on a Nit: read the finding's Quote and Evidence; it is about a tool result field and value set the confirmed data model does not have, not about wording, style, formatting, heading choice or preference, so it is not dropped.
Status: fixed

---

R1-06 | Lies | Nit | 4.1 Scope & Authority, must-not list
Quote: "promise a date by which the refunded money arrives."
Evidence: The user left Round 2 Q2's "money arrives in 5 to 10 business days" (packet line 37) unanswered. Round 3 Q1, which the user confirmed, replaced it with "The agent promises nothing about when the money arrives" (packet line 61). "A date by which" is narrower than "nothing about when" and can be read to allow "within 5 to 10 business days", the unconfirmed proposal. No scenario grades it.
Pattern: a prohibition narrower than the input it comes from.
Source: faithfulness F6.

Verifier: R1-06 | Real | Nit | Could not refute. Line 49, "promise a date by which the refunded money arrives", is narrower than the confirmed R3 Q1 "promises nothing about when the money arrives". It can be read to allow "5 to 10 business days", and no other line closes that reading.
Decision: kept. Real; no refutation offered.
Status: fixed

---

R1-07 | Gap | Important | Global Contract / CO Contract (no rule); §5.2 Dimensions (no scenario)
Quote: "absent"
Evidence: Review packet, Round 3 Q1, confirmed with "Yes to all": "The agent promises nothing about when the money arrives." (Round 2 Q2 had proposed "money arrives in 5 to 10 business days"; Round 3 Q1 replaced that.) In the spec this appears only as a Scope "must not" line, agent-spec.md line 49: "- promise a date by which the refunded money arrives." No rule says it (G-01–G-04 and CO-01–CO-08, lines 17–83 never mention arrival timing), and §2 lists no interest it protects. None of the dimensions in the §5.2 table (lines 1497–1509) forbids a timing promise, so an agent that says "your refund will reach your card in 5–10 business days" passes CO-S01, CO-S09, CO-S12, CO-S16 and CO-S19.
Pattern: A confirmed input constraint on what the agent says is kept only as a Scope "must not" line, with no Contract rule, no stakeholder interest and no rubric dimension in any scenario that asserts it.
Source: coverage F1.

Verifier: R1-07 | Real | Important | Could not refute. No rule (G-01 to G-04, CO-01 to CO-08) and no §5.2 dimension (lines 1497–1509) forbids a timing promise. The only checks in CO-S01, S09, S12, S16 and S19 are state checks, action-log checks and "Refund id reported" or "Refund status reported", and none of them catches "your refund will arrive in 5–10 business days". A Gap needs a scenario or dimension that asserts the constraint, and none exists.
Decision: kept. Real; no refutation offered.
Status: fixed

---

R1-08 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1544) guarantees that repeating a cancellation creates nothing new. Read with SG-04, G-04 therefore allows a blind CO-A2 resend, which the input forbids ("no blind resend", packet line 64). Only CO-06 rules it out. The other way round, the CO-A4 retry row (line 106) relies on SG-03 and cites G-04, but G-04 names only SG-01 as its guarantee. No verdict changes, because CO-06 decides every case.
Pattern: a global rule's guarantee clause cites one guarantee but its wording covers the others, which allows a retry the inputs forbid and leaves out the guarantee another retry depends on.
Source: faithfulness F7.

Verifier: R1-08 | Style only | Nit | The finding concedes "No verdict changes, because CO-06 decides every case". CO-06 line 77, "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing", rules out a blind resend whatever G-04's citation covers. Row 106 is a valid retry under G-04's general wording ("the order system guarantees that repeating it creates nothing new"). Agent behavior is unchanged.
Decision: kept. Style only on a Nit: read the finding's Quote and Evidence; it is about what G-04's guarantee clause permits, not about wording, style, formatting, heading choice or preference, so it is not dropped.
Status: open: the fix changes G-04's text, proposed to the user

---

R1-09 | Lies | Nit | CO-S17 and CO-S20 Data variants
Quote: "- <refund final state>" with rows "Exactly one refund exists for HG-10482: RF-5531, status failed." / "No refund exists for HG-10482."
Evidence: SKILL.md line 114 requires rows to have "identical Required events and final-state lines after substituting row values, so the lines differ only in the values their <column> placeholders take". In CO-S17 (lines 1024, 1035–1037) and CO-S20 (lines 1194, 1206–1207) the column holds a whole final-state assertion, and the assertion changes form between rows (a refund with fields versus no refund). The lines do not differ only in values.
Pattern: a data-variant column that holds a whole Expected line rather than a value inside one.
Source: faithfulness F8.

Verifier: R1-09 | Style only | Nit | Its main evidence, SKILL.md line 114, is outside the packet, the spec and references/. Also, a whole-line column changes no verdict: each row's final-state line is a complete, checkable assertion (lines 1035–1037, 1206–1207).
Decision: kept. Style only on a Nit: read the finding's Quote and Evidence; it is about data-variant rows whose final-state lines differ in form, not only in values, which is a structural defect, not wording, style, formatting, heading choice or preference, so it is not dropped.
Status: fixed

---

R1-10 | Lies | Nit | CO-S06 Illustrates
Quote: "**Illustrates** CO-01, CO-05"
Evidence: CO-05 (line 74) allows CO-A3 for an order a lookup shows cancelled, and in CO-S06 the lookup shows the order cancelled. So CO-05 does not hold back the refund here. CO-01, G-02 and CO-04 (no proposal, no confirmation) do. The scenario does not exercise CO-05.
Pattern: an Illustrates entry naming a rule whose condition the scenario does not trigger.
Source: faithfulness F9.

Verifier: R1-10 | Style only | Nit | An Illustrates entry is a label. CO-S06's Forbidden line "CO-A3 at any point" decides the verdict whatever Illustrates lists, so no verdict and no agent behavior changes.
Decision: kept. Style only on a Nit: read the finding's Quote and Evidence; an Illustrates entry naming a rule the scenario does not exercise inflates the checker's rule-to-scenario coverage count; it is not about wording, style, formatting, heading choice or preference, so it is not dropped.
Status: fixed

---

R1-11 | Ambiguous | Nit | CO-A1 failure row (line 89)
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: The input says "Reads may be retried on timeout without limit" (packet line 85), Appendix A line 1519 says the same, and CO-01 (line 62) holds back only "When no lookup of the customer's orders has answered". The row's trigger is one unanswered lookup, so an agent that retries, gets an answer and proposes breaks the row but keeps CO-01. CO-S10 makes every lookup fail, so no verdict changes.
Pattern: a failure row triggered by one unanswered read where the inputs allow reads to be retried without limit.
Source: faithfulness F10.

Verifier: R1-11 | Real | Nit | Could not refute. CO-06 ("lookups are not limited") and Appendix A line 1519 ("may repeat CO-A1 without limit") conflict with row 89, which fires on a single unanswered lookup. The finding concedes that no scenario's verdict changes (CO-S10 fails every lookup). But a builder following row 89 gives up after one timeout, so agent behavior can differ, and Style only does not apply.
Decision: kept. Real; no refutation offered.
Status: fixed

---

R1-12 | Gap | Important | CO-02; CO-S02
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-S02 is the only scenario for this clause, and it asserts the clause only through the action log and the message check "Refund id reported" (Unambiguity note line 230; it is the only dimension the §5.2 table, line 1497, gives CO-S02). The "Which order would you like to cancel?" pair is a required question, but §5.2 Interaction metrics (line 1489) say recall is "never folded into the score". An agent that skips the question and proposes a guessed order passes:
- In rows 1 and 3, a guessed "Shall I cancel HG-10511 and refund $23.75 to Mastercard ending 8810?" equals the in-scope confirmation pair, so the simulated user says Yes.
- In row 2, the wrong-value guess is deflected (§5.1 line 1461). The agent can then guess HG-10482 and be confirmed.
The inputs require the disambiguation: packet Round 2 Q4 known failure case 1 says "agent must disambiguate", and the Scope "must not" (line 46) says "guess which order the customer means". No scenario asserts "proposes nothing until the customer names one".
Pattern: A rule clause requiring the agent to ask, or to hold back a proposal, is asserted only through a User-knows pair, whose recall is not scored. No rubric dimension checks that the question came before any proposal.
Source: coverage F2. Also reported by: verdicts F1 (Gap, Important, quote "CO-A2 occurs exactly once, for <order>, after the user's confirmation turn."; adds: "The Unambiguity note (line 230) says the confirmation turn 'follows the which-order answer', but nothing enforces that order. §5.1 defines no anchor for the which-order turn, and scope markers exist only as '(after Turn n)' (line 1481)." Pattern: "The scenario needs an event or scope line that fails a confirmation question asked before the clarifying answer.")

Verifier: R1-12 | Real | Important | Could not refute. CO-S02's Unambiguity note, "the confirmation turn, which follows the which-order answer", is not enforced: no Forbidden line, scope marker or dimension orders the proposal after the which-order answer. In rows 1 and 3, a guessed "Shall I cancel HG-10511 and refund $23.75 to Mastercard ending 8810?" matches the confirmation pair (§5.1 line 1461). In row 2 a wrong guess is deflected and the agent can try again. Recall is "never folded into the score" (line 1489).
Decision: kept. Real; no refutation offered.
Status: fixed

---

R1-13 | Gap | Important | G-02; CO failure row "the customer changed the order or another proposal term in the confirming turn or after confirming"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: G-02 (line 21) says "Any change to a proposal term after confirmation voids that confirmation." The only scenario with a change of order is CO-S03. Its Turn 2 is scripted "in place of a confirmation" (line 248), and its Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing" (line 292). No scenario has the customer change a term in the confirming turn (e.g. "Yes, but make it HG-10511") or after confirming. This failure row changes the outcome (the confirmation is void and a new one is needed), yet no Initial state or User block triggers it. An agent that cancels HG-10511 on a "Yes, but HG-10511 instead", with no confirmation of HG-10511's refund terms, passes every scenario.
Pattern: A failure row that changes the outcome has no scenario. The nearest scenario puts the trigger at a neighbouring point (before confirmation) instead of the one the row names (in or after the confirming turn).
Source: coverage F3.

Verifier: R1-13 | Real | Important | Partial. CO-S03 Turn 2 (line 248, "in reply to the agent's first question that proposes cancelling HG-10482 ... in place of a confirmation") covers a change made in reply to the proposal with no confirmation. It does not cover the two cases row 96 names: a change inside a confirming turn ("Yes, but HG-10511") and a change after confirming. No other scenario has a Turn 2 or Turn 3 (grep: only CO-S03 and CO-S04).
Decision: kept. Real; the cited clause answers only part.
Status: fixed (change inside a confirming turn, CO-S03 row 4); answered for the after-confirming part: no scripted turn can arrive between a confirmation and CO-A2 for an agent that does not yield there

---

R1-14 | Ambiguous | Important | CO-S19, CO-S20 row 1, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: Lines 1120 (CO-S19), 1177 with row 1 "create refund RF-5531 for HG-10482 with status failed" at line 1206 (CO-S20), and 1236 (CO-S21). Appendix A (line 1525) says "A timeout creates the refund or not as Initial state says". Initial state does not say which call creates the refund. Appendix A also says "The agent may repeat CO-A1 without limit" (line 1519). So a CO-A1 made between the two CO-A3s (a valid extra lookup) has no defined result.
- If the harness shows RF-5531 at that point, an agent that reports it and stops is allowed to: G-03 (line 24) permits reporting what a lookup shows, and CO-06 (line 77) only permits a second CO-A3. That agent then fails "CO-A3 occurs exactly twice" (lines 1132, 1189, 1249). In CO-S19 it also hits "Fewer than one CO-A1 after the second CO-A3" (line 1141), which names a call that never happened.
- If the harness shows no refund, the same agent retries and passes.
The checklist requires "Concrete initial state" and that a mid-trial change be anchored to a specific state-changing call (evaluation-checklist.md lines 35-36).
Pattern: When a record is created by an unanswered call, Initial state must say which call creates it, so every lookup in between has one defined result.
Source: verdicts F2.

Verifier: R1-14 | Real | Important | Partial. Row 102, "Make CO-A3 once more, relying on SG-01", is unconditional. It answers the bullet about an agent that does a lookup and stops: that agent fails in every case. The open fact stands: "together they create" (lines 1120, 1177, 1236) does not say which CO-A3 creates RF-5531, so a CO-A1 between the two calls has no defined result (evaluation-checklist.md lines 35–36). In CO-S21 that result matters. If the in-between lookup shows RF-5531 pending, G-03 lets the agent report pending, while row 105 and "Refund status unknown reported" require "status unknown" and a handoff.
Decision: kept. Real; the cited clause answers only part.
Status: fixed

---

R1-15 | Ambiguous | Important | CO-S16 row 2, Required events
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (line 979). A valid variant does a CO-A1 after that timeout and sees RF-5531 pending. The rules permit reporting it and stopping:
- G-03 (line 24): the agent may report a status "a lookup shows".
- CO-06 (line 77): "It makes a second CO-A3 only after…" is a permission, not a duty.
- G-04 (line 27) is also a permission.
- The CO-08 success guarantee (line 83) is fully met.
But the failure row (line 102) says "Make CO-A3 once more" with no condition, and the Required line fails an agent that stops. One expert reading the rules passes that trajectory and another reading the failure row fails it. The checklist's "Outcome, not path" (evaluation-checklist.md line 16) warns against punishing a valid path, and the brief lists "different read-only lookups" as a valid variant.
Pattern: A Required call count for a retry that the rules only permit fails an agent whose lookup has already made the retry unnecessary. Either the rule must make the retry mandatory, or the count must allow one or two calls.
Source: verdicts F3.

Verifier: R1-15 | Not real | Important | Row 102 settles the case: for an unanswered first CO-A3, "Make CO-A3 once more, relying on SG-01". That is a requirement with no condition, not a permission. CO-06, G-04 and G-03 only permit, and none of them excuses skipping the row. So every expert fails the agent that does a lookup and stops, and "CO-A3 occurs exactly twice" in CO-S16 row 2 matches the contract.
Decision: dropped. Refutation read and agreed: the quoted failure row "| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. |" requires the retry with no condition, and packet case 3 says "agent retries once"; the Required count of two matches the contract for the whole case the finding names.
Status: dropped

---

R1-16 | Untestable | Important | §5.1 End of trial and Appendix A, as applied to CO-S10, CO-S14, CO-S15, CO-S21
Quote: "The agent may repeat CO-A1 without limit; only commit calls are bounded."
Evidence: Appendix A, line 1519; the packet states the same ("Reads may be retried on timeout without limit"). The end of a trial is defined only by agent messages: "the first agent message that asks the user nothing … or at the agent's 12th message" (line 1465). A tool call is not a message (line 1463). Four scenarios make every CO-A1 time out:
- CO-S10: "does not answer any CO-A1 the agent makes" (line 615)
- CO-S14: line 834
- CO-S15: line 892
- CO-S21: line 1237
An agent that keeps retrying list_orders never yields a message, so the trial never ends and no verdict can be computed. An agent that retries dozens of times before reporting passes, though in production the customer waits indefinitely. The brief lists "a retry after an unknown result" as a plausible wrong run.
Pattern: An unbounded action combined with an end of trial defined only by messages leaves trials with no end, and so no verdict, wherever that action always fails. The spec needs a bound on calls or on reads per trial.
Source: verdicts F5.

Verifier: R1-16 | Real | Important | Could not refute. §5.1 line 1465 ends a trial only on an agent message or the 12-message cap, and line 1463 says a tool call is not a message. Line 1519 allows unlimited CO-A1. CO-S10, S14, S15 and S21 make every later CO-A1 time out, and nothing bounds reads or tool calls, so a looping agent's trial never ends and gets no verdict.
Decision: kept. Real; no refutation offered.
Status: open: a bound on reads per trial needs §5.1 fixed text, which step 4 does not edit, and conflicts with the confirmed "Reads may be retried on timeout without limit"; for the user

---

R1-17 | Ambiguous | Nit | CO-S03 and CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: Lines 248 and 308. The checklist says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'" (evaluation-checklist.md line 39). In CO-S03 this trigger cannot be the §5.1 confirmation question (line 1461), because the only confirmation-form pair is for HG-10511 (line 251). So the simulator has to judge whether a question like "Can you confirm it's HG-10482 you want cancelled?" or "Do you want me to cancel HG-10482?" is the trigger. In the paths I traced, Turn 2 still arrives before any write, so no verdict changes.
Pattern: A scripted-turn trigger named by an undefined event ("a question that proposes") needs judgment from the simulator.
Source: verdicts F6.

Verifier: R1-17 | Style only | Nit | The finding concedes "Turn 2 still arrives before any write, so no verdict changes". In CO-S03 and CO-S04, whatever question the simulator takes as the trigger, no write is authorized before a full confirmation (CO-04, the Forbidden lines). No verdict and no agent behavior changes.
Decision: kept. Style only on a Nit: read the finding's Quote and Evidence; it is about a scripted-turn trigger that is not a §5.1-defined event (evaluation checklist), which leaves the simulator to judge, not about wording, style, formatting, heading choice or preference, so it is not dropped.
Status: fixed

---

R1-18 | Gap | Nit | CO-07 and the rubric dimensions "Refund not issued reported" and "Cancellation outcome unknown reported"
Quote: "tells the customer store staff will follow up once the order system has created the task"
Evidence: CO-07 (line 80) ties the "staff will follow up" message to the task having been created. The rubric judge reads text sent alongside tool calls (line 1493). But the definitions at lines 1504-1505 check only that the agent said "store staff will follow up", not when. So in CO-S22 an agent that writes "store staff will follow up" alongside its first, unanswered CO-A4 passes, although no task existed then. CO-S23's dimension (line 1509) catches only the case where no task is ever created.
Pattern: A rule clause about when a statement may be made is not in the definition of the dimension that grades that statement.
Source: verdicts F7.

Verifier: R1-18 | Real | Nit | Could not refute. CO-07 line 80 ties the statement to "once the order system has created the task". The definition of "Refund not issued reported" (line 1505) checks only the content, so in CO-S22 an agent that says "staff will follow up" alongside its first, unanswered CO-A4 passes. CO-S23's dimension covers only the case where no task is ever created.
Decision: kept. Real; no refutation offered.
Status: fixed
