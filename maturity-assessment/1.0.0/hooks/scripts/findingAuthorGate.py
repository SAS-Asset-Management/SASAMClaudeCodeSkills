#!/usr/bin/env python3
"""PreToolUse gate on writes to findings/.

A finding needs both sides of the evidence base, read from the subject's
scoreLedger.json entry (findings are numbered by SUBJECT while reviews
are numbered by ARTEFACT intake order, so file prefixes never join the
two — the ledger does): the say input (a reviews/ path among the
subject's evidence records) and the do input (an interviews/ path among
the evidence, or sayScore and doScore both set). Denies the write when
either is missing, and reminds every allowed write that only the
finding-synthesiser agent may author findings.

The engagement root is resolved by walking up from the target file path
to the nearest engagement.yaml, falling back to CLAUDE_PROJECT_DIR.
Exits 0 silently when neither resolves to an engagement.
"""
from __future__ import annotations

import json
import os
import re
import sys


def readEvent() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        sys.exit(0)


def engagementRoot(fromPath: str = "") -> str:
    if fromPath and os.path.isabs(fromPath):
        current = os.path.dirname(os.path.abspath(fromPath))
        while True:
            if os.path.isfile(os.path.join(current, "engagement.yaml")):
                return current
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent
    root = os.environ.get("CLAUDE_PROJECT_DIR") or ""
    if not root or not os.path.isfile(os.path.join(root, "engagement.yaml")):
        sys.exit(0)
    return root


def ledgerSubject(root: str, prefix: str) -> dict | None:
    """The scoreLedger.json subject entry whose key starts with NN_."""
    ledgerPath = os.path.join(root, "scoreLedger.json")
    if not os.path.isfile(ledgerPath):
        return None
    try:
        with open(ledgerPath, encoding="utf-8") as fh:
            ledger = json.load(fh)
    except Exception:
        return None
    for key, entry in (ledger.get("subjects") or {}).items():
        if key.startswith(prefix + "_") and isinstance(entry, dict):
            return entry
    return None


def main() -> None:
    event = readEvent()
    if event.get("tool_name") not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)
    path = (event.get("tool_input") or {}).get("file_path") or ""
    normalised = path.replace("\\", "/")
    if "/findings/" not in normalised and not normalised.startswith("findings/"):
        sys.exit(0)

    root = engagementRoot(path)

    m = re.match(r"^(\d{2})_", os.path.basename(normalised))
    if not m:
        # Outside the NN_ convention (indexes, run notes): remind, allow.
        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "permissionDecisionReason": (
                        "Reminder: only the finding-synthesiser agent may "
                        "author files under findings/."
                    ),
                }
            },
            sys.stdout,
        )
        sys.exit(0)
    prefix = m.group(1)

    entry = ledgerSubject(root, prefix)
    evidence = [
        e for e in ((entry or {}).get("evidence") or [])
        if isinstance(e, dict)
    ]
    artefacts = [
        str(e.get("artefact") or "").replace("\\", "/") for e in evidence
    ]
    hasSay = any(a.startswith("reviews/") for a in artefacts)
    hasDo = any(a.startswith("interviews/") for a in artefacts) or (
        entry is not None
        and entry.get("sayScore") is not None
        and entry.get("doScore") is not None
    )

    missing = []
    if not evidence:
        missing.append(
            f"ledger evidence: subject {prefix} has no evidence records in "
            "scoreLedger.json (score the subject from its reviewed "
            "artefacts first)"
        )
    else:
        if not hasSay:
            missing.append(
                f"say input: no reviews/ path among subject {prefix} evidence "
                "in scoreLedger.json (file the artefact review and record "
                "its evidence first)"
            )
        if not hasDo:
            missing.append(
                f"do input: no interviews/ path among subject {prefix} "
                "evidence in scoreLedger.json, and sayScore/doScore are not "
                "both set (run transcript-extractor on the interview "
                "transcript first)"
            )

    if missing:
        bullets = "\n".join(f"  - {item}" for item in missing)
        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Finding author gate blocked the write to {path}.\n\n"
                        "A finding reconciles say versus do — both inputs must "
                        "exist before it can be authored. Missing:\n"
                        f"{bullets}\n\n"
                        "Only the finding-synthesiser agent may author "
                        "findings, and it refuses on a missing input for the "
                        "same reason."
                    ),
                }
            },
            sys.stdout,
        )
        sys.exit(0)

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": (
                    "Say and do inputs verified. Reminder: only the "
                    "finding-synthesiser agent may author files under "
                    "findings/."
                ),
            }
        },
        sys.stdout,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
