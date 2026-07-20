#!/usr/bin/env python3
"""ensemble_mcp_server.py — local stdio MCP server wrapping the Ensemble operational API.

Gives a tethered consultant's Claude Code session first-class read+write tools over the
Ensemble (SAS OPS) API, instead of every skill hand-rolling HTTP. It runs LOCALLY on the
consultant's machine and calls the tailnet API over Tailscale.

CONFIG — read from $ENSEMBLE_CONFIG or ~/.ensemble/config.json (mode 0600). Secrets live
ONLY here, never in the repo-shared .mcp.json:
    {
      "api_url":    "https://cortex-t4.<tailnet>.ts.net:8181",
      "api_key":    "<consultant X-API-Key>",
      "import_key": "<X-Import-Key>",
      "verify_tls": true          # optional; default true. May be false or a CA-bundle path.
    }
Env overrides: ENSEMBLE_API_URL, ENSEMBLE_API_KEY, ENSEMBLE_IMPORT_KEY, ENSEMBLE_VERIFY_TLS.

BOUNDARY — this server COMPLEMENTS the git-queue -> PR -> tier-gate handoff, which remains the
*audited* path for fleet deliverable work. The server is for queries + the already-HTTP imports
+ HMI task assignment + approvals. It must NEVER become a deliverable-submission route; to hand
deliverable work to the Ensemble, use the /handoff skill (git queue), not these tools.

AUTH STATUS (read the docstrings):
  * WORKS TODAY (X-API-Key / X-Import-Key): the approvals tools, the research tools, and the
    import tools.
  * GATED on the hardened-auth backend (Principal/get_principal + default-deny route allowlist
    + per-engagement scoping; see the plan's Part B.4 M1-M6): the hmi/projects/crm/issue-flags
    tools. Until that ships they return 401/403 — which this server surfaces verbatim.
  * A consultant key is scoped (read + narrow writes, never write_approvals by default) and
    bound to its own engagement(s); cross-engagement or founder-only routes return 403.

Every write tool's docstring asks Claude to CONFIRM the target with the consultant before calling.
HTTP errors are returned (not raised) with the response body verbatim, so a 422 (e.g. an invalid
approval transition) or a 403 (scope) is actionable rather than a silent failure.
"""
from __future__ import annotations

import json
import os
import pathlib
from typing import Any

import httpx

try:
    from mcp.server.fastmcp import FastMCP
except Exception as exc:  # pragma: no cover - import guard for a clearer error
    raise SystemExit(
        "ensemble MCP server requires the 'mcp' package. Launch via "
        "'uv run --with mcp>=1.2.0 --with httpx>=0.27.0 python ensemble_mcp_server.py' "
        f"(import failed: {exc})"
    )

__version__ = "1.0.0"

# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
_DEFAULT_API_URL = "https://cortex-t4.tail060c48.ts.net:8181"


def _config_path() -> str:
    return os.environ.get("ENSEMBLE_CONFIG") or str(
        pathlib.Path.home() / ".ensemble" / "config.json"
    )


def _load_config() -> dict[str, Any]:
    """Read ~/.ensemble/config.json (or $ENSEMBLE_CONFIG). A MISSING file is fine — env
    vars may supply everything — and returns {}. But a PRESENT, corrupt/invalid-JSON file
    is an ACTIONABLE error: fail fast rather than silently behaving as unauthenticated
    (mirrors the corrupt-config handling in skills/_lib/ensemble_common.py)."""
    path = pathlib.Path(_config_path())
    if not path.exists():
        return {}
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"ensemble MCP: cannot read config {path}: {exc}")
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ensemble MCP: {path} is not valid JSON: {exc}")
    if not isinstance(data, dict):
        raise SystemExit(f"ensemble MCP: {path} must contain a JSON object, got {type(data).__name__}")
    return data


_CFG = _load_config()


