#!/bin/bash
#
# Setup script for SAS-AM Claude Code Skills
#
# This script:
# 1. Installs git hooks for auto-registration of commands
# 2. Registers all current skills as slash commands
#
# Run this after cloning the repository.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_SOURCE="${SCRIPT_DIR}/.hooks"
HOOKS_TARGET="${SCRIPT_DIR}/.git/hooks"

echo "=== SAS-AM Claude Code Skills Setup ==="
echo ""

# Install git hooks
echo "Installing git hooks..."
if [ -d "${HOOKS_SOURCE}" ]; then
    for hook in "${HOOKS_SOURCE}"/*; do
        if [ -f "${hook}" ]; then
            hook_name=$(basename "${hook}")
            target="${HOOKS_TARGET}/${hook_name}"

            # Copy hook and make executable
            cp "${hook}" "${target}"
            chmod +x "${target}"
            echo "  Installed: ${hook_name}"
        fi
    done
    echo "  Git hooks installed successfully."
else
    echo "  Warning: .hooks directory not found, skipping hook installation."
fi

echo ""

# Register commands
echo "Registering slash commands..."
if [ -x "${SCRIPT_DIR}/register-commands.sh" ]; then
    "${SCRIPT_DIR}/register-commands.sh"
else
    echo "  Error: register-commands.sh not found or not executable."
    exit 1
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Your slash commands are now available:"
echo "  /data-quality-analysis"
echo "  /b2b-research-agent"
echo "  /sas-presentation"
echo "  /linkedin-post-generator"
echo "  /beam-selling"
echo ""
echo "Commands will auto-update after git pull or branch checkout."
