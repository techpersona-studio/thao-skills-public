#!/bin/bash
# SessionStart hook (cloud sessions only): registers the thao-skills plugin
# marketplace and installs the tp-skill plugin. engineering-skills is
# deliberately NOT auto-installed here -- opt-in only, same treatment as SEO
# (see README). Runs after Claude Code launches, so the GitHub auth proxy is
# already connected -- unlike an environment setup script, which runs BEFORE
# the proxy connects and can't clone a private repo.
# Idempotent: skips anything already done, so a repeat session in a warm
# environment adds negligible startup time.

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if ! claude plugin marketplace list 2>/dev/null | grep -q "thao-skills-public"; then
  claude plugin marketplace add techpersona-studio/thao-skills-public 2>&1 || true
fi

if ! claude plugin list 2>/dev/null | grep -q "tp-skill@thao-skills-public"; then
  claude plugin install "tp-skill@thao-skills-public" --scope user 2>&1 || true
fi

exit 0
