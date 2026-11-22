"""Fail the build when materials.yml has an incomplete entry or points to a missing file."""

import pathlib
import sys

import yaml

REQUIRED = ("week", "topic", "kind", "title")

root = pathlib.Path(__file__).resolve().parent.parent
entries = yaml.safe_load((root / "materials.yml").read_text()) or []

problems = []
for i, entry in enumerate(entries, start=1):
    label = f"materials.yml entry {i} ({entry.get('title', 'untitled')})"
    missing = [key for key in REQUIRED if key not in entry]
    if missing:
        problems.append(f"{label}: missing {', '.join(missing)}")
    if "file" in entry and not (root / entry["file"]).is_file():
        problems.append(f"{label}: file not found: {entry['file']}")
    if "file" in entry and "href" in entry:
        problems.append(f"{label}: give either file or href, not both")

if problems:
    sys.exit("Materials check failed:\n  " + "\n  ".join(problems))
print(f"Materials check passed: {len(entries)} entries.")
