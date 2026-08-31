---
name: tp-todo
description: Write a structured task/ticket plan for a piece of work before coding starts. Use when the user types `/tp-todo`, says "create a todo", "create a ticket", "write a task doc", "plan this work", or anytime a piece of work is big enough to deserve a written plan with alternatives, steps, and a testing section. Produces a markdown file in the repo's `todo/` folder.
---

# /tp-todo — Write a Task Plan

Write a clear task-plan markdown file before implementation starts. The goal is a doc another engineer can read in 3 minutes and understand **what**, **why**, **what we considered**, **what we picked**, **how we'll do it**, and **how we'll know it worked**.

## When to use

Use this skill when any of these are true:

- User typed `/tp-todo`, `/tp-todo <description>`, or asked to "create a ticket / todo / task plan".
- The work is >1 hour of coding, touches 3+ files, or has non-obvious trade-offs.
- You are about to propose an implementation and the user has not yet approved an approach.

**Skip** for trivial edits (one-line fix, rename, typo) — just do the work.

## Where the file goes

- **Default location**: `todo/` folder at the repo root.
- **Filename format**: `<TICKET-ID>-<kebab-slug>.md`.
- No ticket ID yet? Use just the slug. Rename once the ticket exists.
- **Never commit** unless the repo's `todo/` is tracked. Check `.gitignore` once; don't assume.

If the repo has no `todo/` folder, create it. If the repo has its own convention, follow that instead.

---

## Domain detection

Before drafting, classify the task into one of three domains:

| Signal | Domain |
|--------|--------|
| Task touches only `frontend2/` — components, styles, store, UI tests | **frontend** |
| Task touches only `backend/` — models, tools, agents, API, DB, backend tests | **backend** |
| Task touches both, or you can't tell yet | **fullstack** |

Use these signals: the user's description, file paths, keywords like "component", "dropdown", "CSS", "style", "layout" (frontend) or "API", "model", "tool", "migration" (backend).

**After detecting the domain, read the corresponding file from this skill's directory:**

- **frontend** or **fullstack**: read `frontend.md` from this skill's directory. It contains the frontend-specific template sections (Visual Specification, Component Map, Style & Theme Checklist, Accessibility Checklist, Visual Verification Plan, Test Selectors) and frontend-specific tips.
- **backend**: read `backend.md` from this skill's directory. It contains the backend-specific template section (Wire Compatibility) and backend-specific tips.
- **fullstack**: read **both** files. Include frontend sections + Wire Compatibility if the task involves API shape changes.

Insert the domain-specific sections into the plan after "Success Criteria" and before "Risk Assessment".

---

## Core template

Copy this verbatim as the starting structure. Then insert domain-specific sections from the domain file(s). Fill every section — use "N/A" only when a section genuinely does not apply, and say why.

````markdown
# <TICKET-ID> — <Short Title>

**Status**: Open | In Progress | Review | Done
**Priority**: High | Medium | Low
**Effort**: S (< 1/2 day) | M (1/2-2 days) | L (2-5 days) | XL (> 5 days — split it)
**Created**: YYYY-MM-DD
**Owner**: <name or "AI + user">
**Domain**: frontend | backend | fullstack
**Links**: <Jira URL, PR, related tickets>
**Dependencies**: <tickets or conditions that must be met first, or "None">
**Review mode**: per-step | end-only

---

## User Approval

**Approach Approved By**: _<pending>_
**Approval Date**: _<pending>_
**Approval Notes**: _To be filled when user approves the selected approach._

---

## Problem Statement

_What's broken, missing, or painful today? Combine the "what" and the "why" in one place._

- **Symptom**: _what the user sees / experiences_
- **Root cause**: _the underlying reason, not just the symptom_
- **Impact**: _who is affected, how often, how badly_
- **Evidence**: _links to logs, Datadog queries, screenshots, repro steps, Slack threads_

## Proposed Approaches

_List 2-3 realistic options. For each, write one-sentence pros/cons._

### Approach A — <name>

_One-line summary._

- Pro: _..._
- Con: _..._

### Approach B — <name>

_One-line summary._

- Pro: _..._
- Con: _..._

### Approach C — <name> _(optional)_

_..._

## Selected Approach

**Picked**: Approach <A/B/C>

_Explain **why** this one wins in 2-4 sentences. Call out which cons we're accepting and why they're tolerable._

---

## Planned Approach

### Technical Strategy

_1-2 paragraphs summarizing the high-level "how." Tables, diagrams, or code snippets welcome._

### Implementation Steps

_Narrative, ordered steps. Each step should be independently reviewable (roughly one commit). Describe **what the step solves**, not just which files it touches. List files as sub-bullets._

_**Commit workflow:** Each step is a separate commit (or small commit group). After completing a step, commit the changes and — if review mode is `per-step` — pause for the user to review before moving to the next step._

- [ ] **Step 1: <one-line purpose>.** _What this step does and why it matters._
  - Files: _..._
- [ ] **Step 2: <one-line purpose>.** _..._
  - Files: _..._
- [ ] **Step N: Update docs.** _..._

---

## Success Criteria

_How will we verify the change works and hasn't broken anything? Be specific._

**Automated checks:**
- [ ] _`rg "OldThing" src` -> zero hits_
- [ ] _`cd backend && make check` passes_
- [ ] _..._

