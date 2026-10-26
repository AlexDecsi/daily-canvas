"""Checks for the site builder. Run from the project folder:
    python3 -m unittest discover tests
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "pipeline"))
import build_site  # noqa: E402


def good_entry(date="2026-11-01", **overrides):
    entry = {
        "date": date,
        "status": "published",
        "published_at": f"{date}T21:00:00-04:00",
        "title": "Test",
        "caption": "Test caption.",
        "stories": [{"name": "S", "sources": [{"url": "https://example.com/a"}]}],
        "artwork": {"path": "artwork/2026-10-24-sample.svg", "alt": "Alt text"},
    }
    entry.update(overrides)
    return entry


class ValidateTests(unittest.TestCase):
    def test_good_entry_passes(self):
        self.assertEqual(build_site.validate(good_entry(), "2026-11-01.json"), [])

    def test_filename_must_match_date(self):
        self.assertTrue(build_site.validate(good_entry(), "2026-11-02.json"))

    def test_missing_alt_text_blocks(self):
        e = good_entry(artwork={"path": "artwork/2026-10-24-sample.svg"})
        self.assertIn("missing artwork alt text", build_site.validate(e, "2026-11-01.json"))

    def test_missing_artwork_file_blocks(self):
        e = good_entry(artwork={"path": "artwork/nope.svg", "alt": "x"})
        self.assertTrue(any("not found" in p for p in build_site.validate(e, "2026-11-01.json")))

    def test_unsafe_artwork_path_blocks(self):
        e = good_entry(artwork={"path": "../CLAUDE.md", "alt": "x"})
        self.assertTrue(build_site.validate(e, "2026-11-01.json"))

    def test_non_https_source_blocks(self):
        e = good_entry(stories=[{"name": "S", "sources": [{"url": "javascript:alert(1)"}]}])
        self.assertTrue(build_site.validate(e, "2026-11-01.json"))

    def test_backfill_needs_reason(self):
        e = good_entry(status="backfilled")
        self.assertIn("backfilled entry needs backfill.reason", build_site.validate(e, "2026-11-01.json"))

    def test_no_entries_after_project_end(self):
        e = good_entry(date="2026-12-19")
        self.assertTrue(build_site.validate(e, "2026-12-19.json"))


class LoadTests(unittest.TestCase):
    def test_pending_hidden_and_newest_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            for date in ("2026-11-01", "2026-11-03"):
                (d / f"{date}.json").write_text(json.dumps(good_entry(date)))
            (d / "2026-11-02.json").write_text(json.dumps({"date": "2026-11-02", "status": "pending"}))
            public, errors = build_site.load_entries(d)
        self.assertEqual(errors, {})
        self.assertEqual([e["date"] for e in public], ["2026-11-03", "2026-11-01"])

    def test_bad_json_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "2026-11-01.json").write_text("{not json")
            _, errors = build_site.load_entries(Path(tmp))
        self.assertIn("2026-11-01.json", errors)

    def test_real_content_builds(self):
        _, errors = build_site.load_entries()
        self.assertEqual(errors, {})


if __name__ == "__main__":
    unittest.main()
