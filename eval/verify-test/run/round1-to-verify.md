# Round 1 findings to verify (Important)

15 findings.

## R1-01
Sources: faithfulness F1, verdicts F8

R1-01 | Lies | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-S17 row 3
Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |" and CO-S17 row 3: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |", with the Final state line "HG-10482 has status cancelled."
Evidence: Appendix A (agent-spec.md line 1525) defines this outcome as "the order is not cancelled: `OrderNotCancelled`". The input adds the outcome without saying how to handle it (review-packet.md line 82, "issue_refund adds outcome OrderNotCancelled"). The spec's world in CO-S17 row 3 cannot exist: the order is cancelled, yet the tool reports it not cancelled. That contradicts the spec's own tool definition. The required behavior then has the agent tell the customer "the order is cancelled" right after the order system said it is not. G-03 (line 24) allows saying "cancelled" only when the order system returned it cancelled or a lookup shows it, and the latest answer here says the opposite. The "Refund not issued reported" rubric (line 1505) then requires that claim in row 3. No input says OrderNotCancelled means "cancelled, refund not issued". The input's matching case for an uncertain cancellation is to re-read and hand off as `cancellation_unknown` (review-packet.md line 64).
Pattern: a tool outcome is merged into a failure row whose required message and Final state contradict what the outcome means. Every instance: the CO-A3 failure row at line 103, CO-S17 row 3 Initial state and Final state, and the "Refund not issued reported" dimension as it applies to CO-S17 row 3.

## R1-02
Sources: faithfulness F2, coverage F4

R1-02 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: Interview round 3 Q4, confirmed "Yes to all" (review-packet.md line 64): "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." This covers every cancel timeout, not only the first. The spec row drops the re-read after the second timeout and bans CO-A3 even if a lookup would show the order cancelled. It also says the outcome is "not known" without the agent trying to learn it. CO-07 (line 80) calls for a handoff only "when the agent cannot tell whether the order was cancelled", and a lookup could tell. CO-S15 hides the conflict: its Initial state (line 892) makes every CO-A1 after the second CO-A2 unanswered, so no scenario shows the case where the lookup does answer.
Pattern: a failure row skips the read-then-branch handling the input requires for that kind of timeout. Instance: line 101, with the masking Initial state line in CO-S15.

## R1-03
Sources: faithfulness F3

R1-03 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3", failed-or-no-refund branch; CO-S20
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Interview round 3 Q3, confirmed (review-packet.md line 63): "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet." The spec replaces the confirmed statement ("not confirmed yet") with a different, stronger one ("has not been issued"). CO-S20 enforces it through the "Refund not issued reported" rubric (lines 1223 and 1505). An agent that follows the confirmed policy word for word may fail CO-S20.
Pattern: the spec rewrites a customer-facing statement the user confirmed into a different claim, and a rubric dimension enforces the rewritten claim. Instances: the failure row at line 105 and CO-S20 (Unambiguity note and dimension use).

## R1-04
Sources: coverage F1

R1-04 | Gap | Important | CO Scope & Authority "must not", Contract, all success scenarios
Quote: "promise a date by which the refunded money arrives."
Evidence: Interview round 3 Q1 (review-packet.md line 61), confirmed "Yes to all": "The agent promises nothing about when the money arrives." Round 2 Q2 (line 37) puts a figure on the table ("money arrives in 5 to 10 business days"), so an agent is likely to repeat it. In the spec this prohibition appears only in the Scope "must not" list (agent-spec.md line 49). No rule in CO-01..CO-08 or G-01..G-04 states it. No rubric dimension in §5.2 (lines 1495-1509) checks it. The only check on the agent's words in CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13 and CO-S16 is the message check "Refund id reported" (e.g. CO-S01 Unambiguity note, line 170). So an agent that says "your money will be back in 3 days" passes every scenario.
Pattern: a domain prohibition from the inputs that lives only in Scope, with no Contract rule and no scenario or rubric dimension asserting it.

## R1-05
Sources: coverage F2

R1-05 | Gap | Important | Stakeholders (primary actor) vs CO-08 and success scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
Quote: "wants to be told truthfully whether the order was cancelled and where the refund stands." / CO-08: "...and the agent tells the customer the refund id."
Evidence: On the success path, CO-08 (line 83) requires only that the refund id is told. No rule requires the agent to say the order was cancelled or that the refund is pending or issued. G-03 (line 24) only restricts when those things may be said. The success scenarios check the agent's words only with "Refund id reported" (CO-S01 Unambiguity note, line 170; §5.2 line 1497). So a final message such as "RF-5531: sorry, we could not cancel your order" passes CO-S01. CO-S19 does have a status dimension ("Refund status reported", line 1507), but that applies only to the lookup branch. Input: the user's known case 3 (packet line 54): "Final message must match the final refund status."
Pattern: a stakeholder interest in being told the outcome that only a restrictive rule covers. No rule requires the report on the success exit, and no rubric dimension asserts it in the success scenarios.

