# Memory Plugin

Active memory management for Claude Code projects using the `.workspace/`-shared layout. Keep persistent context fresh, organized, and relevant — across both Claude and Codex sessions.

## Overview

Memory lives at `.workspace/memory/` and is referenced by `AGENTS.md` via `@-include` so Claude loads it on every session and Codex reads it on demand. The seed is intentionally small (3 files) — add more only when a recurring need emerges.

```
.workspace/memory/
├── project_state.md   # What's working, stubbed, decisions to make
├── conventions.md     # Code, data, testing, commits, infrastructure rules
└── decisions.md       # Load-bearing choices with rationale
```

How it works:
- `AGENTS.md` includes the three files via `@.workspace/memory/<file>.md`.
- `CLAUDE.md` is one line (`@AGENTS.md`), so Claude inherits the same context.
- Stale content silently degrades agent quality — run `/memory-gc` periodically.

## Commands

### `/memory-review`
List all `.workspace/memory/` files with size, line count, and modification age. Flags entries >30 days old. Use before starting work, after long breaks, or before `/memory-gc` to preview.

### `/memory-update`
Interactive add/update/remove/relocate workflow. Suggests entries based on recent commits and decisions. Apply after shipping a feature, making an architectural choice, or changing conventions.

### `/memory-gc`
Identify and remove stale entries. Detects superseded decisions, completed temp tasks, and content that hasn't been touched in >30 days. Backs up to `.workspace/work/archives/memory/` before destructive ops.

```bash
/memory-gc            # analyze + suggest
/memory-gc --auto     # auto-clean with confirmation
/memory-gc --dry-run  # preview only
```

