"""Test fixture stub of the engine configLoader public API.

The deliverable tests must run standalone in this work package before
the real engine package merges, so this stub implements the same public
API the real engine/configLoader.py exposes: loadYaml, loadEngagement,
and resolvePack (honouring the local overlay resolution order). Tests
point CLAUDE_PLUGIN_ROOT at tests/fixtures/pluginRoot so the deliverable
scripts import this stub instead of the merged engine.
"""

import os


def _parseScalar(text):
    text = text.strip()
    if text == "":
        return None
    if (text.startswith('"') and text.endswith('"')) or (
        text.startswith("'") and text.endswith("'")
    ):
        return text[1:-1]
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [_parseScalar(part) for part in inner.split(",")]
    if text in ("true", "True"):
        return True
    if text in ("false", "False"):
        return False
    if text in ("null", "~"):
        return None
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    return text


def _parseKey(text):
    text = text.strip()
    try:
        return int(text)
    except ValueError:
        return text.strip('"').strip("'")


def _collectLines(source):
    lines = []
    for raw in source.splitlines():
        stripped = raw.split("#", 1)[0].rstrip() if not raw.strip().startswith("#") else ""
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        lines.append((indent, stripped.strip()))
    return lines


def _parseBlock(lines, start, indent):
    if start >= len(lines):
        return None, start
    if lines[start][1].startswith("- "):
        return _parseList(lines, start, indent)
    return _parseMap(lines, start, indent)


def _parseList(lines, start, indent):
    items = []
    i = start
    while i < len(lines):
        lineIndent, content = lines[i]
        if lineIndent < indent or not content.startswith("- "):
            break
        body = content[2:].strip()
        if ":" in body:
            key, _, rest = body.partition(":")
            item = {}
            if rest.strip():
                item[_parseKey(key)] = _parseScalar(rest)
                i += 1
            else:
                value, i = _parseBlock(lines, i + 1, lineIndent + 2)
                item[_parseKey(key)] = value
            while i < len(lines) and lines[i][0] > lineIndent and not lines[i][1].startswith("- "):
                childKey, _, childRest = lines[i][1].partition(":")
                if childRest.strip():
                    item[_parseKey(childKey)] = _parseScalar(childRest)
                    i += 1
                else:
                    value, i = _parseBlock(lines, i + 1, lines[i][0] + 2)
                    item[_parseKey(childKey)] = value
            items.append(item)
        else:
            items.append(_parseScalar(body))
            i += 1
    return items, i


def _parseMap(lines, start, indent):
    result = {}
    i = start
    while i < len(lines):
        lineIndent, content = lines[i]
        if lineIndent < indent or content.startswith("- "):
            break
        key, _, rest = content.partition(":")
        if rest.strip():
            result[_parseKey(key)] = _parseScalar(rest)
            i += 1
        else:
            value, i = _parseBlock(lines, i + 1, lineIndent + 1)
            result[_parseKey(key)] = value
    return result, i


def loadYaml(path):
    with open(path, "r", encoding="utf-8") as handle:
        lines = _collectLines(handle.read())
    if not lines:
        return {}
    value, _ = _parseBlock(lines, 0, 0)
    return value


def loadEngagement(repoRoot):
    return loadYaml(os.path.join(repoRoot, "engagement.yaml"))


def resolvePack(repoRoot, pluginRoot):
    engagement = loadEngagement(repoRoot)
    packId = (engagement.get("framework", {}) or {}).get("pack")
    for base in (repoRoot, pluginRoot):
        packDir = os.path.join(base, "packs", str(packId))
        packYaml = os.path.join(packDir, "pack.yaml")
        if os.path.isfile(packYaml):
            return packDir, loadYaml(packYaml)
    raise FileNotFoundError(
        "pack {} not found in {} or {}".format(packId, repoRoot, pluginRoot)
    )
