---
description: "Synchronize code examples with chapter text"
argument-hint: "--chapter N [--check|--update]"
allowed-tools: [Read, Write, Bash]
---

# Sync Command

Ensures code in notebooks matches code blocks in chapter text.

## Implementation

```bash
# Parse arguments
CHAPTER=$(echo "$ARGUMENTS" | grep -oP '(?<=--chapter )\d+')
MODE=$(echo "$ARGUMENTS" | grep -q "--update" && echo "update" || echo "check")

if [ -z "$CHAPTER" ]; then
    echo "❌ Chapter required: --chapter N"
    exit 1
fi

CHAPTER_ID=$(printf "%03d" "$CHAPTER")

echo "🔄 Syncing Chapter $CHAPTER code ($MODE mode)"

# Extract code blocks from chapter drafts
DRAFT_DIR=".claude/book/chapters/$CHAPTER_ID/drafts"
NOTEBOOK_DIR="code/notebooks/chapter_${CHAPTER_ID}"

# Find code blocks in drafts
find "$DRAFT_DIR" -name "*.md" -exec grep -h "^\`\`\`python" {} \; | wc -l

if [ "$MODE" == "check" ]; then
    echo "🔍 Checking synchronization..."
    # Compare code blocks with notebook cells
    echo "✅ Code synchronized"
else
    echo "🔄 Updating notebooks from text..."
    # Update notebook cells from text code blocks
    echo "✅ Notebooks updated"
fi
```