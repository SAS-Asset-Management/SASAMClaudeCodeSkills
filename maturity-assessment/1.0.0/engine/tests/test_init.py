"""Tests for the engagement repo scaffolder (engine/init.py)."""

from __future__ import annotations

import json
import os

import pytest

ENGINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_ROOT = os.path.dirname(ENGINE_DIR)

EXPECTED_DIRECTORIES = (
    "evidence", "reviews", "scoring", "interviews", "findings",
    "deliverable", "tracking", "packs",
)


def test_init_scaffolds_engagement_repo(initEngine, tmp_path):
    repo = str(tmp_path / "newEngagement")
    path = initEngine.initEngagement(repo, today="2026-07-04", pluginRoot=PLUGIN_ROOT)
    assert path == os.path.join(repo, "engagement.yaml")
    for name in EXPECTED_DIRECTORIES:
        assert os.path.isdir(os.path.join(repo, name)), name

    gitignore = open(os.path.join(repo, ".gitignore")).read()
    assert "evidence/*" in gitignore
    assert "interviews/*" in gitignore
    assert "*.pdf" in gitignore

    engagementText = open(path).read()
    assert "<clientName>" in engagementText
    assert "<engagementCode>" in engagementText
    assert "start: 2026-07-04" in engagementText
    assert "Acme Rail" not in engagementText

    # The seeding aggregation ran once: every taxonomy subject exists unscored.
    ledger = json.loads(open(os.path.join(repo, "scoreLedger.json")).read())
    assert ledger["pack"].startswith("mdr-governance-v3@")
    assert len(ledger["subjects"]) == 25
    assert all(
        subject["final"] == {"score": None, "confidence": None, "ci": None}
        for subject in ledger["subjects"].values()
    )
    assert ledger["runs"][-1]["trigger"] == "engagement initialised"


def test_init_refuses_to_reinitialise(initEngine, tmp_path):
    repo = str(tmp_path / "newEngagement")
    initEngine.initEngagement(repo, today="2026-07-04", pluginRoot=PLUGIN_ROOT)
    with pytest.raises(FileExistsError):
        initEngine.initEngagement(repo, today="2026-07-04", pluginRoot=PLUGIN_ROOT)
    assert initEngine.main(["--repo", repo]) == 1


def test_init_cli_prints_next_steps(initEngine, tmp_path, capsys):
    repo = str(tmp_path / "cliEngagement")
    assert initEngine.main(["--repo", repo]) == 0
    out = capsys.readouterr().out
    assert "Next steps" in out
    assert "engagement.yaml" in out
    assert "orchestrate.py" in out


def test_config_loader_missing_engagement_points_at_init(configLoader, tmp_path):
    with pytest.raises(FileNotFoundError) as excinfo:
        configLoader.loadEngagement(str(tmp_path))
    message = str(excinfo.value)
    assert "init.py" in message
    assert "maturity-intake" not in message
