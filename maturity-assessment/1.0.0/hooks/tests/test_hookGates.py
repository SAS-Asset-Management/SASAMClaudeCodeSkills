"""Smoke tests for the hook gates.

Each test drives a hook script as a subprocess, the way Claude Code does:
event JSON on stdin, decision JSON (or silence) on stdout. Fixtures build
a throwaway engagement so the gates read a real layout, and the proseRules
tests run against the real pack qaRules.yaml shipped in this plugin.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = PLUGIN_ROOT / "hooks" / "scripts"

ENGAGEMENT_YAML = """engagement:
  client: "Test Client"
  code: "TEST-2026"

framework:
  pack: "mdr-governance-v3"
  scale: "iam-0-5"

brand:
  bannedPhrasings: ["synergy"]
"""


def runHook(script: str, event: dict, env: dict | None = None) -> str:
    """Run a hook script with the event on stdin; return stdout."""
    fullEnv = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_ROOT")}
    if env:
        fullEnv.update(env)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        env=fullEnv,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def writeEvent(path: Path, content: str = "x") -> dict:
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": str(path), "content": content},
    }


def makeEngagement(root: Path, subjects: dict) -> None:
    (root / "engagement.yaml").write_text(ENGAGEMENT_YAML, encoding="utf-8")
    ledger = {
        "engagement": "TEST-2026",
        "pack": "mdr-governance-v3",
        "scale": "iam-0-5",
        "runs": [],
        "subjects": subjects,
    }
    (root / "scoreLedger.json").write_text(json.dumps(ledger), encoding="utf-8")
    for sub in ("reviews", "interviews", "scoring", "findings"):
        (root / sub).mkdir()


def subjectEntry(evidence: list[dict], sayScore=None, doScore=None) -> dict:
    return {
        "final": {"score": None, "confidence": None, "ci": None},
        "sayScore": sayScore,
        "doScore": doScore,
        "evidence": evidence,
        "history": [],
        "flag": None,
        "disputes": [],
    }


# --- scoringGate ------------------------------------------------------------

def test_scoringGateAllowsRoadTestCase(tmp_path):
    """The road test case: scoring/06_* draws its evidence from review 02.

    Subject and review numbering never match — the ledger evidence record
    is the join, and the gate must ALLOW.
    """
    makeEngagement(tmp_path, {
        "06_assessorCompetency": subjectEntry([
            {"artefact": "reviews/02_nlrTrackAssessmentProcedure_review.md", "tag": "Direct"},
        ]),
    })
    (tmp_path / "reviews" / "02_nlrTrackAssessmentProcedure_review.md").write_text("review", encoding="utf-8")

    out = runHook("scoringGate.py", writeEvent(tmp_path / "scoring" / "06_assessorCompetency_scoring.md"))
    assert out == ""


def test_scoringGateDeniesSubjectWithNoEvidence(tmp_path):
    makeEngagement(tmp_path, {
        "07_emptySubject": subjectEntry([]),
    })
    out = runHook("scoringGate.py", writeEvent(tmp_path / "scoring" / "07_emptySubject_scoring.md"))
    assert '"deny"' in out
    assert "no evidence record" in out


def test_scoringGateDeniesWhenEvidenceArtefactMissingOnDisk(tmp_path):
    makeEngagement(tmp_path, {
        "06_assessorCompetency": subjectEntry([
            {"artefact": "reviews/02_missing_review.md", "tag": "Direct"},
        ]),
    })
    out = runHook("scoringGate.py", writeEvent(tmp_path / "scoring" / "06_assessorCompetency_scoring.md"))
    assert '"deny"' in out


def test_scoringGateResolvesRootFromFilePath(tmp_path):
    """The gate must fire even when CLAUDE_PROJECT_DIR points elsewhere —
    root resolution walks up from the target file path."""
    engagement = tmp_path / "engagement"
    engagement.mkdir()
    makeEngagement(engagement, {"07_emptySubject": subjectEntry([])})
    other = tmp_path / "somewhereElse"
    other.mkdir()

    out = runHook(
        "scoringGate.py",
        writeEvent(engagement / "scoring" / "07_emptySubject_scoring.md"),
        env={"CLAUDE_PROJECT_DIR": str(other)},
    )
    assert '"deny"' in out


def test_scoringGateLedgerWriteDeniesMissingCitedReview(tmp_path):
    makeEngagement(tmp_path, {})
    content = json.dumps({"subjects": {"01_x": {"evidence": [
        {"artefact": "reviews/09_ghost_review.md"},
    ]}}})
    out = runHook("scoringGate.py", writeEvent(tmp_path / "scoreLedger.json", content))
    assert '"deny"' in out
    assert "09_ghost_review.md" in out


# --- findingAuthorGate ------------------------------------------------------

def test_findingGateAllowsWithSayAndDoEvidence(tmp_path):
    makeEngagement(tmp_path, {
        "06_assessorCompetency": subjectEntry([
            {"artefact": "reviews/02_nlrTrackAssessmentProcedure_review.md"},
            {"artefact": "interviews/06_assessorCompetency_notes.md"},
        ]),
    })
    out = runHook("findingAuthorGate.py", writeEvent(tmp_path / "findings" / "06_assessorCompetency_finding.md"))
    assert '"allow"' in out


def test_findingGateAllowsWithSayEvidenceAndBothScoresSet(tmp_path):
    makeEngagement(tmp_path, {
        "06_assessorCompetency": subjectEntry(
            [{"artefact": "reviews/02_nlrTrackAssessmentProcedure_review.md"}],
            sayScore=2, doScore=1,
        ),
    })
    out = runHook("findingAuthorGate.py", writeEvent(tmp_path / "findings" / "06_assessorCompetency_finding.md"))
    assert '"allow"' in out


def test_findingGateDeniesWhenDoInputMissing(tmp_path):
    makeEngagement(tmp_path, {
        "06_assessorCompetency": subjectEntry([
            {"artefact": "reviews/02_nlrTrackAssessmentProcedure_review.md"},
        ]),
    })
    out = runHook("findingAuthorGate.py", writeEvent(tmp_path / "findings" / "06_assessorCompetency_finding.md"))
    assert '"deny"' in out
    assert "do input" in out


def test_findingGateDeniesSubjectWithNoEvidence(tmp_path):
    makeEngagement(tmp_path, {"06_assessorCompetency": subjectEntry([])})
    out = runHook("findingAuthorGate.py", writeEvent(tmp_path / "findings" / "06_assessorCompetency_finding.md"))
    assert '"deny"' in out
    assert "no evidence records" in out


def test_findingGateResolvesRootFromFilePath(tmp_path):
    engagement = tmp_path / "engagement"
    engagement.mkdir()
    makeEngagement(engagement, {"06_assessorCompetency": subjectEntry([])})
    other = tmp_path / "somewhereElse"
    other.mkdir()
    out = runHook(
        "findingAuthorGate.py",
        writeEvent(engagement / "findings" / "06_assessorCompetency_finding.md"),
        env={"CLAUDE_PROJECT_DIR": str(other)},
    )
    assert '"deny"' in out


# --- proseRules (against the real pack qaRules.yaml) -------------------------

def proseEnv() -> dict:
    return {"CLAUDE_PLUGIN_ROOT": str(PLUGIN_ROOT)}


def test_proseRulesFlagsPackSeedPattern(tmp_path):
    makeEngagement(tmp_path, {})
    content = "The register should be delivered within 6 months of award.\n"
    out = runHook(
        "proseRules.py",
        writeEvent(tmp_path / "findings" / "06_assessorCompetency_finding.md", content),
        env=proseEnv(),
    )
    assert "banned phrasing" in out
    assert "within 6 months" in out


def test_proseRulesAllowsSingleSentenceParagraph(tmp_path):
    makeEngagement(tmp_path, {})
    content = "The register exists.\n\nIt is maintained by the operator and audited annually.\n"
    out = runHook(
        "proseRules.py",
        writeEvent(tmp_path / "findings" / "06_assessorCompetency_finding.md", content),
        env=proseEnv(),
    )
    assert out == ""


def test_proseRulesUsesPackParagraphMaximum(tmp_path):
    """The pack declares maxParagraphSentences 6: five sentences pass,
    seven are flagged."""
    makeEngagement(tmp_path, {})
    five = " ".join(f"Sentence number {w} stands here." for w in ("one", "two", "three", "four", "five"))
    seven = " ".join(f"Sentence number {w} stands here." for w in ("one", "two", "three", "four", "five", "six", "seven"))

    outFive = runHook(
        "proseRules.py",
        writeEvent(tmp_path / "findings" / "06_assessorCompetency_finding.md", five + "\n"),
        env=proseEnv(),
    )
    assert "paragraph length" not in outFive

    outSeven = runHook(
        "proseRules.py",
        writeEvent(tmp_path / "findings" / "06_assessorCompetency_finding.md", seven + "\n"),
        env=proseEnv(),
    )
    assert "paragraph length" in outSeven
    assert "at most 6" in outSeven
