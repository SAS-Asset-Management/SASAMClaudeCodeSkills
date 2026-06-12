#!/usr/bin/env python3
"""Hand an externally-authored proposal into the Ensemble opportunities pipeline.

POSTs a proposal to the Ensemble's `/api/import/proposal` intake (the reverse of
the normal flow, where a proposal is an *output* of a stage-4 deal). The intake
finds-or-creates the opportunity by company, advances it to the BEAM "Propose"
stage (never regressing a later-stage deal), and attaches the proposal as a
PENDING_APPROVAL Proposal for founder approval.

stdlib only (urllib) — no pip install needed. Reachable over Tailscale.

Config (env vars, overridable by flags):
  ENSEMBLE_API_URL    base URL of the Ensemble API, e.g. https://<tailscale-host>:8181
                      (the script appends /api/import/proposal)
  ENSEMBLE_IMPORT_KEY the shared import key (sent as the X-Import-Key header)

Artifact — supply at least one of --pdf / --html / --sections-json. They compose:
a PDF is uploaded as-is; HTML is rendered to PDF server-side; structured JSON
slots into the proposal record and is re-renderable.

Examples:
  ENSEMBLE_API_URL=https://r740.tailnet.ts.net:8181 ENSEMBLE_IMPORT_KEY=... \
    python handoff_proposal.py --company "Transdev" --title "ISO 55001 uplift" \
      --pdf ~/proposals/transdev.pdf --sector Transport \
      --contact ops.director@transdev.com.au

  python handoff_proposal.py --company "Yarra Trams" --html ./proposal.html --dry-run
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request


def _read_bytes(path: str) -> bytes:
    with open(os.path.expanduser(path), "rb") as fh:
        return fh.read()


def _read_text(path: str) -> str:
    with open(os.path.expanduser(path), encoding="utf-8") as fh:
        return fh.read()


def build_body(args: argparse.Namespace) -> dict:
    body: dict[str, object] = {"company": args.company, "source": args.source}
    if args.client_name:
        body["client_name"] = args.client_name
    if args.title:
        body["proposal_title"] = args.title
    if args.sector:
        body["sector"] = args.sector
    if args.contact:
        body["primary_contact_email"] = args.contact
    if args.notes:
        body["notes"] = args.notes

    if args.pdf:
        body["proposal_pdf_base64"] = base64.b64encode(_read_bytes(args.pdf)).decode()
    if args.html:
        body["proposal_html"] = _read_text(args.html)
    if args.sections_json:
        data = json.loads(_read_text(args.sections_json))
        # Accept either a bare sections dict or a full structured object.
        for key in ("proposal_sections", "client_problem_map", "timeline_weeks",
                    "case_study_references"):
            if isinstance(data, dict) and key in data:
                body[key] = data[key]
        if "proposal_sections" not in body and isinstance(data, dict) and \
                not any(k in data for k in ("client_problem_map", "timeline_weeks")):
            body["proposal_sections"] = data

    if not any(k in body for k in ("proposal_pdf_base64", "proposal_html", "proposal_sections")):
        sys.exit("error: supply at least one artifact — --pdf, --html, or --sections-json")
    return body


def post(api_url: str, key: str, body: dict) -> dict:
    url = api_url.rstrip("/") + "/api/import/proposal"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "X-Import-Key": key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        sys.exit(f"error: {exc.code} from {url}\n{detail}")
    except urllib.error.URLError as exc:
        sys.exit(f"error: cannot reach {url} — {exc.reason}\n"
                 "Check ENSEMBLE_API_URL and that you're on the Tailscale tailnet.")


def main() -> None:
    p = argparse.ArgumentParser(description="Hand a proposal into the Ensemble opportunities pipeline.")
    p.add_argument("--company", required=True, help="prospect company (find-or-create key)")
    p.add_argument("--title", help="proposal title (default: 'Proposal — <company>')")
    p.add_argument("--client-name", help="client/account name if different from company")
    p.add_argument("--sector", help="sector, e.g. Transport / Water / Resources")
    p.add_argument("--contact", help="primary contact email")
    p.add_argument("--notes", help="free-text context for the import")
    p.add_argument("--pdf", help="path to a finished proposal PDF")
    p.add_argument("--html", help="path to a single-page proposal HTML")
    p.add_argument("--sections-json", help="path to structured proposal JSON "
                   "(proposal_sections / client_problem_map / timeline_weeks / case_study_references)")
    p.add_argument("--source", default="proposal_handoff", help="source tag (default: proposal_handoff)")
    p.add_argument("--api-url", default=os.environ.get("ENSEMBLE_API_URL"),
                   help="Ensemble API base URL (default: $ENSEMBLE_API_URL)")
    p.add_argument("--key", default=os.environ.get("ENSEMBLE_IMPORT_KEY"),
                   help="import key (default: $ENSEMBLE_IMPORT_KEY)")
    p.add_argument("--dry-run", action="store_true", help="build + print the body, don't POST")
    args = p.parse_args()

    body = build_body(args)

    if args.dry_run:
        preview = {k: (f"<{len(v)} chars>" if isinstance(v, str) and len(v) > 200 else v)
                   for k, v in body.items()}
        print(json.dumps(preview, indent=2))
        return

    if not args.api_url:
        sys.exit("error: no API URL — set ENSEMBLE_API_URL or pass --api-url")
    if not args.key:
        sys.exit("error: no import key — set ENSEMBLE_IMPORT_KEY or pass --key")

    result = post(args.api_url, args.key, body)
    print(json.dumps(result, indent=2))
    if result.get("opportunity_id"):
        verb = "created" if result.get("created") else "updated"
        pdf = "with PDF" if result.get("pdf_attached") else "no PDF"
        print(f"\n✓ {result.get('company')}: opportunity {verb} at stage "
              f"{result.get('stage')} ({result.get('stage_name')}), proposal attached ({pdf}).",
              file=sys.stderr)


if __name__ == "__main__":
    main()
