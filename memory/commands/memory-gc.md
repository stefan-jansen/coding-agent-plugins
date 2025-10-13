---
title: memory-gc
aliases: [/memory-gc]
description: Garbage collection for stale memory entries - identify and clean up obsolete content
---

# Memory Garbage Collection

Systematic cleanup of stale, obsolete, or incorrect memory entries.

## Philosophy: Removal Without Guilt

Memory should reflect CURRENT reality, not history. Remove entries proven wrong, superseded, or obsolete. Archive if historical value exists.

```bash
#!/bin/bash

# Constants
MEMORY_DIR=".claude/memory"
ARCHIVE_DIR=".claude/work/archives/memory"
CURRENT_DATE=$(date +%Y-%m-%d)
STALENESS_THRESHOLD=30

echo "Memory Garbage Collection - $CURRENT_DATE"
echo ""

# Check if memory directory exists
if [[ ! -d "$MEMORY_DIR" ]]; then
    echo "❌ No memory directory found at $MEMORY_DIR"
    exit 1
fi

# Function to calculate days since date
days_since() {
    local date_str=$1
    if [[ -z "$date_str" ]] || [[ "$date_str" == "N/A" ]]; then
        echo "999"
        return
    fi
    local date_epoch=$(date -d "$date_str" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$date_str" "+%s" 2>/dev/null || echo 0)
    local current_epoch=$(date +%s)
    local diff_days=$(( (current_epoch - date_epoch) / 86400 ))
    echo $diff_days
}

# Step 1: Identify stale files
echo "📋 Step 1: Identify Stale Files"
echo "--------------------------------"
echo ""

stale_files=()

for file in "$MEMORY_DIR"/*.md; do
    if [[ ! -f "$file" ]]; then
        continue
    fi

    filename=$(basename "$file")
    last_validated=$(grep -oP "Last (validated|updated).*?(\d{4}-\d{2}-\d{2})" "$file" | tail -1 | grep -oP "\d{4}-\d{2}-\d{2}" || echo "")

    if [[ -z "$last_validated" ]]; then
        echo "⚠️  $filename - No timestamp found"
        stale_files+=("$filename")
    else
        days=$(days_since "$last_validated")
        if [[ $days -gt $STALENESS_THRESHOLD ]]; then
            echo "🔴 $filename - Stale ($days days since validation)"
            stale_files+=("$filename")
        else
            echo "✅ $filename - Fresh ($days days)"
        fi
    fi
done

echo ""

# Step 2: Review stale entries
if [[ ${#stale_files[@]} -eq 0 ]]; then
    echo "✅ No stale files found!"
    echo "   All memory entries are fresh (<$STALENESS_THRESHOLD days)"
    echo ""
    exit 0
fi

echo "📝 Step 2: Review Stale Content"
echo "--------------------------------"
echo ""
echo "Found ${#stale_files[@]} stale file(s) to review"
echo ""

# Interactive review
for filename in "${stale_files[@]}"; do
    file="$MEMORY_DIR/$filename"

    echo "Reviewing: $filename"
    echo "---"
    echo ""

    # Show file summary
    echo "First 20 lines:"
    head -20 "$file"
    echo ""
    echo "[... file continues ...]"
    echo ""

    # Ask what to do
    echo "Actions:"
    echo "  1) Keep and update timestamp (content still valid)"
    echo "  2) Archive (historical value but not current)"
    echo "  3) Delete (incorrect or obsolete)"
    echo "  4) Skip (review later)"
    echo ""
    read -p "Choice [1-4]: " choice

    case $choice in
        1)
            # Update timestamp
            if grep -q "Last validated:" "$file"; then
                sed -i "s/Last validated:.*$/Last validated: $CURRENT_DATE/" "$file"
            elif grep -q "Last updated:" "$file"; then
                sed -i "s/Last updated:.*$/Last updated: $CURRENT_DATE/" "$file"
            else
                sed -i "2i\\**Last validated**: $CURRENT_DATE\\n" "$file"
            fi
            echo "✅ Timestamp updated"
            echo ""
            ;;

        2)
            # Archive
            mkdir -p "$ARCHIVE_DIR"
            archive_name="${filename%.md}_${CURRENT_DATE}.md"
            mv "$file" "$ARCHIVE_DIR/$archive_name"
            echo "📦 Archived to $ARCHIVE_DIR/$archive_name"
            echo ""
            ;;

        3)
            # Delete
            read -p "⚠️  Confirm deletion of $filename [y/N]: " confirm
            if [[ "$confirm" == "y" ]]; then
                rm "$file"
                echo "🗑️  Deleted"
            else
                echo "⏭️  Skipped deletion"
            fi
            echo ""
            ;;

        4)
            echo "⏭️  Skipped"
            echo ""
            ;;

        *)
            echo "❌ Invalid choice, skipping"
            echo ""
            ;;
    esac
done

# Summary
echo "📈 Step 3: Garbage Collection Summary"
echo "--------------------------------------"
echo ""

remaining_files=$(find "$MEMORY_DIR" -name "*.md" -type f | wc -l)
total_size=$(du -sh "$MEMORY_DIR" 2>/dev/null | cut -f1)

echo "Memory state after GC:"
echo "  - Files remaining: $remaining_files"
echo "  - Total size: $total_size"
echo ""

if [[ -d "$ARCHIVE_DIR" ]]; then
    archived_count=$(find "$ARCHIVE_DIR" -name "*.md" -type f 2>/dev/null | wc -l)
    echo "  - Archived entries: $archived_count"
    echo ""
fi

echo "✅ Garbage collection complete"
echo ""
echo "💡 Next steps:"
echo "   - Run /memory-review to verify state"
echo "   - Run /memory-update to add new learnings"
echo "   - Schedule next GC in ~30 days"
```

## Integration

**Called by**: `/status` (warn if >30 days), Manual execution
**Related**: `/memory-review`, `/memory-update`

---

**Plugin**: claude-code-memory v1.0.0
**Status**: ✅ Implemented and tested
