#!/usr/bin/env python3
"""
Extract YouTube video transcripts and metadata to Markdown format.
Saves to Thao-OS 01-Worlds/life/01 - Notes/ with Thao-OS frontmatter.
"""

import json
import os
import subprocess
import sys
import re
from pathlib import Path
from datetime import date


def _find_vault_notes_dir():
    """Locate the Thao-OS vault's Notes folder: THAO_OS_VAULT env var
    (pointing at '01-Worlds/life'), else the first matching Google Drive
    desktop sync folder under ~/Library/CloudStorage."""
    override = os.environ.get("THAO_OS_VAULT")
    if override:
        return Path(override) / "01 - Notes"
    matches = sorted(Path.home().glob(
        "Library/CloudStorage/GoogleDrive-*/My Drive/Thao-OS/01-Worlds/life"
    ))
    if matches:
        return matches[0] / "01 - Notes"
    sys.exit(
        "Could not find the Thao-OS vault. Set THAO_OS_VAULT to its "
        "'01-Worlds/life' path, or make sure Google Drive desktop sync is running."
    )


def sanitize_filename(title):
    """Convert video title to safe filename."""
    clean = re.sub(r'[<>:"/\\|?*]', '', title)
    clean = clean.replace('  ', ' ').strip()
    return clean[:100]


