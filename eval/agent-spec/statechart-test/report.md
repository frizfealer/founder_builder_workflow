# Statechart test: report

Inputs: `eval/agent-spec/round0-agent-spec.md` and `eval/agent-spec/review-packet.md`, nothing else.
Regenerate everything: `cd eval/agent-spec/statechart-test && python3 check.py && python3 selftest.py`
(`check.py` writes `chart.mmd`, `scenario-map.md`, `index.html`, `results.json`).

## What was built

- `model.py`: the state, the events, the agent's policy (the spec's failure-handling table, row by row), the rules as checks, and the assumptions table as data.
- `check.py`: breadth-first search over every reachable state; every rule checked on every state and step; shortest path per violation; deadlocks; unreached chart states.
- `chart.py`: projects the model onto the chart; the set of rules broken at a model state is part of its chart state, so states that break different rules are never merged.
- `scenarios.py`: replays each CO-S scenario. The scenario fixes the customer and the order system (a supporting actor answers normally unless Initial state says otherwise, §5.1). The agent is left free, and every complete path counts.
- `selftest.py`: a deliberately broken CO-06 ("at most one cancel") must report a known 11-step path.

**How to read a "breaks".** The agent in the model does exactly what the failure table says. A break means that following the table, under the stated assumption, violates the rule as written. Each break below names the assumptions it depends on.

## Rules

| Rule | Invariant | Result |
|---|---|---|
| CO-01 Only open orders are proposed | Step: a proposal only after a lookup showed the order open. End: shipped or cancelled seen gets the matching message and no proposal. | holds |
| CO-02 The customer's own order, by number | Step: no proposal for a number not on the account, and none while two orders are open and unnamed. End: an unknown number gets "no such order". | holds |
| CO-03 Whole order, full refund, original payment method | Step: a proposal after a part-order request only once the customer asks for the whole order, and after a refund-elsewhere request only with the terms stated. End: those requests get the matching message. | breaks. The first sentence is not expressible, because the model has one proposal value. |
| CO-04 Confirmation precedes cancellation | Step: cancel and refund calls only while a confirmation is current. | holds. Which customer words count as confirmation is not expressible. |
| CO-05 Refund only for a cancelled order | Step: a refund call only when the order was returned or shown cancelled. End: a shipped rejection, a post-cancel lookup showing shipped, or "not found" gets the matching message and no refund. | breaks |
| CO-06 Limited retries | Step: the call counts, and the condition for each second call. | holds |
| CO-07 Unfinished orders go to store staff | Step: a first hand-off only in one of the two named situations, with a matching reason. End: either situation means a hand-off was made, and "staff will follow up" is said only after the task was created. | breaks (two ways) |
| S-1 (not a CO rule) No unfinished order left with nobody, from the §2 support-team line | End, after the order system settles: if this conversation's cancel took effect, a refund is pending or issued, or a task exists, or the customer was sent to support. | breaks |
| S-2 (not a CO rule) G-03 checked against what the order system holds | End, after the order system settles: every status claim the agent made is true. | breaks |

The rule lines are quoted in full in `model.py` (`RULES`) and on the page.

## Violations (shortest paths, from the real output below)

