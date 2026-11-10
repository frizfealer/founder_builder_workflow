# Round 2 findings (merged, verbatim)

Merged count line: 9 findings: 8 Important, 1 Nit.

## R2-01 — kept — fixed

```
R2-01 | Lies | Important | Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"; CO-S27; dimension "Cancellation not done reported"
Source: faithfulness F1
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 and no CO-A4."
Evidence: This branch came from the R1-01 fix. The spec itself says an unanswered cancellation can take effect after a lookup has already shown the order open. Appendix B SG-04 Covers: "A second cancellation call that reaches the order system after a first, unanswered one took effect late." Appendix A CO-A2: "A timeout changes the order or not as Initial state says." So when the second CO-A2 goes unanswered, a lookup showing placed or processing does not prove the order stays uncancelled. The inputs cover only the first timeout (review-packet.md, Round 3 Q4: "If the cancel call times out: no blind resend; re-read the order. ... Still placed or processing, send the cancel once more"). Nothing in the inputs supports calling the outcome known after the second timeout, or skipping the handoff. The spec's own rules point the other way: G-03 ("when it cannot tell, that the outcome is unknown"), CO-07 ("when the agent cannot tell whether the order was cancelled, the agent makes CO-A4"), and the support team's interest in §2 ("wants every order whose refund is unfinished or whose cancellation is uncertain handed to it"). CO-S27's Forbidden "CO-A4 at any point" and the dimension text ("never says ... that whether it was cancelled is unknown") would fail an agent that hands off and says the outcome is uncertain. Meanwhile an order that gets cancelled late would end up with no refund and no follow-up task.
Pattern: A branch states a known outcome after an unanswered commit call, even though the spec's own supporting-actor guarantees allow late effects. The inputs do not decide this branch, so it should go to the user as an open question, not be written as settled behavior.
```

Verifier: `R2-01 | Real | Important | I could not refute it. No input covers a second unanswered CO-A2: Round 3 Q4 decides only the first timeout ("Still placed or processing, send the cancel once more"). The spec admits late effects after a lookup. G-04 and CO-06 allow a second CO-A2 only after a lookup shows the order open, so SG-04 Covers ("A second cancellation call that reaches the order system after a first, unanswered one took effect late") can only mean a first call that took effect after that lookup. A lookup showing the order open therefore does not settle the outcome. "No CO-A4" also conflicts with the support team's interest in §2 ("whose cancellation is uncertain"). Row 102's branch and CO-S27's "CO-A4 at any point" have no input behind them.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. Quotes a line round 1 changed (R1-01 fix). Still-open branch now treated as cannot-tell: cancellation-unknown handoff; CO-S27 rewritten; whether staff should follow up there is also listed as an open question.

## R2-02 — dropped — dropped

```
R2-02 | Lies | Important | dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15) against failure rows "did not answer the first CO-A2" and "did not answer the second CO-A2"
Source: faithfulness F2, coverage F2
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: Both governing failure rows say only "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown". Neither requires telling the customer that no refund was issued. The input (review-packet.md, Round 3 Q4) says "Re-read fails, say outcome unknown, issue no refund, hand off": the agent must not issue a refund, but it is not required to tell the customer about it. An agent that follows the failure rows exactly fails CO-S14 and CO-S15 on this dimension. The CO-S14 and CO-S15 reference trajectories (step 8 and step 10, "no refund was issued") repeat the extra requirement.
Pattern: A rubric dimension requires a statement that the rule or failure row it grades does not require. Every part of the dimension should trace to the governing row's "tell the customer" text, or that row needs the same requirement added.
Merged duplicate (coverage F2), verbatim:
  F2 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (used by CO-S14, CO-S15)
  Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not." (line 1637)
  Evidence: The dimension grades CO-S14 and CO-S15, and the failure rows behind those scenarios do not require the agent to say "no refund was issued":
  - First CO-A2 unanswered, lookup unanswered (line 101): "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
  - Second CO-A2 unanswered, lookup unanswered (line 102): the same wording.
  The source does not require it either. Round 3 Q4 reads "Re-read fails, say outcome unknown, issue no refund, hand off" (review-packet.md, Round 3): the agent must not issue a refund, but it is not told to say so. Only the reference trajectories add the clause: CO-S14 step 8 (line 878) and CO-S15 step 10 (line 939). An agent that follows the failure row word for word therefore fails CO-S14 and CO-S15 on this dimension. If the stakeholder interest "where the refund stands" (line 9) is meant to require the clause, then the two failure rows are the incomplete side and need it added.
  Pattern: a rubric dimension that requires a statement the failure row it grades does not require (or a row that leaves out a statement its dimension requires). Each dimension's definition should match the "tell the customer" text of the rows its scenarios exercise.
  
  Coverage maps with no other empty cells:
  - Every stakeholder interest maps to a rule.
  - Every tool outcome in the packet has a failure row. The CO-A2 OrderNotFound and CO-A3 OrderNotCancelled rows still have no scenario, but that is R1-07 in answered.md, so I did not report it again.
  - Every "act only when" rule (CO-01, CO-02, CO-04, CO-05, CO-06 per action, CO-07, G-04) has an acting and a holding-back scenario.
  - Every branch of every lookup-branching row maps to a scenario (CO-S11 row 2 through CO-S15, CO-S19 through CO-S21, CO-S25 through CO-S27).
  - Every required User-knows pair is used in its reference trajectory.
  - All three known failure cases from the packet, plus the processing-to-shipped race, map to scenarios.
  - Initial-state values are consistent with the rules: 2026-11-05 is a Thursday, and in CO-S02 row 3 "yesterday" is HG-10511's 2026-11-04 placed date.
