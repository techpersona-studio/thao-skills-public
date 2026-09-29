# Install

Two ways. Pick one.

## A. Claude Code plugin (laptop, desktop app, IDE)

```
/plugin marketplace add techpersona-studio/thao-skills-public
/plugin install tp-skill@thao-skills-public
/plugin install engineering-skills@thao-skills-public    # optional: design + architecture skills
```

Skills then appear as `/tp-skill:tp-eli5` and so on. Auto-update is off by default for this
marketplace: turn it on in `/plugin` → Marketplaces, or update by hand with
`claude plugin marketplace update thao-skills-public && claude plugin update tp-skill@thao-skills-public`
and `/reload-plugins`.

Cloud sessions cannot use this route. See the README section "Cloud agents".

## B. Symlink into your tools (Claude Code, Codex, Cursor)

Feed everything between the lines to an agent on the new machine as its prompt.

---

Role: install a public skills repo on this machine.

Repo: https://github.com/techpersona-studio/thao-skills-public (public, no login needed).

Steps:
1. If `~/.agents/skills-public` already exists and is not empty, stop and show me what is in it.
   Do not overwrite anything.
2. `git clone https://github.com/techpersona-studio/thao-skills-public ~/.agents/skills-public`
3. Run `~/.agents/skills-public/bin/install.sh`. It links each skill into `~/.claude/skills`,
   `~/.codex/skills` and `~/.cursor/skills-cursor`, only for tools that exist here. It never
   deletes a real folder, skips a tool folder that is itself a symlink, and prints a line for every
   existing symlink it repoints.
4. Report what got linked where, every "exists and is not a symlink" warning, every "replaced"
   line, and every tool that was skipped.

Important:
- Do not commit or push anything to this repo.
- Do not rename any skill folder.

---

No login is needed: the repo is public.
