#!/usr/bin/env python3
"""submit_state.py — render the outbox files for the /submit skill, deterministically.

/submit lets a consultant bring in work they did THEMSELVES (offline / by hand),
match it to one or more engagement deliverables ("Lars's delivery page"), and land
it as a reviewed PR into `main`. The PR carries a self-contained result set under
``handoffs/outbox/<id>/``:

  packet.md       front-matter packet (schema-valid) — this is what tier-gate.yml
                  reads for review_tier + requested_by, so the PR gates correctly.
  summary.md      the human-readable submission: what was done, which deliverables it
                  satisfies, the evidence, and the artefact list.
  submission.json structured deliverable claims, for the fleet to reconcile the
                  Deliverable rows (status -> DELIVERED) on merge.

This module owns ONLY the file rendering + schema validation (so quoting/JSON safety
lives in one place). The bash driver (``submit.sh``) does the git/gh orchestration.

Subcommand:

  build
      Read a JSON config object from stdin, render the three files into the outbox
      directory, validating packet.md against the engagement's packet.schema.json
      BEFORE writing anything. Exit non-zero (with errors on stderr) on any failure.

Stdlib only. Australian English in user-facing strings. Never prints secrets.
"""
from __future__ import annotations

import json
import os
import sys

import ensemble_common as e

# Packet front-matter is `additionalProperties: false`, so submission-specific data
# (deliverables, evidence) lives in submission.json / summary.md — NOT in packet.md.
_PACKET_ORDER = [
    "id", "engagement", "requested_by", "kind", "review_tier",
    "route_hint", "deadline", "inputs", "definition_of_done",
    "retries", "context",
]


def _yval(v: object) -> str:
    """A JSON scalar — valid YAML for the stdlib parser and unambiguous."""
    return json.dumps(v, ensure_ascii=False)


def _ylist(items: list) -> str:
    return "[" + ", ".join(json.dumps(i, ensure_ascii=False) for i in items) + "]"


def _render_packet(cfg: dict) -> str:
    fm = {
        "id": cfg["id"],
        "engagement": cfg["engagement"],
        "requested_by": cfg["requested_by"],
        "kind": cfg.get("kind", "task"),
        "review_tier": cfg["review_tier"],
        "route_hint": cfg.get("route_hint", "api"),
        "deadline": cfg.get("deadline", "none"),
        "inputs": cfg.get("inputs", []),
        "definition_of_done": cfg["definition_of_done"],
        "retries": 0,
        "context": cfg.get("context", []),
    }
    out = ["---"]
    for k in _PACKET_ORDER:
        v = fm[k]
        out.append(f"{k}: {_ylist(v)}" if isinstance(v, list) else f"{k}: {_yval(v)}")
    out.append("---")
    out.append("")
    out.append("## Brief")
    out.append("")
    delivs = cfg.get("deliverables", [])
    out.append(
        "Consultant submission of work completed outside the fleet. "
        + (f"Claimed against deliverable(s): {', '.join(delivs)}. " if delivs else "")
        + "See summary.md and submission.json in this folder."
    )
    out.append("")
    if cfg.get("evidence"):
        out.append(cfg["evidence"].rstrip() + "\n")
    return "\n".join(out)


def _render_summary(cfg: dict) -> str:
    delivs = cfg.get("deliverables", [])
    arts = cfg.get("inputs", [])
    L = [
        f"# Submission — {cfg['title']}",
        "",
        f"- **Submitted by:** {cfg['requested_by']}",
        f"- **Engagement:** {cfg['engagement']}",
        f"- **Review tier:** {cfg['review_tier']}",
        "",
        "## Deliverables this satisfies",
        "",
    ]
    L += [f"- {d}" for d in delivs] or ["- (none matched — free submission; triage to file)"]
    L += ["", "## Evidence / how it meets the criteria", "", cfg.get("evidence", "_(none provided)_"), ""]
    L += ["## Acceptance criteria claimed", ""]
    L += [f"- [x] {c}" for c in cfg.get("definition_of_done", [])] or ["- (none stated)"]
    L += ["", "## Artefacts in this submission", ""]
    L += [f"- `{a}`" for a in arts] or ["- (none attached)"]
    L += [""]
    return "\n".join(L)


def _render_submission_json(cfg: dict) -> str:
    obj = {
        "id": cfg["id"],
        "engagement": cfg["engagement"],
        "submitted_by": cfg["requested_by"],
        "submitted_at": cfg["submitted_at"],
        "title": cfg["title"],
        "review_tier": cfg["review_tier"],
        "deliverable_claims": [
            {"deliverable": d, "accepted_claim": True} for d in cfg.get("deliverables", [])
        ],
        "acceptance_criteria": cfg.get("definition_of_done", []),
        "evidence": cfg.get("evidence", ""),
        "artefacts": cfg.get("inputs", []),
    }
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def _build() -> int:
    cfg = json.load(sys.stdin)
    for req in ("id", "engagement", "requested_by", "review_tier", "title",
                "definition_of_done", "outbox_abs", "schema"):
        if not cfg.get(req):
            print(f"ensemble: submit build is missing required field {req!r}.", file=sys.stderr)
            return 2

    packet_text = _render_packet(cfg)

    # Validate the packet against the engagement's schema BEFORE writing anything.
    parsed, _brief = e.split_packet(packet_text)
    errs = e.validate_packet(parsed, cfg["schema"])
    if errs:
        print("ensemble: submission packet failed schema validation:", file=sys.stderr)
        for er in errs:
            print(f"  - {er}", file=sys.stderr)
        return 1

    outbox = cfg["outbox_abs"]
    os.makedirs(outbox, exist_ok=True)
    with open(os.path.join(outbox, "packet.md"), "w", encoding="utf-8") as fh:
        fh.write(packet_text)
    with open(os.path.join(outbox, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write(_render_summary(cfg))
    with open(os.path.join(outbox, "submission.json"), "w", encoding="utf-8") as fh:
        fh.write(_render_submission_json(cfg))
    print(f"ensemble: wrote packet.md, summary.md, submission.json into {outbox}", file=sys.stderr)
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] != "build":
        print("usage: submit_state.py build  (reads a JSON config on stdin)", file=sys.stderr)
        return 2
    try:
        return _build()
    except e.EnsembleError as exc:
        print(f"ensemble: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"ensemble: could not parse the submit config JSON: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
