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
import difflib
import json
import re
import sys
from pathlib import Path


def load(p):
    return json.loads(Path(p).read_text())


def applies(m, kind):
    """A metric applies to every kind unless it lists its kinds."""
    return kind in m.get("kinds", [kind])


def final_spec_path(t, label):
    """The trial's end-state artifact, relative to the eval dir."""
    return t.get("final_spec") or f"results/{label}/agent-spec-final.md"


def golden_distance(eval_dir, t, label, m):
    """1 - difflib ratio over whitespace-normalised non-blank lines of the trial's final spec and the golden file."""
    def lines(p):
        return [re.sub(r"\s+", " ", l).strip() for l in Path(p).read_text().splitlines() if l.strip()]
    trial = eval_dir / final_spec_path(t, label)
    if not trial.exists():
        return None
    ratio = difflib.SequenceMatcher(None, lines(eval_dir / m["golden"]), lines(trial), autojunk=False).ratio()
    return round(1 - ratio, 3)


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
            r = rates.get(model_of(s_, default_model), rates.get(default_model, {}))
            if isinstance(r, (int, float)):  # old flat form
                r = {"blended": float(r), "in": float(r), "out": float(r), "cache_read": float(r)}
            if s_.get("tokens_in") is not None or s_.get("tokens_out") is not None:
                cost += (s_.get("tokens_in") or 0) * r.get("in", 0) / 1e6
                cost += (s_.get("tokens_out") or 0) * r.get("out", 0) / 1e6
                cost += (s_.get("tokens_cache_read") or 0) * r.get("cache_read", 0) / 1e6
            elif s_.get("tokens") is not None:
                cost += s_["tokens"] * r.get("blended", 0) / 1e6
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
        "effort": t.get("effort") or "?",
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


def blind_finding_text(folder, fid, rnd):
    """A finding's own block (header, Quote, Evidence, Pattern) from round<rnd>-findings.md, with every
    verifier / decision / status line cut, so a judge rules on the finding, not on the refutation.
    Handles three layouts seen so far: bare body under the header; body in a code fence; and
    'Finder <name> wrote:' followed by a fenced copy under the finder's local id (F4, N2, ...)."""
    f = folder / f"round{rnd}-findings.md"
    if not f.exists():
        return ""
    lines = f.read_text().splitlines()
    hdr = re.compile(r"^(?:##+\s*)?" + re.escape(fid) + r"\b")
    start = next((i for i, l in enumerate(lines) if hdr.match(l)), None)
    if start is None:
        return ""
    head = re.sub(r"\s+[\u2014-]+\s+(kept|dropped|Pre-existing)\b.*$", "", lines[start], flags=re.I)
    any_id = r"(?:R\d-L?\d+|[MNP]\d+)"
    # 1. the finding's section: up to the next finding header
    section = []
    for l in lines[start + 1:]:
        m = re.match(r"^(?:##+\s*)?(" + any_id + r")\b", l)
        if (m and m.group(1) != fid) or (l.startswith("## ") and not hdr.match(l)):
            break
        section.append(l)
    has_body = lambda txt: re.search(r"^(Quote|Evidence|Pattern):", txt, re.M) is not None
    meta = re.compile(r"^\**\s*(Verifier|Verifiers?|Decision|Decision reason|Status|Routing|Standard verifier|Adversarial verifier|Outcome|Kept|Dropped|Disposition)\b", re.I)
    # 2. prefer a fenced copy of the finding, unless a verifier line introduces the fence
    i, prev = 0, ""
    while i < len(section):
        l = section[i]
        if l.strip().startswith("```"):
            j = i + 1
            while j < len(section) and not section[j].strip().startswith("```"):
                j += 1
            block = "\n".join(section[i + 1:j]).strip()
            if has_body(block) and not re.search(r"verifier|adversarial|refut", prev, re.I):
                return (head + "\n" + block).strip()
            i = j + 1
            continue
        if l.strip():
            prev = l
        i += 1
    # 3. bare body: walk until a verifier / decision line
    out = [head]
    for l in section:
        if meta.match(l.strip()):
            break
        if l.strip() == "```":
            continue
        out.append(l)
    body = "\n".join(out).strip()
    return body if has_body(body) else ""

