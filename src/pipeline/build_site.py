"""Build public/entries.json from the dated entry files in content/entries/.

Each file in content/entries/ is one day's entry (YYYY-MM-DD.json). This script
checks every entry, keeps only the ones that are ready to show the public
(status "published" or "backfilled"), and writes them to public/entries.json,
which the gallery page reads.

Run it from the project folder:
    python3 src/pipeline/build_site.py

It uses only the Python standard library, so there is nothing to install.
"""

import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENTRIES_DIR = ROOT / "content" / "entries"
PUBLIC_DIR = ROOT / "public"
OUTPUT = PUBLIC_DIR / "entries.json"

PUBLIC_STATUSES = {"published", "backfilled"}
ALL_STATUSES = PUBLIC_STATUSES | {"pending", "failed"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LAST_DAY = "2026-12-18"


def validate(entry, filename):
    """Return a list of problems with one entry (empty list means it's fine)."""
    problems = []
    date = entry.get("date", "")
    if not DATE_RE.match(date):
        problems.append("date must look like YYYY-MM-DD")
    elif filename != f"{date}.json":
        problems.append(f"file name should be {date}.json")
    elif date > LAST_DAY and not entry.get("sample"):
        problems.append(f"date is after the project's last day ({LAST_DAY})")

    status = entry.get("status")
    if status not in ALL_STATUSES:
        problems.append(f"status must be one of {sorted(ALL_STATUSES)}")
    if status not in PUBLIC_STATUSES:
        return problems  # pending/failed entries are not checked further

    for field in ("title", "caption", "published_at"):
        if not entry.get(field):
            problems.append(f"missing {field}")

    art = entry.get("artwork") or {}
    if not art.get("alt"):
        problems.append("missing artwork alt text")
    path = art.get("path", "")
    if not path:
        problems.append("missing artwork path")
    elif path.startswith(("/", "http:", "https:")) or ".." in path:
        problems.append("artwork path must be relative to public/")
    elif not (PUBLIC_DIR / path).is_file():
        problems.append(f"artwork file not found: public/{path}")

    stories = entry.get("stories") or []
    if not stories:
        problems.append("no stories listed")
    for story in stories:
        for src in story.get("sources") or []:
            if not str(src.get("url", "")).startswith("https://"):
                problems.append(f"source URL must be https: {src.get('url')}")
    if status == "backfilled" and not (entry.get("backfill") or {}).get("reason"):
        problems.append("backfilled entry needs backfill.reason")
    return problems


def load_entries(entries_dir=ENTRIES_DIR):
    """Read all entry files. Returns (public_entries, errors_by_file)."""
    public, errors = [], {}
    for path in sorted(entries_dir.glob("*.json")):
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors[path.name] = [f"not valid JSON: {exc}"]
            continue
        problems = validate(entry, path.name)
        if problems:
            errors[path.name] = problems
        elif entry["status"] in PUBLIC_STATUSES:
            public.append(entry)
    public.sort(key=lambda e: e["date"], reverse=True)
    return public, errors


def write_atomically(path, data):
    """Write to a temporary file, then swap it in, so the site never sees half a file."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def main():
    public, errors = load_entries()
    for name, problems in errors.items():
        for p in problems:
            print(f"  ✗ {name}: {p}", file=sys.stderr)
    if errors:
        print(f"Build stopped: {len(errors)} entry file(s) have problems.", file=sys.stderr)
        return 1
    write_atomically(OUTPUT, {"entries": public})
    print(f"Wrote {len(public)} public entries to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
