#!/usr/bin/env bash
# submit.sh — /submit : land work a consultant did THEMSELVES as a reviewed PR into
# the engagement's `main`, matched to one or more deliverables ("Lars's delivery
# page"). Unlike /handoff (which queues work FOR the fleet), /submit brings finished
# work IN: it builds a self-contained result set under handoffs/outbox/<id>/ and
# opens a PR into main, where tier-gate requires the right approval before merge.
#
# Usage (the SKILL.md interviews the consultant + matches deliverables, then calls us):
#   submit.sh --title "<short title>" \
#             [--slug "<kebab-slug>"] \
#             [--deliverable "<deliverable name/id>"]...  (repeatable; the matched ones) \
#             [--artefact "<path>"]...                    (repeatable; files produced) \
#             [--evidence "<how it meets the criteria>"] \
#             [--dod "<acceptance criterion>"]...         (repeatable) \
#             [--review-tier auto|light|full|founder]     (default: full) \
#             [--requested-by "<gh-handle>"] \
#             [--remote <name>]                           (default: ensemble) \
#             [--no-pr]                                   (build + commit the branch, skip push/PR)
#
# Idempotent-ish: aborts on an id collision, returns you to your original branch on
# exit, and stages ONLY handoffs/outbox/<id>/. Australian English. Never prints secrets.
set -euo pipefail

_LIB="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../_lib" && pwd)"
# shellcheck source=/dev/null
. "$_LIB/ensemble_common.sh"
HERE="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

ens_have git
ens_have python3

ROOT="$(ens_require_tethered)"
cd "$ROOT"

# --- args --------------------------------------------------------------------
TITLE="" SLUG="" EVIDENCE="" REVIEW_TIER="full" REQUESTED_BY="" REMOTE="ensemble" DO_PR=1
declare -a DELIVS=() ARTEFACTS=() DOD=()
usage() { awk 'NR>=2 && /^#/ {sub(/^# ?/, ""); print; next} NR>=2 {exit}' "${BASH_SOURCE[0]}"; }
while [ "$#" -gt 0 ]; do
  case "$1" in
    --title)        TITLE="${2-}"; shift 2 ;;
    --slug)         SLUG="${2-}"; shift 2 ;;
    --deliverable)  DELIVS+=("${2-}"); shift 2 ;;
    --artefact)     ARTEFACTS+=("${2-}"); shift 2 ;;
    --evidence)     EVIDENCE="${2-}"; shift 2 ;;
    --dod)          DOD+=("${2-}"); shift 2 ;;
    --review-tier)  REVIEW_TIER="${2-}"; shift 2 ;;
    --requested-by) REQUESTED_BY="${2-}"; shift 2 ;;
    --remote)       REMOTE="${2-}"; shift 2 ;;
    --no-pr)        DO_PR=0; shift ;;
    -h|--help)      usage; exit 0 ;;
    *) ens_die "unknown argument: $1 (see --help)" ;;
  esac
done

[ -n "$TITLE" ] || ens_die "a --title is required (a short name for this submission)."
case "$REVIEW_TIER" in auto|light|full|founder) : ;; *) ens_die "invalid --review-tier '$REVIEW_TIER'." ;; esac

ENGAGEMENT="$(ens_project_field scope_tag)"
[ -n "$ENGAGEMENT" ] || ens_die "project.json has no scope_tag — cannot stamp the submission."

if [ -z "$REQUESTED_BY" ] && command -v gh >/dev/null 2>&1; then
  REQUESTED_BY="$(gh api user --jq .login 2>/dev/null || true)"
fi
# Must be a GitHub LOGIN, not a display name — tier-gate matches review approvals
# against the login, so a full name (with spaces) would make `full` unsatisfiable.
# Do NOT fall back to git user.name. Require gh auth or an explicit --requested-by.
[ -n "$REQUESTED_BY" ] || ens_die "could not determine your GitHub handle — run 'gh auth login', or pass --requested-by <github-login>."
case "$REQUESTED_BY" in *[!A-Za-z0-9-]*) ens_die "requested_by '$REQUESTED_BY' is not a valid GitHub login — pass --requested-by <github-login>." ;; esac

# slug: from --slug, else from --title. kebab, <=24 chars (schema pattern).
[ -n "$SLUG" ] || SLUG="$TITLE"
SLUG="$(printf '%s' "$SLUG" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' \
        | sed -E 's/^-+//; s/-+$//; s/-+/-/g' | cut -c1-24 | sed -E 's/-+$//')"
[ -n "$SLUG" ] || ens_die "slug is empty after normalisation — supply an alphanumeric --title/--slug."

TODAY="$(date -u +%Y-%m%d)"
ID="HX-${TODAY}-${SLUG}"
python3 - "$ID" <<'PY' || ens_die "computed id '$ID' is not a valid id (HX-YYYY-MMDD-slug)."
import re, sys
sys.exit(0 if re.match(r"^HX-[0-9]{4}-[0-9]{4}-[a-z0-9]([a-z0-9-]{0,22}[a-z0-9])?$", sys.argv[1]) else 1)
PY

