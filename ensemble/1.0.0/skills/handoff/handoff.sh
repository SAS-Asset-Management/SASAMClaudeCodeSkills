#!/usr/bin/env bash
# handoff.sh — /handoff : write a handoff task packet and push it to the engagement
# repo's `queue` branch (the consultant mailbox the Norbert-poller watches).
#
# This is the ONLY direct push a consultant makes: a single fast-forward commit of
# one packet file (handoffs/inbox/HX-<date>-<slug>.md) to `queue`. Results never
# come back this way — they arrive by PR into `main` (handoffs/outbox/<id>/).
#
# Usage (the SKILL.md gathers these from the session, then calls us):
#   handoff.sh --brief "<text>" \
#              --slug "<kebab-slug>" \
#              [--kind project|task] \
#              [--review-tier auto|light|full|founder] \
#              [--route-hint api] \
#              [--deadline "<ISO8601>|none"] \
#              [--requested-by "<gh-handle>"] \
#              [--input <repo-relative-path>]...   (repeatable) \
#              [--dod "<criterion>"]...             (repeatable, >=1 required) \
#              [--context "<pr#-or-packet-id>"]...  (repeatable) \
#              [--remote <name>]                    (default: ensemble) \
#              [--no-push]                          (build + commit, skip the push)
#
# Idempotent and re-runnable: aborts cleanly on an id collision, never half-writes
# state, and leaves the working tree on its original branch on exit. Australian
# English throughout. Prints errors to stderr and exits non-zero. Never prints
# secrets/tokens.
set -euo pipefail

_LIB="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../_lib" && pwd)"
# shellcheck source=/dev/null
. "$_LIB/ensemble_common.sh"

# --- tooling -----------------------------------------------------------------
ens_have git
ens_have python3

# --- (1) require a tethered engagement repo ----------------------------------
ROOT="$(ens_require_tethered)"
cd "$ROOT"

# --- argument parsing --------------------------------------------------------
BRIEF=""
SLUG=""
KIND="project"
REVIEW_TIER="full"
ROUTE_HINT="api"
DEADLINE="none"
REQUESTED_BY=""
REMOTE="ensemble"   # the remote /tether binds to the engagement repo (in both tether modes)
DO_PUSH=1
declare -a INPUTS=()
declare -a DOD=()
declare -a CONTEXT=()

usage() {
  # Print the contiguous leading comment header (line 2 → first non-comment line),
  # robust to the header's length unlike a hardcoded line range.
  awk 'NR>=2 && /^#/ {sub(/^# ?/, ""); print; next} NR>=2 {exit}' "${BASH_SOURCE[0]}"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --brief)        BRIEF="${2-}"; shift 2 ;;
    --slug)         SLUG="${2-}"; shift 2 ;;
    --kind)         KIND="${2-}"; shift 2 ;;
    --review-tier)  REVIEW_TIER="${2-}"; shift 2 ;;
    --route-hint)   ROUTE_HINT="${2-}"; shift 2 ;;
    --deadline)     DEADLINE="${2-}"; shift 2 ;;
    --requested-by) REQUESTED_BY="${2-}"; shift 2 ;;
    --remote)       REMOTE="${2-}"; shift 2 ;;
    --input)        INPUTS+=("${2-}"); shift 2 ;;
    --dod)          DOD+=("${2-}"); shift 2 ;;
    --context)      CONTEXT+=("${2-}"); shift 2 ;;
    --no-push)      DO_PUSH=0; shift ;;
    -h|--help)      usage; exit 0 ;;
    *) ens_die "unknown argument: $1 (see --help)" ;;
  esac
done

# --- (2) validate the gathered fields ----------------------------------------
[ -n "$BRIEF" ] || ens_die "a --brief is required (the handoff body)."
[ -n "$SLUG" ]  || ens_die "a --slug is required (kebab-case, <=24 chars)."
[ "${#DOD[@]}" -ge 1 ] || ens_die "at least one --dod (definition-of-done criterion) is required."

case "$KIND" in
  project|task) : ;;
  *) ens_die "invalid --kind '$KIND' (expected: project|task)." ;;
esac
case "$REVIEW_TIER" in
  auto|light|full|founder) : ;;
  *) ens_die "invalid --review-tier '$REVIEW_TIER' (expected: auto|light|full|founder)." ;;
esac
# route_hint: api only. local-bulk is reserved/deferred (no vLLM yet) — reject it.
case "$ROUTE_HINT" in
  api) : ;;
  local-bulk) ens_die "route_hint 'local-bulk' is deferred (no local bulk route yet). Use 'api'." ;;
  *) ens_die "invalid --route-hint '$ROUTE_HINT' (expected: api)." ;;
