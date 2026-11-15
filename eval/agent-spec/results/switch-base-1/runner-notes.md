# Runner notes

- Stand-in replies arrived as hand-back messages; each task notification (usage) arrived afterwards. The harness reported only subagent_tokens, not the input/output/cache split, so tokens_in/out/cache_read are null.
- Grilling and grill-with-docs were not invoked: the skill under test does not mention them.
- The run prompt names steps 3.8 and 3.9; this skill version has no such steps. The tool confirmation is in step 3.4 (question 9).
- Step 3.4: the first checker run had 2 breaks (R-02, R-09), both mistakes in the model's rule checks (R-02 checked a shipped order the request was not about; R-09 counted a retry that returned a failed refund as unchecked). Fixed in the model, not taken to the owner.
- Step 3.4 turn 2, question 13: the stand-in answered from the record ("Reads may be retried on timeout without limit"), which rejects my three-try bound. I recorded it as the owner's decision D-10 and left C-34 (the first list fails) as spec only.
- After the 3.4 answers, the R-11 break appeared (different amount on the retry, then the list fails). Both 3.4 turns were spent, so it stays an open decision on policy.md.
- Drops: F1, F2, F6, F7, F11 on the verifier's quoted lines, which I read and agree settle each case. F8 is Style only and a phrasing preference (the row's action already says "shipped or been delivered"). F9 is kept although Style only: the reason states a fact C-05 contradicts, so it is not phrasing. F10 is kept for C-02, C-04, C-07 and C-13 (a claim saying more than its quote is Lies by definition). C-29 and C-38 are refuted by the claims template.
- F5 was kept at the verifier's severity, Nit (lower than the finder's Important).
- F3: the owner accepted the R-04 change in the 4.5 turn (question 17, stand-in default). I did not edit R-04's text. The skill says "A fix that changes a rule's text stops at that rule ... apply only the other lines the fix touches, and report the rule change as a proposal for the owner to decide." Status: open. The row describing it stays as R-04 now reads, so no row departs from its rule.
- The skill allows one round only ("There is no second round"), so rounds = [1]. checker_zero_errors_seen: step 3.3 read 0 errors after round 1. The skill's own stop is a single round, not a no-change round.
- The step-5 report.md write was refused by the harness, so the report goes back in the hand-back under REPORT.MD.
