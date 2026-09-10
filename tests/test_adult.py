"""Hand-verified fixtures for the adult methods: Cameriere pulp/tooth AREA ratio
(2009) and Kvaal (1995) pulp/tooth size ratios.

Each expected value is computed by hand from the published regression and must match
to 2 dp. The formulae are transcribed from the primary papers rendered at full
resolution (see docs/EVIDENCE.md).
"""
import pytest

import odontoage
from odontoage.errors import InvalidInputError


def approx(x):
    return pytest.approx(x, abs=0.01)


# --------------------------------------------------------------------------- #
# Cameriere adult (2009): Age = intercept + slope * RA                         #
# --------------------------------------------------------------------------- #

def test_cameriere_adult_upper():
    # 100.598 - 544.433 * 0.08 = 57.04336
    e = odontoage.estimate("cameriere_adult_upper_2009", variables={"RA": 0.08})
    assert e.estimated_age_years == approx(57.0434)
    assert e.verified is True
    assert e.doi == "10.1016/j.forsciint.2009.09.011"
    assert e.interval is not None and e.interval.low < e.estimated_age_years < e.interval.high


def test_cameriere_adult_lower():
    # 91.362 - 480.901 * 0.08 = 52.88992
    e = odontoage.estimate("cameriere_adult_lower_2009", variables={"RA": 0.08})
    assert e.estimated_age_years == approx(52.8899)


def test_cameriere_adult_ratio_alias():
    # 'ratio' is accepted as an alias for RA.
    a = odontoage.estimate("cameriere_adult_upper_2009", variables={"RA": 0.12})
    b = odontoage.estimate("cameriere_adult_upper_2009", variables={"ratio": 0.12})
    assert a.estimated_age_years == approx(b.estimated_age_years)


def test_cameriere_adult_is_monotonic_decreasing():
    young = odontoage.estimate("cameriere_adult_upper_2009", variables={"RA": 0.14})
    old = odontoage.estimate("cameriere_adult_upper_2009", variables={"RA": 0.06})
    assert old.estimated_age_years > young.estimated_age_years


def test_cameriere_adult_missing_ratio_raises():
    with pytest.raises(InvalidInputError):
        odontoage.estimate("cameriere_adult_upper_2009", variables={"foo": 1})


def test_cameriere_adult_out_of_range_ratio_raises():
    for bad in (0.0, -0.1, 1.0, 2.5):
        with pytest.raises(InvalidInputError):
            odontoage.estimate("cameriere_adult_upper_2009", variables={"RA": bad})


# --------------------------------------------------------------------------- #
# Kvaal (1995): nine equations, first predictor M, second predictor (W - L)    #
# --------------------------------------------------------------------------- #

def test_kvaal_six_teeth_default():
    # default equation is six_teeth: 129.8 - 316.4*0.25 - 66.8*0.05 = 47.36
    e = odontoage.estimate("kvaal_1995", variables={"M": 0.25, "W_minus_L": 0.05})
    assert e.estimated_age_years == approx(47.36)
    assert e.verified is True
    assert e.doi == "10.1016/0379-0738(95)01760-G"


def test_kvaal_maxillary_three_via_W_and_L():
    # 120.0 - 256.6*0.22 - 45.3*(0.30-0.24) = 60.83
    e = odontoage.estimate("kvaal_1995", equation="maxillary_three",
                           variables={"M": 0.22, "W": 0.30, "L": 0.24})
    assert e.estimated_age_years == approx(60.83)


def test_kvaal_mandibular_canine_has_no_second_predictor():
    # 158.8 - 255.7*0.30 = 82.09 ; supplying W-L must not change the result.
    a = odontoage.estimate("kvaal_1995", equation="mandibular_canine",
                           variables={"M": 0.30})
    b = odontoage.estimate("kvaal_1995", equation="mandibular_canine",
                           variables={"M": 0.30, "W_minus_L": 0.9})
    assert a.estimated_age_years == approx(82.09)
    assert b.estimated_age_years == approx(82.09)


def test_kvaal_lateral_incisor_gender_shifts_by_six_years():
    # 32/42 carries -6.0*(G). Male (G=1) is exactly 6 years younger than female (G=0).
    male = odontoage.estimate("kvaal_1995", equation="mandibular_lateral_incisor",
                              sex="male", variables={"M": 0.25, "W_minus_L": 0.05})
    female = odontoage.estimate("kvaal_1995", equation="mandibular_lateral_incisor",
                                sex="female", variables={"M": 0.25, "W_minus_L": 0.05})
    assert male.estimated_age_years == approx(34.615)
    assert female.estimated_age_years == approx(40.615)
    assert female.estimated_age_years - male.estimated_age_years == approx(6.0)


def test_kvaal_lateral_incisor_requires_sex():
    with pytest.raises(InvalidInputError):
        odontoage.estimate("kvaal_1995", equation="mandibular_lateral_incisor",
                           variables={"M": 0.25, "W_minus_L": 0.05})


def test_kvaal_missing_M_raises():
    with pytest.raises(InvalidInputError):
        odontoage.estimate("kvaal_1995", variables={"W_minus_L": 0.05})


def test_kvaal_missing_second_predictor_raises():
    # six_teeth needs the second predictor; supplying only M must fail.
    with pytest.raises(InvalidInputError):
        odontoage.estimate("kvaal_1995", variables={"M": 0.25})


def test_kvaal_unknown_equation_raises():
    with pytest.raises(InvalidInputError):
        odontoage.estimate("kvaal_1995", equation="no_such_tooth",
                           variables={"M": 0.25, "W_minus_L": 0.05})


def test_kvaal_all_nine_equations_produce_numbers():
    m = odontoage.list_methods()
    kvaal = next(x for x in m if x["id"] == "kvaal_1995")
    assert kvaal["verified"] is True
    # Exercise every equation with a plausible input set.
    from odontoage import _data
    eqs = _data.get_method("kvaal_1995")["equations"]
    assert len(eqs) == 9
    for name in eqs:
        e = odontoage.estimate("kvaal_1995", equation=name, sex="female",
                               variables={"M": 0.22, "W_minus_L": 0.05})
        assert e.estimated_age_years is not None
