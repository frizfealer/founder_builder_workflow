5 findings: 3 Important, 2 Nit.

F1 | Gap | Important | §4.1 Contract (no rule); §5.2 dimension table
Quote: "absent" (the only mention is the Scope line "- promise a date by which the refunded money arrives.", agent-spec.md line 49, under "The agent must not")
Evidence: review-packet.md, Round 3 Q1: "The agent promises nothing about when the money arrives." The user answered "Yes to all". Round 2 Q2 had first proposed "money arrives in 5 to 10 business days", so an agent repeating that timeline is a likely failure. No Contract rule (G-01 to G-04, CO-01 to CO-08) states this constraint. No rubric dimension in §5.2 (lines 1497-1509) checks that the agent stated no arrival date, including "Refund id reported" and "Refund status reported" on the success paths. An agent that tells every customer "your money will arrive in 5-10 business days" passes every scenario.
Pattern: an input constraint that appears only in the "must not" list of Scope & Authority, with no Contract rule protecting it and no scenario or dimension asserting it.

F2 | Gap | Important | Failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" (line 96); G-02, CO-04
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: The only scenario that triggers this row is CO-S03. Its Turn 2 is scripted "in place of a confirmation" (line 248) and changes only the order. No scenario's confirming turn itself carries a change (for example "Yes, but put it on my Mastercard" or "Yes, but make it HG-10511"). CO-S09 puts the different payment method in Turn 1 (lines 587-589), before any proposal exists. Packet Round 1 Q4: "any change after confirmation voids it". An agent that reads "Yes, but …" as a confirmation, then cancels and refunds, passes the whole suite.
Pattern: a compound failure-row condition where only one of its causes (here, a change in place of confirmation) has a scenario whose Initial state or User turns trigger it.

F3 | Gap | Important | G-03; success-path scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16; CO-08
Quote: "The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: On every success path the refund status is pending (for example CO-S01 line 139). The only check on the agent's words there is the message check "Refund id reported" (CO-S01 Unambiguity note, line 170: "the only check on the agent's words"). An agent that says "refund RF-5531 has been issued" when it is pending therefore passes. The status the agent reports is graded only in CO-S19 ("Refund status reported", line 1507). §2 (line 9) says the customer "wants to be told truthfully whether the order was cancelled and where the refund stands", yet CO-08 requires the agent to tell only the refund id. Packet Round 2 Q4, case 3: "Final message must match the final refund status."
Pattern: a G-03 truthfulness clause, or a stakeholder interest in being told an outcome, that is asserted by a rubric dimension on failure paths but by no dimension on the success paths where the same false claim is possible.

F4 | Gap | Nit | Failure row "the order system did not answer the first CO-A2" (line 100)
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, … If the lookup does not answer, …"
Evidence: use-case checklist (cockburn-checklist.md, Failure handling): "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." The "lookup answers but the order is not in the list" branch is missing. That result can happen: OrderNotFound is a declared cancel_order outcome (packet, tool confirmation turn, change 1), and CO-S24 already sets up the order system reporting a listed order as not found. Nit because CO-05 and CO-06 already block a further CO-A2 and any CO-A3, and CO-07's "cannot tell whether the order was cancelled" plausibly decides the handoff.
Pattern: a lookup-branching failure row with no "nothing found" branch.

F5 | Gap | Nit | §4.1 Failure handling (rows at lines 90-93); CO-01, CO-02
Quote: "absent"
Evidence: use-case checklist brainstorm: "the lookup returns more than one plausible match, or none". The rows cover more than one open order with no order named (line 90), a named number not on the account (line 91), and a named order that is shipped, delivered or cancelled (lines 92-93). No row covers an unnamed request ("I want to cancel my order") when the customer has no orders at all, or none with status placed or processing. The rows at lines 92-93 are keyed to "the named order", so they do not apply. CO-01 keeps the agent from proposing, so no write is at risk, but what the agent tells the customer is left undefined.
Pattern: an ambiguous-match failure covered for "more than one" but not for "none" when the user names no record.

Checked and found covered: (stakeholder interests other than F1/F3; every declared tool outcome has a failure row; every act-only-when rule has acting and holding-back scenarios; every outcome-changing failure row has a trigger except F2's part; User-knows pairs used; three known failure cases covered by CO-S02, CO-S16-18, CO-S16/S19-21; race by CO-S11; Initial-state values inside contract.)

Files read: briefs/r1-finder-coverage.md, review-packet.md, product-idea.md, run/agent-spec.md, references/cockburn-checklist.md, evaluation-checklist.md, specification-by-example-checklist.md, verification.md
