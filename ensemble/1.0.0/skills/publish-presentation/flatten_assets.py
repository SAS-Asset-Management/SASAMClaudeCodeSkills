#!/usr/bin/env python3
"""flatten_assets.py — inline a deck's LOCAL assets into one self-contained HTML.

Usage:
    flatten_assets.py <deck.html> <out.html>

The contentLibrary publish API (`POST /api/presentations/create`) stores exactly
ONE file per deck, so a presentation must be a single self-contained HTML to render
correctly on the portal. This reads <deck.html> and inlines its LOCAL assets:

  * <link rel="stylesheet" href="LOCAL">  -> <style>…</style> (with the CSS's own
    url(...) font/image refs inlined as data: URIs, resolved next to the CSS file)
  * <script src="LOCAL">                  -> inline <script>…</script>
  * <img src="LOCAL">                     -> src="data:…"
  * url(LOCAL) in <style> blocks / style="" -> data: URI

Remote refs (http(s)://, protocol-relative //, data:, mailto:/tel:, #fragments and
{{template}} placeholders) are left untouched — sas-presentation decks load reveal.js
and fonts from a CDN, which must stay remote. Missing or unreadable local refs are
left in place and reported (they would 404 on the portal — presentation_qa flags them).

Writes the flattened HTML to <out.html> and prints a JSON report to stdout. stdlib only.
"""

from __future__ import annotations

import base64
import json
import mimetypes
import os
import re
import sys
from urllib.parse import unquote, urlsplit

# Fonts/Images the stdlib mimetypes table can miss — register so data: URIs are typed.
for _ext, _mime in (
    (".woff2", "font/woff2"),
    (".woff", "font/woff"),
    (".ttf", "font/ttf"),
    (".otf", "font/otf"),
    (".svg", "image/svg+xml"),
    (".webp", "image/webp"),
):
    mimetypes.add_type(_mime, _ext)

_REMOTE = re.compile(r"^(?:[a-z][a-z0-9+.\-]*:|//|#|mailto:|tel:)", re.I)
_TEMPLATE = re.compile(r"\{\{")

report: dict[str, list[str] | int] = {"inlined": [], "skipped": [], "remote_kept": 0}


def _inlined(kind: str, url: str) -> None:
    report["inlined"].append(f"{kind}:{url}")  # type: ignore[union-attr]


def _skipped(kind: str, url: str, why: str) -> None:
    report["skipped"].append(f"{kind}:{url} ({why})")  # type: ignore[union-attr]


def is_remote(url: str) -> bool:
    u = (url or "").strip()
    if not u:
        return True
    if _TEMPLATE.search(u) or u.startswith("data:"):
        return True
    return bool(_REMOTE.match(u))


def local_path(base: str, url: str) -> str | None:
    """Resolve a local ref to an existing absolute file path, or None."""
    if is_remote(url):
        return None
    path = unquote(urlsplit(url.strip()).path)
    if not path:
        return None
    cand = os.path.normpath(os.path.join(base, path))
    return cand if os.path.isfile(cand) else None


def data_uri(path: str, data: bytes) -> str:
    mime, _ = mimetypes.guess_type(path)
    return f"data:{mime or 'application/octet-stream'};base64," + base64.b64encode(data).decode(
        "ascii"
    )


_URL = re.compile(r"""url\(\s*(['"]?)([^)'"]+)\1\s*\)""")


def inline_css_urls(css: str, css_dir: str) -> str:
    """Inline local url(...) refs inside a CSS string (fonts/images) as data: URIs."""

    def repl(m: re.Match[str]) -> str:
        url = m.group(2)
        if is_remote(url):
            report["remote_kept"] += 1  # type: ignore[operator]
            return m.group(0)
        lp = local_path(css_dir, url)
        if lp is None:
            _skipped("css-url", url, "not found")
            return m.group(0)
        try:
            with open(lp, "rb") as fh:
                data = fh.read()
        except OSError:
            _skipped("css-url", url, "unreadable")
            return m.group(0)
        _inlined("css-url", url)
        return f"url({data_uri(lp, data)})"

    return _URL.sub(repl, css)


def _attr(tag: str, name: str) -> str | None:
    m = re.search(rf"\b{name}\s*=\s*(['\"])(.*?)\1", tag, re.I | re.S)
    return m.group(2) if m else None


