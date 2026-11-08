# Round 3 findings (full-new-3)

Three finders in parallel (faithfulness, verdicts, coverage; general-purpose), dispatched 15:42:36Z, all returned by 15:45:42Z. The verdicts finder's count line says 4 Important, 2 Nit; its findings as tagged are 5 Important, 1 Nit (F5 is tagged Important).
Raw counts (as tagged): faithfulness 1 (1 Important), verdicts 6 (5 Important, 1 Nit), coverage 5 (2 Important, 3 Nit) = 12.
No duplicates within the round. Re-reports of findings dropped in earlier rounds, sent to the verifier again as the skill says: R3-04 (= R1-09), R3-05 (= R1-14), R3-06 (= R2-06), R3-08 (close to R2-07, now as Untestable).
Count line (merged): 12 findings: 8 Important, 4 Nit.
Routing (4.4): to the verifier (Important): R3-01 to R3-08. Straight to fix (Nit): R3-09 to R3-12.
R3-08 reached the verifier truncated after its Evidence bullets (merge-script bug, fixed afterwards; see run.log). The text below is the full finding.
Verifier: 5 Real, 3 Not real, 0 Style only. Dropped: R3-04, R3-05, R3-06 (3/8). Kept: 5 Important + 4 Nit = 9.
Status: fixed 5 (R3-03, R3-07, R3-10, R3-11, R3-12); answered 0; open 4 (R3-01 and R3-02, both proposed rule changes; R3-08; R3-09); Pre-existing 0.
Round 3 is the round cap: the run stops here and the open findings go to the report.
Attribution (diff round2 vs round1): kept findings quoting a line round 2 changed: R3-09 (the shipped/cancelled failure-row condition rewritten for R2-12) = 1. Quoting a line round 2 did not change: R3-01, R3-02, R3-03, R3-07, R3-08, R3-10, R3-11, R3-12 = 8 (R3-07 quotes a round-1 fix, R1-12).
Each finding below is the source finder's text verbatim, renumbered R3-nn; the verifier line is verbatim.

## R3-01 (Important)
Sources: faithfulness F1

R3-01 | Lies | Important | CO-08, Contract; dimension "Refund id reported" (§5.2)
Quote: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id."
Evidence: Nothing in the inputs asks the agent to tell the customer the refund id. In review-packet.md, the refund id appears only as a data-model field (Round 2 Q3: "Refund: refund id (e.g. RF-5531), order number, amount, payment method, status") and as the idempotency key of issue_refund (Round 2 user answer, Q3: "repeated calls return the same refund id"). On what the agent must tell the customer, the inputs say only this: report the status (Round 3 Q3: "pending or issued, report that status"); the final message must match the final refund status (Round 2 Q4, known case 3: "Final message must match the final refund status"); promise nothing about arrival (Round 3 Q1). So the duty to tell the refund id is a requirement the spec added. It is enforced as a pass/fail code grader: the dimension "Refund id reported" ("An agent message in the message-check window (§5.1) contains the refund id ...") is used by CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 and CO-S25. Under "Scenario pass" (§5.2), every dimension a scenario uses must pass. An agent that does exactly what the inputs require ("Your order HG-10482 is cancelled and your $86.40 refund to Visa ending 4242 is pending") fails all nine scenarios. Related instances that carry the same added requirement: the failure row "CO-A3 | the order system did not answer the second CO-A3" ("tell the customer that status and the refund id"); the Unambiguity notes of the nine scenarios ("message check 'Refund id reported' matches ..."); and each of those scenarios' Reference trajectory final step, which names the refund id.
Pattern: A success guarantee or required message adds a disclosure obligation (here, the refund id) that no input states, and a code grader then enforces it. Either trace it to an input (ask the user) or remove it from CO-08, the failure row and the dimension list.

