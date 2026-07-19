# roborev plugin

SessionStart hook that surfaces open [roborev](https://roborev.io) reviews
on the current branch — single line at session start, silent when there
is nothing to surface.

## What it does

On `SessionStart`, runs:

```bash
roborev list --open --json --limit 5
```

and prints **one line only when the count > 0**:

```
roborev: 2 open reviews on feature/short-side-debit
```

The hook is silent when:

- `roborev` is not on `PATH`
- there are 0 open reviews on the current branch
- the daemon is unreachable
- the command takes longer than the timeout

This is the SessionStart hook only. The `roborev init` step that installs
the post-commit reviewer hook is wired into `/setup` (default-Yes opt-in).

## Install

The plugin is registered in the local marketplace. In a project's
`.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "roborev@local": true
  }
}
```

`/setup:*` enables it by default when the user accepts the roborev
opt-in question. To disable per-project, set the value to `false` or
omit the entry.

## Performance budget

The hook script targets ≤300ms wall in the common case. It degrades
silently on timeout (`hooks.json` enforces a 1s outer guard; the script
itself uses a 500ms `timeout` on the `roborev list` invocation).

## Why this is its own plugin

`/setup:*` could shell out to `roborev init` directly without a plugin,
but the SessionStart summary needs a host-managed hook entry. Keeping
both behaviours in one disable-able plugin lets projects opt out cleanly
(e.g. scratch dirs that don't want background reviewers).
