# Round 2 findings (merged)

15 findings: 8 Important, 7 Nit.

### R2-01 (from faithfulness F1)

R2-01 | Lies | Important | CO-A2 failure rows "did not answer the first CO-A2" and "did not answer the second CO-A2" vs §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: The failure rows that CO-S14 and CO-S15 trigger only require the agent to say the outcome is unknown and that staff will follow up. Neither asks it to say anything about the refund. The first-CO-A2 row (agent-spec.md line 100) and the second-CO-A2 row (line 101) both read: "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown." The input does not require a refund statement either. Round 3 Q4 (review-packet.md) says: "Re-read fails, say outcome unknown, issue no refund, hand off." That is an action ("issue no refund"), not something to tell the customer. The clause "no refund was issued" appears only in the CO-A3 "reported the order not cancelled" row (line 104), and no scenario triggers that row. So an agent that does exactly what the CO-A2 rows say fails the dimension, and therefore fails CO-S14 and CO-S15. The reference trajectories (CO-S14 step 8, CO-S15 step 10) also include "no refund was issued", which the rows do not support.
Pattern: A rubric dimension requires the agent to tell the customer something that the failure row the scenario triggers (and the inputs) never requires. Either add the clause to the row or drop it from the dimension and the trajectory.

Verifier: R2-01 | Not real | Important | G-03 already requires the refund clause in CO-S14 and CO-S15: "tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it. Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." In both scenarios no CO-A3 occurs, so the agent can tell the refund was not done, and G-03 requires it to say so. G-03 is cited in the second-CO-A2 row (line 101). As a global minimal guarantee it also binds the first-CO-A2 row. The primary-actor interest (line 9) agrees: "wants to be told truthfully whether the order was cancelled and where the refund stands". An agent that follows the CO-A2 rows together with G-03 says "no refund was issued", so the dimension and the reference trajectories match the contract.
Decision: dropped | Status: dropped | Refutation quoted: G-03 'tells the customer a refund is pending or issued only when ... Otherwise it tells the customer the action was not done'. I agree: with no CO-A3 made, G-03 requires the agent to say no refund was issued, so the dimension and trajectories match the contract.

### R2-02 (from faithfulness F2)

R2-02 | Lies | Important | §4.1 Failure handling, row "any | the customer changed the order or another proposal term…"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: CO-04 (line 71) names the proposal terms: "order number, refund amount and payment method". So "another proposal term" means the amount or the payment method. For those two terms, the row tells the agent to propose the customer's changed terms, which the inputs forbid:
- Round 2 Q3 user answer (review-packet.md): "refund amount = order total paid; refund payment method = order's payment method".
- Round 3 Q1: "No cancellation fee, no store-credit option".
- The tool takes no amount or payment method. The packet tool set lists `issue_refund(order_number)`, and Appendix A says "amount and payment method through the order". A changed proposal such as "refund to my Mastercard" therefore cannot be executed. Confirming it would authorize something CO-A3 cannot do, against G-02 "the exact proposal it executes".
- It also contradicts the spec's own CO-03 (line 68: "proposes nothing else") and the row at line 95 ("propose only that").
Pattern: A failure row tells the agent to propose a change to a term that a domain rule or the tool contract fixes. Limit "propose the changed proposal" to a change of order. A requested change to amount or payment method goes to the CO-03 handling.

Verifier: R2-02 | Real | Important | Partial refutation only. CO-03 "Every proposal cancels the whole order and refunds its total paid to its payment method" and row 95 "propose only that" settle what may be proposed when the customer asks for a different amount or payment method. Row 96, which also applies in the confirming turn, still says "propose the changed proposal" for "another proposal term", and CO-04 defines those terms as amount and payment method. The two rows give opposite instructions for that case. Only a reconciling reading the spec never states resolves it, and the conflict stands against round 2 Q3 ("refund payment method = order's payment method").
Decision: kept | Status: fixed | Row 96 limited to a different order; row 95 now covers a term change at any point before CO-A2, including in reply to the confirmation question; new CO-S27.

### R2-03 (from faithfulness F3; duplicate: verdicts F4)