1. **CO-03, depends on A-13.** The order has shipped or been delivered. The customer asks to cancel only some items. The lookup shows the order shipped. The agent gives only the shipped message. CO-03 also requires "only the whole order can be cancelled". The same path with a refund-elsewhere request breaks CO-03's refund-terms message. CO-01 and CO-03 both apply here, and the table does not say which comes first.
2. **CO-07, missing hand-off, depends on A-03 and A-15.** The order is already cancelled with no refund pending or issued. The customer asks to cancel it. The lookup shows it cancelled with no refund. The agent says it is already cancelled, as CO-01 requires. CO-07 read literally ("the order is cancelled but its refund is not shown pending or issued") then requires a hand-off, and none is made.
3. **CO-07, hand-off in a situation CO-07 does not name, depends on A-14.** 15 steps: the cancel times out with nothing changed; the lookup shows the order open; the cancel is sent again and times out; a lookup now answers "placed or processing"; the agent hands off as "cancellation unknown", because the table row for an unanswered second cancel says so whatever a lookup shows. The agent can tell the order was not cancelled, and CO-07 says the hand-off "occurs in no other situation". The same happens when that lookup shows the order cancelled, and then the table also forbids the refund that CO-05 and CO-06 would allow.
4. **CO-05, depends on A-14 and A-10.** 18 steps: the same as 3, but the order ships between the first lookup and the second cancel, so the last lookup shows it shipped. The table says to tell the customer "not known whether cancelled"; CO-05 says to tell them it shipped, was not cancelled, and returns are separate.
5. **S-1 and S-2, depend on A-05 and A-09.** 14 steps: the first cancel times out but will take effect later. The lookup still shows the order open. The late cancel lands. The second cancel answers "order not found". The agent tells the customer the order was not cancelled. The order system now holds it cancelled, with no refund and no follow-up task.

No deadlocks. Every declared chart state is reached. CO-01, CO-02, CO-04 and CO-06 hold.

## Chart

`chart.mmd` has 18 states and 28 arrows, which is over the ~20 budget. The extra arrows come from the six break states: each needs its own node, and the rule "never merge states that break different rules" keeps them apart. Rendering in a browser was not checked in this session; see the note at the end.

The chart hides these model steps (9,415 of 13,785 steps are hidden inside merged states):
- every agent tool call and decision, which are drawn inside the state they lead to;
- the first refund retry, the lookup after a second unanswered refund, and the first hand-off retry, because the first and second attempts are merged;
- the first and second cancel, which are merged ("Cancel sent", "Cancel sent, no answer"); the arrow text says "after the second cancel" where the difference matters;
- "order ships", which changes no chart state by itself and shows up at the next result;
- "customer changes the order or a term", a loop back to the proposal;
- a late cancel that finds the order not open;
- the five account set-ups, all drawn as the start arrow.

## Assumptions

Every place the inputs are silent and the model had to choose. Source of truth: `model.py` (`ASSUMPTIONS`).

