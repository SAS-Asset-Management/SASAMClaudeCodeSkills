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

1. **Which project** — a uuid (exact) or a name (fuzzy substring match). This is the
   `<uuid|name>` the user gave with `/tether`. If they did not give one, ask for it.

2. **Clone or remote?** — You MUST ask this before running, unless the answer is obvious
   from the user's request:
   - **clone** — *"I'm starting fresh."* The skill runs `git clone` of the engagement
     repo into the current directory (or `--dir`). Use this when the current directory is
     **not** already the engagement's checkout.
   - **remote** — *"I'm already in the repo."* The current directory is already a git
     repo and the skill simply adds the engagement as a remote named `ensemble`
     (`git remote add ensemble <url>`). Use this when the user is already inside the
     engagement's working tree (or a sibling clone they want to attach).

   Phrase it plainly, e.g. *"Do you want me to clone the engagement repo here, or are you
   already inside a git repo I should attach as a remote?"*

## How to run it

Once you know the project query and the mode, invoke the script in this folder:

```bash
bash "$SKILL_DIR/tether.sh" --query "<uuid-or-name>" --mode <clone|remote> [--dir <target-dir>]
```

- `--query` — the uuid or name the user supplied (quote it; names can contain spaces).
- `--mode`  — `clone` or `remote`, per the user's answer above.
- `--dir`   — optional; the working directory (defaults to the current directory). Pass it
  only if the user wants the clone/attach to happen somewhere other than the cwd.

The script is **idempotent** — re-running it refreshes the registry, re-fetches `main`
and `queue`, and updates the tether record. It is safe to run again.

### What the script does (deterministic — do not reproduce by hand)

1. Ensures `~/.ensemble/registry` is a shallow clone/pull of `registry_repo` from
   `~/.ensemble/config.json`. (If `registry_repo` is unset it prints a one-line hint and
   exits non-zero — relay that to the user.)
2. Resolves the project: **exact uuid** first, else a **fuzzy** case-insensitive match on
   name/scope_tag. If the query is **ambiguous**, it lists the candidates to stderr and
   exits non-zero — when that happens, show the candidates and ask the user to re-run
   `/tether` with the **exact uuid or full name**.
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

- `0` — tethered successfully.
- `2` — bad/missing arguments (e.g. no `--query`, or `registry_repo` unset).
- `3` — no project in the registry matched the query.
- `4` — the query was ambiguous (candidates listed on stderr).
- other non-zero — a git/clone/access error; relay the stderr message to the user.