R2-03 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Two problems with the second clause.
- It permits a blind cancel resend. SG-04 (Appendix B line 1620; tool confirmation change 1, "cancel_order is idempotent") is exactly a guarantee that a repeated cancel creates nothing new. Read literally, G-04 lets the agent resend an unanswered CO-A2 without a lookup. The input forbids that. Round 3 Q4: "If the cancel call times out: no blind resend; re-read the order."
- It cites only SG-01. The CO-A4 retry (row at line 107, "relying on SG-03") can rest only on this clause, because list_orders returns no follow-up tasks (Appendix A CO-A1 return shape), so no lookup can show that a handoff took no effect. Yet G-04 names SG-01 (refunds) as its guarantee.
CO-06 and the Forbidden lines ("A second CO-A2 before a CO-A1 made after the first CO-A2") still settle the scenario verdicts, so no verdict changes.
Pattern: A global rule's permission is broader than the input allows for one action, and its guarantee citation leaves out the guarantees the failure rows actually rely on. Restrict the guarantee clause to CO-A3 and CO-A4 (SG-01, SG-03), and state that CO-A2 is repeated only after a lookup.

Duplicate report (verdicts F4), kept for its evidence:
R2-03-dup | Ambiguous | Nit | G-04 vs CO-06; CO-S12 and CO-S13 Forbidden
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (Appendix B, line 1620) states exactly such a guarantee for CO-A2: "cancelling an order that is already cancelled returns it cancelled and changes nothing". So under G-04, a blind second CO-A2 after an unanswered first one is allowed. CO-06 (line 77) allows a second CO-A2 "only after ... a lookup made after it shows the order still placed or processing". The input agrees with CO-06: round 3 Q4, "no blind resend; re-read the order". CO-S12's Forbidden "A second CO-A2." and CO-S13's Forbidden "A second CO-A2 before a CO-A1 made after the first CO-A2." enforce CO-06, so scenario verdicts are decided. The global rule still tells a builder the opposite.
Pattern: A general rule's escape clause ("when the order system guarantees ...") covers a case a capability rule forbids. Limit G-04's guarantee clause to the actions whose retry the inputs allow (CO-A3 under SG-01, CO-A4 under SG-03), or exclude CO-A2 by name.

Verifier: R2-03 | Real | Nit | Could not refute; the defect holds either way G-04 is read. Read "(Appendix B, SG-01)" as non-restrictive: SG-04 ("cancelling an order that is already cancelled returns it cancelled and changes nothing") qualifies, and G-04 permits a blind CO-A2 resend against round 3 Q4 "no blind resend; re-read the order". Read it as restrictive: the CO-A4 retry (row 107, "relying on SG-03") has no G-04 basis. CO-06 ("a second CO-A2 only after ... a lookup made after it shows the order still placed or processing") and the CO-S12/S13 Forbidden lines settle the verdicts, as the finding concedes, but G-04's text still stands.
Decision: kept | Status: open | The fix changes G-04's text, so it stops at the rule: proposed rule change for the user (guarantee clause limited to CO-A3/CO-A4, SG-01/SG-03).

### R2-04 (from coverage F1)

R2-04 | Gap | Important | CO-02; Failure handling row "more than one of the customer's orders has status placed or processing"; Scenarios
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-02 (agent-spec.md line 65) is an "act only when" rule: the agent asks only when more than one order is open. The asking side has a scenario, CO-S02 (line 186, "I want to cancel my order.", two open orders). No scenario covers the other side, a request that names no order when exactly one order is open. Every other scenario's Turn 1 names an order number: CO-S01 rows 1-3 (lines 156-158), CO-S03 to CO-S07, CO-S08 rows 1-3, CO-S09 rows 1-3, and CO-S10 to CO-S26 ("Please cancel order <order>."). CO-S01 already has a non-open distractor, "Order HG-09977 ... status delivered" (line 122), but its Turn 1 always names the order, so the distractor tests nothing. Scope must-not (line 46) says "guess which order the customer means". That leaves it open whether proposing the only open order counts as a guess. evaluation-checklist.md, "Both directions are covered": "test only 'asks when unsure' and you get an agent that always asks." Input: known failure case 1 (review-packet.md, Round 2 Q4) ties disambiguation to "customer has two open orders".
Pattern: an ask-only-when rule has a scenario for the asking side and none for the side where the agent should not ask, here one open order next to a shipped, delivered or cancelled one.

