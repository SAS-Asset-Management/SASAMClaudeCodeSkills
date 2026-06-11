#!/usr/bin/env python3
"""collect_impl.py — the deterministic half of the /collect skill.

Given an engagement repo whose ``main`` branch has just been fast-forwarded by the
bash wrapper, this:

  * enumerates **merged** result sets — ``handoffs/outbox/<id>/`` directories that
    exist in the committed tree of ``main`` (only results that actually landed by
    PR, never a stray local directory);
  * for any Git LFS *pointer* file in a result set, runs ``git lfs pull`` for just
    those paths and **verifies** the materialised file's sha256 against the
    pointer's ``oid sha256:`` — if the LFS mesh is unreachable, it reports that and
    lists what was skipped (it does **not** fail hard);
  * records each collected result into ``~/.ensemble/collected.json``
    (``id, engagement, collected_at, paths``) — an idempotent upsert keyed by id;
  * prints a per-result summary (the head of each ``summary.md``) to stdout for the
    session.

Stdlib only. Reuses the shared lib (``ensemble_common``) for repo/project resolution
and atomic state writes — it does NOT re-implement state I/O. All user-facing strings
use Australian English. On any unrecoverable error it prints a clear message to
stderr and exits non-zero; a missing-result is not an error (exit 0 with a note).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ensemble_common as e

# A result set lives at handoffs/outbox/<id>/ ; the conductor writes summary.md +
# packet.md plus any deliverable files there (see ensemble_poller/dispatch.py).
OUTBOX_PREFIX = "handoffs/outbox"
SUMMARY_NAME = "summary.md"
# How many characters of each summary.md to echo to the session.
SUMMARY_HEAD_CHARS = 1600
# The first line of every Git LFS pointer file (spec v1).
LFS_POINTER_MAGIC = "version https://git-lfs.github.com/spec/v1"
_LFS_OID_RE = re.compile(r"^oid sha256:([0-9a-f]{64})\s*$", re.MULTILINE)
_LFS_SIZE_RE = re.compile(r"^size (\d+)\s*$", re.MULTILINE)


def _die(msg: str) -> "None":
    print(f"ensemble: {msg}", file=sys.stderr)
    raise SystemExit(1)


def _git(root: Path, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a git command in ``root``; never leaks output unless we choose to."""
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
    )
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        _die(f"git {' '.join(args)} failed: {detail}")
    return proc


