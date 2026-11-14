#!/usr/bin/env python3
"""Calibrate the judges against a human.

  calibrate.py sample <eval-dir> --trials a,b [--n 20] [--seed 1] [--pool dropped|kept|all]
                                 [--exclude <calibration-dir>,...] [--no-recall]
      Writes <eval-dir>/calibration/<date>/worksheet.md (findings with the spec text they quote,
      judge verdicts hidden), answers.md (a form to fill), and sealed.json (the judge verdicts).
  calibrate.py score <eval-dir>/calibration/<date>
      Reads answers.md, compares with sealed.json, prints agreement and where it breaks.

Sample mix (--pool all, the default): ~40 % kept Important, ~30 % kept Nit, ~30 % dropped, split
across the trials given, plus 5 recall matches to confirm. --pool dropped (or kept) draws only from
that pool; --exclude skips findings already sealed in earlier calibration folders; --no-recall
omits the recall matches. Findings are drawn deterministically from the seed so the
worksheet can be regenerated.
"""
import json
import random
import re
import sys
from datetime import date
from pathlib import Path


def load(p):
    return json.loads(Path(p).read_text())


sys.path.insert(0, str(Path(__file__).resolve().parent))
from grade import blind_finding_text as finding_text  # same cut the judge gets: finding only, no refutation

def spec_excerpt(folder, quote, rnd, width=10):
    """±width lines around the first line of the quote in the spec snapshot the finding read."""
    snap = folder / "rounds" / f"round{max(rnd - 1, 0)}-agent-spec.md"
    if not snap.exists() or not quote:
        return None, snap.name
    needle = re.sub(r"\s+", " ", quote.strip().strip('"').split("\n")[0])[:60]
    lines = snap.read_text().splitlines()
    for i, l in enumerate(lines):
        if needle and needle[:40] in re.sub(r"\s+", " ", l):
            lo, hi = max(0, i - width), min(len(lines), i + width + 1)
            return "\n".join(f"{n + 1:5d}  {lines[n]}" for n in range(lo, hi)), f"{snap.name} lines {lo + 1}-{hi}"
    return None, snap.name


