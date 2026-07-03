"""
Validation harness for the MDR defect scoring cascade.

Tests are organised so each one cites the MDR section / equation it validates.
The truth table is generated inside the test from a literal encoding of
Table 9 + Equations 2 and 4 — so the test is an *independent* reference
implementation against which calculate.py is checked.
"""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import pytest

_SKILL_ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("defectScoringCalc", _SKILL_ROOT / "calculate.py")
_calc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_calc)

TABLE_9 = _calc.TABLE_9
dcr_adjust = _calc.dcr_adjust
dcr_cc = _calc.dcr_cc
score_defect = _calc.score_defect
validate_csv = _calc.validate_csv
report_examples = _calc.report_examples


# Independent encoding of MDR Table 9 (p.20). DCR_cc rows 1 to 5, RMC cols 1 to 3.
MDR_TABLE_9 = {
    (1, 1): 0, (1, 2): 0, (1, 3): 1,
    (2, 1): 0, (2, 2): 1, (2, 3): 2,
    (3, 1): 0, (3, 2): 2, (3, 3): 3,
    (4, 1): 0, (4, 2): 2, (4, 3): 4,
    (5, 1): 0, (5, 2): 3, (5, 3): 5,
}


def _expected_dcr_cc(dcr_raw: int, cc, method: str) -> int:
    """Independent reference for Equations 2 and 4."""
    if cc is None:
        return dcr_raw + 1
    if method == "simple":
        return 0 if cc < 3 else dcr_raw + 1
    return dcr_raw if cc < 3 else dcr_raw + 1


def _expected_dcr_adjust(dcr_cc_value: int, rmc: int) -> int:
    if dcr_cc_value == 0:
        return 0
    return MDR_TABLE_9[(dcr_cc_value, rmc)]


# ---- Table 9 (MDR p.20) --------------------------------------------------

@pytest.mark.parametrize("dcr_cc_value, rmc, expected", [
    (k[0], k[1], v) for k, v in MDR_TABLE_9.items()
])
def test_table_9_lookup(dcr_cc_value, rmc, expected):
    """Every cell of Table 9 must be reproduced by calculate.py."""
    assert TABLE_9[(dcr_cc_value, rmc)] == expected
    assert dcr_adjust(dcr_cc_value, rmc) == expected


def test_table_9_dcr_cc_zero_short_circuit():
    """DCR_cc = 0 (Simple method, CC<3) drops to DCR_adjust = 0 for any RMC."""
    for rmc in (1, 2, 3):
        assert dcr_adjust(0, rmc) == 0


# ---- Equation 2 (Simple, MDR p.21) ---------------------------------------

@pytest.mark.parametrize("dcr_raw", [1, 2, 3, 4])
@pytest.mark.parametrize("cc", [1, 2])
def test_equation_2_simple_low_criticality_zeroes_dcc(dcr_raw, cc):
    assert dcr_cc(dcr_raw, cc, "simple") == 0


@pytest.mark.parametrize("dcr_raw", [1, 2, 3, 4])
@pytest.mark.parametrize("cc", [3, 4])
def test_equation_2_simple_high_criticality_increments(dcr_raw, cc):
    assert dcr_cc(dcr_raw, cc, "simple") == dcr_raw + 1


@pytest.mark.parametrize("dcr_raw", [1, 2, 3, 4])
def test_equation_2_simple_no_criticality_increments(dcr_raw):
    assert dcr_cc(dcr_raw, None, "simple") == dcr_raw + 1


# ---- Equation 4 (Complex, MDR p.22) --------------------------------------

@pytest.mark.parametrize("dcr_raw", [1, 2, 3, 4])
@pytest.mark.parametrize("cc", [1, 2])
def test_equation_4_complex_low_criticality_passes_through(dcr_raw, cc):
    assert dcr_cc(dcr_raw, cc, "complex") == dcr_raw


@pytest.mark.parametrize("dcr_raw", [1, 2, 3, 4])
@pytest.mark.parametrize("cc", [3, 4])
def test_equation_4_complex_high_criticality_increments(dcr_raw, cc):
    assert dcr_cc(dcr_raw, cc, "complex") == dcr_raw + 1


@pytest.mark.parametrize("dcr_raw", [1, 2, 3, 4])
def test_equation_4_complex_no_criticality_increments(dcr_raw):
    assert dcr_cc(dcr_raw, None, "complex") == dcr_raw + 1


# ---- Full cascade truth table -------------------------------------------

def _all_combinations():
    for method in ("simple", "complex"):
        for cc in (1, 2, 3, 4, None):
            for dcr_raw in (1, 2, 3, 4):
                for rmc in (1, 2, 3):
                    yield method, cc, dcr_raw, rmc


