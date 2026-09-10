"""Load and index the encoded method datasets bundled with the package."""
from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from typing import Any, Dict

_FAMILIES = ("cameriere", "demirjian", "willems", "kvaal")


def _load_json(filename: str) -> Dict[str, Any]:
    ref = resources.files("odontoage").joinpath("data", filename)
    with ref.open("r", encoding="utf-8") as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def sources() -> Dict[str, Any]:
    """Return the source/citation registry keyed by source id."""
    return _load_json("sources.json").get("sources", {})


@lru_cache(maxsize=1)
def methods() -> Dict[str, Any]:
    """Return every registered method definition keyed by method id.

    Each definition is annotated with its ``family`` so callers do not need to
    know which file it came from.
    """
    registry: Dict[str, Any] = {}
    for family in _FAMILIES:
        data = _load_json(f"{family}.json")
        for method_id, mdef in data.get("methods", {}).items():
            mdef = dict(mdef)
            mdef.setdefault("family", family)
            registry[method_id] = mdef
    return registry


def get_method(method_id: str) -> Dict[str, Any]:
    return methods().get(method_id)


def get_source(source_id: str) -> Dict[str, Any]:
    return sources().get(source_id, {})
