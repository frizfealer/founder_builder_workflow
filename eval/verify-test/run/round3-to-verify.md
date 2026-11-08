# Round 3 findings to verify (Important)

8 findings.

## R3-01
Sources: faithfulness F1

R3-01 | Lies | Important | CO-08, Contract; dimension "Refund id reported" (§5.2)
Quote: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id."
Evidence: Nothing in the inputs asks the agent to tell the customer the refund id. In review-packet.md, the refund id appears only as a data-model field (Round 2 Q3: "Refund: refund id (e.g. RF-5531), order number, amount, payment method, status") and as the idempotency key of issue_refund (Round 2 user answer, Q3: "repeated calls return the same refund id"). On what the agent must tell the customer, the inputs say only this: report the status (Round 3 Q3: "pending or issued, report that status"); the final message must match the final refund status (Round 2 Q4, known case 3: "Final message must match the final refund status"); promise nothing about arrival (Round 3 Q1). So the duty to tell the refund id is a requirement the spec added. It is enforced as a pass/fail code grader: the dimension "Refund id reported" ("An agent message in the message-check window (§5.1) contains the refund id ...") is used by CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 and CO-S25. Under "Scenario pass" (§5.2), every dimension a scenario uses must pass. An agent that does exactly what the inputs require ("Your order HG-10482 is cancelled and your $86.40 refund to Visa ending 4242 is pending") fails all nine scenarios. Related instances that carry the same added requirement: the failure row "CO-A3 | the order system did not answer the second CO-A3" ("tell the customer that status and the refund id"); the Unambiguity notes of the nine scenarios ("message check 'Refund id reported' matches ..."); and each of those scenarios' Reference trajectory final step, which names the refund id.
Pattern: A success guarantee or required message adds a disclosure obligation (here, the refund id) that no input states, and a code grader then enforces it. Either trace it to an input (ask the user) or remove it from CO-08, the failure row and the dimension list.

## R3-02
Sources: coverage F1

R3-02 | Gap | Important | CO-01 / CO-07, Failure handling row "status cancelled", CO-S06 Initial state
Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence: The Trigger is "The customer asks to cancel an order or to get their money back for an order" (spec §4.1 Preconditions and Trigger). The spec itself ends some trials with an order that is cancelled but whose refund is failed, with no follow-up task: in CO-S23, the handoff goes unanswered twice and the customer is told to contact support. Two lines then give different answers when that customer comes back:
- CO-07 says "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4". A cancelled order whose refund is failed, or that has no refund, meets that condition.
- The failure row "the lookup shows the named order ... with status cancelled" says "Tell the customer the order is already cancelled; propose nothing for it". The packet's shared-understanding summary says the same: "An already cancelled order: the agent reports that and changes nothing."
CO-S06 uses only an already-cancelled order whose refund is issued, so no scenario decides between CO-A4, a fresh CO-A3 (which CO-05 allows, since the order is cancelled) and doing nothing.
Pattern: a state-dependent rule is tested only at its easy value (refund issued). The value where two rules give different answers (cancelled, refund failed or absent) has no scenario and no failure row.

## R3-03
Sources: coverage F2

R3-03 | Gap | Important | Failure handling rows "the order system did not answer the first CO-A2" and "... the second CO-A2"
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
Evidence: The use-case checklist (references/cockburn-checklist.md, Failure handling) says: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer. A missing branch is the else-branch a coder will invent." Both CO-A2-timeout rows have branches for cancelled, open, shipped/delivered and no answer, but none for a lookup that answers without the order in it. The spec treats that case as possible: cancel_order has outcome OrderNotFound (Appendix A CO-A2 row), and CO-S24 has the order system report not-found for an order that the earlier lookup listed. The same gap is in both rows: the first-CO-A2 timeout row and the second-CO-A2 timeout row.
Pattern: a lookup-branching failure row has no "nothing found" branch.

## R3-04
Sources: verdicts F1

