"""Generalised standard chunker for the maturity assessment suite.

Slices a governing standard PDF into per section markdown chunks plus an
INDEX.md routing table, driven by a manifest of page ranges. This script is
how each engagement generates its LOCAL standard chunks: the plugin never
ships a chunked standard — the pack carries only a README stub, and each
engagement runs this script against its licensed copy of the document,
writing the output into the engagement repo at packs/<packId>/standard/.

CLI:
    python3 chunker.py --pdf <path> --manifest <manifest.yaml> --out <dir>

The manifest is a YAML block list (parsed by engine/configLoader.py, so it
must stay within the supported subset) of rows shaped:

    - file: 001_introduction.md
      title: "Section 1 — Introduction"
      subtitle: "Purpose and scope"        # optional
      startPage: 6
      endPage: 8

Mechanism: pdftotext extracts the PDF to a temporary text file whose pages
are separated by form feed characters; each manifest row slices its page
range, writes a chunk with a heading block (title, subtitle, source page
range), and INDEX.md is generated as a routing table (chunk file, title,
page range, topics seeded from the titles).

External dependency: the ``pdftotext`` binary from poppler. Install with
``brew install poppler`` on macOS or ``apt install poppler-utils`` on Debian
and Ubuntu. The script fails with a clear message when it is missing.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

_ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))

_STOP_WORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "into", "of",
    "on", "or", "per", "section", "the", "to", "with",
}


def _loadConfigLoader():
    spec = importlib.util.spec_from_file_location(
        "maturityConfigLoader", os.path.join(_ENGINE_DIR, "configLoader.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _topicsFromTitle(title):
    words = re.findall(r"[A-Za-z][A-Za-z0-9]+", title)
    topics = []
    for word in words:
        lowered = word.lower()
        if lowered in _STOP_WORDS or lowered in topics:
            continue
        topics.append(lowered)
    return ", ".join(topics)


def _normaliseManifest(manifest, source):
    rows = manifest
    if isinstance(rows, dict):
        rows = rows.get("chunks")
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{source}: manifest must be a list of chunk rows (or a map with a 'chunks' list)")
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise ValueError(f"{source}: manifest row {index} is not a map")
        for field in ("file", "title", "startPage", "endPage"):
            if row.get(field) in (None, ""):
                raise ValueError(f"{source}: manifest row {index} is missing {field!r}")
        start, end = row["startPage"], row["endPage"]
        if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start:
            raise ValueError(
                f"{source}: manifest row {index} has an invalid page range {start!r} to {end!r}"
            )
    return rows


def _pageRangeLabel(start, end):
    return f"page {start}" if start == end else f"pages {start} to {end}"


def chunkText(rawText, manifest, sourceName="source.pdf", manifestSource="manifest"):
    """Slice form feed separated page text into chunk files plus INDEX.md.

    ``rawText`` is the pdftotext output (pages separated by form feeds);
    ``manifest`` is the parsed manifest list. Returns a dict mapping output
    file name to markdown content. Exposed separately from the CLI so tests
    can exercise the slicing without a PDF or poppler present.
    """
    rows = _normaliseManifest(manifest, manifestSource)
    pages = rawText.split("\f")
    pageCount = len(pages)

    outputs = {}
    indexRows = []
    for row in rows:
        start, end = row["startPage"], row["endPage"]
        if end > pageCount:
            raise ValueError(
                f"{manifestSource}: chunk {row['file']} wants pages up to {end} but the document has {pageCount}"
            )
        body = "\n\n".join(page.rstrip() for page in pages[start - 1 : end])
        heading = [f"# {row['title']}", ""]
        if row.get("subtitle"):
            heading.extend([f"*{row['subtitle']}*", ""])
        heading.extend([f"**Source:** `{sourceName}`, {_pageRangeLabel(start, end)}.", "", "---", ""])
        outputs[row["file"]] = "\n".join(heading) + f"\n{body}\n"
        indexRows.append((row["file"], row["title"], _pageRangeLabel(start, end), _topicsFromTitle(row["title"])))

    indexLines = [
        "# Standard chunk index",
        "",
        f"Routing table for the chunked standard. Source: `{sourceName}`.",
        "Generated locally for this engagement with engine/chunker.py; the chunks are not shipped with the pack.",
        "",
        "| Chunk | Title | Pages | Topics |",
        "| --- | --- | --- | --- |",
    ]
    for fileName, title, pageLabel, topics in indexRows:
        indexLines.append(f"| `{fileName}` | {title} | {pageLabel} | {topics} |")
    outputs["INDEX.md"] = "\n".join(indexLines) + "\n"
    return outputs


def extractPdfText(pdfPath):
    """Run pdftotext and return the raw form feed separated text."""
    if shutil.which("pdftotext") is None:
        sys.exit(
            "pdftotext not found. Install poppler first: 'brew install poppler' on macOS, "
            "or 'apt install poppler-utils' on Debian and Ubuntu."
        )
    with tempfile.TemporaryDirectory() as tmpDir:
        txtPath = os.path.join(tmpDir, "extracted.txt")
        subprocess.run(["pdftotext", pdfPath, txtPath], check=True)
        with open(txtPath, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Chunk a governing standard PDF into markdown sections.")
    parser.add_argument("--pdf", required=True, help="path to the licensed standard PDF")
    parser.add_argument("--manifest", required=True, help="YAML manifest of chunk page ranges")
    parser.add_argument("--out", required=True, help="output directory for the chunks and INDEX.md")
    args = parser.parse_args(argv)

    loader = _loadConfigLoader()
    manifest = loader.loadYaml(args.manifest)
    rawText = extractPdfText(args.pdf)
    outputs = chunkText(
        rawText,
        manifest,
        sourceName=os.path.basename(args.pdf),
        manifestSource=args.manifest,
    )

    os.makedirs(args.out, exist_ok=True)
    for fileName, content in outputs.items():
        with open(os.path.join(args.out, fileName), "w", encoding="utf-8") as handle:
            handle.write(content)
    print(f"Wrote {len(outputs) - 1} chunks plus INDEX.md to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
