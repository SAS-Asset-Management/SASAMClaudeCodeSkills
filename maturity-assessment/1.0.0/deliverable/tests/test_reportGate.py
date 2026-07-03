"""Unit tests for reportGate.evaluateGate over synthetic dicts."""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))

ALL_SUBJECTS = ["01_alpha", "02_beta", "03_gamma"]


def _loadModule(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


reportGate = _loadModule(
    "reportGateUnderTest", os.path.join(HERE, os.pardir, "reportGate.py")
)


def makePack():
    return {
        "id": "acme-governance",
        "taxonomy": {
            "domains": [
                {"id": "D1", "name": "Strategy", "subjects": ["01_alpha", "02_beta"]},
                {"id": "D2", "name": "Delivery", "subjects": ["03_gamma"]},
            ]
        },
    }


def makeSubject(score=3, sayScore=2, doScore=3, disputes=None):
    return {
        "final": {"score": score, "confidence": "High", "ci": [score, score] if score is not None else None},
        "sayScore": sayScore,
        "doScore": doScore,
        "evidence": [],
        "history": [],
        "flag": None,
        "disputes": disputes or [],
    }


def makeLedger():
    return {
        "engagement": "ACME-CYBER-2026",
        "pack": "acme-governance@1.0.0",
        "scale": "iam-0-5",
        "runs": [],
        "subjects": {
            "01_alpha": makeSubject(),
            "02_beta": makeSubject(score=2, sayScore=None, doScore=None),
            "03_gamma": makeSubject(score=4),
        },
    }


def makeFindingsRepo(tmp_path, subjectIds=ALL_SUBJECTS, run="run01"):
    """Create an engagement root whose findings/<run>/ carries a
    reconciled finding for each subject id given."""
    runDir = tmp_path / "findings" / run
    runDir.mkdir(parents=True, exist_ok=True)
    for subjectId in subjectIds:
        (runDir / "{}_finding.md".format(subjectId)).write_text(
            "# finding\n", encoding="utf-8"
        )
    return str(tmp_path)


def test_signatureAndShape(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path)
    verdict = reportGate.evaluateGate(makeLedger(), makePack(), repoRoot)
    assert set(verdict.keys()) == {"open", "reasons"}
    assert isinstance(verdict["open"], bool)
    assert isinstance(verdict["reasons"], list)


def test_completeLedgerOpensGate(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path)
    verdict = reportGate.evaluateGate(makeLedger(), makePack(), repoRoot)
    assert verdict["open"] is True
    assert verdict["reasons"] == []


def test_missingSubjectClosesGate(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path)
    ledger = makeLedger()
    del ledger["subjects"]["03_gamma"]
    verdict = reportGate.evaluateGate(ledger, makePack(), repoRoot)
    assert verdict["open"] is False
    assert any(
        "03_gamma" in reason and "missing" in reason
        for reason in verdict["reasons"]
    )


def test_nullFinalScoreClosesGate(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path)
    ledger = makeLedger()
    ledger["subjects"]["02_beta"]["final"]["score"] = None
    verdict = reportGate.evaluateGate(ledger, makePack(), repoRoot)
    assert verdict["open"] is False
    assert any(
        "02_beta" in reason and "final.score" in reason
        for reason in verdict["reasons"]
    )


def test_halfSetSayScoreClosesGate(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path)
    ledger = makeLedger()
    ledger["subjects"]["01_alpha"]["doScore"] = None
    verdict = reportGate.evaluateGate(ledger, makePack(), repoRoot)
    assert verdict["open"] is False
    assert any(
        "01_alpha" in reason and "doScore" in reason
        for reason in verdict["reasons"]
    )


def test_halfSetDoScoreClosesGate(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path)
    ledger = makeLedger()
    ledger["subjects"]["01_alpha"]["sayScore"] = None
    verdict = reportGate.evaluateGate(ledger, makePack(), repoRoot)
    assert verdict["open"] is False
    assert any(
        "01_alpha" in reason and "sayScore" in reason
        for reason in verdict["reasons"]
    )


def test_openDisputeClosesGate(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path)
    ledger = makeLedger()
    ledger["subjects"]["03_gamma"]["disputes"] = [
        {
            "id": "DSP-07",
            "raised": "2026-06-10",
            "description": "weighting disagreement",
            "status": "open",
            "resolution": None,
        }
    ]
    verdict = reportGate.evaluateGate(ledger, makePack(), repoRoot)
    assert verdict["open"] is False
    assert any(
        "03_gamma" in reason and "DSP-07" in reason
        for reason in verdict["reasons"]
    )


def test_resolvedDisputeDoesNotCloseGate(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path)
    ledger = makeLedger()
    ledger["subjects"]["03_gamma"]["disputes"] = [
        {
            "id": "DSP-08",
            "raised": "2026-06-10",
            "description": "resolved disagreement",
            "status": "resolved",
            "resolution": "assessor ruling accepted",
        }
    ]
    verdict = reportGate.evaluateGate(ledger, makePack(), repoRoot)
    assert verdict["open"] is True


def test_everyFailureIsListed(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path)
    ledger = makeLedger()
    del ledger["subjects"]["03_gamma"]
    ledger["subjects"]["01_alpha"]["doScore"] = None
    ledger["subjects"]["02_beta"]["final"]["score"] = None
    ledger["subjects"]["02_beta"]["disputes"] = [
        {"id": "DSP-09", "raised": "2026-06-12", "description": "x", "status": "open", "resolution": None}
    ]
    verdict = reportGate.evaluateGate(ledger, makePack(), repoRoot)
    assert verdict["open"] is False
    assert len(verdict["reasons"]) == 4


def test_noFindingsDirectoryClosesGateNamingEverySubject(tmp_path):
    verdict = reportGate.evaluateGate(
        makeLedger(), makePack(), str(tmp_path)
    )
    assert verdict["open"] is False
    for subjectId in ALL_SUBJECTS:
        assert any(
            subjectId in reason and "no findings run directory" in reason
            for reason in verdict["reasons"]
        )


def test_noRepoRootClosesGate():
    verdict = reportGate.evaluateGate(makeLedger(), makePack())
    assert verdict["open"] is False
    assert any(
        "no findings run directory" in reason
        for reason in verdict["reasons"]
    )


def test_missingFindingNamesOnlyThatSubject(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path, ["01_alpha", "02_beta"])
    verdict = reportGate.evaluateGate(makeLedger(), makePack(), repoRoot)
    assert verdict["open"] is False
    assert verdict["reasons"] == [
        "03_gamma: no reconciled finding in findings/run01 and no waiver "
        "is recorded"
    ]


def test_waiverOpensGateWithoutFinding(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path, ["01_alpha", "02_beta"])
    ledger = makeLedger()
    ledger["subjects"]["03_gamma"]["waiver"] = (
        "descoped by client agreement, 2026-06-20"
    )
    verdict = reportGate.evaluateGate(ledger, makePack(), repoRoot)
    assert verdict["open"] is True
    assert verdict["reasons"] == []


def test_blankWaiverDoesNotCount(tmp_path):
    repoRoot = makeFindingsRepo(tmp_path, ["01_alpha", "02_beta"])
    ledger = makeLedger()
    ledger["subjects"]["03_gamma"]["waiver"] = "   "
    verdict = reportGate.evaluateGate(ledger, makePack(), repoRoot)
    assert verdict["open"] is False


def test_latestRunDirectoryGoverns(tmp_path):
    makeFindingsRepo(tmp_path, ALL_SUBJECTS, run="run01")
    repoRoot = makeFindingsRepo(tmp_path, ["01_alpha"], run="run02")
    verdict = reportGate.evaluateGate(makeLedger(), makePack(), repoRoot)
    assert verdict["open"] is False
    assert any(
        "02_beta" in reason and "findings/run02" in reason
        for reason in verdict["reasons"]
    )
    assert any(
        "03_gamma" in reason and "findings/run02" in reason
        for reason in verdict["reasons"]
    )
