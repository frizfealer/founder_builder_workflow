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
| `verified_by` | list of `script`, `metrics`, `reviewer`, `you`. Never the agent that built the task | Owner; manager may draft |
| `may_edit` | protected paths this task may change; a trailing `/` names a folder. Empty for most | Owner; manager may draft |
| `runs_as` | `build`, `iterate`, `measurement`, `you` | Owner; manager may draft |
| `priority` | `high`, `medium`, `low` | Owner |
| `depends_on` | list of `{"id": <int>, "soft": <bool>}`; hard unless `soft` is true | Owner; manager may draft |
| `tokens` | `null`, or `{"agents": <int>, "main_session": "not recorded"}` | Manager |
| `draft_note` | text, optional | Whoever drafted the fields |
| `needs_you` | optional; `{"question", "recommendation", "if_vetoed"}`, required when status is Needs you | Manager |
| `decided_for_you` | optional; list of `{"chosen", "rejected", "would_change"}` | Manager |

A Ready task must have `done_means`, `verified_by`, `runs_as` and `priority`. A draft counts
only when the owner sets the task to Ready; after that the manager changes none of the owner's
fields.

`tokens.agents` is the sum of what Claude Code reports for each agent run on the task
(`subagent_tokens` in the Agent result). The main session's own use is not available yet
(task 30); write `"not recorded"` until it is.
