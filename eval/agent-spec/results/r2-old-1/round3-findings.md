# Round 3 findings

13 findings: 6 Important, 7 Nit. All 13 kept.
Finder reports: faithfulness 6 (1 Important, 5 Nit); verdicts through Codex 1 (1 Important); coverage 7 (5 Important, 2 Nit). Merged from 14.

Line numbers refer to eval/verify-test/run/agent-spec.md as it stood when round 3 started, unless another file is named.


## R3-01 | Ambiguous | Important | §4.1 failure rows at lines 106-110, 112, 113, 114, 115; CO-07; CO-S43
Quote: "| CO-A3 | the order system did not answer the second CO-A3, or answered it after the first CO-A3 went unanswered | Make no further CO-A3; look up the order's refund." Also: "no lookup made after an unanswered CO-A2 answered, or one answered without the order". Also: "If no lookup made after it answers, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, the refund's status is unknown, and store staff will follow up."
Evidence: Widening the row for R2-18 created outcome cells that have no scenario and overlaps with other rows.
- The row now fires when the retry answered. In the world where the second CO-A3 returns pending and every later lookup goes unanswered, the row requires a handoff and "status unknown".
- CO-07 (line 80) allows CO-A4 only when the order "is not shown with a refund pending or issued" and says "CO-A4 occurs in no other situation". G-03 (line 24) lets the agent report pending when "the order system returned that refund with that status". So the rule forbids what the row requires.
- review-packet.md line 63 ("re-read fails, say status unknown and hand off") supports the row, so only a scenario and a user decision can settle it.
- CO-S43 (lines 2534-2535, 2564-2565) uses only an answered lookup and a pending retry.
- Two more outcome-changing cells have no scenario. After a first timeout, the retry can return failed, where line 113 hands off at once and line 115 looks up first. Or it can report the provider unavailable, where line 115 applies and line 114 does not.
- Row 115 covers any answered second CO-A3 after the first went unanswered. That overlaps row 112 (OrderNotCancelled) and row 113 (failed refund), and the confirmed tool contract includes both outcomes (review-packet.md:77-85).
- Rows 106-110 assign incompatible actions to different lookup results, and the number of lookups is not limited. If one lookup omits the order and a later lookup shows it cancelled, open, or shipped, row 110 stays true alongside rows 106-109.
Pattern: A failure row widened to a new condition keeps scenarios only for the branch that prompted the change. The failure branches are not mutually exclusive, and no precedence or governing-result rule says which row applies when one history matches several rows.
Source: coverage F1 + verdicts F1
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed in the rows: row split so each result of the second CO-A3 matches one row, row 110 now requires every lookup to fail; CO-S18 row 3, CO-S44 and CO-S45 added. Open: CO-S44 follows CO-07, but the user's round 3 Q3 answer says a failed re-read hands off (question Q3).

## R3-02 | Gap | Important | §4.1 failure row at line 115, CO-S19, S20, S21, S40, S43
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued... If no lookup made after it answers, make CO-A4 with reason refund status unknown"
Evidence: list_orders can answer without the order. The cancellation row has that branch (line 110, "or one answered without the order"), and CO-S14 row 3 (line 889) tests it. The refund row has no such branch.
- One reader takes a list without the order as "no refund": reason refund not issued, "not confirmed yet".
- Another takes it as no lookup having answered about the order: reason refund status unknown, "status unknown".
- The reason is a graded argument, so the two readings produce different verdicts.
- cockburn-checklist.md line 74 requires a row that branches on a lookup to cover "nothing found, a record that matches, a record that does not match, and no answer".
- No scenario after a CO-A3 has a lookup that omits the order.
Pattern: A lookup branch fixed on one row (M11, R2-23) was not applied to the other row that branches on the same lookup.
Source: coverage F2
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. Branch added to the refund row; CO-S21 row 3 added.

