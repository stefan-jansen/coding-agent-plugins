---
title: "spike"
aliases: ["explore-spike", "prototype"]
---

# Spike - Time-boxed Technical Exploration

Isolated environment for experimental code exploration with automatic cleanup.

## Commands

| Command | Description |
|---------|-------------|
| `/spike start "topic"` | Create spike branch, start timer |
| `/spike start "topic" --duration 60` | Custom duration (minutes) |
| `/spike complete` | Generate findings report |
| `/spike abandon` | Discard and cleanup |
| `/spike status` | Check current spike |

## Process

### Start
1. Create isolated branch: `spike/topic-timestamp`
2. Create tracking file: `.claude/spikes/current.json`
3. Set time box (default: 2 hours)

### During Spike
- Experiment freely, quality doesn't matter
- Try multiple approaches
- Focus on learning
- Document findings as you go

### Complete
1. Generate findings report to `.claude/spikes/report_*.md`
2. Options: keep branch / merge useful code / delete

### Abandon
- Switch to main branch
- Delete spike branch
- Remove tracking file

## Report Structure

```markdown
# Spike Report: [Topic]

## Executive Summary
- What was explored
- Key findings
- Recommendation (proceed/pivot/abandon)

## Technical Findings
- What worked / didn't work
- Performance observations
- Libraries evaluated

## Recommendations
- Suggested approach
- Estimated effort
- Next steps
```

## File Locations

```
.claude/spikes/
├── current.json           # Active spike tracking
├── completed_*.json       # Archived spikes
└── report_*.md           # Spike reports
```

## Guidelines

**DO**: Experiment, break things, time-box strictly, document findings
**DON'T**: Polish code, write tests, exceed time limit
