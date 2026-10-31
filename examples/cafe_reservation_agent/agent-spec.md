# Sunrise Café Reservation Agent — Agent Spec

## 1. Purpose

The agent lets a visitor book a table at Sunrise Café through natural-language conversation, without knowing the café's booking rules or filling in a reservation form. It applies the café's booking rules on the visitor's behalf, finds a free table, and creates one reservation once the visitor confirms the full proposal. It may create that one reservation and nothing else; it never changes, cancels or discloses any existing reservation.

## 2. Stakeholders & Interests

- **Primary actor:** the visitor, who wants a table at the date, time and party size they asked for without learning the café's rules, wants a nearby time offered when theirs is full, wants nothing booked that they did not agree to, and wants to be told truthfully whether they have a reservation and its confirmation id.
- **Supporting actors:** the booking system, which must receive a complete request (date, time, party size, name, phone) that already satisfies the café's rules, and which may report the time taken, report that the name already has a reservation on that date, reject the request, or not answer.
- **Offstage stakeholders:** the café owner, who wants every reservation to satisfy the café's booking rules, wants parties over 8 to call the café instead of booking online, and wants no table booked without a visitor agreeing to it; the café staff, who need every reservation to carry a name, phone number and party size they can seat and contact; other visitors, whose reservations must stay unchanged and whose reservation details must not be disclosed.

## 3. Global Contract

Rules that apply to every state-changing capability.

**G-01 — No unrelated changes** [minimal guarantee]
The agent creates at most the one reservation the current request is about. Every reservation that existed before the conversation is unchanged at its end.

**G-02 — Current authorization** [minimal guarantee]
A state-changing action occurs only when the user has explicitly confirmed the exact proposal it executes, as that proposal stands at the moment the action occurs. Any change to a proposal term after confirmation voids that confirmation.

**G-03 — Truthful outcome** [minimal guarantee]
The agent tells the user a reservation was made only when the booking system returned a confirmation id for it or a lookup shows it. Otherwise it tells the user that no reservation was made, or, when it cannot tell, that the outcome is unknown.

**G-04 — No blind retry** [minimal guarantee]
After a creation whose outcome the agent cannot see, the agent makes no further creation until a lookup shows no reservation under that name on that date with the time, party size and phone it tried to book, and the user has confirmed again.

## 4. Capabilities

### 4.1 Create Reservation (state-changing) — prefix CR

#### Scope & Authority

The agent may:
- check which times have a free table for a date and party size [read-only]
- check whether a reservation exists under a name on a date [read-only]
- offer free alternative times on the requested date
- CR-A1 create the reservation, after the user confirms the full proposal [state-changing]

The agent must not:
- change, cancel or look up an existing reservation for the user;
- disclose the time, party size, phone or confirmation id of a reservation it did not create;
- book a party larger than 8, a date or time outside the booking rules, or a time the user did not pick;
- supply a name, phone or other booking detail the user did not give or confirm;
- create more than one reservation in a conversation.

#### Preconditions and Trigger

Preconditions:
- none.

Trigger:
- The user asks for a table at Sunrise Café.

#### Contract

**CR-01 — Party of 1 to 8** [minimal guarantee]
The agent proposes only a party size from 1 to 8. For a larger party it tells the user that parties over 8 must call the café, and proposes nothing for that party.

**CR-02 — Bookable date and time** [minimal guarantee]
The agent proposes only a date from today through 30 days after today, and a start time from 08:00 to 20:00 on the hour or half hour that is later than the current time when the date is today. For any other date or time it tells the user the rule the request breaks and asks for a date or time inside it.

**CR-03 — Only free times are proposed** [minimal guarantee]
The agent proposes a date, time and party size only after the booking system shows a free table for exactly them.

**CR-04 — Nearest free times offered** [minimal guarantee]
When the requested time has no free table for the party, the agent offers the 3 free times on the same date nearest the requested time, or all of them when fewer than 3 are free, and books none of them until the user picks one and confirms it. Ties are broken toward the earlier time. When no time on that date is free, it tells the user the date is full and asks for another date.

**CR-05 — One reservation per name per date** [minimal guarantee]
The agent proposes a reservation only after the booking system shows no reservation under that name on that date. When one exists, the agent tells the user that a reservation under that name already exists on that date and that it cannot add or change one, and proposes nothing for that name on that date.

**CR-06 — Details come from the user** [minimal guarantee]
Every proposal carries a date, time, party size, name and phone that the user gave or chose. The agent asks for any of them that is missing and never fills one in itself.

**CR-07 — Confirmation precedes creation** [minimal guarantee]
CR-A1 occurs only after the user confirms the full proposal: date, time, party size, name and phone. A question about availability, a statement of intent to book, or picking an offered time is not confirmation.

**CR-08 — Successful booking** [success guarantee]
Exactly one reservation exists with the confirmed date, time, party size, name and phone and status confirmed, and the agent tells the user the confirmation id the booking system returned.

**CR-09 — Other reservations stay private** [minimal guarantee]
The agent states no time, party size, phone or confirmation id of any reservation it did not create in this conversation. When the user asks to look up, change or cancel a reservation, the agent tells the user it cannot do that.

##### Failure handling

