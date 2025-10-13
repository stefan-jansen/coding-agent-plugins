---
description: "Display project status and progress metrics"
argument-hint: "[--detailed] [--json]"
allowed-tools: [Read, Bash]
---

# Status Command

Display comprehensive project status including chapter progress, word counts, and active work using the manifest operations system.

## Check Project Status

First, validate and read the project manifest using manifest operations:

```bash
MANIFEST_FILE=".claude/book/manifest.json"
MANIFEST_OPS=".claude/book/manifest_ops.py"

# Check for JSON output mode
JSON_MODE=false
if [[ "$ARGUMENTS" == *"--json"* ]]; then
    JSON_MODE=true
fi

# Validate manifest first
if ! python3 "$MANIFEST_OPS" validate >/dev/null 2>&1; then
    echo "❌ Invalid or missing project manifest. Initialize project first."
    exit 1
fi

# Get basic status report from manifest operations
if [ "$JSON_MODE" = true ]; then
    # Output raw JSON for programmatic use
    cat "$MANIFEST_FILE"
    exit 0
fi

# Parse manifest data
PROJECT_TITLE=$(jq -r '.project.title' "$MANIFEST_FILE")
TARGET_WORDS=$(jq -r '.project.target_words' "$MANIFEST_FILE")
CURRENT_WORDS=$(jq -r '.project.current_words' "$MANIFEST_FILE")
STATUS=$(jq -r '.project.status' "$MANIFEST_FILE")
VERSION=$(jq -r '.project.version' "$MANIFEST_FILE")
AUTHORS=$(jq -r '.project.authors | join(", ")' "$MANIFEST_FILE" 2>/dev/null || echo "Not specified")
TARGET_DATE=$(jq -r '.project.target_completion' "$MANIFEST_FILE")

# Calculate progress with decimal precision
if [ "$TARGET_WORDS" -gt 0 ]; then
    PROGRESS=$(echo "scale=1; $CURRENT_WORDS * 100 / $TARGET_WORDS" | bc 2>/dev/null || echo "0")
else
    PROGRESS="0.0"
fi

# Create progress bar
PROGRESS_INT=${PROGRESS%.*}
PROGRESS_BLOCKS=$((PROGRESS_INT / 5))
PROGRESS_BAR=""
for ((i=0; i<20; i++)); do
    if [ $i -lt $PROGRESS_BLOCKS ]; then
        PROGRESS_BAR="${PROGRESS_BAR}█"
    else
        PROGRESS_BAR="${PROGRESS_BAR}░"
    fi
done

# Display header
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                   📚 PROJECT STATUS                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📖 Title: $PROJECT_TITLE"
echo "👥 Authors: $AUTHORS"
echo "🏷️  Version: $VERSION"
echo "📊 Status: ${STATUS//_/ }" | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1'
echo "🎯 Target: $(date -d "$TARGET_DATE" "+%B %d, %Y" 2>/dev/null || echo "$TARGET_DATE")"
echo ""
echo "📝 Word Count Progress:"
echo "   $PROGRESS_BAR $PROGRESS%"
printf "   %'d / %'d words\n" "$CURRENT_WORDS" "$TARGET_WORDS"
echo ""
```

## Chapter Status

```bash
# Display chapter information with better formatting
echo "📖 Chapter Overview:"
echo "┌────┬──────────────────────────────────┬────────────┬──────────────┐"
echo "│ ID │ Title                            │ Status     │ Progress     │"
echo "├────┼──────────────────────────────────┼────────────┼──────────────┤"

# Process each chapter
jq -r '.chapters | to_entries[] | [.key, .value.title, .value.status, .value.word_count, .value.target_words] | @tsv' "$MANIFEST_FILE" | 
while IFS=$'\t' read -r id title status words target; do
    # Truncate title if too long
    if [ ${#title} -gt 32 ]; then
        title="${title:0:29}..."
    fi
    
    # Format status for display
    display_status="${status//_/ }"
    
    # Calculate chapter progress
    if [ "$target" -gt 0 ] 2>/dev/null; then
        ch_progress=$((words * 100 / target))
    else
        ch_progress=0
    fi
    
    # Color coding for status
    case "$status" in
        "not_started") status_icon="⚪" ;;
        "research")    status_icon="🔬" ;;
        "outlined")    status_icon="📋" ;;
        "drafting")    status_icon="✏️" ;;
        "drafted")     status_icon="📄" ;;
        "review")      status_icon="👁️" ;;
        "revision")    status_icon="🔄" ;;
        "final")       status_icon="✅" ;;
        "published")   status_icon="🎉" ;;
        *)             status_icon="❓" ;;
    esac
    
    printf "│ %3s │ %-32s │ %s %-9s │ %5d/%5d │\n" \
        "$id" "$title" "$status_icon" "$display_status" "$words" "$target"
done

echo "└────┴──────────────────────────────────┴────────────┴──────────────┘"
echo ""

# Summary statistics
TOTAL_CHAPTERS=$(jq '.chapters | length' "$MANIFEST_FILE")
COMPLETED_CHAPTERS=$(jq '[.chapters[] | select(.status == "final" or .status == "published")] | length' "$MANIFEST_FILE")
IN_PROGRESS=$(jq '[.chapters[] | select(.status != "not_started" and .status != "final" and .status != "published")] | length' "$MANIFEST_FILE")

echo "📊 Chapter Statistics:"
echo "   Total: $TOTAL_CHAPTERS | Completed: $COMPLETED_CHAPTERS | In Progress: $IN_PROGRESS"
echo ""
```

