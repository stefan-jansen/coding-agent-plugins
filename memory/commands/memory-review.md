---
title: memory-review
aliases: [/memory-review]
description: Display current memory state with timestamps, sizes, and staleness indicators
---

# Memory Review

Display comprehensive view of current memory state to support active memory maintenance.

## What This Command Does

Show current memory files with metadata to help identify what needs updating, removing, or relocating.

```bash
#!/bin/bash

# Constants
MEMORY_DIR=".claude/memory"
DOCUMENTATION_DIR=".claude/documentation"
STALENESS_THRESHOLD=30
SIZE_LIMIT=5120
CURRENT_DATE=$(date +%Y-%m-%d)

# Check if memory directory exists
if [[ ! -d "$MEMORY_DIR" ]]; then
    echo "❌ No memory directory found at $MEMORY_DIR"
    echo "💡 Run /memory-update to create initial memory structure"
    exit 1
fi

echo "Memory Review - $CURRENT_DATE"
echo ""

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

# Analyze memory files
echo "📁 Memory Files ($MEMORY_DIR/):"

total_size=0
fresh_count=0
stale_count=0
oversized_count=0
file_count=0

for file in "$MEMORY_DIR"/*.md; do
    if [[ -f "$file" ]]; then
        filename=$(basename "$file")
        size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
        size_human=$(numfmt --to=iec-i --suffix=B $size 2>/dev/null || echo "${size} bytes")

        # Extract last validated date
        last_validated=$(grep -oP "Last (validated|updated).*?(\d{4}-\d{2}-\d{2})" "$file" | tail -1 | grep -oP "\d{4}-\d{2}-\d{2}" || echo "N/A")

        status="✅"
        note=""

        # Check staleness
        if [[ "$last_validated" != "N/A" ]]; then
            days=$(days_since "$last_validated")
            if [[ $days -gt $STALENESS_THRESHOLD ]]; then
                status="🔴"
                note="(Stale: $days days)"
                stale_count=$((stale_count + 1))
            elif [[ $days -gt 7 ]]; then
                status="⚠️"
                note="(Aging: $days days)"
                stale_count=$((stale_count + 1))
            else
                note="(Fresh)"
                fresh_count=$((fresh_count + 1))
            fi
        else
            status="⚠️"
            note="(No timestamp)"
            stale_count=$((stale_count + 1))
        fi

        # Check size
        if [[ $size -gt $SIZE_LIMIT ]]; then
            status="⚠️"
            note="$note (Oversized: >5KB)"
            oversized_count=$((oversized_count + 1))
        fi

        printf "  %s %-25s %-12s %-20s %s\n" "$status" "$filename" "$size_human" "$last_validated" "$note"

        total_size=$((total_size + size))
        file_count=$((file_count + 1))
    fi
done

echo ""

# Analyze documentation files
if [[ -d "$DOCUMENTATION_DIR" ]]; then
    echo "📁 Documentation Files ($DOCUMENTATION_DIR/):"
    for file in "$DOCUMENTATION_DIR"/*.md; do
        if [[ -f "$file" ]]; then
            filename=$(basename "$file")
            size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
            size_human=$(numfmt --to=iec-i --suffix=B $size 2>/dev/null || echo "${size} bytes")
            created=$(date -r "$file" +%Y-%m-%d 2>/dev/null || stat -f "%Sm" -t "%Y-%m-%d" "$file" 2>/dev/null || echo "Unknown")
            printf "  ✅ %-25s %-12s Created: %s\n" "$filename" "$size_human" "$created"
        fi
    done
    echo ""
fi

# Summary
total_size_human=$(numfmt --to=iec-i --suffix=B $total_size 2>/dev/null || echo "${total_size} bytes")

echo "📊 Summary:"
echo "  Total memory: $total_size_human ($file_count files)"
echo "  Fresh: $fresh_count files (validated <7 days)"
echo "  Stale: $stale_count files (validated >7 days or no timestamp)"
echo "  Oversized: $oversized_count files (>5KB)"
echo ""

# Recommendations
if [[ $stale_count -gt 0 ]] || [[ $oversized_count -gt 0 ]]; then
    echo "⚠️  Actions Recommended:"
    if [[ $stale_count -gt 0 ]]; then
        echo "  - Review stale files with /memory-update"
        echo "  - Run /memory-gc to clean up stale content"
    fi
    if [[ $oversized_count -gt 0 ]]; then
        echo "  - Split oversized files into smaller modules"
    fi
else
    echo "✅ Memory health: Good"
    echo "   All files are fresh, properly sized, and timestamped"
fi

echo ""
echo "💡 Next steps:"
echo "   - /memory-update  : Update or add memory entries"
echo "   - /memory-gc      : Clean up stale content"
echo "   - /status         : Check overall project health"
```

## Integration

**Called by**: `/status`, `/ship`
**Related**: `/memory-update`, `/memory-gc`

---

**Plugin**: claude-code-memory v1.0.0
**Status**: ✅ Implemented and tested