def sample(eval_dir, trials, n, seed, which="all", exclude=(), with_recall=True):
    rnd = random.Random(seed)
    seen = set()
    for ex in exclude:
        for v in load(Path(ex) / "sealed.json").get("findings", {}).values():
            seen.add((v["trial"], v["id"]))
    pool = {"kept_important": [], "kept_nit": [], "dropped": []}
    recall = []
    for lab in trials:
        folder = eval_dir / "results" / lab
        t = load(folder / "trial.json")
        for f in t["findings"]:
            if (lab, f["id"]) in seen:
                continue
            if f.get("kept") is True and f.get("severity") == "Important":
                pool["kept_important"].append((lab, f))
            elif f.get("kept") is True:
                pool["kept_nit"].append((lab, f))
            elif f.get("kept") is False:
                pool["dropped"].append((lab, f))
        rk = folder / "judge" / "recall_key.verdict.json"
        if rk.exists():
            for key_id, match in load(rk).get("matches", {}).items():
                if match:
                    recall.append((lab, key_id, match))
    if which == "dropped":
        quota = {"kept_important": 0, "kept_nit": 0, "dropped": n}
    elif which == "kept":
        quota = {"kept_important": round(n * 0.6), "kept_nit": 0, "dropped": 0}
        quota["kept_nit"] = n - quota["kept_important"]
    else:
        quota = {"kept_important": round(n * 0.4), "kept_nit": round(n * 0.3)}
        quota["dropped"] = n - quota["kept_important"] - quota["kept_nit"]
    picked = []
    for k, q in quota.items():
        items = pool[k][:]
        rnd.shuffle(items)
        picked += [(k, lab, f) for lab, f in items[:q]]
    rnd.shuffle(picked)
    rnd.shuffle(recall)
    recall = recall[:5] if with_recall else []

    sealed = {"findings": {}, "recall": {}}
    ws = ["# Calibration worksheet", "",
          f"Trials: {', '.join(trials)}. {len(picked)} findings + {len(recall)} recall matches. Rule each one WITHOUT opening any judge/ file.", "",
          "For each finding, read its Quote, Evidence and Pattern, then the spec excerpt (the text the finder saw). Rule:",
          "- **Real** — the defect exists as described and belongs to its class.",
          "- **Not real** — the spec or the inputs refute it; note what refutes it.",
          "- **Style only** — wording or preference; changes no verdict and no agent behavior.",
          "", "Write your rulings in `answers.md`. Then run `calibrate.py score <this folder>`.", ""]
    ans = ["# Answers", "", "One line per item: `<item> | Real|Not real|Style only | <one line why>`", "",
           "## Findings", ""]
    for i, (k, lab, f) in enumerate(picked, 1):
        folder = eval_dir / "results" / lab
        text = finding_text(folder, f["id"], f["round"])
        exc, where = spec_excerpt(folder, f.get("quote", ""), f["round"])
        ws += [f"## F{i} — {lab} {f['id']} (round {f['round']}, {f.get('severity')})", "",
               "```", text or f"{f['id']} | {f.get('class')} | {f.get('severity')} | {f.get('location')}\nQuote: {f.get('quote')}", "```", "",
               f"Spec the finder read: `results/{lab}/rounds/round{max(f['round'] - 1, 0)}-agent-spec.md`" + (f" ({where})" if exc else " — quote not located by text search; open the file at the finding's location") , ""]
        if exc:
            ws += ["```", exc, "```", ""]
        ans.append(f"F{i} | | ")
        # the judge's view, sealed
        jf = folder / "judge" / ("false_positives.verdict.json" if f.get("kept") else "dropped_real.verdict.json")
        jv = load(jf).get("verdicts", {}).get(f["id"]) if jf.exists() else None
        je = load(jf).get("evidence", {}).get(f["id"]) if jf.exists() else None
        sealed["findings"][f"F{i}"] = {"trial": lab, "id": f["id"], "pool": k, "skill_decision": "kept" if f.get("kept") else "dropped",
                                        "judge": jv, "judge_evidence": je}
    ws += ["## Recall matches", "", "The judge says the trial finding reports the SAME defect in the SAME block as the key item. Agree or not?", ""]
    ans += ["", "## Recall matches", "", "One line per item: `<item> | same|different | <one line why>`", ""]
    g = load(eval_dir / "grading.json")
    for i, (lab, key_id, match) in enumerate(recall, 1):
        kind = load(eval_dir / "results" / lab / "trial.json")["kind"]
        keyfile = eval_dir / g["key"][kind]["file"]
        ktext = ""
        if keyfile.exists():
            kl = keyfile.read_text().splitlines()
            s = next((j for j, l in enumerate(kl) if re.match(r"^(?:##\s*)?" + re.escape(key_id) + r"\s*\|", l)), None)
            if s is not None:
                ktext = "\n".join(kl[s:s + 5])
        folder = eval_dir / "results" / lab
        mf = next((f for f in load(folder / "trial.json")["findings"] if f["id"] == match), {})
        ws += [f"## R{i} — key {key_id} vs {lab} {match}", "", "Key item:", "```", ktext or "(not found)", "```",
               "Trial finding:", "```", finding_text(folder, match, mf.get("round", 1)) or f"{match}: {mf.get('location')} / {mf.get('quote')}", "```", ""]
        ans.append(f"R{i} | | ")
        sealed["recall"][f"R{i}"] = {"trial": lab, "key": key_id, "match": match}
    out = eval_dir / "calibration" / date.today().isoformat()
    out.mkdir(parents=True, exist_ok=True)
    (out / "worksheet.md").write_text("\n".join(ws) + "\n")
    (out / "answers.md").write_text("\n".join(ans) + "\n")
    (out / "sealed.json").write_text(json.dumps(sealed, indent=1))
    print(f"wrote {out}/worksheet.md ({len(picked)} findings, {len(recall)} recall matches), answers.md, sealed.json")
    print("pool sizes available:", {k: len(v) for k, v in pool.items()})


