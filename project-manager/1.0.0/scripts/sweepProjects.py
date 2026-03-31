#!/usr/bin/env python3
"""
marcov.GATE Portfolio Sweep Script

Scans ~/Documents/Repos/**/.project-status.json files,
validates them, and outputs aggregated portfolio data as JSON.

Usage:
    python sweepProjects.py                  # JSON output of all projects
    python sweepProjects.py --list           # Human-readable table
    python sweepProjects.py --stale          # Only projects not updated in 14+ days
    python sweepProjects.py --summary        # Summary statistics only
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


SEARCH_ROOTS = [
    Path.home() / "Documents" / "Repos",
]

SCHEMA_VERSION = "marcov-gate-v1"
STALE_THRESHOLD_DAYS = 14


def findProjectFiles():
    """Discover all .project-status.json files under search roots."""
    found = []
    for root in SEARCH_ROOTS:
        if not root.exists():
            continue
        for statusFile in root.rglob(".project-status.json"):
            found.append(statusFile)
    return found


def validateProject(data):
    """Basic validation against marcov-gate-v1 schema."""
    if data.get("schema") != SCHEMA_VERSION:
        return False, f"Invalid schema: {data.get('schema')}"

    required = ["project", "status", "gates"]
    for field in required:
        if field not in data:
            return False, f"Missing required field: {field}"

    project = data["project"]
    for field in ["id", "client", "name", "type", "tier"]:
        if field not in project:
            return False, f"Missing project.{field}"

    status = data["status"]
    for field in ["currentPhase", "phaseName", "rag", "lastUpdated"]:
        if field not in status:
            return False, f"Missing status.{field}"

    return True, "Valid"


def isStale(data):
    """Check if project has not been updated in STALE_THRESHOLD_DAYS."""
    lastUpdated = data.get("status", {}).get("lastUpdated")
    if not lastUpdated:
        return True
    try:
        updateDate = datetime.strptime(lastUpdated, "%Y-%m-%d")
        return (datetime.now() - updateDate).days >= STALE_THRESHOLD_DAYS
    except ValueError:
        return True


def loadProjects():
    """Load and validate all discovered projects."""
    projects = []
    errors = []

    for filePath in findProjectFiles():
        try:
            with open(filePath, "r") as f:
                data = json.load(f)

            valid, message = validateProject(data)
            if not valid:
                errors.append({"path": str(filePath), "error": message})
                continue

            data["_filePath"] = str(filePath)
            data["_repoPath"] = str(filePath.parent)
            data["_isStale"] = isStale(data)
            projects.append(data)

        except json.JSONDecodeError as e:
            errors.append({"path": str(filePath), "error": f"Invalid JSON: {e}"})
        except Exception as e:
            errors.append({"path": str(filePath), "error": str(e)})

    return projects, errors


def buildSummary(projects):
    """Generate portfolio summary statistics."""
    total = len(projects)
    byPhase = {}
    byRag = {"green": 0, "amber": 0, "red": 0}
    byType = {"advisory": 0, "software": 0, "hybrid": 0}
    byTier = {"micro": 0, "standard": 0, "major": 0}
    staleCount = 0
    totalValue = 0
    totalAllocation = 0

    for p in projects:
        phase = p["status"]["phaseName"]
        byPhase[phase] = byPhase.get(phase, 0) + 1

        rag = p["status"]["rag"]
        if rag in byRag:
            byRag[rag] += 1

        pType = p["project"]["type"]
        if pType in byType:
            byType[pType] += 1

        tier = p["project"]["tier"]
        if tier in byTier:
            byTier[tier] += 1

        if p["_isStale"]:
            staleCount += 1

        totalValue += p["project"].get("contractValue", 0)

        for member in p.get("team", []):
            totalAllocation += member.get("allocation", 0)

    return {
        "totalProjects": total,
        "byPhase": byPhase,
        "byRag": byRag,
        "byType": byType,
        "byTier": byTier,
        "staleCount": staleCount,
        "totalContractValue": totalValue,
        "totalTeamAllocation": totalAllocation,
    }


def formatDate(isoDate):
    """Convert ISO date to DD/MM/YYYY."""
    if not isoDate:
        return "N/A"
    try:
        dt = datetime.strptime(isoDate, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return isoDate


def printTable(projects):
    """Print a human-readable table of projects."""
    if not projects:
        print("No projects found.")
        return

    header = f"{'Client':<20} {'Project':<25} {'Phase':<14} {'RAG':<8} {'%':>4} {'Tier':<10} {'Updated':<12} {'Path'}"
    print(header)
    print("=" * len(header))

    for p in sorted(projects, key=lambda x: x["status"]["currentPhase"]):
        client = p["project"]["client"][:19]
        name = p["project"]["name"][:24]
        phase = p["status"]["phaseName"][:13]
        rag = p["status"]["rag"].upper()
        pct = p["status"].get("percentComplete", 0)
        tier = p["project"]["tier"].capitalize()
        updated = formatDate(p["status"]["lastUpdated"])
        path = p["_repoPath"].replace(str(Path.home()), "~")

        staleMarker = " *" if p["_isStale"] else ""

        print(f"{client:<20} {name:<25} {phase:<14} {rag:<8} {pct:>3}% {tier:<10} {updated:<12} {path}{staleMarker}")

    staleProjects = [p for p in projects if p["_isStale"]]
    if staleProjects:
        print(f"\n* {len(staleProjects)} project(s) not updated in {STALE_THRESHOLD_DAYS}+ days")


def printSummary(projects):
    """Print summary statistics."""
    summary = buildSummary(projects)
    print(f"Active Projects:    {summary['totalProjects']}")
    print(f"Total Value:        ${summary['totalContractValue']:,.0f} AUD")
    print(f"Team Allocation:    {summary['totalTeamAllocation']:.1f} FTE")
    print()
    print("By Phase:")
    for phase, count in sorted(summary["byPhase"].items()):
        print(f"  {phase:<14} {count}")
    print()
    print("By RAG:")
    for rag, count in summary["byRag"].items():
        if count > 0:
            print(f"  {rag.upper():<8} {count}")
    print()
    if summary["staleCount"] > 0:
        print(f"WARNING: {summary['staleCount']} project(s) stale (>{STALE_THRESHOLD_DAYS} days since update)")


def main():
    mode = "json"
    if "--list" in sys.argv:
        mode = "list"
    elif "--stale" in sys.argv:
        mode = "stale"
    elif "--summary" in sys.argv:
        mode = "summary"

    projects, errors = loadProjects()

    if mode == "list":
        printTable(projects)
    elif mode == "stale":
        staleProjects = [p for p in projects if p["_isStale"]]
        printTable(staleProjects)
    elif mode == "summary":
        printSummary(projects)
    else:
        output = {
            "generatedAt": datetime.now().isoformat(),
            "searchRoots": [str(r) for r in SEARCH_ROOTS],
            "summary": buildSummary(projects),
            "projects": projects,
            "errors": errors,
        }
        print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
