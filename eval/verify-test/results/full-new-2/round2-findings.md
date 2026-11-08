# Round 2 findings (full-new-2)

Round 2 (re-review header, bundle eval/verify-test/run/rereview-r2.md): three finders in parallel, faithfulness and coverage (general-purpose, Opus 5.5) and verdicts (codex:codex-rescue). The Codex verdicts finder handed back with no report (its Codex job was still running) and was messaged to collect it; per 4.3 the round went to 4.4 when the two non-Codex finders had returned (19:38:45Z). Its findings, if they arrive, go to round 3.
The round-1 Codex verdicts finder's late findings were folded into this round: R2-L1 (duplicate of R1-06), R2-L2, R2-L3.
Raw counts: faithfulness 4 (1 Important, 3 Nit) + 1 Pre-existing line; coverage 5 (1 Important, 4 Nit); verdicts/Codex: no report in time.
Count line (merged, round-2 finders): 7 findings: 2 Important, 5 Nit. With the late round-1 Codex findings: 9 findings: 4 Important, 5 Nit (R2-L1 not counted, a duplicate of R1-06).
Routing (4.4): to verifiers (Important): R2-01, R2-02, R2-L2, R2-L3. Straight to fix (Nit): R2-03, R2-04, R2-05, R2-06, R2-07.
After verification: 4 kept (1 Important; 3 Nit after splits), 0 dropped. Verifier drop rate 0/4.
Status: fixed 8 (R2-01, R2-03, R2-04, R2-05, R2-06, R2-07, R2-L2, R2-L3); open 1 (R2-02); Pre-existing 1.
Previous-round attribution (kept findings from round-2 finders): quote a line round 1 changed: 7 (R2-01, R2-02, R2-03, R2-04, R2-05, R2-06, R2-07); quote a line round 1 did not change: 0. In a bundle context block: 0 kept (the one Pre-existing line). Late round-1 Codex findings R2-L2 and R2-L3 quote round-0 lines (defects round-1 finders missed).

Each finding is quoted verbatim from the first finder in its Sources line (ids renumbered R2-nn; R2-Ln are late round-1 Codex findings). Verifier lines are verbatim.

## R2-01 (Important)
Sources: faithfulness F1

R2-01 | Lies | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (section 3)
Quote: "Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers. ... If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: The row's first sentence says no CO-A4 until a lookup *answers*. Its last branch then requires CO-A4 when the lookup does *not* answer. The row contradicts itself. CO-S15 (section 2) sets Initial state "The order system does not answer any CO-A1 the agent makes after its second CO-A2", so under the opening clause no lookup ever answers and CO-A4 is never allowed. Yet CO-S15 Required events demand "CO-A4 occurs exactly once, for <order>, reason cancellation unknown, after the second CO-A2", and its Forbidden line uses a different condition: "CO-A4 before a CO-A1 *made* after the second CO-A2", not one that *answers*. Reads may be retried without limit (review-packet.md, tool confirmation turn, change 4). So an agent that follows the opening clause can keep retrying the lookup and never hand off, and it fails CO-S15. The first-CO-A2 row (section 4) says "Make no CO-A2 or CO-A3 until a lookup made after it answers". It leaves CO-A4 out of that clause, so it is consistent. The fix round added "or CO-A4" to the new row and broke that.
Pattern: A "no X until a lookup answers" gate also lists an action that a later branch requires when the lookup does not answer. Gate on "until a lookup has been made after it", matching the Forbidden lines, or take CO-A4 out of the gate.

