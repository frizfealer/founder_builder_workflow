"""pytest options, the drift check, and the fixtures the step functions share.

  uv run pytest                                    every test, reference agent, no LLM call
  uv run pytest tests/test_scenarios.py --agent break-R-03
  uv run pytest tests/test_scenarios.py --agent probe --from M5 --prompt retry --out runs/x --run-id run-01

--from start runs each scenario from the start; --from M1..M7 replays that tested moment's history
(data.json) in its scenario and lets the agent take one action, as does a moment of the second probe run
(data.json probe_moments). --out writes one transcript file and one verdict file per run, in separate
folders, so transcripts can be labelled blind: a transcript holds what the agent saw and did, and nothing
that says what really happened behind an unanswered call or what a checker or the judge made of it.
"""
import json
import re
from pathlib import Path

import pytest

import generate_features
from harness import datacheck
from harness.agents import AGENTS
from harness.checkers import BREAKS, UNDECIDED, verdict
from harness.data import data, moment as moment_entry, moment_names, rule_text, rule_titles
from harness.fake import FakeBookingSystem
from harness.judge import MessageJudge
from harness.slot import Driver

CITED = pytest.StashKey[list]()
OUTCOME = pytest.StashKey[dict]()
FAILED = pytest.StashKey[dict]()
LLM_FIRST = pytest.StashKey[int]()  # how many LLM calls the session had made when this scenario began


def pytest_addoption(parser):
    g = parser.getgroup("cafe")
    g.addoption("--agent", default="reference", choices=[*AGENTS, "probe"], help="what fills the agent slot")
    g.addoption("--from", dest="start", default="start", choices=["start", *moment_names()],
                help="run from the start, or one action from a tested moment")
    g.addoption("--prompt", default="plain", choices=[p for p in data()["probe_prompts"] if not p.startswith("_")],
                help="probe only: the name of a data.json probe prompt")
    g.addoption("--out", default=None, help="folder for transcripts/ and verdicts/")
    g.addoption("--run-id", default="run", help="file name of this run's transcript and verdict")


def pytest_sessionstart(session):
    """The drift check: the feature files must equal what the script writes from the spec today, and the
    data file must still agree with the spec (harness/datacheck.py)."""
    bad = generate_features.drift()
    if bad:
        pytest.exit(f"feature files differ from the spec: {', '.join(p.name for p in bad)}; "
                    "rerun `uv run python generate_features.py`", returncode=3)
    stale = datacheck.problems()
    if stale:
        pytest.exit("data.json no longer agrees with the spec:\n  " + "\n  ".join(stale), returncode=3)


# ---------------------------------------------------------------------- fixtures


@pytest.fixture
def moment(request):
    start = request.config.getoption("start")
    return None if start == "start" else start


@pytest.fixture
def system():
    return FakeBookingSystem()


@pytest.fixture
def world():
    """The scenario's World lines after the starting situation, appended by the When steps."""
    return []


@pytest.fixture(scope="session")
def llm(request):
    if request.config.getoption("agent") != "probe":
        return None
    from probe.llm import LLM
    return LLM()


@pytest.fixture
def agent(request, llm):
    name = request.config.getoption("agent")
    if name == "probe":
        from probe.agent import ProbeAgent
        return ProbeAgent(llm, request.config.getoption("prompt"))
    return AGENTS[name]()


@pytest.fixture
def judge(llm):
    if llm is None:
        return MessageJudge()
    from probe.agent import judge_llm
    return MessageJudge(judge_llm(llm))


@pytest.fixture
def outcome(request, world, system, agent, judge, moment):
    """Run the scenario once, at the first Then step, and judge every rule it cites. The LLM calls it makes
    are recorded by write_run, so a run that raises keeps them."""
    run = Driver(world, system, agent).run(moment)
    rules = {r: verdict(r, run.events, run.over, judge) for r in request.node.stash[CITED]}
    played_out = moment is not None or (run.over and run.played == run.lines)
    if any(v["verdict"] == BREAKS for v in rules.values()):
        status = "fail"
    elif any(v["verdict"] == UNDECIDED for v in rules.values()) or not played_out:
        status = "no verdict"
    else:
        status = "pass"
    out = {"run": run, "rules": rules, "status": status, "played_out": played_out, "judge": judge.asked}
    request.node.stash[OUTCOME] = out
    return out


# ---------------------------------------------------------------------- pytest-bdd hooks


