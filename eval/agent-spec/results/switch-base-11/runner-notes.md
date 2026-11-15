# Runner notes (switch-base-11)

## Step 2
- Turn 1 asked only the systems question, as the skill requires it first. The stand-in rejected my two-system recommendation; the record names three systems (order system, payment provider behind it with Stripe docs, staff task queue).
- Turns 2-4 asked rows 1, 3, 4, 5, then limits, money mismatch, handoff, multiple orders, row 6, and three outcomes the record named but did not handle (order not cancelled, order not found) plus the success message.
- Q6 (bound on reads): owner's record says "without limit"; logged as owner decision D-06 and left as an open limit. Not re-asked in step 3.4: the owner already answered it, and asking again would only repeat the same record line.
- The skill no longer has a step 3.8/3.9 (the run prompt names them); the tool confirmation ran inside step 3.4 (Q16), so run.log has 3.4 and 3.5 timestamps instead.
- Stripe docs read for the payment provider (WebFetch, docs.stripe.com/refunds). C-51 (expired or cancelled cards usually reach the replacement card) sits beside the owner's "terminal = card closed or expired"; I did not put it to the owner because the agent reacts only to what the refund call answers, so neither answer changes a model step (decision filter, third test).

## Step 3
- Interpretation: after a refund call with no answer, the agent retries once and then always re-reads the refund, whatever the retry answered (the record: "after the retry the agent re-reads the refund record"). The model follows that literally.
- Interpretation: a transient error followed by a timeout on the second call goes to the refund re-read too (record does not cover it; model says re-read).
- First check run: 0 errors, one no-step break (second cancel unanswered, order still open); put to the owner as Q14 in step 3.4.
- Two of my own model rule bugs fixed before the first --write (R-02 fired when the list failed; R-10 required one specific handoff reason).

## Step 4
- Round 1 finder dispatched 14:50:04Z, returned 14:53:32Z; verifier dispatched 14:53:32Z, returned 14:56:13Z. All task notifications arrived; none reported the in/out/cache-read split.
- Drops: F2 (I agree with the verifier: "get a confirmation naming the order number" is the owner's line, and R-04 restates it for the two-order case), F4 (Q16 confirmed the read can fail and Q10 delegated derived cases), F6 (Style only; the body defines the case in the next sentence).
- F3 fix added rows for conversation cases, with no rule text change, so no owner turn in 4.5. The rows' wording for a yes with a change is mine, derived from R-03/R-04/R-05; listed as an open question in the report.
- After the 4.5 fix I updated SC-46's "Why not a path" line, since the model now has a step for a yes with a change; the checker reread 0 errors and round1/ was re-copied after it.
- report.md: the harness refused the Write for a subagent; the text goes back in the hand-back under REPORT.MD.