Routing: Important, to verifiers.
Standard verifier: R2-01 | Real | Important | The row's gate "no CO-A3 or CO-A4 until a lookup made after it answers" can never be met when the lookup fails, yet its last branch requires "make CO-A4 with reason cancellation unknown". The gate also contradicts round 3 Q4 ("Re-read fails, say outcome unknown, issue no refund, hand off"), so the Lies class fits. It does not match CO-S15's Forbidden line ("CO-A4 before a CO-A1 *made* after the second CO-A2") or the first-CO-A2 row, which leaves CO-A4 out of its gate. Reads can be retried without limit (tool confirmation change 4), so an agent that obeys the gate never hands off and fails CO-S15's Required CO-A4.
Adversarial verifier: R2-01 | Real | Important | I could not refute it. The row's opening clause in spec line 105 is "no CO-A3 or CO-A4 until a lookup made after it answers", and its last branch is "If the lookup does not answer ... make CO-A4 with reason cancellation unknown". The row contradicts itself. Its gate also contradicts CO-07 ("when the agent cannot tell whether the order was cancelled, the agent makes CO-A4") and the input in round 3 Q4 ("Re-read fails, say outcome unknown, issue no refund, hand off"). Appendix A defines only "a CO-A1 made after", not "answers", so it does not rescue the wording. CO-S15's Forbidden line and Unambiguity note grade the case correctly ("a handoff before a lookup was tried fails"), but that confirms the contradiction rather than settling it. The packet's tool confirmation turn says "Reads may be retried on timeout without limit", so an agent built from the row can retry lookups forever and never hand off, which is production misbehavior. The first-CO-A2 row at line 104 leaves CO-A4 out of its gate and is consistent.
Decision: kept, Important. Both Real.
Status: fixed. Row now reads "Make no further CO-A2; make no CO-A3 until a lookup made after it answers, and no CO-A4 until a lookup has been made after it."

## R2-02 (Important)
Sources: coverage F1

R2-02 | Gap | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (placed-or-processing branch); CO-S27
Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 or CO-A4."
Evidence: product-idea.md lines 5-6 ("A customer should be able to ... cancel an order they placed and get their money back"). The order is still cancellable, but the agent cannot cancel it in this conversation: CO-06 (bundle §4) allows "at most two CO-A2 ... in a conversation", and CO-07 says "CO-A4 occurs in no other situation". So no rule gives the customer a next step. The dimension "Cancellation not made reported" (bundle §2) even forbids saying staff will follow up. Compare the CO-A4 second-unanswered row (bundle §4), which tells the customer "to contact Harbor Goods customer support" once retries run out. The interview never decides this case: round 3 Q4 covers only the first unanswered cancel (review-packet.md, Round 3). In CO-S27 the agent passes by saying "not cancelled" and stopping, while the customer's open order goes on to ship.
Pattern: when the retry budget is spent and the order can still be cancelled, the customer's goal is left unmet and no rule says what next step the agent offers (try again later, contact support, or a handoff).

Routing: Important, to verifiers.
Standard verifier: R2-02 | Real | Important | In the placed-or-processing branch, CO-06 allows at most two CO-A2 and CO-07 says "CO-A4 occurs in no other situation". So the agent stops with "not cancelled" and offers no next step, while the order can still be cancelled and goes on to ship. The primary actor's interest ("wants the order they mean cancelled", §2) has no rule protecting it here. Round 3 Q4 covers only the first unanswered cancel. Compare the second-unanswered CO-A4 row, which tells the customer to "contact Harbor Goods customer support". The fix needs a user decision. It would also change CO-S27, where an agent that just stops now passes.
Adversarial verifier: R2-02 | Not real | Nit | The case is settled and asserted. Row 105 says "If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 or CO-A4". CO-S27 asserts it through dimension "Cancellation not made reported" ("...never says the order was cancelled, a refund was issued or store staff will follow up"). That meets the brief's condition for refuting a Gap. The "next step" the finding wants is not an interest any stakeholder in §2 or any input names. The support team wants only orders "whose refund is unfinished or whose cancellation is uncertain", and here the order is known not to be cancelled. The two-cancel limit comes from the user ("send the cancel once more"; "only commit calls are bounded"). The "contact Harbor Goods customer support" step the finding points to comes from the user's change 3 for the handoff timeout only, not from a general rule. No rule stops the agent suggesting a later retry, so this is a preference for an extra rule ("one more ... would be nice"), not a missing contract item.
Decision: kept, Nit. Split: standard Real Important, adversarial Not real Nit; kept at the lower severity, Nit. Adversarial refutation: "The case is settled and asserted. Row 105 says 'If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 or CO-A4'. CO-S27 asserts it ... The 'next step' the finding wants is not an interest any stakeholder in §2 or any input names."
Status: open. Which next step, if any, the agent offers when both cancellations went unanswered and the lookup shows the order still open (try again later, contact support, or a staff handoff) is a business decision the inputs do not make (round 3 Q4 covers only the first unanswered cancel); the standard verifier also says the fix needs a user decision.

