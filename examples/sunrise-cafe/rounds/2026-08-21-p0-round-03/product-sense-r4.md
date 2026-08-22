# Product Sense — Sunrise Café Reservation Agent

Authoritative input for this draft: `product-idea.md`. Every normative statement below traces to it. Where a truth the product needs is not supplied, the section says so explicitly rather than stating a guess.

## Product Framing

- **User:** a visitor — a person seeking a table at Sunrise Café.
- **Problem:** getting a table should not require the visitor to understand the café's booking rules or to fill out a traditional reservation form.
- **Desired outcome:** through natural-language conversation, the visitor finds an available table and makes a simulated reservation.
- **Why AI:** the committed interaction is free-form natural-language conversation in which the agent — not the visitor — carries the café's booking rules. Interpreting conversational requests and applying those rules on the visitor's behalf is the AI reservation agent's role.
- **Initial boundary:** reservations are simulated; no real booking is placed with the actual café. The product covers finding an available table and making the simulated reservation.

## Product Scope

**In scope now**

- Natural-language conversation with a visitor about reserving a table.
- Finding an available table for the visitor.
- Making a simulated reservation.
- Applying the café's booking rules on the visitor's behalf, so the visitor never needs to understand them.
- Completing all of the above without requiring the visitor to fill out a traditional reservation form.

**Out of scope**

- Placing real reservations with Sunrise Café — reservations are simulated by definition.

No other scope commitments are established by the authoritative input.

**Committed future scope**

- None. The authoritative input commits no future scope. (Recorded explicitly because committed scope is what distinguishes a deferred decision from a dropped one.)

## Responsibilities & Authority

- The agent conducts the reservation conversation and can carry it to completion: the conversation alone is sufficient for the visitor to find an available table and make the simulated reservation, with no step required of the visitor outside it.
- The agent bears the café's booking rules on the visitor's behalf; the visitor is never required to know, state, or apply them.
- No confirmation requirements, authority limits, or human-escalation policy are established by the authoritative input. None are stated here; whether any agent action requires confirmation or a human is undecided.

## Capabilities & Behaviors

The product must observably:

1. Hold a natural-language conversation in which the visitor expresses a reservation request in their own words — no traditional reservation form is required at any point.
2. Find an available table: determine availability on the visitor's behalf and present an available table to the visitor.
3. Make a simulated reservation for an available table at the visitor's instigation.
4. Let the visitor succeed without understanding the café's booking rules: the agent applies any rule that bears on the outcome; the visitor never has to know one to succeed.

What "available" means and what a simulated reservation records depend on the domain model, which is unresolved this round — see Business & Domain Rules.

## Business & Domain Rules

What the authoritative input establishes:

- Sunrise Café has booking rules, and the product — not the visitor — is responsible for applying them.
- Relieving the visitor of the rules does not exempt the outcome from them: a reservation that violates the café's booking rules is incorrect, even though the visitor never sees the rules. **Invariant.**
- A simulated reservation is only made for a table that is available. **Invariant.**
- A simulated reservation places no real booking with the actual café. **Invariant.**

What is unresolved and deliberately not stated:

- The content of the booking rules.
- The table and availability model: what tables exist, what makes a table available, and whether simulated reservations consume availability for later visitors.
- What a simulated reservation records.

These are unresolved this round and left explicitly open. No substitute values are stated, and nothing in this artifact may be read as supplying them.

## Failure & Recovery

**The product must never claim:**

- That a real reservation has been placed with Sunrise Café — reservations are simulated by definition, so a claim of a real booking asserts something the product does not do.
- That a table is available, or a reservation made, contrary to the domain model: availability and reservation success reported to the visitor must be true.

**Failure behavior:** the authoritative input establishes no behavior for failure paths — no table available, a request the agent cannot understand, a request the rules cannot satisfy. No failure or recovery policy is stated here; it is undecided.

## Acceptable Quality

The product is correct when a visitor can, through natural-language conversation alone — without understanding the café's booking rules and without filling out a traditional reservation form — find an available table and complete a simulated reservation that conforms to those rules.

No quantitative quality thresholds — success rates, latency, supported languages, conversation length — are established by the authoritative input; none are stated.

## Open Questions

None. No question has been explicitly kept open by the founder, and no deferred decisions exist. Where a section above is left open, it says so in place.
