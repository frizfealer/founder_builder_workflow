# Rule checkers and the message judge

A rule checker is a function `(events, over, ask) -> (verdict, reason)` that reads the recorded events of one run and says whether one rule of `rules.md` held. The café's `harness/checkers.py` has one per rule, R-01 to R-11.

## Verdicts

- **holds**: the rule held, including when the run never met the case it is about ("no booking call answered booked"). Every checker runs on every scenario through the closing sentence "no other rule is broken", so a rule that does not apply holds.
- **breaks**: the agent did what the rule forbids, or ended its turn without what the rule asks.
- **undecided**: the rule asks for something the agent has not done yet and still could, because the run stopped before the conversation, or the agent's turn, was over. A judge that cannot answer also leaves the rule undecided.

A scenario's test fails on any break, and has no verdict, which also fails, on any undecided or when it did not play every World line.

## Writing a checker

- **First docstring sentence**: the rule's id and title, then exactly what the checker tests. A reader compares this sentence with the rule's text.
- **What it compares**: which kind of tool was called (through the data file's tool kinds), with which ids and values. A tool's name or a value's format is the data file's free choice and carries no verdict.
- **What it asks**: every question about what a message means goes to the judge, `ask(text, question)`, one yes/no question named in the data file's `judge_questions`. Exact facts, such as a confirmation id inside a message, are a string test.
- **The turn rule** (the owner's ruling of 2026-11-19 on the café): a rule of the shape "the agent tells the visitor X and asks Y" reads all the agent's messages of one turn together, one message or several. A turn is everything the agent does before it waits for the visitor. The checker breaks the rule only when the turn ended without every part, and is undecided while the turn is still open.
- **Where another rule owns the case**: when the table "What the agent does" gives a row to another rule, the checker stops there on purpose and says so in a comment (the café's R-04 at a release with no answer, a row of R-06), and `unchecked_sentences.json` lists it.
- **The reason**: names the event index and what the agent did, so a failing test says what went wrong.

## Each checker's tests

- an agent that breaks the rule gets breaks, and the reference agent gets holds on every scenario;
- for a rule under the turn rule: two parts in two messages of one turn hold, and a turn ending with one part breaks;
- a failing Then quotes the rule's full text from `rules.md` and every message and call of the agent.

Café: `tests/test_slice_b.py`.

## Unchecked sentences

`unchecked_sentences.json` lists, per rule of `rules.md`, each sentence of the rule that its checker does not check, or checks only in part. Start from [the template](../assets/unchecked_sentences.template.json). Each item quotes the sentence word for word, says the part not checked, and gives the reason. An empty list means the checker checks every sentence. A test checks that every rule is there and every quote is in its rule's text.

## The message judge

`harness/judge.py`'s `MessageJudge` answers a sentence of the data file's `agent` section from the `judge` answers recorded beside it, with no model call. Any other sentence goes to an LLM; a judge built without one raises, and the checker's verdict is undecided. So a lane 1 run, with the reference agent or a variant, makes no model call, and a test shows every judge answer of a run came from the data file.

A real agent words its messages freely, so its runs need the LLM judge, and the judge's questions need a direct test. When a checker asks a new question, add cases for it to the judge cases file in the café's `judge_cases.json` form: some messages that should get yes in free wording, more that should get no. Do not run them: each case costs a model call per repeat, and the run waits for the owner's go. Report how many you added.
