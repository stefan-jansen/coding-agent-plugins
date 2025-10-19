---
title: continue
aliases: [resume]
---

# Continue from Latest Handoff

Automatically loads and continues from the most recent handoff document, with verification.

## Purpose

This command automates the continuation workflow after `/clear` by:
1. Finding the latest handoff via symlink
2. Verifying it points to the actual most recent handoff
3. Reading and loading context
4. Briefing you on what we're continuing from

## Usage

```bash
# After /clear, simply run:
/continue

# That's it - no manual file paths needed
```

## What It Does

### Step 1: Locate Latest Handoff
Checks `.claude/transitions/latest/handoff.md` symlink.

### Step 2: Verify Recency
Confirms the symlink points to the actual newest handoff (not stale).

### Step 3: Load Context
Reads the handoff document and extracts key information.

### Step 4: Brief You
Tells you:
- Which handoff file is being loaded
- Session focus from that handoff
- Active work status
- Main next steps

## Example Output

```
📋 Continuing from: .claude/transitions/2025-10-18_005/handoff.md

Session Focus: Plugin v1.0.0 delivery + web development plugin fix
Active Work: Completed work unit 009, shipped v1.0.0
Next Steps: Applied AI website work

Main Takeaways:
- Plugin architecture refactored to 6 focused plugins
- Web development plugin fixed and ready
- CRITICAL: Context perception error discovered (Claude sees ~66% but actual 103%)
- Custom slash commands broken (bug #8499) - use direct instructions

Ready to continue. What would you like to work on?
```

## Error Handling

If issues detected:
- **Symlink missing**: Creates it pointing to newest handoff
- **Stale symlink**: Updates to point to newest handoff
- **No handoffs found**: Alerts you to create first handoff

## Why This Exists

The `/handoff` command creates handoff documents but doesn't load them - that's intentional separation:
- **Create** (`/handoff`): Save current session state
- **Load** (`/continue`): Resume from saved state

This follows the principle of single responsibility and makes the workflow explicit.

## Typical Workflow

```bash
# End of session (context getting high)
/handoff

# Clear conversation
/clear

# Resume in new session
/continue
```

Clean, simple, explicit.

---

*Companion to `/handoff` - completes the handoff workflow loop*
