#!/usr/bin/env bash
# Register this marketplace and enable plugins in ~/.claude/settings.json.
#
# Usage:
#   scripts/enable.sh                      # register marketplace + enable the default set
#   scripts/enable.sh workflow memory       # register + enable only these
#   scripts/enable.sh --list                # show what is currently enabled
#
# Enabling at the user level means a plugin is on in every project on this
# machine, and no project repo carries agent config. Sync ~/.claude/settings.json
# with your dotfiles to carry the same set to another machine.
#
# Idempotent: re-running changes nothing. Existing settings are merged, not
# overwritten; a timestamped backup is written before the first change.

set -euo pipefail

MARKETPLACE="local"
SETTINGS="${CLAUDE_SETTINGS:-$HOME/.claude/settings.json}"
MARKETPLACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

DEFAULT_PLUGINS=(workflow memory transition development system)

command -v jq >/dev/null 2>&1 || { echo "✗ jq is required (brew install jq / apt install jq)" >&2; exit 1; }

if [[ ! -f "$MARKETPLACE_DIR/.claude-plugin/marketplace.json" ]]; then
  echo "✗ $MARKETPLACE_DIR is not a marketplace (no .claude-plugin/marketplace.json)" >&2
  exit 1
fi

mkdir -p "$(dirname "$SETTINGS")"
[[ -f "$SETTINGS" ]] || echo '{}' > "$SETTINGS"
jq empty "$SETTINGS" 2>/dev/null || { echo "✗ $SETTINGS is not valid JSON — fix it first" >&2; exit 1; }

if [[ "${1:-}" == "--list" ]]; then
  echo "settings:    $SETTINGS"
  echo "marketplace: $(jq -r --arg m "$MARKETPLACE" '.extraKnownMarketplaces[$m].source.path // "(not registered)"' "$SETTINGS")"
  echo "enabled:"
  jq -r --arg m "@$MARKETPLACE" \
    '(.enabledPlugins // {}) | to_entries | map(select(.key | endswith($m))) | .[] | "  \(.key) = \(.value)"' \
    "$SETTINGS"
  exit 0
fi

if [[ $# -gt 0 ]]; then
  PLUGINS=("$@")
else
  PLUGINS=("${DEFAULT_PLUGINS[@]}")
fi

for p in "${PLUGINS[@]}"; do
  if [[ ! -f "$MARKETPLACE_DIR/$p/.claude-plugin/plugin.json" ]]; then
    echo "✗ no such plugin in $MARKETPLACE_DIR: $p" >&2
    exit 1
  fi
done

updated=$(jq \
  --arg m "$MARKETPLACE" \
  --arg path "$MARKETPLACE_DIR" \
  --argjson names "$(printf '%s\n' "${PLUGINS[@]}" | jq -R . | jq -s .)" \
  '
  .extraKnownMarketplaces //= {}
  | .extraKnownMarketplaces[$m] = {source: {source: "directory", path: $path}}
  | .enabledPlugins //= {}
  | reduce $names[] as $n (.; .enabledPlugins["\($n)@\($m)"] = true)
  ' "$SETTINGS")

if [[ "$(jq -S . <<<"$updated")" == "$(jq -S . "$SETTINGS")" ]]; then
  echo "✓ already up to date — no changes to $SETTINGS"
else
  backup="$SETTINGS.bak-$(date +%Y%m%d%H%M%S)"
  cp "$SETTINGS" "$backup"
  printf '%s\n' "$updated" > "$SETTINGS"
  echo "✓ updated $SETTINGS (backup: $backup)"
fi

echo "  marketplace $MARKETPLACE -> $MARKETPLACE_DIR"
echo "  enabled: ${PLUGINS[*]}"
echo ""
echo "Restart Claude Code to load them."
