#!/usr/bin/env bash
# tether.sh — /tether <uuid|name>: bind this session to an Ensemble engagement repo.
#
# Steps (see the skill SPEC):
#   1. Ensure ~/.ensemble/registry is a shallow clone/pull of config.json registry_repo.
#   2. Resolve the project by exact uuid OR fuzzy name against registry.json
#      (ambiguous -> list candidates + exit non-zero).
#   3. Bring the engagement repo local:
#        --mode clone   : git clone <repo> into the current directory.
#        --mode remote  : cwd is already a git repo -> git remote add ensemble <url>.
#      Either way: fetch BOTH main and queue; run git lfs install; verify CLAUDE.md
#      at the repo root; HEAD-check the .lfsconfig LFS endpoint over Tailscale
#      (WARN-ONLY if unreachable — the control plane still works).
#   4. Upsert a ~/.ensemble/tethers.json entry.
#   5. Print a one-screen orientation: name, scope_tag, open PRs, inbox depth.
#
# Idempotent and re-runnable. Errors -> stderr + non-zero exit. Never prints secrets.
# Australian English throughout.
set -euo pipefail

_LIB="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../_lib" && pwd)"
# shellcheck source=/dev/null
. "$_LIB/ensemble_common.sh"

HERE="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TETHER_PY="$HERE/tether_state.py"

usage() {
  cat >&2 <<'EOF'
usage: tether.sh --query <uuid|name> --mode <clone|remote> [--dir <target-dir>]

  --query   the project uuid (exact) or name (fuzzy substring) from the registry.
  --mode    clone  : git clone the engagement repo into --dir (default: cwd).
            remote : cwd is already a git repo -> add it as the 'ensemble' remote.
  --dir     working directory (default: current directory).
EOF
  exit 2
}

# --- parse args --------------------------------------------------------------
QUERY="" MODE="" TARGET_DIR=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --query) QUERY="${2:-}"; shift 2 ;;
    --mode)  MODE="${2:-}";  shift 2 ;;
    --dir)   TARGET_DIR="${2:-}"; shift 2 ;;
    -h|--help) usage ;;
    *) ens_die "unknown argument: $1" ;;
  esac
done

[ -n "$QUERY" ] || { printf 'ensemble: --query <uuid|name> is required.\n' >&2; usage; }
case "$MODE" in
  clone|remote) : ;;
  "") printf 'ensemble: --mode <clone|remote> is required (ask the user which they want).\n' >&2; usage ;;
  *)  ens_die "--mode must be 'clone' or 'remote', not '$MODE'." ;;
esac

ens_have git
ens_have python3
# git-lfs is a SOFT dependency: engagement repos are LFS-backed for large files, but
# the control plane (packets, PRs) works without it. Warn rather than fail if absent.
HAS_LFS=0
if command -v git-lfs >/dev/null 2>&1 || git lfs version >/dev/null 2>&1; then
  HAS_LFS=1
else
  printf 'ensemble: WARNING — git-lfs is not installed; large files will not sync. The control plane still works. Install it: https://git-lfs.com\n' >&2
fi

TARGET_DIR="${TARGET_DIR:-$PWD}"
[ -d "$TARGET_DIR" ] || ens_die "target directory does not exist: $TARGET_DIR"
TARGET_DIR="$(CDPATH= cd -- "$TARGET_DIR" && pwd)"

# --- 1) ensure the registry mirror is present + fresh ------------------------
REG_URL="$(ens_config_get registry_repo)" || exit 1
REG_DIR="$(python3 -c 'import ensemble_common as e; print(e.registry_dir())')"

