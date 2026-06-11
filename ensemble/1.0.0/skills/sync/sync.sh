#!/usr/bin/env bash
# sync.sh — entry point for the Ensemble /sync skill.
#
# Sources the shared lib (which checks tools, resolves the engagement repo root,
# and — as a source side-effect — prepends _lib to PYTHONPATH so the Python half
# can `import ensemble_common`), then hands off to sync.py for the read-only
# fetch + four-part report. All real logic lives in sync.py; this wrapper only
# guards preconditions so failures are loud and actionable.
#
# Usage:  sync.sh [--no-fetch] [--remote=<name>]
# Read-only and fast — never mutates engagement state, never blocks the session.
set -euo pipefail

_LIB="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../_lib" && pwd)"
# shellcheck source=/dev/null
. "$_LIB/ensemble_common.sh"

# Preconditions (the lib dies with a one-line install hint if a tool is missing).
ens_have git
ens_have python3

# Must be inside a tethered engagement repo (echoes the root; we discard it —
# sync.py re-resolves via the shared lib. This call gives an early, clear failure
# with the lib's standard "tether this engagement first" message).
ens_require_tethered >/dev/null

_HERE="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$_HERE/sync.py" "$@"
