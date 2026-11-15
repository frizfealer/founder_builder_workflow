"""Map each CO-S scenario onto the model.

A scenario fixes what the customer and the order system do (its Initial state, User turns
and User-knows answers, read under §5.1: "A supporting actor answers every call normally
unless an Initial-state line says otherwise"). The agent is left free. Every complete
path the model allows under those choices is a match:
  one path  - the scenario pins one model path
  no path   - the model cannot do what the scenario describes
  ambiguous - the scenario's text matches two or more model paths
"""
import html

from chart import START

OPEN, OPEN2, SHIPPED, CANC_OK = "open/none/False", "open/none/True", "shipped/none/False", "cancelled/ok/False"


def normal(kind, s):
    if kind == "lookup":
        return {"answered"}
    if kind == "cancel":
        return {"not_cancellable"} if s.order == "shipped" else {"cancelled"}
    if kind == "refund":
        return {"ok": {"returns_ok"}, "failed": {"returns_failed"}}.get(s.refund, {"ok"})
    if kind == "followup":
        return {"created"}
    return set()


def together(created):
    """'The first and second CO-A3 do not answer, and together they create <refund>'."""
    def first(s):
        return {created, "timeout_none"}

    def second(s):
        return {"timeout_none"} if s.refund != "none" else {created}
    return {1: first, 2: second}


def sc(sid, rows, setup, ask, replies=(), note="", **kw):
    return dict(id=sid, rows=rows, setup=setup, ask=ask, replies=list(replies), note=note, **kw)


YES = ["confirm"]
SCENARIOS = [
    sc("CO-S01", "1-3", OPEN, "number", YES,
       note="Rows differ only in placed/processing and wording, which the model merges (A-01); the delivered "
            "second order is not modelled (A-18)."),
    sc("CO-S02", "1-3", OPEN2, "none", ["names", "confirm"],
       note="Naming by number, item or date is one model event, 'customer names the order'."),
    sc("CO-S03", "1-3", OPEN2, "number", ["change", "confirm"],
       note="Switching to the other order is modelled as 'customer changes the order or a term' (A-12); "
            "the model does not track which order ends up cancelled."),
    sc("CO-S04", "1-3", OPEN, "number", ["withdraw"]),
    sc("CO-S05", "1-3", SHIPPED, "number", note="Shipped and delivered are one value (A-01)."),
    sc("CO-S06", "1-2", CANC_OK, "number"),
    sc("CO-S07", "1-3", OPEN, "unknown"),
    sc("CO-S08", "1-3", OPEN, "partial", ["keeps"]),
    sc("CO-S09", "1-3", OPEN, "other_method", YES),
    sc("CO-S10", "1-2", OPEN, "number", lookup_pre="timeout"),
    sc("CO-S11", "1", OPEN, "number", YES, ship=lambda s: s.pending == "cancel" and s.cancel_n == 1,
       cancel={1: lambda s: {"not_cancellable"} if s.order == "shipped" else set()}),
    sc("CO-S11", "2", OPEN, "number", YES, ship=lambda s: s.pending == "cancel" and s.cancel_n == 1,
       cancel={1: lambda s: {"timeout_none"} if s.order == "shipped" else set()}),
    sc("CO-S12", "1-2", OPEN, "number", YES, cancel={1: {"timeout_cancelled", "timeout_late"}}, late=True,
       note="'That CO-A2 cancels <order>' does not say when; a cancel that lands after the agent's lookup "
            "is the case SG-04 names (A-09)."),
    sc("CO-S13", "1-2", OPEN, "number", YES, cancel={1: {"timeout_none"}}),
    sc("CO-S14", "1-2", OPEN, "number", YES, cancel={1: {"timeout_none"}}, lookup_cancel={1: "timeout"}),
    sc("CO-S15", "1-2", OPEN, "number", YES, cancel={1: {"timeout_none"}, 2: {"timeout_none"}},
       lookup_cancel={2: "timeout"}),
    sc("CO-S16", "1", OPEN, "number", YES, refund={1: {"provider_unavailable"}}),
    sc("CO-S16", "2", OPEN, "number", YES, refund={1: {"timeout_ok"}}),
    sc("CO-S16", "3", OPEN, "number", YES, refund={1: {"timeout_none"}}),
    sc("CO-S17", "1-2", OPEN, "number", YES, refund={1: {"failed"}},
       note="Card closed and provider declined are one value; the model has no failure reason."),
    sc("CO-S17", "3", OPEN, "number", YES, refund={1: {"not_cancelled"}}),
    sc("CO-S18", "1-2", OPEN, "number", YES, refund={1: {"provider_unavailable"}, 2: {"provider_unavailable"}}),
    sc("CO-S19", "1-2", OPEN, "number", YES, refund=together("timeout_ok"),
       note="Pending and issued are one value (A-02)."),
    sc("CO-S20", "1", OPEN, "number", YES, refund=together("timeout_failed")),
    sc("CO-S20", "2", OPEN, "number", YES, refund={1: {"timeout_none"}, 2: {"timeout_none"}}),
    sc("CO-S21", "1", OPEN, "number", YES, refund=together("timeout_ok"), lookup_refund="timeout"),
    sc("CO-S21", "2", OPEN, "number", YES, refund=together("timeout_failed"), lookup_refund="timeout"),
    sc("CO-S22", "1", OPEN, "number", YES, refund={1: {"failed"}}, fu={1: {"timeout_none"}}),
    sc("CO-S22", "2", OPEN, "number", YES, refund={1: {"failed"}}, fu={1: {"timeout_created"}}),
    sc("CO-S23", "1-2", OPEN, "number", YES, refund={1: {"failed"}}, fu={1: {"timeout_none"}, 2: {"timeout_none"}}),
    sc("CO-S24", "1-2", OPEN, "number", YES, cancel={1: {"not_found"}}),
]


