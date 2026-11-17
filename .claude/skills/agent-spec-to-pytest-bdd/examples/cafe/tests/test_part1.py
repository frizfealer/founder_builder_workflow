"""Slice A, part 1: the harness proven on the reference agent and its broken variants, with no LLM.

Lines 1 to 3 of task 49's done_means:
1. the 3 scenarios pass with the reference agent, with 0 LLM calls;
2. each broken variant fails the Then sentence of its own rule;
3. every value a step, the fake or a replayed history uses comes from data.json, every entry there is
   labelled, each 'from the spec' entry cites ids the spec has, with words or a number found in the cited
   text or a note that its wording is the builder's own, each value fits its scenario label, the drift
   check covers the data file as well as the feature files, and the feature files equal the script's output.
"""
import copy
import json
import subprocess
import sys

import pytest

import conftest
import generate_features
from harness import datacheck
from harness.agents import AGENTS, ReferenceAgent
from harness.checkers import CHECKERS, HOLDS, verdict
from harness.data import HERE, data, lint, render, scenario, spec_dir, tool, tool_kind, values
from harness.fake import FakeBookingSystem
from harness.judge import MessageJudge
from harness.slot import Driver, world_line

SCENARIOS = generate_features.SCENARIOS


def run_features(tmp_path, agent):
    """Run the feature files in a fresh pytest with this agent; {scenario id: verdict record}."""
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_scenarios.py", "-q", "-p", "no:cacheprovider",
                           "--agent", agent, "--out", str(tmp_path), "--run-id", agent],
                          cwd=HERE, capture_output=True, text=True)
    records = [json.loads(p.read_text()) for p in sorted((tmp_path / "verdicts").glob("*.json"))]
    return {r["scenario"]: r for r in records}, proc


def run_scenario(sc_id, agent, moment=None):
    """What the step functions do for one scenario, without pytest-bdd: Given, When lines, then the run."""
    first, *rest = scenario(sc_id)["world"]
    assert first == "The table is free"
    system = FakeBookingSystem()
    system.start(table_free=True)
    run = Driver([world_line(l) for l in rest], system, agent).run(moment)
    return run, system


# ---------------------------------------------------------------------- line 1


def test_run_features_reference_passes_all_three_without_llm(tmp_path):
    """Should pass SC-08, SC-12 and SC-10 with the reference agent, every message judged from the data file."""
    records, proc = run_features(tmp_path, "reference")
    assert proc.returncode == 0, proc.stdout
    assert sorted(records) == sorted(SCENARIOS)
    for r in records.values():
        assert r["status"] == "pass", r
        assert r["llm_calls"] == 0
        assert all(q["source"] == "data file" for q in r["judge"])
    transcripts = {p.stem: p.read_text() for p in (tmp_path / "transcripts").glob("*.json")}
    assert sorted(transcripts) == [f"reference-{sc}" for sc in sorted(SCENARIOS)]
    first_id = values()["confirmation_ids"][0]
    assert first_id in transcripts["reference-SC-08"]  # sent: the booked answer and the agent's message
    assert first_id not in transcripts["reference-SC-12"]  # issued by the unanswered booking call, never sent


def test_judge_message_outside_data_file_without_llm_raises():
    """Should refuse to judge a message the data file lacks when no LLM is given, so lane 1 cannot call one."""
    with pytest.raises(Exception, match="no LLM judge"):
        MessageJudge()("Your table is booked.", "says_booked")


# ---------------------------------------------------------------------- line 2


@pytest.mark.parametrize("agent, sc_id, rule", [("break-R-03", "SC-08", "R-03"), ("break-R-11", "SC-12", "R-11")])
def test_run_features_variant_fails_its_own_rule_sentence(tmp_path, agent, sc_id, rule):
    """Should fail the scenario on the Then sentence of the rule the variant breaks, with a break, not a no-verdict."""
    records, proc = run_features(tmp_path, agent)
    assert proc.returncode == 1
    r = records[sc_id]
    assert r["status"] == "fail"
    assert r["failed_step"]["step"].endswith(f"rule {rule} holds: {r['titles'][rule]}")
    assert r["rules"][rule]["verdict"] == "breaks"
    assert r["llm_calls"] == 0


