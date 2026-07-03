#!/usr/bin/env python3
"""PreToolUse gate: no score without ledger evidence.

Blocks a FIRST write to scoring/NN_*.md unless subject NN in
scoreLedger.json carries at least one evidence record whose artefact path
exists on disk. Scoring files are numbered by SUBJECT while reviews are
numbered by ARTEFACT intake order, so the two prefixes never need to
match — the ledger is the join. Edits to files that already exist pass —
the gate applies to first writes only.

Also gates scoreLedger.json: any reviews/ path cited in the new content
(evidence records cite their review as the artefact) must exist on disk.

The engagement root is resolved by walking up from the target file path
to the nearest engagement.yaml, falling back to CLAUDE_PROJECT_DIR. Exits
0 silently when neither resolves to an engagement. Structure is derived
from the engagement layout contract; nothing here is client or taxonomy
specific.
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


def deny(reason: str) -> None:
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )
    sys.exit(0)


def newText(tool: str, toolInput: dict) -> str:
    if tool == "Write":
        return toolInput.get("content") or ""
    if tool == "Edit":
        return toolInput.get("new_string") or ""
    if tool == "MultiEdit":
        return "\n".join((e.get("new_string") or "") for e in (toolInput.get("edits") or []))
    return ""


def main() -> None:
    event = readEvent()
    tool = event.get("tool_name", "")
    if tool not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)
    toolInput = event.get("tool_input") or {}
    path = toolInput.get("file_path") or ""
    if not path:
        sys.exit(0)

    root = engagementRoot(path)
    reviewsDir = os.path.join(root, "reviews")
    normalised = path.replace("\\", "/")

    # Gate 1: scoring/NN_*.md first writes need ledger evidence for subject NN.
    if "/scoring/" in normalised or normalised.startswith("scoring/"):
        if not normalised.endswith(".md"):
            sys.exit(0)
        # Edits to an existing scoring file pass; only first writes are gated.
        absPath = path if os.path.isabs(path) else os.path.join(root, path)
        if os.path.exists(absPath):
            sys.exit(0)
        m = re.match(r"^(\d{2})_", os.path.basename(normalised))
        if not m:
            sys.exit(0)
        prefix = m.group(1)
        entry = ledgerSubject(root, prefix)
        evidence = [
            e for e in ((entry or {}).get("evidence") or [])
            if isinstance(e, dict)
        ]
        backed = [
            e for e in evidence
            if (e.get("artefact") or "")
            and os.path.isfile(os.path.join(root, str(e.get("artefact"))))
        ]
        if backed:
            sys.exit(0)
        deny(
            f"Scoring gate blocked the write to {path}.\n\n"
            f"Subject {prefix} carries no evidence record in scoreLedger.json "
            "whose artefact exists on disk. A score may not be recorded "
            "without ledger evidence — run the intake and parse steps on the "
            "source artefact and record its evidence against subject "
            f"{prefix} first."
        )

    # Gate 2: scoreLedger.json — every cited reviews/ path must exist.
    if os.path.basename(normalised) == "scoreLedger.json":
        text = newText(tool, toolInput)
        cited = set(re.findall(r"reviews/(\d{2}_[A-Za-z0-9_]+_review\.md)", text))
        missing = sorted(
            name for name in cited
            if not os.path.isfile(os.path.join(reviewsDir, name))
        )
        if missing:
            bullets = "\n".join(f"  - reviews/{name}" for name in missing)
            deny(
                "Scoring gate blocked the ledger write.\n\n"
                "These evidence records cite reviews that do not exist on disk:\n"
                f"{bullets}\n\n"
                "File the review first — a score may not be recorded without "
                "a filed review."
            )
    sys.exit(0)


if __name__ == "__main__":
    main()
