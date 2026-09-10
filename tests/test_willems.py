"""Willems (2001) direct-age fixtures. Willems values are ANOVA-adapted year
contributions (non-monotonic, some negative) summed directly to an age, so there is
no sum-to-100 checksum; we validate the all-stage-H developmental ceiling and the
documented negative values instead."""
import pytest

import odontoage
from odontoage import _data
from odontoage.methods.base import TEETH

ALL = lambda s: {t: s for t in TEETH}


def test_all_H_boys_ceiling():
    # 2.19+1.64+1.9+2.83+1.15+2.15+4.17 = 16.03
    e = odontoage.estimate("willems_2001", sex="male", stages=ALL("H"))
    assert e.estimated_age_years == pytest.approx(16.03, abs=0.01)
    assert e.interval is not None  # Willems has a reported error term


def test_all_H_girls_ceiling():
    # 3.14+0.7+2.0+2.19+1.51+2.21+4.04 = 15.79
    e = odontoage.estimate("willems_2001", sex="female", stages=ALL("H"))
    assert e.estimated_age_years == pytest.approx(15.79, abs=0.01)


def test_all_G_boys_worked_sum():
    # 2.07+1.32+1.09+2.43+0.4+1.95+2.48 = 11.74
    e = odontoage.estimate("willems_2001", sex="male", stages=ALL("G"))
    assert e.estimated_age_years == pytest.approx(11.74, abs=0.01)


def test_documented_negative_values_present():
    m = _data.get_method("willems_2001")
    assert m["tables"]["female"]["PM1"]["A"] < 0  # -0.95 (ANOVA multicolinearity artifact)
    assert m["tables"]["female"]["PM2"]["A"] < 0  # -0.19


def test_mixed_case_girls():
    # I1 G 3.19 + I2 F 0.49 + C E 0.62 + PM1 D 0.41 + PM2 C 0.27 + M1 E 0.9 + M2 F 1.28
    stages = {"I1": "G", "I2": "F", "C": "E", "PM1": "D", "PM2": "C", "M1": "E", "M2": "F"}
    e = odontoage.estimate("willems_2001", sex="female", stages=stages)
    assert e.estimated_age_years == pytest.approx(7.16, abs=0.01)
