"""Per-method estimators for OdontoAge.

Each module exposes ``run(method_def, *, sex=None, **inputs) -> dict`` returning a
partial result: ``{"age": float|None, "maturity_score": float|None,
"reasoning": [str], "warnings": [str], "see_years": float|None}``. The unified
API in :mod:`odontoage.core` wraps these with citation, disclaimer, verification
gating, and interval construction.
"""
