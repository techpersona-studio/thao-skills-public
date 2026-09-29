# thao-skills-public

Thao's Claude Code / agent skills — the shareable subset. This is the public counterpart to a
private repo; work-specific tooling (a private employer's Jira ticket conventions,
CI bot, internal repo bootstrap scripts) stays out of this one entirely, by construction — it was
never committed here, not redacted after the fact.

## Install on a new machine

```bash
git clone https://github.com/techpersona-studio/thao-skills-public ~/.agents/skills-public
~/.agents/skills-public/bin/install.sh
```

The install script symlinks every skill here into whichever of `~/.claude/skills`,
`~/.codex/skills`, `~/.cursor/skills-cursor` already exist on this machine — it skips any tool
not installed. This repo is the source of truth for what's here; any other tool that wants these
skills should symlink from here too, not copy — one source, no drift.

See [INSTRUCTIONS.md](./INSTRUCTIONS.md) for a ready-to-paste agent prompt that does the above
on a fresh machine.

## Plugin marketplace (laptop, desktop app, IDE; not cloud sessions)

This repo is also a Claude Code [plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
(`.claude-plugin/marketplace.json`). Anyone can:

```
/plugin marketplace add techpersona-studio/thao-skills-public
/plugin install tp-skill@thao-skills-public
/plugin install engineering-skills@thao-skills-public    # optional
```

Skills then appear as `/tp-skill:tp-start-strong`. Cloud sessions cannot use this route (next
section). All 14 skills are grouped into 2 plugins:

| Plugin | Skills |
|---|---|
| `tp-skill` | Thao's personal `tp-*` skills (daily planning, close-clear, strategic zoom-outs, communication style, etc.) — the referenced Google Drive vault paths are Thao's, not yours |
| `engineering-skills` | `matt-improve-codebase-architecture`, plus design (`high-end-visual-design`, `image-to-code`, `excalidraw-diagram`) |

**No SEO plugin here** — see "SEO skills" below for why, and what to install instead.

No `version` field is set in the marketplace, so Claude Code tracks the latest commit on `main`.
But auto-update is off by default for third-party marketplaces like this one. Turn it on in
`/plugin` → Marketplaces, or update by hand and reload:

```
claude plugin marketplace update thao-skills-public && claude plugin update tp-skill@thao-skills-public
/reload-plugins        # inside a session that is already open
```

**These 2 plugins are generated, not hand-maintained** — `plugins/*/skills/*` are symlinks back
to the real top-level `<name>/SKILL.md` directories (never copies), rebuilt by
`bin/build-marketplace.sh`. See "Adding a new skill" below.

## Cloud agents (Claude Code on the web)

What a cloud session does, per Claude Code's docs: it has no `/plugin`, it does not load plugins or
marketplaces named in a repo's `.claude/settings.json`, and it does not carry over the skills in
your laptop's `~/.claude/skills`. It does run a repo's SessionStart hooks (in a session with one
repository) and it reads skills from `~/.claude/skills`.

So the plugin route above is for laptops. For cloud, this repo ships a hook: `.claude/settings.json`
runs `scripts/ensure-cloud-skills.sh` when a session starts. In a cloud session
(`CLAUDE_CODE_REMOTE=true`) it clones this repo, runs `bin/install.sh` (links every skill into
`~/.claude/skills`) and returns `reloadSkills`, so Claude Code re-scans in the same session. On a
laptop it does nothing. A cloud VM is fresh each time, so every session gets the latest `main`.

Checked: the script's steps and output (no-op on a laptop, valid JSON on stdout, safe when the
network fails). Not checked: a live cloud session end to end. To confirm, start a session on this
repo and run `/tp-eli5`.

To get the same in another repo, copy the two files (`.claude/settings.json` and
`scripts/ensure-cloud-skills.sh`) keeping their paths, and merge into an existing
`.claude/settings.json` instead of overwriting it. Repo hooks are read in sessions with one
repository only, not in multi-repository sessions or project threads. The other route is the
environment's Setup script (claude.ai/code, environment settings), which runs before Claude Code
starts; the same clone and `bin/install.sh` steps fit there, but its user and home directory have
not been checked.

**What is useful in a cloud session.** The `tp-*` skills were written around Thao's own notes
vault, folders a cloud VM does not have:

