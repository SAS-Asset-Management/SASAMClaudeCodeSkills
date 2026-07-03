#!/usr/bin/env python3
"""SessionStart: surface the resolved pack's known coverage gaps.

Reads coverageManifest.yaml from the resolved pack (engagement overlay
first, then the plugin pack) and emits knownGaps as additionalContext so
coverage holes are stated caveats rather than silent assumptions.

Exits 0 silently when the session is not an engagement or the manifest
is absent.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys


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


def loadConfigLoader():
    pluginRoot = os.environ.get("CLAUDE_PLUGIN_ROOT") or ""
    path = os.path.join(pluginRoot, "engine", "configLoader.py")
    if not os.path.isfile(path):
        return None
    try:
        spec = importlib.util.spec_from_file_location("configLoader", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        return None


def main() -> None:
    try:
        json.load(sys.stdin)
    except Exception:
        pass

    root = engagementRoot()
    loader = loadConfigLoader()
    if loader is None:
        sys.exit(0)

    try:
        pluginRoot = os.environ.get("CLAUDE_PLUGIN_ROOT") or ""
        packDir, pack = loader.resolvePack(root, pluginRoot)
    except Exception:
        sys.exit(0)

    manifestPath = os.path.join(packDir, "coverageManifest.yaml")
    if not os.path.isfile(manifestPath):
        sys.exit(0)
    try:
        manifest = loader.loadYaml(manifestPath) or {}
    except Exception:
        sys.exit(0)

    coverage = manifest.get("coverage") or {}
    gaps = manifest.get("knownGaps") or []

    lines = [f"Pack coverage ({pack.get('id', 'unknown pack')}):"]
    if coverage:
        subjects = coverage.get("subjects")
        if subjects:
            lines.append(f"- subjects: {subjects}")
        questionBank = coverage.get("questionBank")
        if questionBank:
            lines.append(f"- question bank: {questionBank}")
        if "standardChunked" in coverage:
            lines.append(f"- standard chunked: {coverage.get('standardChunked')}")
        calcEngines = coverage.get("calcEngines") or {}
        pending = [k for k, v in calcEngines.items() if v != "implemented"]
        if pending:
            lines.append(f"- calc engines not implemented: {', '.join(sorted(pending))}")
    if gaps:
        lines.append("Known gaps — state these as caveats wherever they bear on a score or finding:")
        lines.extend(f"- {g}" for g in gaps)
    if len(lines) == 1:
        sys.exit(0)

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "\n".join(lines),
            }
        },
        sys.stdout,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
