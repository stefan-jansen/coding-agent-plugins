# Memory Plugin

Active memory management for Claude Code projects using the `.workspace/`-shared layout. Keep persistent context fresh, organized, and relevant — across both Claude and Codex sessions.

## Overview

Memory lives at `.workspace/memory/` and is referenced by `AGENTS.md`
through a single auto-loaded **index** so Claude pays a bounded
context tax at session start and Codex reads the same surface natively.
Individual memory files are read on demand when their topic is relevant.

```
.workspace/memory/
├── MEMORY_INDEX.md       # the only file auto-loaded by AGENTS.md
├── .index_state.json     # gitignored — runtime sidecar (signals)
├── project_state.md      # read on demand
├── conventions.md
└── decisions.md
```

How it works:
- `AGENTS.md` includes only `@.workspace/memory/MEMORY_INDEX.md`.
- `CLAUDE.md` is one line (`@AGENTS.md`), so Claude inherits the same context.
- Stale content silently degrades agent quality — `/memory-gc` consumes
  observed signals (`last_referenced`, `references`, anchor health) to
  produce a proposed status diff; `--execute` applies it transactionally.

This is the **γ memory-budget architecture**. See
`docs/memory-budget-migration.md` for opting an existing project in.

### Status vocabulary

| Status | When it applies |
|---|---|
| `active` | Currently relevant; read recently or load-bearing |
| `dormant` | Hasn't been touched in `--stale` days (default 90d) — still indexable; demoted from active |
| `deprecated` | Past `--deprecated` days (default 180d) with no signals — terminal status |
| `superseded-by:<slug>` | User-set link to the entry that supersedes this one — never touched by GC |

## Commands

### `/memory-review`
List all `.workspace/memory/` files with size, line count, and modification age. Flags entries >30 days old. Use before starting work, after long breaks, or before `/memory-gc` to preview.

### `/memory-update`
Interactive add/update/remove/relocate workflow. Suggests entries based on recent commits and decisions. Apply after shipping a feature, making an architectural choice, or changing conventions.

### `/memory-gc`
Propose `status` transitions in `MEMORY_INDEX.md` from how recently each entry was last read, then apply them in one transaction. It changes statuses only; it never deletes or moves a memory file.

```bash
/memory-gc                 # dry-run (default), writes nothing
/memory-gc --execute       # apply after confirmation
/memory-gc --json          # dry-run, machine-readable
/memory-gc --stale 60      # tune thresholds (defaults: 90d / 180d)
```

Recency is the whole heuristic: `active → dormant` past 90 days, `→ deprecated` past 180, plus a demotion when every one of an entry's anchors has disappeared from the working tree. `superseded-by:<slug>` is yours and never touched.

It cannot tell you a file is *wrong*. A memory file read every day and contradicted by the code six weeks ago stays `active`, correctly by this rule and uselessly for you. An empty GC diff means "nothing has gone unread", not "memory is accurate".

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
- `default_file_cap: <n>` — optional per-file token budget applied to every
  entry that does not set its own `cap`.

**Per-file entry** — heading is the memory filename relative to the memory
directory (e.g. `## project_state.md`). Each entry carries all four required
fields, plus an optional `cap`:

