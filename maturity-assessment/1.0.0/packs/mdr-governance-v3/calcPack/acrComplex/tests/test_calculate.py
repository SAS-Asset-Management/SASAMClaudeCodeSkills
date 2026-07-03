"""
Validation harness for the Complex ACR method (MDR Section 4.5.6.2).

Tests cite the equation they validate. Worked examples in fixtures/workedExamples.json
are derived from the MDR equations and serve as the independent reference.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

_SKILL_ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("acrComplexCalc", _SKILL_ROOT / "calculate.py")
_calc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_calc)

aecr_for_element = _calc.aecr_for_element
acr_complex = _calc.acr_complex
percentile_80 = _calc.percentile_80
validate_csv = _calc.validate_csv
report_examples = _calc.report_examples

FIXTURES = Path(__file__).resolve().parent / "fixtures"


# ---- Equation 4 (Complex DCR_cc) reflected in element AECR --------------

def test_low_cc_passes_through_under_complex():
    """Complex method: CC<3 means DCR_cc = DCR_raw (no zero-out)."""
    # DCR_raw=2 CC=1 RMC=3 → DCR_cc=2, DCR_adjust=T9[2,3]=2 → AECR=2
    result = aecr_for_element([{"DCR_raw": 2, "CC": 1, "RMC": 3}])
    assert result["AECR"] == 2


def test_high_cc_increments_dcc():
    # DCR_raw=4 CC=4 RMC=3 → DCR_cc=5, DCR_adjust=T9[5,3]=5 → AECR=5
    result = aecr_for_element([{"DCR_raw": 4, "CC": 4, "RMC": 3}])
    assert result["AECR"] == 5


def test_no_cc_increments_dcc():
    result = aecr_for_element([{"DCR_raw": 3, "CC": None, "RMC": 3}])
    # DCR_cc=4, DCR_adjust=T9[4,3]=4
    assert result["AECR"] == 4


# ---- Equation 5 (AECR = max DCR_adjust) + floor rule -------------------

def test_equation_5_max_aggregation():
    defects = [
        {"DCR_raw": 1, "CC": 4, "RMC": 3},   # DCR_adjust=2
        {"DCR_raw": 4, "CC": 4, "RMC": 3},   # DCR_adjust=5
        {"DCR_raw": 2, "CC": 4, "RMC": 3},   # DCR_adjust=3
    ]
    assert aecr_for_element(defects)["AECR"] == 5


def test_floor_no_defects():
    """Element with no defects has AECR = 1 (Section 4.5.6.2 step 7)."""
    assert aecr_for_element([])["AECR"] == 1


def test_floor_all_zeroed_by_rmc():
    """Element where all defects have RMC=1 (DCR_adjust=0) floors to AECR = 1."""
    defects = [
        {"DCR_raw": 4, "CC": 4, "RMC": 1},
        {"DCR_raw": 3, "CC": 3, "RMC": 1},
    ]
    assert aecr_for_element(defects)["AECR"] == 1


def test_inaccessible_element_returns_minus_one():
    """Section 4.5.6.2 step 8: inaccessible elements get AECR=-1 and are excluded."""
    assert aecr_for_element([], inspected=False)["AECR"] == -1


# ---- 80th percentile (Equation 6) ---------------------------------------

@pytest.mark.parametrize("values, expected", [
    ([1], 1),                                          # n=1, ceil(0.8)-1=0
    ([1, 5], 5),                                       # n=2, ceil(1.6)-1=1
    ([1, 2, 3, 4, 5], 4),                              # n=5, ceil(4.0)-1=3
    ([1, 1, 1, 2, 2, 3, 3, 4, 5, 5], 4),               # n=10, ceil(8.0)-1=7
    ([1, 1, 1, 1, 1, 1, 1, 1, 1, 5], 1),               # n=10, single severe → still 1
    ([5, 5, 5], 5),                                    # all worst → 5
    ([1, 1, 1], 1),                                    # all clean → 1
    ([3, 3, 3, 3, 3, 3, 3], 3),                        # n=7, ceil(5.6)-1=5 → all 3s
])
def test_percentile_80(values, expected):
    assert percentile_80(values) == expected


def test_percentile_80_empty_returns_none():
    assert percentile_80([]) is None


# ---- Worked examples ----------------------------------------------------

def _load_scenarios():
    data = json.loads((FIXTURES / "workedExamples.json").read_text())
    return [(s["scenario_id"], s) for s in data["scenarios"]]


@pytest.mark.parametrize("scenario_id, scenario", _load_scenarios())
def test_worked_example(scenario_id, scenario):
    result = acr_complex(scenario["elements"])
    assert result["ACR"] == scenario["expected_ACR"], (
        f"{scenario_id}: ACR mismatch — got {result['ACR']}, expected {scenario['expected_ACR']}"
    )
    assert result["n_elements_inspected"] == scenario["expected_n_inspected"], scenario_id
    assert result["n_elements_excluded"] == scenario["expected_n_excluded"], scenario_id

    # Distribution is keyed by string in JSON; convert for comparison
    expected_dist = {int(k): v for k, v in scenario["expected_aecr_distribution"].items()}
    assert result["aecr_distribution"] == expected_dist, scenario_id


# ---- Sample submission CSV ----------------------------------------------

def test_sample_asset_csv_validates():
    """Both assets in sampleAsset.csv have correct declared ACRs and AECRs."""
    matches, discrepancies = validate_csv(FIXTURES / "sampleAsset.csv")
    assert len(matches) == 2
    assert len(discrepancies) == 0


# ---- Trace integrity ----------------------------------------------------

def test_report_examples_caps_at_two():
    discrepancies = [
        {
            "asset_survey_id": "a1",
            "n_elements_inspected": 5,
            "n_elements_excluded": 0,
            "computed_ACR": 4,
            "declared_ACR": 2,
            "aecr_mismatches": [],
            "match": False,
        },
        {
            "asset_survey_id": "a2",
            "n_elements_inspected": 8,
            "n_elements_excluded": 1,
            "computed_ACR": 3,
            "declared_ACR": 5,
            "aecr_mismatches": [],
            "match": False,
        },
        {
            "asset_survey_id": "a3",
            "n_elements_inspected": 4,
            "n_elements_excluded": 0,
            "computed_ACR": 1,
            "declared_ACR": 1,
            "aecr_mismatches": [
                {"element_id": "e2", "computed_AECR": 1, "declared_AECR": 4},
            ],
            "match": False,
        },
    ]
    examples = report_examples(discrepancies, max_n=2)
    assert len(examples) == 2


def test_report_examples_empty_when_no_discrepancies():
    assert report_examples([], max_n=2) == []


def test_report_examples_prefers_asset_then_element():
    """When asset level and element level errors coexist, surface one of each."""
    discrepancies = [
        {
            "asset_survey_id": "a1",
            "n_elements_inspected": 5,
            "n_elements_excluded": 0,
            "computed_ACR": 4,
            "declared_ACR": 2,  # delta=2 asset level
            "aecr_mismatches": [],
            "match": False,
        },
        {
            "asset_survey_id": "a2",
            "n_elements_inspected": 4,
            "n_elements_excluded": 0,
            "computed_ACR": 3,
            "declared_ACR": 3,  # asset matches, but element doesn't
            "aecr_mismatches": [
                {"element_id": "e1", "computed_AECR": 1, "declared_AECR": 5}
            ],
            "match": False,
        },
    ]
    examples = report_examples(discrepancies, max_n=2)
    levels = [e["level"] for e in examples]
    assert "asset" in levels
    assert "element" in levels


def test_report_examples_narratives_cite_equations():
    discrepancies = [
        {
            "asset_survey_id": "a1",
            "n_elements_inspected": 10,
            "n_elements_excluded": 1,
            "computed_ACR": 4,
            "declared_ACR": 2,
            "aecr_mismatches": [],
            "match": False,
        },
    ]
    examples = report_examples(discrepancies, max_n=2)
    assert len(examples) == 1
    assert "Equation 6" in examples[0]["narrative"] or "80%ile" in examples[0]["narrative"]
    assert examples[0]["delta"] == 2
    assert examples[0]["direction"] == "understated"


def test_trace_per_element_includes_defects():
    elements = [
        {"element_id": "e1", "inspected": True, "defects": [
            {"DCR_raw": 2, "CC": 4, "RMC": 3},
            {"DCR_raw": 1, "CC": 1, "RMC": 2},
        ]},
        {"element_id": "e2", "inspected": False, "defects": []},
    ]
    result = acr_complex(elements)
    assert len(result["elements"]) == 2
    assert len(result["elements"][0]["trace"]) == 2
    assert len(result["elements"][1]["trace"]) == 0
    assert result["elements"][1]["AECR"] == -1
