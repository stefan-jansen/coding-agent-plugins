---
name: quant-viz
description: This skill should be used when the user asks to "create a chart", "plot this data", "visualize results", "make a figure", "improve this plot", "publication-quality chart", or when creating matplotlib/plotly visualizations for quantitative finance data.
version: 1.0.0
---

# Quantitative Visualization Standards

Publication-quality standards for financial data visualization. Every chart must be **intentional, information-dense, and visually distinctive** — not generic matplotlib defaults.

## Before You Plot: The Three Questions

1. **What is the single insight?** If the chart doesn't answer one clear question, it shouldn't exist. Multi-panel figures are fine, but each panel has one job.

2. **Who reads this?** Book figure (must work in grayscale print), interactive dashboard (hover data matters), notebook exploration (speed over polish), or presentation (large labels, minimal detail).

3. **What's the data density?** A scatter of 50 points and a heatmap of 10,000 cells need completely different approaches. Match the technique to the data, not the other way around.

## The ML4T Style System

All visualizations must use the established ML4T identity:

```python
from ml4t.style import COLORS, ml4t_palette, ml4t_diverging

# Matplotlib: automatic via matplotlibrc (no imports needed for basic style)
# Plotly: pio.templates.default = "ml4t" (auto-registered on import)

# Book context only (third-edition):
# from utils.style import save_figure
```

### Color Rules

