# Runner notes (switch-base-7)

## Interview
- Step 2 took three stand-in turns (questions 1 to 9). The systems question went alone in turn 1, as the skill asks it before any other.
- The skill as of 807d36e does not mention grilling or grill-with-docs; none was invoked.
- Q8 (what the customer is told after the refund): the record overrode my recommendation ("The agent promises nothing about when the money arrives."); I dropped the 5-10 business days line.
- Q7 and Q9 replies came back as "stand-in default" with extra record passages. One of them carried a contradiction: "handoff timeout not retried" against "On timeout, retry once; ...". I put it to the owner in the step-3.4 turn (Q12); the record resolved it as retry once.
- Stripe docs were read for the payment provider (refunds, idempotent requests). The agent never calls the provider directly, so only C-45 to C-47 are docs claims.

## Decision turn (3.4)
- Breaks after the first check: 0, so the decision turn held only the tool set, the money mismatch, the follow-up contradiction, and the claims under the decision filter (C-16, C-24, C-27, C-29, C-37, C-43, C-44): 7 claims put, which is under the limit of 10.
- Two turns (turn 4: Q10 to Q13; turn 5: Q14 and Q15) went out in parallel, since their questions did not depend on each other. Turn 5's stand-in returned first.
- Turn 4's stand-in prefixed each question with "Question N:". The raw JSON keeps the prefix; the interview log removes it so that the question matches what was sent.
- Q10 came back confirmed, with four changes: cancel is idempotent and has the outcomes NotCancellable{status} and NotFound; refund adds an OrderNotCancelled outcome; follow-up retries once; reads may be retried without limit. The NotFound and OrderNotCancelled outcomes have no recorded handling, so I gave them spec-only handling (C-51, C-52). The read-retry limit was set to none, and no third decision turn was allowed to ask what ends it, so it stays an open question (C-50).

## Round 1 keep/drop
- F3 dropped: I read C-46 (Stripe: refunds go only to the original payment method) and agree. The confirmed method is the order's own, so a refund cannot name a different one.
- F7 dropped: the replies read "Yes, I accept your recommendation."; answered_by is an eval field, not the owner's words.
- F6 and F8 got Style only verdicts on Nits. I kept both, because neither is a phrasing preference: F6 is claims saying more than their quote cells (the skill's one-passage rule), and F8 is a definition placed after the term's first use. Both fixes were cheap.
- F1 stays open: the rule change was put to the owner (Q16), and the record kept "without limit". Per the skill, a rejected or unanswered rule change stays a proposal.
- F2's row fix needed no change to the rule text (R-08 already said to look up after a time-out). The R-08 "at most twice" sentence was a rule change; the owner accepted it in Q17, logged as D-08.
- F4 rows for two orders in one message and for an order after a case ends have no step of their own in the model; the model docstring calls them new runs.

## Timing
- The finder and the verifier ran one after the other; the stand-in turn 6 ran while I applied the non-rule fixes.
- The skill (807d36e) allows one verification round ("There is no second round"), so round 1 was the last; no round2/round3 files.
- The report.md write was refused by the harness (subagent report-file guard); the report text goes in the hand-back.
