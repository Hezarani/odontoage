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

The children's methods (Demirjian, Willems, Cameriere open apices) use the seven permanent **lower-left** teeth (FDI 31–37): central incisor, lateral incisor, canine, 1st premolar, 2nd premolar, 1st molar, 2nd molar. Cameriere's `x5` is the 2nd premolar. The adult methods use other teeth: Cameriere (2009) an upper or lower **canine**; Kvaal (1995) the maxillary central incisor, lateral incisor and 2nd premolar and the mandibular lateral incisor, canine and 1st premolar.

## Evidence, verification & citation

Exact encoded parameters, their primary sources, the verification method, and accuracy/caveats live in **[`docs/EVIDENCE.md`](docs/EVIDENCE.md)**. Every number is confirmed against ≥2 independent sources; the Python and JavaScript engines are checked for bit-for-bit agreement in the test suite; scientific invariants (e.g. Demirjian stage-H scores summing to 100) are asserted automatically.

To cite OdontoAge, use [`CITATION.cff`](CITATION.cff) or the Zenodo DOI [10.5281/zenodo.22694379](https://doi.org/10.5281/zenodo.22694379).

## Ethics & limitations

- **Dental age ≠ chronological age.** Even the best methods have wide individual error (often ±1 year in children; several years in adults).
- **Population variation.** The reference samples are population-specific (e.g. Demirjian: French-Canadian; Willems: Belgian). Demirjian is known to overestimate elsewhere. Treat outputs as *reference implementations of published standards*, not ground truth for your population.
- **Living persons / age-disputes.** Radiographic age assessment of living people (including unaccompanied minors in asylum proceedings) is scientifically limited and ethically contested; professional and radiology bodies have raised concerns about radiation without clinical benefit and about misclassifying children as adults. OdontoAge exists to make the methods transparent and testable, not to endorse any particular use. Keep a qualified expert in the loop.

## References & prior work

Every encoded parameter traces to the sources below; exact values and the verification method are in [`docs/EVIDENCE.md`](docs/EVIDENCE.md), and the machine-readable registry is [`odontoage/data/sources.json`](odontoage/data/sources.json).

**Methods it implements**

- Demirjian, A., Goldstein, H. & Tanner, J.M. (1973). A new system of dental age assessment. *Human Biology* 45(2):211–227. [PMID 4714564](https://pubmed.ncbi.nlm.nih.gov/4714564/) (no DOI)
- Demirjian, A. & Goldstein, H. (1976). New systems for dental maturity based on seven and four teeth. *Annals of Human Biology* 3(5):411–421. [doi:10.1080/03014467600001671](https://doi.org/10.1080/03014467600001671)
- Willems, G. et al. (2001). Dental age estimation in Belgian children: Demirjian's technique revisited. *Journal of Forensic Sciences* 46(4):893–895. [doi:10.1520/JFS15064J](https://doi.org/10.1520/JFS15064J)
- Cameriere, R., Ferrante, L. & Cingolani, M. (2006). Age estimation in children by measurement of open apices in teeth. *International Journal of Legal Medicine* 120(1):49–52. [doi:10.1007/s00414-005-0047-9](https://doi.org/10.1007/s00414-005-0047-9)
- Cameriere, R. et al. (2007). Age estimation in children by measurement of open apices in teeth: a European formula. *International Journal of Legal Medicine* 121(6):449–453. [doi:10.1007/s00414-007-0179-1](https://doi.org/10.1007/s00414-007-0179-1)
- Cameriere, R. et al. (2009). Age estimation by pulp/tooth area ratio in canines: study of a Portuguese sample to test Cameriere's method. *Forensic Science International* 193(1–3):128.e1–128.e6. [doi:10.1016/j.forsciint.2009.09.011](https://doi.org/10.1016/j.forsciint.2009.09.011)
- Kvaal, S.I. et al. (1995). Age estimation of adults from dental radiographs. *Forensic Science International* 74(3):175–185. [doi:10.1016/0379-0738(95)01760-G](https://doi.org/10.1016/0379-0738(95)01760-G)

**Prior work and cross-verification sources**

- Cameriere, R., Ferrante, L. & Cingolani, M. (2004). Variations in pulp/tooth area ratio as an indicator of age: a preliminary study. *Journal of Forensic Sciences* 49(2):317–319. [doi:10.1520/JFS2003259](https://doi.org/10.1520/JFS2003259)
- Hostiuc, S. et al. (2021). Age estimation using the Cameriere methods of open apices: a meta-analysis. *Healthcare* 9(2):237. [doi:10.3390/healthcare9020237](https://doi.org/10.3390/healthcare9020237)

## Contributing

New methods are added as **data**, not code: drop a cross-verified parameter set into `odontoage/data/`, cite ≥2 sources, add fixtures. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT © 2026 Hossein Boustani Hezarani. Method *parameters* are facts/formulae from the cited literature; OdontoAge encodes and cites them and does not reproduce copyrighted figures, atlas images, or descriptive prose.
