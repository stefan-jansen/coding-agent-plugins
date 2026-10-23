#!/bin/bash
# PreCompact hook: add custom instructions for the compact summary.
#
# Stdout reaches the compaction summarizer (verified 2026-10-23 with a canary
# line that appeared in compact_summary). The stale-/memory-gc nudge was removed:
# the memory plugin's SessionStart hook already reports it every session.
#
# Exit 0: stdout appended as custom compact instructions
# Exit 2: block compaction (not used here)

cat << 'EOF'
Write the summary as a cold-startable handoff for the next agent, following the
same discipline as the `/handoff` skill (workflow plugin) — same target, so the
auto summary and a manual handoff read alike. Curate, do not transcribe.

Include: current task + status (done / in progress / next); key decisions and
their rationale; exact file paths touched and what changed in each; verification
state (tested / run / pushed vs pending, with evidence); open threads, blockers,
and anything waiting on the user.

Do NOT include (this is where auto-summaries bloat):
- Verbatim or message-by-message replay of the conversation.
- Routine tool mechanics — permission denials, retries, keystrokes, shell
  quoting, dead ends that were resolved and left no lasting state.
- Anything the next agent would re-derive from one `git log` / `gh issue list`,
  or that is already captured in "current state".

Terse but complete beats exhaustive. If a fact would not change what the next
agent does, leave it out.
EOF

exit 0
