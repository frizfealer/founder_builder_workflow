# Step-5 report: Harbor Goods order-support Agent Spec, verification rounds 2 and 3 (trial r2-new-1)

## File written

- `eval/verify-test/run-r2-new-1/agent-spec.md` (copy: `results/r2-new-1/agent-spec-final.md`). Round snapshots: `run-r2-new-1/round0/`, `round1/`, `round2/`, `round3/`.
- One capability: **4.1 Cancel Order** (state-changing, prefix CO), 29 scenarios (CO-S01 to CO-S29). No scenario was added or removed in rounds 2 and 3.

## Merges (step 3.9) and dropped rows

- No merges in this run. The checker's six WARNING groups (CO-S01/02/03/12/27/28; CO-S01/02/09/12/28; CO-S11/24/26; CO-S16/19; CO-S18/20; CO-S22/23) are unchanged from round 1. These are update rounds, and existing ids stay stable, so no group was merged.
- Dropped data-variant rows (round 3, R3-4):
  - CO-S17 row 2: the refund failed because the payment provider declined it.
  - CO-S17 row 3: the refund failed because the card has expired.
  - CO-S23 row 2: failure reason "the card has expired".
  - Each one exercised a terminal refund cause that no data-model field and no tool result distinguishes. CO-S17 now has rows RF-5531 and RF-5540 (values only). CO-S23 now has a "refund id" column with RF-5531 and RF-5540.

## Input ledger (final, unchanged in this run)

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial: issue_refund supplied; list_orders, cancel_order, request_staff_followup proposed and confirmed with the user's four changes |
| 3 | Data model | found |
| 4 | Authorization policy | found (default accepted: cancel only after explicit confirmation of the full proposal; any change voids it) |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases, no transcripts |

## Tools

Appendix A is provisional and is the part of the spec that architecture notes may change. The proposed tools are list_orders, cancel_order and request_staff_followup. issue_refund was supplied by the user. Supporting-actor guarantees are SG-01 to SG-04.

## Checker (final run)

```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12, CO-S27, CO-S28: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12, CO-S28: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S11, CO-S24, CO-S26: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)
```

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03, CO-S06 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S27 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S25, CO-S26 |
| G-04 | CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10, CO-S29 |
| CO-02 | CO-S02, CO-S07, CO-S28, CO-S29 |
| CO-03 | CO-S01, CO-S08, CO-S09 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27, CO-S28 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S24, CO-S26 |
| CO-06 | CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S25 |
| CO-08 | CO-S01, CO-S16, CO-S19 |

## Findings

**Rounds 2 and 3: 14 kept findings, 5 Important and 9 Nit. 11 are fixed, 1 is fixed in its failure rows with the rule change open, and 2 are open. 1 finding was dropped. None are Pre-existing.** Three rounds ran in all. Round 1 ran before this trial, and its 13 answered findings are in `run-r2-new-1/answered.md`. The stop condition is round 3 ending. Round 3's fixes were not re-reviewed.

**Round 2: 10 kept (4 Important, 6 Nit), 1 dropped.**

| Id | Sev | Summary | Status |
|---|---|---|---|
| R2-1 | Important | CO-S25 and CO-S26 did not require the lookup after the unanswered CO-A2 before the outcome report | fixed: added "Fewer than one CO-A1 after the second CO-A2." (CO-S25) and "... after the first CO-A2." (CO-S26) |
| R2-2 | Nit | "Order not cancelled reported" lost the "could not be found" check that CO-S24 needs | fixed: CO-S24 now uses its own dimension, "Order not found at cancellation reported" |
| R2-3 | Important | After the second unanswered CO-A2, a lookup showing the order open leads to "not cancelled" with no handoff, though the spec says a timed-out CO-A2 may take effect late | open (only the user can decide; changing it changes CO-07) |
| R2-4 | Important | "names no order" in CO-02 is undefined and differs from the sibling term "has not said which one they mean" | fixed in the two failure rows; the CO-02 rule change is proposed below (open) |
| R2-5 | Nit | CO-02 says "may propose" while its failure row and CO-S28 require the proposal | open: CO-02 rule change proposed below |
| R2-6 | Nit | "a lookup did not answer" rows overlap rows for a retried lookup | fixed: three conditions now read "no lookup ... answered (the agent may repeat the lookup first)" |
| R2-7 | Nit | The none-open row's reason is false for a customer with no orders | fixed: the reason is now "because none is placed or processing", and returns are mentioned only when an order shipped |
| R2-8 | Nit | Replies with no commit call had no guard that the lookup happened | fixed: "Fewer than one CO-A1." added to CO-S05, CO-S06, CO-S07, CO-S10, CO-S29 |
| R2-9 | — | CO-03 "states no date or time frame" was said to be stronger than the input's "promises nothing" | dropped (3 of 3 verifiers: Not real) |
| R2-10 | Important | "Refund not issued reported" accepted "not confirmed yet" after known refund failures | fixed: restored for CO-S17, CO-S18, CO-S22; CO-S20 now uses "Refund not confirmed reported" |
| R2-11 | Nit | Reference trajectories still showed "card closed", which the tool no longer returns | fixed: removed from CO-S17, CO-S22, CO-S23 |

