# Round 2 findings (merged, verbatim, with verifier verdicts and decisions)

9 merged findings: 9 Important, 0 Nit.


## R2-01 | Lies | Important
Merged from: faithfulness F1, coverage F3, verdicts F1

### faithfulness F1

F1 | Lies | Important | CO-S16, Initial state and Reference trajectory (also the Appendix A CO-A2 outcome cell and the failure row "store reports the order is not cancelled")
Quote: "The store answers the first CO-A2 for HG-10482 that the order is not cancelled, and creates no refund." / RT step 6: "Agent → CO-A2 (HG-10482) → refused: the order is not cancelled." / Final state: "Order HG-10482 has status cancelled."
Evidence: Earlier in the same Initial state: "The order system cancels the order and reports it cancelled on the first CO-A1 for HG-10482." The Final state says the order is cancelled. Appendix A ties the outcome to a world condition: "order not cancelled: `OrderNotCancelled`, no refund created". At the moment of CO-A2, that condition is false in this scenario's own world. The only input for this outcome is review-packet.md Q13 change 2, "issue_refund adds outcome OrderNotCancelled", which means the order is not cancelled. No input says the store can return it for an order that is cancelled. Also, CO-05 allows CO-A2 only "after the order system has shown the order cancelled", so this outcome can only reach a correct agent if the store and the order system disagree, and the inputs never describe that. The contradiction also leaves the verdict open: "Outcome reported truthfully" requires the final message to state "whether the order is cancelled ... as the agent's tool results in the trial showed them", and here the two results disagree. RT step 8 avoids the question by not mentioning the cancellation at all. This is the R1-03 fix (new CO-S16) and it is wrong.
Pattern: a scenario injects a tool outcome whose Appendix A condition is false given its Initial state and the results of earlier calls, so the Reference trajectory's tool results cannot match its own Final state.

### coverage F3

F3 | Ambiguous | Important | CO-S16 Initial state / Final state; "Outcome reported truthfully"
Quote: "The store answers the first CO-A2 for HG-10482 that the order is not cancelled, and creates no refund." (line 979), together with "Order HG-10482 has status cancelled." (line 996)
Evidence: Appendix A line 1145 defines `OrderNotCancelled` as the outcome when the "order not cancelled", but in CO-S16 the same order was just reported cancelled by CO-A1 (line 978) and stays cancelled in Final state. The agent's tool results therefore conflict. G-03 (line 24) requires the final message to state the cancellation "as the last results the agent received showed them", and the last result says not cancelled. The rubric "Outcome reported truthfully" (line 1126) requires the final message to state "whether the order is cancelled ... as the agent's tool results in the trial showed them", and those results show both. The failure row (line 106) and the reference trajectory step 8 (line 1020) say only "the refund was not issued", with no cancellation status. One judge could pass "your order is cancelled, refund not issued" and another could fail it (and the reverse for "not cancelled"). This is the R1-03 fix (new CO-S16), so I am reporting it as a defect in that fix.
Pattern: an injected supporting-actor outcome that contradicts an earlier result in the same scenario, so a rule that says "report what the results showed" gets no single reading.

### verdicts F1

F1 | Ambiguous | Important | CO-S16, Initial state and "Outcome reported truthfully" (§5.2)
Quote: "The store answers the first CO-A2 for HG-10482 that the order is not cancelled, and creates no refund."
Evidence: The line just above it in CO-S16 Initial state (spec line 978) reads "The order system cancels the order and reports it cancelled on the first CO-A1 for HG-10482." So the agent's own tool results disagree with each other about the order. The dimension (spec line 1126) passes only when the final message "states whether the order is cancelled ... as the agent's tool results in the trial showed them". In this trial, "cancelled" matches one result and "not cancelled" matches the other, so two judges can grade the same message differently. The reference trajectory step 8 ("Agent tells the customer the refund was not issued and the store's team will complete it") gives no cancellation status at all, which a strict judge would fail on the "states whether the order is cancelled" clause. Failure row line 106 also gives no cancellation status. This scenario was added as the fix for R1-03 (answered.md), so that fix is incomplete.
Pattern: When the scripted tool results contradict each other, a rubric dimension that grades "as the tool results showed them" has no single correct answer. The scenario has to state which result the report must follow, or the dimension needs a clause for this case.

