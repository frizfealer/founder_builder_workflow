# Round 2 findings

25 findings: 15 Important, 10 Nit. All 25 kept.
Finder reports: faithfulness 10 (3 Important, 7 Nit); verdicts through Codex 3 (2 Important, 1 Nit); coverage 17 (13 Important, 4 Nit). Merged from 30.

Line numbers refer to eval/verify-test/run/agent-spec.md as it stood when round 2 started, unless "packet" is named (eval/verify-test/review-packet.md).


## R2-01 | Gap | Important | CO-02, CO-S02 Expected / Forbidden
Quote: "When more than one has, the agent asks which and proposes nothing until the customer names one."
Evidence:
- No line in CO-S02 asserts the asking or the holding back. Its Forbidden lines (213-216) are all about CO-A2, CO-A3 and CO-A4, and it uses no rubric dimension for this clause.
- §5.2 says interaction recall is "never folded into the score".
- An agent that skips the question and proposes HG-10511 gets "Yes" on rows 1 and 3 and passes. On row 2 the wrong-value proposal is deflected, the agent proposes HG-10482 next, and it passes too.
- This is the user's known failure case 1 ("agent must disambiguate", review-packet.md line 52).
Pattern: A clause that requires asking or withholding a proposal is graded only by the later write, so a guess the simulated user happens to confirm passes. Each such clause needs a rubric dimension, or a check that no confirmation question precedes the which-order answer.
Source: coverage F1
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. Dimension "Which order asked" added to CO-S02.

## R2-02 | Gap | Important | CO-08, G-03, success-path scenarios CO-S01, S02, S03, S09, S12, S13, S16, S27, S28, Unambiguity notes and dimensions
Quote: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id." Also: "the only check on the agent's words, message check "Refund id reported", is a match on one exact value, the row's refund id"
Evidence:
- §2 says the customer "wants to be told truthfully whether the order was cancelled and where the refund stands".
- The user's case 3 says "Final message must match the final refund status" (review-packet.md line 54).
- G-03 (line 24) governs what the agent says about cancellation and refund status, and CO-S01 lists G-03 under Illustrates (line 176), but the status the agent states is not asserted.
- No rule requires telling the customer the order was cancelled or the refund's status on success, though every reference trajectory does it (for example CO-S01 step 7).
- Dimension "Refund status reported" (line 1825) is used only by CO-S19.
- In CO-S01, S02, S03, S09, S12, S13, S16, S27 and S28, an agent that says "your refund has been issued" for a pending refund, sends only "RF-5531", or says "RF-5531: your order could not be cancelled", passes.
- CO-S16 rows 2 and 3 (lines 1004-1005) are the timed-out-then-retried case the user's sentence is about, and they have no status check.
- No scenario has a first CO-A3 returning status issued.
Pattern: A success-path scenario grades the refund id but not the truth of the reported cancellation and refund status. Reference trajectories state a report that no rule requires and no dimension grades; G-03 is asserted only on failure paths and in CO-S19.
Source: coverage F2 + faithfulness F2
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed in the scenarios: "Refund status reported" now covers every success scenario. Open: CO-08 does not require the report (rule text, proposal P1).

## R2-03 | Lies | Important | CO-08 and dimension "Refund id reported"; failure rows; CO-S14, CO-S15, CO-S23 rubric dimensions
Quote: "no follow-up task exists for it, and the agent tells the customer the refund id."
Evidence: No input asks the agent to tell the customer the refund id.
- The packet mentions the id only as a data field (line 38) and as the idempotency key (line 49).
- What the user confirmed is status reporting: "pending or issued, report that status" (packet line 63) and "Final message must match the final refund status" (packet line 54).
- The packet's list of the assistant's confirmed derivations (lines 71-73) does not include it.
- Even so, message check "Refund id reported" gates CO-S01, S02, S03, S09, S12, S13, S16, S19, S27 and S28. An agent that truthfully says "cancelled, your $86.40 refund to Visa ending 4242 is pending" fails all ten.
Other instances of an unsupported tell that a rubric gates:
- Line 107 and dimension "Cancellation outcome unknown reported" require saying "that no refund was issued". The input says only "say outcome unknown, issue no refund, hand off" (packet line 64), so not issuing is an action there, not a statement to the customer.
- Line 114 and dimension "Staff contact unconfirmed reported" require "it could not confirm store staff were told". The input says only to "tell the customer to contact Harbor Goods support" (packet line 84).
Pattern: A customer-facing statement that no input requires is written as a rule and gated by a grader. Each one needs a source, an open question to the user, or removal from the pass condition.
Source: faithfulness F1
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: partly fixed: "no refund was issued" and "could not confirm store staff were told" removed from the rows, dimensions and scenarios. Open: the refund-id tell is CO-08 rule text (proposal P1).

