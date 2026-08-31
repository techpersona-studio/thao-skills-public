---
name: tp-youtube-transcript
description: "Extract YouTube video transcripts with metadata and save as Markdown to the Thao-OS vault. Use when user wants to download a YouTube transcript, convert a video to text, extract subtitles, or review video content without watching."
---

# YouTube Transcript

## Overview

Extract YouTube video transcripts, metadata, and chapters using yt-dlp. Output formatted as Markdown with YAML frontmatter, saved to Thao-OS `01-Worlds/life/01 - Notes/`.

## Usage

To extract a transcript from a YouTube video:

```bash
python3 ~/.claude/skills/tp-youtube-transcript/scripts/extract_transcript.py <youtube_url>
```

Optional: Specify custom output filename:

```bash
python3 ~/.claude/skills/tp-youtube-transcript/scripts/extract_transcript.py <youtube_url> custom_filename.md
```

## Output Format

### YAML Frontmatter

Uses Thao-OS note schema:

- `categories` — `[[Learning Notes]]`
- `subjects` — inferred from content
- `status` — `capture`
- `created` — today's date
- `source` — YouTube URL
- Standard video metadata: title, channel, upload_date, duration, tags, view_count, like_count

### Body Structure

Transcript organized by video chapters (if available):

```markdown
## Chapter Title

**00:05:23** Transcript text for this segment.

**00:05:45** Next segment text.
```

If no chapters exist, all content appears under "## Transcript" heading.

## Workflow

1. Extract metadata and subtitles using yt-dlp
2. Parse VTT subtitle format to extract timestamps and text
3. Group transcript segments by video chapters (if present)
4. Format as Markdown with Thao-OS frontmatter
5. Save to `<vault>/01-Worlds/life/01 - Notes/` with date-prefixed filename (`<vault>` resolved the same way as `scripts/extract_transcript.py` — `$THAO_OS_VAULT` if set, else the Google Drive desktop sync folder)
6. Clean up temporary subtitle files

## After extraction

After saving the transcript, ALWAYS:

1. **Create a summary note** — read the transcript and write a human-facing summary note in `01-Worlds/life/01 - Notes/` using the appropriate category (e.g. `[[AI Notes]]`, `[[Learning Notes]]`). Filename: `YYYY-MM-DD - <Category> - <Short Title>.md`. Include:
   - Link to source URL
   - Wikilink to the transcript: `[[YYYY-MM-DD - Transcript - Title]]`
   - Key takeaways, decisions, actionable insights
   - Relevant to Thao's goals (AI, automation, health, side business, career)

2. **Tag transcript with `[[Transcripts]]` subject** — always add to the transcript frontmatter.

3. **When linking in daily note or capture** — always link the **summary note**, not the transcript. The transcript is for agent reading only.

## Deduplication

To remove duplicates from existing transcript files:

```bash
python3 ~/.claude/skills/tp-youtube-transcript/scripts/deduplicate_transcript.py <markdown_file>
```

## Requirements

- `yt-dlp` (installed via Homebrew: `brew install yt-dlp`)

## Limitations

- Extracts English subtitles (auto-generated or manual)
- Requires video to have subtitles available
- Does not download video or audio files
- Description truncated to 500 characters in frontmatter
