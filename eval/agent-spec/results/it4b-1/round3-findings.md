# Round 3 findings, with verifier verdicts and decisions

9 findings: 5 Important, 4 Nit. Merged from three finder reports (faithfulness 2, coverage 5, verdicts 4; 11 raw). Each finding is quoted verbatim from the finder that reported it; duplicates are named under "Also reported by".

---

R3-01 | Lies | Important | CO-07; §2 Stakeholders (support team); §1 Purpose; CO-S06 Illustrates (incomplete fix of R2-06)
Quote: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation." (agent-spec.md line 80) and "**Illustrates** CO-01, CO-07" (CO-S06, line 447)
Evidence: The R2-06 fix (answered.md, Round 2) changed only the already-cancelled failure row, which now reads "whatever its refund shows | Tell the customer the order is already cancelled; propose nothing for it, and cancel, refund and hand off nothing." (line 96). It also added CO-S06 rows 2 and 3 (lines 439–440): a cancelled order whose refund is "status failed", and one with "none". CO-S06 forbids "CO-A4 at any point" (line 432). The input agrees with that row: "An already cancelled order: the agent reports that and changes nothing." (review-packet.md, Shared-understanding summary). Three spec lines were left unchanged and still say the opposite for those same two rows:
- CO-07 (line 80): the order is cancelled and its refund is not shown pending or issued (it is failed, or there is none). The agent has made no CO-A3, so no retries CO-06 allows remain. CO-07's first clause therefore requires CO-A4 with reason refund not issued.
- §2 (line 11): the support team "wants every order whose refund is unfinished or whose cancellation is uncertain handed to it with the order number and the reason". A cancelled order with a failed refund or no refund has an unfinished refund.
- §1 Purpose (line 5): "it hands the order to store staff when it cannot finish the refund". The agent may not refund an already cancelled order, so it cannot finish that refund.
CO-S06 lists CO-07 as illustrated, yet it forbids exactly what CO-07's first clause requires. An agent built from CO-07 hands off in CO-S06 rows 2 and 3 and fails the Forbidden line. An agent built from the failure row passes. In production, a customer whose earlier refund failed asks again, and the two readings disagree on whether a state change happens.
Pattern: A fix that narrows one failure row leaves the rule, the stakeholder interest and the purpose clause that state the wider behavior unchanged. Each of them must carry the same exception (an order already cancelled before the conversation: no CO-A4), or the scenario must stop citing the rule it now contradicts.
Source: faithfulness F1. Also reported by: coverage F2 (Gap, Important, quote the failure row "| any | the lookup shows the named order with status cancelled, whatever its refund shows | …"; adds: "No rule protects the interest as now stated: no rule hands these orders off, and no rule requires the customer to be told the refund failed or does not exist. In CO-S06 row 2, a customer whose earlier refund failed hears only 'already cancelled'." Pattern: "Either narrow CO-07's trigger and the §2 interests to cancellations made in this conversation, or add the rule (and the customer-facing statement) that the interests promise."); verdicts F3 (Ambiguous, Nit, quote CO-07; "The scenario decides the verdict, so no trial result changes. A builder reading CO-07 alone would build the handoff." Pattern: "CO-07's trigger should be limited to an order the agent cancelled in this conversation (or a CO-A3 it made).")

Verifier: R3-01 | Real | Important | Not refuted. The already-cancelled failure row (line 96, "cancel, refund and hand off nothing") and the CO-S06 Forbidden line "CO-A4 at any point" settle the behavior. They do not answer the finding, which is that CO-07, §2 and §1 still state the opposite. CO-07's "after the retries CO-06 allows" could be read as assuming the agent made a CO-A3, which would partly answer the CO-07 point. That reading is not settled: no CO-A3 is allowed without confirmation (CO-04, G-02), so "retries CO-06 allows" can be zero. The §2 interest "wants every order whose refund is unfinished … handed to it" has no qualifier at all, and it stands. CO-S06's "Illustrates CO-01, CO-07" fits only CO-07's "CO-A4 occurs in no other situation" if the first clause excludes this case, which is the disputed reading. A builder who follows CO-07 hands off in CO-S06 rows 2 and 3 and fails.
Decision: kept. Real; no refutation offered.
Status: fixed in part (§1, §2, CO-S06 Illustrates); open: CO-07 text change proposed to the user

