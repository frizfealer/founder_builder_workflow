"""A stub in place of the Claude API: no network, no money.

Tests pass StubClient to probe.llm.LLM.
"""
from types import SimpleNamespace


class StubClient:
    """Answers messages.create with the next canned reply: ('text', str), ('tool', name, args) or
    ('raise', message), the last as an API error would."""

    def __init__(self, replies):
        self.replies, self.requests = list(replies), []
        self.messages = self

    def create(self, **kw):
        self.requests.append(kw)
        kind, *rest = self.replies.pop(0)
        if kind == "raise":
            raise RuntimeError(rest[0])
        block = SimpleNamespace(type="text", text=rest[0]) if kind == "text" else \
            SimpleNamespace(type="tool_use", name=rest[0], input=rest[1], id="toolu_x")
        return SimpleNamespace(content=[block], usage=SimpleNamespace(input_tokens=1000, output_tokens=100,
                                                                      cache_read_input_tokens=0,
                                                                      cache_creation_input_tokens=0))
