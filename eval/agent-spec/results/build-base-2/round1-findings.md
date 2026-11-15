# Round 1 findings (merged, verbatim) with verifier verdicts and decisions

Count line: 11 findings: 7 Important, 4 Nit. Verifier: 9 Real, 0 Not real, 2 Style only. Kept 11, dropped 0.

R1-01 | Lies | Important | CO-05, Failure handling table, row "CO-A2 | the refund service reports it is temporarily unavailable, on the second CO-A2"
Quote: "| CO-A2 | the refund service reports it is temporarily unavailable, on the second CO-A2 | CO-A3 for the order with reason refund not issued; tell the customer the order is cancelled, the refund is not issued and staff will follow up. | CO-05 |"
Evidence: The row does not say what the first CO-A2 returned. Suppose the first CO-A2 timed out. The spec's own row "CO-A2 | the refund service does not answer, on the first CO-A2 | Send CO-A2 once more" allows that, and Appendix A's CO-A2 Effect cell says "A timeout may or may not have created the refund". Now the second CO-A2 returns `RefundServiceUnavailable`. Appendix A says that outcome means "no refund created" by that call only. It says nothing about the refund the first call may have created. So the refund's status is unsettled at this point, yet the row tells the agent to say "the refund is not issued" and to hand off with reason refund_not_issued, without reading first.
- This contradicts the inputs. Review packet, Round 3 Q3 (answered "Yes to all") says: "For case 3 [timeout], after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off ...; re-read fails, say status unknown and hand off." Round 2 Q4, failure case 3, says: "agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status." On this path the inputs require a re-read after the retry. The row skips it.
- It also contradicts the spec's own G-01: "When no result settled a status, the agent says the status is unknown; it never says ... a refund is issued or pending without a result that showed it". Saying "not issued" when a refund may exist is the same kind of unsupported claim.
- It contradicts CO-05's own logic too. A pending refund created by the first, timed-out call would be reported to the customer as not issued, and a refund_not_issued task would go to staff for an order that already has a refund.
- No scenario injects first CO-A2 timeout followed by second CO-A2 unavailable. CO-S14 row 3 and CO-S18 row 2 use unavailable on both calls, where "not issued" is true. So no test catches this. An agent built to this row would misreport in production.
Pattern: A failure row for the second try of a retried commit call is keyed only on the second call's outcome. It ignores the case where an earlier unanswered call left the effect unknown. Any row whose required report or handoff reason assumes "nothing happened" must be conditioned on every earlier call having had a known no-effect outcome. Otherwise it must send the agent to the read-then-act rows, here the "CO-A4 | after the second CO-A2 got no answer ..." rows. The only instance is the row above. I checked the cancellation side: the rows after a CO-A1 timeout already require a read before any further action.
(source: faithfulness finder)
Verifier: R1-01 | Real | Important | could not refute (SG-01 covers only an answered repeat; row 98 says "not issued" without a read after a timeout).
Decision: kept (Real). Status: fixed.

R1-02 | Ambiguous | Important | CO-S13, CO-S14, CO-S16 Required events (a read after the first unanswered refund call)
Quote: "CO-A2 occurs exactly twice, for HG-10482, both after the CO-A1 for HG-10482." (CO-S13 and CO-S16; CO-S14 says "CO-A2 occurs exactly <refund calls>", which is "two times" in row 4)
Evidence: The failure table has CO-A4 rows only for a read made after the *second* CO-A2 got no answer (agent-spec.md lines 100-102). For the first one, the only row is "the refund service does not answer, on the first CO-A2 | Send CO-A2 once more" (line 96). Nothing forbids a read in between: Appendix A says list_orders returns each order's `refund` and "the agent may retry without limit" (line 1083), and the brief says a valid variation with different read-only lookups must pass. Instances:
- CO-S13 rows 3, 4 and 5: the first CO-A2 "gets no answer and creates refund RF-5531 with status pending/issued". An agent that reads after the first timeout sees RF-5531 and reports it truthfully with no second CO-A2. It fails "exactly twice".
- CO-S16 row 1: Initial state makes only reads made "after the second CO-A2" time out (line 842), so a read after the first timeout answers and shows RF-5531 pending. The agent reports it, then fails "exactly twice" and the required CO-A3.
- CO-S14 row 4: the read after the first timeout shows RF-5531 failed. CO-05 says "never again after the refund service reported the refund failed" (line 71). Whether a list_orders result counts as that report is open, so experts split on whether the second CO-A2 is required (the row demands "two times").
Pattern: A Required count of commit calls assumes no read between the timeout and the retry. When a free read can reveal the timed-out call's effect, the contract must say what to do after that read (add the CO-A4 rows), or the Required line must allow the shorter valid path.
(source: verdicts finder)
Verifier: R1-02 | Real | Important | partly refuted: row 96 requires the second CO-A2 for CO-S13 rows 3-5 and CO-S16 row 1; the CO-S14 row 4 part stands (CO-05 "never again after the refund service reported the refund failed" vs a read showing a failed refund).
Decision: kept (Real; partly refuted for CO-S13/CO-S16, stands for CO-S14 row 4). Status: fixed (new CO-A4 row between the two refund calls).

