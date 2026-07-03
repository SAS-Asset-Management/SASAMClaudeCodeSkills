"""Engagement repo scaffolder for the maturity assessment suite.

Stands up a new engagement repo in one command:

* the directory tree: evidence, reviews, scoring, interviews, findings,
  deliverable, tracking, packs
* a data sovereignty .gitignore (client evidence never reaches a remote;
  defence in depth behind the sovereigntyGate hook)
* engagement.yaml copied from schemas/engagementExample.yaml with
  placeholder client and code values for the assessor to fill in
* one aggregation run to seed scoreLedger.json with every taxonomy subject
  unscored

CLI:
    python3 init.py --repo <engagementRoot>

The command refuses to run against a repo that already has an
engagement.yaml, so it can never clobber a live engagement.
"""

from __future__ import annotations

import argparse
import datetime
import importlib.util
import os
import re
import sys

_ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
_PLUGIN_ROOT = os.path.dirname(_ENGINE_DIR)

DIRECTORIES = (
    "evidence",
    "reviews",
    "scoring",
    "interviews",
    "findings",
    "deliverable",
    "tracking",
    "packs",
)

GITIGNORE = """\
# ============================================================
# Data sovereignty — client evidence NEVER leaves this repo.
# Defence in depth behind the sovereigntyGate hook.
# ============================================================

# Raw client artefacts and interview material
evidence/*
!evidence/ARTEFACT_SCHEDULE.md
interviews/*

# Tabular data
*.csv
*.tsv
*.xlsx
*.xls
*.parquet

# Documents that may contain client information
*.pdf
*.docx
*.doc
*.pptx
*.ppt

# Database dumps and structured exports
*.sql
*.db
*.sqlite
*.sqlite3
*.dump
*.bak

# Environment and credentials
.env
.env.*
*.pem
*.key
credentials.json
secrets.*

# IDE and OS
.DS_Store
.vscode/
.idea/
__pycache__/
"""

NEXT_STEPS = """\
Engagement repo initialised at {repoRoot}

Next steps:
  1. Edit engagement.yaml: replace <clientName> and <engagementCode>, and
     confirm the framework pack, scale, and weights suit this engagement.
  2. Drop the first client artefacts into evidence/ and register them with
     the maturity-intake skill.
  3. Check where things stand at any time:
     python3 {engineDir}/orchestrate.py --repo {repoRoot} status
"""


def _loadEngineModule(name):
    spec = importlib.util.spec_from_file_location(
        f"maturity_{name}", os.path.join(_ENGINE_DIR, f"{name}.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _placeholderEngagement(exampleText, today):
    """Turn the example engagement into a placeholder one: fictional client
    and code become obvious placeholders, the start date becomes today."""
    text = exampleText.replace("Acme Rail", "<clientName>")
    text = text.replace("ACME-CYBER-2026", "<engagementCode>")
    text = re.sub(r"^(  start: ).*$", rf"\g<1>{today}", text, count=1, flags=re.MULTILINE)
    return text


def initEngagement(repoRoot, today=None, pluginRoot=None):
    """Scaffold the engagement repo. Raises FileExistsError when the repo is
    already initialised. Returns the engagement.yaml path."""
    if pluginRoot is None:
        pluginRoot = _PLUGIN_ROOT
    engagementPath = os.path.join(repoRoot, "engagement.yaml")
    if os.path.isfile(engagementPath):
        raise FileExistsError(
            f"{engagementPath} already exists — this repo is already initialised. "
            "Edit it directly rather than re running init."
        )
    os.makedirs(repoRoot, exist_ok=True)
    for name in DIRECTORIES:
        os.makedirs(os.path.join(repoRoot, name), exist_ok=True)

    gitignorePath = os.path.join(repoRoot, ".gitignore")
    if not os.path.isfile(gitignorePath):
        with open(gitignorePath, "w", encoding="utf-8") as handle:
            handle.write(GITIGNORE)

    examplePath = os.path.join(pluginRoot, "schemas", "engagementExample.yaml")
    with open(examplePath, "r", encoding="utf-8") as handle:
        exampleText = handle.read()
    if today is None:
        today = datetime.date.today().isoformat()
    with open(engagementPath, "w", encoding="utf-8") as handle:
        handle.write(_placeholderEngagement(exampleText, today))

    aggregate = _loadEngineModule("aggregate")
    aggregate.runAggregation(
        repoRoot, trigger="engagement initialised", pluginRoot=pluginRoot
    )
    return engagementPath


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Scaffold a new maturity assessment engagement repo."
    )
    parser.add_argument("--repo", required=True, help="engagement repo root to create")
    args = parser.parse_args(argv)
    try:
        initEngagement(args.repo)
    except FileExistsError as error:
        print(f"init refused: {error}", file=sys.stderr)
        return 1
    print(NEXT_STEPS.format(repoRoot=args.repo, engineDir=_ENGINE_DIR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
