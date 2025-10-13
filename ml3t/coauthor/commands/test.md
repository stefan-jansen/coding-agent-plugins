---
description: "Validate notebook execution and test code examples"
argument-hint: "[--chapter N] [--notebook name] [--all]"
allowed-tools: [Read, Bash]
---

# Test Command

Tests notebooks and code examples for correctness.

## Implementation

```bash
# Parse arguments
CHAPTER=$(echo "$ARGUMENTS" | grep -oP '(?<=--chapter )\d+')
NOTEBOOK=$(echo "$ARGUMENTS" | grep -oP '(?<=--notebook )\S+')
ALL=$(echo "$ARGUMENTS" | grep -q "--all" && echo "true" || echo "false")

if [ "$ALL" == "true" ]; then
    echo "🧪 Testing all notebooks..."
    find code/notebooks -name "*.ipynb" -exec jupyter nbconvert --to notebook --execute {} \;
    echo "✅ All notebooks tested"
else
    if [ -n "$CHAPTER" ]; then
        CHAPTER_ID=$(printf "%03d" "$CHAPTER")
        NOTEBOOK_DIR="code/notebooks/chapter_${CHAPTER_ID}"
        echo "🧪 Testing chapter $CHAPTER notebooks..."
        find "$NOTEBOOK_DIR" -name "*.ipynb" -exec jupyter nbconvert --to notebook --execute {} \;
    elif [ -n "$NOTEBOOK" ]; then
        echo "🧪 Testing notebook: $NOTEBOOK"
        jupyter nbconvert --to notebook --execute "$NOTEBOOK"
    fi
    echo "✅ Tests complete"
fi
```