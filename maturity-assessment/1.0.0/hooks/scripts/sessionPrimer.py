#!/usr/bin/env python3
"""SessionStart: zero touch engagement progress snapshot.

Everything is derived live from the engagement — week N of
engagement.weeks from engagement.start, artefact count under evidence/,
review count, subjects scored (ledger subjects with a final score) out
of the pack taxonomy total, and open disputes. Nothing is hand
maintained.

Exits 0 silently when the session is not an engagement.
"""
from __future__ import annotations

import datetime
import importlib.util
import json
import os
import sys


def engagementRoot() -> str:
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


def countFiles(directory: str, suffix: str = "") -> int:
    if not os.path.isdir(directory):
        return 0
    return sum(
        1 for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
        and not f.startswith(".")
        and f.endswith(suffix)
    )


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
        engagement = loader.loadEngagement(root)
    except Exception:
        sys.exit(0)
    meta = engagement.get("engagement") or {}

    lines = []

    # Engagement clock.
    start = str(meta.get("start") or "")
    weeks = int(meta.get("weeks") or 0)
    try:
        startDate = datetime.date.fromisoformat(start)
        elapsed = (datetime.date.today() - startDate).days
        week = max(1, min(weeks or 1, elapsed // 7 + 1)) if elapsed >= 0 else 0
        displayStart = startDate.strftime("%d/%m/%Y")
        if week:
            lines.append(f"Engagement clock: week {week} of {weeks} ({elapsed} days since {displayStart}).")
        else:
            lines.append(f"Engagement starts {displayStart}.")
    except Exception:
        pass

    # Evidence pipeline.
    artefacts = countFiles(os.path.join(root, "evidence"))
    reviews = countFiles(os.path.join(root, "reviews"), ".md")
    lines.append(f"Artefacts: {artefacts} received, {reviews} reviewed.")

    # Ledger position against the pack taxonomy.
    taxonomyTotal = 0
    try:
        pluginRoot = os.environ.get("CLAUDE_PLUGIN_ROOT") or ""
        _packDir, pack = loader.resolvePack(root, pluginRoot)
        for domain in ((pack.get("taxonomy") or {}).get("domains")) or []:
            taxonomyTotal += len(domain.get("subjects") or [])
    except Exception:
        pass

    ledgerPath = os.path.join(root, "scoreLedger.json")
    scored = 0
    openDisputes = 0
    if os.path.isfile(ledgerPath):
        try:
            with open(ledgerPath, encoding="utf-8") as fh:
                ledger = json.load(fh)
            for entry in (ledger.get("subjects") or {}).values():
                final = entry.get("final") or {}
                if final.get("score") is not None:
                    scored += 1
                openDisputes += sum(
                    1 for d in (entry.get("disputes") or [])
                    if d.get("status") == "open"
                )
        except Exception:
            lines.append("scoreLedger.json present but unreadable — check it before scoring.")
    if taxonomyTotal:
        lines.append(f"Subjects scored: {scored} of {taxonomyTotal}.")
    elif scored:
        lines.append(f"Subjects scored: {scored}.")
    if openDisputes:
        lines.append(f"Open disputes needing an assessor ruling: {openDisputes}.")

    if not lines:
        sys.exit(0)

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "Engagement snapshot (derived live):\n" + "\n".join(f"- {l}" for l in lines),
            }
        },
        sys.stdout,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