OUTBOX_REL="handoffs/outbox/${ID}"
ARTE_REL="${OUTBOX_REL}/artefacts"

# --- refresh main + id-uniqueness on outbox (current + history) ---------------
if [ "$DO_PR" -eq 1 ] && git remote get-url "$REMOTE" >/dev/null 2>&1; then
  git fetch --quiet "$REMOTE" main 2>/dev/null || true
fi
for ref in main "${REMOTE}/main"; do
  if git rev-parse --verify --quiet "${ref}^{commit}" >/dev/null 2>&1; then
    if git ls-tree -r --name-only "$ref" -- "handoffs/outbox" 2>/dev/null \
        | grep -qE "^handoffs/outbox/${ID}(/|\.md$)"; then
      ens_die "id collision: ${ID} already landed on '$ref'. Choose a different slug."
    fi
  fi
done
if git rev-parse --verify --quiet HEAD >/dev/null 2>&1; then
  if git log --all --diff-filter=A --name-only --format='' -- \
        "handoffs/outbox/${ID}/*" "handoffs/outbox/${ID}.md" 2>/dev/null | head -n1 | grep -q .; then
    ens_die "id collision: ${ID} appears in git history — choose a different slug."
  fi
fi

# --- definition_of_done: need >=1 (schema). Derive from deliverables/title. ----
if [ "${#DOD[@]}" -eq 0 ]; then
  if [ "${#DELIVS[@]}" -gt 0 ]; then
    for d in "${DELIVS[@]}"; do DOD+=("Deliverable satisfied: ${d}"); done
  else
    DOD+=("Submitted work '${TITLE}' is complete and accepted.")
  fi
fi

# --- park local changes + branch off the remote main tip ----------------------
ORIG_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"
STASHED=0
cleanup() {
  [ "$STASHED" -eq 1 ] && git stash pop --quiet 2>/dev/null || true
  [ -n "${ORIG_BRANCH:-}" ] && [ "$ORIG_BRANCH" != "HEAD" ] && git checkout --quiet "$ORIG_BRANCH" 2>/dev/null || true
}
trap cleanup EXIT
if [ -n "$(git status --porcelain --untracked-files=no 2>/dev/null)" ]; then
  git stash push --quiet --message "ensemble-submit:${ID}" 2>/dev/null && STASHED=1 || true
fi

if git rev-parse --verify --quiet "${REMOTE}/main^{commit}" >/dev/null 2>&1; then
  git checkout --quiet -B "submit/${ID}" "${REMOTE}/main"
elif git rev-parse --verify --quiet "main^{commit}" >/dev/null 2>&1; then
  git checkout --quiet -B "submit/${ID}" "main"
else
  ens_die "no main branch found on '$REMOTE' or locally — cannot base a submission PR."
fi

# Refuse to proceed if a local outbox path survived a prior run (untracked leftovers
# would otherwise be silently reused/committed). The clean branch checkout above does
# not remove untracked dirs, so check explicitly.
[ -e "$ROOT/$OUTBOX_REL" ] && ens_die "a local outbox already exists at ${OUTBOX_REL} — remove it (or choose a different --slug) and re-run."

# --- copy artefacts into the outbox (with a >10MB non-LFS guard) --------------
mkdir -p "$ROOT/$ARTE_REL"
declare -a INPUTS=()
MAX_BYTES=$((10 * 1024 * 1024))
lfs_tracked() { case "$(git check-attr filter -- "$1" 2>/dev/null || true)" in *": filter: lfs") return 0 ;; *) return 1 ;; esac; }
for src in ${ARTEFACTS[@]+"${ARTEFACTS[@]}"}; do
  [ -f "$src" ] || ens_die "artefact not found: $src"
  base="$(basename -- "$src")"
  dest_rel="${ARTE_REL}/${base}"
  # Two source paths with the same filename would silently overwrite — refuse instead.
  [ -e "$ROOT/$dest_rel" ] && ens_die "two artefacts resolve to the same name ($base) — rename one and re-run."
  cp -- "$src" "$ROOT/$dest_rel"
  sz="$(wc -c < "$ROOT/$dest_rel" 2>/dev/null | tr -d '[:space:]')"
  if [ -n "$sz" ] && [ "$sz" -gt "$MAX_BYTES" ] && ! lfs_tracked "$dest_rel"; then
    ens_die "artefact $base is >10MB and not LFS-tracked. Add a matching LFS pattern to .gitattributes (e.g. '*.${base##*.} filter=lfs diff=lfs merge=lfs -text') or place it under data/, then re-run."
  fi
  INPUTS+=("$dest_rel")
done

