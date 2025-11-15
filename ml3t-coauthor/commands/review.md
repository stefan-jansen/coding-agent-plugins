---
description: "Create pull request for chapter review"
argument-hint: "--chapter N [--reviewers user1,user2] [--self-review]"
allowed-tools: [Read, Write, Bash]
---

# Review Command

Creates Git branches and pull requests for collaborative chapter review.

## Parse Arguments

```bash
# Extract chapter and reviewer options
CHAPTER=""
REVIEWERS=""
SELF_REVIEW=false

# Parse chapter number
if [[ "$ARGUMENTS" =~ --chapter[[:space:]]+([0-9]+) ]]; then
    CHAPTER="${BASH_REMATCH[1]}"
else
    # Find chapter ready for review
    MANIFEST_FILE=".claude/book/manifest.json"
    CHAPTER=$(jq -r '.chapters | to_entries[] | select(.value.status == "drafted") | .key' "$MANIFEST_FILE" | head -1 | sed 's/^0*//')
    if [ -z "$CHAPTER" ]; then
        echo "❌ No chapters ready for review"
        exit 1
    fi
fi

# Parse reviewers
if [[ "$ARGUMENTS" =~ --reviewers[[:space:]]+([^[:space:]]+) ]]; then
    REVIEWERS="${BASH_REMATCH[1]}"
fi

# Check for self-review mode
if [[ "$ARGUMENTS" =~ --self-review ]]; then
    SELF_REVIEW=true
fi

CHAPTER_ID=$(printf "%03d" "$CHAPTER")
echo "🔍 Starting review for Chapter $CHAPTER"
```

## Verify Chapter Status

```bash
# Load chapter information
MANIFEST_FILE=".claude/book/manifest.json"
CHAPTER_TITLE=$(jq -r ".chapters.\"$CHAPTER_ID\".title" "$MANIFEST_FILE")
CHAPTER_STATUS=$(jq -r ".chapters.\"$CHAPTER_ID\".status" "$MANIFEST_FILE")
WORD_COUNT=$(jq -r ".chapters.\"$CHAPTER_ID\".word_count // 0" "$MANIFEST_FILE")

if [ "$CHAPTER_TITLE" == "null" ]; then
    echo "❌ Chapter $CHAPTER not found"
    exit 1
fi

if [ "$CHAPTER_STATUS" != "drafted" ] && [ "$CHAPTER_STATUS" != "review" ]; then
    echo "⚠️  Chapter is in '$CHAPTER_STATUS' status, expected 'drafted'"
    echo "Use /write to complete drafting first"
    exit 1
fi

echo "📖 Chapter: $CHAPTER_TITLE"
echo "📊 Words: $WORD_COUNT"
```

## Prepare Review Content

```bash
# Consolidate chapter content
CHAPTER_DIR=".claude/book/chapters/$CHAPTER_ID"
REVIEW_DIR="$CHAPTER_DIR/review"
mkdir -p "$REVIEW_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REVIEW_FILE="$REVIEW_DIR/chapter_${CHAPTER_ID}_review_${TIMESTAMP}.md"

# Merge all drafts into review document
echo "# Chapter $CHAPTER: $CHAPTER_TITLE" > "$REVIEW_FILE"
echo "" >> "$REVIEW_FILE"
echo "---" >> "$REVIEW_FILE"
echo "**Review Version**: $TIMESTAMP" >> "$REVIEW_FILE"
echo "**Word Count**: $WORD_COUNT" >> "$REVIEW_FILE"
echo "**Status**: Under Review" >> "$REVIEW_FILE"
echo "---" >> "$REVIEW_FILE"
echo "" >> "$REVIEW_FILE"

# Concatenate all section drafts
find "$CHAPTER_DIR/drafts" -name "*_latest.md" -type l 2>/dev/null | sort | while read -r draft; do
    echo "\n---\n" >> "$REVIEW_FILE"
    # Skip metadata headers when merging
    tail -n +10 "$draft" >> "$REVIEW_FILE"
done

echo "✅ Consolidated content into: $REVIEW_FILE"
```

