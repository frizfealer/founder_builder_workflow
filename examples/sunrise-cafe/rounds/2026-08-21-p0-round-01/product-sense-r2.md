# Product Sense — Sunrise Café Reservation Agent

Authoritative input: `product-idea.md`.

Every statement below is either taken directly from that input or derived from it, with
the derivation stated so a reader can check it. Where a section says a value is
unresolved and deliberately not stated, that is the honest state of product truth — not
an omission to be filled in by a later phase.

## Product Framing

**User.** A visitor to Sunrise Café who wants a table.

**Problem.** Two burdens stand between the visitor and a reservation, and the product
exists to remove both: needing to understand the café's booking rules, and needing to
fill out a traditional reservation form.

**Desired outcome.** Within a natural-language conversation, the visitor finds a table
that is available and a reservation is made for it.

**Why AI.** The visitor states what they want in their own words, and the product — not
the visitor — carries the café's booking rules and turns that intent into a reservation.
Interpreting free-form intent while holding the rules on the visitor's behalf is what
makes this an agent rather than a form.

**Initial boundary.** The reservation the product makes is simulated. What "simulated"
commits the product to is unresolved; see Failure & Recovery.

## Product Scope

**In scope now**

- Natural-language conversation as the visitor's path to a reservation.
- Finding a table that is available.
- Making a simulated reservation for that table.
- Holding and applying the café's booking rules on the visitor's behalf.

**Out of scope now**

- Real (non-simulated) reservations.
- Requiring the visitor to understand the café's booking rules.
- Requiring the visitor to fill out a traditional reservation form. The Product Idea
  removes the visitor's *need* for a form; it does not establish that no form exists
  anywhere.

**Committed future scope**

- None. The Product Idea commits the workflow to nothing beyond the above. In
  particular, it does not commit to replacing the simulated reservation with a real one:
  "simulated" appears as the boundary of this product, not as a declared first stage.

## Responsibilities & Authority

**The agent may do on its own**

- Interpret the visitor's natural-language request.
- Apply the café's booking rules to determine what is available.
  *Derived: the visitor must not need to understand the rules, so the product must be
  the party that applies them.*
- Complete the simulated reservation inside the conversation.
  *Derived: the Idea states the visitor can make a reservation using conversation. If
  completing it required a step outside the conversation, that would not hold.*

**Requires the visitor's agreement**

- Creating a reservation for a specific table and time.
  *Derived: the Idea says the visitor makes the reservation. A reservation created for a
  visitor who has not agreed to it is not the visitor making one.*

**Requires a human**

- Nothing. The Product Idea establishes no café staff, operator, or reviewer in the
  visitor's path, and this round introduces none. This records the current authority
  boundary; it is not a rule that no human may ever be involved.

## Capabilities & Behaviors

1. Accept the visitor's request and respond in natural-language conversation.
2. Elicit from the conversation what the visitor wants, including when they want the
   table. *Derived: both availability and a reservation are meaningless without a time.*
   What else a reservation request must specify is unresolved and deliberately not
   stated here.
3. Determine whether a table is available for that request by applying the café's
   booking rules.
4. Report the outcome to the visitor in the conversation: whether a table was found, and
   what was reserved.
5. When no table is available for what the visitor asked, tell the visitor so. Whether
   the product proposes anything else in that situation is not established.
6. Complete a reservation without the visitor stating a booking rule or filling out a
   form.

## Business & Domain Rules

**Established**

- Sunrise Café has booking rules that govern when a table can be reserved. The Product
  Idea names them without stating them.
- Responsibility for those rules sits with the product, not the visitor.

**Not established.** The content of the café's booking rules is not provided by any
authoritative input. This section deliberately states no specific rule — no opening
hours, table inventory or capacity, party-size limits, reservation duration, lead time,
or cancellation policy. Any such rule written here would be a guess standing as product
truth for every later phase.

**Invariants**

- The product may only reserve a table it has determined to be available.
  *Derived: "find an available table and make a reservation" — reserving an unavailable
  table contradicts the stated outcome.*
- What the product tells the visitor about a reservation must match the reservation
  state the product actually holds.
- The visitor never has to know a booking rule to get a correct outcome.

## Failure & Recovery

- When the visitor's request cannot be satisfied, the product says so plainly and does
  not present an unavailable table as available.
- When the product cannot tell what the visitor wants, it asks in the conversation
  rather than guessing and reserving. *Derived from the agreement requirement above.*
- **Must never claim:** that a reservation exists when the product holds none; that a
  table is available when the café's rules say it is not.
- **Unresolved and deliberately not stated:** what the product owes the visitor about
  the reservation being simulated — whether the visitor must be told, and what a
  confirmation may claim about that reservation's standing at the café. This section
  cannot be completed until that is decided.

## Acceptable Quality

- A reservation is correct when what the product created matches the table and time the
  visitor agreed to.
- The value bar, from the Product Idea: the visitor reaches a reservation without having
  understood a booking rule or completed a form. A run that produces a reservation but
  required either is not a success.
- Truthfulness outranks helpfulness. Reporting that no table is available is a correct
  outcome; a reservation the product cannot stand behind is not.
- No quantitative threshold — success rate, latency, conversation length — is
  established by any authoritative input, and none is stated here. How quality is
  measured belongs to P1.

## Open Questions

None. Nothing has been deliberately kept open by the founder, and no issue from this
round has been classified DEFER. Unresolved findings from this round are reported as
Issues in the PhaseResult, not here.
