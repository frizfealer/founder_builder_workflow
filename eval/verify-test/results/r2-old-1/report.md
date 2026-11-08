# Step 5 report, r2-old-1

Rounds run in this trial: 2 and 3. Round 1 was frozen. Verification stopped at the round cap, so round 3's fixes have not been reviewed by another round.

## File written

`eval/verify-test/run/agent-spec.md`, copied to `results/r2-old-1/agent-spec-final.md`. Nothing under `examples/` changed.

| Capability | Scenarios |
|---|---|
| Cancel Order (CO), state-changing | 46 (CO-S01 to CO-S46) |

The frozen spec had 29 scenarios. Round 2 added CO-S30 to CO-S43, and round 3 added CO-S44 to CO-S46.

## Merges of step 3.9

Step 3.9 did not run, because this trial starts inside step 4. No scenarios were merged and no rows were recorded as dropped. The checker prints 10 merge-candidate warnings on the final spec; the frozen spec had 6.

Two rows moved rather than dropped: CO-S16 rows 2 and 3 became CO-S43 rows 1 and 2. CO-S20 row 2 became CO-S40. CO-S17 and CO-S23 lost rows that differed only in a failure cause the tool cannot return, and now have two rows that differ by order values.

## Input ledger, final state

From the frozen review packet; this trial did not change it.

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial: `issue_refund` supplied by the user, the rest proposed and confirmed with changes |
| 3 | Data model | found |
| 4 | Authorization policy | found, default accepted |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases named by the user, no transcripts |

Default accepted by the user: the agent cancels only after the customer explicitly confirms the full proposal, and any change after confirmation voids it.

## Proposed tools

`list_orders`, `cancel_order` and `request_staff_followup` were proposed and confirmed with the user's changes. `issue_refund` was supplied. They remain provisional. Appendix A is the part of the spec that architecture notes may change. This trial did not change Appendix A.

## Checker

Final run: `0 errors`, with 10 merge-candidate warnings.

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03, CO-S06 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S27, CO-S32, CO-S33, CO-S36, CO-S46 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S25, CO-S26, CO-S31, CO-S38, CO-S39, CO-S40, CO-S43, CO-S44, CO-S45 |
| G-04 | CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26, CO-S30, CO-S31, CO-S43 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10, CO-S29, CO-S33, CO-S41 |
| CO-02 | CO-S02, CO-S07, CO-S28, CO-S29, CO-S41, CO-S42 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S32, CO-S34, CO-S37, CO-S46 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27, CO-S28, CO-S32, CO-S33, CO-S34, CO-S35, CO-S36, CO-S46 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S24, CO-S26, CO-S30, CO-S31 |
| CO-06 | CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S30, CO-S31, CO-S38, CO-S39, CO-S43, CO-S44, CO-S45 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S25, CO-S38, CO-S39, CO-S40, CO-S43, CO-S44, CO-S45 |
| CO-08 | CO-S01, CO-S16, CO-S19 |

## Findings

Round 2: 25 findings: 15 Important, 10 Nit. Round 3: 13 findings: 6 Important, 7 Nit. Every finding was kept, each with three Real verdicts. Each finding's full text, verdicts and outcome are in `round2-findings.md` and `round3-findings.md`.

| Outcome | Round 2 | Round 3 |
|---|---|---|
| fixed in full | R2-01, 04, 05, 06, 07, 09, 10, 11, 13, 14, 15, 16, 18, 20, 21, 23 | R3-02, 03, 06, 10, 12, 13 |
| fixed in part, with an open question or rule proposal | R2-02, 03, 08, 25 | R3-01, 05 |
| fixed in part, with a Pre-existing remainder | none | R3-04, 09 |
| answered, with its reason | R2-19, R2-22 | none |
| open | R2-12, R2-17, R2-24 | R3-07 |
| Pre-existing | none | R3-08, R3-11 |

Reasons for the answered findings:
- R2-19: `OrderNotFound` is a user-confirmed outcome and its failure row needs a scenario, so CO-S24's world stands.
- R2-22: the counting rule is the template's fixed §5.2 text, which changes only when the user asks.

Whether a kept finding quotes a line the previous round changed:

| Round | Quotes a line the previous round changed (a fix that introduced a defect) | Quotes a line it did not change (a defect earlier finders missed) |
|---|---|---|
| 2 | 7: R2-01, 05, 06, 11, 14, 21, 23 | 18 |
| 3 | 6: R3-01, 02, 03, 04, 05, 06 | 7 |

R2-05 quotes "absent", and counts as changed because the missing line belongs to CO-S25, which round 1 added. R3-13's defect predates round 2, although round 2 appended to those two note lines, so it counts as not changed.

## Reviewers

Faithfulness and coverage finders and all six verifiers ran as Claude subagents. Both verdicts finders ran through Codex (`codex:codex-rescue`). Figures are in `subagent-stats.md`.

## Rule changes proposed for you to decide

The skill stops a fix at a rule's text, so none of these is applied.

