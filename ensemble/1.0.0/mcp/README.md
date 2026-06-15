# Ensemble operational MCP server

A **local stdio** MCP server that gives a tethered consultant's Claude Code session first-class
read+write tools over the Ensemble (SAS OPS) API — instead of every skill hand-rolling HTTP. It
runs on the consultant's own machine and calls the Tailscale-only API over the tailnet.

## How it's wired

Every engagement repo created from the template ships a project-scoped `.mcp.json` that launches
this server over stdio:

```jsonc
{
  "mcpServers": {
    "ensemble": {
      "command": "uv",
      "args": ["run", "--with", "mcp>=1.2.0", "--with", "httpx>=0.27.0", "--python", "3.12",
               "python", "${HOME}/.claude/SASAMClaudeCodeSkills/ensemble/1.0.0/mcp/ensemble_mcp_server.py"],
      "env": { "ENSEMBLE_CONFIG": "${HOME}/.ensemble/config.json" }
    }
  }
}
```

`uv run --with` resolves `mcp` + `httpx` into an ephemeral, cached env — no persistent install.
**Fallback** if `uv` is unavailable: `python3.12 -m venv ~/.ensemble/mcp-venv && ~/.ensemble/mcp-venv/bin/pip install -r requirements.txt`, then point the `.mcp.json` `command` at `~/.ensemble/mcp-venv/bin/python`.

Claude Code prompts to approve the project MCP server on first session; the template's
`.claude/settings.json` pre-approves the `ensemble` tools via `"mcp__ensemble"` in its allow-list.

## Provisioning (per consultant) — secrets live ONLY in `~/.ensemble/config.json`

`.mcp.json` is shared via the repo and carries **no secrets**. This server reads them itself:

```jsonc
// ~/.ensemble/config.json   (mode 0600)
{
  "api_url":    "https://cortex-t4.<tailnet>.ts.net:8181",
  "api_key":    "<your consultant X-API-Key>",
  "import_key": "<the X-Import-Key>",
  "verify_tls": true        // optional; default true. Set false (or a CA path) only if a
                            // deployment uses a self-signed cert — never disable casually.
}
```

A consultant key is **scoped** (read + a few narrow writes, never `write_approvals` by default)
and **bound to your own engagement(s)** server-side. It is provisioned into the API's key registry
by the founder; rotate/revoke there. Do **not** paste any key into `.mcp.json`.

## Auth status of the tools

- **Works today** (X-API-Key / X-Import-Key): `ensemble_list_approvals`,
  `ensemble_transition_approval`, the `ensemble_*_research` tools, `ensemble_import_beam_lead`.
- **Gated** on the hardened-auth backend (typed `Principal`/`get_principal` + default-deny route
  allowlist + per-engagement scoping — the plan's Part B.4 M1–M6): the `hmi`/`projects`/`crm`/
  `issue-flags` tools. Until that ships they return 401/403 — surfaced verbatim with a hint.
- `ensemble_import_proposal` needs the backend `POST /import/proposal` route (Part B.5) — 404 until then.

## The boundary (important)

This server **complements** the git-queue → PR → tier-gate handoff, which stays the **audited**
path for fleet deliverable work. The MCP tools are for queries, the already-HTTP imports, HMI task
assignment, and approvals. **Never** use them to submit deliverables — hand deliverable work to the
Ensemble with the `/handoff` skill (git queue), so it lands as a reviewed PR into `main`.

## Verify

```bash
# 1. reachability + auth (no MCP):
curl -fsS -H "X-API-Key: $KEY" "$API_URL/api/approvals?limit=5"

# 2. tool list via the inspector:
npx @modelcontextprotocol/inspector \
  uv run --with mcp --with httpx python ensemble_mcp_server.py

# 3. in Claude Code: open a tethered engagement, approve the 'ensemble' server, run `/mcp`.
```
