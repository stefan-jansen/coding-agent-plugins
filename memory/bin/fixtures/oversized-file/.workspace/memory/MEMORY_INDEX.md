---
auto_loaded_cap: 5000
---

# Memory Index

`lessons_learned.md` is `active` but oversized — on its own it exceeds the cap, and
`AGENTS.md` auto-loads it directly. This is the current-but-oversized bloat the
budget work targets (the file is not stale; staleness-only GC would never flag it).

### project_state.md
- status: active
- last_referenced: 2026-05-28
- tokens: 70
- anchors: src/app.py

### lessons_learned.md
- status: active
- last_referenced: 2026-05-29
- tokens: 12570
- anchors: (none)