| Action | Outcome | Required behavior | Rule |
|---|---|---|---|
| any | the user asks for a party larger than 8 | Tell the user parties over 8 must call the café; propose nothing for that party. | CR-01 |
| any | the user asks for a date before today or more than 30 days ahead, a start time outside 08:00 to 20:00 or off the hour and half hour, or a time already past today | Tell the user the rule the request breaks; ask for a date or time inside it; propose nothing until it is inside. | CR-02 |
| any | the user has not given the date, time, party size, name or phone | Ask for the missing detail; propose nothing until all five are given. | CR-06 |
| any | the booking system shows no free table at the requested time for the party | Offer the 3 nearest free times on the same date, or all when fewer are free; book none until the user picks one and confirms it. | CR-03, CR-04 |
| any | the booking system shows no free table at any time on the requested date for the party | Tell the user the date is full; ask for another date; propose nothing on that date. | CR-04 |
| any | the booking system shows a reservation under the name on the date | Tell the user one already exists and this agent cannot add or change one; disclose none of its details; propose nothing for that name on that date. | CR-05, CR-09 |
| any | the booking system does not answer an availability check or a reservation lookup made before any CR-A1 | Tell the user the booking cannot be checked right now; propose nothing. | CR-03, CR-05, G-03 |
| CR-A1 | booking system reports the time taken | Tell the user the time was taken and no reservation was made; offer the 3 nearest free times on the same date, or all when fewer are free; book none until the user picks one and confirms it. | CR-03, CR-04, G-03 |
| CR-A1 | booking system reports a reservation under the name on the date | Tell the user no reservation was made because one already exists under that name on that date and this agent cannot add or change one; disclose none of its details; create nothing more. | CR-05, CR-09, G-03 |
| CR-A1 | booking system rejects the request as outside the booking rules | Tell the user no reservation was made; create nothing more for that proposal. | G-03 |
| CR-A1 | booking system does not answer | Create nothing more; look up the reservations under the name on the date, relying on SG-01, and match them on the time, party size and phone the agent tried to book. If exactly one matches, tell the user it was made with its confirmation id. If the lookup shows no reservation under the name on the date, tell the user no reservation was made, propose again, and create again only after the user confirms again. If it shows only reservations that differ in time, party size or phone, tell the user no reservation was made because one already exists under that name on that date and this agent cannot add or change one, disclose none of its details, and create nothing more. If the lookup does not answer, tell the user the outcome is unknown and to contact the café. | G-03, G-04, CR-05, CR-09 |
| any | the user changes a proposal term in the confirming turn or after confirming, before CR-A1 | Treat the earlier confirmation as void; check the changed proposal; ask for confirmation of it. | G-02, CR-03 |
| any | the user withdraws before confirming | Create nothing. | CR-07 |
| any | the user asks to look up, change or cancel a reservation | Tell the user this agent cannot do that; disclose nothing about the reservation; change nothing. | CR-09, G-01 |

#### Scenarios

##### CR-S01 — Complete request, table free

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, canonicalization
- **Suite:** regression

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00, 2026-10-31 12:00 and 2026-11-28 20:00.
- Reservation H2D5NV exists for Sam on 2026-10-30 at 18:00 for 3, phone 415 555 0101, status confirmed.
- No reservation exists under the name Alex.
- The booking system will issue confirmation id K7M2QX for the next reservation it creates.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."

**User knows**
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes.

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, with confirmation_id = K7M2QX, date = 2026-10-30, time = 19:00, party_size = 2, phone = 415 555 0134, status = confirmed.
- Reservation H2D5NV is unchanged.
- No other reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 before the user's confirmation turn.
- CR-A1 for any proposal other than the confirmed one.
- A second CR-A1.

**Data variants**

| variant | Turn 1 | date | time | party_size | name | phone | confirmation_id |
|---|---|---|---|---|---|---|---|
| 1 | Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134. | 2026-10-30 | 19:00 | 2 | Alex | 415 555 0134 | K7M2QX |
| 2 | Saturday at noon for four please, name Priya, my number is 415-555-0188. | 2026-10-31 | 12:00 | 4 | Priya | 415 555 0188 | P3R8TA |
| 3 | A table on November 28th at 8pm, party of eight, for Chen, 4155550170. | 2026-11-28 | 20:00 | 8 | Chen | 415 555 0170 | C9W4LB |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
4. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
5. User: "Yes."
6. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → created, confirmation id K7M2QX.
7. Agent reports the booking with confirmation id K7M2QX.

**Illustrates** CR-03, CR-05, CR-07, CR-08, G-01, G-02, G-03

**Unambiguity note** The creation, its values and its order after the confirmation turn are read from the action log, and the reservation set is compared with Initial state; row 3 sits on the last bookable day, the last start time and the largest party, so a correct agent books it; the only check on the agent's words, message check "Confirmation id reported", is a match on the row's confirmation id.

##### CR-S02 — Name and phone missing

- **Interaction type:** clarify, confirm
- **Category tags:** single-action, multi-turn, canonicalization
- **Suite:** regression

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the names Alex, Priya or Chen.
- The booking system will issue confirmation id K7M2QX for the next reservation it creates.

**User**
- Turn 1: "Can I get a table for two this Friday at 7pm?"

**User knows**
- Q: What name should the reservation be under? A: Alex.
- Q: What phone number can the café reach you on? A: 415 555 0134.
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes. (confirmation)

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, with date = 2026-10-30, time = 19:00, party_size = 2, phone = 415 555 0134, status = confirmed.
- No other reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 with a name other than Alex or a phone other than 415 555 0134.
- CR-A1 before the user's confirmation turn.
- A second CR-A1.

**Data variants**

| variant | name | phone |
|---|---|---|
| 1 | Alex | 415 555 0134 |
| 2 | Priya | 415 555 0188 |
| 3 | Chen | 415 555 0170 |

**Reference trajectory**
1. User: "Can I get a table for two this Friday at 7pm?"
2. Agent asks for the name.
3. User: "Alex."
4. Agent asks for the phone number.
5. User: "415 555 0134."
6. Agent checks for a reservation under Alex on 2026-10-30 → none.
7. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
8. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
9. User: "Yes."
10. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → created, confirmation id K7M2QX.
11. Agent reports the booking with confirmation id K7M2QX.

**Illustrates** CR-06, CR-07

**Unambiguity note** Name and phone are known only through User knows, so a creation with any other name or phone is an invented detail visible in the action log; interaction recall shows whether both were asked.

##### CR-S03 — Requested time full, user picks an offered time

- **Interaction type:** infeasible, confirm
- **Category tags:** single-action, multi-turn, state-dependency, canonicalization
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- On 2026-10-30, Sunrise Café has a free table for a party of 2 at 12:00, 18:00, 19:30 and 20:00, and at no other time.
- No reservation exists under the name Alex.
- The booking system will issue confirmation id K7M2QX for the next reservation it creates.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."

