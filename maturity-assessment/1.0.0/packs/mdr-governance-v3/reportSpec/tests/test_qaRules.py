"""
Doctrine tests for the mdr-governance-v3 QA battery (reportSpec/qaRules.yaml).

qaRules.yaml is configuration the report QA gate executes, so its content is
behaviour: these tests pin the no owners doctrine — recommendations name the
capability or process they act on, never a person or role as an accountable
party — and confirm the file stays inside the engine's YAML subset.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPORT_SPEC_DIR = Path(__file__).resolve().parents[1]
ENGINE_DIR = REPORT_SPEC_DIR.parents[2] / "engine"


@pytest.fixture(scope="module")
def qaRules():
    spec = importlib.util.spec_from_file_location(
        "configLoader", ENGINE_DIR / "configLoader.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.loadYaml(str(REPORT_SPEC_DIR / "qaRules.yaml"))


def test_qa_rules_parse_within_yaml_subset(qaRules):
    assert isinstance(qaRules["bannedPhrasings"], list)
    for entry in qaRules["bannedPhrasings"]:
        assert entry["concept"]
        assert entry["rationale"]
        assert isinstance(entry["seedPatterns"], list) and entry["seedPatterns"]


def test_no_rationale_demands_an_owner(qaRules):
    """The settled doctrine: recommendations carry no owners. No QA rule may
    demand that a recommendation name a responsible person, role, or client
    function as an accountable party."""
    ownerDemands = [
        "responsible client function",
        "names the owner",
        "the action and the owner",
        "accountable owner",
    ]
    for entry in qaRules["bannedPhrasings"]:
        rationale = entry["rationale"].lower()
        for phrase in ownerDemands:
            assert phrase not in rationale, (
                f"concept {entry['concept']!r} contradicts the no owners "
                f"doctrine: {entry['rationale']!r}"
            )


def test_recommendation_concept_states_the_doctrine(qaRules):
    rationales = " ".join(
        entry["rationale"] for entry in qaRules["bannedPhrasings"]
    )
    assert "never a person or role as an accountable party" in rationales
