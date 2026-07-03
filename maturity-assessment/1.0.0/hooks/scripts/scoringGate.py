#!/usr/bin/env python3
"""PreToolUse gate: no score without a matching review.

Blocks a FIRST write to scoring/NN_*.md unless a matching reviews/NN_*.md
exists (match by the two digit numeric prefix). Edits to files that already
exist pass — the gate applies to first writes only.

Also gates scoreLedger.json: any reviews/ path cited in the new content
(evidence records cite their review as the artefact) must exist on disk.

Exits 0 silently when the session is not an engagement (no engagement.yaml
under CLAUDE_PROJECT_DIR). Structure is derived from the engagement layout
contract; nothing here is client or taxonomy specific.
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


def engagementRoot() -> str:
    root = os.environ.get("CLAUDE_PROJECT_DIR") or ""
    if not root or not os.path.isfile(os.path.join(root, "engagement.yaml")):
        sys.exit(0)
    return root


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

    root = engagementRoot()
    reviewsDir = os.path.join(root, "reviews")
    normalised = path.replace("\\", "/")

    # Gate 1: scoring/NN_*.md first writes need reviews/NN_*.md.
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
        matches = []
        if os.path.isdir(reviewsDir):
            matches = [
                f for f in os.listdir(reviewsDir)
                if f.startswith(prefix + "_") and f.endswith(".md")
            ]
        if matches:
            sys.exit(0)
        deny(
            f"Scoring gate blocked the write to {path}.\n\n"
            f"No matching review found at reviews/{prefix}_*.md. "
            "A score may not be recorded without a filed review — run the "
            "intake and parse steps on the source artefact first, or confirm "
            f"the review file uses the {prefix}_ prefix."
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
