"""Minimal YAML subset loader for the maturity assessment engine.

This module is Python stdlib only and side effect free on import. Hooks and
the deliverable builder load it via ``importlib.util.spec_from_file_location``,
so the public function signatures below are a contract:

    loadYaml(path: str) -> dict
    loadEngagement(repoRoot: str) -> dict
    resolvePack(repoRoot: str, pluginRoot: str) -> tuple[str, dict]

Supported YAML subset (anything outside it raises ``ValueError`` with the
source path and line number):

* two space indentation only (tabs and odd indents are rejected)
* nested maps (``key: value`` and ``key:`` introducing a nested block)
* block lists (``- item``), including lists of maps (``- key: value``)
* inline lists (``[a, b, c]``)
* scalar strings (bare, single quoted, double quoted), integers, floats,
  booleans (``true`` / ``false``), ``null`` / ``~``, and ISO 8601 dates
  (returned as strings, e.g. ``"2026-08-03"``)
* comments introduced with ``#`` (full line or trailing)

Explicitly NOT supported: anchors and aliases (``&``, ``*``), multiline
scalars (``|``, ``>``), flow maps (``{...}``), tags (``!!``), and documents
separated by ``---``. Every shipped .yaml file in the plugin and its packs
must stay within the subset.
"""

from __future__ import annotations

import math
import os


def _fail(source, lineNo, message):
    raise ValueError(f"{source}:{lineNo}: {message}")


def _stripComment(line):
    """Remove a trailing comment, respecting quoted strings."""
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
    return line


def _significantLines(text, source):
    """Yield (lineNo, indent, content) for every significant line."""
    out = []
    for lineNo, raw in enumerate(text.splitlines(), 1):
        stripped = _stripComment(raw).rstrip()
        if not stripped.strip():
            continue
        leading = stripped[: len(stripped) - len(stripped.lstrip())]
        if "\t" in leading:
            _fail(source, lineNo, "tab indentation is outside the supported subset; use two spaces")
        indent = len(leading)
        if indent % 2 != 0:
            _fail(source, lineNo, f"indentation of {indent} spaces is not a multiple of two")
        content = stripped.strip()
        if content == "---" or content == "...":
            _fail(source, lineNo, "multi document markers are outside the supported subset")
        out.append((lineNo, indent, content))
    return out


def _checkForbiddenScalar(value, source, lineNo):
    if value.startswith("&") or value.startswith("*"):
        _fail(source, lineNo, "anchors and aliases are outside the supported subset")
    if value in ("|", ">") or value.startswith("|") or value.startswith(">"):
        _fail(source, lineNo, "multiline scalars are outside the supported subset")
    if value.startswith("!!") or value.startswith("!"):
        _fail(source, lineNo, "YAML tags are outside the supported subset")
    if value.startswith("{"):
        _fail(source, lineNo, "flow maps are outside the supported subset")


def _splitInlineList(inner, source, lineNo):
    items = []
    current = []
    quote = None
    for ch in inner:
        if quote:
            current.append(ch)
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
            current.append(ch)
        elif ch == ",":
            items.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if quote:
        _fail(source, lineNo, "unterminated quote in inline list")
    tail = "".join(current).strip()
    if tail or items:
        items.append(tail)
    return [item for item in items]


def _parseScalar(value, source, lineNo):
    value = value.strip()
    _checkForbiddenScalar(value, source, lineNo)
    if value.startswith("[") :
        if not value.endswith("]"):
            _fail(source, lineNo, "inline list must open and close on the same line")
        parts = _splitInlineList(value[1:-1], source, lineNo)
        return [_parseScalar(p, source, lineNo) for p in parts if p != ""]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    if value in ("null", "~", "Null", "NULL"):
        return None
    if value in ("true", "True", "TRUE"):
        return True
    if value in ("false", "False", "FALSE"):
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        number = float(value)
        if math.isfinite(number):
            return number
    except ValueError:
        pass
    return value


def _splitKeyValue(content, source, lineNo):
    """Split 'key: value' or 'key:' on the first key separating colon."""
    quote = None
    for i, ch in enumerate(content):
        if quote:
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
        elif ch == ":":
            if i + 1 == len(content) or content[i + 1] in " \t":
                key = content[:i].strip()
                if len(key) >= 2 and key[0] == key[-1] and key[0] in ("'", '"'):
                    key = key[1:-1]
                return key, content[i + 1 :].strip()
    return None, None


def _looksLikeMapEntry(content):
    key, _ = _splitKeyValue(content, "<probe>", 0)
    return key is not None


