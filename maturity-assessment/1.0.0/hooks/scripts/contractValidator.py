#!/usr/bin/env python3
"""SessionStart: validate that what the plugin documents actually ships.

The drift killer ("README says ten, thirteen ship"). Checks:
  1. Every agents/*.md and skills/*/SKILL.md path the plugin CLAUDE.md
     references exists on disk under the plugin root.
  2. The pack directories required by pack.yaml flags exist —
     calcPack/ when calcPack is true, reportSpec/ always.
  3. scoreLedger.json, if present, parses and carries the contract top
     level keys (engagement, pack, scale, runs, subjects).

Discrepancies are emitted as additionalContext, never blocking.
Exits 0 silently when the session is not an engagement.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys

LEDGER_KEYS = ("engagement", "pack", "scale", "runs", "subjects")


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


def referencedPaths(pluginRoot: str) -> set[str]:
    claudeMd = os.path.join(pluginRoot, "CLAUDE.md")
    if not os.path.isfile(claudeMd):
        return set()
    try:
        with open(claudeMd, encoding="utf-8") as fh:
            text = fh.read()
    except Exception:
        return set()
    refs: set[str] = set()
    refs.update(re.findall(r"\bagents/[\w-]+\.md\b", text))
    refs.update(re.findall(r"\bskills/[\w-]+/SKILL\.md\b", text))
    return refs


def main() -> None:
    try:
        json.load(sys.stdin)
    except Exception:
        pass

    root = engagementRoot()
    pluginRoot = os.environ.get("CLAUDE_PLUGIN_ROOT") or ""
    issues: list[str] = []

    # 1. Referenced agents and skills exist.
    if pluginRoot:
        for ref in sorted(referencedPaths(pluginRoot)):
            if not os.path.isfile(os.path.join(pluginRoot, ref)):
                issues.append(f"plugin CLAUDE.md references '{ref}' but it does not exist on disk")

    # 2. Pack directories required by pack.yaml flags.
    loader = loadConfigLoader()
    if loader is not None:
        try:
            packDir, pack = loader.resolvePack(root, pluginRoot)
            if pack.get("calcPack") and not os.path.isdir(os.path.join(packDir, "calcPack")):
                issues.append(
                    f"pack '{pack.get('id', '?')}' declares calcPack true but {packDir}/calcPack/ is missing"
                )
            if not os.path.isdir(os.path.join(packDir, "reportSpec")):
                issues.append(
                    f"pack '{pack.get('id', '?')}' has no reportSpec/ directory — section specs and qaRules.yaml are required"
                )
        except Exception as exc:
            issues.append(f"pack resolution failed: {exc}")

    # 3. Ledger parses and carries the contract keys.
    ledgerPath = os.path.join(root, "scoreLedger.json")
    if os.path.isfile(ledgerPath):
        try:
            with open(ledgerPath, encoding="utf-8") as fh:
                ledger = json.load(fh)
            missing = [k for k in LEDGER_KEYS if k not in ledger]
            if missing:
                issues.append(
                    "scoreLedger.json is missing contract top level keys: " + ", ".join(missing)
                )
        except Exception as exc:
            issues.append(f"scoreLedger.json does not parse: {exc}")

    if not issues:
        sys.exit(0)

    bullets = "\n".join(f"- {i}" for i in issues)
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": (
                    "Contract validator found documentation or structure "
                    f"drift:\n{bullets}\n\n"
                    "Fix the drift before relying on the documented surface."
                ),
            }
        },
        sys.stdout,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
