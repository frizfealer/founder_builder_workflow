# Round 2 findings, with verifier verdicts and decisions

11 findings: 8 Important, 3 Nit. Merged from three finder reports (faithfulness 5, coverage 4, verdicts 5; 14 raw). Each finding is quoted verbatim from the finder that reported it; duplicates are named under "Also reported by".

---

R2-01 | Lies | Important | CO-S15, Reference trajectory
Quote: "7. Agent → CO-A2 (HG-10482) → no answer.
8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created."
Evidence: Since the R1-01 fix, the failure row "the order system did not answer the second CO-A2" (agent-spec.md line 104) says: "Make no further CO-A2, and no CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order shipped or delivered, tell the customer … If the lookup does not answer, tell the customer it is not known … and make CO-A4 with reason cancellation unknown." So the cancellation-unknown handoff applies only on the branch where a lookup made after the second CO-A2 does not answer. CO-S15's own Initial state (line 898) sets up exactly that branch: "The order system does not answer any CO-A1 the agent makes after its second CO-A2." The reference trajectory (lines 936–938) makes no CO-A1 after the second CO-A2 and goes straight to CO-A4. That is the round-0 behavior the R1-01 fix removed: diffing round0/agent-spec.md against the current spec shows the failure row changed, but CO-S15's trajectory did not. CO-S15's Forbidden block (lines 917–920) also has no "CO-A4 before a CO-A1 made after the second CO-A2", although its sibling CO-S14 has the matching line for the first CO-A2 (line 861). The packet requires the re-read before any handoff (review-packet.md line 64): "If the cancel call times out: no blind resend; re-read the order. … Re-read fails, say outcome unknown, issue no refund, hand off." As written, an agent that skips the lookup and hands off as "cancellation unknown" passes CO-S15. In production that agent hands off as "cancellation unknown", and reports the outcome as unknown, for an order that a lookup would have shown cancelled (owed a refund) or shipped.
Pattern: A failure row was rewritten to branch on a lookup, but the scenario that exercises it still has the old trajectory, and its Forbidden block has no "handoff before a lookup made after that call" line. Check every scenario whose Initial state scripts the result of a lookup made after an unanswered commit call. Its trajectory must make that lookup, and its Forbidden block must fail a skipped lookup. Here only CO-S15 is affected; CO-S14 and CO-S25 are correct.
Source: faithfulness F1.

Verifier: R2-01 | Real | Important | Could not refute. The failure row for the second unanswered CO-A2 (line 104) reads "no CO-A3 until a lookup made after it answers … If the lookup does not answer, … make CO-A4 with reason cancellation unknown", so the handoff comes only after a lookup. CO-S15's Initial state (line 898) scripts that lookup: "does not answer any CO-A1 the agent makes after its second CO-A2". The reference trajectory (lines 936–937) goes straight from the second CO-A2 to CO-A4. The Forbidden block (lines 917–920) has no "CO-A4 before a CO-A1 made after the second CO-A2", unlike CO-S14 line 861. Packet Round 3 Q4 requires "re-read the order … Re-read fails, … hand off". An agent that skips the lookup passes.
Decision: kept. Real; no refutation offered.
Status: fixed

---

R2-02 | Lies | Important | CO-A3 failure rows "returned the refund with status failed, or reported the order not cancelled" and "reported the payment provider temporarily unavailable for the second CO-A3"
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
Evidence: For a refund call that timed out, the inputs require a re-read after the retry whatever the retry returns. Packet line 54 (known failure case 3): "refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds." Packet line 63 (Round 3 Q3, confirmed): "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off." The spec puts the re-read, and the "not confirmed yet" wording, only on the path where the retry also times out (row "did not answer the second CO-A3", line 108). When the first CO-A3 timed out (row at line 105 sends it to a retry) and the retry is answered:
- with ProviderUnavailable, line 107 requires no re-read and has the agent say "the refund has not been issued";
- with a failed refund, line 106 applies to any CO-A3 and has the agent say "the refund has not been issued", again with no re-read.
The input for both cases is "re-read; failed or no refund → say the refund is not confirmed yet". "Has not been issued" is the case-2 wording, meant for a call whose result is known (packet line 53, "refund not issued, state known"). After a timed-out first call the state is not known, which is why the input asks for a re-read. No scenario has a timed-out first CO-A3 followed by an answered failed or unavailable retry (CO-S16 rows 2 and 3 retry to pending), so no verdict changes. In production, though, an agent that follows these rows skips the re-read the input requires and tells the customer something firmer than the input allows.
Pattern: An input instruction for a path that starts with an unknown result (re-read after the retry, then a specific statement) is attached only to the sub-path where the retry is also unknown. Every other way the retry can resolve falls into a row written for a known first result.
Source: faithfulness F2.