## R2-L2 (Important)
Sources: r1-verdicts-codex (late) F2

R2-L2 | Ambiguous | Important | CO-S01–CO-S24, Initial state and Final state assertions  
Quote: "- No follow-up task exists."  
Evidence: Every scenario asserts either zero or exactly one follow-up task: CO-S01:141, CO-S02:201, CO-S03:263, CO-S04:320, CO-S05:372, CO-S06:422, CO-S07:471, CO-S08:521, CO-S09:576, CO-S10:630, CO-S11:680, CO-S12:735, CO-S13:792, CO-S14:850, CO-S15:908, CO-S16:967, CO-S17:1025, CO-S18:1081, CO-S19:1137, CO-S20:1195, CO-S21:1255, CO-S22:1316, CO-S23:1375, and CO-S24:1429. No scenario supplies a pre-conversation follow-up-task baseline; the only Initial-state task references describe effects of later CO-A4 calls. The checklist requires every fact on which the verdict depends to have a concrete Initial-state value. Thus a pre-existing task can make the same trajectory pass or fail, and "No follow-up task exists" can also be read globally or as limited to the scenario order.  
Pattern: A final record-count assertion has no corresponding initial full-set baseline and no stated scope.

Routing: Important, to verifiers.
Standard verifier: R2-L2 | Real | Nit (downgraded from Important) | No Initial state says whether any follow-up task exists, even though the spec states absences explicitly for orders and refunds ("The customer has no other orders", "No refund exists"). So the Ambiguous class technically fits. But §5.1 reads Final state assertions "against Initial state", and no Initial state lists a task. A harness therefore starts with an empty task store, and the global-vs-order scope question changes no verdict when the store starts empty. The finding's line numbers are off by about 4-5 (e.g. CO-S01's line is 145, not 141). It also misses the same line in the new in-scope CO-S25, CO-S26 and CO-S27.
Adversarial verifier: R2-L2 | Not real | Nit | No fact is left open. The evaluation checklist requires "existing records with their fields" in Initial state ("Concrete initial state") and says "Each trial starts from the Initial state with no leftovers" ("Isolated trials"). §5.1 says "Final state assertions ... are read against Initial state". So a follow-up task that Initial state does not list does not exist. Reading the count globally or per order gives the same verdict. Per Appendix A, CO-A4 is the only thing that creates a task ("Creates one follow-up task on its first call..."), and every scenario already forbids an extra one ("CO-A4 at any point" or "A second CO-A4"). It also falls mostly outside scope: most of the listed scenarios are unchanged and not in bundle sections 1 to 3.
Decision: kept, Nit. Split: standard Real (downgraded to Nit), adversarial Not real Nit; kept at Nit. Adversarial refutation: "No fact is left open. The evaluation checklist requires 'existing records with their fields' in Initial state ... So a follow-up task that Initial state does not list does not exist."
Status: fixed. Every scenario's Initial state now has "- No follow-up task exists." (pattern edit, 27 scenarios).

## R2-L3 (Important)
Sources: r1-verdicts-codex (late) F3

R2-L3 | Untestable | Important | CO-S03 and CO-S04, User  
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""  
Evidence: The same trigger appears in CO-S03:248 and CO-S04:308. Section 5.1 defines a confirmation question more narrowly as one stating every proposal value; it does not define the looser event "a question that proposes cancelling … and asks to go ahead." The checklist requires a scripted User turn to be anchored to a defined §5.1 event, not merely a proposal or offer. A partial question such as asking only whether to cancel HG-10482 could therefore trigger Turn 2 under one conversion but not another.  
Pattern: A scripted User turn is anchored to an informal message description instead of a defined harness event.

Sources (commands Codex ran, all read-only):
- Spec lines 17-21, 56-72, 238-252, 300-311, 1457-1465 in /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/verify-test/run/agent-spec.md
- rg for follow-up-task assertions over the same spec
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/evaluation-checklist.md lines 34-41