def pick(spec, key, n, kind, s):
    v = spec.get(key, {}).get(n) if isinstance(spec.get(key), dict) else None
    if v is None:
        return normal(kind, s)
    return v(s) if callable(v) else v


def allowed(spec, s, st, ri):
    """Is this non-agent step what the scenario says happens? Returns the new reply index, or None."""
    if st.actor == "setup":
        return ri if st.outcome == spec["setup"] else None
    if st.kind == "ask":
        return ri if st.outcome == spec["ask"] else None
    if st.actor == "customer":
        reps = spec["replies"]
        return ri + 1 if ri < len(reps) and reps[ri] == st.outcome else None
    if st.kind == "ship":
        return ri if spec.get("ship") and spec["ship"](s) else None
    if st.kind == "late":
        return ri if spec.get("late") else None
    if st.kind == "lookup":
        if s.cancel_n == 0:
            want = spec.get("lookup_pre", "answered")
        elif s.refund_n == 0:
            want = spec.get("lookup_cancel", {}).get(s.cancel_n, "answered")
        else:
            want = spec.get("lookup_refund", "answered")
        return ri if st.outcome == want else None
    key, n = {"cancel": ("cancel", s.cancel_n), "refund": ("refund", s.refund_n), "followup": ("fu", s.fu_n)}[st.kind]
    return ri if st.outcome in pick(spec, key, n, st.kind, s) else None


def paths_for(spec, initial, edges, limit=200):
    found = []

    def dfs(s, ri, path, seen):
        if len(found) >= limit:
            return
        if s.loc == "end" and not s.late_cancel and ri == len(spec["replies"]):
            found.append(list(path))
            return
        for st, t in edges[s]:
            nri = ri if st.actor == "agent" else allowed(spec, s, st, ri)
            if nri is None or (t, nri) in seen:
                continue
            seen.add((t, nri))
            path.append((s, st, t))
            dfs(t, nri, path, seen)
            path.pop()
            seen.discard((t, nri))

    dfs(initial, 0, [], {(initial, 0)})
    return found


def run(parent, edges, chart):
    initial = next(iter(parent))
    node, first_step, label = chart["node"], chart["first_step"], chart["label"]
    from chart import short

    rows, covered = [], set()
    for spec in SCENARIOS:
        ps = paths_for(spec, initial, edges)
        for p in ps:
            for s, st, t in p:
                a, b = node(s), node(t)
                if a != b:
                    covered.add((a, b, short(s, st)))
        verdict = "no path" if not ps else "one path" if len(ps) == 1 else "ambiguous"
        shown = ps[:2]
        rows.append(dict(id=spec["id"], rows=spec["rows"], verdict=verdict, count=len(ps),
                         paths=[[st.label for _, st, _ in p] for p in shown],
                         differs=differs(shown) if len(shown) == 2 else "", note=spec["note"]))

    uncovered = []
    for (a, b, lab), (s, st) in first_step.items():
        if (a, b, lab) in covered:
            continue
        steps = path_to(parent, s) + [st]
        frm = "start" if a[0] == START else label(a)
        uncovered.append(dict(arrow=f"{frm} --> {label(b)}", text=lab, path=[x.label for x in steps]))

    counts = {k: sum(1 for r in rows if r["verdict"] == k) for k in ("one path", "no path", "ambiguous")}
    return dict(rows=rows, uncovered=uncovered, counts=counts,
                summary_text=summary_text(rows, uncovered, counts),
                markdown=markdown(rows, uncovered, counts), html=as_html(rows, uncovered, counts))


