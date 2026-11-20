"""Slice C: broken variants written without the rule checkers, and what the checkers make of them.

Lines 1 to 5 of task 51's done_means:
1. at least 14 new variants: one per rule a feature file cites, and a call variant and a message variant for
   R-02, R-04, R-10 and R-11, each docstring naming its rule, quoting it and saying call or message;
2. every variant runs through the 16 feature files with no LLM call, saying only data.json's sentences;
3. variant_results.json equals a rerun, and every variant differs from the reference agent somewhere;
4. every variant has one outcome, and one not caught quotes the unchecked words and says whether
   unchecked_sentences.json lists them;
5. the variants' code imports nothing from harness/checkers.py or tests/test_slice_b.py.
"""
import ast
import json
import subprocess
import sys

import pytest

import variant_results
from harness import agents
from harness.agents import AGENTS, SLICE_C
from harness.data import HERE, render, rule_text, scenario, values, world_scenarios
from harness.judge import known_sentences

SLICE_A = {"break-R-03", "break-R-11"}
TWO_HALVES = {"R-02", "R-04", "R-10", "R-11"}  # rules whose text asks for a tool call and a message
OUTCOMES = {"caught", "caught only by another rule", "survived"}  # line 4's three


def squash(text):
    return " ".join(text.split())


def saved():
    return json.loads(variant_results.RESULTS.read_text(encoding="utf-8"))


def says(name, sc_id):
    """The messages of a variant's run of a scenario, with the data file's judge answers of each."""
    run = variant_results.run(sc_id, AGENTS[name]())
    return [(e["text"], known_sentences()[e["text"]]) for e in run.events if e["kind"] == "message"]


# ---------------------------------------------------------------------- line 1


def test_list_variants_cover_every_cited_rule():
    """Should have a new variant for each of the 10 rules a feature file cites, a call and a message variant
    for each rule that asks for both, 14 or more in all, none of them slice A's."""
    cited = {r for sc in world_scenarios() for r in scenario(sc)["rules"]}
    assert cited == {f"R-{i:02d}" for i in range(1, 12)} - {"R-08"}
    names = [c.name for c in SLICE_C]
    assert len(names) == len(set(names)) >= 14 and not SLICE_A & set(names)
    assert {c.rule for c in SLICE_C} == cited
    for rule in TWO_HALVES:
        assert {c.fault for c in SLICE_C if c.rule == rule} == {"call", "message"}, rule
    assert {c.fault for c in SLICE_C} == {"call", "message"}
    assert set(AGENTS) == {"reference", *SLICE_A, *names}


def test_check_variant_docstrings_name_rule_quote_fault():
    """Should find each variant's docstring naming its rule, quoting words of that rule's text and saying
    whether its fault is in a call or a message."""
    for c in SLICE_C:
        doc = squash(c.__doc__)
        assert doc.startswith(f"Breaks {c.rule}, a {c.fault} fault:"), c.name
        assert squash(c.breaks) in doc, c.name
        assert squash(c.breaks) in squash(rule_text(c.rule)), c.name


def test_run_variant_says_booked_after_no_answer():
    """Should find the R-09 message variant saying the table is booked after a booking call with no answer."""
    for sc in ("SC-12", "SC-13"):
        (text, judge), = says("break-R-09-message", sc)[1:]
        assert judge["says_booked"], text


def test_run_variant_reports_booking_without_id():
    """Should find the R-05 message variant saying the table is booked without its confirmation id."""
    (text, judge), = says("break-R-05-message", "SC-08")[1:]
    assert judge["says_booked"] and not any(c in text for c in values()["confirmation_ids"])


def test_run_variant_says_unknown_without_asking_to_call():
    """Should find the R-11 message variant saying the booking is unknown without asking the visitor to call."""
    for sc in ("SC-12", "SC-13"):
        (text, judge), = says("break-R-11-message", sc)[1:]
        assert judge["says_unknown"] and not judge["asks_call"], text


# ---------------------------------------------------------------------- line 2


