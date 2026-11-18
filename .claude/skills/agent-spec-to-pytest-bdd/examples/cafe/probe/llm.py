"""The one doorway to the Claude API for the probe agent and the message judge, with every call's tokens.

anthropic>=2.9 reads the owner's `ant auth login` by itself; no key is read or written here.
When CAFE_USAGE_LEDGER names a file, every call's usage is also appended to it as one JSON line, tagged with
CAFE_USAGE_SOURCE, so a task's money spent counts every call, those of a run that raised included.
"""
import json
import os
from pathlib import Path

MODEL = "claude-sonnet-5-5"
GRADING = Path(__file__).resolve().parents[6] / "eval" / "agent-spec" / "grading.json"
RATES_KEY = "sonnet"  # grading.json model_rates entry for MODEL


def rates():
    """USD per million tokens for MODEL, from grading.json's model_rates."""
    r = json.loads(GRADING.read_text(encoding="utf-8"))["model_rates"][RATES_KEY]
    return {"in": r["in"], "out": r["out"], "cache_read": r["cache_read"]}


def cost(calls):
    """USD for a list of recorded calls. Cache writes, which these runs do not ask for, are priced at the input rate."""
    r = rates()
    return sum((c["input_tokens"] + c["cache_creation_input_tokens"]) * r["in"] + c["output_tokens"] * r["out"]
               + c["cache_read_input_tokens"] * r["cache_read"] for c in calls) / 1e6


class LLM:
    def __init__(self, client=None, model=MODEL):
        if client is None:
            import anthropic
            client = anthropic.Anthropic()
        self.client, self.model = client, model
        self.calls = []  # one row per API call: purpose and the usage fields of the response

    def create(self, purpose, **kw):
        r = self.client.messages.create(model=self.model, **kw)
        u = r.usage
        self.calls.append({"purpose": purpose, "model": self.model,
                           "input_tokens": u.input_tokens, "output_tokens": u.output_tokens,
                           "cache_read_input_tokens": getattr(u, "cache_read_input_tokens", None) or 0,
                           "cache_creation_input_tokens": getattr(u, "cache_creation_input_tokens", None) or 0})
        ledger = os.environ.get("CAFE_USAGE_LEDGER")
        if ledger:
            with open(ledger, "a", encoding="utf-8") as f:
                f.write(json.dumps({"source": os.environ.get("CAFE_USAGE_SOURCE", "")} | self.calls[-1]) + "\n")
        return r
