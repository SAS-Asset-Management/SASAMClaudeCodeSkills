"""Tests for the fan out orchestrator: resume semantics and the
reconciliation gate failure modes."""

from __future__ import annotations

import json
import os

import pytest


def _readLedger(repo):
    with open(os.path.join(repo, "scoreLedger.json")) as handle:
        return json.load(handle)


def _writeLedger(repo, ledger):
    with open(os.path.join(repo, "scoreLedger.json"), "w") as handle:
        handle.write(json.dumps(ledger, indent=2) + "\n")


def _scoreEverything(repo, aggregate):
    """Give every subject evidence and finals so the gate can open."""
    ledger = _readLedger(repo)
    ledger["subjects"]["03_assetData"]["evidence"].append(
        {"artefact": "reviews/06_assetRegisterExtract_review.md", "tag": "Direct",
         "rubricLevel": 3, "rubricQuote": "Asset data is maintained to a defined standard.",
         "confidence": "Medium"}
    )
    _writeLedger(repo, ledger)
    aggregate.runAggregation(repo, today="2026-01-15", pluginRoot="/nonexistent")


# ---- plan: resume semantics ---------------------------------------------------

def test_plan_pending_score_resumes(orchestrate, aggregate, acmeRepo):
    # Before any aggregation every subject is pending.
    plan = orchestrate.cmdPlan(acmeRepo)
    assert plan["pendingScore"] == [
        "01_governancePolicy", "02_riskRegister", "03_assetData"
    ]
    # Aggregation scores the two evidenced subjects; only the third remains.
    aggregate.runAggregation(acmeRepo, today="2026-01-15", pluginRoot="/nonexistent")
    plan = orchestrate.cmdPlan(acmeRepo)
    assert plan["pendingScore"] == ["03_assetData"]


def test_plan_pending_findings_uses_latest_run(orchestrate, aggregate, acmeRepo):
    aggregate.runAggregation(acmeRepo, today="2026-01-15", pluginRoot="/nonexistent")
    runDir = os.path.join(acmeRepo, "findings", "run01")
    os.makedirs(runDir)
    open(os.path.join(runDir, "01_governancePolicy_finding.md"), "w").write("# Finding\n")
    plan = orchestrate.cmdPlan(acmeRepo)
    # 01 has a finding; 02 has evidence but no finding; 03 has no evidence at all.
    assert plan["pendingFindings"] == ["02_riskRegister"]
    # A later run supersedes: run02 with no files makes both evidenced subjects pending.
    os.makedirs(os.path.join(acmeRepo, "findings", "run02"))
    plan = orchestrate.cmdPlan(acmeRepo)
    assert plan["pendingFindings"] == ["01_governancePolicy", "02_riskRegister"]


def test_plan_pending_sections(orchestrate, acmeRepo):
    plan = orchestrate.cmdPlan(acmeRepo)
    assert plan["pendingSections"] == ["01_executiveSummary.md", "02_methodology.md"]
    draftsDir = os.path.join(acmeRepo, "deliverable", "draft")
    os.makedirs(draftsDir)
    open(os.path.join(draftsDir, "01_executiveSummary.md"), "w").write("# Draft\n")
    plan = orchestrate.cmdPlan(acmeRepo)
    assert plan["pendingSections"] == ["02_methodology.md"]


# ---- check: reconciliation gate ------------------------------------------------

def test_check_fails_on_unscored_subject(orchestrate, aggregate, acmeRepo):
    aggregate.runAggregation(acmeRepo, today="2026-01-15", pluginRoot="/nonexistent")
    ok, reasons = orchestrate.cmdCheck(acmeRepo)
    assert ok is False
    assert any("03_assetData" in reason for reason in reasons)
    assert orchestrate.main(["--repo", acmeRepo, "check"]) == 1


def test_check_passes_when_clean(orchestrate, aggregate, acmeRepo):
    _scoreEverything(acmeRepo, aggregate)
    ok, reasons = orchestrate.cmdCheck(acmeRepo)
    assert ok is True and reasons == []
    assert orchestrate.main(["--repo", acmeRepo, "check"]) == 0


def test_check_fails_on_finding_without_say_and_do(orchestrate, aggregate, acmeRepo):
    _scoreEverything(acmeRepo, aggregate)
    runDir = os.path.join(acmeRepo, "findings", "run01")
    os.makedirs(runDir)
    # 02_riskRegister has null sayScore and doScore in the fixture.
    open(os.path.join(runDir, "02_riskRegister_finding.md"), "w").write("# Finding\n")
    ok, reasons = orchestrate.cmdCheck(acmeRepo)
    assert ok is False
    assert any("sayScore or doScore" in reason for reason in reasons)


