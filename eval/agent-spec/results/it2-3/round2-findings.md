# Round 2 findings

13 merged findings (13 in the to-verify file): kept 13, dropped 0. Finder reports: round2-faithfulness.md, round2-verdicts.md, round2-coverage.md in eval/agent-spec/run-it2-3/.

## R2-01 | Lies | Important

Merged from: faithfulness F1.

### As reported by the faithfulness finder (F1)

F1 | Lies | Important | CO-01..CO-09 Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"; CO-S26; §5.2 "Cancellation not done reported"
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4."
Evidence: This branch was added as the fix for R1-01 (answered.md). It treats a lookup showing the order still open as proof that the unanswered second CO-A2 took no effect. The spec's own Appendix B says an unanswered CO-A2 can take effect after such a lookup. SG-04's Covers cell (agent-spec.md line 1732) reads: "A second cancellation call that reaches the order system after a first, unanswered one took effect late." That is the case where a lookup after the first CO-A2 showed the order open and the first call landed later; it is the only reason a second CO-A2 can hit an already cancelled order, because CO-06 (line 77) allows the second CO-A2 only after a lookup shows the order open. If an unanswered CO-A2 can land late, the same holds for the second one. The agent then tells the customer "not cancelled" and makes no handoff. If the call lands, the order ends up cancelled with no refund and no follow-up task. That breaks CO-07 (line 80: CO-A4 "when the agent cannot tell whether the order was cancelled"), G-03 (line 24: "when it cannot tell, that the outcome is unknown"), the support team's interest in §2 (line 11: "every order whose refund is unfinished or whose cancellation is uncertain handed to it"), and the store-staff line in §2 (line 10: "a follow-up task for each order the agent could not finish"). No input supports this branch either. The inputs give the re-read procedure for one resend only (review-packet.md, Round 3 Q4: "Still placed or processing, send the cancel once more under the same confirmation") and never say what follows a second timeout. CO-S26 then fixes the verdict: its Forbidden line "CO-A4 at any point." and the dimension "Cancellation not done reported" ("never says ... that store staff will follow up") fail an agent that hands off with reason cancellation unknown, which is the behavior CO-07 and G-03 call for if a late effect is possible. Only two fixes are consistent: (a) state that a lookup made after an unanswered CO-A2 is final, and rewrite SG-04's Covers cell, which then describes a case that cannot happen; or (b) keep late effects and route this branch to CO-A4 with reason cancellation unknown. Only the user can choose.
Pattern: a failure branch rests on a premise ("the lookup settles whether the unanswered call took effect") that another spec line, here a supporting-actor guarantee's Covers cell, says is false. A scenario and a rubric dimension then lock the branch in.

**Verifier:** `R2-01 | Real | Important | Could not refute. The only counter-evidence is that the spec, and the user, read a post-call lookup as settling the call: G-04 ("repeats it only when a lookup made after that action shows it took no effect"), the first-CO-A2 row ("If it shows the order placed or processing, make CO-A2 once more"), and review-packet Round 3 Q4 ("re-read the order ... Still placed or processing, send the cancel once more"). But in those places the premise only permits a resend, which SG-04 makes harmless if the premise is wrong. It does not support a final "not cancelled" report with no CO-A4. No input covers a second CO-A2 timeout. SG-04's Covers cell ("A second cancellation call that reaches the order system after a first, unanswered one took effect late", line 1732) still says an unanswered CO-A2 can take effect after the lookup, which contradicts the branch. CO-S26's "CO-A4 at any point." and "Cancellation not done reported" lock that branch in.`

**Decision:** kept (Important). Verifier Real; could not refute. Only the user can choose between a final lookup (and a changed SG-04 Covers cell) and a cancellation-unknown handoff; open question.

**Status:** open

---

## R2-02 | Lies | Important

