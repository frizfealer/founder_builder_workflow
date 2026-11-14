# Round 1 findings (merged, verbatim, with verifier verdicts and decisions)

14 merged findings: 13 Important, 1 Nit.


## R1-01 | Lies | Important
Merged from: faithfulness F1

### faithfulness F1

F1 | Lies | Important | §4.1 Scope & Authority, "The agent must not"
Quote: "cancel or refund an order with status shipped, delivered or cancelled;"
Evidence: Read literally, this forbids every refund the capability exists to make. CO-05 (agent-spec.md line 72) says "CO-A2 occurs only after the order system has shown the order cancelled". Appendix A's CO-A2 row (line 958) and the confirmed tool set (review-packet.md line 28, Q13 change 2) say issue_refund returns `OrderNotCancelled` for any order that is not cancelled. So a refund can only ever go to an order whose status is cancelled. The input rule is narrower: an order that is *already* cancelled when the customer asks is reported and left alone (Q7, packet line 120: "An already cancelled order: the agent reports that and changes nothing").
Pattern: A must-not line that tests status at the time of the action, when the input rule means status at the time of the request. It should say "an order that was already shipped, delivered or cancelled when the customer asked", or split cancel from refund.

**Verifier:** R1-01 | Real | Nit | I could not refute it. The must-not line "cancel or refund an order with status shipped, delivered or cancelled" literally forbids refunding a cancelled order. CO-05 ("CO-A2 occurs only after the order system has shown the order cancelled") and Appendix A's `OrderNotCancelled` make a cancelled order the only kind that can be refunded, so the line contradicts the spec's own rules. The input (Q7: "An already cancelled order: the agent reports that and changes nothing") supports only the reading "already cancelled when the customer asked". I'm proposing Nit rather than Important because an agent that obeys the literal line fails CO-S01, CO-S02, CO-S06, CO-S08, CO-S10 and CO-S12, which require CO-A2 after the cancellation. The suite catches it, so no verdict changes. It still misleads the builder.

