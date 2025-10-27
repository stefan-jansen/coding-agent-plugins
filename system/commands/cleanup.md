---
title: cleanup
aliases: [housekeeping, organize, tidy, clean]
description: Clean up Claude-generated clutter and consolidate documentation
allowed-tools: [Bash, Read, Write, Glob, MultiEdit]
argument-hint: "[--dry-run | --auto | root | tests | reports | work | all]"
---

# Smart Project Cleanup

I'll clean up the real clutter that accumulates during Claude development sessions, with intelligent consolidation of .md reports into README or work units.

**Arguments**: $ARGUMENTS

## Usage Examples

```bash
/cleanup reports         # Consolidate .md reports (your frequent request)
/cleanup reports --auto  # Auto-consolidate without prompts
/cleanup --dry-run       # Preview what would be cleaned
/cleanup all             # Full cleanup including reports
```

## Phase 1: Identify Cleanup Mode

```bash
# Parse arguments
MODE="${ARGUMENTS:-interactive}"
DRY_RUN=false
AUTO=false

case "$MODE" in
    --dry-run)
        DRY_RUN=true
        echo "🔍 DRY RUN MODE - Will show what would be cleaned"
        ;;
    --auto)
        AUTO=true
        echo "🤖 AUTO MODE - Will clean without prompts"
        ;;
    root)
        echo "🏠 Cleaning root directory clutter"
        ;;
    tests)
        echo "🧪 Cleaning test files outside tests/"
        ;;
    reports)
        echo "📝 Consolidating .md reports into README/work units"
        ;;
    work)
        echo "💼 Cleaning .claude/work directory"
        ;;
    all|"")
        echo "🧹 Full cleanup - all categories"
        MODE="all"
        ;;
    *)
        echo "📊 Interactive mode - will ask about each file"
        ;;
esac
```

## Phase 2: Scan for Claude Clutter

I'll identify the real problems that accumulate during Claude sessions:

### 1. Root Directory Clutter
Files that don't belong in the root:
- Random `.md` files (not README/CHANGELOG/CLAUDE)
- One-off shell scripts (`setup_*.sh`, `test_*.sh`, `debug_*.sh`)
- Misplaced config files
- Temporary Python/JS scripts

### 2. Test Files Outside tests/
Development test files scattered around:
- `test_*.py`, `test_*.js` outside tests/
- `debug_*.py`, `debug_*.js` debug scripts
- `temp_*.py`, `quick_*.py` temporary scripts
- `*_test.py`, `*.test.js` alternative patterns

### 3. Claude Report Proliferation
Reports and analyses that should be consolidated:
- `*_REPORT.md`, `*_ANALYSIS.md`
- `*_PLAN.md`, `*_SUMMARY.md`
- `*_TODO.md`, `*_NOTES.md`
- Duplicate documentation that belongs in README

### 4. Work Directory Organization
Work units and their artifacts:
- Completed work > 7 days old
- Abandoned/stale current work
- Reports that belong with their work units
- Duplicate planning documents

## Phase 3: Smart Consolidation

Based on what I find, I'll:

### For Root Directory Files
1. **Identify misplaced files**:
   - `.md` files that aren't core docs → Move to `.claude/work/` or remove
   - Shell scripts → Archive or move to `scripts/`
   - Test files → Move to `tests/` or remove
   - Debug scripts → Remove (they're usually one-time use)

### For Claude Reports
2. **Consolidate intelligently** (now fully implemented):
   - **Auto-detects content type** based on filename and content preview
   - **Work-related reports** → Merge into current work unit or `.claude/work/current/consolidation.md`
   - **Architectural/design docs** → Archive in `.claude/reference/`
   - **General insights** → Append to README.md with clear headers
   - **Interactive mode** → Ask for confirmation on each file
   - **Auto mode** → Consolidate based on intelligent suggestions

### For Test Files
3. **Handle test clutter**:
   - Valid tests → Move to `tests/` directory
   - Debug scripts → Remove (temporary by nature)
   - Quick tests → Evaluate and remove or formalize

### For Documentation
4. **Merge and consolidate**:
   - Duplicate concepts → Merge into authoritative location
   - Temporary docs → Integrate or remove
   - Work documentation → Ensure it's with the work unit

## Phase 4: Execute Cleanup

```bash
# Create archive directory with timestamp
ARCHIVE_DIR=".archive/cleanup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$ARCHIVE_DIR"

# Function to handle file disposition
handle_file() {
    local file="$1"
    local action="$2"  # archive, delete, move, consolidate
    local target="$3"  # target location for moves

    if [ "$DRY_RUN" = true ]; then
        echo "  Would $action: $file" $([ -n "$target" ] && echo "→ $target")
        return
    fi

    case "$action" in
        archive)
            echo "  📦 Archiving: $file"
            mkdir -p "$ARCHIVE_DIR/$(dirname "$file")"
            mv "$file" "$ARCHIVE_DIR/$file"
            ;;
        delete)
            echo "  🗑️  Removing: $file"
            rm -f "$file"
            ;;
        move)
            echo "  📁 Moving: $file → $target"
            mkdir -p "$(dirname "$target")"
            mv "$file" "$target"
            ;;
        consolidate)
            echo "  📋 Consolidating: $file → $target"
            # Append content to target with header
            echo "" >> "$target"
            echo "## Content from $file" >> "$target"
            echo "" >> "$target"
            cat "$file" >> "$target"
            # Archive original
            mkdir -p "$ARCHIVE_DIR/$(dirname "$file")"
            mv "$file" "$ARCHIVE_DIR/$file"
            ;;
    esac
}

# Function to detect consolidation candidates
detect_md_reports() {
    local candidates=()

    # Find standalone .md files (excluding core docs)
    while IFS= read -r -d '' file; do
        case "$(basename "$file")" in
            README.md|CHANGELOG.md|CLAUDE.md|LICENSE.md) ;;
            *) candidates+=("$file") ;;
        esac
    done < <(find . -maxdepth 1 -name "*.md" -type f -print0)

    # Find .md files in project subdirectories (excluding .claude, .git, node_modules)
    while IFS= read -r -d '' file; do
        candidates+=("$file")
    done < <(find . -name "*.md" -type f -path "*/*" ! -path "./.claude/*" ! -path "./.git/*" ! -path "./node_modules/*" ! -path "./tests/*" -print0)

    printf '%s\n' "${candidates[@]}"
}

# Function to suggest consolidation target
suggest_target() {
    local file="$1"
    local content_preview=$(head -10 "$file" | tr '\n' ' ')

    # Check if it's work-related
    if [[ "$file" =~ (analysis|report|summary|findings|results|review) ]] ||
       [[ "$content_preview" =~ (analysis|findings|implemented|completed|tested|reviewed) ]]; then

        # Look for related work unit
        local work_unit=$(find .claude/work -name "*.md" -type f | head -1)
        if [ -n "$work_unit" ]; then
            echo "work_unit:$work_unit"
        else
            echo "work_unit:.claude/work/current/consolidation.md"
        fi

    # Check if it's architectural/reference
    elif [[ "$content_preview" =~ (architecture|design|pattern|structure|framework|reference) ]]; then
        echo "reference:.claude/reference/$(basename "$file")"

    # Check if it's general insights
    elif [[ "$content_preview" =~ (insight|learning|principle|guideline|best.practice) ]]; then
        echo "readme:README.md"

    # Default to work unit
    else
        echo "work_unit:.claude/work/current/consolidation.md"
    fi
}
```

## Phase 5: Execute Reports Consolidation

```bash
# Handle reports mode specifically
if [ "$MODE" = "reports" ] || [ "$MODE" = "all" ]; then
    echo ""
    echo "🔍 Scanning for consolidation candidates..."

    CANDIDATES=($(detect_md_reports))
    CONSOLIDATED_COUNT=0

    if [ ${#CANDIDATES[@]} -eq 0 ]; then
        echo "✅ No standalone .md files found - project is already clean"
    else
        echo "📝 Found ${#CANDIDATES[@]} potential consolidation candidates:"
        echo ""

        for file in "${CANDIDATES[@]}"; do
            if [ ! -f "$file" ]; then continue; fi

            echo "📄 $file"

            # Show preview
            local preview=$(head -3 "$file" | sed 's/^/     /')
            echo "$preview"
            echo "     ..."

            # Get suggestion
            local suggestion=$(suggest_target "$file")
            local target_type=$(echo "$suggestion" | cut -d: -f1)
            local target_path=$(echo "$suggestion" | cut -d: -f2)

            case "$target_type" in
                work_unit)
                    echo "   💼 Suggests: Consolidate with work unit → $target_path"
                    ;;
                reference)
                    echo "   📚 Suggests: Archive as reference → $target_path"
                    ;;
                readme)
                    echo "   📖 Suggests: Integrate into README.md"
                    ;;
            esac

            # Ask for confirmation unless auto mode
            if [ "$AUTO" = false ] && [ "$DRY_RUN" = false ]; then
                echo ""
                read -p "   Consolidate this file? (y/n/s=skip): " choice
                case "$choice" in
                    y|Y)
                        if [ "$target_type" = "readme" ]; then
                            handle_file "$file" consolidate "README.md"
                        else
                            mkdir -p "$(dirname "$target_path")"
                            handle_file "$file" consolidate "$target_path"
                        fi
                        ((CONSOLIDATED_COUNT++))
                        ;;
                    s|S)
                        echo "   ⏭️  Skipping $file"
                        ;;
                    *)
                        echo "   📦 Archiving $file for manual review"
                        handle_file "$file" archive
                        ;;
                esac
            elif [ "$AUTO" = true ]; then
                # Auto mode - consolidate based on suggestion
                if [ "$target_type" = "readme" ]; then
                    handle_file "$file" consolidate "README.md"
                else
                    mkdir -p "$(dirname "$target_path")"
                    handle_file "$file" consolidate "$target_path"
                fi
                ((CONSOLIDATED_COUNT++))
            else
                # Dry run mode
                echo "   🔍 Would consolidate → $target_path"
            fi

            echo ""
        done

        if [ "$DRY_RUN" = false ]; then
            echo "✅ Consolidated $CONSOLIDATED_COUNT files"
        fi
    fi
fi

# Continue with other cleanup modes...
if [ "$MODE" = "root" ] || [ "$MODE" = "all" ]; then
    echo ""
    echo "🏠 Cleaning root directory..."
    # Add root cleanup logic here
fi

if [ "$MODE" = "tests" ] || [ "$MODE" = "all" ]; then
    echo ""
    echo "🧪 Organizing test files..."
    # Add test cleanup logic here
fi

if [ "$MODE" = "work" ] || [ "$MODE" = "all" ]; then
    echo ""
    echo "💼 Cleaning work directory..."
    # Add work cleanup logic here
fi
```

## Phase 6: Final Organization

### Key Directories After Cleanup
```
project/
├── README.md              # Main documentation
├── CHANGELOG.md           # Version history
├── CLAUDE.md              # AI context (if needed)
├── .claude/
│   ├── work/              # All work units
│   │   ├── current/       # Active work
│   │   └── completed/     # Archived work with reports
│   ├── reference/         # Permanent documentation
│   └── memory/            # Memory files
├── tests/                 # ALL test files
├── scripts/               # Utility scripts (if needed)
└── src/                   # Source code
```

### What Gets Preserved
- Core documentation (README, CHANGELOG, CLAUDE.md)
- Active source code and configurations
- Structured work units in `.claude/work/`
- Formal tests in `tests/`
- Essential scripts in `scripts/`

### What Gets Removed/Archived
- Temporary debug scripts
- One-off test files
- Redundant reports and analyses
- Duplicate documentation
- Misplaced files in root

## Success Metrics

✅ **Root directory contains only essential files**
✅ **All tests are in tests/ directory**
✅ **Reports consolidated with their work units**
✅ **No duplicate documentation**
✅ **Clear project structure maintained**
✅ **Important information preserved in appropriate locations**

## Summary Report

After cleanup, I'll provide:
- Files removed/archived count by category
- Documentation consolidated
- Tests organized
- Space recovered
- Remaining actions needed

---

*Smart cleanup that understands how Claude actually creates clutter and consolidates it appropriately*