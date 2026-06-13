#!/usr/bin/env bash
# publish_presentation.sh — /publish-presentation : publish a finished conference
# deck (a sas-presentation reveal.js deck) to the SAS-AM presentations container, so
# it goes live in the team.sas-am.com content library alongside maximoLive2025 etc.
#
# Unlike /handoff (work FOR the fleet) and /submit (your work INTO an engagement),
# this is a DIRECT publish to the contentLibrary container's API over Tailscale —
# no engagement repo, no GitHub control plane, no poller. It flattens the deck to a
# single self-contained HTML, runs warn-only brand/QA lints, then POSTs it.
#
# Usage (the SKILL.md interviews + confirms, then calls us):
#   publish_presentation.sh --name "<deck title>" \
#       [--deck <path>]                 (a .html file or a deck dir; else autodetect cwd) \
#       [--event "<audience/event>"]    (the 'client' field, e.g. "AMPEAK 2026"; default Conference) \
#       [--summary "<one paragraph>"] \
#       [--tags "a,b,c"] \
#       [--author "<name>"]             (default: gh user name / git user.name) \
#       [--status draft|delivered]      (default draft) \
#       [--endpoint <url>]              (default: ~/.ensemble config or the baked tailnet URL) \
#       [--dry-run]                     (flatten + QA + show the target; do NOT publish)
#
# Australian English. Never prints secrets. The endpoint is reachable on the tailnet
# only (Tailscale is the trust boundary, same as the data plane).
set -euo pipefail

_LIB="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../_lib" && pwd)"
# shellcheck source=/dev/null
. "$_LIB/ensemble_common.sh"
HERE="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

ens_have python3
ens_have curl

# Baked default endpoint: this host's Tailscale MagicDNS name + the contentLibrary port.
ENDPOINT_DEFAULT="http://cortex-t4.tail060c48.ts.net:8081"

# --- args --------------------------------------------------------------------
NAME="" DECK="" EVENT="" SUMMARY="" TAGS="" AUTHOR="" STATUS="draft" ENDPOINT="" DRY=0
usage() { awk 'NR>=2 && /^#/ {sub(/^# ?/, ""); print; next} NR>=2 {exit}' "${BASH_SOURCE[0]}"; }
while [ "$#" -gt 0 ]; do
  case "$1" in
    --name)     NAME="${2-}"; shift 2 ;;
    --deck)     DECK="${2-}"; shift 2 ;;
    --event|--client) EVENT="${2-}"; shift 2 ;;
    --summary)  SUMMARY="${2-}"; shift 2 ;;
    --tags)     TAGS="${2-}"; shift 2 ;;
    --author)   AUTHOR="${2-}"; shift 2 ;;
    --status)   STATUS="${2-}"; shift 2 ;;
    --endpoint) ENDPOINT="${2-}"; shift 2 ;;
    --dry-run)  DRY=1; shift ;;
    -h|--help)  usage; exit 0 ;;
    *) ens_die "unknown argument: $1 (see --help)" ;;
  esac
done

[ -n "$NAME" ] || ens_die "a --name is required (the deck title, e.g. \"Edge Intelligence for Rail\")."
case "$STATUS" in
  draft)     STATUS_LABEL="Draft";     STATUS_TONE="draft" ;;
  delivered) STATUS_LABEL="Delivered"; STATUS_TONE="ready" ;;
  *) ens_die "invalid --status '$STATUS' (use draft or delivered)." ;;
esac
[ -n "$EVENT" ] || EVENT="Conference"

# --- resolve the deck HTML ---------------------------------------------------
# Accept a file directly, or find the entry HTML inside a deck directory.
resolve_deck() {
  local d="$1"
  if [ -n "$d" ] && [ -f "$d" ]; then printf '%s\n' "$d"; return 0; fi
  local dir="${d:-.}"
  [ -d "$dir" ] || return 1
  local c
  for c in dist/index.html index.html presentation.html; do
    [ -f "$dir/$c" ] && { printf '%s\n' "$dir/$c"; return 0; }
  done
  local html cnt
  html="$(find "$dir" -maxdepth 1 -name '*.html' 2>/dev/null)"
  cnt="$(printf '%s\n' "$html" | grep -c . || true)"
  if [ "$cnt" = "1" ]; then printf '%s\n' "$html"; return 0; fi
  return 1
}
DECK_HTML="$(resolve_deck "$DECK")" \
  || ens_die "could not find a deck to publish. Pass --deck <file.html|dir>, or run from the deck folder (looked for dist/index.html, index.html, presentation.html, or a single *.html)."
