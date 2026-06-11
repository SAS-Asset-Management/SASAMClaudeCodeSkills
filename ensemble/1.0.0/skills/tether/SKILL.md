---
name: tether
description: Bind this session to an Ensemble engagement repo by uuid or name — clone (or remote-add) the repo, fetch main + queue, and print an orientation.
---

# /tether — bind to an Ensemble engagement

Use this skill when a consultant says **"tether to <project>"**, **"/tether <uuid|name>"**,
or otherwise wants to start working on an Ensemble engagement in the current session.
Tethering resolves the project from the shared **registry**, brings the engagement repo
local, and records the binding under `~/.ensemble/tethers.json` so the other Ensemble
skills (collect, packet, etc.) know which engagement you are operating in.

This is the **first** skill a consultant runs for a given engagement.

## What you need from the user

**Do not interrogate the consultant — the skill is built to need almost nothing.**

1. **Which engagement** — a uuid (exact) or a name/scope-tag (fuzzy; punctuation and
   spacing don't matter, so "transurban WCX NCX" resolves "Transurban WCX/NCX"). If the
   user **did not name one**, do NOT ask — run the skill with **no `--query`** and it will
   **list** the engagements they can tether to; show that list and let them pick.

2. **Clone or remote?** — **Do not ask this.** Omit `--mode` and the skill auto-detects:
   if the current directory is already a git repo it attaches the engagement as a remote
   named `ensemble`; otherwise it clones the engagement repo into the current directory.
   Only pass `--mode` if the user explicitly overrides the default.

There is **no SSH-key or registry setup** to do first: the skill defaults the registry to
the SAS-AM shared one and uses the GitHub CLI's credential helper, so a consultant who has
run `gh auth login` can clone private engagement repos over HTTPS with no further config.

## How to run it

```bash
# list the engagements (use when the user didn't name one):
bash "$SKILL_DIR/tether.sh" --list

# tether (mode auto-detected; quote the name — it can contain spaces/punctuation):
bash "$SKILL_DIR/tether.sh" --query "<uuid-or-name>" [--mode <clone|remote>] [--dir <dir>]
```

- `--query` — the uuid or name/scope-tag the user supplied. Omit (or pass `--list`, `*`,
  or `all`) to list available engagements instead of tethering.
- `--mode`  — optional; `clone` or `remote`. Omit to auto-detect (remote if cwd is a git
  repo, else clone).
- `--dir`   — optional; the working directory (defaults to the current directory).

The script is **idempotent** — re-running it refreshes the registry, re-fetches `main`
and `queue`, and updates the tether record. It is safe to run again.

### What the script does (deterministic — do not reproduce by hand)

0. Wires the GitHub CLI as git's HTTPS credential helper (`gh auth setup-git`, best-effort)
   so private engagement repos clone with no SSH key.
1. Ensures `~/.ensemble/registry` is a shallow clone/pull of `registry_repo`. If it's not
   pinned in `~/.ensemble/config.json`, the skill **defaults to the SAS-AM shared registry**
   and records it — no manual setup.
2. If no `--query` (or `--list`/`*`/`all`): **lists the engagements** and exits. Otherwise
   resolves: **exact uuid** first, else a **punctuation-insensitive** match on
   name/scope_tag (spacing/`/`/`-` don't matter). If the query is **ambiguous**, it lists
   the candidates to stderr and exits non-zero — show them and ask the user to re-run with
   the exact uuid or full name.
3. Clones (or `remote add ensemble`) the engagement repo, **fetches both `main` and
   `queue`**, runs `git lfs install`, verifies `CLAUDE.md` at the repo root, and HEAD-checks
   the LFS endpoint from `.lfsconfig` over Tailscale (**warn-only** if unreachable — the
   control plane still works without large-file access).
4. Upserts the entry in `~/.ensemble/tethers.json`.
5. Prints a one-screen orientation: **project name, scope_tag, status, local path, open
   PRs** (`gh pr list`), and **inbox depth** (count of `HX-*.md` packets on `queue`).

## After it runs

- Relay the orientation block to the user (project, scope, inbox depth, open PRs).
- If the script **warned** about the LFS endpoint, tell the user large-file pulls will
  fail until Tailscale is back, but the control plane (packets, PRs) still works.
- Remind the user of the golden rule when they're ready to send work: **the only direct
  push to the engagement is a single packet commit to the `queue` branch (fast-forward
  only)** — results always come back as a **PR into `main`**, never a push to `main`.

## Exit codes

- `0` — tethered successfully, **or** listed the available engagements (no query given).
- `2` — bad arguments (e.g. an invalid `--mode`).
- `3` — no engagement in the registry matched the query.
- `4` — the query was ambiguous (candidates listed on stderr).
- other non-zero — a git/clone/access error; relay the stderr message to the user.
