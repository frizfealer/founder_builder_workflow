# Product Sense — Sunrise Café Reservation Agent

Authoritative product truth for P0. Every statement here traces to the Product Idea
or to a necessary implication of it. Where product truth does not yet exist, the
section says so explicitly rather than filling the gap with a plausible answer.

## Product Framing

- **User** — a visitor to Sunrise Café who wants a table.
- **Problem** — reserving a table today requires the visitor to know the café's
  booking rules or to fill out a traditional reservation form.
- **Desired outcome** — the visitor finds an available table and holds it through a
  simulated reservation, without needing either of those things.
- **Why AI** — the visitor expresses the request in natural-language conversation,
  and the product interprets it and applies the café's booking rules on the
  visitor's behalf.
- **Initial boundary** — the product covers finding a table and making a simulated
  reservation for Sunrise Café. A simulated reservation is not a real booking and
  creates no obligation on the café.

## Product Scope

**In scope now**

- Natural-language conversation as a sufficient path from request to completed
  simulated reservation.
- Finding a table that is available.
- Creating a simulated reservation.
- Producing outcomes that conform to the café's booking rules without requiring the
  visitor to know or apply them.

**Out of scope**

- Real reservations. The Product Idea commits to a simulated reservation, so the
  product creates no real, binding hold on the café.

**Not excluded, and not committed**

The Product Idea says the visitor need not fill out a traditional reservation form
and need not understand the booking rules. That makes the conversational path
sufficient on its own; it does not establish that other paths are forbidden. No
statement about non-conversational entry points, staff-facing surfaces, or rule
disclosure to the visitor is made here in either direction.

**Committed future scope**

None. The authoritative inputs commit the workflow to nothing beyond the in-scope
list above.

## Responsibilities & Authority

**The agent acts on its own to**

- Interpret the visitor's natural-language request.
- Determine whether a table is available for that request.
- Present an available table to the visitor.

**The agent acts only on the visitor's expressed intent to**

- Create a simulated reservation. The Product Idea has the visitor make the
  reservation through conversation, so a reservation the visitor did not ask for is
  not a reservation this product may create.

**The agent must never**

- Create a real booking, or act as if it holds authority to commit the café.

**Unresolved and deliberately not stated**

Whether creating a simulated reservation requires an explicit confirmation step —
the agent restating the details and the visitor assenting before the reservation
exists — is not established by the authoritative inputs. Neither is whether any
part of the flow requires a human staff member. This section is open on both
points; no confirmation semantics and no escalation authority should be read into
it.

## Capabilities & Behaviors

1. **Converses in natural language.** The visitor states the request in their own
   words and receives the agent's response in the same form.
2. **Finds an available table.** Given the visitor's request, the agent identifies a
   table that is available and presents it.
3. **Requires no rule knowledge from the visitor.** The visitor reaches a completed
   simulated reservation without stating, knowing, or applying any of the café's
   booking rules, and without filling out a reservation form.
4. **Creates a simulated reservation** at the visitor's request.
5. **Never presents an unavailable table as available.** Availability claims the
   agent makes are true of the availability the product maintains.
6. **Never presents a simulated reservation as a real booking.**

Behaviors 2 and 4 have observable shape but not yet observable content: what makes
a table available, and what a reservation consists of, are unresolved below.

## Business & Domain Rules

- **The café has booking rules.** The Product Idea refers to them as existing.
- **The outcome must conform to them regardless of who knows them.** Relieving the
  visitor of understanding the rules does not relieve the reservation of obeying
  them. The agent carries the conformance the visitor no longer carries.

**Invariants**

- A simulated reservation is never created for a table that is not available.
- A simulated reservation never creates a real obligation on Sunrise Café.

**Unresolved and deliberately not stated**

- **What the café's booking rules are.** No party-size limits, seating durations,
  operating hours, lead times, or hold policies are established by the authoritative
  inputs. The conformance requirement above is committed; its content is not.
- **What availability means.** The table inventory, what a table is available *for*
  (a time, a duration, a party size), and whether an existing simulated reservation
  reduces availability for anyone else are all unestablished. No persistence model
  across visitors or sessions should be read into this section.
- **What a reservation consists of.** What the agent must obtain from the visitor,
  and what the resulting reservation records, are not established.

## Failure & Recovery

**The product must never claim**

- That a simulated reservation is a real reservation at Sunrise Café.
- That a table is available, or reserved, when it is not.

**Unresolved and deliberately not stated**

What the agent does when no table satisfies the request, when it cannot interpret
what the visitor asked for, or when it cannot determine availability, is not
established. No recovery behavior — offering alternatives, escalating to staff,
holding the conversation open — is committed here. What holds in every such case is
the invariant above: the agent makes no false availability or reservation claim, and
creates no reservation that is not available.

## Acceptable Quality

- **Conversation alone must be sufficient.** A visitor who knows none of the café's
  booking rules, and fills out no form, still reaches a completed simulated
  reservation through conversation when a table is available. A flow that only works
  for a visitor who already knows the rules does not meet the product's intent.
- **Availability truthfulness is not a trade-off.** The invariant against false
  availability and false-booking claims holds regardless of how much more helpful,
  faster, or more conversational the alternative would be.

**Unresolved and deliberately not stated**

No numeric bar is established: no success rate, no response latency, no bound on how
many turns a reservation may take, no accuracy target for interpreting requests. No
ranking among quality concerns beyond the invariant above is established either.

## Open Questions

None. Nothing has been deliberately kept open by the founder, and no Issue from this
round has been classified DEFER. The unresolved items marked in the sections above
left this round as Issues in the PhaseResult and are awaiting routing, not retained
here as product truth.
