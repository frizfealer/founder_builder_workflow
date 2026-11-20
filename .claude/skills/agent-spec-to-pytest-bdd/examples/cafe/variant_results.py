"""Slice C's results: what the rule checkers make of the broken variants of harness/agents.py.

Usage:
  uv run python variant_results.py           write variant_results.json
  uv run python variant_results.py --check   exit 1 when a rerun of the variants differs from the file

For each slice C variant and each scenario with World lines (SC-01 to SC-16) it runs the scenario as the
feature file does, with no LLM (a message the data file lacks raises), and records whether the variant's
events differ from the reference agent's, the verdict of every rule that has a checker, and the status the
scenario's test would get. Each variant then gets one outcome:
  caught                          its own rule's verdict is a break in at least one scenario
  caught only by another rule     no break of its own rule, a break of another rule somewhere
  survived                        every scenario's test passes
A variant with none of these three (no rule breaks anywhere, yet a test ends without a verdict) stops the
script: task 51's done_means line 4 names no outcome for it, and no variant has it.
For a variant not caught, the words of its rule that went unchecked, and whether unchecked_sentences.json
already lists them: a heuristic string-search of that file, made here so that its content need not be read.
A variant with a note below gets it in the file.
"""
import json
import re
import sys

from harness.agents import SLICE_C, ReferenceAgent
from harness.checkers import BREAKS, CHECKERS, UNDECIDED, verdict
from harness.data import HERE, scenario, world_scenarios
from harness.fake import FakeBookingSystem
from harness.judge import MessageJudge, known_sentences
from harness.slot import Driver, world_line

RESULTS = HERE / "variant_results.json"
UNCHECKED = HERE / "unchecked_sentences.json"
SCENARIOS = world_scenarios()
OUTCOMES = ("caught", "caught only by another rule", "survived")
NOTES = {
    "break-R-04-message": "R-04's message half is reached in no scenario: R-04's 'asks again' follows a changed "
                          "table held, no scenario has one, and there the reference agent stops the test. This "
                          "variant sits at a failed release instead, where the reference agent does not ask again "
                          "either but says release_failed (rules.md's R-06 row). What it changes is that it "
                          "re-proposes the unchanged table instead of saying the release failed; R-01 caught that.",
}


def run(sc_id, agent):
    """The scenario's run from the start, as the step functions make it: Given, the When lines, the agent."""
    first, *rest = scenario(sc_id)["world"]
    system = FakeBookingSystem()
    system.start(table_free=first == "The table is free")
    return Driver([world_line(line) for line in rest], system, agent).run()


def judged(sc_id, agent):
    """One scenario: the events, every rule's verdict and the test's status, as conftest.py's outcome makes them."""
    try:
        r = run(sc_id, agent)
    except Exception as e:  # a variant with no step here; the test of the scenario errors
        return {"events": None, "status": "error", "error": f"{type(e).__name__}: {e}", "verdicts": {}}
    judge = MessageJudge()
    verdicts = {rule: verdict(rule, r.events, r.over, judge)["verdict"] for rule in sorted(CHECKERS)}
    played_out = r.over and r.played == r.lines
    if BREAKS in verdicts.values():
        status = "fail"
    elif UNDECIDED in verdicts.values() or not played_out:
        status = "no verdict"
    else:
        status = "pass"
    known = known_sentences()
    unlabelled = [e["text"] for e in r.events if e["kind"] == "message" and e["text"] not in known]
    return {"events": r.events, "status": status, "played_out": played_out, "verdicts": verdicts,
            "unlabelled_sentences": unlabelled, "llm_calls": judge.llm_calls()}


def norm(text):
    return re.sub(r"\s+", " ", text.replace("“", '"').replace("”", '"').replace("’", "'")).strip().lower()


def strings(x):
    if isinstance(x, dict):
        return [s for k, v in x.items() for s in [k, *strings(v)]]
    if isinstance(x, list):
        return [s for v in x for s in strings(v)]
    return [x] if isinstance(x, str) else []


def listed(words):
    """Whether unchecked_sentences.json lists these words of a rule: they are inside one of its strings, or one
    of its strings of 3 or more words is inside them. Only the answer is kept, not the file's text."""
    found = [norm(s) for s in strings(json.loads(UNCHECKED.read_text(encoding="utf-8")))]
    q = norm(words)
    if any(q in s for s in found):
        return "yes: the words are inside a string of the file"
    if any(len(s.split()) >= 3 and s in q for s in found):
        return "yes: a string of the file is inside the words"
    return "no"


def results():
    reference = {sc: judged(sc, ReferenceAgent())["events"] for sc in SCENARIOS}
    variants = {}
    for cls in SLICE_C:
        per = {}
        for sc in SCENARIOS:
            j = judged(sc, cls())
            per[sc] = {"differs": j["events"] != reference[sc], "status": j["status"], "verdicts": j["verdicts"]}
            if j["status"] == "error":
                per[sc]["error"] = j["error"]
            else:
                per[sc] |= {"played_out": j["played_out"], "unlabelled_sentences": j["unlabelled_sentences"],
                            "llm_calls": j["llm_calls"]}
        broken = sorted({r for s in per.values() for r, v in s["verdicts"].items() if v == BREAKS})
        if cls.rule in broken:
            outcome = "caught"
        elif broken:
            outcome = "caught only by another rule"
        else:
            assert all(s["status"] == "pass" for s in per.values()), \
                f"{cls.name}: no rule breaks, yet a test ends without a verdict; line 4 has no outcome for it"
            outcome = "survived"
        v = {"rule": cls.rule, "fault": cls.fault, "breaks": cls.breaks, "outcome": outcome, "broken_rules": broken,
             "differs_in": [sc for sc, s in per.items() if s["differs"]],
             "failing_tests": [sc for sc, s in per.items() if s["status"] != "pass"]}
        if outcome != "caught":
            v["unchecked"] = {"rule": cls.rule, "words": cls.breaks, "listed_in_unchecked_sentences": listed(cls.breaks)}
        if cls.name in NOTES:
            v["note"] = NOTES[cls.name]
        variants[cls.name] = v | {"scenarios": per}
    counts = {o: sum(1 for v in variants.values() if v["outcome"] == o) for o in OUTCOMES}
    return {"_about": "Written by variant_results.py; tests/test_slice_c.py fails when a rerun differs. "
                      "Per slice C variant and scenario: whether its events differ from the reference agent's, "
                      "every rule's verdict, the test's status; per variant its outcome.",
            "counts": counts, "variants": variants}


def text():
    return json.dumps(results(), indent=1, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    if sys.argv[1:] == ["--check"]:
        same = RESULTS.exists() and RESULTS.read_text(encoding="utf-8") == text()
        print("variant_results.json equals a rerun" if same else "variant_results.json differs from a rerun")
        sys.exit(0 if same else 1)
    RESULTS.write_text(text(), encoding="utf-8")
    print(json.dumps(results()["counts"]))
