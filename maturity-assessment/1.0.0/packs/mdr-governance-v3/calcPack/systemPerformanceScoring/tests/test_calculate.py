"""
Validation harness for the System Performance Scoring skill (MDR Section 4.7).
Tests cite the Equation / Table 12 row they validate.
"""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import pytest

_SKILL_ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "systemPerformanceCalc", _SKILL_ROOT / "calculate.py"
)
_calc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_calc)

fit_power_law = _calc.fit_power_law
chi_squared_trend = _calc.chi_squared_trend
spcr_band = _calc.spcr_band
spcr_from_failures = _calc.spcr_from_failures
validate_csv = _calc.validate_csv
report_examples = _calc.report_examples

FIXTURES = Path(__file__).resolve().parent / "fixtures"


# ---- Equation 10 (β estimate) -------------------------------------------

def test_equation_10_beta_known_inputs():
    """Hand computed: t = [1,2,3,4,5], β̂ = 5 / (5·ln(5) − Σ ln(t_i))."""
    fit = fit_power_law([1, 2, 3, 4, 5])
    expected_denom = 5 * math.log(5) - sum(math.log(t) for t in [1, 2, 3, 4, 5])
    expected_beta = 5 / expected_denom
    assert math.isclose(fit["beta"], expected_beta, rel_tol=1e-9)
    assert fit["m"] == 5
    assert fit["t_k"] == 5


def test_equation_9_theta_uses_beta_and_t_k():
    """θ̂ = m / (t_k)^β̂."""
    fit = fit_power_law([1, 2, 3, 4, 5])
    expected_theta = 5 / (5 ** fit["beta"])
    assert math.isclose(fit["theta"], expected_theta, rel_tol=1e-9)


def test_fit_returns_none_for_insufficient_data():
    assert fit_power_law([])["m"] == 0
    assert fit_power_law([])["beta"] is None
    assert fit_power_law([3.5])["m"] == 1
    assert fit_power_law([3.5])["beta"] is None


def test_fit_rejects_non_positive_times():
    with pytest.raises(ValueError):
        fit_power_law([0.0, 1.0, 2.0])
    with pytest.raises(ValueError):
        fit_power_law([-1.0, 2.0])


# ---- Equation 11 (χ² trend statistic) -----------------------------------

def test_equation_11_chi_squared_known_inputs():
    """χ² = 2 · Σ_{i=1..m-1} ln(t_k / t_i),  df = 2(m-1)."""
    t = [1.0, 2.0, 3.0, 4.0, 5.0]
    chi = chi_squared_trend(t)
    t_k = max(t)
    expected = 2.0 * sum(math.log(t_k / t_i) for t_i in t[:-1])
    assert math.isclose(chi["chi_squared"], expected, rel_tol=1e-9)
    assert chi["df"] == 2 * (len(t) - 1)


def test_equation_12_p_is_smaller_tail():
    """p = min(F(χ²), 1 − F(χ²)) — must always be ≤ 0.5."""
    chi = chi_squared_trend([1.0, 2.0, 3.0, 4.0, 5.0])
    assert 0.0 <= chi["p_value"] <= 0.5


# ---- Table 12 banding ---------------------------------------------------

@pytest.mark.parametrize("beta, p, expected_spcr", [
    (None, None, 1),
    (0.5, 0.001, 1),    # β ≤ 1 dominates regardless of p
    (1.0, 0.001, 1),    # β ≤ 1 dominates
    (1.5, 0.30, 1),     # p ≥ 0.20 → SPCR 1
    (1.5, 0.20, 1),     # boundary — p ≥ 0.20 inclusive into 1
    (1.5, 0.19, 2),     # 0.20 > p ≥ 0.10
    (1.5, 0.10, 2),     # boundary — p ≥ 0.10 inclusive into 2
    (1.5, 0.09, 3),     # 0.10 > p ≥ 0.05
    (1.5, 0.05, 3),     # boundary — p ≥ 0.05 inclusive into 3
    (1.5, 0.04, 4),     # 0.05 > p ≥ 0.02
    (1.5, 0.02, 4),     # boundary — p ≥ 0.02 inclusive into 4
    (1.5, 0.01, 5),     # p < 0.02
    (1.5, 0.0, 5),
])
def test_table_12_banding(beta, p, expected_spcr):
    spcr, _, _ = spcr_band(beta, p)
    assert spcr == expected_spcr


