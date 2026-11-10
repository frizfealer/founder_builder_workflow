# Verification briefs

Step 4 of the skill sends these briefs to reviewers who start with no context. Each brief is self-contained: paste the shared header, then the role section, then fill the bracketed slots.

## What a defective spec looks like

Every finding belongs to exactly one of four classes.

- **Lies.** The spec states something the inputs contradict or do not support. A rule invents a domain fact; a tool is called with a parameter it does not take; a reference trajectory's tool results would not produce the scenario's Final state; the Reference trajectory disagrees with its Data variants row 1.
- **Ambiguous.** Two domain experts could reach different verdicts on the same trajectory. Initial state leaves open a fact the verdict depends on; an Expected line needs judgment; a Forbidden line depends on the agent's wording; a rule uses a term it never defines ("material change").
- **Untestable.** A line cannot become one step without rewording, or the check it implies cannot be computed from world state and the tool log. A rubric dimension is used where a state check, a tool-call check or a verbatim-value message check would do, or a message check is used for a value the agent can rephrase or for a check with a part that needs judgment.
- **Gap.** Something the contract needs is missing. A stakeholder interest no rule protects; a tool failure mode from the inputs with no failure row; an "act only when" rule without both an acting and a holding-back scenario; a failure row that changes the outcome with no scenario; a required User-knows pair the reference trajectory never uses; a rule that requires the agent to tell the user something, with no scenario asserting it.

Wording, style, formatting, heading choice and preferences ("I would phrase this rule differently", "one more scenario would be nice") are not findings.

## Finding format

```
F<n> | <Lies | Ambiguous | Untestable | Gap> | <Important | Nit> | <rule or scenario id, block or section>
Quote: "<the exact line from the spec, or 'absent' for a Gap>"
Evidence: <the input passage, tool definition or other spec line that shows the defect, with file and location>
Pattern: <the general form of the defect, so every instance can be fixed>
```

*Important* means the defect would let an agent pass a scenario it should fail, fail one it should pass, or misbehave in production. *Nit* means the defect is real but changes no verdict.

The report starts with a count line, such as "3 findings: 2 Important, 1 Nit." or "0 findings."

## Shared header (every finder)

> You are reviewing an Agent Spec, a behavior contract for an LLM agent whose scenarios will become executable tests. You did not write it. Find defects; do not edit any file.
>
> Read, in this order: the review packet at [packet path], which lists the inputs the spec was written from; every source file the packet lists; the spec at [spec path]; the checklists in [skill dir]/references/.
>
> A script has already verified section and block order, rule tags, action marks, id references, rule-to-scenario coverage counts, a failure row for every state-changing action, data-variant row counts, read-only actions in Required events, the Appendix A binding of actions to tools, tool names outside Appendix A, data-variant values written as <column>, Initial-state lines about a supporting actor's response that name no action, event lines that rely on the confirmed proposal in a scenario with several confirmation-form pairs, confirmation-form pairs with equal values in scope at once, and dimension bookkeeping (message checks and rubric dimensions). Skip those.
>
> Scope: [the whole spec | only these sections: …].
>
> Findings already answered in earlier rounds are listed at [answered path] when that file exists. Do not report them again; if a fix for one is wrong or incomplete, report that as a new finding quoting the new line.
>
> Report only defects in the four classes below, in the finding format below. Every finding quotes the spec and cites evidence; a suspicion without evidence is not a finding. When you find a pattern, report it once and list every instance in Evidence. If nothing is wrong, report "0 findings."
>
> [paste "What a defective spec looks like" and "Finding format"]

## Finder: faithfulness

Hunt for **Lies**. Read every rule, failure row, Required event, Forbidden line and reference trajectory against the inputs. Check each tool call's name, parameters and failure modes against the tool list; each domain fact against the domain rules; each authorization rule against the policy. Replay each reference trajectory and confirm its tool results produce exactly the Final state assertions. Confirm each Reference trajectory equals the scenario's blocks with Data variants row 1 substituted for every <column>, and that every other row has identical Required events and final-state lines after substitution.

## Finder: verdicts

Hunt for **Ambiguous** and **Untestable**. For each scenario, write down three trajectories in your head:

1. the reference trajectory;
2. a valid variation the scenario does not mention: different read-only lookups, different phrasing, one extra reasonable question;
3. a plausible wrong run: a write before the authorizing turn, a guessed value, a retry after an unknown result.

The scenario must pass the first two and fail the third, and every line must decide its part without judgment. Then turn each Initial state, Required event, Final state and Forbidden line into a Given or Then step; a line that needs rewording or splitting is a finding. Check that each rubric dimension measures something state, tool calls and the message's literal content cannot show, and that each message check is, in full, a match on values the agent copies verbatim, with no part that needs judgment and no date, time, amount or name.

## Finder: coverage

Hunt for **Gaps**. Build these maps and report every empty cell:

- each stakeholder interest to the rules that protect it;
- each tool failure mode in the inputs, and each failure in the brainstorm list of the use-case checklist that the agent can detect, to a failure row;
- each "act only when" rule to one acting scenario and one holding-back scenario;
- each failure row that changes the outcome to a scenario whose Initial state triggers it;
- each required User-knows pair to the step of the reference trajectory that uses it;
- each rule clause that requires the agent to tell the user something to a scenario that asserts it by a rubric dimension;
- each known failure case or transcript in the inputs to a scenario;
- each Initial-state value to the capability's own contract rules it lies inside, such as an available time inside the bookable hours.

## Adversarial verifier brief

> You are checking findings other reviewers made against an Agent Spec, a behavior contract for an
> LLM agent whose scenarios will become executable tests. Your job is to show that each finding is
> Not real or Style only. For each one, look for: a rule, failure row, §5.1 or §5.2 clause, or
> Unambiguity note that already settles the case the finding raises; a quoted line that does not say
> what the finding claims; evidence that is not in the packet or the spec; or a defect that changes
> no verdict and no agent behavior (Style only). Say Real only when you cannot do any of these. The
> reference checklists under references/ are the spec's standards and count as evidence for a
> finding, the same as the packet and the spec.
>
> The first two routes, a clause that settles the case and a quoted line that does not say what the
> finding claims, are limited as follows. The other two, missing evidence and Style only, are not.
> - A refutation must show the finding does not fit its class as defined in 'What a defective spec
>   looks like': for a Lies finding that says no input supports a line, showing that no input
>   contradicts the line is not a refutation; for a Gap finding, showing the behavior is settled by a
>   rule is not a refutation unless a scenario or dimension asserts it.
> - A clause that only permits a kind of line does not refute a finding that one such line
>   contradicts the spec's own definitions, the scenario's Initial state, or the results of the
>   scenario's earlier calls. §5.1's "A supporting actor answers every call normally unless an
>   Initial-state line says otherwise" lets a scenario inject an outcome, but that outcome's entry in
>   Appendix A's "Outcomes, as tool results" cell must still describe something that can be true of
>   the scenario at that call, given its Initial state and the results of the calls before it.
> - The line a finding quotes as defective does not refute the finding by restating what it says.
>   Refute it with an input or another spec line that supports what this line says in this case, not
>   one that only permits lines of its kind.
>
> Read the spec at [spec path]; then the review packet at [packet path] and the sources it lists; then the findings at
> [findings path]; you report, you do not decide: the main thread decides each drop. Grep the spec for any id a finding names that you have not read.
>
> For each finding, one line: `<id> | Real / Not real / Style only | Important / Nit | <the clause
> or line that refutes it, quoted, or why you could not refute it>`. Then the count line: how many
> of each verdict.