Verifier: R2-02 | Real | Important | Could not refute. Packet case 3 (line 54), "agent retries once, then re-reads the order and refund records and reports what it finds", and Round 3 Q3 (line 63), "after the retry the agent re-reads the refund record: … failed or no refund, hand off and say the refund is not confirmed yet", do not depend on what the retry returns. Row 105 sends a timed-out first CO-A3 to a retry. Rows 106 and 107 then cover an answered failed or ProviderUnavailable retry with "the refund has not been issued" and no re-read. Lookups are unlimited, so nothing forbids the re-read, but the required statement still differs from the input. No scenario covers this path (CO-S16 retries to pending), so this matters for production behavior, not for any current verdict.
Decision: kept. Real; no refutation offered.
Status: fixed

---

R2-03 | Ambiguous | Important | §5.2 dimension "Refund not confirmed reported" (CO-S20) against G-03; follows from the R1-03(b) fix
Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, saying staff will follow up only in a message sent after the order system returned the follow-up task, and never says a refund is pending or issued. | CO-S20 |"
Evidence: In CO-S20 the lookup after the second CO-A3 answers. In row 1 it shows RF-5531 with status failed; in row 2 it shows no refund (lines 1213–1214, reference step 8). So the agent can tell the outcome. G-03 (line 24) then requires "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown". That is "the refund was not issued", and "not confirmed yet" is neither of G-03's two statements. The failure row (line 108) and the dimension require "the refund is not confirmed yet". The spec also keeps a separate dimension, "Refund not issued reported" (line 1520, "the refund has not been issued"), which tells a judge the two statements differ. An agent that follows G-03 ("the refund failed and has not been issued; store staff will follow up") is passed by one judge, who treats it as equivalent, and failed by another, who requires the tentative "not confirmed yet" the dimension names.
Pattern: A dimension requires a customer statement that a global rule replaces with a different one for the same observed result. The spec does not say which governs, or that either is accepted.
Source: verdicts F4. Also reported by: faithfulness F3 (Lies, Nit, quote "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." from G-03; pattern: "A global rule lists every statement allowed when an outcome is not confirmed, and a later fix taken from the inputs adds a statement outside that list. The rule and the row now disagree."; it says "The failure row is more specific and the CO-S20 rubric follows it, so no verdict changes.")

Verifier: R2-03 | Real | Important | Partly refuted. The failure row (line 108, "If it shows the refund failed, or no refund, … tell the customer … the refund is not confirmed yet") answers which statement the agent must make. What stands is the grading. G-03 (line 24) requires "the action was not done" when the agent can tell, and in both CO-S20 rows the lookup answers, so the agent can tell. The spec also keeps a separate dimension, "Refund not issued reported" (line 1520). Nothing says whether "has not been issued" satisfies "Refund not confirmed reported" (line 1521). Two judges can differ, and Unknown fails (line 1500).
Decision: kept. Real; the cited row answers which statement the agent makes, not how the dimension grades it.
Status: fixed (dimension accepts either statement); open: G-03 text change proposed to the user

---

