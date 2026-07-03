"""Tests for the validated evidence append CLI (engine/ledger.py).

Every rejection path is exercised: bad tag, bad confidence, out of bounds
rubricLevel, missing artefact file, unknown subject. Nothing may reach the
ledger unless every check passes.
"""

from __future__ import annotations

import json
import os

import pytest


def _makeArtefact(repo, relPath):
    path = os.path.join(repo, relPath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write("# review\n")
    return relPath


def _appendArgs(repo, **overrides):
    values = {
        "subject": "03_assetData",
        "artefact": "reviews/06_assetRegisterExtract_review.md",
        "tag": "Direct",
        "rubricLevel": "3",
        "rubricQuote": "Asset data is maintained to a defined standard.",
        "confidence": "Medium",
    }
    values.update(overrides)
    return [
        "--repo", repo, "append-evidence",
        "--subject", values["subject"],
        "--artefact", values["artefact"],
        "--tag", values["tag"],
        "--rubric-level", values["rubricLevel"],
        "--rubric-quote", values["rubricQuote"],
        "--confidence", values["confidence"],
    ]


def _readLedger(repo):
    with open(os.path.join(repo, "scoreLedger.json")) as handle:
        return json.load(handle)


def test_append_evidence_happy_path(ledgerCli, aggregate, acmeRepo):
    _makeArtefact(acmeRepo, "reviews/06_assetRegisterExtract_review.md")
    assert ledgerCli.main(_appendArgs(acmeRepo)) == 0
    ledger = _readLedger(acmeRepo)
    records = ledger["subjects"]["03_assetData"]["evidence"]
    assert len(records) == 1
    assert records[0] == {
        "artefact": "reviews/06_assetRegisterExtract_review.md",
        "tag": "Direct",
        "rubricLevel": 3,
        "rubricQuote": "Asset data is maintained to a defined standard.",
        "confidence": "Medium",
    }
    # The appended record aggregates cleanly.
    aggregate.runAggregation(acmeRepo, today="2026-01-15", pluginRoot="/nonexistent")
    assert _readLedger(acmeRepo)["subjects"]["03_assetData"]["final"]["score"] == 3


def test_append_rejects_invalid_tag(ledgerCli, acmeRepo, capsys):
    _makeArtefact(acmeRepo, "reviews/06_assetRegisterExtract_review.md")
    assert ledgerCli.main(_appendArgs(acmeRepo, tag="Somewhat")) == 1
    assert "Somewhat" in capsys.readouterr().err
    assert _readLedger(acmeRepo)["subjects"]["03_assetData"]["evidence"] == []


def test_append_rejects_invalid_confidence(ledgerCli, acmeRepo, capsys):
    _makeArtefact(acmeRepo, "reviews/06_assetRegisterExtract_review.md")
    assert ledgerCli.main(_appendArgs(acmeRepo, confidence="Certain")) == 1
    assert "Certain" in capsys.readouterr().err
    assert _readLedger(acmeRepo)["subjects"]["03_assetData"]["evidence"] == []


def test_append_rejects_out_of_bounds_rubric_level(ledgerCli, acmeRepo, capsys):
    _makeArtefact(acmeRepo, "reviews/06_assetRegisterExtract_review.md")
    assert ledgerCli.main(_appendArgs(acmeRepo, rubricLevel="47")) == 1
    err = capsys.readouterr().err
    assert "47" in err and "between 0 and 5" in err
    assert _readLedger(acmeRepo)["subjects"]["03_assetData"]["evidence"] == []


def test_append_rejects_missing_artefact(ledgerCli, acmeRepo, capsys):
    assert ledgerCli.main(
        _appendArgs(acmeRepo, artefact="reviews/99_missing_review.md")
    ) == 1
    assert "does not exist" in capsys.readouterr().err
    assert _readLedger(acmeRepo)["subjects"]["03_assetData"]["evidence"] == []


def test_append_rejects_unknown_subject(ledgerCli, acmeRepo, capsys):
    _makeArtefact(acmeRepo, "reviews/06_assetRegisterExtract_review.md")
    assert ledgerCli.main(_appendArgs(acmeRepo, subject="99_notASubject")) == 1
    assert "99_notASubject" in capsys.readouterr().err


def test_tag_none_is_accepted(ledgerCli, acmeRepo):
    _makeArtefact(acmeRepo, "reviews/06_assetRegisterExtract_review.md")
    assert ledgerCli.main(_appendArgs(acmeRepo, tag="None")) == 0
    records = _readLedger(acmeRepo)["subjects"]["03_assetData"]["evidence"]
    assert records[0]["tag"] == "None"
