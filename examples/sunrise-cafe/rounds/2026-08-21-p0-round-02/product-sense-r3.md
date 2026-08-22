# Product Sense — Sunrise Café Reservation Agent

Authoritative input for this draft: `product-idea.md`. No business or domain
context beyond that document was available. Sections below marked as
deliberately open are not oversights — the authoritative inputs do not decide
them, and no value has been assumed.

## Product Framing

**User.** A visitor to Sunrise Café who wants a table.

**Problem.** The visitor wants an available table, but securing one otherwise
requires them to understand the café's booking rules or complete a traditional
reservation form. The café has booking rules that govern which tables can be
booked; the visitor is not expected to know them.

**Desired outcome.** The visitor obtains a simulated reservation for an
available table, entirely through conversation.

**Why AI.** The visitor's request arrives as free-form natural language, and the
café's booking rules must still be satisfied by someone. Since the visitor is
not required to understand those rules, the product carries them and applies
them on the visitor's behalf.

**Initial boundary.** Reservations at Sunrise Café, made through conversation,
and simulated rather than real. A simulated reservation does not commit the
café's actual capacity.

What "simulated" consists of beyond that — whether it produces a record, whether
that record outlives the conversation, whether anyone but this visitor can see
it — is unresolved and deliberately not stated here.

## Product Scope

**In scope now**

- Natural-language conversation between a visitor and the product.
- Finding a table that is available for what the visitor is asking for.
- Making a simulated reservation for that table.
- Applying the café's booking rules on the visitor's behalf.
- Obtaining, within the conversation, whatever details the product needs in
  order to find a table — the conversation is the only interface the visitor
  has.

**Out of scope**

- Requiring the visitor to understand the café's booking rules.
- Requiring the visitor to fill out a traditional reservation form as the path
  to a reservation.
- Committing the café's real capacity. The reservation is simulated, so it
  creates no real obligation on the café or the visitor.

**Committed future scope**

No future scope is committed. In particular, whether non-simulated (binding)
reservations are a later commitment or are excluded outright is unresolved and
deliberately not stated here.

## Responsibilities & Authority

The product is authorized to interpret the visitor's natural-language request
and to determine, on the visitor's behalf, whether a table is available under
the café's booking rules. This follows from the visitor not being required to
understand those rules: if the visitor does not apply them, the product does.

Everything else about authority is unresolved and deliberately not stated here:
whether the product may finalize a simulated reservation on its own or must
obtain the visitor's explicit confirmation first, and whether any café staff
member is in the loop at all.

## Capabilities & Behaviors

The product must exhibit these observable behaviors:

- Accepts a visitor's request in natural language and responds in natural
  language.
- Determines whether a table is available for what the visitor asked for.
- Produces a simulated reservation for an available table.
- Resolves missing details it needs through the conversation itself, rather
  than by handing the visitor a form or asking them to state the booking rules.
- Never requires the visitor to know or satisfy the café's booking rules in
  order to reach a reservation.

What the product does when the visitor's request cannot be satisfied is covered
under Failure & Recovery, and is open.

## Business & Domain Rules

**The rules exist and govern correctness.** Sunrise Café has booking rules that
determine which tables are available. A simulated reservation the product
produces must conform to those rules; a reservation that violates them is
incorrect regardless of how good the conversation was.

**The content of those rules is unresolved and deliberately not stated here.**
No authoritative input supplies the café's table inventory and capacities,
service hours, party-size limits, how long a reservation occupies a table, or
any other booking constraint. This section states that such rules bind the
product, not what they are.

**Invariants**

- A table is presented as available only when the café's booking rules make it
  available.
- A simulated reservation is never represented as committing the café's real
  capacity.

## Failure & Recovery

**Must never claim.** The product must never represent a simulated reservation
as a real, binding booking, and must never state that a table is available when
the booking rules do not make it available.

**Recovery behavior is unresolved and deliberately not stated here.** What the
product does when no table satisfies the request, when it cannot determine
availability, or when the visitor asks for something the booking rules forbid,
is not decided by any authoritative input.

## Acceptable Quality

Two correctness criteria are decided:

- A conversation that ends with the visitor having had to learn the café's
  booking rules, or having been handed a traditional reservation form, has
  failed — regardless of whether a reservation resulted.
- A simulated reservation that violates the café's booking rules is wrong, not
  merely low quality.

Everything that makes "good enough" measurable is unresolved and deliberately
not stated here: how often the product may fail to reach a reservation a visitor
was entitled to, how much conversational back-and-forth is acceptable, and what
response latency the visitor will tolerate.

## Open Questions

None. Nothing has been deliberately kept open by the founder, and no Issue has
been classified DEFER. Unresolved findings from this round leave the round as Issues in
the phase result and are not recorded here.