## R2-04 | Lies | Important | Dimension "Shipped order explained" against CO-S05
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process"
Evidence:
- The dimension is shared by CO-S05, CO-S11 and CO-S26 (line 1816).
- CO-S05's own reference step 3 (line 403), its Unambiguity note (line 407), CO-01 (line 62) and failure row line 94 all require "has shipped and cannot be cancelled". None of them requires "was not cancelled".
- CO-S05 has no cancellation attempt, so its reference message does not literally state the dimension's "was not cancelled" clause. A judge can answer No or Unknown, and Unknown counts as not passed (line 1803).
- The evaluation checklist item "A shared rubric dimension has one definition" requires the definition to hold as each scenario's reference trajectory describes the behavior.
Pattern: The definition of a shared rubric dimension follows the post-attempt scenarios (CO-S11, CO-S26) and does not match the behavior written for the pre-attempt scenario (CO-S05).
Source: faithfulness F3
Verifier verdicts: A Real, Important; B Real, Nit; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. Definition accepts "cannot be or was not cancelled".

## R2-05 | Gap | Important | CO-S25 Forbidden
Quote: absent. The lookup requirement is missing from lines 1518-1522.
Evidence:
- Row 102 says no further action "until a lookup has been made after it". Row 105 branches on "a lookup made after the second CO-A2".
- CO-S25's Forbidden lines bound the lookup only after the first CO-A2. Nothing requires one after the second.
- An agent that stops right after the second no-answer and says "the order was not cancelled", with no read, passes all checks and "Order not cancelled reported". G-03 forbids that claim without a lookup.
- Sibling scenarios have the line: CO-S19 "Fewer than one CO-A1 after the second CO-A3." CO-S15 "CO-A4 before a CO-A1 made after the second CO-A2."
Pattern: A report that must wait for a read has no Forbidden line when the scenario's only other evidence is a rubric on the report's words.
Source: coverage F3
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. Forbidden line added to CO-S25, and to CO-S26 for the same pattern.

## R2-06 | Gap | Important | Failure rows 103 and 106 (lookup after the second unanswered CO-A2)
Quote: "a lookup made after an unanswered CO-A2 shows the order cancelled"
Evidence:
- Rows 103 and 106 cover any unanswered CO-A2. Their scenarios only use the first one: CO-S12 and CO-S26 both turn on "the agent's first CO-A2".
- The second-call worlds are only CO-S15 (lookup unanswered) and CO-S25 (still open).
- No scenario has the second CO-A2 unanswered and the order then shown cancelled. An agent that treats two attempts as terminal and reports "not cancelled" or stops would leave a cancelled order with no refund and no handoff, and every scenario still passes.
- SG-04 names this world ("took effect late").
- Second-call shipped is equally absent.
Pattern: A lookup-branch row reachable from both attempts is exercised for each branch on only one attempt.
Source: coverage F4
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. CO-S30 and CO-S31 added.