def _cfg(key: str, env: str, default: Any = "") -> Any:
    val = os.environ.get(env)
    if val is not None and val != "":
        return val
    return _CFG.get(key, default)


API_URL = str(_cfg("api_url", "ENSEMBLE_API_URL", _DEFAULT_API_URL)).rstrip("/")
API_KEY = str(_cfg("api_key", "ENSEMBLE_API_KEY", ""))
IMPORT_KEY = str(_cfg("import_key", "ENSEMBLE_IMPORT_KEY", ""))


def _resolve_verify() -> Any:
    """TLS verification: True by default (Tailscale issues valid certs). Never silently
    disable. An explicit `verify_tls: false` opt-in or a CA-bundle path is honoured."""
    raw = _cfg("verify_tls", "ENSEMBLE_VERIFY_TLS", True)
    if isinstance(raw, bool):
        return raw
    s = str(raw).strip()
    if s.lower() in {"false", "0", "no"}:
        return False
    if s.lower() in {"true", "1", "yes", ""}:
        return True
    return s  # treat as a CA-bundle path


# nginx strips the /api/ prefix and proxies FastAPI; the public path is <api_url>/api/<route>.
# IMPORTANT: httpx replaces a base_url path when the request path is ABSOLUTE (starts with
# "/"). base_url=<host>/api + request "/approvals" would resolve to <host>/approvals — wrong,
# bypassing the nginx /api route. So we keep base_url at the host and prefix "/api" inside
# _call (paths there start with "/", e.g. "/approvals" -> <host>/api/approvals).
_client = httpx.Client(base_url=API_URL, timeout=30.0, verify=_resolve_verify())

mcp = FastMCP("ensemble")


# --------------------------------------------------------------------------- #
# HTTP plumbing — return structured results; surface error bodies verbatim.
# --------------------------------------------------------------------------- #
def _clean(params: dict[str, Any] | None) -> dict[str, Any]:
    if not params:
        return {}
    return {k: v for k, v in params.items() if v is not None and v != ""}


def _body(resp: httpx.Response) -> Any:
    try:
        return resp.json()
    except Exception:
        return resp.text


def _hint(code: int) -> str:
    if code in (401, 403):
        return (
            "Auth/scope rejected. Either your consultant key lacks the scope/engagement for this "
            "route, or the route is founder-only, or this endpoint still requires the hardened-auth "
            "backend (Part B.4 M1-M6) that lets it accept an X-API-Key. Check ~/.ensemble/config.json."
        )
    if code == 404:
        return "Not found. (Note: ensemble_import_proposal needs the backend POST /import/proposal route, which may not exist yet.)"
    if code == 422:
        return "Validation/state error — see 'detail' for the exact reason (e.g. an invalid approval transition)."
    return ""


def _call(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    import_key: bool = False,
) -> Any:
    if import_key:
        if not IMPORT_KEY:
            return {
                "ok": False,
                "error": "no_import_key",
                "detail": f"import_key not set (env ENSEMBLE_IMPORT_KEY, or 'import_key' in {_config_path()})",
            }
        headers = {"X-Import-Key": IMPORT_KEY}
    else:
        if not API_KEY:
            return {
                "ok": False,
                "error": "no_api_key",
                "detail": f"api_key not set (env ENSEMBLE_API_KEY, or 'api_key' in {_config_path()})",
            }
        headers = {"X-API-Key": API_KEY}
    try:
        resp = _client.request(method, "/api" + path, params=_clean(params), json=json_body, headers=headers)
    except httpx.HTTPError as exc:
        return {
            "ok": False,
            "error": "request_failed",
            "detail": str(exc),
            "hint": f"Could not reach {API_URL}. Confirm Tailscale is up and api_url is correct.",
        }
    if resp.status_code >= 400:
        return {
            "ok": False,
            "status": resp.status_code,
            "error": f"HTTP {resp.status_code}",
            "detail": _body(resp),
            "hint": _hint(resp.status_code),
        }
    return _body(resp)


