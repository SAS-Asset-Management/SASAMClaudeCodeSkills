#!/usr/bin/env python3
"""tether_state.py — registry resolution + tethers.json upsert for the /tether skill.

The deterministic JSON half of the tether skill. The bash driver (``tether.sh``)
shells out to these subcommands so all state I/O goes through the shared lib
(``ensemble_common``) and never gets re-spelled here.

Subcommands (all read/write under ~/.ensemble via the shared lib):

  resolve <query>
      Resolve a project from the local registry by EXACT uuid, else by fuzzy
      (case-insensitive substring) name match. Prints one TSV line
      ``uuid<TAB>name<TAB>scope_tag<TAB>repo<TAB>status`` on a unique match and
      exits 0. On no match: a message to stderr, exit 3. On an ambiguous match:
      lists the candidates to stderr, exit 4.

  upsert <uuid> <name> <scope_tag> <repo> <path>
      Upsert (insert-or-replace by uuid) an entry into ~/.ensemble/tethers.json,
      stamping ``tethered_at`` with the current UTC time. Idempotent. Prints
      ``tethered`` or ``re-tethered`` to stdout.

Stdlib only. Australian English in all user-facing strings. Never prints secrets.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone

import ensemble_common as e


def _utc_now() -> str:
    """ISO8601 UTC timestamp, e.g. 2026-06-10T04:21:09Z."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve(query: str) -> int:
    """Resolve a registry project by exact uuid or fuzzy name. See module docstring."""
    query = (query or "").strip()
    if not query:
        print("ensemble: a project uuid or name is required.", file=sys.stderr)
        return 2

    registry = e.load_registry()
    projects = [p for p in registry.get("projects", []) if isinstance(p, dict)]

    # 1) Exact uuid wins outright — uuids are unique and unambiguous.
    for p in projects:
        if str(p.get("uuid", "")) == query:
            _emit(p)
            return 0

    # 2) Exact (case-insensitive) name match.
    ql = query.lower()
    exact_name = [p for p in projects if str(p.get("name", "")).lower() == ql]
    if len(exact_name) == 1:
        _emit(exact_name[0])
        return 0
    if len(exact_name) > 1:
        return _ambiguous(query, exact_name)

    # 3) Fuzzy: case-insensitive substring against name OR scope_tag.
    fuzzy = [
        p
        for p in projects
        if ql in str(p.get("name", "")).lower()
        or ql in str(p.get("scope_tag", "")).lower()
    ]
    if len(fuzzy) == 1:
        _emit(fuzzy[0])
        return 0
    if len(fuzzy) > 1:
        return _ambiguous(query, fuzzy)

    print(
        f"ensemble: no project in the registry matches {query!r}. "
        "Check the name/uuid, or refresh the registry and try again.",
        file=sys.stderr,
    )
    return 3


def _emit(p: dict) -> None:
    """Print a resolved project as a single TSV line for the bash driver to read."""
    fields = [
        str(p.get("uuid", "")),
        str(p.get("name", "")),
        str(p.get("scope_tag", "")),
        str(p.get("repo", "")),
        str(p.get("status", "")),
    ]
    print("\t".join(fields))


def _ambiguous(query: str, matches: list[dict]) -> int:
    """List candidate projects to stderr and return the ambiguous exit code (4)."""
    print(
        f"ensemble: {query!r} is ambiguous — {len(matches)} projects match. "
        "Re-run /tether with the exact uuid or full name:",
        file=sys.stderr,
    )
    for p in matches:
        print(
            f"  - {p.get('name', '?')}  "
            f"[scope: {p.get('scope_tag', '?')}]  uuid: {p.get('uuid', '?')}",
            file=sys.stderr,
        )
    return 4


def _upsert(uuid: str, name: str, scope_tag: str, repo: str, path: str) -> int:
    """Insert-or-replace a tethers.json entry keyed by uuid. Idempotent."""
    if not uuid:
        print("ensemble: a project uuid is required to record a tether.", file=sys.stderr)
        return 2

    state = e.load_json(e.tethers_path(), default={"tethers": []})
    if not isinstance(state, dict):
        state = {"tethers": []}
    tethers = state.setdefault("tethers", [])
    if not isinstance(tethers, list):
        tethers = []
        state["tethers"] = tethers

    entry = {
        "uuid": uuid,
        "name": name,
        "scope_tag": scope_tag,
        "path": path,
        "repo": repo,
        "tethered_at": _utc_now(),
    }

    existing_idx = next(
        (i for i, t in enumerate(tethers) if isinstance(t, dict) and t.get("uuid") == uuid),
        None,
    )
    if existing_idx is None:
        tethers.append(entry)
        verb = "tethered"
    else:
        tethers[existing_idx] = entry
        verb = "re-tethered"

    e.save_json(e.tethers_path(), state)
    print(verb)
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: tether_state.py <resolve|upsert> ...", file=sys.stderr)
        return 2
    cmd = argv[1]
    try:
        if cmd == "resolve":
            if len(argv) != 3:
                print("usage: tether_state.py resolve <uuid|name>", file=sys.stderr)
                return 2
            return _resolve(argv[2])
        if cmd == "upsert":
            if len(argv) != 7:
                print(
                    "usage: tether_state.py upsert <uuid> <name> <scope_tag> <repo> <path>",
                    file=sys.stderr,
                )
                return 2
            return _upsert(argv[2], argv[3], argv[4], argv[5], argv[6])
        print(f"ensemble: unknown subcommand {cmd!r}.", file=sys.stderr)
        return 2
    except e.EnsembleError as exc:
        print(f"ensemble: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
