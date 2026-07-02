---
name: submit
description: Submit work a consultant did themselves into the engagement — interview them about it, match it to the engagement's deliverables (Lars's delivery page), and open a reviewed PR into main. Use when a consultant says "submit this", "I've finished X", "log this deliverable", "I did this offline and want it on the record", or wants their own completed work captured against the project plan.
---

# /submit — land your own completed work as a reviewed deliverable

`/handoff` sends work **to** the fleet. **`/submit` brings finished work _in_** — work
the consultant did themselves (offline, by hand, in a workshop) — matches it to the
engagement's **deliverables** ("Lars's delivery page"), and opens a **PR into `main`**
so it lands as a reviewed, auditable result under `handoffs/outbox/<id>/`.

Run this from **inside a tethered engagement repo** (one with `.ensemble/project.json`).
The script calls `ens_require_tethered` and aborts otherwise.

## How to run it

1. **Interview the consultant** conversationally — don't dump a form:
   - **What did you do?** A short **title** + a paragraph of **evidence**: what the work
     is and how it meets the bar. This becomes `summary.md`.
   - **Which artefact(s)?** The file(s) they produced (paths on disk). These are copied
     into the PR under `handoffs/outbox/<id>/artefacts/`. Anything >10MB must be
     LFS-tracked (the script tells you if not).

2. **Match it to a deliverable.** This is the point of `/submit`:
   - If the engagement repo has **`.ensemble/deliverables.json`**, read it and show the
     consultant the open deliverables (name, description, acceptance criteria). Help them
     pick the one(s) this satisfies, and lift the acceptance criteria into `--dod`.
   - If that file is **absent** (not all engagements export it yet), ask the consultant
     which deliverable or requirement this satisfies in their own words, and capture their
     acceptance criteria as `--dod`. The fleet reconciles the exact deliverable on merge.
   - Pass each matched deliverable as a `--deliverable` and each acceptance criterion as
     a `--dod`.

3. **Call the script** with what you gathered:

```bash
bash "$SKILL_DIR/submit.sh" --title "<short title>" \
  --deliverable "<matched deliverable>"   # repeatable \
  --artefact "<path/to/file>"             # repeatable \
  --evidence "<how it meets the criteria>" \
  --dod "<acceptance criterion>"          # repeatable \
  [--review-tier auto|light|full|founder] # default full
```

- **Default tier is `full`** — the consultant who submitted approves it. Use `founder`
  for client-facing or contractual deliverables. Only drop to `light`/`auto` for low-risk
  internal artefacts.
- Use `--no-pr` to build and commit the branch **without** pushing/opening the PR (handy
  to show the consultant the result set first).

## What the script does (deterministic — don't reproduce by hand)

1. Resolves the engagement (`scope_tag`) and the submitter (`gh` login) automatically.
2. Computes a unique id `HX-<YYYY-MMDD>-<slug>` and checks it against `main` + history.
3. Branches off `ensemble/main`, copies the artefacts into `handoffs/outbox/<id>/artefacts/`
   (guarding >10MB non-LFS files), and writes a **schema-valid `packet.md`** (so tier-gate
   reads the right review tier + requester), a human **`summary.md`**, and a structured
   **`submission.json`** (the deliverable claims).
4. Commits **only** that outbox folder, pushes the branch, and opens a **PR into `main`**.

## After it runs

- Relay the **PR URL** and tell the consultant: tier-gate is **red** until the required
  reviewer (for `full`, themselves) approves — approve on GitHub to merge.
- On merge, the fleet reconciles the matched deliverable(s) on Lars's delivery page
  (status → delivered). Their work is now on the record, reviewed.

## Exit codes

- `0` — submission built (and PR opened unless `--no-pr`).
- `1` — any error: bad/missing arguments (e.g. no `--title`), an id collision, or a packet/schema/git/push failure (relay the stderr message).
