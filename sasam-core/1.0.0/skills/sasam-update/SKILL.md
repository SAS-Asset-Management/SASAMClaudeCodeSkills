---
name: sasam-update
description: Check for and apply updates to SASAMClaudeCodeSkills marketplace plugins. Shows changelog, backs up local modifications, and updates all plugins.
---

# SASAMClaudeCodeSkills Update Skill

Check for updates, view changelog, and update all SAS-AM plugins.

## Overview

This skill manages updates for the SASAMClaudeCodeSkills marketplace. It compares local and remote versions, displays changelogs, and handles the update process.

## Commands

| Command | Action |
|---------|--------|
| `check` | Check if updates are available (default) |
| `changelog` | View recent changelog entries |
| `apply` | Apply available updates |
| `version` | Show current installed version |

## Invocation Examples

```
/sasam-update              # Check for updates (default)
/sasam-update check        # Same as above
/sasam-update changelog    # View changelog
/sasam-update apply        # Apply updates
/sasam-update version      # Show current version
```

---

## Update Check Workflow

### Step 1: Read Local Version

```bash
LOCAL_VERSION=$(cat ~/.claude/SASAMClaudeCodeSkills/VERSION 2>/dev/null || echo "unknown")
echo "Local version: $LOCAL_VERSION"
```

### Step 2: Fetch Remote Version

```bash
REMOTE_VERSION=$(curl -s "https://raw.githubusercontent.com/SAS-Asset-Management/SASAMClaudeCodeSkills/main/VERSION" 2>/dev/null || echo "error")
echo "Remote version: $REMOTE_VERSION"
```

### Step 3: Compare Versions

```bash
if [ "$LOCAL_VERSION" = "$REMOTE_VERSION" ]; then
  echo "You are up to date (v$LOCAL_VERSION)"
else
  echo "Update available: $LOCAL_VERSION -> $REMOTE_VERSION"
fi
```

---

## Changelog Workflow

### Fetch and Display Changelog

```bash
# Fetch changelog from GitHub
CHANGELOG=$(curl -s "https://raw.githubusercontent.com/SAS-Asset-Management/SASAMClaudeCodeSkills/main/CHANGELOG.md")

# Display recent entries (first 50 lines)
echo "$CHANGELOG" | head -50
```

### Extract Changes Between Versions

When updating, show only the relevant changelog entries between the installed version and the latest version.

---

## Apply Update Workflow

### Step 1: Check for Local Modifications

Before updating, compare local files against the manifest to detect modifications:

```bash
cd ~/.claude/SASAMClaudeCodeSkills

# Load manifest
MANIFEST="sasam-file-manifest.json"

# Check each file against its stored hash
MODIFIED_FILES=()
while IFS= read -r file; do
  STORED_HASH=$(jq -r --arg f "$file" '.files[$f]' "$MANIFEST")
  CURRENT_HASH=$(shasum -a 256 "$file" 2>/dev/null | cut -d' ' -f1)

  if [ "$STORED_HASH" != "$CURRENT_HASH" ]; then
    MODIFIED_FILES+=("$file")
  fi
done < <(jq -r '.files | keys[]' "$MANIFEST")

if [ ${#MODIFIED_FILES[@]} -gt 0 ]; then
  echo "Modified files detected:"
  printf '  - %s\n' "${MODIFIED_FILES[@]}"
fi
```

### Step 2: Backup Modified Files

```bash
BACKUP_DIR="sasam-local-patches/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

for file in "${MODIFIED_FILES[@]}"; do
  mkdir -p "$BACKUP_DIR/$(dirname "$file")"
  cp "$file" "$BACKUP_DIR/$file"
done

echo "Backed up ${#MODIFIED_FILES[@]} modified files to $BACKUP_DIR"
```

### Step 3: Pull Updates

```bash
cd ~/.claude/SASAMClaudeCodeSkills
git pull origin main
```

### Step 4: Re-register Commands

```bash
cd ~/.claude/SASAMClaudeCodeSkills
./register-commands.sh
```

### Step 5: Update Marketplace Clone

```bash
cd ~/.claude/plugins/marketplaces/SASAMClaudeCodeSkills
git pull origin main
```

### Step 6: Regenerate Manifest

```bash
cd ~/.claude/SASAMClaudeCodeSkills
./generate-manifest.sh
```

### Step 7: Display Success

```
SASAMClaudeCodeSkills updated to v{NEW_VERSION}

Changes in this update:
{CHANGELOG_EXCERPT}

{N} modified files were backed up to:
  sasam-local-patches/{TIMESTAMP}/

To restore your modifications, copy files from the backup directory.
```

---

## Version Display

When showing version info:

```
SASAMClaudeCodeSkills v1.1.0

Installed plugins:
  - sas-presentation v1.0.0
  - data-quality-analysis v1.0.0
  - b2b-research-agent v1.0.0
  - beam-selling v1.0.0
  - linkedin-post-generator v1.0.0
  - tender-assessment v1.0.0
  - push-notifications v1.0.0
  - nano-banana-2 v1.1.0
  - sasam-core v1.0.0

Last manifest: 2026-02-27T10:30:00Z
Files tracked: 67
```

---

## Error Handling

### Network Error

```
Unable to check for updates

Could not reach GitHub to check for latest version.
Please check your internet connection and try again.

To force update from local git:
  cd ~/.claude/SASAMClaudeCodeSkills && git pull
```

### Git Conflict

```
Update failed due to git conflict

Your local changes conflict with the update.
Modified files have been backed up to:
  sasam-local-patches/{TIMESTAMP}/

To resolve:
1. Review the conflicts in git
2. Resolve and commit, or reset
3. Run /sasam-update apply again
```

---

## GitHub URLs

| Resource | URL |
|----------|-----|
| VERSION | https://raw.githubusercontent.com/SAS-Asset-Management/SASAMClaudeCodeSkills/main/VERSION |
| CHANGELOG | https://raw.githubusercontent.com/SAS-Asset-Management/SASAMClaudeCodeSkills/main/CHANGELOG.md |
| Repository | https://github.com/SAS-Asset-Management/SASAMClaudeCodeSkills |