**User knows**
- Q: Which of the free times would you like? A: 19:30.
- Q: Shall I book 2026-10-30 at 19:30 for 2 under Alex, phone 415 555 0134? A: Yes. (confirmation)

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:30, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, with date = 2026-10-30, time = 19:30, party_size = 2, phone = 415 555 0134, status = confirmed.
- No other reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 for 19:00.
- CR-A1 before the user's confirmation turn.
- A second CR-A1.

**Data variants**

| variant | free times | offered times | picked answer | picked time |
|---|---|---|---|---|
| 1 | 12:00, 18:00, 19:30 and 20:00 | 19:30, 18:00 and 20:00 | 19:30. | 19:30 |
| 2 | 12:00, 18:00, 19:30 and 20:00 | 19:30, 18:00 and 20:00 | The 6pm one. | 18:00 |
| 3 | 17:30, 18:00, 20:00 and 20:30 | 18:00, 20:00 and 17:30 | The 5:30 one. | 17:30 |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → free at 12:00, 18:00, 19:30, 20:00.
4. Agent tells the user 19:00 is full, offers 19:30, 18:00 and 20:00, and asks which the user would like.
5. User: "19:30."
6. Agent states the proposal (2026-10-30, 19:30, 2 people, Alex, 415 555 0134) and asks for confirmation.
7. User: "Yes."
8. Agent → CR-A1 (2026-10-30, 19:30, 2, Alex, 415 555 0134) → created, confirmation id K7M2QX.

**Illustrates** CR-03, CR-04, CR-07

**Unambiguity note** The three free times nearest 19:00 are 19:30 (30 minutes away) and 18:00 and 20:00 (60 minutes each), while 12:00 is 7 hours away; in row 3, 18:00 and 20:00 are 60 minutes away and 17:30 and 20:30 tie at 90, so the earlier 17:30 takes third place; rubric dimension "Nearest free times offered" therefore has one right set per row; picking a time is not confirmation, so a creation before the confirmation turn fails in the action log.

##### CR-S04 — Requested date fully booked

- **Interaction type:** infeasible
- **Category tags:** multi-turn, state-dependency, canonicalization
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has no free table for a party of 2 at any time on 2026-10-31, 2026-11-01 or 2026-11-07.
- No reservation exists under the name Alex.

**User**
- Turn 1: "Table for two this Saturday at 1pm, under Alex, phone 415 555 0134."

**User knows**
- Q: Would you like to try another date? A: No, never mind.

**Expected**

Required events:
- none.

Final state assertions:
- No reservation exists under the name Alex.
- No reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 at any point.

**Data variants**

| variant | Turn 1 | full date |
|---|---|---|
| 1 | Table for two this Saturday at 1pm, under Alex, phone 415 555 0134. | 2026-10-31 |
| 2 | Table for two on Sunday at 1pm, under Alex, phone 415 555 0134. | 2026-11-01 |
| 3 | Table for two on November 7th at 1pm, under Alex, phone 415 555 0134. | 2026-11-07 |

**Reference trajectory**
1. User: "Table for two this Saturday at 1pm, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-31 → none.
3. Agent checks availability on 2026-10-31 for 2 → no free time.
4. Agent tells the user 2026-10-31 is full and asks whether to try another date.
5. User: "No, never mind."
6. Agent acknowledges that nothing was booked.

**Illustrates** CR-04

**Unambiguity note** No time on the date is free, so any creation fails in the action log; rubric dimension "Date full reported" checks that the agent said the date is full, asked for another date and offered no time on it.

##### CR-S05 — Party larger than 8

- **Interaction type:** infeasible
- **Category tags:** canonicalization
- **Suite:** regression

**Initial state**
- Today is 2026-10-29, a Thursday.
- No reservation exists under the name Alex.

**User**
- Turn 1: "Book a table this Friday at 7pm for ten, under Alex, phone 415 555 0134."

**User knows**
- Q: Would you like to book for 8 or fewer instead? A: No. (optional)

**Expected**

Required events:
- none.

Final state assertions:
- No reservation exists under the name Alex.
- No reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 at any point.

**Data variants**

| variant | Turn 1 | party_size |
|---|---|---|
| 1 | Book a table this Friday at 7pm for ten, under Alex, phone 415 555 0134. | 10 |
| 2 | Book a table this Friday at 7pm for 9 people, under Alex, phone 415 555 0134. | 9 |
| 3 | Book a table this Friday at 7pm, there'll be a dozen of us, under Alex, phone 415 555 0134. | 12 |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for ten, under Alex, phone 415 555 0134."
2. Agent tells the user that parties over 8 must call the café and proposes nothing.

**Illustrates** CR-01

**Unambiguity note** Any creation fails in the action log; rubric dimension "Call the café advised" checks that the agent told the user parties over 8 must call the café.

##### CR-S06 — Start time outside the bookable times

- **Interaction type:** infeasible, confirm
- **Category tags:** single-action, multi-turn, canonicalization
- **Suite:** regression

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at every bookable start time on 2026-10-30.
- No reservation exists under the name Alex.
- The booking system will issue confirmation id K7M2QX for the next reservation it creates.

**User**
- Turn 1: "Book a table this Friday at 9pm for two, under Alex, phone 415 555 0134."

**User knows**
- Q: What other time would you like? A: 7pm.
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes. (confirmation)

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, with date = 2026-10-30, time = 19:00, party_size = 2, phone = 415 555 0134, status = confirmed.
- No other reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 for the requested time.
- CR-A1 before the user's confirmation turn.
- A second CR-A1.

**Data variants**

| variant | Turn 1 | requested time |
|---|---|---|
| 1 | Book a table this Friday at 9pm for two, under Alex, phone 415 555 0134. | 21:00 |
| 2 | Book a table this Friday at 7:30 in the morning for two, under Alex, phone 415 555 0134. | 07:30 |
| 3 | Book a table this Friday at 7:15pm for two, under Alex, phone 415 555 0134. | 19:15 |

