#!/usr/bin/env python3
"""Query observer database and format context for injection.

Called from SessionStart hook. Outputs markdown to stdout.
The shell wrapper formats it as hookSpecificOutput JSON.
"""
import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path.home() / ".claude-toolkit" / "observer" / "observer.db"

MAX_SUMMARIES = 3
MAX_OBSERVATIONS = 15


def detect_project() -> str:
    """Detect project name from current working directory."""
    cwd = os.getcwd()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return os.path.basename(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return os.path.basename(cwd)


def relative_time(iso_str: str) -> str:
    """Convert ISO timestamp to relative time string."""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = now - dt
        hours = int(delta.total_seconds() / 3600)
        if hours < 1:
            mins = int(delta.total_seconds() / 60)
            return f"{max(1, mins)}m ago"
        if hours < 24:
            return f"{hours}h ago"
        days = hours // 24
        return f"{days}d ago"
    except (ValueError, TypeError):
        return iso_str[:10] if iso_str else "unknown"


def format_context(project: str, summaries: list, observations: list) -> str:
    """Format query results as markdown for context injection."""
    if not summaries and not observations:
        return ""

    lines = [f'<observer-context project="{project}">', "## Recent Session Memory", ""]

    # Latest summary
    if summaries:
        latest = summaries[0]
        _, _, _, request, learned, completed, next_steps, created_at = latest
        when = relative_time(created_at)
        lines.append(f"### Last Session ({when})")
        if request:
            lines.append(f"**Goal**: {request}")
        if completed:
            lines.append(f"**Completed**: {completed}")
        if learned:
            lines.append(f"**Learned**: {learned}")
        if next_steps:
            lines.append(f"**Next**: {next_steps}")
        lines.append("")

    # Prior summaries (compact)
    if len(summaries) > 1:
        lines.append("### Prior Sessions")
        for row in summaries[1:]:
            _, _, _, request, learned, completed, _, created_at = row
            when = relative_time(created_at)
            desc = completed or request or learned or "(no description)"
            # Truncate to one line
            if len(desc) > 100:
                desc = desc[:97] + "..."
            lines.append(f"- **{when}**: {desc}")
        lines.append("")

    # Recent observations table
    if observations:
        lines.append("### Key Observations")
        lines.append("| Type | Title | When |")
        lines.append("|------|-------|------|")
        for row in observations:
            _, _, _, obs_type, title, _, _, _, _, created_at = row
            when = relative_time(created_at)
            title_str = title or "(untitled)"
            if len(title_str) > 60:
                title_str = title_str[:57] + "..."
            lines.append(f"| {obs_type} | {title_str} | {when} |")
        lines.append("")

    lines.append("</observer-context>")
    return "\n".join(lines)


def main():
    if not DB_PATH.exists():
        return  # No database yet, nothing to inject

    project = detect_project()

    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("PRAGMA busy_timeout = 2000")

        summaries = conn.execute(
            "SELECT * FROM summaries WHERE project = ? ORDER BY created_at DESC LIMIT ?",
            (project, MAX_SUMMARIES),
        ).fetchall()

        observations = conn.execute(
            "SELECT * FROM observations WHERE project = ? ORDER BY created_at DESC LIMIT ?",
            (project, MAX_OBSERVATIONS),
        ).fetchall()

        conn.close()
    except (sqlite3.Error, OSError):
        return  # Graceful degradation

    context = format_context(project, summaries, observations)
    if context:
        print(context)


if __name__ == "__main__":
    main()