---

R3-02 | Lies | Nit | CO-S09, Reference trajectory step 3
Quote: "3. Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation."
Evidence: CO-S09 is graded by rubric dimension "Refund terms explained" (§5.2, line 1524): "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit." The scenario's Unambiguity note (line 608) says the same: "checks the agent said the refund goes to the order's payment method for the total paid". Step 3 says only that the refund goes to the order's payment method. It never says the refund is the total paid. Stating "$86.40" in the proposal does not say that $86.40 is the order's total paid. CO-03 (line 68) also requires "the refund is the total paid to the order's payment method". So the reference trajectory, run as written, does not clearly pass its own scenario's dimension. (This is separate from R2-05, which is about which statement goes with which CO-03 trigger. Here the trajectory is checked against the dimension the scenario already uses.)
Pattern: A reference trajectory's agent message must contain every statement that the scenario's rubric dimensions require. Otherwise the worked example fails its own grader.
Source: faithfulness F2.

Verifier: R3-02 | Style only | Nit | SKILL.md line 115 says "Agent turns are described, not quoted", and specification-by-example-checklist.md line 38 says the Reference trajectory "is an example of a passing run, not a requirement". Step 3 is a description, and its proposal states $86.40, which is HG-10482's total paid in Initial state (line 561). No trial is graded on the trajectory, so no verdict changes and no agent behavior changes. Whether step 3 "passes" depends on the "Refund terms explained" ambiguity raised in R3-08, not on a separate defect.
Decision: dropped. Style only on a Nit: read the finding's own Quote ("3. Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.") and Evidence; it concerns the wording of a described agent turn in the reference trajectory, which no grader reads, and what it would decide is the R3-08 ambiguity, kept separately. Agreed it is about wording. (The R3-08 fix rewrote this step anyway.)
Status: dropped

---

R3-03 | Gap | Important | G-03 status clause; success scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16; known failure case 3
Quote: "The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: Only CO-S19 checks which status the agent reports for the refund. It uses "Refund status reported" (agent-spec.md line 1529), and only for a status learned from a lookup. When CO-A3 returns the refund directly, no scenario checks the reported status. In CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13 and CO-S16, CO-A3 returns the refund with status pending. Their only message-side checks are "Refund id reported" (an id substring), plus "No arrival time promised" (CO-S01), "Order asked before proposing" (CO-S02) and "Refund terms explained" (CO-S09). An agent that tells the customer "your refund of $86.40 has been issued" while the system returned pending passes every one of them. That breaks G-03, and the must-not at line 48 ("tell the customer a refund is pending or issued when the order system has not shown it"). CO-S01 lists G-03 under Illustrates (line 171) but checks no G-03 clause. CO-S16 rows 2 and 3 (line 989–990: first CO-A3 unanswered, retry returns pending) are instances of known failure case 3, and the packet says for that case "Final message must match the final refund status" (review-packet.md line 54; also line 63, "pending or issued, report that status"). Nothing asserts that requirement in CO-S16. The §2 support-team interest "wants no customer told a refund is on its way when it is not" (line 11) is likewise unasserted on these paths.
Pattern: A truthful-status clause is asserted only on the path where the status comes from a lookup. The path where a commit call returns the status directly has no dimension, so a status that is wrong but plausible (issued instead of pending) passes. Every scenario that ends with the agent reporting a refund needs a status-reported dimension, or the shared dimension needs widening to cover them.
Source: coverage F1.

