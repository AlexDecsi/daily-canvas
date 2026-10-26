"""The daily run's bookkeeping: the steps that must be exact, not judged.

Claude (the editor and artist) does the judgment steps described in
ops/daily-run.md: choosing stories, writing the brief, drawing, captioning.
This script handles everything around them:

    python3 src/pipeline/daily.py status
        Today's Boston date, whether it's done, and missed days to backfill.

    python3 src/pipeline/daily.py due
        A quick check for the scheduled task: prints NOTHING TO DO (exit 2) when the
        due day is published, no missed days are waiting, no commits are waiting to be
        pushed and no weekly report is due, so the backup runs (11:07 p.m., 8:07 a.m.) cost almost nothing.

    python3 src/pipeline/daily.py prepare [YYYY-MM-DD]
        (No date: the day that is due: today after 9 p.m. Boston time, else yesterday.)
        Lock the date, stop if it's already published, start the run log, and
        gather news: feeds for today, Wikipedia-as-of-that-day for past dates.

    python3 src/pipeline/daily.py finalize YYYY-MM-DD
        Check the brief, the artwork, the caption draft and the source links;
        then publish atomically: write the entry and rebuild the site, rolling
        back if anything fails. Never overwrites a published entry.

    python3 src/pipeline/daily.py fail YYYY-MM-DD "reason"
        Record that the date couldn't be done (it stays flagged for backfill).

Exit codes: 0 = done/OK, 1 = blocked or failed (see message), 2 = already published,
3 = outside the project window, 4 = another run holds the lock.
"""

import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "news"))
sys.path.insert(0, str(ROOT / "src" / "pipeline"))
sys.path.insert(0, str(ROOT / "src" / "art"))

import brief as brief_check  # noqa: E402
import build_site  # noqa: E402
import check_art  # noqa: E402
from timewindow import BOSTON, iso, today_in_boston  # noqa: E402

CONFIG = json.loads((ROOT / "config" / "pipeline.json").read_text())
LIMITS = CONFIG["limits"]
ENTRIES = ROOT / "content" / "entries"
LOCKS = ROOT / "cache" / "locks"
DRAFTS = ROOT / "cache" / "drafts"
DAILY_LOGS = ROOT / "logs" / "daily"
RESEARCH = ROOT / "logs" / "research"
PUBLIC_STATUSES = {"published", "backfilled"}


# ---------- small helpers ----------

def now_utc():
    return datetime.now(timezone.utc)


