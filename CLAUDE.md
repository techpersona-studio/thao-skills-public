# CLAUDE.md

See README.md for the full picture. Short version:

Public counterpart to a private skills repo.

- Cloud sessions of THIS repo: the SessionStart hook (`scripts/ensure-cloud-skills.sh`) installs
  every skill into `~/.claude/skills` and reloads. For another repo, see README "Cloud agents".
- Laptop: two plugins, `tp-skill` and `engineering-skills` (README "Plugin marketplace").

No SEO, no work-specific tooling, no hive skills: those live only in the private repo.

Before adding or changing anything here, check it is meant to be public:
- no employer or coworker names, work ticket keys, tenant or stack names, work calendar ids,
  private repo or client names, or home paths with a username;
- `git log -1 --format='%ae %ce'` shows only the personal address, never a work one;
- after changing a skill, run `bin/build-marketplace.sh` (needs bash 4+; on macOS use Homebrew's
  bash) and commit the regenerated `plugins/`.
