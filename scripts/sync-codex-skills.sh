#!/usr/bin/env bash
set -euo pipefail

# Project the marketplaces' plugin skills into Codex's skills namespace.
#
# Claude Code discovers skills through a plugin's `plugin.json`; Codex discovers
# them by scanning `~/.codex/skills/<name>/SKILL.md`. A SKILL.md is plain
# markdown, so the same file serves both agents. Nothing bridges the two
# namespaces automatically, so a skill added to a plugin stays invisible to
# Codex until someone links it by hand. That is how `deslopify` shipped to
# Claude on 2026-08-17 and reached Codex only after the gap was noticed.
#
# This links rather than copies. A symlink cannot drift, so editing a SKILL.md
# changes it for both agents at once. That is the opposite choice from
# sync-from-toolkit.sh, which copies on purpose because the OSS marketplace has
# to stand alone when cloned. Here both ends are local to one machine, so the
# live link is strictly better.
#
# Usage:
#   scripts/sync-codex-skills.sh            # reconcile ~/.codex/skills/
#   scripts/sync-codex-skills.sh --check    # report drift; nonzero if any
#   scripts/sync-codex-skills.sh DIR...     # use specific marketplace roots
#
# Roots default to this marketplace plus a sibling `plugins-internal` when it
# exists. Override the destination with $CODEX_SKILLS_DIR.
#
# Safety: only symlinks pointing inside the given roots are ever created,
# repointed, or removed. A real directory, or a symlink aimed anywhere else
# (Codex's own skills, the toolkit, hand-written ones), is reported and left
# untouched.
#
# Exit: 0 in sync (or Codex not installed); 1 drift in --check, or a fatal
# config error such as two plugins claiming the same skill name.

CHECK=0
roots=()
for arg in "$@"; do
  case "$arg" in
    --check) CHECK=1 ;;
    -*) echo "sync-codex-skills: unknown option $arg" >&2; exit 1 ;;
    *) roots+=("$arg") ;;
  esac
done