def _git_available_lfs(root: Path) -> bool:
    """True if the git-lfs subcommand is installed (needed to materialise pointers)."""
    proc = subprocess.run(
        ["git", "-C", str(root), "lfs", "version"],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def list_merged_result_ids(root: Path) -> list[str]:
    """Return the result-set ids present in the committed tree of ``main``.

    Reads ``git ls-tree main handoffs/outbox/`` so we only ever collect results that
    were merged into the reviewed record — a result half-written in the working tree
    (not yet on main) is deliberately invisible here.
    """
    proc = _git(root, ["ls-tree", "main", f"{OUTBOX_PREFIX}/"], check=False)
    if proc.returncode != 0:
        # No outbox on main yet (or no main) — nothing merged to collect.
        return []
    ids: list[str] = []
    for line in proc.stdout.splitlines():
        # Format: "<mode> tree <oid>\t<path>" for directories.
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        meta, path = parts
        if " tree " not in meta:
            continue
        name = path.rstrip("/").split("/")[-1]
        if name:
            ids.append(name)
    return sorted(set(ids))


def list_result_files(root: Path, result_id: str) -> list[str]:
    """Repo-relative paths of every file in a merged result set (from main's tree)."""
    prefix = f"{OUTBOX_PREFIX}/{result_id}/"
    proc = _git(root, ["ls-tree", "-r", "--name-only", "main", prefix], check=False)
    if proc.returncode != 0:
        return []
    return [ln for ln in proc.stdout.splitlines() if ln.strip()]


def _is_lfs_pointer_blob(root: Path, rel_path: str) -> tuple[bool, str | None, int | None]:
    """Inspect the blob of ``rel_path`` on ``main``: is it an LFS pointer?

    Returns (is_pointer, oid_hex, size). Reading the blob (not the working-tree file)
    means we correctly classify even when the working tree already holds the
    materialised content or nothing at all.
    """
    proc = _git(root, ["show", f"main:{rel_path}"], check=False)
    if proc.returncode != 0:
        return (False, None, None)
    blob = proc.stdout
    if not blob.startswith(LFS_POINTER_MAGIC):
        return (False, None, None)
    oid_m = _LFS_OID_RE.search(blob)
    size_m = _LFS_SIZE_RE.search(blob)
    oid = oid_m.group(1) if oid_m else None
    size = int(size_m.group(1)) if size_m else None
    return (True, oid, size)


def _sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _pull_and_verify_lfs(
    root: Path, pointers: list[tuple[str, str | None, int | None]]
) -> tuple[list[str], list[str]]:
    """Materialise LFS pointer paths and verify each against its oid.

    Args:
        root: engagement repo root.
        pointers: list of (rel_path, oid_hex, size) for files that are LFS pointers.

    Returns:
        (verified_paths, skipped_notes) — ``verified_paths`` are the rel paths whose
        materialised content matched the pointer oid; ``skipped_notes`` are
        human-readable reasons a path could not be verified (mesh unreachable,
        git-lfs absent, oid mismatch, …). This never raises on a fetch failure — a
        skipped LFS object is reported, not fatal.
    """
    verified: list[str] = []
    skipped: list[str] = []
    if not pointers:
        return (verified, skipped)

    if not _git_available_lfs(root):
        for rel, _oid, _size in pointers:
            skipped.append(f"{rel}: Git LFS is not installed — install git-lfs to fetch this object")
        return (verified, skipped)

    includes = ",".join(rel for rel, _o, _s in pointers)
    pull = subprocess.run(
        ["git", "-C", str(root), "lfs", "pull", "--include", includes],
        capture_output=True,
        text=True,
    )
    mesh_unreachable = pull.returncode != 0

    for rel, oid, _size in pointers:
        target = root / rel
        # Still a pointer on disk (or absent) → the object never came down.
        if not target.exists() or _looks_like_pointer_file(target):
            if mesh_unreachable:
                skipped.append(f"{rel}: LFS mesh unreachable — object not fetched (skipped)")
            else:
                skipped.append(f"{rel}: LFS object did not materialise (skipped)")
            continue
        if not oid:
            skipped.append(f"{rel}: pointer carried no sha256 oid — cannot verify integrity (skipped)")
            continue
        actual = _sha256_of_file(target)
        if actual == oid:
            verified.append(rel)
        else:
            skipped.append(
                f"{rel}: sha256 MISMATCH — pointer oid {oid[:12]}… != file {actual[:12]}… (skipped)"
            )
    return (verified, skipped)


def _looks_like_pointer_file(path: Path) -> bool:
    """True if the on-disk file is (still) an LFS pointer rather than real content."""
    try:
        with path.open("rb") as fh:
            head = fh.read(len(LFS_POINTER_MAGIC.encode()))
    except OSError:
        return False
    return head == LFS_POINTER_MAGIC.encode()


def _summary_head(root: Path, result_id: str) -> str | None:
    """Return the head of a result's summary.md (working tree, falling back to main's blob)."""
    rel = f"{OUTBOX_PREFIX}/{result_id}/{SUMMARY_NAME}"
    wt = root / rel
    text: str | None = None
    if wt.is_file():
        try:
            text = wt.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = None
    if text is None:
        proc = _git(root, ["show", f"main:{rel}"], check=False)
        if proc.returncode == 0:
            text = proc.stdout
    if text is None:
        return None
    head = text.strip()
    if len(head) > SUMMARY_HEAD_CHARS:
        head = head[:SUMMARY_HEAD_CHARS].rstrip() + "\n…(truncated — full summary.md is in the result set)"
    return head


def _upsert_collected(record: dict[str, Any]) -> None:
    """Idempotently record a collected result in ~/.ensemble/collected.json.

    Keyed by ``id``: a re-collect updates the existing entry (refreshing
    ``collected_at`` and ``paths``) rather than appending a duplicate.
    """
    state = e.load_json(e.collected_path(), default={"collected": []})
    if not isinstance(state, dict):
        state = {"collected": []}
    items = state.get("collected")
    if not isinstance(items, list):
        items = []
    replaced = False
    for idx, existing in enumerate(items):
        if isinstance(existing, dict) and existing.get("id") == record["id"]:
            items[idx] = record
            replaced = True
            break
    if not replaced:
        items.append(record)
    state["collected"] = items
    e.save_json(e.collected_path(), state)


def collect_one(root: Path, scope_tag: str, result_id: str) -> dict[str, Any]:
    """Collect a single merged result set: materialise+verify LFS, record, summarise.

    Returns a small report dict the caller renders for the session.
    """
    files = list_result_files(root, result_id)
    if not files:
        return {"id": result_id, "found": False}

    pointers: list[tuple[str, str | None, int | None]] = []
    for rel in files:
        is_ptr, oid, size = _is_lfs_pointer_blob(root, rel)
        if is_ptr:
            pointers.append((rel, oid, size))

    verified, skipped = _pull_and_verify_lfs(root, pointers)

    collected_at = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {
        "id": result_id,
        "engagement": scope_tag,
        "collected_at": collected_at,
        "paths": files,
    }
    _upsert_collected(record)

    return {
        "id": result_id,
        "found": True,
        "engagement": scope_tag,
        "collected_at": collected_at,
        "paths": files,
        "lfs_pointers": [rel for rel, _o, _s in pointers],
        "lfs_verified": verified,
        "lfs_skipped": skipped,
        "summary_head": _summary_head(root, result_id),
    }


def _render(report: dict[str, Any]) -> None:
    """Print one result's outcome to stdout for the session (Australian English)."""
    rid = report["id"]
    print(f"\n=== {rid} ===")
    print(f"Engagement: {report['engagement']}  |  collected at {report['collected_at']}")
    print(f"Files ({len(report['paths'])}):")
    for p in report["paths"]:
        print(f"  - {p}")
    if report["lfs_pointers"]:
        print(f"Git LFS objects: {len(report['lfs_verified'])} verified, "
              f"{len(report['lfs_skipped'])} skipped (of {len(report['lfs_pointers'])}).")
        for v in report["lfs_verified"]:
            print(f"  ✓ verified: {v}")
        for s in report["lfs_skipped"]:
            print(f"  ! skipped:  {s}")
    summary = report.get("summary_head")
    if summary:
        print("\nsummary.md:")
        print("-" * 60)
        print(summary)
        print("-" * 60)
    else:
        print("\n(no summary.md in this result set)")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="collect",
        description="Collect merged engagement result sets from main.",
    )
    parser.add_argument("--root", required=True, help="engagement repo root")
    parser.add_argument("--id", default=None, help="collect only this packet/result id")
    parser.add_argument("--main-synced", default="0",
                        help="1 if the wrapper fast-forwarded main, else 0 (advisory)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    try:
        proj = e.require_tethered(root)
    except e.EnsembleError as exc:
        _die(str(exc))
        return 1  # unreachable — _die raises
    scope_tag = str(proj.get("scope_tag") or proj.get("engagement") or "")

    merged = list_merged_result_ids(root)
    if args.id:
        if args.id not in merged:
            print(
                f"ensemble: no merged result set '{args.id}' found on main. "
                f"It may not be merged yet, or the id is wrong.",
                file=sys.stderr,
            )
            if merged:
                print("ensemble: merged result sets currently available:", file=sys.stderr)
                for m in merged:
                    print(f"ensemble:   - {m}", file=sys.stderr)
            return 0
        targets = [args.id]
    else:
        targets = merged

    if not targets:
        print("ensemble: no merged result sets to collect yet "
              "(handoffs/outbox/ on main is empty).")
        return 0

    collected = 0
    for rid in targets:
        report = collect_one(root, scope_tag, rid)
        if not report.get("found"):
            print(f"ensemble: result set '{rid}' has no files on main — skipping.",
                  file=sys.stderr)
            continue
        _render(report)
        collected += 1

    print(f"\nensemble: collected {collected} result set(s) into ~/.ensemble/collected.json.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except e.EnsembleError as exc:  # state I/O failures from the lib
        print(f"ensemble: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    except BrokenPipeError:  # `| head` in the session — exit quietly
        try:
            sys.stdout.close()
        except Exception:
            pass
        os._exit(0)
