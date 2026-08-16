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

The default cap in the seeded index is `5000`. Measure what `AGENTS.md`
loads today, then set the cap against the *index-only* baseline you will
have after step 3:

```bash
bash "$BIN/measure_memory.sh"                       # per-file breakdown + total
```

Then update the frontmatter:

```yaml
---
auto_loaded_cap: 3500    # for example
---
```

The cap covers the whole auto-loaded set, not just the index — and
`AGENTS.md` is usually the larger term, often by an order of magnitude.
So derive it from the measured post-step-3 total, not from the index
size: `cap = 1.3 * (AGENTS.md + CLAUDE.md + MEMORY_INDEX.md)`, rounded up
to the nearest 500.

If that lands somewhere uncomfortable, the number is telling you
`AGENTS.md` is the thing to trim; index-only memory cannot fix an
instructions file that is itself the budget.

The cap is not decoration: `measure_memory.sh` reports every total against
it, `--check` exits non-zero past it (step 6), and the `SessionStart` hook
nudges when a session would start over budget.

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

### 4. Gitignore the sidecar (and the hook's lockfile)

```bash
cat >> .gitignore <<'EOF'
.workspace/memory/.index_state.json
.workspace/memory/.index_state.lock
EOF
git add .gitignore .workspace/memory/MEMORY_INDEX.md
git commit -m "feat(memory): adopt index-first auto-load (γ)"
```

The PreToolUse hook creates `.index_state.lock` as an fcntl lockfile
when capturing references concurrently. Neither file belongs in source
control — `.index_state.json` is runtime state, `.index_state.lock` is
machine-local synchronization.

### 5. Verify

```bash
bash "$BIN/verify_index.sh"           # entries complete + @-include target correct
bash "$BIN/measure_memory.sh" --check # total under cap (exit 1 if not)
python3 "$BIN/memory_review.py"       # human-readable index summary
```

All three should exit 0. `verify_index.sh` is the one that catches a
half-applied migration: if step 3 was skipped it fails with
`<file> is @-included directly by AGENTS.md/CLAUDE.md`, which is otherwise
invisible — the index exists and looks authoritative while every memory
file still loads in full.

Start a fresh `claude` / `codex` session; you should see the reduced
auto-load total.

### 6. Gate it in pre-commit

Steps 1-5 are reversible by a single edit to `AGENTS.md`, and nothing
notices. Wire the two checks into `.pre-commit-config.yaml` so a
regression fails the commit that causes it:

```yaml
repos:
  - repo: local
    hooks:
      - id: memory-index
        name: Memory index integrity + @-include target
        entry: bash -c 'bash "$HOME/agents/coding/plugins/memory/bin/verify_index.sh" --quiet'
        language: system
        files: ^(AGENTS\.md|CLAUDE\.md|\.workspace/memory/.*\.md)$
        pass_filenames: false
      - id: memory-budget
        name: Auto-loaded memory within cap
        entry: bash -c 'bash "$HOME/agents/coding/plugins/memory/bin/measure_memory.sh" --check'
        language: system
        files: ^(AGENTS\.md|CLAUDE\.md|\.workspace/memory/.*\.md)$
        pass_filenames: false
```

Then `pre-commit install`. Both hooks only run when a file that can move
the number changes. This is the same shape as an `mdtoken`-style markdown
budget, applied to the files the memory plugin owns.

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
`transition`) is enabled, at either the user or the project level —
`scripts/enable.sh memory transition` from the marketplace root does it
at the user level. The plugins' `hooks/hooks.json` manifests register
themselves automatically once the plugin is enabled. Enablement is read
at session start, so restart after changing it.

**verify_index.sh warns that `tokens` is stale.** The size field stopped
tracking the file. Re-run `bash "$BIN/memory_init_index.sh"` — it
recomputes tokens and preserves statuses and anchors.

**Cap creep.** Run `python3 "$BIN/memory_review.py"` — if `Auto-loaded`
keeps climbing toward the cap, the index is gaining entries. Run
`/memory-gc` to demote stale ones, or split the index across multiple
files (γ has no requirement that it's a single document).

**A memory file is active, correct, and enormous.** `/memory-gc` will
never flag it: its unit is the whole entry and its signal is
`last_referenced`, so intra-file growth is invisible to it. Set a budget
and trim:

```yaml
---
auto_loaded_cap: 3500
default_file_cap: 2500     # applies to every entry without its own cap
---

## project_state.md
- status: active
- tokens: 8200
- cap: 4000                # this one entry gets more room
```

`verify_index.sh` then warns on any entry over its cap. The trim: keep
the conclusion and a pointer in the memory file, move the cut text
verbatim to a sibling `<name>_archive.md`. Index the archive like any
other memory file — it costs nothing per session, since only the index is
`@`-included and every memory file is read on demand regardless of size.

The growth usually has a cause worth fixing at the same time. Two
recurring ones: an `AGENTS.md` convention that says to log changes in a
new dated block (append-only files only grow), and mirroring `/handoff`
detail into the state file (the state file should carry the conclusion
and a pointer, not a copy of the handoff).

## Reverting

`γ` is additive. To revert, restore the original `@-include` lines in
`AGENTS.md`. The `MEMORY_INDEX.md` file remains harmless on disk; the
sidecar is gitignored so dropping it leaves no trace.