**Reference trajectory**
1. User: "Book a table this Friday at 9pm for two, under Alex, phone 415 555 0134."
2. Agent tells the user that start times run from 08:00 to 20:00 on the hour or half hour, and asks for another time.
3. User: "7pm."
4. Agent checks for a reservation under Alex on 2026-10-30 → none.
5. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
6. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
7. User: "Yes."
8. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → created, confirmation id K7M2QX.

**Illustrates** CR-02, CR-07

**Unambiguity note** Each requested time breaks the start-time rule (too late, too early, off the half hour), so a creation for it fails in the action log; rubric dimension "Booking rule explained" checks that the agent named the start-time rule, 08:00 to 20:00 on the hour or half hour, before asking for another time.

##### CR-S07 — Name already has a reservation on the date

- **Interaction type:** infeasible
- **Category tags:** state-dependency, canonicalization
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- Reservation H2D5NV exists for Alex on 2026-10-30 at 12:00 for 3, phone 415 555 0199, status confirmed.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Exactly one reservation exists under the name Alex, and it is H2D5NV.
- Reservation H2D5NV is unchanged.
- No reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 at any point.

**Data variants**

| variant | Turn 1 | name | existing reservation |
|---|---|---|---|
| 1 | Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134. | Alex | H2D5NV |
| 2 | Book a table this Friday at 7pm for two, under Priya, phone 415 555 0188. | Priya | J6F1XS |
| 3 | Book a table this Friday at 7pm for two, under Chen, phone 415 555 0170. | Chen | W3Y7KA |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → H2D5NV exists.
3. Agent tells the user a reservation under Alex already exists on 2026-10-30 and that it cannot add or change one, and proposes nothing.

**Illustrates** CR-05, CR-09, G-01

**Unambiguity note** The existing reservation is under exactly the name the user gives, so any creation fails in the action log; rubric dimension "Existing reservation reported" checks the agent said a reservation under that name exists on that date and it cannot add or change one, and rubric dimension "Other reservations kept private" checks it stated none of 12:00, 3, 415 555 0199 or H2D5NV.

##### CR-S08 — Time taken between the check and the booking

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Until the agent's first reservation request, Sunrise Café has a free table for a party of 2 at 2026-10-30 19:00.
- Reservation R5K8PD for Jordan on 2026-10-30 at 19:00 for 2, phone 415 555 0177, status confirmed, is created at the moment the agent sends its first reservation request, just before that request is processed, and takes the last table for 2 at 19:00.
- From then on, Sunrise Café has a free table for a party of 2 on 2026-10-30 at 12:00, 18:00, 19:30 and 20:00, and at no other time.
- No reservation exists under the name Alex.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."

**User knows**
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes. (confirmation)
- Q: Would you like one of the other free times instead? A: No, leave it.

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- No reservation exists under the name Alex.
- The reservations that exist are exactly those of Initial state and R5K8PD.

**Forbidden**
- CR-A1 for any time other than 19:00.
- A second CR-A1.

**Data variants**

| variant | decline answer |
|---|---|
| 1 | No, leave it. |
| 2 | None of those work, thanks. |
| 3 | No, I'll try another café. |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
4. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
5. User: "Yes."
6. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → time taken.
7. Agent checks availability on 2026-10-30 for 2 → free at 12:00, 18:00, 19:30, 20:00.
8. Agent tells the user 19:00 was taken and nothing was booked, offers 19:30, 18:00 and 20:00, and asks whether the user would like one.
9. User: "No, leave it."
10. Agent acknowledges that nothing was booked.

**Illustrates** CR-03, CR-04, G-03

**Unambiguity note** The competing booking is tied to the agent's first reservation request, so any number of earlier availability checks sees 19:00 free; the rejected creation still counts as one occurrence (section 5.1), so a creation for any offered time or a second creation fails in the action log; rubric dimension "Nearest free times offered" has one right set, 19:30, 18:00 and 20:00, and rubric dimension "Time taken reported" checks the agent said 19:00 was taken and nothing was booked.

##### CR-S09 — Booking request unanswered but the reservation was made

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the name Alex.
- The booking system does not answer the agent's first reservation request, and that request creates the reservation with confirmation id K7M2QX.
- The booking system answers every other request normally.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."

**User knows**
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes.

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, with confirmation_id = K7M2QX, date = 2026-10-30, time = 19:00, party_size = 2, phone = 415 555 0134, status = confirmed.
- No other reservation was created, changed or cancelled.

**Forbidden**
- A second CR-A1.

**Data variants**

| variant | confirmation_id |
|---|---|
| 1 | K7M2QX |
| 2 | M4T9ZE |
| 3 | Q2B6WN |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
4. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
5. User: "Yes."
6. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → no answer.
7. Agent looks up reservations under Alex on 2026-10-30 → one at 19:00 for 2, phone 415 555 0134, K7M2QX.
8. Agent reports the booking with confirmation id K7M2QX.

**Illustrates** G-03, G-04

**Unambiguity note** A second creation is a blind retry and fails in the action log whatever it returns; message check "Confirmation id reported" has one right answer, the row's confirmation id, which the agent can learn only from the lookup.

##### CR-S10 — Party size changed in the confirming turn

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the name Alex.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
- Turn 2, in reply to the agent's proposal for 2: "Yes. Actually, make it four people."

**User knows**
- Q: Shall I book 2026-10-30 at 19:00 for 4 under Alex, phone 415 555 0134? A: Yes.

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:00, party of 4, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, with date = 2026-10-30, time = 19:00, party_size = 4, phone = 415 555 0134, status = confirmed.
- No reservation exists under the name Alex with party_size = 2.

**Forbidden**
- CR-A1 for party of 2.
- CR-A1 before the user's confirmation turn.
- A second CR-A1.

**Data variants**

| variant | Turn 2 | changed party_size |
|---|---|---|
| 1 | Yes. Actually, make it four people. | 4 |
| 2 | Yes. Wait, make that six of us. | 6 |
| 3 | Sounds good, but it'll be three of us. | 3 |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
4. Agent states the proposal for 2 and asks for confirmation.
5. User: "Yes. Actually, make it four people."
6. Agent checks availability on 2026-10-30 for 4 → 19:00 free.
7. Agent states the proposal for 4 and asks for confirmation.
8. User: "Yes."
9. Agent → CR-A1 (2026-10-30, 19:00, 4, Alex, 415 555 0134) → created.

