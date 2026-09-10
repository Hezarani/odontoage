"""API surface + the safety gate that refuses unverified method parameters."""
from unittest import mock

import pytest

import odontoage
import odontoage.core as core
from odontoage.errors import (InvalidInputError, MethodNotVerifiedError,
                              UnknownMethodError)

# A synthetic unverified method used to exercise the safety gate. All six shipped
# methods are now verified, so the gate is tested against this injected fixture
# rather than against real data.
_FAKE_PENDING = {
    "id": "fake_pending", "label": "fake pending method", "family": "kvaal",
    "kind": "regression", "dentition": "adult", "source": "kvaal_1995",
    "verified": False, "status": "pending_sourcing",
    "default_equation": "six_teeth", "equations": {},
}


def test_unknown_method():
    with pytest.raises(UnknownMethodError):
        odontoage.estimate("does_not_exist", sex="male")


def test_pending_method_is_gated():
    # An unverified method must be refused outright (no number returned).
    with mock.patch.object(core._data, "get_method", return_value=_FAKE_PENDING):
        with pytest.raises(MethodNotVerifiedError):
            odontoage.estimate("fake_pending", variables={"M": 0.25, "W_minus_L": 0.06})


def test_allow_unverified_bypasses_gate_but_still_needs_data():
    # allow_unverified must get PAST the gate; it then fails inside the runner because
    # the pending dataset has no usable coefficients - proving the gate is what blocks.
    with mock.patch.object(core._data, "get_method", return_value=_FAKE_PENDING):
        with pytest.raises(InvalidInputError):
            odontoage.estimate("fake_pending", allow_unverified=True,
                               variables={"M": 0.25, "W_minus_L": 0.06})


def test_list_methods_counts():
    all_m = odontoage.list_methods()
    verified = odontoage.list_methods(verified_only=True)
    ids = {m["id"] for m in all_m}
    assert ids == {
        "cameriere_italian_2006", "cameriere_european_2007",
        "cameriere_adult_upper_2009", "cameriere_adult_lower_2009",
        "demirjian_1976", "willems_2001", "kvaal_1995",
    }
    # Every shipped method is now cross-verified.
    assert {m["id"] for m in verified} == ids
    assert all(m["verified"] for m in verified)


def test_compare_runs_only_verified_applicable():
    res = odontoage.compare(sex="male", variables={"x5": 0.06, "N0": 5, "s": 0.42})
    ids = {e.method for e in res}
    assert ids == {"cameriere_italian_2006", "cameriere_european_2007"}
    for e in res:
        assert e.estimated_age_years is not None
        assert e.disclaimer  # every estimate carries the disclaimer


def test_compare_with_stages_runs_staged_methods():
    # Staged input drives the two staged methods (Demirjian score + Willems age);
    # Cameriere is skipped because it needs open-apex measurements, not stages.
    res = odontoage.compare(sex="male",
                            stages={"I1": "H", "I2": "H", "C": "G", "PM1": "F",
                                    "PM2": "E", "M1": "H", "M2": "D"})
    ids = {e.method for e in res}
    assert "willems_2001" in ids and "demirjian_1976" in ids
    assert all(not e.method.startswith("cameriere") for e in res)
