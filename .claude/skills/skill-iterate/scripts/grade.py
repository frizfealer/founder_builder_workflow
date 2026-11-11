#!/usr/bin/env python3
"""Grade skill trials against a baseline, from eval/<skill>/grading.json and results/*/trial.json.

Usage:
  grade.py <eval-dir> [--labels a,b,c] [--set <prefix>] [--gate] [--json out.json]

Code metrics are computed here. Judge metrics (kind "judge" in grading.json) are read from
results/<label>/judge/<metric>.verdict.json when present; otherwise a task file
results/<label>/judge/<metric>.task.md is written for a fresh-context judge to answer, and the
cell shows "pending". The /grade command dispatches those judges and reruns this script.

--set <prefix> groups labels <prefix>-1, <prefix>-2, ... and reports min/max across them.
--gate exits 1 when any gated metric fails in any trial of the set (or of all labels given).
A gated metric fails when it misses its absolute bound (min/max) or is worse than the worst
baseline value by more than `tolerance`. Baseline labels per kind come from grading.json.
"""
import json
import re
import sys
from pathlib import Path


def load(p):
    return json.loads(Path(p).read_text())


def model_of(sub, default):
    """A subagent's model: its own field, else a name found in its role/agent text, else the default."""
    m = (sub.get("model") or "").lower()
    if not m:
        text = (sub.get("role", "") + " " + str(sub.get("agent", ""))).lower()
        for k in ("sonnet", "haiku", "opus", "codex"):
            if k in text:
                m = k
                break
    if sub.get("codex") and not m:
        m = "codex"
    for k in ("sonnet", "haiku", "opus", "codex"):
        if k in m:
            return k
    return default


def code_metrics(t, g=None):
    subs = t.get("subagents", [])
    rates = (g or {}).get("model_rates", {})
    default_model = rates.get("default", "opus")
    cost = None
    if rates:
        cost = 0.0
        for s_ in subs:
            if s_.get("tokens") is not None:
                cost += s_["tokens"] * float(rates.get(model_of(s_, default_model), rates.get(default_model, 0))) / 1e6
        cost = round(cost, 2)
    finders = [s for s in subs if s["kind"] == "finder" and not s.get("codex")]
    kept = sum(r.get("kept", 0) for r in t["rounds"])
    dropped = sum(r.get("dropped", 0) for r in t["rounds"])
    tool = [s["tool_uses"] for s in finders if s.get("tool_uses") is not None]
    dur = [s["duration_ms"] for s in finders if s.get("duration_ms") is not None]
    tok = [s["tokens"] for s in subs if s.get("tokens") is not None]
    i = t.get("integrity", {})
    return {
        "integrity": "pass" if (i.get("script_errors", 1) == 0 and i.get("checker_zero_errors_seen") and not i.get("asked_user")) else "FAIL",
        "wall_clock_s": t.get("wall_clock_s"),
        "finder_tool_calls_max": max(tool) if tool else None,
        "finder_duration_max_s": round(max(dur) / 1000) if dur else None,
        "tokens_total_k": round(sum(tok) / 1000) if tok else None,
        "cost_usd": cost,
        "rounds_run": len(t["rounds"]),
        "kept_total": kept,
        "important_kept": sum(r.get("important_kept", 0) for r in t["rounds"]),
        "verifier_drop_rate": round(dropped / (kept + dropped), 2) if (kept + dropped) else None,
        "codex_subagents": sum(1 for s in subs if s.get("codex")),
    }


def key_findings_text(eval_dir, key):
    text = (eval_dir / key["file"]).read_text()
    lines = text.splitlines()
    out = {}
    hdr = re.compile(r"^(?:##\s*)?(" + "|".join(map(re.escape, key["ids"])) + r")\s*\|")
    starts = [(i, hdr.match(l).group(1)) for i, l in enumerate(lines) if hdr.match(l)]
    for k, (i, fid) in enumerate(starts):
        end = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
        block = "\n".join(lines[i:end]).strip()
        # cut at the next non-key finding header
        block = re.split(r"\n(?:##\s*)?[A-Z]\d*-?\d+\s*\|", block)[0]
        out[fid] = block
    return out


