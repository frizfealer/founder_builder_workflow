import json

import grade_spec


def write_log(tmp_path, questions):
    (tmp_path / "interview-log.json").write_text(json.dumps({"questions": questions}))
    return tmp_path


def test_interview_counts_questions_and_flags(tmp_path):
    """Should count every logged question and every distinct claim named in a question's closing mark."""
    trial = write_log(tmp_path, [
        {"n": 1, "question": "q1", "recommended": "r", "reply": "Yes.", "answered_by": "record"},
        {"n": 2, "question": "Does a lookup show a refund at once? Claims put to the owner: C-07, C-10.",
         "recommended": "r", "reply": "Yes.", "answered_by": "record"},
        {"n": 3, "question": "Can an order ship in parts? Claims put to the owner: C-10.", "recommended": "r",
         "reply": "Yes.", "answered_by": "stand-in default"},
    ])
    got = grade_spec.interview(trial)
    assert got["questions_asked"] == 3
    assert got["owner_flags"] == 2


def test_interview_without_flags_counts_zero(tmp_path):
    """Should report 0 owner flags when no question carries the closing mark."""
    trial = write_log(tmp_path, [{"n": 1, "question": "q", "recommended": "r", "reply": "Yes.",
                                  "answered_by": "record"}])
    assert grade_spec.interview(trial)["owner_flags"] == 0


def test_interview_without_log_is_null(tmp_path):
    """Should report both new metrics as null when the trial has no interview log."""
    got = grade_spec.interview(tmp_path)
    assert got["questions_asked"] is None and got["owner_flags"] is None
