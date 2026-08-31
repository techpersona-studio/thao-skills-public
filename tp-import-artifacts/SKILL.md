---
name: tp-import-artifacts
description: Import an artifact (a lesson, meeting export, or any HTML/markdown/canvas file plus related images) into the Thao-OS vault. Any dropped md or html file lands in `01-Worlds/life/05 - Views/` as the raw human view; a processed summary note is created in `01-Worlds/life/01 - Notes/`, and views/images are linked from the relevant index. Use when the user drops an md/html file, mentions adding a new lesson, uploads notes, a new class/session happened, or says "add the lesson" / "import lesson" / "import this artifact" for any course or source (weight loss, n8n, etc).
---

# import-artifacts

## The rule (applies whenever the user drops an md or html file)

- **Raw artifact → `01-Worlds/life/05 - Views/`.** Any dropped md or html file is the user's own note / human view. Move it there, never leave it in Downloads.
- **Summary → `01-Worlds/life/01 - Notes/`.** Always also create a processed summary note in `01-Worlds/life/01 - Notes/` with standard frontmatter. The Views file is for human reading; the Notes file is the retrievable, linked summary.
- **Link both** from the course index note and bump its `updated` date.

## Quick start

User provides: the file path(s) (md and/or html, plus any images), the course/note it belongs to, a lesson title, and the session date.

Run the script to move files, then create the summary note + update the index.

```bash
python3 ~/.claude/skills/tp-import-artifacts/scripts/import_artifact.py \
  --md "/path/to/notes.md" \
  --html "/path/to/lesson.html" \
  --images "/path/img1.png" "/path/img2.png" \
  --lesson-note "Weight Loss Science - Lesson Notes" \
  --day "Day 6" \
  --title "Fiber" \
  --date "2026-06-07"
```

At least one of `--md`, `--html`, or `--images` is required. Provide whichever the user actually dropped.

## Workflow

1. **Get the files** — ask for the md/html path(s) and any images. If unsure of the lesson note, check `01-Worlds/life/01 - Notes/` for matching course notes.
2. **Run the script** — moves any md/html/images into `01-Worlds/life/05 - Views/` using the naming convention `Day N - <Title>` (md and html both get the ` Notes` suffix).
3. **Create the summary note** in `01-Worlds/life/01 - Notes/` named `YYYY-MM-DD - Lesson - Day N <Title>.md`:
   - Standard frontmatter (see template). **Quote `ai_summary` if it contains a colon** — an unquoted `: ` breaks the YAML parse and shows red in Obsidian.
   - Write the processed lesson content (or a summary of the dropped md/html).
   - Link the project note + related lessons.
4. **Update the index note** (`<Course> - Lesson Notes.md`):
   - Add the summary note under `## Lessons`
   - Add the view file under `## Human views` (md → `[[basename]]`, html → relative link)
   - Embed images under `## Reference images` using `![[filename]]`
   - Bump `updated`.

## File naming convention

- HTML: `Day N - <Short Title> Notes.html`
- Markdown: `Day N - <Short Title> Notes.md`
- Images: `Day N - <Description>.png` (or original name if descriptive)
- Summary note in `01-Worlds/life/01 - Notes/`: `YYYY-MM-DD - Lesson - Day N <Title>.md`

## Lesson note locations

| Course | Note file |
|--------|-----------|
| Weight loss coaching | `Weight Loss Science - Lesson Notes.md` |
| n8n course | create `n8n Course - Lesson Notes.md` if it doesn't exist |
| Any new course | create `<Course Name> - Lesson Notes.md` |

## New lesson note template

If the course note doesn't exist yet, create it in `01-Worlds/life/01 - Notes/` with:

```yaml
---
categories:
  - "[[Learning Notes]]"
subjects:
  - "[[Health]]"   # or relevant subject
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
source:
project:
review_cycle: monthly
ai_summary:
next_review:
---
```

## Views folder path

All HTML and image artifacts live at `<vault>/01-Worlds/life/05 - Views/`, where `<vault>` is the
Thao-OS vault root — `$THAO_OS_VAULT` if set, else the Google Drive desktop sync folder under
`~/Library/CloudStorage/GoogleDrive-*/My Drive/Thao-OS`. See `scripts/import_artifact.py`.

Links in notes use relative path: `../05 - Views/filename.html`  
Images use wikilink syntax: `![[filename.png]]`
