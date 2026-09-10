"""Python <-> JavaScript parity: the shipped browser engine must return the same
age as the Python package for identical inputs (to 1e-6). This is what lets the web
demo and the library be cited as one implementation."""
import json
import os
import shutil
import subprocess

import pytest

import odontoage

FIXTURES = [
    {"method": "cameriere_european_2007", "sex": "male", "variables": {"x5": 0.06, "N0": 5, "s": 0.42}},
    {"method": "cameriere_european_2007", "sex": "female", "variables": {"x5": 0.0, "N0": 7, "s": 0.0}},
    {"method": "cameriere_italian_2006", "sex": "male", "variables": {"x5": 0.5, "N0": 3, "s": 1.5}},
    {"method": "cameriere_italian_2006", "sex": "female", "variables": {"x5": 0.0, "N0": 7, "s": 0.0}},
    {"method": "cameriere_european_2007", "sex": "male", "teeth": {
        "I1": {"closed": True}, "I2": {"closed": True}, "C": {"closed": True},
        "PM1": {"open": True, "Ai": 0.42, "Li": 21.0},
        "PM2": {"open": True, "Ai": 1.05, "Li": 21.0},
        "M1": {"closed": True}, "M2": {"closed": True}}},
    {"method": "willems_2001", "sex": "male",
     "stages": {"I1": "H", "I2": "H", "C": "H", "PM1": "H", "PM2": "H", "M1": "H", "M2": "H"}},
    {"method": "willems_2001", "sex": "female",
     "stages": {"I1": "G", "I2": "F", "C": "E", "PM1": "D", "PM2": "C", "M1": "E", "M2": "F"}},
    # Adult methods
    {"method": "cameriere_adult_upper_2009", "sex": None, "variables": {"RA": 0.08}},
    {"method": "cameriere_adult_lower_2009", "sex": None, "variables": {"RA": 0.15}},
    {"method": "kvaal_1995", "sex": None, "variables": {"M": 0.25, "W_minus_L": 0.05}},
    {"method": "kvaal_1995", "sex": None, "equation": "mandibular_canine",
     "variables": {"M": 0.30}},
    {"method": "kvaal_1995", "sex": "male", "equation": "mandibular_lateral_incisor",
     "variables": {"M": 0.25, "W_minus_L": 0.05}},
    {"method": "kvaal_1995", "sex": "female", "equation": "mandibular_lateral_incisor",
     "variables": {"M": 0.25, "W_minus_L": 0.05}},
    {"method": "kvaal_1995", "sex": None, "equation": "maxillary_three",
     "variables": {"M": 0.22, "W": 0.30, "L": 0.24}},
]


def _python_age(f):
    kw = {k: v for k, v in f.items() if k not in ("method", "sex")}
    return odontoage.estimate(f["method"], sex=f["sex"], **kw).estimated_age_years


def test_python_js_parity():
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available for parity check")
    runner = os.path.join(os.path.dirname(__file__), "_parity_runner.js")
    proc = subprocess.run([node, runner], input=json.dumps(FIXTURES),
                          capture_output=True, text=True)
    assert proc.returncode == 0, f"node failed: {proc.stderr}"
    js_ages = json.loads(proc.stdout)
    assert len(js_ages) == len(FIXTURES)
    for f, js_age in zip(FIXTURES, js_ages):
        py_age = _python_age(f)
        assert isinstance(js_age, (int, float)), f"JS error for {f['method']}: {js_age}"
        assert abs(py_age - js_age) < 1e-6, \
            f"parity mismatch {f['method']}: py={py_age} js={js_age}"