**Verifier:** R2-01 | Real | Important | I could not refute it. CO-S16's Initial state has CO-A1 cancel the order and report it cancelled (spec line 978). Appendix A's CO-A1 effect says it "Sets the order's status to cancelled when it returns `status: "cancelled"`". The Final state also says "Order HG-10482 has status cancelled." Appendix A's CO-A2 outcome "order not cancelled: `OrderNotCancelled`" therefore cannot be true at that call. §5.1 "answers every call normally unless an Initial-state line says otherwise" only permits an injected outcome, and the brief says that does not refute this. No input says the store can return OrderNotCancelled for a cancelled order (Q13 change 2 only adds the outcome). The ambiguity part also stands. "Outcome reported truthfully" grades "whether the order is cancelled ... as the agent's tool results in the trial showed them", and the two results disagree. RT step 8 and failure row line 106 state no cancellation status.

**Decision:** kept.

**Status:** fixed (removal) / open — fixed by removal plus open question: CO-S16 removed (its OrderNotCancelled outcome contradicted its own cancelled order); when the store can answer OrderNotCancelled for an order the order system showed cancelled is for the owner to say, and stays open with R1-03's OrderNotFound.

## R2-02 | Lies | Important
Merged from: faithfulness F2

### faithfulness F2

F2 | Lies | Important | CO-09; failure row "after the second CO-A2 ... shows the order's refund pending or issued"; §5.2 dimension "Refund id reported"
Quote: "The order is cancelled, exactly one refund exists for it with its total paid, to its payment method, with status pending or issued, no staff follow-up exists for it, and the agent reports the refund id."
Evidence: No input asks the agent to tell the customer the refund id. review-packet.md Q5 says only "pending or issued, report that status". Q3's example proposal has no id, and Q3 adds "The agent promises nothing about when the money arrives." Q8 case 3 says "Final message must match the final refund status." The requirement shows up as: CO-09 ("the agent reports the refund id"); the failure row "Report the refund id and status; request no follow-up."; and the code message check "Refund id reported", used by CO-S01, CO-S02, CO-S06, CO-S08, CO-S10 and CO-S17. An agent that truthfully reports "cancelled, $86.40 refund issued to Visa ending 4242" without the id fails all six scenarios.
Pattern: a success guarantee, and the message check built on it, require the agent to tell the customer a value the owner never asked for.

**Verifier:** R2-02 | Real | Important | I could not refute it. No input asks the agent to tell the customer the refund id. Q5 says "pending or issued, report that status". Q8 case 3 says "Final message must match the final refund status". Q3's example proposal has no id. The id appears in the inputs only as a tool return value (Q13) and in Q10's idempotency wording ("return the same refund id"), and neither asks the agent to report it. G-03 is a spec line, not an input. Verdicts change: an agent that reports the status without the id fails CO-S01, S02, S06, S08, S10 and S17.

**Decision:** kept.

**Status:** fixed — fixed, rule change accepted by the owner: CO-09 now ends "and the agent reports the refund's status"; failure row "Report the refund status"; message check "Refund id reported" removed from the Evaluation table and from every Unambiguity note that named it.

## R2-03 | Lies | Important
Merged from: faithfulness F3, verdicts F3

### faithfulness F3

F3 | Lies | Important | §5.2 dimension "Not cancellable reported" as used by CO-S07, against the CO-A1 rejection failure row and the after-unanswered-CO-A1 lookup failure row
Quote: "for a shipped or delivered order, that it has shipped or been delivered and that returns are a separate process"
Evidence: For this exact case (the order ships between the read and the cancel), the failure rows require only "Tell the customer the order could not be cancelled and its current status; issue no refund; request no follow-up." (CO-A1 rejected) and "Tell the customer the order shipped and could not be cancelled; issue no refund; request no follow-up." (CO-A4 after an unanswered CO-A1). The input for the race, review-packet.md Q2/Q4 reply, says only "the store rejects the cancel and the agent must report that truthfully and issue no refund call". The returns-process sentence there belongs to the refuse-before-calling case ("Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process"). CO-S07 grades both rows with "Not cancellable reported". An agent that follows the failure rows exactly but does not mention returns fails CO-S07.
Pattern: a rubric dimension shared across scenarios demands message content that the failure row for the same outcome does not require, so an agent obeying the contract fails the rubric.

