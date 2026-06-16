#!/bin/bash
# Generate file manifest with SHA-256 hashes for SASAMClaudeCodeSkills
# Run this before each release to track file integrity

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VERSION=$(cat VERSION 2>/dev/null || echo "unknown")
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
MANIFEST_FILE="sasam-file-manifest.json"

echo "Generating manifest for SASAMClaudeCodeSkills v${VERSION}..."

# Start JSON
echo '{' > "$MANIFEST_FILE"
echo "  \"version\": \"${VERSION}\"," >> "$MANIFEST_FILE"
echo "  \"generated_at\": \"${TIMESTAMP}\"," >> "$MANIFEST_FILE"
echo '  "files": {' >> "$MANIFEST_FILE"

# List release files from git (tracked files only) so the manifest never
# references untracked local cruft (.notifications/, sasam-local-patches/,
# editor backups). Keeps the same extension allow-list and path exclusions.
FIRST=true
git ls-files -- '*.md' '*.json' '*.sh' '*.js' '*.png' \
  | grep -vE '(^|/)node_modules/|(^|/)__pycache__/|/generated-images/|^\.planning/|^sasam-file-manifest\.json$|(^|/)package-lock\.json$' \
  | sort | while read -r file; do
    # git ls-files yields repo-relative paths already
    REL_PATH="${file#./}"

    # Calculate SHA-256 hash
    if [[ "$OSTYPE" == "darwin"* ]]; then
      HASH=$(shasum -a 256 "$file" | cut -d' ' -f1)
    else
      HASH=$(sha256sum "$file" | cut -d' ' -f1)
    fi

    # Add comma for all but first entry
    if [ "$FIRST" = true ]; then
      FIRST=false
    else
      echo "," >> "$MANIFEST_FILE"
    fi

    # Write entry (no trailing newline for comma handling)
    printf '    "%s": "%s"' "$REL_PATH" "$HASH" >> "$MANIFEST_FILE"
done

# Close JSON
echo '' >> "$MANIFEST_FILE"
echo '  }' >> "$MANIFEST_FILE"
echo '}' >> "$MANIFEST_FILE"

# Count files
FILE_COUNT=$(grep -c '"sha256' "$MANIFEST_FILE" 2>/dev/null || echo "0")
# Alternative count method
FILE_COUNT=$(jq '.files | length' "$MANIFEST_FILE" 2>/dev/null || echo "unknown")

echo "Manifest generated: $MANIFEST_FILE"
echo "Version: $VERSION"
echo "Files tracked: $FILE_COUNT"
