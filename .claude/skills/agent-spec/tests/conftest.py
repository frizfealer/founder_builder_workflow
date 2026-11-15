import shutil
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))


@pytest.fixture
def toy(tmp_path):
    """A writable copy of the toy spec folder, with the interview log and input document beside it."""
    dst = tmp_path / "toy"
    shutil.copytree(SKILL / "tests" / "fixtures" / "toy", dst)
    shutil.copytree(SKILL / "tests" / "fixtures" / "toy-product", tmp_path, dirs_exist_ok=True)
    return dst
