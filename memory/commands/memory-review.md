---
title: memory-review
aliases: [/memory-review]
description: Index-aware view of `.workspace/memory/` — status counts (active/dormant/deprecated), per-entry table, and auto-loaded tokens vs cap.
---

# Memory Review (γ — index-driven)

`/memory-review` summarizes a project's memory in terms of the
`MEMORY_INDEX.md` it auto-loads, not in terms of disk size + mtime. It
combines four sources:

- `MEMORY_INDEX.md` for status, tokens, anchors
- `.index_state.json` for per-file `last_referenced` (newer of index vs
  sidecar wins) and project-level `last_gc_run`
- `bin/measure_memory.sh` for the actual auto-loaded total to check
  against the `auto_loaded_cap` from the index frontmatter

Recognizes Claude's auto-memory shape at
`~/.claude/projects/<slug>/memory/` as display-only (listed but not
analyzed for status — we don't manage it).

## Usage

```bash
/memory-review              # default: current project (.workspace/memory)
/memory-review --dir DIR    # explicit memory directory
```

## Plan (Claude executes)

Invoke the shared helper:

```bash
BIN="${CLAUDE_PLUGIN_ROOT}/bin"
[[ -z "$CLAUDE_PLUGIN_ROOT" ]] && BIN="$HOME/agents/coding/plugins/memory/bin"
python3 "$BIN/memory_review.py"        # current project
# python3 "$BIN/memory_review.py" --dir "$path"   # alternate path
```

Show the output verbatim. If `auto_loaded` > `cap`, recommend
`/memory-gc` to demote stale entries (or revisit the cap value).

## What the output covers

- **Per-entry table** — file, status, last_referenced (best signal),
  tokens, anchors.
- **Status counts** — how many `active` / `dormant` / `deprecated` /
  `superseded-by:*`.
- **Inventory tokens** — sum of `tokens` across all index entries
  (what could be loaded on demand).
- **Auto-loaded** — what's actually loaded at session start via the
  AGENTS.md @-include chain, vs the cap.
- **last_gc_run** — date + days-ago. Drives the SessionStart nudge.

## Integration

| Plugin | Touchpoint |
|---|---|
| `system` | `/system:status` may surface the status counts + cap line |
| `workflow` | `/ship` reads memory for context; consult `/memory-review` if context tax feels high |
| `memory` (this plugin) | Run `/memory-gc` to act on whatever `/memory-review` surfaces |