## Create Git Branch

```bash
# Ensure we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository. Initialize with: git init"
    exit 1
fi

# Create review branch
BRANCH_NAME="review/chapter-${CHAPTER_ID}-${TIMESTAMP}"
CURRENT_BRANCH=$(git branch --show-current)

echo "🌿 Creating branch: $BRANCH_NAME"

# Stash any uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "💾 Stashing uncommitted changes..."
    git stash push -m "Auto-stash before review branch creation"
    STASHED=true
fi

# Create and switch to review branch
git checkout -b "$BRANCH_NAME"

# Copy review file to main content location
CONTENT_FILE="content/chapters/chapter_${CHAPTER_ID}.md"
mkdir -p "$(dirname "$CONTENT_FILE")"
cp "$REVIEW_FILE" "$CONTENT_FILE"

# Copy associated notebooks
if [ -d "code/notebooks/chapter_${CHAPTER_ID}" ]; then
    echo "📓 Including notebooks in review"
    git add "code/notebooks/chapter_${CHAPTER_ID}/"
fi

# Stage changes
git add "$CONTENT_FILE"
git add "$CHAPTER_DIR/"
git add "$MANIFEST_FILE"

echo "📦 Staged files for review"
```

## Create Review Checklist

```bash
# Generate review checklist
CHECKLIST_FILE="$REVIEW_DIR/REVIEW_CHECKLIST.md"

cat > "$CHECKLIST_FILE" << EOF
# Review Checklist - Chapter $CHAPTER: $CHAPTER_TITLE

## Content Quality
- [ ] Learning objectives clearly stated
- [ ] Content flows logically
- [ ] Examples are clear and relevant
- [ ] Technical accuracy verified
- [ ] No gaps in explanation

## Code Quality
- [ ] All code examples run without errors
- [ ] Code follows style guidelines
- [ ] Comments explain complex logic
- [ ] Error handling implemented
- [ ] Performance considerations addressed

## Documentation
- [ ] Mathematical notation consistent
- [ ] Figures and diagrams clear
- [ ] Cross-references accurate
- [ ] Citations properly formatted
- [ ] Glossary terms defined

## Technical Review
- [ ] Algorithms correctly implemented
- [ ] Best practices followed
- [ ] Security considerations addressed
- [ ] Scalability discussed where relevant
- [ ] Edge cases handled

## Style and Readability
- [ ] Consistent tone throughout
- [ ] Grammar and spelling checked
- [ ] Technical terms explained
- [ ] Appropriate for target audience
- [ ] Engaging and clear writing

## Completeness
- [ ] All sections from outline covered
- [ ] Exercises provided and tested
- [ ] Summary reinforces key points
- [ ] Further reading suggestions included
- [ ] Preview of next chapter provided

## Reviewer Comments

### Strengths
- 

### Areas for Improvement
- 

### Specific Suggestions
- 

---
**Reviewer**: [Name]
**Date**: $(date -I)
**Recommendation**: [ ] Approve [ ] Request Changes [ ] Comment Only
EOF

git add "$CHECKLIST_FILE"
echo "📋 Created review checklist"
```

## Commit Changes

```bash
# Commit the review content
git commit -m "feat(chapter-$CHAPTER_ID): Add $CHAPTER_TITLE for review

- Consolidated drafts into review document
- Total word count: $WORD_COUNT
- Includes outline and all drafted sections
- Added review checklist
- Associated notebooks included

Ready for review: Chapter $CHAPTER - $CHAPTER_TITLE"

echo "✅ Committed review content"
```

## Create Pull Request

