---
name: tp-check-in
description: Mid-day plan adjustment loop. Audits task progress against current time, fills health log fields that should be done by now, handles replanning when a popup meeting or new task appears, and quizzes on completed learning/coding tasks. Use when user says "check in", "check-in", "/tp-check-in", "update plan", "new meeting popped up", "replan", or pushes an update like "finished X, took 2 hours".
---

# Check-in

## Purpose

Stay on track mid-day. Not a full replanning session — a fast alignment loop.
Four jobs: time audit → health log sync → replan if needed → quiz if applicable.

## Quick start

User can invoke two ways:
- `/tp-check-in` — run the full loop silently from current time + daily note
- `/tp-check-in <update>` — e.g. `/tp-check-in finished PR #270 review, took 45 min` — apply the update first, then run the loop

## Phase 1: gather context (silent)

Read in parallel:
1. Today's daily note — current time (from hook) determines what should be done
2. Today's health log — check what's filled vs. empty
3. Short-term plan — `01-Worlds/life/01 - Notes/2026-05-27 - Short-Term Plan - AI Career Two-Track Strategy.md`

## Phase 2: apply inline update (if args provided)

If user passed an update (e.g. "finished T2b skeleton, took 3 hrs, ran into SSE edge case"):
- Mark the task done in the daily note
- Log time delta if different from expected (note in Capture: `blocked | T2b took 3h vs 1h expected — SSE edge case`)
- Do this silently before the audit

## Timestamping rule (applies everywhere, not just check-in)

Whenever the user asks to log, update, or mark anything — always include the current time (from hook injection) in the note entry. Examples:

- Lunch started → `- [x] Lunch (~2 PM): 100g Tofu — started 2:35 PM`
- Task completed → `- [x] PR #270 review — 11:05 AM–12:50 PM`
- Meeting done → `- [x] 1:45 PM — Standup — done 2:18 PM`
- Skipped item → `- [-] Fiber mix — skipped 2:35 PM, not hungry`

Rules:
- Use current time from the hook-injected `systemMessage` (format: `HH:MM AM/PM`)
- If user provides a start time in their message, use that; otherwise use current time as end/log time
- For tasks with known start (user mentioned earlier), compute duration if possible
- Keep it inline — append to the existing checklist line, don't add a separate timestamp line

## Phase 3: time audit

Based on current time, scan unchecked tasks that should be done by now.

Present as a single grouped question:
```
It's [time]. These should be done or in progress:
1. [task] — was due [block/time]
2. [task] — was due [block/time]

Reply: A. Done  B. In progress  C. Carry  D. Drop  E. Blocked
```

Rules:
- Only surface tasks whose block has already started (don't surface afternoon tasks at 10 AM)
- If everything on track, say "On track. Nothing overdue." and skip to Phase 4

## Phase 4: health log sync

**Same-day logging** — a health log dated D holds D's own activity. Weight is D's morning weigh-in; meals, movement, poop, and water are all today's. Log things as they happen today, into today's log.

Check current time against health log. Ask one question at a time for anything that should be filled by now but isn't:

| Time | What to check |
|------|--------------|
| After 9 AM | Weight filled? (today's weigh-in) |
| After a meal | Today's meal row checked? (log meals as eaten) |

Rules:
- One question per message
- Skip if already filled
- Everything logs today's activity, into today's log
- After any health log update, sync today's row in `01-Worlds/life/01 - Notes/Weight Loss Journey - May 2026.md` — weight, protein, carb, poop, movement notes

## Phase 5: replan (only if triggered)

Triggers: user mentions a new meeting, a new task, or a significant time overrun.

**New meeting:**
- Add to Meetings section
- Ask: "What does this displace?" Force a conscious tradeoff — don't just stack

**New task:**
- Ask: "Is this actually high-value or a distraction in disguise?"
- Options: Genuine high-value (add to Block A) / Can wait until tomorrow / Delegate or drop
- If it displaces something: ask what gets bumped before adding it

**Time overrun (>50% over estimate):**
- Note actual time in Capture
- Ask: "Does this change what's realistic for the rest of the day?"
- If yes: simplify remaining blocks, protect Block B (personal growth)

## Phase 6: quiz (only if a learning or complex coding task just completed)

Triggers: task marked done that involves learning (n8n, AI, engineering), a complex design decision, or a PR review.

Ask one targeted question:
- **Learning task** — quiz on the concept (e.g. "What's the practical difference between a webhook trigger and a polling trigger in n8n?")
- **Complex coding task** — grill on design: "Why did you choose X approach over Y? What breaks if Z changes?"
- **PR review** — "What was the most important thing you caught in that review?"

One question only. Give brief feedback after the answer. Connect to goals if relevant.

## Phase 7: personal growth block check (after 5 PM only)

If it's past 5 PM and Block B (personal growth / n8n / side hustle) is still unchecked:

> "Block B untouched — job work expanded again. Still protecting the evening slot?"

Options: Yes, starting now / Pushing to tomorrow / Dropping today

Force the decision explicitly. Don't let it silently slip.

## Style rules

- Fast. This is a mid-day check, not a replanning session.
- One question per message.
- Flag drift without moralizing.
- Default to keeping the plan — only replan if something actually changed.
- Protect Block B from job work creep every time.
- **No long run-on lines.** When listing multiple items (tasks remaining, overdue items, health fields), use bullets instead of packing into one sentence. If it's truly one thing, one line is fine.