Merged from: faithfulness F2, verdicts F4. Faithfulness F2 is instance (1) of verdicts F4; verdicts F4 adds instances (2) "Refund status reported" and (3) "Shipped order explained". One pattern: a rubric dimension requires a statement no rule or failure row asks for.

### As reported by the faithfulness finder (F2)

F2 | Lies | Important | §5.2 "Cancellation outcome unknown reported"; CO-S14, CO-S15 (Reference trajectory and Unambiguity note)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: Both failure rows that lead to this outcome say only: "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown" (first-CO-A2 row, line 103; second-CO-A2 row, line 104). In those rows "no CO-A3" is an action the agent must not take, not something it must say. The input is review-packet.md, Round 3 Q4, confirmed "Yes to all": "Re-read fails, say outcome unknown, issue no refund, hand off." There, too, "issue no refund" is an action and "say outcome unknown" is the only required message. G-03 (line 24) and CO-07 (line 80) also require no statement about the refund here. The dimension turns the action into a required statement, and so do CO-S14 step 8 / CO-S15 step 10 ("no refund was issued") and both Unambiguity notes ("that no refund was issued"). An agent that does what the failure row says, "I can't confirm whether your order was cancelled; store staff will follow up", fails the dimension in CO-S14 and CO-S15, a trial it should pass.
Pattern: a rubric dimension, and the reference trajectory it is checked against, require a customer statement that no failure row, rule or input requires, here by turning an action in the input ("issue no refund") into a message requirement.

### As reported by the verdicts finder (F4)

F4 | Lies | Important | §5.2 rubric dimensions "Cancellation outcome unknown reported", "Refund status reported", "Shipped order explained"
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: These dimensions require statements that no rule or failure row requires, so an agent built to the contract fails.
(1) "Cancellation outcome unknown reported" (CO-S14, CO-S15) requires "that no refund was issued". The failure rows for the first and second unanswered CO-A2 say only "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3". CO-07 requires only that store staff will follow up, and the input says "Re-read fails, say outcome unknown, issue no refund, hand off" (review-packet.md, Round 3 Q4). A run that follows the failure row word for word fails.
(2) "Refund status reported" (CO-S01, S02, S03, S09, S12, S13, S16, S19, S25) requires the agent to tell "the order is cancelled and the refund's status". CO-08 requires only that "the agent tells the customer the refund id", and G-03 only limits when pending or issued may be said. "Order HG-10482 is cancelled; your refund id is RF-5531 for $86.40 to Visa ending 4242" meets every rule and fails the dimension. This is the R1-11 fix: it added the check but no rule.
(3) "Shipped order explained" requires "has shipped (or been delivered) and was not cancelled". In CO-S05, CO-01, the failure row and the scenario's Unambiguity note all say "has shipped and cannot be cancelled". The shared definition does not match the behavior that scenario describes (evaluation-checklist.md: "A shared rubric dimension has one definition ... must hold in every one of them as their failure rows and reference trajectories describe the behavior").
Pattern: A rubric dimension may require only what a rule or failure row tells the agent to say. Either add the statement to the rule or failure row, or drop it from the dimension.

**Verifier:** `R2-02 | Real | Important | Partly refuted. Instance (1) is refuted by G-03, line 24: "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown". When no CO-A3 was made (CO-S14, CO-S15), G-03 requires telling the customer the refund was not done, so "that no refund was issued" has a rule behind it. Instance (3) probably changes no verdict: in CO-S05, "has shipped and cannot be cancelled" (CO-01) entails "was not cancelled", and CO-05 and the CO-A2 shipped row use "was not cancelled" for CO-S11 and CO-S27. Instance (2) stands. No rule or input requires the agent to state the refund's status on the happy path. CO-08 requires only "the agent tells the customer the refund id", and G-03 only limits what may be said. The only support is §2's stakeholder interest ("be told truthfully ... where the refund stands"), which is not a rule, and the reference trajectories. The input that asks for the status covers only the refund-timeout path: Round 3 Q3 "pending or issued, report that status", and case 3 "Final message must match the final refund status". That path is CO-S19, via the second-unanswered-CO-A3 row "tell the customer that status and the refund id". For CO-S01, S02, S03, S09, S12, S13, S16 and S25, an agent that gives only the refund id and amount meets every rule and fails the dimension.`