# =========================================================================== #
# status / dashboard  (read)   — GATED on hardened-auth backend
# =========================================================================== #
@mcp.tool()
def ensemble_morning_brief() -> Any:
    """Latest morning brief (outputs queued for approval). Read-only. [needs hardened-auth backend]"""
    return _call("GET", "/hmi/morning-brief/latest")


@mcp.tool()
def ensemble_list_standup_reports(limit: int = 10) -> Any:
    """Recent agent standup reports. Read-only. [needs hardened-auth backend]"""
    return _call("GET", "/hmi/standup-reports", params={"limit": limit})


@mcp.tool()
def ensemble_list_intelligence_digests(limit: int = 10) -> Any:
    """Recent intelligence digests (Sigrid/Eirik daily briefs). Read-only. [needs hardened-auth backend]"""
    return _call("GET", "/hmi/intelligence-digests", params={"limit": limit})


@mcp.tool()
def ensemble_client_dossier(client_id: str) -> Any:
    """B2B research dossier snapshot for a client. Read-only. Engagement-scoped. [needs hardened-auth backend]"""
    return _call("GET", f"/hmi/clients/{client_id}/dossier")


# =========================================================================== #
# approvals  (read + write)   — WORKS TODAY (verify_api_key_or_jwt)
# =========================================================================== #
@mcp.tool()
def ensemble_list_approvals(status: str = "PENDING_APPROVAL", agent_id: str = "", limit: int = 50) -> Any:
    """List the approval queue. Read-only. WORKS TODAY.

    status filters by approval state (default PENDING_APPROVAL); agent_id optionally narrows by agent.
    """
    return _call("GET", "/approvals", params={"status": status, "agent_id": agent_id, "limit": limit})


@mcp.tool()
def ensemble_transition_approval(output_id: str, to_status: str, reviewer_comment: str = "") -> Any:
    """Transition an agent output through the approval state machine. WORKS TODAY.

    to_status is one of APPROVED | REJECTED | NEEDS_REVISION. Invalid transitions return 422
    (surfaced verbatim). NOTE: APPROVED can fire downstream effects (remediation dispatch,
    topic->calendar promotion, agent respawn). CONFIRM the output_id + target status with the
    consultant before calling.
    """
    return _call(
        "POST",
        f"/approvals/{output_id}/transition",
        json_body={"to_status": to_status, "reviewer_comment": reviewer_comment or None},
    )


# =========================================================================== #
# tasks  (read + write)  — HMI standup queue, NOT the deliverable handoff
# =========================================================================== #
@mcp.tool()
def ensemble_list_tasks() -> Any:
    """List queued/running HMI tasks. Read-only. [needs hardened-auth backend]"""
    return _call("GET", "/hmi/tasks")


@mcp.tool()
def ensemble_assign_task(
    agent_id: str, title: str, description: str = "", priority: str = "normal", fire_now: bool = False
) -> Any:
    """Assign a task to an Ensemble agent (drained at the next 06:00 standup, or immediately if
    fire_now). This assigns AGENT ATTENTION; it is NOT the deliverable-work handoff — for that use
    the /handoff skill (git queue). CONFIRM agent_id + title with the consultant first.
    [needs hardened-auth backend]
    """
    return _call(
        "POST",
        "/hmi/tasks",
        json_body={
            "agent_id": agent_id,
            "title": title,
            "description": description,
            "priority": priority,
            "fire_now": fire_now,
        },
    )


@mcp.tool()
def ensemble_update_task(task_id: str, current_state: str, next_state: str, result_summary: str = "") -> Any:
    """Update an HMI task's state. Optimistic-locked on current_state (409 on mismatch — read the
    current state via ensemble_list_tasks first). [needs hardened-auth backend]
    """
    return _call(
        "PATCH",
        f"/hmi/tasks/{task_id}",
        json_body={"current_state": current_state, "next_state": next_state, "result_summary": result_summary or None},
    )