Routing: Important, to verifiers.
Standard verifier: R2-L3 | Real | Nit (downgraded from Important) | The trigger "the agent's first question that proposes cancelling HG-10482 and asks to go ahead" is not a §5.1 event. The checklist rule says "A User turn's trigger names an event §5.1 defines... never 'a proposal'". §5.1's "wrong-value question" would fit, since CO-S03's only confirmation pair is for HG-10511. However, a partial and a full HG-10482 question both end with Turn 2 and an HG-10511 re-proposal, and CO-S04 passes either way (no Required events), so no realistic verdict changes. This finding is also out of scope. The trigger line is unchanged pre-existing text (not in CO-S03's hunks), and CO-S04 is a section-4 context block, so it should have been reported as a one-line Pre-existing item.
Adversarial verifier: R2-L3 | Not real | Nit | The quoted line does not say what the finding claims. "the agent's first question that proposes cancelling HG-10482 and asks to go ahead" has no "states every value" condition, so a partial question plainly triggers Turn 2. No reading excludes it, and the simulated user, an LLM, can act on the line without rewording (§5.2: "It says the User turns on its own, at the points they state"). Where Turn 2 fires changes no verdict. No User-knows pair confirms HG-10482, and under §5.1 a question with a wrong value "is not the confirmation question; the simulated user deflects it". The Unambiguity notes settle both scenarios. CO-S03: "in every row it confirms nothing; any action on HG-10482 ... fails in the action log". CO-S04: "no confirmation is ever given, so any cancellation, refund or handoff fails". This one is the closest call: the wording does break the evaluation checklist item "A User turn's trigger names an event §5.1 defines ... never 'a proposal'", but it changes no verdict. SKILL.md line 109 itself uses "in reply to the agent's proposal, in place of a confirmation" as its example, though SKILL.md is not one of the sources the brief counts as evidence. The line is also out of scope: it is unchanged, not in a CO-S03 hunk, and CO-S04 is not in the bundle.
Decision: kept, Nit. Split: standard Real (downgraded to Nit), adversarial Not real Nit; kept at Nit. Adversarial refutation: "The quoted line does not say what the finding claims ... a partial question plainly triggers Turn 2 ... Where Turn 2 fires changes no verdict."
Status: fixed. CO-S03 and CO-S04 Turn 2 now: "in reply to the agent's first question that states cancelling HG-10482 and refunding $86.40 to Visa ending 4242 and asks to go ahead, in place of a confirmation".

## R2-03 (Nit)
Sources: faithfulness F2, coverage F4

R2-03 | Lies | Nit | CO-S26, Initial state / Data variants row 2
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's second CO-A2 reaches the order system, and status <final status> from that moment on" with row "| 2 | delivered |"
Evidence: Row 2 has the order jump from processing straight to delivered, mid-conversation, at the moment of a cancel call. The only race the inputs describe is "status can flip processing → shipped between the agent's read and its cancel call" (review-packet.md, Round 2 user answer, Q1). The status list is placed, processing, shipped, delivered, cancelled. Nothing supports an instant processing-to-delivered change that skips shipped. CO-S11 uses only shipped for the same race. The verdict does not change, because shipped and delivered are handled the same way.
Pattern: A data-variant row invents a domain transition that the inputs' state model does not allow.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept (Nit, not verified).
Status: fixed. CO-S26 rewritten with the processing-to-shipped race only; rows are HG-10482 and HG-10530 (both processing, shipped at the second CO-A2). Dropped row: old row 2 (final status delivered), which exercised the delivered branch of the same failure-row clause; the shipped-or-delivered branch stays exercised by row 1.

## R2-04 (Nit)
Sources: faithfulness F3, coverage F5

R2-04 | Lies | Nit | row: CO-A3 issue the refund (Appendix A, section 3): the R1-09 fix is incomplete
Quote: "refund failed: returns the refund with `status: \"failed\"`; payment provider temporarily unavailable: `ProviderUnavailable`"
Evidence: The fix took `failure_reason` out of CO-A3's result. The refund record now has only refund id, order number, amount, payment method and status (review-packet.md, Round 2 Q3 and the user's changes). But three reference trajectories still show the tool returning a failure reason. CO-S17 step 6: "Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed." CO-S22 step 6 and CO-S23 step 6 say the same: "refund RF-5531, failed, card closed". CO-A3 can no longer produce that result. A side effect: CO-S17 rows 1 and 2, and CO-S23 rows 1 and 2, now differ only in a cause the agent cannot observe.
Pattern: When a field is removed from a tool's result, some reference trajectories still show that field in the tool's result.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept (Nit, not verified).
Status: fixed. CO-S17, CO-S22 and CO-S23 step 6 now read "Agent → CO-A3 (HG-10482) → refund RF-5531, failed." The CO-S17 and CO-S23 rows that differ only in an unobservable cause stay: each scenario has one such row, which step 3.6 allows.

