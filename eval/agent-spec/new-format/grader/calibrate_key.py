#!/usr/bin/env python3
"""Calibrate the key_recall judge's reading of a defect against the owner (HARNESS-PLAN.md step 6).

Usage:
  calibrate_key.py tasks   writes one judge task per finding of calibration/2026-11-11/worksheet.md
                           into calibration/2026-11-14-key-judge/
  calibrate_key.py score   compares the judges' verdicts with the owner's rulings in
                           calibration/2026-11-11/answers.md and prints the agreement

The judge applies new-format/judge-brief-key.md, the brief the key_recall task names. Agreement
is on the metric's bucket, Real against Not real or Style only, as in calibrate.py. Passes at
18 of 20. Owner ruling 4 (2026-11-14) reads three rulings by their reason: F2 is Real, F7 and F12
are Style only.
"""
import json
import re
import sys
from pathlib import Path

EVAL = Path(__file__).resolve().parents[2]
SOURCE = EVAL / "calibration" / "2026-11-11"
OUT = EVAL / "calibration" / "2026-11-14-key-judge"
BRIEF = "new-format/judge-brief-key.md"
sys.path.insert(0, str(EVAL.parents[1] / ".claude" / "skills" / "skill-iterate" / "scripts"))
from grade import blind_finding_text  # noqa: E402  the extractor the dropped_real judge uses

RULING_4 = {"F2": "Real", "F7": "Style only", "F12": "Style only"}
PASS = 18
LABELS = {"real": "Real", "not real": "Not real", "style only": "Style only"}


def findings():
    """The worksheet's finding sections, by item id. Six it2-2 findings have an empty body in the
    worksheet, written by an older extractor; their body is taken from the trial's findings file."""
    text = (SOURCE / "worksheet.md").read_text(encoding="utf-8")
    text = text.split("\n## Recall matches", 1)[0]
    parts = re.split(r"^## (F\d+) — ", text, flags=re.M)
    out = {}
    for i in range(1, len(parts), 2):
        section = "## " + parts[i] + " — " + parts[i + 1].strip()
        m = re.match(r"## F\d+ — (\S+) (\S+) \(round (\d)", section)
        empty = "```\n## " + m.group(2) + "\n\n```\n```"
        if empty in section:
            body = blind_finding_text(EVAL / "results" / m.group(1), m.group(2), int(m.group(3)))
            section = section.replace(empty, "```\n" + body + "\n```")
        out[parts[i]] = section
    return out


def tasks():
    OUT.mkdir(exist_ok=True)
    for fid, section in findings().items():
        body = [f"# Calibration task: {fid}", "",
                "Run from the repo root: all paths below are relative to `eval/agent-spec/`.", "",
                "A reviewer reported the defect below against an old-format Agent Spec. You did not write the spec or the finding. Read only; edit nothing except your verdict file.", "",
                f"Apply the section \"What a defect is\" of `{BRIEF}` and rule the finding Real, Not real or Style only. You may open only: that brief, the spec snapshot the section below names, `review-packet.md` and the inputs it lists. Do not open anything under `calibration/` or any `judge/` folder.", "",
                f"Write exactly one JSON object, nothing else, to `calibration/{OUT.name}/{fid}.verdict.json`:",
                "```json", '{"item": "' + fid + '", "verdict": "Real|Not real|Style only", "why": "<one line>"}', "```", "",
                section, ""]
        (OUT / f"{fid}.task.md").write_text("\n".join(body), encoding="utf-8")
    print(f"wrote {len(findings())} tasks to {OUT}")


def owner_rulings():
    out = {}
    for line in (SOURCE / "answers.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(F\d+)\s*\|\s*(not real|style only|real)\b", line, re.I)
        if m:
            out[m.group(1)] = LABELS[m.group(2).lower()]
    out.update(RULING_4)
    return out


def score():
    owner = owner_rulings()
    rows, agree = [], 0
    for fid in sorted(owner, key=lambda k: int(k[1:])):
        vf = OUT / f"{fid}.verdict.json"
        judge = LABELS.get(json.loads(vf.read_text()).get("verdict", "").strip().lower()) if vf.exists() else None
        ok = judge is not None and (judge == "Real") == (owner[fid] == "Real")
        agree += ok
        rows.append(f"| {fid} | {judge or 'missing'} | {owner[fid]} | {'yes' if ok else 'no'} |")
    print("| item | judge | owner | same bucket |\n|---|---|---|---|\n" + "\n".join(rows))
    print(f"\n{agree} of {len(owner)} agree; {'pass' if agree >= PASS else 'FAIL'} (needs {PASS}).")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "tasks":
        tasks()
    elif cmd == "score":
        score()
    else:
        print(__doc__)
        sys.exit(2)