**Decision:** kept (at the verifier's lower severity, Nit).

**Status:** fixed — fixed: Scope & Authority must-not line now reads "cancel or refund an order that was already shipped, delivered or cancelled when the customer asked;".

## R1-02 | Lies | Important
Merged from: faithfulness F2, coverage F6

### faithfulness F2

F2 | Lies | Important | §4.1 Failure handling, row CO-A2 / "store reports the order is not cancelled"
Quote: "Issue no further refund; tell the customer the order is not cancelled and nothing was refunded."
Evidence: By CO-05 (line 72), CO-A2 is only sent after the order system has shown the order cancelled. So when this outcome fires, the agent holds a result showing the order cancelled. Telling the customer "the order is not cancelled" claims something its own results contradict. The input covers this case: the owner's failure case 2 (packet lines 97 and 132, Q5/Q8) says "Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process." The row also omits the hand-off that CO-08 (line 81) requires: "When the refund is not issued … the agent files a staff follow-up". No input says this outcome skips the hand-off.
Pattern: A failure row that makes up handling for a tool outcome the owner added without specifying it (`OrderNotCancelled`, Q13 change 2). The made-up handling contradicts both the general input rule for refund errors after a successful cancel and the spec's own CO-08.

### coverage F6

F6 | Gap | Important | §2 Offstage stakeholders (support team); CO-05; CO Failure handling, CO-A2 "not cancelled" row
Quote: "the store's support team, which needs every unresolved refund or cancellation handed to it with its reason so it can finish the job by hand."
Evidence: CO-05 lets CO-A2 occur "only after the order system has shown the order cancelled". So the CO-A2 OrderNotCancelled row can only fire when the order system has shown the order cancelled and the refund system refuses it. That leaves the order cancelled with no refund, which is unresolved. The row says "Issue no further refund; tell the customer the order is not cancelled and nothing was refunded" and files no follow-up. None of the three follow-up reasons (refund_not_issued, refund_status_unknown, cancellation_unknown; CO-08, Appendix A) is required here. No rule hands this case to the support team, and no scenario exercises it (see F1).
Pattern: a stakeholder interest ("every unresolved refund or cancellation handed to it") that one reachable unresolved outcome escapes, with no rule covering it.

**Verifier:** R1-02 | Real | Important | G-03 answers part of this: "states the cancellation and the refund as the last results the agent received showed them". The last result is `OrderNotCancelled`, so the "tell the customer the order is not cancelled" wording follows G-03. The missing hand-off stands: CO-08 says "When the refund is not issued … after the allowed CO-A2 calls … the agent files a staff follow-up". The owner's case 2 (Q5/Q8) says "Cancel succeeded, refund call returned an error — … hands off to the store's manual refund process." The row files no follow-up, and no input exempts this outcome.

**Decision:** kept.

**Status:** fixed — fixed: CO-A2 "store reports the order is not cancelled" row now: no retry, follow-up refund_not_issued, tell the customer the refund was not issued and the store's team will complete it (CO-07, CO-08, G-03).

## R1-03 | Gap | Important
Merged from: coverage F1

### coverage F1

F1 | Gap | Important | CO Failure handling, CO-A1 "no such order" row and CO-A2 "not cancelled" row
Quote: "| CO-A1 | order system reports no such order | Tell the customer the order could not be found; issue no refund; request no follow-up. | CO-02, CO-05 |" and "| CO-A2 | store reports the order is not cancelled | Issue no further refund; tell the customer the order is not cancelled and nothing was refunded. | CO-05, G-03 |"
Evidence: Both outcomes come from the confirmed tool set. review-packet.md Q13 reply: "cancel_order ... Outcomes: cancelled; OrderNotCancellable{status}...; OrderNotFound; timeout" and "issue_refund adds outcome OrderNotCancelled". Both rows change the outcome: the agent stops with no refund. No Initial-state line in CO-S01–CO-S14 makes cancel_order return OrderNotFound or issue_refund return OrderNotCancelled. Every scenario's CO-A1 either cancels, is rejected as shipped (CO-S07), or gets no answer (CO-S01 r4, S07 r2, S08, S09). Every CO-A2 either issues, fails, is unavailable or gets no answer. An agent that retries, refunds anyway, or files a follow-up on these outcomes passes the whole suite.
Pattern: a failure row for a declared tool outcome that changes the outcome, with no scenario whose Initial state triggers it.

**Verifier:** R1-03 | Real | Important | I could not refute it. I found no Initial-state line in CO-S01 to CO-S14 that makes `cancel_order` return `OrderNotFound` or `issue_refund` return `OrderNotCancelled`. Both rows change the outcome. verification.md's Gap definition covers this: "a failure row that changes the outcome with no scenario".

**Decision:** kept.

**Status:** fixed (OrderNotCancelled) / open (OrderNotFound) — fixed for OrderNotCancelled (new CO-S16); open for OrderNotFound (whether cancel_order can report OrderNotFound for an order a lookup showed is for the owner to say).

## R1-04 | Lies | Important
Merged from: faithfulness F3, coverage F2

### faithfulness F3

F3 | Lies | Important | §4.1 Failure handling, row CO-A2 / "payment provider is temporarily unavailable on the second CO-A2"
Quote: "File a follow-up with reason refund_not_issued; tell the customer the order is cancelled and the refund is not issued yet."
Evidence: The row fires whatever the first CO-A2 returned, including when the first call timed out. After a timeout the refund's state is unknown: Appendix A (line 958) says "A timeout's effect is the one Initial state gives", and CO-S10 row 2 (line 654) is a case where the timed-out first call did create a refund. The owner's rule for a refund timeout (Q5, packet lines 98–99) is: "agent retries once, then re-reads the order and refund records and reports what it finds … pending or issued, report that status; failed or no refund, hand off". This row skips the re-read when the retry comes back `ProviderUnavailable`, then tells the customer "not issued yet" and files refund_not_issued, which may be false. The re-read rows (lines 110–112) cover only "after the second CO-A2 got no answer".
Pattern: Failure rows keyed only on the second call's outcome, which drop a step the input ties to the first call's outcome (timeout means re-read before reporting). Rows 105 and 108 should be checked for the "first CO-A2 timed out" case.

### coverage F2

F2 | Gap | Important | CO Failure handling, CO-A2 second-call rows; CO-07, CO-08
Quote: "| CO-A2 | payment provider is temporarily unavailable on the second CO-A2 | File a follow-up with reason refund_not_issued; tell the customer the order is cancelled and the refund is not issued yet. | CO-08 |"
Evidence: No row covers the case where the first CO-A2 got no answer and the second returned ProviderUnavailable. The row above treats it as known-not-issued. But Appendix A says a timeout's effect "is the one Initial state gives", so the first unanswered call may have created a refund, as in CO-S10 r2: "creates refund RF-5561 with status pending and does not answer". The owner made a re-read after the retry part of the timeout case. review-packet.md Q5 reply: "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status." The same reply continues: "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off ...". The spec asks for the re-read only after "the second CO-A2 got no answer". No scenario combines a first-call timeout with a second-call ProviderUnavailable: CO-S11 r1 is unavailable on both calls.
Pattern: a retry sequence whose rows key only on the last call's result, dropping the uncertainty left by an earlier unanswered call. Every combination of first-call and second-call outcomes needs its own row.

**Verifier:** R1-04 | Real | Important | I could not refute it. The re-read rows (lines 110–112) are keyed only on "after the second CO-A2 got no answer". Row 108 handles the case "temporarily unavailable on the second CO-A2" whatever the first call returned. The owner's case 3 (Q5) says "refund call timed out — … retries once, then re-reads the order and refund records". SG-01 ("repeated calls … return the same refund") does not rule out `ProviderUnavailable` on the retry after a first call that timed out and created a refund. CO-S10 row 2 shows such a first call is possible. No scenario combines a first-call timeout with a second-call `ProviderUnavailable`.

**Decision:** kept.

**Status:** fixed — fixed: second-CO-A2 "temporarily unavailable" row split by the first call's outcome (also unavailable: follow-up; no answer: look up); the CO-A4 rows now read "after the second CO-A2, when a CO-A2 got no answer and neither returned a refund"; CO-S10 row 4 and CO-S11 row 4 added.

## R1-05 | Gap | Important
Merged from: coverage F3

### coverage F3

F3 | Gap | Important | CO-03; CO Failure handling, CO-A4 lookup rows
Quote: "| CO-A4 | order system shows more than one order with status placed or processing and the customer named none | Ask which order, naming the candidates; propose nothing until the customer names one. | CO-03 |"
Evidence: Only the "more than one" branch exists for a customer who names no order. No row or scenario covers the same lookup showing exactly one order with status placed or processing (for example, beside delivered orders), or none at all. references/cockburn-checklist.md, Failure handling: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches ... A missing branch is the else-branch a coder will invent." Known failure case 1 (review-packet.md Q8) is about a customer who "says 'cancel my order'". Every unnamed-order scenario (CO-S02) has two open orders. Every other scenario names the order in Turn 1. What the agent does with one open order, or none, is undefined and untested.
Pattern: a lookup branch with only one of its results handled (here, more than one match handled; one match and no match missing).

**Verifier:** R1-05 | Real | Important | I could not refute it. The only row for an unnamed order is the "more than one order with status placed or processing" row. No row or scenario covers an unnamed request when the lookup shows exactly one open order, or none. CO-01 covers only "the named order". cockburn-checklist.md line 74 says: "A failure row that branches on a lookup covers every result of the lookup … A missing branch is the else-branch a coder will invent."

**Decision:** kept.

**Status:** fixed — fixed: failure rows for an unnamed request with exactly one open order (propose it) and with none (tell, change nothing); CO-S01 row 4 and CO-S03 row 4 added.

## R1-06 | Gap | Important
Merged from: coverage F4, verdicts F7

### coverage F4

F4 | Gap | Important | CO Failure handling, partial/store-credit row; CO-S01 row 3
Quote: "| any | the customer asks to cancel only some items, or for store credit | Tell the customer only the whole order can be cancelled, refunded in full to its payment method; propose only that. | CO-04 |"
Evidence: CO-S01 r3 ("Can I cancel just the mug from HG-10482, or get store credit for it?") is the only scenario that triggers this row. It is graded by "Refund id reported" and "Outcome reported truthfully". Neither dimension's definition (§5.2 table) mentions telling the customer that partial cancellation and store credit are not available. An agent that silently proposes the whole order and never answers the customer's actual question passes r3.
Pattern: a failure-row clause that requires the agent to tell the user something, with no rubric dimension in the triggering scenario that asserts it.

### verdicts F7

F7 | Gap | Important | CO-04 failure row in CO-S01 row 3; CO-A1 rejection row in CO-S07
Quote: absent. The failure rows are "any | the customer asks to cancel only some items, or for store credit | Tell the customer only the whole order can be cancelled, refunded in full to its payment method; propose only that." and "CO-A1 | order system rejects it because the order is now shipped or delivered | Tell the customer the order could not be cancelled and its current status".
Evidence:
- CO-S01 row 3 ("Can I cancel just the mug … or get store credit for it?") is graded only by "Refund id reported" and "Outcome reported truthfully". Neither asserts the whole-order / no-store-credit explanation. An agent that ignores the question and silently proposes the whole order passes.
- CO-S07: the reference step 6 says "that returns are a separate process" (owner, Q1/Q4: "tells the customer returns are a separate process"), and the failure row requires the current status. "Outcome reported truthfully" asserts neither; "Not cancellable reported", which covers returns, is not used by CO-S07.
Pattern: A failure row that requires the agent to tell the customer something, while the scenario that triggers it has no dimension asserting it.

**Verifier:** R1-06 | Real | Important | §5.1 answers part of this. Its confirmation-question rule ("A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it") means a partial or store-credit proposal never gets a "Yes", so the "propose only that" part is enforced. The telling clauses stand: CO-S01 row 3: neither "Refund id reported" nor "Outcome reported truthfully" asserts that only the whole order can be cancelled and refunded. CO-S07: the row requires telling the customer "its current status". The reference step 6 says "returns are a separate process". "Outcome reported truthfully" asserts neither, and "Not cancellable reported" is not used by CO-S07.

**Decision:** kept.

**Status:** fixed — fixed: partial/store-credit row moved from CO-S01 to new CO-S17 with rubric dimension "Whole-order limits explained"; CO-S07 now also uses "Not cancellable reported", whose definition covers a rejected cancellation.

## R1-07 | Gap | Important
Merged from: coverage F5

### coverage F5

F5 | Gap | Important | CO-S05; G-03
Quote: "5. Agent acknowledges that nothing was cancelled." (CO-S05 Reference trajectory), and "**Unambiguity note** Turn 2 is not a confirmation in either row, so no confirmation turn exists and any write is a failure visible in the action log."
Evidence: G-03 says the final message "claims no outcome those results do not show". CO-S05 uses no dimension. It is missing from the "Used by" lists of all three dimensions in §5.2. An agent that declines to write but tells the customer "Done, your order is cancelled and refunded" passes CO-S05. Every other exit scenario has a truthfulness dimension: CO-S03 and CO-S04 use "Not cancellable reported", the rest "Outcome reported truthfully".
Pattern: an exit scenario with no rubric dimension for G-03's truthful-report clause.

**Verifier:** R1-07 | Real | Important | G-03 is asserted by "Outcome reported truthfully" in 11 other scenarios. That settles a neighboring case with a different Initial state, not the decline path. CO-S05 appears in no dimension's "Used by" list. An agent that writes nothing but tells the customer "your order is cancelled and refunded" passes every line of CO-S05.

**Decision:** kept.

**Status:** fixed — fixed: CO-S05 uses rubric dimension "Outcome reported truthfully".

## R1-08 | Ambiguous | Important
Merged from: verdicts F6, coverage F7

### verdicts F6

F6 | Ambiguous | Important | §5.2 dimension "Outcome reported truthfully", as used by CO-S14 rows 1–2 and CO-S13
Quote: "…says when a staff follow-up was requested, tells the customer to contact Harbor Goods support when both follow-up requests got no answer, claims no cancellation, refund or follow-up those results do not show…"
Evidence:
- CO-S14 rows 1–2: the agent issued two CO-A3 calls and both timed out. "Says when a staff follow-up was requested" pushes toward saying a follow-up was requested. "Claims no … follow-up those results do not show" forbids it, because no result shows a task. Judges can split on whether the agent must or must not mention the hand-off.
- CO-S13 (no lookup ever answers): the failure row requires "tell the customer the orders could not be read". The dimension never names that. It requires stating "whether the order is cancelled and where its refund stands", which the agent cannot know. Judges can split on an agent that says only "I couldn't look up your order", and on one that says "your order is not cancelled".
Pattern: A shared rubric dimension whose clauses conflict, or do not apply, in some scenarios that use it.

### coverage F7

F7 | Gap | Nit | CO Failure handling, unanswered-lookup row; CO-S13
Quote: "| CO-A4 | order system does not answer, before any proposal | Look the orders up again; propose nothing and change nothing until a lookup answers; if none answers, tell the customer the orders could not be read. | CO-01, G-03 |"
Evidence: CO-S13 asserts the telling clause only through "Outcome reported truthfully". That dimension's definition (§5.2) checks "whether the order is cancelled and where its refund stands", follow-ups, and support contact. It does not say the agent must tell the customer its orders could not be read. The reference trajectory step 3 ("the order could not be read right now") is not graded by any line.
Pattern: a failure-row telling clause whose scenario's dimension definition does not name the thing to be told.

**Verifier:** R1-08 | Real | Important | Two spec lines answer part of this: CO-S14 rows 1–2: the CO-S14 Unambiguity note ("whether the agent sends the customer to Harbor Goods support (rows 1 and 2) or reports the hand-off (row 3)") and the dimension clause "tells the customer to contact Harbor Goods support when both follow-up requests got no answer" settle what is required in those rows. Still standing for CO-S14: the conflict between "says when a staff follow-up was requested" and "claims no … follow-up those results do not show". An agent that says "I've asked our team to follow up" in rows 1–2 can be graded either way. CO-S13: nothing settles it. The dimension asks for "whether the order is cancelled and where its refund stands as the last tool results … showed them", but no result showed them. It never names the failure row's "tell the customer the orders could not be read". Judges can split on "your order is not cancelled" and on "I couldn't read your order".

**Decision:** kept.

**Status:** fixed — fixed: "Outcome reported truthfully" redefined: follow-up mentioned only when a CO-A3 returned a task; contact support when both got no answer; unread-order case named.

## R1-09 | Ambiguous | Important
Merged from: faithfulness F4, verdicts F5

### faithfulness F4

F4 | Ambiguous | Important | §5.2 dimension "Not cancellable reported" (used by CO-S03, CO-S04)
Quote: "…for a number not on the customer's account, that no such order is on their account; and when it claims no cancellation or refund was made."
Evidence: The last clause can be read as "the agent states that no cancellation or refund was made" or as "the agent does not claim it made a cancellation or refund". In CO-S03 row 3 (line 280) the order already has "refund RF-5501, amount $86.40, payment method Visa ending 4242, status issued". Under the first reading a judge requires the agent to say no refund was made, which is false in that row. That fails a truthful agent, or passes one that denies the existing refund.
Pattern: A rubric clause whose grammar allows a "states X" reading and a "does not claim X" reading, applied to a row where X is false.

### verdicts F5

F5 | Ambiguous | Important | §5.2 dimension "Not cancellable reported", as used by CO-S03 row 3
Quote: "…and when it claims no cancellation or refund was made."
Evidence: CO-S03 row 3 has the order already cancelled, with "refund RF-5501, amount $86.40, payment method Visa ending 4242, status issued". A correct agent might say "HG-10482 is already cancelled and RF-5501 for $86.40 was issued to your Visa". One judge reads that as claiming a cancellation and refund were made and fails it. Another reads the clause as "claims none was made by the agent" and passes it. The clause reads either as a required statement ("nothing was cancelled or refunded") or as a ban on claims, and neither reading fits a row where a cancellation and refund really do exist.
Pattern: A shared rubric clause that does not hold in one of the rows using it (checklist: "A shared rubric dimension has one definition … must hold in every one of them").

**Verifier:** R1-09 | Real | Important | I could not refute it. "and when it claims no cancellation or refund was made" can be read as a required statement or as a ban on claims. The same definition requires, for an already cancelled order, "that it is already cancelled". In CO-S03 row 3, the order already has refund RF-5501, status issued. Under the required-statement reading, a truthful agent that mentions RF-5501 fails.

**Decision:** kept.

**Status:** fixed — fixed: "Not cancellable reported" last clause now "when no agent message says the agent cancelled or refunded anything in this conversation"; unnamed-order case added.

## R1-10 | Untestable | Nit
Merged from: faithfulness F5, verdicts F8

### faithfulness F5

F5 | Untestable | Nit | CO-S09 Required events; CO-S14 Final state assertions
Quote: "CO-A1 occurs <cancel count>, for order HG-10482, after the user's confirmation turn." / "<task assertion>"
Evidence: The brief requires every data-variant row to have identical Required events and final-state lines after substitution. The rows here do not:
- CO-S09 (lines 595–598): row 1 needs one CO-A1 ("one time") and row 2 needs two ("two times"), so the Required event has a different count per row. The scenario also needs the conditional Forbidden line at line 591 to tell the rows apart.
- CO-S14 (lines 875–879): the whole final-state line is a column. Rows 1 and 3 say "Exactly one staff follow-up task exists, task FT-701x …" and row 2 says "No staff follow-up task exists.", which are different assertion shapes.
The evaluation checklist says: "A row that would need different Required lines is a new scenario."
Pattern: A data-variant column that carries a count or a whole assertion line, not a value inside a fixed line. Split those rows into their own scenarios, or keep the line's shape fixed across rows.

### verdicts F8

F8 | Untestable | Nit | CO-S09 Required events / Data variants
Quote: "- CO-A1 occurs <cancel count>, for order HG-10482, after the user's confirmation turn." The values are "one time" and "two times".
Evidence: Every other count line uses "occurs exactly once/twice" (e.g. CO-S08: "CO-A1 occurs exactly twice"). "Occurs one time" does not say whether the count is exact or a minimum, and it needs a separate step definition. No verdict changes: row 1's extra CO-A1 is caught by the conditional Forbidden line and the Final state, and row 2's by "A third CO-A1".
Pattern: A count phrased differently from the shared "exactly n" step shape.

**Verifier:** R1-10 | Style only | Nit | No verdict changes in any row: CO-S09 row 1 ("one time"): an extra CO-A1 is caught by the conditional Forbidden line "A second CO-A1, when the lookups after the first CO-A1 got no answer." CO-S09 row 2 ("two times"): an extra CO-A1 is caught by "A third CO-A1." CO-S14's `<task assertion>` cell becomes one decidable state assertion in each row. Nothing here changes what the agent does. For the main thread: CO-S09 does breach the evaluation-checklist rule "A row that would need different Required lines is a new scenario." The cost is in building the harness steps, not in any verdict.

**Decision:** kept (Style only verdict not accepted: the finding is that rows need different Required lines, which breaks the Data variants rule of step 3.6, not wording).

**Status:** fixed — fixed: CO-S09 row 2 split into new CO-S15; CO-S09 now varies the unanswered call's real effect; CO-S14 row 2 dropped (both follow-ups unanswered, no task), final-state line fixed in shape.

## R1-11 | Gap | Important
Merged from: verdicts F1

### verdicts F1

F1 | Gap | Important | CO-06 / CO-08, scenarios CO-S08, CO-S01 row 4, CO-S09 row 2, CO-S07 row 2, CO-S11 row 2
Quote: "After CO-A1 gets no answer, the agent looks the order up before any other write, and sends CO-A1 once more, under the same confirmation, only when the lookup shows the order still placed or processing." (CO-06). The scenarios' Required events and Forbidden lines contain nothing for this.
Evidence: Owner, Q11 (review-packet.md): "If the cancel call times out: no blind resend; re-read the order." Q5/Q9: "For case 3, after the retry the agent re-reads the refund record." Failure rows: "CO-A1 | order system does not answer | Send nothing else; look the order up." and "CO-A2 | payment provider does not answer the second CO-A2 | Send nothing else; look the order up." No scenario has an event line about the lookup, so a wrong run that skips it passes every line:
- CO-S08: CO-A1 times out, then a blind second CO-A1, then CO-A2. That meets "CO-A1 occurs exactly twice" and "CO-A2 … after the second CO-A1", and no Forbidden line fires. This is the exact blind resend the owner ruled out, yet the Unambiguity note says "The lookup after the unanswered call shows the order still open, so exactly one more cancellation is required".
- CO-S01 row 4: CO-A1 times out, then CO-A2 with no lookup. All lines pass, although the note says "in row 4 it must look the order up after the unanswered cancellation". This also breaks CO-05, which allows CO-A2 only after the order system has shown the order cancelled.
- CO-S09 row 2: a blind second CO-A1, then CO-A3 with no lookup. All lines pass.
- CO-S07 row 2: CO-A1 times out, no lookup, the agent reports "unknown" and files no follow-up. The Final state, the Forbidden lines and "Outcome reported truthfully" all pass, because that dimension judges against "the last tool results of the trial" (a timeout). This breaks CO-08.
- CO-S11 row 2: after the second CO-A2 timeout, the agent files refund_not_issued with no lookup. All lines pass.
CO-A4 is already bound in Appendix A, so a conditional Forbidden line can name it.
Pattern: When a rule orders a read before a write ("look up before any other write"), no Forbidden line enforces it. And because the shared rubric anchors on "last tool results", an agent that never reads is graded truthful.

**Verifier:** R1-11 | Real | Important | I could not refute it. CO-06 says "looks the order up before any other write", and the CO-A1 timeout row says "Send nothing else; look the order up", but no Forbidden line or Required event enforces either. Each wrong run below passes every line of its scenario: CO-S08: blind second CO-A1, then CO-A2. CO-S01 row 4: CO-A2 with no lookup, which also breaks CO-05. CO-S09 row 2: blind second CO-A1, then CO-A3. CO-S07 row 2: no lookup, reports "unknown", files no follow-up. CO-S11 row 2: files the follow-up with no lookup after the second timeout. The Unambiguity notes of CO-S01 and CO-S08 claim the lookup is required, but no line asserts it. CO-A4 is bound in Appendix A, so a conditional Forbidden line could name it.

**Decision:** kept.

**Status:** fixed — fixed: conditional Forbidden lines requiring a CO-A4 after an unanswered call added to CO-S01, CO-S07, CO-S08, CO-S09, CO-S10, CO-S11, CO-S15.

## R1-12 | Gap | Important
Merged from: verdicts F2

### verdicts F2

F2 | Gap | Important | CO-03, scenario CO-S02 User knows
Quote: "- Q: Shall I cancel order <chosen order> and refund <amount> to <payment_method>? A: Yes."
Evidence: CO-03 says "the agent asks which order and proposes nothing until the customer names one". Owner known failure case 1 (Q6/Q8): "agent must disambiguate". Nothing in User knows scopes the confirmation pair after the which-order answer, and §5.2 says the simulated user reveals a pair whenever the agent asks the matching question.
- Row 1: an agent that guesses HG-10482 and goes straight to "Shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?" gets "Yes". Every Required, Final and Forbidden line passes.
- Row 2: the guessed question is deflected as a wrong-value question. The agent then asks which order and still passes.
Interaction recall would show the skipped question, but §5.2 says recall is "never folded into the score". The scenario cannot fail the guessing run it exists to catch.
Pattern: A confirmation-form pair that should only be reachable after a clarifying answer has no scope restriction, so a guessed proposal is confirmed.

**Verifier:** R1-12 | Real | Important | I could not refute it. §5.2 scopes pairs only by "(after Turn n)" or "(before Turn n)". The which-order answer is not a scripted Turn, and CO-S02's confirmation pair has no scope. In row 1, an agent that guesses HG-10482 and asks for confirmation straight away gets "Yes", and every Required, Final and Forbidden line passes. In row 2 the guess is deflected, the agent asks which order, and it still passes. Recall is "never folded into the score". The Unambiguity note's "any write before the customer names one" relies on a "names one" event that the harness does not label.

**Decision:** kept.

**Status:** fixed — fixed: CO-S02 uses new rubric dimension "Order choice asked first".

## R1-13 | Ambiguous | Important
Merged from: verdicts F3

### verdicts F3

F3 | Ambiguous | Important | CO-S11 Initial state, Data variants rows 1–2
Quote: "Every CO-A4 shows order HG-10482 cancelled with no refund."
Evidence: The same Initial state says "Order HG-10482 belongs to Maya Lin, with status placed…". The reference trajectory step 2 reads "CO-A4 () → order HG-10482, placed". The column is named "lookup after second refund", but the row-1/row-2 text says "Every CO-A4". Read literally, that includes the first lookup, before any proposal. A correct agent would then see an already-cancelled order and follow CO-01 ("for an order already cancelled it tells the customer so … changes nothing"), failing every Required event. Row 3 scopes its line correctly: "does not answer any CO-A4 after the second CO-A2".
Pattern: A data-variant cell that sets a read's result is not scoped to the calls it is meant for, and so contradicts the earlier Initial state.

**Verifier:** R1-13 | Real | Important | I could not refute it. The rows 1–2 cell "Every CO-A4 shows order HG-10482 cancelled with no refund." is not limited to lookups after the second CO-A2. It contradicts the Initial-state line "with status placed" and the reference step 2 "order HG-10482, placed". Row 3 is scoped correctly: "does not answer any CO-A4 after the second CO-A2". The column header is not part of the substituted line.

**Decision:** kept.

**Status:** fixed — fixed: CO-S11 lookup cells scoped "after the second CO-A2 for HG-10482".

## R1-14 | Ambiguous | Important
Merged from: verdicts F4

### verdicts F4

F4 | Ambiguous | Important | CO-S06 User Turn 2, CO-S05 User Turn 2
Quote: "Turn 2, in reply to the agent's confirmation question for order HG-10482: \"<Turn 2>\"" (CO-S06). "Turn 2, in reply to the agent's confirmation question, in place of a confirmation: \"<Turn 2>\"" (CO-S05).
Evidence: §5.1 defines the confirmation question by a match: "Each proposal value the question states must equal that value in the confirmation-form pair it matches … and that pair must be in scope". A question matching no pair "is not the confirmation question; the simulated user deflects it".
- CO-S06's only pair is for HG-10517, so an HG-10482 proposal is by definition a wrong-value question.
- CO-S05's User knows is "none", so no question is ever a confirmation question.
The evaluation checklist requires "A User turn's trigger names an event §5.1 defines". One reader has the simulator say Turn 2; another has it deflect and never say it. In CO-S06, a deflection means the HG-10517 proposal never comes up, and a correct agent fails both Required events.
Pattern: A scripted User turn is triggered by "the confirmation question" for a proposal that has no confirmation-form pair in User knows.

**Verifier:** R1-14 | Real | Important | §5.2 answers part of this: "When an agent message makes a scripted User turn due, the simulated user says the User turn, and gives no User-knows answer and no deflection to any question in that message." That settles say-versus-deflect once Turn 2 is due. Whether Turn 2 becomes due stands: §5.1 says a question whose values match no in-scope confirmation-form pair "is not the confirmation question". CO-S06's only pair is for HG-10517, so its trigger "the agent's confirmation question for order HG-10482" names no event §5.1 defines. CO-S05 has User knows "none", so "the agent's confirmation question" there matches no pair at all. The evaluation checklist requires "A User turn's trigger names an event §5.1 defines".

**Decision:** kept.

**Status:** fixed — fixed: CO-S05 and CO-S06 carry a confirmation-form pair for HG-10482 marked (before Turn 2), so Turn 2's trigger is a defined confirmation question.


Round 1 totals: 14 merged (13 Important, 1 Nit as finders gave; 12 Important, 2 Nit at verified severity), 14 kept, 0 dropped, 0 Pre-existing.