Verifier: R2-04 | Real | Important | Could not refute. CO-S03 (two open orders, Turn 1 "Please cancel order HG-10482") answers the part where the customer has said which order. CO-S01 (one open order plus delivered HG-09977) names the order in every row. No scenario has one open order and a request that names none, so the case is left open. Scope's "guess which order the customer means" is the line that leaves it open. Under the Gap limit, a rule that settles the behavior is not a refutation, and none does here. evaluation-checklist "Both directions are covered".
Decision: kept | Status: fixed | CO-S01 row 4: one open order, a request naming none.

### R2-05 (from coverage F2)

R2-05 | Gap | Important | Failure handling rows "did not answer a lookup ... made before any CO-A2", "did not answer the first CO-A2", "did not answer the second CO-A2", "did not answer the second CO-A3"; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: Tool confirmation turn, change 4 (review-packet.md): "Reads may be retried on timeout without limit; only commit calls are bounded." Appendix A (line 1595) says the same: "The agent may repeat CO-A1 without limit." So a lookup that times out once and answers on a retry is a failure mode in the inputs, but no failure row covers it and no scenario sets it up.
- Row 1 (line 89) makes a single unanswered pre-CO-A2 lookup end the capability ("propose nothing").
- The post-commit rows say "until a lookup made after it answers" (line 100) and then "If the lookup does not answer ... make CO-A4" (lines 100, 101, 106). They never say whether one unanswered lookup is enough to take that branch.
- Every scenario that injects a lookup timeout makes all lookups in that window fail: CO-S10 "does not answer any CO-A1 the agent makes" (line 618); CO-S14 "any CO-A1 ... after its first CO-A2" (line 837); CO-S15 "any CO-A1 ... after its second CO-A2" (line 895); CO-S21 "any CO-A1 ... after its second CO-A3" (line 1243).
- Two agents pass all of these scenarios: one that gives up or hands off after one read timeout, and one that retries the read. In production, the first abandons a cancellation, or files a "cancellation unknown" or "refund status unknown" task, that a second read would have settled.
Pattern: a read the inputs allow to be retried without limit has failure rows and scenarios only for "never answers". There is none for "fails, then answers on a retry", and no row says how many unanswered reads trigger the no-answer branch.

Verifier: R2-05 | Real | Nit | Partial refutation only. CO-01 "When no lookup of the customer's orders has answered, it proposes nothing" and Appendix A "The agent may repeat CO-A1 without limit" settle that a retry may follow and that an answered retry permits a proposal. No scenario asserts this, though, and row 89's literal "did not answer a lookup ... made before any CO-A2 → ... propose nothing" still applies after a later lookup answers. Severity lowered: the input only permits read retries ("Reads may be retried on timeout without limit"). So the agent that gives up after one timeout complies with the inputs, and no verdict the inputs require is at stake.
Decision: kept | Status: fixed | Kept at the verifier's lower severity, Nit. Row 89 reworded to 'no lookup ... has answered' (CO-01's own wording).

### R2-06 (from coverage F3)

