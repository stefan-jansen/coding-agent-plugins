# codex

Delegate work to OpenAI Codex from inside Claude Code. Ships slash commands for review, task delegation, and status/cancellation of running Codex jobs.

## Commands

| Command | Purpose |
|---|---|
| `/codex:review` | Ask Codex to review the current diff |
| `/codex:adversarial-review` | Adversarial review — Codex tries to break the change |
| `/codex:setup` | Configure Codex authentication and defaults |
| `/codex:status` | Show status of running Codex tasks |
| `/codex:result` | Fetch the result of a completed Codex task |
| `/codex:cancel` | Cancel a running Codex task |
| `/codex:rescue` | Recover a stalled Codex session |

## Prerequisites

- OpenAI Codex CLI installed and authenticated (`codex login`).
- Codex plugin enabled in `.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "codex@local": true
  }
}
```

## License

See `LICENSE` and `NOTICE` in this directory (upstream from OpenAI).
