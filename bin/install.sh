#!/usr/bin/env bash
# Symlinks every skill in this repo into whichever of Claude Code / Codex / Cursor
# are actually set up on this machine. Run after cloning this repo (for example to ~/.agents/skills-public).
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "installing from $REPO_DIR (the symlinks below point there)"

# name -> target dir. Only linked if the tool's own config dir already exists,
# so this never scaffolds a directory for a tool that isn't installed here.
# (Plain arrays, not an associative array: macOS ships bash 3.2, which has no `declare -A`.)
TARGETS=(
  "Claude|$HOME/.claude/skills"
  "Codex|$HOME/.codex/skills"
  "Cursor|$HOME/.cursor/skills-cursor"
)

for entry in "${TARGETS[@]}"; do
  tool="${entry%%|*}"
  target="${entry#*|}"
  parent="$(dirname "$target")"
  if [ ! -d "$parent" ]; then
    echo "skip $tool: $parent not found, doesn't look installed on this machine"
    continue
  fi
  # A tool dir that is itself a symlink (e.g. ~/.claude/skills -> ~/.agents/skills) is already
  # wired; per-skill links inside it would land in whatever it points at.
  if [ -L "$target" ]; then
    echo "skip $tool: $target is itself a symlink -> $(readlink "$target")"
    continue
  fi
  mkdir -p "$target"
  count=0
  for dir in "$REPO_DIR"/*/; do
    name="$(basename "$dir")"
    case "$name" in
      hive-*) continue ;;  # owned by a separate private repo, not this one
    esac
    [ -f "$dir/SKILL.md" ] || continue
    link="$target/$name"
    if [ -L "$link" ]; then
      old="$(readlink "$link")"
      [ "$old" = "$dir" ] || echo "replaced $link (was -> $old)"
      rm -f "$link"
    elif [ -e "$link" ]; then
      echo "warning: $link exists and is not a symlink - leaving it alone" >&2
      continue
    fi
    ln -s "$dir" "$link"
    count=$((count + 1))
  done
  echo "linked $count skills into $target ($tool)"
done

echo "note: hive-* skills are NOT part of this repo (owned by a separate private repo) and are not linked anywhere by this script."