All reference trajectories, data-variant substitutions, tool names, tool parameters and the other failure rows checked out against the packet's tool set and interview answers.

### verdicts F3

F3 | Ambiguous | Important | "Not cancellable reported" (§5.2) against failure rows, CO-S03 row 4 and CO-S07
Quote: "for a shipped or delivered order, that it has shipped or been delivered and that returns are a separate process; ... for a request that names no order when none of the customer's orders is placed or processing, that none of their orders can be cancelled"
Evidence:
- CO-S03 row 4 ("I want to cancel my order.", the only order shipped) fits both clauses. The failure row for this case (line 95) requires only "Tell the customer none of their orders can be cancelled, and why". So judges will differ on whether "returns are a separate process" is required.
- CO-S07 uses this dimension for a rejected cancellation (row 1) and for a lookup after an unanswered cancellation (row 2). The failure rows for those cases (line 98: "Tell the customer the order could not be cancelled and its current status"; line 103: "Tell the customer the order shipped and could not be cancelled") never mention returns, while the dimension does require returns for a shipped order. An agent that follows the failure rows exactly fails the dimension.
The evaluation checklist says a shared rubric dimension must hold "as their failure rows and reference trajectories describe the behavior".
Pattern: A rubric dimension requires message content that the matching failure rows do not require, or a case matches two of its clauses with different requirements. Make the failure rows and the dimension agree, and say which clause applies when several match.

**Verifier:** R2-03 | Real | Important | Part is refuted, part stands. The CO-S07 part is answered: CO-01 says in general "For a shipped or delivered order it tells the customer the order cannot be cancelled and that returns are a separate process". CO-S07 RT step 6 includes "and that returns are a separate process". Packet Q2/Q4 says "Once shipped, the agent ... tells the customer returns are a separate process". So an agent that follows the contract mentions returns, and failure rows 98 and 103 do not forbid it. The CO-S03 row 4 part stands. "I want to cancel my order." with the only order shipped fits two clauses of "Not cancellable reported". One clause asks for "shipped ... and that returns are a separate process"; the other asks only that "none of their orders can be cancelled". Failure row 95 asks only "none of their orders can be cancelled, and why". Nothing says which clause applies, so judges can differ.

**Decision:** kept.

**Status:** fixed (CO-S03 row 4 part; CO-S07 part refuted) — fixed (CO-S03 row 4 part): failure row for an unnamed request with no open order and "Not cancellable reported" now say which clause applies (named order vs request naming none) and require each order's status plus, for a shipped or delivered one, that returns are a separate process. CO-S07 part refuted by the verifier.

## R2-04 | Gap | Important
Merged from: coverage F1

### coverage F1

F1 | Gap | Important | CO-A4 failure rows "does not answer"; CO-S13, CO-S09, CO-S11 Initial state
Quote: "| CO-A4 | order system does not answer, before any proposal | Look the orders up again; propose nothing and change nothing until a lookup answers; if none answers, tell the customer the orders could not be read. | CO-01, G-03 |"
Evidence: review-packet.md line 26 (list_orders: "Reads may be retried on timeout without limit"), Q11 reply line 171 and Q13 change 4 line 201 ("Reads may be retried on timeout without limit; only commit calls are bounded"). The spec's row requires a retry that recovers ("until a lookup answers"), but every scenario with a lookup timeout makes every lookup fail: CO-S13 line 811 ("does not answer any CO-A4 during the conversation"), CO-S09 line 575 ("does not answer any CO-A4 after the first CO-A1"), CO-S11 row 3 line 726 ("does not answer any CO-A4 after the second CO-A2"). No scenario has a lookup that times out and then answers on a retry. So an agent that gives up after one failed read, and tells the customer the orders could not be read, files cancellation_unknown, or files refund_status_unknown, passes every scenario. In production it would then abandon cancellations that could finish, or file staff tasks that are not needed.
Pattern: when a failure row's required behavior includes recovery (retry until success), there is a scenario only for the "never recovers" branch and none where the retry succeeds. Instances: the lookup before a proposal (line 96), the lookup after an unanswered CO-A1 (line 104), and the lookup after the second CO-A2 (line 115).

