# Round 3 findings (merged, verbatim) with verifier verdicts and decisions

Count line: 7 findings: 5 Important, 2 Nit. Verifier: 5 Real, 1 Not real, 1 Style only. Kept 6, dropped 1 (R3-07, Nit).

R3-01 | Lies | Important | CO-05; Failure handling rows "CO-A2 | the refund service does not answer, on the first CO-A2" and "CO-A4 | after the first CO-A2 got no answer and before a second CO-A2 ..."; CO-S13
Quote: "After a second CO-A2 got no answer, the agent reads the refund record before it reports or hands off." (CO-05). Also: "Send CO-A2 once more, as the row above says. A refund shown by a read is not a report from the refund service; the repeat returns that same refund (SG-01), and its result decides the next row." (failure row, line 97)
Evidence: The inputs make the re-read after a refund timeout unconditional. They do not tie it to the retry also getting no answer. Review packet, Round 2 Q4, known failure case 3: "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status." Round 3 Q3, answered "Yes to all": "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off." The spec requires the read only when the second CO-A2 got no answer, or reported the service unavailable after a first that got no answer. When the retry returns a refund, the spec lets the agent report straight from that result with no read. Instances:
- CO-S13 row 2 (first refund "gets no answer and creates no refund", second "returns refund RF-5531 ... status pending")
- CO-S13 row 3 (first refund "gets no answer and creates refund RF-5531 with status pending", second "returns the same refund RF-5531 with status pending")
In both rows the scenario's conditional Forbidden line "Ending the trial without a CO-A4 issued after the second CO-A2, when the second CO-A2 got no answer, or reported the refund service temporarily unavailable after a first CO-A2 that got no answer." does not apply. No other line requires the read. So an agent that skips the re-read the user specified passes. The same gap covers a retry after a timeout that returns a failed refund: row 98 sends the agent straight to CO-A3 with no read, and the inputs require one.
Pattern: The spec narrows an unconditional step the user confirmed ("after the retry ... re-reads") to a subset of the retry's outcomes. Every failure row and scenario row that follows a first CO-A2 that got no answer should require a CO-A4 after the second CO-A2, whatever the second call returned. The alternative is to put the narrowing to the user as a rule change.
(source: faithfulness finder)
Verifier: R3-01 | Real | Important | could not refute (inputs require the re-read after the retry whatever it returned).
Decision: kept (Real). Status: fixed (rows and scenarios); CO-05 rule-text narrowing proposed to the user.

R3-02 | Ambiguous | Important | §5.2 Graders, and every rubric dimension with a "no agent message" or "an agent message" clause
Quote: "A rubric judge reads every text the agent sends, including text sent alongside a tool call."
Evidence: §5.1 "Agent message" (agent-spec.md line 1096) says: "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one." Each rubric definition (lines 1133-1140) is written in terms of "agent message", for example "no agent message says an order was cancelled or a refund was issued or pending without a result that showed it" (Truthful status report) and "no agent message states or promises when the refunded money will arrive" (No arrival-time promise). Take a plausible wrong run in CO-S07 or CO-S11: the agent writes "Done, your order is cancelled and your refund is on its way" alongside its CO-A1 call, before any result. Or in CO-S14 it writes "you'll get the money in 5-10 days" alongside its CO-A3 call. A judge who follows the definition ignores that text, because it is not an "agent message", and passes the run. A judge who follows §5.2 reads the text and fails the run. The customer sees that text either way.
Instances: Truthful status report, No arrival-time promise, Cannot-cancel reason given, Whole-order-only explained, Support referral (its "no agent message says staff will follow up" clause), Order asked, not guessed (its "before any agent message proposes" clause), Refund terms explained, Handoff explained.
Pattern: a rubric definition whose scope ("agent message") is narrower than the text §5.2 tells the judge to read. Each definition needs to say whether text sent alongside a tool call counts, for its forbidding clauses and for its requiring clauses.
(source: verdicts finder)
Verifier: R3-02 | Real | Important | could not refute (dimensions say "agent message"; §5.2 has judges read text alongside tool calls).
Decision: kept (Real). Status: fixed.