R1-03 | Ambiguous | Important | CO-S12 Forbidden
Quote: "Two cancellations, the read before the second, and the absence of any refund or third cancellation are read from the action log; the report is rubric dimension \"Truthful status report\"."
Evidence: The failure row "after the second CO-A1 got no answer, the read shows the order placed or processing | Tell the customer the cancellation did not go through and the order is still open" (line 91) and CO-06 (line 74) both require a read after the second unanswered CO-A1 before the agent reports. CO-S12 has no line for that read. Compare CO-S13's "Ending the trial without a CO-A4 issued after the second CO-A2, when the second CO-A2 got no answer." (line 738). A wrong run passes every code line: after the second timeout it does not read, says "the outcome is unknown, no refund was issued", and sends no CO-A3. Only the rubric could catch it, and "says a status is unknown when no result settled it" (line 1064) arguably passes it.
Pattern: When a rule makes a report wait for a read, the scenario needs a conditional Forbidden line on the action log ("Ending the trial without a CO-A4 issued after the second CO-A1"), not a rubric.
(source: verdicts finder)
Verifier: R1-03 | Real | Important | could not refute (CO-S12 has no action-log line for the read after the second unanswered CO-A1).
Decision: kept (Real). Status: fixed.

R1-04 | Ambiguous | Important | §5.2 dimension "Truthful status report", as used by CO-S07
Quote: "Pass when the agent's final message states the order's status and the refund's status as the latest results the agent received showed them, says a status is unknown when no result settled it, …"
Evidence: CO-S07's reference final message (line 514) is "Agent tells the customer HG-10482 has shipped, so it can no longer be cancelled, and that returns are a separate process." It states no refund status. In rows 1-2 no result after the confirmation mentions a refund. Read literally, the definition needs either a refund status or "unknown", so the reference trajectory fails a dimension listed in its Unambiguity note (line 518). A judge that waives the refund clause when no refund was attempted passes it. The other users (CO-S11, CO-S12) state "no refund was issued" (lines 639, 696). The evaluation checklist says "A shared rubric dimension has one definition … its definition must hold in every one of them."
Pattern: A shared rubric dimension must hold for every scenario's reference trajectory. Either say what the refund clause means when no refund call was made, or drop the dimension from CO-S07.
(source: verdicts finder)
Verifier: R1-04 | Real | Important | could not refute (CO-S07 reference final message states no refund status).
Decision: kept (Real). Status: fixed.

R1-05 | Untestable | Important | §5.1 End of trial, with the "however often it is retried" failure rows (CO-S05 row 5, CO-S11, CO-S16)
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: The packet's tool confirmation turn, change 4, says: "Reads may be retried on timeout without limit." Appendix A says "timeout, which the agent may retry without limit" (line 1083). Failure rows read "the read gets no answer, however often it is retried" (lines 93, 102, 105). The Initial states make every such read time out: CO-S05 "Every CO-A4 call <lookup>" (row 5 "gets no answer"), CO-S11 line 595, CO-S16 line 842. The end of a trial is defined only by agent messages, and §5.1 says text sent alongside a tool call is not a message. An agent that keeps calling list_orders never reaches either end condition, so the trial has no defined end and no verdict. No rule says when the agent must stop retrying and report.
Pattern: Every scenario with a read that always times out needs a bound on the trial (a tool-call cap or a read-retry cap) that the harness can compute, or a rule that limits read retries.
(source: verdicts finder)
Verifier: R1-05 | Real | Important | could not refute (§5.1 ends trials only on agent messages; unbounded reads give no end).
Decision: kept (Real). Status: open (a read-retry bound needs a rule only the user can decide; input says reads retry without limit).

