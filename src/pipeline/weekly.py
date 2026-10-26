"""Weekly report: a short factual summary of one Monday–Sunday week (Boston dates).

Built from the real records: content/entries/, logs/daily/ and logs/changes.md.
Each week's report is written once to reports/weekly/<YYYY-Www>.md and never
regenerated. The daily run then adds 2–4 sentences of highlights and lessons
under "Agent notes".

    python3 src/pipeline/weekly.py              # write the most recently finished week, if it's due
    python3 src/pipeline/weekly.py 2026-W43     # write a specific week (if it doesn't exist yet)
"""

import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "pipeline"))
sys.path.insert(0, str(ROOT / "src" / "news"))
from timewindow import BOSTON  # noqa: E402

ENTRIES = ROOT / "content" / "entries"
DAILY_LOGS = ROOT / "logs" / "daily"
CHANGES = ROOT / "logs" / "changes.md"
REPORTS = ROOT / "reports" / "weekly"
CONFIG = json.loads((ROOT / "config" / "pipeline.json").read_text())
NOTES_PLACEHOLDER = "_(to be added by the daily run: 2–4 sentences of highlights and lessons)_"


def week_label(day):
    year, week, _ = day.isocalendar()
    return f"{year}-W{week:02d}"


def week_monday(label):
    return datetime.strptime(label + "-1", "%G-W%V-%u").date()


def last_finished_week(due_day):
    """The newest week whose Sunday entry is already due (on a Sunday after 9 p.m., that same week)."""
    d = date.fromisoformat(due_day)
    sunday = d - timedelta(days=(d.weekday() + 1) % 7)
    return week_label(sunday)


def read(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def has_activity(monday, entries_dir=ENTRIES, logs_dir=DAILY_LOGS):
    days = [(monday + timedelta(days=i)).isoformat() for i in range(7)]
    return any((entries_dir / f"{d}.json").exists() or (logs_dir / f"{d}.json").exists() for d in days)


def week_due(due_day, reports_dir=REPORTS, entries_dir=ENTRIES, logs_dir=DAILY_LOGS):
    """Return the label of the finished week that still needs a report, or None."""
    label = last_finished_week(due_day)
    if (reports_dir / f"{label}.md").exists():
        return None
    return label if has_activity(week_monday(label), entries_dir, logs_dir) else None


def boston_day(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(BOSTON).date().isoformat() if ts else "?"


def owner_feedback(monday, sunday, changes_path=CHANGES):
    """Headings and owner quotes from logs/changes.md sections dated inside the week."""
    if not changes_path.exists():
        return []
    out, current = [], None
    for line in changes_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (\d{4}-\d{2}-\d{2})\S*\s*[:—-]?\s*(.*)$", line)
        if m:
            day = date.fromisoformat(m.group(1))
            current = {"date": m.group(1), "title": m.group(2).strip(), "owner": None} if monday <= day <= sunday else None
            if current:
                out.append(current)
        elif current and current["owner"] is None and re.match(r"^\*\*Owner[^*]*:\*\*", line):
            text = re.sub(r"^\*\*Owner[^*]*:\*\*\s*", "", line).strip().strip('"“”').strip()
            current["owner"] = text[:220] + ("…" if len(text) > 220 else "")
    return out


def build(label, entries_dir=ENTRIES, logs_dir=DAILY_LOGS, changes_path=CHANGES, launch=None):
    monday = week_monday(label)
    sunday = monday + timedelta(days=6)
    launch = launch if launch is not None else CONFIG["launch_date"]
    rows, flags, usage = [], [], {"article_reads": 0, "web_searches": 0, "render_rounds": 0}
    counts = {"published": 0, "backfilled": 0, "pending": 0, "missing": 0}
    for i in range(7):
        day = (monday + timedelta(days=i)).isoformat()
        entry = read(entries_dir / f"{day}.json") or {}
        log = read(logs_dir / f"{day}.json") or {"runs": []}
        status = entry.get("status") or "missing"
        counts[status if status in counts else "pending"] += 1
        failed_runs = [r for r in log["runs"] if r.get("outcome") == "failed"]
        for run in log["runs"]:
            for key in usage:
                usage[key] += (run.get("usage") or {}).get(key, 0) or 0
        made = boston_day(entry.get("published_at")) if entry.get("published_at") else "–"
        tag = " (pre-launch)" if entry.get("prelaunch") else ""
        rows.append(f"| {day} | {status}{tag} | {entry.get('title', '–')} | {made} |")
        after_launch = launch and day >= launch
        if status == "backfilled":
            flags.append(f"- **{day}: missed on schedule, recovered late** (published {made}). "
                         f"Reason: {(entry.get('backfill') or {}).get('reason') or 'not recorded'}")
        for run in failed_runs:
            flags.append(f"- **{day}: failed run**: {run.get('reason', 'no reason recorded')}")
        if status in ("missing", "pending", "failed") and after_launch:
            flags.append(f"- **{day}: still unresolved** (no published entry yet); queued for backfill")
    feedback = owner_feedback(monday, sunday, changes_path)

    lines = [f"# Weekly report {label} ({monday:%b %d} – {sunday:%b %d, %Y})", "",
             f"Generated {datetime.now(BOSTON):%Y-%m-%d %H:%M} Boston time from `content/entries/`, `logs/daily/` and `logs/changes.md`.",
             f"Launch date: {launch or 'not set yet: entries this week are pre-launch dry runs'}.", "",
             "## Entries", "", "| News date | Status | Title | Made on |", "|---|---|---|---|", *rows, "",
             f"Published on time: {counts['published']} · Backfilled late: {counts['backfilled']} · "
             f"Pending/failed: {counts['pending']} · No entry: {counts['missing']}", "",
             "## Missed runs and recoveries", "", *(flags or ["- None this week."]), "",
             "## Usage (from run logs)", "",
             f"- Article reads: {usage['article_reads']} · Web searches: {usage['web_searches']} · "
             f"Art render rounds: {usage['render_rounds']}", "",
             "## Owner feedback and decisions", "",
             *([f"- {f['date']}: {f['title']}" + (f": \"{f['owner']}\"" if f["owner"] else "") for f in feedback]
               or ["- None recorded this week."]), "",
             "## Agent notes", "", NOTES_PLACEHOLDER, ""]
    return "\n".join(lines)


def write(label, reports_dir=REPORTS, **kwargs):
    path = reports_dir / f"{label}.md"
    if path.exists():
        return None  # never regenerate a week
    reports_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(build(label, **kwargs), encoding="utf-8")
    return path


def main(argv):
    import daily
    label = argv[0] if argv else week_due(daily.due_day())
    if not label:
        print("No weekly report due.")
        return 0
    path = write(label)
    print(f"Wrote {path.relative_to(ROOT)}" if path else f"{label} already exists; not regenerated.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
