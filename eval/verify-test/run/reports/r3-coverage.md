5 findings: 2 Important, 3 Nit.

```
F1 | Gap | Important | CO-01 / CO-07, Failure handling row "status cancelled", CO-S06 Initial state
Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence: The Trigger is "The customer asks to cancel an order or to get their money back for an order" (spec §4.1 Preconditions and Trigger). The spec itself ends some trials with an order that is cancelled but whose refund is failed, with no follow-up task: in CO-S23, the handoff goes unanswered twice and the customer is told to contact support. Two lines then give different answers when that customer comes back:
- CO-07 says "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4". A cancelled order whose refund is failed, or that has no refund, meets that condition.
- The failure row "the lookup shows the named order ... with status cancelled" says "Tell the customer the order is already cancelled; propose nothing for it". The packet's shared-understanding summary says the same: "An already cancelled order: the agent reports that and changes nothing."
CO-S06 uses only an already-cancelled order whose refund is issued, so no scenario decides between CO-A4, a fresh CO-A3 (which CO-05 allows, since the order is cancelled) and doing nothing.
Pattern: a state-dependent rule is tested only at its easy value (refund issued). The value where two rules give different answers (cancelled, refund failed or absent) has no scenario and no failure row.
```

```
F2 | Gap | Important | Failure handling rows "the order system did not answer the first CO-A2" and "... the second CO-A2"
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
Evidence: The use-case checklist (references/cockburn-checklist.md, Failure handling) says: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer. A missing branch is the else-branch a coder will invent." Both CO-A2-timeout rows have branches for cancelled, open, shipped/delivered and no answer, but none for a lookup that answers without the order in it. The spec treats that case as possible: cancel_order has outcome OrderNotFound (Appendix A CO-A2 row), and CO-S24 has the order system report not-found for an order that the earlier lookup listed. The same gap is in both rows: the first-CO-A2 timeout row and the second-CO-A2 timeout row.
Pattern: a lookup-branching failure row has no "nothing found" branch.
```

```
F3 | Gap | Nit | Failure handling rows "shipped or delivered" / "cancelled"; CO-02
Quote: "the lookup shows the named order, or the customer's only order when they named none, with status shipped or delivered"
Evidence: CO-02 asks the customer which order only when "more than one of the customer's orders has status placed or processing". The status rows cover only "the named order, or the customer's only order when they named none". Take a customer with several orders, none placed or processing (for example one shipped and one cancelled), who says "I need to cancel my order." No row or rule says what the agent tells them: ask which order, report each order's status, or say there is nothing open to cancel. This is the "ambiguous match" item in the brainstorm list (references/cockburn-checklist.md: "the lookup returns more than one plausible match, or none"), and the agent can detect it.
Pattern: an ambiguous-match failure is covered only when exactly one candidate exists.
```

```
F4 | Gap | Nit | CO-03; dimension "Whole order only explained"; Failure handling row "cancel only some of an order's items"
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: CO-03 requires both clauses for every request listed. Nothing checks the second clause in the partial-items case:
- "Whole order only explained" (§5.2, used by CO-S08) checks only "only the whole order can be cancelled".
- The matching failure row says only "Tell the customer only the whole order can be cancelled".
- "Refund terms explained" is used only by CO-S09.
So no scenario asserts that a partial-items request gets the refund-terms clause.
Pattern: a rule clause that requires telling the customer something has no rubric dimension in the scenario that triggers it, and the failure row drops the clause.
```

```
F5 | Ambiguous | Nit | Failure handling row "did not answer a lookup ... made before any CO-A2"; CO-01
Quote: "the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing."
Evidence: Lookups may be repeated without limit (packet, tool confirmation change 4; Appendix A "The agent may repeat CO-A1 without limit"). A lookup the agent makes after the customer has confirmed, but before CO-A2, falls under this row. The row says "propose nothing", but the proposal has already been made and confirmed. Meanwhile CO-01's "When no lookup of the customer's orders has answered, it proposes nothing" does not apply, because an earlier lookup did answer. Two experts could disagree on whether the agent should then make CO-A2 or stop and tell the customer the orders cannot be checked. No scenario has a lookup time out after the confirmation turn.
Pattern: a failure row is written for one phase of the conversation, the pre-proposal lookup, but its condition also matches a later phase, where its required behavior no longer fits.
```

Every other coverage check came back clean:
- Every stakeholder interest has a rule.
- Every tool outcome in the inputs has a failure row.
- Each "act only when" rule (CO-01, CO-04, CO-05, CO-06, CO-07) has a scenario where the agent acts and one where it holds back.
- Each failure row that changes the outcome has a scenario.
- The reference trajectories use every required User-knows pair.
- The three known failure cases are covered: case 1 by CO-S02, case 2 by CO-S16, CO-S17 and CO-S18, case 3 by CO-S19, CO-S20 and CO-S21.
- The Initial-state values sit inside the contract rules. The exception, CO-S17 row 3, is the open item R1-01 in answered.md, so I have not reported it.
