"""Exhaustive check of model.py, plus the chart, the scenario map and the HTML page.

Run:  python3 check.py        (writes chart.mmd, scenario-map.md, index.html; prints the results)
"""
import html
import json
from collections import deque
from pathlib import Path

import model
from model import INITIAL, RULES, SUPPLEMENTARY, successors, is_end
import scenarios
import chart as chartmod

HERE = Path(__file__).parent


def explore(succ=successors, initial=INITIAL):
    parent = {initial: None}  # state -> (prev_state, step)
    edges = {}
    queue = deque([initial])
    while queue:
        s = queue.popleft()
        out = succ(s)
        edges[s] = out
        for st, t in out:
            if t not in parent:
                parent[t] = (s, st)
                queue.append(t)
    return parent, edges


def path_to(parent, s):
    steps = []
    while parent[s] is not None:
        prev, st = parent[s]
        steps.append(st)
        s = prev
    return list(reversed(steps))


def check(parent, edges, rules):
    """Return {rule id: [violation, ...]} with the shortest path for each distinct reason."""
    found = {r["id"]: {} for r in rules}
    order = list(parent)  # BFS order, so the first hit per reason is a shortest path
    for s in order:
        for r in rules:
            if r["state"]:
                why = r["state"](s)
                if why and why not in found[r["id"]]:
                    found[r["id"]][why] = path_to(parent, s)
        for st, t in edges[s]:
            for r in rules:
                if r["step"]:
                    why = r["step"](s, st, t)
                    if why and why not in found[r["id"]]:
                        found[r["id"]][why] = path_to(parent, s) + [st]
    return found


def deadlocks(parent, edges):
    return [s for s in parent if not edges[s] and not is_end(s)]


def fmt_path(steps):
    return [st.label for st in steps]


def main():
    parent, edges = explore()
    n_states = len(parent)
    n_steps = sum(len(v) for v in edges.values())
    all_rules = RULES + SUPPLEMENTARY
    found = check(parent, edges, all_rules)
    dead = deadlocks(parent, edges)

    chart = chartmod.build(parent, edges, found)
    scen = scenarios.run(parent, edges, chart)

    print(f"States reached: {n_states}")
    print(f"Steps: {n_steps}")
    print(f"End states: {sum(1 for s in parent if is_end(s))}")
    print(f"Deadlocks (no step out, not an end state): {len(dead)}")
    for s in dead[:5]:
        print("  ", " -> ".join(fmt_path(path_to(parent, s))))
    print(f"Declared chart states never reached: {chart['unreached'] or 'none'}")
    print()
    for r in all_rules:
        v = found[r["id"]]
        print(f"{r['id']} {r['title']}: {'BREAKS' if v else 'holds'}")
        for why, steps in v.items():
            print(f"  violation: {why}")
            print(f"  shortest path ({len(steps)} steps):")
            for i, lab in enumerate(fmt_path(steps), 1):
                print(f"    {i:2d}. {lab}")
    print()
    print(f"Chart: {chart['n_nodes']} states, {chart['n_arrows']} arrows; "
          f"{chart['hidden']} model steps hidden inside merged states")
    print()
    print(scen["summary_text"])

    (HERE / "chart.mmd").write_text(chart["mermaid"])
    (HERE / "scenario-map.md").write_text(scen["markdown"])
    (HERE / "results.json").write_text(json.dumps({
        "states": n_states, "steps": n_steps, "deadlocks": len(dead),
        "violations": {k: {w: fmt_path(p) for w, p in v.items()} for k, v in found.items()},
        "chart": {k: chart[k] for k in ("n_nodes", "n_arrows", "hidden", "hidden_kinds", "unreached", "legend")},
        "scenarios": scen["rows"], "uncovered": scen["uncovered"],
    }, indent=1))
    write_html(n_states, n_steps, dead, found, chart, scen)


