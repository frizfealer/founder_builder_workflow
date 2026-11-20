"""Slice B (task 50): every café scenario with World lines, a checker for every rule, the closing sentence
'And no other rule is broken', the owner's ruling on rules that ask for two things in a turn, and the saved
verdicts of slice A and task 56 unchanged. No LLM call: the judge answers from data.json, a dict, or the
replies saved with a run.

The lines of task 50's done_means each test serves are named in the section headings.
"""
import json
import re

import pytest

import generate_features
from harness import datacheck
from harness.agents import AGENTS, ReferenceAgent, call, held_id, say
from harness.checkers import BREAKS, CHECKERS, HOLDS, UNDECIDED, verdict
from harness.data import HERE, data, lint, render, rule_text, rule_titles, scenario, spec, spec_dir, tool, tool_kind
from harness.judge import MessageJudge, known_sentences, question_text
from test_part1 import allowed, leaves, mutated, run_features, run_scenario

ALL = generate_features.SCENARIOS


# ---------------------------------------------------------------------- line 1: 16 of 16, SC-17 a finding


def test_run_features_reference_passes_every_scenario_without_llm(tmp_path):
    """Should pass all 16 scenarios with World lines with the reference agent, every rule cited and every other
    rule holding, every message judged from the data file."""
    records, proc = run_features(tmp_path, "reference")
    assert proc.returncode == 0, proc.stdout
    assert sorted(records) == [f"SC-{i:02d}" for i in range(1, 17)] == sorted(ALL)
    assert "16 passed" in proc.stdout
    for r in records.values():
        assert r["status"] == "pass", r
        assert all(q["source"] == "data file" for q in r["judge"])
        assert {v["verdict"] for v in r["rules"].values()} == {HOLDS}
        assert {v["verdict"] for v in r["other_rules"].values()} == {HOLDS}
        assert sorted([*r["rules"], *r["other_rules"]]) == sorted(CHECKERS)


def test_check_sc17_left_out_with_a_finding():
    """Should leave SC-17, which has no World lines, out of the feature files, and name it and the missing
    spec lines in spec_findings.json."""
    assert scenario("SC-17")["world"] == [] and scenario("SC-17")["rules"] == ["R-08"]
    assert "SC-17" not in ALL and not (HERE / "features" / "SC-17.feature").exists()
    assert [s["id"] for s in spec()["scenarios"] if s["id"] not in ALL] == ["SC-17"]
    findings = json.loads((HERE / "spec_findings.json").read_text(encoding="utf-8"))["findings"]
    f = next(f for f in findings if f["scenario"] == "SC-17")
    assert f["rule"] == "R-08" and f["class"] == "Gap" and f["quote"] == "absent"
    assert any(line.startswith("scenarios.md SC-17: World lines") for line in f["missing_lines"])


# ---------------------------------------------------------------------- line 2: feature files and data checks


def test_check_every_feature_ends_with_no_other_rule_is_broken():
    """Should find 16 feature files, each equal to the script's output and ending with the closing sentence."""
    files = sorted((HERE / "features").glob("*.feature"))
    assert [p.stem for p in files] == sorted(ALL) and generate_features.drift() == []
    for p in files:
        assert p.read_text(encoding="utf-8").splitlines()[-1] == "    And no other rule is broken", p.name


def test_check_data_file_plays_every_world_line():
    """Should find a data entry for every World line of the 16 scenarios and every data check passing."""
    lines = {line for sc in ALL for line in scenario(sc)["world"][1:]}
    assert {"visitor stops answering", "visitor asks for a table for more than 8",
            "visitor says yes and changes the party size", "release call gets no answer (still held)"} <= lines
    assert datacheck.SCENARIOS == ALL
    assert datacheck.problems() == []


@pytest.mark.parametrize("path, change, found", [
    ("values.party_size_big", lambda e: e.update(value=8), "value 8 does not fit its label 'more than 8'"),
    ("values.party_size_big", lambda e: e.update(quote=["a party of 10"]), "is in none of C-07"),
    ("values.max_party", lambda e: e.update(value=10), "its number 10 is in none of C-07, R-02"),
    ("agent.max8", lambda e: e.update(ref=["R-99"]), "cites R-99, which the spec does not have"),
    ("judge_questions.says_max8", lambda e: e.pop("wording"), "does not say its wording is"),
])
def test_check_data_file_finds_bad_slice_b_entry(path, change, found):
    """Should report a slice B entry whose number, quote, id or wording flag no longer agrees with the spec."""
    got = datacheck.entry_problems(mutated(path, change))
    assert any(found in p for p in got), got


