import shutil
import sys
from pathlib import Path

import pytest

GRADER = Path(__file__).resolve().parents[1]
NEW_FORMAT = GRADER.parent
EVAL = NEW_FORMAT.parent
sys.path.insert(0, str(GRADER))


@pytest.fixture
def seeded():
    return NEW_FORMAT / "seeded"


@pytest.fixture
def clean():
    return NEW_FORMAT / "seeded-clean"


@pytest.fixture
def units():
    return GRADER / "answer-units.json"


@pytest.fixture
def copy_of(tmp_path):
    """A writable copy of a fixture folder, so a test can damage one file."""
    def make(src):
        dst = tmp_path / src.name
        shutil.copytree(src, dst)
        return dst
    return make