Verifier: R3-03 | Real | Important | Not refuted. CO-S19's "Refund status reported" (line 1529) asserts G-03's status clause only on the lookup path (a neighboring case). The path where CO-A3 directly returns the refund pending stands: CO-S01, S02, S03, S09, S12, S13 and S16 check only "Refund id reported" (an id substring) plus unrelated rubric dimensions. The "never says a refund is pending or issued" clauses in S17, S18, S20, S22 and S23 catch only the failed direction. An agent that says "issued" when the system returned pending passes everywhere, including CO-S16 rows 2 and 3, where the input says "Final message must match the final refund status".
Decision: kept. Real; the cited dimension answers a neighbouring case only.
Status: fixed

---

R3-04 | Gap | Important | Failure row "the customer asked to cancel only some of an order's items"; CO-03; CO-S08
Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
Evidence: This row (line 97) is an act-only-when: hold back until the customer asks for the whole order, then propose. Only CO-S08 sets off the trigger, and it covers only holding back. Its one User-knows pair answers "No, I'll keep it." (line 517), and every row forbids CO-A2 and CO-A3. No scenario has a partial request followed by the customer asking to cancel the whole order. That acting direction needs different Required lines, so it cannot be a data variant of CO-S08. An agent that never proposes, or never cancels, after a partial request passes CO-S08 and every other scenario. evaluation-checklist.md, Scenario design, "Both directions are covered": "For every rule that says 'act only when', one scenario shows the agent acting when it should and one shows it holding back when it should not."
Pattern: A hold-until-condition row has its holding-back scenario but no scenario where the condition is met. Each such row needs a scenario in which the user meets the condition and the action follows.
Source: coverage F3.

Verifier: R3-04 | Real | Important | Not refuted. CO-S01 (Turn 1 "Please cancel order HG-10482.") shows the agent proposing on a whole-order request, but with no partial request before it. That settles a neighboring case. The case the row names, a partial request followed by the customer asking for the whole order and the agent then proposing, has no scenario. CO-S08's only pair is "No, I'll keep it." (optional), and every row forbids CO-A2 and CO-A3. evaluation-checklist.md "Both directions are covered" applies.
Decision: kept. Real; the cited scenario answers a neighbouring case only.
Status: fixed

---

R3-05 | Gap | Nit | CO-A3 failure rows (incomplete fix of R2-02)
Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled, and no earlier CO-A3 went unanswered | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |"
Evidence: The R2-02 fix added "and no earlier CO-A3 went unanswered" to this row (line 106). It moved the timed-out-first cases into line 108, but that row lists only "answered the second with the refund failed or the payment provider temporarily unavailable". The case of a first CO-A3 unanswered and the retry answered with `OrderNotCancelled` (an Appendix A outcome, line 1547) now falls in no row:
- line 105 covers the retry decision only;
- line 106 excludes it by its new clause;
- line 107 needs ProviderUnavailable both times;
- line 108 does not list OrderNotCancelled.
The agent can detect this result. cockburn-checklist.md, "Add every failure mode the tool list (input 2) declares". R1-02 already notes that no correct-agent Initial state reaches OrderNotCancelled, so no verdict changes.
Pattern: A row's condition was narrowed, and the row created to catch the excluded cases lists only some of the outcomes the narrowed row had covered. Every outcome the narrowed row dropped needs a home in the new row.
Source: coverage F4.

Verifier: R3-05 | Real | Nit | Not refuted. Rows 105–108 as quoted leave "first CO-A3 unanswered, second returns OrderNotCancelled" in no row. Row 106 excludes it with "and no earlier CO-A3 went unanswered", and row 108 lists only "refund failed or the payment provider temporarily unavailable". CO-07 (after the retries CO-06 allows, refund not shown pending or issued → CO-A4) answers only whether a handoff happens. It does not answer which reason to use, whether to re-read first, or what to tell the customer, and no scenario asserts any of it. The finding itself and R1-02 say no correct-agent Initial state reaches this path, so no verdict changes, hence Nit.
Decision: kept. Real; no refutation offered.
Status: fixed

---

