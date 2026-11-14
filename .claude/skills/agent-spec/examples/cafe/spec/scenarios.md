# Scenarios

Derived from the policy model in `model.py`, plus the cases the model cannot express. Each
model-path scenario fixes what the outside world does; the agent is left free.

## SC-01 Party of more than 8, visitor leaves
Kind: model path
Rules: R-02
World:
1. The table is free
2. visitor asks for a table for more than 8
3. visitor stops answering

## SC-02 Party of more than 8 while the table is taken
Kind: model path
Rules: R-02
World:
1. The table is taken
2. visitor asks for a table for more than 8
3. visitor stops answering

## SC-03 Hold call unanswered though the table was held
Kind: model path
Rules: R-01, R-09
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call gets no answer (table held)

## SC-04 Visitor leaves at the proposal
Kind: model path
Rules: R-01, R-03
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call answers held
4. visitor stops answering

## SC-05 Hold call unanswered, nothing held
Kind: model path
Rules: R-01
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call gets no answer (nothing held)

## SC-06 Party too large, then a party of 8 or fewer
Kind: model path
Rules: R-02, R-01
World:
1. The table is free
2. visitor asks for a table for more than 8
3. visitor gives a party of 8 or fewer
4. hold call gets no answer (table held)

## SC-07 Table taken
Kind: model path
Rules: R-01
World:
1. The table is taken
2. visitor asks for a table for 8 or fewer
3. hold call answers taken

## SC-08 Table held and booked
Kind: model path
Rules: R-01, R-03, R-05, R-09
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call answers held
4. visitor says yes
5. booking call answers booked

## SC-09 Party size changed with the yes, release unanswered (released)
Kind: model path
Rules: R-04, R-06
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call answers held
4. visitor says yes and changes the party size
5. release call gets no answer (released)

## SC-10 Visitor withdraws after the proposal
Kind: model path
Rules: R-07, R-09
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call answers held
4. visitor withdraws
5. release call answers released

## SC-11 Hold expired, new hold unanswered
Kind: model path
Rules: R-10, R-01
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call answers held
4. visitor says yes
5. booking call answers hold expired
6. hold call gets no answer (table held)

## SC-12 Booking call unanswered (booked)
Kind: model path
Rules: R-11, R-09
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call answers held
4. visitor says yes
5. booking call gets no answer (booked)

## SC-13 Booking call unanswered (nothing booked)
Kind: model path
Rules: R-11, R-09
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call answers held
4. visitor says yes
5. booking call gets no answer (nothing booked)

## SC-14 Party size changed with the yes, release unanswered (still held)
Kind: model path
Rules: R-06
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call answers held
4. visitor says yes and changes the party size
5. release call gets no answer (still held)

## SC-15 Party size changed with the yes, old hold released, new hold unanswered
Kind: model path
Rules: R-04, R-06
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call answers held
4. visitor says yes and changes the party size
5. release call answers released
6. hold call gets no answer (table held)

## SC-16 Hold expired twice
Kind: model path
Rules: R-10, R-09
World:
1. The table is free
2. visitor asks for a table for 8 or fewer
3. hold call answers held
4. visitor says yes
5. booking call answers hold expired
6. hold call answers held
7. visitor says yes
8. booking call answers hold expired

## SC-17 Visitor asks to change a reservation that exists
Kind: conversational
Rules: R-08
Why not a path: the model holds only the one table this request is about, so it has no reservation that exists to change.
