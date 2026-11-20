# The data file

`data.json` is the one home of every value a test uses that the spec does not give. It doubles as the list of everything the test builder invented, so a person can read what was chosen and why. The café's `data.json` is the worked example; `harness/datacheck.py` is its check.

## Where a value comes from

| Home | What lives there |
|---|---|
| The spec, unchanged | Everything a rule depends on: limits, what a proposal contains, what each tool can answer. |
| The data file | Everything else: dates, times, names, sizes, ids, every full sentence, tool and argument names, the fake's open choices. |

- A limit from a claim is played at its boundary: the café's claim C-07 ("The largest party the agent may book is 8 people") gives 8 for "8 or fewer" and 9 for "more than 8".
- Every value a run contains comes from the data file. A test walks the events of every run, and every history, and finds each value among the data file's values.
- Checkers compare which tool was called and with which values, read through the data file. A tool's name and argument names are free choices; when the architecture notes fix the real ones, only the data file and the fake change.

## Labels

Every entry carries `source`, either `"from the spec"` or `"free choice"`, and a `note` saying which part is still a free choice. A `"from the spec"` entry also has:

| Field | Holds | The check |
|---|---|---|
| `ref` | the claim and rule ids it rests on | each id exists in the spec |
| `quote` | words of the spec it takes | each appears in the text of one cited id |
| `wording` | `"builder's own"` when its value holds words the cited text does not | without it, every word of the value is in the cited text, and a number value appears there |
| `label` | the scenario label its value plays, such as `"8 or fewer"` | the label is in a World line, and the value fits it |

The cited text of a claim is its row in the claims table plus the Systems row of its system. The cited text of a rule is its section of `rules.md` plus each row of "What the agent does" that names it.

A free choice that turns out to be a fact about an outside system, or a decision only the owner can make, is a finding (the café's `fake.book_without_an_active_hold` notes "finding candidate for agent-spec").

## Sections

| Section | One entry per | Fields beside the labels |
|---|---|---|
| `spec` | the spec folder | `value`: its path, relative to the test folder |
| `values` | value a sentence or call uses | `value`; templates name these keys as `{key}` |
| `tools` | tool of the Systems table | `name`, `description`, `input_schema`, `args` (argument name to `values` key), `model_step` (`model.py`'s step label) |
| `answers` | answer a claim gives a tool | `value`: the payload the agent sees |
| `fake` | choice the claims leave open | `value`: what the fake does |
| `visitor` | visitor World line | `world_step` (the World line, exact), `value` (the sentence), `means` (what checkers read, such as `"yes"`), `change` for a line that changes the proposal |
| `agent` | sentence an agent says | `model_step`, `value`, `judge`: the recorded answer to every judge question, the builder's reading of its own sentence |
| `judge_instruction`, `judge_questions` | the judge's instruction, and each yes/no question a checker asks | `value` |
| `action_limit` | the whole file | `value`: the agent actions a run from the start may take before it stops with no verdict |

Ids the fake issues (the café's `hold_ids` and `confirmation_ids`) number at least `action_limit`, since each action makes at most one call. A sentence is a Python format string over the keys of `values` and the ids the fake issues. `means`, `change` and `judge` are readings for the checkers; a transcript leaves them out.

## What the check reports

`harness/datacheck.py` `problems()` returns one line per problem, and `generate_features.py --check` prints them:
- an entry labelled neither way, or a `"from the spec"` entry failing a check of the labels table;
- a World line of a runnable scenario that no entry plays, and a visitor entry whose World line no scenario has;
- a World line that names a number no entry is labelled for;
- a tested moment whose history is not the reference agent's run of its scenario up to that turn, when the folder has moments.