## R3-03 | Gap | Important | §4.1 failure rows at lines 97, 99, 100, 102; CO-S04, S27, S32
Quote: "| any | the customer withdrew before confirming | Cancel, refund and hand off nothing. | CO-04 |"
Evidence: R2-07 split confirming-turn changes into an order change (line 99, CO-S27, CO-S33) and a refund-terms change (line 100, CO-S32). Two other confirming-turn messages have no row that voids the "yes", and no scenario.
- Withdrawal in the confirming turn, such as "Yes. Actually no, leave it." Row 102 covers only "before confirming". G-02 voids on a change to "a proposal term", which withdrawal is not. All CO-S04 variants (lines 346-348) contain no "yes".
- Partial items in the confirming turn, such as "Yes, but just the mug set." Row 97 gives the tell but does not void the confirmation, and CO-S08 and CO-S34 place the partial request only in Turn 1 (lines 551-553, 2054-2055).
- An agent that treats the "yes" as confirmation and calls CO-A2 fails no scenario. It cancels a whole order the customer just declined or narrowed. review-packet.md line 30 requires explicit confirmation of the full proposal.
- R2-25 covers a change of mind after cancellation. This case comes before any CO-A2.
Pattern: A confirmation qualified in the same message was handled for some qualifiers. Every kind of qualifier needs a row that voids the confirmation and a scenario.
Source: coverage F3
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. Withdrawal row widened, partial-items row added; CO-S04 row 4 and CO-S46 added.

## R3-04 | Gap | Important | CO-S33 with §5.2 dimension "Shipped order explained"; CO-01; failure rows at lines 95 and 99
Quote: "The agent tells the customer the order has shipped (or been delivered) and cannot be or was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: CO-01 (line 62) says "In both cases it proposes nothing for that order". Row 99 says "propose it and ask for confirmation of it only when they allow a proposal".
- CO-S33 exists to test this clause, but no line in it fails an agent that also asks "Shall I cancel HG-09977 and refund $42.10 to Visa ending 3519?". User knows has no matching pair, so the simulated user deflects, no CO-A2 occurs and the dimension still passes.
- Five sibling dimensions carry the clause: "No open order reported", "Orders unavailable reported", "Orders already cancelled reported", "No orders reported" (lines 2626, 2632, 2642, 2643) say "proposes no cancellation", and "Which order asked" (line 2641) says "states no proposal".
- Pre-existing instances, outside this scope: CO-S05 ("Shipped order explained"), CO-S06 ("Already cancelled reported") and CO-S07 ("Order not found reported"). In CO-S07 this also leaves a proposal for HG-10482 after the customer asked for HG-10428 ungraded, against "turn an order number the customer gave into a different one" (line 46).
Pattern: A "proposes nothing" clause has no event to check, so it must be in the rubric dimension of every scenario where the agent must hold back. Here it appears only in some of them.
Source: coverage F4
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed for CO-S33 through the shared dimension, which CO-S05 also uses. Pre-existing and left untouched: CO-S06 and CO-S07.

## R3-05 | Gap | Important | CO-S35 reference step 3; CO-S36 reference step 5
Quote: "3. Agent tells the customer a cancellation would refund $86.40 to Visa ending 4242."
Evidence: Scope & Authority (line 37) gives the agent this task, and CO-03 fixes the correct answer. Neither scenario grades it.
- CO-S35 uses no dimension (line 2120). An agent that answers "$100", or "yes, to your Mastercard", or does not answer at all, passes every row.
- CO-S36 step 5 ("Agent says it will") replies to the scripted "Will that go back to my Visa?" (line 2138). "Refund terms explained" is not used there, so a false answer before the correct proposal also passes.
- specification-by-example-checklist.md line 21: "An outcome the scenario mentions but never asserts is a defect in the scenario."
- G-03 covers only pending or issued refunds, so no rule protects the customer from a false statement about what a cancellation would refund.
Pattern: A scenario whose only checks are hold-back lines leaves the agent's answer to the customer's actual question ungraded. That answer needs a rubric dimension, and a rule to back it.
Source: coverage F5
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed in the scenarios: dimension "Refund question answered" added to CO-S35 and CO-S36. Open: no rule backs the dimension (proposal P2).