# --- render packet.md + summary.md + submission.json (validated) --------------
SCHEMA="$ROOT/schemas/packet.schema.json"
[ -f "$SCHEMA" ] || ens_die "engagement repo has no schemas/packet.schema.json — is this a real engagement repo?"
SUBMITTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

export ID ENGAGEMENT REQUESTED_BY REVIEW_TIER TITLE EVIDENCE SUBMITTED_AT ROOT OUTBOX_REL SCHEMA
DELIVS_NL="$(printf '%s\n' ${DELIVS[@]+"${DELIVS[@]}"})"; export DELIVS_NL
INPUTS_NL="$(printf '%s\n' ${INPUTS[@]+"${INPUTS[@]}"})"; export INPUTS_NL
DOD_NL="$(printf '%s\n' "${DOD[@]}")"; export DOD_NL
CONFIG="$(python3 - <<'PY'
import json, os, sys
def arr(name):
    raw = os.environ.get(name, "")
    return [x for x in raw.split("\n") if x.strip()]
cfg = {
    "id": os.environ["ID"], "engagement": os.environ["ENGAGEMENT"],
    "requested_by": os.environ["REQUESTED_BY"], "review_tier": os.environ["REVIEW_TIER"],
    "title": os.environ["TITLE"], "evidence": os.environ.get("EVIDENCE", ""),
    "submitted_at": os.environ["SUBMITTED_AT"], "kind": "task", "route_hint": "api", "deadline": "none",
    "deliverables": arr("DELIVS_NL"), "inputs": arr("INPUTS_NL"), "definition_of_done": arr("DOD_NL"),
    "outbox_abs": os.path.join(os.environ["ROOT"], os.environ["OUTBOX_REL"]),
    "schema": os.environ["SCHEMA"],
}
print(json.dumps(cfg))
PY
)"
printf '%s' "$CONFIG" | python3 "$HERE/submit_state.py" build || exit $?

# --- stage ONLY the outbox, commit, (push + PR) ------------------------------
git add -- "$OUTBOX_REL"
STAGED="$(git diff --cached --name-only | grep -v "^${OUTBOX_REL}/" || true)"
[ -z "$STAGED" ] || ens_die "refusing to commit — staged set strays outside ${OUTBOX_REL} (got: ${STAGED//$'\n'/, })."
git commit --quiet -m "submit: ${ID} — ${TITLE}"
NEW_SHA="$(git rev-parse HEAD)"

if [ "$DO_PR" -eq 0 ]; then
  printf 'ensemble: built submission %s on branch submit/%s (%s) — push/PR skipped (--no-pr).\n' "$ID" "$ID" "${NEW_SHA:0:8}" >&2
  echo "$ID"; exit 0
fi

ens_have gh
git remote get-url "$REMOTE" >/dev/null 2>&1 || ens_die "no '$REMOTE' remote — cannot push the submission branch."
git push --quiet "$REMOTE" "HEAD:refs/heads/submit/${ID}" \
  || ens_die "could not push submit/${ID} to ${REMOTE}. Re-run after resolving the push error."

REPO_SLUG="$(git remote get-url "$REMOTE" | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')"
PR_BODY="$(printf 'Consultant submission of completed work, matched to the delivery page.\n\n- **Submitted by:** %s\n- **Review tier:** %s\n- **Deliverables:** %s\n\nSee `%s/summary.md` and `%s/submission.json`. tier-gate requires the %s approval before merge.\n' \
  "$REQUESTED_BY" "$REVIEW_TIER" "$(IFS=,; echo "${DELIVS[*]:-(none matched)}")" "$OUTBOX_REL" "$OUTBOX_REL" "$REVIEW_TIER")"
set +e
PR_OUT="$(gh pr create --repo "$REPO_SLUG" --base main --head "submit/${ID}" \
  --title "submit: ${TITLE} (${ID})" --body "$PR_BODY" 2>&1)"
PR_RC=$?
set -e
if [ "$PR_RC" -ne 0 ]; then
  {
    printf '\nensemble: submission %s was pushed to %s/submit/%s, but OPENING THE PR FAILED:\n' "$ID" "$REMOTE" "$ID"
    printf '%s\n' "$PR_OUT" | sed 's/^/  /'
    printf 'ensemble: nothing is under review yet. Create the PR manually:\n'
    printf 'ensemble:   gh pr create --repo %s --base main --head submit/%s\n' "$REPO_SLUG" "$ID"
  } >&2
  echo "$ID"; exit 1
fi

{
  printf '\nensemble: submission %s pushed; PR opened into main.\n' "$ID"
  [ -n "$PR_OUT" ] && printf 'ensemble: %s\n' "$PR_OUT"
  printf 'ensemble: tier-gate is RED until the %s reviewer approves; approve on GitHub to merge.\n' "$REVIEW_TIER"
  printf 'ensemble: on merge, the fleet reconciles the matched deliverable(s) on Lars'"'"'s delivery page.\n'
} >&2
echo "$ID"