```

Verifier: `R2-02 | Not real | Important | G-03, a minimal guarantee for every state-changing capability, already requires the statement: "tells the customer a refund is pending or issued only when ... Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." In CO-S14 and CO-S15 the agent made no CO-A3, so it knows the refund was not done, and G-03 requires it to say so. Both scenarios list G-03 under Illustrates, and row 102 cites G-03. The dimension follows G-03. Rows 101 and 102 leave that statement out of their "tell the customer" text, but an agent that omits it breaks G-03 anyway, so the dimension's verdict is correct.`

Decision: dropped. Verifier Not real, quoting G-03 'Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown.' I read it and agree: in CO-S14 and CO-S15 the agent made no CO-A3, so G-03, which both scenarios illustrate and the row cites, already requires telling the customer the refund was not done; the dimension follows the rule.

Status: dropped. 

## R2-03 — dropped — dropped

```
R2-03 | Ambiguous | Important | Failure handling, row "any | the customer changed the order or another proposal term ..."
Source: faithfulness F3
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: Besides the order, the proposal has two terms, the refund amount and the payment method, and CO-03 fixes both: "When the customer asks ... for a different amount, a different payment method or store credit, the agent tells the customer ... and proposes nothing else". The sibling row says the same: "Tell the customer the refund is the order's total paid, to the order's payment method; propose only that." Take a confirming turn like "Yes, but refund it to my Mastercard". This row tells the agent to propose the changed proposal, which is a refund to a different card. CO-03 and its row forbid that. Two experts would give different verdicts on an agent that proposes the Mastercard refund. The source (review-packet.md, Round 1 Q4: "any change after confirmation voids it") voids the confirmation but does not authorize re-proposing changed money terms.
Pattern: A generic "changed term" row prescribes re-proposing any changed term, including terms another rule fixes. Limit it to terms the customer may change (the order), or say that a change to a fixed term is handled by the CO-03 row.
```

Verifier: `R2-03 | Not real | Important | CO-03 settles the case: "Every proposal cancels the whole order and refunds its total paid to its payment method ... and proposes nothing else." The sibling row adds "Tell the customer the refund is the order's total paid, to the order's payment method; propose only that." So a "changed proposal" can differ only in the order. For "Yes, but refund it to my Mastercard", G-02 voids the confirmation and the CO-03 row says what to propose. Any expert fails an agent that proposes the Mastercard refund.`

Decision: dropped. Verifier Not real, quoting CO-03 'Every proposal cancels the whole order and refunds its total paid to its payment method ... and proposes nothing else.' I read it and agree: a changed proposal can differ only in the order, so no expert would pass an agent that re-proposes a refund to another card.

Status: dropped. 

## R2-04 — kept — fixed

