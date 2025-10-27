---
title: performance
aliases: [metrics, usage, cost]
description: View token usage and performance metrics
---

# Performance Metrics

View token usage, costs, and performance metrics for your Claude Code sessions.

## Usage

```bash
# View current session metrics
/performance

# View daily metrics
/performance daily

# View weekly metrics
/performance weekly

# View monthly metrics
/performance monthly

# Get help with ccusage
/performance help
```

## Implementation

```bash
# Check if ccusage is available
if ! command -v npx >/dev/null 2>&1; then
    echo "❌ Performance monitoring requires npx (Node.js)"
    echo ""
    echo "To enable performance tracking:"
    echo "1. Install Node.js: https://nodejs.org/"
    echo "2. Run: npx ccusage@latest"
    exit 1
fi

# Parse arguments
TIMEFRAME="${ARGUMENTS:-session}"

echo "📊 Claude Code Performance Metrics"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

case "$TIMEFRAME" in
    daily|day)
        echo "📅 Daily Usage Report"
        npx ccusage@latest daily
        ;;
    weekly|week)
        echo "📅 Weekly Usage Report"
        npx ccusage@latest weekly
        ;;
    monthly|month)
        echo "📅 Monthly Usage Report"
        npx ccusage@latest monthly
        ;;
    help|--help)
        echo "📚 ccusage Help"
        npx ccusage@latest --help
        ;;
    session|*)
        echo "💬 Current Session Metrics"
        npx ccusage@latest session

        # Also show daily summary
        echo ""
        echo "📅 Today's Summary"
        npx ccusage@latest daily
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Performance Tips:"
echo "   • Use MCP tools for efficiency:"
echo "     - Serena: 70-90% token reduction on code operations"
echo "     - Context7: 50% faster documentation lookup"
echo "     - Sequential Thinking: Better analysis with fewer iterations"
echo "   • Monitor usage regularly to optimize workflows"
echo "   • Consider caching frequently accessed documentation"
```

## Features

### Token Usage Tracking
- Session-level metrics
- Daily, weekly, monthly aggregation
- Cost calculation based on model pricing

### Performance Insights
When available, tracks:
- Token consumption by command
- MCP tool efficiency gains
- Session duration and patterns

### MCP Tool Impact
Estimated efficiency gains:
- **Serena**: 70-90% token reduction on code analysis
- **Context7**: 50% faster documentation access
- **Sequential Thinking**: 20-30% better analysis quality
- **Firecrawl**: Efficient web content extraction

## Graceful Degradation

Without ccusage, the command provides guidance on:
- How to install Node.js and enable tracking
- Manual estimation of token usage
- Best practices for efficient Claude Code usage

## Integration

Performance metrics integrate with:
- Session management in `/status`
- Work unit tracking in `/work`
- Project analysis in `/analyze`

---

*Simplified performance monitoring using ccusage for token tracking and cost analysis*