def write_html(n_states, n_steps, dead, found, chart, scen):
    e = html.escape
    RULE_TITLES = {r['id']: r['title'] for r in RULES + SUPPLEMENTARY}
    rules_rows = []
    for r in RULES + SUPPLEMENTARY:
        v = found[r["id"]]
        verdict = "breaks" if v else "holds"
        if r["id"] in ("CO-03", "CO-04"):
            verdict += " (partly not expressible)"
        rules_rows.append(f"<tr><td><b>{r['id']}</b><br>{e(r['title'])}</td><td class=q>{e(r['quote'])}</td>"
                          f"<td>{e(r['encoding'])}</td><td class='{('bad' if v else 'ok')}'>{verdict}</td></tr>")
    viol = []
    for r in RULES + SUPPLEMENTARY:
        for why, steps in found[r["id"]].items():
            items = "".join(f"<li>{e(st.label)}</li>" for st in steps)
            viol.append(f"<div class=viol><h3>{r['id']}: {e(why)}</h3><ol>{items}</ol></div>")
    assum = "".join(f"<tr><td>{a}</td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>"
                    for a, b, c, d in model.ASSUMPTIONS)
    page = f"""<!doctype html>
<html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Cancel-Refund Statechart</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a66;--line:#d9d6cf;--bad:#b3261e;--badbg:#fbe9e7;--ok:#1e6b3a}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#161614;--fg:#ecebe6;--mut:#a3a19a;--line:#3a3935;--bad:#ff8a80;--badbg:#3b1d1a;--ok:#7fd49b}}}}
:root[data-theme="dark"]{{--bg:#161614;--fg:#ecebe6;--mut:#a3a19a;--line:#3a3935;--bad:#ff8a80;--badbg:#3b1d1a;--ok:#7fd49b}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;margin:0;padding:24px 16px;}}
main{{max-width:1100px;margin:auto}} h1{{font-size:24px}} h2{{margin-top:40px;border-bottom:1px solid var(--line)}}
table{{border-collapse:collapse;width:100%;font-size:13px}} td,th{{border:1px solid var(--line);padding:6px;vertical-align:top;text-align:left}}
.q{{color:var(--mut);font-style:italic}} .bad{{color:var(--bad);font-weight:600}} .ok{{color:var(--ok);font-weight:600}}
.viol{{background:var(--badbg);padding:8px 14px;margin:10px 0;border-radius:6px}} .viol h3{{font-size:15px;margin:4px 0}}
.wrap{{overflow-x:auto}} .chartbox{{overflow:auto;max-height:90vh;border:1px solid var(--line);border-radius:6px}} .chartbox svg{{max-width:none!important}} .chartbox, .chartbox *{{line-height:normal;font-family:'trebuchet ms',verdana,arial,sans-serif}} .chartbox .edgeLabel foreignObject, .chartbox .label foreignObject{{overflow:visible}} .chartbox .edgeLabel foreignObject > div{{max-height:12em;overflow:auto}} .chartbox .node foreignObject{{overflow:hidden}} .chartbox .node foreignObject > div{{max-width:220px;max-height:100%;overflow:auto;white-space:normal!important}} .mermaid{{background:#fff;padding:10px;border-radius:6px}} .mut{{color:var(--mut)}}
</style></head><body><main>
<h1>Cancel-and-refund policy as a state machine</h1>
<p class=mut>Built from round0-agent-spec.md (CO-01..CO-07) and review-packet.md. The agent follows the spec's
failure-handling table; the order system, the clock and the customer do anything the inputs allow.
{n_states} states, {n_steps} steps, {len(dead)} deadlocks. Regenerate with <code>python3 check.py</code>.</p>
<h2>Chart</h2>
<p class=mut>Red states are where a rule breaks; the yellow note on each names the rule, and the legend below gives each rule's title. {chart['hidden']} model steps are hidden
inside merged states ({e(', '.join(chart['hidden_kinds']))}).</p>
<div class=chartbox><pre class=mermaid>{e(chart['mermaid'])}</pre></div>
<p><b>Legend for the red states</b></p><ul>{''.join(f"<li><b>{e(lab)}</b>: breaks {e(' and '.join(f'{rid} {RULE_TITLES[rid]}' for rid in rids))}</li>" for lab, rids in chart['legend'])}</ul>
<h2>Rules</h2><div class=wrap><table><tr><th>Rule</th><th>Spec line</th><th>Invariant</th><th>Result</th></tr>{''.join(rules_rows)}</table></div>
<p class=mut>S-1 and S-2 are not CO rules; they check outcomes the stakeholder lines (§2) and G-03 ask for.</p>
<h2>Violations, each with its shortest path</h2>{''.join(viol) or '<p>None.</p>'}
<h2>Assumptions</h2><p class=mut>Every place the inputs are silent and the model had to choose.</p>
<div class=wrap><table><tr><th>Id</th><th>Assumed</th><th>Silent or ambiguous line</th><th>Alternative not chosen</th></tr>{assum}</table></div>
<h2>Scenario map</h2>{scen['html']}
</main>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true, theme:'default', state:{{useMaxWidth:false, nodeSpacing:90, rankSpacing:90}}}});</script>
</body></html>"""
    (HERE / "index.html").write_text(page)


if __name__ == "__main__":
    main()
