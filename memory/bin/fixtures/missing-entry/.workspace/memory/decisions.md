## 2026-05-15: index-only auto-load
**Why**: Full-file @-includes cost ~10-13K tokens at session start.
**Trade-off**: Index needs maintenance; offset by signal-driven GC.

<!-- This file exists but is deliberately NOT listed in MEMORY_INDEX.md. -->
