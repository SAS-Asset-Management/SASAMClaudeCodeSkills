#!/usr/bin/env python3
"""sync.py — the /sync report for an Ensemble consultant.

Read-only, fast, never blocks the session. Fetches and fast-forwards the
engagement repo's ``main`` and ``queue`` branches, then reports — IN ORDER —
the four things a consultant needs to see on returning to a tethered repo:

  (a) merged results not yet collected   — outbox/* on main vs ~/.ensemble/collected.json
  (b) open PRs awaiting this consultant  — gh pr list --search 'review-requested:@me'
  (c) packets returned to the queue       — queue:inbox/HX-*.md with retries>0 / rejection note
  (d) claims in flight                    — queue:claimed/**/HX-*.md with age (claim commit date)

Zero-state across all four is a SINGLE line. We reuse the shared lib for repo
resolution, project.json reads and ~/.ensemble state — this script owns only the
git/gh plumbing and the presentation. Stdlib only; Australian English.

Exit codes: 0 on a successful report (even with nothing to show); non-zero only on
a hard failure (not a tethered repo, git unavailable, etc.). A degraded git
fetch / pull / gh call is reported inline and does NOT fail the run — /sync must
never block a session on a bad network.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone

import ensemble_common as e

# Branches we keep in step on every sync.
MAIN = "main"
QUEUE = "queue"

# Where things live in an engagement repo (spec v1.2 §2).
OUTBOX = "handoffs/outbox"   # on main: handoffs/outbox/<id>/{packet.md,summary.md,...}
INBOX = "handoffs/inbox"     # on queue: handoffs/inbox/HX-*.md
CLAIMED = "handoffs/claimed"  # on queue: handoffs/claimed/<agentId>/HX-*.md


def _err(msg: str) -> None:
    """Print a non-fatal warning to stderr (never a secret)."""
    print(f"ensemble: {msg}", file=sys.stderr)


def _git(root: str, *args: str, check: bool = False) -> subprocess.CompletedProcess[str]:
    """Run a git command in ``root`` and capture its output (text)."""
    return subprocess.run(
        ["git", "-C", root, *args],
        capture_output=True,
        text=True,
        check=check,
    )


def _gh(root: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Run a gh command in ``root`` and capture its output (text)."""
    return subprocess.run(
        ["gh", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )


def _have(cmd: str) -> bool:
    """True if ``cmd`` is on PATH."""
    from shutil import which

    return which(cmd) is not None


# ---------------------------------------------------------------------------
# Step 1 — fetch + fast-forward main and queue (best effort)
# ---------------------------------------------------------------------------


def sync_branches(root: str, remote: str = "ensemble") -> list[str]:
    """Fetch the remote, then fast-forward ``main`` and ``queue`` if checked out.

    Read-only/non-destructive: only ``--ff-only`` pulls. Never switches the
    consultant's working branch, never resets. Returns a list of human-readable
    warnings (empty when everything fast-forwarded cleanly). A failure here is
    reported, not fatal — the report below still runs against whatever refs we
    have locally (the remote-tracking refs after fetch).
    """
    warnings: list[str] = []

    fetch = _git(root, "fetch", "--quiet", remote, MAIN, QUEUE)
    if fetch.returncode != 0:
        warnings.append(
            "could not fetch from the remote — showing the last-known local state."
        )
        return warnings  # nothing else will succeed offline; bail to the report.

    # Fast-forward only the branch we currently have checked out (if it is main or
    # queue). We must not switch branches in a shared/working checkout.
    cur = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    current = cur.stdout.strip() if cur.returncode == 0 else ""
    if current in (MAIN, QUEUE):
        pull = _git(root, "merge", "--ff-only", f"{remote}/{current}")
        if pull.returncode != 0:
            warnings.append(
                f"could not fast-forward '{current}' (you have local commits or a "
                "divergence) — reporting against the fetched remote-tracking ref instead."
            )
    return warnings


def _ref(root: str, remote: str, branch: str) -> str:
    """Best ref to read a branch from: remote-tracking after fetch, else local."""
    rt = f"{remote}/{branch}"
    if _git(root, "rev-parse", "--verify", "--quiet", rt).returncode == 0:
        return rt
    if _git(root, "rev-parse", "--verify", "--quiet", branch).returncode == 0:
        return branch
    return ""


# ---------------------------------------------------------------------------
# Step 2a — merged results not yet collected
# ---------------------------------------------------------------------------


def _collected_ids() -> set[str]:
    """The set of result ids already recorded in ~/.ensemble/collected.json."""
    data = e.load_json(e.collected_path(), default={"collected": []})
    out: set[str] = set()
    if isinstance(data, dict):
        for row in data.get("collected", []) or []:
            if isinstance(row, dict):
                rid = row.get("id")   # key strictly on packet id (matches the writer's shape)
                if rid:
                    out.add(str(rid))
    return out


def uncollected_results(root: str, main_ref: str, scope: str) -> list[dict[str, str]]:
    """Result-set ids present under outbox/ on main but not yet in collected.json.

    A result set is a directory ``handoffs/outbox/<id>/`` (spec §2). We list those
    ids from the tree at ``main_ref`` and subtract the collected set. Each entry
    carries a one-line title pulled from the result's ``summary.md`` first heading/
    line when available (best effort — purely for the report).
    """
    if not main_ref:
        return []
    ls = _git(root, "ls-tree", "-r", "--name-only", main_ref, f"{OUTBOX}/")
    if ls.returncode != 0:
        return []
    ids: dict[str, None] = {}
    for line in ls.stdout.splitlines():
        # handoffs/outbox/<id>/<file...>
        rest = line[len(OUTBOX) + 1:]
        if "/" not in rest:
            continue
        rid = rest.split("/", 1)[0]
        if rid:
            ids.setdefault(rid, None)

    collected = _collected_ids()
    results: list[dict[str, str]] = []
    for rid in ids:
        if rid in collected:
            continue
        results.append({"id": rid, "title": _summary_title(root, main_ref, rid)})
    results.sort(key=lambda r: r["id"])
    return results


def _summary_title(root: str, main_ref: str, rid: str) -> str:
    """First meaningful line of a result's summary.md (best effort, may be empty)."""
    path = f"{OUTBOX}/{rid}/summary.md"
    show = _git(root, "show", f"{main_ref}:{path}")
    if show.returncode != 0:
        return ""
    for raw in show.stdout.splitlines():
        line = raw.lstrip("#").strip()
        if line:
            return line[:100]
    return ""


# ---------------------------------------------------------------------------
# Step 2b — open PRs where this consultant is a required reviewer
# ---------------------------------------------------------------------------


def review_requested_prs(root: str) -> tuple[list[dict[str, str]], str | None]:
    """Open PRs requesting THIS consultant as a reviewer.

    Returns ``(prs, warning)``. ``warning`` is non-None when gh is unavailable or
    unauthenticated (we never fail the report on it). Each PR dict has number,
    title, author, tier.

    Authority note: the packet front-matter ``review_tier`` in
    ``handoffs/outbox/<id>/packet.md`` is the schema-owned source of truth (and is what
    ``/status`` reads). Here we read the fast ``tier:<x>`` PR label as a HINT only, to keep
    ``/sync`` non-blocking; the poller derives that label from the packet when it opens the
    PR, so they agree by construction. Treat a missing/blank label as "unknown", not a
    contradiction.
    """
    if not _have("gh"):
        return [], "GitHub CLI not found — skipping the review-requested check."
    res = _gh(
        root,
        "pr",
        "list",
        "--state",
        "open",
        "--search",
        "review-requested:@me",
        "--json",
        "number,title,author,labels",
    )
    if res.returncode != 0:
        # gh prints its own reason (auth, no remote); surface a one-liner.
        first = (res.stderr or "").strip().splitlines()
        why = first[0] if first else "gh pr list failed"
        return [], f"could not query GitHub PRs ({why}); skipping review-requested."
    try:
        rows = json.loads(res.stdout or "[]")
    except json.JSONDecodeError:
        return [], "could not parse GitHub PR list; skipping review-requested."
    prs: list[dict[str, str]] = []
    for r in rows:
        author = (r.get("author") or {}).get("login", "?")
        tier = ""
        for lbl in r.get("labels", []) or []:
            name = lbl.get("name") or ""
            if name.startswith("tier:"):
                tier = name.split(":", 1)[1]
        prs.append(
            {
                "number": str(r.get("number", "?")),
                "title": str(r.get("title", "")).strip(),
                "author": author,
                "tier": tier,
            }
        )
    prs.sort(key=lambda p: int(p["number"]) if p["number"].isdigit() else 0)
    return prs, None


# ---------------------------------------------------------------------------
# Step 2c — packets returned to queue:inbox with retries>0 / rejection note
# ---------------------------------------------------------------------------

_REJECT_HINT = ("reject", "returned", "janitor", "stuck", "retry")


def returned_packets(root: str, queue_ref: str, scope: str) -> list[dict[str, str]]:
    """Inbox packets on ``queue`` that have been bounced back (retries>0 / note).

    A returned packet is one whose front-matter ``retries`` is > 0, OR whose body
    carries a rejection/janitor note. We parse the front-matter with the shared lib
    (no re-spelling of packet rules here) and look at the brief body for a note.
    """
    if not queue_ref:
        return []
    ls = _git(root, "ls-tree", "-r", "--name-only", queue_ref, f"{INBOX}/")
    if ls.returncode != 0:
        return []
    out: list[dict[str, str]] = []
    for path in ls.stdout.splitlines():
        base = path.rsplit("/", 1)[-1]
        if not (base.startswith("HX-") and base.endswith(".md")):
            continue
        show = _git(root, "show", f"{queue_ref}:{path}")
        if show.returncode != 0:
            continue
        try:
            fm, body = e.split_packet(show.stdout)
        except e.EnsembleError:
            continue
        retries = fm.get("retries") or 0
        try:
            retries = int(retries)
        except (TypeError, ValueError):
            retries = 0
        note = _rejection_note(body)
        if retries <= 0 and not note:
            continue
        out.append(
            {
                "id": str(fm.get("id") or base[:-3]),
                "retries": str(retries),
                "note": note,
            }
        )
    out.sort(key=lambda r: r["id"])
    return out


def _rejection_note(body: str) -> str:
    """Extract a short rejection/janitor note from a packet body (best effort)."""
    for raw in body.splitlines():
        line = raw.strip().lstrip("#>*-").strip()
        if not line:
            continue
        low = line.lower()
        if any(h in low for h in _REJECT_HINT):
            return line[:120]
    return ""


# ---------------------------------------------------------------------------
# Step 2d — claims in flight on queue, with age from the claim commit date
# ---------------------------------------------------------------------------


def claims_in_flight(root: str, queue_ref: str) -> list[dict[str, str]]:
    """Open claims under queue:claimed/<agentId>/ with age since the claim commit.

    Age is the time since the last commit that touched the claimed packet path on
    ``queue`` (the rename-commit that claimed it, plus any worker progress). We
    read it via ``git log -1 --format=%ct`` per path so the age reflects the actual
    claim, not the consultant's wall clock.
    """
    if not queue_ref:
        return []
    ls = _git(root, "ls-tree", "-r", "--name-only", queue_ref, f"{CLAIMED}/")
    if ls.returncode != 0:
        return []
    now = datetime.now(timezone.utc).timestamp()
    out: list[dict[str, str]] = []
    for path in ls.stdout.splitlines():
        base = path.rsplit("/", 1)[-1]
        if not (base.startswith("HX-") and base.endswith(".md")):
            continue
        # path = handoffs/claimed/<agentId>/HX-*.md
        rest = path[len(CLAIMED) + 1:]
        agent = rest.split("/", 1)[0] if "/" in rest else "?"
        log = _git(root, "log", "-1", "--format=%ct", queue_ref, "--", path)
        ts = None
        if log.returncode == 0 and log.stdout.strip().isdigit():
            ts = int(log.stdout.strip())
        out.append(
            {
                "id": base[:-3],
                "agent": agent,
                "age": _humanise_age(now - ts) if ts is not None else "unknown age",
                "stale": "1" if (ts is not None and (now - ts) > 6 * 3600) else "",
            }
        )
    out.sort(key=lambda r: r["id"])
    return out


def _humanise_age(seconds: float) -> str:
    """'3h 12m' / '2d 4h' / '45m' / '20s' — coarse, human, Australian English."""
    s = int(max(0, seconds))
    d, rem = divmod(s, 86400)
    h, rem = divmod(rem, 3600)
    m, _ = divmod(rem, 60)
    if d:
        return f"{d}d {h}h"
    if h:
        return f"{h}h {m}m"
    if m:
        return f"{m}m"
    return f"{s}s"


# ---------------------------------------------------------------------------
# Presentation
# ---------------------------------------------------------------------------


def render(
    name: str,
    scope: str,
    results: list[dict[str, str]],
    prs: list[dict[str, str]],
    returned: list[dict[str, str]],
    claims: list[dict[str, str]],
    warnings: list[str],
) -> str:
    """Build the report. Zero-state across all four buckets => a SINGLE line."""
    total = len(results) + len(prs) + len(returned) + len(claims)
    if total == 0:
        head = f"{name} ({scope})" if scope else (name or "engagement")
        line = f"Sync: {head} — all clear: nothing to collect, review, retry or chase."
        if warnings:
            line += "  [" + "; ".join(warnings) + "]"
        return line

    lines: list[str] = []
    head = f"{name} ({scope})" if scope else (name or "engagement")
    lines.append(f"Sync — {head}")

    lines.append("")
    lines.append(f"(a) Merged results not yet collected: {len(results)}")
    for r in results:
        suffix = f" — {r['title']}" if r["title"] else ""
        lines.append(f"    • {r['id']}{suffix}   (run /collect {r['id']})")
    if not results:
        lines.append("    • none")

    lines.append("")
    lines.append(f"(b) PRs awaiting your review: {len(prs)}")
    for p in prs:
        tier = f" [tier:{p['tier']}]" if p["tier"] else ""
        title = f" — {p['title']}" if p["title"] else ""
        lines.append(f"    • #{p['number']} by @{p['author']}{tier}{title}")
    if not prs:
        lines.append("    • none")

    lines.append("")
    lines.append(f"(c) Packets returned to the queue: {len(returned)}")
    for r in returned:
        note = f" — {r['note']}" if r["note"] else ""
        lines.append(f"    • {r['id']} (retries={r['retries']}){note}")
    if not returned:
        lines.append("    • none")

    lines.append("")
    lines.append(f"(d) Claims in flight: {len(claims)}")
    for c in claims:
        flag = "  ⚠ stale (>6h)" if c["stale"] else ""
        lines.append(f"    • {c['id']} — {c['agent']}, {c['age']}{flag}")
    if not claims:
        lines.append("    • none")

    if warnings:
        lines.append("")
        lines.append("Notes:")
        for w in warnings:
            lines.append(f"    • {w}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    remote = "ensemble"   # the remote /tether binds to the engagement repo (both tether modes)
    no_fetch = False
    for arg in argv[1:]:
        if arg in ("--no-fetch", "-n"):
            no_fetch = True
        elif arg.startswith("--remote="):
            remote = arg.split("=", 1)[1] or "ensemble"
        elif arg in ("-h", "--help"):
            print(
                "usage: sync.py [--no-fetch] [--remote=<name>]\n"
                "  Read-only /sync report for the current tethered engagement repo.",
            )
            return 0
        else:
            _err(f"ignoring unknown argument: {arg}")

    if not _have("git"):
        _err("required command 'git' not found. Install git — https://git-scm.com/downloads")
        return 1

    try:
        root = str(e.find_repo_root())
        proj = e.require_tethered(root)
    except e.EnsembleError as exc:
        _err(str(exc))
        return 1

    name = str(proj.get("name") or "")
    scope = str(proj.get("scope_tag") or "")

    warnings: list[str] = []
    if no_fetch:
        warnings.append("--no-fetch: reporting against local refs without fetching.")
    else:
        warnings.extend(sync_branches(root, remote))

    main_ref = _ref(root, remote, MAIN)
    queue_ref = _ref(root, remote, QUEUE)
    if not main_ref:
        warnings.append("no 'main' ref available locally — results may be incomplete.")
    if not queue_ref:
        warnings.append("no 'queue' ref available locally — queue items may be incomplete.")

    try:
        results = uncollected_results(root, main_ref, scope)
    except e.EnsembleError as exc:
        results = []
        warnings.append(f"could not read collected state: {exc}")

    prs, pr_warn = review_requested_prs(root)
    if pr_warn:
        warnings.append(pr_warn)

    returned = returned_packets(root, queue_ref, scope)
    claims = claims_in_flight(root, queue_ref)

    print(render(name, scope, results, prs, returned, claims, warnings))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(130)
