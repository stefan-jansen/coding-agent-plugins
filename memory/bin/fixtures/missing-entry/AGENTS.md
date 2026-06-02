# Missing-entry fixture project

Identical to `complete/`, except `decisions.md` exists on disk but has **no entry**
in `MEMORY_INDEX.md`. `verify_index.sh` must flag exactly one missing entry
(`decisions.md`) and fail.

@.workspace/memory/MEMORY_INDEX.md
