---
name: tp-north-star
description: Strategic zoom-out. Pretty-prints Thao's long-term North Stars and 60-day plan, ranks the highest-value task in each track against current state, and suggests a next-few-days plan. Use when user says "north star", "/tp-north-star", "what should I focus on", "am I on track", "zoom out", "what's the highest-value thing", or wants strategic (not daily-tactical) direction. Vault-only by default; pulls live Jira/calendar with --live.
---

# North Star

## Purpose

Strategic altitude check, not a daily to-do list. `/tp-start-strong` plans a day; `/tp-north-star` answers "am I working on the things that actually move my North Stars, and what's the highest-value next move?"

Three outputs every run:
1. Pretty-printed long-term + mid-term goals
2. Highest-value tasks ranked per track
3. A next-few-days plan (3-5 days)

Then offer to seed the picks into notes.

## Modes

- **`/tp-north-star`** (default) — vault only. Fast, no API calls.
- **`/tp-north-star --live`** — also pull open Jira issues + today/tomorrow calendar so the plan respects real tickets and meetings.

If the user asks "what's blocking" or "what's due" without the flag, suggest `--live` once, then proceed vault-only.

## Phase 1: gather context (silent)

Read in parallel, skip silently if missing:

1. **Goal hierarchy + 60-day plan** — `01-Worlds/life/01 - Notes/2026-05-29 - Goal Hierarchy and 60-Day Plan.md` (PRIMARY source of truth — North Stars, tracks, sequencing locks)
2. **North Star filter** — `01-Worlds/life/01 - Notes/stay-on-the-path.md` (drift rules)
3. **Weekly note** — `01-Worlds/life/01 - Notes/YYYY-Www - Weekly.md` (goals + review in one; this week's commitments + progress)
4. **Last 1-2 daily notes** — `01-Worlds/life/01 - Notes/YYYY-MM-DD - Daily Note.md` (what got done, carryover, energy)
5. **AI automation roadmap** — `01-Worlds/life/01 - Notes/2026-05-29 - AI Automation Person - Niche and Roadmap.md` (Track 1 task bank)

**If `--live`:**
6. Open Jira issues — `search_jira_issues` with `assignee = currentUser() AND statusCategory != Done ORDER BY priority DESC`
7. Calendar — `list-events` for today + next few days, BOTH `primary` AND Luma calendar (`mo7f6lts4rke57i2cfd9bgrsurer2o8f@import.calendar.google.com`)

Use the hook-injected current time to resolve "today", the current week number, and which deadlines are closing in.

## Phase 2: pretty-print goals

Print clean and scannable. Long-term North Stars (numbered, one line each). Then the 60-day tracks with their sequencing. Mark deadlines that are close (flag anything due within 14 days of current date). Keep it tight — this is a reminder, not a re-read of the whole plan.

## Phase 3: rank highest-value tasks per track

For each active track, surface the single highest-value next task (1-2 max). Score each candidate by the locked rules:

1. **Serves a North Star?** If you can't name which one, cut it (stay-on-the-path filter).
2. **Sequenced-next or jumping ahead?** Respect the locks — do NOT surface a task that the sequencing defers. Hard examples:
   - Task B does NOT fire until its prerequisite (task A) ships.
   - A side-project demo does NOT compete with a hard work deadline; it's scheduled for after.
   - A later track is deferred until the automation that enables it exists.
   - A build stops at its locked v1 scope — no scope creep once shipped.
3. **Deadline pressure.** A hard external deadline outranks everything else that week. A fixed-date personal commitment (an event, a milestone) can outrank routine tasks too.
4. **Effort vs return.** Prefer high-value/low-effort to build momentum; protect the 20% that drives 80%.

Output a compact ranked table: task | track | which North Star | why-now. Order by value across all tracks, not within.

Apply the [[Priority Philosophy]]: urgent & beneficial first, protect not-urgent-but-beneficial, push back urgent-not-beneficial, eliminate the rest.

## Phase 4: next-few-days plan

Propose a realistic 3-5 day plan. Respect:
- Sequencing locks (never schedule a deferred task)
- The 80% job / 20% side split
- Current energy/mode from recent daily notes
- Real meetings/deadlines (if `--live`)

Keep it concrete: which day, which task, why. Don't over-schedule — name the few moves that compound.

**Do NOT plan weekends.** Don't assume Saturday/Sunday are side-business or work blocks. Skip weekend days unless the user explicitly says what they're doing then.

## Phase 5: offer to seed

After printing, ask once: **"Seed these into tomorrow's daily note / this week's goals? (y/n)"**

If yes:
- Add picks to the relevant daily note or weekly goals file, matching the lean daily-note format (targets on top, single Capture section).
- Do NOT create new structure or duplicate existing tasks. Only add what's missing.
- Timestamp per the vault rule if logging into a daily note.

If no, stop. The print-out is the deliverable.

## Rules

- This is a decision tool, not a status report. Every task must tie to a named North Star.
- Be direct. Name drift when you see it ("X feels productive but serves no North Star — skip it").
- Don't invent tasks. Pull only from the plan, roadmap, weekly goals, or live Jira.
- Honor the grill-locked sequencing. The plan was hard-won; don't quietly un-sequence it.
- If a deadline is at risk (e.g. June release vs. days remaining), say so plainly.
