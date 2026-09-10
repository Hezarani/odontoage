"""Command-line interface for OdontoAge.

Examples:
  odontoage list --verified
  odontoage estimate cameriere_european_2007 --sex male --vars "x5=0.06,N0=5,s=0.42"
  odontoage estimate willems_2001 --sex female --stages "I1:H,I2:H,C:G,PM1:F,PM2:E,M1:H,M2:D"
  odontoage compare --sex male --stages "I1:H,I2:H,C:G,PM1:F,PM2:E,M1:H,M2:D"
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

from . import __version__, compare, estimate, list_methods
from .errors import OdontoAgeError
from .model import Estimate


def _parse_stages(text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for part in filter(None, (p.strip() for p in text.split(","))):
        if ":" not in part and "=" not in part:
            raise SystemExit(f"bad --stages token {part!r}; use TOOTH:STAGE")
        sep = ":" if ":" in part else "="
        tooth, stage = part.split(sep, 1)
        out[tooth.strip()] = stage.strip()
    return out


def _parse_teeth(text: str) -> Dict[str, Any]:
    """Parse 'PM2=2.4/21.0,I1=closed,M2=3.1/19.0' into a teeth dict."""
    out: Dict[str, Any] = {}
    for part in filter(None, (p.strip() for p in text.split(","))):
        tooth, spec = part.split("=", 1)
        tooth, spec = tooth.strip(), spec.strip()
        if spec.lower() in ("closed", "c", "0"):
            out[tooth] = {"closed": True}
        elif "/" in spec:
            ai, li = spec.split("/", 1)
            out[tooth] = {"open": True, "Ai": float(ai), "Li": float(li)}
        else:
            out[tooth] = {"open": True, "x": float(spec)}
    return out


def _parse_vars(text: str) -> Dict[str, float]:
    out: Dict[str, float] = {}
    for part in filter(None, (p.strip() for p in text.split(","))):
        k, v = part.split("=", 1)
        out[k.strip()] = float(v.strip())
    return out


def _collect_inputs(args) -> Dict[str, Any]:
    inputs: Dict[str, Any] = {}
    if args.stages:
        inputs["stages"] = _parse_stages(args.stages)
    if args.teeth:
        inputs["teeth"] = _parse_teeth(args.teeth)
    if args.vars:
        inputs["variables"] = _parse_vars(args.vars)
    if getattr(args, "equation", None):
        inputs["equation"] = args.equation
    return inputs


def _print_estimate(e: Estimate, as_json: bool) -> None:
    if as_json:
        print(json.dumps(e.to_dict(), indent=2))
        return
    print(f"\n{e.label}  [{e.method}]")
    if e.estimated_age_years is not None:
        line = f"  Estimated age: {e.estimated_age_years:.2f} years"
        if e.interval:
            line += f"  (95% ~ {e.interval.low:.2f}-{e.interval.high:.2f} y)"
        print(line)
    if e.maturity_score is not None:
        print(f"  Maturity score: {e.maturity_score:.1f}/100")
    for r in e.reasoning:
        print(f"    {r}")
    for w in e.warnings:
        print(f"  ! {w}")
    if e.citation:
        print(f"  Source: {e.citation}" + (f"  doi:{e.doi}" if e.doi else ""))


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="odontoage", description="Dental age estimation (research/education).")
    p.add_argument("--version", action="version", version=f"odontoage {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list", help="list available methods")
    pl.add_argument("--verified", action="store_true", help="only cross-verified methods")
    pl.add_argument("--dentition", choices=["developing", "adult"])
    pl.add_argument("--json", action="store_true")

    def add_inputs(sp):
        sp.add_argument("--sex", help="male/female")
        sp.add_argument("--stages", help="TOOTH:STAGE,... for Demirjian/Willems")
        sp.add_argument("--teeth", help="TOOTH=Ai/Li or TOOTH=closed,... for Cameriere")
        sp.add_argument("--vars", help="name=value,... precomputed variables")
        sp.add_argument("--json", action="store_true")
        sp.add_argument("--allow-unverified", action="store_true")

    pe = sub.add_parser("estimate", help="estimate with one method")
    pe.add_argument("method")
    pe.add_argument("--equation", help="Kvaal equation name")
    add_inputs(pe)

    pc = sub.add_parser("compare", help="run all applicable methods")
    pc.add_argument("--dentition", choices=["developing", "adult"])
    add_inputs(pc)

    args = p.parse_args(argv)

    try:
        if args.cmd == "list":
            methods = list_methods(verified_only=args.verified, dentition=args.dentition)
            if args.json:
                print(json.dumps(methods, indent=2))
            else:
                for m in methods:
                    flag = "OK " if m["verified"] else "...."
                    rng = m["age_range_years"]
                    print(f"  [{flag}] {m['id']:<28} {m['dentition']:<10} "
                          f"{str(rng):<10} {m['label']}")
            return 0

        if args.cmd == "estimate":
            e = estimate(args.method, sex=args.sex,
                         allow_unverified=args.allow_unverified, **_collect_inputs(args))
            _print_estimate(e, args.json)
            if not args.json:
                print(f"\n  {e.disclaimer}\n")
            return 0

        if args.cmd == "compare":
            results = compare(sex=args.sex, dentition=args.dentition,
                              allow_unverified=args.allow_unverified, **_collect_inputs(args))
            if args.json:
                print(json.dumps([e.to_dict() for e in results], indent=2))
            else:
                if not results:
                    print("No applicable verified methods for those inputs.")
                for e in results:
                    _print_estimate(e, False)
                if results:
                    print(f"\n  {results[0].disclaimer}\n")
            return 0
    except OdontoAgeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
