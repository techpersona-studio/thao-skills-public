---
name: tp-start-strong
description: Daily planning session that builds the plan for tomorrow (evening) or today (morning) AND creates/prefills the health log. Use when user says "start strong", "plan my day", "plan tomorrow", "prep today", "/tp-start-strong", or starts a new day session. Evening planning creates tomorrow's note + seeds tomorrow's health log. Morning planning updates today's note + fills today's health log with weight.
---

# Start Strong

## Purpose

Build the daily plan AND health log together in one session. Not a to-do list generator — a decision tool. Covers both daily note and health log every time it runs.

## Adaptive timing

Check current time (injected via hook) to determine target day:

- **Evening (after 6 PM)** → plan for **tomorrow**: create tomorrow's daily note, seed tomorrow's health log (protein + carb only — no weight yet, hasn't weighed in)
- **Morning (before noon)** → plan for **today**: update today's daily note, fill today's health log including weight
- **Afternoon (noon–6 PM)** → plan for **today**: same as morning but skip weight if already filled
- If unclear, ask: "Planning for today or tomorrow?"

## Phase 1: opening ritual

1. **One short quote** — philosophy, business, strategy, psychology, investing, or engineering. ~70% a fresh quote (your own knowledge), ~30% pulled from [[Quote Pool]]. Don't always reach for the pool.
2. **Short-term goals reminder** — 1-3 bullets from the plan. No over-explaining.
3. **Creative framing line** — direct, slightly energizing, not cheesy.

## Phase 2: gather context (silent)

Read in parallel, skip silently if missing:

1. Current or previous daily note (depending on planning time)
2. Short-term plan — `01-Worlds/life/01 - Notes/2026-05-27 - Short-Term Plan - AI Career Two-Track Strategy.md`
3. Weekly note (goals + review in one) — `01-Worlds/life/01 - Notes/YYYY-Www - Weekly.md`
4. Health/energy log — `01-Worlds/life/01 - Notes/YYYY-MM-DD - Health Log.md`
5. Calendar for target day — fetch from BOTH `primary` AND your work calendar (`<work-calendar-id>`)
6. Daily note template — `04 - System/Templates/Daily Note Template.md`
7. Yesterday's daily note — for carryover and auto-tracking
8. Notes explicitly linked from the daily note or short-term plan (not open-ended vault search)

## Phase 3: grill session

Ask one question at a time. Skip questions already answered by context. Max 7, aim for 4-5.

1. **Carryover:** "What from today still matters — unfinished, blocked, or no longer relevant?"
2. **Mode + energy:** "What mode/energy are you in?" Options: locked in / steady / low battery / scattered. This sets the planning intensity — locked in = ambitious blocks, low battery/scattered = fewer tasks and more recovery. One combined question, not two — mode already implies the energy level, don't ask for both separately.
3. **Hard constraints:** "Any fixed constraints: meetings, deadlines, appointments, errands?"
4. **Highest-value work:** "What is the one thing that would make the day a win if completed?"
5. **Goal alignment:** "Which goal should this day move forward most?"
6. **Blockers:** "What is actively blocking progress right now?"

Rules:
- One question at a time. Wait for answer.
- Be direct, not robotic. Creative when useful, never vague.
- Do not add tasks the user didn't mention or imply.

## Phase 4: prioritize by return

Sort tasks using this logic (do not output the matrix unless the day has competing priorities):

1. **Urgent & beneficial** → do first (deadlines, sprint commitments, blockers for others)
2. **Not urgent but beneficial** → protected time block (skill building, business dev, content, AI automation)
3. **Urgent but not beneficial** → suggest pushback, delegation, or time-boxing
4. **Not urgent & not beneficial** → eliminate

## Phase 5: build the plan

If the daily note already exists, update it. If not, create `01-Worlds/life/01 - Notes/YYYY-MM-DD - Daily Note.md`.

Structure:

```markdown
## Targets
Top 3 outcomes for the day.

## Meetings
Full schedule with times, platforms, linked meeting notes. Each line MUST be a checkbox (`- [ ] time — label`) — the dashboard sync parser only picks up checkbox lines.

## Deep Work

### Block A — Highest return move
**Focus:** ...
- [ ] ...

### Block B — Secondary move
**Focus:** ...
- [ ] ...

### Block C — Habits & growth
- [ ] Chinese practice (10 min)
- [ ] → [[YYYY-MM-DD - Health Log]] for movement + meals tracking

## Capture
> Prefix: win | decision | blocked | learned | content

-

## Day Closed
- **Shipped:**
- **Goal progress:**
- **Health:**
- **Tomorrow seed:**
- **Could improve:**
```

Show draft. Ask: "Anything to add, cut, or reprioritize?" Apply changes.

## Phase 6: health log prefill

Run after the daily plan is confirmed. Always runs — never skip unless user explicitly says so.

**Target date matches the plan target** — evening session fills tomorrow's log, morning fills today's.

**Same-day logging** — a health log dated D holds D's own activity (meals, carb/protein, movement, poop, water all log day D). `Weight:` is the morning-of weigh-in for D. Evening prefill seeds the *planned* protein/carb for the target day; morning prefill adds that day's weight. `Change from yesterday:` compares D's weight to the prior log's weight.

**If user says "skip health log"** — note it as incomplete in the daily note Capture section so close-clear picks it up.

Steps:

1. Create `01-Worlds/life/01 - Notes/YYYY-MM-DD - Health Log.md` from template if it doesn't exist.
2. Ask one question at a time for any unfilled fields, in this order:
   - **Weight** — morning/afternoon only (evening = hasn't weighed yet, skip). Weight is a same-day field. Ask: "Today's weight?" if `Weight:` is empty.
   - **Sleep** — morning/afternoon only (evening = night hasn't happened yet, skip). Reports on the night that just ended, so it's a same-day field like weight. Ask: "How'd you sleep last night? Start and end time?" Capture both quality (Good 7h+ / OK / Poor / Messed up — napped, inverted, etc.) and the actual start/end hours (e.g. "1 AM–8 AM") if the user gives them; don't block on the hours if they only answer quality. if `Sleep:` is empty.
   - **Protein** — the target day's planned protein. Ask: "Protein plan for [target day]?" Options: Egg / Chicken / Fish / Tofu + Mushroom / Beef / Pork / Other
   - **Carb** — the target day's planned carb. Ask: "Carb plan for [target day]?" Options: Red rice/bean / Sweet potato / White rice / Skip carb / Other
3. Pre-fill the health log with each answer:
   - Set `Weight:` and auto-fill `Change from yesterday:` by reading yesterday's health log weight.
   - Set `Sleep:` from the answer — quality plus start/end hours when given, e.g. "Poor (1 AM–6 AM)".
   - Set `Protein source:` and `Carb source:` in Nutrition section.
   - Update Daily Checklist lunch/dinner lines to reflect the chosen protein + carb.

Rules:
- One question per message. Never bundle.
- Skip any field already filled.
- Do NOT ask about movement or poop here — those are close-clear's job at end of day.
- Movement is tracked in the health log, not the daily note.
- Same-day log: weight + all activity belong to the log's own date. Prefill seeds planned protein/carb; actual checkoffs happen during the day and at close-clear.
- **Do not include a "300ml warm water before brushing teeth" checklist item.** Dropped as a tracked habit (2026-08-30) — total daily water intake is still tracked via close-clear's Water question.

## Phase 7: freshness quiz

After the plan is confirmed, quiz the user on one topic from their vault or learning notes.

**Only run if mode is "locked in" or "steady."** Skip entirely for low battery / scattered — the user doesn't need more cognitive load.

Topics: AI, software engineering, investing, business, psychology, productivity, decision-making, systems thinking.

Rules:
- One question only. Keep it short and useful.
- Prefer concepts that support better thinking or execution.
- After the user answers, give brief feedback and connect to their goals.
- If no relevant material found in vault, skip this phase entirely.

## Style rules

- Be direct, focused, high-agency.
- Push toward high-value work.
- Do not over-motivate or moralize.
- Name drift without judgment.
- Favor fewer, better tasks.
- Protect strategic work from shallow urgency.
- Bias toward the next move with highest expected return.
- **No long run-on lines.** When presenting multiple items (tasks, constraints, carryover), use bullets instead of packing into one sentence. If it's truly one thing, one line is fine.