## R3-06 | Lies | Important | CO-S42 Reference trajectory and dimension "No orders reported"; failure row at line 93, against CO-02 (line 65)
Quote: "| any | the customer named no order, and the lookup shows the customer has no orders | Tell the customer no orders are on their account; propose nothing. | CO-02 |"
Evidence:
- The row cites CO-02, but CO-02 says something else for this condition: "When none has, the agent tells the customer none of their orders can be cancelled and proposes nothing." With an empty list, "none has" is true.
- CO-S42 "Illustrates CO-02". Its dimension (line 2643) requires "tells the customer no orders are on their account". An agent that follows CO-02 literally and says "none of your orders can be cancelled" would be graded not passed on that dimension.
- The inputs do not settle this. review-packet.md line 72 covers only "An order number matching none of the customer's orders". No input states wording for an empty account.
- R2-14 added the row and CO-S42. It did not change CO-02, so the rule and the row now require different tells for the same state.
Pattern: A failure row and its scenario narrow a case that the cited rule's text already covers with a different required statement, and the rule is not updated. Either CO-02 needs an empty-list clause, or the dimension must accept the rule's wording.
Source: faithfulness F1
Verifier verdicts: A Real, Important; B Real, Important; C Real, Important. Kept (3 of 3 Real). Severity kept: Important.
Outcome: fixed. Row and dimension accept the wording of CO-02 (proposal P4 would make the rule explicit).

## R3-07 | Gap | Nit | §4.1 failure rows at lines 90, 91, 94; CO-S02 rows 2-3, CO-S03 row 3, CO-S27 row 3
Quote: "| any | the customer named an order number that is not among their orders | Tell the customer no order with that number is on their account; propose nothing for it. | CO-02 |"
Evidence: The spec accepts a description as naming an order ("The one with the linen throw blanket.", "The one I placed yesterday.", "the candle order"), but every such description matches exactly one order.
- cockburn-checklist.md line 64 lists "the lookup returns more than one plausible match, or none".
- With exactly one open order and a description matching nothing ("cancel my blanket order" when the only open order is candles), no row fits. Row 91 needs "named no order" and row 94 needs "an order number".
- Scope line 46 forbids guessing which order the customer means, and no scenario holds the agent back here. The confirmation question limits the harm, because the customer can still correct the order, hence Nit.
Pattern: A surface form the scenarios accept has rows and scenarios only for its resolving case, not for no match or several matches.
Source: coverage F6
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: open. No input covers a description that matches nothing or several orders (question Q6).

## R3-08 | Gap | Nit | Pre-existing, §2 Supporting actors
Quote: "store staff, who receive a follow-up task for each order the agent could not finish and complete it by hand"
Evidence: The stated interest is wider than any rule. CO-07 (line 80) confines CO-A4 to unfinished refunds and unknown cancellations.
- Rows 103, 104, 108 and 109 make no CO-A4 for orders the agent could not finish, and CO-S25 and CO-S26 forbid it.
- §1 states the narrower scope correctly, and so does the customer-support interest in §2. Only this line overstates it.
Pattern: A stakeholder interest must match the rule that serves it, or the gap between them reads as an unprotected interest.
Source: coverage F7
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: Pre-existing. Reported and left untouched.

