#!/usr/bin/env python3
"""Batch-process session observations with claude -p.

Called from SessionEnd hook (background). Reads buffered observations,
sends a single batch prompt to claude -p --model haiku, parses XML
response, and stores structured observations + summary in SQLite.

Usage: python3 process.py <session_id> <cwd>
"""
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path.home() / ".claude-toolkit" / "observer"
BUFFER_DIR = DATA_DIR / "buffers"
DB_PATH = DATA_DIR / "observer.db"
ERROR_LOG = DATA_DIR / "errors.log"

MIN_OBSERVATIONS = 3  # Skip trivial sessions
MAX_BUFFER_ENTRIES = 200  # Sample if more
SAMPLE_TARGET = 100
CLAUDE_TIMEOUT = 120  # seconds


# ---------------------------------------------------------------------------
# SQLite schema
# ---------------------------------------------------------------------------

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    project TEXT NOT NULL,
    observation_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    project TEXT NOT NULL,
    type TEXT NOT NULL DEFAULT 'action',
    title TEXT,
    narrative TEXT,
    facts TEXT,
    files_read TEXT,
    files_modified TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    project TEXT NOT NULL,
    request TEXT,
    learned TEXT,
    completed TEXT,
    next_steps TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

CREATE INDEX IF NOT EXISTS idx_obs_project ON observations(project);
CREATE INDEX IF NOT EXISTS idx_obs_session ON observations(session_id);
CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project);

CREATE VIRTUAL TABLE IF NOT EXISTS observations_fts USING fts5(
    title, narrative, facts,
    content='observations',
    content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS obs_fts_insert AFTER INSERT ON observations BEGIN
    INSERT INTO observations_fts(rowid, title, narrative, facts)
    VALUES (new.id, new.title, new.narrative, new.facts);
END;

CREATE TRIGGER IF NOT EXISTS obs_fts_delete AFTER DELETE ON observations BEGIN
    INSERT INTO observations_fts(observations_fts, rowid, title, narrative, facts)
    VALUES('delete', old.id, old.title, old.narrative, old.facts);
END;
"""


def init_db():
    """Create database and tables if needed."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA busy_timeout = 5000")
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    return conn


# ---------------------------------------------------------------------------
# Buffer reading and sampling
# ---------------------------------------------------------------------------