normalise_remote() {
  # Resolve a registry/config remote spec to something git can clone:
  #   - full URL (scheme://… or scp-like git@host:…) or a filesystem path -> used as-is
  #   - bare GitHub 'owner/repo' shorthand                                 -> https URL
  # Only a single-segment owner/repo (no scheme, not a path) is treated as shorthand.
  local spec="$1"
  case "$spec" in
    *://*|*@*:*)         printf '%s\n' "$spec"; return ;;   # URL or scp-like remote
    /*|./*|../*|~*)      printf '%s\n' "$spec"; return ;;   # absolute/relative/home path
  esac
  if printf '%s' "$spec" | grep -Eq '^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$'; then
    printf 'https://github.com/%s.git\n' "$spec"            # bare owner/repo shorthand
  else
    printf '%s\n' "$spec"                                   # anything else: leave untouched
  fi
}
REG_REMOTE="$(normalise_remote "$REG_URL")"

if [ -d "$REG_DIR/.git" ]; then
  printf 'ensemble: refreshing registry mirror (%s)...\n' "$REG_DIR" >&2
  if ! git -C "$REG_DIR" pull --ff-only --depth 1 >/dev/null 2>&1; then
    printf 'ensemble: WARNING — could not refresh the registry mirror; using the cached copy.\n' >&2
  fi
else
  printf 'ensemble: cloning registry mirror...\n' >&2
  rm -rf "$REG_DIR"
  git clone --depth 1 "$REG_REMOTE" "$REG_DIR" >/dev/null 2>&1 \
    || ens_die "could not clone the registry from '$REG_URL'. Check ~/.ensemble/config.json registry_repo and your access."
fi
[ -f "$REG_DIR/registry.json" ] \
  || ens_die "registry.json is missing from the registry mirror at $REG_DIR — is registry_repo correct?"

# --- 2) resolve the project --------------------------------------------------
# resolve prints a TSV line on a unique match; exits non-zero (and explains) otherwise.
set +e
RESOLVED="$(python3 "$TETHER_PY" resolve "$QUERY")"
RC=$?
set -e
[ "$RC" -eq 0 ] || exit "$RC"

IFS=$'\t' read -r P_UUID P_NAME P_SCOPE P_REPO P_STATUS <<EOF
$RESOLVED
EOF
[ -n "$P_UUID" ] || ens_die "internal error: the registry entry has no uuid."
[ -n "$P_REPO" ] || ens_die "the registry entry for '$P_NAME' has no repo URL — cannot tether."
REPO_REMOTE="$(normalise_remote "$P_REPO")"

printf 'ensemble: resolved %s [scope: %s, status: %s]\n' "$P_NAME" "$P_SCOPE" "${P_STATUS:-unknown}" >&2

# --- 3) bring the engagement repo local --------------------------------------
fetch_both_branches() {
  # Fetch main + queue from the 'ensemble' remote (best-effort per branch so a
  # missing queue branch warns rather than fails the tether).
  local repo_dir="$1"
  git -C "$repo_dir" fetch ensemble main >/dev/null 2>&1 \
    || printf 'ensemble: WARNING — could not fetch the main branch.\n' >&2
  if ! git -C "$repo_dir" fetch ensemble queue >/dev/null 2>&1; then
    printf 'ensemble: WARNING — could not fetch the queue branch (the mailbox). It may not exist yet.\n' >&2
  fi
}

if [ "$MODE" = "clone" ]; then
  # Derive the clone target dir from the repo name; idempotent if it already exists.
  REPO_BASE="$(basename "$P_REPO")"; REPO_BASE="${REPO_BASE%.git}"
  REPO_DIR="$TARGET_DIR/$REPO_BASE"
  if [ -d "$REPO_DIR/.git" ]; then
    printf 'ensemble: %s already cloned — reusing it.\n' "$REPO_DIR" >&2
  else
    printf 'ensemble: cloning engagement repo into %s ...\n' "$REPO_DIR" >&2
    git clone "$REPO_REMOTE" "$REPO_DIR" >/dev/null 2>&1 \
      || ens_die "could not clone the engagement repo for '$P_NAME'. Check your access to the repo."
  fi
  # Ensure an 'ensemble' remote exists pointing at the canonical repo URL.
  if git -C "$REPO_DIR" remote get-url ensemble >/dev/null 2>&1; then
    git -C "$REPO_DIR" remote set-url ensemble "$REPO_REMOTE"
  else
    git -C "$REPO_DIR" remote add ensemble "$REPO_REMOTE"
  fi
else
  # remote mode: cwd must already be a git repo; add/update the 'ensemble' remote.
  git -C "$TARGET_DIR" rev-parse --git-dir >/dev/null 2>&1 \
    || ens_die "--mode remote needs the current directory to already be a git repo. Use --mode clone instead."
  REPO_DIR="$(git -C "$TARGET_DIR" rev-parse --show-toplevel)"
  if git -C "$REPO_DIR" remote get-url ensemble >/dev/null 2>&1; then
    printf 'ensemble: updating existing '"'"'ensemble'"'"' remote -> %s\n' "$REPO_REMOTE" >&2
    git -C "$REPO_DIR" remote set-url ensemble "$REPO_REMOTE"
  else
    git -C "$REPO_DIR" remote add ensemble "$REPO_REMOTE"
  fi
fi

fetch_both_branches "$REPO_DIR"

# git lfs install (idempotent; --local so we don't touch the user's global config).
if [ "$HAS_LFS" -eq 1 ]; then
  git -C "$REPO_DIR" lfs install --local >/dev/null 2>&1 \
    || printf 'ensemble: WARNING — git lfs install did not complete; large files may not sync.\n' >&2
fi

# Verify CLAUDE.md is present at the repo root (the engagement operating contract).
if [ ! -f "$REPO_DIR/CLAUDE.md" ]; then
  # In remote mode CLAUDE.md may only exist on the ensemble/main branch.
  if git -C "$REPO_DIR" cat-file -e ensemble/main:CLAUDE.md 2>/dev/null; then
    printf 'ensemble: WARNING — CLAUDE.md is on ensemble/main but not in your working tree (check out main to see it).\n' >&2
  else
    ens_die "CLAUDE.md is missing at the engagement repo root — this does not look like an Ensemble engagement repo."
  fi
fi

# HEAD-check the LFS endpoint from .lfsconfig over Tailscale (WARN-ONLY).
lfs_endpoint_check() {
  local repo_dir="$1" cfg url
  cfg="$repo_dir/.lfsconfig"
  [ -f "$cfg" ] || { printf 'ensemble: note — no .lfsconfig found; skipping the LFS endpoint check.\n' >&2; return 0; }
  url="$(git config -f "$cfg" --get lfs.url 2>/dev/null || true)"
  [ -n "$url" ] || { printf 'ensemble: note — .lfsconfig has no lfs.url; skipping the LFS endpoint check.\n' >&2; return 0; }
  if ! command -v curl >/dev/null 2>&1; then
    printf 'ensemble: note — curl not available; skipping the LFS endpoint reachability check.\n' >&2
    return 0
  fi
  # Reachability only — never print the URL/creds. Warn-only on failure.
  if curl -fsS -I --max-time 8 "$url" >/dev/null 2>&1; then
    printf 'ensemble: LFS endpoint reachable over Tailscale.\n' >&2
  else
    printf 'ensemble: WARNING — the LFS endpoint is unreachable (Tailscale down?). The control plane still works; large-file pulls will fail until it is back.\n' >&2
  fi
}
lfs_endpoint_check "$REPO_DIR"

# --- 4) upsert the tethers.json entry ----------------------------------------
python3 "$TETHER_PY" upsert "$P_UUID" "$P_NAME" "$P_SCOPE" "$P_REPO" "$REPO_DIR" >/dev/null \
  || ens_die "could not record the tether in ~/.ensemble/tethers.json."

# --- 5) one-screen orientation ----------------------------------------------
# Open PRs via gh (best-effort — gh may be absent or unauthenticated).
prs_summary() {
  local repo_dir="$1"
  if ! command -v gh >/dev/null 2>&1; then
    printf '  (install the GitHub CLI to see open PRs)\n'
    return 0
  fi
  local out
  if out="$(gh pr list --repo "$REPO_REMOTE" --state open \
              --json number,title,headRefName \
              --template '{{range .}}  #{{.number}}  {{.title}}  ({{.headRefName}}){{"\n"}}{{end}}' 2>/dev/null)"; then
    if [ -n "$out" ]; then printf '%s' "$out"; else printf '  (none open)\n'; fi
  else
    printf '  (could not list PRs — gh may be unauthenticated)\n'
  fi
}

# Inbox depth: count HX-*.md packets on the queue branch's handoffs/inbox/.
inbox_depth() {
  local repo_dir="$1" count
  count="$(git -C "$repo_dir" ls-tree -r --name-only ensemble/queue 2>/dev/null \
            | grep -E '^handoffs/inbox/HX-.*\.md$' | wc -l | tr -d ' ')" || count=0
  printf '%s' "${count:-0}"
}

DEPTH="$(inbox_depth "$REPO_DIR")"

printf '\n'
printf '════════════════════════════════════════════════════════\n'
printf '  Tethered to: %s\n' "$P_NAME"
printf '  Scope tag  : %s\n' "$P_SCOPE"
printf '  Status     : %s\n' "${P_STATUS:-unknown}"
printf '  Local path : %s\n' "$REPO_DIR"
printf '  Inbox      : %s packet(s) waiting on queue (handoffs/inbox/)\n' "$DEPTH"
printf '────────────────────────────────────────────────────────\n'
printf '  Open PRs:\n'
prs_summary "$REPO_DIR"
printf '════════════════════════════════════════════════════════\n'
printf '\n'
printf 'ensemble: tether complete. Results land via PR into main — only a single packet commit ever goes to the queue branch.\n' >&2
