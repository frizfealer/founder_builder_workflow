# Sunrise Café reservation agent

The agent lets a visitor book a table at Sunrise Café in conversation, without knowing the café's
booking rules. It may hold a table while the visitor decides, book it once the visitor says yes,
and release a hold it placed. It changes no other reservation.

Read in this order:

1. [Claims](claims.md): what the spec relies on about the café's booking system and about the café.
2. [Rules](rules.md): the rules, what the agent does in each situation, and the decisions behind them.
3. [Policy](policy.md): the chart, and each rule break as its shortest path.
