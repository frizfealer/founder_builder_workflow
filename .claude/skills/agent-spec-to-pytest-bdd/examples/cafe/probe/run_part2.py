"""Part 2 of slice A: the probe agent through the feature files, 27 one-action runs and 9 whole conversations.

Usage:
  uv run python probe/run_part2.py             run what is not run yet, then write the summary
  uv run python probe/run_part2.py --summary   only write and print the summary

Each run is one `pytest tests/test_scenarios.py --agent probe ...`, so the probe goes through the same
step functions and checkers as the reference agent. Transcripts go to runs/part2/transcripts/ and
verdicts to runs/part2/verdicts/. The one-action runs get shuffled ids (run-01 to run-27) so a labeller
reading transcripts sees neither the prompt nor the verdict; verdicts/index.json maps each id back.
Stops before a run once the money spent reaches STOP_AT, and at the first run the API refuses.
"""
import json
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from harness.data import data  # noqa: E402
from probe.llm import GRADING, MODEL, RATES_KEY, cost, rates  # noqa: E402

OUT = HERE / "runs" / "part2"
CAP = 5.0
STOP_AT = 4.5  # leaves room for the run in flight
RUNS_PER_CASE = 3
BAD_AT = {"retry": ("M5", "R-11"), "book-when-held": ("M2", "R-03")}


def plan():
    """[(run id, moment, prompt)]: 7 moments x 3 plain, 2 bad prompts x 3 at their moment, then 3 x the 3 scenarios."""
    moments = [m for m in data()["moments"] if not m.startswith("_")]
    one = [(m, "plain") for m in moments for _ in range(RUNS_PER_CASE)]
    one += [(m, p) for p, (m, _) in BAD_AT.items() for _ in range(RUNS_PER_CASE)]
    random.Random(49).shuffle(one)
    runs = [(f"run-{i:02d}", m, p) for i, (m, p) in enumerate(one, 1)]
    return runs + [(f"conv-{k}", "start", "plain") for k in range(1, RUNS_PER_CASE + 1)]


def verdicts():
    return [json.loads(p.read_text()) for p in sorted((OUT / "verdicts").glob("*.json"))
            if p.name not in ("index.json", "summary.json", "preflight-usage.json")]


def preflight_usage():
    pre = OUT / "verdicts" / "preflight-usage.json"
    return json.loads(pre.read_text()) if pre.exists() else []


def spent():
    return cost([u for v in verdicts() for u in v.get("usage", [])] + preflight_usage())


def preflight():
    """One tiny call, so a missing login or credit stops the run before any test starts."""
    from probe.llm import LLM
    llm = LLM()
    llm.create("preflight", max_tokens=1, messages=[{"role": "user", "content": "ok"}])
    return llm.calls


def run_all():
    (OUT / "verdicts").mkdir(parents=True, exist_ok=True)
    index = {rid: {"moment": m, "prompt": p} for rid, m, p in plan()}
    (OUT / "verdicts" / "index.json").write_text(json.dumps(index, indent=1))
    pre = OUT / "verdicts" / "preflight-usage.json"
    if not pre.exists():
        pre.write_text(json.dumps(preflight(), indent=1))
    for rid, m, p in plan():
        done = (OUT / "verdicts" / f"{rid}.json").exists() or list((OUT / "verdicts").glob(f"{rid}-SC-*.json"))
        if done:
            continue
        if spent() >= STOP_AT:
            print(f"stopped before {rid}: {spent():.2f} USD spent")
            break
        cmd = [sys.executable, "-m", "pytest", "tests/test_scenarios.py", "-q", "-p", "no:cacheprovider",
               "--agent", "probe", "--from", m, "--prompt", p, "--out", str(OUT), "--run-id", rid]
        proc = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
        written = [v for v in verdicts() if v["run_id"] == rid or v["run_id"].startswith(f"{rid}-")]
        print(f"{rid} {m} {p}: {[v['status'] for v in written]}  spent {spent():.3f} USD")
        errors = [v for v in written if v["status"] == "error"]
        if errors or not written:
            print(proc.stdout[-3000:])
            print("stopped: a run raised (see above)")
            break


def summary():
    vs = verdicts()
    usage = [u for v in vs for u in v.get("usage", [])] + preflight_usage()
    one = [v for v in vs if v["run_id"].startswith("run-")]
    whole = [v for v in vs if v["run_id"].startswith("conv-")]

    def per_rule(rows):
        out = {}
        for v in rows:
            for r, x in v["rules"].items():
                c = out.setdefault(r, {"holds": 0, "breaks": 0, "undecided": 0})
                c[x["verdict"]] += 1
        for c in out.values():
            judged = c["holds"] + c["breaks"]
            c["pass_rate"] = round(c["holds"] / judged, 3) if judged else None
        return dict(sorted(out.items()))

    bad = {}
    for p, (m, rule) in BAD_AT.items():
        rows = [v for v in one if v["prompt"] == p]
        bad[p] = {"moment": m, "rule": rule, "runs": len(rows),
                  "failed_on_its_rule": sorted(v["run_id"] for v in rows if v["rules"][rule]["verdict"] == "breaks")}
    s = {
        "model": MODEL,
        "one_action_runs": {"planned": 27, "run": len(one),
                            "reached_a_verdict": sum(v["status"] in ("pass", "fail") for v in one),
                            "status": {k: sum(v["status"] == k for v in one) for k in ("pass", "fail", "no verdict", "error")},
                            "pass_rate_per_rule": per_rule(one)},
        "whole_conversations": {"planned": 9, "run": len(whole),
                                "reached_a_verdict": sum(v["status"] in ("pass", "fail") for v in whole),
                                "status": {k: sum(v["status"] == k for v in whole) for k in ("pass", "fail", "no verdict", "error")},
                                "pass_rate_per_rule": per_rule(whole)},
        "bad_prompts_checker_side": bad,
        "money": {"usd": round(cost(usage), 4), "cap_usd": CAP, "api_calls": len(usage),
                  "input_tokens": sum(u["input_tokens"] for u in usage),
                  "output_tokens": sum(u["output_tokens"] for u in usage),
                  "cache_read_input_tokens": sum(u["cache_read_input_tokens"] for u in usage),
                  "cache_creation_input_tokens": sum(u["cache_creation_input_tokens"] for u in usage),
                  "rates_usd_per_million": rates(),
                  "rates_from": f"{GRADING.relative_to(HERE.parents[4])} model_rates.{RATES_KEY}"},
    }
    (OUT / "verdicts" / "summary.json").write_text(json.dumps(s, indent=1))
    print(json.dumps(s, indent=1))


if __name__ == "__main__":
    if "--summary" not in sys.argv[1:]:
        run_all()
    summary()
