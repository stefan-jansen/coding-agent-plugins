# Broken-anchor fixture project

Every memory file has an index entry, but `project_state.md`'s anchor list points
at `src/removed.py`, which does not exist in this tree (the other anchors,
`src/auth.py` and `src/db.py`, do). `check_anchors.sh` must report `missing` for
`src/removed.py` and `present` for the rest.

@.workspace/memory/MEMORY_INDEX.md
