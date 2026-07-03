"""Tests for the standard chunker.

The slicing logic is exercised through chunkText with a pre made form feed
text fixture, so no PDF or poppler install is needed. The full pdftotext
path runs only when the binary is present, against a minimal hand rolled PDF.
"""

from __future__ import annotations

import os
import shutil

import pytest

RAW_TEXT = "\f".join(
    [
        "Page one: purpose of the standard.",
        "Page two: definitions.",
        "Page three: requirement REQ-04.7-01 shall apply.",
        "Page four: data supply obligations.",
        "Page five: appendix.",
    ]
)

MANIFEST = [
    {"file": "001_introduction.md", "title": "Section 1 — Introduction",
     "subtitle": "Purpose and definitions", "startPage": 1, "endPage": 2},
    {"file": "002_requirements.md", "title": "Section 2 — Requirements",
     "startPage": 3, "endPage": 3},
    {"file": "003_dataSupply.md", "title": "Section 3 — Data Supply",
     "startPage": 4, "endPage": 5},
]


def test_chunk_slicing_by_page_range(chunker):
    outputs = chunker.chunkText(RAW_TEXT, MANIFEST, sourceName="standard.pdf")
    intro = outputs["001_introduction.md"]
    assert "Page one" in intro and "Page two" in intro
    assert "Page three" not in intro
    assert "# Section 1 — Introduction" in intro
    assert "*Purpose and definitions*" in intro
    assert "pages 1 to 2" in intro
    assert "`standard.pdf`" in intro

    requirements = outputs["002_requirements.md"]
    assert "Page three" in requirements
    assert "Page two" not in requirements and "Page four" not in requirements
    assert "page 3" in requirements  # single page label, no range

    supply = outputs["003_dataSupply.md"]
    assert "Page four" in supply and "Page five" in supply


def test_index_routing_table(chunker):
    outputs = chunker.chunkText(RAW_TEXT, MANIFEST, sourceName="standard.pdf")
    index = outputs["INDEX.md"]
    assert "| Chunk | Title | Pages | Topics |" in index
    assert "`001_introduction.md`" in index
    assert "pages 4 to 5" in index
    # Topics are seeded from titles, lowercased, stop words removed.
    assert "introduction" in index
    assert "requirements" in index
    assert "generated locally" in index.lower()


def test_manifest_accepts_chunks_map_wrapper(chunker):
    outputs = chunker.chunkText(RAW_TEXT, {"chunks": MANIFEST})
    assert "INDEX.md" in outputs and len(outputs) == 4


@pytest.mark.parametrize(
    "row, fragment",
    [
        ({"file": "x.md", "title": "T", "startPage": 1}, "endPage"),
        ({"file": "x.md", "title": "T", "startPage": 0, "endPage": 1}, "invalid page range"),
        ({"file": "x.md", "title": "T", "startPage": 3, "endPage": 2}, "invalid page range"),
        ({"file": "x.md", "title": "T", "startPage": 1, "endPage": 99}, "has 5"),
    ],
)
def test_bad_manifest_rows_fail_loudly(chunker, row, fragment):
    with pytest.raises(ValueError) as excinfo:
        chunker.chunkText(RAW_TEXT, [row])
    assert fragment in str(excinfo.value)


def test_manifest_must_be_a_list(chunker):
    with pytest.raises(ValueError, match="list of chunk rows"):
        chunker.chunkText(RAW_TEXT, {"notChunks": []})


def test_yaml_manifest_round_trip(chunker, configLoader, tmp_path):
    manifestPath = tmp_path / "manifest.yaml"
    manifestPath.write_text(
        "\n".join(
            [
                "- file: 001_introduction.md",
                "  title: \"Section 1 — Introduction\"",
                "  subtitle: \"Purpose and definitions\"",
                "  startPage: 1",
                "  endPage: 2",
                "- file: 002_requirements.md",
                "  title: \"Section 2 — Requirements\"",
                "  startPage: 3",
                "  endPage: 3",
                "",
            ]
        ),
        encoding="utf-8",
    )
    manifest = configLoader.loadYaml(str(manifestPath))
    outputs = chunker.chunkText(RAW_TEXT, manifest)
    assert set(outputs) == {"001_introduction.md", "002_requirements.md", "INDEX.md"}


# ---- full CLI path, only when poppler is installed ----------------------------

_MINIMAL_PDF = b"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length 60 >> stream
BT /F1 24 Tf 72 700 Td (Acme standard chunk test) Tj ET
endstream endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
trailer << /Root 1 0 R >>
"""


@pytest.mark.skipif(shutil.which("pdftotext") is None, reason="pdftotext (poppler) not installed")
def test_cli_end_to_end_with_pdftotext(chunker, tmp_path):
    pdfPath = tmp_path / "standard.pdf"
    pdfPath.write_bytes(_MINIMAL_PDF)
    manifestPath = tmp_path / "manifest.yaml"
    manifestPath.write_text(
        "- file: 001_all.md\n  title: \"Section 1 — All\"\n  startPage: 1\n  endPage: 1\n",
        encoding="utf-8",
    )
    outDir = tmp_path / "standard"
    rc = chunker.main(
        ["--pdf", str(pdfPath), "--manifest", str(manifestPath), "--out", str(outDir)]
    )
    assert rc == 0
    chunk = (outDir / "001_all.md").read_text()
    assert "Acme standard chunk test" in chunk
    assert (outDir / "INDEX.md").is_file()
