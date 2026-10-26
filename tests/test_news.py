"""Checks for news research: Boston dates, feed parsing, no future leaks, grouping and brief rules.
No network access needed. Run from the project folder:
    python3 -m unittest discover tests
"""

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "news"))
import brief  # noqa: E402
import cluster  # noqa: E402
import feeds  # noqa: E402
import wiki_events  # noqa: E402
from timewindow import day_window, parse_timestamp  # noqa: E402

SOURCE = {"id": "t", "publisher": "Test News", "group": "test", "kind": "news"}


class TimeTests(unittest.TestCase):
    def test_summer_day_is_utc_minus_4(self):
        start, cutoff = day_window("2026-10-20")
        self.assertEqual(start.isoformat(), "2026-10-20T04:00:00+00:00")
        self.assertEqual(cutoff.isoformat(), "2026-10-21T03:59:59+00:00")

    def test_dst_end_day_is_25_hours(self):
        start, cutoff = day_window("2026-11-01")
        self.assertEqual((cutoff - start).total_seconds() + 1, 25 * 3600)

    def test_timestamp_formats(self):
        self.assertEqual(parse_timestamp("Sun, 25 Oct 2026 16:35:35 -0400").isoformat(), "2026-10-25T20:35:35+00:00")
        self.assertEqual(parse_timestamp("2026-10-25T22:15:00Z").isoformat(), "2026-10-25T22:15:00+00:00")
        self.assertIsNotNone(parse_timestamp("Sun, 25 Oct 2026 19:31:50 EST"))
        self.assertIsNone(parse_timestamp("not a date"))


class FeedTests(unittest.TestCase):
    RSS2 = b"""<rss><channel><item><title>Storm hits coast</title><link>https://x.test/a</link>
        <pubDate>Tue, 20 Oct 2026 15:00:00 GMT</pubDate><description>&lt;p&gt;Hello (AP)&lt;/p&gt;</description></item>
        <item><title>No link</title></item></channel></rss>"""
    ATOM = b"""<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Atom item</title>
        <link href="https://x.test/b"/><updated>2026-10-20T12:00:00Z</updated></entry></feed>"""

    def test_parse_rss2_and_wire_flag(self):
        items = feeds.parse_feed(self.RSS2, SOURCE, ["(AP)"])
        self.assertEqual(len(items), 1)  # the item without a link is skipped
        self.assertEqual(items[0]["summary"], "Hello (AP)")
        self.assertTrue(items[0]["wire"])

    def test_parse_atom(self):
        items = feeds.parse_feed(self.ATOM, SOURCE)
        self.assertEqual(items[0]["url"], "https://x.test/b")

    def test_html_page_rejected(self):
        with self.assertRaises(ValueError):
            feeds.parse_feed(b"<!DOCTYPE html><html></html>", SOURCE)

    def test_window_blocks_future_and_other_days(self):
        def item(ts):
            return {"published_at": ts}
        items = [item("2026-10-20T15:00:00Z"),   # inside the Boston day
                 item("2026-10-21T05:00:00Z"),   # after the cutoff: future leak
                 item("2026-10-20T03:00:00Z"),   # the evening before, Boston time
                 item(None)]                      # undated
        kept = feeds.in_window(items, "2026-10-20", now=datetime(2026, 10, 30, tzinfo=timezone.utc))
        self.assertEqual([i["published_at"] for i in kept], ["2026-10-20T15:00:00Z"])

    def test_window_never_passes_now(self):
        items = [{"published_at": "2026-10-20T20:00:00Z"}]
        now = datetime(2026, 10, 20, 18, 0, tzinfo=timezone.utc)
        self.assertEqual(feeds.in_window(items, "2026-10-20", now=now), [])


def report(title, group, kind="news", wire=False, ts="2026-10-20T15:00:00Z", region="us", front=False):
    return {"title": title, "group": group, "publisher": group.upper(), "kind": kind, "wire": wire,
            "region": region, "front": front, "summary": "",
            "url": f"https://{group}.test/{abs(hash(title))}", "published_at": ts}


