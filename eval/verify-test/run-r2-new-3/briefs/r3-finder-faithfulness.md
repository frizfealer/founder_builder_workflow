You are reviewing the changes one fix round made to an Agent Spec, a behavior contract for an LLM agent whose scenarios will become executable tests. You did not write it. Find defects; do not edit any file.

Read, in this order: the re-review bundle at /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/verify-test/run-r2-new-3/rereview-r3.md, which holds the pattern edits, every block the fix round added or rewrote in full, diff hunks for lightly edited blocks, the unchanged blocks that cite them, and the findings already answered; then the review packet at /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/verify-test/review-packet.md and the sources it lists. Do not read the full spec or the reference checklists. If a line in the bundle names an id the bundle does not define, grep the spec at /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/verify-test/run-r2-new-3/agent-spec.md for that id and read only that block.

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

Path note: the review packet names eval/verify-test/run/agent-spec.md as the spec. That path belongs to a different run. The spec for this review is /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/verify-test/run-r2-new-3/agent-spec.md. Do not read anything under eval/verify-test/run/ or any other eval/verify-test/run-*/ directory except /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/verify-test/run-r2-new-3/, and in that directory read only the bundle and, for an id lookup, the spec.

## Your role: faithfulness finder

In a re-review round, 'every' and 'each' mean the blocks in sections 1 to 3 of the bundle.

Hunt for **Lies**. Read every rule, failure row, Required event, Forbidden line and reference trajectory against the inputs. Check each tool call's name, parameters and failure modes against the tool list; each domain fact against the domain rules; each authorization rule against the policy. Replay each reference trajectory and confirm its tool results produce exactly the Final state assertions. Confirm each Reference trajectory equals the scenario's blocks with Data variants row 1 substituted for every <column>, and that every other row has identical Required events and final-state lines after substitution.

Your report opens with its count line.

At the very end of your report, after the findings, add one line: "Files read: " followed by the paths you opened.
