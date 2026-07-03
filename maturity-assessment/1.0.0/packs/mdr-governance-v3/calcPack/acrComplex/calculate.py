"""
ACR — Complex Method.

Reference implementation of the MDR standard v3.0 Section 4.5.6.2 (Equations 4, 5, 6).
Consumes the defectScoring skill for per defect DCR_cc / DCR_adjust under
the 'complex' DCR_cc rule (Equation 4).

Public API:
    aecr_for_element(defects: list[dict], inspected: bool) -> dict
    acr_complex(elements: list[dict]) -> dict
    percentile_80(values: list[int]) -> int

CLI:
    python calculate.py aecr     --defects "3,4,3;2,1,2"
    python calculate.py compute  --spec spec.json
    python calculate.py validate path/to/submission.csv [--report path]
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Optional

# Sibling skill import — load by file path to avoid the calculate.py name clash
import importlib.util as _ilu

_DEFECT_PATH = Path(__file__).resolve().parents[1] / "defectScoring" / "calculate.py"
_spec = _ilu.spec_from_file_location("defectScoringCalc", _DEFECT_PATH)
_defect_mod = _ilu.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_defect_mod)  # type: ignore[union-attr]
score_defect = _defect_mod.score_defect


# --- Per element AECR -----------------------------------------------------

def aecr_for_element(defects: Iterable[dict], inspected: bool = True) -> dict:
    """
    Compute AECR for one element using Equations 4 and 5 (Complex method).

    - Inaccessible elements (inspected=False) → AECR = -1.
    - Element with no defects or all DCR_adjust == 0 → AECR = 1 (floor).
    - Otherwise AECR = max(DCR_adjust).
    """
    if not inspected:
        return {"AECR": -1, "n_defects": 0, "trace": []}

    trace = []
    max_adj = 0
    n = 0
    for d in defects:
        n += 1
        cc_val = d.get("CC")
        if cc_val is not None and cc_val != "":
            cc = int(cc_val)
        else:
            cc = None
        result = score_defect(int(d["DCR_raw"]), cc, int(d["RMC"]), "complex")
        trace.append(result)
        if result["DCR_adjust"] > max_adj:
            max_adj = result["DCR_adjust"]

    # Equation 5 + floor rule
    aecr = max_adj if max_adj > 0 else 1
    return {"AECR": aecr, "n_defects": n, "trace": trace}


# --- Asset 80th percentile -----------------------------------------------

def percentile_80(values: list[int]) -> Optional[int]:
    """
    Inverse empirical CDF at 0.80 over the given AECR values.

    Returns the smallest value v such that the proportion of values <= v
    is >= 0.80. Returns None if the input is empty.
    """
    if not values:
        return None
    sorted_v = sorted(values)
    n = len(sorted_v)
    idx = math.ceil(0.80 * n) - 1
    idx = max(0, min(idx, n - 1))
    return sorted_v[idx]


def acr_complex(elements: list[dict]) -> dict:
    """
    Compute ACR using the Complex Method (MDR Section 4.5.6.2).

    Each element dict must contain:
      - 'inspected' (bool, default True)
      - 'defects' (list of {DCR_raw, CC, RMC})
      - optional 'element_id' for tracing

    Returns:
      {
        ACR, n_elements_total, n_elements_inspected, n_elements_excluded,
        aecr_distribution, percentile_80_aecr, elements: [{element_id, AECR, trace}, ...]
      }
    """
    enriched = []
    aecrs = []
    excluded = 0
    for el in elements:
        inspected = el.get("inspected", True)
        result = aecr_for_element(el.get("defects", []), inspected)
        record = {
            "element_id": el.get("element_id"),
            "AECR": result["AECR"],
            "n_defects": result["n_defects"],
            "trace": result["trace"],
        }
        enriched.append(record)
        if result["AECR"] == -1:
            excluded += 1
        else:
            aecrs.append(result["AECR"])

    p80 = percentile_80(aecrs)
    distribution = dict(Counter(aecrs))

    return {
        "ACR": p80 if p80 is not None else None,
        "n_elements_total": len(elements),
        "n_elements_inspected": len(aecrs),
        "n_elements_excluded": excluded,
        "aecr_distribution": distribution,
        "percentile_80_aecr": p80,
        "elements": enriched,
    }


# --- CSV ingest -----------------------------------------------------------

def acr_complex_from_csv(
    path: Path,
    asset_key: str = "asset_survey_id",
    element_key: str = "element_id",
) -> dict[str, dict]:
    """
    Read a joined defect CSV with columns including:
      asset_survey_id, element_id, element_inspected, DCR_raw, CC, RMC

    Rows where element_inspected == 'No' / False / 0 with no defects represent
    inaccessible elements. Rows where DCR_raw is empty represent elements
    with no defects (placeholder rows used to register the element).

    Returns per asset ACR result keyed by asset_survey_id.
    """
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Group rows: asset_id -> element_id -> [defect rows]
    asset_elements: dict[str, dict[str, dict]] = defaultdict(lambda: defaultdict(
        lambda: {"inspected": True, "defects": [], "element_id": None}
    ))
    for row in rows:
        a = row[asset_key]
        e = row[element_key]
        bucket = asset_elements[a][e]
        bucket["element_id"] = e

        inspected_flag = (row.get("element_inspected") or row.get("element_survey_completed") or "Yes").strip().lower()
        if inspected_flag in ("no", "false", "0"):
            bucket["inspected"] = False

        # If DCR_raw is present, it's a defect row
        if row.get("DCR_raw") not in (None, ""):
            bucket["defects"].append({
                "DCR_raw": int(row["DCR_raw"]),
                "CC": row.get("CC") or row.get("component_criticality"),
                "RMC": int(row.get("RMC") or row.get("renewal_mode_criteria")),
            })

    out: dict[str, dict] = {}
    for asset_id, els in asset_elements.items():
        elements_list = list(els.values())
        out[asset_id] = acr_complex(elements_list)
    return out


def validate_csv(
    path: Path,
    asset_key: str = "asset_survey_id",
    element_key: str = "element_id",
    declared_acr_col: str = "ACR",
    declared_aecr_col: str = "AECR",
) -> tuple[list[dict], list[dict]]:
    """
    Validate per asset declared ACR (and per element AECR if declared).
    Returns (matches, discrepancies) at the asset level.
    """
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    declared_acr: dict[str, int] = {}
    declared_aecr: dict[tuple[str, str], int] = {}
    for row in rows:
        a, e = row[asset_key], row[element_key]
        if row.get(declared_acr_col) not in (None, ""):
            declared_acr[a] = int(row[declared_acr_col])
        if row.get(declared_aecr_col) not in (None, ""):
            declared_aecr[(a, e)] = int(row[declared_aecr_col])

    computed = acr_complex_from_csv(path, asset_key, element_key)

    matches, discrepancies = [], []
    for asset_id, result in computed.items():
        # Element level AECR diffs
        aecr_mismatches = []
        for el in result["elements"]:
            key = (asset_id, el["element_id"])
            if key in declared_aecr and declared_aecr[key] != el["AECR"]:
                aecr_mismatches.append({
                    "element_id": el["element_id"],
                    "computed_AECR": el["AECR"],
                    "declared_AECR": declared_aecr[key],
                })
        record = {
            "asset_survey_id": asset_id,
            "n_elements_inspected": result["n_elements_inspected"],
            "n_elements_excluded": result["n_elements_excluded"],
            "computed_ACR": result["ACR"],
            "declared_ACR": declared_acr.get(asset_id),
            "aecr_mismatches": aecr_mismatches,
            "match": (
                (declared_acr.get(asset_id) is None or declared_acr.get(asset_id) == result["ACR"])
                and not aecr_mismatches
            ),
        }
        (matches if record["match"] else discrepancies).append(record)
    return matches, discrepancies


# --- CLI ------------------------------------------------------------------

def report_examples(discrepancies: list[dict], max_n: int = 2) -> list[dict]:
    """
    Return up to `max_n` representative discrepancies in report ready form.

    Selection priority:
      1. Largest |declared_ACR - computed_ACR| (asset level errors first).
      2. If asset ACRs all match but element AECRs don't, pick the largest
         element level AECR delta.

    Where possible we surface one asset level and one element level example
    for diversity.
    """
    if not discrepancies:
        return []

    def asset_severity(d: dict) -> int:
        if d.get("declared_ACR") is None or d.get("computed_ACR") is None:
            return 0
        return abs(int(d["declared_ACR"]) - int(d["computed_ACR"]))

    def element_severity(d: dict) -> int:
        if not d.get("aecr_mismatches"):
            return 0
        return max(abs(m["declared_AECR"] - m["computed_AECR"]) for m in d["aecr_mismatches"])

    examples: list[dict] = []

    # Pass 1 — best asset level discrepancy
    asset_ranked = sorted(
        (d for d in discrepancies if asset_severity(d) > 0),
        key=lambda d: -asset_severity(d),
    )
    if asset_ranked and len(examples) < max_n:
        d = asset_ranked[0]
        delta = asset_severity(d)
        direction = "overstated" if int(d["declared_ACR"]) > int(d["computed_ACR"]) else "understated"
        narrative = (
            f"Asset {d['asset_survey_id']} declared ACR = {d['declared_ACR']} "
            f"but the Complex Method (80%ile of {d['n_elements_inspected']} inspected "
            f"AECR values per Equation 6) yields {d['computed_ACR']} "
            f"— condition {direction} by {delta} point(s)."
        )
        examples.append({
            "id": d["asset_survey_id"],
            "level": "asset",
            "declared_ACR": d["declared_ACR"],
            "computed_ACR": d["computed_ACR"],
            "delta": delta,
            "direction": direction,
            "n_elements_inspected": d["n_elements_inspected"],
            "n_elements_excluded": d["n_elements_excluded"],
            "mdr_citation": "MDR Section 4.5.6.2 (Equations 4, 5, 6)",
            "narrative": narrative,
        })

    # Pass 2 — best element level AECR discrepancy (preferring distinct asset)
    element_pool = []
    for d in discrepancies:
        for m in d.get("aecr_mismatches", []):
            element_pool.append((d, m, abs(m["declared_AECR"] - m["computed_AECR"])))
    element_pool.sort(key=lambda t: -t[2])

    used_assets = {ex["id"] for ex in examples}
    for d, m, delta in element_pool:
        if len(examples) >= max_n:
            break
        if d["asset_survey_id"] in used_assets:
            continue
        direction = "overstated" if m["declared_AECR"] > m["computed_AECR"] else "understated"
        narrative = (
            f"Element {m['element_id']} of asset {d['asset_survey_id']} declared "
            f"AECR = {m['declared_AECR']} but the cascade gives "
            f"{m['computed_AECR']} (Equation 5: AECR = max DCR_adjust, with floor "
            f"of 1 for clean elements and -1 for inaccessible) — element condition "
            f"{direction} by {delta} point(s)."
        )
        examples.append({
            "id": f"{d['asset_survey_id']} / {m['element_id']}",
            "level": "element",
            "declared_AECR": m["declared_AECR"],
            "computed_AECR": m["computed_AECR"],
            "delta": delta,
            "direction": direction,
            "mdr_citation": "MDR Section 4.5.6.2 (Equation 5)",
            "narrative": narrative,
        })
        used_assets.add(d["asset_survey_id"])

    # Pass 3 — fill remaining slots from any element level mismatch
    for d, m, delta in element_pool:
        if len(examples) >= max_n:
            break
        # Skip if we already used this exact element
        if any(ex["id"].endswith(f"/ {m['element_id']}") for ex in examples):
            continue
        direction = "overstated" if m["declared_AECR"] > m["computed_AECR"] else "understated"
        narrative = (
            f"Element {m['element_id']} of asset {d['asset_survey_id']} declared "
            f"AECR = {m['declared_AECR']} but the cascade gives "
            f"{m['computed_AECR']} — {direction} by {delta} point(s)."
        )
        examples.append({
            "id": f"{d['asset_survey_id']} / {m['element_id']}",
            "level": "element",
            "declared_AECR": m["declared_AECR"],
            "computed_AECR": m["computed_AECR"],
            "delta": delta,
            "direction": direction,
            "mdr_citation": "MDR Section 4.5.6.2 (Equation 5)",
            "narrative": narrative,
        })

    return examples[:max_n]


def _parse_defects_flag(s: str) -> list[dict]:
    out = []
    for triple in s.split(";"):
        if not triple.strip():
            continue
        dcr, cc, rmc = triple.split(",")
        out.append({
            "DCR_raw": int(dcr),
            "CC": None if cc.strip().lower() in ("", "none") else int(cc),
            "RMC": int(rmc),
        })
    return out


def _cli() -> int:
    parser = argparse.ArgumentParser(description="MDR ACR Complex Method")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_aecr = sub.add_parser("aecr", help="Compute AECR for a single element")
    p_aecr.add_argument("--defects", type=str, default="")
    p_aecr.add_argument("--inspected", type=str, default="yes", choices=["yes", "no"])

    p_compute = sub.add_parser("compute", help="Compute ACR for an asset (JSON spec)")
    p_compute.add_argument("--spec", type=Path, required=True)

    p_validate = sub.add_parser("validate", help="Validate declared ACR vs computed for a CSV")
    p_validate.add_argument("path", type=Path)
    p_validate.add_argument("--report", type=Path, default=None)

    args = parser.parse_args()

    if args.cmd == "aecr":
        result = aecr_for_element(_parse_defects_flag(args.defects), args.inspected == "yes")
        print(f"AECR:           {result['AECR']}")
        print(f"Defects scored: {result['n_defects']}")
        for t in result["trace"]:
            print(
                f"  DCR_raw={t['DCR_raw']} CC={t['CC']} RMC={t['RMC']} "
                f"-> DCR_cc={t['DCR_cc']} DCR_adjust={t['DCR_adjust']}"
            )
        return 0

    if args.cmd == "compute":
        spec = json.loads(args.spec.read_text())
        result = acr_complex(spec["elements"])
        print(f"ACR:                  {result['ACR']}")
        print(f"Elements (total):     {result['n_elements_total']}")
        print(f"Elements (inspected): {result['n_elements_inspected']}")
        print(f"Elements (excluded):  {result['n_elements_excluded']}")
        print(f"AECR distribution:    {result['aecr_distribution']}")
        return 0

    if args.cmd == "validate":
        matches, discrepancies = validate_csv(args.path)
        print(f"Assets scored:    {len(matches) + len(discrepancies)}")
        print(f"Matches:          {len(matches)}")
        print(f"Discrepancies:    {len(discrepancies)}")
        for d in discrepancies:
            print(
                f"  {d['asset_survey_id']}: "
                f"declared ACR={d['declared_ACR']} computed ACR={d['computed_ACR']} "
                f"AECR mismatches={len(d['aecr_mismatches'])}"
            )
        if discrepancies:
            print("\nReport examples (max 2):")
            for ex in report_examples(discrepancies, max_n=2):
                print(f"  - {ex['narrative']}")
        if args.report and discrepancies:
            with open(args.report, "w", newline="", encoding="utf-8") as f:
                fieldnames = [k for k in discrepancies[0].keys() if k != "aecr_mismatches"]
                fieldnames.append("aecr_mismatches_json")
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for d in discrepancies:
                    out_row = {k: d[k] for k in fieldnames if k in d}
                    out_row["aecr_mismatches_json"] = json.dumps(d["aecr_mismatches"])
                    writer.writerow(out_row)
            print(f"Report:           {args.report}")
        return 0 if not discrepancies else 1

    return 0


if __name__ == "__main__":
    sys.exit(_cli())
