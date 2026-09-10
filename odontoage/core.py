"""Unified OdontoAge API: estimate(), compare(), list_methods()."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from . import _data
from .errors import MethodNotVerifiedError, UnknownMethodError
from .methods import cameriere, demirjian, kvaal, willems
from .model import Estimate, Interval

_RUNNERS = {
    "cameriere": cameriere.run,
    "demirjian": demirjian.run,
    "willems": willems.run,
    "kvaal": kvaal.run,
}

GENERAL_DISCLAIMER = (
    "OdontoAge is a research and educational reference implementation of published "
    "dental age-estimation methods. Estimates carry substantial uncertainty and must "
    "never be used as the SOLE basis for any legal, forensic, immigration, or clinical "
    "determination about a real person. Dental age is not chronological age. Age "
    "estimation of living people (e.g. asylum age-disputes) raises serious scientific "
    "and ethical concerns; follow the guidance of the relevant professional bodies and "
    "always keep a qualified human expert in the loop."
)


def _interval_for(age: Optional[float], see: Optional[float]) -> Optional[Interval]:
    if age is None or not see:
        return None
    see = float(see)
    return Interval(low=age - 1.96 * see, high=age + 1.96 * see,
                    level=0.95, basis=f"+/- 1.96 x SEE ({see} y); population-level, approximate")


def estimate(method: str, *, sex: Any = None, allow_unverified: bool = False,
             **inputs: Any) -> Estimate:
    """Estimate age with a single named method. See ``list_methods()`` for ids and inputs."""
    mdef = _data.get_method(method)
    if mdef is None:
        raise UnknownMethodError(
            f"unknown method {method!r}; known: {sorted(_data.methods())}")
    if not mdef.get("verified") and not allow_unverified:
        raise MethodNotVerifiedError(
            f"method {method!r} has not been cross-verified yet "
            f"(status: {mdef.get('status', 'unverified')}). Refusing to produce a number. "
            f"Pass allow_unverified=True only for development/inspection.")

    runner = _RUNNERS[mdef["family"]]
    res = runner(mdef, sex=sex, **inputs)

    age = res.get("age")
    warnings = list(res.get("warnings", []))
    rng = mdef.get("age_range_years") or [None, None]
    lo, hi = (rng + [None, None])[:2]
    if age is not None and lo is not None and (age < lo or age > hi):
        warnings.append(
            f"Estimated age {age:.1f} y is outside this method's validated range "
            f"{lo}-{hi} y; interpret with particular caution.")

    src = _data.get_source(mdef.get("source", ""))
    return Estimate(
        method=method,
        label=mdef.get("label", method),
        estimated_age_years=age,
        dentition=mdef.get("dentition", ""),
        sex=str(sex) if sex is not None else None,
        interval=_interval_for(age, res.get("see_years")),
        maturity_score=res.get("maturity_score"),
        reasoning=res.get("reasoning", []),
        inputs=inputs,
        citation=src.get("citation", ""),
        doi=src.get("doi"),
        disclaimer=GENERAL_DISCLAIMER,
        warnings=warnings,
        verified=bool(mdef.get("verified")),
    )


def compare(*, sex: Any = None, dentition: Optional[str] = None,
            allow_unverified: bool = False, **inputs: Any) -> List[Estimate]:
    """Run every applicable method for the given inputs and return their estimates.

    Methods whose required inputs are not satisfied are skipped silently, so you can
    pass, e.g., ``stages=...`` to get Demirjian+Willems, or ``teeth=...`` for Cameriere.
    """
    results: List[Estimate] = []
    for mid, m in _data.methods().items():
        if not m.get("verified") and not allow_unverified:
            continue
        if dentition and m.get("dentition") != dentition:
            continue
        try:
            results.append(estimate(mid, sex=sex, allow_unverified=allow_unverified, **inputs))
        except Exception:
            continue
    return results


def list_methods(verified_only: bool = False,
                 dentition: Optional[str] = None) -> List[Dict[str, Any]]:
    """List registered methods with their metadata."""
    out = []
    for mid, m in _data.methods().items():
        if verified_only and not m.get("verified"):
            continue
        if dentition and m.get("dentition") != dentition:
            continue
        out.append({
            "id": mid,
            "label": m.get("label", mid),
            "family": m.get("family"),
            "dentition": m.get("dentition"),
            "measurement": m.get("measurement"),
            "sex_required": m.get("sex_required", False),
            "age_range_years": m.get("age_range_years"),
            "verified": bool(m.get("verified")),
            "source": m.get("source"),
        })
    return out