# =========================================================================== #
# projects / delivery (read + write)   — GATED on hardened-auth backend
# =========================================================================== #
@mcp.tool()
def ensemble_list_projects() -> Any:
    """List delivery projects/engagements. Read-only. Engagement-scoped. [needs hardened-auth backend]"""
    return _call("GET", "/projects")


@mcp.tool()
def ensemble_get_project(project_id: str) -> Any:
    """Project detail (workstreams, tasks, gates, risks, forecast). Read-only. Engagement-scoped. [needs hardened-auth backend]"""
    return _call("GET", f"/projects/{project_id}")


@mcp.tool()
def ensemble_create_project(name: str, project_type: str = "advisory", tier: str = "full") -> Any:
    """Create a delivery project. CONFIRM with the consultant first. [needs hardened-auth backend]
    (project_type maps to the API 'type' field; body is best-effort — a 422 will name the expected fields.)
    """
    return _call("POST", "/projects", json_body={"name": name, "type": project_type, "tier": tier})


@mcp.tool()
def ensemble_create_project_task(
    project_id: str,
    name: str,
    description: str = "",
    workstream_id: str = "",
    phase_no: int | None = None,
) -> Any:
    """Add a task to a project. Pass workstream_id (from ensemble_get_project) so the task lands
    inside a workstream — without it the task is created unassigned. Engagement-scoped.
    CONFIRM first. [needs hardened-auth backend]"""
    return _call(
        "POST",
        f"/projects/{project_id}/tasks",
        json_body=_clean({
            "name": name,
            "description": description,
            "workstream_id": workstream_id,
            "phase_no": phase_no,
        }),
    )


@mcp.tool()
def ensemble_update_project_task(
    project_id: str,
    task_id: str,
    status: str = "",
    name: str = "",
    description: str = "",
) -> Any:
    """Update a project task (status, name and/or description). Only the fields you pass are
    changed — empty fields are omitted from the update. Engagement-scoped. [needs hardened-auth backend]"""
    body = _clean({"status": status, "name": name, "description": description})
    if not body:
        return {
            "ok": False,
            "error": "no_fields",
            "detail": "Pass at least one of status, name or description to update.",
        }
    return _call("PATCH", f"/projects/{project_id}/tasks/{task_id}", json_body=body)


@mcp.tool()
def ensemble_decide_gate(project_id: str, phase_no: int, decision: str, note: str = "") -> Any:
    """Record a marcov.GATE phase decision (advances the project phase). HIGH-CONSEQUENCE — echo the
    project tier (via ensemble_get_project) and CONFIRM project + phase + decision with the consultant
    before calling. [needs hardened-auth backend]
    """
    return _call("POST", f"/projects/{project_id}/gates/{phase_no}/decide", json_body={"decision": decision, "note": note})


# =========================================================================== #
# opportunities / CRM  (read + write)   — GATED on hardened-auth backend
# =========================================================================== #
@mcp.tool()
def ensemble_list_opportunities(stage: str = "", limit: int = 50) -> Any:
    """List BEAM opportunities. Read-only. Engagement-scoped. [needs hardened-auth backend]"""
    return _call("GET", "/hmi/opportunities", params={"stage": stage, "limit": limit})


@mcp.tool()
def ensemble_get_opportunity(opportunity_id: str) -> Any:
    """Opportunity detail (stage, gates, contacts, evidence). Read-only. Engagement-scoped. [needs hardened-auth backend]"""
    return _call("GET", f"/hmi/opportunities/{opportunity_id}")


@mcp.tool()
def ensemble_assess_opportunity(opportunity_id: str) -> Any:
    """Queue a stage assessment (enqueues eirikSolheim; async — returns 202, no result body).
    Engagement-scoped. [needs hardened-auth backend]
    """
    return _call("POST", f"/hmi/opportunities/{opportunity_id}/assess")


