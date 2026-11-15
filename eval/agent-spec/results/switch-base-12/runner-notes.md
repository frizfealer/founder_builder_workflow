# Runner notes (switch-base-12)

## Dispatch and reply handling

- Every stand-in reply arrived as an agent hand-back message, followed by a task notification carrying subagent_tokens, tool_uses and duration_ms. The notifications do not split input, output and cache-read tokens, so those are "n/r" in subagent-stats.md and null in trial.json.
- Grilling / grill-with-docs were not invoked: SKILL.md at 807d36e does not tell the runner to invoke them.
- The skill at this commit has no steps 3.8 or 3.9. The tool confirmation (row 2 was *proposed*) went out in the step-3.4 decision turn as log question 10.
- Step 3.4 used its two-turn maximum (log questions 10 to 17).

## How I read the stand-in's replies

- Q1 (systems): "No" plus the record's Systems table; I took the three systems from it, including the payment provider with docs at docs.stripe.com. I read docs.stripe.com/refunds and docs.stripe.com/api/idempotent_requests and settled C-17, C-18, C-19 from them.
- Q2-Q5: the record answered every question in more detail than my recommendations; claims quote record lines.
- The record had two internal contradictions: follow-up timeout ("handoff timeout not retried" vs "retry once; ... contact Harbor Goods support") and money timing ("money arrives in 5 to 10 business days" vs "promises nothing about when the money arrives"). Put both to the owner as Q11 and Q12; the replies quote "Confirmed, with four changes: ... 3. ... On timeout, retry once" and the "Yes to all" accepted round-3 Q1, so I took the later answers (D-04, D-05).
- Q10 (tools): "No" — the record's confirmed set has only three reasons and adds an OrderNotCancelled refund outcome and unlimited read retries. I dropped my proposed fourth reason and asked which existing reason applies (Q15: refund status unknown, accepted).
- Q13 (list no answer / not found): "No" because reads are retried without limit. I modelled a list call with no answer as resent with no limit, and kept an error outcome (spec only, C-06) so the owner's "re-read fails" answers have a case; C-07 (error at the start) is spec only.
- Q14 (bound on reads): rejected; the owner set no limit. Recorded as C-50 with "none: the owner set no limit"; it goes to the report as an open limit.
- Q17 (second cancel no answer; change after yes): "No" with the cancel re-read passages. I read it as: after the second unanswered cancel call the agent re-reads again (C-38, owner's words), and cancel calls stay bounded at two. What happens when that re-read shows the order still open is spec only (C-51), open in the report. Part (b), the change after the yes, got no passage that answers it; the agent's re-proposal is spec only (C-47), open in the report.

## Keep / drop decisions

- F1 kept, Important, open. The verifier refuted the error outcome itself: the owner's "re-read fails" answers only make sense if a failure other than a timeout exists. What stands is the message when the first list call fails. No turn was left to ask about it, so it is open.
- F2 kept at Nit, the verifier's severity, though its verdict was Not real. D-06 and C-50 refute the "no end" part. They do not cover what the customer hears, or a customer leaving, while reads repeat; the verifier named that part itself. Open.
- F3 kept and fixed. R-04's text went to the owner as a proposal, and the owner accepted it (log question 18, D-10). The model still offers the proposal again after a change. That step is allowed by the new text, but the owner never said it, so the report lists it as open.
- F4 kept at Nit despite Not real. R-13 says what the agent does, but the Gap class names "a case ... no row of 'What the agent does' covers, such as two requests in one message". A row was missing, so I added one. The case stays conversational in the model.
- F5 kept and fixed in model.py and the row. Neither fix changes a rule's text.
- F6 dropped. C-43 and the owner's "say outcome unknown ... hand off" support telling the state in every hand-off.
- F7 kept and fixed. The row and the model step no longer ask a question.
- F8 dropped. C-26 covers delivered.
- F9 dropped. C-17 (the Stripe docs) rules out a different refund destination.
- Only one round ran. SKILL.md 4.5 says "There is no second round", so round2 and round3 files do not exist.
- report.md: the Write tool refused it ("Subagents should return findings as text"). Rule 17 forbids writing it another way, so it goes back in the hand-back.
