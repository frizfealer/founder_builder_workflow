# Runner notes, switch-base-8

- Step 1: one input, product-idea.md. Row 2 marked proposed. SKILL.md at 807d36e does not say to invoke grilling, so it was not invoked.
- Turn 1: systems question alone, as the skill says it comes before any other question.
- Turn 2 (Q2-Q5) and turn 3 (Q6-Q9) covered rows 1, 3, 4, 5 and 6. The stand-in answered Q7 and Q8 by stand-in default.
- Q2's recommendation (a staff task for a shipped order) was not taken: the owner's record says the agent changes nothing; the spec follows the record.
- Turn 4 (step 3.4, Q10-Q13): the owner's tool confirmation came "with four changes": cancel idempotent with new outcomes, refund adds OrderNotCancelled, staff request idempotent and retried once (this supersedes the earlier "handoff timeout not retried"), reads retried without limit. C-15 was rewritten to the newer statement.
- Q11's reply replaced my recommendation with the owner's own policy (re-read after a cancel timeout); applied as R-08.
- Turn 5 (step 3.4, second and last turn, Q14-Q17): Q14 (what ends a read that keeps timing out) got the owner's restatement "without limit"; no bound applied; it stays an open question. Q15-Q17 accepted by stand-in default.
- Read errors (not timeouts) are a spec-only claim (C-08); what the agent does when the first order list read fails with an error is C-43, missing, nobody; R-15 states my handling and the report lists it as open.
- Claims put to the owner under the decision filter: C-10 and C-14 (2).
- The model treats a timed-out read as a loop back to the same state, so unlimited read retries keep the model finite.
- A discard redirect of one check run went to /tmp/x (output only, no content of the trial); noted for integrity.
- Round 1: kept F1, F2, F4, F5 (at Nit, the verifier's lower severity) and F7. Dropped F3: Style only, and I agree, because the skill allows the accepted question as the quote. Dropped F6: Not real, and I agree, because R-12's own sentence says which statuses "made" covers. Dropped F8: Not real, and I agree, because C-19 and C-27 rule out a different payment method.
- Step 4.5 fixes: three rule-text changes (R-10, R-13, R-15) and one sentence kept (R-15, failed first read) went to the owner in one turn (Q18 to Q21), and all four were accepted by stand-in default. Rows, claims, decisions and the model were changed alongside. The F7 rows for several orders, a different order named before the yes, out-of-policy requests and no open order are not model steps; conversational scenarios cover them.
- An error of mine: one append to scenarios.md opened the file for writing before reading it, which truncated it. I rebuilt it from derive.txt with fill_scenarios.py, then SC-46/47, then SC-48 to SC-51 (logged in run.log). The skill's scripts had no errors.
- The harness refused the write of report.md ("Subagents should return findings as text"). Per PROMPT rule 17, the report text goes in the hand-back under REPORT.MD.
- Q2's recommendation (a staff task for a shipped order) and Q11's recommendation were both replaced by the owner's record. Neither counts as an accepted default.
