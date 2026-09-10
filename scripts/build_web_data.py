#!/usr/bin/env python3
"""Generate docs/data.js (window.ODONTOAGE_DATA) from the packaged JSON datasets.

Bundling the data as a plain JS assignment lets the web app run fully offline and
from file:// (no fetch/CORS), and guarantees the app and the Python package use the
exact same encoded parameters.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "odontoage" / "data"
OUT = ROOT / "docs" / "data.js"
FAMILIES = ("cameriere", "demirjian", "willems", "kvaal")


def main() -> None:
    methods = {}
    for fam in FAMILIES:
        d = json.loads((DATA / f"{fam}.json").read_text(encoding="utf-8"))
        for mid, m in d.get("methods", {}).items():
            m = dict(m)
            m.setdefault("family", fam)
            methods[mid] = m
    sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8")).get("sources", {})
    payload = {"version": "0.1.0", "methods": methods, "sources": sources}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("window.ODONTOAGE_DATA = " + json.dumps(payload, indent=2) + ";\n",
                   encoding="utf-8")
    verified = [k for k, v in methods.items() if v.get("verified")]
    print(f"wrote {OUT} ({len(methods)} methods, {len(verified)} verified: {verified})")


if __name__ == "__main__":
    main()
