# Product Sense — Barbershop Reschedule Agent

Authoritative input: `product-idea.md`. Every normative statement below is traceable to it; where a needed truth is not derivable from it, the section says so explicitly rather than guessing.

## Product Framing

- **The business**: a one-chair barbershop with a single owner.
- **Users**: the owner, on whose behalf the product acts, and the customer, who interacts with it. The product is an AI stand-in for the owner: it handles the customer's text conversation about rescheduling in the owner's place.
- **Problem**: a customer with an existing appointment texts to reschedule it, and someone must move that appointment to a time that works for both the customer and the shop.
- **Desired outcome**: the appointment is moved to a slot that works for both sides.
- **Why AI**: the Product Idea's premise is an AI acting in the owner's place for these conversations — the reschedule request is handled without the owner conducting the exchange. No further motivation (time savings, after-hours coverage, etc.) is established by the authoritative inputs.
- **Initial boundary**: customer-initiated reschedule requests, arriving by text, for an existing appointment at this shop.

## Product Scope

- **In scope now**: handling a customer's text request to reschedule an existing appointment, and moving that appointment to a slot that works for both sides, using the owner's calendar and the scheduling rules below.
- **Out of scope**: nothing beyond the rescheduling flow is committed by the authoritative inputs. In particular, no commitment exists for booking new appointments, cancellations, reminders, payments, or channels other than text. Their exclusion is not itself a decision — they are simply not committed, and admitting any of them would require new authoritative input.
- **Committed future scope**: none. The authoritative inputs establish no future commitments. (Decision Management reads this section to tell DEFER from DROP; as of this draft there is nothing committed to defer against.)

## Responsibilities & Authority

- The agent acts as the owner's stand-in for the rescheduling flow. The Product Idea assigns the move itself to the agent: for a conforming reschedule — a slot that satisfies every scheduling rule, is free per the owner's calendar, and works for both sides — the agent completes the move on its own; no owner pre-approval step is established by the authoritative inputs, and the stand-in premise is that the owner does not conduct these exchanges.
- The agent's authority extends only to this flow. The authoritative inputs authorize nothing else.
- Completed moves are visible to the owner through the calendar, which must reflect them (see Business & Domain Rules). No additional owner-notification policy is established by the authoritative inputs.
- Whether the customer must explicitly confirm the specific new time before the move — versus the agent inferring fit from the customer's request — is unresolved and deliberately not stated here. See Capabilities & Behaviors.

## Capabilities & Behaviors

Observable behaviors the product must exhibit:

1. **Receive and handle** a customer's text requesting to reschedule an existing appointment, conversing in the owner's place.
2. **Determine availability solely from the owner's calendar**, the source of truth for free slots.
3. **Select a new slot** that satisfies all of the following:
   - falls on an open day (Tuesday through Saturday);
   - lies entirely within opening hours (10:00–18:00) at the 45-minute appointment length;
   - does not overlap any other booking (no double-booking);
   - is free per the owner's calendar;
   - works for both sides. The owner-side criteria are exactly the calendar and the scheduling rules above; the customer-side criterion — how the agent establishes that the slot works for the customer — is unresolved and deliberately not stated.
4. **Execute the move**: the existing appointment leaves its old slot and occupies the new one, and the owner's calendar reflects the change.

Deliberately left open in this draft, because the authoritative inputs do not decide them:

- how customer-side fit is established (behavior 3);
- what the agent does when no conforming free slot works for both sides;
- what the agent does when it cannot tie an incoming text to an existing appointment.

## Business & Domain Rules

- The shop is open Tuesday through Saturday, 10:00–18:00.
- Every appointment is 45 minutes; a rescheduled appointment remains 45 minutes.
- An appointment lies entirely within opening hours on an open day.
- One chair: appointments never overlap. No double-booking, without exception.
- The owner's calendar is the sole source of truth for free slots: a slot is free if and only if the calendar shows it free, and the agent makes no availability judgment apart from it.
- Rescheduling moves the existing appointment: it never duplicates it and never drops it — the customer ends the flow with exactly their one appointment, at the new time.
- Every completed move is reflected in the owner's calendar; otherwise the calendar would no longer be the source of truth.

## Failure & Recovery

What the product must never do or claim (each follows from the rules above):

- Never violate a scheduling rule to satisfy a request — no double-booking, no slot outside open days or hours, regardless of what the customer asks for.
- Never treat a slot as free that the owner's calendar does not show free; when the calendar cannot be consulted, no move happens and no availability is claimed.
- Never tell the customer their appointment was moved unless the move is real and reflected in the owner's calendar.

What the product does instead when it cannot fulfill a request is not established by the authoritative inputs and is deliberately not stated here — specifically: when no conforming free slot works for both sides, and when the incoming text cannot be tied to an existing appointment. Beyond the invariants above, no recovery or messaging policy for an unavailable calendar is established by the authoritative inputs.

## Acceptable Quality

- Rule conformance is absolute, not a quality trade-off: a completed reschedule is correct only if the resulting appointment satisfies every Business & Domain Rule. A single double-booking, out-of-hours appointment, wrong-length appointment, or calendar mismatch is a defect.
- "Works for both sides" is part of correctness. Its owner side is fully defined by the calendar and the scheduling rules; its customer side is unresolved (see Capabilities & Behaviors) and its quality bar cannot be stated until that is resolved.
- No other quality bar — response latency, conversational tone, resolution rate — is established by the authoritative inputs.

## Open Questions

None. No question has been explicitly kept open by the founder, and Decision Management has classified nothing as deferred. (Findings this draft could not resolve are reported through the phase's result for routing, not retained here.)
