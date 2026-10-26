"""Checks for the daily run's bookkeeping: locks, idempotency, missed days, the project window, artwork checks.
No network. Run from the project folder:
    python3 -m unittest discover tests
"""

import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "pipeline"))
sys.path.insert(0, str(ROOT / "src" / "art"))
import check_art  # noqa: E402
import daily  # noqa: E402


class LockTests(unittest.TestCase):
    def test_second_run_is_refused_then_allowed_after_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            locks = Path(tmp)
            self.assertTrue(daily.acquire_lock("2026-11-02", locks))
            self.assertFalse(daily.acquire_lock("2026-11-02", locks))
            daily.release_lock("2026-11-02", locks)
            self.assertTrue(daily.acquire_lock("2026-11-02", locks))

    def test_stale_lock_is_taken_over(self):
        with tempfile.TemporaryDirectory() as tmp:
            locks = Path(tmp)
            old = datetime.now(timezone.utc) - timedelta(hours=5)
            (locks / "2026-11-02.lock").write_text(old.isoformat())
            self.assertTrue(daily.acquire_lock("2026-11-02", locks, stale_minutes=120))


class DueDayTests(unittest.TestCase):
    def at(self, iso_utc):
        return daily.due_day(datetime.fromisoformat(iso_utc), "21:00")

    def test_after_9pm_today_is_due(self):
        self.assertEqual(self.at("2026-10-27T01:10:00+00:00"), "2026-10-26")  # 9:10 p.m. EDT on Oct 26

    def test_before_9pm_yesterday_is_due(self):
        self.assertEqual(self.at("2026-10-27T11:00:00+00:00"), "2026-10-26")  # 7 a.m. EDT Oct 27: finish the missed evening
        self.assertEqual(self.at("2026-10-26T23:00:00+00:00"), "2026-10-25")  # 7 p.m. EDT Oct 26

    def test_after_daylight_saving_ends(self):
        self.assertEqual(self.at("2026-11-03T02:05:00+00:00"), "2026-11-02")  # 9:05 p.m. EST (UTC-5)
        self.assertEqual(self.at("2026-11-03T01:30:00+00:00"), "2026-11-01")  # 8:30 p.m. EST: not yet


class MissedDayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def put(self, day, status):
        (self.dir / f"{day}.json").write_text(json.dumps({"date": day, "status": status}))

    def test_finds_missing_and_pending_days_oldest_first(self):
        self.put("2026-11-01", "published")
        self.put("2026-11-02", "pending")
        self.put("2026-11-04", "backfilled")
        missing = daily.missing_dates("2026-11-06", "2026-11-01", "2026-12-18", self.dir)
        self.assertEqual(missing, ["2026-11-02", "2026-11-03", "2026-11-05"])

    def test_no_backfill_before_launch(self):
        self.assertEqual(daily.missing_dates("2026-11-06", None, "2026-12-18", self.dir), [])

    def test_stops_at_last_day(self):
        missing = daily.missing_dates("2026-12-25", "2026-12-16", "2026-12-18", self.dir)
        self.assertEqual(missing, ["2026-12-16", "2026-12-17", "2026-12-18"])

    def test_published_check(self):
        self.put("2026-11-01", "published")
        self.put("2026-11-02", "failed")
        self.assertTrue(daily.is_published("2026-11-01", self.dir))
        self.assertFalse(daily.is_published("2026-11-02", self.dir))
        self.assertFalse(daily.is_published("2026-11-03", self.dir))


class EntryTests(unittest.TestCase):
    BRIEF = {"stories": [
        {"role": "focal", "name": "Main", "facts": ["f"],
         "sources": [{"publisher": "A", "title": "t", "url": "https://a.test/1", "published_at": "2026-11-02T10:00:00Z", "checked": "x"}]},
        {"role": "supporting", "name": "Side", "facts": ["g"], "sources": [{"url": "https://b.test/1", "published_at": "2026-11-02T10:00:00Z"}]}]}
    DRAFT = {"title": "T", "caption": "C", "alt": "A", "stories_shown": ["Main"]}

    def test_entry_only_includes_stories_drawn_and_marks_backfill(self):
        e = daily.build_entry("2026-11-02", self.DRAFT, self.BRIEF, "backfill", False, {})
        self.assertEqual([s["name"] for s in e["stories"]], ["Main"])
        self.assertEqual(e["status"], "backfilled")
        self.assertTrue(e["backfill"]["is_backfill"])
        self.assertNotIn("checked", e["stories"][0]["sources"][0])  # internal notes stay in the brief

    def test_live_entry_is_published_not_backfill(self):
        e = daily.build_entry("2026-11-02", self.DRAFT, self.BRIEF, "live", True, {})
        self.assertEqual(e["status"], "published")
        self.assertTrue(e["prelaunch"])
        self.assertFalse(e["backfill"]["is_backfill"])

    def test_draft_cannot_invent_a_story(self):
        with self.assertRaises(ValueError):
            daily.build_entry("2026-11-02", dict(self.DRAFT, stories_shown=["Not in brief"]), self.BRIEF, "live", True, {})


class ArtCheckTests(unittest.TestCase):
    GOOD = ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900">'
            '<title>t</title><desc>d</desc><defs><linearGradient id="g"/></defs>'
            '<rect width="10" height="10" fill="url(#g)"/></svg>')

    def write(self, text):
        f = tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False)
        f.write(text)
        f.close()
        return f.name

    def test_good_svg_passes(self):
        self.assertEqual(check_art.check(self.write(self.GOOD)), [])

    def test_script_and_external_refs_blocked(self):
        bad = self.GOOD.replace("<title>", '<script>alert(1)</script><image href="https://x.test/a.png"/>'
                                          '<rect onclick="x()" fill="url(https://x.test/p)"/><title>')
        errors = check_art.check(self.write(bad))
        self.assertTrue(any("<script>" in e for e in errors))
        self.assertTrue(any("<image>" in e for e in errors))
        self.assertTrue(any("onclick" in e for e in errors))
        self.assertTrue(any("url()" in e for e in errors))

    def test_wrong_size_and_missing_title_blocked(self):
        errors = check_art.check(self.write(self.GOOD.replace('viewBox="0 0 1200 900"', 'viewBox="0 0 800 600"')
                                            .replace("<title>t</title>", "")))
        self.assertTrue(any("viewBox" in e for e in errors))
        self.assertTrue(any("<title>" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