def write_judge_task(eval_dir, t, g, metric, folder):
    jd = folder / "judge"
    jd.mkdir(exist_ok=True)
    kind = t["kind"]
    ctx = g["judge_context"]
    spec = Path(ctx["spec_for_kind"].get(kind) or "")  # paths below are relative to eval_dir; the judge runs from there
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
        real_folder = eval_dir / folder
        body = [f"# Judge task: {metric} for trial {t['label']}", "",
                ("You are checking whether each kept finding is a real defect." if metric == "false_positives" else "You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation.") + " You did not write the spec or the findings. Read only; edit nothing.", "",
                f"Read the review packet `{ctx['packet']}`, the sources it lists, and the spec `{spec}`. Apply the verifier brief in `{ctx['verifier_brief']}`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.", "",
                (f"The findings with their evidence are in `{findings_glob}`; the ids to judge are listed below." if metric == "false_positives"
                 else "Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected.")
                + " A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes" + (f"; `{final_spec}` is the end state." if final_spec else "; no end-state copy exists for this trial, judge from the finding's own evidence.") + snap_note, "",
                f"Output exactly one JSON object, nothing else, as the file `judge/{metric}.verdict.json`:",
                '```json', '{"metric": "' + metric + '", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}', '```', "",
                "## Findings to judge", ""]
        for f in pool:
            body.append(f"- {f['id']} (round {f['round']}) | {f.get('class')} | {f.get('severity')} | {f.get('location')}")
            if metric == "dropped_real":
                txt = blind_finding_text(real_folder, f["id"], f["round"])
                body += ["", "```", txt or f"(text not found) Quote: {f.get('quote', '')}", "```", ""]
    elif metric in ("input_coverage", "unsupported_statements"):
        inputs = ", ".join(f"`{p}`" for p in [ctx["packet"]] + ctx.get("inputs", []))
        body = [f"# Judge task: {metric} for trial {t['label']}", "",
                "You are checking a spec the trial wrote from scratch against the inputs it was written from. You did not write the spec or the inputs. Read only; edit nothing.", "",
                f"Inputs: {inputs}. The interview answers, the shared-understanding summary and the tool confirmation turn in the packet are the user's words; the packet's ledger and tool table summarise them. The spec: `{final_spec}`.", ""]
        if metric == "input_coverage":
            key = g["key"][kind]
            keytext = key_findings_text(eval_dir, key)
            body += ["For each checklist item below, decide whether the spec asserts it the way the item says it must be asserted: the named kind of rule, failure row, Appendix line or scenario exists, and what it asserts matches the input. `covered` when it does; `missing` when no such line exists or it asserts only part of the item; `contradicted` when the spec asserts something the item's input rules out. Ids in the spec are the trial's own; match on substance, not on ids.", "",
                     f"Output exactly one JSON object, nothing else, as the file `judge/{metric}.verdict.json`:",
                     '```json', '{"metric": "input_coverage", "items": {"<item id>": "covered|missing|contradicted"}, "evidence": {"<item id>": "<one line: the spec rule/scenario id and quote that covers it, or what is missing>"}}', '```', "",
                     "## Checklist items", ""]
            for fid in key["ids"]:
                body += [keytext.get(fid, f"{fid} | (not found in key file)").splitlines()[0], ""]  # one line per item
        else:
            body += ["List every UNSUPPORTED statement in the spec. A statement is one rule, precondition, Scope & Authority line, failure row, Appendix A or Appendix B row, data-model field or tool outcome. It is unsupported when it asserts a product fact (a policy, limit, time window, fee, field, status, tool parameter or outcome, staff or store behaviour, or a promise to the customer) that the inputs neither state nor follow from, or that the inputs contradict.", "",
                     "Not unsupported: a rule the inputs imply; handling the inputs leave to the writer when it adds no new product fact (the user asked the writer to derive further failure cases); the generic guarantees every Agent Spec carries (truthful reporting, no change outside the request, authorization current at each write, no blind retry after an unknown result); template text in the Evaluation section; illustrative values in scenarios (order numbers, amounts, names, dates); anything the spec itself marks as an open question or assumption for the user to confirm.", "",
                     "Count each distinct unsupported fact once, at its first or clearest occurrence, even when several lines repeat it.", "",
                     f"Output exactly one JSON object, nothing else, as the file `judge/{metric}.verdict.json`:",
                     '```json', '{"metric": "unsupported_statements", "statements": [{"location": "<rule, row or section id>", "quote": "<the spec line>", "why": "<one line: what the inputs say instead, or that they are silent>"}]}', '```', ""]
    else:
        return
    body.insert(2, f"Run from `{eval_dir.name}`'s parent: all paths below are relative to `eval/{eval_dir.name}/`.")
    (jd / f"{metric}.task.md").write_text("\n".join(body) + "\n")


