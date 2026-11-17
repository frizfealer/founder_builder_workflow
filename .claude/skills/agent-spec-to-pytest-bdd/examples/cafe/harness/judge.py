"""The message judge: one yes/no question about one agent message.

A sentence of data.json's 'agent' section is answered from the answers recorded beside it, with no
LLM. Any other sentence goes to `ask_llm(message, question) -> "yes" | "no" | other text`; without
one the judge raises, so a run of the reference agent cannot make an LLM call by accident.
"""
from harness.data import data, render, values


class NoLLM(Exception):
    """A message the data file does not hold reached a judge that has no LLM."""


class Unclear(Exception):
    """The LLM answered neither yes nor no."""


def known_sentences():
    """{sentence text: recorded answers} for every agent sentence of the data file, with each id it can carry."""
    out = {}
    for entry in data()["agent"].values():
        for cid in values()["confirmation_ids"]:
            out[render(entry["value"], confirmation_id=cid)] = entry["judge"]
    return out


def question_text(question):
    return render(data()["judge_questions"][question]["value"])


class MessageJudge:
    def __init__(self, ask_llm=None):
        self.ask_llm = ask_llm
        self.asked = []  # every question put, in order: message, question, answer, source
        self._known = known_sentences()
        self._cache = {}

    def __call__(self, message, question):
        key = (message, question)
        if key not in self._cache:
            self._cache[key] = self._ask(message, question)
        return self._cache[key]

    def llm_calls(self):
        return sum(1 for a in self.asked if a["source"] == "llm")

    def _ask(self, message, question):
        if message in self._known:
            answer = self._known[message][question]
            self.asked.append({"message": message, "question": question, "answer": answer, "source": "data file"})
            return answer
        if self.ask_llm is None:
            raise NoLLM(f"no LLM judge for a message the data file does not hold: {message!r}")
        reply = self.ask_llm(message, question_text(question))
        word = reply.strip().lower().rstrip(".")
        answer = True if word.startswith("yes") else False if word.startswith("no") else None
        self.asked.append({"message": message, "question": question, "answer": answer, "source": "llm",
                           "reply": reply})
        if answer is None:
            raise Unclear(f"judge answered {reply!r} to {question}")
        return answer
