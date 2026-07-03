#!/usr/bin/env python3
"""PreToolUse gate on writes to findings/.

A finding needs both sides of the evidence base: the say input (at least
one review matching the subject's numeric prefix under reviews/) and the
do input (interview notes matching interviews/NN_*_notes.md). Denies the
write when either is missing, and reminds every allowed write that only
the finding-synthesiser agent may author findings.

Exits 0 silently when the session is not an engagement.
"""
from __future__ import annotations

import glob
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


def main() -> None:
    event = readEvent()
    if event.get("tool_name") not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)
    path = (event.get("tool_input") or {}).get("file_path") or ""
    normalised = path.replace("\\", "/")
    if "/findings/" not in normalised and not normalised.startswith("findings/"):
        sys.exit(0)

    root = engagementRoot()

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

    notes = glob.glob(os.path.join(root, "interviews", f"{prefix}_*_notes.md"))
    reviews = glob.glob(os.path.join(root, "reviews", f"{prefix}_*.md"))

    missing = []
    if not notes:
        missing.append(
            f"do input: interviews/{prefix}_*_notes.md (run transcript-extractor "
            "on the interview transcript first)"
        )
    if not reviews:
        missing.append(
            f"say input: reviews/{prefix}_*.md (file the artefact review first)"
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