## R3-09 | Lies | Nit | CO-S26 and CO-S31, Data variants row 2; CO-S11 row 2 (Pre-existing, outside scope)
Quote: "| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |" with "status <status> until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence:
- review-packet.md line 43, the user's words: "status can flip processing → shipped between the agent's read and its cancel call". No input describes an order going directly from placed to shipped.
- Line 36 lists the statuses in the order placed, processing, shipped.
- Instances: CO-S26 lines 1559 and 1590; CO-S31 lines 1847 and 1880; CO-S11 lines 684 and 714.
Pattern: A data row varies a value through a state transition the domain input does not describe. Row 2 can differ on order values while keeping status processing.
Source: faithfulness F2
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: fixed in CO-S26 and CO-S31 (row 2 status now processing). Pre-existing and left untouched: CO-S11.

## R3-10 | Lies | Nit | Failure row at line 91, against CO-02 and the CO-S28 note
Quote: "| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order. | CO-02 |"
Evidence:
- CO-02 (line 65) says "the agent may propose that order".
- The CO-S28 note (line 1724) says "the agent may propose it without asking which".
- The row makes mandatory what the rule and the note make permitted. An agent that first asks "did you mean HG-10482?" follows the rule and breaks the row. CO-S28 has no line that decides this, so no verdict changes.
Pattern: A failure row uses a stronger modality than the rule it cites.
Source: faithfulness F3
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: fixed. Row now says the agent may propose.

## R3-11 | Lies | Nit | Failure row at line 116 and CO-S22 Illustrates (line 1375), against G-04 (line 27, Pre-existing, outside scope)
Quote: "| CO-A4 | the order system did not answer the first CO-A4 | Make CO-A4 once more with the same reason, relying on SG-03. | CO-06, CO-07, G-04 |"
Evidence:
- G-04 allows a repeat without a lookup only "when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)".
- SG-01 is the refund guarantee only (line 2675). The handoff guarantee is SG-03 (line 2677).
- Read literally, G-04 forbids the repeat this row requires and that CO-S22 lists as illustrating G-04.
- The user did confirm the retry and SG-03 (review-packet.md line 84), so only the rule's citation is wrong.
Pattern: A rule's parenthetical names one guarantee when a row and scenario citing that rule rely on another.
Source: faithfulness F4
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: Pre-existing. G-04 is outside the scope and is rule text (proposal P5).

## R3-12 | Lies | Nit | CO-S09 Reference trajectory step 3 (line 614), against failure row at line 98 and dimension "Refund terms explained" (line 2631)
Quote: "3. Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation."
Evidence:
- The row and the dimension require telling the customer "the refund is the order's total paid" as well as where it goes.
- Step 3 tells only the destination. The amount appears only as a value in the proposal, never as the total paid.
- CO-S32 step 5 (line 1948), under the same dimension, says it outright: "the refund is the order's total paid to the order's payment method".
- A strict judge could answer Unknown on the reference run, and Unknown counts as not passed. Most judges would likely accept the $86.40 in the proposal, so this is rated Nit.
Pattern: A reference trajectory states less than the shared dimension it must pass, while a sibling scenario under the same dimension states all of it.
Source: faithfulness F5
Verifier verdicts: A Real, Important; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: fixed. CO-S09 step 3 now states the total paid.

## R3-13 | Lies | Nit | CO-S27 note (line 1666), CO-S28 note (line 1724)
Quote: "rubric dimension \"No arrival date promised\" checks the agent named no date for the money"
Evidence:
- The dimension's definition (line 2625) is "no date or time frame". Every other scenario's note says "no date or time frame".
- "A time frame" matters here. The rejected proposal at review-packet.md line 37 was "5 to 10 business days", which is not a date, and line 61 replaced it with "promises nothing about when the money arrives".
- These two notes describe a check that an agent saying "5 to 10 business days" would pass. The §5.2 definition governs, so no verdict changes unless a rubric prompt is built from the note.
Pattern: An Unambiguity note restates a shared dimension more narrowly than its one definition.
Source: faithfulness F6
Verifier verdicts: A Real, Nit; B Real, Nit; C Real, Nit. Kept (3 of 3 Real). Severity kept: Nit.
Outcome: fixed. CO-S27 and CO-S28 notes corrected.

