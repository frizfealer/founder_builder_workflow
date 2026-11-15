# Assumption-flag test: list every claim about the outside world, and flag the unusual ones

You are building a throwaway instrument, not changing the product. Work only inside
`eval/agent-spec/assumption-flag-test/`. Do not edit the spec or any skill.

Your inputs are exactly:

- `eval/agent-spec/round0-agent-spec.md` — the rules, the failure-handling table, the
  supporting-actor guarantees, Appendix A (tool contract), and anything else it states.
- `eval/agent-spec/review-packet.md` — the record of the interviews with the owner.

Do not read anything else under `eval/`, and do not read `DECISIONS.md`, any `FINDINGS*.md`,
`.sessions/`, or any handoff or notes file. They would bias the result.

## What to build

One file, `claims.md`, holding one table. Each row is one claim that the spec relies on and
that the spec's author could not have verified by reading the two inputs alone. Three kinds:

1. **System behaviour** — how a system outside the agent behaves: the order system, the refund
   or payment side, store staff, the customer's session. What a tool call does, what its
   answers mean, what happens on a timeout or a repeated call, what can change while the
   conversation runs, what one call does or does not do together with another.
2. **Policy decision** — a choice about the business that a rule encodes: who may do what,
   which cases are in or out, and every limit (how many, how long, how much, how often),
   including a limit set to "none".
3. **Missing** — something ordinary practice in this kind of business has a rule or a limit
   for, and the spec has none. List it only if adding it would change a rule, the tool
   contract, or what a customer gets.

**Being decided does not exempt a claim.** A line the packet records as the owner's answer,
or as proposed and confirmed, is still a row. So is a line the spec states as a rule or a
contract. The table is of what the spec depends on, not of what is still open.

Split claims until each row could be true or false by itself. "The call is safe to repeat and
returns the earlier result" is two rows if one could hold without the other.

## Columns

| Column | Content |
|---|---|
| Id | C-01, C-02, … |
| Claim | One plain sentence, in the owner's words, no rule ids or variable names. |
| Kind | system / policy / missing |
| Where | The spec section or rule id that states or relies on it (several if needed). |
| Source | Exactly one of: `owner's words` (quote the packet line) · `proposed, accepted` (the interviewer proposed it, the owner confirmed) · `proposed, not answered` · `spec only` (in the spec, not traceable to the packet) · `silent` (neither input says; the spec's rules need it anyway). Give the packet line number when there is one. |
| Rules that depend on it | Rule ids. |
| Flag | `unusual` / `ok` / `unsure` — see below. |
| Common practice | For `unusual` and `unsure` rows only: what widely used commerce and payment systems, or ordinary store policy, do instead. Name what you are comparing to. One or two sentences. |
| What would change | For `unusual` rows only: which rules or contract lines would change if the common practice applied, and what the customer or the store would see differently. |

## When to flag

Flag a row `unusual` only when both hold:

- Widely used systems behave differently, or ordinary store policy chooses differently, or a
  careful operator would not rely on it without checking; **and**
- if the common practice applied instead, at least one rule or contract line would change, or
  a customer or the store would get a different outcome (money, a wrong message, an order in
  the wrong state).

Use `unsure` when you cannot say what common practice is. Do not flag to be safe, and do not
leave a row `ok` to be polite: a claim the owner stated in his own words is flagged exactly
like any other. You may look up public documentation of real systems to settle a row; if you
do, name the source in the Common practice cell.

Order the table: `unusual` rows first, most costly if wrong at the top; then `unsure`; then `ok`.

## Rules for the work

- Report only. Do not propose spec changes and do not rewrite rules.
- Every row cites where the claim comes from. No citation, no row, except kind `missing`,
  which cites the nearest rule that would hold it.
- Do not merge rows to keep the table short, and do not pad it: a restatement of a row that
  is already listed is not a new row.

## Reply

Total rows; rows by kind; rows by source; the count of `unusual`, `unsure`, `ok`; then the
`unusual` and `unsure` rows in full. Say what you looked up, if anything.