- Kept findings that quote a line round 1 changed (a fix that introduced a defect): **9** (R2-1, R2-2, R2-3, R2-4, R2-5, R2-6, R2-7, R2-8, R2-10).
- Kept findings that quote a line round 1 did not change (a defect earlier finders missed): **1** (R2-11, a leftover of round 1's Appendix A edit).
- Kept findings that fell in a bundle context block: **0**. Two fixes extended past the bundle: R2-6 also fixed a section-4 context row, and R2-8 also fixed CO-S05, CO-S06, CO-S07 and CO-S10, which were not in the bundle.

**Round 3: 4 kept (1 Important, 3 Nit), 0 dropped.**

| Id | Sev | Summary | Status |
|---|---|---|---|
| R3-1 | Important | The lookup-count guards (R2-1, R2-8) do not require the report to come after the lookup; a question-bearing message or text sent with a tool call does not end the trial | fixed: six rubric dimensions now check that the outcome is stated only in text sent after the tool result that shows it |
| R3-2 | Nit | The cancellation-unknown row put the follow-up promise before CO-A4 | fixed: reordered so CO-A4 comes first |
| R3-3 | Nit | "No open order reported" and the CO-S29 note did not accept the reason the R2-7 fix wrote | fixed: both now accept either reason |
| R3-4 | Nit | CO-S17, CO-S22 and CO-S23 state refund-failure causes that no field or tool result carries, so variants are duplicates | fixed: causes removed; rows replaced (see Dropped rows) |

- Kept findings that quote a line round 2 changed: **3** (R3-1, R3-2, R3-3).
- Kept findings that quote a line round 2 did not change: **1** (R3-4).
- Kept findings that fell in a bundle context block: **0**.

Proposed rule change (R2-4, R2-5), not applied:

- CO-02 before: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order. When more than one has, the agent asks which and proposes nothing until the customer names one."
- CO-02 after: "When the customer has not said which order they mean, by number or otherwise, and exactly one of the customer's orders has status placed or processing, the agent proposes that order. When more than one has, the agent asks which and proposes nothing until the customer names one."

## Reviewers

All of them ran as fresh-context subagents, and none was given the spec author's conclusions.

| Role | Round 2 | Round 3 |
|---|---|---|
| Faithfulness finder | general-purpose subagent | general-purpose subagent |
| Verdicts finder | Codex, via `codex:codex-rescue` | Codex, via `codex:codex-rescue` |
| Coverage finder | general-purpose subagent | general-purpose subagent |
| Verifiers (three per round) | general-purpose subagents | general-purpose subagents |

Finders and verifiers read the re-review bundle and the review packet, and grepped the spec only for ids the bundle did not define.

## Open questions

- **What if the second CO-A2 times out, the lookup still shows the order open, and that CO-A2 then lands late?** The order ends up cancelled with no refund and no follow-up task, after the customer was told it was not cancelled. Should the agent hand off (reason cancellation unknown), add a caveat, or should the order system guarantee that a timed-out cancel never takes effect later? (R2-3)
- **What if the customer names an order by description ("my blanket order") and only a different order is open?** Does "has not said which order" include naming by item or date? The proposed CO-02 text says yes. And should the agent propose the only open order, or may it ask? The proposed text says it proposes. (R2-4, R2-5)
- Carried from round 1:
  - **What if issue_refund reports the order not cancelled?** The right handling is undecided (M2).
  - **What if an already-cancelled order has a failed or missing refund when a later conversation starts?** Should the agent do more than report it (M10)?

## What verification cannot catch

Verification cannot show whether these rules are Harbor Goods' real cancellation and refund rules, or whether the stakeholder list is complete. Only the user can confirm those.

## Proposed checklist lines

These cover kept-finding patterns no checklist covers. R2-2 and R2-10 are already covered by evaluation-checklist "A shared rubric dimension has one definition".

- **cockburn-checklist, Failure section** (R2-3): "A 'not done' outcome after a call that went unanswered, and that the spec allows to take effect late, ends in a handoff or a caveat, never a bare 'not done'."
- **evaluation-checklist** (R2-1, R2-8, R3-1): "When a report is truthful only after a lookup, the scenario checks both that the lookup occurred and that the report came after it. This is a narrow exception to 'Outcome, not path', and the lookup's place in the log is part of the outcome being reported."
- **specification-by-example-checklist** (R3-4, R2-11): "Initial state and data variants state no cause or attribute that no data-model field and no tool result carries; rows that differ only in such a cause are one row."

## Interview

No interview ran in this trial. The verification step started from round 1's answered findings. The review packet does not say which interview skill ran. Its interview was three rounds of questions plus a shared-understanding summary and a tool-confirmation turn.
