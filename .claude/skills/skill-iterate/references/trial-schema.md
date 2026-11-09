# trial.json

One file per trial at `eval/<skill>/results/<label>/trial.json`, written by the trial runner at
the end of the run. `grade.py` reads only this file; the markdown beside it is for humans and
judges. Numbers come from the harness (task notifications, timestamps, the checker), never from
the agent's memory of them.

```json
{
  "schema": 1,
  "label": "full-new-3",
  "kind": "full",                       // a key of grading.json "kinds"
  "legacy": false,                      // true when built by legacy_extract.py
  "skill_commit": "e622e24",            // git rev of the skill under test
  "wall_clock_s": 1588,                 // first round start to last round end
  "rounds": [
    {"n": 1, "start": "2026-11-08T15:23:37Z", "end": "2026-11-08T15:35:15Z", "seconds": 698,
     "merged": 18, "kept": 14, "dropped": 4, "preexisting": 0, "unknown_kept": 0,
     "important_kept": 11, "header_count": {"merged": 18, "important": 15, "nit": 3}}
  ],
  "integrity": {"script_errors": 0, "checker_zero_errors_seen": true, "asked_user": false},
  "subagents": [
    {"round": 1, "role": "finder: faithfulness", "kind": "finder",   // finder | verifier | other
     "codex": false, "tool_uses": 8, "duration_ms": 128993, "tokens": 134288}
  ],
  "findings": [
    {"id": "R1-01", "round": 1, "class": "Lies", "severity": "Important",
     "location": "CO-A3 failure row ...", "quote": "...",
     "kept": true,                      // true kept, false dropped, null pre-existing/unknown
     "status": "fixed"}                 // fixed | answered | open | dropped | pre-existing
  ],
  "warnings": []                        // anything the writer could not determine
}
```

Rules for the writer:

- `kept` is the verifier/decision outcome, not the finder's opinion. Pre-existing findings are
  `kept: null`, `status: "pre-existing"`.
- `wall_clock_s` excludes waiting for a subagent after the last round ended.
- A subagent that never returned still gets a row, with `tool_uses` and `duration_ms` null.
- Round-2-only kinds start at round 2; `rounds` then has no `n: 1`.

Per-round snapshots of the artifact live beside it in `rounds/round<N>-<artifact>` (round0 = before round 1). Judge verdicts live in `judge/<metric>.verdict.json`; `grade.py` writes the task
file `judge/<metric>.task.md` when the verdict is missing.
