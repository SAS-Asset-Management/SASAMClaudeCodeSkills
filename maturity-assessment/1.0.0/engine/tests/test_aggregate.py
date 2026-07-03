"""Adversarial tests for the aggregation and confidence engine.

The weighting and rounding maths are re encoded here as independent local
helper functions (never imported from the module under test), and the module
loaded via importlib is cross checked against them — the same discipline the
calc validator applies to calcPack engines.
"""

from __future__ import annotations

import json
import math
import os

import pytest

# ---- independent reference encoding of the contract maths -------------------

def _refTagWeight(tag, directOverIndirect):
    if tag == "Direct":
        return directOverIndirect
    if tag == "Indirect":
        return 1.0
    return None  # tag None carries no scoring weight


def _refConfWeight(confidence, highOverLow):
    return {"High": highOverLow, "Medium": 1.0, "Low": 1.0 / highOverLow}[confidence]


def _refMean(records, directOverIndirect, highOverLow):
    pairs = []
    for tag, level, confidence in records:
        tagWeight = _refTagWeight(tag, directOverIndirect)
        if tagWeight is None:
            continue
        pairs.append((tagWeight * _refConfWeight(confidence, highOverLow), level))
    total = sum(w for w, _ in pairs)
    return sum(w * x for w, x in pairs) / total


def _refRoundFrom07(mean):
    frac = round(mean - math.floor(mean), 9)
    return int(math.ceil(mean)) if frac > 0.7 else int(math.floor(mean))


def _refFlag(score):
    if score < 2:
        return "lowOutlier"
    if score > 4:
        return "highOutlier"
    return None


# ---- rounding rule boundary battery -----------------------------------------

@pytest.mark.parametrize(
    "mean, expected",
    [
        (0.7, 0),            # exact boundary rounds down
        (0.700000001, 1),    # strictly greater rounds up
        (1.70, 1),           # the documented example, down
        (1.71, 2),           # the documented example, up
        (1.69, 1),
        (4.71, 5),
        (2.0, 2),            # integral mean is untouched
        (0.0, 0),
        (5.0, 5),
    ],
)
def test_round_from_07_boundaries(aggregate, mean, expected):
    assert aggregate.roundFrom07(mean) == expected
    assert _refRoundFrom07(mean) == expected  # reference agrees with itself


@pytest.mark.parametrize("score, flag", [(0, "lowOutlier"), (1, "lowOutlier"), (2, None), (4, None), (5, "highOutlier")])
def test_flag_for(aggregate, score, flag):
    assert aggregate.flagFor(score) == flag
    assert _refFlag(score) == flag


# ---- computeSubject cross checked against the reference ----------------------

CROSS_CHECK_CASES = [
    # (records as (tag, level, confidence), directOverIndirect, highOverLow)
    ([("Direct", 3, "High"), ("Indirect", 2, "Medium")], 2.0, 1.5),
    ([("Direct", 4, "Low"), ("Indirect", 1, "High"), ("Indirect", 3, "Medium")], 2.0, 1.5),
    ([("Indirect", 0, "Low")], 3.0, 2.0),
    ([("Direct", 5, "High"), ("Direct", 5, "High"), ("Indirect", 4, "Low")], 1.5, 4.0),
    ([("None", 5, "High"), ("Indirect", 2, "Medium")], 2.0, 1.5),
]


@pytest.mark.parametrize("records, direct, high", CROSS_CHECK_CASES)
def test_compute_subject_matches_reference(aggregate, records, direct, high):
    evidence = [
        {"artefact": "reviews/01_x_review.md", "tag": tag, "rubricLevel": level,
         "rubricQuote": "quote", "confidence": confidence}
        for tag, level, confidence in records
    ]
    score, confidence, ci = aggregate.computeSubject(evidence, direct, high)
    expectedMean = _refMean(records, direct, high)
    assert score == _refRoundFrom07(expectedMean)
    assert ci[0] <= round(expectedMean, 4) <= ci[1]
    assert 0.0 <= ci[0] <= ci[1] <= 5.0
    assert confidence in ("Low", "Medium", "High")


def test_tag_none_excluded_entirely(aggregate):
    evidence = [
        {"tag": "None", "rubricLevel": 5, "confidence": "High"},
        {"tag": "Indirect", "rubricLevel": 2, "confidence": "Medium"},
    ]
    score, confidence, ci = aggregate.computeSubject(evidence, 2.0, 1.5)
    assert score == 2
    assert ci == [2.0, 2.0]  # a single weighted record gives ci = [mean, mean]