```
R2-04 | Lies | Nit | Appendix A, CO-A3 row; CO-S17, CO-S22, CO-S23 reference trajectories
Source: faithfulness F4
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: No input gives the refund a failure-reason field. The refund fields are "refund id ..., order number, amount, payment method, status (pending, issued)", changed by the user to "Refund status: pending, issued, failed" (review-packet.md, Round 2 Q3 and the user's answer). The tool confirmation turn says only "terminal refund error returns a refund with status failed". Round 3 Q3 names the causes (card closed or expired, provider declines) as kinds of terminal error, not as values in a result field. The reference trajectories rely on the invented field ("refund RF-5531, failed, card closed" in CO-S17 step 6, CO-S22 step 6, CO-S23 step 6). No verdict depends on it, since every row's Required events and final state are the same whatever the reason.
Pattern: A tool result field or enum is invented beyond the confirmed tool contract. Either drop it or mark it as a proposal for architecture to confirm.

No defects found elsewhere. Every reference trajectory matches its Data variants row 1 after substitution. Replaying each trajectory's tool results gives exactly its Final state assertions, and the other rows keep the same Required events and final-state lines. Tool names, parameters and outcomes match the confirmed tool set apart from F4. 2026-11-05 is a Thursday, and "placed yesterday" points to HG-10511. Points already in answered.md were not reported again; that includes G-04 allowing a blind cancel resend under SG-04 (R1-09).
```

Verifier: `R2-04 | Real | Nit | I could not refute it. The packet gives the refund fields as "refund id ..., order number, amount, payment method, status", then "Refund status: pending, issued, failed", and the tool confirmation turn says only "terminal refund error returns a refund with status failed". No input has a `failure_reason` field. Round 3 Q3 names the causes but not a field. It changes no verdict, but it is an invented contract field, not a matter of wording, so I did not call it Style only.`

Decision: kept. Verifier Real (it ruled the same defect Not real as R1-10 in round 1); could not refute: no input defines a failure_reason field. Kept at Nit.

Status: fixed. failure_reason field removed from Appendix A; three trajectories updated. Quotes a line round 1 did not change (re-report of dropped R1-10).

## R2-05 — kept — fixed

```
R2-05 | Gap | Important | CO-01 / CO-07, CO-S06 Initial state
Source: coverage F1
Quote: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation." (CO-07, agent-spec.md line 80). Also CO-S06: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued." (line 411)
Evidence: No scenario starts with an order that is already cancelled and whose refund is failed or missing. The spec's own failure paths leave exactly that state behind: CO-S17 and CO-S22 (failed refund, lines 1029-1032, 1323-1325), CO-S18 (cancelled, no refund, line 1086), CO-S20 (failed or no refund, lines 1201-1203, 1214-1215), and CO-S23 (failed refund and no follow-up task, lines 1382-1384, where the customer is told to contact support). The Trigger includes "to get their money back for an order" (line 57), so a customer coming back with "where is my money for HG-10482" is in scope.
Two rules then pull different ways:
- CO-01 says only "for an order with status cancelled, it tells the customer the order is already cancelled ... it proposes nothing" (line 62). The packet backs this: "An already cancelled order: the agent reports that and changes nothing." (review-packet.md, Shared-understanding summary).
- CO-07's condition, "the order is cancelled but its refund is not shown pending or issued", is literally true here, so an agent can read it as requiring a CO-A4 handoff.
Two stakeholder interests are touched. The support team "wants every order whose refund is unfinished ... handed to it" (line 11). The customer wants to be told "where the refund stands" (line 9), and no rule or dimension says whether the agent reports the refund's state for an already-cancelled order.
CO-S06 is the only already-cancelled scenario. Its refund is issued, so CO-07 cannot fire there, and the boundary is never tested. In production an agent could make a handoff that "CO-A4 occurs in no other situation" forbids, or could tell a customer with a failed refund only "already cancelled".
Pattern: an Initial state the spec's own scenarios produce, lying inside the conditions of two rules that call for different actions, with no holding-back or acting scenario to decide which rule wins.
```

