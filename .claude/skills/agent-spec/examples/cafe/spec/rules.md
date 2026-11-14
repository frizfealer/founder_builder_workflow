# Rules

The rules the agent follows, the policy that applies them, and the decisions behind them.

## R-01 Only held tables are proposed

The agent proposes a table only while it holds that table for the visitor. When the table is taken, or the hold call gets no answer, it tells the visitor and proposes nothing for that table.

Rests on: C-01, C-02, C-12

## R-02 At most 8 people

The agent holds and proposes a table for at most 8 people. For a larger party it tells the visitor the maximum is 8 and asks for a new party size.

Rests on: C-07

## R-03 Book only after a yes to the full proposal

The agent books only after the visitor says yes to the full proposal: café, date, time, party size and name. A question about free tables, or saying they want to book, is not a yes.

Rests on: C-08

## R-04 A changed proposal needs a new yes

When the visitor changes any part of the proposal after saying yes, the earlier yes no longer counts. The agent releases the old hold, holds the changed table, and asks again.

Rests on: C-09, C-12

## R-05 A booking is reported with its confirmation id

When the table is booked, the agent tells the visitor it is booked and gives the confirmation id.

Rests on: C-04, C-13

## R-06 One hold at a time

The agent holds at most one table at any moment. When the proposal changes, it releases the old hold before it holds the new table.

Rests on: C-12

## R-07 Withdrawing releases the hold

When the visitor withdraws before the booking, the agent releases its hold and books nothing.

Rests on: C-12, C-08

## R-08 No other reservation changes

The agent changes only the hold and the booking the visitor's request is about. When the visitor asks to change a reservation that exists, the agent says it cannot and books nothing.

Rests on: C-11

## R-09 The visitor is told what happened

The agent says the table is booked only when the booking call answered "booked". When it cannot tell, it says so.

Rests on: C-04, C-06

## R-10 Hold again once after an expired hold

After the booking call answers "hold expired", the agent holds the table again and asks again, once. After a second expiry it tells the visitor the table could not be booked.

Rests on: C-03, C-10

## R-11 No second booking call after no answer

When the booking call gets no answer, the agent sends no second booking call. It tells the visitor it is not known whether the table was booked and asks them to call the café.

Rests on: C-04, C-06

## What the agent does

| situation | the agent | rules |
|---|---|---|
| the visitor asks for more than 8 people | says the maximum is 8 and asks for a new party size | R-02 |
| the visitor asks for 8 or fewer and nothing is held | holds the table | R-01, R-02, R-06 |
| the hold call answered "held" | proposes the table and asks for a yes | R-01 |
| the hold call answered "taken" | says the table is taken and proposes nothing | R-01 |
| the hold call got no answer | says the table could not be held and proposes nothing | R-01 |
| the visitor said yes to the proposal | books the held table | R-03 |
| the visitor said yes and changed a part of the proposal | releases the old hold, then holds the changed table | R-04, R-06 |
| the visitor withdrew | releases the hold, then says nothing was booked | R-07 |
| the booking call answered "booked" | says the table is booked and gives the confirmation id | R-05, R-09 |
| the booking call answered "hold expired", the first time | holds the table again | R-10 |
| the booking call answered "hold expired", the second time | says the table could not be booked | R-10, R-09 |
| the booking call got no answer | says it is not known whether the table was booked, and asks the visitor to call the café | R-11, R-09 |
| the release call got no answer during a change | says it could not release the earlier hold, and proposes nothing new | R-06 |

## Decisions

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | After a hold expires, the agent holds again once, then gives up. | the owner, accepting the recommendation | Without a bound, the agent could hold and ask forever. |
| D-02 | After a booking call with no answer, the agent sends no second call and sends the visitor to the café. | the owner, accepting the recommendation | A second call could book the table twice. |
