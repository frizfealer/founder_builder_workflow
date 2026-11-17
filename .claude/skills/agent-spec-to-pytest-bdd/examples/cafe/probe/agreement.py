"""Lines 4 and 5 of task 49: the rule checkers' verdicts against the labels Claude in chat gave the transcripts.

Usage:
  uv run python probe/agreement.py --template            print a blank labels file from runs/part2/transcripts/
  uv run python probe/agreement.py <labels.json>         print line 4's agreement, every disagreement, and line 5

The labels file holds one "pass" or "fail" per one-action run and rule, for the rules each transcript
lists under rules_to_label; keys starting with "_" are ignored (room for notes):
  {"run-01": {"R-01": "pass", "R-03": "fail", "R-05": "pass", "R-09": "pass"}, ...}

A checker verdict "holds" agrees with "pass", "breaks" with "fail"; "undecided" agrees with neither and
is listed as a disagreement. Line 4 holds when at least 9 of every 10 labelled rule verdicts agree and
no label is missing. Line 5 holds for a bad prompt when at least 1 of its runs shows the bad behaviour
(its tested action is a booking call, and the label fails the prompt's rule) and its checker breaks
that rule.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from harness.data import tool  # noqa: E402
from probe.run_part2 import BAD_AT, OUT  # noqa: E402

AGREES = {"holds": "pass", "breaks": "fail"}


def one_action_runs(out):
    """{run id: (transcript, verdict record)} for the 27 one-action runs."""
    runs = {}
    for p in sorted((out / "transcripts").glob("run-*.json")):
        runs[p.stem] = (json.loads(p.read_text()), json.loads((out / "verdicts" / p.name).read_text()))
    return runs


def template(out):
    runs = one_action_runs(out)
    return {rid: {r: None for r in t["rules_to_label"]} for rid, (t, _) in runs.items()}


def books(transcript):
    """Whether the agent's tested action holds a booking call."""
    return any(e["kind"] == "call" and e["tool"] == tool("book")["name"] and e["under_test"]
               for e in transcript["events"])


def report(labels, out):
    runs = one_action_runs(out)
    labels = {k: v for k, v in labels.items() if not k.startswith("_")}
    rows, missing = [], []
    for rid, (t, v) in runs.items():
        for rule in t["rules_to_label"]:
            label = labels.get(rid, {}).get(rule)
            if label not in ("pass", "fail"):
                missing.append(f"{rid} {rule}: {label!r}")
                continue
            got = v["rules"][rule]
            rows.append({"run": rid, "rule": rule, "label": label, "checker": got["verdict"], "reason": got["reason"],
                         "moment": v["moment"], "prompt": v["prompt"], "agree": AGREES.get(got["verdict"]) == label})
    extra = sorted(set(labels) - set(runs))
    agree = sum(r["agree"] for r in rows)
    n = len(rows)
    line4 = n > 0 and not missing and not extra and agree * 10 >= 9 * n
    lines = [f"one-action runs with a transcript: {len(runs)} of 27",
             f"LINE 4: the checkers agree with the labels on {agree} of {n} rule verdicts"
             f" ({agree / n:.1%})" if n else "LINE 4: no labelled rule verdicts",
             f"  needed: at least 9 of every 10, every label present -> {'HOLDS' if line4 else 'DOES NOT HOLD'}"]
    lines += [f"  missing label: {m}" for m in missing]
    lines += [f"  label for a run with no transcript: {x}" for x in extra]
    dis = [r for r in rows if not r["agree"]]
    lines.append(f"DISAGREEMENTS: {len(dis)}")
    lines += [f"  {r['run']} {r['rule']} ({r['moment']}, prompt {r['prompt']}): label {r['label']}, checker "
              f"{r['checker']} ({r['reason']})" for r in dis]
    line5 = True
    lines.append("LINE 5: each bad prompt has a run that shows the bad behaviour and is failed on its rule")
    for prompt, (moment, rule) in BAD_AT.items():
        hits = []
        lines.append(f"  prompt {prompt!r} at {moment}, rule {rule}:")
        for rid, (t, v) in runs.items():
            if v["prompt"] != prompt:
                continue
            label = labels.get(rid, {}).get(rule)
            shows = books(t) and label == "fail"
            failed = v["rules"][rule]["verdict"] == "breaks"
            if shows and failed:
                hits.append(rid)
            lines.append(f"    {rid}: books {books(t)}, label {label}, checker {v['rules'][rule]['verdict']}"
                         f" -> {'shows it and is failed' if shows and failed else 'no'}")
        line5 &= bool(hits)
        lines.append(f"    -> {'HOLDS' if hits else 'DOES NOT HOLD'} ({len(hits)} run(s): {', '.join(hits) or 'none'})")
    lines.append(f"LINE 5 -> {'HOLDS' if line5 else 'DOES NOT HOLD'}")
    return "\n".join(lines), line4 and line5


def main():
    args = sys.argv[1:]
    if args == ["--template"]:
        print(json.dumps(template(OUT), indent=1))
        return
    if len(args) != 1:
        sys.exit(__doc__)
    text, ok = report(json.loads(Path(args[0]).read_text()), OUT)
    print(text)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
