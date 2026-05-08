---
name: quant-tearsheet
description: This skill should be used when the user asks to "create a tearsheet", "generate a PDF report", "strategy summary", "backtest report", "performance tearsheet", "factor tearsheet", or when producing single-page or multi-page PDF summaries of quantitative results.
version: 1.0.0
---

# Quantitative Tearsheet Standards

PDF tearsheets are the final deliverable — dense, polished, print-ready summaries that distill complex analysis into scannable documents. Built on the ML4T visual identity established in `quant-viz`.

## Tearsheet Philosophy

A tearsheet is **not a report with charts**. It is a **designed artifact** where layout, hierarchy, and density are as important as the data itself. Think Bloomberg terminal printout meets editorial design.

### Design Principles

1. **Information density over whitespace**: every square centimeter earns its place
2. **Scannable in 30 seconds**: key metrics visible without reading text
3. **Self-contained**: no external context needed to understand the story
4. **Print-first**: grayscale compatible, A4/Letter safe margins, 150+ dpi

## Tearsheet Types

### Strategy Tearsheet (Single Page)

The canonical one-pager for strategy evaluation:

```
+------------------------------------------------------------------+
|  STRATEGY NAME                              Period: 2015-2024     |
|  Subtitle / description                     Generated: 2026-03-02 |
+------------------+-------------------+---------------------------+
|  KEY METRICS     |  RISK METRICS     |  ROLLING PERFORMANCE      |
|  ─────────────── |  ─────────────── |  [Sparkline area chart]    |
|  Ann. Return  12%|  Max DD     -18% |                            |
|  Ann. Vol     15%|  DD Duration 4mo |                            |
|  Sharpe      0.80|  Calmar     0.67 |                            |
|  Sortino     1.12|  Tail Ratio 1.24 |                            |
|  Win Rate     54%|  VaR 95%   -2.1% |                            |
+------------------+-------------------+---------------------------+
|  CUMULATIVE RETURNS                                               |
|  [Line chart: strategy vs benchmark, regime shading]              |
|                                                                   |
+------------------------------------------------------------------+
|  DRAWDOWN                          |  MONTHLY RETURNS HEATMAP    |
|  [Fill chart, annotate max DD]     |  [Year x Month grid]        |
|                                    |  Jan Feb Mar ... Dec  Year  |
|                                    |  1.2 -0.3 2.1 ...    12.4  |
+------------------------------------+-----------------------------+
|  RETURN DISTRIBUTION               |  ROLLING SHARPE (252d)      |
|  [Histogram + VaR lines]           |  [Line + zero reference]    |
+------------------------------------+-----------------------------+
|  Footer: Data source | Methodology notes | Disclaimers            |
+------------------------------------------------------------------+
```

### Factor Tearsheet

For alpha factor evaluation:

```
+------------------------------------------------------------------+
|  FACTOR: momentum_12m_1m               Universe: SP500            |
+------------------+-------------------+---------------------------+
|  IC SUMMARY      |  TURNOVER         |  IC TERM STRUCTURE        |
|  Mean IC   0.035 |  Monthly    42%   |  [Heatmap: horizon x lag] |
|  IC IR     0.45  |  Annual    180%   |                           |
|  Hit Rate   58%  |  Avg Hold   2.3mo |                           |
+------------------+-------------------+---------------------------+
|  QUINTILE RETURNS (annualized)                                    |
|  [Bar chart: Q1 through Q5, long-short spread annotated]          |
+------------------------------------------------------------------+
|  CUMULATIVE FACTOR RETURNS          |  IC TIME SERIES             |
|  [Line: long-short, long, short]    |  [Line + 12mo rolling avg]  |
+------------------------------------+-----------------------------+
|  SECTOR EXPOSURE                    |  FACTOR CORRELATION MATRIX  |
|  [Stacked bar by quintile]          |  [Heatmap, masked upper]    |
+------------------------------------+-----------------------------+
```

### Multi-Strategy Comparison

Side-by-side strategy comparison:

```
+------------------------------------------------------------------+
|  STRATEGY COMPARISON                        Period: 2015-2024     |
+------------------------------------------------------------------+
|  METRICS TABLE                                                    |
|  ┌──────────┬────────┬────────┬────────┬────────┐                |
|  │ Metric   │ Strat A│ Strat B│ Strat C│ Bench. │                |
|  ├──────────┼────────┼────────┼────────┼────────┤                |
|  │ Return   │  12.3% │   9.8% │  15.1% │   8.2% │  ← best bold |
|  │ Vol      │  14.5% │  11.2% │  18.3% │  16.0% │                |
|  │ Sharpe   │  0.85  │  0.88  │  0.82  │  0.51  │  ← best bold |
|  │ Max DD   │ -18.2% │ -12.5% │ -24.1% │ -33.9% │                |
|  └──────────┴────────┴────────┴────────┴────────┘                |
+------------------------------------------------------------------+
|  CUMULATIVE RETURNS (all strategies overlaid)                     |
+------------------------------------------------------------------+
|  ROLLING 1Y SHARPE                  |  DRAWDOWN COMPARISON        |
+------------------------------------+-----------------------------+
|  CORRELATION MATRIX                 |  MONTHLY RETURN SCATTER     |
|  [Strategy x Strategy]              |  [Strat A vs Strat B]       |
+------------------------------------+-----------------------------+
```

## Implementation

### Page Setup

```python
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from ml4t.style import COLORS, ml4t_palette, GRAYSCALE

# A4 landscape for single-page tearsheets
fig = plt.figure(figsize=(16.5, 11.7), dpi=150)
fig.set_facecolor('white')

# GridSpec for precise layout control
gs = GridSpec(4, 3, figure=fig,
             hspace=0.35, wspace=0.3,
             left=0.05, right=0.95,
             top=0.92, bottom=0.05)

# Header spans full width
ax_header = fig.add_subplot(gs[0, :])
ax_header.axis('off')

# Metric panels
ax_cumret = fig.add_subplot(gs[1, :])          # Full width
ax_dd     = fig.add_subplot(gs[2, :2])          # 2/3 width
ax_monthly= fig.add_subplot(gs[2, 2])           # 1/3 width
ax_dist   = fig.add_subplot(gs[3, 0])           # 1/3 width
ax_sharpe = fig.add_subplot(gs[3, 1])           # 1/3 width
ax_table  = fig.add_subplot(gs[3, 2])           # 1/3 width
```

### Key Metrics Panel

```python
def render_metrics_panel(ax, metrics: dict, title: str = "KEY METRICS"):
    """Render a metrics panel with label-value pairs.

    Args:
        metrics: {"Ann. Return": "12.3%", "Sharpe": "0.85", ...}
    """
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Title bar
    ax.text(0.5, 0.95, title, transform=ax.transAxes,
            fontsize=10, fontweight='bold', ha='center', va='top',
            color=COLORS['blue'])
    ax.axhline(y=0.90, xmin=0.05, xmax=0.95,
               color=COLORS['amber'], linewidth=2)

    # Metrics rows
    y = 0.82
    for label, value in metrics.items():
        ax.text(0.08, y, label, fontsize=9, color=COLORS['neutral'],
                va='center')
        ax.text(0.92, y, str(value), fontsize=9, fontweight='semibold',
                color=COLORS['blue'], ha='right', va='center',
                fontfamily='monospace')
        y -= 0.12
```

### Monthly Returns Heatmap

```python
def render_monthly_heatmap(ax, returns: pd.Series):
    """Render year x month returns heatmap."""
    monthly = returns.resample('M').sum()
    table = monthly.groupby([monthly.index.year, monthly.index.month]).first().unstack()

    # Use diverging colormap centered at 0
    vmax = max(abs(table.min().min()), abs(table.max().max()))
    im = ax.imshow(table.values, cmap='RdYlGn', vmin=-vmax, vmax=vmax,
                   aspect='auto')

    # Annotate cells with values
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            val = table.iloc[i, j]
            if pd.notna(val):
                color = 'white' if abs(val) > vmax * 0.6 else COLORS['neutral']
                ax.text(j, i, f"{val:.1%}", ha='center', va='center',
                       fontsize=7, color=color, fontfamily='monospace')

    ax.set_xticks(range(12))
    ax.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'], fontsize=8)
    ax.set_yticks(range(len(table.index)))
    ax.set_yticklabels(table.index, fontsize=8)
    ax.set_title("Monthly Returns", fontsize=10, fontweight='semibold',
                 color=COLORS['blue'])
```