def write_judge_task(eval_dir, t, g, metric, folder):
    jd = folder / "judge"
    jd.mkdir(exist_ok=True)
    kind = t["kind"]
    ctx = g["judge_context"]
    spec = Path(ctx["spec_for_kind"][kind])  # paths below are relative to eval_dir; the judge runs from there
    folder = Path("results") / folder.name
    findings_glob = t.get("findings_glob") or f"{folder}/round*-findings.md"
    final_spec = t.get("final_spec", f"{folder}/agent-spec-final.md")
    snaps = sorted(p.name for p in (eval_dir / folder / "rounds").glob("round*-agent-spec.md")) if (eval_dir / folder / "rounds").exists() else []
    snap_note = (f" The spec as it stood after each round is in `{folder}/rounds/` ({', '.join(snaps)}); read a round-N finding against round{{N-1}}, which is the text it quoted.") if snaps else " No per-round snapshots exist for this trial; judge round-2 and round-3 findings from their own quoted text."
    kept = [f for f in t["findings"] if f.get("kept")]
    if metric in ("recall_key", "recall_found"):
        key = g["key"][kind]
        keytext = key_findings_text(eval_dir, key)
        pool = kept if metric == "recall_key" else [f for f in t["findings"] if f.get("kept") is not None]
        body = [f"# Judge task: {metric} for trial {t['label']}", "",
                "You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.", "",
                f"Spec the findings refer to: `{spec}`. Review packet: `{ctx['packet']}`.",
                f"The trial's full findings, with evidence, are in `{findings_glob}`.", "",
                "For each KEY defect below, decide whether any finding in the trial reports the SAME defect in the SAME block of the spec: the same rule, failure row, scenario or dimension, and the same thing wrong with it. A finding that touches the same block but names a different defect is not a match. A finding that names the same defect under a wider pattern that includes this block is a match.", "",
                f"Output exactly one JSON object, nothing else, as the file `judge/{metric}.verdict.json`:",
                '```json', '{"metric": "' + metric + '", "matches": {"<KEY id>": "<trial finding id or null>"}, "evidence": {"<KEY id>": "<one line: the trial quote or location that matches, or why nothing does>"}}', '```', "",
                "## KEY defects", ""]
        for fid in key["ids"]:
            body += [f"### {fid}", "```", keytext.get(fid, "(not found in key file)"), "```", ""]
        body += ["## Trial findings (" + ("kept only" if metric == "recall_key" else "kept AND dropped: a dropped finding still counts as reported") + "), summary lines", ""]
        for f in pool:
            body.append(f"- {f['id']} | {f.get('class')} | {f.get('severity')} | {f.get('location')}\n  Quote: {f.get('quote', '')[:300]}")
    elif metric in ("false_positives", "dropped_real"):
        pool = kept if metric == "false_positives" else [f for f in t["findings"] if f.get("kept") is False]
        body = [f"# Judge task: {metric} for trial {t['label']}", "",
                ("You are checking whether each kept finding is a real defect." if metric == "false_positives" else "You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation.") + " You did not write the spec or the findings. Read only; edit nothing.", "",
                f"Read the review packet `{ctx['packet']}`, the sources it lists, and the spec `{spec}`. Apply the verifier brief in `{ctx['verifier_brief']}`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.", "",
                f"The findings with their evidence are in `{findings_glob}`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes" + (f"; `{final_spec}` is the end state." if final_spec else "; no end-state copy exists for this trial, judge from the finding's own evidence.") + snap_note, "",
                f"Output exactly one JSON object, nothing else, as the file `judge/{metric}.verdict.json`:",
                '```json', '{"metric": "' + metric + '", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}', '```', "",
                "## Findings to judge", ""]
        for f in pool:
            body.append(f"- {f['id']} (round {f['round']}) | {f.get('class')} | {f.get('severity')} | {f.get('location')}")
    else:
        return
    body.insert(2, f"Run from `{eval_dir.name}`'s parent: all paths below are relative to `eval/{eval_dir.name}/`.")
    (jd / f"{metric}.task.md").write_text("\n".join(body) + "\n")