| Id | Assumed | Silent or ambiguous line | Alternative not chosen |
|---|---|---|---|
| A-01 | Statuses placed and processing are one value (open); shipped and delivered are one value (shipped). | CO-01 and CO-05 treat each pair alike; nothing distinguishes them. | Keep four values; needed only if some rule treats placed and processing differently. |
| A-02 | Refund statuses pending and issued are one value. A refund's status never changes after the agent sees it (no pending to failed, no pending to issued that matters). | Packet round 2 Q3 lists pending, issued, failed; the spec never says whether pending can later become failed. | A pending refund can later fail; then 'refund pending' told at the end can become untrue with no hand-off. |
| A-03 | An order can already be cancelled with no refund pending or issued (refund failed or none), and the customer can ask to cancel it. | CO-01 covers 'status cancelled' without saying anything about its refund; CO-S06 has only a cancelled order with an issued refund. | Every cancelled order has a pending or issued refund (then the CO-07 break below cannot occur). |
| A-04 | 'Cancel my order' without a number is modelled only when the order meant is open. With exactly one open order, the agent proposes that order. | CO-02 says what to do when more than one order is open; it is silent when exactly one is, and the must-not list forbids 'guess which order the customer means'. | With one open order the agent still asks which, or proposes only after the customer names it. |
| A-05 | OrderNotFound can come back for any cancel call, even for an order the lookup just showed. | Appendix A lists OrderNotFound as an outcome; CO-S24 has it for an order on the account; no cause is given. | OrderNotFound only for a number that is not the customer's (then it cannot follow a confirmed proposal). |
| A-06 | OrderNotCancelled can come back from the refund tool even after cancel_order returned cancelled, and the order is then still cancelled in the order system. | CO-S17 row 3 has exactly this; the spec does not say which answer is true. | OrderNotCancelled means the cancellation did not hold; then 'the order is cancelled' told by the table is untrue. |
| A-07 | Once a refund exists, every later refund call returns it (or times out); it never answers 'payment provider temporarily unavailable'. | SG-01 and Appendix A: 'every later call returns that same refund'. Silent on whether the provider check comes first. | The provider check comes first: a timed-out first call creates the refund, the retry answers 'unavailable', the agent tells 'refund not issued' while one is pending. |
| A-08 | A refund call for an order that is not cancelled answers 'order not cancelled' or times out, and creates nothing. | Appendix A gives OrderNotCancelled as an outcome; the agent never sends a refund before seeing the order cancelled, so this branch is reached only if A-06 is reversed. | The order system creates a refund anyway. |
| A-09 | An unanswered cancel can take effect late: after the agent's lookup, at any later moment, even after the conversation ends. Late effects are modelled for cancel only; refund and hand-off timeouts take effect, or not, at the moment they time out. | SG-04 names 'a first, unanswered one took effect late'; Appendix A: 'A timeout changes the order or not as Initial state says', silent on when. Nothing is said about late refunds or late tasks. | Timeouts take effect immediately or never (no late effects); or refunds and tasks can also land late. |
| A-10 | The order can ship at any moment while it is open, including while a proposal waits and while a call is in flight; nothing else changes the order (no staff cancellation, no other channel). | Packet round 2 Q1 names the processing-to-shipped race between read and cancel; the spec names no other actor. | The order can ship only between the lookup and the cancel; or store staff can also cancel it. |
| A-11 | A lookup that gets no answer is not retried; the agent follows the table's 'does not answer' row at once. | Packet tool change 4: 'Reads may be retried on timeout without limit'; CO-06: 'lookups are not limited'. The table's rows act on the first unanswered lookup. | The agent retries lookups; then the 'lookup does not answer' rows need a stopping point the spec does not give. |
| A-12 | A customer change before confirming (another order, or another term) voids the proposal and the agent states a new one without a new lookup. Switching to the other open order is not distinguished from changing a term. | G-02 and the table row 'the customer changed the order or another proposal term'. The spec does not say whether a fresh lookup is needed before the new proposal. | A fresh lookup before every new proposal (would matter if the other order shipped meanwhile). |
| A-13 | When a part-order or refund-elsewhere request is about an order that has shipped or is cancelled, the agent gives only the shipped or already-cancelled message. | CO-01 and CO-03 both apply; the table has a row for each and no order between them. | The agent gives both messages. |
| A-14 | After the second unanswered cancel, the agent may make one lookup before handing off, and then follows the table row literally: hand off as 'cancellation unknown', no refund, whatever the lookup showed. | The row 'did not answer the second CO-A2' prescribes the hand-off with no lookup; CO-06 says lookups are not limited, and CO-S15's Initial state describes lookups 'after its second CO-A2'. | The agent never looks up there; or, if it does, it acts on what the lookup shows (refund if cancelled, etc.). |
| A-15 | CO-07 'the order is cancelled' means the agent has seen it cancelled by any lookup, including one before any proposal; 'after the retries CO-06 allows' is read as 'no further refund call is allowed'. | CO-07 does not say whether it covers only an order this conversation cancelled. | CO-07 covers only orders this conversation cancelled (then the already-cancelled break below disappears). |
| A-16 | The customer cannot speak between the confirmation and the agent's final message: the agent does not yield the turn while it works through cancel, refund and hand-off. | G-02 voids a confirmation on any later change; nothing says whether the customer can speak mid-flow. | The customer can change or withdraw between cancel and refund; then the refund would be unauthorized. |
| A-17 | Lookups show only orders and refunds, never follow-up tasks. | Appendix A: list_orders returns orders with their refund. | Lookups also show tasks. |
| A-18 | Amounts, payment methods, order numbers and the second order's contents are not modelled; the second open order exists only to make 'which order' a question. The other order is never touched. | G-01 and CO-02; the model's purpose is the cancel-and-refund flow for one order. | Model two orders fully (needed to check G-01 or a switch between orders). |

## Scenario map