def test_check_fails_on_open_dispute(orchestrate, aggregate, acmeRepo):
    _scoreEverything(acmeRepo, aggregate)
    ledger = _readLedger(acmeRepo)
    ledger["subjects"]["01_governancePolicy"]["disputes"].append(
        {"id": "DSP-02", "raised": "2026-01-14", "description": "Assessee contests the score",
         "status": "open", "resolution": None}
    )
    _writeLedger(acmeRepo, ledger)
    ok, reasons = orchestrate.cmdCheck(acmeRepo)
    assert ok is False
    assert any("open dispute" in reason for reason in reasons)
    assert orchestrate.main(["--repo", acmeRepo, "check"]) == 1


def _enableComplianceMatrix(repo):
    packYaml = os.path.join(repo, "packs", "acme-rail-governance", "pack.yaml")
    text = open(packYaml).read().replace("complianceMatrix: false", "complianceMatrix: true")
    open(packYaml, "w").write(text)
    os.makedirs(os.path.join(repo, "compliance"), exist_ok=True)


def _writeCsv(repo, name, rows):
    with open(os.path.join(repo, "compliance", name), "w") as handle:
        handle.write("\n".join(rows) + "\n")


def test_check_fails_on_matrix_row_count_mismatch(orchestrate, aggregate, acmeRepo):
    _scoreEverything(acmeRepo, aggregate)
    _enableComplianceMatrix(acmeRepo)
    _writeCsv(acmeRepo, "requirements.csv", [
        "requirementId,text",
        "REQ-04.7-01,Requirement one",
        "REQ-04.7-02,Requirement two",
        "REQ-04.7-03,Requirement three",
    ])
    _writeCsv(acmeRepo, "matrix.csv", [
        "requirementId,conformance",
        "REQ-04.7-01,Complete",
        "REQ-04.7-02,Partial",
    ])
    ok, reasons = orchestrate.cmdCheck(acmeRepo)
    assert ok is False
    assert any("2 rows" in reason and "3" in reason for reason in reasons)
    assert orchestrate.main(["--repo", acmeRepo, "check"]) == 1


def test_check_validates_conformance_enum(orchestrate, aggregate, acmeRepo):
    _scoreEverything(acmeRepo, aggregate)
    _enableComplianceMatrix(acmeRepo)
    _writeCsv(acmeRepo, "requirements.csv", ["requirementId,text", "REQ-04.7-01,Requirement one"])
    _writeCsv(acmeRepo, "matrix.csv", ["requirementId,conformance", "REQ-04.7-01,Mostly"])
    ok, reasons = orchestrate.cmdCheck(acmeRepo)
    assert ok is False
    assert any("Mostly" in reason for reason in reasons)
    # Correct the value: the gate opens.
    _writeCsv(acmeRepo, "matrix.csv", ["requirementId,conformance", "REQ-04.7-01,Out of scope"])
    ok, reasons = orchestrate.cmdCheck(acmeRepo)
    assert ok is True


def _setEngagementComplianceMatrix(repo, value):
    path = os.path.join(repo, "engagement.yaml")
    text = open(path).read().replace(
        "  rounding: from-0.7",
        f"  rounding: from-0.7\n  complianceMatrix: {value}",
    )
    open(path, "w").write(text)


def test_check_engagement_overrides_pack_compliance_on(orchestrate, aggregate, acmeRepo):
    # Pack says false; engagement.yaml switches the matrix track on.
    _scoreEverything(acmeRepo, aggregate)
    _setEngagementComplianceMatrix(acmeRepo, "true")
    ok, reasons = orchestrate.cmdCheck(acmeRepo)
    assert ok is False
    assert any("complianceMatrix is enabled" in reason for reason in reasons)


def test_check_engagement_overrides_pack_compliance_off(orchestrate, aggregate, acmeRepo):
    # Pack says true; engagement.yaml switches the matrix track off, so the
    # gate opens with no compliance files at all.
    _scoreEverything(acmeRepo, aggregate)
    _enableComplianceMatrix(acmeRepo)
    _setEngagementComplianceMatrix(acmeRepo, "false")
    ok, reasons = orchestrate.cmdCheck(acmeRepo)
    assert ok is True and reasons == []


# ---- status ---------------------------------------------------------------------

def test_status_renders_counts(orchestrate, aggregate, acmeRepo):
    aggregate.runAggregation(acmeRepo, today="2026-01-15", pluginRoot="/nonexistent")
    os.makedirs(os.path.join(acmeRepo, "reviews"))
    open(os.path.join(acmeRepo, "reviews", "01_governancePolicy_review.md"), "w").write("x\n")
    os.makedirs(os.path.join(acmeRepo, "evidence"))
    open(os.path.join(acmeRepo, "evidence", "ARTEFACT_SCHEDULE.md"), "w").write("x\n")
    open(os.path.join(acmeRepo, "evidence", "governancePolicy.pdf"), "w").write("x\n")
    table = orchestrate.cmdStatus(acmeRepo)
    assert "2 of 3" in table          # subjects scored
    assert "1 of 1" in table          # reviews versus artefacts (schedule excluded)
    assert orchestrate.main(["--repo", acmeRepo, "status"]) == 0
