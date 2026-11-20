# The variant brief

Step 9 sends this brief to one fresh-context subagent. A checker written by the same hand that writes the variants shares its blind spots, so the variant builder starts with no context and never opens the checkers. Fill the bracketed slots and paste the brief whole.

> You write broken variants of a scripted agent, to test whether a test suite catches each broken
> rule. Work in the test folder [test folder path]. You did not write its rule checkers, and you do
> not open them.
>
> **Read only these**, before you write any variant: the spec's `rules.md` and `scenarios.md` at
> [spec folder path]; the test folder's `data.json`, `harness/agents.py` (the reference agent),
> `harness/slot.py`, `harness/data.py` and `variant_results.py`. Do not open `harness/checkers.py`,
> `unchecked_sentences.json`, the checkers' tests ([checker test files]), or any review of them.
> Your report lists every file you read before you first ran a variant.
>
> **Each variant** is a subclass of `ReferenceAgent` in `harness/agents.py` with exactly one fault,
> in a tool call or in a message. It sets four class attributes: `name` (`"break-<rule id>-call"` or
> `"break-<rule id>-message"`), `rule` (the rule id), `fault` (`"call"` or `"message"`) and `breaks`
> (the words of the rule it breaks, quoted word for word). Its docstring names the rule, quotes those
> words, says whether the fault is a call or a message, and says what the variant does instead. It
> imports nothing from `harness/checkers.py` or a test file. List every variant in the tuple
> `variant_results.py` reads ([tuple name]); `AGENTS` makes each one selectable with `--agent`.
>
> **Coverage**: one variant for each rule a feature file cites; for each rule whose text asks for
> both a tool call and a message, one call variant and one message variant. Write message faults
> as well as call faults: say the thing is done when it is not, leave out a part the rule names,
> skip a question the rule asks.
>
> **Sentences**: a variant that says a sentence the reference agent never says gets a `data.json`
> `agent` entry of its own, labelled `"free choice"`, with a note naming the variant and a `judge`
> answer for every judge question, your reading of the sentence. A variant says only sentences of
> `data.json`.
>
> **Reach**: each variant's events differ from the reference agent's in at least one runnable
> scenario. When a fault sits where no scenario goes, move it to a place a scenario reaches that
> breaks the same words, and say so in its docstring; when no such place exists, report the rule's
> words as reached by no scenario.
>
> **Then** run `uv run python variant_results.py` and `uv run pytest`. Fix nothing a variant
> reveals, and keep every variant as you wrote it, whatever its outcome. Report each variant with
> its outcome from `variant_results.json`, and the files you read.

## The outcomes

`variant_results.py` gives each variant one outcome from its verdicts over every runnable scenario:

| Outcome | Meaning | What follows (step 9) |
|---|---|---|
| caught | its own rule breaks in at least one scenario | nothing |
| caught only by another rule | its own rule never breaks, another rule does | its rule's checker misses the words it broke, or no scenario reaches them |
| survived | every scenario's test passes | the same, and nothing else noticed the fault |

A variant with no break anywhere whose tests still end without a verdict stops the script: it fits none of the three, and the case needs a person.

For a variant not caught, the results file quotes the words of its rule that went unchecked and says whether `unchecked_sentences.json` already lists them. A variant with a known reason for its outcome gets a note in the script's `NOTES` (the café's `break-R-04-message`).
