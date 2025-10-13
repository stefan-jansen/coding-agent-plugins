---
description: "Design code examples aligned with chapter learning outcomes"
argument-hint: "--chapter N [--style free|premium|both] [--skeleton-only]"
allowed-tools: [Read, Write, Bash, Glob]
---

# Design Code Examples Command

Designs pedagogically-aligned code examples for a chapter by reviewing learning outcomes, proposing example structure, and creating skeleton notebooks.

## Parse Arguments

```bash
# Extract chapter and options
CHAPTER=""
STYLE="both"  # free, premium, both
SKELETON_ONLY=true  # Default to skeleton only (safer)

# Parse chapter number
if [[ "$ARGUMENTS" =~ --chapter[[:space:]]+([0-9]+) ]]; then
    CHAPTER="${BASH_REMATCH[1]}"
    CHAPTER_ID=$(printf "%02d" "$CHAPTER")
else
    echo "❌ Chapter number required: --chapter N"
    exit 1
fi

# Parse style
if [[ "$ARGUMENTS" =~ --style[[:space:]]+(free|premium|both) ]]; then
    STYLE="${BASH_REMATCH[1]}"
fi

echo "💻 Designing Code Examples for Chapter $CHAPTER"
echo "🎨 Style: $STYLE"
echo "📝 Mode: Skeleton creation"
```

## Setup Paths

```bash
# Project paths
PROJECT_ROOT="$HOME/ml4t"
CHAPTERS_DIR="$PROJECT_ROOT/third_edition/chapters"
CODE_BASE="$HOME/ml3t"

# Find chapter directory
CHAPTER_DIR=$(find "$CHAPTERS_DIR" -maxdepth 1 -type d -name "${CHAPTER_ID}_*" | head -1)
if [ -z "$CHAPTER_DIR" ]; then
    echo "❌ Chapter directory not found for chapter $CHAPTER"
    exit 1
fi

OUTLINE_FILE="${CHAPTER_DIR}/manuscript/outline.md"

# Output paths
DESIGN_DIR="$CHAPTER_DIR/code_design"
NOTEBOOKS_DIR="$CHAPTER_DIR/notebooks"
MAPPING_FILE="$DESIGN_DIR/code_to_lo_mapping.md"

mkdir -p "$DESIGN_DIR"
mkdir -p "$NOTEBOOKS_DIR"

echo "📁 Chapter directory: $CHAPTER_DIR"
echo "📁 Code design: $DESIGN_DIR"
echo "📁 Notebooks: $NOTEBOOKS_DIR"
```

## Step 1: Review Chapter Context

```bash
echo ""
echo "📖 Step 1: Reviewing chapter context..."

# Check outline exists
if [ ! -f "$OUTLINE_FILE" ]; then
    echo "❌ No outline found: $OUTLINE_FILE"
    exit 1
fi

# Extract chapter metadata
CHAPTER_TITLE=$(grep "^# " "$OUTLINE_FILE" | head -1 | sed 's/^# //' | sed 's/\*//g' | xargs)
WORD_TARGET=$(grep -A 5 "CHAPTER GUIDANCE" "$OUTLINE_FILE" | grep "Word Target" | grep -oP '\d+' | head -1)

echo "  📚 Chapter: $CHAPTER - $CHAPTER_TITLE"
echo "  🎯 Word target: $WORD_TARGET words"

# Extract learning outcomes
echo "  🎓 Learning Outcomes:"
LOS_SECTION=$(awk '
    /Learning Outcomes:/,/^---/ {
        if (/Learning Outcomes:/) {
            in_los = 1
            next
        }
        if (in_los && /^[[:space:]]*\*/) {
            print
        }
        if (in_los && /^---/) {
            exit
        }
    }
' "$OUTLINE_FILE")

echo "$LOS_SECTION" | sed 's/^[[:space:]]*\*/     -/' | head -10

# Count notebooks mentioned in outline
NOTEBOOK_MENTIONS=$(grep -c -i "notebook" "$OUTLINE_FILE")
echo "  💻 Notebooks mentioned in outline: $NOTEBOOK_MENTIONS"
```