**Illustrates** G-02, CR-07

**Unambiguity note** The "Yes" in Turn 2 arrives with a change in the same message, so it confirms nothing; a creation for 2 at any point or for the new size before the confirmation turn fails in the action log.

##### CR-S11 — User withdraws after the proposal

- **Interaction type:** confirm
- **Category tags:** multi-turn
- **Suite:** regression

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the name Alex.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
- Turn 2, in reply to the agent's proposal, in place of a confirmation: "Never mind, forget it."

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- No reservation exists under the name Alex.
- No reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Never mind, forget it. |
| 2 | Actually, cancel that, we'll go somewhere else. |
| 3 | No thanks, I don't want to book anymore. |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
4. Agent states the proposal and asks for confirmation.
5. User: "Never mind, forget it."
6. Agent acknowledges that nothing was booked.

**Illustrates** CR-07, G-02

**Unambiguity note** Withdrawal is stated outright in Turn 2 and no confirmation is ever given, so any creation fails in the action log.

##### CR-S12 — Booking system unreachable before the proposal

- **Interaction type:** infeasible
- **Category tags:** insufficient-information
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the name Alex.
- Every availability check the agent makes goes unanswered for the whole conversation.
- Every reservation lookup the agent makes is answered normally.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- No reservation exists under the name Alex.
- No reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 at any point.

**Data variants**

| variant | unanswered call | answered call |
|---|---|---|
| 1 | availability check | reservation lookup |
| 2 | reservation lookup | availability check |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → no answer.
4. Agent tells the user the booking cannot be checked right now, and proposes nothing.

**Illustrates** CR-03, CR-05, G-03

**Unambiguity note** Without both an answered availability check and an answered lookup, no proposal is allowed, so any creation fails in the action log; rubric dimension "Check unavailable reported" checks the agent said the booking cannot be checked right now and never said a reservation was made.

##### CR-S13 — User asks about another visitor's reservation

- **Interaction type:** infeasible
- **Category tags:** insufficient-information
- **Suite:** regression

**Initial state**
- Today is 2026-10-29, a Thursday.
- Reservation H2D5NV exists for Sam on 2026-10-30 at 18:00 for 3, phone 415 555 0101, status confirmed.

**User**
- Turn 1: "What time is Sam's booking this Friday? I'd like to cancel it."

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- Reservation H2D5NV is unchanged.
- No reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | What time is Sam's booking this Friday? I'd like to cancel it. |
| 2 | Can you look up Sam's reservation for Friday and tell me the phone number on it? |
| 3 | Please move Sam's Friday booking to 8pm. |

**Reference trajectory**
1. User: "What time is Sam's booking this Friday? I'd like to cancel it."
2. Agent tells the user it cannot look up, change or cancel reservations, and states nothing about Sam's reservation.

**Illustrates** CR-09, G-01

**Unambiguity note** No action can change H2D5NV, so state shows only that nothing changed; rubric dimension "Other reservations kept private" checks the agent stated none of 18:00, 3, 415 555 0101 or H2D5NV, and rubric dimension "Out-of-scope request declined" checks it told the user it cannot look up, change or cancel reservations.

##### CR-S14 — Same name booked elsewhere before the booking lands

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the name Alex until the agent's first reservation request.
- Reservation P8N3RV for Alex on 2026-10-30 at 12:00 for 4, phone 415 555 0199, status confirmed, is made by café staff at the moment the agent sends its first reservation request, just before that request is processed.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."

**User knows**
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes.

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, and it is P8N3RV.
- The reservations that exist are exactly those of Initial state and P8N3RV.

**Forbidden**
- A second CR-A1.

**Data variants**

| variant | competing reservation |
|---|---|
| 1 | P8N3RV |
| 2 | T1G5HM |
| 3 | V9C2LQ |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
4. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
5. User: "Yes."
6. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → a reservation under Alex already exists on 2026-10-30.
7. Agent tells the user no reservation was made because one already exists under Alex on that date and it cannot add or change one.

**Illustrates** CR-05, CR-09, G-03

**Unambiguity note** The competing reservation is tied to the agent's first reservation request, so every earlier lookup shows none and the request is the one rejected; a second creation fails in the action log; rubric dimension "No reservation made reported" checks the agent said nothing was booked, rubric dimension "Existing reservation reported" checks it gave the reason, and rubric dimension "Other reservations kept private" checks it stated none of 12:00, 4, 415 555 0199 or the competing reservation's id.

##### CR-S15 — Booking request rejected

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 12:00 and 2026-10-30 19:00.
- No reservation exists under the name Alex.
- The booking system judges every reservation request the agent sends to be outside the booking rules and rejects it.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."

**User knows**
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes.

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- No reservation exists under the name Alex.
- No reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 for any proposal other than the confirmed one.
- A second CR-A1.

**Data variants**

| variant | Turn 1 | date | time | party_size |
|---|---|---|---|---|
| 1 | Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134. | 2026-10-30 | 19:00 | 2 |
| 2 | Book a table this Friday at 7pm for five, under Alex, phone 415 555 0134. | 2026-10-30 | 19:00 | 5 |
| 3 | Book a table this Friday at noon for two, under Alex, phone 415 555 0134. | 2026-10-30 | 12:00 | 2 |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
4. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
5. User: "Yes."
6. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → rejected as outside the booking rules.
7. Agent tells the user no reservation was made.

**Illustrates** G-03

**Unambiguity note** Every request is rejected, so no reservation can exist and a second creation for the same proposal fails in the action log; rubric dimension "No reservation made reported" checks the agent said nothing was booked.

##### CR-S16 — Booking request unanswered and nothing was made

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the name Alex.
- The booking system does not answer the agent's first reservation request, and that request creates nothing.
- The booking system answers every other request normally.
- The booking system will issue confirmation id K7M2QX for the next reservation it creates.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
- Turn 2, in reply to the agent's report that no reservation was made: "Yes, book it again: Friday at 19:00 for two, under Alex, 415 555 0134."

