# Report: agent-spec verification run, trial it2-3

This run began at step 4.1 on a spec that already existed. Steps 1 to 3 and 4.2 did not run: the packet was copied, as the run prompt said.

## File and capabilities

- File written: `eval/agent-spec/run-it2-3/agent-spec.md`. It is copied to `results/it2-3/agent-spec-final.md`.
- One capability, **4.1 Cancel Order (state-changing), prefix CO**, now with **29 scenarios** (CO-S01 to CO-S29). The run started with 24. This run added these:
  - CO-S25, CO-S26 and CO-S27, the lookup branches after a second unanswered cancellation (R1-01);
  - CO-S28, a request that names no order when no order is open (R2-11);
  - CO-S29, a confirmation and a refund-term change in one turn (R3-01).
- One rule was added: **CO-09, No arrival date** (R1-12). The other rule texts are unchanged. Four rule changes are proposed below.

## Merges (step 3.9) and dropped rows

- Step 3.9 did not run, because the run started at step 4.1. No scenarios were merged.
- The checker still prints WARNING groups. Each group stays apart for a stated reason:
  - CO-S01/S02/S03/S12, CO-S01/S02/S09/S12/S29 and CO-S11/S24 predate this run.
  - CO-S13/S25 stay apart because CO-S25 forbids "CO-A3 before a CO-A1 made after the second CO-A2", which would wrongly fail CO-S13's rows.
  - CO-S26/S27 stay apart because their final status differs (open or shipped) and so do their dimensions ("Cancellation not done reported" or "Shipped order explained").
  - CO-S16/S19, CO-S18/S20 and CO-S22/S23 predate this run.
- Dropped data-variant row: **CO-S17, old row 2** (failed refund "because the payment provider declined it"). It exercised a terminal refund failure, the same handling and the same tool result as row 1, once R1-05 removed `failure_reason`. It was dropped under R2-09, and old row 3 is now row 2.
- CO-S23 changed its varied column from a failure reason to the order (HG-10482 or HG-10511).

## Input ledger (final state, from the review packet; unchanged by this run)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied by the user, the rest proposed and confirmed with changes | interview round 2 Q3 answer, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found (default accepted) | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases named by the user, no transcripts | interview round 2 Q4 answer |

The user accepted one default, for authorization: a state-changing call is authorized only by the customer's explicit confirmation of the full proposal, and any change voids that confirmation (round 1 Q4: "Yes to all").

## Tools

These tools are proposed and provisional: `list_orders()`, `cancel_order(order_number)` and `request_staff_followup(order_number, reason)`. `issue_refund(order_number)` was supplied by the user. Appendix A is the part of the spec that architecture notes may change. This run changed Appendix A in one place: R1-05 removed the `failure_reason` field from issue_refund's failed outcome, because no input defines it.

## Checker (final run, round 3 after fixes)

Count line: **0 errors** (8 WARNING merge-candidate groups, listed above).

Coverage table:

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S29 |
| G-03 | CO-S01, CO-S02, CO-S03, CO-S06, CO-S09, CO-S10, CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S25, CO-S26, CO-S27, CO-S29 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26, CO-S27 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10, CO-S28 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S29 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S29 |
| CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S24, CO-S25, CO-S27 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26, CO-S27 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S26 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25, CO-S29 |

## Findings

**39 findings over 3 rounds: 29 Important, 10 Nit.** Every finding went to a verifier. 34 were kept and 5 were dropped.

Kept findings by status: 24 fixed, 0 answered, 10 open, 0 Pre-existing. The scope was the whole spec, so no finding was tagged Pre-existing.

The run stopped at the round cap. Round 3 still had kept findings, and the round 3 fixes were not verified again.

| Round | Merged (Important / Nit) | Kept | Dropped | Fixed | Open |
|---|---|---|---|---|---|
| 1 | 16 (12 / 4) | 14 | 2 | 11 | 3 |
| 2 | 13 (10 / 3) | 13 | 0 | 10 | 3 |
| 3 | 10 (7 / 3) | 7 | 3 | 3 | 4 |

The full text of every finding is in `round1-findings.md`, `round2-findings.md` and `round3-findings.md`. Each has the verifier line and the decision.

