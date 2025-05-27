#!/usr/bin/env python3
import os
import json
from datetime import datetime
from pathlib import Path

# --- CONFIGURATION ---
BASE_DIR         = Path(__file__).parent.parent
SUBMISSIONS_DIR  = BASE_DIR / "submissions"
OUTPUT_TIMELINE  = BASE_DIR / "Timeline.md"
# ----------------------

def load_timeline_entries(directory: Path):
    entries = []
    for file in sorted(directory.iterdir()):
        if file.suffix.lower() != ".json":
            continue

        try:
            data = json.loads(file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"⚠️  Skipping invalid JSON ({file.name}): {e}")
            continue

        roll = data.get("roll")
        name = data.get("name", "").strip()
        if not roll or not name:
            print(f"⚠️  Skipping incomplete entry in {file.name}")
            continue

        # Use filesystem creation time; switch to git commit date if needed
        timestamp = os.path.getctime(file)
        dt = datetime.fromtimestamp(timestamp)

        entries.append((dt, roll, name))

    # Sort chronologically
    return sorted(entries, key=lambda x: x[0])


def write_timeline(entries, path: Path):
    with path.open("w", encoding="utf-8") as out:
        out.write("# 📅 Rollmates Timeline\n\n")
        for dt, roll, name in entries:
            out.write(f"- **{dt.date()}** — `{roll}` ({name})\n")
    print(f"✅ Generated timeline at {path}")


def main():
    if not SUBMISSIONS_DIR.exists():
        print(f"❌ Submissions directory not found: {SUBMISSIONS_DIR}")
        return

    entries = load_timeline_entries(SUBMISSIONS_DIR)
    if not entries:
        print("⚠️  No valid submissions found.")
    else:
        write_timeline(entries, OUTPUT_TIMELINE)


if __name__ == "__main__":
    main()