def judge_metrics(eval_dir, t, g, folder):
    out = {}
    for m in g["metrics"]:
        if m["kind"] != "judge":
            continue
        vf = folder / "judge" / f"{m['name']}.verdict.json"
        if vf.exists():
            v = load(vf)
            if v.get("error"):
                write_judge_task(eval_dir, t, g, m["name"], folder)
                out[m["name"]] = "pending"
                t.setdefault("warnings", []).append(f"judge {m['name']}: {v['error']}")
                continue
            if m["name"] in ("recall_key", "recall_found"):
                ids = g["key"][t["kind"]]["ids"]
                hit = sum(1 for k in ids if v.get("matches", {}).get(k))
                out[m["name"]] = round(hit / len(ids), 2)
            elif m["name"] in ("fp_important", "fp_nit"):
                continue  # derived from the false_positives verdict below
            elif m["name"] == "dropped_real":
                vals = list(v.get("verdicts", {}).values())
                if not vals or all(x is None for x in vals):
                    out[m["name"]] = 0 if not [f for f in t["findings"] if f.get("kept") is False] else "pending"
                    if out[m["name"]] == "pending":
                        write_judge_task(eval_dir, t, g, m["name"], folder)
                    continue
                out[m["name"]] = sum(1 for x in vals if isinstance(x, str) and x.lower() == "real")
            elif m["name"] == "false_positives":
                vals = list(v.get("verdicts", {}).values())
                if not vals or all(x is None for x in vals):
                    write_judge_task(eval_dir, t, g, m["name"], folder)
                    out[m["name"]] = "pending"
                    continue
                out[m["name"]] = sum(1 for x in vals if isinstance(x, str) and x.lower() in ("not real", "style only"))
                sev = {f["id"]: f.get("severity") == "Important" for f in t["findings"]}
                fps = [fid for fid, x in v.get("verdicts", {}).items() if isinstance(x, str) and x.lower() in ("not real", "style only")]
                out["fp_important"] = sum(1 for fid in fps if sev.get(fid))
                out["fp_nit"] = sum(1 for fid in fps if not sev.get(fid))
                if any(x is None for x in vals):
                    t.setdefault("warnings", []).append(f"judge false_positives: {sum(1 for x in vals if x is None)} null verdicts counted as Real")
        elif m["name"] in ("fp_important", "fp_nit"):
            out.setdefault(m["name"], "pending")
        elif m["name"] == "dropped_real" and not [f for f in t["findings"] if f.get("kept") is False]:
            out[m["name"]] = 0  # nothing was dropped, nothing to judge
        else:
            write_judge_task(eval_dir, t, g, m["name"], folder)
            out[m["name"]] = "pending"
    return out


def worse(direction, value, ref, tol):
    if direction == "lower":
        return value > ref * (1 + tol)
    if direction == "higher":
        return value < ref * (1 - tol)
    return False


def evaluate(eval_dir, labels, g):
    results_dir = eval_dir / "results"
    trials = {}
    for lab in labels:
        tj = results_dir / lab / "trial.json"
        if not tj.exists():
            print(f"skip {lab}: no trial.json", file=sys.stderr)
            continue
        t = load(tj)
        row = code_metrics(t, g)
        row.update(judge_metrics(eval_dir, t, g, results_dir / lab))
        trials[lab] = {"kind": t["kind"], "metrics": row, "warnings": t.get("warnings", [])}
    # baseline references per kind
    refs = {}
    for kind, spec in g["kinds"].items():
        vals = {}
        for bl in spec["baseline_labels"]:
            tj = results_dir / bl / "trial.json"
            if not tj.exists():
                continue
            bt = load(tj)
            bm = code_metrics(bt, g)
            bm.update(judge_metrics(eval_dir, bt, g, results_dir / bl))
            excl = set(g.get("baseline_exclude", {}).get(bl, []))
            for k, v in bm.items():
                if isinstance(v, (int, float)) and k not in excl:
                    vals.setdefault(k, []).append(v)
        refs[kind] = vals
    # gate decisions
    for lab, tr in trials.items():
        fails = []
        for m in g["metrics"]:
            if not m.get("gate"):
                continue
            v = tr["metrics"].get(m["name"])
            if v == "pending":
                fails.append(f"{m['name']}: pending")
                continue
            if m["direction"] == "pass":
                if v != "pass":
                    fails.append(f"{m['name']}: {v}")
                continue
            if v is None:
                fails.append(f"{m['name']}: missing")
                continue
            if "min" in m and v < m["min"]:
                fails.append(f"{m['name']}: {v} < {m['min']}")
            if "max" in m and v > m["max"]:
                fails.append(f"{m['name']}: {v} > {m['max']}")
            ref = refs.get(tr["kind"], {}).get(m["name"])
            if ref and lab not in g["kinds"][tr["kind"]]["baseline_labels"]:
                worst = max(ref) if m["direction"] == "lower" else min(ref)
                if worse(m["direction"], v, worst, g.get("tolerance", 0.1)):
                    fails.append(f"{m['name']}: {v} vs baseline worst {worst}")
        tr["fails"] = fails
    return trials, refs


