---
name: handoff-proposal
description: Hand an externally-authored proposal into the Ensemble opportunities pipeline. Use when a consultant says "hand off this proposal", "push this proposal into the pipeline", "log this proposal against the deal", "import this proposal", or has a finished proposal (PDF/HTML/structured) for a company that should attach to a BEAM opportunity and advance it to "Propose". POSTs to the Ensemble's /api/import/proposal intake over Tailscale.
---

# /handoff-proposal — push a finished proposal into the opportunities pipeline

Normally a proposal is an **output** of the BEAM pipeline — finnDahlgren drafts one at
stage 4 ("Propose"). This skill goes the **other way**: it takes a proposal authored
**outside** the Ensemble (a deck you wrote by hand, a `sas-presentation` proposal, a PDF
from a partner) and hands it **into** the pipeline. The Ensemble intake then:

1. **Finds or creates** the opportunity by **company** (idempotent — one opportunity per
   client; re-running attaches another proposal to the same deal).
2. **Advances** the opportunity to BEAM stage 4 **"Propose"** — but never regresses a deal
   already at Commit/Deliver.
3. **Attaches** the proposal as a `PENDING_APPROVAL` proposal (visible on the opportunity
   rail and in the founder's approval queue), rendering/uploading a PDF where possible, and
   records the inbound handoff as a radar-replay beam.

This is the proposal sibling of the `import-beam-leads` skill: a direct, API-key-guarded
intake over **Tailscale** (not the GitHub task-packet `/handoff` channel).

## Prerequisites

- On the **Tailscale tailnet** that can reach the Ensemble API.
- Two env vars set (ask the consultant if unset — never hardcode the key):
  - `ENSEMBLE_API_URL` — e.g. `https://<tailscale-host>:8181` (the script appends
    `/api/import/proposal`).
  - `ENSEMBLE_IMPORT_KEY` — the shared import key (sent as `X-Import-Key`).
- `python3` (the script is stdlib-only — no pip install).

## How to run it

1. **Interview briefly** — don't dump a form. Gather:
   - **Company** (required) — the find-or-create key for the opportunity.
   - **The proposal artifact** — at least one of:
     - a finished **PDF** (`--pdf`), or
     - single-page **HTML** (`--html`, rendered to PDF server-side), or
     - **structured JSON** (`--sections-json`) with any of `proposal_sections`,
       `client_problem_map`, `timeline_weeks`, `case_study_references`.
   - Optional: **title** (defaults to `Proposal — <company>`), **sector**, primary
     **contact** email, **notes**.

2. **Preview first** with `--dry-run` to show the consultant the body that will be sent
   (large fields are summarised), then send for real.

3. **Call the script:**

```bash
python3 "$SKILL_DIR/handoff_proposal.py" \
  --company "Transdev" \
  --title "ISO 55001 maturity uplift" \
  --pdf ~/proposals/transdev-iso55001.pdf \
  --sector Transport \
  --contact ops.director@transdev.com.au
# add --dry-run to preview without sending
```

`$SKILL_DIR` is this skill's directory. The script reads `ENSEMBLE_API_URL` and
`ENSEMBLE_IMPORT_KEY` from the environment (override with `--api-url` / `--key`).

## What you get back

JSON with `opportunity_id`, `proposal_id`, `agent_output_id`, `company`, `stage`,
`stage_name`, `created` (was the opportunity new), and `pdf_attached`. Relay the human
line the script prints, e.g.:

> ✓ Transdev: opportunity created at stage 4 (Propose), proposal attached (with PDF).

Tell the consultant the proposal now sits in the founder's **approval queue** and on the
opportunity's **Proposals** rail in the HMI — sending to the client goes through the normal
approval/Resend flow (this skill does **not** email the client).

## Notes

- **Idempotent on company.** Re-running for the same company attaches another proposal and
  re-asserts stage ≥ Propose; it won't duplicate the opportunity.
- **Structured-only is fine** — if you pass only `--sections-json` with no PDF/HTML, the
  proposal still attaches (no PDF until someone renders it).
- **Errors** surface verbatim: a `401` means a bad/missing key, `422` means no company,
  `503` means the intake isn't configured on the server.
