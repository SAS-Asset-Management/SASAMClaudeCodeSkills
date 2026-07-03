"""
Validation harness for the Simple ACR method (MDR Section 4.5.6.1).

Each test cites the equation it validates. Worked examples are loaded from
workedExamples.csv — these are derived directly from the MDR equations and
serve as the independent reference for calculate.py.
"""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import pytest

_SKILL_ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("acrSimpleCalc", _SKILL_ROOT / "calculate.py")
_calc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_calc)

acr_simple = _calc.acr_simple
validate_csv = _calc.validate_csv
report_examples = _calc.report_examples

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _parse_defects(spec: str) -> list[dict]:
    out = []
    if not spec:
        return out
    for triple in spec.split(";"):
        if not triple.strip():
            continue
        dcr, cc, rmc = triple.split(",")
        out.append({
            "DCR_raw": int(dcr),
            "CC": None if cc.strip() == "" else int(cc),
            "RMC": int(rmc),
        })
    return out


# ---- Equation 1 — no defects ⇒ ACR = 1 -----------------------------------

def test_equation_1_no_defects():
    """MDR p.21: 'If no defects are recorded against the Asset then ACR = 1'."""
    result = acr_simple([])
    assert result["ACR"] == 1
    assert result["n_defects"] == 0
    assert result["n_renewal_drivers"] == 0


# ---- Equation 3 — ACR = max(DCR_adjust) ---------------------------------

def test_equation_3_max_aggregation():
    """ACR is the maximum DCR_adjust across all defects."""
    defects = [
        {"DCR_raw": 1, "CC": 4, "RMC": 3},   # DCR_cc=2, DCR_adjust=T9[2,3]=2
        {"DCR_raw": 3, "CC": 4, "RMC": 3},   # DCR_cc=4, DCR_adjust=T9[4,3]=4
        {"DCR_raw": 2, "CC": 4, "RMC": 3},   # DCR_cc=3, DCR_adjust=T9[3,3]=3
    ]
    result = acr_simple(defects)
    assert result["ACR"] == 4
    assert result["n_renewal_drivers"] == 1


def test_equation_3_floor_of_one():
    """If max(DCR_adjust) = 0, ACR is set to 1 (asset still has a floor)."""
    # All defects on low criticality components → DCR_cc = 0 under Simple
    defects = [
        {"DCR_raw": 4, "CC": 1, "RMC": 3},
        {"DCR_raw": 3, "CC": 2, "RMC": 3},
    ]
    result = acr_simple(defects)
    assert result["ACR"] == 1
    assert result["n_renewal_drivers"] == 0


# ---- Equation 2 (Simple) DCR_cc behaviour reflected in ACR --------------

def test_low_cc_zeroes_defect_under_simple():
    """Simple method: CC<3 means the defect cannot drive ACR even if RMC=3 and DCR_raw=4."""
    result = acr_simple([{"DCR_raw": 4, "CC": 2, "RMC": 3}])
    assert result["ACR"] == 1


def test_high_cc_drives_acr():
    """Simple method: CC ≥ 3 means DCR_cc = DCR_raw + 1."""
    # DCR_raw=4 CC=4 RMC=3 → DCR_cc=5, DCR_adjust=T9[5,3]=5
    result = acr_simple([{"DCR_raw": 4, "CC": 4, "RMC": 3}])
    assert result["ACR"] == 5


def test_no_cc_defaults_to_increment():
    """Components without a criticality rating: DCR_cc = DCR_raw + 1."""
    result = acr_simple([{"DCR_raw": 3, "CC": None, "RMC": 3}])
    # DCR_cc=4, DCR_adjust=T9[4,3]=4
    assert result["ACR"] == 4


# ---- RMC behaviour (Table 9) --------------------------------------------

def test_rmc_1_zeroes_all_defects():
    """RMC=1 means the defect 'will not trigger renewal at any point' → DCR_adjust=0."""
    defects = [
        {"DCR_raw": 4, "CC": 4, "RMC": 1},
        {"DCR_raw": 3, "CC": 3, "RMC": 1},
    ]
    result = acr_simple(defects)
    assert result["ACR"] == 1


# ---- Worked examples fixture --------------------------------------------

def _load_worked_examples():
    rows = list(csv.DictReader(open(FIXTURES / "workedExamples.csv")))
    return [(r["scenario_id"], r) for r in rows]


@pytest.mark.parametrize("scenario_id, row", _load_worked_examples())
def test_worked_example(scenario_id, row):
    defects = _parse_defects(row["defects"])
    result = acr_simple(defects)
    assert result["ACR"] == int(row["expected_ACR"]), (
        f"{scenario_id}: ACR mismatch — got {result['ACR']}, expected {row['expected_ACR']}"
    )
    assert result["n_defects"] == int(row["expected_n_defects"]), scenario_id
    assert result["n_renewal_drivers"] == int(row["expected_n_drivers"]), scenario_id


# ---- Sample submission CSV ----------------------------------------------

def test_sample_asset_csv_validates():
    """sampleAsset.csv has 4 assets; 3 declared correctly, 1 incorrectly."""
    matches, discrepancies = validate_csv(FIXTURES / "sampleAsset.csv")
    assert len(matches) == 3
    assert len(discrepancies) == 1
    bad = discrepancies[0]
    assert bad["asset_survey_id"] == "ACME-2026-a4"
    assert bad["computed_ACR"] == 4
    assert bad["declared_ACR"] == 3


# ---- Trace integrity ----------------------------------------------------

def test_report_examples_caps_at_two():
    matches, discrepancies = validate_csv(FIXTURES / "sampleAsset.csv")
    examples = report_examples(discrepancies, max_n=2)
    assert len(examples) <= 2


def test_report_examples_empty_when_no_discrepancies():
    assert report_examples([], max_n=2) == []


def test_report_examples_narrative_includes_asset_and_acr_values():
    matches, discrepancies = validate_csv(FIXTURES / "sampleAsset.csv")
    examples = report_examples(discrepancies, max_n=2)
    for ex in examples:
        assert ex["id"] in ex["narrative"]
        assert "ACR" in ex["narrative"]
        assert "Equation" in ex["narrative"]
        assert ex["mdr_citation"].startswith("MDR Section 4.5.6.1")


def test_report_examples_prefers_largest_acr_delta():
    discrepancies = [
        {"asset_survey_id": "small", "n_defects": 2, "computed_ACR": 3, "declared_ACR": 4, "match": False},
        {"asset_survey_id": "huge",  "n_defects": 4, "computed_ACR": 5, "declared_ACR": 1, "match": False},
    ]
    examples = report_examples(discrepancies, max_n=2)
    assert examples[0]["id"] == "huge"
    assert examples[0]["delta"] == 4
    assert examples[0]["direction"] == "understated"


def test_trace_includes_all_defects():
    defects = [
        {"DCR_raw": 1, "CC": 4, "RMC": 3},
        {"DCR_raw": 2, "CC": 1, "RMC": 2},
        {"DCR_raw": 3, "CC": None, "RMC": 1},
    ]
    result = acr_simple(defects)
    assert len(result["trace"]) == 3
    for t in result["trace"]:
        assert "DCR_cc" in t
        assert "DCR_adjust" in t
