# Oversized-file fixture project

This project regressed to full-file auto-loading: `AGENTS.md` @-includes the index
**and** the bloated `lessons_learned.md` directly, so the auto-loaded total blows
past `auto_loaded_cap` (5000). `measure_memory.sh --total-only` must report a total
greater than the cap, which is the signal an index-only refactor is overdue.

@.workspace/memory/MEMORY_INDEX.md
@.workspace/memory/lessons_learned.md
