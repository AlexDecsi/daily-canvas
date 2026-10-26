"""Checks for the weekly report: week boundaries, once-per-week writing, and missed-run flags.
Run from the project folder:
    python3 -m unittest discover tests
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "pipeline"))
sys.path.insert(0, str(ROOT / "src" / "news"))
import weekly  # noqa: E402


class WeekTests(unittest.TestCase):
    def test_finished_week_turns_over_on_sunday_evening(self):
        self.assertEqual(weekly.last_finished_week("2026-10-24"), "2026-W42")  # Saturday: previous week
        self.assertEqual(weekly.last_finished_week("2026-10-25"), "2026-W43")  # Sunday entry due: this week
        self.assertEqual(str(weekly.week_monday("2026-W44")), "2026-10-26")


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.entries, self.logs, self.reports = base / "e", base / "l", base / "r"
        for d in (self.entries, self.logs):
            d.mkdir()
        self.changes = base / "changes.md"
        self.changes.write_text('## 2026-11-03: Brighter colours\n\n**Owner feedback:** "make it brighter"\n\n'
                                '## 2026-10-20: Too early\n\n**Owner feedback:** "outside the week"\n')

    def tearDown(self):
        self.tmp.cleanup()

    def put(self, day, **entry):
        (self.entries / f"{day}.json").write_text(json.dumps({"date": day, **entry}))

    def kwargs(self):
        return dict(entries_dir=self.entries, logs_dir=self.logs, changes_path=self.changes, launch="2026-11-02")

    def test_flags_backfills_failures_and_unresolved_days(self):
        self.put("2026-11-02", status="published", title="A", published_at="2026-11-03T01:30:00Z")
        self.put("2026-11-03", status="backfilled", title="B", published_at="2026-11-04T12:00:00Z",
                 backfill={"is_backfill": True, "reason": "Mac asleep at 9 p.m."})
        (self.logs / "2026-11-04.json").write_text(json.dumps({"runs": [{"outcome": "failed", "reason": "no verified story"}]}))
        report = weekly.build("2026-W45", **self.kwargs())
        self.assertIn("2026-11-03: missed on schedule, recovered late", report)
        self.assertIn("Mac asleep at 9 p.m.", report)
        self.assertIn("2026-11-04: failed run**: no verified story", report)
        self.assertIn("2026-11-05: still unresolved", report)
        self.assertIn('Brighter colours: "make it brighter"', report)
        self.assertNotIn("outside the week", report)
        self.assertIn("| 2026-11-02 | published | A | 2026-11-02 |", report)  # made-on shown in Boston time

    def test_written_once_never_regenerated(self):
        self.put("2026-11-02", status="published", title="A", published_at="2026-11-03T01:30:00Z")
        first = weekly.write("2026-W45", reports_dir=self.reports, **self.kwargs())
        self.assertTrue(first.exists())
        first.write_text("edited by the run")
        self.assertIsNone(weekly.write("2026-W45", reports_dir=self.reports, **self.kwargs()))
        self.assertEqual(first.read_text(), "edited by the run")

    def test_week_due_only_with_activity_and_no_report(self):
        self.assertIsNone(weekly.week_due("2026-11-08", self.reports, self.entries, self.logs))  # empty week
        self.put("2026-11-02", status="published", title="A")
        self.assertEqual(weekly.week_due("2026-11-08", self.reports, self.entries, self.logs), "2026-W45")
        self.assertIsNone(weekly.week_due("2026-11-07", self.reports, self.entries, self.logs))  # week not finished


if __name__ == "__main__":
    unittest.main()