def norm(v):
    v = (v or "").strip().lower()
    return {"real": "Real", "not real": "Not real", "style only": "Style only", "style": "Style only",
            "same": "same", "different": "different"}.get(v, v)


def score(folder):
    folder = Path(folder)
    sealed = load(folder / "sealed.json")
    answers = {}
    for l in (folder / "answers.md").read_text().splitlines():
        m = re.match(r"^([FR]\d+)\s*\|\s*(.*)$", l)
        if m and m.group(2).strip():
            rest = m.group(2)
            # ruling = the first recognised word; everything after it is the note
            rm = re.match(r"\s*(not real|style only|style|real|same|different)\b[\s\u258e|.,:-]*(.*)$", rest, re.I)
            if rm:
                answers[m.group(1)] = (norm(rm.group(1)), rm.group(2).strip())
    rows, agree, total = [], 0, 0
    by_pool = {}
    for item, s in sealed["findings"].items():
        if item not in answers:
            continue
        human, why = answers[item]
        judge = norm(s["judge"])
        # the judge's Real/Not real on a dropped finding vs the human's: compare directly
        ok = human == judge
        # the metrics treat Not real and Style only alike (neither should be kept)
        same_bucket = (human == "Real") == (judge == "Real")
        total += 1; agree += same_bucket
        by_pool.setdefault(s["pool"], [0, 0]); by_pool[s["pool"]][0] += ok; by_pool[s["pool"]][1] += 1
        rows.append(f"| {item} | {s['trial']} {s['id']} | {s['skill_decision']} | {judge} | {human} | {'✓' if same_bucket else ('~' if ok else '✗')} | {why[:60]} |")
    r_agree = r_total = 0
    for item, s in sealed["recall"].items():
        if item not in answers:
            continue
        human, why = answers[item]
        ok = human == "same"
        r_total += 1; r_agree += ok
        rows.append(f"| {item} | {s['trial']} {s['match']}→{s['key']} | match | same | {human} | {'✓' if ok else '✗'} | {why[:60]} |")
    print("Agreement is on the metric's bucket: Real vs (Not real | Style only). '~' = same bucket, different label.")
    print("| item | finding | skill | judge | you | agree | your note |")
    print("|---|---|---|---|---|---|---|")
    print("\n".join(rows))
    if total:
        print(f"\nFindings: {agree}/{total} agree ({agree / total:.0%}). By pool: " + ", ".join(f"{k} {a}/{n}" for k, (a, n) in by_pool.items()))
    if r_total:
        print(f"Recall matches: {r_agree}/{r_total} you call the same defect.")
    if total and agree / total >= 0.9:
        print("\nVerdict: judges agree with you at or above 90 %; the table's judge metrics are trustworthy. Record the rate in EXPERIMENTS.md and move on.")
    elif total:
        print("\nVerdict: below 90 %. Look at the ✗ rows: if they cluster on one ruling (e.g. judge says Style only where you say Real), fix that rule in the judge task text and re-judge the affected metric; if they scatter, sample 20 more before changing anything.")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("sample", "score"):
        print(__doc__); sys.exit(2)
    if a[0] == "sample":
        eval_dir = Path(a[1]).resolve()
        trials = a[a.index("--trials") + 1].split(",")
        n = int(a[a.index("--n") + 1]) if "--n" in a else 20
        seed = int(a[a.index("--seed") + 1]) if "--seed" in a else 1
        which = a[a.index("--pool") + 1] if "--pool" in a else "all"
        exclude = a[a.index("--exclude") + 1].split(",") if "--exclude" in a else []
        sample(eval_dir, trials, n, seed, which, exclude, "--no-recall" not in a)
    else:
        score(a[1])