esac

# scope_tag (the engagement) comes from project.json — the packet's `engagement`
# field MUST equal it (tier-gate cross-checks this).
ENGAGEMENT="$(ens_project_field scope_tag)"
[ -n "$ENGAGEMENT" ] || ens_die "project.json has no scope_tag — cannot stamp the packet's engagement field."

# requested_by: prefer the supplied handle, else the gh-authenticated login, else
# git user.name — but it must be a real handle (full tier needs it to approve).
if [ -z "$REQUESTED_BY" ]; then
  if command -v gh >/dev/null 2>&1; then
    REQUESTED_BY="$(gh api user --jq .login 2>/dev/null || true)"
  fi
fi
if [ -z "$REQUESTED_BY" ]; then
  REQUESTED_BY="$(git config user.name 2>/dev/null || true)"
fi
[ -n "$REQUESTED_BY" ] || ens_die "could not determine requested_by — pass --requested-by <github-handle>."

# Normalise the slug to kebab and enforce <=24 chars (matches the schema pattern).
SLUG="$(printf '%s' "$SLUG" \
  | tr '[:upper:]' '[:lower:]' \
  | tr -cs 'a-z0-9' '-' \
  | sed -E 's/^-+//; s/-+$//; s/-+/-/g' \
  | cut -c1-24 \
  | sed -E 's/-+$//')"
[ -n "$SLUG" ] || ens_die "slug is empty after kebab-normalisation — supply an alphanumeric --slug."

# --- (4) compute the id and ENSURE UNIQUENESS --------------------------------
TODAY="$(date -u +%Y-%m%d)"   # HX-<YYYY-MMDD> uses a single dash inside the date block
ID="HX-${TODAY}-${SLUG}"

# Final shape sanity against the schema pattern before we do any I/O.
python3 - "$ID" <<'PY' || ens_die "computed id '$ID' is not a valid packet id (HX-YYYY-MMDD-slug)."
import re, sys
pat = r"^HX-[0-9]{4}-[0-9]{4}-[a-z0-9]([a-z0-9-]{0,22}[a-z0-9])?$"
sys.exit(0 if re.match(pat, sys.argv[1]) else 1)
PY

INBOX_REL="handoffs/inbox/${ID}.md"

# Refresh our view of the remote mailbox + record branches so the collision scan is
# truthful (best-effort: an offline consultant still gets the local-history check).
if [ "$DO_PUSH" -eq 1 ] && git remote get-url "$REMOTE" >/dev/null 2>&1; then
  git fetch --quiet "$REMOTE" queue main 2>/dev/null || true
fi

# Collect every ref that might already carry this id: local + remote queue/main,
# plus whatever HEAD we are on (covers detached / odd checkouts).
collision_in_tree() {
  # $1 = ref (e.g. origin/queue), $2 = path-prefix (e.g. handoffs/inbox)
  local ref="$1" prefix="$2"
  git rev-parse --verify --quiet "${ref}^{commit}" >/dev/null 2>&1 || return 1
  git ls-tree -r --name-only "$ref" -- "$prefix" 2>/dev/null \
    | grep -qx "${prefix}/${ID}.md"
}

for ref in queue "${REMOTE}/queue"; do
  if collision_in_tree "$ref" "handoffs/inbox"; then
    ens_die "id collision: ${INBOX_REL} already exists on '$ref' (queue inbox). Choose a different slug."
  fi
  # claimed/<agentId>/<id>.md — the poller moves a claimed packet here.
  if git rev-parse --verify --quiet "${ref}^{commit}" >/dev/null 2>&1; then
    if git ls-tree -r --name-only "$ref" -- "handoffs/claimed" 2>/dev/null \
        | grep -qE "^handoffs/claimed/[^/]+/${ID}\.md$"; then
      ens_die "id collision: ${ID} is already claimed on '$ref' (handoffs/claimed). Choose a different slug."
    fi
  fi
done

for ref in main "${REMOTE}/main"; do
  if git rev-parse --verify --quiet "${ref}^{commit}" >/dev/null 2>&1; then
    if git ls-tree -r --name-only "$ref" -- "handoffs/outbox" 2>/dev/null \
        | grep -qE "^handoffs/outbox/${ID}(/|\.md$)"; then
      ens_die "id collision: ${ID} already landed on '$ref' (handoffs/outbox). Choose a different slug."
    fi
  fi
done

