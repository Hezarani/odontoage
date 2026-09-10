---
title: "OdontoAge: an open, cross-verified reference implementation of dental age-estimation methods"
tags:
  - forensic odontology
  - dental age estimation
  - legal medicine
  - paediatric dentistry
  - Python
authors:
  - name: Hossein Boustani Hezarani
    orcid: 0009-0007-8481-0498
    affiliation: 1
affiliations:
  - name: Independent researcher, Ankara, Türkiye
    index: 1
date: 3 September 2026
bibliography: paper.bib
---

# Summary

Dental age estimation supports forensic identification, paediatric assessment, and legal
age determination. In practice it relies on a small set of published scoring systems —
Demirjian's maturity method [@demirjian1973; @demirjian1976], Willems' direct-age revision
[@willems2001], Cameriere's open-apex formulae for children [@cameriere2006; @cameriere2007],
and, for adults, Cameriere's canine pulp/tooth **area**-ratio regressions [@cameriere2009]
and Kvaal's pulp/tooth size-ratio method [@kvaal1995]. Despite decades of use and a
continuous stream of validation studies, there has been **no open, tested, citable software
implementation** of these methods; researchers and clinicians re-implement them by hand in
spreadsheets or rely on closed web calculators, which impedes reproducibility.

`OdontoAge` is an open-source, dependency-free implementation of these methods, exposed
identically through a Python library, a command-line tool, and a zero-install web
application. Each estimate is returned with an approximate confidence interval, a
transparent step-by-step reasoning trace, and the citation for the method used.

# Statement of need

Method-comparison papers repeatedly re-code the same equations, and small transcription
errors in a table or a coefficient can materially change an estimated age — a serious risk
in forensic and legal contexts. `OdontoAge` encodes each method **once**, as data, and
verifies it: every parameter is confirmed against at least two independent authoritative
sources; scientific invariants are asserted in the test suite (for example, Demirjian's
self-weighted stage scores must sum to 100 at full maturity); and the Python and JavaScript
engines are tested for numerical parity so the library and the web demo are provably one
implementation. All six methods shipped in the initial release are cross-verified and
enabled; the safety gate remains part of the design, so any method whose parameters are not
yet fully cross-verified is hard-gated — requesting one raises an error rather than returning
an unverified number.

The package is designed to be **embeddable** (a clean `estimate`/`compare` API), **auditable**
(all parameters and sources in machine-readable JSON and a human-readable evidence dossier),
and **honest** (explicit intervals, population caveats, and an ethics statement on the use of
age estimation in living persons).

# Functionality

- `estimate(method, sex=..., **inputs)` returns an `Estimate` with the age, an approximate
  95% interval, an optional Demirjian maturity score, a reasoning trace, and the citation.
- `compare(...)` runs every applicable, verified method for a given set of inputs.
- A CLI (`odontoage`) mirrors the API for shell and scripting use.
- A single-page web application presents the staged-tooth and open-apex inputs, shows every
  method side-by-side on a shared age axis, and gates use behind an ethics acknowledgement.

# Verification and testing

Parameters are cross-verified against the primary literature and independent reproductions;
the Cameriere European formula, for instance, is confirmed against the original paper and a
meta-analysis, and the package intentionally distinguishes it from the frequently
mislabelled 2006 Italian formula. The test suite covers hand-computed fixtures, input
validation, dataset-integrity invariants, and Python↔JavaScript parity.

# Ethics

Estimated dental age is not chronological age and carries substantial uncertainty.
Radiographic age assessment of living people — notably unaccompanied minors in asylum
proceedings — is scientifically limited and ethically contested. `OdontoAge` is intended for
research and education under expert oversight and takes no position endorsing such uses; it
aims only to make the published methods transparent, reproducible, and inspectable.

# Acknowledgements

The author thanks the forensic-odontology and legal-medicine communities whose published
methods this software implements and cites.

# References
