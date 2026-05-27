# Project Setup Templates

## .claude/settings.json

```json
{
  "extraKnownMarketplaces": {
    "local": {
      "source": {
        "source": "directory",
        "path": "/home/stefan/agents/plugins"
      }
    }
  },
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "memory@local": true,
    "development@local": true,
    "transition@local": true
  },
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/project/.claude/hooks/init-transition.sh"
          }
        ]
      }
    ]
  }
}
```

## .claude/hooks/init-transition.sh

```bash
#!/bin/bash
# Initialize hourly transition file for session progress tracking
# Format: .workspace/transitions/YYYY-MM-DD/HH.md
set -e
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TRANSITIONS_DIR="$PROJECT_ROOT/.workspace/transitions"
TODAY=$(date +%Y-%m-%d)
HOUR=$(date +%H)
TODAY_DIR="$TRANSITIONS_DIR/$TODAY"
HOURLY_FILE="$TODAY_DIR/${HOUR}.md"

mkdir -p "$TODAY_DIR"

if [ ! -f "$HOURLY_FILE" ]; then
    cat > "$HOURLY_FILE" << EOF
# Session Progress: $TODAY ${HOUR}:00

---

EOF
fi
exit 0
```

Make executable: `chmod +x .claude/hooks/init-transition.sh`

## Directory Structure

```
AGENTS.md                  # canonical project doc (Codex reads natively)
CLAUDE.md                  # one line: @AGENTS.md
.workspace/                   # SHARED state for both Claude and Codex
├── memory/
│   ├── project_state.md
│   ├── conventions.md
│   └── decisions.md
├── transitions/           # YYYY-MM-DD/HH.md (auto-created)
└── work/                  # active work units
.claude/                   # CLAUDE-SPECIFIC ONLY
├── settings.json          # plugins, hooks, permissions
├── hooks/
│   └── init-transition.sh
└── commands/              # project slash-commands
```

## AGENTS.md Template

```markdown
# [Project Name]

## Purpose

<one-paragraph statement>

## Code vs data layout

| Path | Purpose |
|---|---|
| | |

## Common bash invocations

```bash
```

## Slash commands (Claude Code)

- See `.claude/commands/`

## Project memory

@.workspace/memory/project_state.md
@.workspace/memory/conventions.md
@.workspace/memory/decisions.md

Session progress goes to `.workspace/transitions/YYYY-MM-DD/HH.md` — the hook
auto-creates the hourly file on each prompt.
```

## CLAUDE.md (one line)

```markdown
@AGENTS.md
```

## Quick Setup Commands

```bash
# Create structure — DO NOT create .claude/transitions/ (deprecated; .workspace/transitions is canonical)
mkdir -p .workspace/{memory,transitions,work}
mkdir -p .claude/{hooks,commands}
touch .workspace/transitions/.gitkeep .workspace/work/.gitkeep

# Create settings.json (edit path for your system)
cat > .claude/settings.json << 'EOF'
[paste settings.json template above]
EOF

# Create hook
cat > .claude/hooks/init-transition.sh << 'HOOK'
[paste hook script above]
HOOK
chmod +x .claude/hooks/init-transition.sh

# CLAUDE.md is one line
echo "@AGENTS.md" > CLAUDE.md

# Initialize git if needed
git init
echo ".workspace/transitions/" >> .gitignore  # Optional: exclude transitions
```

## Plugin selection

Verify each `<plugin>@local` exists in `~/agents/plugins/<plugin>/` before
enabling. Current marketplace (May 2026):

- Core: `system`, `workflow`, `memory`, `development`, `transition`
- Domain: `writing-skills`, `content-marketing`, `references`, `quant`,
  `web-development`, `reports`, `diagrams`, `docs`, `hooks`, `setup`, `codex`

Removed/renamed (do not enable): `content` (use `content-marketing`),
`ml3t-researcher`/`ml3t-coauthor` (academic research moved into `references`),
`marketing` (use `content-marketing`).

## MCP servers (.mcp.json)

Use these exact package names — earlier setups generated bogus
`@modelcontextprotocol/server-*` names that don't exist.

**`chrome-devtools` requires an explicit `env` block on Linux/X11.**
MCP subprocesses do not reliably inherit `$DISPLAY`/`$XAUTHORITY` from
the launching shell — works when Claude Code is started from a
`.bashrc`-sourcing terminal, fails from IDE/desktop launchers,
systemd units, or tmux non-login shells. Hit 18+ times across
projects (2026-05). Always write the env block.

Auto-detect the right values from `gnome-shell` (not from `$DISPLAY`
in a subshell — `.bashrc` may carry a stale value):

```bash
gs=$(pgrep -f gnome-shell | head -1)
DISPLAY_VAL=$(tr '\0' '\n' < /proc/$gs/environ | awk -F= '/^DISPLAY=/  {print $2; exit}')
XAUTH_VAL=$(tr  '\0' '\n' < /proc/$gs/environ | awk -F= '/^XAUTHORITY=/ {print $2; exit}')
# Validate before committing — xdpyinfo, NOT headless Chrome (headless
# doesn't attach to X so it false-positives bad values).
XAUTHORITY="$XAUTH_VAL" xdpyinfo -display "$DISPLAY_VAL" >/dev/null 2>&1 || {
  echo "WARN: X server not reachable; chrome-devtools will fail at runtime"
}
```

Then write the `env` block with the validated values:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "/home/stefan/.nvm/versions/node/v22.21.0/bin/npx",
      "args": ["-y", "chrome-devtools-mcp@latest"],
      "env": {
        "DISPLAY": ":1",
        "XAUTHORITY": "/run/user/1000/gdm/Xauthority"
      }
    },
    "serena": {
      "command": "/home/stefan/.nvm/versions/node/v22.21.0/bin/npx",
      "args": ["-y", "@anthropic-ai/serena-mcp@latest"]
    },
    "context7": {
      "command": "/home/stefan/.nvm/versions/node/v22.21.0/bin/npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "ml4t-refs": {
      "command": "uv",
      "args": ["run", "--extra", "mcp", "python", "-m", "ml4t_refs.mcp_server"],
      "cwd": "/home/stefan/ml4t/references"
    }
  }
}
```

`context7` is also available globally via the `context7-mcp` binary in
`~/.claude.json`; the local `.mcp.json` entry is project-scoped and overrides.

**On non-Linux or Wayland-only:** skip the `env` block for chrome-devtools
(macOS doesn't need it; Wayland needs `WAYLAND_DISPLAY` + `--ozone-platform=wayland`
via `--chromeArg` instead).

**Bulk-fixing existing projects:**
```bash
find ~ -name ".mcp.json" -not -path "*/node_modules/*" | while read f; do
  jq -e '.mcpServers."chrome-devtools" and (.mcpServers."chrome-devtools".env.DISPLAY == null)' "$f" >/dev/null 2>&1 || continue
  jq '.mcpServers."chrome-devtools".env = {"DISPLAY":":1","XAUTHORITY":"/run/user/1000/gdm/Xauthority"}' "$f" \
    > "$f.tmp" && mv "$f.tmp" "$f" && echo "patched: $f"
done
```

## Language-Specific Additions

**Python**: Claude can generate pyproject.toml, .pre-commit-config.yaml, Makefile on demand.

**JavaScript**: Claude can generate package.json, tsconfig.json, eslint config on demand.

**Existing projects**: Add the structure above; existing source code stays put.