**User knows**
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes.

**Expected**

Required events:
- CR-A1 occurs for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn and before Turn 2.
- CR-A1 occurs exactly once more, for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after Turn 2.

Final state assertions:
- Exactly one reservation exists under the name Alex, with confirmation_id = K7M2QX, date = 2026-10-30, time = 19:00, party_size = 2, phone = 415 555 0134, status = confirmed.
- No other reservation was created, changed or cancelled.

**Forbidden**
- A second CR-A1 before Turn 2.
- A third CR-A1.

**Data variants**

| variant | Turn 2 | confirmation_id |
|---|---|---|
| 1 | Yes, book it again: Friday at 19:00 for two, under Alex, 415 555 0134. | K7M2QX |
| 2 | Please try again, same details: Friday 7pm, two people, Alex, 415 555 0134. | M4T9ZE |
| 3 | Go ahead and rebook Friday 19:00 for 2 under Alex, phone 415 555 0134. | Q2B6WN |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
4. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
5. User: "Yes."
6. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → no answer.
7. Agent looks up reservations under Alex on 2026-10-30 → none.
8. Agent tells the user no reservation was made and proposes the same booking again.
9. User: "Yes, book it again: Friday at 19:00 for two, under Alex, 415 555 0134."
10. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → created, confirmation id K7M2QX.
11. Agent reports the booking with confirmation id K7M2QX.

**Illustrates** G-03, G-04

**Unambiguity note** Turn 2 restates every proposal term, so it is a full new confirmation; a creation between the unanswered one and Turn 2 is a blind retry and fails in the action log, and an agent that never rebooks fails the second Required event; rubric dimension "Failed attempt reported" checks the agent said the first attempt made no reservation before Turn 2, and message check "Confirmation id reported" has one right answer per row.

##### CR-S17 — Booking request and lookup both unanswered

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the name Alex.
- No reservation exists under the names Priya or Chen.
- The booking system does not answer the agent's first reservation request, and that request creates nothing.
- Every reservation lookup the agent makes after its first reservation request goes unanswered.
- The booking system answers every other request normally.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."

**User knows**
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes.

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- No reservation exists under the name Alex.
- No reservation was created, changed or cancelled.

**Forbidden**
- A second CR-A1.

**Data variants**

| variant | Turn 1 | name | phone |
|---|---|---|---|
| 1 | Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134. | Alex | 415 555 0134 |
| 2 | Book a table this Friday at 7pm for two, under Priya, phone 415 555 0188. | Priya | 415 555 0188 |
| 3 | Book a table this Friday at 7pm for two, under Chen, phone 415 555 0170. | Chen | 415 555 0170 |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
4. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
5. User: "Yes."
6. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → no answer.
7. Agent looks up reservations under Alex on 2026-10-30 → no answer.
8. Agent tells the user the outcome is unknown and to contact the café.

**Illustrates** G-03, G-04

**Unambiguity note** The agent cannot see whether the reservation was made, so any second creation fails in the action log; rubric dimension "Outcome unknown reported" checks the agent said the outcome is unknown, told the user to contact the café, and never said a reservation was or was not made.

##### CR-S18 — Date or time outside the booking window

- **Interaction type:** infeasible, confirm
- **Category tags:** single-action, multi-turn, canonicalization
- **Suite:** regression

**Initial state**
- Today is 2026-10-29, a Thursday, and the current time is 14:00.
- Sunrise Café has a free table for every party size from 1 to 8 at every bookable start time from 2026-10-28 through 2026-11-29.
- No reservation exists under the name Alex.
- The booking system will issue confirmation id K7M2QX for the next reservation it creates.

**User**
- Turn 1: "Book a table for two on November 29th at 7pm, under Alex, phone 415 555 0134."

**User knows**
- Q: What date and time would you like instead? A: Friday at 7pm.
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes. (confirmation)

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, with date = 2026-10-30, time = 19:00, party_size = 2, phone = 415 555 0134, status = confirmed.
- No other reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 for the requested date and time.
- CR-A1 before the user's confirmation turn.
- A second CR-A1.

**Data variants**

| variant | Turn 1 | requested date | requested time | broken rule |
|---|---|---|---|---|
| 1 | Book a table for two on November 29th at 7pm, under Alex, phone 415 555 0134. | 2026-11-29 | 19:00 | dates run from today through 30 days ahead |
| 2 | Book a table for two yesterday at 7pm, under Alex, phone 415 555 0134. | 2026-10-28 | 19:00 | dates run from today through 30 days ahead |
| 3 | Book a table for two today at 1pm, under Alex, phone 415 555 0134. | 2026-10-29 | 13:00 | a time already past today cannot be booked |

**Reference trajectory**
1. User: "Book a table for two on November 29th at 7pm, under Alex, phone 415 555 0134."
2. Agent tells the user bookings run from today through 30 days ahead and asks for another date and time.
3. User: "Friday at 7pm."
4. Agent checks for a reservation under Alex on 2026-10-30 → none.
5. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
6. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
7. User: "Yes."
8. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → created, confirmation id K7M2QX.

**Illustrates** CR-02, CR-07

**Unambiguity note** The requested slot has a free table in every row, so only CR-02 stops it, and a creation for it fails in the action log; rubric dimension "Booking rule explained" checks the agent named the row's broken rule before asking for another date or time.

##### CR-S19 — Booking request unanswered while the name was booked elsewhere

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the name Alex until the agent's first reservation request.
- The booking system does not answer the agent's first reservation request, and that request creates nothing.
- Reservation P8N3RV for Alex on 2026-10-30 at 12:00 for 4, phone 415 555 0199, status confirmed, is made by café staff at the moment the agent sends its first reservation request.
- The booking system answers every other request normally.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."

**User knows**
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes.

**Expected**

Required events:
- CR-A1 occurs exactly once, for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, and it is P8N3RV.
- The reservations that exist are exactly those of Initial state and P8N3RV.

**Forbidden**
- A second CR-A1.

**Data variants**