def format_duration(seconds):
    """Convert seconds to HH:MM:SS format."""
    if not seconds:
        return "00:00:00"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def extract_metadata(url):
    """Extract video metadata using yt-dlp."""
    cmd = [
        'yt-dlp',
        '--dump-json',
        '--no-download',
        '--cookies-from-browser', 'chrome',
        url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to extract metadata: {result.stderr}")

    return json.loads(result.stdout)


def extract_subtitles(url, video_id):
    """Extract English subtitles/transcript using yt-dlp."""
    output_template = f'/tmp/{video_id}'

    for old_file in Path('/tmp').glob(f'{video_id}*.vtt'):
        old_file.unlink()

    cmd = [
        'yt-dlp',
        '--write-auto-subs',
        '--write-subs',
        '--sub-lang', 'en',
        '--sub-format', 'vtt',
        '--skip-download',
        '--cookies-from-browser', 'chrome',
        '-o', output_template,
        url
    ]

    subprocess.run(cmd, capture_output=True, text=True)

    subtitle_files = list(Path('/tmp').glob(f'{video_id}*.vtt'))
    if subtitle_files:
        return subtitle_files[0]

    return None


def parse_vtt(vtt_path):
    """Parse VTT subtitle file, extracting clean non-overlapping text."""
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    entries = []
    current_time = None
    current_text = []

    for line in lines:
        if '-->' in line:
            if current_time and current_text:
                entries.append((current_time, ' '.join(current_text)))
            current_time = line.split('-->')[0].strip()
            current_text = []
        elif line.strip() and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and not line.isdigit():
            clean_text = re.sub(r'<[^>]+>', '', line)
            if clean_text.strip():
                current_text.append(clean_text.strip())

    if current_time and current_text:
        entries.append((current_time, ' '.join(current_text)))

    # Deduplicate: auto-generated VTT repeats text across overlapping cues.
    # Keep only the NEW text from each cue by removing any prefix that appeared in the previous cue.
    deduplicated = []
    prev_text = ""

    for timestamp, text in entries:
        # Find the longest suffix of prev_text that is a prefix of text
        new_text = text
        if prev_text:
            # Try to find where the overlap ends
            for split_point in range(min(len(text), len(prev_text)), 0, -1):
                if prev_text.endswith(text[:split_point]):
                    new_text = text[split_point:].strip()
                    break

        if new_text and new_text != prev_text:
            deduplicated.append((timestamp, new_text))

        prev_text = text

    # Merge into ~60-word paragraphs for readability
    merged = []
    current_words = []
    current_ts = None

    for timestamp, text in deduplicated:
        if current_ts is None:
            current_ts = timestamp
        current_words.extend(text.split())

        if len(current_words) >= 60:
            merged.append((current_ts, ' '.join(current_words)))
            current_words = []
            current_ts = None

    if current_words:
        merged.append((current_ts or "00:00:00", ' '.join(current_words)))

    return merged


def group_by_chapters(transcript_entries, chapters):
    """Group transcript entries by video chapters."""
    if not chapters:
        return [("Transcript", transcript_entries)]

    grouped = []
    chapter_times = [(ch['start_time'], ch['title']) for ch in chapters]
    chapter_times.append((float('inf'), None))

    for i, (start_time, title) in enumerate(chapter_times[:-1]):
        next_start = chapter_times[i + 1][0]

        chapter_entries = []
        for timestamp, text in transcript_entries:
            parts = timestamp.split(':')
            if len(parts) == 3:
                h, m, s = parts
                total_seconds = int(h) * 3600 + int(m) * 60 + float(s)
            else:
                m, s = parts
                total_seconds = int(m) * 60 + float(s)

            if start_time <= total_seconds < next_start:
                chapter_entries.append((timestamp, text))

        if chapter_entries:
            grouped.append((title, chapter_entries))

    return grouped if grouped else [("Transcript", transcript_entries)]


def create_markdown(metadata, transcript_entries):
    """Create Markdown document with Thao-OS frontmatter."""
    title = metadata.get('title', 'Unknown')
    channel = metadata.get('channel', metadata.get('uploader', 'Unknown'))
    url = metadata.get('webpage_url', '')
    upload_date = metadata.get('upload_date', '')
    if upload_date:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
    duration = format_duration(metadata.get('duration'))
    description = metadata.get('description', '').replace('\n', ' ').strip()
    tags = metadata.get('tags', [])
    view_count = metadata.get('view_count', 0)
    like_count = metadata.get('like_count', 0)
    chapters = metadata.get('chapters', [])
    today = date.today().isoformat()

    md = "---\n"
    md += "categories:\n"
    md += '  - "[[Learning Notes]]"\n'
    md += "subjects:\n"
    md += '  - "[[AI]]"\n'
    md += "status: capture\n"
    md += f"created: {today}\n"
    md += f"updated: {today}\n"
    md += f"source: {url}\n"
    md += "project:\n"
    md += "review_cycle:\n"
    md += "ai_summary:\n"
    md += "next_review:\n"
    md += f"title: \"{title}\"\n"
    md += f"channel: \"{channel}\"\n"
    md += f"upload_date: {upload_date}\n"
    md += f"duration: {duration}\n"
    md += f"description: \"{description[:500]}\"\n"
    md += f"tags: {json.dumps(tags)}\n"
    md += f"view_count: {view_count}\n"
    md += f"like_count: {like_count}\n"
    md += "---\n\n"

    md += f"# {title}\n\n"
    md += f"**Channel:** {channel}  \n"
    md += f"**Duration:** {duration}  \n"
    md += f"**Uploaded:** {upload_date}  \n\n"

    grouped = group_by_chapters(transcript_entries, chapters)

    for chapter_title, entries in grouped:
        md += f"## {chapter_title}\n\n"

        for timestamp, text in entries:
            simple_ts = timestamp.split('.')[0]
            md += f"**{simple_ts}** {text}\n\n"

    return md


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_transcript.py <youtube_url> [output_filename]")
        sys.exit(1)

    url = sys.argv[1]
    custom_filename = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Extracting metadata from {url}...")
    metadata = extract_metadata(url)

    video_id = metadata['id']
    title = metadata.get('title', 'Unknown')

    print(f"Extracting subtitles for: {title}")
    subtitle_file = extract_subtitles(url, video_id)

    if not subtitle_file:
        print("No subtitles available for this video.")
        sys.exit(1)

    print("Found English subtitles")

    print("Parsing transcript...")
    transcript_entries = parse_vtt(subtitle_file)
    print(f"Processed {len(transcript_entries)} segments")

    print("Creating Markdown document...")
    markdown = create_markdown(metadata, transcript_entries)

    vault_path = _find_vault_notes_dir()
    today = date.today().isoformat()

    if custom_filename:
        output_file = vault_path / custom_filename
    else:
        filename = f"{today} - Transcript - {sanitize_filename(title)}.md"
        output_file = vault_path / filename

    vault_path.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"Saved to: {output_file}")

    if subtitle_file.exists():
        subtitle_file.unlink()


if __name__ == '__main__':
    main()
