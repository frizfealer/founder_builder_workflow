# Verification briefs

Step 4 of the skill sends these briefs to reviewers who start with no context. Each brief is self-contained: paste the shared header, then the role section, then fill the bracketed slots.

## What a defective spec looks like

Every finding belongs to exactly one of four classes.

- **Lies.** The spec states something the inputs contradict or do not support. A rule invents a domain fact; a tool is called with a parameter it does not take; a reference trajectory's tool results would not produce the scenario's Final state; the scenario body disagrees with its Data variants row 1.
- **Ambiguous.** Two domain experts could reach different verdicts on the same trajectory. Initial state leaves open a fact the verdict depends on; an Expected line needs judgment; a Forbidden line depends on the agent's wording; a rule uses a term it never defines ("material change").
- **Untestable.** A line cannot become one pytest-bdd step without rewording, or the check it implies cannot be computed from world state and the tool log. A rubric dimension is used where a state or tool-call check would do.
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

> You are reviewing an Agent Spec, a behavior contract for an LLM agent whose scenarios will become pytest-bdd tests. You did not write it. Find defects; do not edit any file.
>
> Read, in this order: the review packet at [packet path], which lists the inputs the spec was written from; every source file the packet lists; the spec at [spec path]; the checklists in [skill dir]/references/.
>
> A script has already verified section and block order, rule tags, id references, rule-to-scenario coverage counts, data-variant row counts, read-only tools in Required events and rubric-dimension bookkeeping. Skip those.
>
> Scope: [the whole spec | only these sections: …]. Already answered, do not report again: [list of finding summaries, or "none"].
>
> Report only defects in the four classes below, in the finding format below. Every finding quotes the spec and cites evidence; a suspicion without evidence is not a finding. When you find a pattern, report it once and list every instance in Evidence. If nothing is wrong, report "0 findings."
>
> [paste "What a defective spec looks like" and "Finding format"]

## Finder: faithfulness

Hunt for **Lies**. Read every rule, failure row, Required event, Forbidden line and reference trajectory against the inputs. Check each tool call's name, parameters and failure modes against the tool list; each domain fact against the domain rules; each authorization rule against the policy. Replay each reference trajectory and confirm its tool results produce exactly the Final state assertions. Confirm each scenario body uses the values of its Data variants row 1, and that no other row would change which rule applies.

## Finder: verdicts

Hunt for **Ambiguous** and **Untestable**. For each scenario, write down three trajectories in your head:

1. the reference trajectory;
2. a valid variation the scenario does not mention: different read-only lookups, different phrasing, one extra reasonable question;
3. a plausible wrong run: a write before the authorizing turn, a guessed value, a retry after an unknown result.

The scenario must pass the first two and fail the third, and every line must decide its part without judgment. Then turn each Initial state, Required event, Final state and Forbidden line into a Given or Then step; a line that needs rewording or splitting is a finding. Check that each rubric dimension measures something state and tool calls cannot show.

## Finder: coverage

Hunt for **Gaps**. Build these maps and report every empty cell:

- each stakeholder interest to the rules that protect it;
- each tool failure mode in the inputs, and each failure in the brainstorm list of the use-case checklist that the agent can detect, to a failure row;
- each "act only when" rule to one acting scenario and one holding-back scenario;
- each failure row that changes the outcome to a scenario whose Initial state triggers it;
- each required User-knows pair to the step of the reference trajectory that uses it;
- each rule clause that requires the agent to tell the user something to a scenario that asserts it by a rubric dimension;
- each known failure case or transcript in the inputs to a scenario.

## Verifier brief

> You are checking findings that other reviewers reported on an Agent Spec. You did not write the spec or the findings. Do not edit any file.
>
> Read the review packet at [packet path], the sources it lists, and the spec at [spec path]. Then, for each finding below, read the quoted line and the evidence yourself and give one verdict:
>
> - **Real**: the defect exists as described and belongs to its class.
> - **Not real**: the spec or the inputs refute it. Quote what refutes it.
> - **Style only**: it concerns wording or preference and changes no verdict and no agent behavior.
>
> Also confirm or change the severity, Important or Nit, using these definitions: [paste the two definitions from "Finding format"]. Give one line of evidence per verdict. Answer every finding.
>
> Findings: [paste the findings, each with its class, severity, location, quote, evidence and pattern, without the finder's other commentary]