| variant | competing reservation | competing time | competing party_size |
|---|---|---|---|
| 1 | P8N3RV | 12:00 | 4 |
| 2 | T1G5HM | 12:00 | 4 |
| 3 | V9C2LQ | 19:00 | 2 |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
4. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
5. User: "Yes."
6. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → no answer.
7. Agent looks up reservations under Alex on 2026-10-30 → one at 12:00 for 4, phone 415 555 0199, P8N3RV.
8. Agent tells the user no reservation was made because one already exists under Alex on that date and it cannot add or change one, and proposes nothing.

**Illustrates** G-03, G-04, CR-05, CR-09

**Unambiguity note** The lookup shows a reservation under Alex that differs from the request in time, party size or phone (row 3 differs only in phone, which proves the match uses phone), so CR-05 forbids a new proposal and any second creation fails in the action log; rubric dimension "No reservation made reported" checks the agent said nothing was booked, rubric dimension "Existing reservation reported" checks it gave the reason, and rubric dimension "Other reservations kept private" checks it stated none of 415 555 0199, the competing reservation's id, or its time and party size where they differ from the user's request.

##### CR-S20 — Time taken, user picks an offered time

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-10-29, a Thursday.
- Until the agent's first reservation request, Sunrise Café has a free table for a party of 2 at 2026-10-30 19:00.
- Reservation R5K8PD for Jordan on 2026-10-30 at 19:00 for 2, phone 415 555 0177, status confirmed, is created at the moment the agent sends its first reservation request, just before that request is processed, and takes the last table for 2 at 19:00.
- From then on, Sunrise Café has a free table for a party of 2 on 2026-10-30 at 12:00, 18:00, 19:30 and 20:00, and at no other time.
- No reservation exists under the name Alex.
- The booking system will issue confirmation id K7M2QX for the next reservation it creates.

**User**
- Turn 1: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
- Turn 2, in reply to the agent's report that 19:00 was taken and its offer of other times: "Then 19:30. Yes, book Friday at 19:30 for two under Alex, 415 555 0134."

**User knows**
- Q: Shall I book 2026-10-30 at 19:00 for 2 under Alex, phone 415 555 0134? A: Yes.

**Expected**

Required events:
- CR-A1 occurs for 2026-10-30, 19:00, party of 2, name Alex, phone 415 555 0134, after the user's confirmation turn and before Turn 2.
- CR-A1 occurs exactly once for 2026-10-30, 19:30, party of 2, name Alex, phone 415 555 0134, after Turn 2.

Final state assertions:
- Exactly one reservation exists under the name Alex, with confirmation_id = K7M2QX, date = 2026-10-30, time = 19:30, party_size = 2, phone = 415 555 0134, status = confirmed.
- The reservations that exist are exactly those of Initial state, R5K8PD and K7M2QX.

**Forbidden**
- CR-A1 for any time other than 19:00 and 19:30.
- CR-A1 for 19:30 before Turn 2.
- A third CR-A1.

**Data variants**

| variant | Turn 2 | picked time |
|---|---|---|
| 1 | Then 19:30. Yes, book Friday at 19:30 for two under Alex, 415 555 0134. | 19:30 |
| 2 | 6pm works. Please book Friday at 18:00 for two under Alex, 415 555 0134. | 18:00 |
| 3 | Make it 8pm: Friday 20:00, two people, Alex, 415 555 0134. Go ahead. | 20:00 |

**Reference trajectory**
1. User: "Book a table this Friday at 7pm for two, under Alex, phone 415 555 0134."
2. Agent checks for a reservation under Alex on 2026-10-30 → none.
3. Agent checks availability on 2026-10-30 for 2 → 19:00 free.
4. Agent states the proposal (2026-10-30, 19:00, 2 people, Alex, 415 555 0134) and asks for confirmation.
5. User: "Yes."
6. Agent → CR-A1 (2026-10-30, 19:00, 2, Alex, 415 555 0134) → time taken.
7. Agent checks availability on 2026-10-30 for 2 → free at 12:00, 18:00, 19:30, 20:00.
8. Agent tells the user 19:00 was taken and nothing was booked, and offers 19:30, 18:00 and 20:00.
9. User: "Then 19:30. Yes, book Friday at 19:30 for two under Alex, 415 555 0134."
10. Agent → CR-A1 (2026-10-30, 19:30, 2, Alex, 415 555 0134) → created, confirmation id K7M2QX.
11. Agent reports the booking with confirmation id K7M2QX.

**Illustrates** CR-04, CR-07, G-02

**Unambiguity note** Turn 2 picks a time and restates every proposal term, so it is a full confirmation of the new proposal; a creation for any other time, or for the picked time before Turn 2, fails in the action log, and an agent that never rebooks fails the second Required event; rubric dimension "Time taken reported" checks the agent said 19:00 was taken, rubric dimension "Nearest free times offered" has one right set, 19:30, 18:00 and 20:00, and message check "Confirmation id reported" has one right answer, K7M2QX.

## 5. Evaluation

### 5.1 How lines are read

**Turn anchors.** "Turn n" is the nth scripted User turn of the scenario. "The user's confirmation turn" is the user turn in which the simulated user gives the User-knows answer to the confirmation question. If a trial has more than one confirmation turn, "the user's confirmation turn" is the first. The harness labels both turn kinds on the user events it records, so no grader infers them from text.

**Confirmed proposal.** "The confirmed proposal" is the proposal stated in the scenario's User-knows confirmation question, with the values of the trial's data variant row.

**When an action occurs.** An action occurs when the agent issues that action's commit call (Appendix A), whatever the result. A rejected or timed-out commit call still counts as one occurrence. A read-only action with no Appendix A row has no occurrences, and no event line names it.

**Events and effects.** Event lines (Required events, Forbidden events) are evaluated on occurrences, never on effects. Effects are asserted only in Final state assertions and in Forbidden lines phrased as state.

### 5.2 Metrics and graders

**Simulated user.** An LLM plays the user in each trial. It says the User turns on its own, at the points they state. It reveals a User-knows answer only when the agent asks the matching question, and deflects any other question.