| Use Case | Colors | Why |
|----------|--------|-----|
| Primary data series | `COLORS['blue']` (#0a1628) | Deep, authoritative, prints dark |
| Highlight / accent | `COLORS['amber']` (#D4A84B) | Warm contrast, draws the eye |
| Positive returns | `COLORS['positive']` (#10b981) | Semantic green |
| Negative returns | `COLORS['negative']` (#ef4444) | Semantic red — use sparingly |
| Secondary series | `COLORS['slate']` (#1a2d4a) | Distinct from primary |
| Grid / borders | `COLORS['silver_muted']` (#e8e8e6) | Recede, don't compete |

**Never**: rainbow colormaps for sequential data, red-green for colorblind users without redundant encoding, more than 6 colors in one chart.

**Always**: `ml4t_palette(n, categorical=True)` for categories, `ml4t_diverging()` for positive/negative splits.

### Typography

- Titles: 14pt, semibold, `COLORS['blue']`
- Axis labels: 11pt, sentence case ("Forward returns (%)" not "FORWARD RETURNS (%)")
- Tick labels: 10pt
- Annotations: 9pt, with subtle background box
- Font: DM Sans (auto via matplotlibrc), fallback DejaVu Sans

## Static Figures (Matplotlib)

### Layout Principles

- **Remove chart junk**: no top/right spines (automatic), no unnecessary gridlines, no 3D when 2D works
- **Aspect ratios**: time series = wide (12, 5), comparison = square (8, 8), multi-panel = constrained_layout
- **White space is data**: tight but not cramped — `pad_inches=0.1`, `labelpad=8`, `titlepad=12`

### Chart Type Selection

| Data Pattern | Chart Type | Not This |
|-------------|-----------|----------|
| Time series (1-3 lines) | Line plot, regime shading | Bar chart |
| Time series (many assets) | Heatmap or small multiples | Spaghetti plot |
| Distribution | Histogram + KDE, violin | Pie chart |
| Correlation matrix | Clustered heatmap, mask upper tri | Full symmetric heatmap |
| Feature importance | Horizontal bar, sorted | Vertical unsorted bars |
| Returns by period | Heatmap calendar | Line plot |
| Model comparison | Grouped bar or dot plot | Stacked bar |
| Risk/return tradeoff | Scatter with Sharpe isolines | Plain scatter |
| IC decay | Line with confidence band | Points only |

### Annotations That Add Value

```python
from ml4t.style import annotate_peak, add_regime_shading, format_pct_axis

# Mark crises — context that explains the data
add_regime_shading(ax, [('2008-09', '2009-03'), ('2020-02', '2020-04')])

# Annotate peaks — draw attention to what matters
annotate_peak(ax, peak_date, peak_val, f"Peak: {peak_val:.1%}")

# Format axes — make numbers readable
format_pct_axis(ax, 'y')
```

### Multi-Panel Figures

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)

# Each panel has: title, clear axis labels, shared legend if applicable
# Use fig.suptitle() for overall title, ax.set_title() for panel titles
# Letter labels (a), (b), (c) for paper figures
for i, ax in enumerate(axes.flat):
    ax.text(-0.1, 1.05, f"({chr(97+i)})", transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='top')
```

### Grayscale Compatibility (Book Figures)

Book figures MUST be readable in grayscale print:
- Use markers + linestyles to distinguish series, not just color
- Reference `GRAYSCALE` dict for gray equivalents
- Test: `fig.savefig('test.png', cmap='gray')`
- Hatching patterns for filled areas: `ax.fill_between(..., hatch='//')`

### Save Convention

```python
# Book context (third-edition):
# from utils.style import save_figure
# save_figure(fig, "figure_11_3_ic_decay", chapter="11_ml_pipeline", formats=["png", "pdf"])

# General context:
fig.savefig("figure_name.png", dpi=150, bbox_inches="tight", facecolor="white")
fig.savefig("figure_name.pdf", bbox_inches="tight", facecolor="white")
```

## Interactive Figures (Plotly)

### When to Use Plotly Over Matplotlib

- User needs to hover for exact values
- Data has 100+ series (use dropdown/slider to filter)
- Exploring relationships interactively (zoom, pan)
- Dashboard components
- HTML report output

### Plotly Standards

```python
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "ml4t"  # Auto-registered

fig = go.Figure()

# Consistent hover format
fig.update_traces(
    hovertemplate="Date: %{x}<br>Return: %{y:.2%}<extra></extra>"
)

# Meaningful layout
fig.update_layout(
    title=dict(text="Strategy Performance", font_size=16),
    xaxis_title="Date",
    yaxis_title="Cumulative Return",
    yaxis_tickformat=".0%",
    height=500,
    margin=dict(l=60, r=20, t=60, b=40),
)
```

### Interactive Enhancements

- **Range slider** for time series: `fig.update_xaxes(rangeslider_visible=True)`
- **Dropdown filters** for multi-asset: `updatemenus` with visibility toggles
- **Linked axes** for multi-panel: `fig = make_subplots(shared_xaxes=True)`
- **Custom hover**: show context (date, asset, value, percentile rank)

### Plotly Anti-Patterns

- Don't use Plotly Express defaults (they ignore the ML4T template)
- Don't set `template="plotly_white"` — use `"ml4t"`
- Don't use `fig.show()` in scripts — use `fig.write_html()` or `pio.write_json()`
- Don't create interactive charts that could be static — interactivity must earn its complexity

## Quant-Specific Patterns

### Returns Visualization

```python
# Cumulative returns: always start at 0 or 1 (be explicit)
cumulative = (1 + returns).cumprod() - 1  # Start at 0
# OR
cumulative = (1 + returns).cumprod()  # Start at 1 (wealth growth)

# Drawdown: always negative, use fill_between
drawdown = cumulative / cumulative.cummax() - 1
ax.fill_between(drawdown.index, drawdown, 0, alpha=0.3, color=COLORS['negative'])
```

### Risk Metrics Display

- Sharpe ratio: annotate on chart, not just in title
- Drawdown: fill area, annotate max drawdown date and recovery
- Volatility: rolling window with confidence band
- VaR/CVaR: vertical lines on return distribution

### Factor Analysis

- IC heatmap: features x horizons, diverging colormap, annotate values
- Factor returns: cumulative line with turnover on secondary axis
- Quintile spread: bar chart with error bars from bootstrap

## The Quality Test

Before finalizing any visualization:

- [ ] Does the title state the insight, not describe the chart? ("Model alpha decays after 10 days" not "IC by horizon")
- [ ] Are axes labeled with units? ("Return (%)" not "return")
- [ ] Does it work without color? (grayscale test for print)
- [ ] Is the data-ink ratio high? (no chartjunk)
- [ ] Would a domain expert find this informative? (not just pretty)
- [ ] Is the code reproducible? (`save_figure()` called, random seeds set)

---

*The best quant chart is one where the methodology is invisible and the insight is obvious.*
