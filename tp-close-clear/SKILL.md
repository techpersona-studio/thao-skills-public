---
name: tp-close-clear
description: End-of-day review assistant that grills the user with low-effort multiple-choice questions, reviews completed and unfinished work, updates today's daily note, checks for shifts in short-term goals, captures lessons learned, and prepares a simple seed for tomorrow. Use when the user says "close clear", "end of day", "close the loop", "review today", "shutdown", "update today's note", or wants to reflect on what got done.
---

# Close the Loop

## Purpose

Low-friction end-of-day review. Close the day cleanly: what moved, what blocked, what learned, what carries forward.

Assume the user is tired. Multiple choice > open-ended. Keep it under 3 minutes.

## Phase 1: gather context (silent)

Read in parallel, skip silently if missing:

1. Today's daily note — `01-Worlds/life/01 - Notes/YYYY-MM-DD - Daily Note.md`
2. Today's health log — `01-Worlds/life/01 - Notes/YYYY-MM-DD - Health Log.md`
3. Today's calendar — fetch from BOTH `primary` AND your work calendar (`<work-calendar-id>`)
4. Short-term plan — `01-Worlds/life/01 - Notes/2026-05-27 - Short-Term Plan - AI Career Two-Track Strategy.md`
5. Weekly note (goals + review in one) — `01-Worlds/life/01 - Notes/YYYY-Www - Weekly.md`

## Phase 2: opening + checkbox review (combined)

Start with:

> Let's close the loop. I'll keep it quick.

Show what was planned, then immediately present unchecked items from **both** the daily note and health log:

```
Planned today:
- Block A: [summary]
- Block B: [summary]
- Habits: [summary]

These items are unchecked:
1. [task from daily note]
2. [movement — from health log]
3. [poop — from health log]
...

Reply: A. Done  B. Partial  C. Carry over  D. Drop  E. Blocked
Example: 1A, 2C, 3D
```

Rules:
- Skip items already checked `[x]`.
- Pull daily work tasks from the daily note.
- Pull health items (movement, poop, water, meals) directly from the health log.
- Group all unchecked items into one question.
- If everything is checked in both, skip this and say "All planned items checked. Nice."

## Phase 3: three quick questions (max)

Ask at most 3 questions total. Pick the most relevant based on context. Use AskUserQuestion tool with multiple choice.

**Q1 — Blocker/friction (always ask):**
What slowed the day down?
- Meetings / interruptions
- Low energy
- Technical blocker
- Over-scoping
- Emotional / mental friction
- Nothing major

**Q2 — Goal shift (only ask if the day deviated significantly from plan):**
Any shift in short-term goals?
- No change
- One goal became more urgent
- One goal became less relevant
- New opportunity appeared
- Need to simplify

**Q3 — Learning (only ask if something non-obvious happened):**
Anything worth remembering?
- Technical lesson
- Process / work lesson
- Business / career insight
- Personal pattern noticed
- Nothing today

If user reports a lesson, ask one follow-up: "One sentence — what was it?" (This is the one open-ended question allowed.)

## Phase 3b: health log close-out

**Same-day logging** — a health log dated D holds D's own activity. So TODAY's activity (poop, movement, water, dinner, meals) gets recorded into **today's** health log file (`01-Worlds/life/01 - Notes/[D] - Health Log.md`). Today's log already holds today's weigh-in + meals logged through the day; close-out fills the rest.

Ask one question at a time for each end-of-day field, writing answers into **today's** log:

- **Poop** — "Did you poop today?" (yes → check it off in today's log)
- **Movement** — "Any movement today?" Options: Walk / Elliptical / Neckline workout / Stretching / None
- **Water** — "Roughly how much water today?" Options: 1L / 1.5L / 2L / 2.5L / 3L+
- **Dinner** — if past 8 PM: "Did you have dinner?" (yes → check it; no → mark skipped)
- **Meals/protein/carb** — capture today's protein + carb into today's `Protein source:` / `Carb source:` and lunch/dinner lines

Rules:
- Write today's activity into today's log.
- One question per message.
- If user says "skip" — note it and move on. Don't repeat next session.
- After close-out, sync today's row in `01-Worlds/life/01 - Notes/Weight Loss Journey - May 2026.md` — weight, protein, carb, poop, movement notes. Also update Week N movement summary and Total Progress.
- **Do not ask about or check off a "300ml warm water before brushing teeth" item.** Dropped as a tracked habit (2026-08-30) — total daily water intake is still tracked via the Water question above.

## Phase 4: update today's note

Write a `## Day Closed` section (replaces any existing End-of-Day or End-of-Day Reflection section). Use this exact 5-line format:

```markdown
## Day Closed
- **Shipped:** [what moved — merged PRs, completed tasks, decisions made. Use numbers.]
- **Goal progress:** [one line on short-term plan or weekly goals progress]
- **Health:** [weight delta, movement done or skipped, meals tracked — pull from health log, not daily note.]
- **Tomorrow seed:** [carryover items + one low-effort habit that slipped]
- **Could improve:** [infer from friction answer — one specific, actionable suggestion]
```

If the user reported a learning/insight, append one more line:
```markdown
- **Learned:** [one sentence — the insight]
```

Also update `## Capture` with prefixed bullets for any wins, decisions, or lessons.

Rules:
- **No long run-on lines.** If a field has multiple items, use sub-bullets instead of packing them into one sentence.
- Be specific — mention numbers, PR numbers, ticket IDs.
- Don't duplicate what's already in Capture or Accomplishments.
- Infer "Could improve" from the friction answer.

**Formatting preference — bullets over long lines:**

```markdown
# ❌ BAD: long packed line
- **Shipped:** TICKET-1 legal disclaimer merged, TICKET-2 mockup data merged, TICKET-3 T1 research ~70% done, BE specs agreed, n8n API setups done.

# ✅ GOOD: sub-bullets when there are multiple items
- **Shipped:**
  - TICKET-1 legal disclaimer merged
  - TICKET-2 mockup data merged
  - TICKET-3 T1 research ~70% (transport patterns, SSE, Postgres v1 locked)
  - BE data specs agreed with a teammate
  - n8n API setups + "Don't Use AI Agent Wrong" section done
```

Apply the same pattern to **Goal progress**, **Health**, and **Tomorrow seed** when they contain more than one distinct item. If it's truly one thing, one line is fine.

## Phase 5: day-closed summary (chat only)

Print the same 5-line Day Closed content directly in chat (no markdown header). This is the last thing the user sees. No motivational fluff.

## Style rules

- Low effort for user. 3 questions max after checkbox review.
- Be direct, not robotic.
- Do not moralize skipped habits. Note them, move on.
- If the day was bad, acknowledge without judgment.
- If the day was good, say so in one line.
- Respect that the user is tired. Speed > thoroughness.
