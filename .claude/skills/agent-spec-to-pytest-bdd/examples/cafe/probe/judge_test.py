"""Task 56 part 1: the message judge on the 32 messages of judge_cases.json, 3 times each.

Usage:
  uv run python probe/judge_test.py            put every case to the judge 3 times, write runs/judge-test.json, print the report
  uv run python probe/judge_test.py --report   print the report from runs/judge-test.json, no API call;
                                               exit 1, naming the case, when a case there differs from
                                               judge_cases.json or lacks its 3 answers, and exit 1 unless
                                               the pass line holds

Another cases file (task 51: slice B's judge_cases_b.json) is given with its own result file, pass line and
ledger, so the defaults above keep task 56's files as they are:
  uv run python probe/judge_test.py --cases judge_cases_b.json --out runs/judge-test-b.json --needed 17 \
      --ledger runs/task-051-usage.jsonl --stop-at 0.45 [--report]

Each case goes through the judge call the rule checkers use: harness.judge.MessageJudge over
probe.agent.judge_llm, with the question data.json holds under the case's question name. A fresh
MessageJudge per repeat, since one keeps a single answer per message and question. A reply that is
neither yes nor no is recorded as "unclear" and does not count as the expected answer.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from harness.judge import MessageJudge, Unclear, known_sentences, question_text  # noqa: E402
from probe import money  # noqa: E402
from probe.agent import judge_llm  # noqa: E402

CASES = HERE / "judge_cases.json"
OUT = HERE / "runs" / "judge-test.json"
REPEATS = 3
AT_LEAST = 2  # repeats that must give the expected answer
NEEDED = 28  # of the cases not marked hard, answered as expected in at least 2 of their 3 repeats
WORD = {True: "yes", False: "no", None: "unclear"}


def ask_case(llm, case):
    """The 3 answers and replies of one case."""
    assert case["message"] not in known_sentences(), f"{case['id']} would be answered from data.json, not by the LLM"
    answers, replies = [], []
    for _ in range(REPEATS):
        judge = MessageJudge(judge_llm(llm))
        try:
            answers.append(WORD[judge(case["message"], case["question"])])
        except Unclear:
            answers.append(WORD[None])
        replies.append(judge.asked[-1]["reply"])
    return answers, replies


def result(cases, answered, needed=NEEDED, about="Task 56 part 1: each message of judge_cases.json"):
    """The result file's content from the cases and {case id: (answers, replies)}."""
    rows = []
    for c in cases:
        answers, replies = answered[c["id"]]
        rows.append({"id": c["id"], "question": c["question"], "hard": c["hard"], "expected": c["expected"],
                     "answers": answers, "replies": replies,
                     "as_expected": sum(a == c["expected"] for a in answers),
                     "message": c["message"], "question_text": question_text(c["question"])})
    plain = [r for r in rows if not r["hard"]]
    ok = [r for r in plain if r["as_expected"] >= AT_LEAST]
    return {
        "_about": f"{about} put to the message judge 3 times (probe/judge_test.py). "
                  "as_expected counts the repeats that gave the case's expected answer.",
        "cases": rows,
        "pass_line": {"cases_not_hard": len(plain), "as_expected_in_2_of_3": len(ok), "needed": needed,
                      "holds": len(ok) >= needed},
        "not_as_expected": [{"id": r["id"], "expected": r["expected"], "answers": r["answers"]}
                            for r in plain if r not in ok],
        "hard_cases": [{"id": r["id"], "expected": r["expected"], "answers": r["answers"]} for r in rows if r["hard"]],
        "differing_repeats": [{"id": r["id"], "hard": r["hard"], "expected": r["expected"], "answers": r["answers"]}
                              for r in rows if len(set(r["answers"])) > 1],
    }


