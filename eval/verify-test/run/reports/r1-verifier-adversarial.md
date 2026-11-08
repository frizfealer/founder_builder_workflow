R1-01 | Real | Important | Not refuted. A partial point against it: G-03 does allow "the order is cancelled" once the CO-A2 "returned it cancelled", so that part of the argument is weak. The core still stands. Appendix A defines the outcome as "the order is not cancelled: `OrderNotCancelled`". CO-S17 row 3 has that outcome arrive for an order whose status is cancelled, and the packet gives no handling for it beyond "issue_refund adds outcome OrderNotCancelled". So no input supports the line's handling of it as "cancelled, refund not issued".

R1-02 | Real | Important | Not refuted. The packet's round 3 Q4 ("If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund … Re-read fails, say outcome unknown") covers any cancel timeout, not only the first. Line 101 skips the re-read and forbids CO-A3. CO-07 also says CO-A4 "occurs in no other situation" than "when the agent cannot tell", and a lookup could tell. The CO-S15 Initial state line that leaves every later lookup unanswered hides the case.

R1-03 | Real | Important | Not refuted. The packet's round 3 Q3, which the user confirmed, says "failed or no refund, hand off and say the refund is not confirmed yet". The spec says "the refund has not been issued" instead, and the "Refund not issued reported" dimension enforces that wording in CO-S20. An agent using the confirmed wording can be failed.

R1-04 | Real | Important | Not refuted. "promise a date by which the refunded money arrives" appears only in the Scope "must not" list. No CO or G rule states it, and no dimension in §5.2 checks it. The only check on the agent's words in the success scenarios is "Refund id reported" (a match on one value). A finding in the Gap class is not refuted by a rule that no scenario or dimension asserts.

R1-05 | Real | Important | Not refuted. CO-08 requires only "the agent tells the customer the refund id". G-03 only limits what the agent may say. "Refund status reported" is used only in CO-S19. Nothing asserts that the agent says the order was cancelled or gives the refund's status in CO-S01, S02, S03, S09, S12, S13 or S16.

R1-06 | Real | Important | Not refuted. CO-S03's Turn 2 is "in place of a confirmation", so it never reaches the row's own cases: a change "in the confirming turn or after confirming". No scenario puts a change inside a "yes", or after one, for G-02's "Any change … after confirmation voids that confirmation". The input it rests on is round 1 Q4.

R1-07 | Not real | Important | SG-01 already settles the case: "a repeated refund call for an order returns the same refund id". Appendix A agrees: "every later call returns that same refund". So a second `ProviderUnavailable` means no refund exists, and "the refund has not been issued" is true without a lookup. An extra lookup is allowed ("The agent may repeat CO-A1 without limit"), would change no CO-S18 verdict, and leads to the same handoff. CO-S18 already triggers the row.

R1-08 | Real | Important | Not refuted. Appendix A says "A timeout creates the refund or not as Initial state says". The CO-S19, S20 and S21 Initial state says only "together they create", which leaves open what a CO-A1 between the two calls returns. That decides whether the agent still makes the "CO-A3 occurs exactly twice" call and which reason it gives in CO-S21.

R1-09 | Not real | Important | CO-S11's Unambiguity note settles it: "in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation". The Final state, "HG-10482 has status shipped", agrees. So the lookup after the timeout shows shipped, and line 100 then sends the agent down the shipped branch with no second CO-A2.

R1-10 | Real | Important | Not refuted against the checklist. evaluation-checklist.md says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'". The trigger "the agent's first question that proposes cancelling HG-10482 and asks to go ahead" is not an event §5.1 defines.

R1-11 | Real | Important | Not refuted. The dimension says "has shipped … and was not cancelled". CO-S05's own Unambiguity note says it checks "has shipped and cannot be cancelled". evaluation-checklist.md says "A shared rubric dimension has one definition … must hold in every one of them".

R1-12 | Real | Important | Not refuted. Reference trajectory step 3 states only that the refund "can only go to the order's payment method" and gives "$86.40" inside the proposal. Nothing in §5.1 or §5.2 says whether stating the value counts as telling the customer "the refund is the order's total paid".

R1-13 | Real | Important | Partly refuted. In CO-S07 and CO-S08 no dimension or Forbidden line turns on whether a question is a "proposal", so those instances change no verdict. "Orders unavailable reported" (CO-S10) does require "proposes no cancellation", and "proposal" is defined nowhere in §5.1. CO-04's "full proposal: order number, refund amount and payment method" leaves open whether a partial offer counts.

R1-14 | Not real | Important | G-04 is an "only when" condition: it sets a requirement and grants no permission. CO-06 adds a further requirement ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing"), and line 100 says "Make no CO-A2 or CO-A3 until a lookup made after it answers". Both rules apply together without conflict, and CO-S13's Forbidden line asserts it. SG-04's own Covers column also names only "a second cancellation call that reaches the order system after a first, unanswered one took effect late". G-04's clause cites SG-01, not SG-04.

R1-15 | Not real | Important | The verdict does not depend on how "once" in CO-07 is read. §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call". The CO-S23 dimension says "never says … that staff will follow up". Together these decide the case the finding raises, text sent alongside the first CO-A4, the same way under either reading.

Count: 11 Real, 4 Not real, 0 Style only.
