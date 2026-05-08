# Conventions

## Code

- Formatting: (e.g., ruff, prettier, gofmt)
- Naming: (e.g., snake_case for Python, camelCase for JavaScript)
- Import order: (e.g., standard lib → third party → local)

## Data

- (Where generated artifacts live; what's committed; stable IDs.)

## Testing

- Test file naming: (e.g., test_*.py, *.test.js)
- Test organization: (e.g., mirrors src/ structure)
- Coverage requirements: (e.g., minimum 80%)

## Commits

- Use `git safe-commit -m "..."` so pre-commit hooks run. Never `--no-verify`.
- Conventional-commit style: `feat:`, `fix:`, `chore:`, `docs:`. Scope optional: `fix(quality): ...`.
- Co-author tag for AI-assisted commits.

## Infrastructure

- Memory + transitions live at `.agents/` (shared by Claude and Codex). NOT `.claude/memory/`.
- `.claude/` holds only Claude-specific config: `settings.json`, `hooks/`, `commands/`. Different schema from Codex; can't be unified.
- Every project session writes progress to `.agents/transitions/YYYY-MM-DD/HH.md`.
