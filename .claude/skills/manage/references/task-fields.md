# Task fields

One JSON object per file, `tasks/<id>.json`, id zero-padded to 3 (`tasks/020.json`).
`scripts/tasks.py lint` checks every rule below that a script can check.

| Field | Values | Who sets it |
| --- | --- | --- |
| `id` | positive integer, equal to the file name | Owner; the manager for a Proposed task (one more than the highest id) |
| `title`, `item`, `motivation`, `notes`, `source_chat` | text | Owner |
| `added` | `YYYY-MM-DD` | Owner, or the manager for a Proposed task |
| `finished` | `YYYY-MM-DD` when Done or Dropped, else `""` | Manager |
| `status` | Proposed, Backlog, Ready, In progress, Needs you, Done, Dropped | Owner sets Ready. Manager sets In progress, Needs you, Done, and creates Proposed |
| `done_means` | the observable end state | Owner; manager may draft |
| `verified_by` | list of `script`, `metrics`, `reviewer`, `advisor`, `you`. Never the agent that built the task. Each verifies every line of `done_means` that `verifier_of_line` leaves out. `tasks.py lint` rejects `advisor` and `you` together while a line is left out, since that line would be both theirs and the advisor never rules on the owner's line | Owner; manager may draft |
| `verifier_of_line` | optional; object from the number of a `done_means` line, written `(n)` where the line starts, to one verifier from the list above: `{"3": "advisor"}`. That line is verified by that verifier alone; a line not in the object by every verifier in `verified_by`. `tasks.py lint` rejects a key not written `(n)` in `done_means` and a value that is not a verifier | Owner; manager may draft |
| `may_edit` | protected paths this task may change; a trailing `/` names a folder. Empty for most | Owner; manager may draft |
| `may_delete` | optional; list of paths this task may delete or rename, matched like `may_edit`. `checks.py protected` fails a branch that deletes or renames a file the working branch held when the branch left it and this does not name; a file the branch added itself needs no entry. `tasks.py lint` rejects anything but a list of paths | Owner; manager may draft |
| `runs_as` | `build`, `iterate`, `measurement`, `you` | Owner; manager may draft |
| `priority` | `high`, `medium`, `low` | Owner |
| `tags` | list of 1 to 3 tags, each a line of `tasks/tags.txt` | Owner; the manager or builder for a Proposed task |
| `depends_on` | list of `{"id": <int>, "soft": <bool>}`; hard unless `soft` is true | Owner; manager may draft |
| `tokens` | `null`, or `{"agents": <int>, "main_session": "not recorded"}` | Manager |
| `draft_note` | text, optional | Whoever drafted the fields |
| `summary` | optional; `{"outcome", "scope", "risk", "cost"}`, each non-empty text, what the owner reads to say Ready, change or drop. The standard of each part is below the table. `tasks.py lint` rejects a summary that lacks a part or holds an empty one, and a Proposed or Ready task with an id above 71 that has none; a task up to 71 passes with or without one | Whoever drafts the task: the owner, the manager or the builder for a Proposed task |
| `needs_you` | optional; `{"question", "recommendation", "if_vetoed"}`, required when status is Needs you | Manager |
| `decided_for_you` | optional; list of `{"chosen", "rejected", "why", "would_change"}`, each text; `why` is one sentence, the reason for the choice. The manager writes `why` in every new entry; an entry written before task 68 has none, so `tasks.py lint` accepts an entry without it and rejects a `why` that is not non-empty text | Manager |
| `outside_needs` | optional; list of distinct values from a fixed set, today only `claude-api`. `checks.py needs` runs one check per value before a builder starts; a failure parks the task | Owner; manager may draft |
| `outside_problems` | optional; for a Proposed task, a non-empty list of `{"file", "problem"}`: each file that existed before the branch that adds the task, and the problem in it the task is about. A task branch adds a Proposed task only with it (`checks.py protected`) | Whoever proposes the task, builder or manager |
| `for_retry` | optional; list of findings, each quoted, on files that exist only on the task's branch or on lines it added or changed (`checks.py unmerged`). Written when the task parks, on the working branch only; the retry builder's brief quotes it | Manager |
| `owner_verified` | optional; `YYYY-MM-DD` the owner checked his lines of `verified_by`, or `""`. May be set while the task is Ready or Needs you. While a line is verified by `you` and this is empty, `checks.py owner` parks the task | Owner, or on his instruction; never the manager, never inferred from other text |

A line of `done_means` is the text after `(n)`, where `(n)` starts a line: at the start of the
text or of a text line, or after the `.`, `:`, `;`, `!` or `?` that ends the line before. A
`(n)` inside a line is text, not a line number, and so is one after an abbreviation that never
ends a sentence (`e.g.`, `i.e.`, `cf.`, `vs.`, `viz.`). A `done_means` that numbers no line is one
line, line 1. `advisor` is the `manager-advisor` agent: for each of its lines the manager saves
its reply in `tasks/advice/<id>-<n>.md`, and `checks.py advice` refuses the merge until the
latest reply on each line starts `RULING: HOLDS`; a line `you` verifies too is the owner's and
needs no reply. A line for `you` waits for `owner_verified`.

`summary` has four parts, each one or two sentences (owner, 2026-11-20):

- **Outcome:** what is true when the task is done.
- **Scope:** what it changes and what it leaves alone, in words the owner already knows, with no
  file name or field name unless the same sentence explains it; a scope line that needs
  explaining is badly written.
- **Risk:** the worst outcome if it goes wrong, and what guards against it.
- **Cost:** builder runs, and the agent tokens of a named earlier task of similar size.

A Ready task must have `done_means`, `verified_by`, `runs_as` and `priority`. A draft counts
only when the owner sets the task to Ready; after that the manager changes none of the owner's
fields.

`tokens.agents` is the sum of what Claude Code reports for each agent run on the task
(`subagent_tokens` in the Agent result, or `total_tokens` in a background agent's notice). During
a run the manager counts each one on its task with `checks.py tokens`, and adds the run's count to
the field when the task merges or parks. The main session's own use is not available yet
(task 30); write `"not recorded"` until it is.