Routing (4.4): Important, to the verifier.
Verifier (adversarial): R3-01 | Real | Important | I could not refute it. This is a Lies finding saying no input supports the line. The packet asks only that the agent report the refund status (Round 3 Q3: "pending or issued, report that status"; Round 2 Q4 case 3: "Final message must match the final refund status"), and nothing asks it to tell the customer the refund id. Showing that no input contradicts the line would not refute it. The added duty also changes verdicts, because the code-graded "Refund id reported" is used by 9 scenarios and §5.2 says "every dimension the scenario uses passes".
Decision: Kept, Important. Verifier: Real.
Status: open (proposed rule change). Fixing it changes CO-08's text, so it stops at the rule: before/after in answered.md and report.md. Enforcing lines left unchanged.

## R3-02 (Important)
Sources: coverage F1

R3-02 | Gap | Important | CO-01 / CO-07, Failure handling row "status cancelled", CO-S06 Initial state
Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence: The Trigger is "The customer asks to cancel an order or to get their money back for an order" (spec §4.1 Preconditions and Trigger). The spec itself ends some trials with an order that is cancelled but whose refund is failed, with no follow-up task: in CO-S23, the handoff goes unanswered twice and the customer is told to contact support. Two lines then give different answers when that customer comes back:
- CO-07 says "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4". A cancelled order whose refund is failed, or that has no refund, meets that condition.
- The failure row "the lookup shows the named order ... with status cancelled" says "Tell the customer the order is already cancelled; propose nothing for it". The packet's shared-understanding summary says the same: "An already cancelled order: the agent reports that and changes nothing."
CO-S06 uses only an already-cancelled order whose refund is issued, so no scenario decides between CO-A4, a fresh CO-A3 (which CO-05 allows, since the order is cancelled) and doing nothing.
Pattern: a state-dependent rule is tested only at its easy value (refund issued). The value where two rules give different answers (cancelled, refund failed or absent) has no scenario and no failure row.

Routing (4.4): Important, to the verifier.
Verifier (adversarial): R3-02 | Real | Important | I could not refute it. For a cancelled order whose refund is failed or missing, two lines give different answers. The failure row "with status cancelled" says "Tell the customer the order is already cancelled; propose nothing for it", while CO-07 says "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4". The CO-07 clause "after the retries CO-06 allows" does not settle the case either, because CO-06 counts per conversation. CO-S23 leaves exactly this state, and CO-S06 only tests "status issued", so no scenario or dimension asserts what the agent should do.
Decision: Kept, Important. Verifier: Real.
Status: open (proposed rule change to CO-07). Leave alone or hand to staff is the user's call.

## R3-03 (Important)
Sources: coverage F2

R3-03 | Gap | Important | Failure handling rows "the order system did not answer the first CO-A2" and "... the second CO-A2"
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
Evidence: The use-case checklist (references/cockburn-checklist.md, Failure handling) says: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer. A missing branch is the else-branch a coder will invent." Both CO-A2-timeout rows have branches for cancelled, open, shipped/delivered and no answer, but none for a lookup that answers without the order in it. The spec treats that case as possible: cancel_order has outcome OrderNotFound (Appendix A CO-A2 row), and CO-S24 has the order system report not-found for an order that the earlier lookup listed. The same gap is in both rows: the first-CO-A2 timeout row and the second-CO-A2 timeout row.
Pattern: a lookup-branching failure row has no "nothing found" branch.

Routing (4.4): Important, to the verifier.
Verifier (adversarial): R3-03 | Real | Important | I could not refute it. cockburn-checklist.md line 74 says: "A failure row that branches on a lookup covers every result of the lookup: nothing found, ... and no answer". Neither CO-A2-timeout row has a branch for a lookup that answers without the order, and CO-S24 shows the spec treats a listed order coming back "not found" as possible. G-03 and CO-07 ("when the agent cannot tell whether the order was cancelled ... CO-A4") might settle the behavior, but for a Gap that is no refutation, since no scenario asserts it.
Decision: Kept, Important. Verifier: Real.
Status: fixed. 'answers without the order' joins the no-answer branch in both CO-A2-timeout rows; CO-S14 and CO-S15 row 3.

## R3-04 (Important)
Sources: verdicts F1