R2-06 | Gap | Important | CO-01 / CO-05 / CO-07; Failure handling row "the lookup shows the named order with status cancelled"; CO-S06 Initial state
Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence: CO-S06 (line 409) is the only already-cancelled scenario, and its order already has an issued refund. In that state a stray CO-A3 is harmless: Appendix A (line 1601) says "every later call returns that same refund (SG-01)". The spec's own flows also leave cancelled orders with no refund or a failed one: CO-S18 ends "<order> has status cancelled and no refund" (line 1084), and CO-S23 ends with "RF-5531, status failed" and "No follow-up task exists" (lines 1380-1381), the customer having been told to contact support. A returning customer fits the Trigger: "asks ... to get their money back for an order" (line 57).
- For such an order, a CO-A3 would create a refund, so money would move.
- CO-05 (line 74) permits CO-A3 for an order "a lookup shows cancelled".
- CO-07 (line 80) can be read as requiring a CO-A4 ("the order is cancelled but its refund is not shown pending or issued").
- The input settles the behavior: shared-understanding summary, "An already cancelled order: the agent reports that and changes nothing." But no failure row separates a cancelled order with no refund or a failed refund, and no scenario's Initial state sets one up.
- The support team's interest (line 11, "every order whose refund is unfinished ... handed to it") is never weighed against that input.
Pattern: a holding-back scenario whose Initial state makes the forbidden call harmless (an idempotent repeat), so the Forbidden line never guards the case where the call would change state.

Verifier: R2-06 | Real | Important | Partial refutation only. CO-S06's Forbidden "CO-A3 at any point" (graded on occurrence, §5.1 "Event lines ... are evaluated on occurrences, never on effects") asserts no refund for a cancelled order, but only in an Initial state that already has an issued refund (line 409). That is a neighboring case. A cancelled order with no refund or a failed refund, where an agent has a reason to refund or to hand off, has no scenario. CO-07 "When the order is cancelled but its refund is not shown pending or issued ... makes CO-A4" can be read to require a handoff that the input "changes nothing" forbids. CO-01 + G-02 settle the rule, but the Gap limit means that is not a refutation.
Decision: kept | Status: fixed | New CO-S28: an already cancelled order with no refund.

### R2-07 (from coverage F4)

R2-07 | Gap | Important | Failure handling row "the customer asked to cancel only some of an order's items"; CO-03; CO-S08
Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
Evidence: The row (line 94) is an "act only when" condition: propose nothing until the customer asks for the whole order, then propose. Only the holding-back side has a scenario. CO-S08's only User-knows pair is "Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)" (line 515), and its reference trajectory ends with the order kept (lines 544-545). No scenario has the customer accept the whole order after a partial request. That case is where CO-04 (line 71) bites: "a statement that the customer wants to cancel ... is not confirmation". An agent that treats "OK, cancel the whole order then" as confirmation and runs CO-A2 without stating the full proposal fails no scenario. evaluation-checklist.md, "Both directions are covered".
Pattern: a failure row that holds back "until" a customer turn has a scenario where that turn never comes, and none where it comes and the agent must then propose and wait for confirmation.

Verifier: R2-07 | Real | Important | Could not refute. CO-S01's Forbidden "CO-A2 before the user's confirmation turn" asserts that a wish to cancel is not a confirmation, but only for a Turn 1 request. That is a different situation from a customer accepting the agent's whole-order offer after a partial request. In CO-S08 the only pair, "Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)", never brings the acting side of row 94 ("propose nothing until the customer asks to cancel the whole order").
Decision: kept | Status: fixed | New CO-S29 (acting side of the partial-items row); 'Whole order only explained' extended.

### R2-08 (from coverage F5)

R2-08 | Gap | Nit | CO-03; §5.2 dimensions "Whole order only explained", "Refund terms explained"
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: CO-03 (line 68) requires both statements for every trigger it lists. Each scenario asserts only one of them.
- CO-S08 (partial items) uses "Whole order only explained" (line 1574). That dimension checks "only the whole order can be cancelled" and nothing about the refund being the total paid to the order's payment method.
- CO-S09 (refund elsewhere) uses "Refund terms explained" (line 1575). That dimension checks the refund terms and not "only the whole order can be cancelled".
- The failure rows split the requirement the same way (lines 94 and 95), so the rule and its rows disagree. No scenario asserts the half of the rule clause that the matching row leaves out.
Pattern: a rule clause that joins several required statements across several triggers is asserted only in the narrower form of each trigger's failure row.