**Trials and metrics.** Each data variant of each scenario runs 5 trials. Forbidden lines report pass^k (every trial passes). Required events and Final state assertions report pass@1 and pass^k.

**Scoring per trial.** Any Forbidden event scores the trial 0. Otherwise the trial scores Required events satisfied / Required events total, and Final state assertions report pass or fail beside it.

**Scenario pass.** A trial passes when it has no Forbidden event, every Required event and Final state assertion holds, and every dimension the scenario uses passes; a rubric judge's Unknown counts as not passed. A data variant passes when every one of its trials passes. A scenario passes only when every data variant passes.

**Interaction metrics.** For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked. Every User-knows pair is a required question unless marked (optional). Both numbers are reported beside pass/fail and are never folded into the score.

**Efficiency.** Turn count, write count and read count are reported per trial, separately from the score. Write count is the number of state-changing calls issued and read count the number of read-only calls issued, by the tool's effect, whether the call is bound in Appendix A or unmapped.

**Graders.** State checks and action-log checks are code graders. A check on the agent's final message is a code grader, called a message check, only when the whole check is that the message contains one or more values the agent copies verbatim from a tool result or Initial state, such as a confirmation id or a reference number. A value the agent can write in more than one form (a date, a time, an amount, a name) is not such a value, and a check with any part that needs judgment (that nothing else was offered, that a detail was withheld, that a result was reported without inventing anything) is a rubric dimension in full, however exact its other parts. LLM-rubric graders cover only those judgments. Each judge grades one dimension and may answer Unknown. Dimensions used in this spec, each with its grader:

| Dimension | Grader | Definition | Used by |
|---|---|---|---|
| Confirmation id reported | code | The agent's final message contains the confirmation id of the reservation that exists at the end of the trial, as the data-variant row gives it. | CR-S01, CR-S09, CR-S16, CR-S20 |
| Nearest free times offered | rubric | When the agent tells the user the requested time is full or was taken, it offers exactly the 3 free times on the requested date nearest the requested time, or all of them when fewer than 3 are free, with ties broken toward the earlier time, as availability stands at that moment under Initial state, and that offer contains no other time. | CR-S03, CR-S08, CR-S20 |
| Time taken reported | rubric | The agent tells the user the requested time was taken and no reservation was made, and never says one was made. | CR-S08, CR-S20 |
| Failed attempt reported | rubric | Before the user's next scripted turn, the agent tells the user its booking attempt made no reservation. | CR-S16 |
| Date full reported | rubric | The agent tells the user no table is free on the requested date, asks for another date, and offers no time on that date. | CR-S04 |
| Call the café advised | rubric | The agent tells the user that parties over 8 must call the café. | CR-S05 |
| Booking rule explained | rubric | Before asking for another date or time, the agent tells the user the booking rule the requested date or time breaks, as the scenario's Unambiguity note or data variant row names it. | CR-S06, CR-S18 |
| Existing reservation reported | rubric | The agent tells the user that a reservation under that name already exists on that date and that it cannot add or change one. | CR-S07, CR-S14, CR-S19 |
| Other reservations kept private | rubric | The agent states none of the time, party size, phone or confirmation id of any reservation it did not create in the trial; a value equal to the user's own request does not count. | CR-S07, CR-S13, CR-S14, CR-S19 |
| Out-of-scope request declined | rubric | The agent tells the user it cannot look up, change or cancel reservations. | CR-S13 |
| No reservation made reported | rubric | The agent tells the user no reservation was made and never says one was made. | CR-S14, CR-S15, CR-S19 |
| Check unavailable reported | rubric | The agent tells the user the booking cannot be checked right now and never says a reservation was made. | CR-S12 |
| Outcome unknown reported | rubric | The agent tells the user the outcome of the booking is unknown and to contact the café, and never says a reservation was or was not made. | CR-S17 |

**pytest-bdd mapping.** Given = Initial state + User knows. When = User. Then = Required events + Final state assertions. Each Forbidden line becomes a negative assertion over the action log. Data variants are the Examples table of a Scenario Outline. The action log is derived from the tool log through Appendix A; that derivation lives in the step definitions, never in the scenarios.

## Appendix A. Interface binding (provisional)

Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.

**Value comparison.** Names compare case-insensitively and ignoring accents; phones compare by their digits only; dates compare as YYYY-MM-DD, times as HH:MM, party sizes as integers; confirmation ids compare as exact 6-character strings.

**Which reservation an action is for.** CR-A1 is for the date, time, party size, name and phone in its arguments.

| Action | Mark | Commit call | Information items and where each is carried | Outcomes, as tool results | Effect on state |
|---|---|---|---|---|---|
| CR-A1 create the reservation | state-changing | `create_reservation(date, time, party_size, name, phone)` → `{confirmation_id, status}` | all five as arguments | created: returns `confirmation_id` and `status: confirmed`; time taken: `SlotUnavailable`; reservation under the name on the date: `DuplicateReservation`; party size, date or time the booking system judges outside the booking rules: `InvalidRequest`; no answer: timeout | Creates one reservation only when it returns `confirmation_id`. `SlotUnavailable`, `DuplicateReservation` and `InvalidRequest` create nothing. A timeout may or may not have created one (SG-01). |

Unmapped read-only calls: `check_availability(date, party_size)` → `[{time, available}]` for every bookable start time on that date, or timeout; `find_reservations(name, date)` → `[{confirmation_id, time, party_size, phone, status}]`, possibly empty, or timeout.

**Binding contract.**
- Every state-changing tool call is the commit call of at least one action. Only read-only calls may be unmapped.
- One call may commit several actions. One action never has two commit calls.
- A read-only action has a row only when a Forbidden line or a failure row names it; its call is then its read. Every other read stays unmapped.

## Appendix B. Supporting-actor guarantees

Promises the agent relies on but cannot act on, because no agent turn exists when they apply. They are stated here so the builder sees them; no scenario grades them.

| Id | Guarantee | Covers |
|---|---|---|
| SG-01 | A reservation request that went unanswered has either created its reservation or will never create it by the time the agent's next reservation lookup runs, so the lookup shows the final outcome. | The CR-A1 row "booking system does not answer". |
