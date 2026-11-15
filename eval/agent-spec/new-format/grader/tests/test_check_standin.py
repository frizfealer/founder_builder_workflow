import json
import subprocess
import sys

import check_standin
from conftest import GRADER

SECOND_CANCEL = {
    "n": 14,
    "question": "After a cancel call gets no answer, the agent looks the order up and, if it is still placed or processing, sends the cancel once more. Nothing says what happens when that second cancel call also gets no answer. What ends it?",
    "recommended": "The agent sends no third cancel call, says it is not known whether the order was cancelled, issues no refund, and creates a follow-up task for staff with the reason cancellation unknown.",
    "reply": "Yes, I accept your recommendation.",
    "answered_by": "stand-in default",
}
FROM_RECORD = {
    "n": 15,
    "question": "Which statuses can be cancelled?",
    "recommended": "",
    "reply": "> Cancellable while placed or processing, no time limit.",
    "answered_by": "record",
}


def run(tmp_path, questions):
    (tmp_path / "interview-log.json").write_text(json.dumps({"questions": questions}), encoding="utf-8")
    return subprocess.run([sys.executable, str(GRADER / "check_standin.py"), str(tmp_path)], capture_output=True, text=True)


def test_passages_come_from_the_readable_record_only():
    """Should take passages from the interview sections of the review packet, and none from its tool-set table."""
    texts = check_standin.passages()
    assert "Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." in texts
    assert not any(t.startswith("Supporting-actor guarantees") for t in texts)
    assert "An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing." in texts


def test_nearest_finds_the_cancel_timeout_answer():
    """Should pick round 3 Q4, the owner's cancel-timeout answer, as nearest to the second-cancel question."""
    passage, _ = check_standin.nearest(SECOND_CANCEL["question"] + " " + SECOND_CANCEL["recommended"], check_standin.passages())
    assert passage.startswith("Q4 If the cancel call times out")


def test_main_prints_default_beside_nearest_passage(tmp_path):
    """Should print a stand-in default's recommendation and its nearest record passage, and nothing of the kind for a record answer."""
    out = run(tmp_path, [SECOND_CANCEL, FROM_RECORD]).stdout
    assert "recommended: The agent sends no third cancel call" in out
    assert "nearest record passage" in out and "Q4 If the cancel call times out" in out
    assert out.count("nearest record passage") == 1
    assert "2 questions, 1 from the record, 1 stand-in defaults, 0 with a quote not in the record." in out
