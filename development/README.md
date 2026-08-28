# Development Plugin

Code analysis, review, testing, debugging, documentation and git operations.

Everything here works without MCP servers. Where one is installed it is used
for the same job with fewer tokens; see [MCP tools](#mcp-tools).

## Skills

Claude invokes these on its own when the work matches, or you can call them
directly.

| Skill | Does |
|---|---|
| `/analyze` | Maps an unfamiliar codebase: structure, patterns, components, how the pieces relate. Not for a single file read or a grep. |
| `/review` | Reviews code for bugs and quality problems, by file, directory, or your current changes. |
| `/docs` | Writes and updates project documentation, and fetches documentation for external libraries. |

For review that outlives the session, [roborev](https://github.com/kenn-io/roborev)
is a separate external tool; the `roborev` plugin here only surfaces its open
reviews when a session starts.

## Commands

| Command | Argument | Does |
|---|---|---|
| `/test` | `[tdd]` or a pattern | Test-driven development, running through the test-engineer agent. |
| `/fix` | `[error\|review\|audit\|all] [file/pattern]` | Debugs and applies the fix. |
| `/git` | `commit\|pr\|issue` | Commits, pull requests, issue management. |
| `/prepare-review` | `[focus area]` | Packages the repo for review by an outside tool or person, using RepoMix. Optionally narrowed to one area. Runs `npx repomix`, so it needs Node. |

## Agents

Invoked by the skills and commands above, and available to `Task` directly.

| Agent | For |
|---|---|
| `architect` | System design and architectural decisions. |
| `code-reviewer` | Code review, documentation quality, security audit. |
| `test-engineer` | Test creation and coverage analysis. |

## MCP tools

Optional. Each has a fallback, so nothing here breaks without them.

| Server | Used by | Without it |
|---|---|---|
| `serena` | analyze, review, fix, test-engineer, code-reviewer | Reading files and grep |
| `sequential-thinking` | analyze, review, architect, code-reviewer | The model reasons unaided |
| `context7` | docs | Web search |

## Working with other plugins

| | |
|---|---|
| `workflow` | `/analyze` fits the read-only survey `/align` runs first; `/review` and `/test` fit `/ship`'s checks; `/fix` clears what blocks `/next-issue`. |
| `memory` | `/analyze` findings are worth recording with `/memory-update` when they will outlive the session. |
| `roborev` | Surfaces open roborev reviews for the current branch at session start. |

## Naming

A plugin's commands and skills are namespaced as `/development:analyze` and so
on. The bare form also works and is used throughout this file.
