"""Task 56's money: every Claude API call the task makes, from one ledger, against one cap.

Usage:
  uv run python probe/money.py     write runs/task-056-money.json from the ledger and print it

probe/judge_test.py and probe/run_probe2.py set CAFE_USAGE_LEDGER to LEDGER, for themselves and for each
pytest they start, so probe/llm.py appends every call's usage there, first tries and runs that raised
included. A call made any other way for this task must be run with the same variable set.
"""
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from probe.llm import GRADING, MODEL, RATES_KEY, cost, rates  # noqa: E402

LEDGER = HERE / "runs" / "task-056-usage.jsonl"
SUMMARY = HERE / "runs" / "task-056-money.json"
CAP = 2.0
STOP_AT = 1.8  # leaves room for the call or run in flight


def use_ledger(source, ledger=None):
    """Send this process's calls, and those of every process it starts, to the ledger, tagged with source."""
    os.environ["CAFE_USAGE_LEDGER"] = str(ledger or LEDGER)
    os.environ["CAFE_USAGE_SOURCE"] = source


def calls(ledger=None):
    path = Path(ledger or LEDGER)
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] \
        if path.exists() else []


def spent(ledger=None):
    return cost(calls(ledger))


def summary(ledger=None, out=None):
    """The money of a ledger, written to out (default SUMMARY), its text naming that ledger, and the task of a
    ledger named task-<id>-usage.jsonl."""
    path = Path(ledger or LEDGER).resolve()
    task = re.fullmatch(r"task-(\d+)-usage\.jsonl", path.name)
    shown = path.relative_to(HERE) if path.is_relative_to(HERE) else path
    writers = "every call of probe/judge_test.py and probe/run_probe2.py appends to" if path == Path(LEDGER).resolve() \
        else "the calls made with CAFE_USAGE_LEDGER set to it append to"
    about = f"All that task {int(task[1])} spent on the Claude API, from the ledger {shown}, which {writers}." \
        if task else f"The Claude API spend recorded in the ledger {shown}, which {writers}."
    rows = calls(path)
    by = {}
    for c in rows:
        by.setdefault(c["source"] or "untagged", []).append(c)
    s = {"_about": about,
         "model": MODEL, "usd": round(cost(rows), 4), "cap_usd": CAP, "api_calls": len(rows),
         "by_source": {k: {"api_calls": len(v), "usd": round(cost(v), 4)} for k, v in sorted(by.items())},
         "input_tokens": sum(c["input_tokens"] for c in rows),
         "output_tokens": sum(c["output_tokens"] for c in rows),
         "rates_usd_per_million": rates(), "rates_from": f"{GRADING.relative_to(HERE.parents[4])} model_rates.{RATES_KEY}"}
    Path(out or SUMMARY).write_text(json.dumps(s, indent=1) + "\n")
    return s


if __name__ == "__main__":
    print(json.dumps(summary(), indent=1))