| Id | Sev | Status | One-line summary |
|---|---|---|---|
| R1-01 | I | fixed | The second-unanswered-cancel row had no lookup branch. Branches added, plus CO-S25/26/27 and the CO-S15 lookup. |
| R1-02 | I | open | CO-S17 row 3 (OrderNotCancelled after cancelled) and CO-S24 (OrderNotFound for an order the lookup shows) inject outcomes that cannot happen. |
| R1-03 | I | fixed | The timeout path now says "the refund is not confirmed yet" (Round 3 Q3), with a new dimension on CO-S20. |
| R1-04 | N | open | G-04 lets SG-04 permit a blind cancel resend, and it cites only SG-01. Proposed rule change. |
| R1-05 | N | fixed | Removed `failure_reason`, which is not in the data model. |
| R1-06 | I | dropped | CO-S11 "reaches the order system" timing. |
| R1-07 | I | fixed | CO-S19/20/21 now say which unanswered refund call creates the refund. |
| R1-08 | I | dropped | CO-S16 "exactly twice" against a read-first agent. |
| R1-09 | I | fixed | "Refund terms explained" judged the amount term ambiguously. |
| R1-10 | I | fixed | In CO-S02 a guessed proposal could be confirmed. Added "Which order asked first". |
| R1-11 | I | fixed | Success scenarios did not check the reported refund status. |
| R1-12 | I | fixed | No check on promising an arrival date. Added CO-09 and its dimension. |
| R1-13 | N | fixed | The CO-S03/S04 Turn 2 trigger now names the question's values. |
| R1-14 | N | fixed | Removed the "Fewer than one CO-A1" absence line from CO-S19. |
| R1-15 | I | fixed | No scenario voided a given confirmation. Added CO-S03 row 4. |
| R1-16 | I | open | "No time limit" had no example. Added an old placed date (CO-S01 row 2). The CO-01 rule change is proposed. |
| R2-01 | I | open | The "still open after the second unanswered cancel" branch conflicts with SG-04's late-effect Covers cell. |
| R2-02 | I | fixed | "Refund status reported" asked for a statement no rule requires. Split off "No wrong refund status". Instances 1 and 3 stand (G-03 supports them). |
| R2-03 | N | fixed | The CO-S19 note credited the action log after R1-14. |
| R2-04 | I | fixed | Customer-facing meaning of pending and issued defined. |
| R2-05 | I | fixed | "Which order asked first" now defines a proposal. |
| R2-06 | I | fixed | "Refund not confirmed reported" now lists the wordings that count. |
| R2-07 | I | open | CO-09 is narrower than the input ("promises nothing about when"). Proposed rule change. |
| R2-08 | N | fixed | Forbidden lines with no confirmation turn now read "with no user's confirmation turn before it". |
| R2-09 | N | fixed | Removed the leftover "because ..." failure reasons. CO-S17 row dropped, CO-S23 re-varied. |
| R2-10 | I | fixed | CO-S06 now has failed-refund and no-refund rows. |
| R2-11 | I | fixed | New row and CO-S28 for an unnamed request when no order is open. |
| R2-12 | I | fixed | CO-S09 row 4 is a different-amount request. Dimension covers the term asked about. |
| R2-13 | I | open | The spec does not say what the agent tells a customer who asks to cancel a second order. |
| R3-01 | I | fixed | The "changed proposal term" row would propose a changed refund term. Split, plus CO-S29. |
| R3-02 | I | dropped | CO-07 against CO-S06 rows 2 and 3. |
| R3-03 | N | fixed | CO-S08 offered to cancel the whole order (a proposal under the spec's own definition). Removed. |
| R3-04 | I | open | How a rubric judge treats a true statement about an unfinished attempt, and the reading of CO-07's "once". |
| R3-05 | I | dropped | Message check against text sent alongside tool calls. |
| R3-06 | I | dropped | Whether "failed" meets "has not been issued". |
| R3-07 | N | open | The end-of-trial rule has no bound on unlimited read retries. |
| R3-08 | I | fixed | Unnamed request with exactly one open order: CO-S01 row 4. |
| R3-09 | I | open | Lookup "does not answer" branches do not say whether to retry first. |
| R3-10 | N | open | CO-03's telling clause does not match the per-cause failure rows. Proposed rule change. |

### Previous-round attribution (diff of the round snapshots)

- **Round 2: 13 kept.**
  - 7 quote a line round 1 changed, so a fix introduced the defect: R2-01, R2-03, R2-04, R2-05, R2-06, R2-07, R2-12.
  - 6 quote a line round 1 did not change, so earlier finders missed it: R2-02, R2-08, R2-09, R2-10, R2-11 (Gap, "absent"), R2-13.
  - R2-09's quoted line is unchanged, but the defect follows from R1-05 removing the field.
- **Round 3: 7 kept.**
  - 0 quote a line round 2 changed.
  - 7 quote a line it did not change: R3-01, R3-03, R3-04, R3-07, R3-08 (Gap, "absent"), R3-09, R3-10.
  - R3-03 relies on the proposal definition that R2-05 added, and R3-10 sharpens a point R2-12 raised.

### Verifier drop rate

- Important: **5 dropped / 29 verified** (R1-06, R1-08, R3-02, R3-05, R3-06).
- Nit: **0 dropped / 10 verified**. Three Nits got Style only verdicts in round 1 (R1-05, R1-13, R1-14) and two got Not real in round 3 (R3-03, R3-10). I kept all five, because none is about wording, style, formatting, heading choice or preference, and the round 3 refutations did not hold, as recorded in the findings files.

Each dropped finding, with the refutation I agreed with:

- **R1-06:** CO-S11 Unambiguity note: "The status change is tied to the agent's first cancellation, so every earlier lookup sees processing; in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation".
- **R1-08:** CO-A3 failure row: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. |". The packet also says the same: "agent retries once, then re-reads".
- **R3-02:** Scope & Authority: "The agent must not: cancel, refund or hand off any order other than the one the customer confirmed". CO-07's trigger also reads "after the retries CO-06 allows".
- **R3-05:** §5.1: "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one." §5.2: "A rubric judge reads every text the agent sends, including text sent alongside a tool call". Each grader's input is defined exactly.
- **R3-06:** The dimension's own "(pending and issued read as defined for No wrong refund status)", together with that definition, "issued when the money has been sent".

### Proposed rule changes (not applied; for the user to decide)

1. **G-04 (R1-04).**
   - Before: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
   - After: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or, for CO-A3 and CO-A4, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03)."