## R2-07 | Ambiguous | Important | Failure row 98, G-02, CO-01 to CO-03
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence:
- The catch-all row requires reproposing every changed order or term (line 98), while CO-01 and CO-02 prohibit proposals for shipped, delivered, cancelled, or unknown orders (lines 62-65), and CO-03 plus its failure row prohibit proposing a customer-selected amount, payment method, or store credit (lines 68 and 97). For example, changing the confirming turn to a shipped order or a new payment method simultaneously requires and forbids the changed proposal.
- Row 98 says "propose the changed proposal"; row 97 says "propose only that" (the original terms). No scenario settles which applies.
- CO-S03 and CO-S27 change only the order number. No scenario changes the amount or payment method in or after the confirming turn, such as "Yes, but put it on my Mastercard". CO-S09 asks for another destination only in Turn 1, before any proposal.
- The policy is user-confirmed: "any change after confirmation voids it" (review-packet.md line 30). An agent that reads the "yes" and cancels, refunding to Visa against the customer's stated wish, passes everything.
Pattern: A compound rule on "any term" conflicts with the rules that forbid some changed proposals, and it is exercised on one term only. Split confirmation-time changes into valid proposal changes that may be reproposed and policy-ineligible changes that must follow CO-01 through CO-03, and exercise the untested terms.
Source: coverage F5 + verdicts F2
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. Row split into an order change and a refund-terms change; CO-S32 and CO-S33 added.

## R2-08 | Ambiguous | Important | Failure rows 89, 107, 112 (read retries)
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence:
- The user's change 4 says "Reads may be retried on timeout without limit" (review-packet.md line 85). Appendix A repeats that CO-A1 may be repeated without limit (line 1837). CO-06 repeats that lookups are not limited.
- CO-01 blocks proposals only when "no lookup ... has answered" (line 62), but the quoted row triggers after any one unanswered lookup (line 89). The same conflict appears after an unanswered CO-A2 (line 107) and after the second unanswered CO-A3 (line 112): an initial lookup timeout followed by a successful retry matches both a terminal failure branch and the successful-result branch.
- CO-S10, S14, S15 and S21 all make every lookup after the trigger fail ("any CO-A1"), so no scenario has a read that fails once and then answers.
- Row 89 also fires literally if a re-read times out after an earlier lookup answered and the customer has confirmed, contradicting the proceed-with-CO-A2 path.
Pattern: An input-declared recovery (retrying reads) has no row and no scenario, and failure scenarios only model permanent outages. Define read-failure branches by whether no retry ever obtains an answer, or state when retrying stops; do not make one timeout terminal while also permitting unlimited retries.
Source: coverage F10 + verdicts F1
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed in the rows: they fire only when no lookup answered. Open: whether the agent must retry and when it stops (question Q1), so no fail-then-answer scenario exists.

## R2-09 | Gap | Important | Failure row 96, CO-S08
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence:
- CO-S08 covers only the holding-back half. Its one User-knows pair is optional and answers "No, I'll keep it."
- No scenario has the customer accept the whole order after a partial request.
- This leaves two wrong behaviours untested: refusing to continue, and treating "ok, cancel all of it" as confirmation and calling CO-A2 with no full proposal, against CO-04.
Pattern: A row whose second half reopens the path ("until the customer...") has a holding-back scenario and no acting scenario.
Source: coverage F6
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. CO-S34 added.

## R2-10 | Gap | Important | CO-04 holding-back side
Quote: "A question about an order, a statement that the customer wants to cancel, or naming which order is not confirmation."
Evidence:
- No scenario has a customer asking a question about an order on an open order, such as "How much would I get back if I cancelled HG-10482?". Every open-order opener in the Data variants and User blocks is a request.
- No scenario has a reply to the proposal that is a question ("Will that go to my Visa?").
- No scenario has an opener that waives confirmation ("just cancel it, no need to ask"). The checklist requires authorization rules to name what looks like authorization and is not (cockburn-checklist.md line 53).
- "Statement" and "naming which order" are exercised (CO-S01, CO-S02). The first-named lookalike is not.
Pattern: A rule lists non-authorizing events and only some have a scenario.
Source: coverage F7
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. CO-S35 and CO-S36 added.