def flatten(html: str, base_dir: str) -> str:
    # 1. <link rel="stylesheet" href="LOCAL"> -> <style>…</style>
    def repl_link(m: re.Match[str]) -> str:
        tag = m.group(0)
        if not re.search(r"\brel\s*=\s*(['\"]?)[^'\">]*stylesheet", tag, re.I):
            return tag
        href = _attr(tag, "href")
        if not href or is_remote(href):
            if href:
                report["remote_kept"] += 1  # type: ignore[operator]
            return tag
        lp = local_path(base_dir, href)
        if lp is None:
            _skipped("link", href, "not found")
            return tag
        try:
            css = open(lp, encoding="utf-8", errors="replace").read()
        except OSError:
            _skipped("link", href, "unreadable")
            return tag
        css = inline_css_urls(css, os.path.dirname(lp))
        media = _attr(tag, "media")
        _inlined("link", href)
        return f"<style{f' media="{media}"' if media else ''}>\n{css}\n</style>"

    html = re.sub(r"<link\b[^>]*>", repl_link, html, flags=re.I)

    # 2. <script src="LOCAL"></script> -> inline <script>…</script>
    def repl_script(m: re.Match[str]) -> str:
        src = m.group(3)
        if is_remote(src):
            report["remote_kept"] += 1  # type: ignore[operator]
            return m.group(0)
        lp = local_path(base_dir, src)
        if lp is None:
            _skipped("script", src, "not found")
            return m.group(0)
        try:
            js = open(lp, encoding="utf-8", errors="replace").read()
        except OSError:
            _skipped("script", src, "unreadable")
            return m.group(0)
        typ = _attr(m.group(1) + m.group(4), "type")
        _inlined("script", src)
        js = js.replace("</script>", "<\\/script>")
        return f"<script{f' type="{typ}"' if typ else ''}>\n{js}\n</script>"

    html = re.sub(
        r"""<script\b([^>]*)\bsrc\s*=\s*(['"])(.*?)\2([^>]*)>\s*</script>""",
        repl_script,
        html,
        flags=re.I,
    )

    # 3. <img src="LOCAL"> -> src="data:…"
    def repl_img(m: re.Match[str]) -> str:
        tag = m.group(0)
        ms = re.search(r"\bsrc\s*=\s*(['\"])(.*?)\1", tag, re.I)
        if not ms:
            return tag
        src = ms.group(2)
        if is_remote(src):
            report["remote_kept"] += 1  # type: ignore[operator]
            return tag
        lp = local_path(base_dir, src)
        if lp is None:
            _skipped("img", src, "not found")
            return tag
        try:
            with open(lp, "rb") as fh:
                data = fh.read()
        except OSError:
            _skipped("img", src, "unreadable")
            return tag
        _inlined("img", src)
        return tag[: ms.start(2)] + data_uri(lp, data) + tag[ms.end(2) :]

    html = re.sub(r"<img\b[^>]*>", repl_img, html, flags=re.I)

    # 4. url(LOCAL) inside <style> blocks and style="" attrs (resolved at base_dir).
    html = re.sub(
        r"(<style\b[^>]*>)(.*?)(</style>)",
        lambda m: m.group(1) + inline_css_urls(m.group(2), base_dir) + m.group(3),
        html,
        flags=re.I | re.S,
    )
    html = re.sub(
        r"(\bstyle\s*=\s*)(['\"])(.*?)\2",
        lambda m: m.group(1) + m.group(2) + inline_css_urls(m.group(3), base_dir) + m.group(2),
        html,
        flags=re.I | re.S,
    )
    return html


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: flatten_assets.py <deck.html> <out.html>", file=sys.stderr)
        return 2
    src, out = argv[1], argv[2]
    if not os.path.isfile(src):
        print(f"flatten: not a file: {src}", file=sys.stderr)
        return 2
    base_dir = os.path.dirname(os.path.abspath(src))
    html = open(src, encoding="utf-8", errors="replace").read()
    flat = flatten(html, base_dir)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(flat)
    report["out"] = out  # type: ignore[assignment]
    report["bytes"] = len(flat.encode("utf-8"))  # type: ignore[assignment]
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