Verifier: `R2-05 | Real | Important | I could not refute it. The confirmed derivation "An already cancelled order: the agent reports that and changes nothing" (packet, Shared-understanding summary) and CO-01 settle the behavior. Under the Gap limit, though, that counts only if a scenario asserts it. CO-S06 is the only already-cancelled scenario, and its refund is "status issued", so CO-07's condition ("cancelled but its refund is not shown pending or issued") never applies there. CO-S23 leaves the uncovered state behind: a failed refund and no task.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. CO-S06 row 3 (already cancelled, refund failed) asserts nothing changes; a CO-07 clarification is a proposed rule change for the user.

## R2-06 — kept — fixed

```
R2-06 | Ambiguous | Important | CO-S02 Required events; CO-S03 Required events
Source: verdicts F1
Quote: "CO-A3 occurs exactly once, for <order>, after the CO-A2 for <order>."
Evidence: agent-spec.md line 197 (CO-S02) and line 259 (CO-S03, "CO-A3 occurs exactly once, for HG-10511, after the CO-A2 for HG-10511."). The line can be read two ways: (a) the total number of CO-A3 calls for the order is one, and that call comes after the CO-A2; or (b) the number of CO-A3 calls made after the CO-A2 is one, and earlier calls do not count. §5.1 "When an action occurs" (line 1608) says a rejected commit call still counts as an occurrence, but nothing defines which reading "exactly once ... after X" uses. Take this plausible wrong run: issue_refund(<order>) before the confirmation turn (returns OrderNotCancelled and creates nothing), then confirmation, then CO-A2, then CO-A3. G-02 (line 21) forbids it. Neither scenario has a Forbidden line that catches it: CO-S02's Forbidden lines (205-209) and CO-S03's (267-271) have no "A second CO-A3" and no "CO-A3 before the user's confirmation turn". Under reading (a) the trial fails; under (b) it passes. The other scenarios that share this Required shape avoid the problem only because they forbid an extra call: CO-S01 line 150, CO-S09 line 585, CO-S13 line 802 and CO-S25 line 1448 have "A second CO-A3", and CO-S12 line 744 has "CO-A3 before a CO-A1 made after the first CO-A2".
Pattern: an "occurs exactly N times ... after X" Required event, in a scenario with no Forbidden line that rules out an extra occurrence before X, so the verdict depends on whether the count includes occurrences before X.
```

Verifier: `R2-06 | Real | Important | I could not refute it. §5.1 "When an action occurs" makes a rejected CO-A3 an occurrence, but no clause says whether "occurs exactly once ... after the CO-A2" counts calls made before the CO-A2. Neither CO-S02's nor CO-S03's Forbidden lines catch an early CO-A3 for the target order: they have no "A second CO-A3" and no "CO-A3 before the user's confirmation turn". CO-S01, CO-S09, CO-S13 and CO-S25 add "A second CO-A3", which suggests the Required line alone was not meant to cover it.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. 'A second CO-A3.' added to CO-S02 and CO-S03 Forbidden.

## R2-07 — dropped — dropped

```
R2-07 | Ambiguous | Important | CO-S16 Required events, Data variants row 2
Source: verdicts F2
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: in row 2 (line 986) the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". A valid variation: after the timeout the agent makes a CO-A1 lookup (lookups are unlimited, CO-06 line 77 and Appendix A line 1655). The lookup shows RF-5531 pending, so the agent reports the order cancelled and RF-5531 pending, and does not retry. That run meets every Final state assertion (lines 972-974), CO-08 (line 83), G-03 (line 24) and the "Refund id reported" check. CO-07 (line 80) calls for a handoff only when the refund "is not shown pending or issued", and no rule makes the retry mandatory once a lookup shows the refund. The only text requiring the retry is the failure row "Make CO-A3 once more, relying on SG-01" (line 103), and the second call creates nothing (SG-01). The run still fails "exactly twice". One expert reads the failure row as a required path; another applies evaluation-checklist.md "Outcome, not path" ("agents find valid paths the author did not anticipate, and a path assertion punishes them") and passes it. Row 3 does not have the problem: there a lookup shows no refund, so a retry is still needed.
Pattern: a Required count on an idempotent retry, in a row where a read-only lookup can show that the first, unanswered call already took effect.
```

Verifier: `R2-07 | Not real | Important | The failure row that governs CO-S16 row 2 makes the retry required: "CO-A3 | ... did not answer it | Make CO-A3 once more, relying on SG-01." A run that looks up and stops without the retry breaks that row, so it is not a valid variation, and the code-graded "exactly twice" gives every reader the same verdict. The finding admits "The only text requiring the retry is the failure row". This is not an Ambiguous defect. Requiring a call that changes nothing may be worth raising as a separate "Outcome, not path" point (evaluation-checklist.md), but that is not the finding as filed.`