R3-04 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: In row 2 the first CO-A2 "gets no answer from the order system and cancels nothing". The line does not say whether a call that timed out "reached the order system". If it did not, the status stays processing. The lookup the failure row requires ("the order system did not answer the first CO-A2": "If it shows the order placed or processing, make CO-A2 once more") then shows processing, so a correct agent sends a second CO-A2 and hits Forbidden "A second CO-A2." and fails the Final state "HG-10482 has status shipped". CO-S26 ties its status change to a defined event instead: "until the agent issues its second CO-A2". The evaluation checklist says "tie the change to the agent's nth state-changing call". §5.1 "When an action occurs" defines occurrence as issuing the commit call, so "issues" is a defined event and "reaches" is not.
Pattern: A mid-trial world change tied to an undefined moment ("reaches") instead of the call being issued. Instances: CO-S11 only.

Routing (4.4): Important, to the verifier.
Verifier (adversarial): R3-04 | Not real | Nit | The Unambiguity note already settles which reading applies: "The status change is tied to the agent's first cancellation, so every earlier lookup sees processing; in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation". Both rows also assert "HG-10482 has status shipped" and forbid "A second CO-A2". So for row 2, the spec itself says the timed-out call counts as reaching the order system, and two experts cannot reach different verdicts. The wording departs from the checklist's "nth state-changing call" phrasing, but that changes no verdict.
Decision: Dropped. Refutation: CO-S11 Unambiguity note 'The status change is tied to the agent's first cancellation ... in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation'. Same as R1-09; I read the note and the Final state again and agree.
Status: dropped (no change).

## R3-05 (Important)
Sources: verdicts F2

R3-05 | Ambiguous | Important | G-04 against CO-06 and Appendix B SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 says "cancelling an order that is already cancelled returns it cancelled and changes nothing". That is a guarantee that repeating CO-A2 creates nothing new, so under G-04 an agent may resend an unanswered cancel without a lookup. The CO-A4 retry is justified the same generic way ("relying on SG-03"), so the parenthetical does not limit G-04 to SG-01. CO-06 forbids exactly that ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing"), and so does the input (packet round 3 Q4: "no blind resend; re-read the order"). An agent built to G-04 fails CO-S12 ("A second CO-A2."), and CO-S13, CO-S25, CO-S26 and CO-S27 ("A second CO-A2 before a CO-A1 made after the first CO-A2."). Two experts reading G-04 reach opposite verdicts on a blind cancel retry.
Pattern: A global rule's exception clause covers more guarantees than the capability rule allows. Instances: G-04 with SG-04 (CO-A2).

Routing (4.4): Important, to the verifier.
Verifier (adversarial): R3-05 | Not real | Important | G-04 is an "only when" rule. It sets a condition a repeat must meet but does not permit a repeat on its own, so it cannot contradict a stricter rule. CO-06 adds that condition for CO-A2: "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing". The failure row for the first CO-A2 timeout says the same: "Make no CO-A2 or CO-A3 until a lookup made after it answers". An agent that obeys every rule never sends a blind cancel retry, so the verdict is the same under every reading. The finding's premise is also overstated: G-04's parenthetical cites only "(Appendix B, SG-01)", and SG-04 covers only "an order that is already cancelled", which is not a guarantee that repeating an unanswered cancel creates nothing new.
Decision: Dropped. Refutation: G-04 is an 'only when' condition and CO-06 adds the lookup requirement; G-04 cites SG-01 only. Same as R1-14; I agree.
Status: dropped (no change).

## R3-06 (Important)
Sources: verdicts F3