**Behavior:**
- [ ] _At <condition>, <expected outcome>_
- [ ] _..._

**Manual verification:**
- [ ] _Steps a reviewer can follow, including edge cases_
- [ ] _..._

<!-- INSERT DOMAIN-SPECIFIC SECTIONS HERE (from frontend.md and/or backend.md) -->

---

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation | Reviewer / QA verification |
|------|--------|------------|------------|---------------------------|
| _..._ | High/Med/Low | High/Med/Low | _..._ | _Concrete thing to poke post-merge_ |

---

## Implementation Notes

### Progress Log

_Dated entries added as work progresses. One bullet per milestone — reference step numbers._

- YYYY-MM-DD — _..._

### Decisions Made

_Record choices made mid-implementation so reviewers don't have to re-derive them._

- _..._

---

## Completion Summary

_(Filled when task is complete.)_

### What Was Delivered
- _..._

### Lessons Learned
- _..._

### Future Considerations
- _..._

---

## Documentation Updated

_(Filled when docs are synced — by hand or via sync-task-documentation skill.)_

- _..._
````

---

## How to fill it in

1. **First pass** — skeleton: fill Problem Statement and Steps from your current understanding.
2. **Second pass** — decision: fill Proposed Approaches and Selected Approach (this often reshapes the Steps). Then finish Success Criteria, domain-specific sections, and Risk Assessment.

### Writing style

- **Simple words**. Write as if the reader is a smart engineer who is new to this area of the codebase.
- **Short sentences**. If a sentence has three commas, split it.
- **Concrete, not abstract**. "Refactor for clarity" is useless. "Rewrite `PermissionDropdown` as a radio-only selector driven by `PERMISSION_LEVELS` array" is useful.
- **Show, don't tell**. Code snippets and diffs beat prose for technical detail.
- **No filler**. Delete anything that says "we will implement the implementation".

### Section-specific tips

- **Problem Statement**: Separate the **symptom** from the **root cause**. "The UI is slow" is a symptom. "We re-render the entire message list on every keystroke" is a cause.
- **Proposed Approaches**: Include a **"do nothing"** or **"minimal patch"** option when it's viable.
- **Selected Approach**: Name the con you're accepting. Reviewers trust a plan more when the author has already argued with themselves.
- **Implementation Steps**: Each step should tell a *story* — "what this step solves" first, files second. If a step takes more than ~2 hours, split it.
- **Success Criteria**: Include concrete commands — `rg`, `make check`, `make test`. Not just "all tests pass."
- **Risk Assessment**: The "Reviewer / QA verification" column answers "what should I poke after this merges?"
- **Progress Log**: Update as you work. Reference step numbers so the timeline and the steps stay connected.
- **Completion Summary**: Fill this honestly. "Lessons Learned" should capture things that surprised you.

See the domain-specific files (`frontend.md`, `backend.md`) for additional section-specific tips.

---

## Workflow

When the user invokes this skill:

1. **Ask questions up front.** Before drafting anything:
   - Scope questions (2-3 max) to fill Problem Statement if the request is vague.
   - **Review mode**: "Do you want to review each step's commit before I move to the next (`per-step`), or review everything at the end (`end-only`)?"
   - **Domain detection**: Classify the task as frontend / backend / fullstack. State which domain you detected and why, so the user can correct you. Then read the corresponding domain file(s) from this skill's directory.

2. **Draft the file.** Create it in `todo/` with the correct filename. Include the core sections plus domain-specific sections. Use `_TBD — <what's needed>_` for anything that needs user input.

3. **Show the user the filename** and a one-paragraph summary. Do **not** dump the whole file back in chat — they can open it.

4. **Ask for approval** on the Selected Approach before implementation starts. When approved, fill in the **User Approval** section.

5. **During implementation:**
   - Commit each step separately.
   - If review mode is `per-step`: pause after each commit and ask the user to review before continuing.
   - If review mode is `end-only`: proceed through all steps, then present the full diff.
   - Tick off steps as they complete. Update the Progress Log. Append decisions to "Decisions Made."
   - For frontend tasks: run the Visual Verification Plan steps after the final UI-facing step, before the docs step.

6. **After implementation:** Fill the Completion Summary. Run the sync-task-documentation skill if available.

## Anti-patterns

- **Writing the plan after the code**. Plans are for deciding, not documenting.
- **Planning for weeks of work in one file**. If effort is XL, split into child tickets.
- **Skipping Proposed Approaches because "the approach is obvious"**. It's never as obvious as you think.
- **Letting Success Criteria say "run tests"**. Name the tests. Name the commands.
- **Flat file inventories instead of narrative steps**. Each step should say *what it solves*.
- **Forgetting the "Reviewer / QA verification" column in Risk Assessment**.

## Relationship to other artifacts

- **`docs/superpowers/plans/`**: larger, subagent-executable plans (different skill, different shape). Use `/tp-todo` for the initial decision doc, then promote to a full plan if needed.
- **Jira tickets**: the todo file is the **source of truth**; Jira is a mirror for PM/stakeholder visibility.
- **`.cursor/rules/frontend-styling.mdc`**: authoritative styling rules. Frontend domain sections reference the same conventions.
