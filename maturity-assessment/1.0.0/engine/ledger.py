"""Validated ledger writes for the maturity assessment suite.

Skills and agents append evidence to scoreLedger.json through this CLI, never
by hand editing JSON. Every append is validated against the resolved pack
before anything touches disk, so a malformed record can never enter the
ledger in the first place:

* tag must be one of None, Indirect, Direct
* confidence must be one of Low, Medium, High
* rubricLevel must be an integer within the pack scale bounds
* the cited artefact file must exist in the engagement repo
* the subject id must exist in the pack taxonomy

CLI:
    python3 ledger.py --repo <engagementRoot> append-evidence \
        --subject <subjectId> --artefact <repoRelativePath> \
        --tag <None|Indirect|Direct> --rubric-level <int> \
        --rubric-quote "<verbatim rubric sentence>" \
        --confidence <Low|Medium|High>

On success the record is appended and the ledger rewritten through the
aggregation engine's deterministic, atomic writer. Run aggregate.py
afterwards to recompute finals.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys

_ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))


def _loadEngineModule(name):
    spec = importlib.util.spec_from_file_location(
        f"maturity_{name}", os.path.join(_ENGINE_DIR, f"{name}.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _taxonomySubjects(pack):
    subjects = []
    for domain in (pack.get("taxonomy") or {}).get("domains") or []:
        subjects.extend(domain.get("subjects") or [])
    return subjects


def appendEvidence(repoRoot, subjectId, artefact, tag, rubricLevel, rubricQuote,
                   confidence, pluginRoot=None):
    """Validate then append one evidence record. Raises ValueError on any
    invalid input; nothing is written unless every check passes."""
    loader = _loadEngineModule("configLoader")
    aggregate = _loadEngineModule("aggregate")
    if pluginRoot is None:
        pluginRoot = os.path.dirname(_ENGINE_DIR)
    _, pack = loader.resolvePack(repoRoot, pluginRoot)

    if tag not in aggregate.VALID_TAGS:
        raise ValueError(f"tag {tag!r} is not one of {', '.join(aggregate.VALID_TAGS)}")
    if confidence not in aggregate.VALID_CONFIDENCE:
        raise ValueError(
            f"confidence {confidence!r} is not one of {', '.join(aggregate.VALID_CONFIDENCE)}"
        )
    scaleLow, scaleHigh = loader.scaleBounds(pack)
    if not isinstance(rubricLevel, int) or isinstance(rubricLevel, bool) or not (
        scaleLow <= rubricLevel <= scaleHigh
    ):
        raise ValueError(
            f"rubricLevel {rubricLevel!r} is not an integer between {scaleLow} and {scaleHigh} "
            f"(pack scale {(pack.get('scale') or {}).get('id')})"
        )
    subjects = _taxonomySubjects(pack)
    if subjectId not in subjects:
        raise ValueError(
            f"subject {subjectId!r} is not in the pack taxonomy; known subjects: "
            + ", ".join(subjects)
        )
    artefactPath = os.path.join(repoRoot, artefact)
    if not os.path.isfile(artefactPath):
        raise ValueError(
            f"cited artefact {artefact!r} does not exist in the engagement repo "
            f"(looked at {artefactPath})"
        )

    ledgerPath = os.path.join(repoRoot, "scoreLedger.json")
    if os.path.isfile(ledgerPath):
        ledger = aggregate.loadLedger(ledgerPath)
    else:
        ledger = {"runs": [], "subjects": {}}
    ledger.setdefault("subjects", {})
    subject = ledger["subjects"].setdefault(subjectId, aggregate._emptySubject())
    subject.setdefault("evidence", []).append(
        {
            "artefact": artefact,
            "tag": tag,
            "rubricLevel": rubricLevel,
            "rubricQuote": rubricQuote,
            "confidence": confidence,
        }
    )
    aggregate.writeLedger(ledgerPath, ledger)
    return ledgerPath


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validated evidence appends to scoreLedger.json."
    )
    parser.add_argument("--repo", required=True, help="engagement repo root")
    subparsers = parser.add_subparsers(dest="verb", required=True)

    appendParser = subparsers.add_parser(
        "append-evidence", help="validate and append one evidence record"
    )
    appendParser.add_argument("--subject", required=True, help="subject id, e.g. 01_governancePolicy")
    appendParser.add_argument("--artefact", required=True, help="engagement relative artefact path")
    appendParser.add_argument("--tag", required=True, help="None, Indirect, or Direct")
    appendParser.add_argument("--rubric-level", dest="rubricLevel", required=True, type=int,
                              help="integer rubric level within the pack scale bounds")
    appendParser.add_argument("--rubric-quote", dest="rubricQuote", required=True,
                              help="verbatim rubric sentence the evidence was scored against")
    appendParser.add_argument("--confidence", required=True, help="Low, Medium, or High")

    args = parser.parse_args(argv)
    try:
        ledgerPath = appendEvidence(
            args.repo, args.subject, args.artefact, args.tag, args.rubricLevel,
            args.rubricQuote, args.confidence,
        )
    except (ValueError, FileNotFoundError) as error:
        print(f"append-evidence rejected: {error}", file=sys.stderr)
        return 1
    print(f"Evidence appended to {ledgerPath} for {args.subject}.")
    print("Run: python3 engine/aggregate.py --repo <repo> to recompute finals.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
