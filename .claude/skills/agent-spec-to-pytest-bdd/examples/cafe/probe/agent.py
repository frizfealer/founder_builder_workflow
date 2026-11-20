"""What is left of the probe agent: its prompts, how it saw a conversation, and the message judge's LLM call.

The probe agent was one prompt holding rules.md, the four tools, and one LLM call per action. It was not the
product agent; slice A and task 56 used it only to measure whether the tests' verdicts are right on a real
LLM, and task 52 deleted it (the class ProbeAgent and pytest's --agent probe), so probe/run_part2.py and
probe/run_probe2.py no longer run; their saved runs under runs/ stay. Its system prompts are data.json's
probe_prompts, each named by its key: "plain", slice A's two bad prompts "retry" (R-11) and "book-when-held"
(R-03), and task 56's "no-R-11" and "no-R-03", the plain prompt with one rule left out. build_prompt is how
each text is made from rules.md; tests/test_probe2.py keeps the stored texts equal to it. tools and
to_messages are the tools and the Messages API turns it was sent. judge_llm is the message judge's LLM
call, which probe/judge_test.py uses.
"""
import json
import re

from harness.data import data, render, spec_dir, values


def rules_without(text, left_out):
    """rules.md without the given ids: a rule's section, every row of 'What the agent does' that names the
    rule, and a decision's row of 'Decisions'."""
    out, section, skip, found = [], "", False, set()
    for line in text.splitlines(keepends=True):
        if line.startswith("## "):
            section = line[3:].strip()
            skip = next((i for i in left_out if line.startswith(f"## {i} ")), None)
            found |= {skip} if skip else set()
        if skip:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
        if section == "What the agent does" and cells and (hit := set(left_out) & set(re.findall(r"R-\d+", cells[-1]))):
            found |= hit
            continue
        if section == "Decisions" and cells and cells[0] in left_out:
            found.add(cells[0])
            continue
        out.append(line)
    assert found == set(left_out), f"rules.md has nothing to leave out for {sorted(set(left_out) - found)}"
    return "".join(out)


def build_prompt(left_out=(), instruction=None):
    """The probe's system prompt: rules.md, less the ids left out, in slice A's frame, with an instruction
    from the café after it for a bad prompt."""
    rules = rules_without((spec_dir() / "rules.md").read_text(encoding="utf-8"), left_out)
    text = (f"You are the reservation agent of {values()['cafe']}. You talk with one visitor who wants a table, "
            "and you use the booking system's tools. Follow these rules.\n\n"
            f"<rules>\n{rules}</rules>\n\n"
            "Each reply is either one tool call or one message to the visitor.")
    if instruction:
        text += f"\n\nInstruction from the café: {instruction}"
    return text


def system_prompt(prompt):
    """The stored text of a probe prompt, by its name in data.json's probe_prompts."""
    return data()["probe_prompts"][prompt]["value"]


def tools():
    return [{"name": t["name"], "description": t["description"], "input_schema": t["input_schema"]}
            for t in data()["tools"].values()]


def to_messages(events):
    """The events as Messages API turns: the visitor and tool results are the user, the agent the assistant."""
    msgs, n, last_id = [], 0, None

    def add(role, block):
        if msgs and msgs[-1]["role"] == role:
            msgs[-1]["content"].append(block)
        else:
            msgs.append({"role": role, "content": [block]})

    for e in events:
        if e["kind"] == "visitor":
            add("user", {"type": "text", "text": e["text"]})
        elif e["kind"] == "message" and e["text"]:
            add("assistant", {"type": "text", "text": e["text"]})
        elif e["kind"] == "call":
            n += 1
            last_id = render(data()["tool_use_id"]["value"], n=n)
            add("assistant", {"type": "tool_use", "id": last_id, "name": e["tool"], "input": e["args"]})
        elif e["kind"] == "result":
            content = e["payload"] if isinstance(e["payload"], str) else json.dumps(e["payload"], ensure_ascii=False)
            add("user", {"type": "tool_result", "tool_use_id": last_id, "content": content, "is_error": e["is_error"]})
    return msgs


def judge_llm(llm):
    """ask(message, question) -> the LLM's one-word answer, for harness.judge.MessageJudge."""
    instruction = render(data()["judge_instruction"]["value"])

    def ask(message, question):
        # claude-sonnet-5-5 thinks first by default, and a thinking block alone fills 5 tokens with no
        # answer; "between_tools" is how this model takes thinking off.
        r = llm.create("judge", max_tokens=5, thinking={"type": "between_tools"}, system=instruction,
                       messages=[{"role": "user", "content": f"<message>\n{message}\n</message>\n\nQuestion: {question}"}])
        return "".join(b.text for b in r.content if b.type == "text")

    return ask
