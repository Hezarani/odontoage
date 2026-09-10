"""Demirjian (1976) 7-tooth maturity-score fixtures, validated against the paper's
built-in checksum (stage-H scores sum to 100) and per-tooth monotonicity."""
import pytest

import odontoage
from odontoage import _data
from odontoage.errors import InvalidInputError
from odontoage.methods.base import TEETH

ALL = lambda s: {t: s for t in TEETH}
STAGE_ORDER = ["0", "A", "B", "C", "D", "E", "F", "G", "H"]


def test_all_stage_H_scores_100_boys():
    e = odontoage.estimate("demirjian_1976", sex="male", stages=ALL("H"))
    assert e.maturity_score == pytest.approx(100.0, abs=0.05)
    assert e.estimated_age_years is None  # score-only; age via Willems


def test_all_stage_H_scores_100_girls():
    e = odontoage.estimate("demirjian_1976", sex="female", stages=ALL("H"))
    assert e.maturity_score == pytest.approx(100.1, abs=0.05)  # rounding in the source


def test_all_stage_G_boys_worked_sum():
    # 12.8+13.9+12.5+15.5+11.4+10.5+11.2 = 87.8
    e = odontoage.estimate("demirjian_1976", sex="male", stages=ALL("G"))
    assert e.maturity_score == pytest.approx(87.8, abs=0.05)


def test_scores_strictly_increase_by_stage_per_tooth():
    m = _data.get_method("demirjian_1976")
    for sex in ("male", "female"):
        for tooth, smap in m["scores"][sex].items():
            present = [s for s in STAGE_ORDER if s in smap]
            vals = [float(smap[s]) for s in present]
            assert vals == sorted(vals), f"{sex}/{tooth}: scores not increasing {vals}"
            assert vals[0] == 0.0, f"{sex}/{tooth}: first defined score should be 0.0"


def test_stage_not_defined_for_tooth_raises():
    # M1 has no stage 'A' in the table (it develops early); inputting it is invalid.
    stages = ALL("H")
    stages["M1"] = "A"
    with pytest.raises(InvalidInputError):
        odontoage.estimate("demirjian_1976", sex="male", stages=stages)


def test_absent_tooth_counts_zero():
    stages = ALL("H")
    stages["M2"] = "0"  # M2 stage 0 scores 0.0
    e = odontoage.estimate("demirjian_1976", sex="male", stages=stages)
    assert e.maturity_score == pytest.approx(100.0 - 13.6, abs=0.05)