def table(trials, g, refs):
    names = [m["name"] for m in g["metrics"]]
    gated = {m["name"] for m in g["metrics"] if m.get("gate")}
    head = "| trial | kind | " + " | ".join(("*" if n in gated else "") + n for n in names) + " | verdict |"
    sep = "|" + "---|" * (len(names) + 3)
    rows = [head, sep]
    for lab, tr in trials.items():
        cells = [str(tr["metrics"].get(n, "")) for n in names]
        verdict = "baseline" if lab in sum((k["baseline_labels"] for k in g["kinds"].values()), []) else ("PASS" if not tr["fails"] else "FAIL: " + "; ".join(tr["fails"]))
        rows.append(f"| {lab} | {tr['kind']} | " + " | ".join(cells) + f" | {verdict} |")
    for kind, vals in refs.items():
        if vals:
            rows.append(f"| baseline worst ({kind}) | {kind} | " + " | ".join(
                (str(max(vals[n]) if g_dir(g, n) == "lower" else min(vals[n])) if n in vals and g_dir(g, n) in ("lower", "higher") else "") for n in names) + " | |")
    return "\n".join(rows)


def g_dir(g, name):
    return next(m["direction"] for m in g["metrics"] if m["name"] == name)


def set_summary(trials, prefix, g):
    members = {k: v for k, v in trials.items() if re.fullmatch(re.escape(prefix) + r"-\d+", k)}
    if not members:
        return ""
    lines = [f"\n**Set {prefix}** ({len(members)} trials): worst value per gated metric"]
    for m in g["metrics"]:
        if not m.get("gate") or m["direction"] == "pass":
            continue
        vals = [t["metrics"].get(m["name"]) for t in members.values()]
        nums = [v for v in vals if isinstance(v, (int, float))]
        if len(nums) < len(vals):
            lines.append(f"- {m['name']}: pending in {len(vals) - len(nums)} trial(s)")
        elif nums:
            lines.append(f"- {m['name']}: {max(nums) if m['direction'] == 'lower' else min(nums)}  (all: {vals})")
    allpass = all(not t["fails"] for t in members.values())
    lines.append(f"- set verdict: {'PASS' if allpass else 'FAIL'}")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    eval_dir = Path(args[0]).resolve()
    g = load(eval_dir / "grading.json")
    labels = None
    prefix = None
    gate = "--gate" in args
    out_json = None
    for i, a in enumerate(args):
        if a == "--labels":
            labels = args[i + 1].split(",")
        if a == "--set":
            prefix = args[i + 1]
        if a == "--json":
            out_json = args[i + 1]
    if labels is None:
        labels = sorted(p.name for p in (eval_dir / "results").iterdir() if (p / "trial.json").exists())
    trials, refs = evaluate(eval_dir, labels, g)
    print(f"# Grades: {g['skill']}  ({eval_dir})\n")
    print(table(trials, g, refs))
    print("\nMetrics (* = gated; a gated metric fails below its bound or when worse than the worst baseline by more than "
          f"{int(g.get('tolerance', 0.1) * 100)} %):")
    for m in g["metrics"]:
        bound = f" (min {m['min']})" if "min" in m else f" (max {m['max']})" if "max" in m else ""
        print(f"- {'*' if m.get('gate') else ''}{m['name']}{bound}: {m.get('about', m['direction'])}")
    if g.get("notes"):
        print("- note: " + g["notes"])
    if prefix:
        print(set_summary(trials, prefix, g))
    derived = {"fp_important", "fp_nit"}  # computed from the false_positives verdict; no task of their own
    pend = [f"{lab}/judge/{m}.task.md" for lab, tr in trials.items() for m, v in tr["metrics"].items() if v == "pending" and m not in derived]
    if pend:
        print(f"\n{len(pend)} judge task(s) written, run them and re-grade:")
        for p in pend:
            print("  results/" + p)
    warn = {lab: tr["warnings"] for lab, tr in trials.items() if tr["warnings"]}
    if warn:
        print("\nExtraction warnings:")
        for lab, ws in warn.items():
            for w in ws:
                print(f"  {lab}: {w}")
    if out_json:
        Path(out_json).write_text(json.dumps({"trials": trials, "baseline_refs": refs}, indent=1))
    if gate:
        target = {k: v for k, v in trials.items() if (prefix is None or re.fullmatch(re.escape(prefix) + r"-\d+", k))}
        sys.exit(1 if any(t["fails"] for t in target.values()) else 0)


if __name__ == "__main__":
    main()
