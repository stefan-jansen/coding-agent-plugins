---
title: memory-gc
aliases: [/memory-gc]
description: Signal-driven garbage collection for `.workspace/memory/`. Produces a structured diff of proposed status transitions (active↔dormant↔deprecated) from last_referenced + references + anchor health, then applies it transactionally on --execute.
---

# Memory Garbage Collection (γ — index-driven)

`/memory-gc` reads three sources and proposes status transitions in
`MEMORY_INDEX.md`:

| Source | Provides |
|---|---|
| `.workspace/memory/MEMORY_INDEX.md` | Current `status`, `anchors`, `tokens` per entry |
| `.workspace/memory/.index_state.json` | `last_referenced` (per file) + `references` count (per file) + project-level `last_gc_run` |
| `bin/check_anchors.sh` against the working tree | `present` / `missing` / `n/a` per entry's anchors |

Transitions (v0.1 heuristic; LLM-grounded relevance is out of scope):

- `active → dormant` — `last_referenced` older than `--stale` (default 90d)
  and `references == 0`, OR every anchor is `missing`.
- `active → deprecated` — same as above but past `--deprecated` (default 180d).
- `dormant → deprecated` — past 180d with no references.
- `superseded-by:<slug>` — user-owned; never touched by GC.
- `deprecated` — terminal; never demoted further.

The dry-run **writes nothing**. `--execute` applies the diff in one
transaction (atomic `os.replace` of `MEMORY_INDEX.md`) and stamps
`last_gc_run` in `.index_state.json` so the SessionStart nudge stops for
the next 7 days.

## Usage

```bash
/memory-gc                    # default: dry-run, human-readable
/memory-gc --execute          # apply the diff after confirmation
/memory-gc --execute --auto   # apply without confirmation (CI / scripts)
/memory-gc --json             # dry-run, machine-readable
/memory-gc --stale 60         # tune thresholds (defaults: 90/180)
```

## Plan (Claude executes)

When the user invokes `/memory-gc`, run the following — adjust flags from
the user's input:

1. **Locate plugin bin/** — the scripts live at
   `${CLAUDE_PLUGIN_ROOT}/bin/` for the memory plugin. If the user invoked
   without that env var (e.g. via `claude -p`), fall back to
   `~/agents/coding/plugins/memory/bin/`.

2. **Run the dry-run**:
   ```bash
   python3 "$BIN/gc_propose.py" --json > /tmp/gc-diff.json
   python3 "$BIN/gc_propose.py"      # human-readable summary
   ```
   Show the human-readable summary to the user. If `--json` was passed,
   emit the JSON file path so it can be piped.

3. **Decide based on flags**:
   - No `--execute`: stop here.
   - `--execute` without `--auto`: ask the user to confirm "Apply N
     transitions to MEMORY_INDEX.md? (y/N)". Abort on anything but `y`.
   - `--execute --auto`: skip confirmation.

4. **Apply**:
   ```bash
   python3 "$BIN/gc_apply.py" --diff /tmp/gc-diff.json --memory-dir "<resolved>/.workspace/memory"
   ```
   The script writes `MEMORY_INDEX.md` atomically and stamps `last_gc_run`
   in the sidecar. On status drift (the index changed between dry-run and
   apply), it exits 1 with conflict details — re-run the dry-run to get a
   fresh diff, or pass `--force` to apply the original diff anyway.

5. **Summarize** for the user:
   - How many transitions applied.
   - That `last_gc_run` advanced (so the SessionStart nudge resets).
   - That a re-run dry-run is now empty (good check for criterion 5).

## Constraints (from the spec)

- **<30s** on ≤50 memory files. Verified by `bin/test_gc.sh`.
- **No partial application**: the index is rewritten as a single
  `os.replace`. Either all transitions land or none do.
- **MCP-optional**: if Serena is available, future versions can produce
  smarter section-aware diffs; absent it, we fall back to whole-file
  status proposals (current behavior). No hard MCP dependency.
- **Sidecar contract preserved**: only `last_gc_run` is touched on apply;
  per-file `last_referenced` / `references` are owned by the PreToolUse
  hook and never reset by GC.

## Troubleshooting

**"no MEMORY_INDEX.md"**: run `bash $BIN/memory_init_index.sh` first.

**"conflict: status drift"**: the index changed between dry-run and apply
(another agent wrote to it, or the user edited manually). Re-run the
dry-run for a fresh diff, or pass `--force` to apply the original diff.

**Diff looks too aggressive**: tune with `--stale N --deprecated M`. The
defaults (90d/180d) are conservative for code projects where memory
naturally turns over on quarterly cadence.

**Transitions touch a file that's actively used**: the hook isn't firing.
Verify the memory plugin is enabled and `.index_state.json` is being
updated on Read. See `bin/test_hooks.sh` for the reference behavior.
