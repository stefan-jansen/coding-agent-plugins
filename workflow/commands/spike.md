---
title: "spike"
aliases: ["explore-spike", "prototype"]
---

# Spike - Time-boxed Technical Exploration

Creates an isolated environment for experimental code exploration with relaxed quality gates and automatic cleanup.

## Usage

```bash
# Start a spike
/spike start "exploration topic" [--duration MINUTES]

# Complete and generate report
/spike complete

# Abandon spike (cleanup)
/spike abandon
```

## Purpose

Spikes are time-boxed technical investigations to:
- Explore new technologies or approaches
- Prototype solutions without commitment
- Research implementation feasibility
- Learn through experimentation
- Gather information for decisions

## Process

### Starting a Spike

```bash
/spike start "websocket implementation"
```

Creates:
1. Isolated git branch (spike/topic-timestamp)
2. Spike tracking file
3. Relaxed quality gates
4. Time box (default: 2 hours)

### During the Spike

- Experiment freely
- Try multiple approaches
- Break things safely
- Focus on learning
- Document findings

### Completing a Spike

```bash
/spike complete
```

Generates:
1. Findings report
2. Code artifacts
3. Recommendations
4. Decision points
5. Optional: merge or discard

## Implementation

```bash
#!/bin/bash

SPIKE_DIR=".claude/spikes"
CURRENT_SPIKE="$SPIKE_DIR/current.json"
COMMAND="${ARGUMENTS%% *}"
ARGS="${ARGUMENTS#* }"

mkdir -p "$SPIKE_DIR"

case "$COMMAND" in
    "start")
        echo "🔬 Starting Technical Spike"
        echo "════════════════════════════════════"
        echo ""

        TOPIC="$ARGS"
        DURATION=120  # Default 2 hours

        # Parse duration if provided
        if [[ "$ARGS" == *"--duration"* ]]; then
            DURATION=$(echo "$ARGS" | grep -oP '(?<=--duration )\d+')
            TOPIC=$(echo "$ARGS" | sed 's/--duration.*//' | xargs)
        fi

        # Check for existing spike
        if [ -f "$CURRENT_SPIKE" ]; then
            echo "⚠️  Active spike detected!"
            echo ""
            echo "Complete or abandon current spike first:"
            echo "  /spike complete  - Generate report and finish"
            echo "  /spike abandon   - Discard and cleanup"
            exit 1
        fi

        # Create spike branch
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        BRANCH_NAME="spike/$(echo "$TOPIC" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g')-$TIMESTAMP"

        echo "📁 Creating spike branch: $BRANCH_NAME"
        git checkout -b "$BRANCH_NAME" 2>/dev/null || {
            echo "❌ Failed to create branch. Commit or stash current changes first."
            exit 1
        }

        # Create spike tracking
        cat > "$CURRENT_SPIKE" <<EOF
{
  "topic": "$TOPIC",
  "branch": "$BRANCH_NAME",
  "started": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "duration_minutes": $DURATION,
  "status": "active",
  "findings": [],
  "artifacts": [],
  "recommendations": []
}
EOF

        echo ""
        echo "✅ Spike initialized!"
        echo ""
        echo "📋 Spike Details:"
        echo "  Topic: $TOPIC"
        echo "  Branch: $BRANCH_NAME"
        echo "  Time box: $DURATION minutes"
        echo ""
        echo "🎯 Spike Goals:"
        echo "  • Explore implementation options"
        echo "  • Identify technical challenges"
        echo "  • Prototype potential solutions"
        echo "  • Document learnings"
        echo ""

        cat <<'EOF'
Begin exploring: $TOPIC

**Spike Guidelines**:
1. **Experiment Freely** - Try different approaches
2. **Break Things** - It's isolated in a branch
3. **Learn Fast** - Focus on understanding
4. **Document Findings** - Note what works/doesn't
5. **Time Box** - Stop at $DURATION minutes

**Focus Areas**:
- Technical feasibility
- Implementation complexity
- Performance implications
- Integration challenges
- Required dependencies

**What to Explore** for "$TOPIC":
- Available libraries and tools
- Best practices and patterns
- Potential pitfalls
- Architecture options
- Proof of concept code

Start by researching and then prototyping. Quality doesn't matter - learning does!
EOF

        echo ""
        echo "⏰ Time box: $DURATION minutes"
        echo "Complete with: /spike complete"
        ;;

    "complete")
        echo "📊 Completing Spike"
        echo "════════════════════════════════════"
        echo ""

        if [ ! -f "$CURRENT_SPIKE" ]; then
            echo "❌ No active spike found"
            echo "Start a spike with: /spike start \"topic\""
            exit 1
        fi

        # Read spike data
        TOPIC=$(grep -oP '"topic":\s*"\K[^"]+' "$CURRENT_SPIKE")
        BRANCH=$(grep -oP '"branch":\s*"\K[^"]+' "$CURRENT_SPIKE")
        STARTED=$(grep -oP '"started":\s*"\K[^"]+' "$CURRENT_SPIKE")

        echo "📝 Generating Spike Report"
        echo "────────────────────────"
        echo ""
        echo "Topic: $TOPIC"
        echo "Branch: $BRANCH"
        echo "Started: $STARTED"
        echo ""

        # Generate report
        REPORT_FILE="$SPIKE_DIR/report_$(date +%Y%m%d_%H%M%S).md"

        cat <<'EOF'
Complete the spike and generate a comprehensive report.

**Spike Topic**: $TOPIC

Please create a spike report with:

1. **Executive Summary**
   - What was explored
   - Key findings
   - Recommendation (proceed/pivot/abandon)

2. **Technical Findings**
   - What worked well
   - What didn't work
   - Unexpected discoveries
   - Performance observations

3. **Implementation Details**
   - Code samples that worked
   - Libraries/tools evaluated
   - Architecture decisions
   - Integration points

4. **Challenges & Risks**
   - Technical blockers found
   - Complexity assessment
   - Security considerations
   - Scalability concerns

5. **Recommendations**
   - Suggested approach
   - Estimated effort
   - Next steps
   - Alternative options

6. **Artifacts**
   - List useful code created
   - Documentation snippets
   - Configuration examples
   - Test cases

Generate the report and save to: $REPORT_FILE

After generating the report, show a summary and ask whether to:
- Keep the spike branch for reference
- Merge useful code to main
- Archive and delete branch
EOF

        # Show git status
        echo ""
        echo "📂 Changes made during spike:"
        echo "────────────────────────"
        git status --short
        echo ""
        git diff --stat
        echo ""

        # Update spike status
        if command -v jq >/dev/null 2>&1; then
            jq '.status = "completed" | .completed = "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"' "$CURRENT_SPIKE" > "$CURRENT_SPIKE.tmp" && mv "$CURRENT_SPIKE.tmp" "$CURRENT_SPIKE"
        fi

        echo "💡 Options:"
        echo "  1. Keep branch: git checkout main"
        echo "  2. Merge useful code: git checkout main && git merge $BRANCH"
        echo "  3. Archive: git checkout main && git branch -D $BRANCH"
        echo ""
        echo "Report saved to: $REPORT_FILE"

        # Archive current spike
        mv "$CURRENT_SPIKE" "$SPIKE_DIR/completed_$(date +%Y%m%d_%H%M%S).json"
        ;;

    "abandon")
        echo "🗑️  Abandoning Spike"
        echo "════════════════════════════════════"
        echo ""

        if [ ! -f "$CURRENT_SPIKE" ]; then
            echo "❌ No active spike found"
            exit 0
        fi

        BRANCH=$(grep -oP '"branch":\s*"\K[^"]+' "$CURRENT_SPIKE")

        echo "⚠️  This will discard all spike work!"
        echo ""
        echo "Branch to delete: $BRANCH"
        echo ""

        # Switch to main/master
        DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
        git checkout "$DEFAULT_BRANCH" 2>/dev/null || git checkout main 2>/dev/null || git checkout master

        # Delete spike branch
        git branch -D "$BRANCH" 2>/dev/null && echo "✅ Spike branch deleted"

        # Remove tracking
        rm -f "$CURRENT_SPIKE"

        echo ""
        echo "✅ Spike abandoned and cleaned up"
        ;;

    "status"|*)
        echo "📊 Spike Status"
        echo "════════════════════════════════════"
        echo ""

        if [ ! -f "$CURRENT_SPIKE" ]; then
            echo "No active spike"
            echo ""
            echo "Start a spike with:"
            echo "  /spike start \"topic to explore\""
        else
            echo "Active Spike:"
            echo "────────────"
            cat "$CURRENT_SPIKE" | jq . 2>/dev/null || cat "$CURRENT_SPIKE"
            echo ""
            echo "Commands:"
            echo "  /spike complete - Finish and generate report"
            echo "  /spike abandon  - Discard all work"
        fi

        echo ""
        echo "📁 Previous Spikes:"
        echo "────────────────"
        find "$SPIKE_DIR" -name "report_*.md" -type f 2>/dev/null | while read -r report; do
            basename "$report"
        done | head -5
        ;;
esac
```