# ---- Edge cases (insufficient data, β ≤ 1) -----------------------------

def test_zero_failures_returns_spcr_1_with_insufficient_data_rule():
    r = spcr_from_failures([])
    assert r["SPCR"] == 1
    assert "insufficient data" in r["rule"]


def test_one_failure_returns_spcr_1_with_insufficient_data_rule():
    r = spcr_from_failures([3.5])
    assert r["SPCR"] == 1
    assert "insufficient data" in r["rule"]


def test_beta_le_one_skips_chi_squared():
    """When β̂ ≤ 1, the chi squared test is not performed."""
    r = spcr_from_failures([0.1, 0.5, 1.0, 5.0, 10.0])
    assert r["beta"] < 1.0
    assert r["chi_squared"] is None
    assert r["SPCR"] == 1


# ---- Worked examples ----------------------------------------------------

def _load_scenarios():
    data = json.loads((FIXTURES / "workedExamples.json").read_text())
    return [(s["scenario_id"], s) for s in data["scenarios"]]


@pytest.mark.parametrize("scenario_id, scenario", _load_scenarios())
def test_worked_example_reproduces_fixture(scenario_id, scenario):
    """Each fixture row must round trip through calculate.py to the same numbers."""
    r = spcr_from_failures(scenario["t_values"])
    assert r["m"] == scenario["expected_m"], scenario_id
    assert r["SPCR"] == scenario["expected_SPCR"], scenario_id
    if scenario["expected_beta"] is not None:
        assert math.isclose(r["beta"], scenario["expected_beta"], rel_tol=1e-9), scenario_id
    if scenario["expected_p_value"] is not None:
        assert math.isclose(r["p_value"], scenario["expected_p_value"], rel_tol=1e-9), scenario_id


# ---- Sample groups CSV --------------------------------------------------

def test_sample_groups_csv_validates():
    """Three groups: one understated (1 declared, 5 computed); two correct."""
    matches, discrepancies = validate_csv(FIXTURES / "sampleGroups.csv")
    assert len(matches) == 2
    assert len(discrepancies) == 1
    bad = discrepancies[0]
    assert bad["group"] == "ACME-SIG-trackCircuits"
    assert bad["declared_SPCR"] == 1
    assert bad["computed_SPCR"] == 5


# ---- report_examples ----------------------------------------------------

def test_report_examples_caps_at_two():
    matches, discrepancies = validate_csv(FIXTURES / "sampleGroups.csv")
    examples = report_examples(discrepancies, max_n=2)
    assert len(examples) <= 2


def test_report_examples_empty_when_no_discrepancies():
    assert report_examples([], max_n=2) == []


def test_report_examples_narrative_cites_table_and_diagnostics():
    matches, discrepancies = validate_csv(FIXTURES / "sampleGroups.csv")
    examples = report_examples(discrepancies, max_n=2)
    for ex in examples:
        n = ex["narrative"]
        assert ex["id"] in n
        assert "Table 12" in n
        assert "β̂" in n or "β" in n  # diagnostics surfaced
        assert "Crow AMSAA" in n or "fit" in n
        assert ex["mdr_citation"].startswith("MDR Section 4.7")


def test_report_examples_prefers_largest_delta():
    discrepancies = [
        {
            "group": "small", "m": 5, "t_k": 5.0, "beta": 1.5, "theta": 0.1,
            "chi_squared": 6.5, "df": 8, "p_value": 0.4,
            "computed_SPCR": 1, "declared_SPCR": 2, "rule": TABLE_12_RULE_1, "narrative": "x", "match": False,
        },
        {
            "group": "huge", "m": 11, "t_k": 10.0, "beta": 3.3, "theta": 0.05,
            "chi_squared": 5.0, "df": 20, "p_value": 0.001,
            "computed_SPCR": 5, "declared_SPCR": 1, "rule": TABLE_12_RULE_5, "narrative": "y", "match": False,
        },
    ]
    examples = report_examples(discrepancies, max_n=2)
    assert examples[0]["id"] == "huge"
    assert examples[0]["delta"] == 4


# Sentinel rule strings to keep the mock test readable
TABLE_12_RULE_1 = "p ≥ 0.20 or β ≤ 1"
TABLE_12_RULE_5 = "β > 1 and p < 0.02"
