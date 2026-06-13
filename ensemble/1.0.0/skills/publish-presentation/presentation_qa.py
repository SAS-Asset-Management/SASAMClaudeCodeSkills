#!/usr/bin/env python3
"""presentation_qa.py — warn-only brand/quality lints for a deck before publish.

Usage:
    presentation_qa.py <deck.html>

Prints findings, one per line, as "SEVERITY\tmessage". ALWAYS exits 0 — these are
advisory (the publish flow is warn-then-publish, never block). Checks:

  * Australian English   — flags clear American spellings in VISIBLE TEXT only
                           (parsed outside <script>/<style>, so CSS `color:` etc.
                           never false-positive).
  * SAS brand palette    — SAS blue #002244 / SAS green #69BE28 present somewhere.
  * SAS-AM tagline       — the mandated tagline appears on at least one slide.
  * Image alt text       — every <img> has an alt attribute (accessibility).
  * Slide count          — a reveal.js deck has a sane number of <section> slides.
  * Surviving local refs — href/src/url() pointing at LOCAL files (post-flatten
                           these would 404 on the portal). The key publish check.

stdlib only.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit

# American spelling -> the Australian form. Conservative: only unambiguous AmE forms
# that AU English spells differently. Matched whole-word, case-insensitive, in text.
AME = {
    "color": "colour",
    "colors": "colours",
    "behavior": "behaviour",
    "behaviors": "behaviours",
    "favor": "favour",
    "favorite": "favourite",
    "labor": "labour",
    "honor": "honour",
    "neighbor": "neighbour",
    "center": "centre",
    "centers": "centres",
    "fiber": "fibre",
    "meter": "metre",
    "liter": "litre",
    "defense": "defence",
    "offense": "offence",
    "catalog": "catalogue",
    "dialog": "dialogue",
    "gray": "grey",
    "organize": "organise",
    "organized": "organised",
    "organizing": "organising",
    "organization": "organisation",
    "organizations": "organisations",
    "recognize": "recognise",
    "recognized": "recognised",
    "optimize": "optimise",
    "optimized": "optimised",
    "optimization": "optimisation",
    "analyze": "analyse",
    "analyzed": "analysed",
    "analyzing": "analysing",
    "prioritize": "prioritise",
    "prioritized": "prioritised",
    "realize": "realise",
    "realized": "realised",
    "minimize": "minimise",
    "maximize": "maximise",
    "utilize": "utilise",
    "specialize": "specialise",
    "modeling": "modelling",
    "modeled": "modelled",
    "labeled": "labelled",
    "traveled": "travelled",
    "fulfill": "fulfil",
    "enrollment": "enrolment",
}

TAGLINE_MARKERS = ("strengths and weaknesses", "audit and benchmarking")
SAS_BLUE = "#002244"
SAS_GREEN = "#69be28"

_REMOTE = re.compile(r"^(?:[a-z][a-z0-9+.\-]*:|//|#|mailto:|tel:|data:)", re.I)
_TEMPLATE = re.compile(r"\{\{")


def is_remote(url: str) -> bool:
    u = (url or "").strip()
    return not u or bool(_TEMPLATE.search(u)) or bool(_REMOTE.match(u))


class _Text(HTMLParser):
    """Collect visible text — data outside <script>/<style>."""

    def __init__(self) -> None:
        super().__init__()
        self._skip = 0
        self.chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: object) -> None:
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self.chunks.append(data)


def visible_text(html: str) -> str:
    p = _Text()
    try:
        p.feed(html)
    except Exception:
        return ""
    return " ".join(p.chunks)


def local_refs(html: str) -> list[str]:
    refs: list[str] = []
    for m in re.finditer(r"\b(?:href|src)\s*=\s*(['\"])(.*?)\1", html, re.I):
        refs.append(m.group(2))
    for m in re.finditer(r"""url\(\s*(['\"]?)([^)'\"]+)\1\s*\)""", html):
        refs.append(m.group(2))
    out: list[str] = []
    seen: set[str] = set()
    for r in refs:
        if is_remote(r):
            continue
        key = urlsplit(r.strip()).path
        if key and key not in seen:
            seen.add(key)
            out.append(r.strip())
    return out


def run(html: str) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    low = html.lower()
    text = visible_text(html)

    # Australian English (visible text only)
    hits: list[str] = []
    for ame, aue in AME.items():
        if re.search(rf"\b{re.escape(ame)}\b", text, re.I):
            hits.append(f"{ame}→{aue}")
    if hits:
        shown = ", ".join(sorted(set(hits))[:8])
        more = "" if len(set(hits)) <= 8 else f" (+{len(set(hits)) - 8} more)"
        findings.append(
            ("WARN", f"American spellings in text: {shown}{more}. Use Australian English.")
        )

    # Brand palette
    if SAS_BLUE not in low and SAS_GREEN not in low:
        findings.append(
            ("WARN", f"SAS brand palette not detected ({SAS_BLUE} / {SAS_GREEN.upper()}).")
        )

    # Tagline
    if not any(marker in low for marker in TAGLINE_MARKERS):
        findings.append(
            ("WARN", "SAS-AM tagline not found — it should appear on at least one slide.")
        )

    # Image alt text
    imgs = re.findall(r"<img\b[^>]*>", html, re.I)
    no_alt = [t for t in imgs if not re.search(r"\balt\s*=", t, re.I)]
    if no_alt:
        findings.append(
            (
                "WARN",
                f"{len(no_alt)} of {len(imgs)} <img> tags have no alt attribute (accessibility).",
            )
        )

    # Slide count (reveal.js sections)
    sections = len(re.findall(r"<section\b", html, re.I))
    if sections == 0:
        findings.append(("WARN", "No <section> slides detected — is this a reveal.js deck?"))
    elif sections > 80:
        findings.append(("INFO", f"{sections} slides — unusually large for a conference deck."))

    # Surviving local refs (would 404 on the portal)
    locals_ = local_refs(html)
    if locals_:
        shown = ", ".join(locals_[:6])
        more = "" if len(locals_) <= 6 else f" (+{len(locals_) - 6} more)"
        findings.append(
            (
                "WARN",
                f"{len(locals_)} local asset ref(s) will 404 on the portal: {shown}{more}. "
                "Flatten could not inline them — embed or remove.",
            )
        )
    return findings


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: presentation_qa.py <deck.html>", file=sys.stderr)
        return 0  # warn-only tool: never fail the publish on usage
    try:
        html = open(argv[1], encoding="utf-8", errors="replace").read()
    except OSError as exc:
        print(f"INFO\tQA could not read the deck ({exc}).")
        return 0
    findings = run(html)
    if not findings:
        print("OK\tQA: no issues found.")
    else:
        for sev, msg in findings:
            print(f"{sev}\t{msg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
