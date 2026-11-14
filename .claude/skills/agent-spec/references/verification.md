# Verification briefs

Steps 4.3 and 4.4 of the skill send these briefs to reviewers who start with no context. Each brief is self-contained: paste the shared header, then the role section, then fill the bracketed slots.

The lint and the model checker have already run when a reviewer starts. They settle everything a program can: fields, ids and links, whether the rules agree with each other in every reachable state, and whether each scenario is a path of the model. A reviewer reads for what no program can see: whether the spec says what the owner said.

## What a defective spec looks like

Every finding belongs to exactly one of three classes.

- **Lies.** The spec states something the owner's answers or the inputs contradict or do not support. A rule narrows or widens what the owner said ("promises nothing about when" written as "names no date"); a rule's wording for what the agent tells the customer departs from the owner's wording; a claim says more than its quote; a row of "What the agent does" departs from the rule it cites; a decision is logged as the owner's when the owner never made it.
- **Gap.** Something the owner said, or a case the agent will meet, has no rule. A recorded answer that no rule and no claim carries; a case an agent will meet that no row of "What the agent does" covers, such as two requests in one message or a second order named mid-conversation; a repeated thing with no end; an amount passed on from a tool with nothing said about a mismatch.
- **Unclear.** The owner could misread a line. A term the spec coins with no one-line definition where it first appears, or used outside its everyday sense; a rule id standing in for a sentence the owner would need to read.

Preferences about phrasing ("I would word this rule differently", "one more scenario would be nice") are not findings. A term the owner would misread is.

## Finding format

```
F<n> | <Lies | Gap | Unclear> | <Important | Nit> | <file and id: rules.md R-04, claims.md C-12>
Quote: "<the exact line from the spec, or 'absent' for a Gap>"
Evidence: <the input passage or interview answer that shows the defect, with file and location>
Pattern: <the general form of the defect, so every instance can be fixed>
```

*Important* means the defect would make an agent built from the spec behave differently from what the owner asked. *Nit* means the defect is real but changes no behavior.

The report starts with a count line, such as "3 findings: 2 Important, 1 Nit." or "0 findings."

## Shared header (every finder)

> You are reviewing an agent spec, the behavior contract for an LLM agent, written from an owner's interview. You did not write it. Find defects; do not edit any file.
>
> Read, in this order: the review packet at [packet path], which holds the interview answers verbatim and lists the inputs the spec was written from; every source file the packet lists; then the spec folder at [spec path]: `claims.md`, then `rules.md`, then `policy.md`.
>
> A lint and a model checker have already verified the fields, ids and links, that the rules agree with each other in every reachable state of the policy model, and that every scenario is a path of it. Skip those.
>
> Scope: [the whole spec | only these rules and claims: …].
>
> Report only defects in the three classes below, in the finding format below. Every finding quotes the spec and cites evidence; a suspicion without evidence is not a finding. When you find a pattern, report it once and list every instance in Evidence. If nothing is wrong, report "0 findings."
>
> [paste "What a defective spec looks like" and "Finding format"]

## Finder: faithfulness

Read every answer in the packet, then every rule, claim, row of "What the agent does" and decision against the answers. For each answer, find the rule or claim that carries it, and check it says the same thing, no more and no less, including the words the owner gave for what the agent tells the customer. For each rule, find the answer or claim it rests on. For each repeated thing (a retry, a lookup, a follow-up) find what ends it, and for each amount the agent passes on from a tool find what happens when it differs from what the customer confirmed. Then read the three pages as the owner would, and report each term the owner could misread.

## Adversarial verifier brief

> You are checking findings another reviewer made against an agent spec, the behavior contract for an
> LLM agent written from an owner's interview. Your job is to show that each finding is Not real or
> Style only. For each one, look for: a rule, claim, row of "What the agent does" or decision that
> already settles the case the finding raises; a quoted line that does not say what the finding
> claims; evidence that is not in the packet or the spec; or a defect that changes no agent behavior
> and that the owner would not misread (Style only). Say Real only when you cannot do any of these.
> The reference checklists under references/ are the spec's standards and count as evidence for a
> finding, the same as the packet and the spec.
>
> The first two routes, a line that settles the case and a quoted line that does not say what the
> finding claims, are limited as follows. The other two, missing evidence and Style only, are not.
> - A refutation must show the finding does not fit its class as defined in 'What a defective spec
>   looks like': for a Lies finding that says no input supports a line, showing that no input
>   contradicts the line is not a refutation; for a Gap finding, showing that some rule mentions the
>   case is not a refutation unless the rule says what the agent does in it.
> - A line that only permits a kind of behavior does not refute a finding that one case contradicts
>   the owner's answers. A claim that lets a system answer a call in some way lets the model use that
>   answer, but the answer must still be possible at that point, given what the steps before it
>   showed.
> - The line a finding quotes as defective does not refute the finding by restating what it says.
>   Refute it with an answer or another spec line that supports what this line says in this case,
>   not one that only permits lines of its kind.
> - A refutation by either of the first two routes must answer the case the finding names, and all
>   of it. A rule that settles the case for a different situation, or an answer that supports one
>   part of the line the finding quotes, settles a neighboring case and leaves the finding standing
>   for the rest. A line or answer that answers only part of a finding does not refute it: say Real,
>   and in your line for that finding quote what you cited and name the part it answers and the part
>   that stands.
>
> Read the spec folder at [spec path]; then the review packet at [packet path] and the sources it lists; then the findings at
> [findings path]; you report, you do not decide: the main thread decides each drop. Grep the spec for any id a finding names that you have not read.
>
> For each finding, one line: `<id> | Real / Not real / Style only | Important / Nit | <the line
> that refutes it, quoted, or why you could not refute it>`. Then the count line: how many of each
> verdict.