2. **CO-01 (R1-16).**
   - Before, first sentence: "The agent proposes cancelling an order only after a lookup shows it with status placed or processing."
   - After: "The agent proposes cancelling an order only after a lookup shows it with status placed or processing, whatever the order's placed date."
3. **CO-09 (R2-07).**
   - Before: "The agent promises the customer no date and no length of time by which the refunded money arrives."
   - After: "The agent tells the customer nothing about when the refunded money arrives."
   - Dimension "No arrival date promised" would follow the new wording.
4. **CO-03 (R3-10).**
   - Before, second sentence: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
   - After: "When the customer asks to cancel only some items, the agent tells the customer that only the whole order can be cancelled; when the customer asks for a different amount, a different payment method or store credit, it tells the customer that the refund is the total paid to the order's payment method; in both cases it proposes nothing else."

## Open questions

- **R1-02.** What if `issue_refund` returns OrderNotCancelled right after `cancel_order` returned cancelled? Or `cancel_order` returns OrderNotFound for an order the lookup just showed? Can either happen? If so, what does the agent tell the customer, and which handoff reason applies: refund not issued or cancellation unknown?
- **R2-01.** What if the lookup after a second unanswered cancellation shows the order still open? Is that lookup final, in which case SG-04's Covers cell should change? Or can the cancellation still land late, in which case the agent should hand off with reason cancellation unknown and not report "not cancelled"?
- **R2-13.** What if the customer asks to cancel a second order, in the same turn or later in the conversation? What does the agent tell them? Do the CO-06 retry caps count across orders?
- **R3-04.** What if the agent says something true about an attempt that has not finished, such as "still processing, retrying" or "the refund didn't go through, retrying"? Does that break a "never says ... was not cancelled" or "states no other status" clause? And is CO-07's "once the order system has created the task" a limit on when the agent may say staff will follow up?
- **R3-07.** What if every read times out and the agent retries list_orders forever? Where does the harness cut the trial off, and how is a cut-off trial scored? (This belongs in §5.1's fixed text.)
- **R3-09.** What if a lookup times out once and would answer on a retry? Must the agent retry before acting on "no answer"? If so, how many times?
- The rule changes proposed for R1-04, R1-16, R2-07 and R3-10 are open until the user decides them.

## What verification cannot catch

Verification checks the spec against its inputs. It cannot tell whether these rules are Harbor Goods' real cancellation and refund rules, or whether the stakeholder list is complete: the customer, the order system, store staff, Harbor Goods, the customer-support team and other customers. Only the user can confirm those.

Several open questions above came from this run's own fixes. R2-01 came from R1-01, and R3-02 (dropped) came from R2-10. They are business decisions, not spec mechanics.

## Proposed checklist lines

These are kept findings whose pattern I could not find, by grep, in any file under references/.

- **evaluation-checklist.md** (R2-02, R2-04, R2-06):
  - A rubric dimension may require only statements that a rule or failure row tells the agent to make.
  - Where a dimension grades a record status the agent may paraphrase, give each status a customer-facing meaning.
  - List the truthful wordings that meet a required proposition.
- **evaluation-checklist.md** (R3-04): Say how a judge treats a statement that is true when made about an attempt still in progress.
- **cockburn-checklist.md** (R2-11, R3-08): For a request that names no record, cover every count of eligible records: none, one, more than one. The "one" case needs ineligible records beside it.
- **cockburn-checklist.md** (R2-01): A failure branch that treats a lookup as settling an unanswered call must agree with every supporting-actor guarantee's Covers cell about late effects.
- **cockburn-checklist.md** (R3-01): A failure row about a changed proposal term must route each term the inputs fix (amount, payment method) to the rule that fixes it, not to "propose the changed proposal".

## Interview

No interview ran in this trial. It is a verification-only run that started at step 4.1, and step 4.2 was skipped. The packet records the original interview verbatim but does not say which interview skill ran.

## Reviewers

- Every finder and verifier ran as a native Agent-tool subagent: general-purpose, no model override.
- 12 subagents in all, 3 finders and 1 verifier per round.
- None ran through Codex. The skill's step 4.3 names three finders and no Codex finder, and the trial instructions required native subagents for every role.
