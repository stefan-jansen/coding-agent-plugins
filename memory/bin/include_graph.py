#!/usr/bin/env python3
"""@-include graph helper — the single source of truth for "what is auto-loaded".

Claude and Codex read `CLAUDE.md` and `AGENTS.md` at a project root on every
session and expand `@<path>` includes transitively. Several scripts need to know
that set: measure_memory.sh sums its tokens, verify_index.sh checks that the only
memory file in it is MEMORY_INDEX.md. They share this module so they cannot
disagree about what "auto-loaded" means.

Use as a module:
    from include_graph import parse_includes, reachable, SEED_FILES
    files, missing = reachable("/path/to/project")
"""
import os

# Files Claude/Codex read on every session before any @-include expansion.
SEED_FILES = ("CLAUDE.md", "AGENTS.md")


def parse_includes(path):
    """@-include targets declared in `path`, as absolute, normalized paths.

    An include is a line whose entire content is `@<relative-path>` (optionally
    surrounded by whitespace) — the canonical Claude Code / Codex form. Mentions
    of @path inside prose or fenced code blocks are deliberately ignored, since
    Claude does not expand those either.
    """
    out = []
    base = os.path.dirname(path)
    in_fence = False
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                stripped = line.strip()
                if stripped.startswith("```") or stripped.startswith("~~~"):
                    in_fence = not in_fence
                    continue
                if in_fence or not stripped.startswith("@"):
                    continue
                ref = stripped[1:]
                if not ref or any(c.isspace() for c in ref):
                    continue
                out.append(os.path.normpath(os.path.join(base, ref)))
    except (OSError, IOError):
        pass
    return out


def reachable(project_root):
    """(ordered existing files, missing-include paths) auto-loaded for a project.

    Breadth-first from the seed files, following @-includes transitively and
    de-duplicating. Missing include targets are reported separately rather than
    silently dropped.
    """
    seen, order, missing = set(), [], []
    queue = []
    for name in SEED_FILES:
        p = os.path.normpath(os.path.join(project_root, name))
        if os.path.isfile(p):
            queue.append(p)
    while queue:
        cur = queue.pop(0)
        if cur in seen:
            continue
        seen.add(cur)
        order.append(cur)
        for inc in parse_includes(cur):
            if inc in seen:
                continue
            if os.path.isfile(inc):
                queue.append(inc)
            elif inc not in missing:
                missing.append(inc)
    return order, missing
