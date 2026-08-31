#!/usr/bin/env bash
# Regenerates the Claude Code plugin marketplace (.claude-plugin/marketplace.json
# + plugins/*/skills/* symlinks) from whatever top-level <name>/SKILL.md
# directories exist in this repo. Run after adding, removing, or renaming a
# skill, alongside bin/install.sh (which handles the separate local-machine
# symlink flow for Claude/Codex/Cursor).
#
# This script never touches the top-level skill directories themselves — it
# only (re)builds plugins/*/skills/* as symlinks back to them, so hive-testbed's
# bare-name references (see README) and the existing install.sh flow are
# unaffected.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

declare -A CATEGORY_DESC=(
  [engineering-skills]="General engineering skill pack: code review, TDD, architecture, prototyping, and research skills (Matt Pocock pack + design + misc)."
  [tp-workflow]="Thao's personal workflow skills: daily planning, close-clear, strategic zoom-outs, and related habits."
)

classify() {
  local name="$1"
  case "$name" in
    seo|seo-*) echo "" ;;  # not vendored -- point to AgriciDaniel/claude-seo directly, see README
    tp-*) echo "tp-workflow" ;;
    matt-*|codebase-design|diagnosing-bugs|domain-modeling|grilling|implement|tdd|high-end-visual-design|image-to-code|excalidraw-diagram|find-skills)
      echo "engineering-skills" ;;
    *) echo "" ;;
  esac
}

# Reset plugins/ so removed/renamed skills don't leave stale symlinks behind.
rm -rf plugins
mkdir -p plugins
mkdir -p .claude-plugin

declare -A COUNT=()

for dir in */; do
  name="${dir%/}"
  case "$name" in
    plugins|bin|.git) continue ;;
  esac
  [ -f "$dir/SKILL.md" ] || continue

  category="$(classify "$name")"
  if [ -z "$category" ]; then
    echo "warning: '$name' has a SKILL.md but doesn't match any known prefix (seo-*, tp-*, matt-*, or the known unprefixed set) — skipping, add it to bin/build-marketplace.sh's classify()." >&2
    continue
  fi

  mkdir -p "plugins/$category/skills"
  ln -s "../../../$name" "plugins/$category/skills/$name"
  COUNT[$category]=$(( ${COUNT[$category]:-0} + 1 ))
done

for category in "${!CATEGORY_DESC[@]}"; do
  mkdir -p "plugins/$category/.claude-plugin"
  cat > "plugins/$category/.claude-plugin/plugin.json" <<EOF
{
  "name": "$category",
  "description": "${CATEGORY_DESC[$category]}",
  "author": { "name": "Thao" }
}
EOF
done

cat > .claude-plugin/marketplace.json <<'EOF'
{
  "name": "thao-skills-public",
  "owner": { "name": "Thao", "email": "techpersonastudio@gmail.com" },
  "description": "Thao's personal + team Claude Code skill packs, grouped into plugins.",
  "plugins": [
    {
      "name": "engineering-skills",
      "source": "./plugins/engineering-skills",
      "description": "General engineering skill pack: code review, TDD, architecture, prototyping, and research skills (Matt Pocock pack + design + misc)."
    },
    {
      "name": "tp-workflow",
      "source": "./plugins/tp-workflow",
      "description": "Thao's personal workflow skills: daily planning, close-clear, strategic zoom-outs, and related habits."
    }
  ]
}
EOF

echo "Rebuilt marketplace:"
for category in "${!COUNT[@]}"; do
  echo "  $category: ${COUNT[$category]} skills"
done
