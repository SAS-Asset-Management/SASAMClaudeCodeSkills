#!/usr/bin/env python3
"""
deployGate.py — Automate gated download deployment to Cortex4 server.

Handles the full server-side deployment:
  1. SCP the asset file to the sas-gate assets directory
  2. Register the resource in resources.json
  3. Restart the sas-gate container
  4. Verify the container is running

Usage:
  python3 deployGate.py <asset_file> <resource_slug> <label> [--dry-run]

Examples:
  python3 deployGate.py ./maintenanceBusinessCase.html maintenance-business-case "Maintenance Business Case Template"
  python3 deployGate.py ./pmChecklist.html pm-effectiveness-checklist "PM Effectiveness Audit Checklist" --dry-run
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

# ── Server Configuration ──────────────────────────────────────────────
SERVER_HOST = "cortext4@cortext-t4"
SERVER_PASS = "iso55001:2024"
PROJECT_DIR = "/home/cortext4/docker/clientDatabase"
ASSETS_DIR = f"{PROJECT_DIR}/app/assets"
RESOURCES_JSON = f"{ASSETS_DIR}/resources.json"


def ssh_cmd(command, capture=True):
    """Execute a command on the remote server via sshpass + ssh."""
    full = [
        "sshpass", "-p", SERVER_PASS,
        "ssh", "-o", "StrictHostKeyChecking=no", SERVER_HOST,
        command,
    ]
    if capture:
        result = subprocess.run(full, capture_output=True, text=True)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    else:
        return subprocess.run(full).returncode, "", ""


def scp_upload(local_path, remote_path):
    """Upload a local file to the remote server via sshpass + scp."""
    full = [
        "sshpass", "-p", SERVER_PASS,
        "scp", "-o", "StrictHostKeyChecking=no",
        local_path, f"{SERVER_HOST}:{remote_path}",
    ]
    result = subprocess.run(full, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check_sshpass():
    """Verify sshpass is installed."""
    result = subprocess.run(["which", "sshpass"], capture_output=True)
    if result.returncode != 0:
        print("ERROR: sshpass is not installed.")
        print("  Install with: brew install hudochenkov/sshpass/sshpass")
        sys.exit(1)


def check_connectivity():
    """Test SSH connectivity to the server."""
    print("  Testing SSH connectivity...")
    rc, out, err = ssh_cmd("echo ok")
    if rc != 0:
        print(f"  ERROR: Cannot connect to {SERVER_HOST}")
        print(f"  {err}")
        sys.exit(1)
    print("  Connected.")


def upload_asset(local_path, slug):
    """SCP the asset file to the server assets directory."""
    ext = os.path.splitext(local_path)[1] or ".html"
    remote_path = f"{ASSETS_DIR}/{slug}{ext}"

    print(f"  Uploading {local_path} -> {remote_path}")
    rc, out, err = scp_upload(local_path, remote_path)
    if rc != 0:
        print(f"  ERROR: Upload failed: {err}")
        sys.exit(1)
    print("  Upload complete.")
    return f"assets/{slug}{ext}"


def get_resources():
    """Read the current resources.json from the server."""
    print("  Reading current resources.json...")
    rc, out, err = ssh_cmd(f"cat {RESOURCES_JSON}")
    if rc != 0:
        print(f"  WARNING: Could not read resources.json ({err}). Starting fresh.")
        return []
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        print(f"  WARNING: Invalid JSON in resources.json. Starting fresh.")
        return []


def register_resource(slug, label, file_path, dry_run=False):
    """Add or update the resource entry in resources.json."""
    resources = get_resources()

    # Check if slug already exists
    existing = next((r for r in resources if r.get("slug") == slug), None)
    if existing:
        print(f"  Resource '{slug}' already exists — updating.")
        existing["label"] = label
        existing["file"] = file_path
        existing["active"] = True
    else:
        print(f"  Registering new resource '{slug}'.")
        resources.append({
            "slug": slug,
            "label": label,
            "file": file_path,
            "active": True,
        })

    updated_json = json.dumps(resources, indent=2)

    if dry_run:
        print("  [DRY RUN] Would write resources.json:")
        print(f"  {updated_json}")
        return

    # Write back to server
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp.write(updated_json)
        tmp_path = tmp.name

    rc, out, err = scp_upload(tmp_path, RESOURCES_JSON)
    os.unlink(tmp_path)

    if rc != 0:
        print(f"  ERROR: Failed to write resources.json: {err}")
        sys.exit(1)
    print("  resources.json updated.")


def restart_container(dry_run=False):
    """Restart the sas-gate container to pick up the new resource."""
    if dry_run:
        print("  [DRY RUN] Would restart sas-gate container.")
        return

    print("  Restarting sas-gate container...")
    rc, out, err = ssh_cmd(f"cd {PROJECT_DIR} && docker compose restart app")
    if rc != 0:
        print(f"  WARNING: Restart may have failed: {err}")
    else:
        print("  Container restarted.")


def verify_container():
    """Check that the sas-gate container is running."""
    print("  Verifying container status...")
    rc, out, err = ssh_cmd(f"cd {PROJECT_DIR} && docker compose ps --format json app")
    if rc != 0:
        # Fallback to plain format
        rc, out, err = ssh_cmd(f"cd {PROJECT_DIR} && docker compose ps app")

    if "Up" in out or "running" in out.lower():
        print("  sas-gate is running.")
        return True
    else:
        print(f"  WARNING: sas-gate may not be running. Status:\n  {out}")
        return False


def list_resources():
    """Print the current resources registered on the server."""
    resources = get_resources()
    if not resources:
        print("  No resources registered.")
        return

    print(f"\n  {'Slug':<40} {'Label':<50} {'Active'}")
    print(f"  {'─'*40} {'─'*50} {'─'*6}")
    for r in resources:
        active = "Yes" if r.get("active", True) else "No"
        print(f"  {r['slug']:<40} {r.get('label', '?'):<50} {active}")


def check_downloads(slug=None, limit=10):
    """Query recent downloads from the database."""
    where = f"WHERE d.resource = '{slug}'" if slug else ""
    query = (
        f"SELECT c.first_name, c.last_name, c.email, c.job_title, "
        f"d.resource, d.downloaded_at "
        f"FROM downloads d JOIN contacts c ON d.contact_id = c.id "
        f"{where} ORDER BY d.downloaded_at DESC LIMIT {limit};"
    )
    rc, out, err = ssh_cmd(
        f'docker exec sas-db psql -U sas -d sas -c "{query}"'
    )
    if rc != 0:
        print(f"  ERROR: Query failed: {err}")
        return
    print(out)


def main():
    parser = argparse.ArgumentParser(
        description="Deploy a gated download asset to Cortex4 server.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Subcommands:
  deploy    Upload asset, register resource, restart container
  list      List currently registered resources
  downloads Show recent download activity
  verify    Check server connectivity and container status
        """,
    )
    sub = parser.add_subparsers(dest="command", help="Action to perform")

    # deploy subcommand
    deploy_p = sub.add_parser("deploy", help="Deploy a new gated asset")
    deploy_p.add_argument("asset_file", help="Path to the local asset file (HTML or PDF)")
    deploy_p.add_argument("slug", help="Resource slug (kebab-case, e.g. maintenance-business-case)")
    deploy_p.add_argument("label", help="Human-readable resource label")
    deploy_p.add_argument("--dry-run", action="store_true", help="Show what would happen without making changes")

    # list subcommand
    sub.add_parser("list", help="List registered resources on the server")

    # downloads subcommand
    dl_p = sub.add_parser("downloads", help="Show recent downloads")
    dl_p.add_argument("--slug", help="Filter by resource slug")
    dl_p.add_argument("--limit", type=int, default=10, help="Number of records (default: 10)")

    # verify subcommand
    sub.add_parser("verify", help="Check server connectivity and container status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    check_sshpass()

    if args.command == "verify":
        check_connectivity()
        verify_container()

    elif args.command == "list":
        check_connectivity()
        list_resources()

    elif args.command == "downloads":
        check_connectivity()
        check_downloads(slug=args.slug, limit=args.limit)

    elif args.command == "deploy":
        # Validate inputs
        if not os.path.isfile(args.asset_file):
            print(f"ERROR: File not found: {args.asset_file}")
            sys.exit(1)

        if " " in args.slug or args.slug != args.slug.lower():
            print(f"ERROR: Slug must be lowercase kebab-case: '{args.slug}'")
            sys.exit(1)

        print(f"\n{'='*60}")
        print(f"  Deploying gated download to Cortex4")
        print(f"{'='*60}")
        print(f"  Asset:  {args.asset_file}")
        print(f"  Slug:   {args.slug}")
        print(f"  Label:  {args.label}")
        if args.dry_run:
            print(f"  Mode:   DRY RUN")
        print(f"{'='*60}\n")

        # Step 1: Connectivity
        print("[1/5] Checking connectivity")
        check_connectivity()

        # Step 2: Upload asset
        print("\n[2/5] Uploading asset to server")
        if args.dry_run:
            ext = os.path.splitext(args.asset_file)[1] or ".html"
            file_path = f"assets/{args.slug}{ext}"
            print(f"  [DRY RUN] Would upload to {ASSETS_DIR}/{args.slug}{ext}")
        else:
            file_path = upload_asset(args.asset_file, args.slug)

        # Step 3: Register resource
        print("\n[3/5] Registering resource in resources.json")
        register_resource(args.slug, args.label, file_path, dry_run=args.dry_run)

        # Step 4: Restart container
        print("\n[4/5] Restarting sas-gate container")
        restart_container(dry_run=args.dry_run)

        # Step 5: Verify
        print("\n[5/5] Verifying deployment")
        if not args.dry_run:
            verify_container()

        print(f"\n{'='*60}")
        if args.dry_run:
            print("  DRY RUN COMPLETE — no changes made")
        else:
            print("  DEPLOYMENT COMPLETE")
            print(f"  Resource '{args.slug}' is live at gate.sas-am.com")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