@mcp.tool()
def ensemble_set_opportunity_status(opportunity_id: str, status: str = "", win_probability: float = -1.0) -> Any:
    """Set an opportunity's stage/status (and optional win_probability 0-100). Direct mutation —
    CONFIRM first. Engagement-scoped. [needs hardened-auth backend]
    """
    body: dict[str, Any] = {}
    if status:
        body["status"] = status
    if win_probability >= 0:
        body["win_probability"] = win_probability
    return _call("POST", f"/hmi/opportunities/{opportunity_id}/status", json_body=body)


@mcp.tool()
def ensemble_add_opportunity_evidence(
    opportunity_id: str, claim: str, stage: str = "", gate: str = "", source: str = ""
) -> Any:
    """Attach an evidence item to an opportunity. Engagement-scoped. [needs hardened-auth backend]"""
    return _call(
        "POST",
        f"/hmi/opportunities/{opportunity_id}/evidence",
        json_body={"claim": claim, "stage": stage, "gate": gate, "source": source},
    )


@mcp.tool()
def ensemble_list_contacts(query: str = "", limit: int = 50) -> Any:
    """List CRM contacts (optional free-text query). Read-only. [needs hardened-auth backend]"""
    return _call("GET", "/hmi/crm/contacts", params={"query": query, "limit": limit})


@mcp.tool()
def ensemble_create_contact(name: str, email: str = "", title: str = "", org: str = "") -> Any:
    """Create a CRM contact. CONFIRM first. [needs hardened-auth backend]"""
    return _call("POST", "/hmi/crm/contacts", json_body={"name": name, "email": email, "title": title, "org": org})


@mcp.tool()
def ensemble_update_contact(contact_id: str, name: str = "", email: str = "", title: str = "", org: str = "") -> Any:
    """Update a CRM contact (only non-empty fields are sent). [needs hardened-auth backend]"""
    body = {k: v for k, v in {"name": name, "email": email, "title": title, "org": org}.items() if v}
    return _call("PATCH", f"/hmi/crm/contacts/{contact_id}", json_body=body)


# =========================================================================== #
# issue-flags  (read + write)   — GATED on hardened-auth backend
# =========================================================================== #
@mcp.tool()
def ensemble_list_issue_flags(status: str = "", target_type: str = "") -> Any:
    """List IssueFlags (the Uplift Roadmap intake). Read-only. [needs hardened-auth backend]"""
    return _call("GET", "/hmi/issue-flags", params={"status": status, "target_type": target_type})


@mcp.tool()
def ensemble_create_issue_flag(
    target_type: str,
    target_id: str,
    title: str,
    description: str,
    category: str = "bug",
    severity: str = "medium",
    frequency: str = "sometimes",
) -> Any:
    """Raise an IssueFlag — the single intake feeding the Uplift Roadmap. Use this to FLAG
    out-of-scope work (a bug or a substantial improvement) rather than actioning it inline.
    category: bug|error|missing_capability ; severity: low|medium|high|critical ;
    frequency: rarely|sometimes|often|constant ; target_type like agent:<id> / page:<route> /
    capability:<slug>. Make title + description build-ready. [needs hardened-auth backend]
    """
    return _call(
        "POST",
        "/hmi/issue-flags",
        json_body={
            "target_type": target_type,
            "target_id": target_id,
            "title": title,
            "description": description,
            "category": category,
            "severity": severity,
            "frequency": frequency,
            "submitted_by": "consultant-mcp",
            "status": "new",
        },
    )


@mcp.tool()
def ensemble_update_issue_flag(flag_id: str, status: str = "") -> Any:
    """Update an IssueFlag (e.g. acknowledge/close). [needs hardened-auth backend]"""
    return _call("PATCH", f"/hmi/issue-flags/{flag_id}", json_body={"status": status})