Decision: dropped. Verifier Not real, quoting the failure row 'Make CO-A3 once more, relying on SG-01.' I read it and agree: a run that skips the required retry breaks that row, so it is not a valid variation, and the code-graded count gives every reader the same verdict; the finding is not an Ambiguous defect.

Status: dropped. 

## R2-08 — kept — fixed

```
R2-08 | Ambiguous | Important | §5.2 dimension "Refund not confirmed reported" (CO-S20 row 1)
Source: verdicts F3
Quote: "The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued."
Evidence: in CO-S20 row 1 (line 1214, trajectory step 8 at line 1225) the lookup shows RF-5531 with status failed. An agent that truthfully says "the refund failed and has not been issued; store staff will follow up" follows G-03 (line 24: "Otherwise it tells the customer the action was not done"). That is also exactly what "Refund not issued reported" (line 1638) demands for the same observed status, failed, in CO-S17. Whether "has not been issued" or "failed" satisfies "is not confirmed yet" is left to the judge: one reads "not confirmed yet" as a hedge that a definite "not issued" covers, another as a required statement of uncertainty that a definite statement contradicts. The R1-08 fix (failure row line 107, after round 3 Q3) set the wording but not whether a definite not-issued report passes when the lookup shows failed.
Pattern: a rubric dimension that requires a specific framing ("not confirmed yet") where the observed state also supports a truthful, stronger statement the spec elsewhere requires, with no rule on whether that statement satisfies the dimension.
```

Verifier: `R2-08 | Real | Important | I could not refute it. Row 107 and Round 3 Q3 fix the wording "the refund is not confirmed yet". But G-03 ("Otherwise it tells the customer the action was not done") and "Refund not issued reported" support a definite "the refund failed / has not been issued" when the lookup shows failed. No §5.2 clause tells the judge whether that stronger statement meets "not confirmed yet". The meaning-matching rule covers only the simulated user.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. Quotes a line round 1 added (R1-08 fix). Dimension now accepts 'has not been issued' or 'failed' as meeting 'not confirmed yet'.

## R2-09 — kept — fixed

```
R2-09 | Ambiguous | Important | §5.2 dimension "Which order asked first" (CO-S02); also "Orders unavailable reported" (CO-S10)
Source: verdicts F4
Quote: "Before stating any proposal, the agent asks the customer which order they mean, and it states no proposal for any order before the customer has named one."
Evidence: neither the spec nor §5.1 defines "proposal". §5.1 defines only the confirmation question (line 1594) and the confirmed proposal (line 1604). Scope & Authority (line 37) allows the agent to "tell the customer which of their orders can be cancelled and what the refund would be". So a valid CO-S02 run might ask: "Which one: HG-10482 (linen throw blanket, refund $86.40 to Visa ending 4242) or HG-10511 (2 beeswax candles, refund $23.75 to Mastercard ending 8810)?" One judge treats each listed order-plus-refund as a stated proposal and fails the run; another sees a permitted which-order question and passes it. The reference trajectory step 3 ("asks which order ..., naming both", line 222) does not settle it. The same undefined term decides "Orders unavailable reported" (line 1636: "proposes no cancellation") in CO-S10. There an agent that says "once the system is back I can cancel HG-10482 and refund it to your card" may or may not count as proposing.
Pattern: a rubric dimension whose verdict turns on whether the agent "stated a proposal" or "proposed", a term with no definition separating it from the order-and-refund information Scope & Authority permits.
```

Verifier: `R2-09 | Real | Important | I could not refute it. §5.1 defines only "Confirmation question" and "Confirmed proposal", not what stating a proposal is. Scope & Authority lists "tell the customer which of their orders can be cancelled and what the refund would be" as a separate permitted item, which suggests listing refund details is not proposing, but nothing in the dimension says so. A which-order question that gives each order's refund and card could be judged either way in CO-S02, and so could "proposes no cancellation" in CO-S10.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. Quotes a line round 1 added (R1-11 fix) and one it did not ('Orders unavailable reported'). Both dimensions now say 'asks the customer to go ahead with cancelling'.


Round 2 tally: 9 merged (8 Important, 1 Nit) from 10 raw finder findings; 6 kept, 3 dropped (R2-02, R2-03, R2-07, all Important). Kept: 5 Important, 1 Nit; all 6 fixed.
