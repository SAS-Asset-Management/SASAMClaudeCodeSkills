"""
Defect Scoring — DCR_raw to DCR_cc to DCR_adjust cascade.

Reference implementation of the the MDR standard calculation profile (Section 4.5).
Pure stdlib. No third party dependencies.

Equations encoded:
  - Equation 2 (Simple)  — Section 4.5.6.1, step 3, MDR p.21
  - Equation 4 (Complex) — Section 4.5.6.2, step 2, MDR p.22
  - Table 9   (RMC impact on DCR) — MDR p.20

Public API:
    score_defect(dcr_raw, cc, rmc, method) -> dict
    score_dataframe(rows, method) -> list[dict]
    validate_csv(path, method) -> tuple[matches, discrepancies]

CLI:
    python calculate.py compute  --dcr 3 --cc 4 --rmc 2 --method complex
    python calculate.py validate path/to/defects.csv --method complex
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable, Optional


# MDR Table 9 — DCR_adjust lookup keyed by (DCR_cc, RMC)
# DCR_cc rows 1 to 5, RMC columns 1 to 3
TABLE_9: dict[tuple[int, int], int] = {
    (1, 1): 0, (1, 2): 0, (1, 3): 1,
    (2, 1): 0, (2, 2): 1, (2, 3): 2,
    (3, 1): 0, (3, 2): 2, (3, 3): 3,
    (4, 1): 0, (4, 2): 2, (4, 3): 4,
    (5, 1): 0, (5, 2): 3, (5, 3): 5,
}


def dcr_cc(dcr_raw: int, cc: Optional[int], method: str) -> int:
    """
    Compute DCR_cc per Equation 2 (simple) or Equation 4 (complex).

    Components without a criticality rating (cc is None) follow the
    "no CC" rule: DCR_cc = DCR_raw + 1 under both methods.
    """
    if dcr_raw < 1 or dcr_raw > 4:
        raise ValueError(
            f"DCR_raw must be 1 to 4 per MDR Section 8 subclass tables (got {dcr_raw})"
        )
    if cc is not None and (cc < 1 or cc > 4):
        raise ValueError(
            f"Component Criticality must be 1 to 4 per MDR Table 7 (got {cc})"
        )
    if method not in ("simple", "complex"):
        raise ValueError(f"method must be 'simple' or 'complex' (got {method!r})")

    if cc is None:
        return dcr_raw + 1

    if method == "simple":
        # Equation 2: DCR_cc = 0 if CC < 3, else DCR_raw + 1
        return 0 if cc < 3 else dcr_raw + 1
    else:
        # Equation 4: DCR_cc = DCR_raw if CC < 3, else DCR_raw + 1
        return dcr_raw if cc < 3 else dcr_raw + 1


def dcr_adjust(dcr_cc_value: int, rmc: int) -> int:
    """
    Look up DCR_adjust from MDR Table 9.

    DCR_cc = 0 short circuits to DCR_adjust = 0 (the simple method can
    produce DCR_cc = 0 for CC < 3; Table 9 does not enumerate this row).
    """
    if rmc < 1 or rmc > 3:
        raise ValueError(f"RMC must be 1 to 3 per MDR Table 8 (got {rmc})")
    if dcr_cc_value == 0:
        return 0
    if dcr_cc_value < 1 or dcr_cc_value > 5:
        raise ValueError(
            f"DCR_cc must be 0 to 5 (got {dcr_cc_value})"
        )
    return TABLE_9[(dcr_cc_value, rmc)]


def score_defect(
    dcr_raw: int,
    cc: Optional[int],
    rmc: int,
    method: str,
) -> dict:
    """
    Run the full defect scoring cascade. Returns a dict with all
    intermediate values for traceability.
    """
    cc_val = dcr_cc(dcr_raw, cc, method)
    adj_val = dcr_adjust(cc_val, rmc)
    return {
        "DCR_raw": dcr_raw,
        "CC": cc,
        "RMC": rmc,
        "method": method,
        "DCR_cc": cc_val,
        "DCR_adjust": adj_val,
    }


def score_dataframe(rows: Iterable[dict], method: str) -> list[dict]:
    """
    Apply score_defect to an iterable of dicts. Each row must contain
    DCR_raw, CC (or component_criticality), RMC (or renewal_mode_criteria).
    Returns the input rows enriched with computed_DCR_cc and computed_DCR_adjust.
    """
    out: list[dict] = []
    for row in rows:
        dcr_raw = int(row.get("DCR_raw") or row.get("dcr_raw"))
        cc_raw = row.get("CC") or row.get("component_criticality")
        cc = int(cc_raw) if cc_raw not in (None, "", "None") else None
        rmc = int(row.get("RMC") or row.get("renewal_mode_criteria"))
        result = score_defect(dcr_raw, cc, rmc, method)
        enriched = dict(row)
        enriched["computed_DCR_cc"] = result["DCR_cc"]
        enriched["computed_DCR_adjust"] = result["DCR_adjust"]
        out.append(enriched)
    return out


def validate_csv(
    path: Path,
    method: str,
) -> tuple[list[dict], list[dict]]:
    """
    Validate a franchisee submission CSV. Returns (matches, discrepancies).
    A discrepancy is any row where declared DCR_cc or DCR_adjust does
    not equal the recomputed value.
    """
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    matches: list[dict] = []
    discrepancies: list[dict] = []
    for row in rows:
        dcr_raw = int(row["DCR_raw"])
        cc_raw = row.get("CC") or row.get("component_criticality") or ""
        cc = int(cc_raw) if cc_raw not in ("", "None") else None
        rmc = int(row.get("RMC") or row.get("renewal_mode_criteria"))
        computed = score_defect(dcr_raw, cc, rmc, method)

        declared_cc = row.get("DCR_cc")
        declared_adj = row.get("DCR_adjust")

        cc_match = declared_cc is None or declared_cc == "" or int(declared_cc) == computed["DCR_cc"]
        adj_match = declared_adj is None or declared_adj == "" or int(declared_adj) == computed["DCR_adjust"]

        record = {
            **row,
            "computed_DCR_cc": computed["DCR_cc"],
            "computed_DCR_adjust": computed["DCR_adjust"],
            "DCR_cc_match": cc_match,
            "DCR_adjust_match": adj_match,
        }
        if cc_match and adj_match:
            matches.append(record)
        else:
            discrepancies.append(record)

    return matches, discrepancies


def _explain_dcr_cc_error(row: dict, method: str) -> str:
    """One sentence explaining why declared DCR_cc differs from computed."""
    dcr_raw = int(row["DCR_raw"])
    cc_raw = row.get("CC") or row.get("component_criticality") or ""
    cc = int(cc_raw) if cc_raw not in ("", "None") else None
    declared = int(row["DCR_cc"])
    computed = row["computed_DCR_cc"]

    if cc is None:
        rule = f"no criticality assigned, DCR_cc = DCR_raw + 1 = {dcr_raw + 1}"
    elif method == "simple" and cc < 3:
        rule = f"CC = {cc} (< 3), Equation 2 sets DCR_cc = 0"
    elif method == "simple":
        rule = f"CC = {cc} (≥ 3), Equation 2 sets DCR_cc = DCR_raw + 1 = {dcr_raw + 1}"
    elif method == "complex" and cc < 3:
        rule = f"CC = {cc} (< 3), Equation 4 sets DCR_cc = DCR_raw = {dcr_raw}"
    else:
        rule = f"CC = {cc} (≥ 3), Equation 4 sets DCR_cc = DCR_raw + 1 = {dcr_raw + 1}"

    return (
        f"declared DCR_cc = {declared} disagrees with the MDR cascade "
        f"({rule}); computed DCR_cc = {computed}"
    )


def _explain_dcr_adjust_error(row: dict) -> str:
    """One sentence explaining why declared DCR_adjust differs from computed."""
    rmc = int(row.get("RMC") or row.get("renewal_mode_criteria"))
    declared = int(row["DCR_adjust"])
    computed = row["computed_DCR_adjust"]
    cc_value = row["computed_DCR_cc"]
    if cc_value == 0:
        rule = "DCR_cc = 0 short circuits DCR_adjust to 0"
    else:
        rule = f"MDR Table 9 lookup at (DCR_cc = {cc_value}, RMC = {rmc}) returns {computed}"
    return (
        f"declared DCR_adjust = {declared} disagrees with the MDR Table 9 lookup "
        f"({rule}); computed DCR_adjust = {computed}"
    )


def report_examples(
    discrepancies: list[dict],
    method: str,
    max_n: int = 2,
) -> list[dict]:
    """
    Return up to `max_n` representative discrepancies in report ready form.

    Selection: largest absolute DCR_adjust delta first (since DCR_adjust drives
    the asset ACR), with a tie breaker preferring distinct error kinds for
    diversity (one DCR_cc driven, one DCR_adjust only) where possible.
    """
    if not discrepancies:
        return []

    def annotate(d: dict) -> dict:
        cc_err = not d["DCR_cc_match"]
        adj_err = not d["DCR_adjust_match"]
        adj_delta = abs(int(d["DCR_adjust"]) - d["computed_DCR_adjust"]) if adj_err and d.get("DCR_adjust") not in (None, "") else 0
        cc_delta = abs(int(d["DCR_cc"]) - d["computed_DCR_cc"]) if cc_err and d.get("DCR_cc") not in (None, "") else 0
        return {
            **d,
            "_cc_err": cc_err,
            "_adj_err": adj_err,
            "_severity": adj_delta + cc_delta,
            "_kind": "DCR_cc_and_DCR_adjust" if cc_err and adj_err else ("DCR_cc" if cc_err else "DCR_adjust"),
        }

    annotated = sorted((annotate(d) for d in discrepancies), key=lambda x: -x["_severity"])

    picked: list[dict] = []
    seen_kinds: set[str] = set()
    # Pass 1: prefer diverse kinds
    for d in annotated:
        if len(picked) >= max_n:
            break
        if d["_kind"] not in seen_kinds:
            picked.append(d)
            seen_kinds.add(d["_kind"])
    # Pass 2: fill remaining slots from highest severity
    for d in annotated:
        if len(picked) >= max_n:
            break
        if d not in picked:
            picked.append(d)

    examples: list[dict] = []
    for d in picked[:max_n]:
        notes: list[str] = []
        if d["_cc_err"]:
            notes.append(_explain_dcr_cc_error(d, method))
        if d["_adj_err"]:
            notes.append(_explain_dcr_adjust_error(d))
        narrative = (
            f"Defect {d.get('defect_survey_id') or d.get('defect_id') or 'unknown'} "
            f"(asset {d.get('asset_id') or d.get('authority_asset_id') or 'unknown'}, "
            f"DCR_raw = {d['DCR_raw']}, CC = {d.get('CC') or 'none'}, "
            f"RMC = {d.get('RMC') or d.get('renewal_mode_criteria')}, method = {method}) — "
            + "; ".join(notes)
            + "."
        )
        examples.append({
            "id": d.get("defect_survey_id") or d.get("defect_id"),
            "kind": d["_kind"],
            "declared_DCR_cc": d.get("DCR_cc"),
            "computed_DCR_cc": d["computed_DCR_cc"],
            "declared_DCR_adjust": d.get("DCR_adjust"),
            "computed_DCR_adjust": d["computed_DCR_adjust"],
            "severity": d["_severity"],
            "mdr_citation": "MDR Section 4.5 (Equations 2/4, Table 9)",
            "narrative": narrative,
        })
    return examples


def _cli() -> int:
    parser = argparse.ArgumentParser(description="MDR defect scoring (DCR cascade)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_compute = sub.add_parser("compute", help="Compute DCR_cc and DCR_adjust for one defect")
    p_compute.add_argument("--dcr", type=int, required=True)
    p_compute.add_argument("--cc", type=str, default="None", help="1 to 4 or None")
    p_compute.add_argument("--rmc", type=int, required=True)
    p_compute.add_argument("--method", choices=["simple", "complex"], required=True)

    p_validate = sub.add_parser("validate", help="Validate a CSV of declared defect scores")
    p_validate.add_argument("path", type=Path)
    p_validate.add_argument("--method", choices=["simple", "complex"], required=True)
    p_validate.add_argument("--report", type=Path, default=None, help="Write discrepancy CSV here")

    args = parser.parse_args()

    if args.cmd == "compute":
        cc_val: Optional[int] = None if args.cc in ("None", "none", "") else int(args.cc)
        result = score_defect(args.dcr, cc_val, args.rmc, args.method)
        for k, v in result.items():
            print(f"{k}: {v}")
        return 0

    if args.cmd == "validate":
        matches, discrepancies = validate_csv(args.path, args.method)
        print(f"Method:        {args.method}")
        print(f"Rows scored:   {len(matches) + len(discrepancies)}")
        print(f"Matches:       {len(matches)}")
        print(f"Discrepancies: {len(discrepancies)}")
        if discrepancies:
            print("\nReport examples (max 2):")
            for ex in report_examples(discrepancies, args.method, max_n=2):
                print(f"  - {ex['narrative']}")
        if args.report and discrepancies:
            fieldnames = list(discrepancies[0].keys())
            with open(args.report, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(discrepancies)
            print(f"Report:        {args.report}")
        return 0 if not discrepancies else 1

    return 0


if __name__ == "__main__":
    sys.exit(_cli())
