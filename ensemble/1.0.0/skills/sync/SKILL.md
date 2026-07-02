---
name: sync
description: Read-only catch-up for the current Ensemble engagement repo — fetches main + queue and reports merged results to collect, PRs awaiting your review, packets bounced back to the queue, and claims in flight.
---

# Ensemble — `/sync`

Run this when a consultant returns to a tethered engagement repo and wants to know
"what happened while I was away?". It is **read-only and fast**: it fetches and
fast-forwards `main` and `queue`, then prints a four-part catch-up. It never
mutates engagement state, never pushes, and never blocks the session on a slow
network — a degraded fetch or `gh` call is reported inline, not treated as fatal.

This skill is also what the SessionStart hook runs to greet the consultant.

## When to use it

- The user says **"sync"**, "catch me up", "what's waiting on me", "anything to
  collect", "any reviews", or asks for the state of the current engagement.
- At the **start of a session** inside an engagement repo (the hook does this).
- After the Ensemble poller has had time to claim/work a packet you pushed.

Do **not** use it to *fetch deliverables* — that is `/collect`. `/sync` only
*reports* which merged results are uncollected; `/collect` pulls the bytes.

## What it reports (always in this order)

1. **(a) Merged results not yet collected** — result sets under
   `handoffs/outbox/<id>/` on `main` whose `id` is not yet in
   `~/.ensemble/collected.json`. Each is shown with a one-line title from its
   `summary.md` and the exact `/collect <id>` to run.
2. **(b) PRs awaiting your review** — open PRs where you are a requested reviewer
   (`gh pr list --search 'review-requested:@me'`), with number, author and tier.
3. **(c) Packets returned to the queue** — `handoffs/inbox/HX-*.md` on `queue`
   with `retries > 0` or a rejection/janitor note, so you can see what bounced and
   why before re-queuing it.
4. **(d) Claims in flight** — `handoffs/claimed/<agentId>/HX-*.md` on `queue`,
   with the age since the claim commit. Claims older than 6 hours are flagged as
   stale (the janitor's reclaim threshold).

When **all four are empty**, the output is a **single line** — e.g.
`Sync: Transdev ISO 55001 (transdev-iso55001) — all clear: nothing to collect, review, retry or chase.`

## How to run it

1. Confirm the session's working directory is inside a tethered engagement repo
   (one with `.ensemble/project.json`). If you are not sure, just run the script —
   it fails with a clear "tether this engagement first" message via the shared lib.
2. Invoke the wrapper from this folder. No inputs are required:

   ```bash
   bash "$CLAUDE_SKILL_DIR/sync.sh"
   ```

   Optional flags (pass through to `sync.py`):
   - `--no-fetch` — skip the network fetch and report against local refs only
     (use when offline or when you only just fetched).
   - `--remote=<name>` — use a non-default remote (defaults to `ensemble`, the remote `/tether` creates).

3. Relay the script's report to the consultant verbatim, then offer the obvious
   next actions it implies: run `/collect <id>` for any uncollected results, open
   the PRs awaiting review, and re-`/handoff` (or chase) anything bounced back.

## Notes for the assistant

- This is a **read-only** skill. Never let it push, reset, switch branches, or
  edit packets — that is what makes it safe to run unprompted at session start.
- Do not re-implement repo resolution, `project.json` reads, packet front-matter
  parsing, or `~/.ensemble` state access — `sync.sh` sources
  `../_lib/ensemble_common.sh` and `sync.py` imports `ensemble_common`, which own
  all of that.
- If the report carries a `Notes:` section (e.g. "could not fetch", "GitHub CLI
  not found"), surface it plainly — it means part of the picture may be stale, not
  that anything is broken.