## R2-11 | Gap | Important | CO-03 last clause, Failure handling
Quote: "The agent states no date or time frame by which the refunded money arrives."
Evidence:
- The input is round 3 Q1: "The agent promises nothing about when the money arrives."
- Dimension "No arrival date promised" only observes unprompted statements. In no scenario does the customer ask when the money arrives, and there is no failure row saying what the agent answers.
- The Scope list's "promise a date" is the behaviour most likely to appear when asked directly, and an agent that volunteers nothing but answers "5 to 10 business days" when asked passes all 10 scenarios using the dimension.
- This is separate from M9, which added the clause and dimension but not the provoking case.
Pattern: A prohibition is tested only where nothing provokes it.
Source: coverage F8
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. Failure row and CO-S37 added.

## R2-12 | Gap | Important | CO-02, CO-06, G-01, Failure handling
Quote: "The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation; lookups are not limited."
Evidence:
- No failure row or scenario covers a customer who wants two orders cancelled, either at once ("cancel both", including as the CO-S02 which-order answer) or one after the other.
- CO-02 says "Every proposal names one order number". G-01 limits actions to "the one order the current request is about".
- CO-06's limits are per conversation rather than per order, so a second order's cancellation consumes the first order's retry allowance, and a third is forbidden.
- The inputs give the two-open-orders situation (review-packet.md line 52) and never decide this.
- The Specification-by-Example checklist (line 12) says such a question is recorded as an open question for the user. None is recorded in the sections in scope.
Pattern: A "what if" the inputs leave undecided has no row and no open question, and a limit is scoped by conversation where the rule protects per-order behaviour.
Source: coverage F9
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: open. Only the user can decide (question Q2); the limit in CO-06 is rule text (proposal P3).

## R2-13 | Gap | Important | Failure row 114, CO-S23
Quote: "Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03, that it could not confirm store staff were told, and to contact Harbor Goods customer support."
Evidence:
- The row's message depends on what the agent knows. CO-S23 only tests the failed-refund branch, and dimension "Staff contact unconfirmed reported" is hard-coded to "the order is cancelled, the refund has not been issued".
- No scenario has the double CO-A4 timeout with reason cancellation unknown (after CO-S14 or CO-S15) or refund status unknown (after CO-S21). There the same dimension would be wrong, because saying the order is cancelled would break G-03.
- CO-S22's single retry is also exercised for refund not issued only.
Pattern: A row whose required message varies by state is exercised in one state, with a dimension that cannot be reused for the others.
Source: coverage F11
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. CO-S38 and CO-S39 added, each with its own dimension.

## R2-14 | Gap | Important | Failure row 92, CO-S29
Quote: "Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing."
Evidence:
- CO-S29's orders are only shipped and delivered.
- There is no scenario for a customer whose orders are all cancelled. There, "returns are a separate process" misdescribes the situation and "No open order reported" ("because they have shipped or been delivered") cannot be applied.
- The input ties the returns statement to shipped orders only: "Once shipped, the agent refuses … and tells the customer returns are a separate process" (packet line 43). Row 95 and CO-01 give a cancelled order no returns statement.
- There is no scenario or row for an empty order list with no order named. Following the row literally gives a false reason ("each has shipped...").
- The brainstorm item applies: "the lookup returns more than one plausible match, or none" (cockburn-checklist.md line 64).
Pattern: A row's "none" boundary is covered for one non-empty mix only, and a shipped-only statement is extended to a status the input does not attach it to. The empty set and the third listed status are missing.
Source: coverage F12 + faithfulness F9
Verifier verdicts: A Real, Important; B Real, Nit; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. Reason now depends on status; empty-list row, CO-S41 and CO-S42 added.

## R2-15 | Gap | Important | Failure row 97, CO-03, CO-S09 Data variants
Quote: "the customer asked for the refund to go to a different payment method, as store credit, or in a different amount"
Evidence:
- CO-S09's rows are another card, store credit and PayPal. No row asks for a different amount.
- The user made the amount a rule ("refund amount = order total paid", review-packet.md line 48), and the rule's interest is in §2.
- The Reference trajectory step and scenario wording also address destination only.
- Because `issue_refund(order_number)` takes no amount, state cannot show this failure. Only the agent's words can (for example, agreeing to refund only the mugs' price), so a scenario row is the only place it can be caught.
Pattern: A row clause lists three conditions and the data variants exercise two.
Source: coverage F13
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. CO-S09 row 4 and CO-S32 row 3 added.