# Git HISTORY across ALL refs: any commit that ever ADDED a file for this id — even
# if it was later moved/deleted — means the id has been used. This catches a packet
# that was claimed-then-completed (no longer in any current tree).
if git rev-parse --verify --quiet HEAD >/dev/null 2>&1; then
  HIST="$(git log --all --diff-filter=A --name-only --format='' -- \
            "handoffs/inbox/${ID}.md" \
            "handoffs/claimed/*/${ID}.md" \
            "handoffs/outbox/${ID}/*" \
            "handoffs/outbox/${ID}.md" 2>/dev/null | head -n1 || true)"
  if [ -n "$HIST" ]; then
    ens_die "id collision: ${ID} appears in git history ($HIST). This id has been used before — choose a different slug."
  fi
fi

# --- (3) large-input guard + LFS coverage ------------------------------------
# Any input >10MB that is NOT covered by an .gitattributes LFS filter must be fixed
# (LFS-tracked or moved under data/) before we build a packet that references it.
# We use `git check-attr filter` so we honour the repo's actual .gitattributes
# exactly — no need for the git-lfs binary, no pattern re-implementation.
MAX_BYTES=$((10 * 1024 * 1024))
file_size() { wc -c < "$1" 2>/dev/null | tr -d '[:space:]'; }

lfs_tracked() {
  # 0 (true) if `git check-attr` reports filter=lfs for this repo-relative path.
  local rel="$1" out
  out="$(git check-attr filter -- "$rel" 2>/dev/null || true)"
  case "$out" in
    *": filter: lfs") return 0 ;;
    *) return 1 ;;
  esac
}

declare -a OFFENDERS=()
for rel in ${INPUTS[@]+"${INPUTS[@]}"}; do
  abs="$ROOT/$rel"
  # Only existing, on-disk regular files can be sized; a path that does not exist
  # yet (e.g. an LFS-tracked output not pulled) is left to the schema/poller.
  [ -f "$abs" ] || continue
  sz="$(file_size "$abs")"
  [ -n "$sz" ] || continue
  if [ "$sz" -gt "$MAX_BYTES" ] && ! lfs_tracked "$rel"; then
    OFFENDERS+=("$rel ($(( (sz + 1048575) / 1048576 )) MB)")
  fi
done
if [ "${#OFFENDERS[@]}" -gt 0 ]; then
  {
    echo "ensemble: these inputs are >10MB and not covered by an LFS filter in .gitattributes:"
    for o in "${OFFENDERS[@]}"; do echo "  - $o"; done
    echo "ensemble: fix this before handing off — either:"
    echo "  * add a matching LFS pattern to .gitattributes (e.g. '*.<ext> filter=lfs diff=lfs merge=lfs -text'), or"
    echo "  * move the file under data/ (which is LFS-tracked by the template), then 'git add' it so it becomes an LFS pointer."
  } >&2
  exit 1
fi

# Install the pre-push hook that rejects >10MB non-LFS blobs (belt-and-braces: the
# poller and GitHub also enforce, but stop a bad push before it leaves the laptop).
install_prepush_hook() {
  local hooks_dir hook
  hooks_dir="$(git rev-parse --git-path hooks 2>/dev/null)" || return 0
  mkdir -p "$hooks_dir"
  hook="$hooks_dir/pre-push"
  # Idempotent: only (re)write when our marker is absent or content differs.
  local marker="# ensemble-handoff pre-push guard v1"
  if [ -f "$hook" ] && grep -qF "$marker" "$hook" 2>/dev/null; then
    return 0
  fi
  if [ -f "$hook" ] && ! grep -qF "$marker" "$hook" 2>/dev/null; then
    printf 'ensemble: a pre-push hook already exists (%s) without our guard — leaving it untouched.\n' "$hook" >&2
    printf 'ensemble: add a >10MB non-LFS blob check to it manually, or remove it so /handoff can install ours.\n' >&2
    return 0
  fi
  cat > "$hook" <<'HOOK'
#!/usr/bin/env bash
# ensemble-handoff pre-push guard v1
# Reject any pushed blob >10MB that is NOT an LFS pointer. Large/binary engagement
# data rides MinIO over LFS, never GitHub. Honours .gitattributes via check-attr.
set -euo pipefail
MAX=$((10 * 1024 * 1024))
ZERO="0000000000000000000000000000000000000000"
fail=0
while read -r _local_ref local_sha _remote_ref remote_sha; do
  [ "$local_sha" = "$ZERO" ] && continue   # a branch deletion — nothing to scan.
  if [ "$remote_sha" = "$ZERO" ]; then
    range="$local_sha"                     # new branch — scan all its objects.
  else
    range="${remote_sha}..${local_sha}"    # update — scan only the new objects.
  fi
  # Inspect every blob this push would introduce; flag any >10MB non-pointer.
  while IFS=$'\t' read -r sha path; do
    [ -n "${sha:-}" ] || continue
    size="$(git cat-file -s "$sha" 2>/dev/null || echo 0)"
    [ "$size" -gt "$MAX" ] || continue
    # LFS pointers are tiny; a >10MB blob is by definition not a pointer. But also
    # respect .gitattributes: if the path is LFS-tracked, a large blob means the
    # filter did not run — still a defect, so reject either way.
    echo "pre-push: BLOCKED — $path is ${size} bytes (>10MB) and not an LFS pointer." >&2
    echo "          LFS-track it (.gitattributes) or move it under data/, then re-commit." >&2
    fail=1
  done < <(git rev-list --objects "$range" 2>/dev/null \
            | while read -r sha path; do
                [ -n "${path:-}" ] || continue
                [ "$(git cat-file -t "$sha" 2>/dev/null)" = "blob" ] || continue
                printf '%s\t%s\n' "$sha" "$path"
              done)
done
exit "$fail"
HOOK
  chmod +x "$hook"
  printf 'ensemble: installed pre-push >10MB-non-LFS guard at %s\n' "$hook" >&2
}
install_prepush_hook

# --- (5) build the packet, validate, commit, fast-forward push ---------------
SCHEMA="$ROOT/schemas/packet.schema.json"
[ -f "$SCHEMA" ] || ens_die "engagement repo has no schemas/packet.schema.json — is this a real engagement repo?"

# Render the packet (front-matter + '## Brief' body) deterministically in Python so
# strings with special chars are JSON-safe, then validate via the shared lib before
# we touch git. We pass the gathered fields over argv/env to avoid quoting hazards.
export ENS_ID="$ID" ENS_ENGAGEMENT="$ENGAGEMENT" ENS_REQUESTED_BY="$REQUESTED_BY" \
       ENS_KIND="$KIND" ENS_REVIEW_TIER="$REVIEW_TIER" ENS_ROUTE_HINT="$ROUTE_HINT" \
       ENS_DEADLINE="$DEADLINE" ENS_BRIEF="$BRIEF" ENS_SCHEMA="$SCHEMA" \
       ENS_INBOX_ABS="$ROOT/$INBOX_REL"

# Pass list items as NUL-delimited env blobs (newline-free, order-preserving).
ENS_INPUTS="$(printf '%s\n' ${INPUTS[@]+"${INPUTS[@]}"})"
ENS_DOD="$(printf '%s\n' "${DOD[@]}")"
ENS_CONTEXT="$(printf '%s\n' ${CONTEXT[@]+"${CONTEXT[@]}"})"
export ENS_INPUTS ENS_DOD ENS_CONTEXT

python3 - <<'PY' || exit 1
import json, os, sys
import ensemble_common as e

def lines(name):
    raw = os.environ.get(name, "")
    return [ln for ln in raw.split("\n") if ln.strip()]

fm = {
    "id":            os.environ["ENS_ID"],
    "engagement":    os.environ["ENS_ENGAGEMENT"],
    "requested_by":  os.environ["ENS_REQUESTED_BY"],
    "kind":          os.environ["ENS_KIND"],
    "review_tier":   os.environ["ENS_REVIEW_TIER"],
    "route_hint":    os.environ["ENS_ROUTE_HINT"],
    "deadline":      os.environ["ENS_DEADLINE"],
    "inputs":        lines("ENS_INPUTS"),
    "definition_of_done": lines("ENS_DOD"),
    "retries":       0,
    "context":       lines("ENS_CONTEXT"),
}

def yval(v):
    # Emit a JSON scalar — valid YAML for our stdlib parser and unambiguous.
    return json.dumps(v, ensure_ascii=False)

def ylist(items):
    # Flow list of JSON-quoted strings: [ "a", "b" ] (empty -> []).
    return "[" + ", ".join(json.dumps(i, ensure_ascii=False) for i in items) + "]"

order = ["id", "engagement", "requested_by", "kind", "review_tier",
         "route_hint", "deadline", "inputs", "definition_of_done",
         "retries", "context"]

out = ["---"]
for k in order:
    v = fm[k]
    if isinstance(v, list):
        out.append(f"{k}: {ylist(v)}")
    else:
        out.append(f"{k}: {yval(v)}")
out.append("---")
out.append("")
out.append("## Brief")
out.append("")
out.append(os.environ["ENS_BRIEF"].rstrip() + "\n")
text = "\n".join(out)

# Round-trip parse + validate against the engagement repo's schema BEFORE writing.
parsed, _brief = e.split_packet(text)
errs = e.validate_packet(parsed, os.environ["ENS_SCHEMA"])
if errs:
    print("ensemble: packet failed schema validation:", file=sys.stderr)
    for er in errs:
        print(f"  - {er}", file=sys.stderr)
    sys.exit(1)

dest = os.environ["ENS_INBOX_ABS"]
os.makedirs(os.path.dirname(dest), exist_ok=True)
with open(dest, "w", encoding="utf-8") as fh:
    fh.write(text)
print(f"ensemble: wrote {dest}", file=sys.stderr)
PY

# --- git: branch onto queue, commit just the packet, fast-forward push -------
ORIG_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"
STASHED=0
cleanup() {
  # Always return the consultant to where they started.
  if [ "$STASHED" -eq 1 ]; then
    git stash pop --quiet 2>/dev/null || true
  fi
  if [ -n "${ORIG_BRANCH:-}" ] && [ "$ORIG_BRANCH" != "HEAD" ]; then
    git checkout --quiet "$ORIG_BRANCH" 2>/dev/null || true
  fi
}
trap cleanup EXIT

# Park any unrelated working-tree changes so the queue commit is the packet ALONE.
if [ -n "$(git status --porcelain --untracked-files=no 2>/dev/null)" ]; then
  # Our just-written packet is untracked, so --untracked-files=no leaves it in place
  # while stashing only tracked modifications.
  if git stash push --quiet --keep-index --message "ensemble-handoff:${ID}" 2>/dev/null; then
    STASHED=1
  fi
fi

# Move onto a fresh local `queue` that tracks the remote tip (fast-forward base).
if git rev-parse --verify --quiet "${REMOTE}/queue^{commit}" >/dev/null 2>&1; then
  git checkout --quiet -B queue "${REMOTE}/queue"
elif git rev-parse --verify --quiet "queue^{commit}" >/dev/null 2>&1; then
  git checkout --quiet queue
else
  # First-ever packet on a brand-new engagement: base queue on main's tip.
  if git rev-parse --verify --quiet "${REMOTE}/main^{commit}" >/dev/null 2>&1; then
    git checkout --quiet -B queue "${REMOTE}/main"
  else
    git checkout --quiet -B queue
  fi
fi

# The packet file was written into the working tree before the checkout; ensure it
# survived (checkout of an untracked path is preserved by git) then stage ONLY it.
[ -f "$ROOT/$INBOX_REL" ] || ens_die "packet file vanished after switching to queue — aborting (no push)."
git add -- "$INBOX_REL"

# Guard: the staged change must be exactly our one packet file, nothing else.
STAGED="$(git diff --cached --name-only)"
if [ "$STAGED" != "$INBOX_REL" ]; then
  ens_die "refusing to commit — staged set is not exactly ${INBOX_REL} (got: ${STAGED//$'\n'/, })."
fi

git commit --quiet -m "handoff: ${ID}" -- "$INBOX_REL"
NEW_SHA="$(git rev-parse HEAD)"

if [ "$DO_PUSH" -eq 0 ]; then
  printf 'ensemble: built and committed %s on local queue (%s) — push skipped (--no-push).\n' "$ID" "${NEW_SHA:0:8}" >&2
  echo "$ID"
  exit 0
fi

git remote get-url "$REMOTE" >/dev/null 2>&1 \
  || ens_die "no '$REMOTE' remote configured — cannot push the packet to the queue branch."

# FAST-FORWARD ONLY: never force, never push to main. If the remote queue moved
# under us, this fails and the consultant simply re-runs (the id stays unique).
if ! git push --quiet "$REMOTE" "HEAD:refs/heads/queue"; then
  ens_die "fast-forward push to ${REMOTE}/queue failed (the queue may have advanced). Re-run /handoff to rebase onto the new tip and retry."
fi

# --- (6) confirm -------------------------------------------------------------
{
  printf '\n'
  printf 'ensemble: handoff %s pushed to %s/queue (%s).\n' "$ID" "$REMOTE" "${NEW_SHA:0:8}"
  printf 'ensemble: file %s — review tier: %s, kind: %s, engagement: %s.\n' "$INBOX_REL" "$REVIEW_TIER" "$KIND" "$ENGAGEMENT"
  printf 'ensemble: the Norbert-poller polls every ~2 min; it will claim this packet into handoffs/claimed/<agentId>/.\n'
  printf 'ensemble: results return by PR into main (handoffs/outbox/%s/) — never to the queue branch.\n' "$ID"
} >&2

# Stdout: the id alone, so a caller (or the SKILL.md) can capture it.
echo "$ID"