PLUGINS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ ${#roots[@]} -eq 0 ]]; then
  roots=("$PLUGINS_ROOT")
  [[ -d "$PLUGINS_ROOT/../plugins-internal" ]] &&
    roots+=("$(cd "$PLUGINS_ROOT/../plugins-internal" && pwd)")
fi

DEST="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"

# Codex absent is not a failure: contributors who only use Claude Code must not
# be blocked by a pre-commit hook about an agent they do not run.
if [[ ! -d "$(dirname "$DEST")" ]]; then
  echo "sync-codex-skills: Codex not installed at $(dirname "$DEST"); nothing to do."
  exit 0
fi

# ---- collect declared skills ------------------------------------------------
# name -> absolute source dir, and name -> declaring plugin, for collisions.
declare -A src_of=()
declare -A owner_of=()
fatal=0

for root in "${roots[@]}"; do
  if [[ ! -d "$root" ]]; then
    echo "sync-codex-skills: ERROR root not found: $root" >&2
    exit 1
  fi
  while IFS= read -r manifest; do
    plugin_dir="$(cd "$(dirname "$(dirname "$manifest")")" && pwd)"
    plugin="$(basename "$plugin_dir")"
    while IFS= read -r rel; do
      [[ -z "$rel" ]] && continue
      src="$plugin_dir/${rel#./}"
      name="$(basename "$src")"
      if [[ ! -f "$src/SKILL.md" ]]; then
        echo "sync-codex-skills: ERROR $plugin declares $rel but $src/SKILL.md is missing" >&2
        fatal=1
        continue
      fi
      if [[ -n "${src_of[$name]:-}" && "${src_of[$name]}" != "$src" ]]; then
        echo "sync-codex-skills: ERROR skill name '$name' claimed by both ${owner_of[$name]} and $plugin" >&2
        echo "  Codex's namespace is flat, so the names must be unique across marketplaces." >&2
        fatal=1
        continue
      fi
      src_of["$name"]="$src"
      owner_of["$name"]="$plugin"
    done < <(jq -r '.skills[]? // empty' "$manifest")
  done < <(find "$root" -mindepth 3 -maxdepth 3 -path '*/.claude-plugin/plugin.json' -print)
done

[[ $fatal -ne 0 ]] && exit 1

if [[ ${#src_of[@]} -eq 0 ]]; then
  echo "sync-codex-skills: no skills declared in ${roots[*]}" >&2
  exit 1
fi

# Is a path inside one of the marketplace roots? Only those are ours to manage.
in_roots() {
  local p="$1" root
  for root in "${roots[@]}"; do
    [[ "$p" == "$root"/* ]] && return 0
  done
  return 1
}

mkdir -p "$DEST"

drift=0
declare -i linked=0 repointed=0 removed=0 ok=0 skipped=0

# ---- reconcile declared skills ---------------------------------------------
for name in $(printf '%s\n' "${!src_of[@]}" | sort); do
  src="${src_of[$name]}"
  link="$DEST/$name"

  if [[ -L "$link" ]]; then
    current="$(readlink -f "$link" || true)"
    if [[ "$current" == "$src" ]]; then
      ok+=1
      continue
    fi
    if ! in_roots "$current" || [[ -z "$current" && ! -e "$link" ]]; then
      # Points outside the marketplaces, or dangles. Not ours to redirect.
      if [[ -z "$current" ]]; then
        echo "sync-codex-skills: WARN $name is a broken symlink -> $(readlink "$link"); leaving alone" >&2
      else
        echo "sync-codex-skills: WARN $name already links outside the marketplaces -> $current; leaving alone" >&2
      fi
      skipped+=1
      continue
    fi
    if [[ $CHECK -eq 1 ]]; then
      echo "DRIFT: $name links to $current, expected $src" >&2
      drift=1
    else
      ln -sfn "$src" "$link"
      echo "repointed: $name -> $src"
      repointed+=1
    fi
    continue
  fi

  if [[ -e "$link" ]]; then
    echo "sync-codex-skills: WARN $name exists as a real directory in $DEST; leaving alone" >&2
    skipped+=1
    continue
  fi

  if [[ $CHECK -eq 1 ]]; then
    echo "DRIFT: $name is declared by ${owner_of[$name]} but missing from $DEST" >&2
    drift=1
  else
    ln -s "$src" "$link"
    echo "linked: $name -> $src"
    linked+=1
  fi
done

# ---- remove links to skills no longer declared ------------------------------
# Only symlinks aimed inside the roots. A real directory or a link elsewhere is
# someone else's, and a dangling link is only ours if it pointed into a root.
while IFS= read -r link; do
  name="$(basename "$link")"
  [[ -n "${src_of[$name]:-}" ]] && continue
  target="$(readlink "$link")"
  resolved="$(readlink -f "$link" || true)"
  in_roots "$target" || in_roots "$resolved" || continue
  if [[ $CHECK -eq 1 ]]; then
    echo "DRIFT: $name links into the marketplaces but no plugin declares it: $target" >&2
    drift=1
  else
    rm "$link"
    echo "removed stale: $name -> $target"
    removed+=1
  fi
done < <(find "$DEST" -mindepth 1 -maxdepth 1 -type l -print)

# ---- report -----------------------------------------------------------------
if [[ $CHECK -eq 1 ]]; then
  if [[ $drift -ne 0 ]]; then
    echo "sync-codex-skills: DRIFT detected. Run scripts/sync-codex-skills.sh to reconcile." >&2
    exit 1
  fi
  echo "sync-codex-skills: $DEST in sync ($ok skill(s) linked, $skipped left alone)."
  exit 0
fi

echo "sync-codex-skills: ${#src_of[@]} declared; $linked linked, $repointed repointed, $removed stale removed, $ok already correct, $skipped left alone."
