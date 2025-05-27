#!/usr/bin/env python3
import os
import json
from pathlib import Path

# --- CONFIGURATION ---
SUBMISSIONS_DIR = Path(__file__).parent.parent / "submissions"
OUTPUT_MD       = Path(__file__).parent.parent / "thread.md"
OUTPUT_JSON     = Path(__file__).parent.parent / "rollmates.json"
# ----------------------

def load_submissions(directory: Path):
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
        msg  = data.get("message", "").strip()
        email = data.get("email", "").strip()
        facebook = data.get("facebook", "").strip()

        if not roll or len(roll) < 2:
            print(f"⚠️  Skipping entry with invalid roll in {file.name}")
            continue
        if not name:
            print(f"⚠️  Warning: missing name in {file.name}")
        if not msg:
            print(f"⚠️  Warning: missing message in {file.name}")

        batch = roll[:2]  # derive batch from roll prefix

        entries.append({
            "roll": roll,
            "name": name or "UNKNOWN",
            "batch": batch,
            "message": msg or "",
            "email": email,
            "facebook": facebook
        })

    # sort by roll number (lexicographically works since same length)
    return sorted(entries, key=lambda e: e["roll"])


def write_markdown(entries, path: Path):
    with path.open("w", encoding="utf-8") as out:
        out.write("# 🧵 Rollmates Thread\n\n")
        for e in entries:
            out.write(f"## 🎓 {e['roll']} – {e['name']}\n")
            out.write(f"**Batch:** {e['batch']}\n\n")
            
            # Add email and Facebook if available
            if e.get('email'):
                out.write(f"**Email:** {e['email']}\n\n")
            if e.get('facebook'):
                out.write(f"**Facebook:** [{e['facebook']}]({e['facebook']})\n\n")
                
            out.write(f"📝 {e['message']}\n\n")
            out.write("---\n\n")
    print(f"✅ Generated Markdown thread at {path}")


def write_json_manifest(entries, path: Path):
    # Include all fields in the JSON output
    manifest = [
        {
            "roll": e["roll"], 
            "name": e["name"], 
            "message": e["message"],
            "batch": e["batch"],
            "email": e.get("email", ""),
            "facebook": e.get("facebook", "")
        }
        for e in entries
    ]
    with path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"✅ Wrote JSON manifest at {path}")


def main():
    if not SUBMISSIONS_DIR.exists():
        print(f"❌ Submissions directory not found: {SUBMISSIONS_DIR}")
        return

    entries = load_submissions(SUBMISSIONS_DIR)
    if not entries:
        print("⚠️  No valid submissions found.")
    else:
        write_markdown(entries, OUTPUT_MD)
        write_json_manifest(entries, OUTPUT_JSON)


if __name__ == "__main__":
    main()
