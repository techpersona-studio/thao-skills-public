#!/usr/bin/env bash
# Symlinks every skill in this repo into whichever of Claude Code / Codex / Cursor
# are actually set up on this machine. Run after cloning this repo to ~/.agents/skills.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "$REPO_DIR" != "$HOME/.agents/skills" ]; then
  echo "warning: this repo is not at ~/.agents/skills (found at $REPO_DIR)." >&2
  echo "the symlinks below will still point at $REPO_DIR, but other tooling" >&2
  echo "(hive-dispatch, \$SKILLS_DIR references) may expect ~/.agents/skills." >&2
fi

# name -> target dir. Only linked if the tool's own config dir already exists,
# so this never scaffolds a directory for a tool that isn't installed here.
declare -A TARGETS=(
  [Claude]="$HOME/.claude/skills"
  [Codex]="$HOME/.codex/skills"
  [Cursor]="$HOME/.cursor/skills-cursor"
)

for tool in "${!TARGETS[@]}"; do
  target="${TARGETS[$tool]}"
  parent="$(dirname "$target")"
  if [ ! -d "$parent" ]; then
    echo "skip $tool: $parent not found, doesn't look installed on this machine"
    continue
  fi
  mkdir -p "$target"
  count=0
  for dir in "$REPO_DIR"/*/; do
    name="$(basename "$dir")"
    case "$name" in
      hive-*) continue ;;  # owned by hive-testbed, not this repo
    esac
    [ -f "$dir/SKILL.md" ] || continue
    link="$target/$name"
    if [ -L "$link" ] || [ -e "$link" ]; then
      rm -rf "$link"
    fi
    ln -s "$dir" "$link"
    count=$((count + 1))
  done
  echo "linked $count skills into $target ($tool)"
done

echo "note: hive-* skills are NOT part of this repo (owned by hive-testbed) and are not linked anywhere by this script."
