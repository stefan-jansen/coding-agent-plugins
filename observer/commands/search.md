# /observer:search

Search past session observations across all projects.

## Usage

```
/observer:search <query> [--project <name>] [--type <type>] [--limit <n>]
```

## Arguments

- `query` (required) — Search text (matched against titles, narratives, facts)
- `--project` — Filter to a specific project
- `--type` — Filter by type: action, discovery, decision, bugfix, feature, refactor
- `--limit` — Max results (default: 20)

## Process

1. Run the search script:
```bash
python3 ~/applied-ai/claude-code-toolkit/plugins/observer/scripts/search.py "$QUERY" $ARGS
```

2. Present results to the user with observation details.

## Examples

```
/observer:search "authentication"
/observer:search "SQLite schema" --project factory
/observer:search "bug" --type bugfix --limit 5
```

## Database

Searches `~/.claude-toolkit/observer/observer.db` using SQLite FTS5 full-text search.
If no database exists, prompt user to complete at least one session with observer hooks enabled.
