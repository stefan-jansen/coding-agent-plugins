#!/bin/bash
# SessionStart hook: print one line if there are open roborev reviews on the
# current branch, silent otherwise.
#
# Acceptance:
#   - silent when `roborev` not on PATH
#   - silent when 0 open reviews
#   - silent on any failure (timeout, daemon down, parse error)
#   - prints exactly: `roborev: N open reviews on <branch>` when N > 0
#   - completes in ≤300ms common case (500ms inner timeout, 1s outer in hooks.json)

set -u

# Stay silent on any failure path.
trap 'exit 0' ERR

command -v roborev >/dev/null 2>&1 || exit 0

# Read SessionStart payload from stdin (we only need cwd; fall back to $PWD).
PAYLOAD="$(cat 2>/dev/null || true)"
CWD="${CLAUDE_PROJECT_DIR:-${PWD:-.}}"
if command -v python3 >/dev/null 2>&1 && [ -n "$PAYLOAD" ]; then
  PARSED_CWD="$(printf '%s' "$PAYLOAD" \
    | python3 -c 'import json,sys
try:
  d=json.load(sys.stdin)
  v=d.get("cwd") if isinstance(d,dict) else None
  print(v if isinstance(v,str) else "")
except Exception:
  print("")' 2>/dev/null)"
  [ -n "$PARSED_CWD" ] && CWD="$PARSED_CWD"
fi

cd "$CWD" 2>/dev/null || exit 0

# Resolve current branch (silent if not in a repo or detached HEAD with no name).
BRANCH="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
[ -z "$BRANCH" ] && exit 0

# Query the daemon with a short inner timeout. JSON output keeps parsing robust.
JSON="$(timeout 0.5 roborev list --open --json --limit 5 --branch "$BRANCH" 2>/dev/null || true)"
[ -z "$JSON" ] && exit 0

# Count the open reviews. Use python3 for resilient JSON parsing.
COUNT="$(printf '%s' "$JSON" \
  | python3 -c 'import json,sys
try:
  d=json.load(sys.stdin)
  if isinstance(d,list):
    print(len(d))
  elif isinstance(d,dict):
    for k in ("jobs","reviews","items","data"):
      v=d.get(k)
      if isinstance(v,list):
        print(len(v)); break
    else:
      print(0)
  else:
    print(0)
except Exception:
  print(0)' 2>/dev/null)"

[ -z "$COUNT" ] && exit 0
case "$COUNT" in
  ''|*[!0-9]*) exit 0 ;;
esac
[ "$COUNT" -gt 0 ] || exit 0

printf 'roborev: %s open review%s on %s\n' \
  "$COUNT" \
  "$([ "$COUNT" -eq 1 ] && echo '' || echo 's')" \
  "$BRANCH"
