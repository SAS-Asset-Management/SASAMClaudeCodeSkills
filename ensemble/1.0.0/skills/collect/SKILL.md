---
name: collect
description: Pull merged Ensemble result sets from an engagement's main branch into the session — materialise and verify any LFS deliverables, record what was collected, and summarise each result.
---

# collect

Use this skill when the consultant wants to **pick up finished work** for an
engagement — i.e. retrieve the result sets that the Ensemble has merged into the
engagement repo's `main` branch (the reviewed record). Results always arrive by PR
into `main` under `handoffs/outbox/<id>/` (a `summary.md`, the original `packet.md`,
and any deliverable files, some of which may be **Git LFS** objects).

Trigger phrases: "collect my results", "pull the finished work", "/collect",
"grab HX-2026-0610-foo", "what has come back for this engagement".

## Preconditions

- The session's working directory must be **inside a tethered engagement repo**
  (one that has `.ensemble/project.json`). If it is not, the script refuses and
  prints a hint — tether the engagement first (the `/tether` skill).
- `git` is required; `git-lfs` is only required if a result set contains LFS
  deliverables (the script will tell you if it is missing and skip those objects).

## How to run it

1. Confirm you are in the right engagement repo. If the consultant named a specific
   result, capture its **packet id** (`HX-YYYY-MMDD-slug`); otherwise leave it blank
   to collect **everything merged**.
2. Run the script from this skill folder, from within the engagement repo:

   ```bash
   # Collect every merged result set:
   bash <skill-dir>/collect.sh

   # Or just one, by packet id:
   bash <skill-dir>/collect.sh HX-2026-0610-pump-fmeca
   ```

3. Read the output back to the consultant: for each result it prints the file list,
   the LFS verification outcome, and the head of `summary.md`. Offer to open or act
   on specific deliverables next.

## What the script does (deterministic — do not duplicate by hand)

1. **Fast-forward-only pull of `main`** so freshly-merged results are visible. A
   fast-forward-only update never rewrites the reviewed record. If the mesh is
   unreachable the script says so and collects from the local `main` instead of
   failing.
2. **Enumerates merged result sets** from the committed tree of `main`
   (`handoffs/outbox/<id>/`) — only results that genuinely landed by PR, never a
   stray local directory. With an id argument it collects just that one; without, it
   collects all.
3. **Materialises + verifies LFS deliverables.** For every Git LFS *pointer* in a
   result set it runs `git lfs pull --include=<paths>` then verifies the file's
   **sha256 against the pointer's `oid`**. If the LFS mesh is unreachable (or
   `git-lfs` is absent, or a hash mismatches) it **lists what was skipped and why**
   and keeps going — it does not fail the whole collect.
4. **Records each collected result** into `~/.ensemble/collected.json`
   (`id`, `engagement`, `collected_at`, `paths`) — an idempotent upsert keyed by id,
   so re-running refreshes rather than duplicates.
5. **Summarises each result's `summary.md`** to stdout for the session.

## Notes

- Idempotent and re-runnable. Collecting the same result twice updates its
  `collected_at` and `paths` in place.
- Never pushes anything and never touches `main`'s history — it only *reads* merged
  results and writes local `~/.ensemble` state.
- All output is in Australian English; errors go to stderr with a non-zero exit.

## Files in this skill

- `collect.sh` — entry point: sources the shared lib, does the ff-only `main` pull,
  then hands off to the Python implementation.
- `collect_impl.py` — the deterministic worker: result-set enumeration, LFS
  pointer detection + sha256 verification, `collected.json` upsert, and the
  `summary.md` print. Stdlib only; reuses `_lib/ensemble_common.py`.
