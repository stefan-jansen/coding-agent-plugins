---
title: prepare-review
aliases: [review-prep, external-review]
---

# Prepare External Code Review Package

Package codebase for external review using RepoMix.

## Usage

```bash
/development:prepare-review                        # Generic review
/development:prepare-review "API authentication"   # Focused review
```

## Process

1. **Determine Scope**
   - With focus: Select relevant files only
   - No focus: All main source files, exclude tests

2. **Select Files**

   **Include**: Entry points, core logic, API routes, models, key config

   **Exclude**: tests/, node_modules/, venv/, dist/, build/, migrations

3. **Summarize Docs** (if >10k tokens total)
   - README >5k tokens → summarize
   - Multiple specs → combine and summarize

4. **Generate RepoMix Config**
   ```json
   {
     "output": {
       "style": "xml",
       "showLineNumbers": false,
       "removeEmptyLines": true
     },
     "include": ["src/**/*.py", "config.yaml"],
     "ignore": {"useGitignore": true}
   }
   ```

5. **Run RepoMix**
   ```bash
   npx -y repomix --config .repomix/config.json
   ```

6. **Create Package**
   - Location: `.claude/external_reviews/YYYY-MM-DD-HHMM/review_package.md`
   - Contains: Review prompt + docs summary + codebase (RepoMix XML)

## Token Budget

Target: <100,000 tokens total
- Review prompt: ~5k
- Docs summary: ~10k
- Codebase: ~40-80k

## Review Prompt Template

```markdown
# Code Review Request

## Focus Areas
1. Architecture & Design
2. Completeness & Correctness
3. Code Quality & Maintainability
4. Integration & Dependencies
5. Best Practices

## Not Included
- Tests (N files) - excluded for focus
- Build artifacts

## Output Format
1. Executive Summary
2. Critical Issues (must fix)
3. Important Issues (should fix)
4. Minor Issues
5. Positive Observations
```

## If Token Count >100k

Reduce by: narrowing focus, summarizing docs more, excluding utility files
