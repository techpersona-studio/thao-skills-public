#!/bin/bash
# SessionStart hook (cloud sessions only): registers the thao-skills plugin
# marketplace and installs its 3 plugins. Runs after Claude Code launches, so
# the GitHub auth proxy is already connected — unlike an environment setup
# script, which runs BEFORE the proxy connects and can't clone a private repo.
# Idempotent: skips anything already done, so a repeat session in a warm
# environment adds negligible startup time.

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if ! claude plugin marketplace list 2>/dev/null | grep -q "thao-skills"; then
  claude plugin marketplace add techpersona-studio/thao-skills 2>&1 || true
fi

for p in seo-skills engineering-skills tp-workflow; do
  if ! claude plugin list 2>/dev/null | grep -q "$p@thao-skills"; then
    claude plugin install "$p@thao-skills" --scope user 2>&1 || true
  fi
done

exit 0
