---
name: tp-update-brain
description: Manually run a full Living Brain sync on Thao-OS — scans the current conversation for new/changed info, files it into the correct vault layer (hot_cache, wiki, world notes, CONTEXT.md, log.md), and updates today's daily note with what got done/found. Also has a "prune sweep" mode that promotes matured/DONE hot_cache bullets into the right wiki page and clears them, so hot_cache doesn't silently bloat. Backstop for when the passive CLAUDE.md auto-capture instruction misses something. Use when the user says "update brain", "update-brain", "/tp-update-brain", "update the vault", "save this to the brain", "capture this conversation", "sync the brain", "file this into the vault", "prune the brain", "clean up hot_cache", or "promote hot_cache to wiki".
---

# Update Brain

## Purpose

Same law as the standing CLAUDE.md auto-evolve instruction (`00-Rules/rules.md` — Living Brain), run deliberately and thoroughly instead of as a rushed end-of-session aside. Exists because passive capture is unreliable — this is the on-demand backstop.

Three jobs, forward-looking: read current state → file new/changed info in the right vault layer → sync today's daily note. Plus one job, backward-looking: prune matured WIP out of hot_cache into the right wiki (its own mode, below — the "promote + prune" half of the law that keeps getting skipped because nothing forces it).

## Quick start

- `/tp-update-brain` — scan the whole conversation so far, file everything new
- `/tp-update-brain <specific thing>` — e.g. `/tp-update-brain we decided to drop Kafka for now` — file just that, skip the full scan
- `/tp-update-brain prune [world]` — backward-looking sweep instead of a forward-looking capture: promote matured hot_cache bullets into wiki, clear them out. No world named = global `hot_cache.md`.

## Phase 1: read current state (silent)

1. Global `hot_cache.md` (vault root)
2. The relevant World's `hot_cache.md` + `wiki/index.md` — see World detection below. Also skim that world's `CLAUDE.md` if unfamiliar with its structure.
3. `CONTEXT.md` — only if the conversation touched identity/values/weaknesses/preferences
4. Today's daily note — `01-Worlds/life/01 - Notes/<date> - Daily Note.md` (assume it exists, created by `/tp-start-strong`; if genuinely missing, create a minimal one rather than skipping the capture)

**World detection** — infer from repo/cwd + conversation content, not cwd alone:
- work-specific tooling/repo → `work` (🔒 confidential)
- a client is named → that client under `01-Worlds/clients/`
- Thao's own reusable tooling (hive skills, this skill, scripts, prompts) → **global** (`hot_cache.md` / `02-Wikis/`), cross-referenced from a touched world if relevant — don't file tooling as if it belongs to one world
- content / business / finance / personal → match by topic
- multiple worlds touched in one session → file each fact to **its own** world, don't collapse into one

## Phase 2: extract what's new (silent, main session — it has the conversation)

Scan the full visible conversation, not just the latest message, for anything matching the Living Brain law's categories: a decision made, a new/changed fact (technical, business, client, personal), a WIP status change, an identity/value/weakness/preference signal, anything timeline-worthy.

For each candidate, check it against what Phase 1 loaded:
- **Already captured, correctly?** Drop it. Don't write a duplicate "confirms X" line just to prove the skill ran — this is the #1 gap this skill exists to close.
- **Contradicts existing content?** Keep it, mark as a reconcile (not a plain append).
- **Genuinely new?** Keep it.

Output: a short list of `{fact, category, likely target file, new-vs-contradicts}`. If the list is empty, stop here — go straight to Phase 5 and say so.

## Phase 3: file it — always dispatch to Opus

Per `00-Rules/rules.md` and `04-Agents/vault-manager.md`: filing/reconciling is a judgment task, and the Vault Manager role that owns it is **pinned to Opus 4.8, never downgraded**. Dispatch this phase as an `Agent` call with `model: "opus"` regardless of what model is running this skill.

Give the subagent:
- the Phase-2 candidate list (not the raw conversation — it doesn't need to re-derive what's new)
- the current content of every file Phase 1 loaded
- the routing rules below
- explicit reconcile / infer-the-home / restructure-if-needed instructions, and: ask Thao only if genuinely ambiguous or high-stakes, never as a default

