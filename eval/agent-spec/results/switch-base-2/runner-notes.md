# Runner notes (switch-base-2)

## Interview and decision turns
- Grilling / grill-with-docs: the skill at e8ed321 does not tell the runner to invoke them, so they were not used.
- Turn 1 asked the systems question alone, as the skill's first question; turns 2 and 3 asked the gaps of rows 1 and 3 to 6 (4 questions each).
- Docs: the payment provider has docs (docs.stripe.com). I read /refunds and /api/idempotent_requests and settled the provider claims C-31 to C-34 from them. The order system and staff task queue have no docs.
- Decision turn 1 (step 3.4) carried the tool confirmation (row 2 was proposed), two no-step breaks (listing no answer; read after unanswered cancel shows the order still open — the second was hidden behind the first in the checker's single no-step key, found by reading the model) and the C-24 claim (second refund call) behind the R-05 break.
- Decision turn 2 carried the "reads retried without limit" limit, two new no-step cases introduced by the owner's turn-1 answers (cancel answers "order not found"; second cancel unanswered with the order still open), and the R-11 vs R-09 disagreement the checker found.
- The stand-in answered the read-limit question from the record ("Reads may be retried on timeout without limit"), so the limit stays none: C-37's "what ends it" says nothing ends it but the customer leaving. That is an open question for the report; the skill allows at most two decision turns.
- Reconciling two answers: Q11 accepted "tells the customer it cannot see their orders right now" for a listing with no answer, while Q10/Q11 also quote "Reads may be retried on timeout without limit". I modelled a listing with no answer as retried and applied the Q11 handling to a listing that answers an error (C-16 adds "answers an error" as a spec-only read outcome; C-41 says "When listing the orders fails"). The same split is used for "re-read fails" (error) vs a re-read timeout (retried). A finder may flag this.
- A cancel answered "not cancellable" (the race) does not trigger a staff task: the owner said report truthfully and issue no refund call; I read "a cancel ... call fails" in the accepted Q7 recommendation as no answer or an unknown result, not a definite refusal.
- The hand-off reason "refund amount differs" was added by me in the tool turn; the owner's reply "Confirmed, with four changes" did not object, recorded as proposed, accepted (C-43).
- issue_refund's "OrderNotCancelled" outcome is recorded in C-19 but has no model step: the agent sends the refund call only after the order system shows the order cancelled, so the model never reaches it.

## Subagent notifications
- Each stand-in's report arrived as a hand-back message, followed by a task notification carrying subagent_tokens, tool_uses and duration_ms. No input/output/cache split was reported.

## Round 1 keep/drop
- Dropped F6, F9, F10 after reading each verifier-quoted line myself (D-09; R-05 with R-03; R-01 and R-09's paired "fails" / "no answer" sentences). Reasons are in round1-findings.md.
- F3 kept at the verifier's lower severity (Nit). F7 kept only for its "delivered" part; the returns-wording part is refuted by the race answer.
- The step-4.5 owner turn held 4 rule-change questions (R-12, R-08, R-02, fifth hand-off reason). F7's R-07 change did not fit, so it stays open as a proposal.
- F1 and F4(b) were fixed without a rule-text change (a new row and a model step; a reason mapping), so they did not go to the owner.
- Timing: the verifier was dispatched about 35 s after the finder returned; the step-4.5 owner turn right after the verifier returned.
- report.md: the harness refused the write; the report goes back in the hand-back.
