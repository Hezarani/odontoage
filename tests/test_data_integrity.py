"""Structural + scientific-invariant checks over the encoded datasets.

These run against whatever is in the data files, so the moment a staged method is
marked ``verified: true`` its tables must be complete and satisfy the published
invariants (e.g. Demirjian stage-H scores summing to 100) or the suite fails.
"""
from odontoage import _data
from odontoage.methods.base import TEETH

REQUIRED_FIELDS = {"id", "label", "family", "kind", "dentition", "verified", "source"}


def test_every_method_has_required_fields_and_source():
    sources = _data.sources()
    for mid, m in _data.methods().items():
        missing = REQUIRED_FIELDS - set(m)
        assert not missing, f"{mid} missing fields {missing}"
        assert m["source"] in sources, f"{mid}: source {m['source']!r} not in sources.json"


def test_verified_regressions_are_complete():
    for mid, m in _data.methods().items():
        if not m.get("verified") or m.get("kind") != "regression":
            continue
        if "equations" in m:
            # Multi-equation method (Kvaal): every equation needs an intercept and an
            # M coefficient; the second predictor and gender term are optional.
            eqs = m.get("equations", {})
            assert eqs, f"{mid}: no equations"
            default = m.get("default_equation")
            assert default in eqs, f"{mid}: default_equation {default!r} not among equations"
            for name, eq in eqs.items():
                assert eq.get("intercept") is not None, f"{mid}/{name}: null intercept"
                assert eq.get("M") is not None, f"{mid}/{name}: null M coefficient"
        else:
            reg = m.get("regression", {})
            assert reg.get("intercept") is not None, f"{mid}: null intercept"
            assert reg.get("terms"), f"{mid}: no regression terms"
            for term in reg["terms"]:
                assert term.get("coef") is not None, f"{mid}: term {term.get('var')} has null coef"


def test_verified_maturity_tables_satisfy_sum_to_100():
    for mid, m in _data.methods().items():
        if not m.get("verified") or m.get("kind") != "maturity_score":
            continue
        for sex in ("male", "female"):
            scores = m["scores"].get(sex)
            assert scores, f"{mid}: no {sex} scores"
            for t in TEETH:
                assert t in scores, f"{mid}/{sex}: missing tooth {t}"
            h_sum = sum(float(scores[t]["H"]) for t in TEETH)
            # Demirjian scores are rounded to 0.1, so the sum can be 100.0 +/- rounding.
            assert abs(h_sum - 100.0) < 0.2, f"{mid}/{sex}: stage-H sum {h_sum} != 100"


def test_verified_direct_age_tables_are_complete():
    for mid, m in _data.methods().items():
        if not m.get("verified") or m.get("kind") != "direct_age":
            continue
        for sex in ("male", "female"):
            table = m["tables"].get(sex)
            assert table, f"{mid}: no {sex} table"
            for t in TEETH:
                assert t in table and table[t], f"{mid}/{sex}: missing/empty tooth {t}"


def test_staged_methods_use_canonical_tooth_order():
    for mid, m in _data.methods().items():
        if m.get("measurement") == "staging":
            assert tuple(m.get("teeth", ())) == TEETH, f"{mid}: non-canonical tooth order"


def test_cameriere_european_x5_coefficient_is_negative():
    # Guards against a well-meaning 'fix' that would silently break the European formula.
    m = _data.get_method("cameriere_european_2007")
    x5 = next(t for t in m["regression"]["terms"] if t["var"] == "x5")
    assert x5["coef"] < 0, "European formula x5 coefficient must be negative (-1.692)"


def test_cameriere_italian_x5_coefficient_is_positive():
    m = _data.get_method("cameriere_italian_2006")
    x5 = next(t for t in m["regression"]["terms"] if t["var"] == "x5")
    assert x5["coef"] > 0, "Italian formula x5 coefficient must be positive (+1.631)"


def test_cameriere_adult_methods_use_single_RA_term():
    # The adult pulp-area models are simple linear fits in the area ratio RA only.
    for mid in ("cameriere_adult_upper_2009", "cameriere_adult_lower_2009"):
        m = _data.get_method(mid)
        assert m["measurement"] == "pulp_tooth_area"
        terms = m["regression"]["terms"]
        assert len(terms) == 1 and terms[0]["var"] == "RA", f"{mid}: expected one RA term"
        assert terms[0]["coef"] < 0, f"{mid}: RA coefficient must be negative"


def test_kvaal_canine_has_no_second_predictor():
    # Kvaal states the second predictor was NOT included for mandibular canines (P=0.06).
    m = _data.get_method("kvaal_1995")
    assert m["equations"]["mandibular_canine"]["W_minus_L"] is None, \
        "mandibular canine equation must omit the W-L term"


def test_kvaal_lateral_incisor_is_the_only_gendered_equation():
    # Kvaal states gender was only included for the mandibular lateral incisor.
    m = _data.get_method("kvaal_1995")
    gendered = [name for name, eq in m["equations"].items() if eq.get("G") is not None]
    assert gendered == ["mandibular_lateral_incisor"], \
        f"only the mandibular lateral incisor carries a gender term, got {gendered}"
    assert m["equations"]["mandibular_lateral_incisor"]["G"] == -6.0
