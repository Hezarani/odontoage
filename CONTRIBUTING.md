# Contributing to OdontoAge

Thank you for helping build an accurate, open reference for dental age estimation.
Because this tool can touch forensic and legal contexts, **correctness is the priority**.

## Ground rules

1. **Verify before you encode.** Every numeric parameter must be confirmed against **at
   least two independent authoritative sources** (the original paper plus a reproduction, or
   two independent reproductions). Cite them in `odontoage/data/sources.json` and note the
   cross-check in `docs/EVIDENCE.md`.
2. **Encode facts, not prose.** Add formulae and statistically-derived constants. Do **not**
   paste copyrighted figures, atlas images, or descriptive text; paraphrase concepts in your
   own words.
3. **Nothing unverified ships enabled.** New methods start with `"verified": false` and are
   gated off until their values are confirmed and tested.

## Dev setup

```bash
pip install -e ".[test]"
python -m pytest -q
```

## Adding or completing a method (it's data, not code)

1. Put the parameters in the right family file under `odontoage/data/` (`cameriere.json`,
   `demirjian.json`, `willems.json`, `kvaal.json`) following the existing shape:
   - regression methods: `regression.intercept` + `regression.terms` (`var`, `coef`);
     interaction terms use `*`, e.g. `"s*N0"`.
   - staged score methods: `scores.{male,female}[tooth][stage]` (+ `conversion`).
   - direct-age tables: `tables.{male,female}[tooth][stage]`.
2. Add the citation to `sources.json` and set the method's `source` to its key.
3. Add **hand-verified fixtures** in `tests/` from a published worked example where possible.
4. When confirmed, set `"verified": true`.
5. Regenerate the web bundle so the demo matches the library:
   ```bash
   python scripts/build_web_data.py
   ```
6. Run the suite — the integrity tests enforce invariants (e.g. Demirjian stage-H sums to
   100) and the parity test enforces Python↔JavaScript agreement.

## Pull requests

Keep changes focused, include tests, and describe the sources you verified against. Thanks!