# =========================================================================== #
# imports  (write)   — X-Import-Key. beam-lead WORKS TODAY; proposal needs the B.5 route.
# =========================================================================== #
@mcp.tool()
def ensemble_import_beam_lead(
    company: str,
    sector: str = "",
    current_stage: str = "",
    stage_name: str = "",
    status: str = "",
    primary_contact_email: str = "",
    client_name: str = "",
    source: str = "",
    win_probability: str = "",
    fit_score: str = "",
    timing_score: str = "",
    deal_estimate: str = "",
    gates: dict | list | None = None,
    stakeholders: list | None = None,
    evidence: list | None = None,
    next_steps: list | None = None,
    notes: str = "",
) -> Any:
    """Import a BEAM lead into the opportunities pipeline (upsert client + Opportunity by company).
    Pass the full developed BEAM; confirm with the consultant first. X-Import-Key. Liberal: only
    `company` is required — everything else (gates, stakeholders, evidence, next_steps, scores,
    stage_name/status/client_name/source) is optional and passed through untouched; the backend
    coercers own the shape. Empty/None fields are dropped before sending, so a re-commit (upsert
    by company) enriches rather than blanking previously-set fields.
    """
    return _call(
        "POST",
        "/import/beam-lead",
        import_key=True,
        json_body=_clean({
            "company": company,
            "sector": sector,
            "current_stage": current_stage,
            "stage_name": stage_name,
            "status": status,
            "primary_contact_email": primary_contact_email,
            "client_name": client_name,
            "source": source,
            "win_probability": win_probability,
            "fit_score": fit_score,
            "timing_score": timing_score,
            "deal_estimate": deal_estimate,
            "gates": gates,
            "stakeholders": stakeholders,
            "evidence": evidence,
            "next_steps": next_steps,
            "notes": notes,
        }),
    )


@mcp.tool()
def ensemble_import_proposal(
    company: str,
    proposal_title: str = "",
    proposal_html: str = "",
    client_name: str = "",
    sector: str = "",
    notes: str = "",
) -> Any:
    """Hand an externally-authored proposal INTO the opportunities pipeline (find-or-create
    opportunity by company, advance to "Propose", attach the proposal). X-Import-Key.
    NOTE: needs the backend POST /import/proposal route (plan Part B.5) — returns 404 until it lands.
    CONFIRM with the consultant first.
    """
    return _call(
        "POST",
        "/import/proposal",
        import_key=True,
        json_body={
            "company": company,
            "proposal_title": proposal_title,
            "proposal_html": proposal_html,
            "client_name": client_name,
            "sector": sector,
            "notes": notes,
        },
    )


# =========================================================================== #
# research  (read + write)   — WORKS TODAY (verify_api_key)
# =========================================================================== #
@mcp.tool()
def ensemble_submit_research(query: str, requesting_agent_id: str = "consultant-mcp", priority: str = "normal") -> Any:
    """Submit a deep-research request to the sorenAaberg queue. WORKS TODAY.
    priority: urgent | normal | background. Returns the created request (poll results with
    ensemble_get_research_results).
    """
    return _call(
        "POST",
        "/research",
        json_body={"requesting_agent_id": requesting_agent_id, "query": query, "priority": priority},
    )


@mcp.tool()
def ensemble_list_research(status: str = "", limit: int = 50) -> Any:
    """List research requests (urgent first). WORKS TODAY. Optional status:
    PENDING | IN_PROGRESS | COMPLETED | FAILED.
    """
    return _call("GET", "/research", params={"status": status, "limit": limit})


@mcp.tool()
def ensemble_get_research_results(request_id: str) -> Any:
    """Fetch the results of a completed research request. WORKS TODAY.

    NOTE: this returns Soren's research-request results. There is currently no HTTP route for a
    direct pgvector library/brain vector search; a dedicated `ensemble_library_search` would need
    a new backend POST /research/retrieve (optional follow-up, not shipped to avoid a broken tool).
    """
    return _call("GET", f"/research/{request_id}/results")


if __name__ == "__main__":
    mcp.run()
