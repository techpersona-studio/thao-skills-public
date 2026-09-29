#!/bin/bash
# SessionStart hook, cloud sessions only.
#
# A cloud session has no /plugin, does not load plugins declared in a repo's settings, and does
# not carry over the skills in your laptop's ~/.claude/skills. What it does do: run this repo's
# SessionStart hooks and read skills from ~/.claude/skills. So this script puts the skills
# there and asks Claude Code to re-scan, which makes them usable in the same session.
#
# Cloud VMs start fresh, so every session installs the latest `main`. On a laptop this exits
# at once. Anything printed to stdout must stay valid JSON, so all noise goes to stderr.
# Never blocks the session: any failure just leaves the session without the skills.

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

REPO_URL="https://github.com/techpersona-studio/thao-skills-public.git"
DEST="$HOME/.agents/skills-public"

if {
  if [ -d "$DEST/.git" ]; then
    git -C "$DEST" pull --quiet --ff-only
  else
    mkdir -p "$(dirname "$DEST")" && git clone --quiet --depth 1 "$REPO_URL" "$DEST"
  fi &&
  mkdir -p "$HOME/.claude" &&
  bash "$DEST/bin/install.sh"
} 1>&2; then
  echo '{"hookSpecificOutput":{"hookEventName":"SessionStart","reloadSkills":true}}'
fi
exit 0
