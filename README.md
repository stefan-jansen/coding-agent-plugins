# coding-agent-plugins

Plugin marketplace for [coding-agent-toolkit](https://github.com/stefan-jansen/coding-agent-toolkit).

Provides a small set of workflow, memory, and code-quality plugins for Claude Code. Each plugin is a directory with a `plugin.json` and its own README documenting the skills/commands it ships.

## Getting started

### 1. Clone the marketplace

```bash
git clone git@github.com:stefan-jansen/coding-agent-plugins.git ~/path/to/coding-agent-plugins
```

### 2. Register it and enable plugins

```bash
cd ~/path/to/coding-agent-plugins
scripts/enable.sh                    # workflow, memory, transition, development, system
scripts/enable.sh workflow memory    # or pick your own set
scripts/enable.sh --list             # show what is enabled
```

The script merges into `~/.claude/settings.json`, so the plugins are on in every project on this machine and no project repo carries agent config. It is idempotent and backs the file up before its first change. To do it by hand, or to scope plugins to one project instead, see [Where to enable](#where-to-enable).

### 3. Restart Claude Code

Plugins, their hooks, and settings are read at session start and are not hot-reloaded. Restart the session (or `Cmd/Ctrl+Shift+P → Claude Code: Restart` in VS Code) after enabling a plugin or editing one.

## Plugins

**Foundation** — generic infrastructure most projects want:

| Plugin | Ships | Description |
|---|---|---|
| `workflow` | `/align` `/plan` `/plan-issues` `/next-issue` `/ship` `/handoff` `/continue` `/delegate` `/next` `/work` `/spike` | Structured task execution — spec → issues → implement → deliver, plus session handoffs |
| `memory` | `/memory-gc` `/memory-review` `/memory-update` `/index` `/performance` | Persistent project memory under a token budget |
| `transition` | PreCompact / PostCompact / SessionEnd hooks | Write a session summary to `.workspace/transitions/YYYY-MM-DD/HHMMSS.md` on every compaction |
| `development` | `/analyze` `/review` `/test` `/fix` `/git` `/docs` | Code analysis, review, TDD, debugging |
| `system` | `/audit` `/cleanup` `/status` | Framework health, cleanup, unified status view |
| `setup` | `/setup` `/setup:user` | Project initialization (interview-driven) + global user config — enable once, disable after |
| `codex` | `/codex:*` commands | Delegate work to OpenAI Codex from Claude Code |
| `roborev` | SessionStart summary | Open roborev review status for the current branch |

**Extras** — additional plugins registered in the manifest:

| Plugin | Description |
|---|---|
| `observer` | Cross-session memory via batched `claude -p` observation processing |

Every plugin directory has its own README with skill/command details.

## Where to enable

Claude Code merges `enabledPlugins` from `~/.claude/settings.json` and from a project's `.claude/settings.json`, so a plugin can be turned on at either level. Pick one level per plugin; listing the same plugin in both is redundant, and the duplicate entries drift.

**User level (`~/.claude/settings.json`)** is the default and what `scripts/enable.sh` writes. One entry covers every project on the machine, and project repos stay free of agent config. It is per-machine, so carry it to another machine by syncing `~/.claude/settings.json` with your dotfiles or by re-running `scripts/enable.sh` there.

**Project level (`.claude/settings.json`)** is for a plugin only one project needs, or when the enablement should travel in git so collaborators and CI get it without a setup step. Same JSON, written to the project instead:

```json
{
  "extraKnownMarketplaces": {
    "local": {
      "source": {
        "source": "directory",
        "path": "/absolute/path/to/coding-agent-plugins"
      }
    }
  },
  "enabledPlugins": {
    "workflow@local": true,
    "memory@local": true
  }
}
```

Hooks are plugin-level: enabling a plugin anywhere activates its hooks in every session that resolves it. `@local` names only resolve where the marketplace is registered, so a project entry is inert on a machine without this clone.

## Using the skills from Codex

A `SKILL.md` is plain markdown, so the same file works for Claude Code and for OpenAI Codex. The two discover skills differently: Claude Code reads a plugin's `plugin.json`, while Codex scans `~/.codex/skills/<name>/SKILL.md`. Nothing bridges the namespaces on its own, so a skill added to a plugin stays invisible to Codex until it is linked.

```bash
scripts/sync-codex-skills.sh            # link every declared skill into ~/.codex/skills/
scripts/sync-codex-skills.sh --check    # report drift, nonzero exit if any
```

It links rather than copies, so one edit changes the skill for both agents with no re-sync. Only symlinks pointing back into a marketplace are created, repointed, or removed; a real directory or a link aimed anywhere else is reported and left alone, so Codex's own skills and any hand-written ones survive. Skill names have to be unique across the marketplaces, because Codex's namespace is flat; a collision is an error rather than a silent overwrite. With Codex not installed the script is a no-op, so the `--check` hook does not block contributors who only use Claude Code.

## Troubleshooting

**Commands not appearing after enabling a plugin.** Restart Claude Code; plugins are resolved at session start.

**A skill works in Claude Code but Codex does not know it.** Run `scripts/sync-codex-skills.sh`. See [Using the skills from Codex](#using-the-skills-from-codex).

**An edit to a plugin file has no effect.** A `directory` marketplace is read in place, with no copy and no cache, so the edit is already live for every project that enables the plugin — but only from the next session. Restart or resume.

**Marketplace not found.** Verify the `path` in `extraKnownMarketplaces` points at the directory containing `.claude-plugin/marketplace.json` (i.e., the repo root of this clone). `scripts/enable.sh` writes an absolute path for you.

**A plugin is on in a project you did not enable it in.** Check both levels: `scripts/enable.sh --list` for the user level, and the project's `.claude/settings.json`. Enablement is the merge of the two.

## License

MIT
