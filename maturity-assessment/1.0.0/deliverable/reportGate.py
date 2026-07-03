"""Report gate for the maturity assessment deliverable.

The gate decides whether the deliverable renders clean or with a DRAFT
badge. It is driven entirely by ledger state — no manual checklist.

Gate opens only when all three conditions hold:
  1. Every subject in the pack taxonomy exists in the ledger with a
     non null final.score.
  2. Every subject with either sayScore or doScore set has BOTH set
     (findings must be dual sourced).
  3. No dispute anywhere in the ledger has status "open".

Public API:
  evaluateGate(ledger: dict, pack: dict) -> {"open": bool, "reasons": [str]}

CLI:
  python3 reportGate.py --repo <engagementRoot>
"""

import argparse
import importlib.util
import json
import os
import sys


def evaluateGate(ledger, pack):
    """Evaluate the report gate against a score ledger and a pack.

    Returns {"open": bool, "reasons": [str]} where reasons precisely
    lists every failure (subject id plus what is missing). An open gate
    has an empty reasons list.
    """
    reasons = []
    subjects = ledger.get("subjects", {}) or {}

    taxonomySubjects = []
    for domain in (pack.get("taxonomy", {}) or {}).get("domains", []) or []:
        taxonomySubjects.extend(domain.get("subjects", []) or [])

    for subjectId in taxonomySubjects:
        record = subjects.get(subjectId)
        if record is None:
            reasons.append(
                "{}: missing from the ledger".format(subjectId)
            )
            continue
        final = record.get("final") or {}
        if final.get("score") is None:
            reasons.append(
                "{}: final.score is null".format(subjectId)
            )

    for subjectId, record in subjects.items():
        sayScore = record.get("sayScore")
        doScore = record.get("doScore")
        if sayScore is not None and doScore is None:
            reasons.append(
                "{}: sayScore is set but doScore is null".format(subjectId)
            )
        if doScore is not None and sayScore is None:
            reasons.append(
                "{}: doScore is set but sayScore is null".format(subjectId)
            )
        for dispute in record.get("disputes", []) or []:
            if dispute.get("status") == "open":
                reasons.append(
                    "{}: dispute {} is open".format(
                        subjectId, dispute.get("id", "(no id)")
                    )
                )

    return {"open": not reasons, "reasons": reasons}


def _loadConfigLoader():
    """Load engine/configLoader.py via importlib.

    Resolves ${CLAUDE_PLUGIN_ROOT}/engine/configLoader.py, falling back
    to this file's parent parent (the plugin root) when the environment
    variable is absent.
    """
    pluginRoot = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not pluginRoot:
        pluginRoot = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    loaderPath = os.path.join(pluginRoot, "engine", "configLoader.py")
    if not os.path.isfile(loaderPath):
        raise FileNotFoundError(
            "engine configLoader not found at {}".format(loaderPath)
        )
    spec = importlib.util.spec_from_file_location("configLoader", loaderPath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Evaluate the report gate for an engagement repo."
    )
    parser.add_argument("--repo", required=True, help="Engagement repo root")
    args = parser.parse_args(argv)

    repoRoot = os.path.abspath(args.repo)
    ledgerPath = os.path.join(repoRoot, "scoreLedger.json")
    if not os.path.isfile(ledgerPath):
        print("Gate CLOSED: scoreLedger.json not found at {}".format(ledgerPath))
        return 1
    with open(ledgerPath, "r", encoding="utf-8") as handle:
        ledger = json.load(handle)

    configLoader = _loadConfigLoader()
    pluginRoot = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    _, pack = configLoader.resolvePack(repoRoot, pluginRoot)

    verdict = evaluateGate(ledger, pack)
    if verdict["open"]:
        print("Gate OPEN — the deliverable renders without a DRAFT badge.")
        return 0
    print("Gate CLOSED — the deliverable renders with a DRAFT badge.")
    for reason in verdict["reasons"]:
        print("  - {}".format(reason))
    return 1


if __name__ == "__main__":
    sys.exit(main())