def write_json_atomically(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def read_json(path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def entry_status(day, entries_dir=ENTRIES):
    entry = read_json(entries_dir / f"{day}.json")
    return entry.get("status") if entry else None


def is_published(day, entries_dir=ENTRIES):
    return entry_status(day, entries_dir) in PUBLIC_STATUSES


def due_day(now=None, publish_time=None):
    """The newest news day that should be finished by now: today from 9 p.m. Boston time, otherwise yesterday.

    A run that starts late (e.g. the Mac was asleep at 9 p.m. and wakes at 7 a.m.) finishes the evening it
    missed instead of starting a half-day entry for a day whose news isn't over yet.
    """
    now = (now or now_utc()).astimezone(BOSTON)
    hour, minute = map(int, (publish_time or CONFIG["target_publish_time"]).split(":"))
    if (now.hour, now.minute) >= (hour, minute):
        return now.date().isoformat()
    return (now.date() - timedelta(days=1)).isoformat()


def missing_dates(today, launch, last_day, entries_dir=ENTRIES):
    """Dates from launch up to yesterday (and no later than last_day) without a public entry, oldest first."""
    if not launch:
        return []
    end = min(date.fromisoformat(today) - timedelta(days=1), date.fromisoformat(last_day))
    day, out = date.fromisoformat(launch), []
    while day <= end:
        if not is_published(day.isoformat(), entries_dir):
            out.append(day.isoformat())
        day += timedelta(days=1)
    return out


# ---------- lock ----------

def acquire_lock(day, locks_dir=LOCKS, stale_minutes=None):
    stale_minutes = stale_minutes or LIMITS["lock_stale_minutes"]
    locks_dir.mkdir(parents=True, exist_ok=True)
    lock = locks_dir / f"{day}.lock"
    if lock.exists():
        held = datetime.fromisoformat(lock.read_text().strip())
        if now_utc() - held < timedelta(minutes=stale_minutes):
            return False
        lock.unlink()  # a crashed run left it behind
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w") as f:
        f.write(now_utc().isoformat())
    return True


def release_lock(day, locks_dir=LOCKS):
    (locks_dir / f"{day}.lock").unlink(missing_ok=True)


# ---------- run log ----------

def log_path(day):
    return DAILY_LOGS / f"{day}.json"


def update_log(day, **fields):
    log = read_json(log_path(day), {"date": day, "runs": []})
    run = log["runs"][-1] if log["runs"] and log["runs"][-1].get("outcome") == "in_progress" else None
    if run is None or fields.pop("_new_run", False):
        run = {"started_at": iso(now_utc()), "outcome": "in_progress", "steps": []}
        log["runs"].append(run)
    step = fields.pop("step", None)
    if step:
        run["steps"].append({"at": iso(now_utc()), "step": step})
    run.update(fields)
    write_json_atomically(log_path(day), log)
    return log


# ---------- commands ----------

def cmd_status():
    today, due = today_in_boston(), due_day()
    launch, last = CONFIG["launch_date"], CONFIG["last_day"]
    print(f"Boston date today: {today}   (target publish ~{CONFIG['target_publish_time']} {CONFIG['timezone']})")
    print(f"Launch date: {launch or 'not set yet (pre-launch dry runs)'}   Last day: {last}")
    print(f"Due now: {due} -> entry: {entry_status(due) or 'none'}")
    missing = missing_dates(due, launch, last)
    cap = LIMITS["backfill_dates_per_run"]
    print(f"Missed days needing backfill: {len(missing)}" + (f" -> this run takes {missing[:cap]}" if missing else ""))
    if len(missing) > cap:
        print(f"  backlog remains after this run: {missing[cap:]}")
    if due > last:
        print("The project window has ended: no new daily entries (backfill/corrections only with owner approval).")
    return 0


def unpushed_commits():
    """Number of local commits not yet on GitHub (0 if it can't be determined)."""
    result = subprocess.run(["git", "rev-list", "--count", "origin/main..HEAD"], cwd=ROOT, capture_output=True, text=True)
    return int(result.stdout.strip() or 0) if result.returncode == 0 else 0


def cmd_due():
    import weekly  # local import: weekly.py imports this module too
    due = due_day()
    work = []
    if due <= CONFIG["last_day"] and not is_published(due):
        work.append(f"{due} is due")
    missing = [d for d in missing_dates(due, CONFIG["launch_date"], CONFIG["last_day"]) if d != due]
    if missing:
        work.append(f"{len(missing)} missed day(s): {missing[:LIMITS['backfill_dates_per_run']]}")
    pushes = unpushed_commits()
    if pushes:
        work.append(f"{pushes} commit(s) waiting to be pushed")
    week = weekly.week_due(due)
    if week:
        work.append(f"weekly report {week} is due")
    if not work:
        print(f"NOTHING TO DO (due day {due} is published; no backlog, pushes or reports waiting)")
        return 2
    print("WORK: " + "; ".join(work))
    return 0


def cmd_prepare(day=None):
    today = today_in_boston()
    day = day or due_day()
    if day > CONFIG["last_day"]:
        print(f"{day} is after the project's last day ({CONFIG['last_day']}). Stopping.")
        return 3
    if CONFIG["launch_date"] and day < CONFIG["launch_date"]:
        print(f"{day} is before the launch date ({CONFIG['launch_date']}). Stopping.")
        return 3
    if day > today:
        print(f"{day} is in the future (Boston). Stopping.")
        return 3
    if not acquire_lock(day):
        print(f"Another run is working on {day} (lock held). Stopping without changes.")
        return 4
    if is_published(day):
        release_lock(day)
        print(f"{day} is already published. Nothing to do (no duplicate).")
        update_log(day, _new_run=True, outcome="already_published", step="prepare: entry exists, no action")
        return 2

    mode = "live" if day == today else "backfill"
    prelaunch = CONFIG["launch_date"] is None
    update_log(day, _new_run=True, mode=mode, prelaunch=prelaunch, step=f"prepare: lock acquired ({mode})")

    # Feeds still hold a day or two of past items, so recent missed days get the same US/Boston-focused
    # ranking; Wikipedia-as-of-that-day adds leads for backfill (it can't fail the run on its own).
    steps = [["src/news/feeds.py", day, True], ["src/news/cluster.py", day, True]]
    if mode == "backfill":
        steps.append(["src/news/wiki_events.py", day, False])
    for script, arg, required in steps:
        result = subprocess.run([sys.executable, str(ROOT / script), arg], capture_output=True, text=True, timeout=300)
        print(result.stdout.strip())
        if result.returncode != 0 and not required:
            update_log(day, step=f"prepare: optional {script} found nothing usable")
            continue
        if result.returncode != 0:
            msg = (result.stderr or result.stdout).strip()[-300:]
            update_log(day, step=f"prepare: {script} failed: {msg}")
            print(f"Research step failed: {script}. Record with: daily.py fail {day} \"...\"")
            return 1
        update_log(day, step=f"prepare: ran {script}")

    print(f"\nReady. Next (Claude): write logs/research/{day}/brief.json, then draw public/artwork/{day}.svg, "
          f"then write cache/drafts/{day}.entry.json, then run: daily.py finalize {day}")
    return 0


def link_ok(url, timeout):
    """Return (ok, note). Sites that block bots (401/403/429/451) count as 'unverified', not broken."""
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "DailyCanvas/0.1 (link check)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as err:
        if err.code in (401, 402, 403, 429, 451):
            return True, f"HTTP {err.code} (blocks automated checks; not verifiable here)"
        return False, f"HTTP {err.code}"
    except (urllib.error.URLError, TimeoutError) as err:
        return False, f"unreachable: {err}"[:120]


def build_entry(day, draft, brief, mode, prelaunch, art_meta):
    """Combine Claude's draft (title, caption, alt, stories shown) with exact computed fields."""
    brief_urls = {s["url"] for st in brief["stories"] for s in st["sources"]}
    stories = []
    for name in draft["stories_shown"]:
        match = next((st for st in brief["stories"] if st["name"] == name), None)
        if not match:
            raise ValueError(f"draft names a story not in the brief: {name!r}")
        stories.append({"name": match["name"], "role": match["role"], "facts": match["facts"],
                        "sources": [{k: s[k] for k in ("publisher", "title", "url", "published_at") if k in s}
                                    for s in match["sources"] if s["url"] in brief_urls]})
    is_backfill = mode == "backfill"
    return {
        "date": day,
        "published_at": iso(now_utc()),
        "status": "backfilled" if is_backfill else "published",
        "prelaunch": prelaunch,
        "title": draft["title"],
        "caption": draft["caption"],
        "stories": stories,
        "artwork": {"path": f"artwork/{day}.svg", "format": "svg", "alt": draft["alt"],
                    "method": "code-generated SVG (graphic-poster kit, src/art/daily/)",
                    "revision": art_meta.get("revision", "r1")},
        "backfill": {"is_backfill": is_backfill,
                     "reason": draft.get("backfill_reason") or ("Created after its news date" if is_backfill else None)},
    }


def remove_samples():
    """The first real entry replaces the clearly labelled sample data, so fake news never sits beside real news."""
    removed = []
    for path in ENTRIES.glob("*.json"):
        entry = read_json(path)
        if entry and entry.get("sample"):
            art = (entry.get("artwork") or {}).get("path")
            if art and (build_site.PUBLIC_DIR / art).exists():
                (build_site.PUBLIC_DIR / art).unlink()
            path.unlink()
            removed.append(path.name)
    return removed


def cmd_finalize(day):
    log = read_json(log_path(day))
    run = log["runs"][-1] if log and log["runs"] else {}
    if run.get("outcome") != "in_progress":
        print(f"No run in progress for {day}. Run prepare first.")
        return 1
    if is_published(day):
        print(f"{day} is already published; refusing to overwrite.")
        return 2
    problems = []

    brief = read_json(RESEARCH / day / "brief.json")
    if not brief:
        problems.append("missing brief")
    else:
        errors, warnings = brief_check.check(brief)
        problems += [f"brief: {e}" for e in errors]
        for w in warnings:
            print(f"  ! brief: {w}")

    svg = build_site.PUBLIC_DIR / "artwork" / f"{day}.svg"
    art_errors = check_art.check(svg, LIMITS["artwork_max_kb"])
    problems += [f"art: {e}" for e in art_errors]

    draft = read_json(DRAFTS / f"{day}.entry.json")
    if not draft:
        problems.append(f"missing draft cache/drafts/{day}.entry.json")
    else:
        words = len(draft.get("caption", "").split())
        if words > LIMITS["caption_max_words"]:
            problems.append(f"caption has {words} words (max {LIMITS['caption_max_words']})")
        if len(draft.get("alt", "")) > LIMITS["alt_max_chars"]:
            problems.append(f"alt text longer than {LIMITS['alt_max_chars']} characters")
        if not draft.get("art_reviewed"):
            problems.append("draft doesn't confirm the artwork was visually reviewed against the checklist (art_reviewed)")

    if problems:
        for p in problems:
            print(f"  ✗ {p}")
        update_log(day, step=f"finalize blocked: {len(problems)} problem(s)", problems=problems)
        print("BLOCKED. Fix and re-run finalize, or record: daily.py fail")
        return 1

    entry = build_entry(day, draft, brief, run.get("mode", "live"), run.get("prelaunch", True), draft.get("art", {}))
    link_notes = []
    for story in entry["stories"]:
        for src in story["sources"]:
            ok, note = link_ok(src["url"], LIMITS["link_check_timeout_seconds"])
            link_notes.append({"url": src["url"], "ok": ok, "note": note})
            if not ok:
                problems.append(f"broken source link: {src['url']} ({note})")
    entry_errors = build_site.validate(entry, f"{day}.json")
    problems += [f"entry: {e}" for e in entry_errors]
    if problems:
        for p in problems:
            print(f"  ✗ {p}")
        update_log(day, step="finalize blocked at link/entry check", problems=problems, link_checks=link_notes)
        return 1

    # publish atomically: entry file + rebuilt site; undo the entry if the build fails
    removed = remove_samples() if not entry.get("sample") else []
    target = ENTRIES / f"{day}.json"
    previous = read_json(target)  # a pending/failed placeholder may exist
    write_json_atomically(target, entry)
    public, errors = build_site.load_entries()
    if errors:
        if previous:
            write_json_atomically(target, previous)
        else:
            target.unlink()
        print(f"Site build failed after writing the entry; rolled back. {errors}")
        update_log(day, step="finalize: site build failed, rolled back", problems=[str(errors)])
        return 1
    build_site.write_atomically(build_site.OUTPUT, {"entries": public})
    release_lock(day)
    update_log(day, outcome=entry["status"], finished_at=iso(now_utc()), link_checks=link_notes,
               samples_removed=removed, stories_shown=draft["stories_shown"],
               usage=draft.get("usage", {}), step="finalize: published to local site")
    print(f"Published {day} ({entry['status']}{', pre-launch' if entry['prelaunch'] else ''}). "
          f"{len(public)} entries on the site." + (f" Removed sample entries: {removed}" if removed else ""))
    return 0


def cmd_fail(day, reason):
    if not is_published(day):
        write_json_atomically(ENTRIES / f"{day}.json", {"date": day, "status": "pending", "reason": reason,
                                                       "recorded_at": iso(now_utc())})
    update_log(day, outcome="failed", finished_at=iso(now_utc()), reason=reason, step=f"fail: {reason}")
    release_lock(day)
    print(f"Recorded {day} as pending: {reason}. It will be retried as a backfill and flagged in the weekly report.")
    return 0


def main(argv):
    if not argv or argv[0] not in ("status", "due", "prepare", "finalize", "fail"):
        print(__doc__)
        return 1
    cmd = argv[0]
    if cmd == "status":
        return cmd_status()
    if cmd == "due":
        return cmd_due()
    if cmd == "prepare":
        return cmd_prepare(argv[1] if len(argv) > 1 else None)
    if cmd == "finalize":
        return cmd_finalize(argv[1])
    return cmd_fail(argv[1], argv[2] if len(argv) > 2 else "unspecified")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
