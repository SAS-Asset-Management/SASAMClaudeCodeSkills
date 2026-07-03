"""Adversarial tests for the YAML subset loader.

Happy paths cover the exact shapes the suite ships (engagement.yaml,
pack.yaml, chunker manifests); failure paths assert the loader errors loudly,
with line numbers, on anything outside the documented subset.
"""

from __future__ import annotations

import os

import pytest


# ---- happy paths against the shipped shapes --------------------------------

def test_engagement_fixture_shape(configLoader, fixturesDir):
    data = configLoader.loadYaml(
        os.path.join(fixturesDir, "acmeEngagement", "engagement.yaml")
    )
    assert data["engagement"]["client"] == "Acme Rail"
    assert data["engagement"]["code"] == "ACME-CYBER-2026"
    assert data["engagement"]["weeks"] == 6
    assert data["engagement"]["interviewCeiling"] == 8
    assert data["engagement"]["start"] == "2026-08-03"  # ISO date kept as string
    assert data["engagement"]["pluginVersion"] == "1.0.0"
    assert data["framework"]["pack"] == "acme-rail-governance"
    assert data["framework"]["rounding"] == "from-0.7"
    assert data["brand"]["bannedPhrasings"] == ["owner", "delivery horizon"]
    assert data["brand"]["citationFormat"] == "{standard} §{clause} (p{page})"
    assert data["deliverable"]["dashboard"] is True
    assert data["deliverable"]["benchmark"] == "none"


def test_pack_fixture_shape(configLoader, fixturesDir):
    pack = configLoader.loadYaml(
        os.path.join(
            fixturesDir, "acmeEngagement", "packs", "acme-rail-governance", "pack.yaml"
        )
    )
    assert pack["id"] == "acme-rail-governance"
    assert pack["version"] == "1.0.0"
    assert pack["scale"]["id"] == "iam-0-5"
    assert pack["scale"]["levels"]["0"] == "Innocent"
    assert pack["scale"]["levels"]["5"] == "Excellent"
    domains = pack["taxonomy"]["domains"]
    assert [d["id"] for d in domains] == ["D1", "D2"]
    assert domains[0]["subjects"] == ["01_governancePolicy", "02_riskRegister"]
    assert pack["calcPack"] is False
    assert pack["defaultWeights"] == {"directOverIndirect": 2.0, "highOverLow": 1.5}


def test_scalar_coercions(configLoader):
    data = configLoader.parseYamlText(
        "\n".join(
            [
                "count: 42",
                "ratio: 1.5",
                "flagOn: true",
                "flagOff: false",
                "nothing: null",
                "tilde: ~",
                'quoted: "hash # not a comment"',
                "single: 'kept as is'",
                "bare: plain words here",
                "isoDate: 2026-07-03",
                "inline: [1, 2.5, true, alpha, \"b, c\"]",
                "emptyList: []",
            ]
        )
    )
    assert data["count"] == 42
    assert data["ratio"] == 1.5
    assert data["flagOn"] is True and data["flagOff"] is False
    assert data["nothing"] is None and data["tilde"] is None
    assert data["quoted"] == "hash # not a comment"
    assert data["single"] == "kept as is"
    assert data["bare"] == "plain words here"
    assert data["isoDate"] == "2026-07-03"
    assert data["inline"] == [1, 2.5, True, "alpha", "b, c"]
    assert data["emptyList"] == []


def test_block_list_of_maps(configLoader):
    data = configLoader.parseYamlText(
        "\n".join(
            [
                "chunks:",
                "  - file: 001_intro.md",
                "    title: Introduction",
                "    startPage: 1",
                "    endPage: 3",
                "  - file: 002_scope.md",
                "    title: Scope",
                "    startPage: 4",
                "    endPage: 4",
            ]
        )
    )
    assert len(data["chunks"]) == 2
    assert data["chunks"][0] == {
        "file": "001_intro.md", "title": "Introduction", "startPage": 1, "endPage": 3
    }
    assert data["chunks"][1]["endPage"] == 4


