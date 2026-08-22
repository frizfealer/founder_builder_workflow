# Product Sense — Barbershop Reschedule Agent

Authoritative input: `product-idea.md`. Every normative statement below is explicitly stated by that input or necessarily implied by it; where a needed truth is neither, the section says so and the value is deliberately not stated.

## Product Framing

- **User:** a customer of a one-chair barbershop who has an existing appointment and texts to reschedule it. The owner is also served: the product acts in the owner's place for these requests.
- **Problem:** a customer's texted reschedule request must be resolved by moving the appointment to a slot that works for both the customer and the owner.
- **Desired outcome:** the appointment ends up in a slot that works for both sides, and the owner did not have to handle the exchange — the agent stood in.
- **Why AI:** the product is conceived, by its authoritative input, as an AI stand-in for the owner. No further rationale is established by the input, and none is stated here.
- **Initial boundary:** customer-initiated rescheduling of existing appointments at a single one-chair barbershop.

## Product Scope

- **In scope now:**
  - Receiving a customer's reschedule request, which arrives as a text message.
  - Identifying the existing appointment the request concerns; the agent moves only the requesting customer's own appointment.
  - Arriving at a replacement slot that works for both sides and satisfies every rule in Business & Domain Rules.
  - Moving the appointment so the owner's calendar reflects the change, and the customer ends up knowing the new time.
- **Out of scope:** the authoritative input explicitly excludes nothing. Capabilities it does not mention — booking new appointments, cancellations, reminders, payments, walk-ins, any non-text channel — are **undecided, not excluded**: the product is not committed to them, and their absence here is not a commitment against them.
- **Committed future scope:** none. The authoritative input commits to rescheduling only. (Decision Management should read this section accordingly: no deferred commitments exist yet.)

## Responsibilities & Authority

- The agent acts as the owner's stand-in for handling customer reschedule requests, and the agent is the actor that moves the appointment.
- Any move the agent performs must satisfy every rule in Business & Domain Rules; the agent never has authority to violate them.
- **Left open — unresolved and deliberately not stated:**
  - Whether the agent may finalize a reschedule without the customer's explicit confirmation of the proposed slot — equivalently, how "works for the customer" is established. The input commits to the outcome but not to the confirmation mechanism.
  - Whether the agent finalizes calendar moves on its own authority or requires per-move owner approval. "Stand-in for the owner" is consistent with both readings.

## Capabilities & Behaviors

Observable behaviors the product must exhibit:

1. Accept a customer's reschedule request arriving by text message.
2. Determine which existing appointment the request refers to (an appointment cannot be moved without knowing which one).
3. Determine candidate replacement slots using the owner's calendar as the source of truth for free slots, admitting only slots that satisfy Business & Domain Rules.
4. Arrive at a replacement slot that works for both the customer and the owner. (The mechanism by which each side's acceptance is established is left open — see Responsibilities & Authority.)
5. Move the appointment: after a completed reschedule, the owner's calendar reflects the change — the old slot is freed and the new slot is occupied. This follows necessarily from the calendar being the source of truth and from the no-double-booking rule.
6. The customer ends up knowing the appointment's new time: a slot the customer is unaware of cannot work for the customer's side. The channel for conveying it is not established and is not stated here.

## Business & Domain Rules

- Open Tuesday to Saturday, 10:00–18:00.
- Appointments are 45 minutes.
- No double-booking. The shop has one chair, so at most one appointment occupies any moment in time.
- The owner's calendar is the source of truth for free slots.
- Derived boundary: an appointment must lie entirely within open hours — service past close would contradict the stated hours — so the latest start time is 17:15 on an open day.

**Invariants that must never break:** no two appointments overlap; no appointment lies outside open hours; after any move, the owner's calendar truthfully reflects the appointment's actual slot.

Not established by the authoritative input, and deliberately not stated: buffer or turnaround time between appointments; how far in advance a reschedule may reach; any timezone rule; any limit on how often a customer may reschedule.

## Failure & Recovery

- **What the product must never claim:** the agent must never confirm to the customer an appointment time that is not actually secured on the owner's calendar. Claiming an unsecured time would contradict the calendar being the source of truth and risks double-booking.
- **Left open — unresolved and deliberately not stated:** what the agent does when no slot satisfying the rules works for both sides. The committed outcome cannot always be achieved on a finite calendar, and the input establishes no behavior for that branch.
- No recovery behavior is established for the owner's calendar being unreachable; only the never-claim invariant above constrains that situation, and nothing further is stated here.
- No behavior is established for a reschedule text that matches no existing appointment; the committed trigger presupposes one exists.

## Acceptable Quality

A completed reschedule is correct only if all of the following hold: the appointment occupies exactly one slot; that slot was free on the owner's calendar when taken; it is 45 minutes long, entirely within open hours, and overlaps nothing; the calendar reflects the move; and the customer knows the new time. Correctness of every completed reschedule against these conditions is the quality bar the authoritative input establishes.

No threshold is established for response latency, conversational quality, tone, or reschedule success rate, and none is stated here.

## Open Questions

None. The founder has deliberately kept no question open, and no Decision Management deferral exists. Unresolved findings from this round leave it as Issues in the phase result, not as entries here.
