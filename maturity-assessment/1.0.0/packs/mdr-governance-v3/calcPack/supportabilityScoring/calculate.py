"""
Supportability Scoring — TTI_SUP and SCR (MDR Section 4.6).

Reference implementation of:
  - Equation 7  — TTI_SUP = TSE_time + S_years
  - Figure 7    — SCR banding (1: TTI > 20; 2: 14 < TTI <= 20; 3: 8 < TTI <= 14;
                                4: 3 < TTI <= 8; 5: TTI <= 3)

Public API:
    tti_sup(tse_time, s_years) -> float
    scr_band(tti_sup) -> int
    scr_for_system(components) -> dict
    scr_from_csv(path) -> dict[group, dict]
    validate_csv(path) -> tuple[matches, discrepancies]
    report_examples(discrepancies, max_n=2) -> list[dict]

CLI:
    python calculate.py compute  --components "LED,12,5;LCD,4.5,1.5"
    python calculate.py validate path/to/submission.csv [--report path]
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Optional


# Figure 7 banding — break points and SCRs (right inclusive: 20 → 2, 14 → 3, 8 → 4, 3 → 5)
FIGURE_7_BANDS = [
    (20.0, 1),  # TTI > 20 → SCR 1
    (14.0, 2),  # 14 < TTI <= 20 → SCR 2
    (8.0, 3),   # 8 < TTI <= 14 → SCR 3
    (3.0, 4),   # 3 < TTI <= 8 → SCR 4
    # else → SCR 5 (TTI <= 3)
]


def tti_sup(tse_time: float, s_years: float) -> float:
    """Equation 7 — TTI_SUP = TSE_time + S_years."""
    if tse_time < 0 or s_years < 0:
        raise ValueError(
            f"TSE_time and S_years must be non negative (got {tse_time}, {s_years})"
        )
    return float(tse_time) + float(s_years)


def scr_band(value: float) -> int:
    """Figure 7 — map TTI_SUP onto SCR 1 to 5 (right inclusive thresholds)."""
    if value > 20.0:
        return 1
    if value > 14.0:
        return 2
    if value > 8.0:
        return 3
    if value > 3.0:
        return 4
    return 5


def scr_for_system(components: Iterable[dict]) -> dict:
    """
    Compute SCR for a system grouping per MDR Section 4.6.

    Each component must contain:
      - component_id (string, optional)
      - TSE_time (float, years) or None to exclude
      - S_years  (float, years) or None to exclude

    Returns:
        SCR, system_TTI_SUP, binding_component, n_components, n_components_excluded,
        components (per component trace).
    """
    trace: list[dict] = []
    excluded = 0
    for c in components:
        tse = c.get("TSE_time")
        sy = c.get("S_years")
        if tse is None or sy is None or tse == "" or sy == "":
            excluded += 1
            trace.append({
                "component_id": c.get("component_id"),
                "TSE_time": tse,
                "S_years": sy,
                "TTI_SUP": None,
                "excluded": True,
            })
            continue
        tti = tti_sup(float(tse), float(sy))
        trace.append({
            "component_id": c.get("component_id"),
            "TSE_time": float(tse),
            "S_years": float(sy),
            "TTI_SUP": tti,
            "excluded": False,
        })

    valid = [t for t in trace if not t["excluded"]]
    if not valid:
        return {
            "SCR": None,
            "system_TTI_SUP": None,
            "binding_component": None,
            "n_components": len(trace),
            "n_components_excluded": excluded,
            "components": trace,
        }

    binding = min(valid, key=lambda t: t["TTI_SUP"])
    return {
        "SCR": scr_band(binding["TTI_SUP"]),
        "system_TTI_SUP": binding["TTI_SUP"],
        "binding_component": binding["component_id"],
        "n_components": len(trace),
        "n_components_excluded": excluded,
        "components": trace,
    }


# ---- CSV ingest / validate ----------------------------------------------

def scr_from_csv(
    path: Path,
    group_key: str = "system_id",
) -> dict[str, dict]:
    """
    Read a CSV grouped by system / system grouping. Each row represents one
    component with columns: component_id, TSE_time, S_years.
    Returns per group SCR result.
    """
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row[group_key]].append({
            "component_id": row.get("component_id"),
            "TSE_time": row.get("TSE_time"),
            "S_years": row.get("S_years"),
        })

    return {gid: scr_for_system(comps) for gid, comps in grouped.items()}


def validate_csv(
    path: Path,
    group_key: str = "system_id",
    declared_scr_col: str = "SCR",
) -> tuple[list[dict], list[dict]]:
    """
    Validate declared SCR against recomputed SCR for each system grouping.
    Returns (matches, discrepancies).
    """
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    declared: dict[str, Optional[int]] = {}
    for row in rows:
        d = row.get(declared_scr_col)
        if d not in (None, ""):
            declared[row[group_key]] = int(d)

    computed = scr_from_csv(path, group_key)

    matches, discrepancies = [], []
    for group_id, result in computed.items():
        record = {
            "system_id": group_id,
            "n_components": result["n_components"],
            "n_components_excluded": result["n_components_excluded"],
            "system_TTI_SUP": result["system_TTI_SUP"],
            "binding_component": result["binding_component"],
            "computed_SCR": result["SCR"],
            "declared_SCR": declared.get(group_id),
            "match": (
                declared.get(group_id) is None
                or declared.get(group_id) == result["SCR"]
            ),
        }
        if record["match"]:
            matches.append(record)
        else:
            # Include the binding component's TSE/S_years for narrative
            binding = next(
                (c for c in result["components"] if c["component_id"] == result["binding_component"]),
                None,
            )
            if binding:
                record["binding_TSE_time"] = binding["TSE_time"]
                record["binding_S_years"] = binding["S_years"]
            discrepancies.append(record)
    return matches, discrepancies


def report_examples(discrepancies: list[dict], max_n: int = 2) -> list[dict]:
    """
    Return up to `max_n` representative SCR discrepancies in report ready form.
    Ranked by |declared_SCR - computed_SCR|.
    """
    if not discrepancies:
        return []

    def severity(d: dict) -> int:
        if d.get("declared_SCR") is None or d.get("computed_SCR") is None:
            return 0
        return abs(int(d["declared_SCR"]) - int(d["computed_SCR"]))

    ranked = sorted(discrepancies, key=lambda d: -severity(d))[:max_n]

    examples: list[dict] = []
    for d in ranked:
        delta = severity(d)
        direction = "overstated" if int(d["declared_SCR"]) > int(d["computed_SCR"]) else "understated"
        binding_detail = ""
        if d.get("binding_component") is not None:
            binding_detail = (
                f" — bound by component {d['binding_component']} "
                f"(TSE_time = {d.get('binding_TSE_time')}, "
                f"S_years = {d.get('binding_S_years')})"
            )
        narrative = (
            f"System {d['system_id']} declared SCR = {d['declared_SCR']} but the "
            f"Supportability cascade (min component TTI_SUP across "
            f"{d['n_components']} components = {d['system_TTI_SUP']} years, banded "
            f"per Figure 7) yields SCR = {d['computed_SCR']}{binding_detail}. "
            f"Condition {direction} by {delta} point(s)."
        )
        examples.append({
            "id": d["system_id"],
            "declared_SCR": d["declared_SCR"],
            "computed_SCR": d["computed_SCR"],
            "system_TTI_SUP": d["system_TTI_SUP"],
            "binding_component": d.get("binding_component"),
            "delta": delta,
            "direction": direction,
            "mdr_citation": "MDR Section 4.6 (Equation 7, Figure 7)",
            "narrative": narrative,
        })
    return examples


# ---- CLI ----------------------------------------------------------------

def _parse_components_flag(s: str) -> list[dict]:
    """Parse 'LED,12,5;LCD,4.5,1.5' → list of component dicts."""
    out = []
    for triple in s.split(";"):
        if not triple.strip():
            continue
        parts = triple.split(",")
        if len(parts) != 3:
            raise ValueError(f"Component spec must be 'id,TSE,S' (got {triple!r})")
        cid, tse, sy = parts
        out.append({
            "component_id": cid.strip(),
            "TSE_time": float(tse),
            "S_years": float(sy),
        })
    return out


def _cli() -> int:
    parser = argparse.ArgumentParser(description="MDR Supportability Scoring")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_compute = sub.add_parser("compute", help="Compute SCR for an inline system")
    p_compute.add_argument(
        "--components",
        type=str,
        required=True,
        help="Components as 'id,TSE_years,S_years' triples separated by ;",
    )

    p_validate = sub.add_parser("validate", help="Validate a franchisee supportability CSV")
    p_validate.add_argument("path", type=Path)
    p_validate.add_argument("--group-key", default="system_id")
    p_validate.add_argument("--report", type=Path, default=None)

    args = parser.parse_args()

    if args.cmd == "compute":
        components = _parse_components_flag(args.components)
        result = scr_for_system(components)
        print(f"SCR:                {result['SCR']}")
        print(f"System TTI_SUP:     {result['system_TTI_SUP']}")
        print(f"Binding component: {result['binding_component']}")
        print(f"Components:         {result['n_components']} ({result['n_components_excluded']} excluded)")
        for c in result["components"]:
            if c["excluded"]:
                print(f"  {c['component_id']}: excluded")
            else:
                print(
                    f"  {c['component_id']}: TSE = {c['TSE_time']}, "
                    f"S_years = {c['S_years']}, TTI_SUP = {c['TTI_SUP']}"
                )
        return 0

    if args.cmd == "validate":
        matches, discrepancies = validate_csv(args.path, args.group_key)
        print(f"Systems scored:   {len(matches) + len(discrepancies)}")
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
