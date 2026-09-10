# Changelog

All notable changes to OdontoAge are documented here. This project adheres to
[Semantic Versioning](https://semver.org/). PyPI releases are immutable.

## [0.1.0] — 2026-09-09

Initial public release. **Six cross-verified methods across children and adults.**

### Added
- **Cameriere open-apex formulas** for children — Italian (2006) and European (2007) —
  cross-verified and enabled.
- **Demirjian (1976)** 7-tooth maturity scoring (boys + girls), transcribed from the
  primary paper at full resolution and validated by the stage-H = 100 checksum.
- **Willems (2001)** direct-age tables (boys + girls), transcribed from the primary paper
  and validated by an all-stage-H developmental-ceiling sanity total.
- **Cameriere adult (2009)** — upper and lower canine pulp/tooth **area**-ratio regressions
  (combined Italian + Portuguese, sex-independent), transcribed from Table 5 of the primary
  paper at full resolution; DOI confirmed against CrossRef.
- **Kvaal (1995)** — all nine pulp/tooth size-ratio regressions (six-tooth, maxillary-three,
  mandibular-three, and six single-tooth models), including the mandibular-canine model with
  no second predictor and the mandibular-lateral-incisor model's gender term; transcribed
  from Table 5 at full resolution (resolving the 66.8/6.8 text-extraction ambiguity to −66.8).
- Data-driven, dependency-free engine with a unified `estimate()` / `compare()` API and a
  `list_methods()` registry; every result carries an approximate 95% interval, a reasoning
  trace, the citation/DOI, and a disclaimer.
- **Safety gate**: methods whose parameters are not yet cross-verified raise
  `MethodNotVerifiedError` instead of returning an unverified number.
- **CLI** (`odontoage list | estimate | compare`).
- **Zero-install web app** (GitHub Pages): staged-tooth, open-apex, and adult inputs;
  side-by-side comparison on a shared age axis; ethics acknowledgement gate; dark mode;
  print; reduced-motion / -transparency / -contrast support.
- **Tests**: hand-verified Cameriere fixtures, API/gating, dataset-integrity invariants
  (incl. the Demirjian stage-H sum-to-100 guard), and Python↔JavaScript numeric parity.
- Evidence dossier (`docs/EVIDENCE.md`), deploy guide (`docs/DEPLOY.md`), JOSS-style
  `paper.md`, `CITATION.cff`, `.zenodo.json`.
- All primary-source DOIs confirmed against the CrossRef registry (and the publisher record
  for Kvaal 1995); corrected the European-formula author list to Cameriere, De Angelis,
  Ferrante, Scarpino & Cingolani.
