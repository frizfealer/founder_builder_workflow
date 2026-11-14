# Claims

Every claim the spec relies on about the café's booking system or about Sunrise Café, with its source.

## Systems

| system | owner | docs | tools |
|---|---|---|---|
| booking system | Sunrise Café | none | hold a table, book the held table, release a hold, search free tables |

## Claims

| id | claim | kind | system | source | quote | what ends it | if it differs from what the customer confirmed |
|---|---|---|---|---|---|---|---|
| C-01 | A call to hold a table answers "held", answers "taken", or gets no answer. | system | booking system | spec only | | | |
| C-02 | A hold call that gets no answer may or may not have held the table. | system | booking system | proposed, accepted | Yes: an unanswered hold or booking call may have done its work. | | |
| C-03 | An unconfirmed hold expires 10 minutes after it was placed. | system | booking system | owner's words | An unconfirmed hold expires 10 minutes after it was placed. | | |
| C-04 | A call to book the held table answers "booked" with a confirmation id, answers "hold expired", or gets no answer; a call with no answer may or may not have booked it. | system | booking system | proposed, accepted | Yes: an unanswered hold or booking call may have done its work. | | |
| C-05 | A call to release a hold answers "released" or gets no answer. | system | booking system | spec only | | | |
| C-06 | When the booking call gets no answer, the agent sends no second booking call, tells the visitor it is not known whether the table was booked, and asks them to call the café. | policy | | proposed, accepted | When the booking call gets no answer, the agent cannot tell whether the table was booked. What should it do? | | |
| C-07 | The largest party the agent may book is 8 people. | limit | | owner's words | The largest table seats 8. | a party of 9 or more is not held or proposed | |
| C-08 | The agent books only after the visitor says yes to the full proposal: café, date, time, party size and name. | policy | | proposed, accepted | When may the agent book? | | |
| C-09 | A change to any part of the proposal after the yes needs a new yes. | policy | | proposed, accepted | If any of these changes after the yes, the visitor must say yes again. | | |
| C-10 | After a hold expires, the agent holds the table again once; after a second expiry it tells the visitor the table could not be booked. | limit | | proposed, accepted | The agent holds again once. If the hold expires a second time, it tells the visitor the table could not be booked. | the second expiry | |
| C-11 | The agent makes new reservations only; it never changes or cancels one that exists. | policy | | owner's words | Yes, new reservations only. | | |
| C-12 | The agent holds at most one table at a time. | policy | | spec only | | | |
| C-13 | The visitor is told the confirmation id of the booking. | policy | | spec only | | | |
