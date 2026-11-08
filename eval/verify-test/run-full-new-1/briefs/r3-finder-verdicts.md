You are reviewing the changes one fix round made to an Agent Spec, a behavior contract for an LLM agent whose scenarios will become executable tests. You did not write it. Find defects; do not edit any file.

Read, in this order: the re-review bundle at /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/verify-test/run/rereview-r3.md, which holds the pattern edits, every block the fix round added or rewrote in full, diff hunks for lightly edited blocks, the unchanged blocks that cite them, and the findings already answered; then the review packet at /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/verify-test/review-packet.md and the sources it lists. Do not read the full spec or the reference checklists. If a line in the bundle names an id the bundle does not define, grep the spec at /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/verify-test/run/agent-spec.md for that id and read only that block.

A script has already verified section and block order, rule tags, action marks, id references, rule-to-scenario coverage counts, a failure row for every state-changing action, data-variant row counts, read-only actions in Required events, the Appendix A binding of actions to tools, tool names outside Appendix A, data-variant values written as <column>, Initial-state lines about a supporting actor's response that name no action, event lines that rely on the confirmed proposal in a scenario with several confirmation-form pairs, confirmation-form pairs with equal values in scope at once, and dimension bookkeeping (message checks and rubric dimensions). Skip those.

Scope: sections 1 to 3 of the bundle. Report a defect in a section-4 context block in one line, tagged Pre-existing, with no Quote or Evidence. Do not report a finding listed under "Findings already answered"; if a fix for one is wrong or incomplete, report that as a new finding quoting the new line.

Report only defects in the four classes below, in the finding format below. Every finding quotes the spec and cites evidence; a suspicion without evidence is not a finding. When you find a pattern, report it once and list every instance in Evidence. If nothing is wrong, report "0 findings."

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

## Your role

In a re-review round, 'every' and 'each' mean the blocks in sections 1 to 3 of the bundle.

Hunt for **Ambiguous** and **Untestable**. For each scenario, write down three trajectories in your head:

1. the reference trajectory;
2. a valid variation the scenario does not mention: different read-only lookups, different phrasing, one extra reasonable question;
3. a plausible wrong run: a write before the authorizing turn, a guessed value, a retry after an unknown result.

The scenario must pass the first two and fail the third, and every line must decide its part without judgment. Then turn each Initial state, Required event, Final state and Forbidden line into a Given or Then step; a line that needs rewording or splitting is a finding. Check that each rubric dimension measures something state, tool calls and the message's literal content cannot show, and that each message check is, in full, a match on values the agent copies verbatim, with no part that needs judgment and no date, time, amount or name.
