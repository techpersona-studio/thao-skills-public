# CLAUDE.md

See README.md for the full picture. Short version:

Public counterpart to the private `thao-skills` repo. 2 plugins:

- `tp-skill` — auto-loads via the SessionStart hook (`scripts/ensure-thao-skills-marketplace.sh`).
  Nothing to do.
- `engineering-skills` — opt-in: `/plugin install engineering-skills@thao-skills-public`.

No SEO, no work-specific tooling, no `hive-testbed` dependency — those live only in the private
`thao-skills` repo. Before adding anything here, check it's actually meant to be public.
