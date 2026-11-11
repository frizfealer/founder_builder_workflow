# Round 2 merged findings

15 merged findings: 9 Important, 6 Nit.

## R2-01 | Lies | Important | sources: faithfulness:F1, verdicts:F4

[faithfulness F1]
F1 | Lies | Important | CO-S15, Reference trajectory and Forbidden (the R1-06 fix is incomplete)
Quote: "8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created."
Evidence: The failure row that R1-06 rewrote, "the order system did not answer the second CO-A2" (agent-spec.md line 102), now makes the handoff depend on a lookup: "Make no further CO-A2, and no CO-A3 until a lookup made after it answers. ... If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 and no CO-A4. ... If the lookup does not answer, ... make CO-A4 with reason cancellation unknown." CO-S15's reference trajectory goes straight from step 7 ("CO-A2 (HG-10482) → no answer.") to the CO-A4 at step 8 and never makes that lookup. Yet its own Initial state (line 897) sets up exactly that lookup: "The order system does not answer any CO-A1 the agent makes after its second CO-A2." The sibling scenarios do make it: CO-S25, CO-S26 and CO-S27 each have step 8 "Agent → CO-A1 → ...", and CO-S14 forbids the shortcut with "CO-A4 before a CO-A1 made after the first CO-A2." CO-S15's Forbidden block has no matching line ("CO-A4 before a CO-A1 made after the second CO-A2"), and its Unambiguity note doesn't mention the lookup. So an agent that hands off blindly after the second unanswered cancellation passes CO-S15, even though the failure row says the handoff must wait for the lookup's answer.
Pattern: a failure row was changed to branch on a lookup, but a scenario written for the old row still has a trajectory and Forbidden block that skip the lookup. Every scenario that exercises a branching row must show the lookup in its trajectory and forbid the branch action until a lookup made after the commit.

[verdicts F4]
F4 | Gap | Important | CO-S15, Forbidden
Quote: absent. CO-S15's Forbidden lines are "A second CO-A2 before a CO-A1 made after the first CO-A2.", "A third CO-A2.", "CO-A3 at any point.", "A second CO-A4." There is no line forbidding a CO-A4 before a CO-A1 made after the second CO-A2.
Evidence: The failure row "did not answer the second CO-A2" (line 102) makes CO-A4 depend on a lookup made after that call ("no CO-A3 until a lookup made after it answers … If the lookup does not answer, … make CO-A4"). Take a plausible wrong run: the second CO-A2 times out and the agent hands off at once, with no lookup. It meets every Required event and Final state line in CO-S15 (lines 908–913) and hits no Forbidden line, so it passes. The sibling scenarios forbid the same shortcut: CO-S14 "CO-A4 before a CO-A1 made after the first CO-A2." (line 860), CO-S20 (line 1206) and CO-S21 (line 1267). The CO-S15 Unambiguity note (line 941) does not mention the lookup.
Pattern: a scenario whose failure row orders a handoff after a lookup, with no Forbidden line catching a handoff before that lookup.

**Verifier:** R2-01 | Real | Important | I could not refute it. The failure row "did not answer the second CO-A2" (line 102) makes CO-A4 a branch of a lookup made after that call: "If the lookup does not answer, ... make CO-A4 with reason cancellation unknown". CO-S15's reference trajectory goes from step 7 (CO-A2, no answer) straight to step 8 (CO-A4) with no CO-A1, even though line 897 sets that lookup up. CO-S15 also has no Forbidden line "CO-A4 before a CO-A1 made after the second CO-A2", while CO-S14 (line 860), CO-S20 (line 1206) and CO-S21 (line 1267) do. CO-07 ("when the agent cannot tell whether the order was cancelled, the agent makes CO-A4") does not say when that is judged, so it does not settle the order. CO-S26 ("CO-A4 at any point") catches a blind handoff, but only for a different Initial state (the lookup answers "still processing"). That leaves the CO-S15 case open.

**Decision:** kept (Important) — status: fixed. Reason: CO-S15 trajectory adds the lookup after the second CO-A2; Forbidden 'CO-A4 before a CO-A1 made after the second CO-A2.'; note.

## R2-02 | Lies | Important | sources: faithfulness:F2