@pytest.mark.parametrize("name", [c.name for c in SLICE_C])
def test_run_features_variant_all_scenarios_without_llm(tmp_path, name):
    """Should run the variant through all 16 feature files with no LLM call, every message judged from the
    data file, each scenario's status the one the results file gives, and every test passing only for a
    variant that survived."""
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_scenarios.py", "-q", "-p", "no:cacheprovider",
                           "--agent", name, "--out", str(tmp_path), "--run-id", name],
                          cwd=HERE, capture_output=True, text=True)
    records = {r["scenario"]: r for r in (json.loads(p.read_text()) for p in (tmp_path / "verdicts").glob("*.json"))}
    assert sorted(records) == world_scenarios() and len(records) == 16
    want = saved()["variants"][name]
    for sc, r in records.items():
        assert r["llm_calls"] == 0 and all(q["source"] == "data file" for q in r["judge"]), sc
        assert r["status"] == want["scenarios"][sc]["status"], sc
    assert (proc.returncode == 0) == (want["outcome"] == "survived"), proc.stdout[-2000:]


def test_run_variants_say_only_labelled_sentences():
    """Should find every sentence each variant says among data.json's agent entries, with no LLM call and no
    scenario in which a variant has no step."""
    for name, v in saved()["variants"].items():
        for sc, s in v["scenarios"].items():
            assert s["status"] != "error", (name, sc, s.get("error"))
            assert s["unlabelled_sentences"] == [] and s["llm_calls"] == 0, (name, sc)


def test_check_new_sentences_are_labelled_entries():
    """Should find each sentence only a variant says labelled in data.json, with a recorded judge answer."""
    from harness.data import data
    new = ("propose_no_name", "booked_no_id", "unknown_no_call", "max8_no_ask")
    reference = {render(e["value"], confirmation_id=c) for k, e in data()["agent"].items() if k not in new
                 for c in values()["confirmation_ids"]}
    assert any(text.startswith("Your table is booked.") for text in reference)  # "booked" is compared too
    for key in new:
        e = data()["agent"][key]
        assert e["source"] == "free choice" and e["note"] and set(e["judge"]) == set(data()["judge_questions"])
        assert render(e["value"]) not in reference


# ---------------------------------------------------------------------- lines 3 and 4


def test_check_results_file_equals_rerun():
    """Should find variant_results.json equal to a rerun of the variants."""
    assert variant_results.RESULTS.read_text(encoding="utf-8") == variant_results.text()


def test_check_results_every_variant_differs_from_reference():
    """Should find every variant's events differing from the reference agent's in at least one scenario."""
    for name, v in saved()["variants"].items():
        assert v["differs_in"], name


def test_check_results_one_outcome_each():
    """Should give each variant one outcome, and for each not caught the words of its rule that went
    unchecked and whether unchecked_sentences.json lists them."""
    got = saved()
    assert set(got["variants"]) == {c.name for c in SLICE_C}
    assert sum(got["counts"].values()) == len(SLICE_C)
    for c in SLICE_C:
        v = got["variants"][c.name]
        assert v["outcome"] in OUTCOMES
        assert (v["outcome"] == "caught") == (c.rule in v["broken_rules"])
        if v["outcome"] == "caught":
            assert "unchecked" not in v
        else:
            assert v["unchecked"]["words"] == c.breaks
            assert v["unchecked"]["listed_in_unchecked_sentences"].split(":")[0] in ("yes", "no")


def test_check_results_listed_answer_for_todays_variant():
    """Should record "yes" for the one variant not caught, break-R-04-message, whose words task 51's review
    found unlisted in unchecked_sentences.json and task 67 listed there, and say that R-04's "asks again" is
    reached in no scenario."""
    not_caught = {n: v for n, v in saved()["variants"].items() if v["outcome"] != "caught"}
    assert list(not_caught) == ["break-R-04-message"]
    v = not_caught["break-R-04-message"]
    assert v["unchecked"]["listed_in_unchecked_sentences"] == "yes: the words are inside a string of the file"
    assert "reached in no scenario" in v["note"] and "release_failed" in v["note"]


def test_listed_answers_from_fixture_file(tmp_path, monkeypatch):
    """Should answer yes when the words are inside a string of the file or a string of 3 or more words is inside
    them, and no otherwise, quotes and spaces aside."""
    fixture = tmp_path / "unchecked.json"
    fixture.write_text(json.dumps({"rows": [{"clause": "It holds the  “changed table”, and then"}, "asks again"],
                                   "short": ["the table"]}), encoding="utf-8")
    monkeypatch.setattr(variant_results, "UNCHECKED", fixture)
    assert variant_results.listed('Holds the "changed table"').startswith("yes: the words are inside")
    assert variant_results.listed('so it holds the "changed table", and then asks again') \
        .startswith("yes: a string of the file")
    assert variant_results.listed("gives the confirmation id") == "no"
    assert variant_results.listed("says asks again") == "no"  # "asks again" has 2 words, too short to count


