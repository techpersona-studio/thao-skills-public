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
/plugin install seo-skills@thao-skills-public
/plugin install engineering-skills@thao-skills-public
/plugin install tp-workflow@thao-skills-public
```

All 52 skills are grouped into 3 plugins (so invocation is `/seo-skills:seo-audit`, not one
plugin per skill):

| Plugin | Skills |
|---|---|
| `seo-skills` | all 31 `seo*` skills |
| `engineering-skills` | `matt-improve-codebase-architecture`, the 6 unprefixed Matt-pack skills, design (`high-end-visual-design`, `image-to-code`, `excalidraw-diagram`) |
| `tp-workflow` | Thao's personal `tp-*` skills (daily planning, close-clear, strategic zoom-outs, communication style, etc.) — the referenced Google Drive vault paths are Thao's, not yours |

No `version` field is set anywhere in the marketplace, so Claude Code tracks the latest commit
SHA on `main` automatically — edit a skill, commit, push, and every session that already has the
plugin installed (local or cloud) picks it up on next use / `/plugin marketplace update`. No
re-upload, no delete-then-reinstall.

**These 3 plugins are generated, not hand-maintained** — `plugins/*/skills/*` are symlinks back
to the real top-level `<name>/SKILL.md` directories (never copies), rebuilt by
`bin/build-marketplace.sh`. See "Adding a new skill" below.

## What's here (51 skills)

Naming convention: **`matt-*`** = from Matt Pocock's engineering-skills pack, **`tp-*`** =
written by Thao. Unprefixed = third-party pack (SEO, design).

| Category | Skills |
|---|---|
| SEO (31) | seo, seo-ahrefs, seo-audit, seo-backlinks, seo-bing, seo-cluster, seo-competitor-pages, seo-content, seo-content-brief, seo-dataforseo, seo-drift, seo-ecommerce, seo-firecrawl, seo-flow, seo-geo, seo-google, seo-hreflang, seo-image-gen, seo-images, seo-local, seo-maps, seo-page, seo-plan, seo-profound, seo-programmatic, seo-schema, seo-seranking, seo-sitemap, seo-sxo, seo-technical, seo-unlighthouse |
| Design (3) | high-end-visual-design, image-to-code, excalidraw-diagram |
| Matt Pocock pack, prefixed (1) | matt-improve-codebase-architecture — the only one of the 13 still in regular use |
| Matt Pocock pack, **left unprefixed on purpose** (6) | codebase-design, diagnosing-bugs, domain-modeling, grilling, implement, tdd — see note below |
| Thao-authored, prefixed (10) | tp-building-automation-prompts, tp-close-clear, tp-codebase-walkthrough, tp-eli5, tp-import-artifacts, tp-list-skills, tp-north-star, tp-start-strong, tp-update-brain, tp-youtube-transcript |

### Why 6 Matt-pack skills stay unprefixed

`codebase-design`, `diagnosing-bugs`, `domain-modeling`, `grilling`, `implement`, `tdd` are
called **by exact bare name** from `hive-*` skills owned by a separate private repo. Renaming
them here would silently break those. Leave these 6 bare.

## What's NOT here

- **Work-specific tooling** — anything tied to a private employer's Jira ticket conventions, CI
  bot, or internal repo bootstrap scripts. Lives only in the private `thao-skills` repo, and was
  never committed here.
- **`hive-*` skills** — owned by a separate private repo, with its own sync flow. Gitignored
  here, never tracked.
- **17 skills cut 2026-08-31** after a usage review (mirrors the same cut in the private
  `thao-skills` repo): 12 rarely-used Matt Pocock skills (kept `matt-improve-codebase-architecture`
  — most of what was useful in the rest has been absorbed into the hive-flow workflow),
  `tp-caveman` (superseded by `tp-eli5`), `tp-check-in` (redundant with `tp-close-clear` /
  `tp-start-strong` / `tp-update-brain`), `find-skills` (redundant with `tp-list-skills`), and
  `tp-todo`. `tp-import-lesson` was also cut then kept after all, renamed to `tp-import-artifacts`
  to reflect a broader scope.

## Adding a new skill

Drop a `<name>/SKILL.md` directory in here, then run both:

- `bin/install.sh` — picks it up in `~/.claude/skills` (and Codex/Cursor) on this machine.
- `bin/build-marketplace.sh` — regenerates `plugins/*/skills/*` so it's included in the plugin
  marketplace (see above). Classifies by prefix (`seo-*`, `tp-*`, `matt-*`, or the known
  unprefixed set); a name it doesn't recognize prints a warning instead of silently dropping it.

Commit and push both the new skill and the regenerated `plugins/` directory.

**Before adding anything work-specific, don't — that's what the private `thao-skills` repo is for.**