class ClusterTests(unittest.TestCase):
    def test_same_event_grouped(self):
        a = cluster.tokens("Venezuela opposition leader Machado returns from exile")
        b = cluster.tokens("Machado returns to Venezuela after months in exile")
        self.assertTrue(cluster.similar(a, b))

    def test_different_events_not_grouped(self):
        a = cluster.tokens("Brazil votes in tight presidential runoff")
        b = cluster.tokens("Tornado damages homes in Oklahoma town")
        self.assertFalse(cluster.similar(a, b))

    def test_ranking_counts_independent_outlets_only(self):
        items = [report("Volcano erupts in Iceland near town", "bbc"),
                 report("Iceland volcano erupts near fishing town", "npr"),
                 report("Volcano erupts in Iceland, town evacuated", "agg", kind="aggregator"),
                 report("City council approves budget plan", "cbs"),
                 report("City council approves new budget plan", "abc", wire=True)]
        ranked = cluster.rank(items)
        self.assertEqual(ranked[0]["independent_outlets"], ["BBC", "NPR"])
        self.assertEqual(ranked[1]["independent_outlets"], ["CBS"])


class FocusTests(unittest.TestCase):
    """Owner focus: US front pages first, Boston news boosted, international news only when US outlets lead with it."""

    def test_us_front_page_story_beats_widely_covered_foreign_story(self):
        foreign = [report(f"Serbia election leader concedes defeat {k}", g, region="intl", front=True)
                   for k, g in enumerate(["bbc", "guardian", "dw", "sky", "aljazeera"])]
        us = [report(f"Senate passes budget deal vote tonight {k}", g, front=True) for k, g in enumerate(["nyt", "nbc", "cbs"])]
        ranked = cluster.rank(foreign + us)
        self.assertIn("Senate", ranked[0]["headline"])

    def test_boston_story_gets_local_boost(self):
        local = [report("MBTA Red Line shutdown planned for Boston riders", "globe", region="boston", front=True),
                 report("MBTA Red Line shutdown Boston riders weekend", "wbur", region="boston", front=True)]
        national = [report("Factory output report released Washington data", "politico"),
                    report("Factory output report released data Washington", "axios")]
        ranked = cluster.rank(local + national)
        self.assertEqual(ranked[0]["signals"]["boston_local"], ["boston", "mbta"])
        self.assertGreater(ranked[0]["score"], ranked[1]["score"])

    def test_outlet_name_and_boilerplate_not_local(self):
        self.assertEqual(feeds.clean("Senate race heats up. The post Senate race heats up appeared first on Boston.com."),
                         "Senate race heats up.")
        cluster.load_focus()
        item = report("Senate race heats up in Michigan", "globe", region="boston")
        item.update(publisher="The Boston Globe", summary="From The Boston Globe")
        self.assertEqual(cluster.signals({"items": [item]})["boston_local"], [])

    def test_keyword_match_is_whole_word(self):
        cluster.load_focus()
        sig = cluster.signals({"items": [report("Senator remained silent on mass shooting", "nyt")]})
        self.assertEqual(sig["boston_local"], [])


def good_brief(**changes):
    b = {"date": "2026-10-20", "rationale": "Biggest story by coverage.",
         "stories": [{"role": "focal", "name": "Launch", "facts": ["A probe launched."],
                      "people": [{"name": "Official", "public_figure": True, "verified_action": "spoke at launch"}],
                      "sources": [{"publisher": "A", "group": "a", "url": "https://a.test/1", "published_at": "2026-10-20T10:00:00Z"},
                                  {"publisher": "B", "group": "b", "url": "https://b.test/1", "published_at": "2026-10-20T11:00:00Z"}]}]}
    b.update(changes)
    return b


