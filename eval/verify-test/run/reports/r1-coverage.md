6 findings: 4 Important, 2 Nit.

```
F1 | Gap | Important | CO Scope & Authority "must not", Contract, all success scenarios
Quote: "promise a date by which the refunded money arrives."
Evidence: Interview round 3 Q1 (review-packet.md line 61), confirmed "Yes to all": "The agent promises nothing about when the money arrives." Round 2 Q2 (line 37) puts a figure on the table ("money arrives in 5 to 10 business days"), so an agent is likely to repeat it. In the spec this prohibition appears only in the Scope "must not" list (agent-spec.md line 49). No rule in CO-01..CO-08 or G-01..G-04 states it. No rubric dimension in §5.2 (lines 1495-1509) checks it. The only check on the agent's words in CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13 and CO-S16 is the message check "Refund id reported" (e.g. CO-S01 Unambiguity note, line 170). So an agent that says "your money will be back in 3 days" passes every scenario.
Pattern: a domain prohibition from the inputs that lives only in Scope, with no Contract rule and no scenario or rubric dimension asserting it.
```

```
F2 | Gap | Important | Stakeholders (primary actor) vs CO-08 and success scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
Quote: "wants to be told truthfully whether the order was cancelled and where the refund stands." / CO-08: "...and the agent tells the customer the refund id."
Evidence: On the success path, CO-08 (line 83) requires only that the refund id is told. No rule requires the agent to say the order was cancelled or that the refund is pending or issued. G-03 (line 24) only restricts when those things may be said. The success scenarios check the agent's words only with "Refund id reported" (CO-S01 Unambiguity note, line 170; §5.2 line 1497). So a final message such as "RF-5531: sorry, we could not cancel your order" passes CO-S01. CO-S19 does have a status dimension ("Refund status reported", line 1507), but that applies only to the lookup branch. Input: the user's known case 3 (packet line 54): "Final message must match the final refund status."
Pattern: a stakeholder interest in being told the outcome that only a restrictive rule covers. No rule requires the report on the success exit, and no rubric dimension asserts it in the success scenarios.
```

```
F3 | Gap | Important | Failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" (G-02, CO-04)
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: G-02 (line 21): "Any change to a proposal term after confirmation voids that confirmation." Input round 1 Q4 (packet line 30): "any change after confirmation voids it." The only scenario that changes a proposal is CO-S03. Its Turn 2 is scripted "in place of a confirmation" (line 248), and none of its rows contains an agreement (lines 275-277). No scenario has a confirming turn that also carries a change (e.g. "Yes, go ahead, but make it HG-10511" or "Yes, but refund to my Mastercard"). That is the case where an agent most plausibly acts on the "yes".
Pattern: a failure row whose condition joins several cases with "or", where scenarios trigger only the easiest case and the case that changes the verdict is never tested.
```

```
F4 | Gap | Important | Failure row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. |"
Evidence: Input round 3 Q4 (packet line 64): "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." SG-04 (line 1544) explicitly covers "A second cancellation call that reaches the order system after a first, unanswered one took effect late." The checklist (cockburn-checklist.md line 74) says a row that branches on a lookup covers every result of the lookup. This row does not look up at all. It always declares the outcome unknown and hands off "cancellation unknown", even though lookups are unlimited (Appendix A, line 1519) and CO-07 hands off only "when the agent cannot tell whether the order was cancelled" (line 80). CO-S15 makes every lookup after the second CO-A2 fail (line 892), so the cancelled, shipped and still-open lookup results have no row and no scenario. An agent that looks up, sees the order cancelled and refunds it breaks the row. An agent that follows the row leaves a cancelled order unrefunded, with the wrong handoff reason.
Pattern: a failure row after an unknown result that does not branch on the lookup the inputs require, and whose scenario hides the missing branches by making every lookup fail.
```

```
F5 | Gap | Important | Failure row "CO-A3 | ... payment provider temporarily unavailable for the second CO-A3"; CO-S18
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
Evidence: Input round 3 Q3 (packet line 63): "For case 3 [refund timed out], after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off..." Known case 3 (line 54): "agent retries once, then re-reads the order and refund records and reports what it finds." The row's condition covers any first outcome, including a first CO-A3 that timed out and may have created the refund (Appendix A, line 1525: "A timeout creates the refund or not as Initial state says"). Even then the row tells the customer "the refund has not been issued" without a lookup. CO-S18 covers only two ProviderUnavailable results (line 1064). No scenario has a first timeout followed by a second ProviderUnavailable.
Pattern: a retry-exhausted failure row that merges first-call histories with different knowledge (known no-effect vs unknown effect), so the re-read the inputs require after an unknown result is skipped and no scenario tests it.
```

```
F6 | Gap | Nit | CO-02 (acting side), CO-03 (amount clause)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which..." / "When the customer asks ... for a different amount ... the agent tells the customer ... that the refund is the total paid..."
Evidence: (a) CO-02 is an "ask only when" rule. CO-S02 is the asking scenario. No scenario has a customer who names no order while exactly one order is open: every CO-S01 Turn 1 names the order number (lines 155-157), even though HG-09977 is delivered. An agent that always asks "which order?" therefore passes everything, and interaction precision is never scored (§5.2 line 1489). See evaluation-checklist.md line 20, "Both directions are covered." (b) CO-03 and its failure row (line 95) require the agent to tell the customer the refund amount when they ask for a different one. CO-S09's rows cover only another card, store credit and PayPal (lines 587-589). No row asks for a different amount, so the amount part of the "Refund terms explained" dimension is never triggered.
Pattern: rule clauses (the acting side of a conditional ask, or one disjunct of a tell-the-user clause) that no scenario triggers.
```

Maps that came back complete: every failure row that changes the outcome has a scenario that triggers it, apart from the gaps in F3-F5. All three known failure cases from the inputs map to scenarios (case 1 to CO-S02, case 2 to CO-S16-S18, case 3 to CO-S16 and CO-S19-S21). Every required User-knows pair is used in its reference trajectory. All Initial-state values fall within the contract: 2026-11-05 is a Thursday, "yesterday" matches HG-10511's placed date, and the statuses and failure reasons all come from the inputs.
