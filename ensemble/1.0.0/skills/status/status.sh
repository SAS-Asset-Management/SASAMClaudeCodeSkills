#!/usr/bin/env bash
# status.sh — registry-wide Ensemble status across all tethered engagements.
#
# Read-only. Does NOT mutate any engagement repo or ~/.ensemble state, and does not
# require being run from inside an engagement repo — it iterates the tethers recorded
# in ~/.ensemble/tethers.json. Engagements whose local clone is missing are skipped
# with a note; missing 'queue' branches and an unavailable/unauthenticated gh CLI are
# tolerated (the affected sections report as unavailable rather than failing the run).
#
# All deterministic work lives in ensemble_status.py beside this file; this wrapper
# just verifies tooling and delegates. Sourcing the shared lib puts the lib dir on
# PYTHONPATH so the python engine can `import ensemble_common`.
#
# Usage:
#   status.sh            # formatted text report
#   status.sh --json     # machine-readable JSON
#
# Australian English in all output. Errors go to stderr with a non-zero exit.
set -euo pipefail

HERE="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
_LIB="$(CDPATH= cd -- "$HERE/../_lib" && pwd)"
# shellcheck source=/dev/null
. "$_LIB/ensemble_common.sh"

# Required tooling. git/gh let us read queue branches + open PRs; the report still
# renders (with notes) if a per-repo git/gh call fails, but the binaries must exist.
ens_have python3
ens_have git

exec python3 "$HERE/ensemble_status.py" "$@"