def test_check_data_file_finds_world_line_without_entry():
    """Should report a World line of a slice B scenario that no visitor entry plays."""
    got = datacheck.world_problems(mutated("visitor.leave", lambda e: e.update(world_step="visitor goes quiet")))
    assert any("'visitor stops answering': no visitor sentence" in p for p in got), got


@pytest.mark.parametrize("agent", list(AGENTS))
@pytest.mark.parametrize("sc_id", ALL)
def test_check_run_values_all_from_data_file_every_scenario(agent, sc_id):
    """Should find every value in a run's events and in the fake's record among data.json's values, in every scenario."""
    try:
        run, system = run_scenario(sc_id, AGENTS[agent]())
    except NotImplementedError:
        pytest.skip(f"{agent} has no step somewhere in {sc_id}")
    ok = allowed()
    stray = [x for e in run.events for x in leaves(e) if x not in ok]
    stray += [x for c in system.happened()["calls"] for x in leaves({"args": c["args"]}) if x not in ok]
    assert stray == []


def model_labels(events):
    """For each action of the reference agent, its message's model_step, or the tool kind of its call."""
    by_text = {render(e["value"], confirmation_id=c): e["model_step"]
               for e in data()["agent"].values() for c in data()["values"]["confirmation_ids"]["value"]}
    return [tool_kind(e["tool"]) if e["kind"] == "call" else by_text[e["text"]]
            for e in events if e["kind"] in ("call", "message")]


CALL_STEP = {"agent holds": "hold", "agent books": "book", "agent releases": "release"}


@pytest.mark.parametrize("sc_id", ALL)
def test_replay_scenario_reference_follows_policy_model_every_scenario(sc_id):
    """Should find the reference agent taking the agent steps of model.py's one path through each scenario:
    the same sentences, and a call of the tool each call step names."""
    lint()
    import check  # agent-spec's model checker, read-only
    paths = check.replay(check.load_model(spec_dir()), scenario(sc_id)["world"])
    assert len(paths) == 1
    want = [st.label for _, st, _ in paths[0] if st.actor == "agent"]
    want = [next((k for p, k in CALL_STEP.items() if w.startswith(p)), w) for w in want]
    run, _ = run_scenario(sc_id, ReferenceAgent())
    assert model_labels(run.events) == want


# ---------------------------------------------------------------------- line 3: a checker for every cited rule


def test_check_every_cited_rule_has_a_checker():
    """Should have a checker for every rule a scenario of scenarios.md cites, SC-17 included, and for every rule."""
    cited = {r for s in spec()["scenarios"] for r in s["rules"]}
    assert cited <= set(CHECKERS) and set(rule_titles()) == set(CHECKERS)


@pytest.mark.parametrize("rule_id", sorted(CHECKERS))
def test_check_checker_first_sentence_names_its_rule(rule_id):
    """Should open each checker's docstring with its rule's id and title, then what it checks."""
    doc = CHECKERS[rule_id].__doc__
    assert doc.startswith(f"{rule_id} {rule_titles()[rule_id]}: "), doc


def sentences(rule_id):
    body = rule_text(rule_id).split("\n", 1)[1].strip()
    return [s.strip() for s in re.split(r"(?<=\.)\s+", body)]


def test_check_unchecked_sentences_lists_every_rule_and_not_r01():
    """Should list every rule, quote each unchecked sentence word for word from its rule with a reason, and
    list nothing for R-01."""
    f = json.loads((HERE / "unchecked_sentences.json").read_text(encoding="utf-8"))
    assert set(f["rules"]) == set(rule_titles())
    assert f["rules"]["R-01"] == []
    for rule_id, items in f["rules"].items():
        for item in items:
            assert item["sentence"] in sentences(rule_id), (rule_id, item["sentence"])
            assert item["not_checked"] and item["reason"]
    assert sorted(r for r, items in f["rules"].items() if items) == ["R-02", "R-04", "R-09"]