## R1-06
Sources: coverage F3

R1-06 | Gap | Important | Failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" (G-02, CO-04)
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: G-02 (line 21): "Any change to a proposal term after confirmation voids that confirmation." Input round 1 Q4 (packet line 30): "any change after confirmation voids it." The only scenario that changes a proposal is CO-S03. Its Turn 2 is scripted "in place of a confirmation" (line 248), and none of its rows contains an agreement (lines 275-277). No scenario has a confirming turn that also carries a change (e.g. "Yes, go ahead, but make it HG-10511" or "Yes, but refund to my Mastercard"). That is the case where an agent most plausibly acts on the "yes".
Pattern: a failure row whose condition joins several cases with "or", where scenarios trigger only the easiest case and the case that changes the verdict is never tested.

## R1-07
Sources: coverage F5

R1-07 | Gap | Important | Failure row "CO-A3 | ... payment provider temporarily unavailable for the second CO-A3"; CO-S18
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
Evidence: Input round 3 Q3 (packet line 63): "For case 3 [refund timed out], after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off..." Known case 3 (line 54): "agent retries once, then re-reads the order and refund records and reports what it finds." The row's condition covers any first outcome, including a first CO-A3 that timed out and may have created the refund (Appendix A, line 1525: "A timeout creates the refund or not as Initial state says"). Even then the row tells the customer "the refund has not been issued" without a lookup. CO-S18 covers only two ProviderUnavailable results (line 1064). No scenario has a first timeout followed by a second ProviderUnavailable.
Pattern: a retry-exhausted failure row that merges first-call histories with different knowledge (known no-effect vs unknown effect), so the re-read the inputs require after an unknown result is skipped and no scenario tests it.

## R1-08
Sources: verdicts F1

R1-08 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: The line never says which of the two calls creates the refund, so the result of a CO-A1 made between them is left open. Lookups between the calls are allowed: Appendix A says "The agent may repeat CO-A1 without limit", and the packet's tool confirmation turn says "Reads may be retried on timeout without limit". In CO-S21, only "any CO-A1 the agent makes after its second CO-A3" goes unanswered, so a lookup between the calls is answered. If the harness creates RF-5531 on the first call, that lookup shows the refund as pending (row 1) or failed (row 2). The agent then knows the status, and the required "CO-A4 ... reason refund status unknown" and the rubric "the refund's status is unknown" no longer describe the truthful behaviour that G-03 requires. If the harness creates it on the second call, the lookup shows no refund and the reference path holds. The same choice decides CO-S19, where an agent that sees "pending" after the first call and reports it fails "CO-A3 occurs exactly twice". It also decides CO-S20 row 1 ("together they create refund RF-5531 ... with status failed"). CO-S16 avoids the problem by tying the effect to one call ("The agent's first CO-A3 ... creates refund RF-5531").
Pattern: A world change caused by an unanswered commit call has to be tied to the nth call, never to "together", so that any lookup in between has a defined result.

## R1-09
Sources: verdicts F2

R1-09 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: Row 2 is "gets no answer from the order system and cancels nothing". The spec never defines whether a timed-out call "reaches the order system". If it does not, HG-10482 is still processing when the agent looks up after the timeout. Then the failure row (spec line 100, "If it shows the order placed or processing, make CO-A2 once more") requires a second CO-A2, which CO-S11's Forbidden line "A second CO-A2" fails. The outcome of that second call is also left open. The evaluation checklist says a mid-trial change should be tied "to the agent's nth state-changing call".
Pattern: Tie a mid-trial state change to the issuing of the nth commit call ("at the agent's first CO-A2"), not to a delivery event that a timeout leaves undecided.

## R1-10
Sources: verdicts F3

R1-10 | Ambiguous | Important | CO-S03, CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: The evaluation checklist says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." §5.1 defines only "the confirmation question", which must equal the values of a confirmation-form pair in scope. In CO-S03 the only such pair is for HG-10511, so the HG-10482 question is not a defined event. In CO-S04 there are no User-knows pairs, so no confirmation question exists at all. It is therefore a judgment call whether "Do you want me to cancel HG-10482?" (no amount, no payment method) or "Just to check, HG-10482, right?" sets off Turn 2. In CO-S03, if the simulator does not fire Turn 2, it deflects the question, the agent never learns about HG-10511, and the required CO-A2 for HG-10511 fails.
Pattern: Anchor a scripted reply on an event §5.1 defines. For example, define the confirmation question for the first proposal through a confirmation-form pair that is in scope only before Turn 2, or define the "proposal question" in §5.1.

