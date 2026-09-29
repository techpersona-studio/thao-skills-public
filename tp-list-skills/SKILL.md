---
name: tp-list-skills
description: Print all available skills grouped by category (orchestration/planning, developing/coding, debugging/review, knowledge/vault, integrations, meta/config), tagged by origin, sorted by most recent usage. Use when user says "list skills", "/tp-list-skills", "what skills do I have", "show my skills by category", or wants a categorized skill inventory.
---

# List Skills

## Purpose

Group inventory of skills, not the flat `/skills` dialog. Shows category, origin tag, and recent-usage order so Thao can see what she has and what she actually uses.

## Phase 1: gather usage data (silent)

Count real invocations from session transcripts. Run:

```bash
cd ~/.claude/projects/<project-dir>/
# Skill-tool invocations + slash-command invocations, combined
{ grep -rhoE '"skill":"[a-z0-9-]+"' *.jsonl 2>/dev/null | sed 's/"skill":"//;s/"//';
  grep -rhoE '<command-name>/[a-z0-9-]+' *.jsonl 2>/dev/null | sed 's|<command-name>/||'; } \
  | sort | uniq -c | sort -rn
```

Also get recency (last-used) — most recent transcript mentioning each skill wins ordering ties:

```bash
cd ~/.claude/projects/<project-dir>/
for f in $(ls -t *.jsonl); do grep -loE '"skill":"[a-z0-9-]+"|<command-name>/[a-z0-9-]+' "$f"; done >/dev/null
```

Usage count is the primary sort key (descending). Skills with zero recorded use go last, alphabetical.

## Phase 2: determine origin tags

- **(created by Thao)** — skill has its own dir under `~/.claude/skills/<name>/SKILL.md`
- **(superpowers)** — skill is namespaced `superpowers:*` in the available-skills list
- **(plugin: NAME)** — other namespaced plugin skills (Notion, Slack, etc.)
- Built-in slash commands with no skill dir and no namespace — tag **(built-in)**

Read the available-skills list in context to resolve namespaces. Check `~/.claude/skills/` for local dirs.

## Phase 3: categorize

Bucket every skill. Categories (Thao-confirmed):

- **Orchestration / planning** — start-strong, north-star, close-clear, brainstorming, writing-plans, executing-plans
- **Developing / coding** — implement-jira-ticket, tdd, frontend-design, claude-api, to-prd, to-issues, subagent-driven-development, dispatching-parallel-agents, using-git-worktrees
- **Debugging / review** — diagnose, systematic-debugging, code-review, review, security-review, simplify, verify, verification-before-completion, receiving-code-review, requesting-code-review, improve-codebase-architecture, finishing-a-development-branch
- **Knowledge / vault** — import-artifacts, youtube-transcript, deep-research
- **Integrations** — all Notion:*, all slack:*
- **Meta / config** — write-a-skill, list-skills, update-config, keybindings-help, loop, run, init, fewer-permission-prompts, using-superpowers, writing-skills

New/unknown skills: place by best-fit description, note them at the bottom under "Uncategorized" if unsure.

## Phase 3.5: filter what to display

**Hide any skill that is NOT created by Thao AND has 0 recorded usage.** Nothing is deleted — this is display-only.

- Keep ALL skills created by Thao (own dir in `~/.claude/skills/`), even at 0 usage.
- Keep any non-Thao skill (superpowers, plugin, built-in, Matt Pocock import, etc.) ONLY if it has nonzero usage.
- Drop the rest from the printed tables.

At the end, print a single line: "Hidden: N unused non-Thao skills (run with `--all` to show)." If the user passes `--all`, skip this filter and show everything.

## Phase 4: print

For each category, a table sorted by usage desc:

```
## Orchestration / planning
| Skill | Uses | Origin | What |
|-------|:---:|--------|------|
| start-strong | 4 | created by Thao | plan day + health log |
| ...
```

- `Uses` = combined invocation count from Phase 1 (— if zero).
- Keep `What` to ~5 words.
- Order categories by total usage (most-used category first).
- End with a one-line summary: total skills, total tracked invocations, most-used skill.

## Rules

- Counts come from real transcript data, not guesses. If the grep returns nothing, say "no usage data yet" and sort alphabetically.
- Don't list a skill twice. Every skill lands in exactly one category.
- This is read-only. No file writes.
