"""Fan out orchestrator with resume semantics for the maturity assessment suite.

The orchestrator never invokes agents itself. It reads the pack taxonomy and
the score ledger, then tells the caller (the consultant or a skill) what is
still pending so the fan out can resume rather than restart. It also runs the
reconciliation gate that must pass before the report gate opens.

CLI:
    python3 orchestrate.py --repo <engagementRoot> status
    python3 orchestrate.py --repo <engagementRoot> plan
    python3 orchestrate.py --repo <engagementRoot> check

status  prints a human table: subjects scored versus taxonomy total, reviews
        on disk versus artefacts in evidence/, interview notes count,
        findings count in the latest run, open disputes.
plan    prints JSON with three lists: pendingScore (subjects with no evidence
        or a null final), pendingFindings (subjects with evidence but no
        findings file in the latest findings/runNN/), pendingSections
        (reportSpec section files with no matching draft in the engagement at
        deliverable/sections/).
check   the reconciliation gate: every taxonomy subject has a non null
        final.score; every findings file's subject has non null sayScore AND
        doScore; no dispute has status "open"; when the pack declares
        complianceMatrix, compliance/matrix.csv row count equals
        compliance/requirements.csv row count and every conformance value is
        in the five value enum. Exits 1 with a reasoned list on any failure,
        0 when clean.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import re
import sys

_ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFORMANCE_ENUM = {"Complete", "Partial", "Not at all", "TBC", "Out of scope"}
_FINDING_PATTERN = re.compile(r"^(\d{2}_[A-Za-z0-9]+)_finding\.md$")
_RUN_DIR_PATTERN = re.compile(r"^run(\d{2,})$")


def _loadConfigLoader():
    spec = importlib.util.spec_from_file_location(
        "maturityConfigLoader", os.path.join(_ENGINE_DIR, "configLoader.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _loadContext(repoRoot, pluginRoot):
    loader = _loadConfigLoader()
    if pluginRoot is None:
        pluginRoot = os.path.dirname(_ENGINE_DIR)
    engagement = loader.loadEngagement(repoRoot)
    packDir, pack = loader.resolvePack(repoRoot, pluginRoot)
    ledgerPath = os.path.join(repoRoot, "scoreLedger.json")
    if os.path.isfile(ledgerPath):
        with open(ledgerPath, "r", encoding="utf-8") as handle:
            ledger = json.load(handle)
    else:
        ledger = {"runs": [], "subjects": {}}
    return engagement, packDir, pack, ledger


def _taxonomySubjects(pack):
    subjects = []
    for domain in (pack.get("taxonomy") or {}).get("domains") or []:
        subjects.extend(domain.get("subjects") or [])
    return subjects


def _listFiles(directory, suffix=None):
    if not os.path.isdir(directory):
        return []
    names = []
    for name in sorted(os.listdir(directory)):
        if name.startswith("."):
            continue
        if os.path.isfile(os.path.join(directory, name)) and (suffix is None or name.endswith(suffix)):
            names.append(name)
    return names


def _latestFindingsRun(repoRoot):
    findingsRoot = os.path.join(repoRoot, "findings")
    if not os.path.isdir(findingsRoot):
        return None, []
    runs = []
    for name in os.listdir(findingsRoot):
        match = _RUN_DIR_PATTERN.match(name)
        if match and os.path.isdir(os.path.join(findingsRoot, name)):
            runs.append((int(match.group(1)), name))
    if not runs:
        return None, []
    _, latest = max(runs)
    return latest, _listFiles(os.path.join(findingsRoot, latest), suffix="_finding.md")


def _findingSubjects(findingFiles):
    subjects = []
    for name in findingFiles:
        match = _FINDING_PATTERN.match(name)
        if match:
            subjects.append(match.group(1))
    return subjects


def _openDisputes(ledger):
    openList = []
    for subjectId, subject in (ledger.get("subjects") or {}).items():
        for dispute in subject.get("disputes") or []:
            if dispute.get("status") == "open":
                openList.append((subjectId, dispute.get("id")))
    return openList


def cmdStatus(repoRoot, pluginRoot=None):
    """Build the human status table. Returns the table as a string."""
    _, _, pack, ledger = _loadContext(repoRoot, pluginRoot)
    subjects = _taxonomySubjects(pack)
    scored = sum(
        1
        for subjectId in subjects
        if ((ledger.get("subjects") or {}).get(subjectId) or {}).get("final", {}).get("score") is not None
    )
    reviews = len(_listFiles(os.path.join(repoRoot, "reviews"), suffix="_review.md"))
    artefacts = [
        name for name in _listFiles(os.path.join(repoRoot, "evidence")) if name != "ARTEFACT_SCHEDULE.md"
    ]
    interviewNotes = len(
        [n for n in _listFiles(os.path.join(repoRoot, "interviews"), suffix="_notes.md")]
    )
    latestRun, findingFiles = _latestFindingsRun(repoRoot)
    disputes = _openDisputes(ledger)

    rows = [
        ("Subjects scored", f"{scored} of {len(subjects)}"),
        ("Reviews on disk vs artefacts", f"{reviews} of {len(artefacts)}"),
        ("Interview notes", str(interviewNotes)),
        ("Findings (latest run)", f"{len(findingFiles)}" + (f" in {latestRun}" if latestRun else " (no runs yet)")),
        ("Open disputes", str(len(disputes))),
    ]
    width = max(len(label) for label, _ in rows)
    lines = ["Engagement status", "=" * 40]
    for label, value in rows:
        lines.append(f"{label.ljust(width)}  {value}")
    return "\n".join(lines)


def cmdPlan(repoRoot, pluginRoot=None):
    """Return the resume plan dict: pendingScore, pendingFindings, pendingSections."""
    _, packDir, pack, ledger = _loadContext(repoRoot, pluginRoot)
    subjects = _taxonomySubjects(pack)
    ledgerSubjects = ledger.get("subjects") or {}

    pendingScore = []
    pendingFindings = []
    _, findingFiles = _latestFindingsRun(repoRoot)
    foundSubjects = set(_findingSubjects(findingFiles))
    for subjectId in subjects:
        entry = ledgerSubjects.get(subjectId) or {}
        hasEvidence = bool(entry.get("evidence"))
        finalScore = (entry.get("final") or {}).get("score")
        if not hasEvidence or finalScore is None:
            pendingScore.append(subjectId)
        if hasEvidence and subjectId not in foundSubjects:
            pendingFindings.append(subjectId)

    pendingSections = []
    sectionsDir = os.path.join(packDir, "reportSpec", "sections")
    draftsDir = os.path.join(repoRoot, "deliverable", "sections")
    for sectionFile in _listFiles(sectionsDir, suffix=".md"):
        if not os.path.isfile(os.path.join(draftsDir, sectionFile)):
            pendingSections.append(sectionFile)

    return {
        "pendingScore": pendingScore,
        "pendingFindings": pendingFindings,
        "pendingSections": pendingSections,
    }


def _csvRows(path):
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def cmdCheck(repoRoot, pluginRoot=None):
    """Run the reconciliation gate. Returns (ok, reasons)."""
    _, _, pack, ledger = _loadContext(repoRoot, pluginRoot)
    reasons = []
    ledgerSubjects = ledger.get("subjects") or {}

    for subjectId in _taxonomySubjects(pack):
        entry = ledgerSubjects.get(subjectId)
        if entry is None or (entry.get("final") or {}).get("score") is None:
            reasons.append(f"subject {subjectId} has no final score in the ledger")

    _, findingFiles = _latestFindingsRun(repoRoot)
    for subjectId in _findingSubjects(findingFiles):
        entry = ledgerSubjects.get(subjectId) or {}
        if entry.get("sayScore") is None or entry.get("doScore") is None:
            reasons.append(
                f"subject {subjectId} has a findings file but sayScore or doScore is null"
            )

    for subjectId, disputeId in _openDisputes(ledger):
        reasons.append(f"subject {subjectId} has an open dispute ({disputeId})")

    if pack.get("complianceMatrix"):
        requirementsPath = os.path.join(repoRoot, "compliance", "requirements.csv")
        matrixPath = os.path.join(repoRoot, "compliance", "matrix.csv")
        if not os.path.isfile(requirementsPath) or not os.path.isfile(matrixPath):
            reasons.append(
                "pack declares complianceMatrix but compliance/requirements.csv or compliance/matrix.csv is missing"
            )
        else:
            requirements = _csvRows(requirementsPath)
            matrix = _csvRows(matrixPath)
            if len(matrix) != len(requirements):
                reasons.append(
                    f"compliance/matrix.csv has {len(matrix)} rows but compliance/requirements.csv has {len(requirements)}"
                )
            for index, row in enumerate(matrix, 1):
                value = (row.get("conformance") or "").strip()
                if value not in CONFORMANCE_ENUM:
                    reasons.append(
                        f"compliance/matrix.csv row {index} has conformance {value!r}, expected one of "
                        + ", ".join(sorted(CONFORMANCE_ENUM))
                    )

    return (len(reasons) == 0), reasons


def main(argv=None):
    parser = argparse.ArgumentParser(description="Fan out orchestration with resume semantics.")
    parser.add_argument("--repo", required=True, help="engagement repo root")
    parser.add_argument("command", choices=["status", "plan", "check"])
    args = parser.parse_args(argv)

    if args.command == "status":
        print(cmdStatus(args.repo))
        return 0
    if args.command == "plan":
        print(json.dumps(cmdPlan(args.repo), indent=2))
        return 0
    ok, reasons = cmdCheck(args.repo)
    if ok:
        print("Reconciliation checks passed.")
        return 0
    print("Reconciliation checks FAILED:")
    for reason in reasons:
        print(f"  * {reason}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