def test_only_none_tags_yield_no_score(aggregate):
    evidence = [{"tag": "None", "rubricLevel": 4, "confidence": "High"}]
    assert aggregate.computeSubject(evidence, 2.0, 1.5) is None
    assert aggregate.computeSubject([], 2.0, 1.5) is None


def test_single_record_ci_collapses_to_mean(aggregate):
    evidence = [{"tag": "Direct", "rubricLevel": 4, "confidence": "High"}]
    score, _, ci = aggregate.computeSubject(evidence, 2.0, 1.5)
    assert score == 4
    assert ci == [4.0, 4.0]


def test_ci_clamped_to_scale(aggregate):
    evidence = [
        {"tag": "Direct", "rubricLevel": 5, "confidence": "Low"},
        {"tag": "Indirect", "rubricLevel": 0, "confidence": "Low"},
    ]
    _, _, ci = aggregate.computeSubject(evidence, 2.0, 1.5)
    assert ci[0] >= 0.0 and ci[1] <= 5.0


# ---- end to end boundary battery through a real repo -------------------------

def _writeRepo(tmp_path, directOverIndirect, evidenceByLevel):
    """Build a one subject engagement repo whose weighted mean is exact."""
    repo = tmp_path / "repo"
    packDir = repo / "packs" / "test-pack"
    packDir.mkdir(parents=True)
    (repo / "engagement.yaml").write_text(
        "\n".join(
            [
                "engagement:",
                "  client: \"Acme Rail\"",
                "  code: ACME-CYBER-2026",
                "framework:",
                "  pack: test-pack",
                "  aggregationWeights:",
                f"    directOverIndirect: {directOverIndirect}",
                "    highOverLow: 1.5",
                "  rounding: from-0.7",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (packDir / "pack.yaml").write_text(
        "\n".join(
            [
                "id: test-pack",
                "version: 1.0.0",
                "scale:",
                "  id: iam-0-5",
                "taxonomy:",
                "  domains:",
                "    - id: D1",
                "      name: Only",
                "      subjects: [01_onlySubject]",
                "defaultWeights:",
                "  directOverIndirect: 2.0",
                "  highOverLow: 1.5",
                "",
            ]
        ),
        encoding="utf-8",
    )
    evidence = [
        {"artefact": "reviews/01_a_review.md", "tag": tag, "rubricLevel": level,
         "rubricQuote": "quote", "confidence": "Medium"}
        for tag, level in evidenceByLevel
    ]
    ledger = {
        "engagement": "ACME-CYBER-2026",
        "pack": "test-pack@1.0.0",
        "scale": "iam-0-5",
        "runs": [],
        "subjects": {
            "01_onlySubject": {
                "final": {"score": None, "confidence": None, "ci": None},
                "sayScore": None, "doScore": None,
                "evidence": evidence, "history": [], "flag": None, "disputes": [],
            }
        },
    }
    (repo / "scoreLedger.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    return repo


@pytest.mark.parametrize(
    "directOverIndirect, indirectCount, directLevel, indirectLevel, expectedScore, expectedFlag",
    [
        # mean = (direct*level + count*level) / (direct + count) with Medium confidence
        (70.0, 30, 2, 1, 1, "lowOutlier"),   # mean 1.70 exactly: rounds DOWN
        (71.0, 29, 2, 1, 2, None),            # mean 1.71: rounds UP
        (69.0, 31, 2, 1, 1, "lowOutlier"),   # mean 1.69
        (71.0, 29, 5, 4, 5, "highOutlier"),  # mean 4.71: rounds up and flags high
    ],
)
def test_end_to_end_rounding_and_flags(
    aggregate, tmp_path, directOverIndirect, indirectCount, directLevel, indirectLevel,
    expectedScore, expectedFlag,
):
    records = [("Direct", directLevel)] + [("Indirect", indirectLevel)] * indirectCount
    repo = _writeRepo(tmp_path, directOverIndirect, records)
    # Independent expectation from the reference encoding.
    refRecords = [(tag, level, "Medium") for tag, level in records]
    expectedMean = _refMean(refRecords, directOverIndirect, 1.5)
    assert _refRoundFrom07(expectedMean) == expectedScore

    aggregate.runAggregation(str(repo), today="2026-01-15", pluginRoot=str(tmp_path / "noPlugin"))
    ledger = json.loads((repo / "scoreLedger.json").read_text())
    subject = ledger["subjects"]["01_onlySubject"]
    assert subject["final"]["score"] == expectedScore
    assert subject["flag"] == expectedFlag


# ---- golden fixture: byte for byte determinism --------------------------------

def test_golden_fixture_byte_for_byte(aggregate, acmeRepo, fixturesDir):
    aggregate.runAggregation(acmeRepo, today="2026-01-15", pluginRoot=os.path.join(acmeRepo, "noPlugin"))
    produced = open(os.path.join(acmeRepo, "scoreLedger.json"), "rb").read()
    expected = open(os.path.join(fixturesDir, "expectedScoreLedger.json"), "rb").read()
    assert produced == expected


def test_second_run_is_byte_identical_and_appends_nothing(aggregate, acmeRepo):
    changed = aggregate.runAggregation(acmeRepo, today="2026-01-15", pluginRoot="/nonexistent")
    assert changed is True
    first = open(os.path.join(acmeRepo, "scoreLedger.json"), "rb").read()
    changed = aggregate.runAggregation(acmeRepo, today="2026-01-15", pluginRoot="/nonexistent")
    assert changed is False
    second = open(os.path.join(acmeRepo, "scoreLedger.json"), "rb").read()
    assert first == second
    ledger = json.loads(second)
    assert len(ledger["runs"]) == 1
    assert len(ledger["subjects"]["01_governancePolicy"]["history"]) == 1


def test_missing_evidence_leaves_final_null(aggregate, acmeRepo):
    aggregate.runAggregation(acmeRepo, today="2026-01-15", pluginRoot="/nonexistent")
    ledger = json.loads(open(os.path.join(acmeRepo, "scoreLedger.json")).read())
    subject = ledger["subjects"]["03_assetData"]
    assert subject["final"] == {"score": None, "confidence": None, "ci": None}
    assert subject["flag"] is None
    assert subject["history"] == []


def test_history_appends_on_change_with_direction(aggregate, acmeRepo):
    aggregate.runAggregation(acmeRepo, today="2026-01-15", pluginRoot="/nonexistent")
    path = os.path.join(acmeRepo, "scoreLedger.json")
    ledger = json.loads(open(path).read())
    subject = ledger["subjects"]["02_riskRegister"]
    assert subject["history"][-1]["driver"].startswith("sets initial score 1")
    # New strong evidence lands: the score must lift and say so in the driver.
    subject["evidence"].append(
        {"artefact": "reviews/05_riskCommitteePapers_review.md", "tag": "Direct",
         "rubricLevel": 4, "rubricQuote": "Risks are reviewed on a defined cycle.",
         "confidence": "High"}
    )
    open(path, "w").write(json.dumps(ledger, indent=2) + "\n")
    aggregate.runAggregation(
        acmeRepo, trigger="interview evidence landed", today="2026-01-16", pluginRoot="/nonexistent"
    )
    ledger = json.loads(open(path).read())
    subject = ledger["subjects"]["02_riskRegister"]
    assert len(subject["history"]) == 2
    latest = subject["history"][-1]
    assert latest["run"] == 2
    assert latest["score"] > 1
    assert latest["driver"].startswith("lifts from 1 to")
    assert "interview evidence landed" in latest["driver"]
    assert ledger["runs"][-1] == {
        "run": 2, "date": "2026-01-16", "trigger": "interview evidence landed"
    }


def test_engine_never_deletes_agent_owned_fields(aggregate, acmeRepo):
    path = os.path.join(acmeRepo, "scoreLedger.json")
    ledger = json.loads(open(path).read())
    ledger["subjects"]["01_governancePolicy"]["disputes"].append(
        {"id": "DSP-01", "raised": "2026-01-10", "description": "Assessee disputes the level",
         "status": "resolved", "resolution": "Evidence reconfirmed at level 3"}
    )
    open(path, "w").write(json.dumps(ledger, indent=2) + "\n")
    aggregate.runAggregation(acmeRepo, today="2026-01-15", pluginRoot="/nonexistent")
    ledger = json.loads(open(path).read())
    subject = ledger["subjects"]["01_governancePolicy"]
    assert subject["sayScore"] == 2 and subject["doScore"] == 3
    assert len(subject["evidence"]) == 2
    assert subject["disputes"][0]["id"] == "DSP-01"
