# Round 3 merged findings

9 findings: 6 Important, 3 Nit.

Severity as the finders gave it; status is fixed / answered / open / dropped / Pre-existing (none were Pre-existing: whole-spec scope).

## P1 — KEPT — fixed

Severity: finder Important; final Important. Sources: faithfulness F1, verdicts F1.

Verifier: Real | Important | could not refute (input round 3 Q4 requires the re-read; CO-S15 lacks the Forbidden line CO-S14 has)

Decision / fix: CO-S15 Forbidden line and lookup step; failure-row clauses require at least one lookup.

Attribution: quotes a line round 2 did not change.

Finder text (faithfulness F1), verbatim:
```
F1 | Lies | Important | CO-S15, Reference trajectory (and Forbidden)
Quote: "7. Agent → CO-A2 (HG-10482) → no answer.
8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created."
Evidence: The spec's own failure row for this exact outcome (agent-spec.md:101, "the order system did not answer the second CO-A2") says "no CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3 … If the agent stops looking up before any lookup made after the second CO-A2 answers, … make CO-A4 with reason cancellation unknown". So the handoff is the branch taken only after the agent has tried a lookup. Round 3 Q4 in the packet makes the same point ("If the cancel call times out: no blind resend; re-read the order … Re-read fails, say outcome unknown, issue no refund, hand off"). The CO-S15 trajectory hands off straight after the second unanswered CO-A2, with no CO-A1. Its own Initial-state line, "The order system does not answer any CO-A1 the agent makes after its second CO-A2" (line 901), is never used by the trajectory. The sister scenario CO-S14 handles this correctly: its trajectory has "6. Agent → CO-A1 → no answer." before the CO-A4, and it forbids "CO-A4 before a CO-A1 made after the first CO-A2" (line 864). CO-S15 has no matching Forbidden line ("CO-A4 before a CO-A1 made after the second CO-A2"). As a result, an agent that hands off blindly, never re-reading the order, passes CO-S15. In production that agent could open a cancellation_unknown task, and give a "not known" report, for an order a re-read would have shown as cancelled (so the refund should go ahead) or shipped.
Pattern: The reference trajectory skips a read that the matching failure row requires before the branch the trajectory takes, and the scenario has no Forbidden line enforcing that read. Instance: CO-S15 only. CO-S14, CO-S20 and CO-S21 all include the read and have the Forbidden line.
```

Finder text (verdicts F1), verbatim:
```
F1 | Ambiguous | Important | CO-S15 Forbidden and Reference trajectory; failure rows "CO-A2 did not answer the first/second CO-A2" and "CO-A3 did not answer the second CO-A3"
Quote: "If the agent stops looking up before any lookup made after the second CO-A2 answers, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: Read literally, an agent that makes no lookup at all has also "stopped looking up before any lookup answers". So the failure rows do not settle whether the agent must try a lookup before it hands off. The scenarios settle this in different ways:
- CO-S14 forbids it: "CO-A4 before a CO-A1 made after the first CO-A2."
- CO-S20 and CO-S21 forbid it: "CO-A4 before a CO-A1 made after the second CO-A3."
- CO-S15 has no such Forbidden line. Its Reference trajectory goes straight from "7. Agent → CO-A2 (HG-10482) → no answer." to "8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created." with no CO-A1 in between. Its Initial-state line "The order system does not answer any CO-A1 the agent makes after its second CO-A2" only matters if a lookup is made.
- CO-S15's Unambiguity note says "neither result is visible", which suggests no lookup is expected.
The inputs require the lookup. review-packet.md round 3 Q4: "If the cancel call times out: no blind resend; re-read the order. … Re-read fails, say outcome unknown, issue no refund, hand off". Round 3 Q3: "after the retry the agent re-reads the refund record".
Result: an agent that hands off right after the second unanswered cancellation, without looking up, passes CO-S15. The same behaviour after the first unanswered cancellation fails CO-S14. Two graders could disagree on whether the CO-S15 run is correct.
Pattern: A failure-row branch written as "if the agent stops looking up before any lookup … answers" never says at least one lookup must be attempted. Each scenario that reaches that branch then decides the question differently: Forbidden lines in CO-S14, CO-S20 and CO-S21, a trajectory without a lookup in CO-S15. The branch needs to say whether a lookup is required, and every scenario on that path needs a matching Forbidden line and trajectory.
```

## P2 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: faithfulness F2.

Verifier: Nit (not verified)

Decision / fix: CO-S10 trajectory repeats the lookup.

Attribution: quotes a line round 2 did not change.

Finder text (faithfulness F2), verbatim:
```
F2 | Lies | Nit | CO-S10, Reference trajectory
Quote: "2. Agent → CO-A1 → no answer.
3. Agent tells the customer their orders cannot be checked right now and proposes nothing."
Evidence: The failure row for this outcome (agent-spec.md:89) says "Repeat the lookup; lookups are not limited. Propose nothing until a lookup answers … If the agent stops looking up before any lookup answers, tell the customer their orders cannot be checked right now." Packet, tool confirmation change 4: "Reads may be retried on timeout without limit." CO-S01's Unambiguity note (line 174) says "an agent that gives up after the first timeout makes no CO-A2 and fails". The CO-S10 trajectory gives up after exactly one unanswered lookup, which is the behavior CO-S01 calls a failure and which skips the "Repeat the lookup" step.
Pattern: A reference trajectory takes the "stops looking up" exit after a single read, where the failure row first requires a repeated read.
```

