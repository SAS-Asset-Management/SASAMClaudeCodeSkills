---
name: project-manager
description: marcov.GATE project delivery framework. Manage projects through a 5-phase stage-gated lifecycle with visual dashboards and portfolio tracking.
arguments:
  - name: action
    description: "Subcommand: new, status, gate-review, dashboard, portfolio, report, update, close, list"
    required: false
  - name: target
    description: "Client name, project name, or project ID (depends on subcommand)"
    required: false
---

Invoke the project-manager skill with the provided arguments.

If `action` is provided, route directly to that subcommand.
If no `action` is provided, show available subcommands and ask which to run.

Valid actions:
- `new` — Start a new project (optionally with client and project name)
- `status` — Show current project status
- `gate-review` — Run evidence-gated phase advancement
- `dashboard` — Generate per-project visual dashboard
- `portfolio` — Sweep all repos, generate master board
- `report` — Generate client-ready status page
- `update` — Update project state interactively
- `close` — Run close-out process
- `list` — List all discovered projects
