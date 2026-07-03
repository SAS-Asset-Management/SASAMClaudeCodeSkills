#!/usr/bin/env python3
"""PreToolUse gate on writes under deliverable/.

Denies content that imports a Python plotting library (the deliverable
renders plots in JavaScript from vendored Plotly, never rasterised via
Python), and content defining a render function outside the closed plot
catalogue. The render function check is a soft tripwire: it catches ad
hoc plots added outside the catalogue, and says so in the reason.

Exits 0 silently when the session is not an engagement.
"""
from __future__ import annotations

import json
import os
import re
import sys

PY_PLOT_LIBS = ("matplotlib", "seaborn", "plotnine", "pylab", "altair")
ALLOWED_RENDERERS = {
    "renderDomainRadar",
    "renderSubjectConfidence",
    "renderRunTrend",
    "renderPeerPercentile",
}
IMPORT_RX = re.compile(
    r"^\s*(?:import\s+(\w+)|from\s+(\w+)(?:\.\w+)*\s+import)", re.MULTILINE
)
RENDER_DEF_RX = re.compile(
    r"(?:\bfunction\s+(render[A-Z]\w*)\s*\(|\b(?:const|let|var)\s+(render[A-Z]\w*)\s*=|\bdef\s+(render[A-Z]\w*)\s*\()"
)


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


def main() -> None:
    event = readEvent()
    tool = event.get("tool_name", "")
    if tool not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)
    toolInput = event.get("tool_input") or {}
    path = (toolInput.get("file_path") or "").replace("\\", "/")
    if "/deliverable/" not in f"/{path}":
        sys.exit(0)

    engagementRoot()

    if tool == "Write":
        text = toolInput.get("content") or ""
    elif tool == "Edit":
        text = toolInput.get("new_string") or ""
    else:
        text = "\n".join((e.get("new_string") or "") for e in (toolInput.get("edits") or []))
    if not text:
        sys.exit(0)

    for m in IMPORT_RX.finditer(text):
        module = (m.group(1) or m.group(2) or "").lower()
        if module in PY_PLOT_LIBS:
            deny(
                f"Plot blocker: {path} imports the Python plotting library "
                f"'{module}'. The deliverable renders plots in JavaScript "
                "only (vendored Plotly, closed catalogue: domainRadar, "
                "subjectConfidence, runTrend, peerPercentile). Never "
                "rasterise plots via Python."
            )

    for m in RENDER_DEF_RX.finditer(text):
        name = m.group(1) or m.group(2) or m.group(3)
        if name not in ALLOWED_RENDERERS:
            allowed = ", ".join(sorted(ALLOWED_RENDERERS))
            deny(
                f"Plot blocker: {path} defines '{name}', a render function "
                "outside the closed plot catalogue. Allowed renderers: "
                f"{allowed}. This is a soft tripwire for ad hoc plots — if "
                "this function is genuinely not a plot renderer, rename it "
                "so it does not match render[A-Z]* and retry."
            )
    sys.exit(0)


if __name__ == "__main__":
    main()