## R2-05 (Nit)
Sources: faithfulness F4

R2-05 | Ambiguous | Nit | failure: CO-A2 | the order system did not answer the second CO-A2 (section 3), lookup-does-not-answer branch
Quote: "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: The row lists telling the customer "store staff will follow up" before making CO-A4. CO-07 says the agent "tells the customer store staff will follow up once the order system has created the task". The CO-A4 double-timeout row says that if CO-A4 goes unanswered twice, the agent tells the customer "it could not confirm store staff were told, and to contact Harbor Goods customer support". Read in order, this row lets the agent promise follow-up before the task exists, which conflicts with CO-07 and G-03. The two new CO-A3 rows in section 2 list CO-A4 first and the message second, so the spec orders these steps inconsistently. Instances: this row, plus the first-CO-A2 row (section 4, pre-existing, same wording).
Pattern: A failure-row action list puts the "staff will follow up" message ahead of the CO-A4 it depends on.

Pre-existing: failure row "CO-A2 | the order system did not answer the first CO-A2" (section 4) has the same message-before-CO-A4 ordering as F4.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept (Nit, not verified).
Status: fixed in the new "second CO-A2 unanswered" row (CO-A4 now precedes the message). The same ordering in the first-CO-A2 row was reported Pre-existing and left untouched.

## R2-06 (Nit)
Sources: coverage F2

R2-06 | Gap | Nit | failure: any | the customer named no order, and none of their orders has status placed or processing; CO-S05 row 4
Quote: "Tell the customer, for each of their orders, what CO-01 says for its status; propose nothing."
Evidence: the only scenario that triggers this row is CO-S05 row 4. There the customer has one order, HG-10466, status delivered, and "The customer has no other orders" (spec CO-S05 Initial state). No scenario gives a customer several non-open orders, or an order with status cancelled, under this row. So the "for each of their orders" clause and the cancelled branch of CO-01 ("tells the customer the order is already cancelled") are never asserted here. An agent that reports only one of several orders would pass.
Pattern: a per-item telling clause exercised only with a single item and a single status.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept (Nit, not verified).
Status: fixed. Row now: "Tell the customer none of their orders can be cancelled, and, when any of them has shipped or been delivered, that returns are a separate process; propose nothing." No per-order clause remains, so CO-S05 row 4 exercises it in full.

## R2-07 (Nit)
Sources: coverage F3

R2-07 | Gap | Nit | failure: any | the customer named no order, and none of their orders has status placed or processing
Quote: "the customer named no order, and none of their orders has status placed or processing"
Evidence: a signed-in customer with no orders at all meets this condition (vacuously). The row's action, "for each of their orders, what CO-01 says", then produces no message. No rule says what the agent tells a customer who has no orders (CO-01, bundle §4, speaks only of orders with a status), and no scenario covers it.
Pattern: a condition that also matches the empty set, with an action defined only over its members.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept (Nit, not verified).
Status: fixed by the same row rewrite: the message is defined for a customer with no orders.

## R2-L1 (late round-1 Codex F1)
Sources: r1-verdicts-codex F1. Duplicate of R1-06 (explicit request to cancel two orders), which round 1 verified (both Real) and left open. Not re-verified; status open (with R1-06).

## Pre-existing (one line, from the faithfulness finder)
Pre-existing: failure row "CO-A2 | the order system did not answer the first CO-A2" (section 4) has the same message-before-CO-A4 ordering as F4.
Status: Pre-existing, reported, left untouched.

## Round 2 Codex verdicts finder
First hand-back had no report (Codex call ended while Codex was still working). Messaged with SendMessage at ~19:36Z; second notification (~19:42Z) said it was again waiting on background work, with no report. Its findings, if they arrive, are folded into round 3.