## Step 2: Create Design Proposal

```bash
echo ""
echo "💡 Step 2: Creating design proposal..."

# Create design document
DESIGN_DOC="$DESIGN_DIR/design_proposal_$(date +%Y%m%d_%H%M%S).md"

cat > "$DESIGN_DOC" << EOF
# Code Examples Design Proposal
## Chapter $CHAPTER: $CHAPTER_TITLE

**Generated**: $(date)
**Scope**: $STYLE content

---

## Learning Outcomes

$LOS_SECTION

---

## Proposed Code Examples

**Instructions**: Edit this proposal to specify concrete code examples that map to the learning outcomes above.

For each example, provide:
- **Example Name**: Descriptive name (will be used for notebook filename)
- **Type**: demonstration | tutorial | exercise
- **LO Mapping**: Which LO(s) it addresses (e.g., LO1, LO2)
- **Content Tier**: free | premium
- **Difficulty**: beginner | intermediate | advanced
- **Rationale**: Why this example for these LOs

### Example 1: [TODO: Name]

- **Type**: demonstration
- **LO Mapping**: LO1, LO2
- **Content Tier**: free
- **Difficulty**: beginner
- **Rationale**: [TODO: Explain pedagogical purpose]

**Outline**:
1. Setup and imports
2. Load sample data
3. Implement baseline
4. Implement advanced technique
5. Compare results
6. Visualize
7. Key takeaways

---

### Example 2: [TODO: Name]

- **Type**: tutorial
- **LO Mapping**: LO3
- **Content Tier**: free
- **Difficulty**: intermediate
- **Rationale**: [TODO: Explain pedagogical purpose]

**Outline**:
1. Problem setup
2. Data preparation
3. Implementation steps
4. Validation
5. Extension exercises

---

### Example 3: [TODO: Name]

- **Type**: exercise
- **LO Mapping**: LO4, LO5
- **Content Tier**: premium
- **Difficulty**: advanced
- **Rationale**: [TODO: Explain pedagogical purpose]

**Outline**:
1. Business problem
2. End-to-end implementation
3. Performance optimization
4. Production considerations

---

## Next Steps

1. Edit this proposal to specify concrete examples
2. Run this command again to generate skeleton notebooks
3. Fill in notebook TODOs with implementation

EOF

echo "  ✅ Design proposal created: $DESIGN_DOC"
```

## Step 3: Check Existing Code

```bash
echo ""
echo "🔍 Step 3: Checking existing ml3t code..."

# Find existing code for this chapter
EXISTING_CODE=$(find "$CODE_BASE" -type d -name "*$(printf "%02d" $CHAPTER)*" 2>/dev/null | head -5)

if [ -n "$EXISTING_CODE" ]; then
    echo "  📦 Found existing code directories:"
    echo "$EXISTING_CODE" | while read -r dir; do
        NOTEBOOK_COUNT=$(find "$dir" -name "*.ipynb" 2>/dev/null | wc -l)
        PY_COUNT=$(find "$dir" -name "*.py" 2>/dev/null | wc -l)
        echo "     - $(basename "$dir"): $NOTEBOOK_COUNT notebooks, $PY_COUNT Python files"

        # List first 5 notebooks
        if [ $NOTEBOOK_COUNT -gt 0 ]; then
            find "$dir" -name "*.ipynb" -exec basename {} \; | head -5 | sed 's/^/         * /'
        fi
    done

    # Add to design proposal
    cat >> "$DESIGN_DOC" << EOF

---

## Existing Code Found

EOF
    echo "$EXISTING_CODE" | while read -r dir; do
        echo "- \`$dir\`" >> "$DESIGN_DOC"
    done

    cat >> "$DESIGN_DOC" << EOF

**Migration Notes**:
- Review existing notebooks for reusable content
- Adapt 2nd edition code to 3rd edition structure
- Update data sources and APIs
- Ensure alignment with new LOs

EOF

else
    echo "  ⚠️  No existing code found for Chapter $CHAPTER"
    echo "     Starting fresh implementation"
fi
```