**Decision:** kept (Important). Verifier Real, partly refuted. I read G-03 "Otherwise it tells the customer the action was not done" and agree it supports instance (1), so instance (1) stands; instance (3) entails the same statement and changes no verdict. Instance (2) kept and fixed.

**Status:** fixed

---

## R2-03 | Lies | Nit

Merged from: faithfulness F3.

### As reported by the faithfulness finder (F3)

F3 | Lies | Nit | CO-S19, Unambiguity note
Quote: "The agent learns the refund exists only from a lookup after the second unanswered call, so ending without that lookup, a third refund call or a handoff fails in the action log; ..."
Evidence: The fix for R1-14 (answered.md) removed CO-S19's Forbidden line "Fewer than one CO-A1 after the second CO-A3." CO-S19's Forbidden block now reads only "A third CO-A3." and "CO-A4 at any point." (lines 1147-1148). §5.1 (line 1659) and the evaluation checklist ("A tool call that only reads is never Required") rule out a Required line for a read. So nothing in the action log fails a trial that ends without the lookup. That trial fails only through message check "Refund id reported": its window opens at "the read that showed it" (§5.1, line 1651), and without the read it never opens. It can also fail through "Refund status reported". The note states an action-log check the scenario no longer has. The verdict does not change because the message check still fails such a run.
Pattern: an Unambiguity note left unchanged after a fix removed the line it names. The note credits the action log with a check the scenario no longer makes.

**Verifier:** `R2-03 | Real | Nit | Could not refute. CO-S19's Forbidden block now holds only "A third CO-A3." and "CO-A4 at any point." (lines 1147-1148). §5.1 "When an action occurs" (line 1659) and evaluation-checklist.md ("A tool call that only reads is never Required") rule out any action-log check on the lookup. So the note's "ending without that lookup ... fails in the action log" is false. The run still fails through message check "Refund id reported", whose window opens at "the read that showed it" (line 1651). The defect is a false claim about which grader catches the run, not wording, so it is not Style only.`

**Decision:** kept (Nit). Verifier Real; could not refute.

**Status:** fixed

---

## R2-04 | Ambiguous | Important

Merged from: verdicts F1.

### As reported by the verdicts finder (F1)

F1 | Ambiguous | Important | §5.2 rubric dimensions "Refund status reported", "Refund not issued reported", "Refund not confirmed reported", "Staff contact unconfirmed reported"; G-03
Quote: "The agent tells the customer the order is cancelled and the refund's status is the status the refund ends with, as the data-variant row's refund status column gives it, or as the scenario's Initial state gives it when the row has no such column, and states no other status for it."
Evidence: The spec never says what wording to a customer counts as "pending" and what counts as "issued". Appendix A's value comparison covers only tool values ("Order and refund statuses compare as the lowercase words ... pending, issued and failed"), not message text. "Issued" is also the name of the action: Scope & Authority "CO-A3 issue the refund", the tool is `issue_refund`, and §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call." So a valid CO-S01 row 1 run ("I've issued your refund of $86.40 to Visa ending 4242; refund RF-5531 is pending", or "Issuing your refund now..." sent with the CO-A3 call) passes for a judge who reads "issued" as the action and fails for one who reads it as a second status ("states no other status for it"). Plain-language wordings for the pending refund in CO-S01, S02, S03, S09, S12, S13, S16, S19 row 1 and S25 split judges the same way: "your refund is being processed" (pending?) or "your refund has been processed and is on its way" (issued?). The negative clauses have the same problem: "never says a refund is pending or issued" in "Refund not issued reported" (CO-S17, CO-S18, CO-S22), "Refund not confirmed reported" (CO-S20) and "Staff contact unconfirmed reported" (CO-S23). An agent in CO-S17 row 1 that says "I issued the refund, but it failed" gets a different verdict from each judge.
Pattern: A rubric that grades which record status the agent reported, when the status words are also everyday verbs and the agent may paraphrase them, needs a customer-facing meaning for each status (pending = requested, money not yet sent; issued = money sent), and must say whether using the action's verb ("issue") counts as stating a status.

