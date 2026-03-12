#!/usr/bin/env python3
"""
SAS-AM Webflow CMS Publisher
Lightweight REST API client for publishing content to Webflow CMS.
Replaces the heavy Webflow MCP server for context-efficient operation.

Usage:
    python3 webflowPublish.py sites                          # List sites
    python3 webflowPublish.py collections <site_id>          # List collections
    python3 webflowPublish.py items <collection_id>          # List items
    python3 webflowPublish.py create <collection_id> <json>  # Create item (draft)
    python3 webflowPublish.py publish <collection_id> <json> # Create item (live)
    python3 webflowPublish.py update <collection_id> <item_id> <json>  # Update item
    python3 webflowPublish.py upload-asset <site_id> <file_path>       # Upload image

Requires: WEBFLOW_TOKEN environment variable

API Reference: https://developers.webflow.com/data/reference
"""

import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
import mimetypes
import uuid
from datetime import datetime, timezone

API_BASE = "https://api.webflow.com/v2"


def get_token():
    token = os.environ.get("WEBFLOW_TOKEN")
    if not token:
        print("Error: WEBFLOW_TOKEN environment variable not set.", file=sys.stderr)
        print("Set it with: export WEBFLOW_TOKEN='your-token-here'", file=sys.stderr)
        sys.exit(1)
    return token


def api_request(method, path, data=None, token=None):
    """Make an authenticated request to the Webflow API v2."""
    if token is None:
        token = get_token()

    url = f"{API_BASE}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            print(json.dumps(error_json, indent=2), file=sys.stderr)
        except json.JSONDecodeError:
            print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def list_sites():
    """List all Webflow sites accessible with the current token."""
    result = api_request("GET", "/sites")
    sites = result.get("sites", [])
    output = []
    for site in sites:
        output.append({
            "id": site.get("id"),
            "name": site.get("displayName", site.get("name", "")),
            "shortName": site.get("shortName", ""),
            "lastPublished": site.get("lastPublished", ""),
        })
    print(json.dumps(output, indent=2))


def list_collections(site_id):
    """List all CMS collections for a site."""
    result = api_request("GET", f"/sites/{site_id}/collections")
    collections = result.get("collections", [])
    output = []
    for col in collections:
        output.append({
            "id": col.get("id"),
            "displayName": col.get("displayName", ""),
            "slug": col.get("slug", ""),
            "singularName": col.get("singularName", ""),
            "itemCount": col.get("lastUpdated", ""),
        })
    print(json.dumps(output, indent=2))


def list_items(collection_id):
    """List items in a collection (paginated, returns first 100)."""
    result = api_request("GET", f"/collections/{collection_id}/items?limit=100")
    items = result.get("items", [])
    output = []
    for item in items:
        field_data = item.get("fieldData", {})
        output.append({
            "id": item.get("id"),
            "name": field_data.get("name", ""),
            "slug": field_data.get("slug", ""),
            "lastUpdated": item.get("lastUpdated", ""),
            "isDraft": item.get("isDraft", False),
        })
    print(json.dumps(output, indent=2))


def resolve_image_fields(field_data, site_id=None):
    """Detect image fields that contain local file paths and upload them.

    If a field value is a string pointing to a local file (e.g. ./generated-images/hero.jpg),
    upload it to Webflow Assets and replace the value with { fileId, alt }.

    If a field value is a dict with a "file" key pointing to a local path, upload it
    and merge the resulting fileId into the dict.

    Recognised image field patterns:
      - "featured-image": "/path/to/image.jpg"
      - "featured-image": { "file": "/path/to/image.jpg", "alt": "description" }
    """
    if site_id is None:
        # Need site_id for asset upload — discover it
        sites_result = api_request("GET", "/sites")
        sites = sites_result.get("sites", [])
        if not sites:
            print("Error: No sites found. Cannot upload image.", file=sys.stderr)
            return field_data
        site_id = sites[0].get("id")
        print(f"Using site: {sites[0].get('displayName', site_id)}", file=sys.stderr)

    IMAGE_FIELDS = {"featured-image", "thumbnail", "hero-image", "image", "og-image"}
    resolved = dict(field_data)

    for key, value in field_data.items():
        is_image_field = key in IMAGE_FIELDS or key.endswith("-image")

        if not is_image_field:
            continue

        file_path = None
        alt_text = ""

        if isinstance(value, str) and os.path.isfile(value):
            file_path = value
        elif isinstance(value, dict) and "file" in value and os.path.isfile(value["file"]):
            file_path = value["file"]
            alt_text = value.get("alt", "")

        if file_path:
            print(f"Uploading {os.path.basename(file_path)} for field '{key}'...",
                  file=sys.stderr)
            asset_id = upload_asset_and_get_id(site_id, file_path)
            if asset_id:
                resolved[key] = {"fileId": asset_id, "alt": alt_text}
                print(f"  -> Asset uploaded: {asset_id}", file=sys.stderr)
            else:
                print(f"  -> Upload failed for {key}, skipping.", file=sys.stderr)

    return resolved


