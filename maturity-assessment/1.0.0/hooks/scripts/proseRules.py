#!/usr/bin/env python3
"""PostToolUse prose checks on scoring/, findings/, and deliverable/.

Mechanical, config driven checks: US to AU spelling, the hyphen ban in
prose (code spans, URLs, CLI flags, and identifiers exempt), paragraph
length (maximum sentences from the pack qaRules proseRules, default 4),
display date format (DD/MM/YYYY in prose), plus banned phrasings from
engagement.yaml brand.bannedPhrasings and the pack's
reportSpec/qaRules.yaml (flat strings or entries carrying nested
seedPatterns).

Non blocking: violations return as additionalContext. Semantic
enforcement (banned concepts expressed as synonyms) lives in the
report-qa agent, not here.

The engagement root is resolved by walking up from the target file path
to the nearest engagement.yaml, falling back to CLAUDE_PROJECT_DIR.
Exits 0 silently when neither resolves to an engagement.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys

SCOPED_DIRS = ("scoring/", "findings/", "deliverable/")

US_WORDS = {
    "organize": "organise", "organized": "organised", "organizing": "organising",
    "organization": "organisation", "organizations": "organisations",
    "color": "colour", "colors": "colours", "colored": "coloured",
    "behavior": "behaviour", "behaviors": "behaviours",
    "center": "centre", "centers": "centres", "centered": "centred",
    "analyze": "analyse", "analyzed": "analysed", "analyzing": "analysing",
    "realize": "realise", "realized": "realised",
    "optimize": "optimise", "optimized": "optimised", "optimizing": "optimising",
    "standardize": "standardise", "standardized": "standardised",
    "prioritize": "prioritise", "prioritized": "prioritised",
    "catalog": "catalogue", "catalogs": "catalogues",
    "license": "licence (noun)", "defense": "defence",
    "labor": "labour", "favor": "favour", "honor": "honour",
}

HYPHEN_RX = re.compile(r"\b[A-Za-z]{2,}-[A-Za-z]{2,}\b")
# Month first or day first ambiguity: flag ISO dates appearing in prose
# (they belong in frontmatter and data at rest, not display text).
ISO_DATE_RX = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
MAX_SENTENCES = 4  # fallback when the pack qaRules declares no maximum


def readEvent() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        sys.exit(0)


def engagementRoot(fromPath: str = "") -> str:
    if fromPath and os.path.isabs(fromPath):
        current = os.path.dirname(os.path.abspath(fromPath))
        while True:
            if os.path.isfile(os.path.join(current, "engagement.yaml")):
                return current
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent
    root = os.environ.get("CLAUDE_PROJECT_DIR") or ""
    if not root or not os.path.isfile(os.path.join(root, "engagement.yaml")):
        sys.exit(0)
    return root


def loadConfigLoader():
    pluginRoot = os.environ.get("CLAUDE_PLUGIN_ROOT") or ""
    path = os.path.join(pluginRoot, "engine", "configLoader.py")
    if not os.path.isfile(path):
        return None
    try:
        spec = importlib.util.spec_from_file_location("configLoader", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        return None


def collectPhrases(value) -> list[str]:
    """Walk flat strings, lists, and maps carrying nested seedPatterns."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out += collectPhrases(item)
        return out
    if isinstance(value, dict):
        return collectPhrases(value.get("seedPatterns"))
    return []


def qaSettings(root: str) -> tuple[list[str], int]:
    """Banned phrasings and the paragraph sentence maximum, from
    engagement.yaml plus the pack qaRules.yaml."""
    phrases: list[str] = []
    maxSentences = MAX_SENTENCES
    loader = loadConfigLoader()
    if loader is None:
        return phrases, maxSentences
    try:
        engagement = loader.loadEngagement(root)
        phrases += collectPhrases(((engagement.get("brand") or {}).get("bannedPhrasings")) or [])
    except Exception:
        pass
    try:
        pluginRoot = os.environ.get("CLAUDE_PLUGIN_ROOT") or ""
        packDir, _pack = loader.resolvePack(root, pluginRoot)
        qaPath = os.path.join(packDir, "reportSpec", "qaRules.yaml")
        if os.path.isfile(qaPath):
            qa = loader.loadYaml(qaPath) or {}
            for key, value in qa.items():
                if "banned" in key.lower() or "phras" in key.lower():
                    phrases += collectPhrases(value)
            declared = ((qa.get("proseRules") or {}).get("maxParagraphSentences"))
            if isinstance(declared, int) and declared > 0:
                maxSentences = declared
    except Exception:
        pass
    return phrases, maxSentences