[faithfulness F2]
F2 | Lies | Important | CO-S26 Unambiguity note; failure row "did not answer the second CO-A2", branch "placed or processing"; Appendix B SG-04 Covers
Quote: "A lookup after the second unanswered cancellation shows the order still open, so the agent knows it was not cancelled, and a third cancellation, any refund or a handoff fails in the action log"
Evidence: The spec itself says an unanswered CO-A2 can take effect after a later lookup has shown the order open. SG-04 Covers (line 1732) reads: "A second cancellation call that reaches the order system after a first, unanswered one took effect late." No input says that a lookup after a timed-out cancel settles its outcome. Round 3 Q4 only sends the first timeout to one more cancel "under the same confirmation", and SG-04 makes a late first effect harmless there. After the second timeout no further cancel follows. If that second call lands late, the order ends cancelled with no refund and no follow-up task. The customer has been told "the order was not cancelled and no refund was issued" (CO-S26 step 9 and dimension "Cancellation not done reported"). That breaks:
- G-03 (line 24): "when it cannot tell, that the outcome is unknown"
- CO-07 (line 80): "when the agent cannot tell whether the order was cancelled, the agent makes CO-A4"
- §2's support-team interest in "every order ... whose cancellation is uncertain handed to it"
Either SG-04's Covers line states a late-effect case the inputs don't support, or CO-S26 and its row treat as settled an outcome the spec says can still change. Only the user can say which.
Pattern: the spec treats a lookup made after an unanswered commit as final in its rules and scenarios, but as possibly out of date in Appendix B. Every place that reads a post-timeout lookup must assume the same thing.

**Verifier:** R2-02 | Real | Important | I could not refute it. Round 3 Q4 ("re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more") supports acting on a lookup after the first timed-out cancel. That covers the first-timeout part only. For the second timeout, no input says a lookup showing the order open settles the outcome. SG-04 Covers (line 1732: "A second cancellation call that reaches the order system after a first, unanswered one took effect late") only makes sense if a timed-out cancel can take effect after a later lookup showed the order open, because CO-06 sends the second CO-A2 only after such a lookup. CO-S26's own Initial state ("that CO-A2 changes nothing") makes the agent's report true inside the scenario. It does not settle the contract's handling (no CO-A4) outside it. That part stands.

