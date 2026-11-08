# Round 2 merged findings

13 findings: 8 Important, 5 Nit.

## R2-01
Sources: faithfulness F1, verdicts F2

R2-01 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (used by CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows the two scenarios exercise ask for only two statements. agent-spec.md, CO-A2 row "did not answer the first CO-A2": "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown". The CO-A2 row "did not answer the second CO-A2" has the same wording. The input says the same: review-packet.md Round 3 Q4, "Re-read fails, say outcome unknown, issue no refund, hand off". There, "issue no refund" is an action, not something the agent must say. No rule, failure row or input asks the agent to tell the customer "no refund was issued". The dimension adds that requirement, and so do the reference trajectories (CO-S14 step 8, CO-S15 step 10). An agent that follows the failure row exactly fails the dimension, so it fails CO-S14 and CO-S15.
Pattern: A rubric dimension requires a statement that no rule or failure row requires. Either the dimension must match the failure row's required behavior, or the row (and rule) must add the statement.

## R2-02
Sources: coverage F1

R2-02 | Gap | Important | CO-09, scenarios on the failure paths (rubric dimensions in §5.2)
Quote: "The agent states no date or time span by which the refunded money arrives."
Evidence: CO-09 is tagged [minimal guarantee], so it has to hold on every exit. Round 3 Q1 of the packet says "The agent promises nothing about when the money arrives," and round 2 Q2 had first proposed "money arrives in 5 to 10 business days." Only one dimension asserts CO-09: "Cancellation and refund reported". It is used only by the success scenarios CO-S01, S02, S03, S09, S12, S13, S16, S19 and S25. The dimensions on the paths where the refund is unfinished and staff take over never check for a date: "Refund not issued reported" (CO-S17, S18, S22), "Refund not confirmed reported" (CO-S20), "Refund status unknown reported" (CO-S21), "Staff contact unconfirmed reported" (CO-S23) and "Cancellation outcome unknown reported" (CO-S14, S15). Those are exactly the exits where an agent is likely to reassure the customer with something like "staff will get your refund to you within 5 to 10 business days", and that agent passes all of them. Also, no scenario has the customer ask when the money will arrive, which is the most direct prompt to break CO-09.
Pattern: A minimal-guarantee rule is asserted only on success exits. Every scenario whose exit the rule covers should have a dimension that checks it, here the "states no date or time span" clause, on the failure-path dimensions too.

## R2-03
Sources: coverage F2

R2-03 | Gap | Important | G-01 / CO-02, Failure handling
Quote: "absent" (no failure row or scenario for a customer who asks to cancel more than one order; G-01 reads "The agent cancels, refunds and hands off at most the one order the current request is about.")
Evidence: The use-case checklist's failure brainstorm (cockburn-checklist.md, "Failure handling") includes "the lookup returns more than one plausible match", and Q4 case 1 in the packet makes customers with two open orders a known situation (CO-S02). A customer with two open orders can say "cancel both of my orders." G-01 allows at most one order, and CO-02 ("Every proposal names one order number") lets the agent propose one at a time. But no rule, failure row or scenario says what the agent tells the customer or does with the second order: refuse it, handle it in a second proposal, or something else. Nothing in the packet says one order per conversation; that limit is the spec's own. CO-06 counts calls "in a conversation" and does not settle it. In production, an agent might cancel both orders (breaking G-01) or quietly drop one, and no scenario would catch either.
Pattern: A user request that a global rule forbids, and that the agent can detect, has no failure row giving the required behavior and no holding-back scenario.

## R2-04
Sources: verdicts F1

R2-04 | Ambiguous | Important | CO-07; CO-S22, CO-S23, dimension "Staff contact unconfirmed reported"
Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
Evidence: The sentence can be read two ways. (a) "once the order system has created the task" says when the agent may tell the customer: only after a CO-A4 returns task_id. (b) It is part of what the agent tells the customer ("staff will follow up once the task is created"), so it can be said before or alongside the call. §5.2 Graders: "A rubric judge reads every text the agent sends, including text sent alongside a tool call." In CO-S23 the dimension "Staff contact unconfirmed reported" requires the agent "never says ... that staff will follow up". Take an agent that sends "I'm passing this to our store staff, who will follow up" alongside the first request_staff_followup call, then reports the double timeout as the failure row says (line 113). Reading (a) fails it; reading (b) passes it. CO-S22 (Reference step 7: first CO-A4 gets no answer) has the same timing question for "Refund not issued reported", which requires "store staff will follow up" but never says when it may be said.
Pattern: a rule that ties a message to a call's result must say whether the condition limits when the message may be sent or is part of what it says. A dimension that reads text sent alongside tool calls must say whether text sent before the result counts.

## R2-05
Sources: verdicts F3

R2-05 | Ambiguous | Important | dimension "Refund not confirmed reported" (CO-S20 row 1)
Quote: "The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued."
Evidence: In CO-S20 row 1 the lookup shows "refund RF-5531 failed" (Reference step 8). An agent that truthfully says "the refund failed" or "the refund has not been issued" uses the same words the spec requires for the same refund status elsewhere: the failure row "returned the refund with status failed" (line 109) and dimension "Refund not issued reported" (CO-S17). Whether "failed" or "not issued" counts as "not confirmed yet" depends on the wording, and judges can differ. This is the R1-03 fix, and it ties the verdict to one phrase.
Pattern: a rubric that requires a particular phrase where other phrasings say the same thing truthfully. List the forms that count, as "Shipped order explained" does, or define the fact the message must convey.

## R2-06
Sources: verdicts F4

R2-06 | Ambiguous | Important | CO-S16 row 2; failure row "did not answer it" (first CO-A3)
Quote: "- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Row 2: "gets no answer from the order system, and creates refund RF-5531 with status pending". Lookups are unlimited (Appendix A: "The agent may repeat CO-A1 without limit"), and CO-A1 returns each order's refund. Take this valid variation: after the timeout the agent calls list_orders, sees RF-5531 pending, and reports it, which G-03 allows ("or a lookup shows it"). It makes one CO-A3 and fails the Required event. The failure row (line 108) says only "Make CO-A3 once more, relying on SG-01". It does not say what to do when a lookup in between already shows the refund. G-04 permits the retry but does not require it. Experts can differ on whether this run is right.
Pattern: a failure row that requires a retry without saying what to do when an allowed lookup has already resolved the outcome. Either allow "or a lookup shows the refund pending or issued" in the failure row and loosen the count to "once or twice", or forbid a lookup in between.

## R2-07
Sources: verdicts F5

R2-07 | Ambiguous | Important | failure rows "did not answer a lookup ... before any CO-A2" (line 95), "did not answer the first/second CO-A2" (lines 106, 107), "did not answer the second CO-A3" (line 111); CO-S10, CO-S14, CO-S15, CO-S21; §5.1 End of trial
Quote: "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: Appendix A says "The agent may repeat CO-A1 without limit". The review packet's tool confirmation turn, change 4, says "Reads may be retried on timeout without limit". "The lookup does not answer" never says whether one unanswered list_orders is enough to go on to the handoff or report, or whether the agent should retry first, and how many times. In CO-S10, S14, S15 and S21 every lookup after the trigger times out. §5.1 ends a trial only at an agent message ("the first agent message that asks the user nothing ... or at the agent's 12th message"). Tool calls are not capped. An agent that keeps calling list_orders without yielding has no defined trial end and no verdict. One that hands off after 1 timeout and one that hands off after 20 timeouts both pass, with nothing to say whether either is wrong.
Pattern: unbounded read retries combined with a condition "the lookup does not answer" and a message-only trial cap. Say how many unanswered lookups count as "does not answer", or cap tool calls per trial.

## R2-08
Sources: verdicts F6

R2-08 | Ambiguous | Important | Required events "CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn." in CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23
Quote: "- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn."
Evidence: The line has two readings: (a) exactly one CO-A2 in the trial, and it comes after the confirmation turn; (b) exactly one CO-A2 among those after the confirmation turn. Neither §5.1 nor §5.2 fixes which. Wrong run: the agent calls cancel_order at Turn 1, then asks the confirmation question, gets "Yes", and calls cancel_order again, which returns cancelled under SG-04 (Appendix A CO-A2 row). Reading (a) fails it; reading (b) passes it. None of the listed scenarios has "CO-A2 before the user's confirmation turn." or "A second CO-A2." in Forbidden; only CO-S16 (line 983) and the CO-A2 retry scenarios have them. So the cancellation before authorization is caught only under reading (a).
Pattern: "exactly N, after X" whose count scope (the whole trial vs. the window after X) is undefined. Define the count scope in §5.1, or add "CO-A2 before the user's confirmation turn." to Forbidden in every confirm scenario.

## R2-09
Sources: faithfulness F2

R2-09 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A, CO-A3 row: `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}`, and "refund failed: returns the refund with `status: \"failed\"`". After the R1-16 fix the result carries no failure reason (answered.md R1-16: "removed `failure_reason` and its values"). The trajectories still show a reason in the tool result, which the tool cannot return. Instances: CO-S17 step 6, CO-S22 step 6, CO-S23 step 6. The R1-16 fix is incomplete.
Pattern: A reference trajectory shows a tool-result field that is not in the Appendix A return shape. Trajectory results should contain only fields the tool returns. The cause can stay in Initial state as world state.

## R2-10
Sources: faithfulness F3

R2-10 | Lies | Nit | CO-S06 Illustrates
Quote: "**Illustrates** CO-01, CO-05"
Evidence: CO-05 says "CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled". In CO-S06 the lookup shows the order cancelled (Initial state "with status cancelled"; Reference step 2 "HG-10399 cancelled"). So CO-05 allows CO-A3 here and does not explain the Forbidden line "CO-A3 at any point." That line is covered by CO-04 (CO-A3 runs only under the confirmation that authorized CO-A2, and no confirmation exists) and CO-01 (no proposal). The scenario claims to illustrate a rule it does not exercise and leaves out the rule that does.
Pattern: An Illustrates line names a rule that the scenario's Forbidden or Expected lines do not depend on. Each Illustrates entry should be a rule the scenario's verdict turns on.

## R2-11
Sources: faithfulness F4

R2-11 | Lies | Nit | CO-A3 failure rows (known case 3) / CO-S16 rows 2–3
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. | CO-06, G-04 |"
Evidence: review-packet.md Round 2 Q4, known case 3: "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds." Round 3 Q3: "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet". The spec requires the re-read only when the retry also times out (row "did not answer the second CO-A3"). When the first CO-A3 timed out and the retry answers, the spec does not re-read and branches on the retry's result. If the retry returns status failed, the spec says "the refund has not been issued" (row "returned the refund with status failed"). The input says that case is the "not confirmed yet" report. No scenario forbids the extra lookup, so no verdict changes, but the production behavior differs from the input.
Pattern: The spec narrows an input's unconditional follow-up step (here, re-read after the retry) to one sub-case. Either apply the step whenever the input's trigger (a first-call timeout) occurred, or record the narrowing as an open question for the user.

## R2-12
Sources: coverage F3

R2-12 | Gap | Nit | CO-01 / CO-02, Failure handling
Quote: "absent" (no row for "the lookup shows no order with status placed or processing and the customer named no order number")
Evidence: The checklist brainstorm lists the case where the lookup returns none (cockburn-checklist.md, "ambiguous match ... or none"), and says a failure row that branches on a lookup must cover "nothing found" too. The rows only cover a named number that is not on the account (CO-02, CO-S07) and a named order that is shipped, delivered or cancelled (CO-01). A customer who says "I need to cancel my order" with no orders at all, or with no open ones, gets nothing on what the agent should say. CO-01 still makes sure nothing is proposed, so no verdict changes, but what the agent tells the customer is left for the builder to invent.
Pattern: A lookup branch (empty result, or no open match when no number was given) has no failure row.

## R2-13
Sources: verdicts F7

R2-13 | Ambiguous | Nit | CO-03 failure row (line 100); CO-S08 Reference trajectory step 3
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence: CO-S08 Reference step 3: "Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order." CO-S08 also has the User-knows question "Would you like to cancel the whole order HG-10530 instead?". The spec never defines "propose". CO-04 implies a proposal names the order number, refund amount and payment method. Whether offering to cancel the whole order is a "proposal" the row forbids is left open. If the agent's offer also states $53.50 to Amex ending 1007, it has the form of a confirmation question. No CO-S08 check grades this, so no verdict changes.
Pattern: an undefined term ("propose", "proposal") on which a failure row's Required behavior and its reference trajectory disagree. Define "proposal" (for example, a message stating order number, amount and payment method and asking to go ahead) in the Contract or §5.1.
