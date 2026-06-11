#!/usr/bin/env python3
"""ensemble_status.py — registry-wide status across all tethered engagements.

The deterministic engine behind the ``/status`` consultant skill. Read-only: it
NEVER mutates an engagement repo or ~/.ensemble state. For every tether recorded in
``~/.ensemble/tethers.json`` it reports, per engagement:

  * open packets       — count on the ``queue`` branch under handoffs/inbox/
  * claims + age       — handoffs/claimed/<agentId>/ entries, with claim age
  * open PRs by tier   — gh pr list into ``main``, grouped by each PR's review_tier
                         (read from handoffs/outbox/<id>/packet.md in the PR head)

and once, globally, the last Ensemble poll heartbeat from
``~/.ensemble/registry/heartbeat.json`` (ts + repos_polled + errors).

It tolerates engagements whose local clone is missing (skips them with a note), a
``queue`` branch that does not exist, and ``gh`` being unavailable or unauthenticated
(PR data is reported as unavailable rather than failing the whole run).

Stdlib only — reuses the shared lib (``ensemble_common``) for all ~/.ensemble state
I/O so this skill never re-spells where state lives. All user-facing strings are in
Australian English; nothing secret is ever printed.

Usage:
    ensemble_status.py [--json]

Exit status:
    0 — report produced (even if some engagements were skipped / had warnings).
    1 — a hard error (e.g. corrupt tethers.json) prevented any report.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ensemble_common as e

# Branch + path conventions (SHARED CONTRACT / engagement-template README).
QUEUE_BRANCH = "queue"
INBOX_DIR = "handoffs/inbox"
CLAIMED_DIR = "handoffs/claimed"
TIER_ORDER = ["auto", "light", "full", "founder", "unknown"]


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------


def _git(repo: Path, *args: str) -> tuple[int, str, str]:
    """Run a git command inside ``repo``; return (returncode, stdout, stderr).

    Never raises on a non-zero git exit — callers decide what a failure means.
    """
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:  # git missing — surfaced by the bash wrapper, but be safe.
        return 127, "", str(exc)
    return proc.returncode, proc.stdout, proc.stderr


def _queue_ref(repo: Path) -> str | None:
    """Pick the freshest available ``queue`` ref in ``repo``.

    Prefers the remote-tracking ``ensemble/queue`` (the engagement remote /tether binds),
    then ``origin/queue`` (clone mode), then a local ``queue`` branch. Returns the ref
    name, or None if none exist.
    """
    for ref in (f"ensemble/{QUEUE_BRANCH}", f"origin/{QUEUE_BRANCH}", QUEUE_BRANCH):
        rc, _, _ = _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
        if rc == 0:
            return ref
    return None


def _ls_tree(repo: Path, ref: str, path: str) -> list[str]:
    """List repo-relative file paths under ``path`` at ``ref`` (recursive).

    Returns [] when the path does not exist at that ref.
    """
    rc, out, _ = _git(repo, "ls-tree", "-r", "--name-only", ref, "--", path)
    if rc != 0:
        return []
    return [ln for ln in out.splitlines() if ln.strip()]


def _commit_epoch_for_path(repo: Path, ref: str, path: str) -> int | None:
    """Author epoch of the most recent commit touching ``path`` on ``ref``.

    Used to age a claim. Returns None if it cannot be determined.
    """
    rc, out, _ = _git(
        repo, "log", "-1", "--format=%at", ref, "--", path
    )
    if rc != 0:
        return None
    out = out.strip()
    if not out.isdigit():
        return None
    return int(out)


def _humanise_age(seconds: int) -> str:
    """Render an age in seconds as a compact Australian-English string."""
    if seconds < 0:
        return "just now"
    mins = seconds // 60
    if mins < 1:
        return "under a minute"
    hours = mins // 60
    if hours < 1:
        return f"{mins} min"
    days = hours // 24
    if days < 1:
        rem = mins % 60
        return f"{hours}h {rem}m" if rem else f"{hours}h"
    rem_h = hours % 24
    return f"{days}d {rem_h}h" if rem_h else f"{days}d"


# ---------------------------------------------------------------------------
# per-engagement collectors
# ---------------------------------------------------------------------------


def _inbox_packets(repo: Path, ref: str) -> list[str]:
    """Open packet ids on the queue branch (filenames under handoffs/inbox/)."""
    out = []
    for p in _ls_tree(repo, ref, INBOX_DIR):
        name = Path(p).name
        if name in (".gitkeep", "") or not name.endswith(".md"):
            continue
        out.append(name[:-3] if name.endswith(".md") else name)
    return sorted(out)


def _claims(repo: Path, ref: str, now_epoch: int) -> list[dict[str, Any]]:
    """Claimed packets on the queue branch: handoffs/claimed/<agentId>/<file>.

    Returns one entry per claimed packet with the claiming agent, packet name, and
    an age derived from the last commit that touched the file (best effort).
    """
    claims: list[dict[str, Any]] = []
    for p in _ls_tree(repo, ref, CLAIMED_DIR):
        rel = Path(p)
        parts = rel.parts
        # Expect handoffs/claimed/<agentId>/<file...>
        if len(parts) < 4 or rel.name == ".gitkeep":
            continue
        agent = parts[2]
        if not rel.name.endswith(".md"):
            continue
        epoch = _commit_epoch_for_path(repo, ref, p)
        age = _humanise_age(now_epoch - epoch) if epoch is not None else "age unknown"
        claims.append(
            {
                "agent": agent,
                "packet": rel.name[:-3],
                "claimed_age": age,
                "claimed_epoch": epoch,
            }
        )
    # Oldest claim first — those are the ones that may be stuck.
    claims.sort(key=lambda c: (c["claimed_epoch"] is None, c["claimed_epoch"] or 0))
    return claims


def _gh_available() -> bool:
    try:
        proc = subprocess.run(
            ["gh", "auth", "status"], capture_output=True, text=True, check=False
        )
    except OSError:
        return False
    return proc.returncode == 0


def _slug_to_owner_repo(repo: Path, repo_url: str | None) -> str | None:
    """Resolve an ``owner/name`` slug for ``gh``, from the recorded repo URL or the
    ``ensemble``/``origin`` remote.

    Accepts an https or ssh GitHub URL, or an already-bare ``owner/name`` slug.
    """
    candidate = repo_url
    if not candidate:
        for remote in ("ensemble", "origin"):   # engagement remote first, clone-mode fallback
            rc, out, _ = _git(repo, "remote", "get-url", remote)
            if rc == 0 and out.strip():
                candidate = out.strip()
                break
    if not candidate:
        return None
    s = candidate.strip()
    if s.endswith(".git"):
        s = s[:-4]
    if s.startswith("git@") and ":" in s:  # git@github.com:owner/name
        s = s.split(":", 1)[1]
    elif "://" in s:  # https://github.com/owner/name
        s = s.split("://", 1)[1]
        if "/" in s:
            s = s.split("/", 1)[1]
    # Now s should be owner/name (or host-trimmed). Keep last two path segments.
    segs = [seg for seg in s.split("/") if seg]
    if len(segs) >= 2:
        return "/".join(segs[-2:])
    return None


def _open_prs_by_tier(
    repo: Path, slug: str | None, gh_ok: bool
) -> tuple[dict[str, list[dict[str, Any]]], str | None]:
    """Group open PRs into ``main`` by review_tier.

    For each open PR, read ``review_tier`` from handoffs/outbox/<id>/packet.md on the
    PR's head ref (preferring the locally fetched copy, then the GitHub API). PRs whose
    tier cannot be determined fall into the ``unknown`` bucket.

    Returns (buckets, warning). ``warning`` is a short note when PR data could not be
    fetched (gh missing / unauthenticated / no slug), in which case buckets is empty.
    """
    buckets: dict[str, list[dict[str, Any]]] = {t: [] for t in TIER_ORDER}
    if not gh_ok:
        return buckets, "gh CLI unavailable or not authenticated — PR data skipped"
    if not slug:
        return buckets, "could not resolve owner/repo — PR data skipped"

    try:
        proc = subprocess.run(
            [
                "gh", "pr", "list",
                "--repo", slug,
                "--base", "main",
                "--state", "open",
                "--json", "number,title,headRefOid,headRefName,author,isDraft",
                "--limit", "100",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return buckets, "gh CLI could not be invoked — PR data skipped"
    if proc.returncode != 0:
        return buckets, "gh pr list failed — PR data skipped"
    try:
        prs = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        return buckets, "could not parse gh output — PR data skipped"

    for pr in prs:
        tier = _pr_tier(repo, slug, pr)
        if tier not in buckets:
            tier = "unknown"
        buckets[tier].append(
            {
                "number": pr.get("number"),
                "title": pr.get("title", ""),
                "author": (pr.get("author") or {}).get("login", ""),
                "draft": bool(pr.get("isDraft")),
            }
        )
    return buckets, None


def _pr_tier(repo: Path, slug: str, pr: dict[str, Any]) -> str:
    """Read review_tier from the PR's outbox packet; 'unknown' if not determinable.

    Tries, in order: the locally available head commit (no network), then the GitHub
    contents API for the packet at the PR head. The packet path is discovered by
    listing handoffs/outbox/ at the head ref (its <id> subdir holds packet.md).
    """
    head_oid = pr.get("headRefOid") or ""
    # 1) Local: if we already have the head commit, read straight from the object DB.
    if head_oid:
        rc, _, _ = _git(repo, "cat-file", "-e", f"{head_oid}^{{commit}}")
        if rc == 0:
            for path in _ls_tree(repo, head_oid, "handoffs/outbox"):
                if Path(path).name == "packet.md":
                    rc2, content, _ = _git(repo, "show", f"{head_oid}:{path}")
                    if rc2 == 0:
                        tier = _tier_from_packet(content)
                        if tier:
                            return tier
    # 2) Network fallback via gh api — list outbox dir, then fetch packet.md.
    head_ref = pr.get("headRefName") or head_oid
    if not head_ref:
        return "unknown"
    listing = _gh_api_json(
        f"repos/{slug}/contents/handoffs/outbox?ref={head_ref}"
    )
    if isinstance(listing, list):
        for entry in listing:
            if entry.get("type") != "dir":
                continue
            pkt = _gh_api_text(
                f"repos/{slug}/contents/{entry.get('path')}/packet.md?ref={head_ref}"
            )
            if pkt:
                tier = _tier_from_packet(pkt)
                if tier:
                    return tier
    return "unknown"


def _tier_from_packet(text: str) -> str | None:
    """Pull review_tier out of a packet's front-matter via the shared parser."""
    try:
        fm = e.parse_front_matter(text)
    except e.EnsembleError:
        return None
    tier = fm.get("review_tier")
    if isinstance(tier, str) and tier in TIER_ORDER:
        return tier
    return None


