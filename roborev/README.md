# RoboRev Plugin

**Purpose**: Surface open RoboRev code reviews at session start and wire
`roborev init` into project setup, so the review tool is first-class across
projects that opt in.

This plugin does **not** ship the `roborev` CLI itself (install separately
from <https://github.com/applied-artificial-intelligence/roborev>). It adds:

- A `SessionStart` hook that prints `roborev: N open reviews on <branch>`
  when there are open reviews on the current branch, silent otherwise.
- Setup integration (via the `setup` plugin) that runs `roborev init`
  idempotently and enables `roborev@local` in the project's
  `enabledPlugins`.

Both pieces degrade silently when `roborev` is not on `PATH`.

## Status

`0.1.0` — scaffold only. SessionStart hook and `/setup:*` wiring land in
subsequent milestones (see marketplace epic).

## Hooks

_None yet — to be added in #40 / #41._

## Enable

```jsonc
// .claude/settings.json
{
  "enabledPlugins": {
    "roborev@local": true
    // ...
  }
}
```

Disable freely per-project; nothing else in the marketplace depends on
this plugin.

---

**Version**: 0.1.0
**License**: MIT