## R1-11
Sources: verdicts F4

R1-11 | Ambiguous | Important | §5.2 dimension "Shipped order explained", used by CO-S05
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process"
Evidence: In CO-S05 no cancellation is attempted. CO-01 and the failure row (spec line 92) tell the agent to say "the order has shipped and cannot be cancelled", and CO-S05's own Unambiguity note says the dimension "checks the agent said the order has shipped and cannot be cancelled". The shared definition asks for "was not cancelled", which is the CO-S11 wording (failure row at line 98). A judge could fail a CO-S05 agent that follows CO-01 exactly ("it has shipped and can't be cancelled") for never saying it "was not cancelled", or could accept it. The evaluation checklist says "A shared rubric dimension has one definition ... must hold in every one of them as their failure rows and reference trajectories describe the behavior."
Pattern: A dimension shared by a refusal before any attempt and a rejection after an attempt needs one wording that both satisfy, or two separate dimensions.

## R1-12
Sources: verdicts F5

R1-12 | Ambiguous | Important | §5.2 dimension "Refund terms explained", used by CO-S09
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: In rows 1 and 3 the customer asks only for a different destination, not a different amount. The reference trajectory, step 3, says only "the refund can only go to the order's payment method", then states the proposal with "$86.40". It is a judgment call whether stating $86.40 in the proposal counts as telling the customer "the refund is the order's total paid". A strict judge fails the reference trajectory itself; a lenient one passes an agent that never explains the amount rule.
Pattern: A rubric clause must say whether stating the value inside the proposal satisfies it, or the clause must apply only to rows where the customer raised that term.

## R1-13
Sources: verdicts F6

R1-13 | Ambiguous | Important | CO-01, CO-02, CO-03, CO-03 failure row; CO-S08; dimension "Orders unavailable reported"
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence: "Propose" and "proposal" are used throughout ("proposes nothing", "proposes nothing for it", "proposes no cancellation") but never defined. CO-S08's reference trajectory, step 3, has the agent ask "whether they want to cancel the whole order", and its User-knows pair is "Would you like to cancel the whole order HG-10530 instead?". Under the failure row, that question is a proposal made before the customer asked, unless a proposal means only a full confirmation question. In the same way, the rubric "Orders unavailable reported" (CO-S10) needs "proposes no cancellation". Two judges can disagree on whether "I can't check right now; want me to try cancelling HG-10482 anyway?" is a proposal. The same applies in CO-S07 to "Did you mean HG-10482?" under CO-02's "proposes nothing for it".
Pattern: Define "proposal" in §5.1 (for example, as a confirmation question or any offer to cancel a named order), and make the rules and the reference trajectories agree with that definition.

## R1-14
Sources: verdicts F7

R1-14 | Ambiguous | Important | G-04 against CO-06 and CO-S13
Quote: "the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 says "cancelling an order that is already cancelled returns it cancelled and changes nothing". That is a guarantee that repeating CO-A2 "creates nothing new", so under G-04's second clause a blind resend of the cancellation is allowed. CO-06 ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing") and CO-S13's Forbidden line "A second CO-A2 before a CO-A1 made after the first CO-A2" ban it. The packet, round 3 Q4, says "If the cancel call times out: no blind resend; re-read the order." An agent built from G-04 retries blindly and fails CO-S13.
Pattern: When a global rule leaves an open clause ("when the order system guarantees..."), list exactly which guarantees and actions it covers, so it cannot permit what a capability rule forbids.

## R1-15
Sources: verdicts F9

R1-15 | Ambiguous | Important | CO-07; dimension "Staff contact unconfirmed reported" (CO-S23)
Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
Evidence: "Once" can mean timing (say it only after the task exists) or describe the future (staff will follow up when the task is created). §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call", and the CO-S23 dimension requires that the agent "never says ... that staff will follow up". In CO-S23, an agent that writes "I'm passing this to store staff so they can follow up" alongside its first CO-A4, before both calls time out, passes under one reading of CO-07 and fails under the other.
Pattern: State the timing of a required statement explicitly ("only after a CO-A4 has returned a task id"), and make each rubric's "never says" clause say whether text sent before or alongside the commit call counts.