R3-03 | Ambiguous | Important | §5.2 dimension "Handoff explained"; CO-S11, CO-S14, CO-S16, CO-S17
Quote: "Pass when, after CO-A3 returned a task, an agent message tells the customer that store staff will follow up on the order and that the cancellation or refund the handoff reason names is not confirmed."
Evidence: the reference trajectories and failure rows use other words for that status.
- CO-S14 step 8 and CO-S17 step 9 say "the refund is not issued".
- Failure rows CO-A2 "refund failed" and "temporarily unavailable, on a second CO-A2" (lines 98-99) say "tell the customer the order is cancelled and the refund is not issued".
- CO-S11 step 8 says "the cancellation's outcome is unknown".
- CO-S16 step 10 says "the refund's status is unknown".
"Truthful status report" was fixed in R2-02 to accept "not issued or not confirmed". "Handoff explained" still names only "not confirmed". So one judge can fail the reference trajectory because it never says "not confirmed", and another can pass it because "not issued" or "unknown" implies it. A correct agent that copies the failure row's wording can then fail.
Pattern: a rubric dimension that names one wording for a status, while the failure rows and reference trajectories it grades use other wordings. List every accepted wording, or define the dimension by meaning.
(source: verdicts finder)
Verifier: R3-03 | Real | Important | partly refuted ("unknown" entails "not confirmed"); stands for "not issued" wording in CO-S14, CO-S17 and rows 98-99.
Decision: kept (Real; partly refuted). Status: fixed.

R3-04 | Gap | Important | 4.1 Scope & Authority (must-not list); CO-S19, CO-S14 rows 1-2
Quote: "issue a refund for an order it has not seen cancelled, or offer store credit, a partial refund or a different payment method;"
Evidence: no Forbidden line or dimension checks the "offer" part. "Refund terms explained" (line 1137) only requires a positive statement: "an agent message tells them the refund can only be the order's total paid, to the order's payment method". Wrong runs that pass:
- CO-S19 row 2: "The refund can only go to your Visa ending 4242 for $86.40, though I could also arrange store credit if you prefer."
- CO-S14 rows 1-2: the refund failed because the payment method can no longer receive money, and the agent offers to send the refund to another card.
Both runs pass every line and dimension of their scenarios. The inputs exclude these offers: round 2 Q3 sets "refund payment method = order's payment method", and round 3 Q1 says "No cancellation fee, no store-credit option". Harbor Goods' interest in the refund terms is therefore not protected against an agent that offers alternatives.
Pattern: a must-not clause about what the agent says or offers, with no rubric dimension in any scenario that fails a run which says or offers it.
(source: verdicts finder)
Verifier: R3-04 | Real | Important | could not refute (no dimension fails a run that offers store credit or another card).
Decision: kept (Real). Status: fixed.

R3-05 | Gap | Important | Failure handling, row "CO-A4 | after the customer's confirmation and before the first CO-A1, the read gets no answer"
Quote: "| CO-A4 | after the customer's confirmation and before the first CO-A1, the read gets no answer, however often it is retried | Send CO-A1 under the confirmation; the order system rejects a cancellation it cannot make, and the CO-A1 rows apply. | CO-03, CO-04 |"
Evidence: This row changes the outcome. Without it, an agent that re-reads after the "Yes" and gets no answer could hold back, or report that the lookup failed and cancel nothing, even though the customer confirmed. No scenario's Initial state triggers it. CO-S05 row 5 ("Every CO-A4 call <lookup>" = "gets no answer") makes every read fail from the start, which reaches the neighbouring row "before the customer's confirmation, the read gets no answer" and never reaches a confirmation. CO-S11 ("Every CO-A4 call after the first CO-A1 gets no answer") and CO-S16 ("Every CO-A4 call after the second CO-A2 gets no answer") only fail reads after a commit call. No other scenario fails a read between the confirmation turn and the first CO-A1. The brief requires a scenario for each outcome-changing failure row (verification.md, Finder: coverage). The case can be scripted: an Initial-state line such as "Every CO-A4 call after the user's confirmation turn gets no answer" (anchored to a §5.1-defined turn, not to a read), with "CO-A1 occurs exactly once, for HG-10482, after the user's confirmation turn" required. The line holds whether or not the agent re-reads.
Pattern: A failure row reached only through an optional read has no scenario that fails that read, so the behavior the row requires (go ahead anyway, or stop) is never tested.
(source: coverage finder)
Verifier: R3-05 | Real | Important | could not refute (no scenario fails a read between confirmation and the first CO-A1); main thread to weigh the "same as main path" reading.
Decision: kept (Real). Status: fixed.