def upload_asset_and_get_id(site_id, file_path):
    """Upload a file to Webflow Assets and return the assetId. Returns None on failure."""
    file_name = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    token = get_token()

    with open(file_path, "rb") as f:
        file_data = f.read()

    # Step 1: Create asset metadata to get pre-signed upload URL
    url = f"{API_BASE}/sites/{site_id}/assets"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    meta_payload = json.dumps({
        "fileName": file_name,
        "fileHash": uuid.uuid4().hex,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=meta_payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            upload_details = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Error requesting upload URL: {e.read().decode()}", file=sys.stderr)
        return None

    # Step 2: Upload to pre-signed S3 URL
    upload_url = upload_details.get("uploadUrl", "")
    upload_details_inner = upload_details.get("uploadDetails", {})
    if not upload_url:
        print("Error: No upload URL returned.", file=sys.stderr)
        return None

    boundary = uuid.uuid4().hex
    body = b""
    for k, v in upload_details_inner.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode()
        body += f"{v}\r\n".encode()
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'.encode()
    body += f"Content-Type: {mime_type}\r\n\r\n".encode()
    body += file_data
    body += f"\r\n--{boundary}--\r\n".encode()

    upload_headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
    }
    upload_req = urllib.request.Request(upload_url, data=body, headers=upload_headers, method="POST")
    try:
        with urllib.request.urlopen(upload_req) as resp:
            pass
    except urllib.error.HTTPError as e:
        if e.code not in (200, 201, 204):
            print(f"Error uploading to S3: HTTP {e.code}", file=sys.stderr)
            return None

    return upload_details.get("assetId", upload_details.get("id", ""))


def create_item(collection_id, field_data, live=False, site_id=None):
    """Create a CMS item. If live=True, publish immediately.

    Image fields containing local file paths are automatically uploaded to
    Webflow Assets and wired into the CMS item via fileId.
    """
    # Auto-upload any image fields that contain file paths
    field_data = resolve_image_fields(field_data, site_id=site_id)

    payload = {
        "isArchived": False,
        "isDraft": not live,
        "fieldData": field_data,
    }

    if live:
        result = api_request("POST", f"/collections/{collection_id}/items/live", payload)
    else:
        result = api_request("POST", f"/collections/{collection_id}/items", payload)

    print(json.dumps({
        "status": "created",
        "live": live,
        "id": result.get("id", ""),
        "fieldData": result.get("fieldData", {}),
    }, indent=2))


def update_item(collection_id, item_id, field_data):
    """Update an existing CMS item."""
    payload = {
        "isArchived": False,
        "isDraft": False,
        "fieldData": field_data,
    }
    result = api_request("PATCH", f"/collections/{collection_id}/items/{item_id}", payload)
    print(json.dumps({
        "status": "updated",
        "id": result.get("id", ""),
        "fieldData": result.get("fieldData", {}),
    }, indent=2))


def upload_asset(site_id, file_path):
    """Upload an image asset to Webflow.

    Webflow asset upload is a two-step process:
    1. Request an upload URL from the API
    2. Upload the file to the pre-signed S3 URL
    """
    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    file_name = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    file_size = os.path.getsize(file_path)

    # Step 1: Request upload URL
    token = get_token()
    upload_request = {
        "fileName": file_name,
        "fileHash": str(uuid.uuid4()),  # Unique hash for deduplication
    }

    # Get presigned upload details
    boundary = uuid.uuid4().hex
    body_parts = []

    with open(file_path, "rb") as f:
        file_data = f.read()

    # Use the assets API endpoint
    url = f"{API_BASE}/sites/{site_id}/assets"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # First, create the asset metadata
    meta_payload = json.dumps({
        "fileName": file_name,
        "fileHash": uuid.uuid4().hex,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=meta_payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            upload_details = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Error requesting upload URL: {error_body}", file=sys.stderr)
        sys.exit(1)

    # Step 2: Upload to pre-signed URL
    upload_url = upload_details.get("uploadUrl", "")
    upload_details_inner = upload_details.get("uploadDetails", {})

    if not upload_url:
        print("Error: No upload URL returned from Webflow.", file=sys.stderr)
        sys.exit(1)

    # Build multipart form data for S3
    boundary = uuid.uuid4().hex
    body = b""

    # Add form fields from uploadDetails
    for key, value in upload_details_inner.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
        body += f"{value}\r\n".encode()

    # Add the file
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'.encode()
    body += f"Content-Type: {mime_type}\r\n\r\n".encode()
    body += file_data
    body += f"\r\n--{boundary}--\r\n".encode()

    upload_headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
    }

    upload_req = urllib.request.Request(upload_url, data=body, headers=upload_headers, method="POST")

    try:
        with urllib.request.urlopen(upload_req) as resp:
            pass  # S3 returns 204 on success
    except urllib.error.HTTPError as e:
        if e.code not in (200, 201, 204):
            print(f"Error uploading file: HTTP {e.code}", file=sys.stderr)
            sys.exit(1)

    asset_id = upload_details.get("assetId", upload_details.get("id", ""))
    print(json.dumps({
        "status": "uploaded",
        "assetId": asset_id,
        "fileName": file_name,
        "url": upload_details.get("url", ""),
    }, indent=2))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "sites":
        list_sites()

    elif command == "collections":
        if len(sys.argv) < 3:
            print("Usage: webflowPublish.py collections <site_id>", file=sys.stderr)
            sys.exit(1)
        list_collections(sys.argv[2])

    elif command == "items":
        if len(sys.argv) < 3:
            print("Usage: webflowPublish.py items <collection_id>", file=sys.stderr)
            sys.exit(1)
        list_items(sys.argv[2])

    elif command in ("create", "publish"):
        if len(sys.argv) < 4:
            print(f"Usage: webflowPublish.py {command} <collection_id> <json_file_or_string>",
                  file=sys.stderr)
            sys.exit(1)
        collection_id = sys.argv[2]
        json_arg = sys.argv[3]

        # Accept JSON file path or inline JSON string
        if os.path.isfile(json_arg):
            with open(json_arg, "r") as f:
                field_data = json.load(f)
        else:
            field_data = json.loads(json_arg)

        # Optional --site flag for auto-uploading images
        site_id = None
        if len(sys.argv) > 4 and sys.argv[4].startswith("--site="):
            site_id = sys.argv[4].split("=", 1)[1]

        create_item(collection_id, field_data, live=(command == "publish"), site_id=site_id)

    elif command == "update":
        if len(sys.argv) < 5:
            print("Usage: webflowPublish.py update <collection_id> <item_id> <json>",
                  file=sys.stderr)
            sys.exit(1)
        collection_id = sys.argv[2]
        item_id = sys.argv[3]
        json_arg = sys.argv[4]

        if os.path.isfile(json_arg):
            with open(json_arg, "r") as f:
                field_data = json.load(f)
        else:
            field_data = json.loads(json_arg)

        update_item(collection_id, item_id, field_data)

    elif command == "upload-asset":
        if len(sys.argv) < 4:
            print("Usage: webflowPublish.py upload-asset <site_id> <file_path>",
                  file=sys.stderr)
            sys.exit(1)
        upload_asset(sys.argv[2], sys.argv[3])

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