**P1, CO-08 (R2-02, R2-03).** No input asks for the refund id, and the user asked for the status to be reported.
- Before: "...no follow-up task exists for it, and the agent tells the customer the refund id."
- After: "...no follow-up task exists for it, and the agent tells the customer the order is cancelled and the refund's status."
- If you accept this, also remove dimension "Refund id reported" from the 17 scenarios that use it. Until then a truthful report without the id fails them.

**P2, CO-03 (R2-17, R3-05).**
- Before: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
- After: "When the customer asks to cancel only some items, the agent tells the customer only the whole order can be cancelled. When the customer asks for a different amount, a different payment method or store credit, the agent tells the customer the refund is the total paid to the order's payment method. In both cases it proposes nothing else. When the customer asks what a cancellation would refund, the agent states the order's total paid and payment method."

**P3, CO-06 (R2-12).** Applies only if your answer to Q2 allows a second order.
- Before: "at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation"
- After: "at most two CO-A2, at most two CO-A3 and at most two CO-A4 for an order"

**P4, CO-02 (R3-06).**
- Before: "When none has, the agent tells the customer none of their orders can be cancelled and proposes nothing."
- After: "When none has, the agent tells the customer none of their orders can be cancelled, or that no orders are on their account when there are none, and proposes nothing."

**P5, G-04 (R3-11).**
- Before: "(Appendix B, SG-01)"
- After: "(Appendix B, SG-01, SG-03)"

## Open questions

- **Q1.** What if a lookup does not answer once? Must the agent retry, and when does it stop? The user allowed unlimited read retries and did not say when to give up, so no scenario has a read that fails once and then answers. (R2-08)
- **Q2.** What if the customer wants two orders cancelled, at once or one after the other? (R2-12)
- **Q3.** What if the retried refund returned pending and the re-read then fails? The user's round 3 Q3 answer says to report status unknown and hand off. CO-07 says "CO-A4 occurs in no other situation" when a refund is shown pending. The row and CO-S44 follow CO-07 for now. If you prefer the Q3 answer, CO-07, that row and CO-S44 all change. (R3-01)
- **Q4.** What if a refund comes back with a different amount or payment method than proposed, an open order already has a refund, or an order lacks its total paid or payment method? (R2-24)
- **Q5.** What if the customer changes their mind after the order is cancelled? No action reverses a cancellation. (R2-25)
- **Q6.** What if the customer describes an order and the description matches none or several? (R3-07)

Carried from round 1 and still open: the right handling of `OrderNotCancelled` (M2), and whether the agent should do more for an order that was already cancelled with a failed or missing refund (M10).

## What verification cannot catch

Whether the rules are the business's real rules, and whether the stakeholder list is complete. Only you can confirm those.

## Patterns no checklist covers, proposed as lines

I searched the three checklists for these patterns and found no line that states them.

- Evaluation checklist: "A clause that requires asking or holding back has no write to check, so it needs a rubric dimension in every scenario where it applies; a simulated user who deflects will hide the failure." (R2-01, R3-04)
- Evaluation checklist: "A prohibition on what the agent says needs a scenario that provokes it, such as the customer asking for the thing it must not promise." (R2-11)
- Evaluation checklist: "An answer the agent owes the customer needs a check, even when the scenario's point is that it holds back." (R3-05)
- Use-case checklist: "A failure row reachable from more than one attempt has a scenario for each branch on each attempt." (R2-06)
- Use-case checklist: "A confirmation qualified in the same message confirms nothing. List every qualifier: another order, other refund terms, some items, a withdrawal." (R2-07, R3-03)
- Use-case checklist: "Failure rows that branch on the same lookup or call are mutually exclusive. When a fix widens a row, recheck it against its neighbours and its rule." (R3-01, R3-02, R3-06)
- Template, §5.2: state whether interaction recall and precision count distinct pairs or occurrences. (R2-22)

## Interview

No interview ran in this trial. The frozen packet records the original interview's questions and answers.

## Things in this trial's setup to check

- **Layout.** `eval/verify-test/` did not exist in the repo. I built it from `~/Downloads/eval` (round-1 files) and `~/Downloads/eval-1` (round-0 spec, packet, product idea), matching the paths in the packet. `baseline/` and the earlier `run/` were left out so reviewers could not read them. `eval/` is untracked.
- **§5.1 and §5.2 re-sync skipped.** The skill re-syncs them in every update run. The frozen spec's §5.1 lacks the template's "Conditional Forbidden lines" paragraph, and I kept it frozen. So no fix used a conditional Forbidden line; that is why CO-S16's timed-out rows became a separate scenario. A run that re-syncs could keep them together.
- **Reviewer reads outside the brief.** Three round-3 reviewers (faithfulness finder, coverage finder, verifier B) opened `run/r2-merged.md` or `run/answered-so-far.md`, because they sit beside the spec. Both were written for this run, so no baseline leaked. It still widens what those reviewers saw. Round-2 verifier C also read the frozen round-0 spec.
- **Verifiers got the merged list as a file path, not pasted.** The content is the same. Verifier tool counts include that one read.
- **Severity count.** Round 2 verifier B's summary line said 18 Important and 7 Nit, but its per-finding lines give 13 and 12. I used the per-finding lines.
