# Ensemble hooks

Claude Code hook scripts for the Ensemble consultant toolkit. These are **hook
scripts**, not skills — the Claude Code harness runs them automatically on the
configured event (no `SKILL.md`, never invoked by the model).

## `session-start-ensemble.sh` — SessionStart `/sync` greeter

On **session start**, if (and only if) the current working directory is a
**tethered engagement repo** (`.ensemble/project.json` present), this hook prints a
short, **read-only** `/sync` report before the first prompt — so you open the
session already knowing the engagement's mailbox + registry state (uncollected
results, claims in flight, returned packets, review-requested PRs).

It does this by delegating to the sibling `/sync` skill (`../sync/sync.sh
--no-fetch`), which is read-only by contract; `--no-fetch` keeps it **network-free**
so the greeting is instant. If `/sync` is not installed beside it, the hook falls
back to a self-contained local summary (engagement identity, mailbox/outbox counts,
cached registry-heartbeat freshness, and one hard-timed `git ls-remote` peek).

### Guarantees (why it is safe to wire in globally)

- **Never delays the session.** The whole hook runs under a single ~5s `timeout`
  with `--kill-after=1`, so even a hung `git`/`/sync` over a flaky tunnel is killed.
  On budget exhaustion it exits **silently** — no truncated output.
- **Never fails the session.** Any error, missing tool, or non-engagement directory
  results in a clean exit 0 with no output. A SessionStart hook must not block.
- **Strictly read-only.** No fetch-that-writes, no commit, no packet, no state
  mutation. The only network touch is the `/sync --no-fetch` path (none) or a single
  read-only `git ls-remote` in the fallback.
- **Never prints secrets/tokens.** Only repo names, scope tags, and counts.

Tunables via environment (optional): `ENSEMBLE_HOOK_BUDGET` (total seconds, default
`5`), `ENSEMBLE_HOOK_NET_TIMEOUT` (per-call seconds, default `3`).

## Register it as a SessionStart hook

Add a `SessionStart` entry to your Claude Code `settings.json` (user-level
`~/.claude/settings.json`, or project-level `.claude/settings.json`). Use the
**absolute path** to the installed hook:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/home/cortext4/repos/theEnsembles-ensemble-handoff/deploy/skills/ensemble/hooks/session-start-ensemble.sh"
          }
        ]
      }
    ]
  }
}
```

Notes:

- If you install the `ensemble` skill folder elsewhere, point `command` at the
  hook's real absolute path there. The hook locates the shared `_lib` and the
  sibling `/sync` skill **relative to itself**, so the whole `ensemble/` folder must
  be kept together (`hooks/`, `_lib/`, `sync/` as siblings).
- Already have a `SessionStart` block? Append another object to the outer
  `"SessionStart"` array — do not overwrite existing entries.
- Wiring it at the **user** level means it greets you in every engagement repo you
  open and stays silent everywhere else, which is the intended behaviour.

### Verify

```bash
# In a tethered engagement repo → prints a short read-only sync report:
cd /path/to/an-engagement-repo
deploy/skills/ensemble/hooks/session-start-ensemble.sh

# Anywhere else → prints nothing, exits 0:
cd /tmp && /…/hooks/session-start-ensemble.sh ; echo "exit=$?"
```
