#!/bin/bash
# PreCompact hook: inject custom instructions for the compact summary
#
# Stdout becomes custom_instructions for the compaction — tells Claude
# what to emphasize in the summary it generates.
#
# Exit 0: stdout appended as custom compact instructions
# Exit 2: block compaction (not used here)

cat << 'EOF'
When compacting this conversation, ensure the summary preserves:
1. Current task and its status (what's done, what's in progress, what's next)
2. Key decisions made and their rationale
3. File paths actively being modified
4. Any errors or blockers encountered and their resolution status
5. Open questions or items waiting on user input
These details are critical for session continuity after compaction.
EOF

exit 0