R3-04 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: In row 2 the first CO-A2 "gets no answer from the order system and cancels nothing". The line does not say whether a call that timed out "reached the order system". If it did not, the status stays processing. The lookup the failure row requires ("the order system did not answer the first CO-A2": "If it shows the order placed or processing, make CO-A2 once more") then shows processing, so a correct agent sends a second CO-A2 and hits Forbidden "A second CO-A2." and fails the Final state "HG-10482 has status shipped". CO-S26 ties its status change to a defined event instead: "until the agent issues its second CO-A2". The evaluation checklist says "tie the change to the agent's nth state-changing call". §5.1 "When an action occurs" defines occurrence as issuing the commit call, so "issues" is a defined event and "reaches" is not.
Pattern: A mid-trial world change tied to an undefined moment ("reaches") instead of the call being issued. Instances: CO-S11 only.

## R3-05
Sources: verdicts F2

R3-05 | Ambiguous | Important | G-04 against CO-06 and Appendix B SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 says "cancelling an order that is already cancelled returns it cancelled and changes nothing". That is a guarantee that repeating CO-A2 creates nothing new, so under G-04 an agent may resend an unanswered cancel without a lookup. The CO-A4 retry is justified the same generic way ("relying on SG-03"), so the parenthetical does not limit G-04 to SG-01. CO-06 forbids exactly that ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing"), and so does the input (packet round 3 Q4: "no blind resend; re-read the order"). An agent built to G-04 fails CO-S12 ("A second CO-A2."), and CO-S13, CO-S25, CO-S26 and CO-S27 ("A second CO-A2 before a CO-A1 made after the first CO-A2."). Two experts reading G-04 reach opposite verdicts on a blind cancel retry.
Pattern: A global rule's exception clause covers more guarantees than the capability rule allows. Instances: G-04 with SG-04 (CO-A2).

## R3-06
Sources: verdicts F3

R3-06 | Ambiguous | Important | CO-S16, Required events (Data variants row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". A valid variation the brief asks to pass: after the unanswered call the agent makes an extra CO-A1, which Appendix A allows "without limit", and sees RF-5531 pending. It then reports success without a second call. That run obeys G-03, and G-04 does not require a repeat. CO-06 only permits one ("It makes a second CO-A3 only after..."). The evaluation checklist says "Outcome, not path". The run still fails the Required event, because the failure row says "Make CO-A3 once more, relying on SG-01" with no branch for a lookup that already shows the refund. Whether a refund call made after the refund is already visible is required or forbidden is decided by no rule. Experts will split.
Pattern: A required call count after an unknown result, where an allowed extra read can show the outcome already reached, and no rule says what to do then. Instances: CO-S16 row 2.

## R3-07
Sources: verdicts F4

R3-07 | Ambiguous | Important | Evaluation §5.2, dimension "Refund terms explained" (CO-S09)
Quote: "Before the user's confirmation turn, the agent tells the customer the refund can go only to the order's payment method and is the order's total paid, and offers no other payment method, amount or store credit. A proposal that states the order's total paid as the refund amount counts as telling the customer the amount."
Evidence: The R1-12 fix lets the proposal count for the amount but not for the payment method. In CO-S09 row 4 ("Cancel HG-10482, and refund only the item price, not the shipping.") the customer never asks about the destination. A correct agent says "I can only refund the full total; shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?" One judge counts the named Visa as the payment-method clause; another needs an explicit "can go only to". Rows 1 to 3 have the mirror problem only for the amount, which the fix settled.
Pattern: A rubric needs both parts of a two-part explanation in every row, but only one part has a rule for what counts. Instances: "Refund terms explained", CO-S09 row 4.

## R3-08
Sources: verdicts F5

R3-08 | Untestable | Important | Evaluation §5.1 "End of trial", with Appendix A "Which order an action is for"
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A says "The agent may repeat CO-A1 without limit; only commit calls are bounded", and CO-06 says "lookups are not limited". Four scenarios make every lookup go unanswered:
- CO-S10: "does not answer any CO-A1 the agent makes"
- CO-S14 and CO-S15: "does not answer any CO-A1 the agent makes after its first/second CO-A2"
- CO-S21: "does not answer any CO-A1 the agent makes after its second CO-A3"

The trial ends only on an agent message, and no limit applies to tool calls. An agent that keeps calling list_orders never sends a message, so the trial never ends and no Final state, Required event or dimension can be computed. No rule tells the agent when to stop retrying a read and report, so a production agent can also hang.
Pattern: Reads with no retry limit in scenarios where the read never answers, and no end-of-trial bound on tool calls. Instances: CO-S10, CO-S14, CO-S15, CO-S21.
