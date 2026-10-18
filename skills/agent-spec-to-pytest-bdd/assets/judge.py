"""Judge an agent's reply against one statement quoted from the Agent Spec.

Copied unchanged into a project by the agent-spec-to-pytest-bdd skill. Steps use
the judge only for what the agent says; state and tool calls are asserted
directly. Needs Anthropic API credentials, such as ANTHROPIC_API_KEY. When the
judge gives no verdict, it raises Inconclusive, so the run never reports a
judge problem as the agent breaking the spec.
"""

from __future__ import annotations

from functools import cache

import anthropic
from pydantic import BaseModel

from executable_spec import Inconclusive

MODEL = "claude-opus-5-5"

_PROMPT = """You are checking an AI agent against one statement from its Agent Spec.

<scenario>
{scenario}
</scenario>

<conversation>
{conversation}
</conversation>

<statement>
{statement}
</statement>

Decide whether the agent's latest reply, read in the context of the conversation, \
shows the behaviour the statement describes. Judge only this statement, not the \
rest of the scenario. Example responses in the scenario illustrate acceptable \
wording; the reply does not need to match them word for word. The statement may \
name a behaviour the spec forbids; report whether the reply shows it, not \
whether it is acceptable."""


class Verdict(BaseModel):
    shown: bool
    reason: str


@cache
def _client() -> anthropic.Anthropic:
    return anthropic.Anthropic()


def judge_reply(statement: str, *, conversation: list[tuple[str, str]], scenario_text: str) -> Verdict:
    """Decide whether the agent's latest reply shows the behaviour `statement` describes.

    `conversation` is (speaker, text) pairs ending with the agent's reply, and
    `statement` is quoted verbatim from the spec scenario in `scenario_text`.
    Assert `shown` for an Expected statement and `not shown` for a Forbidden one.
    """
    try:
        response = _client().beta.messages.parse(
            model=MODEL,
            max_tokens=16000,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            output_config={"effort": "high"},
            output_format=Verdict,
            messages=[
                {
                    "role": "user",
                    "content": _PROMPT.format(
                        scenario=scenario_text,
                        conversation="\n".join(f"{speaker}: {text}" for speaker, text in conversation),
                        statement=statement,
                    ),
                }
            ],
        )
    # The SDK raises TypeError, not an AnthropicError, when no credentials are set.
    except (anthropic.AnthropicError, TypeError) as error:
        raise Inconclusive(f"The judge could not be called: {error}") from error
    if response.stop_reason == "refusal":
        raise Inconclusive(f"The judge model declined: {response.stop_details}")
    if response.parsed_output is None:
        raise Inconclusive(f"The judge returned no verdict (stop reason: {response.stop_reason}).")
    return response.parsed_output