Routing rules (condensed from the law):
- identity / values / weakness / preference / how-to-argue → `CONTEXT.md`, right section (`[seeded]`→`[confirmed]` when verified)
- live WIP → the right `hot_cache.md` (global or world)
- durable / synthesized knowledge → a wiki page (`02-Wikis/` if reusable, a world's local `wiki/` if it dies with the client — "does it die with the client?" test)
- domain fact about a world → that world's notes, `categories/subjects/project` frontmatter + `[[wikilinks]]`
- person / tool / credential-pointer / template → `03-References/`
- timeline-worthy → one line to `log.md`: `## [YYYY-MM-DD] <type> | <one line>` (types: ingest, decision, build, lint, query)
- any page created or deleted → update `index.md`
- **reconcile, don't append** — contradiction found → update to the new truth, record what changed + when, flag it in the subagent's return
- **never** store secrets; **never** bulk-move or mass-delete mid-sync; read a file before overwriting it

## Phase 4: update today's daily note (main session, not dispatched)

Routine and mechanical — no Opus dispatch needed:
- Capture section: what got done, what was found, decisions made — one bullet per item, `prefix | text` (win/decision/blocked/learned/content), current time inline
- Check off any Targets/Deep-Work items this conversation completed (timestamping rule: current time inline)
- Don't duplicate world-level hot_cache detail verbatim — one line + a `[[wikilink]]` or pointer to the fuller entry

## Phase 5: receipt

One terse line, matching Vault Manager's own output contract:

`brain: <what changed + where>` — e.g. `brain: logged decision to luma/hot_cache, updated CONTEXT §5, daily note Capture +2 lines`

If Phase 2 found nothing new: say so plainly — `brain: nothing new to file`. Don't manufacture an entry to look useful.

**Bloat check (every normal run, cheap):** while Phase 1 has hot_cache open, notice if it looks bloated (rough guide: tens of KB, or bullets clearly marked DONE/SHIPPED/100%/RESOLVED still sitting under "Active WIP"). Don't run a prune sweep automatically — it's a heavier, separate pass — but say so in the receipt: `brain: ...; also — <hot_cache> looks prune-able (N old-done bullets), run '/tp-update-brain prune' when you want it swept`. This is what makes the prune mode actually get used instead of sitting unused like the wiki did.

## Prune sweep — separate mode (`/tp-update-brain prune [world]`)

Backward-looking, not forward-looking: it doesn't read the conversation at all. Exists because `00-Rules/rules.md`'s "Promote + prune" line has always been true in principle but nothing made it happen in practice — sessions capture new info fine, nobody goes back and clears out what already matured. Confirmed gap 2026-07-23: global hot_cache hit 82KB against ~6.5KB of actual global wiki content, with fully-"DONE" stories (e.g. the hive-orchestration redesign) still sitting in "Active WIP" weeks after their real home (`build/wiki/hive.md`) existed.

1. Read the target hot_cache.md in full (global, or the named world's).
2. Classify each bullet:
   - still-moving WIP → leave it alone
   - matured (marked done/shipped/complete/resolved, or unchanged across several sessions) → promotion candidate
3. Dispatch to Opus — same non-negotiable rule as Phase 3, doubly true here: shrinking/deleting existing content is higher-stakes than adding a new bullet, and merge-before-shrink takes real judgment.
   - For each candidate: check whether a matching wiki page already exists (global `02-Wikis/` or the world's `wiki/`).
   - **Merge before you shrink.** Anything in the hot_cache bullet not already in the wiki page gets folded in first — never let content disappear because it was "obviously" already covered.
   - Replace the hot_cache bullet with a short pointer, not a silent delete: `✅ done (YYYY-MM-DD) — see [[wiki/<page>]]`. Keeps a breadcrumb for anyone scanning history.
   - Batch small, verify each file after writing — don't rewrite the whole hot_cache in one blind pass (Safety rule: never bulk-move/mass-delete mid-sync).
4. Receipt: `brain: pruned N bullets from <hot_cache>, promoted to <wiki pages>, ~XKB → ~YKB`.

## Style rules

- Reconcile, don't blindly append — always check existing content before writing
- Infer the right home; ask Thao only when genuinely ambiguous or high-stakes
- Low-friction transparency — one receipt line, not a report of every file touched
- Never store secrets (API keys, tokens, passwords) in the vault
- Never bulk-move or mass-delete while Drive may be mid-sync — batch small, verify, continue
- Phase 3 always runs on Opus — no exceptions, even from a cheaper-model session