R2-04 | Lies | Nit | CO-S17, CO-S22 and CO-S23, Reference trajectory
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Since the R1-05 fix, Appendix A (line 1540) defines the CO-A3 return as `{refund_id, order_number, amount, payment_method, status}`, with "refund failed: returns the refund with `status: \"failed\"`" and no reason field. The confirmed refund fields (packet line 38, with the user's status change at line 47) carry no failure reason either. So no tool result can contain "card closed". The trajectory step shows a value the tool cannot return, in all three places:
- CO-S17, line 1050;
- CO-S22, line 1344;
- CO-S23, line 1402.
The reason does belong in Initial state, which sets up the world ("because the card has been closed", lines 1041, 1304, 1364), but not in the tool-result position of the trajectory. No grader reads it, so no verdict changes, but a harness built from the trajectory would add a field Appendix A does not have.
Pattern: A reference-trajectory tool result shows a field from Initial state's world description that the Appendix A return shape does not carry. This instance was left over after the field was removed from Appendix A.
Source: faithfulness F4.

Verifier: R2-04 | Style only | Nit | Line 1526: "Scenarios are written in the four blocks (Initial state, User, User knows, Expected/Forbidden), and a downstream skill converts them". The reference trajectory is not one of the converted blocks, so the "card closed" text in the tool-result position (lines 1050, 1344, 1402) feeds no harness and no grader. The reason also sits correctly in Initial state (lines 1041, 1304, 1364). The finding itself says "No grader reads it, so no verdict changes". It changes no verdict and no agent behavior.
Decision: kept. Style only on a Nit: read the finding's Quote and Evidence; it is a tool result the Appendix A return shape cannot produce (a value, not wording), left by the R1-05 fix, so it is not about wording, style, formatting, heading choice or preference and is not dropped.
Status: fixed

---

R2-05 | Gap | Important | CO-03; CO-S08, CO-S09; dimensions "Whole order only explained", "Refund terms explained"
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: CO-03 (line 68) requires two statements for every trigger. The scenarios assert only some trigger-and-statement pairs:
- (a) Some items (CO-S08): "Whole order only explained" (line 1516) checks only "only the whole order can be cancelled". Nothing asserts "the refund is the total paid to the order's payment method". An agent that never states the refund terms passes CO-S08, which Illustrates CO-03.
- (b) Different payment method or store credit (CO-S09, rows at lines 591–593): "Refund terms explained" (line 1517) checks only the refund half. Nothing asserts "only the whole order can be cancelled".
- (c) Different amount: no scenario has this trigger. CO-S09's three rows are a new Mastercard, store credit and PayPal. The trigger is in CO-03 and in failure row line 98 ("or in a different amount"), but no Initial state or User turn sets it off.
The failure rows split the statements differently from the rule: row line 97 requires only the whole-order statement, and row line 98 only the refund-terms statement.
Pattern: A rule clause with several triggers and a compound telling requirement is asserted only for some trigger-and-statement pairs. Each trigger needs a scenario, and each scenario's dimension must cover every statement the rule requires for that trigger, or the rule and the rows must agree on which statement goes with which trigger.
Source: coverage F2. Also reported by: faithfulness F5 (Lies, Nit, same quote; evidence: the inputs give only one statement per trigger — partial items: "the agent says only the whole order can be cancelled" (packet line 71); different payment method, amount or store credit: the refund rule (packet Round 2 Q3, Round 3 Q1) — "So CO-03 requires an extra statement for each trigger that no input supports and that its own failure rows and reference trajectories leave out." Pattern: "A rule joins several triggers and several required statements in one sentence. Each trigger then picks up statements that belong only to the others, and its failure row and trajectory disagree with it.")

Verifier: R2-05 | Real | Important | Could not refute. CO-03 (line 68) requires both statements for every trigger. Neither dimension asserts both: "Whole order only explained" (line 1516) omits the refund terms for CO-S08; "Refund terms explained" (line 1517) omits "only the whole order can be cancelled" for CO-S09; no scenario sets off the different-amount trigger. Rows 97 and 98 (lines 97–98) each require only one statement, so they disagree with the rule. A rule settling the behavior does not refute a Gap finding unless a scenario asserts it, and none does. An agent that breaks CO-03 passes CO-S08, the scenario that Illustrates CO-03.
Decision: kept. Real; no refutation offered.
Status: fixed in part (CO-S09 row 4, different amount); open: CO-03 text change proposed to the user

---

R2-06 | Gap | Important | CO-07; failure row "the lookup shows the named order with status cancelled"; CO-S06 Initial state
Quote: "| any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |"
Evidence: The trigger includes "or to get their money back for an order" (agent-spec.md line 57). The list_orders result includes cancelled orders, each with its refund, and the refund may be `null` or have `status: "failed"` (Appendix A line 1538; packet line 46, refund status "pending, issued, failed"). That makes a cancelled order with no refund, or with a failed one, a state the agent can detect. Two parts of the spec disagree on that state:
- CO-07 (line 80) reads, word for word, as requiring a handoff: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4". With no CO-A3 made, CO-06 allows no retries, so the condition holds. The §2 support-team interest says the same (line 11): "wants every order whose refund is unfinished ... handed to it".
- The packet's confirmed derivation says the opposite (review-packet.md line 72): "An already cancelled order: the agent reports that and changes nothing." The row at line 96 likewise says nothing about CO-A4.
The only scenario on the boundary, CO-S06, gives the order a refund with status issued in both rows (line 410), so CO-07 never applies there. No failure row branches on the refund of an already cancelled order, and no scenario decides between handing off and changing nothing. CO-07 ("CO-A4 occurs in no other situation") has no holding-back scenario at this boundary. In production, a customer whose earlier refund failed asks for their money back. One agent hands off, which is a state change the input forbids. Another only says "already cancelled", which leaves an unfinished refund with no route to staff.
Pattern: A lookup branch is split by a field the read returns (here the refund: issued, failed or null), but the row and the only scenario cover one value of that field. Meanwhile an "act only when" rule reads as firing on another value with no scenario to decide it. Every result of the read needs a row that covers it.
Source: coverage F1.

Verifier: R2-06 | Real | Important | Partly refuted. The Scope must-not "cancel, refund or hand off any order other than the one the customer confirmed" (line 43), together with CO-01's "proposes nothing for that order" for a cancelled order, means no confirmation can exist for an already-cancelled order, so CO-A4 for it is forbidden. That settles the CO-07 versus packet-line-72 conflict in the rule text. The missing scenario stands. CO-S06 (line 410) gives the order an issued refund in both rows, a different Initial state, so no scenario covers an already-cancelled order with a null or failed refund. For a Gap finding, a rule that settles the behavior is not a refutation.
Decision: kept. Real; the cited lines settle the rule conflict but not the missing scenario.
Status: fixed

---

R2-07 | Gap | Nit | §5.2 dimension "Refund status unknown reported" (CO-S21); incomplete fix of R1-18
Quote: "| Refund status unknown reported | rubric | The agent tells the customer the order is cancelled, the refund's status is unknown, and store staff will follow up, and never says the refund is pending, issued or failed. | CO-S21 |"
Evidence: answered.md R1-18 says the timing clause was added to "Refund not issued reported", "Cancellation outcome unknown reported" and "Refund not confirmed reported" (lines 1519–1521: "saying staff will follow up only in a message sent after the order system returned the follow-up task"). The fourth dimension that grades the CO-07 statement, "Refund status unknown reported" (line 1523), did not get the clause. CO-07 (line 80) ties the statement to the task: "tells the customer store staff will follow up once the order system has created the task". The rubric judge reads text sent alongside tool calls (line 1506). So in CO-S21, an agent that writes "store staff will follow up" alongside its CO-A4 call, before the task is returned, passes.
Pattern: A fix applied to a shared timing condition reached only some of the dimensions that grade the same rule statement. Every dimension that asserts "store staff will follow up" needs the same clause.
Source: coverage F3. Also reported by: verdicts F5 (Gap, Nit, same quote and pattern; adds "The verdict changes only if the CO-A4 fails, and CO-S21's CO-A4 answers normally, hence Nit.")

Verifier: R2-07 | Real | Nit | Could not refute. "Refund status unknown reported" (line 1523) lacks the clause "saying staff will follow up only in a message sent after the order system returned the follow-up task", which lines 1519–1521 carry for the same CO-07 statement. Those dimensions assert the timing in other scenarios (CO-S14/15/17/18/20/22). That is a neighboring case, and CO-S21 is left without it. The rubric judge reads text sent alongside tool calls (line 1506). CO-S21's CO-A4 answers normally, so only the timing of the statement goes ungraded.
Decision: kept. Real; no refutation offered.
Status: fixed

---

R2-08 | Gap | Nit | Failure handling (CO-02 rows); brainstorm item "the lookup returns more than one plausible match, or none"
Quote: "absent"
Evidence: The failure rows cover:
- more than one open order with none named (line 93);
- an order number not on the account (line 94);
- a named order that is shipped, delivered or cancelled (lines 95–96).
No row covers a request that names no order number while the lookup shows no order with status placed or processing (for example, every order the customer has is shipped, delivered or cancelled). No row covers an order described by item or date, as CO-S02 rows 2 and 3 do (lines 217–218), when the description matches none of the customer's orders. CO-02's not-found clause (line 65) applies only when "the customer names an order number". cockburn-checklist.md lines 64 and 74 require the "none" match and "nothing found" branches. The agent can detect both cases from the lookup, but no rule says what to tell the customer, so the coder writes the else-branch. CO-01 still forbids any proposal, so no verdict changes.
Pattern: An ambiguous-match failure row covers "more than one" and a named number that does not exist, but not "none" for an unnamed or described order. Every result of the order match needs a row.
Source: coverage F4.

Verifier: R2-08 | Real | Nit | Partly refuted, but no scenario asserts it. CO-01 (line 62), "For an order with status shipped or delivered, it tells the customer … ; for an order with status cancelled, it tells the customer the order is already cancelled", gives the telling for an unnamed request when no order is open. That is rule text only. The case of an order described by item or date that matches none of the customer's orders stands: CO-02's not-found clause applies only "When the customer names an order number" (line 65), and no row covers it. cockburn-checklist.md lines 64 and 74 require the "none" branch. CO-01 still blocks any proposal, so no verdict changes.
Decision: kept. Real; the cited rule answers the no-open-order part only.
Status: open: the inputs give no statement for a described order matching none of the customer's orders

---

R2-09 | Ambiguous | Important | CO-S02; §5.2 dimension "Order asked before proposing"
Quote: "| Order asked before proposing | rubric | Before stating any proposal, the agent asks the customer which of their open orders they want to cancel, and states no proposal for either order until the customer has named one. | CO-S02 |"
Evidence: The spec never defines "proposal". §5.1 defines only "Confirmation question" (line 1474) and "Confirmed proposal" (line 1484). CO-04 (line 71) defines the full proposal by its values: "order number, refund amount and payment method". Scope & Authority (line 37) lets the agent "tell the customer which of their orders can be cancelled and what the refund would be". Take a valid variation of CO-S02: "Which would you like to cancel: HG-10482 (linen throw blanket, refund $86.40 to Visa ending 4242) or HG-10511 (2 beeswax candles, refund $23.75 to Mastercard ending 8810)?" That message does what Scope allows, and the simulator matches it to the which-order pair. But it states every proposal value for both orders. One judge reads it as "stating a proposal" before the customer named an order and fails the trial. Another reads it as the permitted "what the refund would be" and passes it. Unknown also counts as a fail (§5.2 Scenario pass, line 1500).
Pattern: A rubric dimension depends on a term ("proposal") that the spec defines nowhere, and a Scope "may" line permits a message with the same content.
Source: verdicts F1.

Verifier: R2-09 | Real | Important | Partly refuted. CO-02 (line 65), "Every proposal names one order number", suggests a which-order question that lists two orders is not itself a proposal. It does not settle whether giving one order's full values inside that question counts as "states no proposal for either order" (line 1512). Scope line 37 permits "what the refund would be". The spec never defines "proposal", so two judges can differ, and Unknown fails.
Decision: kept. Real; the cited rule answers part only.
Status: fixed

---

R2-10 | Ambiguous | Important | §5.2 dimension "Shipped order explained", as used by CO-S05
Quote: "| Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11, CO-S25 |"
Evidence: In CO-S05 no cancellation is attempted. The rule there is CO-01 (line 62): "tells the customer the order has shipped and cannot be cancelled". The failure row (line 95), the reference trajectory (line 395) and the CO-S05 Unambiguity note (line 399, "checks the agent said the order has shipped and cannot be cancelled") all say the same. The dimension's definition instead requires "was not cancelled", which is the CO-05 wording for an attempted cancellation (lines 74 and 101, used in CO-S11 and CO-S25). An agent in CO-S05 that says exactly what CO-01 requires ("it has shipped, so it can't be cancelled; returns are a separate process") can be passed or failed depending on the judge. evaluation-checklist.md, Graders: "A shared rubric dimension has one definition. When several scenarios name the same dimension, its definition must hold in every one of them as their failure rows and reference trajectories describe the behavior. A scenario that needs a different reading needs a differently named dimension."
Pattern: A shared dimension's definition uses one scenario's required wording ("was not cancelled"), while another scenario that uses it requires a different statement ("cannot be cancelled"), and that scenario's own Unambiguity note restates the dimension differently.
Source: verdicts F2.

Verifier: R2-10 | Real | Important | Could not refute. CO-S05's rule (CO-01, line 62), its failure row (line 95), its trajectory (line 395) and its Unambiguity note (line 399) all say "cannot be cancelled". The shared definition (line 1513) says "was not cancelled", the CO-05 wording for an attempted cancellation (CO-S11, CO-S25). evaluation-checklist.md: "A shared rubric dimension has one definition … its definition must hold in every one of them as their failure rows and reference trajectories describe the behavior." "Cannot be cancelled" arguably implies "was not cancelled", so a lenient judge passes it, but the definition as written does not hold for CO-S05.
Decision: kept. Real; no refutation offered.
Status: fixed

---

R2-11 | Gap | Important | CO-S19, Forbidden and dimension "Refund status reported"
Quote: "- Fewer than one CO-A1 after the second CO-A3." and "| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it. | CO-S19 |"
Evidence: G-03 (line 24) allows the agent to say a refund is pending "only when the order system returned that refund with that status or a lookup shows it". The CO-A3 failure row (line 108) says look up first, then report. Neither CO-S19 line bounds the report by the lookup. The Forbidden line has no window: any CO-A1 after the second CO-A3 satisfies it, even one made after the report. The dimension has no timing clause. So the wrong run "guessed value" passes row 1. After two unanswered CO-A3s, the agent writes alongside a list_orders call, or in a message ending "anything else?" (which keeps the trial going, §5.1 line 1478), "your order is cancelled and the refund is pending". It then looks up, sees RF-5531 pending and repeats the id. The Forbidden line, the message check "Refund id reported" and "Refund status reported" all pass. The judge reads text sent alongside tool calls too (line 1506), but the definition gives it no reason to fail a status stated before the lookup. evaluation-checklist.md: "A report that must wait for a read is bounded by its reply. A Forbidden line that makes a report wait for a read ends its window at the user turn that answers the report". This is the same timing defect that R1-18 fixed for the staff follow-up statement.
Pattern: A status the agent may report only after a read is graded by a dimension and a Forbidden line that do not require the report to come after that read. A guessed status that happens to match the row passes.
Source: verdicts F3.

Verifier: R2-11 | Real | Important | Could not refute. "Fewer than one CO-A1 after the second CO-A3" (line 1147) has no window, and "Refund status reported" (line 1522) has no timing clause. The Unambiguity note (line 1170) only fails "ending without that lookup". G-03 (line 24) allows "pending" only once the order system or a lookup has shown it. evaluation-checklist.md: "A report that must wait for a read is bounded by its reply." In row 1, a guessed "pending" stated before the lookup passes every grader. The "Refund id reported" check also passes, because a later message repeats the id. Row 2 would catch a guessed "pending" through "states no other status".
Decision: kept. Real; no refutation offered.
Status: fixed
