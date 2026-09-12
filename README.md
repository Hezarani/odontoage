# OdontoAge

**An open, cross-verified, tested reference implementation of dental age-estimation methods** — Cameriere (open apices & adult pulp/tooth area), Demirjian, Willems, and Kvaal — as a dependency-free Python library, a CLI, and a zero-install web app.

[![PyPI](https://img.shields.io/pypi/v/odontoage.svg)](https://pypi.org/project/odontoage/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://pypi.org/project/odontoage/)
[![Live demo](https://img.shields.io/badge/demo-GitHub%20Pages-0e6a7e.svg)](https://hezarani.github.io/odontoage/)
[![DOI](https://zenodo.org/badge/1364571849.svg)](https://doi.org/10.5281/zenodo.22694379)
> ⚠️ **Research and education only.** Estimated dental age is **not** chronological age and carries substantial uncertainty. OdontoAge must **never** be the sole basis for any legal, forensic, immigration, or clinical decision about a real person. Age assessment of living people (e.g. asylum age-disputes) is scientifically limited and ethically contested — see [Ethics & limitations](#ethics--limitations).

---

## Why this exists

Dental age estimation underpins forensic identification, paediatric assessment, and — controversially — legal age-disputes. The field runs on a handful of published scoring systems (Demirjian, Willems, Cameriere, Kvaal). Yet method-comparison papers keep appearing, and **every team re-implements these methods by hand in spreadsheets** or behind closed web calculators. There has been **no open, tested, citable, embeddable implementation.**

OdontoAge fills that gap: one place where the numbers are encoded once, **cross-verified against the primary literature**, unit-tested, and exposed identically to Python, the command line, and the browser.

## Live demo

**https://hezarani.github.io/odontoage/** — enter tooth stages or apex measurements and get every applicable method side-by-side, each with a 95% interval, a reasoning trace, and its citation.

## Methods

| Method | Dentition | Input | Output | Status |
|---|---|---|---|---|
| **Cameriere — Italian (2006)** | children ~5–15 y | open-apex measurements | age + interval | ✅ verified |
| **Cameriere — European (2007)** | children ~4–16 y | open-apex measurements | age + interval | ✅ verified |
| **Demirjian (1976)** | children ~2.5–17 y | 7-tooth stages A–H | maturity score (0–100) | ✅ verified |
| **Willems (2001)** | children ~3–18 y | 7-tooth stages A–H | age (direct) | ✅ verified |
| **Cameriere — adult (2009)** | adults ~20–85 y | canine pulp/tooth **area** ratio (RA), upper or lower | age + interval | ✅ verified |
| **Kvaal (1995)** | adults ~20–85 y | pulp/tooth size ratios (9 tooth/model equations) | age + interval | ✅ verified |

All six shipped methods are now **cross-verified and enabled**. The safety gate remains part of the design: any method whose parameters are not confirmed against ≥2 independent authoritative sources (see [`docs/EVIDENCE.md`](docs/EVIDENCE.md)) is **hard-gated off** and raises `MethodNotVerifiedError` rather than returning an unverified number — a wrong constant in a forensic tool is worse than no tool.

## Install

```bash
pip install odontoage
```

Zero runtime dependencies (pure standard library).

## Quickstart (Python)

```python
import odontoage

# Cameriere European formula from precomputed morphometric variables
e = odontoage.estimate(
    "cameriere_european_2007", sex="male",
    variables={"x5": 0.06, "N0": 5, "s": 0.42},
)
print(e)                       # -> Cameriere — European formula (open apices): 12.40 y
print(e.estimated_age_years)   # 12.40...
print(e.citation, e.doi)

# ...or straight from per-tooth apex measurements (mm)
teeth = {
    "I1": {"closed": True}, "I2": {"closed": True}, "C": {"closed": True},
    "PM1": {"open": True, "Ai": 0.42, "Li": 21.0},
    "PM2": {"open": True, "Ai": 1.05, "Li": 21.0},
    "M1": {"closed": True}, "M2": {"closed": True},
}
e = odontoage.estimate("cameriere_european_2007", sex="female", teeth=teeth)

# Run every applicable method at once
for est in odontoage.compare(sex="male", variables={"x5": 0.06, "N0": 5, "s": 0.42}):
    print(est.method, round(est.estimated_age_years, 2))
```

Every `Estimate` carries: `estimated_age_years`, an approximate 95% `interval`, an optional `maturity_score` (Demirjian), a step-by-step `reasoning` trace, the `citation`/`doi`, and a `disclaimer`.

## Quickstart (CLI)

```bash
odontoage list --verified
odontoage estimate cameriere_european_2007 --sex male --vars "x5=0.06,N0=5,s=0.42"
odontoage compare --sex male --teeth "I1=closed,I2=closed,C=closed,PM1=0.42/21,PM2=1.05/21,M1=closed,M2=closed"
```

## The teeth

All methods use the seven permanent **lower-left** teeth (FDI 31–37): central incisor, lateral incisor, canine, 1st premolar, 2nd premolar, 1st molar, 2nd molar. Cameriere's `x5` is the 2nd premolar.

## Evidence, verification & citation

Exact encoded parameters, their primary sources, the verification method, and accuracy/caveats live in **[`docs/EVIDENCE.md`](docs/EVIDENCE.md)**. Every number is confirmed against ≥2 independent sources; the Python and JavaScript engines are checked for bit-for-bit agreement in the test suite; scientific invariants (e.g. Demirjian stage-H scores summing to 100) are asserted automatically.

To cite OdontoAge, use [`CITATION.cff`](CITATION.cff) or the Zenodo DOI (added at first release).

## Ethics & limitations

- **Dental age ≠ chronological age.** Even the best methods have wide individual error (often ±1 year in children; several years in adults).
- **Population variation.** The reference samples are population-specific (e.g. Demirjian: French-Canadian; Willems: Belgian). Demirjian is known to overestimate elsewhere. Treat outputs as *reference implementations of published standards*, not ground truth for your population.
- **Living persons / age-disputes.** Radiographic age assessment of living people (including unaccompanied minors in asylum proceedings) is scientifically limited and ethically contested; professional and radiology bodies have raised concerns about radiation without clinical benefit and about misclassifying children as adults. OdontoAge exists to make the methods transparent and testable, not to endorse any particular use. Keep a qualified expert in the loop.

## Contributing

New methods are added as **data**, not code: drop a cross-verified parameter set into `odontoage/data/`, cite ≥2 sources, add fixtures. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT © 2026 Hossein Boustani Hezarani. Method *parameters* are facts/formulae from the cited literature; OdontoAge encodes and cites them and does not reproduce copyrighted figures, atlas images, or descriptive prose.