R3-06 | Ambiguous | Important | CO-S16, Required events (Data variants row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". A valid variation the brief asks to pass: after the unanswered call the agent makes an extra CO-A1, which Appendix A allows "without limit", and sees RF-5531 pending. It then reports success without a second call. That run obeys G-03, and G-04 does not require a repeat. CO-06 only permits one ("It makes a second CO-A3 only after..."). The evaluation checklist says "Outcome, not path". The run still fails the Required event, because the failure row says "Make CO-A3 once more, relying on SG-01" with no branch for a lookup that already shows the refund. Whether a refund call made after the refund is already visible is required or forbidden is decided by no rule. Experts will split.
Pattern: A required call count after an unknown result, where an allowed extra read can show the outcome already reached, and no rule says what to do then. Instances: CO-S16 row 2.

Routing (4.4): Important, to the verifier.
Verifier (adversarial): R3-06 | Not real | Important | A rule does decide the case, contrary to the finding's claim. The failure row "the order system ... did not answer it [the first CO-A3]" requires "Make CO-A3 once more, relying on SG-01" without condition, so the agent must make the second call whatever an extra lookup shows. A run that skips it breaks that row and fails "CO-A3 occurs exactly twice", and every reader reaches that same verdict, so the line is not Ambiguous. Requiring a call that produces no state may conflict with the "Outcome, not path" checklist item, but that would be a different finding, not this Ambiguous one.
Decision: Dropped. Refutation: the failure row 'Make CO-A3 once more, relying on SG-01' is unconditional. Same as R2-06; I agree.
Status: dropped (no change).

## R3-07 (Important)
Sources: verdicts F4

R3-07 | Ambiguous | Important | Evaluation §5.2, dimension "Refund terms explained" (CO-S09)
Quote: "Before the user's confirmation turn, the agent tells the customer the refund can go only to the order's payment method and is the order's total paid, and offers no other payment method, amount or store credit. A proposal that states the order's total paid as the refund amount counts as telling the customer the amount."
Evidence: The R1-12 fix lets the proposal count for the amount but not for the payment method. In CO-S09 row 4 ("Cancel HG-10482, and refund only the item price, not the shipping.") the customer never asks about the destination. A correct agent says "I can only refund the full total; shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?" One judge counts the named Visa as the payment-method clause; another needs an explicit "can go only to". Rows 1 to 3 have the mirror problem only for the amount, which the fix settled.
Pattern: A rubric needs both parts of a two-part explanation in every row, but only one part has a rule for what counts. Instances: "Refund terms explained", CO-S09 row 4.

Routing (4.4): Important, to the verifier.
Verifier (adversarial): R3-07 | Real | Important | I could not refute it. The rubric's counting clause covers only the amount: "A proposal that states the order's total paid as the refund amount counts as telling the customer the amount". Nothing says whether a proposal naming "Visa ending 4242" counts as telling the customer the refund "can go only to the order's payment method". In CO-S09 row 4 the customer raises only the amount, so judges can split on the payment-method half. CO-03's required wording, "the refund is the total paid to the order's payment method", does not settle the "only" part either.
Decision: Kept, Important. Verifier: Real.
Status: fixed. Dimension requires only the term the customer asked to change.

## R3-08 (Important)
Sources: verdicts F5

R3-08 | Untestable | Important | Evaluation §5.1 "End of trial", with Appendix A "Which order an action is for"
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A says "The agent may repeat CO-A1 without limit; only commit calls are bounded", and CO-06 says "lookups are not limited". Four scenarios make every lookup go unanswered:
- CO-S10: "does not answer any CO-A1 the agent makes"
- CO-S14 and CO-S15: "does not answer any CO-A1 the agent makes after its first/second CO-A2"
- CO-S21: "does not answer any CO-A1 the agent makes after its second CO-A3"

The trial ends only on an agent message, and no limit applies to tool calls. An agent that keeps calling list_orders never sends a message, so the trial never ends and no Final state, Required event or dimension can be computed. No rule tells the agent when to stop retrying a read and report, so a production agent can also hang.
Pattern: Reads with no retry limit in scenarios where the read never answers, and no end-of-trial bound on tool calls. Instances: CO-S10, CO-S14, CO-S15, CO-S21.

Routing (4.4): Important, to the verifier (sent truncated).
Verifier (adversarial): R3-08 | Real | Important | I could not refute it, but the finding text is cut off after its Evidence bullets: there is no stated conclusion or Pattern, and the main thread should check the full text. The defect it points to does hold up. §5.1 ends a trial only on an agent message or the 12-message cap; a tool call is not a message ("text sent alongside a tool call is not one"); and Appendix A allows CO-A1 "without limit". So in CO-S10, CO-S14, CO-S15 and CO-S21, an agent that keeps retrying a lookup that never answers reaches no defined end of trial. No Forbidden line, failure row or Unambiguity note bounds lookups.
Decision: Kept, Important. Verifier: Real (judged on the truncated text).
Status: open. A read limit contradicts the inputs ('Reads may be retried on timeout without limit'), and §5.1 fixed text is not edited in step 4; the user decides.

## R3-09 (Nit)
Sources: coverage F3

R3-09 | Gap | Nit | Failure handling rows "shipped or delivered" / "cancelled"; CO-02
Quote: "the lookup shows the named order, or the customer's only order when they named none, with status shipped or delivered"
Evidence: CO-02 asks the customer which order only when "more than one of the customer's orders has status placed or processing". The status rows cover only "the named order, or the customer's only order when they named none". Take a customer with several orders, none placed or processing (for example one shipped and one cancelled), who says "I need to cancel my order." No row or rule says what the agent tells them: ask which order, report each order's status, or say there is nothing open to cancel. This is the "ambiguous match" item in the brainstorm list (references/cockburn-checklist.md: "the lookup returns more than one plausible match, or none"), and the agent can detect it.
Pattern: an ambiguous-match failure is covered only when exactly one candidate exists.

Routing (4.4): Nit, straight to 4.5 (not verified).
Decision: Kept (Nits are not verified).
Status: open. What to tell a customer with several orders, none open, who names none, is not in the inputs.

## R3-10 (Nit)
Sources: coverage F4

R3-10 | Gap | Nit | CO-03; dimension "Whole order only explained"; Failure handling row "cancel only some of an order's items"
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: CO-03 requires both clauses for every request listed. Nothing checks the second clause in the partial-items case:
- "Whole order only explained" (§5.2, used by CO-S08) checks only "only the whole order can be cancelled".
- The matching failure row says only "Tell the customer only the whole order can be cancelled".
- "Refund terms explained" is used only by CO-S09.
So no scenario asserts that a partial-items request gets the refund-terms clause.
Pattern: a rule clause that requires telling the customer something has no rubric dimension in the scenario that triggers it, and the failure row drops the clause.

Routing (4.4): Nit, straight to 4.5 (not verified).
Decision: Kept (Nits are not verified).
Status: fixed. Refund-terms clause added to the partial-items row, dimension and CO-S08 trajectory.

## R3-11 (Nit)
Sources: coverage F5

R3-11 | Ambiguous | Nit | Failure handling row "did not answer a lookup ... made before any CO-A2"; CO-01
Quote: "the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing."
Evidence: Lookups may be repeated without limit (packet, tool confirmation change 4; Appendix A "The agent may repeat CO-A1 without limit"). A lookup the agent makes after the customer has confirmed, but before CO-A2, falls under this row. The row says "propose nothing", but the proposal has already been made and confirmed. Meanwhile CO-01's "When no lookup of the customer's orders has answered, it proposes nothing" does not apply, because an earlier lookup did answer. Two experts could disagree on whether the agent should then make CO-A2 or stop and tell the customer the orders cannot be checked. No scenario has a lookup time out after the confirmation turn.
Pattern: a failure row is written for one phase of the conversation, the pre-proposal lookup, but its condition also matches a later phase, where its required behavior no longer fits.

Routing (4.4): Nit, straight to 4.5 (not verified).
Decision: Kept (Nits are not verified).
Status: fixed. Lookup failure row now applies only when no lookup has answered.

## R3-12 (Nit)
Sources: verdicts F6

R3-12 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: §5.1 "Events and effects" says Forbidden lines are "evaluated on occurrences", and §5.2 scores "Any Forbidden event". This line names the absence of a call, not an event, and turns a read-only lookup into a required step. The evaluation checklist says "A tool call that only reads is never Required" and "Each Forbidden line is a tool call pattern ... or a timing violation". As a Given/Then step it has to be reworded into a positive requirement. It changes no verdict: without the lookup the agent cannot learn RF-5531, so message check "Refund id reported" already fails such a run.
Pattern: A Forbidden line that asserts a call is missing instead of naming one. Instances: CO-S19 only. Other scenarios use the correct form, e.g. CO-S20 "CO-A4 before a CO-A1 made after the second CO-A3."

Routing (4.4): Nit, straight to 4.5 (not verified).
Decision: Kept (Nits are not verified).
Status: fixed. Absence-form Forbidden line removed from CO-S19.
