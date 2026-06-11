---
name: status
description: Registry-wide Ensemble status across every tethered engagement — open packets, claims with age, open PRs grouped by review tier, and the last poll heartbeat. Use when the user asks "where do things stand", "/status", "what's in flight", "any pending PRs", or wants a one-shot health view across all their tethered projects.
---

# Ensemble `/status`

A **read-only**, registry-wide view across **all** tethered engagements (from
`~/.ensemble/tethers.json`). It never mutates an engagement repo or any
`~/.ensemble` state, and you do **not** need to be inside an engagement repo to run
it. For each tethered engagement it reports:

- **Open packets** — count of packets waiting on the `queue` branch under
  `handoffs/inbox/`.
- **Claims + age** — packets a poller has picked up, under
  `handoffs/claimed/<agentId>/`, with how long ago each was claimed.
- **Open PRs by tier** — open pull requests into `main`, grouped by each PR's
  `review_tier` (`auto` / `light` / `full` / `founder`), read from the PR head's
  `handoffs/outbox/<id>/packet.md`.
- **Last poll heartbeat** — the most recent Ensemble poll from
  `~/.ensemble/registry/heartbeat.json` (timestamp + repos polled + any errors).

It tolerates engagements whose local clone is not present (skips them with a note),
a missing `queue` branch, and a `gh` CLI that is unavailable or unauthenticated
(PR data is reported as unavailable rather than failing the run).

## When to use it

Run this whenever the user wants a cross-engagement snapshot: "where do things
stand", "what's pending review", "any claims stuck", "show me the queue", or simply
`/status`. It is the registry-wide companion to the per-engagement skills.

## How to run it

This skill takes **no inputs from the session** — there is nothing to gather. Just
invoke the wrapper script in this folder, which sources the shared lib and delegates
to the deterministic Python engine:

```bash
bash status.sh
```

For a machine-readable report (e.g. to summarise or post-process), pass `--json`:

```bash
bash status.sh --json
```

After running, present the report to the user in plain Australian English. If any
engagement was skipped (clone missing), surface that and suggest re-tethering or
cloning it. If the heartbeat is stale or carries errors, call that out. If PR data
was skipped because `gh` is unauthenticated, tell the user to run `gh auth login`.

## Notes

- **Read-only and idempotent** — safe to run repeatedly; it changes nothing.
- Freshness of inbox/claims depends on the local clone: the script reads
  `origin/queue` when present (then falls back to a local `queue`). If counts look
  stale, suggest a `git fetch` in that engagement's clone first.
- No secrets or tokens are ever printed.