@pytest.mark.parametrize("agent, moment, rule", [("break-R-03", "M2", "R-03"), ("break-R-11", "M5", "R-11")])
def test_run_moment_variant_breaks_its_rule(agent, moment, rule):
    """Should break the variant's rule when it takes one action from the moment where it misbehaves."""
    run, _ = run_scenario(data()["moments"][moment]["scenario"], AGENTS[agent](), moment)
    assert verdict(rule, run.events, run.over, MessageJudge())["verdict"] == "breaks"


# ---------------------------------------------------------------------- line 3


def test_check_features_equal_script_output():
    """Should find the feature files equal to what generate_features.py writes from the spec."""
    assert generate_features.drift() == []


def test_check_drift_finds_edited_feature(tmp_path, monkeypatch):
    """Should report a feature file that no longer equals the script's output."""
    for path, text in generate_features.expected().items():
        (tmp_path / path.name).write_text(text)
    (tmp_path / "SC-08.feature").write_text("Feature: edited\n")
    monkeypatch.setattr(generate_features, "FEATURES", tmp_path)
    assert [p.name for p in generate_features.drift()] == ["SC-08.feature"]


def test_check_data_file_every_entry_labelled():
    """Should find each data.json entry labelled 'from the spec' with a ref, or 'free choice'."""
    unlabelled = [p for p, e in datacheck.entries() if not (e.get("source") == "free choice" or
                                                             (e.get("source") == "from the spec" and e.get("ref")))]
    assert unlabelled == []
    top = set(data()) - {"_about"}
    covered = {p.split(".")[0] for p, _ in datacheck.entries()}
    assert top <= covered, f"sections with no labelled entries checked: {top - covered}"


def test_check_data_file_from_spec_entries_cite_quote_and_fit():
    """Should find every 'from the spec' entry citing claim or rule ids the spec has, its quoted words and
    number in the cited text or its wording flagged as the builder's own, and every value fitting its label."""
    from_spec = [e for _, e in datacheck.entries() if e["source"] == "from the spec"]
    assert len(from_spec) >= 30  # values, tools, answers, fake, visitor, agent, judge questions, moments
    assert datacheck.entry_problems() == []
    assert datacheck.world_problems() == []


def test_check_data_file_party_size_fits_8_or_fewer():
    """Should give the World line 'a table for 8 or fewer' a party size of at most 8, and say so in its label."""
    e = data()["values"]["party_size"]
    assert e["label"] == "8 or fewer" and 1 <= e["value"] <= 8
    assert "visitor asks for a table for 8 or fewer" in scenario("SC-08")["world"]


def mutated(path, change):
    """A copy of data.json with change(entry) applied to the entry at 'section.key'."""
    d = copy.deepcopy(data())
    section, key = path.split(".")
    change(d[section][key])
    return d


@pytest.mark.parametrize("path, change, found", [
    ("values.party_size", lambda e: e.update(ref=["C-99"]), "cites C-99, which the spec does not have"),
    ("values.party_size", lambda e: e.update(ref="C-07"), "ref is not a list"),
    ("answers.taken", lambda e: e.pop("quote"), "quotes no words of the spec"),
    ("agent.unknown", lambda e: e.update(quote=["call the café on 555-0100"]), "is in none of R-11, C-06"),
    ("fake.table_seats", lambda e: e.update(value=7), "its number 7 is in none of C-07"),
    ("agent.booked", lambda e: e.pop("wording"), "does not say its wording is \"builder's own\""),
    ("answers.taken", lambda e: e.update(value={"answer": "unavailable"}), "'unavailable' is not in the cited text"),
    ("values.party_size", lambda e: e.update(value=9), "value 9 does not fit its label '8 or fewer'"),
    ("values.party_size", lambda e: e.update(label="6 or fewer"), "label '6 or fewer' is in no World line"),
    ("values.party_size", lambda e: e.pop("label"), "names a number no data entry is labelled for"),
    ("values.cafe", lambda e: e.update(source="the spec"), "labelled neither"),
])
def test_check_data_file_finds_bad_entry(path, change, found):
    """Should report an entry whose id, quote, number, wording flag or label no longer agrees with the spec."""
    got = datacheck.entry_problems(mutated(path, change))
    assert any(found in p for p in got), got


