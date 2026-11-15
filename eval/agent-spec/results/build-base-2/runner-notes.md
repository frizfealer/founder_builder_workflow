# Runner notes (build-base-2)

## Step 3 decisions
- One capability, Cancel Order and Refund (CO), state-changing. Cancellation and refund are one user goal (round 3 Q1: one confirmation covers both).
- CO-A4 (list_orders) is a bound read-only action because failure rows and Forbidden lines name it (re-read after unknown cancel/refund).
- Own derivation, flagged as an open question: after a second CO-A1 that got no answer and a read that shows the order still placed/processing, the agent reports and sends nothing more (no handoff). The interview only covers the first timeout. CO-S12 encodes it.
- OrderNotFound (cancel) and OrderNotCancelled (refund) rows are unreachable for a correct agent; kept as rows with no scenario, noted in the row.

## Step 3.8
- Own proposal written into Appendix A, checker 0 errors, then rebound to the recorded proposal + four changes. Differences logged in interview-replay.md. Change 3 added CO-S17 and changed CO-S18; change 2 added a failure row; changes 1 and 3 added SG-04 and SG-03.

## Step 3.9 merges (checker WARNING groups)
- CO-S08 (cancellation got no answer, read shows cancelled) merged into CO-S01 as row 4 (new column "first cancel"; Forbidden gained the conditional read-before-refund line; Illustrates gained CO-06, G-04). Dropped source row: CO-S08 row 2 (Turn 1 "Cancel HG-10482, please." with the unanswered cancellation) - it exercised only a wording variant of the CO-06 read-then-refund path.
- CO-S10 (cancellation got no answer, read shows shipped) merged into CO-S07 as row 3 (new column "first cancel"; Illustrates gained CO-06, G-04; dimension "Cannot-cancel reason given" now applies to the row too). Dropped source row: CO-S10 row 2 (Turn 1 "Please cancel HG-10482 and refund it." with the unanswered cancellation) - wording variant of the CO-06 shipped branch.
- CO-S15 (two refund calls got no answer, read shows refund pending/issued) merged into CO-S13 as rows 4 and 5 (new columns "second refund", "refund_status"; Forbidden gained the conditional "Ending the trial without a CO-A4 ..." line). No source row dropped.
- CO-S02 / CO-S03 stay apart: final-state lines differ (CO-S02 asserts HG-10455 unchanged) and the User / User-knows blocks differ in kind (a required which-order question vs a scripted Turn 2 change), which data-variant rows cannot express.
- Unused ids: CO-S08, CO-S10, CO-S15.

## Step 4 decisions
- Finder and verifier briefs built from references/verification.md; one line added to each: read only the files named and the packet's files (trial rule 3).
- Style-only Nits kept when the finding was not about wording/style/formatting/heading/preference (R1-06, R1-11, R2-03, R3-06), per step 4.4. Dropped only R2-04 (Not real: Appendix A already marked provisional) and R3-07 (Not real: precision is unscored by design).
- Rule-text changes were not applied (R1-10, R2-03, parts of R2-06, R2-07, R3-01); reported as proposed rule changes.
- I briefly added a sentence to §5.2 Graders fixed text in round 3 (R3-02) and reverted it before the checker's final run; verified the §5.1/§5.2 fixed text is identical to round0 by diff. The fix went into the rubric definitions instead.
- Round 2's duplicate (faithfulness F1 = verdicts F2) merged into R2-01.
- Attribution (round copies diffed): round 2 kept findings quoting a round-1-changed line: R2-02, R2-05, R2-10 (3 of 9); round 3: R3-05 (1 of 6).
- Dispatch: three finders in parallel per round, verifier after all three returned; all notifications arrived.
