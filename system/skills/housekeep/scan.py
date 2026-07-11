#!/usr/bin/env python3
"""Housekeep scan: enumerate .workspace/ and .claude/ agent-infra dirs across
roots, classify each, print findings.

Classes (mutually exclusive, first match wins):
  DOUBLED           — path contains '.workspace/.workspace/' or '.claude/.claude/'
  NESTED_IN_AGENT   — agent dir whose ancestor also contains one at same level
  WORKER_POOL       — path contains '/.claude/worktrees/' (disposable agent-worker worktrees)
  SUBREPO_STRAY     — inside a git worktree/subrepo that is not the project root
  STUB_ONLY         — only stub transition files (header + Session ended line)
  OLD_DEBRIS        — newest content file >30 days old
  EXPECTED          — at project root, or test/eval scaffolding

For each finding, print one line. Also emit --json summary at the end.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

SKIP_DIRS = {"node_modules", ".git", ".venv", "venv", "target", "dist",
             "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
             "build", ".next", ".cache"}
AGENT_DIR_NAMES = {".workspace", ".claude"}
PROJECT_MARKERS = {"README.md", "AGENTS.md", "CLAUDE.md", "pyproject.toml",
                   "package.json", "Cargo.toml", "go.mod", ".git"}
TEST_FIXTURE_MARKERS = ("/fixtures/", "/tests/", "/evals/", "/eval/",
                        "/.archive/", "/demo-project/", "/skill-compiler/")
STUB_RE = re.compile(r"^\s*(#|##)\s*(Session Progress|Session ended)", re.M)


def find_agent_dirs(root: Path):
    """Walk root, yield every .workspace/ or .claude/ directory found."""
    for dirpath, dirnames, _ in os.walk(root, followlinks=False):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for d in list(dirnames):
            if d in AGENT_DIR_NAMES:
                yield Path(dirpath) / d


def looks_like_project_root(p: Path) -> bool:
    """Heuristic: parent has ≥2 project markers or is a well-known project."""
    hits = sum(1 for m in PROJECT_MARKERS if (p / m).exists())
    return hits >= 2


def find_enclosing_project(p: Path) -> Path | None:
    """Walk up from p, find nearest ancestor that looks like a project root."""
    cur = p.parent if p.is_dir() else p
    home = Path.home()
    while cur != cur.parent and cur.is_relative_to(home):
        if looks_like_project_root(cur):
            return cur
        cur = cur.parent
    return None


def newest_mtime(p: Path) -> float:
    """Newest mtime under p, 0 if empty."""
    newest = 0.0
    for f in p.rglob("*"):
        try:
            if f.is_file():
                newest = max(newest, f.stat().st_mtime)
        except OSError:
            pass
    return newest


def count_files_and_stubs(p: Path) -> tuple[int, int]:
    """(total_md_files, stub_only_count)."""
    total = 0
    stubs = 0
    for f in p.rglob("*.md"):
        try:
            total += 1
            text = f.read_text(encoding="utf-8", errors="ignore")
            non_stub = re.sub(STUB_RE, "", text).strip()
            # A file is stub-only if removing the header + "Session ended"
            # patterns leaves only whitespace or trivial separators.
            if len(non_stub) < 20 or non_stub in ("---", "-", ""):
                stubs += 1
        except OSError:
            pass
    return total, stubs


def is_worktree_or_subrepo(p: Path) -> bool:
    """The parent of p is a git worktree (`.git` is a file) or nested repo."""
    parent = p.parent
    git = parent / ".git"
    if git.is_file():
        return True  # worktree
    if git.is_dir():
        # A nested full repo: check whether parent is the actual project root
        # or a sub-repo underneath one.
        return not looks_like_project_root(parent)
    return False


def classify(p: Path, now: float, stub_age_days: int) -> tuple[str, dict]:
    parts = p.parts
    joined = str(p)

    # Stats always computed so the display is uniform across classes.
    total, stubs = count_files_and_stubs(p)
    newest = newest_mtime(p)
    age_days = int((now - newest) / 86400) if newest else None
    stats = {
        "path": joined,
        "total_md": total,
        "stubs": stubs,
        "newest_mtime": newest,
        "age_days": age_days,
    }

    # EXPECTED_FIXTURE first — test/demo/eval scaffolding is legitimate even
    # when it looks structurally like a bug (nested inside an agent dir).
    for marker in TEST_FIXTURE_MARKERS:
        if marker in joined:
            return "EXPECTED_FIXTURE", stats

    # DOUBLED — cheapest structural check
    for a in (".workspace", ".claude"):
        if f"/{a}/{a}/" in joined + "/" or joined.endswith(f"/{a}/{a}"):
            return "DOUBLED", stats

    # WORKER_POOL — more specific than NESTED_IN_AGENT, must come first
    if "/.claude/worktrees/" in joined + "/":
        return "WORKER_POOL", stats

    # NESTED_IN_AGENT — an agent dir whose ancestor path contains another agent
    # dir (with something between them, otherwise it's DOUBLED).
    for i, part in enumerate(parts[:-1]):
        if part in AGENT_DIR_NAMES and any(
            later == p.name and j > i + 1
            for j, later in enumerate(parts)
        ):
            return "NESTED_IN_AGENT", stats

    # SUBREPO_STRAY — not at project root, hook wrote here via git rev-parse
    proj = find_enclosing_project(p)
    if proj and proj != p.parent:
        return "SUBREPO_STRAY", stats
    if is_worktree_or_subrepo(p):
        return "SUBREPO_STRAY", stats

    # STUB_ONLY — most files are stubs
    if total > 0 and stubs / total >= 0.8:
        return "STUB_ONLY", stats

    # OLD_DEBRIS — nothing recent
    if newest and age_days is not None and age_days > stub_age_days and total <= 3:
        return "OLD_DEBRIS", stats

    return "EXPECTED", stats


def format_line(cls: str, stats: dict) -> str:
    p = stats["path"]
    total = stats.get("total_md", 0)
    stubs = stats.get("stubs", 0)
    age = stats.get("age_days")
    age_str = "empty" if age is None else f"{age}d"
    return f"[{cls:15}] {p}  |  {total} md ({stubs} stubs) | {age_str}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", nargs="+", required=True,
                    help="Root dirs to scan (e.g. ~/projects ~/agents).")
    ap.add_argument("--json", action="store_true",
                    help="Emit JSON summary at end.")
    ap.add_argument("--stub-age-days", type=int, default=30,
                    help="Age (days) beyond which stub-heavy dirs are OLD_DEBRIS.")
    ap.add_argument("--severity", choices=["safe", "review", "all"],
                    default="all", help="Filter output by cleanup severity.")
    args = ap.parse_args()

    now = time.time()
    findings: list[tuple[str, dict]] = []

    for r in args.roots:
        root = Path(r).expanduser().resolve()
        if not root.exists():
            print(f"# skip: {root} does not exist", file=sys.stderr)
            continue
        for d in find_agent_dirs(root):
            cls, stats = classify(d, now, args.stub_age_days)
            findings.append((cls, stats))

    # Severity mapping
    SAFE = {"DOUBLED", "NESTED_IN_AGENT"}
    REVIEW = {"WORKER_POOL", "SUBREPO_STRAY", "STUB_ONLY", "OLD_DEBRIS"}

    def in_scope(cls: str) -> bool:
        if args.severity == "all":
            return True
        if args.severity == "safe":
            return cls in SAFE
        if args.severity == "review":
            return cls in SAFE or cls in REVIEW
        return True

    counts: dict[str, int] = {}
    lines: list[str] = []
    for cls, stats in sorted(findings, key=lambda x: (x[0], x[1]["path"])):
        counts[cls] = counts.get(cls, 0) + 1
        if in_scope(cls) and cls not in {"EXPECTED", "EXPECTED_FIXTURE"}:
            lines.append(format_line(cls, stats))

    print("\n".join(lines))
    print()
    print("# Counts by class:")
    for cls in sorted(counts):
        print(f"#   {cls:16} {counts[cls]}")

    if args.json:
        payload = {
            "counts": counts,
            "findings": [
                {"class": cls, **stats}
                for cls, stats in findings
                if cls not in {"EXPECTED", "EXPECTED_FIXTURE"}
            ],
        }
        print()
        print("# JSON:")
        print(json.dumps(payload, indent=2, default=str))

    return 0


if __name__ == "__main__":
    sys.exit(main())