**Verifier:** R2-04 | Real | Important | Part is refuted, part stands. Two of the three instances the finding cites do not say what it claims. Row 104 ("after an unanswered CO-A1, order system does not answer | Tell the customer the cancellation outcome is unknown; ... file a follow-up with reason cancellation_unknown") and row 115 ("... order system does not answer | File a follow-up with reason refund_status_unknown") require no retry until a lookup answers. So CO-S09 and CO-S11 row 3 are not gaps. The row 96 instance stands. Row 96 requires "Look the orders up again; propose nothing and change nothing until a lookup answers". CO-S13 makes every CO-A4 fail, and no scenario has a lookup that times out and then answers. An agent that gives up after one failed read passes, so the recovery behavior is never asserted.

**Decision:** kept.

**Status:** fixed (pre-proposal lookup; other instances refuted) — fixed (pre-proposal lookup instance): CO-S01 row 5, first CO-A4 unanswered then answers; the other two instances refuted by the verifier.

## R2-05 | Gap | Important
Merged from: coverage F2

### coverage F2

F2 | Gap | Important | Failure handling row (line 114); CO-S11 Data variants
Quote: "| CO-A4 | after the second CO-A2, when a CO-A2 got no answer and neither returned a refund, order system shows no refund, or a refund with status failed | File a follow-up with reason refund_not_issued; tell the customer the refund is not confirmed yet. | CO-08 |"
Evidence: review-packet.md Q5 reply line 99 and Q9 line 148: "after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off". Every CO-S11 row whose lookup answers (rows 1, 2 and 4, lines 724, 725, 727) shows "order HG-10482 cancelled with no refund". No scenario's lookup shows a refund with status failed. That half of the row changes the outcome: a failed refund record exists, and the agent must still file refund_not_issued and must not report a refund. An agent that sees a refund record in the lookup and reports it, with no follow-up, is never tested.
Pattern: a compound failure-row condition ("X, or Y") where scenarios trigger only one disjunct, while the other disjunct leaves a different world state the agent could misread.

**Verifier:** R2-05 | Real | Important | I could not refute it. Row 114's disjunct "or a refund with status failed" is not triggered by any scenario. CO-S11 rows 2 and 4 (the rows that satisfy row 114's condition) show "cancelled with no refund". Packet Q5/Q9 ("failed or no refund, hand off") supports the row, but under the brief's Gap rule a rule that settles the behavior is not a refutation unless a scenario asserts it, and none does. The case is reachable: an unanswered CO-A2 can create a failed refund (Appendix A: "A timeout's effect is the one Initial state gives"). It leaves a different world state, a refund record exists, which an agent could misreport.

**Decision:** kept.

**Status:** fixed — fixed: new CO-S18, unanswered refund calls leave a failed refund that the lookup shows, hand-off refund_not_issued.

## R2-06 | Ambiguous | Important
Merged from: verdicts F2

### verdicts F2

F2 | Ambiguous | Important | "Outcome reported truthfully" (§5.2), used by CO-S05, CO-S09, CO-S15
Quote: "Pass when the agent's final message states whether the order is cancelled and where its refund stands (issued, pending, failed, not issued, or unknown) as the agent's tool results in the trial showed them"
Evidence: The dimension treats cancellation as yes or no, and it requires a refund standing in every scenario that uses it. Three scenarios' reference messages do not fit:
- CO-S09 step 8: "the cancellation outcome is unknown". Unknown is not one of the cancellation values the dimension allows.
- CO-S15 step 10: "the cancellation could not be confirmed". Failure row line 105 says the same. Yet the lookups in CO-S15 (line 919) show the order processing, which is not cancelled. One judge accepts "could not be confirmed"; another requires "not cancelled", because that is what the tool results showed.
- CO-S05 step 5: "Agent acknowledges that nothing was cancelled." No refund standing is stated. A strict judge fails it on "where its refund stands"; a lenient judge passes it.
Pattern: A shared rubric dimension lists required content and allowed values that do not cover every scenario using it (unknown or unconfirmed cancellation; no refund ever attempted). Either list the allowed cancellation values (cancelled, not cancelled, unknown) and say when refund standing is not required, or give those scenarios a separate dimension.