## Active Work

```bash
# Check for active work units
WORK_DIR=".claude/work/current"
if [ -d "$WORK_DIR" ] && [ -f "$WORK_DIR/ACTIVE_WORK" ]; then
    ACTIVE_ID=$(cat "$WORK_DIR/ACTIVE_WORK")
    ACTIVE_DIR=$(find "$WORK_DIR" -maxdepth 1 -type d -name "${ACTIVE_ID}_*" 2>/dev/null | head -1)
    
    if [ -n "$ACTIVE_DIR" ] && [ -f "$ACTIVE_DIR/state.json" ]; then
        echo "🔨 Active Work Unit:"
        WORK_NAME=$(basename "$ACTIVE_DIR")
        COMPLETED=$(jq -r '.completed_tasks | length' "$ACTIVE_DIR/state.json")
        TOTAL=$(jq -r '.tasks | length' "$ACTIVE_DIR/state.json")
        CURRENT=$(jq -r '.current_task // "none"' "$ACTIVE_DIR/state.json")
        
        echo "  $WORK_NAME"
        echo "  Progress: $COMPLETED/$TOTAL tasks complete"
        echo "  Current task: $CURRENT"
        echo ""
    fi
fi
```

## Research and Code Statistics

```bash
# Update metrics first
python3 "$MANIFEST_OPS" update_metrics >/dev/null 2>&1

# Get research statistics from manifest
SOURCES_COUNT=$(jq -r '.research.sources_count' "$MANIFEST_FILE")
NOTEBOOKS_COUNT=$(jq -r '.code.notebooks_count' "$MANIFEST_FILE")
EXAMPLES_COUNT=$(jq -r '.code.examples_count' "$MANIFEST_FILE")
TEST_COVERAGE=$(jq -r '.code.test_coverage' "$MANIFEST_FILE")

echo "🔬 Research & Development:"
echo "┌─────────────────────────────────────────────┐"
printf "│ 📚 Research Sources:     %4d papers        │\n" "$SOURCES_COUNT"
printf "│ 📓 Jupyter Notebooks:    %4d files         │\n" "$NOTEBOOKS_COUNT"
printf "│ 💻 Code Examples:        %4d files         │\n" "$EXAMPLES_COUNT"
if [ "$TEST_COVERAGE" != "0" ] && [ "$TEST_COVERAGE" != "null" ]; then
    printf "│ 🧪 Test Coverage:        %4.1f%%             │\n" "$TEST_COVERAGE"
fi
echo "└─────────────────────────────────────────────┘"
echo ""

# Check researcher integration
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/health" 2>/dev/null | grep -q "200"; then
    echo "✅ Researcher Agent: Connected"
else
    echo "⚠️  Researcher Agent: Not available (start with: cd ~/agents/researcher && python run_api_server.py)"
fi
echo ""
```

## Recent Activity

```bash
# Show recent Git commits
echo "📅 Recent Activity:"
git log --oneline --graph --decorate -5 2>/dev/null || echo "  No Git history available"
echo ""
```

## Quality Metrics

```bash
echo "✅ Quality Metrics:"

# Check if any tests exist
if [ -d "tests" ]; then
    TEST_COUNT=$(find tests -name "test_*.py" 2>/dev/null | wc -l)
    echo "  Test files: $TEST_COUNT"
fi

# Check documentation
DOC_COUNT=$(find . -name "*.md" -not -path "./.git/*" 2>/dev/null | wc -l)
echo "  Documentation files: $DOC_COUNT"

# Check code coverage if available
if [ -f ".coverage" ]; then
    echo "  Code coverage: Available"
fi

echo ""
```

## Arguments Processing

Handle optional arguments for detailed view:

```bash
# Check for --detailed flag
if [[ "$ARGUMENTS" == *"--detailed"* ]]; then
    echo "📋 Detailed Chapter Information:"
    echo "═══════════════════════════════════════════════════════════════"
    
    # Show all chapter details with better formatting
    jq -r '.chapters | to_entries[] | 
        "\n📖 Chapter \(.key): \(.value.title)\n" +
        "───────────────────────────────────────────────────────────\n" +
        "  Status: \(.value.status | gsub("_"; " ") | ascii_upcase)\n" +
        "  Progress: \(.value.word_count) / \(.value.target_words) words\n" +
        "  Last Modified: \(.value.last_modified // "Never")\n" +
        "\n  📁 Files:\n" +
        "    • Outline: \(.value.files.outline // "❌ Not created")\n" +
        "    • Draft:   \(.value.files.draft // "❌ Not created")\n" +
        "    • Review:  \(.value.files.review // "❌ Not created")\n" +
        "    • Final:   \(.value.files.final // "❌ Not created")\n" +
        "\n  📓 Notebooks: \(.value.notebooks | length) files" +
        if .value.notebooks | length > 0 then
            "\n    " + (.value.notebooks | join("\n    "))
        else "" end +
        if .value.sections then
            "\n\n  📝 Sections:\n" + 
            (.value.sections | to_entries[] | "    • \(.key): \(.value.status) (\(.value.word_count) words)" | tostring)
        else "" end' "$MANIFEST_FILE"
    
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
fi
```

## Summary

Provide actionable next steps based on intelligent analysis:

```bash
echo "💡 Intelligent Next Steps:"
echo "───────────────────────────────────────"

# Use manifest operations to get next chapter for various actions
NEXT_RESEARCH=$(python3 -c "
import sys
sys.path.append('.claude/book')
from manifest_ops import ManifestOperations
ops = ManifestOperations()
ch = ops.get_next_chapter('research')
if ch: print(f\"{ch['id']}: {ch['title']}\")
" 2>/dev/null)

NEXT_OUTLINE=$(python3 -c "
import sys
sys.path.append('.claude/book')
from manifest_ops import ManifestOperations
ops = ManifestOperations()
ch = ops.get_next_chapter('outline')
if ch: print(f\"{ch['id']}: {ch['title']}\")
" 2>/dev/null)

NEXT_WRITE=$(python3 -c "
import sys
sys.path.append('.claude/book')
from manifest_ops import ManifestOperations
ops = ManifestOperations()
ch = ops.get_next_chapter('write')
if ch: print(f\"{ch['id']}: {ch['title']}\")
" 2>/dev/null)

NEXT_REVIEW=$(python3 -c "
import sys
sys.path.append('.claude/book')
from manifest_ops import ManifestOperations
ops = ManifestOperations()
ch = ops.get_next_chapter('review')
if ch: print(f\"{ch['id']}: {ch['title']}\")
" 2>/dev/null)

# Provide specific recommendations
if [ -n "$NEXT_RESEARCH" ]; then
    echo "  📚 Research: Chapter $NEXT_RESEARCH"
    echo "     Command: /research \"[topic]\" --chapter ${NEXT_RESEARCH:0:3}"
fi

if [ -n "$NEXT_OUTLINE" ]; then
    echo "  📋 Outline: Chapter $NEXT_OUTLINE"
    echo "     Command: /outline --chapter ${NEXT_OUTLINE:0:3}"
fi

if [ -n "$NEXT_WRITE" ]; then
    echo "  ✏️  Write: Chapter $NEXT_WRITE"
    echo "     Command: /write --chapter ${NEXT_WRITE:0:3} --section [name]"
fi

if [ -n "$NEXT_REVIEW" ]; then
    echo "  👁️  Review: Chapter $NEXT_REVIEW"
    echo "     Command: /review --chapter ${NEXT_REVIEW:0:3}"
fi

# Calculate estimated time to completion
WORDS_REMAINING=$((TARGET_WORDS - CURRENT_WORDS))
if [ "$WORDS_REMAINING" -gt 0 ]; then
    # Assume 500 words per day average writing speed
    DAYS_TO_COMPLETE=$((WORDS_REMAINING / 500))
    echo ""
    echo "⏱️  Estimated Time to Completion:"
    echo "   $WORDS_REMAINING words remaining"
    echo "   ~$DAYS_TO_COMPLETE days at 500 words/day"
fi

echo ""
echo "📌 Quick Commands:"
echo "   /help          - Show all commands"
echo "   /status --json - Get JSON output for scripts"
echo "   /work          - Manage work units"
```

## Final Summary

```bash
# Show last update time
LAST_UPDATED=$(jq -r '.metadata.last_updated' "$MANIFEST_FILE")
FRAMEWORK_VERSION=$(jq -r '.metadata.framework_version' "$MANIFEST_FILE")

echo ""
echo "───────────────────────────────────────"
echo "Last Updated: $(date -d "$LAST_UPDATED" "+%B %d, %Y at %H:%M" 2>/dev/null || echo "$LAST_UPDATED")"
echo "Framework Version: $FRAMEWORK_VERSION"
```

---

## Command Options

- `/status` - Basic project overview
- `/status --detailed` - Comprehensive chapter information
- `/status --json` - JSON output for programmatic use

*Your co-authoring command center for book production tracking*