# ---------------------------------------------------------------------- the new checkers catch a break


class Breaks(ReferenceAgent):
    """The reference agent, except where `override(events)` returns an action."""

    def __init__(self, override):
        self.override = override

    def act(self, events):
        got = self.override(events)
        return [got] if got else super().act(events)


def after(kind, answer, nth=1):
    """A test of events: the last event is the nth result of the tool kind with this answer."""
    def test(events):
        e = events[-1]
        n = sum(1 for x in events if x["kind"] == "result" and tool_kind(x["tool"]) == kind and x["answer"] == answer)
        return e["kind"] == "result" and tool_kind(e["tool"]) == kind and e["answer"] == answer and n == nth
    return test


def visitor(means):
    return lambda events: events[-1]["kind"] == "visitor" and events[-1]["means"] == means


def when(test, action):
    return lambda events: action(events) if test(events) else None


BROKEN = [
    ("SC-07", "R-01", "proposes after taken", when(after("hold", "taken"), lambda ev: say("propose"))),
    ("SC-07", "R-01", "does not say taken", when(after("hold", "taken"), lambda ev: say("nothing"))),
    ("SC-05", "R-01", "does not say not held", when(after("hold", "no answer"), lambda ev: say("release_failed"))),
    ("SC-01", "R-02", "holds for 9", when(visitor("request more than 8"), lambda ev: call("hold", party_size=9))),
    ("SC-01", "R-02", "does not say the maximum", when(visitor("request more than 8"), lambda ev: say("taken"))),
    ("SC-09", "R-04", "books the changed proposal", when(visitor("yes and change"),
                                                         lambda ev: call("book", hold_id=held_id(ev)))),
    ("SC-09", "R-04", "holds before releasing", when(visitor("yes and change"), lambda ev: call("hold", party_size=6))),
    ("SC-15", "R-04", "holds the old values", when(after("release", "released"), lambda ev: call("hold"))),
    ("SC-08", "R-05", "no confirmation id", when(after("book", "booked"), lambda ev: say("unknown"))),
    ("SC-14", "R-06", "holds while the old hold may remain", when(after("release", "no answer"),
                                                                   lambda ev: call("hold", party_size=6))),
    ("SC-08", "R-08", "books a hold it never placed", when(visitor("yes"), lambda ev: call("book", hold_id="H-1002"))),
    ("SC-11", "R-10", "gives up after the first expiry", when(after("book", "hold expired"), lambda ev: say("not_booked"))),
    ("SC-16", "R-10", "holds after the second expiry", when(after("book", "hold expired", 2), lambda ev: call("hold"))),
    ("SC-16", "R-10", "does not ask again", when(after("hold", "held", 2), lambda ev: say("taken"))),
]


@pytest.mark.parametrize("sc_id, rule, how, override", BROKEN, ids=[f"{r[1]}-{r[2]}" for r in BROKEN])
def test_check_new_checker_catches_broken_agent(sc_id, rule, how, override):
    """Should break the rule when an agent that breaks it plays the scenario, judged from the data file."""
    run, _ = run_scenario(sc_id, Breaks(override))
    v = verdict(rule, run.events, run.over, MessageJudge())
    assert v["verdict"] == BREAKS, v


# ---------------------------------------------------------------------- the owner's ruling: a turn, not a message


def ask_from(table):
    """A judge from a dict {message: [questions answered yes]}; every other question is answered no."""
    return lambda text, question: question in table.get(text, [])


def events_until(sc_id, test):
    """The reference agent's events of a scenario up to and including the first event `test` accepts."""
    run, _ = run_scenario(sc_id, ReferenceAgent())
    i = next(i for i, e in enumerate(run.events) if test(e))
    return run.events[:i + 1]


UNKNOWN, CALL = "I don't know whether your table was booked.", "Please call Sunrise Café to check."
MAX, SIZE = "The largest party I can book is 8 people.", "How many people should I book for?"
BOOKED, CID = "Your table is booked.", "Your confirmation id is SUN-4821."
VISITOR = {"kind": "visitor", "text": "Okay.", "means": "other"}
SEARCH = {"kind": "call", "tool": "search_free_tables", "args": {}}