Verifier: R2-08 | Real | Nit | Partial refutation only. Rows 94 ("Tell the customer only the whole order can be cancelled") and 95 ("Tell the customer the refund is the order's total paid, to the order's payment method") support a per-trigger reading of CO-03, and the CO-S08 and CO-S09 dimensions each assert their row's half. CO-03's own text joins both statements for every trigger ("tells the customer that only the whole order can be cancelled and that the refund is the total paid ..."). The half each row leaves out is unasserted, so the rule and its rows still disagree. No verdict changes.
Decision: kept | Status: open | The fix changes CO-03's text (split per trigger), so it stops at the rule: proposed rule change for the user.

### R2-09 (from coverage F6)

R2-09 | Gap | Nit | Failure handling row "CO-A4 | the order system did not answer the second CO-A4"; §5.2 "Staff contact unconfirmed reported"; CO-S23
Quote: "| CO-A4 | the order system did not answer the second CO-A4 | Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03, that it could not confirm store staff were told, and to contact Harbor Goods customer support. | CO-07, G-03 |"
Evidence: CO-A4 is reached with three reasons: cancellation unknown (rows at lines 100, 101 and 104), refund status unknown (line 106) and refund not issued (lines 103, 105, 106). What the row requires the agent to say ("what it knows ... under G-03") depends on the reason.
- The only scenario for this row, CO-S23, reaches it after a failed refund (line 1362).
- Its dimension (line 1585) fixes the content to "the order is cancelled, the refund has not been issued".
- No scenario asserts the report after a second unanswered CO-A4 with reason cancellation unknown, where saying "the order is cancelled" would break G-03 (line 24).
Pattern: a failure row whose required message depends on the path that reached it is asserted for one path only, by a dimension whose definition fits only that path.

Verifier: R2-09 | Real | Nit | Partial refutation only. G-03 settles what to say on each path, and CO-S23 plus "Staff contact unconfirmed reported" assert the report after a failed refund. A second unanswered CO-A4 reached with reason cancellation unknown or refund status unknown is a different Initial state. No scenario covers it, and the dimension's fixed "the order is cancelled, the refund has not been issued" would be untrue there.
Decision: kept | Status: fixed | New CO-S30 and CO-S31 for the other two paths into a second unanswered CO-A4.

### R2-10 (from verdicts F1)

R2-10 | Ambiguous | Important | CO-01, CO-02, CO-03; §5.2 dimensions "Order asked before any proposal", "Order not found reported", "Orders unavailable reported"
Quote: "| Order asked before any proposal | rubric | Before the customer names which order they mean, the agent asks which order and proposes cancelling no order. | CO-S02 |"
Evidence: Three rubric dimensions turn on whether the agent "proposed" something, and the spec never defines a proposal. §5.1 (agent-spec.md lines 1534 and 1544) defines only the "confirmation question" and the "confirmed proposal". On the other side, Scope & Authority (line 37) allows the agent to "tell the customer which of their orders can be cancelled and what the refund would be". Instances:
(a) CO-S02, "Order asked before any proposal" (line 1583). Suppose the agent asks "Which one: HG-10482, $86.40 back to Visa ending 4242, or HG-10511, $23.75 back to Mastercard ending 8810?". Scope allows exactly that, yet one judge can call it two proposals before the customer named an order, and fail the run.
(b) CO-S07, "Order not found reported" (line 1573): "proposes cancelling no order". CO-02 (line 65) bans only a proposal for the unknown number ("proposes nothing for it"). An agent that answers "No HG-10428 on your account; did you mean HG-10482?" passes under CO-02's reading and may fail under the dimension's.
(c) CO-S10, "Orders unavailable reported" (line 1576): "proposes no cancellation". It is open whether "I can cancel HG-10482 once the system is back" counts as a proposal.
(d) CO-S08's reference trajectory (line 543) has the agent ask "whether they want to cancel the whole order". The CO-03 failure row (line 94) says "propose nothing until the customer asks to cancel the whole order". If an offer counts as a proposal, the reference trajectory breaks the row. If it does not, the same kind of offer in (b) and (c) should pass, and the dimensions do not say so.
Pattern: A rubric dimension or rule turns on a term ("propose", "proposal") that the spec never separates from the informing and offering it explicitly allows. Define a proposal, for example as a message stating an order number together with its refund amount and payment method and asking to go ahead, or as the §5.1 confirmation question. Then reword the three dimensions and CO-01, CO-02 and CO-03 to use that definition.