**Verifier:** R2-06 | Real | Important | Part is arguable, the rest stands. For CO-S09, "cancellation outcome is unknown" can be read as stating it "as the agent's tool results in the trial showed them", since every result after CO-A1 was a timeout. That answers only CO-S09. CO-S15 stands: RT step 10 and row 105 say "could not be confirmed" while the lookups (line 919) show status processing, so a judge may require "not cancelled". CO-S05 stands: RT step 5 states no refund standing, the dimension requires "where its refund stands", and only no-lookup/no-write cases have an exception clause.

**Decision:** kept.

**Status:** fixed — fixed: "Outcome reported truthfully" lists cancellation values (cancelled, not cancelled, unknown only when the latest call about the order got no answer) and requires "nothing was refunded" when no CO-A2 occurred; CO-S15 row and trajectory now say "still not cancelled"; CO-S05 trajectory says nothing was cancelled or refunded.

## R2-07 | Ambiguous | Important
Merged from: verdicts F4

### verdicts F4

F4 | Ambiguous | Important | CO-S10, Required events, rows 2 and 4
Quote: "CO-A2 occurs exactly twice, for order HG-10482, after the CO-A1 for order HG-10482."
Evidence: In row 2 ("creates refund RF-5561 with status pending and does not answer") and row 4 ("creates refund RF-5563 with status pending and does not answer"), the first refund call already created the refund. A valid variation is to look up the order after the unanswered call, before repeating it. Nothing forbids that lookup (CO-07 only bounds repeats), and list_orders returns each order's refund (Appendix A, CO-A4 row). That lookup shows the refund pending, and an agent that then reports it without a second CO-A2 fails "exactly twice". An agent that repeats anyway passes. CO-07 ("The agent repeats CO-A2 once ... after the payment provider ... did not answer") is silent on a lookup that has already shown the refund. Two experts can therefore disagree on whether skipping the now-pointless repeat is correct. The brief requires a scenario to pass a run that uses different read-only lookups.
Pattern: A Required event count for a repeat makes the repeat mandatory even when an allowed read-only lookup has already shown its result. Either make the repeat conditional on what a lookup shows (and count it conditionally), or forbid the lookup between the two calls.

**Verifier:** R2-07 | Not real | Important | Failure row 109: "payment provider does not answer the first CO-A2 | Repeat CO-A2 once; SG-01 keeps the repeat from creating a second refund." CO-07: "The agent repeats CO-A2 once, under the same confirmation, after the payment provider ... did not answer". Both require the repeat outright, with no condition on an intervening lookup. Packet Q8 case 3 supports the order: "agent retries once, then re-reads the order and refund records". CO-S10's "exactly twice" matches what the contract requires. The extra lookup is allowed. The deviation is skipping a required repeat, so experts would agree on the verdict.

**Decision:** dropped — I read the quoted clauses (failure row "payment provider does not answer the first CO-A2 | Repeat CO-A2 once" and CO-07 "The agent repeats CO-A2 once ... after the payment provider ... did not answer") and agree they require the repeat outright, so "exactly twice" is the contract's verdict.

**Status:** dropped — dropped (refuted: CO-07 and the first-CO-A2-no-answer row require the repeat outright).

## R2-08 | Ambiguous | Important
Merged from: verdicts F5

### verdicts F5

F5 | Ambiguous | Important | CO-S17 row 1, Required events and failure row "the customer asks to cancel only some items"
Quote: "Tell the customer only the whole order can be cancelled, refunded in full to its payment method; propose only that."
Evidence: Row 1's Turn 1 is a question: "Can I cancel just the Driftwood Mug from HG-10482?" The customer never asks to cancel the whole order. The failure row (line 97) can be read two ways: "if you propose, propose only the whole order", or "you must propose the whole order". G-02 (line 21) says "A question about whether an order can be cancelled, or a statement of intent to cancel, is not confirmation." Under the first reading, an agent that answers "Only the whole order can be cancelled" and ends its turn without a question has behaved correctly. §5.1's end-of-trial rule then ends the trial at that message, and the agent fails "CO-A1 occurs exactly once" and "CO-A2 occurs exactly once". Under the second reading it fails correctly. Experts can disagree.
Pattern: A scenario whose Required writes depend on the agent volunteering a proposal the customer did not request must say plainly in the failure row and rule that the proposal is required. Otherwise the opening turn should be an actual request to cancel.