| Works anywhere | Needs the notes vault on disk |
|---|---|
| `tp-eli5`, `tp-codebase-walkthrough`, `tp-building-automation-prompts`¹, `tp-list-skills`, `high-end-visual-design`, `image-to-code`, `matt-improve-codebase-architecture`¹, `excalidraw-diagram`² | `tp-start-strong`, `tp-close-clear`, `tp-north-star`, `tp-update-brain`, `tp-import-artifacts`, `tp-youtube-transcript` (which also needs `yt-dlp`) |

¹ Manual only: `disable-model-invocation` is on, so a human has to type the slash command.
² Needs `uv` and a Playwright Chromium, and its instructions assume a project-local
`.claude/skills/excalidraw-diagram` folder. Treat it as laptop-only.

## What's here (14 skills)

Naming convention: **`matt-*`** = from Matt Pocock's engineering-skills pack, **`tp-*`** =
written by Thao. Unprefixed = third-party pack (design).

| Category | Skills |
|---|---|
| Design (3) | high-end-visual-design, image-to-code, excalidraw-diagram |
| Matt Pocock pack, prefixed (1) | matt-improve-codebase-architecture — the only one of the 13 still in regular use |
| Thao-authored, prefixed (10) | tp-building-automation-prompts, tp-close-clear, tp-codebase-walkthrough, tp-eli5, tp-import-artifacts, tp-list-skills, tp-north-star, tp-start-strong, tp-update-brain, tp-youtube-transcript |

### SEO skills

Not vendored here (removed 2026-08-31). The 31 `seo-*` skills this repo used to carry were a
stale pinned copy of [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) (MIT)
that would need manual updating. SEO is also project-specific: the plugin lists about 26 skills and
19 sub-agents in every session where it is installed. So install it from the source, and only for
the projects that need it:

```
claude plugin marketplace add AgriciDaniel/claude-seo
claude plugin install claude-seo@agricidaniel-claude-seo --scope project
```

Scopes: `user` (the default) is every project on your machine; `project` records it in the repo's
shared `.claude/settings.json`; `local` is just you, in this repo (`.claude/settings.local.json`).
Inside a session, `/plugin install` opens a panel where you pick the scope instead. Always
current, no maintenance on our end.

## What's NOT here

- **Work-specific tooling** — anything tied to a private employer's Jira ticket conventions, CI
  bot, or internal repo bootstrap scripts. Lives only in the private repo, and was
  never committed here.
- **`hive-*` skills** — owned by a separate private repo, with its own sync flow. Gitignored
  here, never tracked.
- **The 6 unprefixed Matt-pack skills** (`codebase-design`, `diagnosing-bugs`, `domain-modeling`,
  `grilling`, `implement`, `tdd`), removed 2026-08-31. They exist only because the private hive
  skills call them by bare name, so they are kept in the private repo and not carried here.
- **17 skills cut 2026-08-31** after a usage review (mirrors the same cut in the private
  repo): 12 rarely-used Matt Pocock skills (kept `matt-improve-codebase-architecture`
  — most of what was useful in the rest has been absorbed into the hive-flow workflow),
  `tp-caveman` (superseded by `tp-eli5`), `tp-check-in` (redundant with `tp-close-clear` /
  `tp-start-strong` / `tp-update-brain`), `find-skills` (redundant with `tp-list-skills`), and
  `tp-todo`. `tp-import-lesson` was also cut then kept after all, renamed to `tp-import-artifacts`
  to reflect a broader scope.
- **All 31 `seo-*` skills, removed 2026-08-31** — see "SEO skills" above.

## Adding a new skill

Drop a `<name>/SKILL.md` directory in here, then run both:

- `bin/install.sh` — picks it up in `~/.claude/skills` (and Codex/Cursor) on this machine.
- `bin/build-marketplace.sh` (needs bash 4+; on macOS use Homebrew's bash) — regenerates `plugins/*/skills/*` so it's included in the plugin
  marketplace (see above). Classifies by prefix (`tp-*`, or the 4 named `engineering-skills`
  members); a name it doesn't recognize prints a warning instead of silently dropping it. `seo-*`
  is a deliberate no-op — see "SEO skills" above.

Commit and push both the new skill and the regenerated `plugins/` directory.

**Before adding anything work-specific, don't — that's what the private repo is for.**