# ---------------------------------------------------------------------- line 5


def test_check_variant_code_imports_no_checker():
    """Should find the variants' module importing nothing from harness/checkers.py or tests/test_slice_b.py."""
    tree = ast.parse((HERE / "harness" / "agents.py").read_text(encoding="utf-8"))
    imported = [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]
    imported += [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
    assert imported == ["harness.data"]
    assert all(c.__module__ == agents.__name__ for c in SLICE_C)


# ---------------------------------------------------------------------- line 6: the judge on slice B's cases

B_ARGS = ["--cases", "judge_cases_b.json", "--out", "runs/judge-test-b.json", "--needed", "17"]


def b_cases():
    return json.loads((HERE / "judge_cases_b.json").read_text(encoding="utf-8"))["cases"]


def test_judge_test_b_cases_with_stub_write_given_result_file(tmp_path, monkeypatch):
    """Should put each of the 20 cases of judge_cases_b.json to the judge 3 times, count the 18 not marked hard
    against 17, write the result file given and record the calls in the ledger given, not task 56's."""
    from probe import judge_test
    from probe.llm import LLM
    from stub_api import StubClient
    monkeypatch.setenv("CAFE_USAGE_LEDGER", str(tmp_path / "usage.jsonl"))
    cs = b_cases()
    assert len(cs) == 20 and sum(c["hard"] for c in cs) == 2
    replies = [("text", c["expected"].capitalize() + ".") for c in cs for _ in range(3)]
    replies[0] = ("text", {"yes": "No.", "no": "Yes."}[cs[0]["expected"]])
    out, ledger = tmp_path / "b.json", tmp_path / "usage.jsonl"
    res = judge_test.run(LLM(client=StubClient(replies)), HERE / "judge_cases_b.json", out, 17, ledger, 0.45)
    assert json.loads(out.read_text()) == res and len(judge_test.money.calls(ledger)) == 60
    assert res["pass_line"] == {"cases_not_hard": 18, "as_expected_in_2_of_3": 18, "needed": 17, "holds": True}
    assert [r["id"] for r in res["hard_cases"]] == [c["id"] for c in cs if c["hard"]]
    assert [r["id"] for r in res["differing_repeats"]] == [cs[0]["id"]]
    assert "judge_cases_b.json" in res["_about"]


def test_judge_test_b_stops_at_the_given_spend(tmp_path, monkeypatch):
    """Should start no case once the given ledger holds the given stop in USD."""
    from probe import judge_test
    ledger = tmp_path / "usage.jsonl"
    monkeypatch.setattr(judge_test.money, "spent", lambda path=None: 0.45 if path == ledger else 0.0)
    with pytest.raises(SystemExit, match="stopped before J33"):
        judge_test.run(object(), HERE / "judge_cases_b.json", tmp_path / "b.json", 17, ledger, 0.45)


def test_judge_test_b_without_ledger_refuses(monkeypatch, capsys):
    """Should refuse, before any call, to run a cases file other than judge_cases.json without --ledger, so its
    calls never go to task 56's ledger."""
    from probe import judge_test
    monkeypatch.setattr(judge_test, "run", lambda **kw: pytest.fail("ran without a ledger"))
    with pytest.raises(SystemExit) as e:
        judge_test.main(["--cases", "judge_cases_b.json", "--out", "runs/judge-test-b.json", "--needed", "17"])
    assert e.value.code == 2 and "--ledger is required" in capsys.readouterr().err


def test_judge_test_b_report_on_saved_file_holds(capsys):
    """Should exit 0 on runs/judge-test-b.json: at least 17 of the 18 cases not marked hard answered as expected
    in at least 2 of 3 repeats, with the hard cases and the cases with differing repeats listed."""
    from probe import judge_test
    with pytest.raises(SystemExit) as e:
        judge_test.main([*B_ARGS, "--report"])
    out = capsys.readouterr().out
    assert e.value.code == 0, out
    assert "of the 18 cases not marked hard" in out and "needed 17 -> HOLDS" in out
    assert "hard cases: J37" in out and "cases with differing repeats:" in out