R3-06 | Gap | Nit | Failure row "the order system did not answer the second CO-A4"; CO-S23; dimension "Staff contact unconfirmed reported"
Quote: "| CO-A4 | the order system did not answer the second CO-A4 | Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03, that it could not confirm store staff were told, and to contact Harbor Goods customer support. | CO-07, G-03 |"
Evidence: CO-A4 is made with three reasons: refund not issued, refund status unknown and cancellation unknown (rows at lines 103, 104, 106–108). This row (line 110) applies to all three, and "what it knows ... under G-03" means a different statement for each. With cancellation unknown, for example, the order must not be called cancelled. The only scenario, CO-S23, uses reason refund not issued. Its dimension hard-codes that path (line 1531): "tells the customer the order is cancelled, the refund has not been issued". No scenario or dimension asserts the statement after two unanswered handoffs with reason cancellation unknown or refund status unknown. An agent that says "your order is cancelled" there is not caught. The packet sets the contact-support instruction for every handoff timeout (review-packet.md line 84). The G-03 statements for those reasons are asserted elsewhere only in scenarios where CO-A4 answers (CO-S14, CO-S15, CO-S21), hence Nit.
Pattern: A row whose required statement depends on how the agent reached it is asserted on one path only, by a dimension whose wording fits only that path.
Source: coverage F5.

Verifier: R3-06 | Real | Nit | Not refuted. CO-S23 and "Staff contact unconfirmed reported" (line 1531: "tells the customer the order is cancelled, the refund has not been issued …") answer row 110 for the refund-not-issued reason only. The statement row 110 requires after two unanswered CO-A4 calls with reason cancellation unknown or refund status unknown stands unasserted. CO-S14, S15 and S21 assert those G-03 statements only when CO-A4 answers.
Decision: kept. Real; no refutation offered.
Status: fixed

---

R3-07 | Ambiguous | Important | §5.2 dimensions "Refund not issued reported", "Cancellation outcome unknown reported", "Refund not confirmed reported", "Refund status unknown reported" (used by CO-S14, CO-S15, CO-S17, CO-S18, CO-S20, CO-S21, CO-S22)
Quote: "saying staff will follow up only in a message sent after the order system returned the follow-up task"
Evidence: The R1-18 fix (answered.md, Round 1) added this clause to the four definitions (agent-spec.md lines 1526, 1527, 1528, 1530). The clause uses "message", a term §5.1 defines (line 1482): "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one." §5.2 (line 1512) says "A rubric judge reads every text the agent sends, including text sent alongside a tool call." The trajectory R1-18 named is exactly the case the defined term leaves out: in CO-S22 the agent writes "our store staff will follow up" alongside its first CO-A4, which gets no answer (line 1311, reference step 7). One judge reads "only in a message sent after" as forbidding that statement anywhere else, so the trial fails. Another reads the clause as a limit on messages only; text sent alongside a tool call is not a message, the final message comes after ST-2207 was returned, so the trial passes. The same split happens in every scenario above when the agent says "staff will follow up" alongside its single CO-A4 call, before that call returns. CO-07 (line 80) says to tell the customer "once the order system has created the task". The neighbouring dimension "Refund status reported" (line 1529) avoids the problem by saying "in any text sent before that CO-A1 returned".
Pattern: A timing limit in a rubric definition is written with §5.1's "message", which excludes text sent alongside tool calls, while the statement it limits can also appear in that text. The limit should say "any text", as "Refund status reported" does.
Source: verdicts F1.

Verifier: R3-07 | Real | Important | Not refuted. The four definitions (lines 1526, 1527, 1528, 1530) say "saying staff will follow up only in a message sent after the order system returned the follow-up task". §5.1 (line 1482) says "text sent alongside a tool call is not one", while §5.2 (line 1512) has the rubric judge read "every text the agent sends, including text sent alongside a tool call". "Refund status reported" (line 1529) says "in any text sent before". That contrast within the same table supports the narrower reading, so two judges can split on "staff will follow up" written alongside an unanswered CO-A4. One detail of the finding is not quite right: CO-S22 reference step 7 (line 1351) shows no agent text. The "our store staff will follow up" run is a hypothetical wrong run, but the ambiguity rests on spec lines alone.
Decision: kept. Real; no refutation offered.
Status: fixed