```bash
if [ "$SELF_REVIEW" == "true" ]; then
    echo "\n👤 Self-Review Mode"
    echo "Review branch created: $BRANCH_NAME"
    echo "Review your changes locally before pushing"
else
    # Push branch to remote
    echo "🚀 Pushing to remote..."
    git push -u origin "$BRANCH_NAME"
    
    # Create PR using GitHub CLI if available
    if command -v gh &> /dev/null; then
        echo "🔗 Creating pull request..."
        
        PR_BODY="## Chapter $CHAPTER: $CHAPTER_TITLE

### Summary
This PR contains the complete draft of Chapter $CHAPTER for review.

### Statistics
- **Word Count**: $WORD_COUNT
- **Sections**: $(grep -c '^## ' "$REVIEW_FILE")
- **Code Examples**: $(grep -c '^```python' "$REVIEW_FILE")
- **Notebooks**: $(ls -1 "code/notebooks/chapter_${CHAPTER_ID}/"*.ipynb 2>/dev/null | wc -l)

### Review Checklist
Please use the checklist in \`$CHECKLIST_FILE\` for your review.

### How to Review
1. Read through the chapter content
2. Run the included notebooks
3. Check technical accuracy
4. Complete the review checklist
5. Leave comments inline for specific feedback
"
        
        if [ -n "$REVIEWERS" ]; then
            REVIEWER_FLAGS="--reviewer $REVIEWERS"
        else
            REVIEWER_FLAGS=""
        fi
        
        PR_URL=$(gh pr create \
            --title "📖 Review: Chapter $CHAPTER - $CHAPTER_TITLE" \
            --body "$PR_BODY" \
            --base main \
            --head "$BRANCH_NAME" \
            $REVIEWER_FLAGS)
        
        echo "✅ Pull request created: $PR_URL"
    else
        echo "\n💡 To create a pull request:"
        echo "1. Visit your repository on GitHub"
        echo "2. You'll see a banner to create a PR for branch: $BRANCH_NAME"
        echo "3. Use this title: 'Review: Chapter $CHAPTER - $CHAPTER_TITLE'"
        if [ -n "$REVIEWERS" ]; then
            echo "4. Add reviewers: $REVIEWERS"
        fi
    fi
fi
```

## Update Manifest Status

```bash
# Update chapter status to review
jq --arg ch "$CHAPTER_ID" \
   --arg branch "$BRANCH_NAME" \
   --arg review_file "$REVIEW_FILE" \
   '.chapters[$ch].status = "review" |
    .chapters[$ch].review_branch = $branch |
    .chapters[$ch].files.review = $review_file |
    .chapters[$ch].review_started = now | todate' \
   "$MANIFEST_FILE" > "${MANIFEST_FILE}.tmp" && \
   mv "${MANIFEST_FILE}.tmp" "$MANIFEST_FILE"

# Commit manifest update
git add "$MANIFEST_FILE"
git commit -m "chore: Update manifest for chapter $CHAPTER_ID review"
git push
```

## Restore Working State

```bash
# Return to original branch
git checkout "$CURRENT_BRANCH"

if [ "${STASHED:-false}" == "true" ]; then
    echo "🔄 Restoring stashed changes..."
    git stash pop
fi
```

## Generate Summary

```bash
echo "\n🎉 Review Process Initiated!"
echo "───────────────────────────────────────"
echo "  Chapter: $CHAPTER - $CHAPTER_TITLE"
echo "  Branch: $BRANCH_NAME"
echo "  Review file: $REVIEW_FILE"
echo "  Checklist: $CHECKLIST_FILE"
if [ -n "$REVIEWERS" ]; then
    echo "  Reviewers: $REVIEWERS"
fi
echo ""
echo "Next steps:"
if [ "$SELF_REVIEW" == "true" ]; then
    echo "  • Review changes locally on branch: $BRANCH_NAME"
    echo "  • Complete the review checklist"
    echo "  • Push and create PR when ready"
else
    echo "  • Reviewers will be notified"
    echo "  • Address feedback in comments"
    echo "  • Update chapter based on review"
    echo "  • Merge when approved"
fi
```

---

## Examples

```bash
# Create review for next ready chapter
/review

# Review specific chapter
/review --chapter 3

# Assign specific reviewers
/review --chapter 2 --reviewers alice,bob

# Self-review mode (local only)
/review --chapter 1 --self-review
```

*The review command manages the Git-based collaborative review workflow.*