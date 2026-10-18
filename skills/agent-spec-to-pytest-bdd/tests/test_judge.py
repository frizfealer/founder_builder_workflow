import sys
from pathlib import Path
from types import SimpleNamespace

import anthropic
import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))

import judge  # noqa: E402
from executable_spec import Inconclusive  # noqa: E402

CONVERSATION = [("User", "Book Cafe Roma Friday at 7pm under Alex."), ("Agent", "How many people?")]


def client_whose_parse(parse):
    return SimpleNamespace(beta=SimpleNamespace(messages=SimpleNamespace(parse=parse)))


def test_judge_reply_unreachable_judge_is_inconclusive(monkeypatch):
    """Should raise Inconclusive, not a failure, when the judge cannot be called."""

    def parse(**_):
        raise anthropic.APIConnectionError(request=httpx.Request("POST", "https://api.anthropic.com/v1/messages"))

    monkeypatch.setattr(judge, "_client", lambda: client_whose_parse(parse))

    with pytest.raises(Inconclusive):
        judge.judge_reply("The agent resolves the party size.", conversation=CONVERSATION, scenario_text="CR-S02")


def test_judge_reply_refusal_is_inconclusive(monkeypatch):
    """Should raise Inconclusive when the judge model declines to give a verdict."""
    refusal = SimpleNamespace(stop_reason="refusal", stop_details=None, parsed_output=None)
    monkeypatch.setattr(judge, "_client", lambda: client_whose_parse(lambda **_: refusal))

    with pytest.raises(Inconclusive):
        judge.judge_reply("The agent resolves the party size.", conversation=CONVERSATION, scenario_text="CR-S02")
