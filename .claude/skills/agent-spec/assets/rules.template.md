# Rules

<!-- Plain words: write every rule and decision in the owner's words. A term you coin is defined in one line where it first appears, and used in its everyday sense or not at all. A rule id never stands in for a sentence. -->

The rules the agent follows, the policy that applies them, and the decisions behind them.

## R-01 <title, a short sentence>

<The rule, in the owner's words: what the agent does or must not do, and when.>

Rests on: <C- and D- ids>

## What the agent does

<!-- The policy model.py encodes: one row per situation the agent can be in, in the order a conversation meets them. -->

| situation | the agent | rules |
|---|---|---|
| <what has happened so far, in plain words> | <what the agent does next> | <R- ids> |

## Decisions

<!-- One row per choice the owner made, or accepted from a recommendation. decided by: the owner, or "the owner, accepting the recommendation". -->

| id | decision | decided by | reason |
|---|---|---|---|
| D-01 | <the choice, one sentence> | <who> | <the owner's reason, or what the choice leads to> |
