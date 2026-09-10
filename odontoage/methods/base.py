"""Shared helpers for method estimators."""
from __future__ import annotations

from typing import Any, Dict

from ..errors import InvalidInputError

# Canonical order of the seven permanent LEFT mandibular teeth used by the
# staged (Demirjian/Willems) and open-apex (Cameriere) methods. Index 5 (1-based)
# is the second premolar, matching Cameriere's "x5".
TEETH = ("I1", "I2", "C", "PM1", "PM2", "M1", "M2")
TEETH_FDI = ("31", "32", "33", "34", "35", "36", "37")

_MALE = {"m", "male", "boy", "b", "1", "man"}
_FEMALE = {"f", "female", "girl", "g", "0", "woman"}


def sex_to_g(sex: Any) -> int:
    """Map a sex value to the g indicator used by regression methods (1 male, 0 female)."""
    if sex is None:
        raise InvalidInputError("this method requires 'sex' (male/female)")
    s = str(sex).strip().lower()
    if s in _MALE:
        return 1
    if s in _FEMALE:
        return 0
    raise InvalidInputError(f"unrecognised sex value: {sex!r} (use 'male'/'female')")


def normalize_sex(sex: Any) -> str:
    return "male" if sex_to_g(sex) == 1 else "female"


def eval_linear(regression: Dict[str, Any], variables: Dict[str, float]) -> float:
    """Evaluate intercept + sum(coef * value) for a linear regression definition.

    Term variable names may contain ``*`` to denote an interaction, e.g. ``"s*N0"``;
    the factors are multiplied from ``variables`` so callers only supply base terms.
    """
    total = float(regression["intercept"])
    for term in regression.get("terms", []):
        name = term["var"]
        if "*" in name:
            value = 1.0
            for factor in name.split("*"):
                value *= _need(variables, factor.strip())
        else:
            value = _need(variables, name)
        total += float(term["coef"]) * value
    return total


def _need(variables: Dict[str, float], key: str) -> float:
    if key not in variables:
        raise InvalidInputError(f"missing regression variable {key!r}")
    return float(variables[key])
