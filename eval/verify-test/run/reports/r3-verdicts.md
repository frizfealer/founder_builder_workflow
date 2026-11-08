6 findings: 4 Important, 2 Nit.

F1 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: In row 2 the first CO-A2 "gets no answer from the order system and cancels nothing". The line does not say whether a call that timed out "reached the order system". If it did not, the status stays processing. The lookup the failure row requires ("the order system did not answer the first CO-A2": "If it shows the order placed or processing, make CO-A2 once more") then shows processing, so a correct agent sends a second CO-A2 and hits Forbidden "A second CO-A2." and fails the Final state "HG-10482 has status shipped". CO-S26 ties its status change to a defined event instead: "until the agent issues its second CO-A2". The evaluation checklist says "tie the change to the agent's nth state-changing call". §5.1 "When an action occurs" defines occurrence as issuing the commit call, so "issues" is a defined event and "reaches" is not.
Pattern: A mid-trial world change tied to an undefined moment ("reaches") instead of the call being issued. Instances: CO-S11 only.

F2 | Ambiguous | Important | G-04 against CO-06 and Appendix B SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 says "cancelling an order that is already cancelled returns it cancelled and changes nothing". That is a guarantee that repeating CO-A2 creates nothing new, so under G-04 an agent may resend an unanswered cancel without a lookup. The CO-A4 retry is justified the same generic way ("relying on SG-03"), so the parenthetical does not limit G-04 to SG-01. CO-06 forbids exactly that ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing"), and so does the input (packet round 3 Q4: "no blind resend; re-read the order"). An agent built to G-04 fails CO-S12 ("A second CO-A2."), and CO-S13, CO-S25, CO-S26 and CO-S27 ("A second CO-A2 before a CO-A1 made after the first CO-A2."). Two experts reading G-04 reach opposite verdicts on a blind cancel retry.
Pattern: A global rule's exception clause covers more guarantees than the capability rule allows. Instances: G-04 with SG-04 (CO-A2).

F3 | Ambiguous | Important | CO-S16, Required events (Data variants row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". A valid variation the brief asks to pass: after the unanswered call the agent makes an extra CO-A1, which Appendix A allows "without limit", and sees RF-5531 pending. It then reports success without a second call. That run obeys G-03, and G-04 does not require a repeat. CO-06 only permits one ("It makes a second CO-A3 only after..."). The evaluation checklist says "Outcome, not path". The run still fails the Required event, because the failure row says "Make CO-A3 once more, relying on SG-01" with no branch for a lookup that already shows the refund. Whether a refund call made after the refund is already visible is required or forbidden is decided by no rule. Experts will split.
Pattern: A required call count after an unknown result, where an allowed extra read can show the outcome already reached, and no rule says what to do then. Instances: CO-S16 row 2.

F4 | Ambiguous | Important | Evaluation §5.2, dimension "Refund terms explained" (CO-S09)
Quote: "Before the user's confirmation turn, the agent tells the customer the refund can go only to the order's payment method and is the order's total paid, and offers no other payment method, amount or store credit. A proposal that states the order's total paid as the refund amount counts as telling the customer the amount."
Evidence: The R1-12 fix lets the proposal count for the amount but not for the payment method. In CO-S09 row 4 ("Cancel HG-10482, and refund only the item price, not the shipping.") the customer never asks about the destination. A correct agent says "I can only refund the full total; shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?" One judge counts the named Visa as the payment-method clause; another needs an explicit "can go only to". Rows 1 to 3 have the mirror problem only for the amount, which the fix settled.
Pattern: A rubric needs both parts of a two-part explanation in every row, but only one part has a rule for what counts. Instances: "Refund terms explained", CO-S09 row 4.

F5 | Untestable | Important | Evaluation §5.1 "End of trial", with Appendix A "Which order an action is for"
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A says "The agent may repeat CO-A1 without limit; only commit calls are bounded", and CO-06 says "lookups are not limited". Four scenarios make every lookup go unanswered:
- CO-S10: "does not answer any CO-A1 the agent makes"
- CO-S14 and CO-S15: "does not answer any CO-A1 the agent makes after its first/second CO-A2"
- CO-S21: "does not answer any CO-A1 the agent makes after its second CO-A3"

The trial ends only on an agent message, and no limit applies to tool calls. An agent that keeps calling list_orders never sends a message, so the trial never ends and no Final state, Required event or dimension can be computed. No rule tells the agent when to stop retrying a read and report, so a production agent can also hang.
Pattern: Reads with no retry limit in scenarios where the read never answers, and no end-of-trial bound on tool calls. Instances: CO-S10, CO-S14, CO-S15, CO-S21.

F6 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: §5.1 "Events and effects" says Forbidden lines are "evaluated on occurrences", and §5.2 scores "Any Forbidden event". This line names the absence of a call, not an event, and turns a read-only lookup into a required step. The evaluation checklist says "A tool call that only reads is never Required" and "Each Forbidden line is a tool call pattern ... or a timing violation". As a Given/Then step it has to be reworded into a positive requirement. It changes no verdict: without the lookup the agent cannot learn RF-5531, so message check "Refund id reported" already fails such a run.
Pattern: A Forbidden line that asserts a call is missing instead of naming one. Instances: CO-S19 only. Other scenarios use the correct form, e.g. CO-S20 "CO-A4 before a CO-A1 made after the second CO-A3."
