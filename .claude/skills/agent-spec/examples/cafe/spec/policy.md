# Policy

The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each break below is a rule that fails in some reachable state, shown as its shortest path.

## Chart steps

| arrow | from | to | step |
|---|---|---|---|
| A1 | Start | Visitor asked | The table is free |
|  |  |  | The table is taken |
| A2 | Visitor asked | Holding a table | visitor asks for a table for 8 or fewer |
| A3 | Visitor asked | Asked for a party size | agent tells the visitor: the largest party is 8 people, and asks for a new party size |
| A4 | Holding a table | Proposal waiting for yes | agent proposes the table and asks for a yes |
| A5 | Holding a table | Nothing booked, visitor told | agent tells the visitor: the table could not be held |
|  |  |  | agent tells the visitor: the table is taken |
| A6 | Asked for a party size | Holding a table | visitor gives a party of 8 or fewer |
| A7 | Asked for a party size | Visitor left | visitor stops answering |
| A8 | Proposal waiting for yes | Visitor left | visitor stops answering |
| A9 | Proposal waiting for yes | Booking | visitor says yes |
| A10 | Proposal waiting for yes | Releasing the hold | visitor says yes and changes the party size |
| A11 | Proposal waiting for yes | Releasing the hold | visitor withdraws |
| A12 | Booking | Booking unknown, visitor told | agent tells the visitor: it is not known whether the table was booked; please call the café |
| A13 | Booking | Holding a table | agent holds the table again |
| A14 | Booking | Nothing booked, visitor told | agent tells the visitor: the table could not be booked |
| A15 | Booking | Booked, visitor told | agent tells the visitor: the table is booked, with its confirmation id |
| A16 | Releasing the hold | Holding a table | agent holds the changed table |
| A17 | Releasing the hold | Nothing booked, visitor told | agent tells the visitor: it could not release the earlier hold, so it cannot propose a new table now |
|  |  |  | agent tells the visitor: nothing was booked |

## Breaks

None.
