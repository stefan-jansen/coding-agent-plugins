# Workflow Plugin

Takes a piece of work from a rough request to a merged PR, with the same steps
on Claude Code and OpenAI Codex, and state on disk so either agent can pick up
where the other stopped.

The canonical sources for the seven shared steps live in
[coding-agent-toolkit](https://github.com/stefan-jansen/coding-agent-toolkit);
this plugin is how Claude Code installs them. Each step's `SKILL.md` is its own
documentation, and this file only says what exists and how the pieces fit.

## The pipeline

```
align ──▶ plan ──▶ plan-issues ──▶ next-issue ──▶ ship
spec.md   plan.md   milestone       branch, impl,   squash-merge,
                    + issues        tests, PR       close milestone
```

| Step | Kind | Does |
|---|---|---|
| `/align` | skill | Surveys the repo and prior work read-only, then interrogates you into `spec.md`: a verifiable end-state covering both what you want and what already exists. Give it a brief (`/align @brief.md`) and it only asks what the brief left open. |
| `/plan` | command | Breaks the spec into issue-sized chunks with dependencies, using Claude's plan mode. |
| `/plan-issues` | skill | Creates a GitHub milestone and one issue per chunk. Dry-run unless you pass `--apply`. |
| `/next-issue` | skill | Takes the lowest-numbered open issue in the active milestone: branch, implementation, tests, `Closes #N`, PR. |
| `/ship` | skill | Verifies every milestone issue has a closing-footer commit, squash-merges, confirms the issues auto-closed, closes the milestone. |

`Closes #N` is what makes this bubble up: a merged PR closes its issue, and the
last issue closing closes the milestone. GitHub holds the state; the file each
step writes is the contract the next step reads instead of re-deriving it.

Nothing invokes `/align` on its own. If you want work to start there by
default, say so in your `AGENTS.md`.

## Session continuity

| Step | Kind | Does |
|---|---|---|
| `/handoff` | skill | Writes `.workspace/transitions/YYYY-MM-DD/HHMMSS.md`: a prose summary plus a bash snapshot of read-only checks, each with an inline `# expect:` value. |
| `/continue` | skill | Replays a transition's snapshot, reports what drifted, surfaces next steps. Never auto-executes. |
| `/delegate` | skill | Coordinates your other Claude Code sessions over `ListAgents` / `SendMessage`. Claude-only; Codex has no cross-session messaging, so there is no prompt mirror for it. |

A prose handoff goes stale silently, because the next session cannot tell
whether what it describes is still true. The `# expect:` values are what make
drift visible.

## Local work-unit commands

These are Claude-only and have no Codex mirror. They track work in
`.workspace/work/` rather than on GitHub, for projects that do not use issues.

| Command | Does |
|---|---|
| `/next` | Executes the next task from a local work unit's plan and updates `state.json`. For issue-tracked work use `/next-issue` instead. |
| `/work` | Lists work units, resumes one, saves a checkpoint, switches between them. |
| `/spike` | Time-boxed exploration on a throwaway branch. Reports findings, then you keep or discard the code. |

## Where state lives

| Path | Contents |
|---|---|
| `AGENTS.md` | Project instructions. Codex reads it natively; Claude includes it from a one-line `CLAUDE.md`. |
| `.workspace/work/<unit>/` | `spec.md`, `plan.md`, and the notes for one piece of work. |
| `.workspace/transitions/` | Session handoffs. |
| `.workspace/memory/` | Facts that survive a `/clear`. |

Both agents read these paths natively, which is what makes swapping hosts
mid-feature work. There is deliberately no "run as the other host" command.

Each of the three is relocatable through the `env` block of the project's
`.claude/settings.json` - `CLAUDE_WORK_DIR`, `CLAUDE_TRANSITIONS_DIR`,
`CLAUDE_MEMORY_DIR`, each absolute or relative to the project root:

```json
{"env": {"CLAUDE_WORK_DIR": "work", "CLAUDE_TRANSITIONS_DIR": "transitions"}}
```

`.workspace/` is the default because it keeps agent state out of the way in a
normal codebase. A repo that *is* the agent workspace has no second thing to
stay out of the way of, and should point these at the root. Relocating without
setting the variables does not work: the hooks recreate the default paths.
`bin/test_work_dir.sh` covers the resolution rules.

## Naming

A plugin's skills are namespaced as `/workflow:align`, `/workflow:ship` and so
on. The bare `/align` also works in Claude Code and is what Codex users type,
so this file uses the bare form throughout.
