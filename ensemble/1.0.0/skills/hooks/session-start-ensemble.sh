#!/usr/bin/env bash
# session-start-ensemble.sh — Ensemble SessionStart hook.
#
# Fires when a Claude Code session starts. If — and ONLY if — the current working
# directory is a tethered Ensemble engagement repo (i.e. `.ensemble/project.json`
# is present), it prints a short, READ-ONLY `/sync` report so the consultant opens
# the session already knowing the engagement's mailbox + registry state.
#
# Hard guarantees (so a bad network or odd checkout never costs you the session):
#   * Total wall-clock budget ~5s, enforced by ONE outer `timeout` around the whole
#     worker (not a fragile self-kill). `timeout --kill-after` guarantees the child
#     process group dies even if a hung `git`/`/sync` ignores TERM. On budget
#     exhaustion the hook exits SILENTLY — no partial spew, no error.
#   * It NEVER fails the session: on any error, missing tool, non-engagement cwd, or
#     timeout it exits 0 with no output. A SessionStart hook must not block the prompt.
#   * It is strictly read-only: no fetch that writes, no commit, no packet, no state
#     mutation. It only reads what is already on disk + one quick, hard-timed remote
#     peek (`git ls-remote`, which never touches the working tree).
#   * It NEVER prints secrets/tokens. Only repo names, scope tags, and counts.
#
# Australian English throughout. Registers via settings.json — see README.md.
#
# Design: this single file is both the WRAPPER and the WORKER. The wrapper re-execs
# itself under `timeout`, setting ENSEMBLE_HOOK_WORKER=1, so the entire data-gather
# runs inside one hard cap. The worker buffers all output and only emits it once it
# has completed within budget — a half-finished, truncated report is never shown.

# Intentionally NOT `set -e`: a SessionStart hook must degrade to silence, never
# abort the session with a non-zero stage. We guard each step and always exit 0.
set -u

# Total budget (seconds) for the whole hook. `timeout` sends TERM at the budget,
# then SIGKILL 1s later if a child wedged.
ENS_HOOK_BUDGET="${ENSEMBLE_HOOK_BUDGET:-5}"
# Per-network-call budget — kept below the total so a single call cannot starve us.
ENS_NET_TIMEOUT="${ENSEMBLE_HOOK_NET_TIMEOUT:-3}"

# ---------------------------------------------------------------------------------
# WRAPPER: re-exec the worker under a single hard timeout, swallow any failure.
# ---------------------------------------------------------------------------------
if [ "${ENSEMBLE_HOOK_WORKER:-0}" != "1" ]; then
  SELF="${BASH_SOURCE[0]:-$0}"
  if ! command -v timeout >/dev/null 2>&1; then
    # No `timeout` available (unlikely on Linux). Fail safe: do nothing rather than
    # risk delaying the session on a bad network.
    exit 0
  fi
  # --kill-after gives a wedged child 1s after TERM before SIGKILL. We discard the
  # worker's exit status entirely: timeout/non-zero/etc. all collapse to a clean 0.
  ENSEMBLE_HOOK_WORKER=1 \
    timeout --kill-after=1 "$ENS_HOOK_BUDGET" bash "$SELF" 2>/dev/null || true
  exit 0
fi

# ---------------------------------------------------------------------------------
# WORKER (runs only when ENSEMBLE_HOOK_WORKER=1, under the wrapper's timeout).
# Buffers the whole report in $REPORT and prints it atomically at the very end, so
# a timeout mid-gather shows nothing rather than a truncated line.
# ---------------------------------------------------------------------------------
REPORT=""

# --- 1. Locate ourselves + the shared lib ---------------------------------------
HOOK_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]:-$0}")" && pwd 2>/dev/null)" || exit 0
LIB="$HOOK_DIR/../_lib/ensemble_common.sh"
SYNC_DIR="$HOOK_DIR/../sync"   # sibling /sync skill, if installed

# Sourcing the lib is best-effort: if it is missing we still want a silent, safe
# exit rather than a stack trace at session start. We use the lib only for its
# PYTHONPATH wiring (so `import ensemble_common` resolves) — never its ens_die*
# helpers, which exit non-zero (forbidden here).
if [ -r "$LIB" ]; then
  # shellcheck source=/dev/null
  . "$LIB" 2>/dev/null || exit 0
else
  # Fall back to wiring PYTHONPATH ourselves so the python helpers still import.
  export PYTHONPATH="$HOOK_DIR/../_lib${PYTHONPATH:+:$PYTHONPATH}"
fi

# Without python3 we cannot read project.json / heartbeat — stay quiet.
command -v python3 >/dev/null 2>&1 || exit 0

# --- 2. Are we in a tethered engagement repo? (read-only, fast, local) ----------
# Resolve the repo root from cwd WITHOUT dying (the lib's ens_* helpers exit on
# failure; here we must never exit non-zero). Pure-stdlib walk-up via the python
# lib, which honours .ensemble/project.json.
ROOT="$(python3 -c 'import ensemble_common as e
try:
    print(e.find_repo_root())
except Exception:
    pass' 2>/dev/null)" || exit 0

[ -n "$ROOT" ] || exit 0
[ -f "$ROOT/.ensemble/project.json" ] || exit 0   # not tethered → silent no-op

