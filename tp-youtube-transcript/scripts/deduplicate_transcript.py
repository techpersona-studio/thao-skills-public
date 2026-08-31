#!/usr/bin/env python3
"""
Remove duplicate consecutive transcript lines from YouTube transcript markdown files.
"""

import sys
import re
from pathlib import Path


def deduplicate_transcript(file_path):
    """Remove duplicate and prefix transcript entries."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    transcript_entries = []
    in_transcript = False

    for i, line in enumerate(lines):
        if line.strip().startswith('## '):
            in_transcript = True

        if in_transcript and line.strip().startswith('**') and '**' in line[2:]:
            match = re.match(r'\*\*([^*]+)\*\*\s*(.*)', line.strip())
            if match:
                timestamp, text = match.groups()
                text = text.strip()
                transcript_entries.append((i, timestamp, text))

    lines_to_keep = set()

    for idx in range(len(transcript_entries)):
        line_num, timestamp, text = transcript_entries[idx]

        is_prefix = False
        for next_idx in range(idx + 1, min(idx + 5, len(transcript_entries))):
            _, next_timestamp, next_text = transcript_entries[next_idx]

            if next_text.startswith(text) and len(next_text) > len(text):
                is_prefix = True
                break

        if not is_prefix:
            lines_to_keep.add(line_num)

    output = []
    for i, line in enumerate(lines):
        if i not in {e[0] for e in transcript_entries}:
            output.append(line)
        elif i in lines_to_keep:
            output.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(output)

    return len(lines), len(output)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 deduplicate_transcript.py <markdown_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    original_lines, final_lines = deduplicate_transcript(file_path)
    removed = original_lines - final_lines

    print(f"Original: {original_lines} lines")
    print(f"Final: {final_lines} lines")
    print(f"Removed: {removed} duplicate lines")
