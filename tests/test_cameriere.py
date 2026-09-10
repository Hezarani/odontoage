"""Hand-verified fixtures for the Cameriere open-apex formulas.

These lock the *implementation* to the published *formulae*: each expected value is
computed by hand from the regression and must match to 2 dp. The formulae themselves
are cross-verified against primary sources (see docs/EVIDENCE.md).
"""
import math

import pytest

import odontoage
from odontoage.errors import InvalidInputError


def approx(x):
    return pytest.approx(x, abs=0.01)


def test_european_precomputed_male():
    # 8.387 + 0.282*1 - 1.692*0.06 + 0.835*5 - 0.116*0.42 - 0.139*(0.42*5) = 12.4019
    e = odontoage.estimate("cameriere_european_2007", sex="male",
                           variables={"x5": 0.06, "N0": 5, "s": 0.42})
    assert e.estimated_age_years == approx(12.40)
    assert e.verified is True
    assert e.doi == "10.1007/s00414-007-0179-1"


def test_european_all_apices_closed_female():
    # g=0, x5=0, s=0, N0=7 -> 8.387 + 0.835*7 = 14.232
    e = odontoage.estimate("cameriere_european_2007", sex="female",
                           variables={"x5": 0.0, "N0": 7, "s": 0.0})
    assert e.estimated_age_years == approx(14.232)


def test_italian_all_apices_closed_female():
    # g=0, x5=0, s=0, N0=7 -> 8.971 + 0.674*7 = 13.689
    e = odontoage.estimate("cameriere_italian_2006", sex="female",
                           variables={"x5": 0.0, "N0": 7, "s": 0.0})
    assert e.estimated_age_years == approx(13.689)


def test_italian_precomputed_male():
    # 8.971 + 0.375 + 1.631*0.5 + 0.674*3 - 1.034*1.5 - 0.176*(1.5*3) = 9.8405
    e = odontoage.estimate("cameriere_italian_2006", sex="male",
                           variables={"x5": 0.5, "N0": 3, "s": 1.5})
    assert e.estimated_age_years == approx(9.8405)


def test_italian_and_european_differ():
    a = odontoage.estimate("cameriere_italian_2006", sex="male",
                           variables={"x5": 0.06, "N0": 5, "s": 0.42})
    b = odontoage.estimate("cameriere_european_2007", sex="male",
                           variables={"x5": 0.06, "N0": 5, "s": 0.42})
    assert abs(a.estimated_age_years - b.estimated_age_years) > 0.05


def test_teeth_dict_matches_precomputed_variables():
    # PM1 open x=0.02, PM2 open x=0.05, rest closed -> N0=5, s=0.07, x5=0.05
    teeth = {
        "I1": {"closed": True}, "I2": {"closed": True}, "C": {"closed": True},
        "PM1": {"open": True, "Ai": 0.42, "Li": 21.0},   # 0.02
        "PM2": {"open": True, "Ai": 1.05, "Li": 21.0},   # 0.05
        "M1": {"closed": True}, "M2": {"closed": True},
    }
    from_teeth = odontoage.estimate("cameriere_european_2007", sex="male", teeth=teeth)
    from_vars = odontoage.estimate("cameriere_european_2007", sex="male",
                                   variables={"x5": 0.05, "N0": 5, "s": 0.07})
    assert from_teeth.estimated_age_years == approx(from_vars.estimated_age_years)


def test_missing_tooth_raises():
    with pytest.raises(InvalidInputError):
        odontoage.estimate("cameriere_european_2007", sex="male",
                           teeth={"I1": {"closed": True}})


def test_missing_sex_raises():
    with pytest.raises(InvalidInputError):
        odontoage.estimate("cameriere_european_2007",
                           variables={"x5": 0.0, "N0": 7, "s": 0.0})


def test_bad_length_raises():
    teeth = {t: {"closed": True} for t in ["I1", "I2", "C", "PM1", "M1", "M2"]}
    teeth["PM2"] = {"open": True, "Ai": 1.0, "Li": 0.0}
    with pytest.raises(InvalidInputError):
        odontoage.estimate("cameriere_european_2007", sex="male", teeth=teeth)