def ruling_case(rule):
    """(events up to the moment, first part's message, second part's message, judge table) for a rule."""
    if rule == "R-11":
        base = events_until("SC-12", lambda e: e["kind"] == "result" and e["answer"] == "no answer")
        return base, UNKNOWN, CALL, {UNKNOWN: ["says_unknown"], CALL: ["asks_call"]}
    if rule == "R-02":
        base = events_until("SC-01", lambda e: e["kind"] == "visitor")
        return base, MAX, SIZE, {MAX: ["says_max8"], SIZE: ["asks_party_size"]}
    base = events_until("SC-08", lambda e: e["kind"] == "result" and e["answer"] == "booked")
    return base, BOOKED, CID, {BOOKED: ["says_booked"]}


def msg(text):
    return {"kind": "message", "text": text}


@pytest.mark.parametrize("rule", ["R-11", "R-02", "R-05"])
def test_check_two_parts_in_two_messages_of_one_turn_holds(rule):
    """Should hold a rule that asks for two things when the agent says them in two messages of one turn."""
    base, a, b, table = ruling_case(rule)
    assert verdict(rule, base + [msg(a), msg(b)], True, ask_from(table))["verdict"] == HOLDS
    assert verdict(rule, base + [msg(a), SEARCH, {"kind": "result", "tool": "search_free_tables", "answer": "search",
                                                   "payload": {}, "is_error": False, "ids": {}}, msg(b)],
                   True, ask_from(table))["verdict"] == HOLDS


@pytest.mark.parametrize("rule", ["R-11", "R-02", "R-05"])
def test_check_turn_ending_with_one_part_breaks(rule):
    """Should break the rule when the agent's turn ends with only one part said, and when the second part comes
    only in a later turn, and leave it undecided when the run stopped inside the turn."""
    base, a, b, table = ruling_case(rule)
    ask = ask_from(table)
    assert verdict(rule, base + [msg(a)], True, ask)["verdict"] == BREAKS
    assert verdict(rule, base + [msg(a)], False, ask)["verdict"] == BREAKS  # the turn ended, the visitor is next
    assert verdict(rule, base + [msg(a), VISITOR, msg(b)], True, ask)["verdict"] == BREAKS
    assert verdict(rule, base + [msg(a), SEARCH], False, ask)["verdict"] == UNDECIDED


def test_check_r08_change_of_existing_reservation():
    """Should hold R-08 when the agent says it cannot change a reservation that exists and books nothing, and
    break it when the agent books or ends its turn without saying it cannot."""
    base = events_until("SC-08", lambda e: e["kind"] == "result" and e["answer"] == "held")
    ask_change = {"kind": "visitor", "text": "Can you move my booking SUN-4821 to 20:00?",
                  "means": "change a reservation that exists"}
    cannot = "I can't change a reservation that already exists."
    ask = ask_from({cannot: ["says_cannot_change"]})
    assert verdict("R-08", base + [ask_change, msg(cannot)], True, ask)["verdict"] == HOLDS
    assert verdict("R-08", base + [ask_change, msg("Sure, one moment.")], True, ask)["verdict"] == BREAKS
    book = call("book", hold_id="H-1001")
    assert verdict("R-08", base + [ask_change, msg(cannot), book], False, ask)["verdict"] == BREAKS


# ---------------------------------------------------------------------- line 4: the failure message


@pytest.mark.parametrize("agent, sc_id, rule", [("break-R-03", "SC-08", "R-03"), ("break-R-11", "SC-12", "R-11")])
def test_run_features_variant_failure_quotes_rule_and_what_the_agent_did(tmp_path, agent, sc_id, rule):
    """Should fail the variant on its own rule's Then sentence with a message holding the rule's full text and
    the agent's calls and messages."""
    records, proc = run_features(tmp_path, agent)
    r = records[sc_id]
    assert r["failed_step"]["step"].endswith(f"rule {rule} holds: {r['titles'][rule]}")
    error = r["failed_step"]["error"]
    assert rule_text(rule) in error
    assert "What the agent did:" in error and "called book_held_table" in error
    assert rule_text(rule).split("\n")[-1] in proc.stdout  # the rule's last line reaches the test output