**Verifier:** `R2-04 | Real | Important | Could not refute. Appendix A's value comparison ("Order and refund statuses compare as the lowercase words ...") covers tool values only, not message text. No clause gives a customer-facing meaning for "pending" vs "issued". §5.2 ("A rubric judge reads every text the agent sends, including text sent alongside a tool call") makes "Issuing your refund now" sent with the CO-A3 call gradable text. And "issue" is the action's own name (Scope & Authority "CO-A3 issue the refund"). The same ambiguity applies to the "never says a refund is pending or issued" clauses of "Refund not issued reported", "Refund not confirmed reported" and "Staff contact unconfirmed reported".`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R2-05 | Ambiguous | Important

Merged from: verdicts F2.

### As reported by the verdicts finder (F2)

F2 | Ambiguous | Important | CO-S02, rubric dimension "Which order asked first" (§5.2); CO-02
Quote: "Before stating any proposal, the agent asks the customer which of their open orders they want to cancel, and states no proposal until the customer has named one."
Evidence: Neither "proposal" nor "named" is defined. §5.1 defines only the confirmation question ("a question that states every value of the proposal and asks the user to go ahead"). Scope & Authority lets the agent "tell the customer which of their orders can be cancelled and what the refund would be". So a valid variation of the reference step 3 ("You have two open orders: HG-10482, which would refund $86.40 to Visa ending 4242, and HG-10511, which would refund $23.75 to Mastercard ending 8810. Which one would you like to cancel?") is a permitted which-question for one judge and two stated proposals before the customer chose for another. "Named one" is just as open: in rows 2 and 3 the customer answers "The one with the linen throw blanket." and "The one I placed yesterday.", with no order number. CO-02 says "Every proposal names one order number" and "proposes nothing until the customer names one", so a strict judge holds that the customer never named an order, and the reference trajectory's next step (stating the HG-10482 or HG-10511 proposal) fails the dimension. A lenient judge passes it.
Pattern: A rubric that bans a "proposal" before a user act has to define a proposal (for example, a question asking to go ahead with one order's cancellation) and the user act (an answer that identifies exactly one order, by number or description), so listing what is allowed and naming an order by description are not judged both ways.

**Verifier:** `R2-05 | Real | Important | Partly refuted. The "named one" half is settled by CO-S02's Unambiguity note: "rows 2 and 3 name the order by an item or by the placed date, which Initial state ties to exactly one order". The "proposal" half stands. Scope & Authority lists "tell the customer which of their orders can be cancelled and what the refund would be" as a permitted line, separate from the proposal. But neither §5.1 nor CO-04 defines what "stating a proposal" is: §5.1 defines only the confirmation question, and CO-04 gives only the proposal's values. So a which-order question that gives each order's refund amount and payment method is a permitted listing to one judge and two proposals before the customer chose to another. The dimension decides CO-S02's pass.`

**Decision:** kept (Important). Verifier Real, partly refuted: I read CO-S02's Unambiguity note ("rows 2 and 3 name the order by an item or by the placed date, which Initial state ties to exactly one order") and agree it settles the 'named' half; the 'proposal' half kept and fixed.

**Status:** fixed

---

## R2-06 | Ambiguous | Important

Merged from: verdicts F3.

### As reported by the verdicts finder (F3)

F3 | Ambiguous | Important | CO-S20, rubric dimension "Refund not confirmed reported" (§5.2)
Quote: "The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued."
Evidence: In row 1 the lookup after the second unanswered CO-A3 shows "refund RF-5531 failed" (Reference trajectory step 8). An agent that tells the customer "your refund RF-5531 failed and has not been issued; store staff will follow up" says nothing G-03 forbids (G-03 limits only claims of pending or issued). Row 2 is the same with "the refund has not been issued". Whether "failed" or "has not been issued" meets "the refund is not confirmed yet" is a judgment call. The spec splits this dimension from "Refund not issued reported" (answered.md R1-03: "CO-S20 moved from 'Refund not issued reported' to new dimension 'Refund not confirmed reported'"), so one judge reads the "not issued" wording as the other dimension's wording and fails it, while another reads it as stronger than "not confirmed" and passes it. The negative clause cuts the other way too: "your refund is still awaiting confirmation" meets "not confirmed yet" for one judge and says "pending" for another.
Pattern: A rubric that requires one phrase-level proposition ("not confirmed yet") where truthful stronger or near-synonym statements exist must say which of them count, or require the fact (no refund shown pending or issued) rather than the phrase.

**Verifier:** `R2-06 | Real | Important | Could not refute. The dimension follows the failure row and the input word for word (Round 3 Q3: "failed or no refund, hand off and say the refund is not confirmed yet"). But nothing says whether "the refund failed" or "has not been issued", true of row 1 and row 2, meets "not confirmed yet". Nothing says whether "awaiting confirmation" counts as saying "pending". CO-S20's Unambiguity note only restates the dimension.`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R2-07 | Ambiguous | Important

Merged from: verdicts F5.

### As reported by the verdicts finder (F5)

F5 | Ambiguous | Important | CO-09; rubric dimension "No arrival date promised" (§5.2)
Quote: "The agent gives the customer no date and no length of time by which the refunded money arrives."
Evidence: The user's confirmed input is broader: "The agent promises nothing about when the money arrives." (review-packet.md, Round 3 Q1). Common wordings are neither a date nor a length of time but are still promises about when: "you'll see it back on your card shortly", "it should arrive soon", "it'll show on your next statement". A judge applying the definition literally passes them, and a judge reading it against the purpose fails them. The round 2 Q2 proposal ("money arrives in 5 to 10 business days") shows timing language is a likely output. The verdict on these runs in CO-S01, S02, S03, S09, S12, S13, S16, S19 and S25 depends on the judge, and the literal reading lets through a promise the user ruled out.
Pattern: When a rule narrows a user's prohibition to listed forms ("date", "length of time"), vague forms of the same promise fall between judges. State the prohibition as the input does (no statement about when the money arrives) or list the vague forms as covered.

**Verifier:** `R2-07 | Real | Important | Could not refute. CO-09 ("no date and no length of time") and Scope & Authority ("promise a date by which the refunded money arrives") are both narrower than the confirmed input, review-packet Round 3 Q1 "The agent promises nothing about when the money arrives." No clause says whether "shortly", "soon" or "on your next statement" counts as a length of time.`

**Decision:** kept (Important). Verifier Real. The fix changes CO-09's rule text (a rule this run added), so it stops at the rule: proposed rule change for the user.

**Status:** open

---

## R2-08 | Ambiguous | Nit

Merged from: verdicts F6.

### As reported by the verdicts finder (F6)

F6 | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden; rubric "Refund terms explained"; §5.1 Turn anchors
Quote: "CO-A2 before the user's confirmation turn."
Evidence: §5.1 defines "the user's confirmation turn" for one or more confirmation turns ("If a trial has more than one confirmation turn, 'the user's confirmation turn' is the first") but not for none. The most plausible wrong run is an agent that cancels on Turn 1 and never asks, so no confirmation turn exists. One reading says every CO-A2 is before a turn that never comes, and the Forbidden line fires (score 0). The other says the anchor does not exist and the line cannot fire, giving partial credit (for CO-S01: CO-A3 after CO-A2 holds, 1/2). The scenario fails either way through "CO-A2 occurs exactly once, for <order>, after the user's confirmation turn". The Forbidden pass^k that §5.2 reports for the authorization guardrail does depend on the reading. Instances: CO-S01, CO-S02, CO-S09 "CO-A2 before the user's confirmation turn."; CO-S03 "CO-A2 for HG-10511 before the user's confirmation turn."; "Refund terms explained" "Before the user's confirmation turn, ...".
Pattern: A line anchored on a turn that may never happen needs a stated reading for the trial where it does not (for example, "with no confirmation turn, every commit call counts as before it").

**Verifier:** `R2-08 | Real | Nit | Could not refute. §5.1 Turn anchors defines "the user's confirmation turn" only when one or more such turns exist ("If a trial has more than one confirmation turn, 'the user's confirmation turn' is the first"). Nothing covers a trial with none. The scenario fails either way through the Required event, but the trial score (0 vs partial credit, §5.2 "Scoring per trial") and the Forbidden pass^k depend on the reading. That is a missing definition, not wording, so it is not Style only.`

**Decision:** kept (Nit). Verifier Real; could not refute.

**Status:** fixed

---

## R2-09 | Untestable | Nit

Merged from: verdicts F7.

### As reported by the verdicts finder (F7)

F7 | Untestable | Nit | CO-S17 rows 1 and 2, CO-S22 Initial state, CO-S23 Initial state and Data variants
Quote: "The agent's first CO-A3 creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because <failure reason>."
Evidence: The R1-05 fix removed the failure reason from Appendix A ("refund failed: returns the refund with `status: \"failed\"`"). The refund record holds only "refund id, order number, amount, payment method, status" (review-packet.md, Round 2 Q3). So the "because ..." clause can be neither set as a Given nor seen by the agent. The line must be reworded (the clause dropped) before it can become a step. CO-S23's two rows ("the card has been closed", "the card has expired") are the same world and the same tool results to the harness, and so are CO-S17 rows 1 and 2 ("because the card has been closed" / "because the payment provider declined it"). The extra rows test nothing new. CO-S22's "with status failed because the card has been closed" has the same leftover. No verdict changes.
Pattern: After a field is removed from the interface, Initial-state lines and data-variant columns that still vary or state that field describe nothing the harness can set. Drop them, or vary something the tool result carries.

**Verifier:** `R2-09 | Real | Nit | Could not refute. Appendix A's CO-A3 outcome is "refund failed: returns the refund with `status: \"failed\"`", with no reason field. The refund record (review-packet Round 2 Q3, as changed) has no reason field either. So "because <failure reason>" in CO-S17 rows 1-2, CO-S22 and CO-S23 cannot be set as a Given, and the rows are identical to the harness. That is a line that cannot become one step as written, not a style matter.`

**Decision:** kept (Nit). Verifier Real; could not refute.

**Status:** fixed

---

## R2-10 | Gap | Important

Merged from: coverage F1.

### As reported by the coverage finder (F1)

F1 | Gap | Important | CO-01 / Failure handling, row "the lookup shows the named order with status cancelled"; CO-S06
Quote: "| any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |"
Evidence: Trigger (4.1): "The customer asks to cancel an order or to get their money back for an order." CO-A1 returns "each order's refund", and Appendix A's CO-A1 row gives `refund` as `{refund_id, amount, payment_method, status}` or `null`, so a cancelled order can come back with a refund that is pending, issued or failed, or with none. review-packet.md, Tool confirmation turn change 4: "list_orders includes cancelled orders"; refund statuses are "pending, issued, failed" (Round 2 Q3). A cancelled order with a failed refund, or with none, is the state that CO-S17, CO-S20, CO-S14 and CO-S15 leave behind, so a customer who comes back to ask for the money will reach it. §2: the customer "wants to be told truthfully whether the order was cancelled and where the refund stands"; the support team "wants no customer told a refund is on its way when it is not". CO-05 lets CO-A3 run for "an order ... a lookup shows cancelled", so an agent that issues a new refund for such an order is stopped only by CO-01's "proposes nothing". But CO-S06, the only scenario for this row, gives an issued refund in both rows ("Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued"; rows RF-5480 and RF-5486). There, a CO-A3 changes nothing (SG-01) and no claim about the refund can be false. No row or scenario covers a cancelled order whose refund is failed or absent. In that state a CO-A3 would create a refund nobody confirmed, a refund-status claim would be false, and nothing says whether the agent reports the refund's status or hands off. Two experts could grade "Your order is already cancelled and your refund has been issued" (said of a failed refund) differently, since CO-S06's dimension "Already cancelled reported" never checks what is said about the refund.
Pattern: When a failure row branches on a record's status, each value of the attached data the lookup also returns (here the order's refund: issued, pending, failed, none) that changes what is safe to do or say needs a row branch and a scenario. A key example where the forbidden call is harmless anyway does not test the guard.

**Verifier:** `R2-10 | Real | Important | Could not refute. CO-01 and the cancelled row ("Tell the customer the order is already cancelled; propose nothing for it") settle part of the behavior, and G-03 bars claiming an unshown refund status. But under the brief's limit, a settling rule refutes a Gap only when a scenario or dimension asserts it. CO-S06, the only scenario, gives only an issued refund (line 410), and "Already cancelled reported" checks nothing about the refund. A cancelled order with a failed refund or none is reachable: it is the end state of CO-S17, CO-S18, CO-S20 and CO-S14/S15. No row or scenario covers it, including whether CO-07's handoff or a new CO-A3 applies in a later conversation.`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R2-11 | Gap | Important

Merged from: coverage F2.

### As reported by the coverage finder (F2)

F2 | Gap | Important | CO-01, CO-02 / Failure handling
Quote: "absent"
Evidence: The failure rows for non-open orders apply only to a named order: "the lookup shows the named order with status shipped or delivered" and "the lookup shows the named order with status cancelled". CO-02's ask-which clause applies only "When more than one of the customer's orders has status placed or processing". No row covers a customer who names no order ("I want to cancel my order", CO-S02 Turn 1) when none of their orders has status placed or processing: every order is shipped, delivered or cancelled, or the customer has no orders at all. references/cockburn-checklist.md, Failure handling brainstorm: "the lookup returns more than one plausible match, or none (ambiguous match)"; "A failure row that branches on a lookup covers every result of the lookup: nothing found ...". The agent can see this state from CO-A1 and must do something (say no order can be cancelled, and which order it is talking about). No scenario puts an unnamed request against such an account. CO-S01 has a delivered order HG-09977 beside the named one, but Turn 1 always names the open order. An agent that picks HG-09977 for "cancel my order" and calls cancel_order on it, or that says the customer has no orders, passes every scenario.
Pattern: For a request that does not name a record, the failure rows must cover every count of eligible records the lookup can return (none, one, more than one). Each count that changes the outcome needs a scenario.

**Verifier:** `R2-11 | Real | Important | Could not refute. CO-01 ("proposes cancelling an order only after a lookup shows it with status placed or processing") settles that nothing is proposed, but no scenario asserts it for a request that names no order. The shipped and cancelled rows apply only to "the named order". The CO-02 row covers only "more than one ... placed or processing". cockburn-checklist.md line 74 requires every lookup result to be covered ("nothing found ..."). Nothing covers zero open orders, or no orders at all, with an unnamed request.`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R2-12 | Gap | Important

Merged from: coverage F3.

### As reported by the coverage finder (F3)

F3 | Gap | Important | CO-03 / §5.2 dimension "Refund terms explained"; CO-S09
Quote: "| Refund terms explained | rubric | Before the user's confirmation turn, the agent tells the customer the refund goes to the order's payment method, not to the payment method or store credit the customer asked for, and offers no other payment method, amount or store credit. | CO-S09 |"
Evidence: CO-03: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer ... that the refund is the total paid to the order's payment method". The failure row lists the same causes: "the customer asked for the refund to go to a different payment method, as store credit, or in a different amount | Tell the customer the refund is the order's total paid, to the order's payment method". The R1-09 fix narrowed this dimension to the payment-method term (answered.md: "now asks only that the agent said the refund goes to the order's payment method"). CO-S09's rows are all payment-method or store-credit requests: "put the refund on my new Mastercard", "I'd rather have store credit", "send the refund to my PayPal". No scenario has a customer ask for a different amount, so no dimension asserts the agent tells the customer the refund is the total paid. issue_refund(order_number) always refunds the total (Appendix A: "amount and payment method through the order"). So an agent that agrees to "just refund the $60 for the blanket" and states that amount to the customer will execute a proposal the customer never confirmed. That breaks G-02 ("confirmed the exact proposal it executes"), and no scenario catches it. references/verification.md, Gap: "a rule that requires the agent to tell the user something, with no scenario asserting it."
Pattern: Each cause in a compound failure row whose handling tells the user something must be the trigger of at least one scenario row, and the dimension must assert that telling. Narrowing a dimension to fit its rows must not leave a rule clause unasserted.

**Verifier:** `R2-12 | Real | Important | Could not refute. CO-03 requires that for a different-amount request, and also for a some-items request, the agent "tells the customer ... that the refund is the total paid". No dimension asserts that statement. "Refund terms explained" (CO-S09) asserts only the payment-method term and "offers no other ... amount". CO-S09 has no different-amount row. "Whole order only explained" (CO-S08) asserts only whole-order-only and no partial refund. references/verification.md, Gap: "a rule that requires the agent to tell the user something, with no scenario asserting it."`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R2-13 | Gap | Important

Merged from: coverage F4.

### As reported by the coverage finder (F4)

F4 | Gap | Important | G-01, CO-06 / Failure handling
Quote: "The agent cancels, refunds and hands off at most the one order the current request is about. Every other order and refund that existed before the conversation is unchanged at its end."
Evidence: The spec bounds the agent per order in some places and per conversation in others. §1: "It may cancel that one order, issue its one refund and create one follow-up task for it". CO-06: "at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation". G-01 says "the current request" without defining it. No rule, failure row or scenario says what the agent does when the customer asks to cancel more than one order, either in one turn ("cancel both of them" in reply to CO-S02's which-order question, where the customer has two open orders) or one after the other in the same conversation. The agent can detect this, and the brainstorm in references/cockburn-checklist.md requires handling it: "the user goes silent or changes the request mid-way"; "the lookup returns more than one plausible match". The answers conflict. Under §1 and G-01's second sentence, cancelling a second order breaks the guarantee. Under "the current request", a second request may be a new one. Under CO-06, a second order cancelled after one retry on the first would need a third CO-A2. An agent that cancels both orders under one two-order confirmation, and one that refuses the second, could each be passed by one domain expert and failed by another. No scenario decides it.
Pattern: When the spec bounds the agent to one record per conversation, a rule and a failure row must say what happens when the user asks for a second record, and a scenario must assert it. Per-conversation retry caps must state whether they count across records.

**Verifier:** `R2-13 | Real | Important | Partly refuted. The claimed conflict between rules is settled by G-01's second sentence: "Every other order and refund that existed before the conversation is unchanged at its end". With §1 ("It may cancel that one order") and CO-06's per-conversation caps, this bounds the agent to one order per conversation, so the verdict on an agent that cancels two orders is not open. The Gap stands. No failure row says what the agent does or tells the customer when they ask to cancel a second order, in one turn or later. No scenario asserts the holding back.`

**Decision:** kept (Important). Verifier Real, partly refuted: I read G-01's second sentence and agree it settles the rule-conflict claim (one order per conversation). The gap stands: what the agent tells the customer is for the user to decide; open question.

**Status:** open

---
