"""Demirjian maturity-score estimator (7 mandibular teeth), with optional age conversion."""
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from ..errors import InvalidInputError
from .base import TEETH, normalize_sex

_ABSENT = {"0", "-", "NONE", "", "NA"}


def _maturity_score(method_def, sex, stages) -> Tuple[float, list, str]:
    sexk = normalize_sex(sex)
    table = method_def.get("scores", {}).get(sexk, {})
    if not table:
        raise InvalidInputError(f"no {method_def['id']} score table for {sexk} (data pending)")
    total = 0.0
    reasoning = []
    for t in TEETH:
        if t not in stages:
            raise InvalidInputError(f"missing developmental stage for tooth {t!r}")
        st = str(stages[t]).strip().upper()
        tooth_scores = table.get(t, {})
        if st in _ABSENT:
            score = 0.0
        elif st in tooth_scores:
            score = float(tooth_scores[st])
        else:
            raise InvalidInputError(
                f"tooth {t}: stage {st!r} not defined; available: {sorted(tooth_scores)}")
        total += score
        reasoning.append(f"  {t} stage {st}: {score}")
    return total, reasoning, sexk


def _convert(method_def, sexk, score) -> Tuple[Optional[float], str]:
    conv = method_def.get("conversion", {}).get(sexk, [])
    if not conv:
        return None, "no conversion table available"
    pts = sorted((float(s), float(a)) for s, a in conv)
    if score <= pts[0][0]:
        return pts[0][1], f"clamped to lower bound (score {pts[0][0]})"
    if score >= pts[-1][0]:
        return pts[-1][1], f"clamped to upper bound (score {pts[-1][0]})"
    for (s0, a0), (s1, a1) in zip(pts, pts[1:]):
        if s0 <= score <= s1:
            age = a0 if s1 == s0 else a0 + (a1 - a0) * (score - s0) / (s1 - s0)
            return age, f"interpolated between ({s0}->{a0}) and ({s1}->{a1})"
    return None, "score outside conversion range"


def run(method_def: Dict[str, Any], *, sex=None, stages=None, **extra) -> Dict[str, Any]:
    if not stages:
        raise InvalidInputError(
            "Demirjian needs 'stages': a dict {tooth: 'A'..'H'} for all 7 teeth "
            f"({list(TEETH)})")
    score, reasoning, sexk = _maturity_score(method_def, sex, stages)
    reasoning.append(f"Maturity score = {score:.1f} / 100.")
    age, note = _convert(method_def, sexk, score)
    warnings = ["Demirjian's standard is known to overestimate age in many populations "
                "outside its French-Canadian reference sample."]
    if age is not None:
        reasoning.append(f"Converted maturity score to age: {age:.2f} y ({note}).")
    else:
        reasoning.append(f"Age conversion unavailable ({note}); returning maturity score only.")
    return {"age": age, "maturity_score": score, "reasoning": reasoning,
            "warnings": warnings, "see_years": method_def.get("prediction_error_years")}
