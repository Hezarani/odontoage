"""Willems (2001) direct-age estimator: per-tooth year-values summed to an age."""
from __future__ import annotations

from typing import Any, Dict

from ..errors import InvalidInputError
from .base import TEETH, normalize_sex

_ABSENT = {"0", "-", "NONE", "", "NA"}


def run(method_def: Dict[str, Any], *, sex=None, stages=None, **extra) -> Dict[str, Any]:
    if not stages:
        raise InvalidInputError(
            "Willems needs 'stages': a dict {tooth: 'A'..'H'} for all 7 teeth "
            f"({list(TEETH)})")
    sexk = normalize_sex(sex)
    table = method_def.get("tables", {}).get(sexk, {})
    if not table:
        raise InvalidInputError(f"no Willems table for {sexk} (data pending)")

    total = 0.0
    reasoning = []
    for t in TEETH:
        if t not in stages:
            raise InvalidInputError(f"missing developmental stage for tooth {t!r}")
        st = str(stages[t]).strip().upper()
        tooth_vals = table.get(t, {})
        if st in _ABSENT:
            val = 0.0
        elif st in tooth_vals:
            val = float(tooth_vals[st])
        else:
            raise InvalidInputError(
                f"tooth {t}: stage {st!r} not defined; available: {sorted(tooth_vals)}")
        total += val
        reasoning.append(f"  {t} stage {st}: {val} y")
    reasoning.append(f"Estimated age = sum of per-tooth values = {total:.2f} y.")
    return {"age": total, "reasoning": reasoning, "warnings": [],
            "see_years": method_def.get("prediction_error_years")}
