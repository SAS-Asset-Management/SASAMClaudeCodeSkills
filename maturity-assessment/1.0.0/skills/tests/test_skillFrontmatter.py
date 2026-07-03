"""
Registration guards for the eight skill frontmatter blocks (OPT-02).

The road test saw two skills surface with no description in a live session.
The frontmatter proved valid — the drop traced to stale command copies — but
these tests pin the invariants that registration depends on: every SKILL.md
carries a name matching its directory, a nonempty single line description,
and a version, in a frontmatter block simple YAML parsers accept.

Run explicitly (the plugin pytest.ini testpaths cover engine and packs):
    python3 -m pytest skills/tests/
"""

from __future__ import annotations

from pathlib import Path

import pytest

SKILLS_DIR = Path(__file__).resolve().parents[1]
SKILL_FILES = sorted(SKILLS_DIR.glob("*/SKILL.md"))


def parseFrontmatter(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "---", f"{path}: frontmatter must open on line 1"
    fields = {}
    for line in lines[1:]:
        if line == "---":
            return fields
        key, sep, value = line.partition(": ")
        assert sep, f"{path}: continuation or non scalar line in frontmatter: {line!r}"
        assert key.strip() == key and " " not in key, f"{path}: bad key {key!r}"
        fields[key] = value
    raise AssertionError(f"{path}: frontmatter never closed")


def test_eight_skills_ship():
    assert len(SKILL_FILES) == 8


@pytest.mark.parametrize("skillFile", SKILL_FILES, ids=lambda p: p.parent.name)
def test_frontmatter_registers_cleanly(skillFile):
    fields = parseFrontmatter(skillFile)
    assert fields["name"] == skillFile.parent.name
    description = fields["description"]
    assert description.strip(), f"{skillFile}: empty description"
    assert len(description) < 1024
    assert "\t" not in description
    assert not description.lstrip().startswith(("#", "'", '"')), (
        f"{skillFile}: description opener risks YAML misparse"
    )
    assert fields["version"]


@pytest.mark.parametrize("skillFile", SKILL_FILES, ids=lambda p: p.parent.name)
def test_agent_fallback_guardrail_present(skillFile):
    body = skillFile.read_text(encoding="utf-8")
    assert "**Agent fallback.**" in body, (
        f"{skillFile}: missing the standard inline execution fallback guardrail"
    )
