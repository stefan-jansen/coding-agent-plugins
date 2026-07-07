#!/usr/bin/env python3
"""Buffer raw tool observations to per-session JSONL files.

Called by PostToolUse hook. Must complete in <50ms.
Reads hook context from stdin, filters uninteresting tools,
truncates large payloads, appends to session buffer.
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

BUFFER_DIR = Path.home() / ".claude-toolkit" / "observer" / "buffers"
MAX_PAYLOAD_BYTES = 5120
TRUNCATE_KEEP = 2048

SKIP_TOOLS = frozenset({
    "TodoWrite", "AskUserQuestion", "Skill", "ToolSearch",
    "ScheduleWakeup", "LSP", "CronCreate", "CronDelete",
    "CronList", "Monitor", "RemoteTrigger", "EnterWorktree",
    "ExitWorktree", "EnterPlanMode", "ExitPlanMode",
    "TaskCreate", "TaskUpdate", "TaskGet", "TaskList",
    "TaskOutput", "TaskStop", "NotebookEdit",
})


def truncate(value, max_bytes=MAX_PAYLOAD_BYTES):
    """Truncate a string if it exceeds max_bytes."""
    s = json.dumps(value) if not isinstance(value, str) else value
    if len(s) <= max_bytes:
        return s
    return s[:TRUNCATE_KEEP] + "\n...[truncated]...\n" + s[-TRUNCATE_KEEP:]


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return
        data = json.loads(raw)
    except (json.JSONDecodeError, EOFError, OSError):
        return

    tool_name = data.get("tool_name", "")
    if not tool_name:
        return

    # Skip uninteresting tools
    if tool_name in SKIP_TOOLS:
        return
    if tool_name.startswith("mcp__"):
        return

    session_id = data.get("session_id", "")
    if not session_id:
        return

    entry = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": tool_name,
        "input": truncate(data.get("tool_input", {})),
        "response": truncate(data.get("tool_response", "")),
        "cwd": data.get("cwd", ""),
    }

    BUFFER_DIR.mkdir(parents=True, exist_ok=True)
    buffer_path = BUFFER_DIR / f"{session_id}.jsonl"

    try:
        with open(buffer_path, "a") as f:
            f.write(json.dumps(entry, separators=(",", ":")) + "\n")
    except OSError:
        pass  # Non-blocking: silently fail


if __name__ == "__main__":
    main()
