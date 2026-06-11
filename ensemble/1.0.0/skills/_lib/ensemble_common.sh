# ensemble_common.sh — shared bash helpers for the Ensemble consultant skills.
#
# Source this from a skill script:
#
#     _LIB="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../_lib" && pwd)"
#     # shellcheck source=/dev/null
#     . "$_LIB/ensemble_common.sh"
#
# Tooling: bash + python3 (stdlib) + git (+ gh / git-lfs where a skill needs them).
# No pip installs, no other deps. All user-facing strings use Australian English.
# Functions print errors to stderr and exit non-zero; they NEVER print secrets.
#
# The python half of the lib (ensemble_common.py) lives beside this file and owns
# packet parsing, schema validation, and the JSON state read/write — bash shells out
# to it rather than re-implementing that logic.

# --- internal: locate this lib dir + the python helper -----------------------
# (resolved once at source-time; safe under `set -u`)
ENS_LIB_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]:-$0}")" && pwd)"
ENS_PY="$ENS_LIB_DIR/ensemble_common.py"

# ens_die <msg...>
#   Print "ensemble: <msg>" to stderr and exit 1. Use for every fatal path.
ens_die() {
  printf 'ensemble: %s\n' "$*" >&2
  exit 1
}

# ens_have <cmd>
#   Verify an executable is on PATH; die with a one-line install hint if missing.
#   Returns 0 when present. Known hints: git, gh, git-lfs, python3.
ens_have() {
  local cmd="$1" hint
  if command -v "$cmd" >/dev/null 2>&1; then
    return 0
  fi
  case "$cmd" in
    gh)      hint="install the GitHub CLI — https://cli.github.com" ;;
    git)     hint="install git — https://git-scm.com/downloads" ;;
    git-lfs) hint="install Git LFS then run 'git lfs install' — https://git-lfs.com" ;;
    python3) hint="install Python 3 — https://www.python.org/downloads" ;;
    *)       hint="install '$cmd' and ensure it is on your PATH" ;;
  esac
  ens_die "required command '$cmd' not found. $hint"
}

# ens_home
#   Echo the ~/.ensemble state directory, creating it with mode 0700 if absent.
#   Delegates to the python lib so bash + python agree on the location/permissions.
ens_home() {
  ens_have python3
  python3 -c 'import ensemble_common as e; print(e.ensemble_home())' \
    || ens_die "could not create ~/.ensemble state directory"
}

# ens_repo_root
#   Echo the engagement repo root, or die. Prefers `git rev-parse --show-toplevel`;
#   falls back to the python walk-up (which also honours .ensemble/project.json) so
#   this works even outside a git checkout that nonetheless carries project.json.
ens_repo_root() {
  local root
  if command -v git >/dev/null 2>&1; then
    if root="$(git rev-parse --show-toplevel 2>/dev/null)" && [ -n "$root" ]; then
      printf '%s\n' "$root"
      return 0
    fi
  fi
  ens_have python3
  root="$(python3 -c 'import ensemble_common as e; print(e.find_repo_root())' 2>/dev/null)" \
    || ens_die "not inside a git repository (run from within an engagement repo)"
  printf '%s\n' "$root"
}

# ens_require_tethered
#   Die unless .ensemble/project.json exists at the repo root. On success echoes the
#   repo root (handy: ROOT="$(ens_require_tethered)"). Use at the top of any skill
#   that mutates engagement state.
ens_require_tethered() {
  local root
  root="$(ens_repo_root)" || exit 1
  if [ ! -f "$root/.ensemble/project.json" ]; then
    ens_die "not a tethered engagement repo: $root/.ensemble/project.json is missing. Tether this engagement first."
  fi
  printf '%s\n' "$root"
}

# ens_project_field <key>
#   Echo a scalar field from the engagement repo's .ensemble/project.json (via the
#   python lib). Dies if not in a tethered repo. A missing key echoes an empty line.
#   e.g.  scope="$(ens_project_field scope_tag)"
ens_project_field() {
  local key="$1" root val
  [ -n "$key" ] || ens_die "ens_project_field: a project.json key is required"
  root="$(ens_require_tethered)" || exit 1
  ens_have python3
  val="$(python3 -c '
import sys, ensemble_common as e
v = e.project_field(sys.argv[1], sys.argv[2])
print("" if v is None else v)
' "$key" "$root" 2>/dev/null)" \
    || ens_die "could not read '$key' from $root/.ensemble/project.json"
  printf '%s\n' "$val"
}

# ens_config_get <key>
#   Echo a single key from ~/.ensemble/config.json. If config.json is absent OR the
#   key is missing/empty, print a one-line hint to set it (to stderr) and exit
#   non-zero — so a skill needing e.g. registry_repo fails loudly and actionably.
#   e.g.  reg="$(ens_config_get registry_repo)" || exit 1
ens_config_get() {
  local key="$1" val
  [ -n "$key" ] || ens_die "ens_config_get: a config key is required"
  ens_have python3
  val="$(python3 -c '
import sys, ensemble_common as e
v = e.config_get(sys.argv[1])
print("" if v is None else v)
' "$key" 2>/dev/null)" \
    || ens_die "could not read ~/.ensemble/config.json"
  if [ -z "$val" ]; then
    printf 'ensemble: %s is not set in ~/.ensemble/config.json.\n' "$key" >&2
    printf "ensemble: set it, e.g.  python3 -c 'import json,os;p=os.path.expanduser(\"~/.ensemble/config.json\");d=json.load(open(p)) if os.path.exists(p) else {};d[\"%s\"]=\"<value>\";json.dump(d,open(p,\"w\"),indent=2)'\n" "$key" >&2
    exit 1
  fi
  printf '%s\n' "$val"
}

# --- make the python lib importable for any `python3 -c` in a sourcing skill --
# Prepend the lib dir to PYTHONPATH so `import ensemble_common` resolves both for
# the helpers above and for ad-hoc python in the consuming skill.
case ":${PYTHONPATH:-}:" in
  *":$ENS_LIB_DIR:"*) : ;;
  *) export PYTHONPATH="$ENS_LIB_DIR${PYTHONPATH:+:$PYTHONPATH}" ;;
esac
