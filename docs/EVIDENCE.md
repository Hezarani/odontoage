# OdontoAge — Evidence & Verification Dossier

This document records the **exact encoded parameters** of every method, their **primary
sources**, how each was **cross-verified**, and the **accuracy and caveats** you must
carry into any interpretation. It is the scholarly backbone of OdontoAge.

## Verification principles

1. **≥2 independent authoritative sources per value.** A parameter is marked
   `verified: true` only when confirmed by at least two independent sources (the original
   paper and/or peer-reviewed reproductions). Anything else is **hard-gated off** — calling
   it raises `MethodNotVerifiedError` rather than returning an unverified number.
2. **Scientific invariants are asserted in tests.** e.g. Demirjian self-weighted stage-H
   scores must sum to 100.0 per sex; staged methods must use the canonical 7-tooth order.
3. **Python ↔ JavaScript parity.** The library and the web engine share the same encoded
   data and are tested to return identical ages (to 1e-6) for the same inputs.
4. **Intellectual property.** OdontoAge encodes the *numeric methods* (formulae and
   statistically-derived constants — facts and mathematical methods, not copyrightable
   expression) and **cites** each source. It does **not** reproduce copyrighted figures,
   atlas images, or descriptive prose; stage descriptions in the UI are our own concise
   paraphrases of standard tooth-development facts.
5. **Domain authorship.** Parameters are curated and reviewed by a dentist (DDS).