[ -f "$DECK_HTML" ] || ens_die "deck not found: $DECK_HTML"

# --- author + date -----------------------------------------------------------
if [ -z "$AUTHOR" ] && command -v gh >/dev/null 2>&1; then
  AUTHOR="$(gh api user --jq '.name // .login' 2>/dev/null || true)"
fi
[ -n "$AUTHOR" ] || AUTHOR="$(git config user.name 2>/dev/null || true)"
[ -n "$AUTHOR" ] || ens_die "could not determine the author — pass --author \"<name>\" (or set git user.name / gh auth login)."
TODAY="$(date -u +%Y-%m-%d)"

# --- endpoint (explicit > ~/.ensemble config > baked default, persisted) -----
if [ -z "$ENDPOINT" ]; then
  ENDPOINT="$(python3 - "$ENDPOINT_DEFAULT" <<'PY'
import json, os, sys
default = sys.argv[1]
p = os.path.expanduser("~/.ensemble/config.json")
try:
    cfg = json.load(open(p)) if os.path.exists(p) else {}
except Exception:
    cfg = {}
val = (cfg.get("presentations_endpoint") or "").strip()
if not val:
    val = default
    try:  # persist so it is discoverable + overridable later
        os.makedirs(os.path.dirname(p), exist_ok=True)
        cfg["presentations_endpoint"] = val
        json.dump(cfg, open(p, "w"), indent=2)
        os.chmod(p, 0o600)
    except Exception:
        pass
print(val.rstrip("/"))
PY
)"
fi
ENDPOINT="${ENDPOINT%/}"

# --- flatten to a single self-contained HTML ---------------------------------
TMPDIR_PP="$(mktemp -d "${TMPDIR:-/tmp}/ensemble-pubpres.XXXXXX")"
trap 'rm -rf "$TMPDIR_PP"' EXIT
FLAT="$TMPDIR_PP/presentation.html"

FLAT_REPORT="$(python3 "$HERE/flatten_assets.py" "$DECK_HTML" "$FLAT")" \
  || ens_die "failed to flatten the deck assets — see the error above."
{
  printf 'ensemble: flattened %s -> self-contained HTML (%s bytes).\n' "$DECK_HTML" \
    "$(python3 -c 'import json,sys;print(json.load(sys.stdin).get("bytes","?"))' <<<"$FLAT_REPORT")"
  python3 - <<PY
import json
r = json.loads('''$FLAT_REPORT''')
inl, sk, rem = r.get("inlined", []), r.get("skipped", []), r.get("remote_kept", 0)
print(f"ensemble:   inlined {len(inl)} local asset(s); kept {rem} remote/CDN ref(s).")
if sk:
    print("ensemble:   could NOT inline (left as-is — may 404 on the portal):")
    for s in sk[:10]:
        print(f"ensemble:     - {s}")
PY
} >&2

# --- QA (warn-only; never blocks) --------------------------------------------
{
  printf 'ensemble: QA (advisory — publishing proceeds regardless):\n'
  python3 "$HERE/presentation_qa.py" "$FLAT" | while IFS=$'\t' read -r sev msg; do
    printf 'ensemble:   [%s] %s\n' "$sev" "$msg"
  done
} >&2

# --- reachability pre-flight -------------------------------------------------
if ! curl -fsS --max-time 6 "$ENDPOINT/api/catalog" >/dev/null 2>&1; then
  ens_die "cannot reach the presentations endpoint ($ENDPOINT). Is Tailscale up? Check 'tailscale status', or pass --endpoint. (The contentLibrary API is tailnet-only.)"
fi

