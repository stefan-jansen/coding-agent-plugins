# Memory Budget Migration Guide (γ — index-first, signal-driven memory)

This guide walks a project through opting in to the γ memory-budget
architecture: index-only auto-load, captured signals, automated
relevance review. The capability ships in this plugin; per-project
rollout is opt-in.

**Why opt in.** Without γ, auto-loaded `.workspace/memory/*.md` files
referenced from `AGENTS.md` / `CLAUDE.md` consume the full body of every
memory file at session start. Even modestly-sized memory directories
quickly hit 10K+ tokens before any actual work begins. With γ, the
auto-loaded payload is bounded by `MEMORY_INDEX.md` (typically <2.5K
tokens); the individual memory files are read on demand when their
topic is relevant.

The Factory project measured 9,047 → 2,405 tokens (-73%) after migration.

## Architecture overview

```
.workspace/memory/
├── MEMORY_INDEX.md       # the only thing auto-loaded by AGENTS.md
├── .index_state.json     # gitignored — sidecar maintained by hooks
├── project_state.md      # read on demand
├── conventions.md
└── ...
```

- **MEMORY_INDEX.md** — committed; source of truth. One entry per file
  with `status` / `last_referenced` / `tokens` / `anchors`. Frontmatter
  carries `auto_loaded_cap`.
- **.index_state.json** — gitignored; runtime sidecar holding
  per-file `last_referenced` (bumped by the PreToolUse hook) and
  project-level `last_gc_run` (stamped by `/memory-gc`).
- **Status vocabulary** — `active | dormant | deprecated |
  superseded-by:<slug>`. `/memory-gc` transitions automatically using
  observed signals; `superseded-by:*` is user-owned.

## One-time migration steps

### 1. Seed the index

From the project root:

```bash
BIN="$HOME/agents/coding/plugins/memory/bin"
bash "$BIN/memory_init_index.sh"
```

This walks `.workspace/memory/`, computes tokens per file, and writes
`MEMORY_INDEX.md` + `.index_state.json`. Idempotent — re-running
preserves any statuses or anchors you've already set.

### 2. Choose a cap

The default cap in the seeded index is `5000`. Measure your current
auto-loaded total and set the cap to ~1.5× the *index-only* baseline:

```bash
bash "$BIN/measure_memory.sh" --total-only          # what AGENTS.md loads today
bash "$BIN/measure_memory.sh" --total-only          # re-run after step 3
```

Then update the frontmatter:

```yaml
---
auto_loaded_cap: 3500    # for example
---
```

A useful rule of thumb: `cap = max(2 * MEMORY_INDEX.md tokens, 3500)`.
Round to the nearest 500.

### 3. Switch AGENTS.md to index-only @-include

Replace any `@.workspace/memory/<file>.md` lines in `AGENTS.md` with a
single line:

```markdown
## Project memory

Memory is **index-only at session start.** Read the body of any indexed
file on demand when its topic is relevant.

@.workspace/memory/MEMORY_INDEX.md
```

`CLAUDE.md` remains the one-line `@AGENTS.md` re-export.

### 4. Gitignore the sidecar

```bash
echo '.workspace/memory/.index_state.json' >> .gitignore
git add .gitignore .workspace/memory/MEMORY_INDEX.md
git commit -m "feat(memory): adopt index-first auto-load (γ)"
```

### 5. Verify

```bash
bash "$BIN/verify_index.sh"          # integrity (every file has an entry)
bash "$BIN/measure_memory.sh"        # total under cap?
python3 "$BIN/memory_review.py"      # human-readable index summary
```

All three should succeed and report under-cap. Start a fresh
`claude` / `codex` session — you should see the reduced auto-load total.

## What γ does once it's on

- The memory plugin's `PreToolUse` hook captures every Read/Grep of
  `.workspace/memory/<file>.md` into the sidecar as `last_referenced` +
  `references++`. This means GC operates on observed reality, not
  guesswork.
- The plugin's `SessionStart` hook reads `last_gc_run` from the sidecar
  and prints a one-line nudge if it's >7 days old (or null). Enable
  `memory.auto_gc: true` in `.claude/settings.json` to also print a
  dry-run inline.
- The transition plugin's `pre-compact.sh` extends the same nudge into
  compaction, ensuring "≥1 effective trigger per active week."
- `/memory-gc` reads the index + sidecar + anchor health and proposes a
  status diff (`active → dormant → deprecated` heuristics + respect for
  `superseded-by:*`). `--execute` applies the diff transactionally and
  stamps `last_gc_run`, resetting the nudge.

## Troubleshooting

**SessionStart says "/memory-gc has not run in never" forever.** Run
`/memory-gc --execute --auto` once (even with no transitions); this
stamps `last_gc_run` so the nudge stops for 7 days.

**verify_index.sh fails with "missing entry"** after I added a file. Run
`bash "$BIN/memory_init_index.sh"` — it picks up new files and writes
a default `active` entry.

**The hooks aren't firing.** Ensure the `memory` plugin (and ideally
`transition`) is in your project's `.claude/settings.json`
`enabledPlugins`. The plugins' `hooks/hooks.json` manifests register
themselves automatically when the plugin is enabled.

**Cap creep.** Run `python3 "$BIN/memory_review.py"` — if `Auto-loaded`
keeps climbing toward the cap, the index is gaining entries. Run
`/memory-gc` to demote stale ones, or split the index across multiple
files (γ has no requirement that it's a single document).

## Reverting

`γ` is additive. To revert, restore the original `@-include` lines in
`AGENTS.md`. The `MEMORY_INDEX.md` file remains harmless on disk; the
sidecar is gitignored so dropping it leaves no trace.
