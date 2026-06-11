#!/usr/bin/env bash
# collect.sh — fetch merged result sets from an engagement's main branch.
#
# Usage:
#   collect.sh [<packet-id>]
#
# With no argument: collect every merged result set under handoffs/outbox/ on main.
# With a packet id (HX-YYYY-MMDD-slug): collect only that result set.
#
# What it does (deterministic — the SKILL.md gathers the optional <id> first):
#   1. Fast-forward-only pull of `main` (the reviewed record). If the mesh is
#      unreachable we say so and carry on against the local checkout of main —
#      never fail hard on a transient network blip.
#   2. Enumerate merged result sets (handoffs/outbox/<id>/) from the committed
#      tree of main — only results that actually landed by PR, not stray local dirs.
#   3. For any Git LFS pointer in a result set, `git lfs pull --include=<paths>`
#      then VERIFY the materialised file's sha256 against the pointer's oid. If the
#      LFS mesh is unreachable, report it and list what was skipped (no hard fail).
#   4. Record each collected result into ~/.ensemble/collected.json
#      (id, engagement, collected_at, paths) — idempotent upsert by id.
#   5. Summarise each result's summary.md to stdout for the session.
#
# Tooling: bash + python3 (stdlib) + git (+ git-lfs when LFS pointers are present).
# Idempotent and re-runnable. Errors print to stderr and exit non-zero. Never prints
# secrets. All user-facing strings use Australian English.
set -euo pipefail

_LIB="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../_lib" && pwd)"
# shellcheck source=/dev/null
. "$_LIB/ensemble_common.sh"

HERE="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

ens_have git
ens_have python3

WANT_ID="${1:-}"

# Must be inside a tethered engagement repo — collecting mutates ~/.ensemble state
# against this engagement, so refuse to guess which repo we mean.
ROOT="$(ens_require_tethered)"

# --- 1. fast-forward-only pull of main ---------------------------------------
# We bring main up to date so we see freshly-merged results. ff-only guarantees we
# never rewrite or merge local work into the reviewed record. A network failure is
# reported, not fatal — we still collect whatever already exists locally on main.
MAIN_SYNCED=0
MAIN_NOTE=""
if git -C "$ROOT" rev-parse --verify --quiet main >/dev/null 2>&1; then
  if git -C "$ROOT" fetch --quiet ensemble main >/dev/null 2>&1; then
    # Bring the local main ref forward without disturbing the current checkout.
    cur_branch="$(git -C "$ROOT" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
    if [ "$cur_branch" = "main" ]; then
      if git -C "$ROOT" merge --ff-only --quiet FETCH_HEAD >/dev/null 2>&1; then
        MAIN_SYNCED=1
      else
        MAIN_NOTE="local main is not a fast-forward of ensemble/main — collecting from local main."
      fi
    else
      # Not on main: update the main ref in place (ff-only) without checking it out.
      if git -C "$ROOT" fetch --quiet ensemble main:main >/dev/null 2>&1; then
        MAIN_SYNCED=1
      else
        MAIN_NOTE="could not fast-forward the local main ref — collecting from its current tip."
      fi
    fi
  else
    MAIN_NOTE="could not reach the ensemble remote to refresh main (mesh unreachable?) — collecting from local main."
  fi
else
  MAIN_NOTE="no local 'main' branch in this repo — nothing merged to collect yet."
fi

if [ -n "$MAIN_NOTE" ]; then
  printf 'ensemble: %s\n' "$MAIN_NOTE" >&2
fi

# --- 2..5. delegate the result-set logic + state I/O to the python half ------
# Python owns: enumerating merged result sets from `main`, LFS pointer detection +
# sha256 verification, collected.json upsert, and the summary.md print. It reuses
# the shared lib for repo/project resolution and atomic state writes.
exec python3 "$HERE/collect_impl.py" --root "$ROOT" --main-synced "$MAIN_SYNCED" ${WANT_ID:+--id "$WANT_ID"}