| Field | Meaning |
|---|---|
| `status` | One of `active`, `dormant`, `deprecated`, or `superseded-by:<slug>` (the slug is another memory's filename). |
| `last_referenced` | `YYYY-MM-DD` of the last time a signal touched the file, or `never`. |
| `tokens` | Estimated token count (integer), from the shared `bin/token_count.py`. Refreshed by `bin/memory_init_index.sh`; `verify_index.sh` warns once it stops tracking the file. |
| `anchors` | Comma-separated file paths / commands / symbols the memory describes. Leave empty (or `none` / `n/a`) when there are none. |
| `cap` | *Optional.* Token budget for this file, overriding `default_file_cap`. |

**Why a per-file cap.** `/memory-gc`'s unit is the whole entry and its signal is
`last_referenced`, so it can express "this file is stale" but not "this file is
active, correctly so, and twelve times the size it should be". Intra-file growth
is invisible to the status vocabulary. A `cap` makes it expressible: over it,
`verify_index.sh` warns and names the trim — keep the conclusion and a pointer in
the memory file, move the cut text to a sibling `<name>_archive.md`. The archive
costs nothing per session: only the index is `@`-included, so every memory file
is read on demand regardless of size.

The index does **not** list itself, and `.index_state.json` (the gitignored
signal sidecar) is runtime state, not an entry.

### Verifying the index

```bash
memory/bin/verify_index.sh              # verify current project's .workspace/memory/
memory/bin/verify_index.sh --dir DIR    # verify a specific memory directory
memory/bin/verify_index.sh --strict     # treat warnings (e.g. frontmatter drift) as failures
memory/bin/verify_index.sh --quiet      # show problems only
```

Exit codes: `0` every memory file has a complete, valid entry (0 missing) and
the `@`-include target is the index; `1` an integrity failure (a file with no
entry, an entry missing a required field, an out-of-vocabulary status, or a
memory file `@`-included directly by `AGENTS.md` / `CLAUDE.md`); `2` an
environment error (no memory directory, or no `MEMORY_INDEX.md` to verify
against).

The `@`-include check is the one that catches a **half-applied migration**:
`MEMORY_INDEX.md` seeded but `AGENTS.md` never switched to include it. That state
is indistinguishable from a healthy project by inspection — the index exists and
looks authoritative — while every memory file still loads in full on every
session. Warnings cover the softer signals: a `tokens` field that no longer
tracks its file, an entry over its `cap`, and an index that nothing
`@`-includes.

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

## Hooks

The plugin registers two hooks via `hooks/hooks.json` (auto-enabled when the
plugin is installed). Both are stdlib Python 3 with no third-party deps.

| Hook | Where | What it does |
|---|---|---|
| `PreToolUse` (matcher `Read\|Grep`) | `hooks/pre_tooluse_memory_ref.py` | Bumps `last_referenced` to today + increments `references` in the memory directory's `.index_state.json` whenever the agent reads or greps a `<file>.md` inside it (excluding `MEMORY_INDEX.md`). Honors `$CLAUDE_MEMORY_DIR`. Idempotent; never blocks a tool call. |
| `SessionStart` | `hooks/session_start.py` | Reads `last_gc_run` from the sidecar. If older than 7 days (or null), prints a one-line nudge to the session-start banner. With `memory.auto_gc: true` in `.claude/settings.json`, also prints a dry-run of proposed status changes (files unread for >90 days proposed `active → dormant`). Bounded: stat + JSON read only, <100ms on a Factory-shaped fixture (verified by `bin/test_hooks.sh`). |

`bin/stamp_gc_run.sh` writes `last_gc_run` after `/memory-gc` runs so the
nudge resets for the next week. The transition plugin's `pre-compact.sh` is
extended (additive, non-replacing) to also surface the nudge during
compaction — making compaction an additional effective trigger for the
relevance review on top of session start.

## Integration

| Plugin | Touchpoint |
|---|---|
| workflow | `/ship` and `/align` trigger update suggestions |
| development | `/review` proposes convention updates |
| system | `/system:status` shows memory size; `/cleanup` archives unused files |
| transition | `/handoff` and `/continue` read memory for session context; `pre-compact.sh` extended to also fire the memory-budget nudge when `/memory-gc` is stale |

## Troubleshooting

**Memory not loading**: confirm `AGENTS.md` includes `@.workspace/memory/<file>.md` lines and that `CLAUDE.md` contains `@AGENTS.md`. Check files are valid markdown.

**`/memory-gc` removes too much**: increase the staleness threshold or run with `--dry-run` first. Backups land in `.workspace/work/archives/memory/`.

**Memory growing beyond 25KB**: run `/memory-gc`, link to source files instead of pasting, split a file only if a section is regularly updated independently.

**File at `.claude/memory/` instead of `.workspace/memory/`**: pre-migration projects keep their old path. New work writes to `.workspace/memory/`. To migrate: `mv .claude/memory .workspace/memory` and update `AGENTS.md` includes.

## Configuration

Memory commands read defaults from the plugin and respect any project-level overrides in `.claude/settings.json` (Claude-specific). There is no separate `memory.config.json` — defaults are sensible and rarely need changing.

### Pointing the plugin at a different directory

`.workspace/memory/` is the default and the convention for new projects. A project that already keeps memory elsewhere, and has enough prose referring to those paths that relocating the files would break more than it fixes, can set `CLAUDE_MEMORY_DIR` in the `env` block of its `.claude/settings.json`:

```json
{
  "env": { "CLAUDE_MEMORY_DIR": "memory" }
}
```

Relative paths resolve against the project root; absolute paths are used as given. The setting reaches the hooks and every `bin/` script, so reads are recorded, the index is built, and GC runs against the directory you named. Every script also still takes an explicit `--dir`, which wins over the variable.

Without this, a project whose memory is not at `.workspace/memory/` records no reads at all and presents GC with an empty index — the commands appear to run fine and do nothing.

## Dependencies

None required. Optional: `sequential-thinking` MCP enhances analysis quality in `/memory-update` and `/memory-gc`. All commands degrade gracefully when MCP unavailable.

---

**Version**: 2.1.0
**Category**: Core
**Commands**: 5 (memory-review, memory-update, memory-gc, index, performance)
**Layout**: `.workspace/memory/` by default, or `$CLAUDE_MEMORY_DIR` (shared with Codex via `AGENTS.md`)