Teeth used throughout: the seven permanent **lower-left** teeth, FDI **31–37** =
central incisor, lateral incisor, canine, 1st premolar, 2nd premolar (Cameriere's *x5*),
1st molar, 2nd molar.

---

## Cameriere — open apices (children) ✅ verified

Cameriere's method measures the **open apices** of the seven lower-left teeth on a
panoramic radiograph. For each tooth *i*: if the apex is open, measure `A_i` (the distance
between the inner sides of the open apex; for two-rooted teeth — the molars — sum the
distances of both apices) and `L_i` (tooth length), and form the **normalised** value
`x_i = A_i / L_i`. A tooth with a closed apex contributes `x_i = 0`. Then:

- `N0` = number of the 7 teeth with **closed** apices,
- `s`  = Σ `x_i` over the 7 teeth (sum of normalised open apices),
- `x5` = normalised value of the **2nd premolar** specifically,
- `g`  = **1 for males, 0 for females**.

**Italian formula (Cameriere, Ferrante & Cingolani, 2006):**

```
Age = 8.971 + 0.375·g + 1.631·x5 + 0.674·N0 − 1.034·s − 0.176·(s·N0)
```

**European formula (Cameriere et al., 2007):**

```
Age = 8.387 + 0.282·g − 1.692·x5 + 0.835·N0 − 0.116·s − 0.139·(s·N0)
```

- Source (Italian): Cameriere R, Ferrante L, Cingolani M. *Age estimation in children by
  measurement of open apices in teeth.* Int J Legal Med. 2006;120(1):49–52.
  doi:10.1007/s00414-005-0047-9.
- Source (European): Cameriere R, De Angelis D, Ferrante L, Scarpino F, Cingolani M. *Age
  estimation in children by measurement of open apices in teeth: a European formula.*
  Int J Legal Med. 2007;121(6):449–453. doi:10.1007/s00414-007-0179-1 (DOI, title, and
  author list confirmed against the CrossRef registry).
- **Cross-verification:** European coefficients confirmed against the primary 2007 paper
  and an independent meta-analysis (PMC7926662), which lists both formulae side by side.
- **Important disambiguation:** the two formulae are **different**, and the secondary
  literature frequently **mislabels the 2006 Italian formula as "European."** Note the
  European formula's `x5` coefficient is **negative** (−1.692) — this is correct for the
  multivariate European fit and is guarded by a regression test.
- **Reported accuracy (European):** R² ≈ 0.861; median residual ≈ −0.114 y.
- **Validated range:** ~4–16 y (most accurate ≈ 7–14 y per the meta-analysis).
- **Confidence interval:** enabled once the published standard error of the estimate is
  encoded (`prediction_error_years`); until then results show a point estimate only.

Worked check (implementation lock): European, male, `x5=0.06, N0=5, s=0.42` →
`8.387 + 0.282 − 0.10152 + 4.175 − 0.04872 − 0.2919 = 12.402 y` (matches code & web app).

---

## Demirjian (1976) — maturity scoring (children) ✅ verified

Seven-tooth self-weighted maturity score (0–100) from developmental stages A–H. The full
boys and girls score grids (Table 2 of the primary paper) are encoded, transcribed from the
paper rendered at high resolution.

- **Validation:** the method's own checksum — the stage-H scores across the 7 teeth sum to
  100 — holds for our transcription (boys **100.0**; girls **100.1**, a 0.1 rounding
  artifact of the source's 1-decimal values), and every tooth's scores increase strictly
  with stage. Enforced by the test suite.
- **Output:** OdontoAge returns the **maturity score (0–100)**. Demirjian's own age
  conversion is read from the published 50th-percentile *curves* (Figs 1–2), which we do
  **not** digitise (to avoid introducing curve-reading error); for a dental *age* from the
  same 7-tooth staging use the Willems method below.
- **Caveat:** French-Canadian reference sample; the score translates to an **over-estimate
  of age in many other populations**.
- Source: Demirjian A, Goldstein H. *New systems for dental maturity based on seven and four
  teeth.* Ann Hum Biol. 1976;3(5):411–421. (Original system: Demirjian A, Goldstein H,
  Tanner JM. Hum Biol. 1973;45(2):211–227.)

## Willems (2001) — direct age (children) ✅ verified

A revision of Demirjian in which each tooth-stage maps directly to a **value in years**;
the seven values are **summed** to give the dental age, with separate boys/girls tables (no
maturity-score conversion step). Both grids (Tables 1 and 2 of the primary paper) are
encoded, transcribed at high resolution.

- **Validation:** Willems values are ANOVA-adapted and intentionally non-monotonic — some
  are **negative** (a multicolinearity artifact the authors state is meaningful only in the
  total sum), so there is no sum-to-100 checksum. Verified instead by the all-stage-H
  developmental-ceiling total (boys **≈16.0 y**, girls **≈15.8 y**) and against the paper's
  documented negative values.
- **Accuracy:** reported SD of (dental − chronological age) on the validation sample ≈ 0.9 y
  (boys) / 1.3 y (girls); the 95% interval uses ~1.1 y as a representative value.
- Reference sample Belgian Caucasian; reduces Demirjian's systematic overestimation.
- Source: Willems G, Van Olmen A, Spiessens B, Carels C. *Dental age estimation in Belgian
  children: Demirjian's technique revisited.* J Forensic Sci. 2001;46(4):893–895.

## Cameriere — adult, pulp/tooth **area** ratio (2009) ✅ verified

Adult age from the pulp-to-tooth **area** ratio (`RA`) of a **canine**, measured by
planimetry on a peri-apical radiograph: outline the whole tooth and the pulp, and form
`RA = pulp area / tooth area`. Two simple linear regressions are provided — one for the
**upper (maxillary)** canine, one for the **lower (mandibular)** canine:

```
Upper canine:  Age = 100.598 − 544.433 · RA        (R² = 0.931, SEE = 4.24 y)
Lower canine:  Age =  91.362 − 480.901 · RA         (R² = 0.9285, SEE = 4.33 y)
```

- Source: Cameriere R, Cunha E, Sassaroli E, Nuzzolese E, Ferrante L. *Age estimation by
  pulp/tooth area ratio in canines: study of a Portuguese sample to test Cameriere's
  method.* Forensic Sci Int. 2009;193(1–3):128.e1–128.e6. doi:10.1016/j.forsciint.2009.09.011.
- **Encoded from:** Table 5 and Eqs. (3)–(4) of the 2009 paper, read from the primary PDF
  rendered at full resolution; the DOI and full citation were confirmed against the CrossRef
  registry.
- **Model scope:** the paper reports that ANCOVA found **neither nationality (Italian vs
  Portuguese) nor gender** significantly affected the fit, so these were dropped — the
  encoded equations are the **combined Italian + Portuguese** regressions and are
  **sex-independent**.
- **Reported accuracy:** upper R² = 0.931, SEE = 4.24 y (mean error 3.32 y); lower
  R² = 0.9285, SEE = 4.33 y (mean error 3.39 y). The 95% interval uses ±1.96 · SEE.
- **Caveat:** secondary-dentine apposition is gradual and variable; adult estimates carry
  several years of uncertainty and should be reported as intervals.

Worked check (implementation lock): upper, `RA = 0.08` → `100.598 − 544.433·0.08 = 57.043 y`
(matches code & web app); lower, `RA = 0.08` → `91.362 − 480.901·0.08 = 52.890 y`.

## Kvaal (1995) — adult pulp/tooth size ratios ✅ verified

Adult age from ratios of pulp to tooth/root dimensions measured on peri-apical radiographs.
Six measurements per tooth (Kvaal Fig. 1) — maximum tooth length **T**, mesial root length
**R**, maximum pulp length **P**, and pulp/root widths at three levels **A** (enamel-cementum
junction), **B** (mid), **C** (mid-root) — are formed into magnification-independent ratios,
from which two predictors are built:

- **M** = mean of the five ratios (pulp/root length, pulp/tooth length, and the three
  pulp/root width ratios). *(The tooth/root length ratio was only weakly correlated with age
  and is excluded.)* First predictor — overall pulp size.
- **W** = mean of the width ratios at levels B and C; **L** = mean of the length ratios;
  **W − L** = second predictor — pulp shape.

Nine regression formulae (Table 5) are encoded — a six-tooth model, maxillary-three and
mandibular-three models, and six single-tooth models:

```
Six teeth (both jaws):        Age = 129.8 − 316.4·M − 66.8·(W−L)      r²=0.76  SEE=8.6
Three maxillary teeth:        Age = 120.0 − 256.6·M − 45.3·(W−L)      r²=0.74  SEE=8.9
Three mandibular teeth:       Age = 135.3 − 356.8·M − 82.5·(W−L)      r²=0.71  SEE=9.4
Maxillary central incisor:    Age = 110.2 − 201.4·M − 31.3·(W−L)      r²=0.70  SEE=9.5
Maxillary lateral incisor:    Age = 103.5 − 216.6·M − 46.6·(W−L)      r²=0.67  SEE=10.0
Maxillary 2nd premolar:       Age = 125.3 − 288.5·M − 46.3·(W−L)      r²=0.60  SEE=11.0
Mandibular 1st premolar:      Age = 133.0 − 318.3·M − 65.0·(W−L)      r²=0.64  SEE=10.5
Mandibular canine:            Age = 158.8 − 255.7·M                    r²=0.56  SEE=11.5
Mandibular lateral incisor:   Age = 106.6 − 251.7·M − 61.2·(W−L) − 6.0·G   r²=0.57  SEE=11.5
```

- **Two structural exceptions, stated in the paper and guarded by tests:** the **mandibular
  canine** has **no second predictor** (W−L was not significant, P = 0.06); the **mandibular
  lateral incisor** is the **only** equation with a **gender term** (`G`: male = 1,
  female = 0).
- Source: Kvaal SI, Kolltveit KM, Thomsen IO, Solheim T. *Age estimation of adults from
  dental radiographs.* Forensic Sci Int. 1995;74(3):175–185. doi:10.1016/0379-0738(95)01760-G.
- **Encoded from:** Table 5 (formulae) and the Table 2 legend (ratio definitions), read from
  the primary PDF at full resolution. Text extraction ambiguously rendered the six-teeth W−L
  coefficient as "66.8" vs "6.8"; the high-resolution render confirms **−66.8**. The DOI was
  confirmed against the publisher record (ScienceDirect PII 0379-0738(95)01760-G).
- **Reference sample & accuracy:** 100 adults; SEE ≈ 8.6–11.5 y depending on the equation
  (best for the six-tooth model). Adult morphometric methods have **wide error** — report the
  interval, not a point value.

Worked check (implementation lock): six-teeth, `M = 0.25, W−L = 0.05` →
`129.8 − 316.4·0.25 − 66.8·0.05 = 47.36 y`; mandibular lateral incisor, `M = 0.25,
W−L = 0.05`, male → `106.6 − 62.925 − 3.06 − 6.0 = 34.615 y` (female = 40.615 y). All match
code & web app, and Python↔JavaScript to 1e-6.

---

## Ethics & limitations (read before use)

- **Not chronological age.** Every method estimates a *biological/dental* age with real
  individual variance. Report intervals, never a bare number, in any serious context.
- **Population specificity.** Reference samples differ from your population; validate
  locally and prefer methods validated for the relevant group.
- **Living persons and age-disputes.** The use of dental radiographs to assess the age of
  living people — especially unaccompanied minors in asylum/immigration proceedings — is
  scientifically limited and ethically contested. Concerns in the literature include wide
  error margins (a misclassified child can lose safeguarding), and radiation exposure with
  no clinical benefit to the person. OdontoAge takes no position endorsing such uses; it
  exists to make the published methods transparent, reproducible, and inspectable.
- **Human-in-the-loop.** Intended for research, teaching, and method comparison — always
  under qualified expert oversight.

## Source list

See [`odontoage/data/sources.json`](../odontoage/data/sources.json) for the machine-readable
citation registry with DOIs.