Full table with paths: `scenario-map.md`. 31 scenario rows (scenarios split where data rows differ in model terms): **25 one path, 0 no path, 6 ambiguous**.

- **CO-S12 (9 paths).** "That CO-A2 cancels <order>" does not say when. The cancel can land before the agent's lookup, which is the reference path, or after it, at any later step. If it lands after the lookup, the lookup shows the order open and the agent sends a second cancel, which the scenario forbids. SG-04 exists for exactly this case.
- **CO-S15 (2 paths).** After the second unanswered cancel, the agent either hands off at once (the reference trajectory) or looks up first, as the Initial state's "any CO-A1 the agent makes after its second CO-A2" allows. Both paths pass.
- **CO-S19, CO-S20 row 1, CO-S21 rows 1-2 (2 paths each).** "Together they create the refund" does not say which unanswered call created it. The agent cannot see the difference, so both paths end the same way.

Arrows no scenario takes: 16. Grouped:
- every break state, with all its arrows in and out (violations 1 to 5 above);
- "customer stops answering", in reply to the proposal and in reply to the which-order question;
- "customer asks to cancel the whole order" after the whole-order-only message (CO-S08's customer always keeps the order).

## State count

8772 states, 13785 steps, 0 deadlocks.

## What the model leaves out

- G-01..G-04 and CO-08 are not invariants. Only CO-01..CO-07 are checked, plus S-1 and S-2.
- Amounts, payment methods, order numbers, item lists and failure reasons are not modelled (A-18). So the first sentence of CO-03 and G-01 hold by construction, and nothing about them is tested.
- Which customer words count as confirmation, a question or a withdrawal. The model has one event for each.
- A second order beyond "it exists and is open". Switching between two orders, as in CO-S03, is modelled as "a change".
- Customer turns between the confirmation and the agent's final message (A-16).
- Lookup retries (A-11), late refunds and late tasks (A-09), and refund status changing after it is seen (A-02).
- The 12-message cap and turn counting.
- The "my order" request when the order meant is not open (A-04).

## Real output of `python3 check.py`

```
States reached: 8772
Steps: 13785
End states: 2376
Deadlocks (no step out, not an end state): 0
Declared chart states never reached: none

CO-01 Only open orders are proposed: holds
CO-02 The customer's own order, by number: holds
CO-03 Whole order, full refund, original payment method: BREAKS
  violation: part-order request: customer never told only the whole order can be cancelled
  shortest path (5 steps):
     1. The order has shipped or been delivered
     2. customer asks to cancel only some items
     3. agent looks up the customer's orders
     4. lookup shows the order shipped
     5. agent tells the customer: the order has shipped and cannot be cancelled; returns are a separate process
  violation: refund-elsewhere request: customer never told the refund terms
  shortest path (5 steps):
     1. The order has shipped or been delivered
     2. customer asks for the refund to go somewhere else
     3. agent looks up the customer's orders
     4. lookup shows the order shipped
     5. agent tells the customer: the order has shipped and cannot be cancelled; returns are a separate process
CO-04 Confirmation precedes cancellation: holds
CO-05 Refund only for a cancelled order: BREAKS
  violation: order shipped after the proposal: customer not told it shipped, was not cancelled, returns are separate
  shortest path (18 steps):
     1. The order is placed or processing
     2. customer asks to cancel the order by its number
     3. agent looks up the customer's orders
     4. lookup shows the order placed or processing
     5. agent proposes: cancel the whole order, refund the total to its payment method
     6. customer says yes
     7. agent sends the cancel
     8. cancel call times out (nothing changed)
     9. agent looks up the customer's orders
    10. lookup shows the order placed or processing
    11. order ships
    12. agent sends the cancel again
    13. cancel call times out (nothing changed)
    14. agent looks up the customer's orders
    15. lookup shows the order shipped
    16. agent asks store staff to follow up (cancellation unknown)
    17. follow-up task created
    18. agent tells the customer: it is not known whether the order was cancelled; no refund was issued; store staff will follow up
CO-06 Limited retries: holds
CO-07 Unfinished orders go to store staff: BREAKS
  violation: order cancelled with no refund shown, or cancellation unknown, and no hand-off made
  shortest path (5 steps):
     1. The order is already cancelled, no refund pending or issued
     2. customer asks to cancel the order by its number
     3. agent looks up the customer's orders
     4. lookup shows the order cancelled, no refund
     5. agent tells the customer: the order is already cancelled
  violation: hand-off (cancellation unknown) in a situation CO-07 does not name
  shortest path (15 steps):
     1. The order is placed or processing
     2. customer asks to cancel the order by its number
     3. agent looks up the customer's orders
     4. lookup shows the order placed or processing
     5. agent proposes: cancel the whole order, refund the total to its payment method
     6. customer says yes
     7. agent sends the cancel
     8. cancel call times out (nothing changed)
     9. agent looks up the customer's orders
    10. lookup shows the order placed or processing
    11. agent sends the cancel again
    12. cancel call times out (nothing changed)
    13. agent looks up the customer's orders
    14. lookup shows the order placed or processing
    15. agent asks store staff to follow up (cancellation unknown)
S-1 No unfinished order left with nobody (stakeholder line, §2): BREAKS
  violation: the order system holds the order cancelled, with no refund, no follow-up task, and the customer not sent to support
  shortest path (14 steps):
     1. The order is placed or processing
     2. customer asks to cancel the order by its number
     3. agent looks up the customer's orders
     4. lookup shows the order placed or processing
     5. agent proposes: cancel the whole order, refund the total to its payment method
     6. customer says yes
     7. agent sends the cancel
     8. cancel call times out (it will still cancel, later)
     9. agent looks up the customer's orders
    10. lookup shows the order placed or processing
    11. the late cancel takes effect
    12. agent sends the cancel again
    13. cancel call reports the order not found
    14. agent tells the customer: the order was not cancelled
S-2 What the agent said is true (G-03 against the order system): BREAKS
  violation: told not cancelled, but it is
  shortest path (14 steps):
     1. The order is placed or processing
     2. customer asks to cancel the order by its number
     3. agent looks up the customer's orders
     4. lookup shows the order placed or processing
     5. agent proposes: cancel the whole order, refund the total to its payment method
     6. customer says yes
     7. agent sends the cancel
     8. cancel call times out (it will still cancel, later)
     9. agent looks up the customer's orders
    10. lookup shows the order placed or processing
    11. the late cancel takes effect
    12. agent sends the cancel again
    13. cancel call reports the order not found
    14. agent tells the customer: the order was not cancelled

Chart: 18 states, 28 arrows; 9415 model steps hidden inside merged states

Scenario map: 31 scenario rows: 25 one path, 0 no path, 6 ambiguous
  CO-S01 rows 1-3: one path
  CO-S02 rows 1-3: one path
  CO-S03 rows 1-3: one path
  CO-S04 rows 1-3: one path
  CO-S05 rows 1-3: one path
  CO-S06 rows 1-2: one path
  CO-S07 rows 1-3: one path
  CO-S08 rows 1-3: one path
  CO-S09 rows 1-3: one path
  CO-S10 rows 1-2: one path
  CO-S11 rows 1: one path
  CO-S11 rows 2: one path
  CO-S12 rows 1-2: ambiguous (9 paths; the paths part at step 8: 'cancel call times out (it did cancel)' vs 'cancel call times out (it will still cancel, later)')
  CO-S13 rows 1-2: one path
  CO-S14 rows 1-2: one path
  CO-S15 rows 1-2: ambiguous (2 paths; the paths part at step 13: 'agent asks store staff to follow up (cancellation unknown)' vs 'agent looks up the customer's orders')
  CO-S16 rows 1: one path
  CO-S16 rows 2: one path
  CO-S16 rows 3: one path
  CO-S17 rows 1-2: one path
  CO-S17 rows 3: one path
  CO-S18 rows 1-2: one path
  CO-S19 rows 1-2: ambiguous (2 paths; the paths part at step 10: 'refund call times out (refund created, pending)' vs 'refund call times out (nothing new created)')
  CO-S20 rows 1: ambiguous (2 paths; the paths part at step 10: 'refund call times out (refund created, failed)' vs 'refund call times out (nothing new created)')
  CO-S20 rows 2: one path
  CO-S21 rows 1: ambiguous (2 paths; the paths part at step 10: 'refund call times out (refund created, pending)' vs 'refund call times out (nothing new created)')
  CO-S21 rows 2: ambiguous (2 paths; the paths part at step 10: 'refund call times out (refund created, failed)' vs 'refund call times out (nothing new created)')
  CO-S22 rows 1: one path
  CO-S22 rows 2: one path
  CO-S23 rows 1-2: one path
  CO-S24 rows 1-2: one path
Chart arrows no scenario takes: 16
  Looking up orders --> Shipped or already cancelled: part-order or refund-elsewhere request left unanswered  [lookup shows shipped]
     shortest path: The order has shipped or been delivered -> customer asks to cancel only some items -> agent looks up the customer's orders -> lookup shows the order shipped
  Looking up orders --> Shipped or already cancelled: part-order or refund-elsewhere request left unanswered  [lookup shows already cancelled]
     shortest path: The order is already cancelled, refund pending or issued -> customer asks to cancel only some items -> agent looks up the customer's orders -> lookup shows the order cancelled, refund pending or issued
  Looking up orders --> Already cancelled with no refund: nothing handed to staff  [lookup shows already cancelled, no refund]
     shortest path: The order is already cancelled, no refund pending or issued -> customer asks to cancel the order by its number -> agent looks up the customer's orders -> lookup shows the order cancelled, no refund
  Looking up orders --> Already cancelled with no refund, part-order or refund-elsewhere request: unanswered, nothing handed to staff  [lookup shows already cancelled, no refund]
     shortest path: The order is already cancelled, no refund pending or issued -> customer asks to cancel only some items -> agent looks up the customer's orders -> lookup shows the order cancelled, no refund
  Proposal stated, waiting for yes --> Nothing changed, customer told why  [customer stops answering]
     shortest path: The order is placed or processing -> customer asks to cancel the order by its number -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent proposes: cancel the whole order, refund the total to its payment method -> customer stops answering
  Asked which order, or whether to cancel the whole order --> Proposal stated, waiting for yes  [customer asks to cancel the whole order]
     shortest path: The order is placed or processing -> customer asks to cancel only some items -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent says only the whole order can be cancelled -> customer asks to cancel the whole order
  Asked which order, or whether to cancel the whole order --> Nothing changed, customer told why  [customer stops answering]
     shortest path: The order is placed or processing, and a second open order exists -> customer asks to cancel 'my order' without saying which -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent asks which order -> customer stops answering
  Cancel sent --> Told 'not cancelled', but the late cancel went through: no refund, no hand-off  [cancel says not found, though the earlier cancel went through]
     shortest path: The order is placed or processing -> customer asks to cancel the order by its number -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent proposes: cancel the whole order, refund the total to its payment method -> customer says yes -> agent sends the cancel -> cancel call times out (it will still cancel, later) -> agent looks up the customer's orders -> lookup shows the order placed or processing -> the late cancel takes effect -> agent sends the cancel again -> cancel call reports the order not found
  Not cancelled, customer told --> Told 'not cancelled', but the late cancel went through: no refund, no hand-off  [the late cancel takes effect]
     shortest path: The order is placed or processing -> customer asks to cancel the order by its number -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent proposes: cancel the whole order, refund the total to its payment method -> customer says yes -> agent sends the cancel -> cancel call times out (it will still cancel, later) -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent sends the cancel again -> cancel call reports the order not found -> the late cancel takes effect
  Cancel sent, no answer --> Handing to staff as 'cancellation unknown' though the lookup answered  [after the second cancel, lookup shows placed or processing]
     shortest path: The order is placed or processing -> customer asks to cancel the order by its number -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent proposes: cancel the whole order, refund the total to its payment method -> customer says yes -> agent sends the cancel -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent sends the cancel again -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order placed or processing
  Cancel sent, no answer --> Handing to staff as 'cancellation unknown' though the lookup answered  [after the second cancel, lookup shows cancelled, no refund]
     shortest path: The order is placed or processing -> customer asks to cancel the order by its number -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent proposes: cancel the whole order, refund the total to its payment method -> customer says yes -> agent sends the cancel -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent sends the cancel again -> cancel call times out (it did cancel) -> agent looks up the customer's orders -> lookup shows the order cancelled, no refund
  Cancel sent, no answer --> Handing to staff as 'cancellation unknown' though the lookup answered  [after the second cancel, lookup shows shipped]
     shortest path: The order is placed or processing -> customer asks to cancel the order by its number -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent proposes: cancel the whole order, refund the total to its payment method -> customer says yes -> agent sends the cancel -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order placed or processing -> order ships -> agent sends the cancel again -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order shipped
  Handing to staff as 'cancellation unknown' though the lookup answered --> Handed to store staff  [task created]
     shortest path: The order is placed or processing -> customer asks to cancel the order by its number -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent proposes: cancel the whole order, refund the total to its payment method -> customer says yes -> agent sends the cancel -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent sends the cancel again -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent asks store staff to follow up (cancellation unknown) -> follow-up task created
  Handing to staff as 'cancellation unknown' though the lookup answered --> Told 'not known if cancelled' though the lookup showed it shipped  [task created]
     shortest path: The order is placed or processing -> customer asks to cancel the order by its number -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent proposes: cancel the whole order, refund the total to its payment method -> customer says yes -> agent sends the cancel -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order placed or processing -> order ships -> agent sends the cancel again -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order shipped -> agent asks store staff to follow up (cancellation unknown) -> follow-up task created
  Handing to staff as 'cancellation unknown' though the lookup answered --> Staff not confirmed, customer sent to support  [hand-off times out twice]
     shortest path: The order is placed or processing -> customer asks to cancel the order by its number -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent proposes: cancel the whole order, refund the total to its payment method -> customer says yes -> agent sends the cancel -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent sends the cancel again -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent asks store staff to follow up (cancellation unknown) -> follow-up call times out (task created) -> agent asks store staff to follow up again (cancellation unknown) -> follow-up call times out (no task)
  Handing to staff as 'cancellation unknown' though the lookup answered --> Told 'not known if cancelled' though the lookup showed it shipped  [hand-off times out twice]
     shortest path: The order is placed or processing -> customer asks to cancel the order by its number -> agent looks up the customer's orders -> lookup shows the order placed or processing -> agent proposes: cancel the whole order, refund the total to its payment method -> customer says yes -> agent sends the cancel -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order placed or processing -> order ships -> agent sends the cancel again -> cancel call times out (nothing changed) -> agent looks up the customer's orders -> lookup shows the order shipped -> agent asks store staff to follow up (cancellation unknown) -> follow-up call times out (task created) -> agent asks store staff to follow up again (cancellation unknown) -> follow-up call times out (no task)
```

## Real output of `python3 selftest.py`

```
   1. The order is placed or processing
   2. customer asks to cancel the order by its number
   3. agent looks up the customer's orders
   4. lookup shows the order placed or processing
   5. agent proposes: cancel the whole order, refund the total to its payment method
   6. customer says yes
   7. agent sends the cancel
   8. cancel call times out (nothing changed)
   9. agent looks up the customer's orders
  10. lookup shows the order placed or processing
  11. agent sends the cancel again
selftest passed: broken CO-06 caught with the expected 11-step path; real CO-06 holds
```

## Not verified

`index.html` was generated, but it was not opened in a browser in this session: the Playwright tool blocks `file://` URLs, and starting a local web server was not permitted. The Mermaid source has no semicolons. If the chart does not render, paste `chart.mmd` into mermaid.live to see the parser error.