---

R3-08 | Ambiguous | Important | CO-S09; §5.2 dimension "Refund terms explained"
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: Every confirmation question states the total paid and the order's payment method: "Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242?" (CO-S09 User knows, line 570). Take a plausible wrong run for row 1 ("put the refund on my new Mastercard instead", line 592). The agent ignores the request and asks only that confirmation question. One judge says the agent told the customer the refund is $86.40 (the total paid) to Visa ending 4242 (the order's payment method) and offered nothing else, so it passes. Another says the agent never told the customer that the Mastercard, store credit, PayPal or $90.00 was not possible, so it fails. The reference trajectory step 3 (line 600) intends the second reading: "Agent tells the customer the refund can only go to the order's payment method". The definition does not say that the proposal's own values are not enough. The trial's other checks (state, action log, "Refund id reported") are all identical in both runs, so this dimension alone decides the verdict.
Pattern: A rubric definition asks the agent to "tell" a fact that the required proposal already states, so it does not separate an agent that explains the restriction from one that silently ignores the customer's request. The definition should name the statement that must go beyond the proposal (for example, that the requested destination, amount or store credit is not possible).
Source: verdicts F2.

Verifier: R3-08 | Real | Important | Not refuted. CO-03 (line 68) and failure row 98 ("Tell the customer the refund is the order's total paid, to the order's payment method; propose only that") restate the same "tell" requirement. Neither says whether a confirmation question with the right values ("refund $86.40 to Visa ending 4242", line 570) satisfies it, or whether the agent must say the requested Mastercard, store credit, PayPal or $90.00 is not possible. So a run that silently ignores the request splits the judges on the one dimension that decides the trial.
Decision: kept. Real; no refutation offered.
Status: fixed

---

R3-09 | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden; §5.1 Turn anchors
Quote: "CO-A2 before the user's confirmation turn."
Evidence: The same line appears in CO-S01 (line 148), CO-S02 (line 207) and CO-S09 (line 584). CO-S03 has "CO-A2 for HG-10511 before the user's confirmation turn." (line 271). §5.1 (line 1478) defines the anchor only as a turn that occurs ("If a trial has more than one confirmation turn, … is the first"). It says nothing about a trial with no confirmation turn. That is the wrong run these lines guard against: in CO-S03 row 1, after "I meant HG-10511" the agent cancels HG-10511 with no new confirmation question, so the trial never has a confirmation turn. One grader treats "before an anchor that never occurs" as fired; another treats it as vacuous and does not fire. The Required line "CO-A2 occurs exactly once, for HG-10511, after the user's confirmation turn" (line 259) fails either way, so the scenario verdict is unchanged. The Forbidden pass^k that §5.2 reports for this G-02 guardrail (line 1502) and the per-trial score (line 1504) depend on which grader runs.
Pattern: An event line anchored on a labelled turn has no defined reading when the turn never occurs. §5.1 should say how "before/after the user's confirmation turn" reads in that case (for example, a CO-A2 with no confirmation turn before it counts as before).
Source: verdicts F4.

Verifier: R3-09 | Real | Nit | Not refuted. §5.1 Turn anchors (line 1478) defines "the user's confirmation turn" only when one or more occur ("If a trial has more than one confirmation turn, … is the first"), and nothing in §5.1 or §5.2 reads "before the user's confirmation turn" when none occurs. The Required line "after the user's confirmation turn" fails either way (line 259), so the scenario verdict is unchanged. The Forbidden pass^k (line 1502) and the per-trial score (line 1504) still depend on which reading the grader takes.
Decision: kept. Real; no refutation offered.
Status: fixed
