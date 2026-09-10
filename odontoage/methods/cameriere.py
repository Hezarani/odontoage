"""Cameriere estimators: open-apex (children) and pulp/tooth-area ratio (adults)."""
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from ..errors import InvalidInputError
from .base import TEETH, eval_linear, sex_to_g


def _open_apex_variables(sex, teeth, variables) -> Tuple[Dict[str, float], list]:
    g = sex_to_g(sex)
    if variables:
        missing = {"x5", "N0", "s"} - set(variables)
        if missing:
            raise InvalidInputError(f"missing precomputed variables: {sorted(missing)}")
        v = {"g": g, "x5": float(variables["x5"]),
             "N0": float(variables["N0"]), "s": float(variables["s"])}
        return v, [f"Using supplied variables: x5={v['x5']:.4f}, N0={v['N0']:.0f}, s={v['s']:.4f}."]

    if not teeth:
        raise InvalidInputError("provide per-tooth 'teeth' measurements or precomputed 'variables'")

    xs: Dict[str, float] = {}
    for t in TEETH:
        if t not in teeth:
            raise InvalidInputError(f"missing tooth {t!r}; need all 7: {list(TEETH)}")
        info = teeth[t]
        if isinstance(info, (int, float)):
            x = float(info)
        elif not info or info.get("closed") or info.get("open") is False:
            x = 0.0
        elif "x" in info and info["x"] is not None:
            x = float(info["x"])
        else:
            Ai, Li = info.get("Ai"), info.get("Li")
            if Ai is None or Li is None:
                raise InvalidInputError(
                    f"tooth {t}: give Ai and Li, or x, or mark {{'closed': true}}")
            Li = float(Li)
            if Li <= 0:
                raise InvalidInputError(f"tooth {t}: Li (tooth length) must be > 0")
            x = float(Ai) / Li
        if x < 0:
            raise InvalidInputError(f"tooth {t}: normalised apex x must be >= 0")
        xs[t] = x

    N0 = sum(1 for val in xs.values() if val == 0.0)
    s = sum(xs.values())
    x5 = xs["PM2"]
    reasoning = [
        f"Normalised open apices x_i = A_i / L_i per tooth (closed apex -> 0).",
        f"s = sum(x_i) = {s:.4f}; N0 (closed apices) = {N0}/7; x5 (2nd premolar) = {x5:.4f}.",
    ]
    return {"g": g, "x5": x5, "N0": float(N0), "s": s}, reasoning


def run(method_def: Dict[str, Any], *, sex=None, teeth=None,
        variables: Optional[Dict[str, float]] = None, **extra) -> Dict[str, Any]:
    measurement = method_def.get("measurement")
    reg = method_def.get("regression", {})

    if measurement == "open_apices":
        vars_, reasoning = _open_apex_variables(sex, teeth, variables)
        age = eval_linear(reg, vars_)
        reasoning.append(f"Age = {age:.3f} y from the {method_def['id']} regression.")
        return {"age": age, "reasoning": reasoning, "warnings": [],
                "see_years": method_def.get("prediction_error_years")}

    if measurement == "pulp_tooth_area":
        vv = dict(variables or {})
        # Accept the pulp/tooth AREA ratio under several friendly names and map
        # it to the regression variable "RA".
        if "RA" not in vv:
            for alias in ("RA", "ratio", "pulp_tooth_area_ratio", "area_ratio"):
                if alias in vv:
                    vv["RA"] = float(vv[alias])
                    break
                if alias in extra and extra[alias] is not None:
                    vv["RA"] = float(extra[alias])
                    break
        if "RA" not in vv:
            raise InvalidInputError(
                "adult method needs the pulp/tooth AREA ratio as variable 'RA' "
                "(e.g. variables={'RA': 0.08}) - the pulp area divided by the whole "
                "tooth area of the canine, measured by planimetry on a peri-apical film")
        ra = float(vv["RA"])
        if not (0.0 < ra < 1.0):
            raise InvalidInputError(
                f"pulp/tooth area ratio RA={ra} is out of range; it must be a fraction "
                "in (0, 1) - pulp area is a small part of the whole tooth area")
        age = eval_linear(reg, vv)
        coef = float(reg["terms"][0]["coef"])
        op = "-" if coef < 0 else "+"
        return {"age": age,
                "reasoning": [
                    f"Adult pulp/tooth AREA-ratio regression ({method_def['id']}): "
                    f"age = {reg['intercept']} {op} {abs(coef)}*RA, RA={ra:.4f}",
                    f"  -> {age:.2f} y.",
                ],
                "warnings": ["Adult morphometric methods are less precise than "
                             "developing-dentition methods (Cameriere reports SEE ~4.2-4.3 y)."],
                "see_years": method_def.get("prediction_error_years")}

    raise InvalidInputError(f"cameriere: unsupported measurement {measurement!r}")