### `/index`
Build or refresh project understanding into `.claude/PROJECT_MAP.md` — architectural overview, component relationships, key patterns. (Lives at `.claude/` because it's Claude-specific code mapping, not shared memory.)

```bash
/index             # initial map
/index --update    # incremental refresh
/index --refresh   # rebuild from scratch
/index backend     # focus area
```

### `/performance`
Show token usage by component (conversation, MCP, memory, system). Recommends optimizations when context climbs past 70/80/90% thresholds.

## MEMORY_INDEX.md format

`MEMORY_INDEX.md` lives at `.workspace/memory/MEMORY_INDEX.md` and is the
single, authoritative manifest of a project's memory. It is what `AGENTS.md`
should `@-include` so a session auto-loads a bounded index instead of every
memory file in full. The companion `bin/verify_index.sh` checks its integrity.

**The index is authoritative.** Where a memory file's own frontmatter disagrees
with the index, the index wins; tooling reports the mismatch and proposes
syncing the file down to the index value. Treat the index as source of truth,
the file frontmatter as informational.

### Structure

YAML frontmatter, then one `##` entry per memory file:

```markdown
---
auto_loaded_cap: 5000
---

# Memory Index

## project_state.md
- status: active
- last_referenced: 2026-06-01
- tokens: 320
- anchors: src/auth/jwt.py, bin/migrate.sh

## conventions.md
- status: dormant
- last_referenced: 2026-05-01
- tokens: 210
- anchors:

## old_architecture.md
- status: superseded-by: project_state.md
- last_referenced: 2026-04-01
- tokens: 90
- anchors: none
```

**Frontmatter**

- `auto_loaded_cap: <n>` — the token ceiling for auto-loaded memory, per-project
  overridable. Recommended (a missing cap is a warning, not an error).

**Per-file entry** — heading is the memory filename relative to the memory
directory (e.g. `## project_state.md`). Each entry carries all four required
fields:

| Field | Meaning |
|---|---|
| `status` | One of `active`, `dormant`, `deprecated`, or `superseded-by:<slug>` (the slug is another memory's filename). |
| `last_referenced` | `YYYY-MM-DD` of the last time a signal touched the file, or `never`. |
| `tokens` | Estimated token count (integer), from the shared `bin/token_count.py`. |
| `anchors` | Comma-separated file paths / commands / symbols the memory describes. Leave empty (or `none` / `n/a`) when there are none. |

The index does **not** list itself, and `.index_state.json` (the gitignored
signal sidecar) is runtime state, not an entry.

### Verifying the index

```bash
memory/bin/verify_index.sh              # verify current project's .workspace/memory/
memory/bin/verify_index.sh --dir DIR    # verify a specific memory directory
memory/bin/verify_index.sh --strict     # treat warnings (e.g. frontmatter drift) as failures
memory/bin/verify_index.sh --quiet      # show problems only
```

Exit codes: `0` every memory file has a complete, valid entry (0 missing);
`1` an integrity failure (a file with no entry, an entry missing a required
field, or an out-of-vocabulary status); `2` an environment error (no memory
directory, or no `MEMORY_INDEX.md` to verify against).

Claude's own auto-memory at `~/.claude/projects/.../memory/` is **recognized for
display only** — `verify_index.sh` notes the shape and lists its files but never
manages it (no writes, no redirects). Only `.workspace/memory/` is managed.

## Memory file guidelines

### project_state.md
Current snapshot — what's working, what's stubbed, decisions still open, recent runs. Update at major milestones or weekly. Keep terse.

```markdown
## What's working
- Auth flow: email + JWT, tested end-to-end

## What's stubbed or absent
- Password reset (placeholder route only)

## Decisions to make
- Session storage: Redis vs Postgres unlogged table
```

### conventions.md
Code, data, testing, commits, infrastructure. Update when establishing or changing a pattern. The `## Infrastructure` section should always note that memory + transitions live at `.workspace/` — not `.claude/memory/`.

### decisions.md
Load-bearing choices with the *why* and the trade-off accepted. Date every entry. Future agents read this before suggesting alternatives.

```markdown
## 2025-10-15: PostgreSQL over MongoDB
**Why**: Need ACID transactions; relational data; team SQL fluency.
**Trade-off**: Lose document flexibility; mitigated by JSONB columns.
```

## When to add more files

The seed is 3 files on purpose. Add a new memory file only when:
- A category of context is referenced 3+ times in conversations
- It doesn't fit cleanly in `project_state` / `conventions` / `decisions`
- It's persistent (not session-local — that goes in `.workspace/transitions/`)

Common organic additions: `domain-terminology.md`, `infrastructure-topology.md`, `<vendor>-quirks.md`. Resist `lessons_learned.md` and `dependencies.md` — the first becomes a graveyard, the second drifts from the lockfile.

## Best practices

Do:
- Update memory after significant work (`/ship` auto-suggests)
- Keep entries 2–4 lines max; link, don't paste
- Date decisions
- Run `/memory-gc` monthly
- Review memory before starting new work

Don't:
- Copy code snippets — link to file:line
- Document temporary state (use `.workspace/transitions/`)
- Keep superseded decisions
- Let memory grow beyond ~25KB (Claude reads it every session)
- Forget to update after major changes

## Auto-reflection

The plugin integrates with other workflow commands to suggest updates at the right moment:

- After `/ship`: prompt to add to `decisions.md` or update `project_state.md`
- After `/fix`: optional addition to `decisions.md` if the fix encoded a non-obvious choice
- After `/review`: convention updates if recurring issues found

## Integration

| Plugin | Touchpoint |
|---|---|
| workflow | `/ship` and `/explore` trigger update suggestions |
| development | `/review` proposes convention updates |
| system | `/system:status` shows memory size; `/cleanup` archives unused files |
| transition | `/handoff` and `/continue` (in transition plugin, not memory) read memory for session context |

## Troubleshooting

**Memory not loading**: confirm `AGENTS.md` includes `@.workspace/memory/<file>.md` lines and that `CLAUDE.md` contains `@AGENTS.md`. Check files are valid markdown.

**`/memory-gc` removes too much**: increase the staleness threshold or run with `--dry-run` first. Backups land in `.workspace/work/archives/memory/`.

**Memory growing beyond 25KB**: run `/memory-gc`, link to source files instead of pasting, split a file only if a section is regularly updated independently.

**File at `.claude/memory/` instead of `.workspace/memory/`**: pre-migration projects keep their old path. New work writes to `.workspace/memory/`. To migrate: `mv .claude/memory .workspace/memory` and update `AGENTS.md` includes.

## Configuration

Memory commands read defaults from the plugin and respect any project-level overrides in `.claude/settings.json` (Claude-specific). There is no separate `memory.config.json` — defaults are sensible and rarely need changing.

## Dependencies

None required. Optional: `sequential-thinking` MCP enhances analysis quality in `/memory-update` and `/memory-gc`. All commands degrade gracefully when MCP unavailable.

---

**Version**: 2.0.0
**Category**: Core
**Commands**: 5 (memory-review, memory-update, memory-gc, index, performance)
**Layout**: `.workspace/memory/` (shared with Codex via `AGENTS.md`)
