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
