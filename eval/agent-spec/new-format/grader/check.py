#!/usr/bin/env python3
"""Frozen model checker for new-format agent specs (FORMAT.md). Standard library only.

Usage:
  check.py <spec-dir> [--json out.json] [--write]

Imports <spec-dir>/model.py, walks every reachable state breadth first, tests every rule on every
step and end state, and reports each break with its shortest path. Also: the self-test (the
model's deliberately broken rule must break), scenario replay (scenarios.md), chart steps no
scenario takes, and which breaks policy.md does not list.

--write regenerates policy.md and chart.mmd in <spec-dir> from the model. A trial's own files are
written by the skill's checker; the harness only compares against them.
"""
import importlib.util
import json
import re
import sys
from collections import deque
from pathlib import Path

import lint

MAX_STATES = 500_000
MAX_DEPTH = 120  # replay: longest path searched
MAX_PATHS = 20  # replay: stop counting after this many


class ModelError(Exception):
    pass


def load_model(spec_dir):
    path = Path(spec_dir) / "model.py"
    if not path.exists():
        raise ModelError("model.py not found")
    spec = importlib.util.spec_from_file_location(f"spec_model_{abs(hash(str(path.resolve())))}", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod  # dataclasses look the module up while the file runs
    try:
        spec.loader.exec_module(mod)
    except Exception as e:  # the model is trial output; any failure is a finding, not a crash
        raise ModelError(f"model.py failed to import: {type(e).__name__}: {e}")
    for name in ("INITIAL", "successors", "is_end", "chart", "RULES", "SELFTEST"):
        if not hasattr(mod, name):
            raise ModelError(f"model.py has no {name}")
    return mod


def explore(m):
    parent = {m.INITIAL: None}
    edges = {}
    queue = deque([m.INITIAL])
    while queue:
        s = queue.popleft()
        out = list(m.successors(s))
        edges[s] = out
        for st, t in out:
            if t not in parent:
                if len(parent) >= MAX_STATES:
                    raise ModelError(f"more than {MAX_STATES} reachable states")
                parent[t] = (s, st)
                queue.append(t)
    return parent, edges


def path_to(parent, s):
    steps = []
    while parent[s] is not None:
        prev, st = parent[s]
        steps.append(st)
        s = prev
    return steps[::-1]


def find_breaks(m, parent, edges, rules):
    """{(rule id, reason): shortest path as step labels}. BFS order makes the first hit a shortest path."""
    found = {}
    for s in parent:
        if m.is_end(s):
            for r in rules:
                why = r.get("end") and r["end"](s)
                if why and (r["id"], why) not in found:
                    found[(r["id"], why)] = [st.label for st in path_to(parent, s)]
        elif not edges[s]:
            key = ("no-step", "the agent has no step here")
            if key not in found:
                found[key] = [st.label for st in path_to(parent, s)]
        for st, t in edges[s]:
            for r in rules:
                why = r.get("step") and r["step"](s, st, t)
                if why and (r["id"], why) not in found:
                    found[(r["id"], why)] = [x.label for x in path_to(parent, s)] + [st.label]
    return found


# --------------------------------------------------------------------------- scenarios


def matches(line, label):
    return label == line or (label.startswith(line + " (") and label.endswith(")"))


def replay(m, world):
    """Every complete path whose setup, customer and system steps are exactly `world`, in order."""
    paths = []

    def walk(s, i, trail):
        if len(paths) >= MAX_PATHS or len(trail) > MAX_DEPTH:
            return
        if m.is_end(s):
            if i == len(world):
                paths.append(list(trail))
            return
        for st, t in m.successors(s):
            if st.actor == "agent":
                walk(t, i, trail + [(s, st, t)])
            elif i < len(world) and matches(world[i], st.label):
                walk(t, i + 1, trail + [(s, st, t)])

    walk(m.INITIAL, 0, [])
    return paths


def rules_broken_on(m, path, rule_ids):
    rules = [r for r in m.RULES if r["id"] in rule_ids]
    broken = set()
    for s, st, t in path:
        for r in rules:
            if r.get("step") and r["step"](s, st, t):
                broken.add(r["id"])
    if path:
        last = path[-1][2]
        for r in rules:
            if r.get("end") and r["end"](last):
                broken.add(r["id"])
    return sorted(broken)


def run_scenarios(m, spec_dir):
    rows = []
    for sc in lint.parse(spec_dir)["scenarios"]:
        row = {"id": sc["id"], "kind": sc["kind"], "rules": sc["rules"]}
        if sc["kind"] == "model path":
            paths = replay(m, sc["world"])
            row["paths"] = len(paths)
            row["result"] = "no path" if not paths else "one path" if len(paths) == 1 else "ambiguous"
            row["cited_rules_broken"] = sorted({r for p in paths for r in rules_broken_on(m, p, sc["rules"])})
            row["_paths"] = paths
        rows.append(row)
    return rows


# --------------------------------------------------------------------------- chart, coverage, policy page


def chart_arrows(m, edges):
    arrows = {}
    for s, out in edges.items():
        a = m.chart(s)
        for st, t in out:
            b = m.chart(t)
            if a != b:
                arrows.setdefault((a, b), [])
                if st.label not in arrows[(a, b)]:
                    arrows[(a, b)].append(st.label)
    return arrows


def uncovered(m, edges, scen_rows):
    """(chart state, step label) pairs some reachable step has and no scenario path takes."""
    taken = {(m.chart(s), st.label) for r in scen_rows for p in r.get("_paths", []) for s, st, t in p}
    every = {(m.chart(s), st.label) for s, out in edges.items() for st, t in out}
    return sorted(every - taken)


def mermaid(m, arrows):
    names = {}
    for a, b in arrows:
        for n in (a, b):
            names.setdefault(n, f"s{len(names)}")
    lines = ["stateDiagram-v2"]
    for n, k in names.items():
        lines.append(f'    state "{n}" as {k}')
    start = m.chart(m.INITIAL)
    lines.append(f"    [*] --> {names.get(start, 's0')}")
    for (a, b), labels in sorted(arrows.items(), key=lambda kv: (names[kv[0][0]], names[kv[0][1]])):
        label = labels[0] if len(labels) == 1 else f"{labels[0]} (+{len(labels) - 1} more)"
        lines.append(f"    {names[a]} --> {names[b]}: {label.replace(':', ' -').replace(';', ',')}")
    return "\n".join(lines) + "\n"


def policy_page(breaks):
    out = ["# Policy", "", "The chart is in [chart.mmd](chart.mmd). Each break below is a rule that fails "
           "in some reachable state, shown as its shortest path.", "", "## Breaks", ""]
    if not breaks:
        out.append("None.")
    for (rid, why), path in breaks.items():
        out += [f"### {rid}: {why}", ""] + [f"{i}. {lab}" for i, lab in enumerate(path, 1)] + [""]
    return "\n".join(out).rstrip() + "\n"


def listed_breaks(spec_dir):
    path = Path(spec_dir) / "policy.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    sec = re.split(r"^## Breaks\s*$", text, flags=re.M)
    if len(sec) < 2:
        return []
    body = re.split(r"^## ", sec[1], flags=re.M)[0]
    return [(m.group(1), m.group(2).strip()) for m in re.finditer(r"^### (\S+?):\s+(.+)$", body, re.M)]


# --------------------------------------------------------------------------- main


def check(spec_dir, write=False):
    spec_dir = Path(spec_dir)
    res = {"error": None}
    try:
        m = load_model(spec_dir)
        parent, edges = explore(m)
        breaks = find_breaks(m, parent, edges, list(m.RULES))
        selftest = find_breaks(m, parent, edges, [m.SELFTEST])
        scen = run_scenarios(m, spec_dir)
        arrows = chart_arrows(m, edges)
        unc = uncovered(m, edges, scen)
    except ModelError as e:
        res["error"] = str(e)
        res["selftest"] = "FAIL"
        return res
    except Exception as e:  # a rule or step function raised while the checker walked the model
        res["error"] = f"model raised while being checked: {type(e).__name__}: {e}"
        res["selftest"] = "FAIL"
        return res
    if write:
        (spec_dir / "policy.md").write_text(policy_page(breaks), encoding="utf-8")
        (spec_dir / "chart.mmd").write_text(mermaid(m, arrows), encoding="utf-8")
    listed = listed_breaks(spec_dir)
    found = list(breaks)
    model_rows = [r for r in scen if r["kind"] == "model path"]
    res.update({
        "states": len(parent),
        "steps": sum(len(v) for v in edges.values()),
        "breaks": [{"rule": rid, "reason": why, "path": p} for (rid, why), p in breaks.items()],
        "selftest": "pass" if [k for k in selftest if k[0] == m.SELFTEST["id"]] else "FAIL",
        "listed_breaks": None if listed is None else len(listed),
        "unlisted_breaks": [{"rule": rid, "reason": why} for rid, why in found if (rid, why) not in set(listed or [])],
        "scenarios": [{k: v for k, v in r.items() if k != "_paths"} for r in scen],
        "one_path_share": round(sum(r["result"] == "one path" for r in model_rows) / len(model_rows), 2) if model_rows else None,
        "chart_states": len({n for ab in arrows for n in ab}),
        "chart_arrows": len(arrows),
        "uncovered_steps": [{"chart_state": a, "step": b} for a, b in unc],
    })
    return res


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    res = check(args[0], write="--write" in args)
    if "--json" in args:
        Path(args[args.index("--json") + 1]).write_text(json.dumps(res, indent=1))
    if res["error"]:
        print("ERROR:", res["error"])
        sys.exit(1)
    print(f"States: {res['states']}  steps: {res['steps']}  self-test: {res['selftest']}")
    print(f"Breaks: {len(res['breaks'])}")
    for b in res["breaks"]:
        print(f"  {b['rule']}: {b['reason']}  ({len(b['path'])} steps)")
    print(f"Listed on policy.md: {res['listed_breaks']}; not listed: {len(res['unlisted_breaks'])}")
    for b in res["unlisted_breaks"]:
        print(f"  {b['rule']}: {b['reason']}")
    rows = [r for r in res["scenarios"] if r["kind"] == "model path"]
    print(f"Scenarios: {len(res['scenarios'])} ({len(rows)} model path); one-path share {res['one_path_share']}")
    for r in rows:
        if r["result"] != "one path" or r["cited_rules_broken"]:
            extra = f"; cited rule breaks on its path: {', '.join(r['cited_rules_broken'])}" if r["cited_rules_broken"] else ""
            print(f"  {r['id']}: {r['result']} ({r['paths']} paths){extra}")
    print(f"Chart: {res['chart_states']} states, {res['chart_arrows']} arrows")
    print(f"Steps no scenario takes: {len(res['uncovered_steps'])}")
    for u in res["uncovered_steps"]:
        print(f"  [{u['chart_state']}] {u['step']}")


if __name__ == "__main__":
    main()