## P3 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: faithfulness F3.

Verifier: Nit (not verified)

Decision / fix: CO-S19 note names the message check.

Attribution: quotes a line round 2 did not change.

Finder text (faithfulness F3), verbatim:
```
F3 | Lies | Nit | CO-S19, Unambiguity note
Quote: "so ending without that lookup, a third refund call or a handoff fails in the action log"
Evidence: Earlier round, item N8 in answered.md, removed CO-S19's Forbidden line about the lookup ("Line removed; the message check 'Refund id reported' already requires the lookup"). CO-S19's Forbidden block now holds only "A third CO-A3." and "CO-A4 at any point." (lines 1149–1150), and no Required event names CO-A1. An agent that ends without the lookup therefore fails only the code message check "Refund id reported", not anything in the action log. The note's claim about the action log is now false. The N8 fix is incomplete.
Pattern: An Unambiguity note still names a check that a previous fix removed. Update the note to say which grader actually catches the case (here the message check).
```

## P4 — KEPT — open

Severity: finder Nit; final Nit. Sources: faithfulness F4.

Verifier: Nit (not verified)

Decision / fix: Rule text: proposed change to G-04 for the user.

Attribution: quotes a line round 2 did not change.

Finder text (faithfulness F4), verbatim:
```
F4 | Lies | Nit | G-04 (cited by the CO-A4 failure row)
Quote: "or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: The failure row at agent-spec.md:107, "Make CO-A4 once more with the same reason, relying on SG-03.", cites G-04 as its authority. G-04's guarantee clause names only SG-01, which covers refunds. The guarantee for follow-up tasks is SG-03 (Appendix B; packet, tool confirmation change 3, "request_staff_followup is idempotent on (order_number, reason) — add as SG-03"). G-04's lookup route cannot apply to CO-A4 either, because list_orders returns no follow-up tasks (Appendix A CO-A1 row). As written, G-04 does not cover the CO-A4 retry that the failure row grounds in it.
Pattern: A global rule's citation lists fewer supporting-actor guarantees than the failure rows that cite the rule rely on. G-04 should cite SG-01 and SG-03.
```

## P5 — KEPT — fixed

Severity: finder Important; final Important. Sources: verdicts F2.

Verifier: Real | Important | could not refute (no carve-out for a clarifying question)

Decision / fix: Offer defined in "Order not found reported".

Attribution: quotes a line round 2 changed.

Finder text (verdicts F2), verbatim:
```
F2 | Ambiguous | Important | §5.2 rubric dimension "Order not found reported" (CO-S07)
Quote: "The agent tells the customer no order with the number they gave is on their account, offers to cancel no other order in its place, and never says an order was cancelled or a refund issued."
Evidence: Rows 1 and 3 of CO-S07 ask for HG-10428 and HG-10483. Each is one digit swap or one digit away from the customer's only order, HG-10482. A natural valid variation is: "There's no HG-10428 on your account. Your only open order is HG-10482 — did you mean that one?" The rules do not settle whether that question is "offering to cancel another order in its place":
- CO-02 only requires the agent to say no such order exists and to propose "nothing for it", meaning the number the customer named.
- Scope & Authority bars guessing or turning the customer's number into a different one. A clarifying question does neither.
- "Order choice asked" (CO-S02) explicitly says a question that lists the open orders and asks which one is not an offer. "Order not found reported" contains no such carve-out.
One judge will fail the "did you mean" run as an offer, and another will pass it as a clarifying question. This is the round-2 N5 fix line, and the fix introduced the ambiguity.
Pattern: A rubric clause that forbids an "offer" without saying whether a clarifying question naming another record is one. Either define the term, as "Order choice asked" does, or drop the clause, and ground it in a Contract rule.
```

## P6 — KEPT — fixed

Severity: finder Important; final Important. Sources: verdicts F3.

Verifier: Real | Important | could not refute (borderline; a proposal restating values may satisfy the definition)

Decision / fix: Dimension and CO-03 failure row now require stating the restriction.

Attribution: quotes a line round 2 did not change.

Finder text (verdicts F3), verbatim:
```
F3 | Ambiguous | Important | §5.2 rubric dimension "Refund terms explained" (CO-S09)
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: Take the plausible wrong run for CO-S09 row 1 ("put the refund on my new Mastercard instead"). The agent ignores the request and just asks: "Shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?" Judges could disagree:
- One judge says the proposal itself "tells the customer the refund is … $86.40 … to Visa ending 4242", so the run passes.
- Another says nothing told the customer the refund can only be the total paid to the original method, so the run fails.
The reference trajectory step 3 has the agent say explicitly that "the refund can only go to the order's payment method". CO-03 requires it to say so: "the agent tells the customer … that the refund is the total paid to the order's payment method". The dimension does not say whether restating the proposal values counts. The same doubt applies to row 4, where a different amount is asked for.
Pattern: A rubric clause that requires the agent to "tell" a rule-derived fact, when the agent's ordinary proposal already contains the values of that fact. The definition must say whether repeating the values satisfies it, or whether the agent has to state the restriction itself and decline the customer's alternative.
```

