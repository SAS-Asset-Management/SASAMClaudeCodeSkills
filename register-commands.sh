#!/bin/bash
#
# Register SAS-AM Claude Code skills as slash commands
#
# This script finds all SKILL.md files in the repository and registers them
# as slash commands in ~/.claude/commands by creating copies with absolute
# paths for reference files.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMANDS_DIR="${HOME}/.claude/commands"

# Ensure commands directory exists
mkdir -p "${COMMANDS_DIR}"

echo "Registering SAS-AM Claude Code skills..."
echo "Repository: ${SCRIPT_DIR}"
echo "Commands directory: ${COMMANDS_DIR}"
echo ""

# Find all SKILL.md files
find "${SCRIPT_DIR}" -name "SKILL.md" -type f | while read -r skill_file; do
    # Extract the skill directory (parent of SKILL.md)
    skill_dir="$(dirname "${skill_file}")"

    # Extract skill name from YAML frontmatter
    skill_name=$(grep -m1 "^name:" "${skill_file}" | sed 's/^name:[[:space:]]*//')

    if [ -z "${skill_name}" ]; then
        echo "  SKIP: ${skill_file} (no name in frontmatter)"
        continue
    fi

    output_file="${COMMANDS_DIR}/${skill_name}.md"

    echo "  Registering: ${skill_name}"
    echo "    Source: ${skill_file}"
    echo "    Target: ${output_file}"

    # Copy the skill file and replace relative references/ paths with absolute paths
    # This handles patterns like:
    #   references/file.html -> /full/path/to/skill/references/file.html
    #   `references/file.md` -> `/full/path/to/skill/references/file.md`
    sed -e "s|\`references/|\`${skill_dir}/references/|g" \
        -e "s|references/\([a-zA-Z0-9._-]*\)|${skill_dir}/references/\1|g" \
        "${skill_file}" > "${output_file}"

    echo "    Done"
done

echo ""
echo "Registration complete!"
echo ""
echo "Registered commands:"
ls -1 "${COMMANDS_DIR}"/*.md 2>/dev/null | while read -r cmd; do
    basename "${cmd}" .md
done