### Header Block

```python
def render_header(fig, name, subtitle, period, benchmark=None):
    """Render tearsheet header with title and metadata."""
    # Strategy name — large, deep blue
    fig.text(0.05, 0.97, name, fontsize=18, fontweight='bold',
             color=COLORS['blue'], va='top')

    # Subtitle
    fig.text(0.05, 0.94, subtitle, fontsize=10,
             color=COLORS['neutral'], va='top')

    # Period and date — right aligned
    fig.text(0.95, 0.97, f"Period: {period}", fontsize=9,
             color=COLORS['neutral'], ha='right', va='top')
    fig.text(0.95, 0.945, f"Generated: {pd.Timestamp.now():%Y-%m-%d}",
             fontsize=8, color=COLORS['silver_muted'], ha='right', va='top')

    if benchmark:
        fig.text(0.95, 0.92, f"Benchmark: {benchmark}", fontsize=8,
                 color=COLORS['neutral'], ha='right', va='top')

    # Amber rule line under header
    line = plt.Line2D([0.05, 0.95], [0.915, 0.915],
                      transform=fig.transFigure,
                      color=COLORS['amber'], linewidth=2)
    fig.add_artist(line)
```

### Footer Block

```python
def render_footer(fig, data_source, notes=None, disclaimer=None):
    """Render tearsheet footer."""
    footer_y = 0.02
    fig.text(0.05, footer_y, f"Data: {data_source}", fontsize=7,
             color=COLORS['silver_muted'])
    if notes:
        fig.text(0.50, footer_y, notes, fontsize=7,
                 color=COLORS['silver_muted'], ha='center')
    if disclaimer:
        fig.text(0.95, footer_y, disclaimer, fontsize=6,
                 color=COLORS['silver_muted'], ha='right', style='italic')
```

## PDF Output

```python
from matplotlib.backends.backend_pdf import PdfPages

# Single tearsheet
fig.savefig("strategy_tearsheet.pdf", dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')

# Multi-page report
with PdfPages("full_report.pdf") as pdf:
    pdf.savefig(strategy_fig, dpi=150, facecolor='white')
    pdf.savefig(factor_fig, dpi=150, facecolor='white')
    pdf.savefig(comparison_fig, dpi=150, facecolor='white')

    # Metadata
    d = pdf.infodict()
    d['Title'] = 'Strategy Performance Report'
    d['Author'] = 'ML4T Framework'
    d['CreationDate'] = pd.Timestamp.now()
```

## Visual Standards for Tearsheets

### Typography Hierarchy

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Strategy name | 18pt | Bold | `blue` |
| Section header | 10pt | Bold | `blue` |
| Metric label | 9pt | Regular | `neutral` |
| Metric value | 9pt | Semibold, mono | `blue` |
| Axis labels | 8-9pt | Regular | `neutral` |
| Cell values | 7pt | Regular, mono | varies |
| Footer | 7pt | Regular | `silver_muted` |

### Conditional Formatting

- Positive returns: `COLORS['positive']` (#10b981)
- Negative returns: `COLORS['negative']` (#ef4444)
- Best-in-class metric: **bold** + `COLORS['blue']`
- Below-threshold metric: `COLORS['negative']` + italic
- Neutral / benchmark: `COLORS['neutral']`

### Density Guidelines

- Strategy tearsheet: 15-20 data elements on one page
- Factor tearsheet: 12-16 data elements
- Comparison: metrics table + 4 chart panels
- Never more than 6 chart panels per page
- Metric tables: max 8 rows, keep them scannable

### Print Checklist

- [ ] All text readable at 100% zoom on A4
- [ ] No text smaller than 7pt
- [ ] Grayscale test passes (markers + linestyles distinguish series)
- [ ] Margins safe for binding (left margin 15mm+)
- [ ] No colored backgrounds that waste toner
- [ ] Amber accent line visible in grayscale (~65% gray)
- [ ] PDF metadata populated (title, author, date)

---

*A tearsheet is a persuasion document. The data makes the argument; the design makes it effortless to follow.*