def pytest_bdd_before_scenario(request, feature, scenario):
    sc_id = scenario.name.split()[0]
    m = request.config.getoption("start")
    if m != "start" and moment_entry(m)["scenario"] != sc_id:
        pytest.skip(f"{m} is tested in {moment_entry(m)['scenario']}")
    request.node.stash[CITED] = [s.name.split()[1] for s in scenario.steps if s.type == "then"]
    llm = request.getfixturevalue("llm")
    request.node.stash[LLM_FIRST] = len(llm.calls) if llm else 0


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    request.node.stash[FAILED] = {"step": f"{step.keyword} {step.name}", "error": f"{type(exception).__name__}: {exception}"}


def pytest_bdd_after_scenario(request, feature, scenario):
    out_dir = request.config.getoption("out")
    if out_dir:
        write_run(Path(out_dir), request, scenario)


def write_run(out_dir, request, scenario):
    """One transcript file (what the agent saw and did, the rules to label) and one verdict file."""
    cfg = request.config.getoption
    sc_id = scenario.name.split()[0]
    m = cfg("start")
    run_id = cfg("run_id") if m != "start" else f"{cfg('run_id')}-{sc_id}"
    out = request.node.stash.get(OUTCOME, None)
    failed = request.node.stash.get(FAILED, None)
    rules = request.node.stash.get(CITED, [])
    llm = request.getfixturevalue("llm")
    usage = llm.calls[request.node.stash.get(LLM_FIRST, len(llm.calls)):] if llm else []
    (out_dir / "transcripts").mkdir(parents=True, exist_ok=True)
    (out_dir / "verdicts").mkdir(parents=True, exist_ok=True)
    if out:
        run = out["run"]
        transcript = {
            "run_id": run_id, "scenario": title_seen(scenario.name),
            "mode": "one action from a tested moment" if m != "start" else "whole conversation from the start",
            "moment": m if m != "start" else None,
            "situation": moment_entry(m)["situation"] if m != "start" else None,
            "rules_to_label": {r: rule_text(r) for r in rules},
            "after_the_run": after_the_run(run),
            "events": [seen(e, under_test=(i >= run.first_tested)) for i, e in enumerate(run.events)],
            "readable": readable(run),
        }
        (out_dir / "transcripts" / f"{run_id}.json").write_text(json.dumps(transcript, indent=1, ensure_ascii=False))
    record = {"run_id": run_id, "scenario": sc_id, "agent": cfg("agent"), "prompt": cfg("prompt"), "moment": m,
              "status": out["status"] if out else "error", "failed_step": failed,
              "rules": out["rules"] if out else {r: {"verdict": UNDECIDED, "reason": "the run raised"} for r in rules},
              "titles": {r: rule_titles()[r] for r in rules}, "llm_calls": len(usage), "usage": usage}
    if out:
        run = out["run"]
        record |= {"over": run.over, "played": run.played, "lines": run.lines, "stopped": run.stopped,
                   "played_out": out["played_out"], "judge": out["judge"]}
    (out_dir / "verdicts" / f"{run_id}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False))


UNSEEN = ("ids", "means", "answer")


def seen(event, **extra):
    """An event as the transcript shows it: what the agent saw and sent. Left out: the ids the fake issued,
    since a call with no answer issued one (a booking that went through) the agent never saw; and the
    checkers' readings, a visitor line's 'means' and a result's 'answer', which could anchor a label."""
    return {k: v for k, v in event.items() if k not in UNSEEN} | extra


def title_seen(name):
    """The scenario's title without its bracket, which says what an unanswered call really did, as in
    'SC-12 Booking call unanswered (booked)'."""
    return re.sub(r"\s*\([^)]*\)$", "", name)


def after_the_run(run):
    if run.moment:
        nxt = "the conversation is over (the World has no visitor line next)" if run.over else \
            "the conversation goes on (a tool call, or the visitor speaks next)"
        return f"The agent took one action from the tested moment; after it {nxt}."
    return f"Stopped: {run.stopped}; {run.played} of {run.lines} World lines played."


def readable(run):
    lines = []
    for i, e in enumerate(run.events):
        mark = ">> " if i >= run.first_tested and e["kind"] in ("message", "call") else "   "
        if e["kind"] == "visitor":
            lines.append(f"{mark}VISITOR: {e['text']}")
        elif e["kind"] == "message":
            lines.append(f"{mark}AGENT TO VISITOR: {e['text']}")
        elif e["kind"] == "call":
            lines.append(f"{mark}AGENT CALLS {e['tool']} {json.dumps(e['args'], ensure_ascii=False)}")
        else:
            lines.append(f"{mark}BOOKING SYSTEM ANSWERS {json.dumps(e['payload'], ensure_ascii=False)}")
    return lines