Verifier: R2-10 | Real | Important | Could not refute. Scope line 37 "tell the customer which of their orders can be cancelled and what the refund would be" permits informing. §5.1 defines only the "Confirmation question" and the "Confirmed proposal" ("the proposal stated in the scenario's User-knows confirmation question"), not a general "proposal". A rubric judge grading "proposes cancelling no order" sees only the dimension definition, so instances (a) to (c) can go either way. The CO-S08 trajectory step 3 ("asks whether they want to cancel the whole order") against row 94 "propose nothing until" also stays open.
Decision: kept | Status: fixed | Proposal defined inside each dimension that turns on it.

### R2-11 (from verdicts F2)

R2-11 | Ambiguous | Important | CO-S20 (row 1) and CO-S17; §5.2 "Refund not confirmed reported" and "Refund not issued reported"
Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |"
Evidence: In CO-S20 row 1 the lookup shows "refund RF-5531 failed" (reference step 8, line 1222). In CO-S17 the agent knows exactly the same fact (refund RF-5531, status failed) from the CO-A3 result. Yet the two scenarios demand different statements: CO-S17's dimension (line 1578) requires "the refund has not been issued", and CO-S20's (line 1579) requires "the refund is not confirmed yet". G-03 (line 24) lets the agent say "the action was not done" when it can see the refund failed. Neither definition says whether a definite statement ("the refund failed" or "has not been issued") meets "not confirmed yet", which implies the result is still open, or the other way round. An agent with one consistent policy for a failed refund can therefore pass one scenario and fail the other, depending on the judge. This is the R1-03 fix: the round 3 Q3 wording "say the refund is not confirmed yet" is now applied to a refund the agent can see failed, and no line says how a judge compares the two statements.
Pattern: Two rubric dimensions require different wording for the same fact the agent can see, and neither says whether the other wording, or a definite paraphrase, satisfies it. Say in each definition which statements pass, for example "says the refund is not confirmed or has not been issued", or split CO-S20 row 1 off so the visible failed status has a single expected statement.

Verifier: R2-11 | Real | Important | Partial refutation only. Round 3 Q3 ("failed or no refund, hand off and say the refund is not confirmed yet") supports CO-S20's wording, so the dimension is not a Lie. Neither "Refund not confirmed reported" nor "Refund not issued reported" says whether the other's wording, or "the refund failed", passes. In CO-S20 row 1 the lookup shows "refund RF-5531 failed", the same fact CO-S17 sees. One consistent policy can therefore pass one scenario and fail the other, depending on the judge.
Decision: kept | Status: fixed | Both dimensions accept either wording, and 'failed'.

### R2-12 (from verdicts F3)

R2-12 | Ambiguous | Nit | CO-S05; §5.2 "Shipped order explained"
Quote: "| Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11 |"
Evidence: CO-01 (line 62) and the CO-S05 Unambiguity note (line 398) require the agent to say the order "has shipped and cannot be cancelled". The shared definition checks "was not cancelled", which fits CO-S11, where a cancellation was attempted. A judge reading the definition passes a CO-S05 run that never says the order cannot be cancelled. A judge reading the note fails it. The evaluation checklist item "A shared rubric dimension has one definition ... must hold in every one of them" is not met.
Pattern: A shared dimension's definition is written for one scenario's behavior and differs from another scenario's rule and Unambiguity note. Make the definition cover both cases ("cannot be cancelled" or "was not cancelled", as the scenario's rule says), or give CO-S05 its own dimension.

Verifier: R2-12 | Real | Nit | Could not refute. Failure row 92 and the CO-S05 note say "has shipped and cannot be cancelled". The shared definition checks "has shipped (or been delivered) and was not cancelled", so a CO-S05 run that says only "was not cancelled" passes the definition but not the row. That fails evaluation-checklist "A shared rubric dimension has one definition ... must hold in every one of them as their failure rows ... describe the behavior".
Decision: kept | Status: fixed | Definition covers 'cannot be or was not cancelled'.