def path_to(parent, s):
    steps = []
    while parent[s] is not None:
        prev, st = parent[s]
        steps.append(st)
        s = prev
    return list(reversed(steps))


def differs(two):
    a, b = ([st.label for _, st, _ in p] for p in two)
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return f"the paths part at step {i + 1}: '{a[i] if i < len(a) else '(end)'}' vs '{b[i] if i < len(b) else '(end)'}'"


def summary_text(rows, uncovered, counts):
    out = [f"Scenario map: {len(rows)} scenario rows: {counts['one path']} one path, "
           f"{counts['no path']} no path, {counts['ambiguous']} ambiguous"]
    for r in rows:
        extra = f" ({r['count']} paths; {r['differs']})" if r["verdict"] == "ambiguous" else ""
        out.append(f"  {r['id']} rows {r['rows']}: {r['verdict']}{extra}")
    out.append(f"Chart arrows no scenario takes: {len(uncovered)}")
    for u in uncovered:
        out.append(f"  {u['arrow']}  [{u['text']}]")
        out.append(f"     shortest path: {' -> '.join(u['path'])}")
    return "\n".join(out)


def markdown(rows, uncovered, counts):
    out = ["# Scenario map", "",
           "Generated by `python3 check.py`. Each CO-S scenario is replayed on the model: the scenario fixes what the "
           "customer and the order system do (its Initial state, User turns and User-knows answers; a supporting actor "
           "answers normally unless Initial state says otherwise, §5.1), and the agent is left free. Every complete path "
           "the model allows is a match.", "",
           f"**Summary:** {len(rows)} scenario rows: {counts['one path']} one path, {counts['no path']} no path, "
           f"{counts['ambiguous']} ambiguous. {len(uncovered)} chart arrows are taken by no scenario.", "",
           "| Scenario | Data rows | Verdict | Model path (events in order) | Note |", "|---|---|---|---|---|"]
    for r in rows:
        if r["verdict"] == "ambiguous":
            p = (f"{r['count']} paths; {r['differs']}.<br>Path 1: " + " → ".join(r["paths"][0]) +
                 "<br>Path 2: " + " → ".join(r["paths"][1]))
        elif r["paths"]:
            p = " → ".join(r["paths"][0])
        else:
            p = "(none)"
        out.append(f"| {r['id']} | {r['rows']} | {r['verdict']} | {p} | {r['note']} |")
    out += ["", "## Paths no scenario covers", "",
            "Each row is a chart arrow (with its text) that no scenario path takes, and the shortest model path that takes it.", "",
            "| Arrow | Arrow text | Shortest path |", "|---|---|---|"]
    for u in uncovered:
        out.append(f"| {u['arrow']} | {u['text']} | {' → '.join(u['path'])} |")
    return "\n".join(out) + "\n"


def as_html(rows, uncovered, counts):
    e = html.escape
    trs = []
    for r in rows:
        if r["verdict"] == "ambiguous":
            p = (f"<b>{r['count']} paths</b>; {e(r['differs'])}<ol>" +
                 "".join("<li>" + e(" → ".join(x)) + "</li>" for x in r["paths"]) + "</ol>")
        else:
            p = e(" → ".join(r["paths"][0])) if r["paths"] else "(none)"
        cls = "ok" if r["verdict"] == "one path" else "bad"
        trs.append(f"<tr><td>{r['id']}</td><td>{r['rows']}</td><td class={cls}>{r['verdict']}</td><td>{p}</td>"
                   f"<td class=mut>{e(r['note'])}</td></tr>")
    us = "".join(f"<tr><td>{e(u['arrow'])}</td><td>{e(u['text'])}</td><td>{e(' → '.join(u['path']))}</td></tr>"
                 for u in uncovered)
    return (f"<p>{len(rows)} scenario rows: {counts['one path']} one path, {counts['no path']} no path, "
            f"{counts['ambiguous']} ambiguous.</p><div class=wrap><table><tr><th>Scenario</th><th>Rows</th><th>Verdict</th>"
            f"<th>Model path</th><th>Note</th></tr>{''.join(trs)}</table></div>"
            f"<h3>Chart arrows no scenario takes ({len(uncovered)})</h3><div class=wrap><table><tr><th>Arrow</th>"
            f"<th>Text</th><th>Shortest path</th></tr>{us}</table></div>")