# Predict the published id (mirrors the server's slugify) for messaging/collision hint.
PRED_ID="$(python3 - "$NAME" <<'PY'
import re, sys
t = sys.argv[1].lower()
t = re.sub(r"[^\w\s-]", "", t)
t = re.sub(r"[\s_-]+", "-", t).strip("-")
print(t)
PY
)"
if curl -fsS --max-time 6 "$ENDPOINT/api/catalog" 2>/dev/null \
    | python3 -c 'import json,sys; ids=[e.get("id") for e in json.load(sys.stdin)]; sys.exit(0 if sys.argv[1] in ids else 1)' "$PRED_ID" 2>/dev/null; then
  ens_die "a deck with id '$PRED_ID' is already in the catalogue. The publish API cannot overwrite — choose a different --name (e.g. add a year or 'v2')."
fi

# --- dry run stops here ------------------------------------------------------
if [ "$DRY" -eq 1 ]; then
  {
    printf '\nensemble: --dry-run — NOT publishing. Would POST to:\n'
    printf 'ensemble:   %s/api/presentations/create\n' "$ENDPOINT"
    printf 'ensemble:   name="%s" event="%s" author="%s" status=%s id=%s\n' "$NAME" "$EVENT" "$AUTHOR" "$STATUS" "$PRED_ID"
    printf 'ensemble:   flattened deck: %s\n' "$FLAT"
  } >&2
  echo "$PRED_ID"; exit 0
fi

# --- publish (multipart; the deck file is saved as presentation.html) --------
RESP="$TMPDIR_PP/resp.json"
HTTP="$(curl -sS -o "$RESP" -w '%{http_code}' --max-time 120 \
  -F "name=$NAME" \
  -F "type=Presentation" \
  -F "client=$EVENT" \
  -F "author=$AUTHOR" \
  -F "summary=$SUMMARY" \
  -F "tags=$TAGS" \
  -F "createdDate=$TODAY" \
  -F "lastUpdated=$TODAY" \
  -F "statusLabel=$STATUS_LABEL" \
  -F "statusTone=$STATUS_TONE" \
  -F "file=@$FLAT;type=text/html;filename=presentation.html" \
  "$ENDPOINT/api/presentations/create" 2>/dev/null)" \
  || ens_die "the publish request failed to send (network/Tailscale). Endpoint: $ENDPOINT"

if [ "$HTTP" = "201" ]; then
  ID="$(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print(d.get("presentation",{}).get("id",""))' "$RESP" 2>/dev/null)"
  DECK_LINK="$(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print(d.get("presentation",{}).get("links",{}).get("deck",""))' "$RESP" 2>/dev/null)"
  {
    printf '\nensemble: published "%s" to the content library (id: %s).\n' "$NAME" "${ID:-$PRED_ID}"
    printf 'ensemble: live (tailnet, verified): %s%s\n' "$ENDPOINT" "${DECK_LINK:-/presentations/$PRED_ID/presentation.html}"
    printf 'ensemble: it now appears in the team.sas-am.com content-library catalogue.\n'
    printf 'ensemble: status is "%s" — re-run with --status delivered once presented.\n' "$STATUS_LABEL"
  } >&2
  echo "${ID:-$PRED_ID}"; exit 0
fi

# --- error paths -------------------------------------------------------------
ERR="$(python3 -c 'import json,sys
try:
    d=json.load(open(sys.argv[1])); print(d.get("error","") + (": "+d.get("details","") if d.get("details") else ""))
except Exception:
    print("")' "$RESP" 2>/dev/null)"
case "$HTTP" in
  409) ens_die "the contentLibrary already has a deck named \"$NAME\" (HTTP 409). Choose a different --name." ;;
  400) ens_die "the publish API rejected the request (HTTP 400)${ERR:+: $ERR}." ;;
  413) ens_die "the deck is too large for the publish API (HTTP 413). Reduce embedded media or raise the server limit." ;;
  *)   ens_die "publish failed (HTTP ${HTTP:-?})${ERR:+: $ERR}. Endpoint: $ENDPOINT" ;;
esac