## Features

### Isolation
- Separate git branch
- No impact on main code
- Easy rollback
- Safe experimentation

### Time Boxing
- Default 2-hour limit
- Configurable duration
- Prevents rabbit holes
- Forces decision making

### Relaxed Rules
- No quality gates during spike
- Commit anything
- Break conventions
- Focus on learning

### Documentation
- Automatic report generation
- Findings capture
- Code artifact preservation
- Decision documentation

## Spike Types

### Technology Spike
```bash
/spike start "evaluate GraphQL vs REST"
```
Explore new technologies or libraries

### Architecture Spike
```bash
/spike start "microservice communication patterns"
```
Test architectural approaches

### Performance Spike
```bash
/spike start "optimize database queries"
```
Investigate performance improvements

### Integration Spike
```bash
/spike start "third-party payment integration"
```
Test external service integration

## Best Practices

### DO:
- Time box strictly
- Document findings immediately
- Try multiple approaches
- Break things to learn
- Focus on specific questions

### DON'T:
- Polish code during spike
- Write comprehensive tests
- Worry about code quality
- Exceed time box
- Spike without clear goals

## Report Structure

Generated reports include:

```markdown
# Spike Report: [Topic]

## Executive Summary
- Duration: X hours
- Status: Completed/Abandoned
- Recommendation: Proceed/Pivot/Abandon

## Findings
### What Worked
- Approach A showed promise
- Library X meets requirements

### What Didn't Work
- Approach B too complex
- Performance issues with Y

## Code Artifacts
- `prototype/api.py` - Working API example
- `config/websocket.json` - Configuration template

## Recommendations
Based on this spike, we recommend...

## Next Steps
1. Create formal design document
2. Estimate implementation effort
3. Plan development tasks
```

## Configuration

Customize in `.claude/settings.json`:

```json
{
  "spike": {
    "default_duration": 120,
    "max_duration": 480,
    "require_report": true,
    "auto_archive": true,
    "branch_prefix": "spike/"
  }
}
```

## See Also

- `/explore` - Formal exploration with planning
- `/quickfix` - Fast fixes without exploration
- `/experiment` - ML experimentation
- `/analyze` - Codebase analysis

---

*Time-boxed technical exploration in isolated environment. Part of Claude Code Framework v3.1.*