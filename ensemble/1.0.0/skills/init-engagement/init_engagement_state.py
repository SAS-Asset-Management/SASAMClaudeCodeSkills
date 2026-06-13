#!/usr/bin/env python3
"""init_engagement_state.py — deterministic helpers for the /init-engagement skill.

The bash driver (``init_engagement.sh``) shells out to these subcommands so all
JSON state I/O goes through the shared lib (``ensemble_common``) and the registry
edit is structurally safe (no sed-ing JSON). Mirrors ``tether_state.py``.

Subcommands:

  new-uuid
      Print a fresh uuid4.

  slug <name>
      Print a kebab-case scope_tag candidate derived from a display name.

  validate-scope <scope_tag>
      Exit 0 if it matches the packet/registry scope_tag pattern, else exit 2
      with a message. The pattern is ^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$.

  consultants-json <comma-separated-handles>
      Print a JSON array of GitHub handles (trimmed, deduped, order-preserved).

  registry-has <scope_tag>
      If the local registry (~/.ensemble/registry/registry.json) already has the
      scope_tag, print ``uuid<TAB>name<TAB>repo`` and exit 0; else exit 3.

  registry-add <uuid> <name> <scope_tag> <repo>
      Idempotently append a {uuid,name,scope_tag,repo,status:active} row to the
      local registry.json (no dup if the scope_tag is already present). Prints
      ``added`` or ``exists``. The driver owns the git pull/commit/push around it.

  registry-remove <scope_tag>
      Remove the row with this scope_tag (used by --cleanup). Prints ``removed``
      or ``absent``.

  fill <file> KEY=VAL [KEY=VAL ...]
      Substitute every ``{{KEY}}`` placeholder in <file> in place. After filling,
      if any ``{{...}}`` remain, list them and exit 2 (so a missing value is loud,
      not silent). If <file> ends in .json, the result must parse as JSON.

Stdlib only. Australian English. Never prints secrets.
"""
from __future__ import annotations

import json
import re
import sys
import uuid as _uuid

import ensemble_common as e

_SCOPE_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$")


def _slug(name: str) -> str:
    """Kebab-case a display name: lowercase, non-alnum -> '-', collapse, trim."""
    s = re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s[:64].rstrip("-")


def _registry() -> dict:
    reg = e.load_json(e.registry_path(), default={"projects": []})
    if not isinstance(reg, dict):
        reg = {"projects": []}
    if not isinstance(reg.get("projects"), list):
        reg["projects"] = []
    return reg


def _validate_scope(scope: str) -> int:
    if _SCOPE_RE.match(scope or ""):
        return 0
    print(
        f"ensemble: {scope!r} is not a valid scope_tag — use kebab-case, 3–64 chars, "
        "starting and ending alphanumeric (e.g. 'transurban-wcx-ncx').",
        file=sys.stderr,
    )
    return 2


def _registry_has(scope: str) -> int:
    for p in _registry()["projects"]:
        if isinstance(p, dict) and str(p.get("scope_tag", "")) == scope:
            print("\t".join([str(p.get("uuid", "")), str(p.get("name", "")), str(p.get("repo", ""))]))
            return 0
    return 3


def _registry_add(uuid: str, name: str, scope: str, repo: str) -> int:
    reg = _registry()
    for p in reg["projects"]:
        if isinstance(p, dict) and str(p.get("scope_tag", "")) == scope:
            print("exists")
            return 0
    reg["projects"].append({
        "uuid": uuid, "name": name, "scope_tag": scope, "repo": repo, "status": "active",
    })
    e.save_json(e.registry_path(), reg)
    print("added")
    return 0


def _registry_remove(scope: str) -> int:
    reg = _registry()
    before = len(reg["projects"])
    reg["projects"] = [
        p for p in reg["projects"]
        if not (isinstance(p, dict) and str(p.get("scope_tag", "")) == scope)
    ]
    if len(reg["projects"]) == before:
        print("absent")
        return 0
    e.save_json(e.registry_path(), reg)
    print("removed")
    return 0


def _consultants_json(csv: str) -> int:
    seen: list[str] = []
    for h in (csv or "").split(","):
        h = h.strip().lstrip("@")
        if h and h not in seen:
            seen.append(h)
    print(json.dumps(seen))
    return 0


def _fill(path: str, pairs: list[str]) -> int:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    for pair in pairs:
        if "=" not in pair:
            print(f"ensemble: bad KEY=VAL argument {pair!r}.", file=sys.stderr)
            return 2
        key, val = pair.split("=", 1)
        text = text.replace("{{" + key + "}}", val)
    leftover = sorted(set(re.findall(r"\{\{[a-z_]+\}\}", text)))
    if leftover:
        print(
            f"ensemble: {path} still has unfilled placeholders: {', '.join(leftover)}.",
            file=sys.stderr,
        )
        return 2
    if path.endswith(".json"):
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            print(f"ensemble: filling {path} produced invalid JSON: {exc}.", file=sys.stderr)
            return 2
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: init_engagement_state.py <subcommand> ...", file=sys.stderr)
        return 2
    cmd = argv[1]
    try:
        if cmd == "new-uuid":
            print(str(_uuid.uuid4()))
            return 0
        if cmd == "slug" and len(argv) == 3:
            print(_slug(argv[2]))
            return 0
        if cmd == "validate-scope" and len(argv) == 3:
            return _validate_scope(argv[2])
        if cmd == "consultants-json" and len(argv) == 3:
            return _consultants_json(argv[2])
        if cmd == "registry-has" and len(argv) == 3:
            return _registry_has(argv[2])
        if cmd == "registry-add" and len(argv) == 6:
            return _registry_add(argv[2], argv[3], argv[4], argv[5])
        if cmd == "registry-remove" and len(argv) == 3:
            return _registry_remove(argv[2])
        if cmd == "fill" and len(argv) >= 4:
            return _fill(argv[2], argv[3:])
        print(f"ensemble: bad usage for {cmd!r}.", file=sys.stderr)
        return 2
    except e.EnsembleError as exc:
        print(f"ensemble: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
