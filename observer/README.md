# Observer Plugin

Automatic cross-session memory for Claude Code. Captures tool observations during sessions, batch-processes them with `claude -p`, and injects relevant context into future sessions.

## How It Works

```
During session:   PostToolUse hook → buffer observations to JSONL
After session:    SessionEnd hook  → background claude -p → SQLite
Next session:     SessionStart hook → query SQLite → inject context
```

No server process. No API keys. No vector database. Uses your Claude Max subscription via `claude -p --model haiku`.

### Cost Comparison

| Approach | Calls/Session | Architecture |
|----------|--------------|--------------|
| claude-mem (Agent SDK) | N+1 (per observation) | Persistent worker + subprocess |
| **observer** (batched) | **1** (end of session) | Stateless hooks + background script |

## Installation

### 1. Enable the plugin

Add to your project's `.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "observer@local": true
  }
}
```

### 2. Register hooks

Add these hooks to your project's `.claude/settings.json`. Replace `PLUGIN_PATH` with the absolute path to the observer plugin directory.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 PLUGIN_PATH/scripts/buffer.py",
            "timeout": 5000
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "PLUGIN_PATH/hooks/session-start.sh",
            "timeout": 30000
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "PLUGIN_PATH/hooks/session-end.sh",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

## Data

All data stored in `~/.claude-toolkit/observer/`:

```
~/.claude-toolkit/observer/
├── observer.db      # SQLite database (sessions, observations, summaries)
├── buffers/         # Temporary JSONL files during active sessions
└── errors.log       # Processing failures
```

## Commands

### `/observer:search <query>`

Search past observations using full-text search.

```
/observer:search "authentication bug"
/observer:search "database" --project factory --type decision
```

## Architecture

### PostToolUse Hook (buffer.py)

Appends raw tool observations to a per-session JSONL buffer. Filters out uninteresting tools (TodoWrite, AskUserQuestion, Skill, MCP tools, etc.). Truncates large payloads (>5KB). Targets <50ms execution.

### SessionEnd Hook (session-end.sh)

Spawns `process.py` in the background via `nohup`. Never blocks session termination.

### Background Processor (process.py)

1. Reads the session's JSONL buffer
2. Samples if >200 entries (keeps first/last 10 + evenly spaced middle)
3. Builds a batch prompt with all observations
4. Calls `claude -p --model haiku --no-session-persistence`
5. Parses XML response into structured observations + summary
6. Stores to SQLite with FTS5 indexing
7. Deletes buffer on success

### SessionStart Hook (inject.py)

Queries SQLite for recent observations and summaries for the current project. Formats as concise markdown and returns via `hookSpecificOutput.additionalContext`.

Also processes any orphaned buffers from previous sessions that failed to process.

## Database Schema

```sql
sessions    (session_id, project, observation_count, created_at, completed_at)
observations (session_id, project, type, title, narrative, facts, files_read, files_modified)
summaries   (session_id, project, request, learned, completed, next_steps)
```

FTS5 virtual table indexes observation titles, narratives, and facts for full-text search.

## Requirements

- Python 3.10+ (uses `sqlite3` stdlib module)
- `claude` CLI in PATH (Max subscription)
- `git` (for project detection)

## Coexistence

- Works alongside the **memory** plugin (manual knowledge management)
- Works alongside the **transition** plugin (explicit session handoffs)
- Works alongside **claude-mem** if installed (separate database and buffer directory)