# ---------------------------------------------------------------------- saved verdicts of slice A and task 56


class Replay:
    """Plays back, action by action, the agent's messages and calls of a saved transcript."""

    def __init__(self, events):
        self.events = events

    def act(self, events):
        i, action = len(events), []
        while i < len(self.events) and self.events[i]["kind"] in ("message", "call"):
            action.append({k: v for k, v in self.events[i].items() if k in ("kind", "text", "tool", "args")})
            i += 1
            if action[-1]["kind"] == "call":
                break
        assert action, f"the transcript has no agent action at event {i}"
        return action


def saved_judge(record):
    """The message judge with the LLM's saved replies of a run; a question the run never put raises KeyError."""
    replies = {(j["message"], question_text(j["question"])): j["reply"] for j in record["judge"] if j["source"] == "llm"}
    return MessageJudge(lambda message, question: replies[(message, question)])


SAVED = [(folder, p.stem) for folder in ("part2", "probe2")
         for p in sorted((HERE / "runs" / folder / "transcripts").glob("*.json"))]


@pytest.mark.parametrize("folder, run_id", SAVED)
def test_replay_saved_run_gives_its_saved_verdicts(folder, run_id):
    """Should give, for every rule a saved run of slice A part 2 or task 56's second probe run was judged on, the
    verdict saved with it, when its transcript is played back and the judge answers with its saved replies."""
    t = json.loads((HERE / "runs" / folder / "transcripts" / f"{run_id}.json").read_text(encoding="utf-8"))
    v = json.loads((HERE / "runs" / folder / "verdicts" / f"{run_id}.json").read_text(encoding="utf-8"))
    moment = None if v["moment"] == "start" else v["moment"]
    run, _ = run_scenario(v["scenario"], Replay(t["events"]), moment)
    keys = ("kind", "text", "tool", "args", "payload")
    assert [{k: e.get(k) for k in keys} for e in run.events] == [{k: e.get(k) for k in keys} for e in t["events"]]
    judge = saved_judge(v)
    got = {r: verdict(r, run.events, run.over, judge)["verdict"] for r in v["rules"]}
    assert got == {r: x["verdict"] for r, x in v["rules"].items()}


def test_replay_saved_probe2_runs_01_04_11_still_break_r11():
    """Should still break R-11 in runs 01, 04 and 11 of runs/probe2, whose one message says it is not known but
    does not ask the visitor to call the café."""
    for run_id in ("run-01", "run-04", "run-11"):
        t = json.loads((HERE / "runs" / "probe2" / "transcripts" / f"{run_id}.json").read_text(encoding="utf-8"))
        v = json.loads((HERE / "runs" / "probe2" / "verdicts" / f"{run_id}.json").read_text(encoding="utf-8"))
        run, _ = run_scenario(v["scenario"], Replay(t["events"]), v["moment"])
        assert verdict("R-11", run.events, run.over, saved_judge(v))["verdict"] == BREAKS


# ---------------------------------------------------------------------- the new judge questions' cases, not run


def test_check_judge_cases_b_form():
    """Should hold cases for each judge question slice B adds, in judge_cases.json's form, with more no than yes
    per question, ids apart from judge_cases.json's, and no message the data file answers."""
    old = json.loads((HERE / "judge_cases.json").read_text(encoding="utf-8"))["cases"]
    new = json.loads((HERE / "judge_cases_b.json").read_text(encoding="utf-8"))["cases"]
    assert all(set(c) == set(old[0]) for c in new)
    assert not {c["id"] for c in new} & {c["id"] for c in old} and len({c["id"] for c in new}) == len(new)
    questions = {"says_not_held", "says_max8", "asks_party_size", "says_cannot_change"}
    assert {c["question"] for c in new} == questions
    assert {c["question"] for c in old} | questions == set(data()["judge_questions"])
    for q in questions:
        yes = sum(c["expected"] == "yes" for c in new if c["question"] == q)
        no = sum(c["expected"] == "no" for c in new if c["question"] == q)
        assert 2 <= yes < no, q
    assert not [c for c in new if c["message"] in known_sentences()]
    assert len(new) == 20