def read_buffer(session_id: str) -> list[dict]:
    """Read observations from session buffer file."""
    buffer_path = BUFFER_DIR / f"{session_id}.jsonl"
    if not buffer_path.exists():
        return []

    entries = []
    with open(buffer_path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def sample_entries(entries: list[dict], target: int = SAMPLE_TARGET) -> list[dict]:
    """Sample entries if buffer is too large. Keep first/last + evenly spaced middle."""
    if len(entries) <= target:
        return entries

    keep_ends = 10
    first = entries[:keep_ends]
    last = entries[-keep_ends:]
    middle = entries[keep_ends:-keep_ends]

    middle_target = target - (2 * keep_ends)
    step = max(1, len(middle) // middle_target)
    sampled_middle = middle[::step][:middle_target]

    return first + sampled_middle + last


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------

def detect_project(cwd: str) -> str:
    """Detect project name from working directory."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd, capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return os.path.basename(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return os.path.basename(cwd) if cwd else "unknown"


def build_prompt(entries: list[dict], project: str, session_id: str) -> str:
    """Build the batch prompt for claude -p."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Format entries as XML
    formatted = []
    for i, entry in enumerate(entries, 1):
        formatted.append(
            f'<entry seq="{i}" ts="{entry.get("ts", "")}">\n'
            f'  <tool>{entry.get("tool", "")}</tool>\n'
            f'  <input>{entry.get("input", "")}</input>\n'
            f'  <response>{entry.get("response", "")}</response>\n'
            f'</entry>'
        )

    tool_log = "\n".join(formatted)

    return f"""You are an AI code observer. You analyze tool usage logs from a coding session and extract structured observations.

## Project: {project}
## Session: {session_id[:12]}
## Date: {today}
## Entries: {len(entries)}

Below are {len(entries)} tool observations from a Claude Code session.

<tool_log>
{tool_log}
</tool_log>

## Instructions

1. Read ALL tool observations above.
2. Group related actions into coherent observations (e.g., Read+Grep+Edit on same file = one observation).
3. Output ONLY XML. No prose, no explanations, no markdown.
4. Output 1-10 <observation> blocks capturing the meaningful work.
5. Output exactly 1 <summary> block at the end.

## Observation Types
- action: Generic meaningful work (config, deps, setup)
- discovery: Learning about existing code/system
- decision: Architectural or design choice with rationale
- bugfix: Something was broken, now fixed
- feature: New capability added
- refactor: Code restructured, behavior unchanged

## Output Format

<observation>
  <type>bugfix|feature|refactor|discovery|decision|action</type>
  <title>Concise title (5-10 words)</title>
  <narrative>1-2 sentence description of what happened and why</narrative>
  <facts>
    <fact>Specific technical fact worth remembering</fact>
  </facts>
  <files_read>
    <file>path/to/file</file>
  </files_read>
  <files_modified>
    <file>path/to/file</file>
  </files_modified>
</observation>

<summary>
  <request>What the user was trying to accomplish</request>
  <learned>Key technical insights from this session</learned>
  <completed>What was actually finished</completed>
  <next_steps>What should happen next</next_steps>
</summary>

## Rules
- Skip trivial Read-only browsing with no resulting action
- Skip duplicate observations (same file edited multiple times = one observation)
- Facts must be specific and technical, not vague
- NEVER output text outside XML tags"""


# ---------------------------------------------------------------------------
# Claude invocation
# ---------------------------------------------------------------------------

def call_claude(prompt: str) -> str:
    """Call claude -p with the batch prompt."""
    claude_path = shutil.which("claude")
    if not claude_path:
        raise RuntimeError("claude CLI not found in PATH")

    result = subprocess.run(
        [
            claude_path, "-p",
            "--model", "haiku",
            "--no-session-persistence",
            "--output-format", "text",
        ],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=CLAUDE_TIMEOUT,
    )

    if result.returncode != 0:
        stderr = result.stderr[:500] if result.stderr else "(no stderr)"
        raise RuntimeError(f"claude -p exited {result.returncode}: {stderr}")

    return result.stdout


# ---------------------------------------------------------------------------
# XML parsing (port of claude-mem's parser.ts)
# ---------------------------------------------------------------------------

def extract_field(content: str, name: str) -> str | None:
    """Extract a single XML field value."""
    match = re.search(rf"<{name}>([\s\S]*?)</{name}>", content)
    if not match:
        return None
    val = match.group(1).strip()
    return val if val else None


def extract_array(content: str, array_name: str, element_name: str) -> list[str]:
    """Extract array of XML elements."""
    array_match = re.search(rf"<{array_name}>([\s\S]*?)</{array_name}>", content)
    if not array_match:
        return []
    elements = []
    for elem_match in re.finditer(
        rf"<{element_name}>([\s\S]*?)</{element_name}>", array_match.group(1)
    ):
        val = elem_match.group(1).strip()
        if val:
            elements.append(val)
    return elements


def parse_observations(text: str) -> list[dict]:
    """Parse <observation> blocks from response."""
    observations = []
    valid_types = {"action", "discovery", "decision", "bugfix", "feature", "refactor"}

    for match in re.finditer(r"<observation>([\s\S]*?)</observation>", text):
        content = match.group(1)
        obs_type = extract_field(content, "type") or "action"
        if obs_type not in valid_types:
            obs_type = "action"

        observations.append({
            "type": obs_type,
            "title": extract_field(content, "title"),
            "narrative": extract_field(content, "narrative"),
            "facts": extract_array(content, "facts", "fact"),
            "files_read": extract_array(content, "files_read", "file"),
            "files_modified": extract_array(content, "files_modified", "file"),
        })
    return observations


def parse_summary(text: str) -> dict | None:
    """Parse <summary> block from response."""
    match = re.search(r"<summary>([\s\S]*?)</summary>", text)
    if not match:
        return None
    content = match.group(1)
    summary = {
        "request": extract_field(content, "request"),
        "learned": extract_field(content, "learned"),
        "completed": extract_field(content, "completed"),
        "next_steps": extract_field(content, "next_steps"),
    }
    # At least one field must be present
    if not any(summary.values()):
        return None
    return summary


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

def store_results(
    conn: sqlite3.Connection,
    session_id: str,
    project: str,
    observations: list[dict],
    summary: dict | None,
    obs_count: int,
):
    """Store parsed observations and summary to SQLite."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    conn.execute(
        "INSERT OR REPLACE INTO sessions (session_id, project, observation_count, completed_at) "
        "VALUES (?, ?, ?, ?)",
        (session_id, project, obs_count, now),
    )

    for obs in observations:
        conn.execute(
            "INSERT INTO observations "
            "(session_id, project, type, title, narrative, facts, files_read, files_modified) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                session_id,
                project,
                obs["type"],
                obs["title"],
                obs["narrative"],
                json.dumps(obs["facts"]),
                json.dumps(obs["files_read"]),
                json.dumps(obs["files_modified"]),
            ),
        )

    if summary:
        conn.execute(
            "INSERT OR REPLACE INTO summaries "
            "(session_id, project, request, learned, completed, next_steps) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                session_id,
                project,
                summary.get("request"),
                summary.get("learned"),
                summary.get("completed"),
                summary.get("next_steps"),
            ),
        )

    conn.commit()


# ---------------------------------------------------------------------------
# Error logging
# ---------------------------------------------------------------------------

def log_error(session_id: str, error: str):
    """Append error to log file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with open(ERROR_LOG, "a") as f:
            f.write(f"{now} | session={session_id[:12]} | {error}\n")
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: process.py <session_id> <cwd>", file=sys.stderr)
        sys.exit(1)

    session_id = sys.argv[1]
    cwd = sys.argv[2]

    # Read buffer
    entries = read_buffer(session_id)
    if len(entries) < MIN_OBSERVATIONS:
        # Trivial session, clean up buffer
        buffer_path = BUFFER_DIR / f"{session_id}.jsonl"
        buffer_path.unlink(missing_ok=True)
        return

    # Detect project
    project = detect_project(cwd)

    # Sample if needed
    entries = sample_entries(entries)

    # Build prompt
    prompt = build_prompt(entries, project, session_id)

    # Call claude -p
    try:
        response = call_claude(prompt)
    except Exception as e:
        log_error(session_id, f"claude -p failed: {e}")
        return  # Buffer preserved for retry

    # Parse response
    observations = parse_observations(response)
    summary = parse_summary(response)

    if not observations and not summary:
        log_error(session_id, "No observations or summary parsed from response")
        # Still delete buffer — response was received, just not parseable
        buffer_path = BUFFER_DIR / f"{session_id}.jsonl"
        buffer_path.unlink(missing_ok=True)
        return

    # Store to SQLite
    try:
        conn = init_db()
        store_results(conn, session_id, project, observations, summary, len(entries))
        conn.close()
    except Exception as e:
        log_error(session_id, f"SQLite error: {e}")
        return  # Buffer preserved

    # Success — remove buffer
    buffer_path = BUFFER_DIR / f"{session_id}.jsonl"
    buffer_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
