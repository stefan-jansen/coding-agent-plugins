---
title: report
aliases: [generate-report]
description: Generate professional stakeholder reports from data
---

# Report Generation

I'll create a professional report from your data using the report-generator agent specialized in transforming raw analysis results into stakeholder-appropriate deliverables.

**Input**: `$ARGUMENTS`

## Command Usage

```bash
/report [audience] [data_source] [options]

# Examples:
/report technical ml_experiment.json --output reports/
/report business quarterly_metrics.csv --format notebook
/report executive incident_data.json --sections "summary,impact,actions"
/report --audience technical --data .agents/work/current/analysis.json
```

## Audience Types
- **technical**: Detailed metrics, code examples, architecture diagrams
- **business**: KPIs, ROI analysis, resource utilization
- **executive**: One-page summaries, key decisions, recommendations

## Execution

```bash
#!/bin/bash

# Parse arguments for audience and data source
AUDIENCE="technical"  # default
DATA_SOURCE=""
OUTPUT_DIR="reports"
SECTIONS=""

# Extract arguments
if [[ "$ARGUMENTS" =~ (technical|business|executive) ]]; then
    AUDIENCE="${BASH_REMATCH[1]}"
fi

if [[ "$ARGUMENTS" =~ ([a-zA-Z0-9_/.-]+\.(json|csv|txt)) ]]; then
    DATA_SOURCE="${BASH_REMATCH[0]}"
fi

if [[ "$ARGUMENTS" =~ --output[[:space:]]+([a-zA-Z0-9_/.-]+) ]]; then
    OUTPUT_DIR="${BASH_REMATCH[1]}"
fi

if [[ "$ARGUMENTS" =~ --sections[[:space:]]+"([^"]+)" ]]; then
    SECTIONS="${BASH_REMATCH[1]}"
fi

echo "📊 Report Generation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Validate data source
if [ -z "$DATA_SOURCE" ]; then
    # Try to find recent analysis data
    if [ -d ".agents/work/current" ]; then
        DATA_SOURCE=$(find .agents/work/current -name "*.json" -o -name "*.csv" | head -1)
        if [ -n "$DATA_SOURCE" ]; then
            echo "📁 Auto-detected data source: $DATA_SOURCE"
        else
            echo "❌ No data source specified and none found in work directory"
            echo ""
            echo "Usage: /report [audience] [data_file]"
            echo "Example: /report technical analysis_results.json"
            exit 1
        fi
    fi
fi

if [ ! -f "$DATA_SOURCE" ]; then
    echo "❌ Data source not found: $DATA_SOURCE"
    exit 1
fi

echo "👥 Target Audience: $AUDIENCE"
echo "📁 Data Source: $DATA_SOURCE"
echo "📂 Output Directory: $OUTPUT_DIR"
if [ -n "$SECTIONS" ]; then
    echo "📑 Sections: $SECTIONS"
fi
echo ""

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Generate timestamp for report naming
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
REPORT_NAME="${TIMESTAMP}_${AUDIENCE}_report"

echo "🚀 Invoking report-generator agent..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

## Agent Invocation

I'll now invoke the specialized report-generator agent to create your report. The agent will:

1. **Analyze your data** to understand structure and content
2. **Select appropriate template** based on audience type
3. **Generate interactive notebook** with visualizations
4. **Create professional narrative** with clear insights
5. **Provide actionable recommendations**

### Report Generation Process

The report-generator agent specializes in:
- **Data Transformation**: Converting raw data into meaningful insights
- **Audience Adaptation**: Tailoring content depth and style
- **Visual Excellence**: Creating impactful charts and dashboards
- **Professional Output**: Ensuring report quality and coherence

### Template Selection

Based on your audience type:

#### Technical Audience
- Detailed implementation analysis
- Performance metrics and benchmarks
- Code examples and architecture diagrams
- Technical recommendations and improvements
- Comprehensive test results

#### Business Audience
- KPI dashboards and trend analysis
- ROI calculations and projections
- Resource utilization metrics
- Competitive positioning
- Strategic recommendations

#### Executive Audience
- One-page executive summary
- 3-5 key findings maximum
- Critical decision points
- High-level recommendations
- Expected outcomes and timeline

## Output Formats

The agent will generate:
1. **Primary**: Jupyter notebook (`.ipynb`) with interactive content
2. **Fallback**: Markdown report if NotebookEdit unavailable
3. **Exports**: HTML for web viewing, PDF-ready formatting

## Success Criteria

Report generation succeeds when:
- ✅ Data successfully parsed and validated
- ✅ Appropriate template selected for audience
- ✅ All visualizations render correctly
- ✅ Code cells execute without errors
- ✅ Narrative is coherent and professional
- ✅ Recommendations are clear and actionable
- ✅ Report saved to specified location

## Error Handling

If issues occur:
- **Missing data**: Report proceeds with available data, notes gaps
- **Invalid format**: Attempts parsing, provides detailed errors
- **NotebookEdit unavailable**: Falls back to markdown output
- **Visualization errors**: Provides data tables as backup

## Integration Notes

The report command integrates with:
- **Work units**: Can use analysis data from current work
- **Experiments**: Transforms ML experiment results
- **Analysis**: Converts code analysis into reports
- **Performance**: Creates performance benchmarking reports

## Next Steps

After report generation:
1. Review the generated report in `{output_dir}/{report_name}.ipynb`
2. Execute notebook cells to see interactive visualizations
3. Export to HTML/PDF if needed for distribution
4. Share with appropriate stakeholders
5. Iterate based on feedback

---

*Professional report generation for effective stakeholder communication across technical, business, and executive audiences.*