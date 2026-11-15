# Runner notes (switch-base-3)

## Step 2
- Turn 1 sent the systems question alone, as the skill puts it before any other question.
- Turn 2 asked rows 5, 3, 4, 6 (most blocking first), four questions.
- Read docs.stripe.com/refunds and docs.stripe.com/api/idempotent_requests via WebFetch for the payment provider, the only system with docs. Three docs claims (C-14, C-15, C-16) come from the refunds page. The idempotency page settled nothing, because the agent never calls the payment provider; listed in the packet as read.

## Step 3.4
- First check: 0 errors, 0 breaks, so the decision turn carried no breaks; it carried the tool set (row 2 proposed), the claims that passed the decision filter (C-13 duplicate refund, C-10 cancel no answer, C-07 lookup no answer), the money mismatch (C-25), the follow-up no-answer case, the orders-per-conversation bound and the refund re-lookup outcomes. Eight questions, two turns of four.
- The two decision turns were dispatched in parallel (questions independent of each other). Their replies changed the model:
  - Cancel timeout: owner record says re-read, cancel once more if still open, report if shipped, hand off if re-read fails. Replaced my recommendation (hand off at once).
  - Follow-up: the record's tool confirmation changes "handoff timeout not retried" to "retry once; if it times out again, tell the customer to contact Harbor Goods support". Applied the later change.
  - Lookups: "Reads may be retried on timeout without limit". Applied to the first lookup as an unbounded loop. The owner's specific answers for the re-reads after an unanswered cancel or refund say "re-read fails ... hand off", so those re-reads hand off on one failure. What ends the unbounded loop, and whether re-reads may also be retried, is left as C-42 (missing, nobody) and an open question.
  - Refund re-lookup: failed or no refund -> hand off, "refund not confirmed yet"; the reason I map to "refund not issued" (C-39, spec only).
- After a second cancel call that leaves the order still open, I added the hand-off "cancellation unknown" (C-41, spec only): the owner bounded the cancel to "once more" but did not say what follows.
- The refund outcome "order not cancelled" (owner's tool change 2) is in the model only when the order system has not cancelled the order, which no path reaches once the cancel answered cancelled; its row of "What the agent does" stays for a coder.

## Step 4
- Finder dispatched with the shared header, the defect classes, the finding format and the faithfulness role, scoped to the whole spec; told to read nothing beyond the packet, its sources and the spec.
- Verifier dispatched with the adversarial brief on opus (the session model).
- Drops: F2 and F11. I read R-07, R-05 and SC-39 for F2, and C-33 and R-06 for F11, and agreed each refutes the finding.
- Kept against the verifier's verdict: F7 (Not real). The cited lines show other rows settle a shipped second cancel, but F7 is an Unclear finding about R-10's own sentence, which literally covered that case; I did not agree that the cited lines stop an owner from misreading R-10. F10 (Style only): a claim naming the wrong party is a misstatement, not a preference about phrasing; kept at Nit.
- Severity: F1 kept at the verifier's lower severity, Nit.
- Rule-text fixes (F1, F3, F4, F5, F7, F8, F12) went to the owner in one turn of four questions (turn 5). Accepted: R-05, R-13, R-14, R-10, R-12. Not accepted: the R-15 bound; the owner's record reply kept unlimited reads, so F4 stays open and R-15 is unchanged.
- Non-rule fixes applied directly: rows (F6, F8), claims C-11, C-16, C-17, C-38, new C-43, C-44, and the model for the different-amount refund on the lookup path, the no-orders setup, and the instead-or-as-well step.
- The skill allows no second round; what is left (F4) is open in the report.
- report.md: the harness refused the Write ("Subagents should return findings as text"); per PROMPT rule 17 the report goes back in the hand-back under REPORT.MD.
