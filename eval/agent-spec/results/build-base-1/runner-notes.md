# Runner notes (build-base-1)

## Writing (steps 1-3)

- The packet had to be read before step 1 (PROMPT rule 4), so my "own questions" in interview-replay.md and my own tool proposal were not formed blind; noted in interview-replay.md.
- One capability, CO (cancel an order and refund it). Rules: G-01..G-04, CO-01..CO-11 (11 capability rules, above the checklist's 3-9 guideline; kept because each maps to a distinct user-stated branch).
- CO-A4 (look-up) is bound to list_orders() because failure rows and Forbidden lines name it (look-up before refund after an unanswered cancel; look-up before reporting after an unanswered second refund).
- Derived (not in the recorded answers), so likely open questions: what happens after a second cancel call also times out; how many read retries before "re-read fails" given reads are unbounded; at most two calls per action per order (G-04) as the reading of "one retry".
- CO-S13 row 3 (OrderNotCancelled after the store reported the order cancelled) is an inconsistent-store case; included only because the user added that outcome and step 3.6 needs a scenario for each outcome-changing failure row.
- 3.9: CO-S08 merged into CO-S01 (row 3); CO-S09 merged into CO-S06 (row 4). Dropped rows: CO-S08 row 2 (placed order, cancel unanswered but cancelled, refund issued; differed from the kept row only in values/wording), CO-S09 row 2 (delivered status discovered by the look-up after an unanswered cancel; differed from row 4 only in value). CO-S02/CO-S05 kept apart: different User blocks (clarify pair vs scripted change-of-mind turn) and different final-state lines. CO-S01 keeps Suite regression although its row 3 is a recovery case (lowest id's suite kept).

## Dispatch

- Round 1 finders dispatched together, in parallel, model opus, general-purpose.
- Rounds 2 and 3 finders were likewise dispatched together; each round's verifier after all three finders returned.

## Keep/drop reasons

- R1-04, R1-13, R2-01 (Nits rated Style only) kept: each states a content mismatch the checklists name (row-1 literal in a note; a trigger not defined by §5.1; a tool result Appendix A cannot return), not wording preference.
- R1-06 kept against a Not real verdict: the cited CO-S04 decline answers the whole-order question in a partial request, not a refusal of the full proposal.
- R2-02 dropped (precision not scored by design); R3-02, the same pattern, kept in round 3 because the verifier showed an agent that refuses to propose the only open order fails nothing, which R2-02's refutation did not answer. Recorded as an inconsistency between rounds.
- R1-08, R1-09, R2-07, R3-03, R3-04 dropped: refuting clauses read and agreed (quoted in the round files).
- R3-01 and R3-05 left open: R3-01 needs a rule change (CO-01 vs CO-09); R3-05 is §5.1 template text, which step 4 does not edit.
- R1-01 fix removed two impossible rows; this leaves the CO-A1 OrderNotFound and CO-A2 OrderNotCancelled failure rows and CO-10's "no such order" clause without a scenario. Reported as a proposed rule change, not edited.

## Timing

- Step 3.8's own-proposal snapshot is run-build-base-1/agent-spec-3.8-own-proposal.md.
- wall_clock_s runs from step 1 start (03:20:29Z) to step 5 end.
