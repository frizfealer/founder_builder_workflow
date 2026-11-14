#!/usr/bin/env python3
"""Code metrics for one new-format trial (HARNESS-PLAN.md section 3). Standard library only.

Usage:
  grade_spec.py --spec <spec-dir> --trial <results-folder> --sources a.md[,b.md] --units answer-units.json

Prints one JSON object of metric values. grade.py runs this for every trial of a kind whose
grading file names it as "spec_grader". A metric that cannot be computed is null.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check  # noqa: E402
import lint  # noqa: E402


def share(hit, total):
    """hit / total rounded; a guard with nothing to apply to holds."""
    return round(hit / total, 2) if total else 1.0


def guards(spec):
    rows = spec["claims"]
    limits = [r for r in rows if r.get("kind") == "limit"]
    money = [r for r in rows if r.get("kind") == "money"]
    named = {r["system"] for r in rows if r.get("kind") == "system" and not lint.blank(r.get("system", ""))}
    systems = {r["system"]: r for r in spec["systems"]}
    every = named | set(systems)
    ok = [s for s in every if s in systems and not lint.blank(systems[s].get("owner", ""))
          and not lint.blank(systems[s].get("docs", ""))]
    return {
        "guard_none_limits": share(sum(not lint.blank(r.get("what ends it", "")) for r in limits), len(limits)),
        "guard_money": share(sum(not lint.blank(r.get("if it differs from what the customer confirmed", ""))
                                 for r in money), len(money)),
        "guard_systems": share(len(ok), len(every)),
    }


def quote_valid(spec, sources):
    text = lint.norm("\n".join(Path(p).read_text(encoding="utf-8") for p in sources))
    rows = [r for r in spec["claims"] if r.get("source") == "owner's words"]
    return share(sum(lint.norm(r.get("quote", "")) in text and not lint.blank(r.get("quote", "")) for r in rows),
                 len(rows))


def interview(trial):
    path = Path(trial) / "interview-log.json"
    if not path.exists():
        return {"guard_recommend": None, "stand_in_defaults": None}
    qs = json.loads(path.read_text(encoding="utf-8")).get("questions", [])
    if not qs:
        return {"guard_recommend": None, "stand_in_defaults": None}
    return {
        "guard_recommend": round(sum(bool((q.get("recommended") or "").strip()) for q in qs) / len(qs), 2),
        "stand_in_defaults": round(sum(q.get("answered_by") == "stand-in default" for q in qs) / len(qs), 2),
    }


def grade(spec_dir, trial, sources, units_file):
    spec = lint.parse(spec_dir)
    out = {"lint_errors": len(lint.lint(spec))}
    res = check.check(spec_dir)
    out["checker_selftest"] = res["selftest"]
    out["unlisted_breaks"] = None if res["error"] else len(res["unlisted_breaks"])
    out["listed_breaks"] = None if res["error"] else res["listed_breaks"]
    out["one_path_share"] = None if res["error"] else res["one_path_share"]
    out["uncovered_steps"] = None if res["error"] else len(res["uncovered_steps"])
    out["quote_valid"] = quote_valid(spec, sources)
    out["unsourced_claims"] = sum(r.get("source") in ("nobody", "spec only") for r in spec["claims"])
    units = lint.load_units(units_file)
    out["answer_reach"] = round(len(lint.reached_units(spec, units)) / len(units), 2)
    out.update(guards(spec))
    out.update(interview(trial))
    texts = [spec["text"][n] or "" for n in lint.OWNER_FILES]
    out["owner_lines"] = sum(1 for t in texts for line in t.splitlines() if line.strip())
    mmd = spec["dir"] / "chart.mmd"
    out["chart_arrows"] = sum(1 for l in mmd.read_text(encoding="utf-8").splitlines()
                              if "-->" in l and not re.match(r"\s*\[\*\]", l)) if mmd.exists() else None
    if res["error"]:
        out["_checker_error"] = res["error"]
    return out


def main():
    args = sys.argv[1:]
    get = lambda k: args[args.index(k) + 1] if k in args else None
    if not get("--spec"):
        print(__doc__)
        sys.exit(2)
    sources = (get("--sources") or "").split(",")
    print(json.dumps(grade(get("--spec"), get("--trial") or ".", [s for s in sources if s], get("--units"))))


if __name__ == "__main__":
    main()