def test_check_data_file_finds_visitor_line_no_scenario_has():
    """Should report a visitor sentence whose world step none of the 3 scenarios has."""
    got = datacheck.world_problems(mutated("visitor.yes", lambda e: e.update(world_step="visitor says yes please")))
    assert any("'visitor says yes'" in p and "no visitor sentence" in p for p in got), got


def test_check_data_file_finds_stale_history(monkeypatch):
    """Should report a moment whose history no longer equals the reference agent's run."""
    d = copy.deepcopy(data())
    d["moments"]["M3"]["history"][-1]["text"] = "Yes please."
    monkeypatch.setattr(datacheck, "data", lambda: d)
    assert datacheck.history_problems() == [
        "moments.M3: the history is not the reference agent's run of SC-08 up to that turn"]


def test_check_drift_stops_run_on_stale_data_file(monkeypatch):
    """Should stop a test run at its start when the data file no longer agrees with the spec."""
    monkeypatch.setattr(datacheck, "problems", lambda: ["values.party_size: value 9 does not fit its label"])
    with pytest.raises(pytest.exit.Exception, match="data.json no longer agrees with the spec"):
        conftest.pytest_sessionstart(None)


def test_check_drift_script_covers_data_file():
    """Should report both halves of the drift check from generate_features.py --check."""
    proc = subprocess.run([sys.executable, "generate_features.py", "--check"], cwd=HERE, capture_output=True, text=True)
    assert proc.returncode == 0
    assert proc.stdout.splitlines() == ["feature files equal the script's output", "data.json agrees with the spec"]


NOT_VALUES = {"_about", "source", "ref", "quote", "note", "wording", "label", "situation"}  # labels, not values


def allowed():
    """Every key and value data.json gives outside its moments and its labels, each template filled with
    every id the fake can issue: the only values a run may contain."""
    v = values()
    ids = [dict(hold_id=h, confirmation_id=c, free_tables=[]) for h, c in zip(v["hold_ids"], v["confirmation_ids"])]
    out = set()

    def walk(x):
        if isinstance(x, dict):
            for k, y in x.items():
                if k not in NOT_VALUES:
                    out.add(k)
                    walk(y)
        elif isinstance(x, list):
            for y in x:
                walk(y)
        elif isinstance(x, str):
            for i in ids:
                try:
                    walk(render(x, **i)) if render(x, **i) != x else out.add(x)
                except (KeyError, ValueError, IndexError):
                    out.add(x)
        else:
            out.add(x)

    d = {k: x for k, x in data().items() if k != "moments"}
    walk(d)
    return out


def leaves(e):
    """The keys and values of an event the agent sees or sends, and the ids the system issued."""
    out = []

    def walk(x):
        if isinstance(x, dict):
            for k, y in x.items():
                out.append(k)
                walk(y)
        elif isinstance(x, list):
            for y in x:
                walk(y)
        else:
            out.append(x)

    for field in ("text", "tool", "args", "payload", "ids"):
        if field in e:
            walk(e[field])
    return out


@pytest.mark.parametrize("agent", list(AGENTS))
@pytest.mark.parametrize("sc_id", SCENARIOS)
def test_check_run_values_all_from_data_file(agent, sc_id):
    """Should find every value in a run's events and in the fake's record among data.json's values."""
    run, system = run_scenario(sc_id, AGENTS[agent]())
    ok = allowed()
    stray = [x for e in run.events for x in leaves(e) if x not in ok]
    stray += [x for c in system.happened()["calls"] for x in leaves({"args": c["args"]}) if x not in ok]
    assert stray == []


def test_check_histories_values_all_from_data_file():
    """Should find every value of the 7 replayed histories among data.json's values outside the histories."""
    ok = allowed()
    stray = [(m, x) for m, h in data()["moments"].items() if not m.startswith("_")
             for e in h["history"] for x in leaves(e) if x not in ok]
    assert stray == []


# ---------------------------------------------------------------------- the moments and the policy model

MOMENTS = [m for m in data()["moments"] if not m.startswith("_")]


def same(e, h):
    return all(e.get(k) == h.get(k) for k in ("kind", "text", "tool", "args", "payload", "is_error"))