def test_full_cascade_truth_table():
    """120 row cascade — every (method, CC, DCR_raw, RMC) combination."""
    for method, cc, dcr_raw, rmc in _all_combinations():
        result = score_defect(dcr_raw, cc, rmc, method)
        expected_cc = _expected_dcr_cc(dcr_raw, cc, method)
        expected_adj = _expected_dcr_adjust(expected_cc, rmc)
        assert result["DCR_cc"] == expected_cc, (
            f"DCR_cc mismatch for method={method} CC={cc} DCR_raw={dcr_raw} RMC={rmc}: "
            f"got {result['DCR_cc']}, expected {expected_cc}"
        )
        assert result["DCR_adjust"] == expected_adj, (
            f"DCR_adjust mismatch for method={method} CC={cc} DCR_raw={dcr_raw} RMC={rmc}: "
            f"got {result['DCR_adjust']}, expected {expected_adj}"
        )


# ---- Spec edge cases -----------------------------------------------------

def test_dcr_raw_out_of_range_rejected():
    with pytest.raises(ValueError):
        dcr_cc(0, 3, "complex")
    with pytest.raises(ValueError):
        dcr_cc(5, 3, "complex")


def test_cc_out_of_range_rejected():
    with pytest.raises(ValueError):
        dcr_cc(2, 0, "complex")
    with pytest.raises(ValueError):
        dcr_cc(2, 5, "complex")


def test_rmc_out_of_range_rejected():
    with pytest.raises(ValueError):
        dcr_adjust(3, 0)
    with pytest.raises(ValueError):
        dcr_adjust(3, 4)


def test_unknown_method_rejected():
    with pytest.raises(ValueError):
        dcr_cc(2, 3, "hybrid")


# ---- CSV validation ------------------------------------------------------

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_sample_submission_complex_partial_match():
    """sampleSubmissionComplex.csv has 6 rows; 4 declared correctly, 2 incorrectly."""
    matches, discrepancies = validate_csv(FIXTURES / "sampleSubmissionComplex.csv", "complex")
    assert len(matches) == 4
    assert len(discrepancies) == 2
    for d in discrepancies:
        assert d["DCR_cc_match"] is False or d["DCR_adjust_match"] is False


def test_report_examples_caps_at_two():
    """report_examples never returns more than max_n entries."""
    matches, discrepancies = validate_csv(FIXTURES / "sampleSubmissionComplex.csv", "complex")
    examples = report_examples(discrepancies, "complex", max_n=2)
    assert len(examples) <= 2
    assert len(examples) == 2  # sample has exactly 2 discrepancies


def test_report_examples_empty_when_no_discrepancies():
    assert report_examples([], "complex", max_n=2) == []


def test_report_examples_narrative_includes_ids_and_rule():
    """Each example must cite the defect ID, the values, and the MDR rule."""
    matches, discrepancies = validate_csv(FIXTURES / "sampleSubmissionComplex.csv", "complex")
    examples = report_examples(discrepancies, "complex", max_n=2)
    for ex in examples:
        narrative = ex["narrative"]
        assert ex["id"] in narrative or ex["id"] is None
        assert "MDR" in narrative or "Equation" in narrative or "Table 9" in narrative
        assert ex["mdr_citation"]


def test_report_examples_prefers_higher_severity():
    """Synthetic discrepancies — the larger DCR_adjust delta should appear first."""
    discrepancies = [
        # delta = 1
        {
            "defect_survey_id": "small",
            "asset_id": "a1",
            "DCR_raw": "2",
            "CC": "4",
            "RMC": "2",
            "DCR_cc": "3",
            "DCR_adjust": "1",
            "computed_DCR_cc": 3,
            "computed_DCR_adjust": 2,
            "DCR_cc_match": True,
            "DCR_adjust_match": False,
        },
        # delta = 5 (declared 0, computed 5)
        {
            "defect_survey_id": "huge",
            "asset_id": "a2",
            "DCR_raw": "4",
            "CC": "4",
            "RMC": "3",
            "DCR_cc": "5",
            "DCR_adjust": "0",
            "computed_DCR_cc": 5,
            "computed_DCR_adjust": 5,
            "DCR_cc_match": True,
            "DCR_adjust_match": False,
        },
    ]
    examples = report_examples(discrepancies, "complex", max_n=2)
    assert examples[0]["id"] == "huge"


def test_truth_table_csv_matches_calculate():
    """The committed truthTable.csv must agree with calculate.py for every row."""
    rows = list(csv.DictReader(open(FIXTURES / "truthTable.csv")))
    assert len(rows) == 120, f"Expected 120 rows, got {len(rows)}"
    for row in rows:
        cc = None if row["CC"] == "" else int(row["CC"])
        result = score_defect(
            int(row["DCR_raw"]), cc, int(row["RMC"]), row["method"]
        )
        assert result["DCR_cc"] == int(row["expected_DCR_cc"]), row
        assert result["DCR_adjust"] == int(row["expected_DCR_adjust"]), row
