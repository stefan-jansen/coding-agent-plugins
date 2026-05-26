---
name: system:status
description: Unified view of work, system, and memory state
allowed-tools: [Read, Bash, Glob]
argument-hint: "[verbose]"
---

# System Status

Comprehensive view of work state, git status, and system health.

**Input**: $ARGUMENTS

## Usage

```bash
/status           # Quick overview
/status verbose   # Extended information
```

## Output Sections

### 📋 WORK STATUS
```
🟢 Active: [work-unit-id]
   Phase: exploring|planning|implementing
   Task: TASK-003
   Total units: 5
```

### 🔀 GIT STATUS
```
🌳 Branch: main
📝 Changes: 3 modified, 1 staged, 2 untracked
📥 Last: abc123 - feat: add auth (2 hours ago)
```

### ⚙️ SYSTEM STATUS
```
🏗️  Framework: Claude Code v3.0 ✅
💾 Memory: 5 files, 24KB
```

### 🧠 MEMORY STATUS (verbose only)
```
🔄 Recent updates: 2 files in last hour
🔗 Transitions: 5 saved
```

### 🎯 NEXT STEPS
```
➡️ Continue with: /next
➡️ Commit changes: /git commit
```

## Checks Performed

- Active work unit in `.workspace/work/ACTIVE_WORK`
- Work unit state from `state.json`
- Git branch and changes
- Framework directory structure
- Memory file count and size
