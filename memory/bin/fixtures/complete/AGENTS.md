# Complete fixture project

A well-formed γ-shaped project: `AGENTS.md` auto-loads only the memory index, so
the auto-loaded payload stays O(index size). Every memory file has an index
entry, every anchor resolves against this tree, and the auto-loaded total is well
under the cap.

@.workspace/memory/MEMORY_INDEX.md
