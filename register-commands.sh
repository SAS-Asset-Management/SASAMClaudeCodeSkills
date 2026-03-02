#!/bin/bash
#
# Register Marcov Beam Pipeline (MBP) skills as slash commands
#
# This script finds all SKILL.md files in the repository and registers them
# as slash commands in ~/.claude/commands by creating copies with absolute
# paths for reference files and shared resources.
#
# MBP skills use colon-namespaced names (e.g., MBP:beam-selling).
# Colons are replaced with dashes in filenames for filesystem safety.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMANDS_DIR="${HOME}/.claude/commands"
MBP_DIR="${SCRIPT_DIR}/marcov-beam-pipeline/1.0.0"
SHARED_DIR="${MBP_DIR}/shared"

# Ensure commands directory exists
mkdir -p "${COMMANDS_DIR}"

echo "Registering Marcov Beam Pipeline skills..."
echo "Repository: ${SCRIPT_DIR}"
echo "Commands directory: ${COMMANDS_DIR}"
echo ""

# Find all SKILL.md files (prioritise MBP versions over legacy)
find "${MBP_DIR}" -name "SKILL.md" -type f 2>/dev/null | while read -r skill_file; do
    # Extract the skill directory (parent of SKILL.md)
    skill_dir="$(dirname "${skill_file}")"

    # Extract skill name from YAML frontmatter (strip any carriage returns from CRLF files)
    skill_name=$(grep -m1 "^name:" "${skill_file}" | sed 's/^name:[[:space:]]*//' | tr -d '\r')

    if [ -z "${skill_name}" ]; then
        echo "  SKIP: ${skill_file} (no name in frontmatter)"
        continue
    fi

    # Replace colon with dash for filename (MBP:beam-selling -> MBP-beam-selling.md)
    file_name="${skill_name//:/-}"
    output_file="${COMMANDS_DIR}/${file_name}.md"

    echo "  Registering: ${skill_name}"
    echo "    Source: ${skill_file}"
    echo "    Target: ${output_file}"

    # Copy the skill file and replace relative paths with absolute paths:
    # - references/ -> absolute skill references path
    # - shared/ -> absolute shared resources path
    sed -e "s|\`references/|\`${skill_dir}/references/|g" \
        -e "s|references/\([a-zA-Z0-9._-]*\)|${skill_dir}/references/\1|g" \
        -e "s|\`shared/|\`${SHARED_DIR}/|g" \
        -e "s|shared/\([a-zA-Z0-9._-]*\)|${SHARED_DIR}/\1|g" \
        "${skill_file}" > "${output_file}"

    echo "    Done"
done

# Also register any legacy skills not yet migrated to MBP
echo ""
echo "Checking for legacy skills..."
find "${SCRIPT_DIR}" -name "SKILL.md" -type f -not -path "*/marcov-beam-pipeline/*" | while read -r skill_file; do
    skill_dir="$(dirname "${skill_file}")"
    skill_name=$(grep -m1 "^name:" "${skill_file}" | sed 's/^name:[[:space:]]*//' | tr -d '\r')

    if [ -z "${skill_name}" ]; then
        continue
    fi

    # Skip if an MBP version already registered
    file_name="${skill_name//:/-}"
    if [ -f "${COMMANDS_DIR}/MBP-${file_name##MBP-}.md" ] 2>/dev/null; then
        echo "  SKIP: ${skill_name} (MBP version already registered)"
        continue
    fi

    output_file="${COMMANDS_DIR}/${file_name}.md"

    # Don't overwrite MBP versions
    if [ -f "${output_file}" ]; then
        continue
    fi

    echo "  Registering legacy: ${skill_name}"
    sed -e "s|\`references/|\`${skill_dir}/references/|g" \
        -e "s|references/\([a-zA-Z0-9._-]*\)|${skill_dir}/references/\1|g" \
        "${skill_file}" > "${output_file}"
done

echo ""
echo "Registration complete!"
echo ""
echo "Registered MBP skills:"
ls -1 "${COMMANDS_DIR}"/MBP-*.md 2>/dev/null | while read -r cmd; do
    name=$(basename "${cmd}" .md)
    echo "  /${name//-/:}"
done

echo ""
echo "Legacy skills (if any):"
ls -1 "${COMMANDS_DIR}"/*.md 2>/dev/null | grep -v "MBP-" | while read -r cmd; do
    echo "  /$(basename "${cmd}" .md)"
done
