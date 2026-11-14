#!/usr/bin/env python3
"""Model checker for an agent spec folder (the templates in assets/). Standard library only.

Usage:
  check.py <spec-dir> [--write] [--derive] [--json out.json]

Runs lint.py first, then imports <spec-dir>/model.py, walks every reachable state breadth first,
tests every rule on every step and end state, and reports each break with its shortest path. Also:
the self-test (the model's deliberately broken rule must break), scenario replay (scenarios.md),
chart steps no scenario takes, and which breaks policy.md does not list.

The first output line is "<n> errors": lint errors, a model that fails to load or raises, a failed
self-test, a break policy.md does not list, and a model-path scenario that replays to no path.
A break itself is not an error; it is an owner decision, listed on policy.md.

--write regenerates policy.md and chart.mmd from the model. --derive prints, after the report,
one scenario per step no scenario takes yet, each a shortest complete path through that step,
with an empty Rules line to fill in.

Optional names in model.py: PHASES = {"<phase>": ["<chart state>", ...]} groups chart states and
colors them; a step's `action` (a short name, such as "customer asks to cancel") makes steps with
the same action between the same two chart states share one arrow.
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
    """{(from, to, action or None): [step labels]}. Steps with no action share an arrow per pair of chart states."""
    arrows = {}
    for s, out in edges.items():
        a = m.chart(s)
        for st, t in out:
            b = m.chart(t)
            if a != b:
                labels = arrows.setdefault((a, b, getattr(st, "action", "") or None), [])
                if st.label not in labels:
                    labels.append(st.label)
    return arrows


def uncovered(m, edges, scen_rows):
    """(chart state, step label) pairs some reachable step has and no scenario path takes."""
    taken = {(m.chart(s), st.label) for r in scen_rows for p in r.get("_paths", []) for s, st, t in p}
    every = {(m.chart(s), st.label) for s, out in edges.items() for st, t in out}
    return sorted(every - taken)


COLORS = ["#dbeafe", "#fde68a", "#bbf7d0", "#fbcfe8", "#e9d5ff", "#fed7aa"]


def arrow_order(m, arrows):
    """Arrows in drawing order, numbered A1, A2, ... in this order on the chart and on the policy page."""
    names = state_ids(m, arrows)
    return sorted(arrows, key=lambda k: (names[k[0]], names[k[1]], k[2] or ""))


def state_ids(m, arrows):
    names = {m.chart(m.INITIAL): "s0"}
    for a, b, _ in arrows:
        for n in (a, b):
            names.setdefault(n, f"s{len(names)}")
    return names


def arrow_name(key, labels):
    if key[2]:
        return key[2]
    return labels[0] if len(labels) == 1 else f"{labels[0]} (+{len(labels) - 1} more)"


def mermaid(m, arrows):
    names = state_ids(m, arrows)
    phases = getattr(m, "PHASES", {})
    lines = ["stateDiagram-v2"]
    for i, (phase, members) in enumerate(phases.items()):
        lines.append(f"    classDef p{i} fill:{COLORS[i % len(COLORS)]}")
    in_phase = {n for members in phases.values() for n in members}
    for n, k in names.items():
        if n not in in_phase:
            lines.append(f'    state "{n}" as {k}')
    for i, (phase, members) in enumerate(phases.items()):
        lines.append(f'    state "{phase}" as g{i} {{')
        lines += [f"        {names[n]}: {n}" for n in members if n in names]
        lines.append("    }")
        drawn = [names[n] for n in members if n in names]
        if drawn:
            lines.append(f"    class {','.join(drawn)} p{i}")
    lines.append(f"    [*] --> {names[m.chart(m.INITIAL)]}")
    for i, key in enumerate(arrow_order(m, arrows), 1):
        label = f"A{i}: {arrow_name(key, arrows[key])}"
        lines.append(f"    {names[key[0]]} --> {names[key[1]]}: {label.replace(':', ' -').replace(';', ',')}")
    return "\n".join(lines) + "\n"


def policy_page(m, arrows, breaks):
    out = ["# Policy", "", "The chart is in [chart.mmd](chart.mmd). Below it, every step each arrow stands for. Each "
           "break below is a rule that fails in some reachable state, shown as its shortest path.", "",
           "## Chart steps", "", "| arrow | from | to | step |", "|---|---|---|---|"]
    for i, key in enumerate(arrow_order(m, arrows), 1):
        for j, label in enumerate(arrows[key]):
            first = j == 0
            out.append(f"| {f'A{i}' if first else ''} | {key[0] if first else ''} | {key[1] if first else ''} | "
                       f"{label.replace('|', '/')} |")
    out += ["", "## Breaks", ""]
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
        res.update(error=str(e), selftest="FAIL")
        res["errors"] = lint.lint(lint.parse(spec_dir)) + [f"model.py: {e}"]
        return res
    except Exception as e:  # a rule or step function raised while the checker walked the model
        res.update(error=f"model raised while being checked: {type(e).__name__}: {e}", selftest="FAIL")
        res["errors"] = lint.lint(lint.parse(spec_dir)) + [f"model.py: {res['error']}"]
        return res
    if write:
        (spec_dir / "policy.md").write_text(policy_page(m, arrows, breaks), encoding="utf-8")
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
        "chart_states": len({n for a, b, _ in arrows for n in (a, b)}),
        "chart_arrows": len(arrows),
        "uncovered_steps": [{"chart_state": a, "step": b} for a, b in unc],
    })
    res["errors"] = lint.lint(lint.parse(spec_dir)) + check_errors(res)
    return res


def check_errors(res):
    e = [] if res["selftest"] == "pass" else ["model.py: the SELFTEST rule never breaks, so the checker is not testing rules"]
    e += [f"policy.md: break {b['rule']}: {b['reason']} is not listed; rerun with --write" for b in res["unlisted_breaks"]]
    e += [f"scenarios.md: {r['id']} replays to no path of the model" for r in res["scenarios"]
          if r["kind"] == "model path" and r["result"] == "no path"]
    return e


def steps_on_path(parent, s):
    """[(state, step, next state)] from INITIAL to s, along the shortest path."""
    out = []
    while parent[s] is not None:
        prev, st = parent[s]
        out.append((prev, st, s))
        s = prev
    return out[::-1]


def derive(spec_dir):
    """Scenario stubs, one per step no scenario takes yet, each a shortest complete path through that step."""
    m = load_model(spec_dir)
    parent, edges = explore(m)
    scen = run_scenarios(m, spec_dir)
    todo = set(uncovered(m, edges, scen))
    toward_end = {}  # state -> (step, next state) on a shortest path to an end state
    back = {}
    for s, out in edges.items():
        for st, t in out:
            back.setdefault(t, []).append((s, st))
    queue = deque(s for s in parent if m.is_end(s))
    seen = set(queue)
    while queue:
        t = queue.popleft()
        for s, st in back.get(t, []):
            if s not in seen:
                seen.add(s)
                toward_end[s] = (st, t)
                queue.append(s)
    n = max((int(x.group(1)) for r in scen if (x := re.match(r"SC-(\d+)", r["id"]))), default=0)
    blocks = []
    for s in parent:  # breadth-first order, so the first state found is on a shortest path
        for st, t in edges[s]:
            key = (m.chart(s), st.label)
            if key not in todo or t not in seen:
                continue
            path = steps_on_path(parent, s) + [(s, st, t)]
            while not m.is_end(path[-1][2]):
                nxt, u = toward_end[path[-1][2]]
                path.append((path[-1][2], nxt, u))
            todo -= {(m.chart(a), x.label) for a, x, _ in path}
            n += 1
            world = [x.label for _, x, _ in path if x.actor != "agent"]
            blocks.append(f"## SC-{n:02d} {key[0]}: {key[1]}\nKind: model path\nRules:\nWorld:\n"
                          + "".join(f"{i}. {w}\n" for i, w in enumerate(world, 1)))
    return "\n".join(blocks)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    res = check(args[0], write="--write" in args)
    if "--json" in args:
        Path(args[args.index("--json") + 1]).write_text(json.dumps(res, indent=1))
    print(f"{len(res['errors'])} errors")
    for e in res["errors"]:
        print("  " + e)
    if res["error"]:
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
    if "--derive" in args and res["uncovered_steps"]:
        print("\nDerived scenarios (append to scenarios.md, then fill in each Rules line):\n")
        print(derive(args[0]))
    sys.exit(1 if res["errors"] else 0)


if __name__ == "__main__":
    main()