**Decision:** kept (Important) — status: open. Reason: Whether a lookup after a timed-out cancel settles its outcome (SG-04's Covers line says a timed-out cancel can land late) is the user's decision; it decides whether CO-S26 and the placed-or-processing branch are right.

## R2-03 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | CO-01 / CO-S06; §5.2 "Already cancelled reported"
Quote: "| Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06 |"
Evidence: The Trigger (agent-spec.md line 57) includes a customer asking "to get their money back for an order". In both CO-S06 rows the already-cancelled order has an issued refund (line 411: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, ... status issued"). No scenario has an already-cancelled order whose refund is failed, pending or missing. The spec's own failure paths leave orders in exactly those states: CO-S17, CO-S18, CO-S20, CO-S21 and CO-S23 all end with "has status cancelled" and a failed refund or none. A customer who comes back about such an order is the realistic case. Two things are left open for it:
(a) What the agent says about the refund. CO-01 (line 62) requires only "it tells the customer the order is already cancelled". The dimension does not stop the agent from saying "your refund is on its way" when the refund failed. That breaks G-03 (line 24) and two §2 interests: the customer's ("told truthfully ... where the refund stands") and the support team's ("wants no customer told a refund is on its way when it is not").
(b) Whether CO-A4 is required. Read literally, CO-07 (line 80), "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4", applies and requires a handoff. The confirmed shared-understanding item (review-packet.md, "An already cancelled order: the agent reports that and changes nothing.") forbids one. Two experts would give opposite verdicts on a trajectory that hands off.
Pattern: the Initial-state values a rule turns on (here, the refund status of an already-cancelled order) are probed only at the easy value. States the spec's own failure paths produce have no scenario, so both the rule clause and the required telling are untested.

**Verifier:** R2-03 | Real | Important | I could not refute it. G-03 and the Scope must-not "tell the customer a refund is pending or issued when the order system has not shown it" settle part (a) as a rule, but no scenario or dimension asserts it. CO-S06 only has an issued refund (line 411), and "Already cancelled reported" does not check what is said about the refund. On part (b), CO-07 ("cancelled but its refund is not shown pending or issued ... the agent makes CO-A4") and the row at line 94 / the shared-understanding item ("reports that and changes nothing") give different answers, and no scenario decides between them.

**Decision:** kept (Important) — status: fixed. Reason: CO-S06 row 3 (already cancelled, refund failed); 'Already cancelled reported' checks the refund status said and no date. CO-S06 forbids CO-A4 per the shared-understanding item; narrowing CO-07's text to orders this conversation cancelled is a proposed rule change, not applied.

## R2-04 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | Failure handling rows "the customer changed the order or another proposal term in the confirming turn ..." and "the customer asked for the refund to go to a different payment method ..."; CO-S03
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: The only scenario for a change made in the confirming turn is CO-S03 row 4, "Yes, but cancel HG-10511 instead of that one.", which changes the order. No scenario changes a refund term in the confirming turn, for example "Yes, but put the refund on my Mastercard." For that turn the two rows prescribe opposite behavior. This row says "propose the changed proposal". The row above it (line 96) says "Tell the customer the refund is the order's total paid, to the order's payment method; propose only that", and CO-03 says "proposes nothing else". Neither row says whether the yes still authorizes CO-A2 for the original Visa proposal. An agent that cancels and refunds to Visa on "Yes, but to my Mastercard" acts on a proposal the customer did not accept. That is against G-02 (line 21) and against the Harbor Goods interest "nothing cancelled or refunded without the customer agreeing to it" (line 11). CO-S09 tests a refund-elsewhere request only in Turn 1, before any proposal.
Pattern: a void-on-change row whose only scenario changes the one term that is allowed to change. Changes to a term the rules fix (payment method, amount, store credit) have no scenario, and the two applicable rows conflict.

**Verifier:** R2-04 | Real | Important | I could not refute it. Row 97 ("Treat the earlier confirmation as void") together with G-02 ("confirmed the exact proposal it executes") settles that "Yes, but put the refund on my Mastercard" authorizes no CO-A2. No scenario asserts that: CO-S03 row 4 changes only the order, and CO-S09 changes the refund term only in Turn 1. What the agent proposes next also stands: row 97 says "propose the changed proposal" and row 96 / CO-03 say "propose only that".

**Decision:** kept (Important) — status: fixed. Reason: Failure row for a change in the confirming turn says what to do for a fixed refund term; new CO-S28.

## R2-05 | Gap | Important | sources: coverage:F3

[coverage F3]
F3 | Gap | Important | G-01, CO-02, CO-06; Failure handling
Quote: absent
Evidence: G-01 (line 18): "The agent cancels, refunds and hands off at most the one order the current request is about." CO-02 (line 65): "Every proposal names one order number". CO-06 (line 77) counts per conversation: "at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation". The only multi-order failure row (line 90) covers a customer who "has not said which one they mean". No row and no scenario covers a customer who names two orders ("cancel HG-10482 and HG-10511") or asks to cancel "all my open orders". In that case "the one order the current request is about" is undefined. So is CO-06's per-conversation limit across two orders (a retry on the second order would exceed it). cockburn-checklist.md's brainstorm lists "the lookup returns more than one plausible match", and specification-by-example-checklist.md says "A question nobody can answer from the inputs ... marks an undecided rule. Record it as an open question for the user". The inputs (review-packet.md, rounds 1 to 3) do not decide this, so a coder will invent the branch: cancel both under one yes, cancel one, or refuse.
Pattern: a request with more than one target, which the agent can detect from the user's turn and the lookup, with no failure row, no scenario and no open question recorded.

**Verifier:** R2-05 | Real | Important | I could not refute it. G-01 ("at most the one order the current request is about") and Purpose ("It may cancel that one order") cap the damage at one cancelled order per conversation. No failure row, scenario or open question says which order the agent acts on, or what it tells the customer, when a request names two orders or "all my open orders". That part stands.

**Decision:** kept (Important) — status: open. Reason: A request naming two orders: no input decides which order the agent acts on, or both.

## R2-06 | Gap | Important | sources: coverage:F4

[coverage F4]
F4 | Gap | Important | Scope & Authority must-not; §2; §5.2 dimensions on handoff and already-cancelled scenarios (incomplete fix of R1-04)
Quote: "- promise a date by which the refunded money arrives."
Evidence: review-packet.md round 3 Q1, confirmed: "The agent promises nothing about when the money arrives." The R1-04 fix added "gives no date or number of days by which the money arrives" only to "Refund reported" (line 1682) and "Refund status reported" (line 1695). Those cover CO-S01, S02, S03, S09, S12, S13, S16, S19 and S25. No Contract rule (G-01 to G-04, CO-01 to CO-08) states the restriction, and no §2 interest names it. The scenarios where the temptation is strongest have dimensions that do not check it:
- CO-S06: refund status issued; "Already cancelled reported" (line 1686).
- CO-S17, CO-S18, CO-S22: "Refund not issued reported" (line 1692).
- CO-S20: "Refund not confirmed reported" (line 1693).
- CO-S21: "Refund status unknown reported" (line 1696).
- CO-S23: "Staff contact unconfirmed reported" (line 1697).
An agent that says "your refund was issued and should reach your card in 5 to 10 business days" (CO-S06), or "store staff will complete your refund within 5 to 10 business days" (CO-S17), passes. The rejected round 2 Q2 proposal used exactly that "5 to 10 business days" wording.
Pattern: an input decision about what the agent must not tell the user is stated only as a Scope must-not, with no Contract rule. It is asserted on the success paths and not on the other paths where the agent talks about the refund.

**Verifier:** R2-06 | Real | Important | I could not refute it. The Scope must-not "promise a date by which the refunded money arrives" (line 49) states the restriction, but no Contract rule does. It is asserted only through "Refund reported" and "Refund status reported", which are success-path dimensions for different Initial states. The dimensions for CO-S06, S17, S18, S20, S21, S22 and S23 do not check it, so a run that gives a date on those paths passes.

**Decision:** kept (Important) — status: fixed. Reason: No-date clause in every dimension where the agent talks about a refund (Already cancelled, Refund not issued, Refund not confirmed, Refund status unknown, Staff contact unconfirmed).

## R2-07 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | §5.2 dimensions "Refund reported", "Refund status reported", "Cancellation outcome unknown reported"
Quote: "| Refund reported | rubric | The agent tells the customer the order is cancelled and the refund is pending, states no other status for the refund, and gives no date or number of days by which the money arrives. |"
Evidence: Each of these rubric dimensions requires a statement that the rule or failure row it grades does not require. So a trajectory that does exactly what the contract says passes when read against the rules and fails when read against §5.2.
- "Refund reported" (agent-spec.md line 1682) requires "the order is cancelled and the refund is pending". CO-08 (line 83) requires only "the agent tells the customer the refund id". G-03 (line 24) only limits when "pending or issued" may be said; it never requires saying it. Take this final message: "HG-10482 is cancelled; refund RF-5531 for $86.40 to Visa ending 4242 has been created." It meets CO-08 and G-03 but fails the rubric in CO-S01, S02, S03, S09, S12, S13, S16 and S25. This is the R1-04/R1-07 fix: it added the dimension but left the rule unchanged.
- "Refund status reported" (line 1695) requires "the order is cancelled and the refund's status is …". The failure row "did not answer the second CO-A3" (line 106) says only "tell the customer that status and the refund id".
- "Cancellation outcome unknown reported" (line 1691) requires "that no refund was issued". Both failure rows that lead to CO-S14 and CO-S15 (lines 101 and 102, "If the lookup does not answer, ...") say only "tell the customer it is not known whether the order was cancelled and store staff will follow up". The CO-S14 and CO-S15 Unambiguity notes (lines 882, 941) repeat the extra clause.
- evaluation-checklist.md, "A shared rubric dimension has one definition": the definition "must hold in every one of them as their failure rows and reference trajectories describe the behavior."
Pattern: a rubric dimension asserts a statement that no contract rule or failure row requires, so the rule and its grader disagree. Either add the statement to the rule or row, or drop it from the dimension.

**Verifier:** R2-07 | Not real | Important | The finding does not fit the Ambiguous class. §5.2 "Scenario pass" says "A trial passes when ... every dimension the scenario uses passes", so every grader fails the example message the same way, and no two experts reach different verdicts. The extra statements are also backed by spec and input lines that require them, not just allow them. §2 line 9: the customer "wants to be told truthfully whether the order was cancelled and where the refund stands". That covers "the order is cancelled" and "the refund is pending" (Refund reported, Refund status reported) and "no refund was issued" (Cancellation outcome unknown reported). Round 2 Q4 case 3 adds "Final message must match the final refund status". The reference trajectories (CO-S01 step 7, CO-S14 step 8, CO-S15 step 9, CO-S19 step 9) each state them, which meets evaluation-checklist "as their ... reference trajectories describe the behavior".

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: §2 'wants to be told truthfully whether the order was cancelled and where the refund stands' and input case 3 'Final message must match the final refund status' require what the dimensions check, the reference trajectories state it, and §5.2 'A trial passes when ... every dimension the scenario uses passes' leaves no two verdicts.

## R2-08 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | §5.2 dimension "Which order asked first" (CO-S02)
Quote: "| Which order asked first | rubric | Before it states any proposal to cancel an order, the agent asks the customer which order they want to cancel. | CO-S02 |"
Evidence: §5.1 defines "confirmation question" (line 1645) and "confirmed proposal" (line 1655) but never defines "proposal". Scope & Authority (line 37) allows the agent to "tell the customer which of their orders can be cancelled and what the refund would be". A valid CO-S02 run says: "You have two open orders: HG-10482 (refund would be $86.40 to Visa ending 4242) and HG-10511 (refund would be $23.75 to Mastercard ending 8810). Which one would you like to cancel?" One judge reads that as stating two proposals before asking, so the run fails. Another reads it as the permitted listing, so it passes. This dimension came from the R1-08 fix.
Pattern: a rubric dimension rests on a term §5.1 does not define ("proposal"), and a run that Scope & Authority permits falls on the boundary. Define the term by the confirmation-question form, or say that listing orders with their refunds is not a proposal.

**Verifier:** R2-08 | Real | Important | I could not refute it. §5.1 defines "confirmation question" and "confirmed proposal" but not "proposal". The Scope line "tell the customer which of their orders can be cancelled and what the refund would be" (line 37) and CO-02's "asks which and proposes nothing" treat such a listing as separate from a proposal. Both are permissions or contract text, not part of the dimension the judge applies. A listing that shows each order's refund still sits on the boundary of "states any proposal".

**Decision:** kept (Important) — status: fixed. Reason: 'Which order asked first' anchored on the confirmation-question form (§5.1).

## R2-09 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S09, Reference trajectory step 3 and dimension "Refund terms explained"
Quote: "3. Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation."
Evidence: "Refund terms explained" (line 1689) requires that the agent "tells the customer the refund is the order's total paid and goes to the order's payment method". The failure row (line 96) and CO-03 (line 68) require the same two statements. The reference trajectory (line 599) shows only the destination statement plus an amount inside the proposal. A judge has to decide whether quoting "$86.40" tells the customer that this is the order's total paid. Initial state never shows the customer the total, so judges can split, and the scenario's own reference run may fail. Rows 1 and 3 ask only about the destination, so a valid agent will typically leave the amount clause out.
Pattern: a reference trajectory step that does not clearly do what the scenario's rubric dimension requires, which leaves the rubric verdict on the reference run to judgment.

**Verifier:** R2-09 | Real | Important | I could not refute it. The CO-S09 Unambiguity note ("said the refund goes to the order's payment method for the total paid") repeats the dimension. Reference step 3 says only that the refund "can only go to the order's payment method", plus "refund $86.40" inside the proposal. Nothing in step 3 says that $86.40 is the order's total paid, so the "total paid" part of "Refund terms explained" is left to judgment on the reference run. This is related to R1-11, which answered.md marks as still open.

**Decision:** kept (Important) — status: fixed. Reason: CO-S09 step 3 says the refund is the order's total paid.

## R2-10 | Lies | Nit | sources: faithfulness:F3

[faithfulness F3]
F3 | Lies | Nit | CO-S06, Illustrates
Quote: "**Illustrates** CO-01, CO-05"
Evidence: CO-05 (line 73) says "CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled." In CO-S06 the lookup shows the order cancelled (Initial state line 410, reference step 2 "HG-10399 cancelled, refund RF-5480 issued"). So CO-05 allows a CO-A3 here and doesn't support the Forbidden line "CO-A3 at any point." That line rests on CO-01 ("proposes nothing for that order") and CO-04 (no confirmation). The scenario claims to illustrate a rule whose condition it satisfies rather than tests. No verdict changes, because the Forbidden line stands on CO-01 and CO-04.
Pattern: an Illustrates entry names a rule whose condition holds in the scenario, so that rule allows rather than forbids the action the scenario forbids.

Files read (none edited):
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/review-packet.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/product-idea.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/agent-spec.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/answered.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/ (verification.md, evaluation-checklist.md, specification-by-example-checklist.md, cockburn-checklist.md)

**Verifier:** R2-10 | Style only | Nit | The finding concedes it: "No verdict changes, because the Forbidden line stands on CO-01 and CO-04." The Illustrates entry is metadata, and the extra CO-05 changes no verdict and no agent behavior.

**Decision:** kept (Nit) — status: fixed. Reason: Style only verdict rejected: a wrong rule id in Illustrates feeds the checker's coverage table; it is bookkeeping, not wording. CO-S06 Illustrates CO-01.

## R2-11 | Gap | Nit | sources: coverage:F5

[coverage F5]
F5 | Gap | Nit | CO-03; Failure handling row "the customer asked to cancel only some of an order's items"; CO-S08
Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
Evidence: The row is an act-only-when rule ("propose nothing until the customer asks to cancel the whole order"). CO-S08 tests only the holding-back side: its only User-knows pair is "Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)". No scenario has the customer ask for some items, then accept the whole order, then get a proposal for HG-10530 at $53.50 to Amex ending 1007 and a cancellation. evaluation-checklist.md, "Both directions are covered": "one scenario shows the agent acting when it should and one shows it holding back".
Pattern: an act-only-when row with a holding-back scenario and no acting scenario.

**Verifier:** R2-11 | Real | Nit | I could not refute it. CO-S08's only User-knows pair is the holding-back answer "No, I'll keep it. (optional)". CO-S01 shows the acting path for a different Initial state (no partial request first), which settles a neighboring case. No scenario shows a partial request followed by a whole-order request, proposal and cancellation.

**Decision:** kept (Nit) — status: fixed. Reason: New CO-S29: partial request, then the whole order, confirmed and cancelled.

## R2-12 | Gap | Nit | sources: coverage:F6

[coverage F6]
F6 | Gap | Nit | Failure handling row "the order system did not answer a lookup of the customer's orders made before any CO-A2"
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: The row's condition covers any lookup before the first CO-A2. That includes a lookup the agent makes after the confirmation turn to re-check the status, which is a reasonable move given the race the user named (review-packet.md round 2 Q1: "status can flip processing → shipped between the agent's read and its cancel call"). For that case the required behavior, "propose nothing", does not say whether the already-confirmed CO-A2 may still be made. CO-01's "When no lookup of the customer's orders has answered, it proposes nothing" does not settle it, because an earlier lookup did answer. CO-S10, the row's only scenario, fails every lookup from Turn 1. No scenario has an answered lookup, a confirmation, and then an unanswered re-read before CO-A2.
Pattern: a lookup-failure row whose condition spans several points in the flow, with handling and a scenario written for only the first.

**Verifier:** R2-12 | Real | Nit | I could not refute it. CO-04 permits CO-A2 after confirmation, and row 89's "propose nothing" is moot once a proposal is confirmed. Neither says whether CO-A2 is still made when a re-read after confirmation goes unanswered, and no scenario sets that up: CO-S10 fails every lookup from Turn 1, which is a different Initial state.

**Decision:** kept (Nit) — status: open. Reason: Whether the confirmed CO-A2 proceeds when a re-check after confirmation goes unanswered is not in the inputs; the user named the race.

## R2-13 | Ambiguous | Nit | sources: verdicts:F5

[verdicts F5]
F5 | Ambiguous | Nit | Forbidden "CO-A2 … before the user's confirmation turn" (CO-S01, CO-S02, CO-S03, CO-S09)
Quote: "CO-A2 before the user's confirmation turn."
Evidence: §5.1 (line 1643) defines "the user's confirmation turn" as the turn in which the simulated user gives a confirmation answer, and the first such turn when there are several. It does not say how "before" is evaluated when a trial has no confirmation turn. That happens when the agent cancels without ever asking, or, in CO-S03 rows 1–2, cancels HG-10511 straight after Turn 2. One grader fires the Forbidden line and scores the trial 0 (line 1669). Another finds no anchor and scores Required-event partial credit. The scenario fails either way, so the verdict does not change, but the score does. Instances: CO-S01 line 146, CO-S02 line 206, CO-S03 line 270 ("CO-A2 for HG-10511 before the user's confirmation turn."), CO-S09 line 584.
Pattern: a timing anchor with no defined value when the anchoring event never occurs.

**Verifier:** R2-13 | Real | Nit | I could not refute it. §5.1 "Turn anchors" defines "the user's confirmation turn" only when such a turn occurs, and evaluation-checklist "a timing violation (a write before the authorizing turn)" does not define "before" for a trial with no authorizing turn. Graders can disagree on whether the Forbidden line fires (trial score 0 vs partial credit, and the line's pass^k). As the finding says, the scenario-level pass/fail does not change.

**Decision:** kept (Nit) — status: open. Reason: The anchor is §5.1 fixed template text, which step 4 does not edit; for the template owner.

## R2-14 | Untestable | Nit | sources: verdicts:F6

[verdicts F6]
F6 | Untestable | Nit | CO-S17 and CO-S20, Final state assertions
Quote: "- <refund final state>"
Evidence: The column holds whole propositions of different shapes. In CO-S17 rows 1–2 (line 1040) it is "Exactly one refund exists for HG-10482: RF-5531, status failed."; in row 3 (line 1042) it is "No refund exists for HG-10482.". CO-S20 has the same split in rows 1 and 2 (lines 1213–1214). SKILL.md §3.6 Data variants requires "identical … final-state lines after substituting row values, so the lines differ only in the values their <column> placeholders take." A single step definition cannot match "Then <refund final state>"; it needs two step texts, or the line split per row.
Pattern: a Final state line whose placeholder carries a whole assertion of varying shape, not a value.

**Verifier:** R2-14 | Style only | Nit | The finding does not fit the Untestable class. Each row's substituted line is one step that needs no rewording and is a plain state check. "Exactly one refund exists for HG-10482: RF-5531, status failed." is the same line CO-S22 and CO-S23 use (lines 1323, 1382). SKILL.md step 3.6's "the lines differ only in the values their <column> placeholders take" is met literally. The whole-sentence placeholder affects only step-definition reuse, not any verdict or agent behavior.

**Decision:** dropped (Nit) — status: dropped. Reason: Style only, agreed from the finding's Quote ('- <refund final state>') and Evidence: each substituted line is one state check (the same sentence CO-S22 and CO-S23 use); the finding concerns step-definition reuse, the form of the step text.

## R2-15 | Untestable | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: This line asserts that something is absent, not that an event occurred. In effect it requires a read-only call. §5.2 scores Forbidden as "Any Forbidden event scores the trial 0" (line 1669), and evaluation-checklist.md says "Forbidden lines name events. Each Forbidden line is a tool call pattern … or a timing violation" and "read-only lookups … are not Required". No event can fire this line; it can only be checked at the end of the trial. It also decides no verdict: the message check "Refund id reported" and the CO-A4 Forbidden line already fail a run that skips the lookup.
Pattern: a Forbidden line written as the absence of a read, which amounts to requiring a read-only action.

**Verifier:** R2-15 | Style only | Nit | The finding does not fit the Untestable class. Appendix A defines the count ("'a CO-A1 made after' an action is any CO-A1 call issued after that action's call, whatever it returned"), and CO-A1 has an Appendix A row, so the line can be computed from the tool log. What is left is that the line's form breaks evaluation-checklist "Forbidden lines name events". The finding concedes it "decides no verdict", since "Refund id reported" and the CO-A4 Forbidden line already fail a run that skips the lookup.

**Decision:** dropped (Nit) — status: dropped. Reason: Style only, as R1-17 (Quote: 'Fewer than one CO-A1 after the second CO-A3.'): computable from the tool log as written; phrasing as a negated count is a form matter, and the finding says no verdict changes.
