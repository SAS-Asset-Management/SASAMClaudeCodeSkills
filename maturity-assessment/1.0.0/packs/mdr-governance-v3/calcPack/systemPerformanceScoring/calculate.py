"""
System Performance Scoring — power law NHPP fit + SPCR (MDR Section 4.7).

Reference implementation of:
  - Equation 8   — Power law M(t) = θ · t^β
  - Equation 9   — θ̂ = m / (t_k)^β̂
  - Equation 10  — β̂ = m / (m·ln(t_k) − Σ ln(t_i))
  - Equation 11  — χ² = 2 · Σ_{i=1..m-1} ln(t_k / t_i),  df = 2·(m-1)
  - Equation 12  — p = min(F(χ²), 1 − F(χ²))   (smaller tail of two sided test)
  - Table 12     — SPCR banding (β, p) → 1..5

Public API:
    fit_power_law(t_values: list[float]) -> dict          # β̂, θ̂, m, t_k
    spcr_from_failures(t_values: list[float]) -> dict     # full result + SPCR
    validate_csv(path) -> tuple[matches, discrepancies]
    report_examples(discrepancies, max_n=2) -> list[dict]

CLI:
    python calculate.py compute  --failures "1.2,3.4,5.0,7.1,8.5"
    python calculate.py validate path/to/submission.csv [--report path]

Pure stdlib. The chi squared CDF is computed in closed form because the
degrees of freedom, df = 2(m - 1), are always even.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Optional



def _chi2_cdf(x: float, df: int) -> float:
    """
    Chi squared CDF for even degrees of freedom, in closed form:
        F(x; 2k) = 1 - exp(-x/2) * sum_{i=0}^{k-1} (x/2)^i / i!
    df is always even here (df = 2(m - 1)), so no gamma function is needed.
    """
    if df <= 0 or df % 2 != 0:
        raise ValueError(f"df must be a positive even integer (got {df})")
    if x <= 0:
        return 0.0
    k = df // 2
    half = x / 2.0
    term = math.exp(-half)
    total = term
    for i in range(1, k):
        term *= half / i
        total += term
    return 1.0 - total


# Table 12 row interpretations
TABLE_12_ROWS = {
    1: "Statistically significant evidence does not exist to suggest an increase in failure rate. Or system is improving / stable.",
    2: "Weak evidence exists to suggest an increase in failure rate.",
    3: "Some evidence exists to suggest an increase in failure rate.",
    4: "Evidence exists to suggest an increase in failure rate.",
    5: "Strong evidence exists to suggest an increase in failure rate.",
}

TABLE_12_RULES = {
    1: "p ≥ 0.20 or β ≤ 1",
    2: "β > 1 and 0.20 > p ≥ 0.10",
    3: "β > 1 and 0.10 > p ≥ 0.05",
    4: "β > 1 and 0.05 > p ≥ 0.02",
    5: "β > 1 and p < 0.02",
}


def fit_power_law(t_values: list[float]) -> dict:
    """
    Compute β̂, θ̂, m, t_k for a power law NHPP fit (Equations 9 and 10).

    t_values must be ages in years measured from the start of the observation
    window. They are sorted ascending before fitting.

    Returns:
        m, t_k, beta, theta, ln_sum (Σ ln(t_i))
        beta and theta are None when m < 2 or t_k <= 0 or all t_i are equal.
    """
    t = sorted(float(v) for v in t_values if v is not None)
    m = len(t)
    if m < 2:
        return {"m": m, "t_k": (t[0] if t else None), "beta": None, "theta": None, "ln_sum": None}
    if any(v <= 0 for v in t):
        raise ValueError("All failure times must be > 0 (measured from start_test_time)")

    t_k = t[-1]
    ln_sum = sum(math.log(v) for v in t)
    denom = m * math.log(t_k) - ln_sum
    if denom <= 0:
        # Pathological — failures all clustered at t_k or numerical degeneracy
        return {"m": m, "t_k": t_k, "beta": None, "theta": None, "ln_sum": ln_sum}

    beta = m / denom
    theta = m / (t_k ** beta)
    return {"m": m, "t_k": t_k, "beta": beta, "theta": theta, "ln_sum": ln_sum}


def chi_squared_trend(t_values: list[float]) -> dict:
    """
    Equation 11 — χ² = 2 · Σ_{i=1..m-1} ln(t_k / t_i),  df = 2(m-1).
    Returns dict with chi_squared, df, p_value (smaller tail of χ² CDF).
    """
    t = sorted(float(v) for v in t_values if v is not None)
    m = len(t)
    if m < 2:
        return {"chi_squared": None, "df": None, "p_value": None}

    t_k = t[-1]
    chi_sq = 2.0 * sum(math.log(t_k / t_i) for t_i in t[:-1])
    df = 2 * (m - 1)
    F = _chi2_cdf(chi_sq, df)
    p = min(F, 1.0 - F)
    return {"chi_squared": chi_sq, "df": df, "p_value": p}


def spcr_band(beta: Optional[float], p: Optional[float]) -> tuple[int, str, str]:
    """
    Apply Table 12 banding. Returns (SPCR, rule, narrative).
    """
    if beta is None or beta <= 1.0 or p is None:
        return 1, TABLE_12_RULES[1], TABLE_12_ROWS[1]
    if p >= 0.20:
        return 1, TABLE_12_RULES[1], TABLE_12_ROWS[1]
    if p >= 0.10:
        return 2, TABLE_12_RULES[2], TABLE_12_ROWS[2]
    if p >= 0.05:
        return 3, TABLE_12_RULES[3], TABLE_12_ROWS[3]
    if p >= 0.02:
        return 4, TABLE_12_RULES[4], TABLE_12_ROWS[4]
    return 5, TABLE_12_RULES[5], TABLE_12_ROWS[5]


def spcr_from_failures(t_values: list[float]) -> dict:
    """
    Full SPCR cascade. Returns m, t_k, β, θ, χ², df, p, SPCR, rule, narrative.

    For groups with m < 2 we short circuit to SPCR = 1 with an "insufficient
    data" rule string — consistent with the MDR's intent (you cannot evidence
    a trend without at least two failures).
    """
    fit = fit_power_law(t_values)
    if fit["m"] < 2:
        return {
            **fit,
            "chi_squared": None,
            "df": None,
            "p_value": None,
            "SPCR": 1,
            "rule": "insufficient data (m < 2)",
            "narrative": "Fewer than two failures observed; trend cannot be evidenced. SPCR floors to 1.",
        }

    if fit["beta"] is None or fit["beta"] <= 1.0:
        return {
            **fit,
            "chi_squared": None,
            "df": None,
            "p_value": None,
            "SPCR": 1,
            "rule": TABLE_12_RULES[1],
            "narrative": TABLE_12_ROWS[1],
        }

    chi = chi_squared_trend(t_values)
    spcr, rule, narrative = spcr_band(fit["beta"], chi["p_value"])
    return {**fit, **chi, "SPCR": spcr, "rule": rule, "narrative": narrative}


# ---- CSV ingest / validate ----------------------------------------------

def _years_between(start: str, event: str) -> float:
    """Convert two dd/mm/yyyy or yyyy-mm-dd dates to years between them."""
    from datetime import datetime
    fmts = ("%d/%m/%Y", "%Y-%m-%d", "%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S")
    s = e = None
    for fmt in fmts:
        try:
            s = s or datetime.strptime(start, fmt)
        except ValueError:
            pass
        try:
            e = e or datetime.strptime(event, fmt)
        except ValueError:
            pass
    if s is None or e is None:
        raise ValueError(f"Could not parse dates: start={start!r}, event={event!r}")
    return (e - s).total_seconds() / (365.25 * 24 * 3600)


def spcr_from_csv(
    path: Path,
    group_key: str = "group",
) -> dict[str, dict]:
    """
    Read a CSV of failure events grouped by `group_key`. Each row should
    contain either a `t` column (years since start_test_time) or both
    `start_test_time` and `failure_time` columns (date strings).
    Returns per group SPCR result.
    """
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if row.get("t") not in (None, ""):
            grouped[row[group_key]].append(float(row["t"]))
        elif row.get("start_test_time") and row.get("failure_time"):
            grouped[row[group_key]].append(
                _years_between(row["start_test_time"], row["failure_time"])
            )
    return {gid: spcr_from_failures(t) for gid, t in grouped.items()}


def validate_csv(
    path: Path,
    group_key: str = "group",
    declared_spcr_col: str = "SPCR",
) -> tuple[list[dict], list[dict]]:
    """
    Validate declared SPCR against recomputed SPCR per group.
    Returns (matches, discrepancies).
    """
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    declared: dict[str, Optional[int]] = {}
    for row in rows:
        d = row.get(declared_spcr_col)
        if d not in (None, ""):
            declared[row[group_key]] = int(d)

    computed = spcr_from_csv(path, group_key)

    matches, discrepancies = [], []
    for gid, result in computed.items():
        record = {
            "group": gid,
            "m": result["m"],
            "t_k": result["t_k"],
            "beta": result["beta"],
            "theta": result.get("theta"),
            "chi_squared": result.get("chi_squared"),
            "df": result.get("df"),
            "p_value": result.get("p_value"),
            "computed_SPCR": result["SPCR"],
            "declared_SPCR": declared.get(gid),
            "rule": result["rule"],
            "narrative": result["narrative"],
            "match": (
                declared.get(gid) is None or declared.get(gid) == result["SPCR"]
            ),
        }
        (matches if record["match"] else discrepancies).append(record)
    return matches, discrepancies


def report_examples(discrepancies: list[dict], max_n: int = 2) -> list[dict]:
    """
    Return up to `max_n` representative SPCR discrepancies in report ready form.
    Ranked by |declared_SPCR - computed_SPCR|.
    """
    if not discrepancies:
        return []

    def severity(d: dict) -> int:
        if d.get("declared_SPCR") is None or d.get("computed_SPCR") is None:
            return 0
        return abs(int(d["declared_SPCR"]) - int(d["computed_SPCR"]))

    ranked = sorted(discrepancies, key=lambda d: -severity(d))[:max_n]

    examples: list[dict] = []
    for d in ranked:
        delta = severity(d)
        direction = "overstated" if int(d["declared_SPCR"]) > int(d["computed_SPCR"]) else "understated"
        # Numeric diagnostics are only meaningful when m >= 2
        if d.get("beta") is not None and d.get("p_value") is not None:
            diag = (
                f"m = {d['m']} failures over {d['t_k']:.2f} years, "
                f"β̂ = {d['beta']:.3f}, χ² = {d['chi_squared']:.2f} "
                f"with df = {d['df']}, two sided p = {d['p_value']:.4f}"
            )
        elif d.get("beta") is not None:
            diag = f"m = {d['m']}, β̂ = {d['beta']:.3f} (≤ 1 → no trend test)"
        else:
            diag = f"m = {d['m']} (insufficient data)"

        narrative = (
            f"Group \"{d['group']}\" declared SPCR = {d['declared_SPCR']} but "
            f"the Crow AMSAA fit ({diag}) yields SPCR = {d['computed_SPCR']} "
            f"— Table 12 rule \"{d['rule']}\" ({d['narrative']}). "
            f"Condition {direction} by {delta} point(s)."
        )
        examples.append({
            "id": d["group"],
            "declared_SPCR": d["declared_SPCR"],
            "computed_SPCR": d["computed_SPCR"],
            "m": d["m"],
            "beta": d["beta"],
            "p_value": d["p_value"],
            "delta": delta,
            "direction": direction,
            "rule": d["rule"],
            "mdr_citation": "MDR Section 4.7 (Equations 8 to 12, Table 12)",
            "narrative": narrative,
        })
    return examples


# ---- CLI ----------------------------------------------------------------

def _parse_failures_flag(s: str) -> list[float]:
    return [float(v) for v in s.split(",") if v.strip()]


def _cli() -> int:
    parser = argparse.ArgumentParser(description="MDR System Performance Scoring")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_compute = sub.add_parser("compute", help="Compute SPCR from inline failure ages")
    p_compute.add_argument(
        "--failures",
        type=str,
        required=True,
        help="Comma separated failure ages in years (since start_test_time)",
    )

    p_validate = sub.add_parser("validate", help="Validate a franchisee system performance CSV")
    p_validate.add_argument("path", type=Path)
    p_validate.add_argument("--group-key", default="group")
    p_validate.add_argument("--report", type=Path, default=None)

    args = parser.parse_args()

    if args.cmd == "compute":
        result = spcr_from_failures(_parse_failures_flag(args.failures))
        print(f"SPCR:        {result['SPCR']}")
        print(f"Rule:        {result['rule']}")
        print(f"Narrative:   {result['narrative']}")
        print(f"m:           {result['m']}")
        print(f"t_k:         {result['t_k']}")
        if result.get("beta") is not None:
            print(f"β̂:           {result['beta']:.4f}")
            print(f"θ̂:           {result['theta']:.4f}")
        if result.get("chi_squared") is not None:
            print(f"χ² ({result['df']} df): {result['chi_squared']:.4f}")
            print(f"p value:     {result['p_value']:.6f}")
        return 0

    if args.cmd == "validate":
        matches, discrepancies = validate_csv(args.path, args.group_key)
        print(f"Groups scored:   {len(matches) + len(discrepancies)}")
        print(f"Matches:         {len(matches)}")
        print(f"Discrepancies:   {len(discrepancies)}")
        if discrepancies:
            print("\nReport examples (max 2):")
            for ex in report_examples(discrepancies, max_n=2):
                print(f"  - {ex['narrative']}")
        if args.report and discrepancies:
            with open(args.report, "w", newline="", encoding="utf-8") as f:
                fieldnames = list(discrepancies[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(discrepancies)
            print(f"Report:          {args.report}")
        return 0 if not discrepancies else 1

    return 0


if __name__ == "__main__":
    sys.exit(_cli())
