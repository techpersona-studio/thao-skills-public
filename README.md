# thao-skills-public

Thao's Claude Code / agent skills — the shareable subset. This is the public counterpart to a
private `thao-skills` repo; work-specific tooling (a private employer's Jira ticket conventions,
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

## Plugin marketplace (Claude Code only, local + cloud + coworkers)

This repo is also a Claude Code [plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
(`.claude-plugin/marketplace.json`), so it can reach Claude Code sessions — yours or a
coworker's, local or cloud — without the manual "zip it, upload it to claude.ai, delete the old
one" cycle. Anyone can:

```
/plugin marketplace add techpersona-studio/thao-skills-public
/plugin install tp-skill@thao-skills-public
```

Only `tp-skill` is meant to auto-load on every session (see the SessionStart hook in
`.claude/settings.json` of this and other repos). `engineering-skills` is opt-in — install it
separately when a project actually needs it:

```
/plugin install engineering-skills@thao-skills-public
```

All 14 skills are grouped into 2 plugins (so invocation is `/tp-skill:tp-start-strong`, not one
plugin per skill):

| Plugin | Skills | Auto-loads? |
|---|---|---|
| `tp-skill` | Thao's personal `tp-*` skills (daily planning, close-clear, strategic zoom-outs, communication style, etc.) — the referenced Google Drive vault paths are Thao's, not yours | **Yes**, via SessionStart hook |
| `engineering-skills` | `matt-improve-codebase-architecture`, plus design (`high-end-visual-design`, `image-to-code`, `excalidraw-diagram`) | No — opt-in |

**No SEO plugin here** — see "SEO skills" below for why, and what to install instead.

No `version` field is set anywhere in the marketplace, so Claude Code tracks the latest commit
SHA on `main` automatically — edit a skill, commit, push, and every session that already has the
plugin installed (local or cloud) picks it up on next use / `/plugin marketplace update`. No
re-upload, no delete-then-reinstall.

**These 2 plugins are generated, not hand-maintained** — `plugins/*/skills/*` are symlinks back
to the real top-level `<name>/SKILL.md` directories (never copies), rebuilt by
`bin/build-marketplace.sh`. See "Adding a new skill" below.

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
copy of [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) (MIT), pinned to an
already-stale version (v2.2.0 vs. their current v2.2.5) that we'd have to keep manually updating.
SEO is also project-specific, not something every session needs — so instead of paying its
context cost (~4.4k tokens, always-on) on every session, install it directly from the source only
on the projects that need it:

```
/plugin marketplace add AgriciDaniel/claude-seo
/plugin install claude-seo@agricidaniel-claude-seo
```

One plugin, `claude-seo`, bundles all 25 skills + 18 sub-agents. Always current, no maintenance
on our end. If a repo needs this every session, add it to that repo's own `.claude/settings.json`
under `extraKnownMarketplaces` (see `seo-os`'s for a working example) — that registers the
marketplace automatically without installing anything, so `/plugin install claude-seo@...` above
is the only manual step left.

## What's NOT here

- **Work-specific tooling** — anything tied to a private employer's Jira ticket conventions, CI
  bot, or internal repo bootstrap scripts. Lives only in the private `thao-skills` repo, and was
  never committed here.
- **`hive-*` skills** — owned by a separate private repo, with its own sync flow. Gitignored
  here, never tracked.
- **The 6 unprefixed Matt-pack skills** (`codebase-design`, `diagnosing-bugs`, `domain-modeling`,
  `grilling`, `implement`, `tdd`), removed 2026-08-31 — turns out `hive-testbed`'s own skills
  don't vendor these themselves; they depend on the *private* `thao-skills` repo supplying them
  locally (`hive-builder` wraps `/tdd`, `hive-architect` calls `/grilling` + `/domain-modeling`,
  etc.). That dependency lives only on your machine via the private repo's local install, so there
  was no reason to carry copies here too. Kept in `thao-skills`, not archived.
- **17 skills cut 2026-08-31** after a usage review (mirrors the same cut in the private
  `thao-skills` repo): 12 rarely-used Matt Pocock skills (kept `matt-improve-codebase-architecture`
  — most of what was useful in the rest has been absorbed into the hive-flow workflow),
  `tp-caveman` (superseded by `tp-eli5`), `tp-check-in` (redundant with `tp-close-clear` /
  `tp-start-strong` / `tp-update-brain`), `find-skills` (redundant with `tp-list-skills`), and
  `tp-todo`. `tp-import-lesson` was also cut then kept after all, renamed to `tp-import-artifacts`
  to reflect a broader scope.
- **All 31 `seo-*` skills, removed 2026-08-31** — see "SEO skills" above.

## Adding a new skill

Drop a `<name>/SKILL.md` directory in here, then run both:

- `bin/install.sh` — picks it up in `~/.claude/skills` (and Codex/Cursor) on this machine.
- `bin/build-marketplace.sh` — regenerates `plugins/*/skills/*` so it's included in the plugin
  marketplace (see above). Classifies by prefix (`tp-*`, or the 4 named `engineering-skills`
  members); a name it doesn't recognize prints a warning instead of silently dropping it. `seo-*`
  is a deliberate no-op — see "SEO skills" above.

Commit and push both the new skill and the regenerated `plugins/` directory.

**Before adding anything work-specific, don't — that's what the private `thao-skills` repo is for.**