def test_root_level_block_list(configLoader):
    data = configLoader.parseYamlText("- alpha\n- beta\n- 3\n")
    assert data == ["alpha", "beta", 3]


def test_comments_and_blank_lines(configLoader):
    data = configLoader.parseYamlText(
        "# leading comment\n\nkey: value  # trailing comment\n\nother: 2\n"
    )
    assert data == {"key": "value", "other": 2}


# ---- loud failures on anything outside the subset ---------------------------

@pytest.mark.parametrize(
    "text, fragment",
    [
        ("key: &anchor value", "anchor"),
        ("key: *alias", "anchor"),
        ("key: |\n  block text", "multiline"),
        ("key: >\n  folded text", "multiline"),
        ("key: {a: 1}", "flow map"),
        ("key: !!str tagged", "tag"),
        ("---\nkey: value", "multi document"),
    ],
)
def test_forbidden_constructs_fail_loudly(configLoader, text, fragment):
    with pytest.raises(ValueError) as excinfo:
        configLoader.parseYamlText(text, source="bad.yaml")
    message = str(excinfo.value)
    assert message.startswith("bad.yaml:1:")
    assert fragment in message


def test_tab_indentation_rejected_with_line_number(configLoader):
    with pytest.raises(ValueError) as excinfo:
        configLoader.parseYamlText("top:\n\tchild: 1", source="tabs.yaml")
    assert "tabs.yaml:2:" in str(excinfo.value)
    assert "tab" in str(excinfo.value)


def test_odd_indentation_rejected(configLoader):
    with pytest.raises(ValueError) as excinfo:
        configLoader.parseYamlText("top:\n   child: 1", source="odd.yaml")
    assert "odd.yaml:2:" in str(excinfo.value)


def test_duplicate_keys_rejected(configLoader):
    with pytest.raises(ValueError, match="duplicate key"):
        configLoader.parseYamlText("a: 1\na: 2")


def test_non_map_line_inside_map_rejected(configLoader):
    with pytest.raises(ValueError, match="key: value"):
        configLoader.parseYamlText("a: 1\njust some words")


# ---- loadEngagement and resolvePack -----------------------------------------

def test_load_engagement_missing_raises_clear_error(configLoader, tmp_path):
    with pytest.raises(FileNotFoundError, match="engagement.yaml"):
        configLoader.loadEngagement(str(tmp_path))


def _writeMinimalEngagement(repo, packId):
    (repo / "engagement.yaml").write_text(
        "engagement:\n  code: TEST-2026\nframework:\n  pack: " + packId + "\n",
        encoding="utf-8",
    )


def test_resolve_pack_prefers_local_overlay(configLoader, tmp_path):
    repo = tmp_path / "repo"
    plugin = tmp_path / "plugin"
    for base, marker in ((repo, "true"), (plugin, "false")):
        packDir = base / "packs" / "p1"
        packDir.mkdir(parents=True)
        (packDir / "pack.yaml").write_text(
            f"id: p1\nversion: 1.0.0\nlocalOverlay: {marker}\n", encoding="utf-8"
        )
    _writeMinimalEngagement(repo, "p1")

    packDir, pack = configLoader.resolvePack(str(repo), str(plugin))
    assert packDir == str(repo / "packs" / "p1")
    assert pack["localOverlay"] is True

    # Remove the overlay: the plugin copy must now win.
    (repo / "packs" / "p1" / "pack.yaml").unlink()
    packDir, pack = configLoader.resolvePack(str(repo), str(plugin))
    assert packDir == str(plugin / "packs" / "p1")
    assert pack["localOverlay"] is False


def test_resolve_pack_missing_everywhere(configLoader, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _writeMinimalEngagement(repo, "ghost-pack")
    with pytest.raises(FileNotFoundError, match="ghost-pack"):
        configLoader.resolvePack(str(repo), str(tmp_path / "plugin"))