## R2-16 | Lies | Nit | CO-S17, CO-S22, CO-S23, Reference trajectory
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence:
- Appendix A (line 1843) has `issue_refund` return `{refund_id, amount, payment_method, status}`, with no reason field. The packet's Refund fields (lines 38 and 46) also have none, and M4 removed `failure_reason`.
- The same result appears at CO-S17 step 6 (line 1071), CO-S22 step 6 (line 1367) and CO-S23 step 6 (line 1426). Each shows a tool result the tool cannot return.
- As a result, the "because …" text in CO-S17 rows 1-3 (lines 1061-1063) and CO-S23 rows 1-2 (lines 1417-1418) is invisible to the agent, so those rows have the same tool outcome. SKILL.md step 3.6 (line 114) allows at most one row that differs only in values or wording.
Pattern: A field removed from the tool contract survives in trajectories and variant rows.
Source: faithfulness F4
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: fixed. Causes removed from trajectories and rows; CO-S17 and CO-S23 rows now differ by order values; CO-S22 line corrected.

## R2-17 | Lies | Nit | CO-03 against failure rows 96-97, CO-S08 and CO-S09 reference trajectories
Quote: "the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: CO-03 requires both statements for every listed request, but the rows and trajectories split them.
- Partial-item requests: row 96 and CO-S08 step 3 (line 555) state only the whole-order part, and "Whole order only explained" grades only that.
- Different-destination requests: row 97 and CO-S09 step 3 (line 610) state only the refund terms.
- Row 96 also says "propose nothing until the customer asks to cancel the whole order", while CO-03 permits the whole-order proposal ("nothing else").
Pattern: A rule and its failure rows state different required behavior for the same condition, and the reference trajectory breaks the rule's literal text.
Source: faithfulness F5
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: open. The fix changes CO-03 rule text (proposal P2).

## R2-18 | Lies | Nit | Failure rows 108, 111 and 112; CO-S16 reference and rows 2-3; mixed sequences
Quote: "| CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund." Also: "the order system reported the payment provider temporarily unavailable for the second CO-A3"
Evidence: The user's case 3 is unconditional on the retry's result: a timed-out refund call means "agent retries once, then re-reads the order and refund records and reports what it finds" (packet line 54), and "after the retry the agent re-reads the refund record" (packet line 63). The spec requires the re-read only when the retry also goes unanswered.
- After a first timeout and an answered retry, CO-S16 rows 2-3 end without a read (lines 1014-1015 pattern), and line 111 hands off with no read.
- Row 111 applies to a first-timeout, second-unavailable sequence, with no re-read and "has not been issued".
- No scenario covers mixed sequences: CO-S18 is unavailable twice, and CO-S19-S21 are timeout twice.
- Idempotency means the results should agree, and Appendix A's effect column makes no refund the only consistent state, so no verdict changes; only the report wording changes.
Pattern: An input's unconditional step is narrowed to one branch without being recorded as a decision; rows keyed on the second call's result ignore the first call's outcome, and no scenario crosses the two.
Source: coverage F16 + faithfulness F6
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: fixed. Row condition widened, and timed-out rows moved from CO-S16 to new CO-S43, which requires the lookup. Round 3 (R3-01) narrowed this row again.

## R2-19 | Lies | Nit | CO-S24, Initial state against the tool outcome
Quote: "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
Evidence:
- The same Initial state says "Order <order> belongs to the customer" (line 1444), and the Final state keeps it with status <status> (line 1461).
- Reference steps 2 and 5 (lines 1478 and 1481) show the same order system listing the order and then not finding it. Any lookup after step 5 still shows it open.
- This is the same kind of self-contradicting world as M2. CO-S11 and CO-S26 avoid it by changing the world at the CO-A2.
- The spec never says how such a world arises, so failure row 101's "could not be found" contradicts what a later lookup would show.
Pattern: An injected failure outcome that the scenario's stated world contradicts.
Source: faithfulness F7
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: answered. OrderNotFound is a user-confirmed outcome (review-packet.md, tool confirmation change 1) and its row needs a scenario.

