#!/usr/bin/env python3
"""PreToolUse gate on Bash: raw evidence never reaches a remote.

When the command contains git push or git commit, inspect the staged diff
and the outgoing commits (tolerating a missing upstream) and DENY when any
touched path starts with evidence/ or interviews/. Additionally warn via
systemMessage when engagement.yaml data.api is not "zdr-no-training".

Exits 0 silently when the session is not an engagement.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys

FORBIDDEN_PREFIXES = ("evidence/", "interviews/")


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


def gitLines(root: str, args: list[str]) -> list[str]:
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if res.returncode != 0:
            return []
        return [ln.strip() for ln in res.stdout.splitlines() if ln.strip()]
    except Exception:
        return []


def main() -> None:
    event = readEvent()
    if event.get("tool_name") != "Bash":
        sys.exit(0)
    command = (event.get("tool_input") or {}).get("command") or ""
    if not re.search(r"\bgit\b[^\n|;&]*\b(push|commit)\b", command):
        sys.exit(0)

    root = engagementRoot()

    touched: set[str] = set()
    touched.update(gitLines(root, ["diff", "--cached", "--name-only"]))
    # Outgoing commits; tolerate no upstream (command simply fails silently).
    touched.update(gitLines(root, ["log", "@{u}..", "--name-only", "--pretty=format:"]))

    offending = sorted(
        p for p in touched
        if any(p.startswith(prefix) for prefix in FORBIDDEN_PREFIXES)
    )
    if offending:
        bullets = "\n".join(f"  - {p}" for p in offending[:20])
        more = "" if len(offending) <= 20 else f"\n  ... and {len(offending) - 20} more"
        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        "Sovereignty gate blocked this git operation.\n\n"
                        "The staged or outgoing changes touch raw engagement "
                        "data that must never reach a remote:\n"
                        f"{bullets}{more}\n\n"
                        "Unstage these paths (git restore --staged <path>) or "
                        "remove the offending commits before pushing. Raw "
                        "evidence and interview material stay local per the "
                        "engagement's data sovereignty rule."
                    ),
                }
            },
            sys.stdout,
        )
        sys.exit(0)

    # ZDR warning: allowed, but nudge when the API posture is not asserted.
    loader = loadConfigLoader()
    if loader is not None:
        try:
            engagement = loader.loadEngagement(root)
            api = ((engagement.get("data") or {}).get("api")) or ""
            if api != "zdr-no-training":
                json.dump(
                    {
                        "systemMessage": (
                            "Sovereignty note: engagement.yaml data.api is "
                            f"'{api or 'unset'}', not 'zdr-no-training'. "
                            "Confirm the API data handling posture before "
                            "processing client evidence."
                        )
                    },
                    sys.stdout,
                )
        except Exception:
            pass
    sys.exit(0)


if __name__ == "__main__":
    main()
