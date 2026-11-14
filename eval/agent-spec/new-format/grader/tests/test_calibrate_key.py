import calibrate_key


def test_findings_fill_empty_worksheet_bodies():
    """Should give all 20 calibration findings a body with a Quote, refilling the six the worksheet left empty."""
    found = calibrate_key.findings()
    assert len(found) == 20
    assert [fid for fid, text in found.items() if "Quote:" not in text] == []


def test_owner_rulings_apply_ruling_4():
    """Should read F2 as Real and F7 and F12 as Style only, per owner ruling 4."""
    owner = calibrate_key.owner_rulings()
    assert len(owner) == 20
    assert (owner["F2"], owner["F7"], owner["F12"]) == ("Real", "Style only", "Style only")
