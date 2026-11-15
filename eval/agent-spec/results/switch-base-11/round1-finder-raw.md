6 findings: 3 Important, 3 Nit.

F1 | Lies | Important | rules.md "What the agent does" (row: "the refund call returned a failed refund, answered order not cancelled, ..."), policy.md A15
Quote: "| the refund call returned a failed refund, answered order not cancelled, or answered a second transient error | hands the case to staff (refund not issued), then says the order is cancelled but the refund was not issued | R-07, R-11, R-09 |"; and policy.md A15: "agent tells the customer: it could not find that order; nothing was cancelled and no refund was issued"
Evidence: Q11 (stand-in default, accepted). On "order not cancelled" the agent "tells the customer the refund was not issued". The owner's wording says nothing about the order being cancelled, and the tool has just answered that it is not. So the row contradicts the rule it cites, R-09: "it never says a refund was made, or that nothing changed, when that is not what the order system showed." Second instance: Q12 (accepted) has the agent say "it could not find that order, cancels nothing more and issues no refund". "Cancels nothing more" describes what the agent does; it is not a claim to the customer. A15 turns it into the statement "nothing was cancelled", which the not-found answer does not establish.
Pattern: a customer message adds a fact about the order that neither the owner's wording nor the tool's answer supports, and in the first case the tool's answer contradicts it. Each message should say only what the owner's wording says and what the tool returned.

F2 | Unclear | Important | rules.md R-04
Quote: "When the customer's words fit more than one open order, the agent asks which one, and the yes must name the order number."
Evidence: Q3/Q4 record, known failure case 1: "agent must disambiguate and get a confirmation naming the order number before the cancel call." C-36 repeats this faithfully ("gets a confirmation naming the order number"). R-04 moves the requirement from the confirmation (the proposal the customer says yes to) to the customer's reply. An agent could then refuse a plain "yes" to "cancel order HG-10482 and refund $86.40 to Visa ending 4242", which the owner's one-yes rule (C-38) accepts.
Pattern: a rule rewords an owner requirement so that it can be read as stricter than what the owner said. The rule should keep the owner's subject: the confirmation names the order number.

F3 | Gap | Important | rules.md "What the agent does" (R-04, R-12)
Quote: absent
Evidence: Q9 (accepted): "one at a time: each order gets its own proposal and its own yes, and a yes for one order never covers another." Q4 record: "any change after confirmation voids it." The table has no row for any of these cases the agent will meet:
(a) the customer asks to cancel two orders in one message;
(b) the customer names a second order mid-conversation, e.g. while a proposal waits for a yes (policy.md A9/A10 has only "customer says yes" / "customer says no");
(c) the customer's reply is a yes carrying a change, e.g. "yes, but refund to my Mastercard" or "yes, just the mug"; the only yes row is "the customer said yes to the proposal | cancels the order";
(d) what the agent does once a yes is voided (propose again? stop?).
R-12 and R-04 state the principle, but no row says what the agent does.
Pattern: a conversation case the owner's rules govern has no row in "What the agent does". Add a row for each multi-order and changed-or-voided-yes situation.

F4 | Lies | Nit | rules.md R-02, "What the agent does" row "the read of the orders failed"
Quote: "When it cannot read the customer's orders, it says so and changes nothing." / "| the read of the orders failed | says it cannot see their orders right now, and changes nothing | R-02 |"
Evidence: R-02 cites C-15 for this, and C-15's quote is about the re-read after a timed-out cancel: "Re-read fails, say outcome unknown, issue no refund, hand off." The wording "cannot see their orders right now" comes from the Q6 recommendation, and the owner answered Q6 "No." No answer or claim covers a failed first read, and no decision in the Decisions table records this behavior.
Pattern: a rule rests on a claim that does not say what the rule says, and on a recommendation the owner rejected, with no decision logged. Either log it as a decision or put the question to the owner.

F5 | Lies | Nit | claims.md C-47, C-49, C-51
Quote: C-51 "Refunds to expired or cancelled cards usually reach the customer's replacement card, and fail only in rare cases."; C-49 "A refund can still fail after it is made, when the customer's bank or card issuer cannot process it."; C-47 "The handoff call creates the task or times out; a call that times out may have created it." (source "spec only")
Evidence: Stripe sentences listed in review-packet.md Sources. The C-51 source says only "in most cases, credited to the customer's replacement card" and nothing about failure being rare. The C-49 source says "A refund can fail if the customer's bank or card issuer can't process it", not "after it is made". C-47's "a call that times out may have created it" has no source in the answers or inputs: Q16 says only "it creates the task or times out." R-11 rests on C-47.
Pattern: a claim says more than its quote, or has no source at all. Trim each claim to its source, or put it to the owner.

F6 | Unclear | Nit | rules.md R-02 title
Quote: "## R-02 Shipped, delivered, cancelled or unknown orders change nothing"
Evidence: Here "unknown orders" means an order number that matches none of the customer's orders (C-35). Everywhere else in the spec "unknown" means an outcome the agent cannot confirm ("outcome unknown", "refund status unknown", "cancellation unknown"; C-11, C-26, C-43). The owner could read the title as covering orders whose cancellation is unknown, which R-06/R-11 send to staff instead.
Pattern: a coined short form reuses a word that the spec gives another meaning elsewhere. Say "an order number that matches none of their orders".
