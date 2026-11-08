# Round 2 findings (merged), with verifier verdicts

Count: 11 merged findings from 14 finder findings plus 1 'Also' (faithfulness 2, verdicts/Codex 6, coverage 6+1). Kept 10: 4 Important, 6 Nit. Dropped 1 (R2-9).

Verifier verdict columns: A, B, C (each Real / Not real / Style only, with severity). Kept when at least two say Real; severity is the majority.

| Id | Verifier A | Verifier B | Verifier C | Kept/dropped | Severity | Disposition | Quotes a line round 1 changed? |
|---|---|---|---|---|---|---|---|
| R2-1 | Real, Important | Real, Important | Real, Important | kept | Important | fixed | yes (CO-S25, CO-S26 new in round 1) |
| R2-2 | Real, Nit | Real, Nit | Real, Important | kept | Nit | fixed | yes (dimension row edited in round 1) |
| R2-3 | Real, Important | Real, Important | Real, Important | kept | Important | open (only the user can decide) | yes (failure row new in round 1) |
| R2-4 | Real, Important | Real, Important | Real, Important | kept | Important | fixed in failure rows; CO-02 rule change proposed, open | yes (CO-02 clause added in round 1) |
| R2-5 | Real, Nit | Real, Important | Real, Nit | kept | Nit | open (CO-02 rule change proposed) | yes (CO-02 clause added in round 1) |
| R2-6 | Real, Nit | Real, Nit | Real, Nit | kept | Nit | fixed | yes (failure row new in round 1; pattern also in two unchanged rows) |
| R2-7 | Real, Nit | Real, Nit | Real, Nit | kept | Nit | fixed | yes (failure row new in round 1) |
| R2-8 | Not real, Nit | Real, Important | Real, Nit | kept | Nit | fixed | partly (CO-S29 new in round 1; same gap in unchanged CO-S05/06/07/10) |
| R2-9 | Not real, Nit | Not real, Nit | Not real, Nit | dropped | - | - | yes (CO-03 sentence added in round 1) |
| R2-10 | Real, Important | Real, Important | Real, Important | kept | Important | fixed | yes (dimension row edited in round 1) |
| R2-11 | Real, Nit | Real, Nit | Real, Nit | kept | Nit | fixed | no (CO-S17 step 6 unchanged in round 1; a residue of round 1's Appendix A edit) |

## Fixes and reasons

- R2-1 CO-S25/CO-S26 did not require the lookup after the unanswered CO-A2: added "Fewer than one CO-A1 after the second CO-A2." (CO-S25) and "Fewer than one CO-A1 after the first CO-A2." (CO-S26).
- R2-2 "Order not cancelled reported" dropped "could not be found" for CO-S24: CO-S24 now uses its own dimension "Order not found at cancellation reported"; "Order not cancelled reported" is CO-S25 only.
- R2-3 "not cancelled" after the second unanswered CO-A2 although a late effect is possible: stands as an open question for the user (the inputs decide only the first timeout; changing it changes CO-07).
- R2-4 "names no order" undefined in CO-02: the two failure rows now say "has not said which order they mean", matching the sibling row; the CO-02 rule text change is proposed to the user, not applied.
- R2-5 CO-02 "may propose" vs failure row "Propose that order.": rule change ("proposes") proposed to the user, not applied.
- R2-6 "a lookup did not answer" rows overlapped retried lookups: the three such conditions now read "no lookup ... answered (the agent may repeat the lookup first)".
- R2-7 none-open row misdescribed a customer with no orders: reason now "because none is placed or processing", and returns are mentioned only when an order has shipped or been delivered.
- R2-8 no lookup guard for state-dependent replies with no commit call: "Fewer than one CO-A1." added to CO-S05, CO-S06, CO-S07, CO-S10, CO-S29.
- R2-10 "Refund not issued reported" accepted "not confirmed yet" for known failures: restored to "has not been issued" for CO-S17, CO-S18, CO-S22; CO-S20 now uses "Refund not confirmed reported".
- R2-11 reference trajectories carried "card closed" the tool no longer returns: removed from CO-S17, CO-S22, CO-S23.

Proposed rule change for the user (R2-4, R2-5), not applied:

- Before: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order. When more than one has, the agent asks which and proposes nothing until the customer names one."
- After: "When the customer has not said which order they mean, by number or otherwise, and exactly one of the customer's orders has status placed or processing, the agent proposes that order. When more than one has, the agent asks which and proposes nothing until the customer names one."

## Merged findings, verbatim (as sent to the verifiers)

R2-1 | Gap | Important | CO-S25 and CO-S26, Expected / Forbidden
Quote: "absent" (CO-S25's only lookup-ordering line is "- A second CO-A2 before a CO-A1 made after the first CO-A2."; CO-S26 has no lookup-ordering line)
Evidence: Failure row "CO-A2 | the order system did not answer a CO-A2 | Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it; then act on the row below that matches the lookup's result." and the rows after it make the reported outcome depend on a lookup after the unanswered CO-A2; G-03 requires "the outcome is unknown" when the agent cannot tell. An agent that skips the lookup after the second unanswered CO-A2 (CO-S25) or after the unanswered CO-A2 (CO-S26) and reports "not cancelled" / "shipped" makes the same calls, leaves the same state, and passes the rubric. Both reference trajectories contain the lookup (CO-S25 step 8, CO-S26 step 6) and both Unambiguity notes rely on it, but no line requires it. CO-S15 has "CO-A4 before a CO-A1 made after the second CO-A2"; CO-S19's note says "ending without that lookup ... fails in the action log".
Pattern: An outcome message that is truthful only after a lookup made after an unanswered action, in a scenario with no Required or Forbidden line that requires that lookup.
(Reported by three finders: faithfulness F1, coverage F2, verdicts F2.)

R2-2 | Gap | Nit (one finder: Important) | Evaluation row "Order not cancelled reported" (CO-S24)
Quote: "| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |"
Evidence: Failure row "CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; make no CO-A3 and no further CO-A2." (agent-spec.md line 101) and CO-S24 reference step 6 still require "could not be found". The round-1 edit dropped it from the dimension and from CO-S24's Unambiguity note to share the dimension with CO-S25, so no scenario checks the not-found part.
Pattern: A shared rubric dimension broadened for one scenario drops a message clause another scenario's failure row still requires.
(Reported by three finders: faithfulness F2, coverage F6, verdicts F5.)

R2-3 | Gap | Important | failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing" (and CO-S25)
Quote: "| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. | CO-06, CO-07, G-03 |"
Evidence: Appendix B SG-04 (agent-spec.md line 1862) cites "A second cancellation call that reaches the order system after a first, unanswered one took effect late", and Appendix A CO-A2 (line 1842) "A timeout changes the order or not as Initial state says" — so the spec allows an unanswered CO-A2 to take effect after a lookup showed the order open. After the second CO-A2 there is no resend and no handoff; a late effect leaves the order cancelled with no refund and no staff task, while the customer was told it was not cancelled. Review packet round 3 Q4 covers only the first cancel timeout ("send the cancel once more"); the inputs never decide this branch.
Pattern: A terminal "not done" outcome stated after an unanswered call the spec itself says may take effect late, with no handoff or caveat.
(Coverage F1.)

R2-4 | Ambiguous | Important | CO-02 (and failure row "the customer named no order, and exactly one ...")
Quote: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order."
Evidence: "names no order" is undefined. The rule title is "by number" and its last clause says "names an order number"; the neighbouring failure row (agent-spec.md line 90) uses "has not said which one they mean"; CO-S02 rows 2 and 3 count naming by item or placed date as saying which. A customer who says "cancel my blanket order" when the blanket order is delivered and the candle order is the only open one: by-number reading, propose the candle order; by-description reading, apply CO-01 and propose nothing. This is known failure case 1, "Wrong order cancelled" (review-packet.md, round 2 Q4). The next clause "When more than one has, the agent asks which" also lost the qualifier "and the customer has not said which one they mean".
Pattern: A new condition term that differs from the term sibling rows use, with no definition.
(Coverage F3.)

R2-5 | Ambiguous | Nit | CO-02 against failure row "the customer named no order, and exactly one ..."
Quote: "the agent may propose that order."
Evidence: The failure row says "Propose that order." and CO-S28 requires CO-A2 and CO-A3 with only the full-proposal User-knows pair. Under "may", an agent that asks which order instead is compliant, but CO-S28 can fail it.
Pattern: A rule that permits ("may") while its failure row and scenario require the action.
(Coverage F4.)

R2-6 | Ambiguous | Nit | failure row "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
Quote: "| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | Tell the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; make no further CO-A2 and no CO-A3; make CO-A4 with reason cancellation unknown. | CO-07, G-03 |"
Evidence: Review packet tool-confirmation change 4: "Reads may be retried on timeout without limit"; CO-06 "lookups are not limited". This row fires on any single unanswered lookup. An agent that retries the lookup and then sees the order placed or processing matches both this row (mandatory CO-A4) and the "still placed or processing" rows; CO-07 allows CO-A4 only when the agent cannot tell. The rows never say whether to retry the lookup first.
Pattern: A failure row triggered by "a lookup did not answer" when lookups are retryable, overlapping rows triggered by a later lookup's result.
(Coverage F5.)

R2-7 | Gap | Nit | failure row "the customer named no order, and none of the customer's orders has status placed or processing"
Quote: "| any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing. | CO-01, CO-02 |"
Evidence: The row also matches a signed-in customer with no orders at all, where "because each has shipped, been delivered or been cancelled" is false. No row covers a customer with no orders.
Pattern: A failure condition that includes an empty case its prescribed message misdescribes.
(Coverage "Also".)

R2-8 | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29, Expected / Forbidden
Quote: "absent"
Evidence: CO-01: "The agent proposes cancelling an order only after a lookup shows it with status placed or processing ... When no lookup of the customer's orders has answered, it proposes nothing." The Required and Forbidden blocks of these scenarios (agent-spec.md 693-703, 924-937, 1511-1522, 1568-1578, 1624-1638, 1686-1699, 1742-1753) have no line that CO-A1 answered before the proposal or the state-dependent response. An agent that guesses status, amount and payment method passes; in CO-S29 it can guess no order is open.
Pattern: State-dependent proposals and responses with no tool-log line proving the required lookup came first.
(Verdicts F1.)

R2-9 | Lies | Important | CO-03 and Evaluation row "No arrival date promised"
Quote: "The agent states no date or time frame by which the refunded money arrives."
Evidence: Review packet round 3 Q1 (line 61): "The agent promises nothing about when the money arrives." The fix forbids any date or time-frame statement, not only a promise. Applied in CO-03, the row "No arrival date promised" ("The agent states no date or time frame by which the refunded money arrives.") and the Unambiguity notes of CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S27, CO-S28.
Pattern: A prohibition on promising strengthened into a prohibition on mentioning timing at all.
(Verdicts F3.)

R2-10 | Gap | Important | Evaluation row "Refund not issued reported" (CO-S17, CO-S18, CO-S22)
Quote: "| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |"
Evidence: Review packet round 2 Q4 known failure case 2: "refund not issued, state known; agent reports it". The failure rows for a failed refund and a second ProviderUnavailable (agent-spec.md 110-112) and the Unambiguity notes of CO-S17, CO-S18, CO-S22 (lines 1077, 1134, 1374) require "has not been issued". The shared dimension now also accepts "is not confirmed yet", which belongs to CO-S20's post-timeout branch, so an agent that says only "not confirmed yet" after a known failure passes CO-S17, CO-S18, CO-S22.
Pattern: A shared rubric broadened for one uncertain scenario weakens the definite report required in others.
(Verdicts F4.)

R2-11 | Lies | Nit | CO-S17 Reference trajectory
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A CO-A3 (line 1843) returns `{refund_id, amount, payment_method, status}`; `failure_reason` was removed in round 1 (answered M4). The tool result in the reference trajectory still carries "card closed", a value the tool no longer returns.
Pattern: Removing a field from the tool contract without removing its value from reference tool results.
(Verdicts F6.)

## Finder reports, verbatim

### faithfulness

```
2 findings: 1 Important, 1 Nit.

F1 | Gap | Important | CO-S25 Expected / Forbidden (also CO-S26)
Quote: "absent" (CO-S25 has no Required event or Forbidden line that ties the closing message to a lookup made after the second CO-A2. Its only lookup-ordering line is "- A second CO-A2 before a CO-A1 made after the first CO-A2.")
Evidence: The new failure row "CO-A2 | the order system did not answer a CO-A2 | Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it; then act on the row below that matches the lookup's result." says the agent may only report "not cancelled" after a lookup ("a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled"). G-03 (bundle section 4) says that when the agent cannot tell, it must say the outcome is unknown. Without a lookup after the second timeout, the agent cannot tell. Picture an agent that treats the second timeout as a failure, skips the lookup and says "your order was not cancelled". It makes exactly two CO-A2, no CO-A3 and no CO-A4, the world state still matches, and rubric dimension "Order not cancelled reported" passes. So CO-S25 passes an agent that broke G-03 and the CO-A2 row. CO-S25's own Unambiguity note relies on that lookup ("after the second unanswered cancellation the agent can see the order is still open"), and its reference trajectory has it at step 8, but no check requires it. CO-S15 closes the same hole with "CO-A4 before a CO-A1 made after the second CO-A2", and CO-S19's note says "ending without that lookup ... fails in the action log". CO-S26 has the same hole: no line requires the CO-A1 after the unanswered CO-A2 (reference step 6) before the agent reports "shipped".
Pattern: When a scenario's closing message is only truthful because of a lookup made after an unanswered action, the scenario must require that lookup in the action log. Add a Required event such as "CO-A1 occurs after the second CO-A2" (CO-S25) or "CO-A1 occurs after the CO-A2" (CO-S26).

F2 | Gap | Nit | row "Order not cancelled reported" (used by CO-S24)
Quote: "| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |"
Evidence: The failure row "CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; ..." still requires the agent to say "could not be found". So does CO-S24's reference trajectory, step 6 ("Agent tells the customer the order could not be found and was not cancelled"). To share the dimension with CO-S25, the rewrite dropped "could not be found", and the CO-S24 Unambiguity note was cut to match. Now no scenario checks the not-found part of that required message.
Pattern: Merging two scenarios' message checks into one dimension must not drop a part that one scenario's failure row still requires. Split the dimension, or keep a CO-S24-only clause for "could not be found".

Files read: rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (grep hits only, plus the Failure handling table, lines 85-114, and the CO-S24 block)
```

### verdicts-codex

```
6 findings: 5 Important, 1 Nit.

F1 | Gap | Important | CO-S11, CO-S15, CO-S25–CO-S29
Quote: absent
Evidence: CO-01 requires an answered lookup before proposing an open order. The scenarios' Required and Forbidden blocks contain no check that CO-A1 answered before the proposal or state-dependent response: agent-spec.md:693-703, 924-937, 1511-1522, 1568-1578, 1624-1638, 1686-1699, 1742-1753. An agent can guess the order status, amount and payment method pass without reading the orders. In CO-S29 it can guess that no order is open.
Pattern: State-dependent proposals and responses lack a tool-log guard proving the required lookup occurred first.

F2 | Gap | Important | CO-S25, CO-S26
Quote: absent
Evidence: The failure rows require a lookup after every unanswered CO-A2 and make the reported outcome depend on that lookup (agent-spec.md:102-106). CO-S25 only requires a lookup between its two CO-A2 calls, not after the second one. CO-S26 requires no post-timeout lookup at all (agent-spec.md:1511-1522 and 1568-1578). An agent can guess "not cancelled" or "shipped" after the timeout and pass.
Pattern: The repaired timeout branch appears in the reference trajectory but is not enforced by Required or Forbidden checks.

F3 | Lies | Important | CO-03; No arrival date promised
Quote: "Every proposal cancels the whole order and refunds its total paid to its payment method, with no fee and no store credit. When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else. The agent states no date or time frame by which the refunded money arrives."
Evidence: The confirmed input says only that the agent "promises nothing" about arrival timing (review-packet.md:61). The fix instead prohibits every non-promissory date or time-frame statement. That stronger condition is applied in CO-03, the shared dimension, and CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S27 and CO-S28 (grep for "states no date or time frame" in agent-spec.md).
Pattern: A prohibition on making a promise was strengthened into an unsupported prohibition on mentioning timing at all.

F4 | Gap | Important | Refund not issued reported; CO-S17, CO-S18, CO-S22
Quote: absent
Evidence: Known refund errors require the agent to report that the refund was not issued (review-packet.md:53). The failure rows and the three scenario notes likewise require "has not been issued". The shared dimension now accepts the weaker "is not confirmed yet" in all four scenarios (agent-spec.md:110-112, 1077, 1134, 1374, 1823). That alternative belongs to CO-S20's post-timeout branch, not the known-failure states in CO-S17, CO-S18 and CO-S22.
Pattern: Broadening a shared rubric for one uncertainty scenario weakens the required definite outcome report in other scenarios.

F5 | Gap | Important | CO-S24; Order not cancelled reported
Quote: absent
Evidence: The OrderNotFound failure row requires telling the customer both that the order could not be found and that it was not cancelled (agent-spec.md:101). CO-S24 has no separate message assertion. Its revised shared dimension checks only "was not cancelled" (agent-spec.md:1455-1467, 1486, 1824). An agent can omit the not-found result and pass.
Pattern: Generalizing a shared dimension for CO-S25 removed a scenario-specific required detail from CO-S24.

F6 | Lies | Nit | CO-A3 Appendix A; CO-S17 reference trajectory
Quote: "| CO-A3 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` | ... | refund failed (the payment method is closed or expired, or the provider declined): returns the refund with `status: "failed"`; ... |"
Evidence: The return schema exposes only refund id, amount, payment method and status. CO-S17's reference tool result still includes "card closed" (agent-spec.md:1071 and 1843).
Pattern: Removing `failure_reason` from the tool contract did not remove the unsupported value from the reference tool result.

Files read: ~/.codex/skills/ground-check/SKILL.md; rereview-r2.md; review-packet.md; product-idea.md; agent-spec.md
```

### coverage

```
6 findings: 3 Important, 3 Nit.

F1 | Gap | Important | failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing" (and CO-S25)
Quote: "| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. | CO-06, CO-07, G-03 |"
Evidence: The spec says an unanswered CO-A2 can still take effect after a lookup has shown the order open. Appendix B SG-04 (agent-spec.md line 1862) gives its basis as "A second cancellation call that reaches the order system after a first, unanswered one took effect late". Appendix A CO-A2 (line 1842) says "A timeout changes the order or not as Initial state says". For the first CO-A2, SG-04 makes a late effect harmless because the resend is idempotent. After the second CO-A2 there is no resend and no handoff. If that call lands late, the order ends up cancelled with no refund and no staff task, and the customer has been told it was not cancelled. The interview (review-packet.md, round 3 Q4) covers only the first timeout ("send the cancel once more"), so the inputs never set this branch. The customer's interest in getting money back for a cancelled order goes unprotected.
Pattern: A terminal "not done" outcome stated after an unanswered call that the spec itself says may still take effect, with no handoff or caveat. Either decide the branch with the user (handoff or "may still be cancelled") or state that a timed-out CO-A2 never takes effect later.

F2 | Gap | Important | CO-S25, Forbidden / Unambiguity note
Quote: "absent" (nothing in CO-S25 requires a lookup after the second CO-A2 before the agent says the order was not cancelled)
Evidence: CO-S25's Forbidden lines cover only a second CO-A2 before a post-first lookup, a third CO-A2, CO-A3 and CO-A4. The rubric "Order not cancelled reported" checks only that the agent "said the order was not cancelled". Take an agent that gets two timeouts and then replies "I couldn't cancel your order" without looking up. It passes every check, yet G-03 allows "not done" only when a lookup shows it, and otherwise requires "the outcome is unknown". The new row also says to tell "not cancelled" only once "a lookup made after the second CO-A2 ... shows the order placed or processing". The Unambiguity note relies on that lookup ("the agent can see the order is still open"), but no line checks it. The sibling CO-S15 checks the same dependency with "CO-A4 before a CO-A1 made after the second CO-A2", and CO-S19 notes "ending without that lookup ... fails in the action log".
Pattern: An outcome message that is truthful only after a read-only lookup, in a scenario with no Forbidden line or rubric clause that fails the message when the lookup is missing.

F3 | Ambiguous | Important | CO-02 (and failure row "the customer named no order, and exactly one ...")
Quote: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order."
Evidence: "names no order" is never defined. The rule's title is "by number", and its last clause says "names an order number". The neighbouring row (agent-spec.md line 90) instead uses "has not said which one they mean", and CO-S02 rows 2 and 3 count naming by item or placed date as saying which. Suppose a customer says "cancel my blanket order", the blanket order is delivered and the candle order is the only open one. Under a by-number reading the agent may propose the candle order. Under a by-description reading it must apply CO-01 to the blanket order and propose nothing. This is the user's known failure case 1, "Wrong order cancelled" (review-packet.md, round 2 Q4). The next clause, "When more than one has, the agent asks which", also drops the old qualifier "and the customer has not said which one they mean", so it is unclear whether "names no order" carries over to it.
Pattern: A new condition term that differs from the one sibling rows use ("names no order" against "has not said which one they mean"), with no definition.

F4 | Ambiguous | Nit | CO-02 against failure row "the customer named no order, and exactly one ..."
Quote: "the agent may propose that order."
Evidence: The new failure row says "Propose that order." (mandatory), and CO-S28 requires CO-A2 and CO-A3. Its only User-knows pair is the full proposal, so there is no answer for "which order?". Under the rule's "may", an agent that asks which order instead is compliant, but CO-S28 can fail it.
Pattern: A rule that permits ("may") while its failure row and scenario require the action.

F5 | Ambiguous | Nit | failure row "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
Quote: "| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | Tell the customer it is not known whether the order was cancelled, ... make CO-A4 with reason cancellation unknown. | CO-07, G-03 |"
Evidence: Lookups may be retried without limit. The user's tool-confirmation change 4 (review-packet.md) says "Reads may be retried on timeout without limit", and CO-06 says "lookups are not limited". This row fires on any single lookup that goes unanswered. An agent that retries the lookup and then sees the order placed or processing matches both this row (mandatory CO-A4) and the "still placed or processing" rows. CO-07 allows CO-A4 only when the agent "cannot tell", which it now can. The rows never say whether the agent should retry the lookup first or hand off on the first timeout.
Pattern: A failure row triggered by "a lookup did not answer" when lookups are retryable, which overlaps rows triggered by a later lookup's result.

F6 | Gap | Nit | row "Order not cancelled reported" (CO-S24)
Quote: "| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |"
Evidence: The CO-A2 not-found row (agent-spec.md line 101) still says "Tell the customer the order could not be found and was not cancelled". The edit dropped "could not be found" from the dimension and from CO-S24's note, so no scenario now checks that part of the message the row requires.
Pattern: A rubric dimension made broader so another scenario can share it, which drops a required message clause for the original scenario.

Also (Nit, Gap): failure row "the customer named no order, and none of the customer's orders has status placed or processing" also matches a signed-in customer with no orders at all. In that case its reason, "because each has shipped, been delivered or been cancelled", is false. No row covers a customer with no orders.

Pre-existing: none noted in the section-4 context blocks.

Files read: rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (grep only: line 10, failure-table lines 89-114, Appendix A lines 1841-1844, SG-02 and SG-04 lines 1860 and 1862, and the Turn 2 and message-check lines)
```

## Verifier reports, verbatim

### Verifier A

```
R2-1 | Real | Important | CO-S25's Forbidden block has only "A second CO-A2 before a CO-A1 made after the first CO-A2." and nothing about a lookup after the second CO-A2, while CO-S15 has "CO-A4 before a CO-A1 made after the second CO-A2". So an agent that skips that lookup and just says "not cancelled" passes, though G-03 and CO-07 require "unknown" plus CO-A4 when it cannot tell. The CO-S26 half is weaker: an agent would have to guess "shipped" without a lookup, which is unlikely.
R2-2 | Real | Nit | The CO-A2 not-found row (line 101) and CO-S24 step 6 still say "could not be found", but the dimension now checks only "was not cancelled". The rule CO-05 itself requires only "tells the customer the order was not cancelled", so the scenario still grades the rule and the customer still hears the true outcome.
R2-3 | Real | Important | SG-04 covers "a first, unanswered one took effect late", and CO-A2 says "A timeout changes the order or not as Initial state says". So the spec allows a late effect, yet the second-timeout row ends with "not cancelled" and no CO-A4. Round 3 Q4 decides only "send the cancel once more", not what happens after the second timeout. A late effect would leave the order cancelled with no refund and no staff task.
R2-4 | Real | Important | The CO-02 title says "by number" and its last clause says "names an order number", while the sibling row (line 90) says "has not said which one they mean". So "names no order" can be read as "gave no number", and a customer asking about a delivered "blanket order" would then be offered the other, open order. That is known failure case 1, wrong order cancelled. Confirmation reduces the harm but does not remove it.
R2-5 | Real | Nit | CO-02 says "may propose" but the failure row says "Propose that order.", so the two conflict. Still, CO-S28 has no Required or Forbidden line that fails an agent which first asks which order and then proposes, so the conflict changes no verdict.
R2-6 | Real | Nit | The packet says "Reads may be retried on timeout without limit", and CO-07 says "CO-A4 occurs in no other situation". Even so, the row makes CO-A4 mandatory after one unanswered lookup, and it overlaps the "shows placed or processing" rows after a retry. CO-S14 (line 855) and CO-S15 (line 914) make every later CO-A1 go unanswered, so no verdict changes.
R2-7 | Real | Nit | The row's condition also matches a signed-in customer with no orders at all, and for that customer "because each has shipped, been delivered or been cancelled" misleads. No scenario covers that case, so no verdict changes.
R2-8 | Not real | Nit | The User-knows answer matches only a proposal that states the exact amount and payment method, and Appendix A gives CO-A1 as the only source of `total_paid` and `payment_method`. So a correct proposal in CO-S11, S15, S25-S28 proves the lookup happened. CO-S29's rubric requires the true reason "shipped or been delivered". No scenario in the spec, changed or not, has such a line, and none needs one.
R2-9 | Not real | Nit | The packet (line 57) says the user never answered round 2 Q2 ("5 to 10 business days"), and round 3 Q1 replaced it with "promises nothing about when the money arrives". So the inputs hold no confirmed time frame, and any time frame the agent stated would be an unsourced commitment. "States no date or time frame" is therefore a faithful rendering.
R2-10 | Real | Important | The dimension now accepts "is not confirmed yet" for CO-S17, S18 and S22, where the refund failed for sure. Yet the failure rows at lines 110-111 and the notes at lines 1077, 1134 and 1374 require "has not been issued", and G-03 says "tells the customer the action was not done". So a vague "not confirmed yet" after a known failure passes. This is a regression caused by the M3 fix, not a repeat of M3.
R2-11 | Real | Nit | Line 1071 reads "refund RF-5531, failed, card closed.", but CO-A3 returns only `{refund_id, amount, payment_method, status}`. The same leftover appears at lines 1367 (CO-S22) and 1426 (CO-S23). It is trajectory text only and changes no check.

Files read: rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (only: failure table lines 86-114, Appendix A/B lines 1838-1862, CO-S14 block, CO-S24 lines 1452-1486, grep hits for CO-A1 event lines, "card closed", "could not be found", "has not been issued")
```

### Verifier B

```
R2-1 | Real | Important | No Required or Forbidden line in CO-S25 needs a CO-A1 after the second CO-A2 (its only lookup line is "A second CO-A2 before a CO-A1 made after the first CO-A2."). An agent that skips that lookup and says "not cancelled" makes the same calls and passes "Order not cancelled reported", but under G-03/CO-07 it should have reported the outcome unknown and made CO-A4. The CO-S26 half is weaker: without the lookup an agent cannot learn the order shipped, so it would most likely make CO-A4 and fail Forbidden. CO-S25 alone carries the severity.
R2-2 | Real | Nit | The failure row (spec line 101) and CO-S24 reference step 6 still say "could not be found", but no dimension checks it any more. It changes no verdict that matters, because the governing rule CO-05 only requires "When the order system reports the order not found, the agent tells the customer the order was not cancelled and issues no refund."
R2-3 | Real | Important | SG-04 (line 1862) exists for "A second cancellation call that reaches the order system after a first, unanswered one took effect late", and CO-A2 (line 1842) says "A timeout changes the order or not as Initial state says". So late effect is part of the spec's own model. After the second CO-A2 there is no protecting resend and no handoff, and the order can end cancelled with no refund. Round 3 Q4 decides only the first timeout ("send the cancel once more").
R2-4 | Real | Important | "names no order" sits next to "by number" in the title, "names an order number" in the last clause, and "has not said which one they mean" in the line-90 row. CO-S02 rows 2 and 3 count an item or a date as naming. The two readings give different proposals (candle order vs nothing). Also, "When more than one has, the agent asks which" no longer says "and the customer has not said which", so it can be read as asking even after the customer gave a number.
R2-5 | Real | Important (raised from Nit) | §5.1 Simulated user (line 1797): it "deflects any other question". CO-S28 has only the full-proposal pair. Under "may propose", an agent that keeps asking which order is compliant but gets only deflections and never reaches CO-A2/CO-A3, so it fails CO-S28. That is failing a scenario it should pass.
R2-6 | Real | Nit | The rows do overlap with "Reads may be retried on timeout without limit" (packet change 4; Appendix A line 1837 "The agent may repeat CO-A1 without limit"). No verdict changes, because CO-S14 (line 855) and CO-S15 (line 914) both make every CO-A1 after the CO-A2 go unanswered.
R2-7 | Real | Nit | Nothing in the row excludes a customer with zero orders, and for that customer the message "because each has shipped, been delivered or been cancelled" is misleading. No scenario uses zero orders.
R2-8 | Real | Important (CO-S29 only; overstated for the rest) | For CO-S11/S15/S25/S26/S27/S28, §5.1 (line 1777) makes the simulated user confirm only a question whose amount and payment method equal the pair's values, and a guess cannot reach those without a lookup. In CO-S29, though, an agent that skips CO-A1 and claims both orders shipped or were delivered passes every check. No spec line requires a CO-A1 before a state-dependent reply (the only CO-A1 lines are post-CO-A2/CO-A3 at 758-1519).
R2-9 | Not real | Nit | The inputs give no time frame for the agent to state. Round 2 Q2 proposed "money arrives in 5 to 10 business days", the user never answered it, and round 3 Q1 replaced it with "The agent promises nothing about when the money arrives". Any date or time frame the agent stated would be invented, which G-03 already forbids, so the stricter wording matches the input's intent.
R2-10 | Real | Important | In CO-S17/S18/S22 the refund is known to have failed, and the failure rows (lines 110-112) and those scenarios' Unambiguity notes require "has not been issued". Known failure case 2 says "refund not issued, state known; agent reports it". The shared dimension now passes "is not confirmed yet", which implies the refund may still go through, so an agent that gives that weaker report passes scenarios it should fail. This is a new consequence of the M3 fix, not a repeat of M3.
R2-11 | Real | Nit | CO-A3 now returns `{refund_id, amount, payment_method, status}` with no reason field (line 1843). The reference trajectories still show "refund RF-5531, failed, card closed." at lines 1071 (CO-S17), 1367 and 1426. Reference trajectories are not graded.

Files read: rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (grep and line-range excerpts only: line 10, 1066-1078, 1125-1136, 1366-1376, 1470-1487, 1775-1797, 1837-1862, and the CO-A1 grep hits)
```

### Verifier C

```
R2-1 | Real | Important | The failure row at line 102 says "Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it; then act on the row below". CO-S25's Forbidden block only orders the lookup after the first CO-A2, and CO-S26 has no lookup line, so an agent that skips the lookup after the second unanswered CO-A2 and says "not cancelled" makes the same calls, leaves the same state and passes. CO-S15 line 936 shows the form that would close this. CO-S25 is the case that matters: an agent that guesses "shipped" in CO-S26 without a lookup is unlikely.
R2-2 | Real | Important (raised from Nit) | Line 101 still requires "Tell the customer the order could not be found and was not cancelled", and CO-S24 step 6 still says it. The dimension now checks only "was not cancelled", so an agent that leaves out the not-found part breaks the failure row and still passes CO-S24. That lets it pass a scenario it should fail.
R2-3 | Real | Important | SG-04 (line 1862) is justified by "a first, unanswered one took effect late", and CO-A2 (line 1842) says "A timeout changes the order or not as Initial state says". So a late-landing second CO-A2 can leave the order cancelled with no refund and no task, after line 105 has already told the customer it was not cancelled. Round 3 Q4 only decides the first timeout ("send the cancel once more"). Nothing in the inputs covers the second.
R2-4 | Real | Important | The same rule pairs "names no order" with "names an order number" under the title "by number", while CO-S02's note counts "name the order by an item or by the placed date" as naming. So "cancel my blanket order" (delivered blanket order, one open candle order) can reasonably lead to proposing the candle order, which is the setup for known failure case 1. Also, "When more than one has" no longer says plainly whether a customer who named an order is exempt.
R2-5 | Real | Nit | CO-02 says "the agent may propose that order", while line 91 says "Propose that order." and CO-S28's User knows has no which-order answer. The rule permits what the row requires. An agent that asks "which?" only gets deflected and can still finish, so the verdict rarely changes.
R2-6 | Real | Nit | Line 107 fires on "a lookup ... did not answer", yet lookups "may be repeated without limit" (line 1837), and a retried lookup that shows the order open also matches line 104 or 105. CO-S14 and CO-S15 make every later CO-A1 go unanswered, so no current scenario's verdict depends on the overlap.
R2-7 | Real | Nit | Line 92's condition also matches a signed-in customer with no orders, for whom "because each has shipped, been delivered or been cancelled" misdescribes the account. No scenario has an empty order list.
R2-8 | Real | Nit (lowered from Important) | No such line exists, but §5.1 says a confirmation question must state every proposal value equal to the User-knows pair, and "A question with the right form and one wrong value is not the confirmation question". So in the confirm scenarios an agent that skips the lookup cannot get a Yes. That leaves only CO-S29's refusal without a lookup as a realistic pass. CO-S01 to CO-S10 have the same gap, so it predates this round.
R2-9 | Not real | Nit | Round 2 Q2 proposed "money arrives in 5 to 10 business days". Round 3 Q1 replaced that with "The agent promises nothing about when the money arrives", and the user said "Yes to all". No input allows stating a time frame, and no Appendix A tool returns an arrival time. "States no date or time frame" is a gradable version of that answer, not a contradiction of it.
R2-10 | Real | Important | Lines 110 and 111 and the notes at 1077, 1134 and 1374 require "the refund has not been issued" when the failure is known. G-03 requires saying "the action was not done" when the agent can tell. The shared dimension now accepts "is not confirmed yet", so an agent that only hedges after a known failure passes CO-S17, CO-S18 and CO-S22. This is a new defect caused by the M3 fix, not a repeat of M3.
R2-11 | Real | Nit | CO-A3's outcome now reads "returns the refund with `status: \"failed\"`" with no reason field, yet CO-S17 step 6 still shows "refund RF-5531, failed, card closed". The reference trajectory is not graded, so no verdict changes.

Files read: rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (blocks only: lines 60-66, 84-116, 180-240, 846-880, 1060-1078, 1438-1490, 1721-1760, 1773-1794, plus grep hits at lines 10, 1134, 1192, 1374, 1837, 1842, 1860, 1862)
```