## R2-20 | Lies | Nit | CO-S20 and CO-S17, Data variants and Final state assertions
Quote: "- <refund final state>"
Evidence:
- CO-S20's row 1 line is "Exactly one refund exists for HG-10482: RF-5531, status failed." Its row 2 line is "No refund exists for HG-10482." (lines 1235-1236). These are different propositions, carried by a column that holds a whole assertion.
- SKILL.md step 3.6 (line 114) requires "identical Required events and final-state lines after substituting row values, so the lines differ only in the values their <column> placeholders take".
- In CO-S17 the same column is identical in all three rows (lines 1061-1063), left over from the removed row 3.
Pattern: A whole-line placeholder gets around the rule that rows must share the same final-state lines.
Source: faithfulness F8
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: fixed. CO-S17 uses a literal line; CO-S20 split into CO-S20 and CO-S40.

## R2-21 | Lies | Nit | CO-S01, Unambiguity note
Quote: "the only check on the agent's words, message check "Refund id reported", is a match on one exact value, the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money."
Evidence: The sentence names a second check on the agent's words right after calling the first the only one. Dimension table lines 1813-1814 list both for CO-S01.
Pattern: An Unambiguity note contradicts the scenario's own dimensions.
Source: faithfulness F10
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: fixed. CO-S01 note corrected.

## R2-22 | Ambiguous | Nit | §5.2 Interaction metrics
Quote: "**Interaction metrics.** For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked. Every User-knows pair is a required question unless marked (optional). Both numbers are reported beside pass/fail and are never folded into the score."
Evidence: Section 5.2 defines how a question matches a User-knows pair (line 1797) but does not define whether the metric counts distinct pairs or question occurrences, how repeated matching questions affect the numerator, or how several questions in one message affect the denominator (line 1805). These choices can produce different recall and precision for the same trajectory. The metrics do not affect pass/fail, so this is a Nit.
Pattern: Define the counting unit and duplicate policy for both numerator and denominator.
Source: verdicts F3
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: answered. This is the template's fixed §5.2 text, which changes only when the user asks; proposed for the template in the report.

## R2-23 | Gap | Nit | Failure row 107
Quote: "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
Evidence: CO-S14 and CO-S15 use only "does not answer". No scenario's lookup answers without the order after M11 merged the branch into this row, and the same Required lines would fit a data variant.
Pattern: A merged compound row has a scenario for one cause only.
Source: coverage F14
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: fixed. CO-S14 row 3 added.

## R2-24 | Gap | Nit | Failure handling (brainstorm items)
Quote: absent
Evidence:
- "The supporting actor answers wrongly" (cockburn-checklist.md line 66): `issue_refund` returns `amount` and `payment_method` (Appendix A), so the agent can detect a refund that differs from the proposal. There is no row and CO-08 would be false.
- "The agent discovers bad or missing internal data" (line 68): an open order that already has a refund, or an order with no total paid or payment method, so no full proposal can be stated. No row covers it.
- No SG in Appendix B guarantees the refund's values.
Pattern: Detectable wrong-answer and bad-data failures have no row.
Source: coverage F15
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: open. No input covers it (question Q4).

## R2-25 | Gap | Nit | Failure rows 98, 99
Quote: "the customer withdrew or stopped answering before confirming"
Evidence:
- "Stopped answering" has no scenario, and §5.2's simulated user cannot go silent. Withdrawal, with the same handling, is covered by CO-S04.
- Row 98's window ends "before CO-A2". No row covers a customer who changes their mind after the cancellation has happened, though no action reverses a cancellation. Brainstorm item: "the user goes silent or changes the request mid-way" (cockburn-checklist.md line 67).
Pattern: User-side brainstorm items are partly undetectable as written, or stop at the commit call with nothing stated afterwards.
Source: coverage F17
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: fixed: "stopped answering" removed from the row because it has no detectable form. Open: a change of mind after cancellation (question Q5).

