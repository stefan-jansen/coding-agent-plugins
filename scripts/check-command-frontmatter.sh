#!/usr/bin/env bash
# Check that every plugin command file declares a `description:` in its
# YAML frontmatter.
#
# Why this exists: Claude Code drops a command with no `description` from the
# slash-command list entirely. The file stays on disk, `plugin.json` still
# lists it, and `claude plugin validate` still passes - the command is simply
# invisible at the prompt, with no error anywhere. Six commands across the two
# marketplaces had silently disappeared this way (2026-08-17).
#
# Usage:
#   scripts/check-command-frontmatter.sh            # check ./*/commands/*.md
#   scripts/check-command-frontmatter.sh DIR...     # check specific roots
#
# Exit: 0 all commands declare a description; 1 one or more do not.

set -euo pipefail

roots=("$@")
if [[ ${#roots[@]} -eq 0 ]]; then
    roots=("$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)")
fi

missing=()
checked=0

while IFS= read -r -d '' file; do
    checked=$((checked + 1))
    if ! awk '
        NR == 1 && $0 != "---" { exit }                       # no frontmatter block at all
        /^---$/ { fence++; if (fence == 2) exit }             # end of frontmatter
        fence == 1 && /^description:[[:space:]]*[^[:space:]]/ { found = 1; exit }
        END { exit found ? 0 : 1 }
    ' "$file"; then
        missing+=("$file")
    fi
done < <(
    for root in "${roots[@]}"; do
        find "$root" -mindepth 3 -maxdepth 3 -path '*/commands/*.md' -print0
    done
)

if [[ ${#missing[@]} -gt 0 ]]; then
    echo "Command files with no 'description:' in frontmatter (Claude Code will not list them):"
    for file in "${missing[@]}"; do
        echo "  - $file"
    done
    echo
    echo "Add a one-line 'description:' to each file's YAML frontmatter."
    exit 1
fi

echo "OK - all $checked command file(s) declare a description."
