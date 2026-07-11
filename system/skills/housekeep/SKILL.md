---
name: housekeep
description: This skill should be used when the user asks to "housekeep", "sweep stray transition dirs", "clean up agent-infra debris", "find misplaced .workspace or .claude dirs", or when auditing project trees for the class of debris caused by hooks writing to the wrong project root (nested repos, worker-pool worktrees, stub-only session files, doubled path prefixes). Do NOT use for general project cleanup (see `/system:cleanup`) or for memory garbage collection (see `/memory-gc`).
disable-model-invocation: false
user-invocable: true
---

# `/housekeep` — sweep stray agent-infra debris

Enumerates `.workspace/` and `.claude/` directories under a set of roots, classifies each
as *expected* or *buggy*, presents a proposed sweep as a dry-run, applies on approval.

Companion to `/memory-gc` (which curates memory entries) and `/system:cleanup` (which
consolidates reports and misplaced files). This skill is narrowly about **agent-infra
directories placed where hooks shouldn't have written them**.

## When to invoke

- After fixing a hook that resolves the project root incorrectly (the canonical trigger).
- Periodically — debris accumulates silently. Run monthly, or when a project's tree feels
  cluttered.
- When onboarding a new project onto the `.workspace/`-interop layout, to catch legacy
  `.claude/transitions/` scatter before it compounds.

## Classes (mutually exclusive; first match wins)

| Class | Rule | Cleanup safety |
|---|---|---|
| `DOUBLED` | path contains `.workspace/.workspace/` or `.claude/.claude/` | **safe — always prune** |
| `NESTED_IN_AGENT` | agent dir inside another agent dir | **safe — always prune** |
| `WORKER_POOL` | path under `/.claude/worktrees/` (disposable worker worktrees) | age-threshold prune |
| `SUBREPO_STRAY` | inside a git worktree or nested repo, not at project root | prune after hook fix |
| `STUB_ONLY` | ≥80% of `.md` files are stub `Session Progress` / `Session ended` only | age-threshold prune |
| `OLD_DEBRIS` | newest file >30d old, ≤3 files total | age-threshold prune |
| `EXPECTED` | sits at a real project root | leave |
| `EXPECTED_FIXTURE` | under `/fixtures/`, `/tests/`, `/evals/`, `/.archive/`, `/demo-project/`, `/skill-compiler/` | leave |

## Usage

```bash
/housekeep                                        # default: dry-run on current project's tree
/housekeep --roots ~/projects ~/agents ~/clients  # cross-project sweep, dry-run
/housekeep --execute                              # apply after confirmation (interactive)
/housekeep --execute --auto                       # apply without confirmation (scripted)
/housekeep --severity safe                        # only show DOUBLED + NESTED_IN_AGENT
/housekeep --stub-age-days 60                     # tune the age threshold
/housekeep --json                                 # machine-readable dry-run
```

Defaults are chosen so the common `/housekeep` invocation is always safe: it writes
nothing. Explicit `--execute` is required to touch the filesystem.

## Plan (Claude executes)

1. **Locate the scan script** — `${CLAUDE_PLUGIN_ROOT}/skills/housekeep/scan.py`.
   Fallback: `~/agents/coding/plugins/system/skills/housekeep/scan.py`.

2. **Choose roots**. If the user passed `--roots`, use those. Otherwise default to the
   current project's root (`${CLAUDE_PROJECT_DIR:-$(pwd)}`). Cross-project sweeps must
   be explicit — do not silently walk the whole home dir.

3. **Run the scan (dry-run)**:
   ```bash
   python3 "$SCAN" --roots <roots...> [--severity ...] [--stub-age-days ...]
   ```
   Show the output. Sort by severity: DOUBLED and NESTED_IN_AGENT first (safe), then
   SUBREPO_STRAY, WORKER_POOL, STUB_ONLY, OLD_DEBRIS.

4. **Decide based on flags**:
   - No `--execute`: stop here. This is the dry-run.
   - `--execute` without `--auto`: present the proposed `rm -rf` list explicitly and ask
     "Prune N dirs (X safe, Y review-required)? (y/N)". Abort on anything but `y`.
   - `--execute --auto`: skip confirmation. Only prune classes with severity `safe`
     (DOUBLED, NESTED_IN_AGENT) unless the user passes `--include-review` to widen.

5. **Apply** with a per-dir `rm -rf`. Never delete a dir whose enclosing project has
   uncommitted changes touching that dir — `git status --porcelain` on the enclosing
   project must return no lines matching the target path. Log every deletion to
   `.workspace/memory/housekeep_history.md` (append-only, one line per deletion:
   `TS class path`).

6. **Summarize** for the user:
   - Number pruned by class.
   - Any deletions the user should double-check (WORKER_POOL and OLD_DEBRIS categories
     lean cautious — call these out).
   - Suggest a re-run of the dry-run to confirm zero remaining.

## Safety invariants

- **Never** delete `EXPECTED` or `EXPECTED_FIXTURE`.
- **Never** delete a directory whose enclosing project has uncommitted changes
  touching that directory.
- **Never** delete without either a dry-run first *or* `--auto`.
- `.workspace/memory/housekeep_history.md` records everything pruned. Append-only.
- The propose-then-apply pattern mirrors `/memory-gc` — same discipline, different
  substrate.

## Notes

- The scan skips `node_modules`, `.git/objects`, `.venv`, `target`, `dist`,
  `__pycache__`, `.next`, `.cache`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`,
  `build`. Add more via editing `SKIP_DIRS` in `scan.py`.
- Classification is intentionally shallow — this is not a memory-content analyzer.
  Deep-content is the domain of `/memory-gc`.
- If the transition plugin's hook resolver bug (`git rev-parse --show-toplevel` in
  nested repos) is unfixed on the target machine, `SUBREPO_STRAY` will repopulate.
  Fix the hook first (upgrade to `transition@1.1.1+`).
