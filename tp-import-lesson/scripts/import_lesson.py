#!/usr/bin/env python3
"""
import_lesson.py — move HTML + image files into Thao-OS life/05 - Views/
and print the markdown snippets needed to update the lesson note.
"""

import argparse
import glob
import os
import shutil
import sys


def _find_vault():
    """Locate the Thao-OS vault: THAO_OS_VAULT env var, else the first
    matching Google Drive desktop sync folder under ~/Library/CloudStorage."""
    override = os.environ.get("THAO_OS_VAULT")
    if override:
        return override
    matches = glob.glob(
        os.path.expanduser("~/Library/CloudStorage/GoogleDrive-*/My Drive/Thao-OS/01-Worlds/life")
    )
    if matches:
        return matches[0]
    sys.exit(
        "Could not find the Thao-OS vault. Set THAO_OS_VAULT to its "
        "'01-Worlds/life' path, or make sure Google Drive desktop sync is running."
    )


VAULT = _find_vault()
VIEWS_DIR = os.path.join(VAULT, "05 - Views")
NOTES_DIR = os.path.join(VAULT, "01 - Notes")


def slugify_title(title):
    """Return a short filesystem-safe version of the title."""
    keep = []
    for ch in title:
        if ch.isalnum() or ch in (" ", "-", "_", "ế", "ầ", "ọ", "ạ", "ả", "ề"):
            keep.append(ch)
    return "".join(keep).strip()


def dest_name(day, title, ext):
    short = slugify_title(title)
    if ext in (".html", ".md"):
        return f"{day} - {short} Notes{ext}"
    return f"{day} - {short}{ext}"


def copy_file(src, dst_dir, dst_name):
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, dst_name)
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.copy2(src, dst)
    return dst_name


def main():
    parser = argparse.ArgumentParser(description="Import lesson HTML + images into Thao-OS vault.")
    parser.add_argument("--html", help="Path to the HTML lesson file")
    parser.add_argument("--md", help="Path to a markdown source/canvas file (moved to 05 - Views/ as the human view)")
    parser.add_argument("--images", nargs="*", default=[], help="Paths to related image files")
    parser.add_argument("--lesson-note", required=True, help="Filename (without .md) of the lesson notes file in 01 - Notes/")
    parser.add_argument("--day", required=True, help="Lesson label, e.g. 'Day 4'")
    parser.add_argument("--title", required=True, help="Lesson title, e.g. 'Fat - Tầm quan trọng của chất béo'")
    parser.add_argument("--date", required=True, help="Session date YYYY-MM-DD")
    args = parser.parse_args()

    if not args.html and not args.md and not args.images:
        parser.error("Provide at least one of --html, --md, or --images.")

    html_dest = None
    md_dest = None

    # Move HTML view (if any)
    if args.html:
        html_ext = os.path.splitext(args.html)[1]
        html_dest = dest_name(args.day, args.title, html_ext)
        copy_file(args.html, VIEWS_DIR, html_dest)
        print(f"Moved HTML  → 05 - Views/{html_dest}")

    # Move markdown source/canvas view (if any)
    if args.md:
        md_dest = dest_name(args.day, args.title, ".md")
        copy_file(args.md, VIEWS_DIR, md_dest)
        print(f"Moved md    → 05 - Views/{md_dest}")

    # Copy images
    img_dests = []
    for img_path in args.images:
        img_name = os.path.basename(img_path)
        copy_file(img_path, VIEWS_DIR, img_name)
        img_dests.append(img_name)
        print(f"Copied image → 05 - Views/{img_name}")

    # Print markdown snippets
    if html_dest or md_dest:
        print()
        print("─── Add to Human views: ───")
        if html_dest:
            print(f"- [{html_dest}](../05%20-%20Views/{html_dest.replace(' ', '%20')})")
        if md_dest:
            # md views link with a wikilink (Obsidian resolves by basename)
            print(f"- [[{os.path.splitext(md_dest)[0]}]] — original md source")

    if img_dests:
        print()
        print("─── Add to Reference images: ───")
        for img in img_dests:
            print(f"- ![[{img}]]")

    print()
    print("─── New section to append: ───")
    print(f"## {args.day}: {args.title} ({args.date})")
    print()
    print("<!-- Add lesson notes here -->")
    print()

    print("─── Reminder: create the summary note ───")
    print(f"Write a processed summary note in 01 - Notes/ named:")
    print(f"  {args.date} - Lesson - {args.day} {args.title}.md")
    print("Use the standard frontmatter. QUOTE ai_summary if it contains a colon.")
    print("The 05 - Views/ file is the raw human view; the 01 - Notes/ file is the retrievable summary.")

    # Check lesson note exists
    note_path = os.path.join(NOTES_DIR, args.lesson_note + ".md")
    if not os.path.exists(note_path):
        print(f"⚠️  Lesson note not found: {note_path}")
        print("   Create the note first or check the --lesson-note value.")
    else:
        print(f"✓ Lesson note found: {note_path}")


if __name__ == "__main__":
    main()
