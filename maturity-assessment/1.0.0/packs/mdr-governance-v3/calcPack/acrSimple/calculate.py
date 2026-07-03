"""
ACR — Simple Method.

Reference implementation of the MDR standard v3.0 Section 4.5.6.1 (Equations 1, 2, 3).
Consumes the defectScoring skill for per defect DCR_cc / DCR_adjust.

Public API:
    acr_simple(defects: list[dict]) -> dict
    acr_simple_from_csv(path) -> dict[asset_survey_id, dict]

CLI:
    python calculate.py compute  --defects "3,4,3;2,1,2"
    python calculate.py validate path/to/submission.csv [--report path]
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Optional

# Import sibling skill (defectScoring) under a unique module name to avoid
# colliding with this file (also named calculate.py).
import importlib.util as _ilu

_DEFECT_PATH = Path(__file__).resolve().parents[1] / "defectScoring" / "calculate.py"
_spec = _ilu.spec_from_file_location("defectScoringCalc", _DEFECT_PATH)
_defect_mod = _ilu.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_defect_mod)  # type: ignore[union-attr]
score_defect = _defect_mod.score_defect


def acr_simple(defects: Iterable[dict]) -> dict:
    """
    Compute ACR using the Simple Method (MDR Section 4.5.6.1).

    Each defect dict must contain DCR_raw, CC (int or None), RMC.

    Returns:
        {
          "ACR": int,                 # 1 to 5
          "n_defects": int,
          "n_renewal_drivers": int,   # count of defects whose DCR_adjust == max
          "trace": [ {DCR_raw, CC, RMC, DCR_cc, DCR_adjust}, ... ]
        }
    """
    trace = []
    max_adjust = 0
    n = 0
    for d in defects:
        n += 1
        cc_val = d.get("CC")
        if cc_val is not None and cc_val != "":
            cc = int(cc_val)
        else:
            cc = None
        result = score_defect(
            int(d["DCR_raw"]),
            cc,
            int(d["RMC"]),
            "simple",
        )
        trace.append(result)
        if result["DCR_adjust"] > max_adjust:
            max_adjust = result["DCR_adjust"]

    if n == 0:
        # Equation 1 — no defects on the asset
        return {"ACR": 1, "n_defects": 0, "n_renewal_drivers": 0, "trace": []}

    # Equation 3 — ACR is the worst DCR_adjust, with floor of 1
    acr = max_adjust if max_adjust > 0 else 1
    n_drivers = sum(1 for t in trace if t["DCR_adjust"] == max_adjust and max_adjust > 0)
    return {
        "ACR": acr,
        "n_defects": n,
        "n_renewal_drivers": n_drivers,
        "trace": trace,
    }


def acr_simple_from_csv(path: Path, asset_key: str = "asset_survey_id") -> dict[str, dict]:
    """
    Read a authority template shaped Table 10-4 defect CSV, group by asset key, return
    per asset ACR result.
    """
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row[asset_key]].append({
            "DCR_raw": int(row["DCR_raw"]),
            "CC": row.get("CC") or row.get("component_criticality"),
            "RMC": int(row.get("RMC") or row.get("renewal_mode_criteria")),
            **row,
        })

    return {asset_id: acr_simple(defects) for asset_id, defects in grouped.items()}


def validate_csv(
    path: Path,
    asset_key: str = "asset_survey_id",
    declared_acr_col: str = "ACR",
) -> tuple[list[dict], list[dict]]:
    """
    Validate declared per-asset ACR values against recomputed ACRs.
    """
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    grouped: dict[str, list[dict]] = defaultdict(list)
    declared: dict[str, Optional[int]] = {}
    for row in rows:
        grouped[row[asset_key]].append(row)
        d = row.get(declared_acr_col)
        if d not in (None, ""):
            declared[row[asset_key]] = int(d)

    matches, discrepancies = [], []
    for asset_id, defects in grouped.items():
        result = acr_simple(defects)
        record = {
            "asset_survey_id": asset_id,
            "n_defects": result["n_defects"],
            "computed_ACR": result["ACR"],
            "declared_ACR": declared.get(asset_id),
            "match": declared.get(asset_id) is None or declared.get(asset_id) == result["ACR"],
        }
        (matches if record["match"] else discrepancies).append(record)
    return matches, discrepancies


def report_examples(discrepancies: list[dict], max_n: int = 2) -> list[dict]:
    """
    Return up to `max_n` representative ACR discrepancies in report ready form.

    Selection: largest |declared_ACR - computed_ACR| first, since the asset
    level rating drives the renewal investment signal.
    """
    if not discrepancies:
        return []

    def severity(d: dict) -> int:
        if d.get("declared_ACR") is None or d.get("computed_ACR") is None:
            return 0
        return abs(int(d["declared_ACR"]) - int(d["computed_ACR"]))

    ranked = sorted(discrepancies, key=lambda d: -severity(d))
    picked = ranked[:max_n]

    examples: list[dict] = []
    for d in picked:
        delta = severity(d)
        direction = "overstated" if int(d["declared_ACR"]) > int(d["computed_ACR"]) else "understated"
        narrative = (
            f"Asset {d['asset_survey_id']} declared ACR = {d['declared_ACR']} "
            f"but the Simple Method (Equation 3, ACR = max DCR_adjust over "
            f"{d['n_defects']} defect(s) with floor of 1) yields {d['computed_ACR']} "
            f"— condition {direction} by {delta} point(s)."
        )
        examples.append({
            "id": d["asset_survey_id"],
            "declared_ACR": d["declared_ACR"],
            "computed_ACR": d["computed_ACR"],
            "n_defects": d["n_defects"],
            "delta": delta,
            "direction": direction,
            "mdr_citation": "MDR Section 4.5.6.1 (Equations 1, 2, 3)",
            "narrative": narrative,
        })
    return examples


def _parse_defects_flag(s: str) -> list[dict]:
    """Parse '3,4,3;2,1,2' → list of dicts."""
    out = []
    for triple in s.split(";"):
        if not triple.strip():
            continue
        parts = triple.split(",")
        if len(parts) != 3:
            raise ValueError(f"Defect spec must be 'DCR_raw,CC,RMC' (got {triple!r})")
        dcr, cc, rmc = parts
        out.append({
            "DCR_raw": int(dcr),
            "CC": None if cc.strip().lower() in ("", "none") else int(cc),
            "RMC": int(rmc),
        })
    return out


def _cli() -> int:
    parser = argparse.ArgumentParser(description="MDR ACR Simple Method")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_compute = sub.add_parser("compute", help="Compute ACR for an inline defect list")
    p_compute.add_argument(
        "--defects",
        type=str,
        default="",
        help="Defects as 'DCR_raw,CC,RMC' triples separated by ; — empty means no defects",
    )

    p_validate = sub.add_parser("validate", help="Validate declared ACR vs computed for a franchisee CSV")
    p_validate.add_argument("path", type=Path)
    p_validate.add_argument("--asset-key", default="asset_survey_id")
    p_validate.add_argument("--report", type=Path, default=None)

    args = parser.parse_args()

    if args.cmd == "compute":
        defects = _parse_defects_flag(args.defects)
        result = acr_simple(defects)
        print(f"ACR:               {result['ACR']}")
        print(f"Defects scored:    {result['n_defects']}")
        print(f"Renewal drivers:   {result['n_renewal_drivers']}")
        print("Trace:")
        for t in result["trace"]:
            print(
                f"  DCR_raw={t['DCR_raw']} CC={t['CC']} RMC={t['RMC']} "
                f"-> DCR_cc={t['DCR_cc']} DCR_adjust={t['DCR_adjust']}"
            )
        return 0

    if args.cmd == "validate":
        matches, discrepancies = validate_csv(args.path, args.asset_key)
        print(f"Assets scored:    {len(matches) + len(discrepancies)}")
        print(f"Matches:          {len(matches)}")
        print(f"Discrepancies:    {len(discrepancies)}")
        if discrepancies:
            print("\nReport examples (max 2):")
            for ex in report_examples(discrepancies, max_n=2):
                print(f"  - {ex['narrative']}")
        if args.report and discrepancies:
            with open(args.report, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=discrepancies[0].keys())
                writer.writeheader()
                writer.writerows(discrepancies)
            print(f"Report:           {args.report}")
        return 0 if not discrepancies else 1

    return 0


if __name__ == "__main__":
    sys.exit(_cli())
