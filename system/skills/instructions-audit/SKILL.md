---
name: instructions-audit
description: This skill should be used when the user asks to "audit my instructions", "audit AGENTS.md", "audit CLAUDE.md", "trim my instruction files", "why is Claude ignoring a rule", "check my agent instructions", or when instruction files have grown to the point that specific rules are being missed. Finds instruction content that never reaches the model, and rules that reach it but get lost in the volume. Proposes replacement text and applies only what is approved. Do NOT use for memory garbage collection (see `/memory-gc`) or for stray agent-infra directories (see `/housekeep`).
disable-model-invocation: false
user-invocable: true
---

# `/instructions-audit` - keep instruction files lean and actually read

Two failures cost the same thing and look nothing alike:

- **A rule is loaded and ignored.** Upstream states the mechanism plainly:
  "Bloated CLAUDE.md files cause Claude to ignore your actual instructions",
  and "If Claude keeps doing something you don't want despite having a rule
  against it, the file is probably too long and the rule is getting lost."
- **Content is written and never loaded.** An auto-memory directory with no
  index, an `@`-import pointing at a file that no longer exists, a
  `.claude/rules/` file scoped to paths the repo does not have.

This skill finds both, proposes specific replacement text, and applies only
what the user approves. It never edits before approval.

## Authority

The rules are **not this skill's opinion**. They come from
`~/.claude/reference/docs/best-practices.md`, section *"Write an effective
CLAUDE.md"* - the include/exclude table, the removal test ("For each line, ask:
would removing this cause Claude to make mistakes? If not, cut it"), and the
emphasis warning ("If you emphasize many lines, none of them stands out").
Read that section during the run and cite the row you are applying. When
upstream changes, this skill's judgments change with it.

`~/.claude/reference/docs/memory-management.md` is the authority for the
auto-memory layout, the typed frontmatter, and `@`-import rules.

If either page is missing, say so and continue with reduced confidence rather
than substituting house opinion for the vendored text.

## Modes

```bash
/instructions-audit           # this project + its consistency with the user-level file
/instructions-audit --user    # every project's evidence, judging the user-level file alone
```

Two modes on one skill, not two subcommands: they converge on the same report
shape and the same approval loop.

**`--user` proposes no edit to any project file.** It reads across projects to
judge one file, and a change to that file alters behaviour in every session of
every project on both hosts.

## Step 1 - Collect

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/instructions-audit/collect.py" \
    --project "${CLAUDE_PROJECT_DIR:-$(pwd)}" > /tmp/ia.json
# --user mode:
python3 "${CLAUDE_PLUGIN_ROOT}/skills/instructions-audit/collect.py" --user > /tmp/ia.json
```

`collect.py` writes nothing. It emits instruction-file targets with their
symlink chains, the auto-memory inventory, typed feedback memories, and - only
where the feedback corpus is thin - a bounded transcript grep.

**Check the inputs before trusting the verdict.** Report these above the
findings, always:

- `transcript.used` false with reason, or `cap_bound` true (the corpus
  exceeded the extraction cap and the evidence is a sample, not a census).
- Any hit with `filter: "degraded"` - that transcript predates the `origin`
  field, so peer and hook turns were excluded by shape rather than
  structurally, and a stray non-human turn is possible.
- `auto_memory.population.classification` of `unknown`.

An audit run on inputs it never collected reports "nothing found" and "nothing
to find" identically. Say which one it is.

## Step 2 - `/doctor` (Claude only)

Invoke the bundled `/doctor` skill and fold its proposals into category 2,
attributed to it. It already proposes cuts for content derivable from the
codebase; do not reimplement that check. On Codex, skip this step and say in
the report that it was skipped.

## Step 3 - Judge

Four categories. **Every finding carries a source. A finding with no source is
a defect, not a low-confidence finding** - drop it rather than reporting it.

| # | Finding | Required source |
|---|---|---|
| 1 | A rule that exists and got ignored | the evidence: feedback-memory path, or session id + date |
| 2 | Content the include/exclude table excludes | the exact table row it fails |
| 3 | A statement the repo now contradicts | the contradicting fact: a path that does not exist, a count that differs |
| 4 | User-level and project-level echo or contradict | both file paths and both line ranges |

Category 1 does not mean the rule should be cut. It usually means the opposite:
the rule is right and is being lost. The fix is to shorten what surrounds it,
move it, or emphasise it - and emphasis only works if few lines carry it.

### The prohibition

**Never propose removing a rule because no violation of it was found.**

Silence is not evidence of disuse. A rule obeyed everywhere generates no
corrections precisely because it is working, so absence of evidence selects for
removing the rules that function best. Every proposed removal cites a row of
the include/exclude table (category 2) or a fact the repo contradicts
(category 3). No exceptions, and no "this appears unused" finding.

### Two more things not to do

- **Do not propose Claude-only content into a shared file.** `AGENTS.md` is
  canonical for both hosts and `CLAUDE.md` is `@AGENTS.md`. Claude-native
  coverage is not grounds for retiring content Codex reads.
- **Do not report a mirrored memory directory as inert.** When
  `population.classification` is `mirrored`, a missing `MEMORY.md` means the
  mirror is missing the index its own mechanism expects - the content is still
  reachable through whatever populates it. Report **"mirror missing its index"**
  (owner: whoever owns the hook) separately from **"content unreachable"**
  (owner: the project). Report off-convention naming separately again: the
  fixes differ.

## Step 4 - Report

Two sections, never merged:

1. **Instruction files.** Findings ordered by blast radius - user-level before
   project-level, because a user-level rule loads in every session of every
   project.
2. **Auto-memory.** Index present and current, naming convention, files absent
   from the index, population classification.

Each finding shows: the file and line range, the category, the source, and the
**exact proposed replacement text**. A removal shows the full text being
removed. Never summarise what would be cut.

Close with the counts and stop. Do not edit anything yet.

## Step 5 - Approve and apply

The user approves per finding, and may approve any subset. Nothing is applied
without an explicit approval naming the findings.

**User-level edits take their own approval, separate from project edits.** The
user-level file is typically a symlink into a dotfiles repo shared with the
other host and the other workstation; an edit there changes behaviour
everywhere.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/instructions-audit/apply.py" <<'JSON'
{"edits": [{"path": "...", "old": "...", "new": "...", "sha256": "...", "finding": "cat2-1"}]}
JSON
```

`apply.py` validates the whole batch first and writes nothing if any edit
fails: with several files, applying one at a time leaves a half-edited set
behind the first failure. It writes to the resolved real path so a symlink is
never replaced by a regular file, and it does not commit.

Commit afterwards with the project's own hooks running. **A failing pre-commit
hook is a stop, not a `--no-verify`** - fix what it caught.

## Idempotency

Re-running proposes nothing already applied. Judge that against the file's
current content, not against a record of what was applied: the second run is
usually a fresh session with no memory of the first. If a proposed edit's
result equals what the file already says, it is not a finding.

## What this does not do

- **Fix the files.** It applies approved edits; a wholesale rewrite of a long
  instruction file is separate work that a first run will scope.
- **Repair auto-memory.** It reports; `/memory-gc` owns the fix.
- **Run unattended.** The approval loop is the point. Never a cron job or a
  timer.
- **Audit settings.** Permissions, hooks and plugin enablement are a different
  audit.