## Step 4: Create Skeleton Notebooks

```bash
echo ""
echo "📝 Step 4: Creating skeleton notebooks..."

# Function to create skeleton notebook
create_skeleton_notebook() {
    local example_name=$1
    local lo_mapping=$2
    local notebook_type=$3
    local difficulty=$4
    local content_tier=$5

    local safe_name=$(echo "$example_name" | sed 's/[^a-zA-Z0-9-]/_/g' | tr '[:upper:]' '[:lower:]')
    local notebook_file="$NOTEBOOKS_DIR/${CHAPTER_ID}_${safe_name}.ipynb"

    echo "  📓 Creating: $(basename "$notebook_file")"

    # Create basic Jupyter notebook structure
    cat > "$notebook_file" << 'NOTEBOOK_EOF'
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Chapter CHAPTER_NUM: EXAMPLE_NAME\n",
    "\n",
    "**Type**: NOTEBOOK_TYPE  \n",
    "**Difficulty**: DIFFICULTY  \n",
    "**Learning Outcomes**: LO_MAPPING  \n",
    "**Content Tier**: CONTENT_TIER\n",
    "\n",
    "---\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Overview\n",
    "\n",
    "**TODO**: Describe what this notebook demonstrates.\n",
    "\n",
    "**Prerequisites**:\n",
    "- TODO: List prerequisites\n",
    "\n",
    "**Deliverables**:\n",
    "- TODO: List what reader will build\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Setup and Imports\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# TODO: Add imports\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Notebook settings\n",
    "plt.style.use('seaborn-v0_8-darkgrid')\n",
    "sns.set_palette('husl')\n",
    "pd.set_option('display.max_columns', None)\n",
    "\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TODO: Section 1\n",
    "\n",
    "**TODO**: Add first major section\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# TODO: Implement Section 1"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TODO: Section 2\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# TODO: Implement Section 2"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Key Takeaways\n",
    "\n",
    "**TODO**: Summarize key learning points\n",
    "\n",
    "1. TODO: First takeaway\n",
    "2. TODO: Second takeaway\n",
    "3. TODO: Third takeaway\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Next Steps\n",
    "\n",
    "**TODO**: Suggest next notebooks or exercises\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
NOTEBOOK_EOF

    # Replace placeholders
    sed -i "s/CHAPTER_NUM/$CHAPTER/g" "$notebook_file"
    sed -i "s/EXAMPLE_NAME/$example_name/g" "$notebook_file"
    sed -i "s/NOTEBOOK_TYPE/$notebook_type/g" "$notebook_file"
    sed -i "s/DIFFICULTY/$difficulty/g" "$notebook_file"
    sed -i "s/LO_MAPPING/$lo_mapping/g" "$notebook_file"
    sed -i "s/CONTENT_TIER/$content_tier/g" "$notebook_file"

    # Add to mapping file
    echo "- **$example_name** → LOs: $lo_mapping → \`$(basename "$notebook_file")\` ($content_tier)" >> "$MAPPING_FILE"

    echo "    ✓ Skeleton created"
}

# Initialize mapping file
cat > "$MAPPING_FILE" << EOF
# Code-to-LO Mapping: Chapter $CHAPTER

**Chapter**: $CHAPTER - $CHAPTER_TITLE
**Generated**: $(date)

## Mapping Table

EOF

# Create default skeleton notebooks (user can customize from design proposal)
echo "  Creating default skeleton structure..."

# Create 3 example skeletons
create_skeleton_notebook \
    "Introduction_to_Concept" \
    "LO1, LO2" \
    "demonstration" \
    "beginner" \
    "free"

create_skeleton_notebook \
    "Step_by_Step_Implementation" \
    "LO3, LO4" \
    "tutorial" \
    "intermediate" \
    "free"

create_skeleton_notebook \
    "Advanced_Challenge" \
    "LO5" \
    "exercise" \
    "advanced" \
    "premium"

SKELETON_COUNT=$(find "$NOTEBOOKS_DIR" -name "${CHAPTER_ID}_*.ipynb" 2>/dev/null | wc -l)
echo ""
echo "  ✅ Created $SKELETON_COUNT skeleton notebooks"
```