def stripExempt(text: str) -> str:
    """Remove frontmatter, code, URLs, CLI flags, and file identifiers."""
    text = re.sub(r"\A---\n.*?\n---\n", " ", text, flags=re.DOTALL)
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"--[A-Za-z][\w-]*", " ", text)
    text = re.sub(r"\b[\w./-]+\.(?:md|py|sh|json|html|css|js|csv|ya?ml|pdf|xlsx?)\b", " ", text)
    return text


def countSentences(paragraph: str) -> int:
    cleaned = re.sub(r"[`_*]+", "", paragraph)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return 0
    parts = [p for p in re.split(r"(?<=[.!?])\s+", cleaned) if p.strip()]
    return len(parts)


def paragraphs(text: str) -> list[str]:
    body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    out = []
    for block in re.split(r"\n\s*\n", body):
        lines = [ln for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue
        if all(re.match(r"^(#{1,6}\s|[-*+]\s|\d+\.\s|>\s|\||<)", ln.strip()) for ln in lines):
            continue
        out.append(" ".join(ln.strip() for ln in lines))
    return out


def findViolations(text: str, phrases: list[str], maxSentences: int = MAX_SENTENCES) -> list[str]:
    cleaned = stripExempt(text)
    out: list[str] = []

    for m in HYPHEN_RX.finditer(cleaned):
        out.append(f"hyphen in prose: '{m.group(0)}' — use an em dash or rephrase")

    lowered = cleaned.lower()
    for us, au in US_WORDS.items():
        if re.search(rf"\b{re.escape(us)}\b", lowered):
            out.append(f"US spelling: '{us}' — use '{au}'")

    for m in ISO_DATE_RX.finditer(cleaned):
        out.append(
            f"display date '{m.group(0)}' in prose — display dates are DD/MM/YYYY; "
            "ISO 8601 belongs in frontmatter and data at rest"
        )

    for phrase in phrases:
        if phrase and phrase.lower() in lowered:
            out.append(f"banned phrasing: '{phrase}'")

    for para in paragraphs(text):
        n = countSentences(para)
        if n > maxSentences:
            snippet = para[:80]
            out.append(f"paragraph length: {n} sentences — prose paragraphs run at most {maxSentences} sentences: '{snippet}…'")

    seen: set[str] = set()
    unique = []
    for v in out:
        if v not in seen:
            seen.add(v)
            unique.append(v)
    return unique


def main() -> None:
    event = readEvent()
    tool = event.get("tool_name", "")
    if tool not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)
    toolInput = event.get("tool_input") or {}
    path = (toolInput.get("file_path") or "").replace("\\", "/")
    if not path.endswith((".md", ".html")):
        sys.exit(0)
    if not any(f"/{d}" in f"/{path}" for d in SCOPED_DIRS):
        sys.exit(0)

    root = engagementRoot(toolInput.get("file_path") or "")

    if tool == "Write":
        text = toolInput.get("content") or ""
    elif tool == "Edit":
        text = toolInput.get("new_string") or ""
    else:
        text = "\n".join((e.get("new_string") or "") for e in (toolInput.get("edits") or []))
    if not text:
        sys.exit(0)

    phrases, maxSentences = qaSettings(root)
    violations = findViolations(text, phrases, maxSentences)
    if not violations:
        sys.exit(0)

    bullets = "\n".join(f"  - {v}" for v in violations[:15])
    more = "" if len(violations) <= 15 else f"\n  ... and {len(violations) - 15} more"
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": (
                    f"Prose rules review for {path} (mechanical checks, non "
                    f"blocking):\n{bullets}{more}\n\n"
                    "Fix before the QA pass. Semantic enforcement (banned "
                    "concepts expressed as synonyms) runs in the report-qa "
                    "agent."
                ),
            }
        },
        sys.stdout,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