def _gh_api_json(endpoint: str) -> Any:
    """GET a GitHub API endpoint via ``gh api``; return parsed JSON or None."""
    try:
        proc = subprocess.run(
            ["gh", "api", "-H", "Accept: application/vnd.github+json", endpoint],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout or "null")
    except json.JSONDecodeError:
        return None


def _gh_api_text(endpoint: str) -> str | None:
    """GET a file's raw text via ``gh api`` with the raw media type; None on failure."""
    try:
        proc = subprocess.run(
            ["gh", "api", "-H", "Accept: application/vnd.github.raw", endpoint],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout or None


# ---------------------------------------------------------------------------
# heartbeat
# ---------------------------------------------------------------------------


def _heartbeat() -> dict[str, Any]:
    """Read the last Ensemble poll heartbeat, normalised for display.

    Returns a dict with: present(bool), ts, repos_polled, errors(list), age (str),
    and on a missing/corrupt file a 'note' explaining why it is unavailable.
    """
    path = e.heartbeat_path()
    try:
        data = e.load_json(path, default=None)
    except e.EnsembleError as exc:
        return {"present": False, "note": f"heartbeat unreadable: {exc}"}
    if not isinstance(data, dict):
        return {
            "present": False,
            "note": "no poll heartbeat yet (registry not cloned or poller not run)",
        }
    ts = data.get("ts")
    age = None
    if isinstance(ts, str):
        age = _age_from_iso(ts)
    return {
        "present": True,
        "ts": ts,
        "repos_polled": data.get("repos_polled"),
        "errors": data.get("errors") or [],
        "claims": data.get("claims"),
        "age": age,
    }


def _age_from_iso(ts: str) -> str | None:
    """Age between an ISO8601 timestamp and now, humanised. None if unparseable."""
    raw = ts.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        when = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    delta = int((datetime.now(timezone.utc) - when).total_seconds())
    return _humanise_age(delta)


# ---------------------------------------------------------------------------
# top-level report
# ---------------------------------------------------------------------------


def build_report() -> dict[str, Any]:
    """Assemble the full registry-wide status report as a plain dict."""
    tethers_doc = e.load_json(e.tethers_path(), default={"tethers": []})
    if not isinstance(tethers_doc, dict):
        raise e.EnsembleError("tethers.json is not a JSON object")
    tethers = tethers_doc.get("tethers") or []

    now_epoch = int(datetime.now(timezone.utc).timestamp())
    gh_ok = _gh_available()

    engagements: list[dict[str, Any]] = []
    for t in tethers:
        if not isinstance(t, dict):
            continue
        name = t.get("name") or t.get("scope_tag") or t.get("uuid") or "(unnamed)"
        scope = t.get("scope_tag")
        path_s = t.get("path")
        repo_url = t.get("repo")
        entry: dict[str, Any] = {
            "name": name,
            "scope_tag": scope,
            "path": path_s,
            "repo": repo_url,
        }

        repo = Path(path_s).expanduser() if path_s else None
        if repo is None or not repo.exists() or not (repo / ".git").exists():
            entry["skipped"] = True
            entry["note"] = "local clone not present — skipped (tether path missing)"
            engagements.append(entry)
            continue

        ref = _queue_ref(repo)
        if ref is None:
            entry["inbox"] = []
            entry["claims"] = []
            entry["queue_note"] = (
                "no 'queue' branch found locally — fetch it to see inbox/claims"
            )
        else:
            entry["queue_ref"] = ref
            entry["inbox"] = _inbox_packets(repo, ref)
            entry["claims"] = _claims(repo, ref, now_epoch)

        slug = _slug_to_owner_repo(repo, repo_url)
        buckets, pr_warn = _open_prs_by_tier(repo, slug, gh_ok)
        entry["prs_by_tier"] = buckets
        if pr_warn:
            entry["pr_note"] = pr_warn

        engagements.append(entry)

    return {
        "generated_at": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "tether_count": len(tethers),
        "engagements": engagements,
        "heartbeat": _heartbeat(),
    }


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------


def _render_text(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("Ensemble status — registry-wide view")
    lines.append(f"  generated: {report['generated_at']}")
    n = report["tether_count"]
    lines.append(f"  tethered engagements: {n}")
    lines.append("")

    if not report["engagements"]:
        lines.append("No tethered engagements. Tether one with the /tether skill.")
        lines.append("")

    for eng in report["engagements"]:
        title = eng["name"]
        if eng.get("scope_tag"):
            title += f"  [{eng['scope_tag']}]"
        lines.append(f"▸ {title}")

        if eng.get("skipped"):
            lines.append(f"    (skipped) {eng.get('note')}")
            lines.append("")
            continue

        # Inbox
        inbox = eng.get("inbox", [])
        if eng.get("queue_note"):
            lines.append(f"    open packets : {eng['queue_note']}")
        else:
            lines.append(f"    open packets : {len(inbox)}")
            for pid in inbox:
                lines.append(f"                   - {pid}")

        # Claims
        claims = eng.get("claims", [])
        if not eng.get("queue_note"):
            lines.append(f"    claims       : {len(claims)}")
            for c in claims:
                lines.append(
                    f"                   - {c['packet']} "
                    f"(by {c['agent']}, {c['claimed_age']})"
                )

        # PRs by tier
        if eng.get("pr_note"):
            lines.append(f"    open PRs      : {eng['pr_note']}")
        else:
            buckets = eng.get("prs_by_tier", {})
            total = sum(len(buckets.get(t, [])) for t in TIER_ORDER)
            lines.append(f"    open PRs      : {total}")
            for tier in TIER_ORDER:
                prs = buckets.get(tier, [])
                if not prs:
                    continue
                lines.append(f"                   {tier}:")
                for pr in prs:
                    draft = " (draft)" if pr.get("draft") else ""
                    author = f" @{pr['author']}" if pr.get("author") else ""
                    lines.append(
                        f"                     #{pr['number']} {pr['title']}"
                        f"{author}{draft}"
                    )
        lines.append("")

    # Heartbeat
    hb = report["heartbeat"]
    lines.append("Last Ensemble poll (heartbeat)")
    if not hb.get("present"):
        lines.append(f"  {hb.get('note', 'unavailable')}")
    else:
        age = f" ({hb['age']} ago)" if hb.get("age") else ""
        lines.append(f"  at         : {hb.get('ts')}{age}")
        lines.append(f"  repos polled: {hb.get('repos_polled')}")
        errs = hb.get("errors") or []
        if errs:
            lines.append(f"  errors     : {len(errs)}")
            for er in errs:
                lines.append(f"               - {er}")
        else:
            lines.append("  errors     : none")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Registry-wide Ensemble status across all tethered engagements."
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Emit the report as JSON instead of formatted text.",
    )
    args = ap.parse_args(argv)

    try:
        report = build_report()
    except e.EnsembleError as exc:
        print(f"ensemble: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        sys.stdout.write(_render_text(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