## Update Mapping Documentation

```bash
# Add migration notes and next steps to mapping file
cat >> "$MAPPING_FILE" << EOF

---

## Migration Notes

### Existing Code Found
EOF

if [ -n "$EXISTING_CODE" ]; then
    echo "$EXISTING_CODE" | while read -r dir; do
        echo "- \`$dir\`" >> "$MAPPING_FILE"
    done
else
    echo "- None (starting fresh)" >> "$MAPPING_FILE"
fi

cat >> "$MAPPING_FILE" << EOF

### Next Steps

1. **Edit design proposal**: $DESIGN_DOC
   - Specify concrete example names and LO mappings
   - Define pedagogical rationale

2. **Rename skeletons** to match design
   - Update notebook filenames based on proposal
   - Ensure clear naming (descriptive, not generic)

3. **Fill in TODOs** in skeleton notebooks
   - Add implementations
   - Create visualizations
   - Write explanations

4. **Test notebooks**: Use \`/test --chapter $CHAPTER\`
   - Verify reproducibility
   - Check code quality

5. **Sync with text**: Use \`/sync --chapter $CHAPTER\`
   - Ensure code-text alignment
   - Check citations

### Premium vs Free Content

- **Free (GitHub + Book)**: Core demonstrations and tutorials
- **Premium (Course)**: Advanced exercises, extended examples, challenge problems

---

**Files Generated**:
- Design Proposal: \`$(basename "$DESIGN_DOC")\`
- Skeleton Notebooks: \`$NOTEBOOKS_DIR\`
- Mapping Document: \`$(basename "$MAPPING_FILE")\`

EOF

echo "  ✅ Mapping documentation updated"
```

## Display Summary

```bash
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║        ✅ CODE EXAMPLES DESIGN COMPLETE                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📚 Chapter: $CHAPTER - $CHAPTER_TITLE"
echo "🎨 Content Style: $STYLE"
echo ""
echo "📁 Generated Files:"
echo "   Design Proposal: $DESIGN_DOC"
echo "   Code Mapping: $MAPPING_FILE"
echo "   Notebooks: $NOTEBOOKS_DIR"
echo ""
echo "📊 Summary:"
echo "   Skeleton notebooks: $SKELETON_COUNT"
if [ -n "$EXISTING_CODE" ]; then
    echo "   Existing code: Yes (review for migration)"
else
    echo "   Existing code: No (fresh implementation)"
fi
echo ""
echo "🔍 Next Steps:"
echo "   1. Edit design proposal: $DESIGN_DOC"
echo "   2. Customize example names and LO mappings"
echo "   3. Rename/update skeleton notebooks"
echo "   4. Fill in TODOs with implementations"
echo "   5. Test: /test --chapter $CHAPTER"
echo "   6. Sync: /sync --chapter $CHAPTER"
echo ""
echo "Quick view:"
echo "   cat $MAPPING_FILE"
echo "   ls -lh $NOTEBOOKS_DIR"
```

---

## Usage Examples

```bash
# Design code examples for chapter 3
/design-code-examples --chapter 3

# Design only free content
/design-code-examples --chapter 5 --style free

# Design only premium content
/design-code-examples --chapter 12 --style premium
```

## Integration Points

- **Reads**: `~/ml4t/third_edition/chapters/$CHAPTER_DIR/manuscript/outline.md`
- **Checks**: `~/ml3t/` (existing code for migration)
- **Writes**: `~/ml4t/third_edition/chapters/$CHAPTER_DIR/code_design/`
- **Writes**: `~/ml4t/third_edition/chapters/$CHAPTER_DIR/notebooks/`
- **Integrates with**: `/notebook`, `/test`, `/sync` commands