def judge_metrics(eval_dir, t, g, folder):
    out = {}
    for m in g["metrics"]:
        if m["kind"] != "judge" or not applies(m, t["kind"]):
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
            elif m["name"] == "input_coverage":
                ids = g["key"][t["kind"]]["ids"]
                items = v.get("items") or {}
                if not items:
                    write_judge_task(eval_dir, t, g, m["name"], folder)
                    out[m["name"]] = "pending"
                    continue
                out[m["name"]] = round(sum(1 for k in ids if items.get(k) == "covered") / len(ids), 2)
            elif m["name"] == "unsupported_statements":
                if not isinstance(v.get("statements"), list):
                    write_judge_task(eval_dir, t, g, m["name"], folder)
                    out[m["name"]] = "pending"
                    continue
                out[m["name"]] = len(v["statements"])
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


def artifact_metrics(eval_dir, t, g, label):
    """Code metrics read from the trial's files rather than trial.json."""
    out = {}
    for m in g["metrics"]:
        if m["name"] == "golden_distance" and applies(m, t["kind"]):
            out[m["name"]] = golden_distance(eval_dir, t, label, m)
    return out


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
        row.update(artifact_metrics(eval_dir, t, g, lab))
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
            bm.update(artifact_metrics(eval_dir, bt, g, bl))
            bm.update(judge_metrics(eval_dir, bt, g, results_dir / bl))
            excl = set(g.get("baseline_exclude", {}).get(bl, []))
            for k, v in bm.items():
                if isinstance(v, (int, float)) and k not in excl:
                    vals.setdefault(k, []).append(v)
        refs[kind] = vals
    # machinery check: a trial's effort must match its kind's baseline
    base_effort = {}
    for kind, spec in g["kinds"].items():
        effs = set()
        for bl in spec["baseline_labels"]:
            tj = results_dir / bl / "trial.json"
            if tj.exists():
                e = load(tj).get("effort")
                if e:
                    effs.add(e)
        base_effort[kind] = effs
    # gate decisions
    for lab, tr in trials.items():
        fails = []
        be = base_effort.get(tr["kind"], set())
        if be and tr["metrics"].get("effort") not in be and lab not in g["kinds"][tr["kind"]]["baseline_labels"]:
            fails.append(f"effort {tr['metrics'].get('effort')} vs baseline {'/'.join(sorted(be))}")
        for m in g["metrics"]:
            if not m.get("gate") or not applies(m, tr["kind"]):
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
    kinds = {tr["kind"] for tr in trials.values()}
    shown = [m for m in g["metrics"] if any(applies(m, k) for k in kinds)]
    names = [m["name"] for m in shown]
    gated = {m["name"] for m in g["metrics"] if m.get("gate")}
    head = "| trial | kind | " + " | ".join(("*" if n in gated else "") + n for n in names) + " | verdict |"
    sep = "|" + "---|" * (len(names) + 3)
    rows = [head, sep]
    for lab, tr in trials.items():
        cells = [str(tr["metrics"].get(m["name"], "")) if applies(m, tr["kind"]) else "" for m in shown]
        verdict = "baseline" if lab in sum((k["baseline_labels"] for k in g["kinds"].values()), []) else ("PASS" if not tr["fails"] else "FAIL: " + "; ".join(tr["fails"]))
        rows.append(f"| {lab} | {tr['kind']} | " + " | ".join(cells) + f" | {verdict} |")
    for kind, vals in refs.items():
        if vals and kind in kinds:
            rows.append(f"| baseline worst ({kind}) | {kind} | " + " | ".join(
                (str(max(vals[m["name"]]) if m["direction"] == "lower" else min(vals[m["name"]])) if m["name"] in vals and m["direction"] in ("lower", "higher") and applies(m, kind) else "") for m in shown) + " | |")
    return "\n".join(rows)


def set_summary(trials, prefix, g):
    members = {k: v for k, v in trials.items() if re.fullmatch(re.escape(prefix) + r"-\d+", k)}
    if not members:
        return ""
    lines = [f"\n**Set {prefix}** ({len(members)} trials): worst value per gated metric"]
    for m in g["metrics"]:
        if not m.get("gate") or m["direction"] == "pass":
            continue
        vals = [t["metrics"].get(m["name"]) for t in members.values() if applies(m, t["kind"])]
        if not vals:
            continue
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