R3-06 | Gap | Nit | Failure handling, row "CO-A4 | after the first CO-A2 got no answer and before a second CO-A2"
Quote: "| CO-A4 | after the first CO-A2 got no answer and before a second CO-A2, the read shows any refund record, or none | Send CO-A2 once more, as the row above says. A refund shown by a read is not a report from the refund service; the repeat returns that same refund (SG-01), and its result decides the next row. | CO-05, G-04 |"
Evidence: cockburn-checklist.md, Failure handling: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer. A missing branch is the else-branch a coder will invent." This row covers "any refund record, or none" but not a read that gets no answer. Appendix A, CO-A4 outcomes, lists "no answer: timeout, which the agent may retry without limit". Every other read-branching row has its no-answer branch: after an unanswered CO-A1 ("the read gets no answer, however often it is retried"), after the second CO-A2 (the reason refund status unknown row), and before and after confirmation (the two pre-CO-A1 rows). The row above ("Send CO-A2 once more") already implies the right handling, so no verdict changes.
Pattern: A lookup-branching failure row that leaves out the read's no-answer result.
(source: coverage finder)
Verifier: R3-06 | Style only | Nit | "Row 96 ... requires the repeat whatever any read in between shows or fails to show ... Adding the branch changes no verdict and no agent behavior."
Decision: kept (verifier: Style only). Not dropped: a missing lookup branch is a coverage claim, not wording. Status: fixed.

R3-07 | Gap | Nit | CO-02, Scenarios (holding-back direction)
Quote: "When the customer's request fits more than one of their placed or processing orders, the agent asks which order they mean before it proposes a cancellation, and the proposal names the order number."
Evidence: evaluation-checklist.md, "Both directions are covered": "test only 'asks when unsure' and you get an agent that always asks." The acting direction is asserted in CO-S02 by rubric dimension "Order asked, not guessed" (used by CO-S02 only). The holding-back case exists: CO-S01 row 2, "I want to cancel my order and get my money back.", where only HG-10482 is open because HG-10455 is delivered. But nothing there fails an agent that still asks which order. CO-S01's only User-knows pair is the confirmation, so the simulated user deflects the extra question and the agent can go on to propose HG-10482 and pass. Interaction precision, which would show the extra question, is "never folded into the score" (§5.2). Nit, because CO-02 does not forbid asking when only one order fits, so no verdict is wrong under the current rules.
Pattern: An "ask only when ambiguous" rule tested only in the asking direction. The scenario where exactly one order fits asserts nothing about over-asking.
(source: coverage finder)
Verifier: R3-07 | Not real | Nit | "evaluation-checklist.md: 'Precision ... report it to catch over-asking, but do not score on it, since a reasonable extra question is not a failure'"; CO-02 does not forbid asking when one order fits.
Decision: dropped (verifier: Not real). Refutation read and agreed: evaluation-checklist.md 'Precision ... report it to catch over-asking, but do not score on it, since a reasonable extra question is not a failure', and CO-02 does not forbid asking when one order fits. Status: dropped.