class _Parser:
    def __init__(self, lines, source):
        self.lines = lines
        self.source = source
        self.pos = 0

    def _peek(self):
        return self.lines[self.pos] if self.pos < len(self.lines) else None

    def parseBlock(self, indent):
        entry = self._peek()
        if entry is None:
            return None
        lineNo, entryIndent, content = entry
        if entryIndent != indent:
            _fail(self.source, lineNo, f"expected indentation of {indent} spaces, found {entryIndent}")
        if content == "-" or content.startswith("- "):
            return self._parseList(indent)
        return self._parseMap(indent)

    def _parseMap(self, indent):
        result = {}
        while True:
            entry = self._peek()
            if entry is None:
                break
            lineNo, entryIndent, content = entry
            if entryIndent < indent:
                break
            if entryIndent > indent:
                _fail(self.source, lineNo, f"unexpected indentation of {entryIndent} spaces inside a map at {indent}")
            if content == "-" or content.startswith("- "):
                break
            key, value = _splitKeyValue(content, self.source, lineNo)
            if key is None:
                _fail(self.source, lineNo, f"expected 'key: value', found {content!r}")
            if key in result:
                _fail(self.source, lineNo, f"duplicate key {key!r}")
            self.pos += 1
            if value == "":
                nxt = self._peek()
                if nxt is not None and nxt[1] > indent:
                    result[key] = self.parseBlock(nxt[1])
                else:
                    result[key] = None
            else:
                result[key] = _parseScalar(value, self.source, lineNo)
        return result

    def _parseList(self, indent):
        result = []
        while True:
            entry = self._peek()
            if entry is None:
                break
            lineNo, entryIndent, content = entry
            if entryIndent != indent or not (content == "-" or content.startswith("- ")):
                if entryIndent > indent:
                    _fail(self.source, lineNo, f"unexpected indentation of {entryIndent} spaces inside a list at {indent}")
                break
            rest = content[1:].strip()
            if rest == "":
                self.pos += 1
                nxt = self._peek()
                if nxt is None or nxt[1] <= indent:
                    result.append(None)
                else:
                    result.append(self.parseBlock(nxt[1]))
            elif _looksLikeMapEntry(rest):
                result.append(self._parseListItemMap(lineNo, indent, rest))
            else:
                self.pos += 1
                result.append(_parseScalar(rest, self.source, lineNo))
        return result

    def _parseListItemMap(self, lineNo, dashIndent, firstEntry):
        """Parse '- key: value' plus continuation keys indented two past the dash."""
        itemIndent = dashIndent + 2
        # Rewrite the dash line as its inline first map entry, then reuse the map parser.
        self.lines[self.pos] = (lineNo, itemIndent, firstEntry)
        return self._parseMap(itemIndent)


def parseYamlText(text, source="<string>"):
    """Parse a YAML subset document from a string. Returns the root value."""
    lines = _significantLines(text, source)
    if not lines:
        return {}
    parser = _Parser(lines, source)
    root = parser.parseBlock(lines[0][1])
    leftover = parser._peek()
    if leftover is not None:
        _fail(source, leftover[0], "content after the root block could not be parsed; check indentation")
    return root


def loadYaml(path):
    """Load a YAML subset file. Returns the parsed root (a dict for every
    shipped configuration file; a list when the document root is a block list,
    as in a chunker manifest)."""
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    return parseYamlText(text, source=path)


def loadEngagement(repoRoot):
    """Load <repoRoot>/engagement.yaml, the single configuration surface."""
    path = os.path.join(repoRoot, "engagement.yaml")
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"No engagement.yaml found at {path}. This command must be run against "
            "an engagement repo initialised with the maturity-intake skill."
        )
    return loadYaml(path)


def resolvePack(repoRoot, pluginRoot):
    """Resolve the framework pack named by engagement framework.pack.

    Resolution order honours the local overlay: <repoRoot>/packs/<id> is
    checked first, then <pluginRoot>/packs/<id>. Returns a tuple of the pack
    directory and the parsed pack.yaml.
    """
    engagement = loadEngagement(repoRoot)
    framework = engagement.get("framework") or {}
    packId = framework.get("pack")
    if not packId:
        raise ValueError(f"{os.path.join(repoRoot, 'engagement.yaml')}: framework.pack is not set")
    for base in (repoRoot, pluginRoot):
        packDir = os.path.join(base, "packs", packId)
        manifest = os.path.join(packDir, "pack.yaml")
        if os.path.isfile(manifest):
            return packDir, loadYaml(manifest)
    raise FileNotFoundError(
        f"Pack {packId!r} not found. Looked for packs/{packId}/pack.yaml under "
        f"{repoRoot} and {pluginRoot}."
    )