# --- 3. Prefer the real /sync skill's report, so we never diverge from /sync ----
# The sibling /sync skill (sync.sh → sync.py) owns the canonical report and is
# read-only by contract. We invoke it with `--no-fetch`: that makes the report
# NETWORK-FREE (it renders against local refs only), which is exactly what a
# SessionStart hook wants — fast, no tunnel round-trip, no risk of blocking the
# prompt. The consultant gets the full fetched picture when they later run /sync
# themselves. Still time-boxed (belt-and-braces) so even a wedged sync can't stall.
SYNC_SH="$SYNC_DIR/sync.sh"
if [ -r "$SYNC_SH" ]; then
  if sync_out="$(timeout "$ENS_NET_TIMEOUT" bash "$SYNC_SH" --no-fetch 2>/dev/null)" \
       && [ -n "$sync_out" ]; then
    printf '%s\n' "$sync_out"
    exit 0
  fi
fi

# --- 4. Fallback: self-contained read-only summary ------------------------------
# Used until the /sync skill is installed beside us. Reports only what is safe and
# fast: the engagement identity from project.json, local mailbox counts (queue
# branch) + outbox results (main), and the cached registry heartbeat freshness.
# A single, hard-timed `git ls-remote` is the ONLY network touch.

# 4a. Engagement identity (local file read — no network). Tab-separated so names
# with spaces survive intact.
ID_LINE="$(python3 -c '
import sys, ensemble_common as e
try:
    p = e.load_project(sys.argv[1])
except Exception:
    sys.exit(0)
def s(v):
    return (str(v) if v not in (None, "") else "-")
print("\t".join([s(p.get("name")), s(p.get("scope_tag"))]))
' "$ROOT" 2>/dev/null)" || ID_LINE=""

ENG_NAME="${ID_LINE%%$'\t'*}"
SCOPE="${ID_LINE##*$'\t'}"
# Nothing parsed → say nothing.
[ -n "${SCOPE:-}" ] && [ "${SCOPE:-}" != "-" ] || exit 0

# 4b. Local mailbox + outbox counts. Working-tree reads only; no network.
# `wc -l` always exits 0 and prints a single number (0 for an empty/absent dir),
# avoiding the `grep -c` "prints 0 but exits 1" trap that doubled the count.
ens_count() {  # ens_count <find-args...> — count matching lines, clean single int
  find "$@" 2>/dev/null | wc -l | tr -d ' \t\n'
}
N_INBOX="$(ens_count "$ROOT/handoffs/inbox" -type f -name '*.md')"
N_CLAIMED="$(ens_count "$ROOT/handoffs/claimed" -type f -name '*.md')"
N_OUTBOX="$(ens_count "$ROOT/handoffs/outbox" -mindepth 1 -maxdepth 1 -type d)"
: "${N_INBOX:=0}" "${N_CLAIMED:=0}" "${N_OUTBOX:=0}"

# 4c. Registry heartbeat freshness (local read of the cached heartbeat.json — the
# poller's last self-report; NO network). Tells the consultant whether the Ensemble
# is currently polling.
HEARTBEAT_LINE="$(python3 -c '
import datetime as dt, ensemble_common as e
try:
    hb = e.load_json(e.heartbeat_path(), default=None)
except Exception:
    hb = None
if not isinstance(hb, dict) or not hb.get("ts"):
    print("registry heartbeat: none cached (run /sync to refresh)")
    raise SystemExit(0)
ts = str(hb.get("ts"))
errs = hb.get("errors") or []
nerr = len(errs) if isinstance(errs, list) else 0
age = ""
try:
    t = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc) if t.tzinfo else dt.datetime.now()
    secs = max(0.0, (now - t).total_seconds())
    mins = int(secs // 60)
    age = f", {mins} min ago" if mins else ", just now"
except Exception:
    pass
tail = f"; {nerr} error(s)" if nerr else ""
print(f"registry heartbeat: {ts}{age}{tail}")
' 2>/dev/null)" || HEARTBEAT_LINE=""

# 4d. ONE hard-timed remote peek: does the `queue` mailbox branch exist on the engagement
# remote? `git ls-remote` is read-only and never touches the working tree; the per-call
# timeout is the network guard. Skipped silently if git is absent or it stalls.
REMOTE_LINE=""
if command -v git >/dev/null 2>&1 && git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  if lsr="$(timeout "$ENS_NET_TIMEOUT" git -C "$ROOT" ls-remote --heads ensemble queue 2>/dev/null)"; then
    if [ -n "$lsr" ]; then
      REMOTE_LINE="queue branch: present on the engagement remote"
    else
      REMOTE_LINE="queue branch: not yet created on the engagement remote"
    fi
  fi
fi

# --- 5. Assemble the report buffer, then emit it once (atomic) ------------------
# Plain text; no colour codes (hook output may be captured/piped). Australian
# English. Nothing here is a secret.
ENG_NAME_DISP="${ENG_NAME:--}"
REPORT+="Ensemble — engagement sync (read-only)"$'\n'
REPORT+="  engagement : ${ENG_NAME_DISP}  [${SCOPE}]"$'\n'
REPORT+="  mailbox    : ${N_INBOX} in inbox · ${N_CLAIMED} claimed · ${N_OUTBOX} result(s) in outbox"$'\n'
[ -n "$HEARTBEAT_LINE" ] && REPORT+="  ${HEARTBEAT_LINE}"$'\n'
[ -n "$REMOTE_LINE" ]   && REPORT+="  ${REMOTE_LINE}"$'\n'
REPORT+="  run /sync for the full report · /status for this engagement"$'\n'

printf '%s' "$REPORT"
exit 0