def mismatches(cases, res):
    """What of the result file does not match the cases: a case differing in id, message, question, expected
    or hard, a case without its 3 answers, or a case missing on either side."""
    out = []
    rows = res["cases"]
    for k, (c, r) in enumerate(zip(cases, rows)):
        differ = [f for f in ("id", "message", "question", "expected", "hard") if c[f] != r.get(f)]
        if differ:
            out.append(f"case {k + 1} ({c['id']}): the result differs from judge_cases.json in {', '.join(differ)}")
        if len(r.get("answers", [])) != REPEATS:
            out.append(f"case {k + 1} ({c['id']}): {len(r.get('answers', []))} answers, not {REPEATS}")
    out += [f"case {c['id']}: not in the result file" for c in cases[len(rows):]]
    out += [f"case {r.get('id')}: in the result file, not in judge_cases.json" for r in rows[len(cases):]]
    return out


def report(res):
    p = res["pass_line"]
    lines = [f"{r['id']} {r['question']:<16} expected {r['expected']:<3} answers {' '.join(r['answers'])}"
             f"{'  (hard)' if r['hard'] else ''}" for r in res["cases"]]
    lines += [f"PASS LINE: {p['as_expected_in_2_of_3']} of the {p['cases_not_hard']} cases not marked hard are answered "
              f"as expected in at least 2 of 3 repeats; needed {p['needed']} -> {'HOLDS' if p['holds'] else 'DOES NOT HOLD'}",
              "not answered as expected (not hard): " + (", ".join(
                  f"{r['id']} (expected {r['expected']}, got {' '.join(r['answers'])})" for r in res["not_as_expected"]) or "none"),
              "hard cases: " + ", ".join(f"{r['id']} (expected {r['expected']}, got {' '.join(r['answers'])})"
                                         for r in res["hard_cases"]),
              "cases with differing repeats: " + (", ".join(
                  f"{r['id']} ({' '.join(r['answers'])})" for r in res["differing_repeats"]) or "none")]
    return "\n".join(lines)


def run(llm=None, cases_file=None, out=None, needed=NEEDED, ledger=None, stop_at=None):
    from probe.llm import LLM
    llm = llm or LLM()
    cases_file, out, stop_at = cases_file or CASES, out or OUT, money.STOP_AT if stop_at is None else stop_at
    cases = json.loads(cases_file.read_text(encoding="utf-8"))["cases"]
    answered = {}
    for c in cases:
        if money.spent(ledger) >= stop_at:
            sys.exit(f"stopped before {c['id']}: {money.spent(ledger):.2f} USD spent, the stop is at {stop_at} USD")
        answered[c["id"]] = ask_case(llm, c)
    about = "Task 56 part 1: each message of judge_cases.json" if cases_file == CASES else \
        f"Each message of {cases_file.name}"
    res = result(cases, answered, needed, about)
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    return res


def main(args):
    p = argparse.ArgumentParser(description="the message judge on a cases file, 3 times each")
    p.add_argument("--report", action="store_true", help="report from the saved result file, no API call")
    p.add_argument("--cases", type=Path, default=CASES, help="the cases file (default judge_cases.json)")
    p.add_argument("--out", type=Path, default=OUT, help="the result file (default runs/judge-test.json)")
    p.add_argument("--needed", type=int, default=NEEDED, help="cases not marked hard that must pass the 2 of 3")
    p.add_argument("--ledger", type=Path, help="the usage ledger the calls are counted in (default task 56's, "
                                               "only with the default cases file; required with another)")
    p.add_argument("--stop-at", type=float, default=money.STOP_AT, help="USD in the ledger at which no case starts")
    a = p.parse_args(args)
    cases_file, out = (x if x.is_absolute() else HERE / x for x in (a.cases, a.out))
    if a.ledger is None and cases_file != CASES and not a.report:
        p.error("--ledger is required with a cases file other than judge_cases.json, so its calls stay out of "
                "task 56's ledger")
    ledger = money.LEDGER if a.ledger is None else a.ledger if a.ledger.is_absolute() else HERE / a.ledger
    if a.report:
        res = json.loads(out.read_text(encoding="utf-8"))
        bad = mismatches(json.loads(cases_file.read_text(encoding="utf-8"))["cases"], res)
        if bad:
            print("\n".join(bad))
            sys.exit(1)
    else:
        money.use_ledger("judge test", ledger)
        res = run(cases_file=cases_file, out=out, needed=a.needed, ledger=ledger, stop_at=a.stop_at)
    print(report(res))
    sys.exit(0 if res["pass_line"]["holds"] else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
