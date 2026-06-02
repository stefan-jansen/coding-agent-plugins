# Memory tooling test fixtures

Static project trees consumed by `bin/test_fixtures.sh`. Each fixture is a
self-contained, γ-shaped project (`CLAUDE.md` → `AGENTS.md` → `.workspace/memory/`)
that isolates one scenario the shared `bin/` scripts must handle. They live under
`bin/` (not `test/`) because the repo `.gitignore` excludes `*/test/`.

> These fixtures double as the working interpretation of the index/sidecar
> contract for M1, derived from the durable spec. They are test data, not a
> standalone spec doc — the authoritative format spec ships inside the
> `verify_index.sh` / `check_anchors.sh` PRs. The harness deliberately asserts on
> spec-mandated vocabulary (`present`/`missing`, "0 missing entries") and on
> observable artifacts (exit codes, files created, filenames echoed) rather than
> on incidental output wording, so it stays robust as those scripts land.

## Index / sidecar shape

`.workspace/memory/MEMORY_INDEX.md` — frontmatter carries the per-project
`auto_loaded_cap`; one `### <file>` section per memory file with `status`,
`last_referenced`, `tokens`, and `anchors` fields:

```markdown
---
auto_loaded_cap: 5000
---

### project_state.md
- status: active            # active | dormant | deprecated | superseded-by:<slug>
- last_referenced: 2026-05-28
- tokens: 70
- anchors: src/auth.py, src/db.py   # file paths/commands/symbols; "(none)" => n/a
```

`.workspace/memory/.index_state.json` — gitignored runtime sidecar in real
projects; committed here as fixture data. Holds `last_gc_run`, `auto_loaded_cap`,
and a per-file `last_referenced` / `tokens` map.

## Fixtures

| Fixture | Scenario | Expected signal |
|---|---|---|
| `complete/` | Well-formed: index covers every file, all anchors resolve, auto-load (index only) under cap. | `verify_index` passes; `check_anchors` all `present`; `measure_memory` total < cap. |
| `missing-entry/` | `decisions.md` exists on disk but has no index entry. | `verify_index` flags 1 missing entry (`decisions.md`) and fails. |
| `broken-anchor/` | `project_state.md` anchors `src/removed.py` (absent) plus two present anchors. | `check_anchors` reports `missing` for `src/removed.py`, `present` for the rest. |
| `oversized-file/` | `AGENTS.md` auto-loads a bloated `lessons_learned.md` (~12.5K tokens) directly. | `measure_memory --total-only` > cap (5000). |

## How the harness uses them

`bin/test_fixtures.sh` copies each fixture into a fresh temp dir before running a
script (so `git rev-parse` resolves to the staged copy's absence of a repo and the
script falls back to the project root, never this plugin's repo root). It exercises
all four `bin/` scripts — `measure_memory.sh`, `verify_index.sh`, `check_anchors.sh`,
`memory_init_index.sh` — and **skips** any not yet present, so the run is green while
sibling M1 scripts are still in flight and becomes fully meaningful as they land. It
also generates a 50-file memory tree in a temp dir and asserts each available script
finishes in < 30 s (the proxy available now for the `< 30 s` GC-proposal constraint;
the full GC perf test lands in M4).