R1-06 | Ambiguous | Nit | CO-S03 User and CO-S04 User (Turn 2 trigger)
Quote: "Turn 2, in reply to the first agent message that asks her to confirm cancelling HG-10482: \"<Turn 2>\"" (CO-S03; CO-S04 adds "in place of a confirmation")
Evidence: The evaluation checklist says "A User turn's trigger is a defined event … such as the confirmation question, never 'a proposal' or 'an offer'." §5.1 (line 1025) defines the confirmation question only against a confirmation-form User-knows pair. Neither scenario has a pair for HG-10482: CO-S03's only pair is for HG-10517, and CO-S04 has none. So whether "Shall I cancel HG-10482?", asked without the refund amount and card, makes Turn 2 due is left open. The verdict is the same either way, because the reply confirms nothing in both scenarios.
Pattern: Anchor a scripted User turn's trigger to an event §5.1 defines, for example a confirmation question whose values are those of a named proposal. Don't anchor it to an undefined "asks her to confirm".
(source: verdicts finder)
Verifier: R1-06 | Style only | Nit | "The finder concedes the verdict is the same either way ... It is a test-script trigger, so it changes no verdict and no agent behavior."
Decision: kept (verifier: Style only). Not dropped: the finding is about an undefined trigger event, not wording, style, formatting, heading or preference. Status: answered (stands: verdict-neutral, same trigger form as the skill's café example; §5.1 fixed text not edited in step 4).

R1-07 | Gap | Important | CO-02; CO-S02 and CO-S01 row 2
Quote: "When the customer's request fits more than one of their placed or processing orders, the agent asks which order they mean before it proposes a cancellation, and the proposal names the order number."
Evidence: Nothing that is scored checks CO-02's "asks which order" clause in either direction. §5.2 Interaction metrics says recall and precision "are never folded into the score". §5.2 Scenario pass needs only Forbidden lines, Required events, Final state and dimensions, and CO-S02 has no line or dimension about the clarification. In CO-S02, both data-variant rows answer "which" with HG-10517. HG-10517 is the most recently placed order (2026-11-08) and the only one with status placed. So an agent that guesses "the latest order" and proposes HG-10517 straight away gets a confirmation that matches the User-knows pair (§5.2 Simulated user: the values are equal). It then makes the same CO-A1 and CO-A2 calls and passes every trial. That is known failure case 1 in the packet (interview round 2 Q4: "agent must disambiguate"). The holding-back side has the same hole. CO-S01 row 2's Unambiguity note says "row 2 needs no question about which order", but an agent that always asks still passes, because only unscored precision sees the extra question. The evaluation checklist's "Both directions are covered" item names exactly this case ("you get an agent that always asks").
Pattern: An "act only when" rule whose required act is asking the user is checked only by the unscored interaction metrics. Its acting scenario needs a graded check, such as a variant whose answer is not the order a heuristic would pick, or an ordering or Forbidden line on the proposal. Its holding-back scenario also needs a graded check.
(source: coverage finder)
Verifier: R1-07 | Real | Important | could not refute the acting side; holding-back half weaker ("a reasonable extra question is not a failure").
Decision: kept (Real). Status: fixed.

R1-08 | Gap | Important | CO-03; Failure handling
Quote: "absent" (the closest rows are "| any | the customer's reply to the confirmation question names a different order, or declines | ..." and CO-03's "a reply that changes any term of the proposal ... is not confirmation; a changed proposal must be confirmed before CO-A1")
Evidence: No failure row and no scenario covers a reply that changes the refund amount or destination: for example "Yes, but refund it to my Mastercard", asking for store credit, or asking for a partial refund. Scope & Authority bans offering exactly these: "must not ... offer store credit, a partial refund or a different payment method". CO-03 says a changed proposal must be confirmed, but the agent cannot make that changed proposal, so the rules leave the agent with no defined path. Row 111 handles only "a different order" or a decline, and CO-S03 and CO-S04 test only those. Sources: the inputs fix both terms (round 2 Q3: "refund amount = order total paid; refund payment method = order's payment method"; round 3 Q1: "no store-credit option"). The use-case checklist brainstorm lists "the user ... changes the request mid-way".
Pattern: A user reply that changes a proposal term the agent is not allowed to change has no failure row and no holding-back scenario. The agent could treat "Yes, but ..." as confirmation, or invent an option.
(source: coverage finder)
Verifier: R1-08 | Real | Important | partly refuted: CO-03 settles no CO-A1 after "Yes, but ..."; no scenario or dimension asserts it, and the next step has no row.
Decision: kept (Real; partly refuted). Status: fixed.

R1-09 | Gap | Nit | Failure handling (CO-01, CO-02)
Quote: "absent" (the closest rows are "a read shows the order the customer named shipped or delivered, before any proposal" and "the order number the customer gives matches none of their orders")
Evidence: No row covers a request that names no order number and fits none of the customer's placed or processing orders. Examples are "cancel my order" when every order has shipped, been delivered or been cancelled, or "cancel my lamp order" when no lamp order exists. CO-02 covers only "more than one". Rows 108 to 110 depend on an order the customer "named" or a number they "gave". The use-case checklist says a lookup that "returns more than one plausible match, or none" needs a row, and that "A failure row that branches on a lookup covers every result of the lookup: nothing found ...".
Pattern: The lookup's "nothing fits" branch is covered only for requests that give an order number, not for requests that describe the order.
(source: coverage finder)
Verifier: R1-09 | Real | Nit | could not refute.
Decision: kept (Real). Status: fixed.

R1-10 | Gap | Nit | CO-08; Failure handling for CO-A2
Quote: "The order's status is cancelled, exactly one refund exists for it, with status pending or issued, and the agent reports the refund id and status without promising when the money will arrive."
Evidence: The customer's interest is "the full amount they paid returned to the payment method they used" (§2, line 9), and the inputs make it a rule (round 2 Q3: "refund amount = order total paid; refund payment method = order's payment method"). The success guarantee CO-08 leaves both terms out. CO-03 binds them only in the proposal text. No failure row covers a CO-A2 result whose amount or payment method differs from the confirmed proposal, which the agent can detect (use-case checklist brainstorm: "the supporting actor answers wrongly"). Scenarios assert amount and payment method in Final state, so no verdict changes.
Pattern: A stakeholder interest is protected only by what the proposal says, not by a guarantee on what actually happened. There is also no row for a detectable wrong answer from a supporting actor.
(source: coverage finder)
Verifier: R1-10 | Real | Nit | partly refuted: Appendix A says amount and method are set by the refund service; no guarantee or row for a wrong answer; CO-08 omits the interest.
Decision: kept (Real; partly refuted). Status: open (proposed rule change to CO-08: 'exactly one refund exists for it, for the order's total paid to the order's payment method, ...'; rule text not changed per the skill).

R1-11 | Gap | Nit | Failure handling row "the customer stops answering before confirming"
Quote: "| any | the customer stops answering before confirming | Send nothing. | CO-03 |"
Evidence: No scenario's Initial state or User block sets up a customer who goes silent before confirming. Every confirm scenario either confirms or replies (CO-S03, CO-S04). The row ends the capability without a cancellation, which is a different outcome from the happy path, and §5.1 End of trial and §5.2 Simulated user give no way to script silence.
Pattern: A failure row that changes the outcome has no scenario that triggers it.
(source: coverage finder)
Verifier: R1-11 | Style only | Nit | "When the customer goes silent there is no agent turn ... A scenario for this row would change no verdict and no agent behavior."
Decision: kept (verifier: Style only). Not dropped: a coverage claim, not wording/style. Status: answered (stands: no agent turn exists when the customer goes silent and §5.2 cannot script silence; resulting state equals CO-S04's).
