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

# Install terminal-notifier for desktop notifications (macOS only)
if [[ "$(uname)" == "Darwin" ]]; then
    echo "Checking desktop notification support..."
    if ! command -v terminal-notifier &> /dev/null; then
        echo "  terminal-notifier not found."
        if command -v brew &> /dev/null; then
            read -p "  Install terminal-notifier via Homebrew? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "  Installing terminal-notifier..."
                brew install terminal-notifier
                echo "  terminal-notifier installed successfully."
            else
                echo "  Skipped. Desktop notifications won't be available for /MBP:notifications."
            fi
        else
            echo "  Homebrew not found. Install manually: brew install terminal-notifier"
        fi
    else
        echo "  terminal-notifier is installed: $(which terminal-notifier)"
    fi
    echo ""
fi

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
echo "Your Marcov Beam Pipeline (MBP) commands are now available:"
echo ""
echo "  Research & Sales:"
echo "    /MBP:b2b-research      — B2B prospect research and intelligence"
echo "    /MBP:beam-selling       — BEAM evidence-gated sales pipeline"
echo "    /MBP:tender             — Government tender assessment"
echo ""
echo "  Marketing (Paid):"
echo "    /MBP:google-ads         — Google Ads performance analysis"
echo "    /MBP:linkedin-ads       — LinkedIn Ads performance analysis"
echo ""
echo "  Marketing (Organic):"
echo "    /MBP:seo                — SEO analysis and optimisation"
echo "    /MBP:content-intel      — Reddit content intelligence"
echo ""
echo "  Marketing (Measurement):"
echo "    /MBP:website-analytics  — GA4 website analytics"
echo "    /MBP:marketing-dashboard — Cross-channel dashboard"
echo ""
echo "  Content & Productivity:"
echo "    /MBP:linkedin-post      — LinkedIn post generation"
echo "    /MBP:presentation       — SAS-AM branded presentations"
echo "    /MBP:nano-banana        — AI image generation"
echo "    /MBP:data-quality       — Data quality analysis"
echo "    /MBP:notifications      — Push notifications (Teams/desktop)"
echo ""
echo "Commands will auto-update after git pull or branch checkout."
