"""Kvaal et al. (1995) adult age estimator from pulp/tooth size-ratio measurements.

Nine regression formulae are encoded (Table 5 of the primary paper): a six-tooth
model, a maxillary-three and a mandibular-three model, and six single-tooth models.
Each predicts age (years) from ``M`` (mean-of-ratios first predictor) and, for all
but the mandibular canine, ``W - L`` (second predictor). The mandibular lateral
incisor (32/42) additionally carries a gender term.
"""
from __future__ import annotations

from typing import Any, Dict

from ..errors import InvalidInputError
from .base import sex_to_g


def run(method_def: Dict[str, Any], *, variables=None, equation=None,
        sex=None, **extra) -> Dict[str, Any]:
    equations = method_def.get("equations", {})
    if equation is None:
        equation = method_def.get("default_equation", "six_teeth")
    eq = equations.get(equation)
    if eq is None or eq.get("intercept") is None:
        raise InvalidInputError(
            f"Kvaal equation {equation!r} is not available; "
            f"choices: {sorted(equations)}")

    if not variables:
        raise InvalidInputError(
            "Kvaal needs 'variables': at least mean pulp/tooth ratio 'M' "
            "(and, for every equation except the mandibular canine, the second "
            "predictor 'W_minus_L', or both 'W' and 'L').")
    if "M" not in variables:
        raise InvalidInputError("Kvaal needs variable 'M' (mean pulp/tooth ratio)")
    M = float(variables["M"])

    intercept = float(eq["intercept"])
    age = intercept + float(eq["M"]) * M
    terms = [f"{intercept} + {eq['M']}*M"]
    detail = [f"M={M:.4f}"]

    # Second predictor (W - L): required unless this equation omits it (mand. canine)
    wl_coef = eq.get("W_minus_L")
    if wl_coef is not None:
        if "W_minus_L" in variables:
            wl = float(variables["W_minus_L"])
        elif "W" in variables and "L" in variables:
            wl = float(variables["W"]) - float(variables["L"])
        else:
            raise InvalidInputError(
                f"Kvaal equation {equation!r} needs 'W_minus_L' (or both 'W' and 'L')")
        age += float(wl_coef) * wl
        terms.append(f"{wl_coef}*(W-L)")
        detail.append(f"(W-L)={wl:.4f}")
    elif ("W_minus_L" in variables) or ("W" in variables and "L" in variables):
        # Supplied but unused for this equation -> tell the caller rather than
        # silently ignoring a predictor they thought mattered.
        pass

    # Gender term (only the mandibular lateral incisor equation carries one)
    g_coef = eq.get("G")
    warnings = ["Adult pulp-ratio methods have wide error (Kvaal reports SEE ~8.6-11.5 "
                "years depending on the equation); treat the result as a broad estimate."]
    if g_coef is not None:
        if sex is None:
            raise InvalidInputError(
                f"Kvaal equation {equation!r} (mandibular lateral incisor) requires "
                "'sex' for its gender term (male=1, female=0)")
        g = sex_to_g(sex)
        age += float(g_coef) * g
        terms.append(f"{g_coef}*G")
        detail.append(f"G={g} ({'male' if g else 'female'})")

    return {
        "age": age,
        "reasoning": [
            f"Kvaal {equation}: age = " + " + ".join(terms).replace("+ -", "- "),
            "  with " + ", ".join(detail) + f"  ->  {age:.1f} y.",
        ],
        "warnings": warnings,
        "see_years": eq.get("see"),
    }
