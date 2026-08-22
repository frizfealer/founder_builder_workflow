# Product Sense — Barbershop Rescheduling Agent

Authoritative product truth for this product, owned by P0. Sole authoritative input for this draft: `product-idea.md`. Every statement below is either explicitly stated by that input or necessarily implied by it; where a derivation is not obvious, it is noted. Where no authoritative truth exists, the section says so rather than filling the gap.

## Product Framing

**Who it is for.** Two sides:

- The owner of a one-chair barbershop, whom the agent stands in for.
- A customer of that shop who has an existing appointment and texts to reschedule it.

**The problem.** Reschedule requests arrive as text messages addressed to the owner. Because the agent is a stand-in for the owner, the work it takes over is what would otherwise fall to the owner personally: reading the request, checking the calendar, and settling on a new time with the customer.

**Desired outcome.** The customer's existing appointment ends up at a different time that works for both the customer and the owner, and the owner's calendar reflects it. (The calendar clause is derived: the calendar is the source of truth for free slots, so a move not reflected there would leave the source of truth wrong.)

**Why AI.** The Product Idea specifies an AI stand-in but states no rationale. What is established is only the shape of the work: the request arrives as a customer's text message, and the resulting time must satisfy both the customer and the owner's calendar and scheduling rules. No further justification for an AI solution is established, and none is assumed here.

**Initial boundary.** The only interaction the Product Idea commits the product to is a customer texting to reschedule an existing appointment, and that appointment being moved. Nothing else about the shop's operations is committed.

## Product Scope

**In scope now**

- Receiving a customer's text message requesting to reschedule an existing appointment.
- Determining which times work for the owner, from the owner's calendar and the scheduling rules.
- Moving the existing appointment to a slot that works for both sides, so that the owner's calendar afterwards shows the appointment at its new time and its former time as free.
- Text as the channel with the customer. It is the only channel any authoritative input establishes.

**Out of scope now.** The Product Idea excludes nothing explicitly. The following are out of scope because no authoritative input commits the product to them, not because they are prohibited. Non-exhaustive: creating new bookings, cancelling appointments, waitlists, payments or deposits, reminders and other outbound-initiated contact, more than one chair or barber, service or duration variation (every appointment is 45 minutes), any channel other than text, and anything initiated by the owner rather than by a customer.

**Committed future scope.** None. The Product Idea commits the product to no later capability. This section is deliberately empty rather than unstated: there is currently no committed future scope for a deferred decision to attach to.

## Responsibilities & Authority

**What the agent may do on its own**

- Act in the owner's place in the exchange with the customer. The Product Idea makes the agent a stand-in for the owner, so the owner is not a required participant in the exchange.
- Read the owner's calendar to determine which slots are free.
- Move the existing appointment. The Product Idea states that the agent should move the appointment; no authoritative input makes the owner's approval a precondition of the move, and no such precondition is invented here.

**What requires confirmation or a human.** Unresolved and deliberately not stated. Two authority questions have no authoritative answer, and this Product Sense states no answer for either:

- Whether the customer's agreement to a specific new time is required before the appointment is moved, and what would count as agreement. "A slot that works for both sides" makes the customer's acceptance a condition of a correct outcome, but nothing establishes how the agent determines the customer's side or whether the calendar change may precede it. Until this is resolved, this artifact asserts neither that the agent may move an appointment without the customer's agreement nor that it must obtain one.
- What identification or verification is required before the agent acts on an appointment on the strength of an inbound text, and on what basis an inbound message is tied to one particular existing appointment. The owner's calendar is authoritative for free slots only; nothing establishes how a sender is matched to a booking or what authority a text confers.

**Other human roles.** The Product Idea names only the owner and the customer. No other human role, and no escalation path to any human including the owner, is established.

## Capabilities & Behaviors

The observable behaviors the product must exhibit:

1. It accepts a reschedule request sent by a customer as a text message.
2. It treats the owner's calendar as the source of truth for which slots are free: a time counts as available only when the calendar shows it free.
3. It considers only times that satisfy every scheduling rule and invariant in Business & Domain Rules.
4. It moves the customer's existing appointment to a time that works for both sides, so that afterwards the calendar shows the appointment at the new time and its previous time as free.
5. It never represents a time as available unless the owner's calendar shows it free, and never represents the appointment as moved unless the calendar reflects the move.

