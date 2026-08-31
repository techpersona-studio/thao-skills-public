# Install on a new machine

Feed this whole section to an agent on the new machine as its prompt.

---

Install my public skills repo on this machine.

Repo: https://github.com/techpersona-studio/thao-skills-public (public — no auth needed to clone).

1. If `~/.agents/skills-public` already exists and is non-empty, stop and show me what's in it
   before doing anything destructive — don't overwrite existing content blindly.
2. Otherwise: `git clone https://github.com/techpersona-studio/thao-skills-public ~/.agents/skills-public`
3. Run `~/.agents/skills-public/bin/install.sh` — it symlinks every skill in the repo into
   whichever of `~/.claude/skills`, `~/.codex/skills`, `~/.cursor/skills-cursor` already exist on
   this machine (it skips any tool whose config dir isn't present).
4. Report what got linked where, and flag anything the script skipped or any pre-existing
   same-named file/symlink it had to overwrite.

Note: 6 skills in the repo (`codebase-design`, `diagnosing-bugs`, `domain-modeling`, `grilling`,
`implement`, `tdd`) are intentionally left without the `matt-`/`tp-` prefix that everything else
has — see the repo's README for why. Don't rename them.

---

## Prerequisite

None — this repo is public. Plain `git clone` (or an unauthenticated `gh repo clone`) works.
