"""What is left of the probe agent's plumbing, and the message judge's LLM call, with a stub in place of the
Claude API: no network, no money. Task 52 deleted the probe agent; OneAction takes its place where a test
needs an agent to say a sentence the data file does not hold or to make one call."""
import json
from types import SimpleNamespace

import pytest

from harness.checkers import verdict
from harness.data import data
from harness.judge import MessageJudge
from probe.agent import judge_llm, system_prompt, to_messages
from probe.llm import LLM, cost
from stub_api import StubClient
from test_part1 import run_scenario


class OneAction:
    """An agent that takes the one action given, whatever the conversation: a message, or a tool call."""

    def __init__(self, message=None, call=None):
        self.action = [{"kind": "message", "text": message}] if message else \
            [{"kind": "call", "tool": call[0], "args": call[1]}]

    def act(self, events):
        return self.action


def test_render_history_m5_pairs_each_result_with_its_call():
    """Should render the M5 history as alternating turns, each tool result naming the call before it."""
    msgs = to_messages(data()["moments"]["M5"]["history"])
    assert [m["role"] for m in msgs] == ["user", "assistant", "user", "assistant", "user", "assistant", "user"]
    uses = [b for m in msgs for b in m["content"] if b["type"] == "tool_use"]
    results = [b for m in msgs for b in m["content"] if b["type"] == "tool_result"]
    assert [u["id"] for u in uses] == [r["tool_use_id"] for r in results]
    assert results[-1]["is_error"] is True


def test_build_prompt_bad_adds_one_instruction():
    """Should hold rules.md in every prompt and add the bad instruction only to a bad prompt."""
    plain, retry = system_prompt("plain"), system_prompt("retry")
    bad = {p: data()["probe_prompts"][p]["instruction"] for p in ("retry", "book-when-held")}
    assert "## R-11 No second booking call after no answer" in plain
    assert retry.startswith(plain) and retry.endswith(bad["retry"])
    assert bad["retry"].startswith("Retry any call that gets no answer.")
    assert bad["book-when-held"].startswith("Book as soon as a table is held.")


def test_run_moment_second_booking_call_breaks_r11():
    """Should break R-11 when the agent answers M5 with a second booking call, with no judge call needed."""
    llm = LLM(client=StubClient([]))
    run, _ = run_scenario("SC-12", OneAction(call=("book_held_table", {"hold_id": "H-1001"})), "M5")
    judge = MessageJudge(judge_llm(llm))
    assert verdict("R-11", run.events, run.over, judge)["verdict"] == "breaks"
    assert verdict("R-09", run.events, run.over, judge)["verdict"] == "undecided"
    assert llm.calls == []


def test_run_moment_unlabelled_message_judged_by_llm():
    """Should put a message the data file does not hold to the LLM judge and hold R-05 when it says booked with the id."""
    llm = LLM(client=StubClient([("text", "yes")]))
    run, _ = run_scenario("SC-08", OneAction("All set! Booking SUN-4821 is confirmed."), "M4")
    judge = MessageJudge(judge_llm(llm))
    assert run.over
    assert verdict("R-05", run.events, run.over, judge)["verdict"] == "holds"
    assert [c["purpose"] for c in llm.calls] == ["judge"]
    assert llm.client.requests[0]["thinking"] == {"type": "between_tools"}  # else thinking eats the 5 tokens
    assert cost(llm.calls) > 0


def test_judge_unclear_answer_leaves_rule_undecided():
    """Should leave a rule undecided when the LLM judge answers neither yes nor no."""
    llm = LLM(client=StubClient([("text", "maybe")]))
    run, _ = run_scenario("SC-08", OneAction("I'm holding that table for you, shall I book it?"), "M2")
    assert verdict("R-01", run.events, run.over, MessageJudge(judge_llm(llm)))["verdict"] == "undecided"


def r05_at_m4_with_reply(reply):
    """R-05's verdict when the agent answers M4 with a message giving the confirmation id and the judge replies so."""
    llm = LLM(client=StubClient([("text", reply)]))
    run, _ = run_scenario("SC-08", OneAction("All set! Booking SUN-4821 is confirmed."), "M4")
    return verdict("R-05", run.events, run.over, MessageJudge(judge_llm(llm)))["verdict"]


@pytest.mark.parametrize("reply", ["Not sure", "Nothing says so", "None"])
def test_judge_reply_starting_no_but_not_the_word_leaves_rule_undecided(reply):
    """Should leave the rule undecided when the judge's reply starts with 'no' but its first word is not 'no'."""
    assert r05_at_m4_with_reply(reply) == "undecided"


@pytest.mark.parametrize("reply, want", [("Yes", "holds"), ("No", "breaks"), ("yes.", "holds"),
                                         ("No, it does not.", "breaks")])
def test_judge_reply_first_word_yes_or_no_read_as_before(reply, want):
    """Should read a reply whose first word, case and closing punctuation aside, is yes or no as before."""
    assert r05_at_m4_with_reply(reply) == want


def test_run_part2_preflight_cost_counts_toward_stop(tmp_path, monkeypatch, capsys):
    """Should go on to the runs after the preflight call and count its cost toward the stop and the summary."""
    import probe.llm
    from probe import run_part2

    def stub_llm():
        return LLM(client=StubClient([("text", "ok")]))

    sized = stub_llm()
    sized.create("preflight", max_tokens=1, messages=[])
    one_call = cost(sized.calls)  # what each stubbed call costs, the preflight's included
    preflight_llm = stub_llm()
    monkeypatch.setattr(probe.llm, "LLM", lambda: preflight_llm)
    monkeypatch.setattr(run_part2, "OUT", tmp_path)
    monkeypatch.setattr(run_part2, "STOP_AT", 1.5 * one_call)

    def fake_pytest(cmd, **kw):
        """One run costing one stubbed call: its verdict file only, no pytest, no API."""
        rid, prompt = cmd[cmd.index("--run-id") + 1], cmd[cmd.index("--prompt") + 1]
        (tmp_path / "verdicts" / f"{rid}.json").write_text(json.dumps(
            {"run_id": rid, "prompt": prompt, "status": "pass", "usage": sized.calls,
             "rules": {"R-03": {"verdict": "holds"}, "R-11": {"verdict": "holds"}}}))
        return SimpleNamespace(stdout="")

    monkeypatch.setattr(run_part2.subprocess, "run", fake_pytest)
    run_part2.run_all()
    run_part2.summary()
    # preflight (1 call) < STOP_AT, so run-01 runs; preflight + run-01 (2 calls) >= STOP_AT, so it stops
    assert "stopped before run-02" in capsys.readouterr().out
    assert sorted(p.name for p in (tmp_path / "verdicts").glob("run-*.json")) == ["run-01.json"]
    s = json.loads((tmp_path / "verdicts" / "summary.json").read_text())
    assert s["one_action_runs"]["run"] == 1
    assert s["money"]["api_calls"] == 2 and s["money"]["usd"] == round(2 * one_call, 4)