class BriefTests(unittest.TestCase):
    def test_good_brief_passes(self):
        errors, _ = brief.check(good_brief())
        self.assertEqual(errors, [])

    def test_future_leak_blocks(self):
        b = good_brief()
        b["stories"][0]["sources"][1]["published_at"] = "2026-10-21T09:00:00Z"
        errors, _ = brief.check(b)
        self.assertTrue(any("FUTURE LEAK" in e for e in errors))

    def test_focal_needs_two_independent_outlets(self):
        b = good_brief()
        b["stories"][0]["sources"][1]["group"] = "a"  # same outlet group twice
        errors, _ = brief.check(b)
        self.assertTrue(any("2 independent outlets" in e for e in errors))

    def test_two_wire_copies_count_once(self):
        b = good_brief()
        for s in b["stories"][0]["sources"]:
            s["wire"] = True
        errors, _ = brief.check(b)
        self.assertTrue(any("2 independent outlets" in e for e in errors))

    def test_different_wire_services_are_independent(self):
        b = good_brief()
        b["stories"][0]["sources"][0]["wire"] = "AP"
        b["stories"][0]["sources"][1]["wire"] = "AFP"
        errors, _ = brief.check(b)
        self.assertEqual(errors, [])

    def test_public_figure_needs_verified_action(self):
        b = good_brief()
        b["stories"][0]["people"][0]["verified_action"] = ""
        errors, _ = brief.check(b)
        self.assertTrue(any("verified action" in e for e in errors))

    def test_http_link_blocks(self):
        b = good_brief()
        b["stories"][0]["sources"][0]["url"] = "http://a.test/1"
        errors, _ = brief.check(b)
        self.assertTrue(any("https" in e for e in errors))

    def test_single_source_supporting_needs_notes(self):
        b = good_brief()
        b["stories"].append({"role": "supporting", "name": "Side", "facts": ["x"],
                             "sources": [{"group": "c", "url": "https://c.test", "published_at": "2026-10-20T12:00:00Z"}]})
        errors, _ = brief.check(b)
        self.assertTrue(any("single-source" in e for e in errors))
        b["stories"][1]["notes"] = "Only one outlet; official statement quoted directly."
        errors, warnings = brief.check(b)
        self.assertEqual(errors, [])
        self.assertTrue(warnings)

    def test_story_from_previous_boston_day_blocks(self):
        b = good_brief()
        for src in b["stories"][0]["sources"]:
            src["published_at"] = "2026-10-19T21:00:00Z"  # 5 p.m. Boston on Oct 19
        errors, _ = brief.check(b)
        self.assertTrue(any("no source published on 2026-10-20" in e for e in errors))
        b["stories"][0]["date_note"] = "Ongoing story; still developing on Oct 20."
        errors, _ = brief.check(b)
        self.assertEqual(errors, [])

    def test_needs_exactly_one_focal(self):
        b = good_brief()
        b["stories"][0]["role"] = "supporting"
        errors, _ = brief.check(b)
        self.assertTrue(any("exactly 1 focal" in e for e in errors))


class WikiTests(unittest.TestCase):
    PAGE = """;Armed conflicts and attacks
*[[War in Sudan]]
**A drone strike hits a market. ([https://a.test/1 Sudans Post])
;Science and technology
*[[JAXA]] launches a probe toward [[Phobos (moon)|Phobos]]. ([https://r.test/2 Reuters]) ([https://b.test/3 BBC])"""

    def test_parse_events(self):
        events = wiki_events.parse_events(self.PAGE)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["topic"], "War in Sudan")
        self.assertEqual(events[1]["category"], "Science and technology")
        self.assertEqual(events[1]["text"], "JAXA launches a probe toward Phobos.")
        self.assertEqual([s["label"] for s in events[1]["sources"]], ["Reuters", "BBC"])

    def test_title(self):
        self.assertEqual(wiki_events.page_title("2026-10-05"), "Portal:Current events/2026 October 5")


if __name__ == "__main__":
    unittest.main()
