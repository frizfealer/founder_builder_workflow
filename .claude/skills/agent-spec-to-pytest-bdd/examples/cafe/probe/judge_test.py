"""Task 56 part 1: the message judge on the 32 messages of judge_cases.json, 3 times each.

Usage:
  uv run python probe/judge_test.py            put every case to the judge 3 times, write runs/judge-test.json, print the report
  uv run python probe/judge_test.py --report   print the report from runs/judge-test.json, no API call;
                                               exit 1 unless the pass line holds

Each case goes through the judge call the rule checkers use: harness.judge.MessageJudge over
probe.agent.judge_llm, with the question data.json holds under the case's question name. A fresh
MessageJudge per repeat, since one keeps a single answer per message and question. A reply that is
neither yes nor no is recorded as "unclear" and does not count as the expected answer.
"""
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


def result(cases, answered):
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
        "_about": "Task 56 part 1: each message of judge_cases.json put to the message judge 3 times (probe/judge_test.py). "
                  "as_expected counts the repeats that gave the case's expected answer.",
        "cases": rows,
        "pass_line": {"cases_not_hard": len(plain), "as_expected_in_2_of_3": len(ok), "needed": NEEDED,
                      "holds": len(ok) >= NEEDED},
        "not_as_expected": [{"id": r["id"], "expected": r["expected"], "answers": r["answers"]}
                            for r in plain if r not in ok],
        "hard_cases": [{"id": r["id"], "expected": r["expected"], "answers": r["answers"]} for r in rows if r["hard"]],
        "differing_repeats": [{"id": r["id"], "hard": r["hard"], "expected": r["expected"], "answers": r["answers"]}
                              for r in rows if len(set(r["answers"])) > 1],
    }


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


def run(llm=None):
    from probe.llm import LLM
    llm = llm or LLM()
    cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"]
    answered = {}
    for c in cases:
        if money.spent() >= money.STOP_AT:
            sys.exit(f"stopped before {c['id']}: {money.spent():.2f} USD spent of the task's {money.CAP} USD")
        answered[c["id"]] = ask_case(llm, c)
    res = result(cases, answered)
    OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    return res


if __name__ == "__main__":
    if sys.argv[1:] == ["--report"]:
        res = json.loads(OUT.read_text(encoding="utf-8"))
    else:
        money.use_ledger("judge test")
        res = run()
    print(report(res))
    sys.exit(0 if res["pass_line"]["holds"] else 1)