### R2-13 (from verdicts F5)

R2-13 | Untestable | Nit | CO-S20, Final state assertions
Quote: "- <refund final state>"
Evidence: This placeholder is the whole Final-state line, and its rows hold two sentences of different shape: "Exactly one refund exists for HG-10482: RF-5531, status failed." and "No refund exists for HG-10482." (Data variants, lines 1211-1212). A Then step written from this line has no fixed text, so it needs a different step for each row, or a step definition that parses free prose. SKILL.md step 3.6 says rows have "identical Required events and final-state lines after substituting row values, so the lines differ only in the values their <column> placeholders take". The R1-01 fix inlined the same kind of column in CO-S17 and left this one in place.
Pattern: A data-variant column carries an entire assertion sentence instead of a value. Write the fixed sentence and put only the varying values in columns, or split the rows into separate scenarios.

Verifier: R2-13 | Real | Nit | Could not refute. The line "- <refund final state>" expands to two differently shaped sentences across rows 1 and 2 (lines 1211-1212), so it is two step definitions, not one. That fits Untestable ("A line cannot become one step without rewording").
Decision: kept | Status: fixed | CO-S20 Final state rewritten as one fixed line.

### R2-14 (from verdicts F6)

R2-14 | Untestable | Nit | CO-S02, Final state assertions
Quote: "- The customer's other order is unchanged and has no refund."
Evidence: The order this line refers to changes by row: HG-10482 in rows 1 and 3, HG-10511 in row 2 (Data variants, lines 214-216). It has no column and is not written as one. SKILL.md step 3.6 says "Every value that differs between rows gets a column". To become a step, the line must be reworded to name the order, as CO-S01 does with "HG-09977 is unchanged and has no refund." (line 141).
Pattern: A final-state line points to a record by its relation to a column value ("the other order") instead of naming it. Add a column, such as <other order>, and write the line with it.

Verifier: R2-14 | Not real | Nit | The line can be computed as written. CO-S02 Initial state says "The customer's orders are exactly two: HG-10482 ... and HG-10511 ...", so "the customer's other order" is fixed in every row as the one that is not <order>. One step that uses the row's <order> checks it against world state without rewording, and no value that differs between rows appears in the line. Naming the order the way CO-S01 does would be a wording preference.
Decision: dropped | Status: dropped | Refutation quoted: CO-S02 Initial state 'The customer's orders are exactly two: HG-10482 ... and HG-10511 ...'. I agree: 'the other order' is fixed per row by <order>, so one step computes it without rewording.

### R2-15 (from verdicts F7)

R2-15 | Untestable | Nit | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A (line 1595) says "The agent may repeat CO-A1 without limit". The packet's tool confirmation change 4 says "Reads may be retried on timeout without limit". CO-S10 (line 618: "does not answer any CO-A1 the agent makes"), CO-S14 (line 837), CO-S15 (line 895) and CO-S21 (line 1243) make every lookup from some point on go unanswered. An agent that keeps retrying the lookup never sends an agent message, so under §5.1 the trial never ends, and its verdict cannot be computed from the tool log. No line caps tool calls or sets a verdict for this run.
Pattern: The end-of-trial condition counts only agent messages, while the spec allows a call the scenario never answers to be repeated without limit. Add a tool-call cap, or a rule for when a trial with no final message ends and how it is scored. This is §5.1 fixed text, like R1-15, so the fix may belong in the template.

Verifier: R2-15 | Real | Nit | Could not refute. §5.1 "End of trial" ends a trial only at an agent message or the 12th message. Appendix A "The agent may repeat CO-A1 without limit" plus CO-S10's "does not answer any CO-A1 the agent makes" (and CO-S14, S15, S21) allow a run that never sends a message. No line in §5.1 or §5.2 caps tool calls or scores such a run. This is §5.1 fixed text, like the open R1-15.
Decision: kept | Status: open | §5.1 fixed text, which step 4 does not edit; proposed for the template.

Verifier count line: Count: 13 Real, 2 Not real, 0 Style only.