class HoldsAndBooksEveryTime:
    """Holds a new slot, then books it, again and again: more holds and bookings than any scenario has."""
    name = "holds-and-books"

    def act(self, events):
        calls = [e for e in events if e["kind"] == "call"]
        last = events[-1]
        if last["kind"] == "result" and last["answer"] == "held":
            return [{"kind": "call", "tool": tool("book")["name"], "args": {"hold_id": last["ids"]["hold_id"]}}]
        args = {a: values()[key] for a, key in tool("hold")["args"].items()}
        return [{"kind": "call", "tool": tool("hold")["name"], "args": args | {"time": f"{len(calls):02d}:00"}}]


def test_run_fake_ids_last_the_action_limit():
    """Should issue a hold id and a confirmation id for every action an agent can take in one run, not raise."""
    limit = data()["action_limit"]["value"]
    assert len(values()["hold_ids"]) >= limit and len(values()["confirmation_ids"]) >= limit
    run, system = run_scenario("SC-08", HoldsAndBooksEveryTime())
    answers = [c["answer"] for c in system.happened()["calls"]]
    assert run.stopped == f"action limit ({limit})"
    assert answers == ["held", "booked"] * (limit // 2)
    assert len(system.happened()["booked"]) == limit // 2 > 3


def test_list_moments_covers_every_agent_turn():
    """Should find the 12 agent turns of the 3 scenarios starting from 7 distinct histories, the 7 moments."""
    def key(events):
        return json.dumps([{k: e.get(k) for k in ("kind", "text", "tool", "args", "payload", "is_error")}
                           for e in events], sort_keys=True)

    turns = []
    for sc_id in SCENARIOS:
        run, _ = run_scenario(sc_id, ReferenceAgent())
        turns += [key(run.events[:i]) for i, e in enumerate(run.events) if e["kind"] in ("message", "call")]
    assert len(turns) == 12
    assert set(turns) == {key(data()["moments"][m]["history"]) for m in MOMENTS}
    assert len(set(turns)) == 7


@pytest.mark.parametrize("moment", MOMENTS)
def test_replay_moment_matches_reference_run_from_start(moment):
    """Should find the moment's history equal to the reference agent's run of its scenario up to that turn,
    and the reference agent's one action from the moment equal to its next action in that run."""
    sc_id = data()["moments"][moment]["scenario"]
    history = data()["moments"][moment]["history"]
    whole, _ = run_scenario(sc_id, ReferenceAgent())
    assert all(same(e, h) for e, h in zip(whole.events, history)) and len(whole.events) > len(history)
    one, _ = run_scenario(sc_id, ReferenceAgent(), moment)
    assert [same(a, b) for a, b in zip(one.events, whole.events)] == [True] * len(one.events)


@pytest.mark.parametrize("moment", MOMENTS)
def test_check_moment_reference_holds_every_cited_rule(moment):
    """Should judge every rule of the moment's scenario as holding for the reference agent's one action."""
    sc_id = data()["moments"][moment]["scenario"]
    run, _ = run_scenario(sc_id, ReferenceAgent(), moment)
    got = {r: verdict(r, run.events, run.over, MessageJudge())["verdict"] for r in scenario(sc_id)["rules"]}
    assert set(got.values()) == {HOLDS}, got


def model_steps(events):
    """The policy model's agent step label for each action of the reference agent."""
    by_text = {}
    for e in data()["agent"].values():
        for c in values()["confirmation_ids"]:
            by_text[render(e["value"], confirmation_id=c)] = e["model_step"]
    return [tool(tool_kind(e["tool"]))["model_step"] if e["kind"] == "call" else by_text[e["text"]]
            for e in events if e["kind"] in ("call", "message")]


@pytest.mark.parametrize("sc_id", SCENARIOS)
def test_replay_scenario_reference_follows_policy_model(sc_id):
    """Should find the reference agent taking the agent steps of model.py's one path through the scenario."""
    lint()  # puts agent-spec's scripts on the path
    import check  # agent-spec's model checker, read-only
    m = check.load_model(spec_dir())
    paths = check.replay(m, scenario(sc_id)["world"])
    assert len(paths) == 1
    want = [st.label for _, st, _ in paths[0] if st.actor == "agent"]
    run, _ = run_scenario(sc_id, ReferenceAgent())
    assert model_steps(run.events) == want


def test_check_every_cited_rule_has_a_checker():
    """Should have a rule checker for every rule SC-08, SC-12 and SC-10 cite."""
    cited = {r for sc in SCENARIOS for r in scenario(sc)["rules"]}
    assert cited <= set(CHECKERS)
