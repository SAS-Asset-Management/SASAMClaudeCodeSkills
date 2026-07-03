"""
Validation harness for the Supportability Scoring skill (MDR Section 4.6).
Tests cite Equation 7 and Figure 7 banding directly.
"""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import pytest

_SKILL_ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "supportabilityCalc", _SKILL_ROOT / "calculate.py"
)
_calc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_calc)

tti_sup = _calc.tti_sup
scr_band = _calc.scr_band
scr_for_system = _calc.scr_for_system
validate_csv = _calc.validate_csv
report_examples = _calc.report_examples

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _parse_components(spec: str) -> list[dict]:
    out = []
    if not spec:
        return out
    for triple in spec.split(";"):
        parts = triple.split(",")
        if len(parts) != 3:
            continue
        cid, tse, sy = parts
        out.append({
            "component_id": cid.strip(),
            "TSE_time": float(tse) if tse.strip() else None,
            "S_years": float(sy) if sy.strip() else None,
        })
    return out


# ---- Equation 7 ---------------------------------------------------------

def test_equation_7_basic():
    """TTI_SUP = TSE_time + S_years."""
    assert tti_sup(12.0, 5.0) == 17.0
    assert tti_sup(0.0, 0.0) == 0.0
    assert tti_sup(2.5, 1.5) == 4.0


def test_equation_7_rejects_negative():
    with pytest.raises(ValueError):
        tti_sup(-1.0, 5.0)
    with pytest.raises(ValueError):
        tti_sup(5.0, -2.0)


# ---- Figure 7 banding (with right inclusive break points) --------------

@pytest.mark.parametrize("tti, expected_scr", [
    (25.0, 1),  # > 20
    (20.01, 1),
    (20.0, 2),  # boundary — right inclusive into 2
    (15.0, 2),
    (14.01, 2),
    (14.0, 3),  # boundary
    (10.0, 3),
    (8.01, 3),
    (8.0, 4),   # boundary
    (5.0, 4),
    (3.01, 4),
    (3.0, 5),   # boundary
    (1.0, 5),
    (0.0, 5),
])
def test_figure_7_banding(tti, expected_scr):
    assert scr_band(tti) == expected_scr


# ---- System rollup ------------------------------------------------------

def test_system_takes_min_tti():
    components = [
        {"component_id": "A", "TSE_time": 30.0, "S_years": 10.0},  # TTI=40
        {"component_id": "B", "TSE_time": 2.0,  "S_years": 1.0},   # TTI=3
        {"component_id": "C", "TSE_time": 15.0, "S_years": 5.0},   # TTI=20
    ]
    result = scr_for_system(components)
    assert result["system_TTI_SUP"] == 3.0
    assert result["binding_component"] == "B"
    assert result["SCR"] == 5


def test_excluded_components_dropped_from_rollup():
    components = [
        {"component_id": "A", "TSE_time": 12.0, "S_years": 5.0},
        {"component_id": "B", "TSE_time": None, "S_years": None},
    ]
    result = scr_for_system(components)
    assert result["n_components_excluded"] == 1
    assert result["binding_component"] == "A"
    assert result["SCR"] == 2  # TTI=17 → 14<17≤20 → SCR 2


def test_all_excluded_returns_none():
    components = [
        {"component_id": "A", "TSE_time": None, "S_years": None},
        {"component_id": "B", "TSE_time": "",   "S_years": ""},
    ]
    result = scr_for_system(components)
    assert result["SCR"] is None
    assert result["system_TTI_SUP"] is None
    assert result["binding_component"] is None


# ---- Worked examples fixture --------------------------------------------

def _load_worked_examples():
    rows = list(csv.DictReader(open(FIXTURES / "workedExamples.csv")))
    return [(r["scenario_id"], r) for r in rows]


@pytest.mark.parametrize("scenario_id, row", _load_worked_examples())
def test_worked_example(scenario_id, row):
    components = _parse_components(row["components"])
    result = scr_for_system(components)
    assert result["system_TTI_SUP"] == float(row["expected_TTI"]), scenario_id
    assert result["SCR"] == int(row["expected_SCR"]), scenario_id
    assert result["binding_component"] == row["expected_binding"], scenario_id
    assert result["n_components_excluded"] == int(row["expected_excluded"]), scenario_id


# ---- Sample submission CSV ----------------------------------------------

def test_sample_system_csv_validates():
    """Three systems; two declared correctly, one (ACME-DSP-02) understated."""
    matches, discrepancies = validate_csv(FIXTURES / "sampleSystem.csv")
    assert len(matches) == 2
    assert len(discrepancies) == 1
    bad = discrepancies[0]
    assert bad["system_id"] == "ACME-DSP-02"
    assert bad["computed_SCR"] == 4
    assert bad["declared_SCR"] == 2


# ---- report_examples ----------------------------------------------------

def test_report_examples_caps_at_two():
    matches, discrepancies = validate_csv(FIXTURES / "sampleSystem.csv")
    examples = report_examples(discrepancies, max_n=2)
    assert len(examples) <= 2


def test_report_examples_empty_when_no_discrepancies():
    assert report_examples([], max_n=2) == []


def test_report_examples_narrative_cites_equation_and_binding():
    matches, discrepancies = validate_csv(FIXTURES / "sampleSystem.csv")
    examples = report_examples(discrepancies, max_n=2)
    for ex in examples:
        n = ex["narrative"]
        assert ex["id"] in n
        assert "Figure 7" in n
        assert "TTI_SUP" in n
        assert ex["mdr_citation"].startswith("MDR Section 4.6")


def test_report_examples_prefers_largest_delta():
    discrepancies = [
        {
            "system_id": "small",
            "n_components": 2,
            "n_components_excluded": 0,
            "system_TTI_SUP": 10.0,
            "binding_component": "X",
            "computed_SCR": 3,
            "declared_SCR": 2,
            "match": False,
        },
        {
            "system_id": "huge",
            "n_components": 4,
            "n_components_excluded": 0,
            "system_TTI_SUP": 1.0,
            "binding_component": "Y",
            "computed_SCR": 5,
            "declared_SCR": 1,
            "match": False,
        },
    ]
    examples = report_examples(discrepancies, max_n=2)
    assert examples[0]["id"] == "huge"
    assert examples[0]["delta"] == 4