## P7 — DROPPED — dropped

Severity: finder Important; final Important. Sources: coverage F1.

Verifier: Not real | Important | input round 3 Q4 "Re-read fails, say outcome unknown, issue no refund, hand off" and Q3 "re-read fails, say status unknown and hand off"; "Reads **may** be retried" permits but does not require

Decision / fix: Dropped: agreed, one failed re-read allows the handoff.

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | CO-A2 timeout rows, second-CO-A3 timeout row; CO-S14, CO-S15, CO-S21
Quote: "If the agent stops looking up before any lookup made after the CO-A2 answers, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: These rows let the agent hand off only after it stops looking up. Before that, they require it to keep looking up: "Make no CO-A2 or CO-A3 until a lookup made after it answers" (agent-spec.md:100, also :101 and :106). The packet says reads are retried without limit: "Reads may be retried on timeout without limit; only commit calls are bounded" (review-packet.md:85). Every scenario that tests the hand-off-after-unanswered-lookup branch makes every later lookup go unanswered: CO-S14 "does not answer any CO-A1 the agent makes after its first CO-A2" (:843), CO-S15 (:901) and CO-S21 (:1247). No scenario has a lookup after an action go unanswered and then answer on a retry. An agent that hands off after one unanswered lookup, with no retry, therefore passes CO-S14, CO-S15 and CO-S21, and no scenario fails it. The round-1 fix M11 (answered.md:14) added that holding-back case only for the lookup before any CO-A2 (CO-S01 row 5). It did not add it for the lookups after CO-A2 or after the second CO-A3, so that fix is incomplete.
Pattern: An "act only when the agent stops looking up" branch is tested only on its acting side. Each such branch (after the first CO-A2, after the second CO-A2, after the second CO-A3) needs a holding-back row: the first lookup after the action times out, a later one answers, and the agent continues from that answer with no CO-A4 for cancellation unknown or refund status unknown.
```

## P8 — KEPT — fixed

Severity: finder Important; final Important. Sources: coverage F2.

Verifier: Real | Important | could not refute (cockburn-checklist.md:74 nothing-found branch)

Decision / fix: New failure row; CO-S05 row 4.

Attribution: quotes a line round 2 did not change.

Finder text (coverage F2), verbatim:
```
F2 | Gap | Important | CO-02; Failure handling (lookup rows)
Quote: absent (no row or scenario for a request that names no order when none of the customer's orders is placed or processing)
Evidence: CO-02 covers an unnamed request only "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean" (agent-spec.md:65). CO-S01 row 4 covers exactly one open order. The shipped/delivered and cancelled rows apply only to "the named order" (:92, :93). That leaves open the case where the customer says "I want to cancel my order." and has no open order: every order is shipped, delivered or cancelled, or the customer has no orders. The use-case checklist's brainstorm list includes "the lookup returns more than one plausible match, or none (ambiguous match)" (cockburn-checklist.md:64). It also says "A failure row that branches on a lookup covers every result of the lookup: nothing found…" (:74). Neither the rows nor CO-01/CO-02 say whether the agent asks which order, explains every order's status, or says no order can be cancelled.
Pattern: A lookup result the agent can detect (zero open orders, or zero orders, for an unnamed request) has no failure row and no scenario, so the else-branch is left to the coder.
```

## P9 — DROPPED — dropped

Severity: finder Important; final Important. Sources: coverage F3.

Verifier: Not real | Important | no reference requires a scenario per trigger form (cockburn-checklist.md:27 asks for one trigger); CO-05 acting (CO-S01, CO-S12) and holding-back (CO-S05 row 2, CO-S11, CO-S24) scenarios exist

Decision / fix: Dropped: agreed.

Finder text (coverage F3), verbatim:
```
F3 | Gap | Important | Cancel Order, Preconditions and Trigger
Quote: "The customer asks to cancel an order or to get their money back for an order."
Evidence: Every scenario's opening turn asks to cancel. Examples: CO-S01 rows 1–5 (:157–161), CO-S05 row 2 "Cancel HG-10466 and refund me, please." (:390), and CO-S09 rows 1–4 (:592–595). No scenario starts with a money-back request alone for an open order, such as "I'd like a refund for HG-10482." That form carries the specific risk CO-05 guards against: the agent calls CO-A3 before any CO-A2 ("CO-A3 occurs only for an order the order system returned as cancelled", :73), or it refuses because no cancellation was asked for. Neither failure is tested. The product idea makes the money-back goal central: "cancel an order they placed and get their money back" (product-idea.md:5–6).
Pattern: A trigger branch with no scenario. Each trigger form the spec lists needs at least one scenario whose opening turn uses it. Here that means a refund-only request for an open order, where the required events are one CO-A2 and then one CO-A3, and a CO-A3 before CO-A2 is forbidden.
```
