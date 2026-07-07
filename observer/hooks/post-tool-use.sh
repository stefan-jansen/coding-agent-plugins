#!/bin/bash
# Observer: Buffer tool observations to JSONL
# PostToolUse hook — must be fast and non-blocking
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/../scripts/buffer.py" 2>/dev/null
exit 0