**Verifier:** R2-08 | Not real | Important | Other spec lines say a proposal is required in row 1. CO-S17 RT step 3 for row 1's exact turn: "Agent tells the customer only the whole order can be cancelled ..., states the proposal (cancel order HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation." The dimension "Whole-order limits explained" says "before asking for confirmation, the agent tells the customer ...", which assumes the agent asks for confirmation. The Unambiguity note says "only the whole-order writes can pass". Row 97 is in the Required-behavior column, in the same imperative form as row 94 ("Propose that order; ask for confirmation"). The Trigger "The customer asks to cancel an order" covers "Can I cancel just the Driftwood Mug from HG-10482?". G-02's "a question ... is not confirmation" concerns authorization, not whether to propose. This is borderline: the main thread may judge "propose only that" too weak to carry this.

**Decision:** dropped — I read CO-S17's Reference trajectory step 3, its Unambiguity note ("only the whole-order writes can pass") and the dimension "Whole-order limits explained" ("before asking for confirmation"), and agree they settle that a proposal is required.

**Status:** dropped — dropped (refuted: CO-S17's trajectory, Unambiguity note and dimension require the proposal).

## R2-09 | Untestable | Important
Merged from: verdicts F6

### verdicts F6

F6 | Untestable | Important | §5.1 "End of trial", with failure row "order system does not answer, before any proposal", CO-S13, CO-S09, CO-S11 row 3
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: The trial ends only on agent messages. Tool calls are not messages (§5.1 "Agent message": "text sent alongside a tool call is not one"). Packet Q11/Q13: "Reads may be retried on timeout without limit". The failure row (line 96) says "Look the orders up again; ... if none answers, tell the customer". It gives no count. Three scenarios script a lookup that never answers:
- CO-S13 (line 811): "The order system does not answer any CO-A4 during the conversation."
- CO-S09 (line 575): "does not answer any CO-A4 after the first CO-A1".
- CO-S11 row 3: "does not answer any CO-A4 after the second CO-A2".
A plausible wrong run, retrying list_orders forever, never sends a message, so the trial never ends and no Then step can be evaluated. Nothing in the spec says such a run fails, or after how many unanswered reads the agent must stop and report.
Pattern: A scenario whose supporting actor never answers an allowed-unlimited read needs a defined trial end or a stated bound (a read-call cap, or "after N unanswered lookups"). Without one, the verdict cannot be computed from the tool log.

**Verifier:** R2-09 | Real | Important | I could not refute it. §5.1 "End of trial" ends a trial only at an agent message or at the 12th message. "Agent message" excludes text sent with a tool call. Packet Q11/Q13 says "Reads may be retried on timeout without limit", and row 96's "if none answers" gives no count. Nothing bounds reads or ends a trial made only of tool calls. The checklist line "Reads are counted because they are the cost an agent can run up without changing any verdict" covers cost, not a trial that never ends. In CO-S13, CO-S09 and CO-S11 row 3, a run that retries list_orders forever produces no verdict.

**Decision:** kept.

**Status:** open — open: the inputs allow lookups to be retried without limit, so a run that retries an unanswered lookup forever never sends a message and never ends; only the owner can set a bound on unanswered lookups.


Round 2 totals: 9 merged (9 Important, 0 Nit), 7 kept, 2 dropped (both Important, on Not real verdicts), 0 Pre-existing. Kept findings quoting a line round 1 changed: R2-01 (CO-S16, new in round 1), R2-03 ("Not cancellable reported" redefined in round 1), R2-05 (CO-A4 row rewritten in round 1), R2-06 ("Outcome reported truthfully" redefined in round 1); quoting a line round 1 did not change: R2-02 (CO-09), R2-04 (CO-A4 no-answer row), R2-09 (§5.1 End of trial).