Deliberately not stated, because no authoritative input decides them: how the customer's side is established (whether the agent offers candidate times and waits for a choice, or selects one and informs), how many options are offered, how far ahead they may be drawn from, and what the agent sends after a successful move. These are the interaction and authority semantics left open in Responsibilities & Authority.

## Business & Domain Rules

Rules, all explicitly stated by the Product Idea:

- The shop is open Tuesday through Saturday, 10:00–18:00, local to the shop. No appointment may fall on a Sunday or Monday.
- Every appointment is 45 minutes.
- No double-booking.
- The owner's calendar is the source of truth for free slots.

Invariants that must never break:

- **I1.** At most one appointment occupies any moment in time. One chair, no double-booking.
- **I2.** An appointment lies entirely within an open period: it starts no earlier than 10:00 and ends no later than 18:00, Tuesday through Saturday. Derived: a 45-minute appointment starting after 17:15 would run past closing, so 17:15 is the latest valid start.
- **I3.** A moved appointment is still 45 minutes. Duration is a property of appointments, not of the original booking.
- **I4.** A time counts as available only if the owner's calendar shows it free as of the moment the move is made. Time blocked on the calendar is unavailable whatever the reason — the calendar's authority does not depend on why a slot is occupied.
- **I5.** After a successful move, the owner's calendar shows the appointment at its new time and its former time as free. Derived: if the calendar is the source of truth for free slots, occupancy must be recorded there, so a move the calendar does not reflect leaves the source of truth wrong.

Not established by any authoritative input, and deliberately not stated here: buffer, cleaning, or preparation time between appointments; breaks or lunch periods beyond what the calendar shows as blocked; a minimum notice period for rescheduling; a limit on how often an appointment may be rescheduled; how far into the future appointments may be placed; holiday or closure handling beyond what appears on the calendar; and any hold or reservation placed on a candidate slot while an exchange is in progress. Availability is determined solely by the rules above together with the calendar.

## Failure & Recovery

What is established:

- If the move cannot be completed — the calendar is unreachable, the write fails, or the chosen slot was taken in the meantime — the product must not represent the appointment as moved. The appointment stands at its original time until the calendar shows otherwise.
- The product must never state that a time is free when the owner's calendar does not show it free, and must never state that an appointment has been moved when the calendar does not reflect the move. Both follow from the calendar being the source of truth.
- The no-double-booking invariant must hold as of the calendar at the moment the move is made. A slot that was free earlier in the exchange is not thereby still free.

Deliberately left open:

- What the product does when no time satisfies both sides, including when the customer declines every time the calendar and scheduling rules allow. The Product Idea commits the product to moving the appointment to a mutually workable slot but says nothing about the case where none exists. Whether the exchange ends, hands off to the owner, or leaves the appointment untouched with some message to the customer is unresolved, and no behavior is assumed here.
- Beyond not claiming a move that did not happen, no recovery behavior — retrying, alerting the owner, following up later — is established for a failed or interrupted move.

## Acceptable Quality

Good enough means:

- No invariant in Business & Domain Rules is ever violated. They are stated as rules, not preferences: a result that breaks one is wrong however satisfactory it otherwise appears.
- The outcome works for both sides. A move that satisfies the calendar and the scheduling rules but not the customer does not meet the Product Idea's bar. How the customer's side is established is unresolved (see Responsibilities & Authority), so the customer-side half of this bar cannot yet be stated precisely enough for a later phase to verify against.
- Everything the product says to the customer about availability and about the appointment agrees with the owner's calendar.

Not established by any authoritative input, and deliberately not stated: response-time or latency targets; a success, containment, or escalation rate; tone or persona; how many exchanges a reschedule may take; and any ranking among these concerns beyond the absoluteness of the invariants above. No threshold and no trade-off order is established, and none is assumed.

## Open Questions

Empty. This section records only two things: questions the founder deliberately keeps open, and issues Decision Management has classified DEFER. Neither exists yet for this product. The unresolved findings from this round left the round as Issues for routing; they are not recorded here, because deciding which unresolved questions are worth retaining is DROP/DEFER classification, which Decision Management owns rather than this phase.
