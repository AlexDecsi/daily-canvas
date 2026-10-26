"""Read the news feeds listed in config/sources.json for one Boston news date.

Keeps only items published inside that day's window (and never after "now"),
so a past date can't pick up later news. Raw items (with publisher summaries)
go to cache/news/<date>/items.json, which git ignores: we keep publisher text
out of the public repository.

Run from the project folder:
    python3 src/news/feeds.py            # today in Boston
    python3 src/news/feeds.py 2026-10-25
"""

import gzip
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from timewindow import day_window, iso, parse_timestamp, today_in_boston  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "sources.json"
CACHE = ROOT / "cache" / "news"

ATOM = "{http://www.w3.org/2005/Atom}"
RSS1 = "{http://purl.org/rss/1.0/}"
DC = "{http://purl.org/dc/elements/1.1/}"


def load_config(path=CONFIG):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fetch(url, config):
    """Download one feed, politely: one retry with a pause, a size limit, our user agent."""
    limits = config["limits"]
    last_error = None
    for attempt in range(limits["feed_retries"] + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": config["user_agent"]})
            with urllib.request.urlopen(req, timeout=limits["feed_timeout_seconds"]) as resp:
                data = resp.read(limits["feed_max_bytes"])
                if data[:2] == b"\x1f\x8b":  # some servers gzip even when not asked
                    data = gzip.decompress(data)
                return data
        except (urllib.error.URLError, TimeoutError) as err:
            last_error = err
            time.sleep(3 * (attempt + 1))
    raise last_error


def clean(text, limit=None):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s*The post .{0,300}? appeared first on .{1,60}$", "", text)  # WordPress feed boilerplate
    return text[:limit] if limit else text


def _text(node, *tags):
    for tag in tags:
        found = node.find(tag)
        if found is not None:
            if found.text and found.text.strip():
                return found.text
            if found.get("href"):
                return found.get("href")
    return ""


def parse_feed(data, source, wire_markers=()):
    """Turn RSS 2.0, RSS 1.0 or Atom bytes into a list of plain dict items."""
    if data.lstrip()[:15].lower().startswith((b"<!doctype html", b"<html")):
        raise ValueError("server sent a web page, not a feed (possibly bot protection; not bypassed)")
    root = ET.fromstring(data)
    nodes = root.findall(".//item") or root.findall(f".//{RSS1}item") or root.findall(f".//{ATOM}entry")
    items = []
    for node in nodes:
        title = clean(_text(node, "title", f"{RSS1}title", f"{ATOM}title"))
        url = _text(node, "link", f"{RSS1}link", f"{ATOM}link").strip()
        raw_date = _text(node, "pubDate", f"{DC}date", f"{ATOM}published", f"{ATOM}updated")
        summary = clean(_text(node, "description", f"{RSS1}description", f"{ATOM}summary"), 400)
        published = parse_timestamp(raw_date)
        if not title or not url:
            continue
        items.append({
            "source_id": source["id"], "publisher": source["publisher"], "group": source["group"],
            "kind": source["kind"], "region": source.get("region", "us"), "front": source.get("front", False),
            "title": title, "url": url, "summary": summary,
            "published_at": iso(published) if published else None,
            "wire": any(marker in summary or marker in title for marker in wire_markers),
        })
    return items


def in_window(items, news_date, now=None):
    """Keep items published inside the Boston day and not after now. Undated items are dropped."""
    start, cutoff = day_window(news_date)
    now = now or datetime.now(timezone.utc)
    limit = min(cutoff, now)
    kept = []
    for item in items:
        published = parse_timestamp(item["published_at"])
        if published and start <= published <= limit:
            kept.append(item)
    return kept


def collect(news_date, config=None, now=None):
    """Fetch every source and return (items_in_window, report)."""
    config = config or load_config()
    all_items, report = [], []
    for source in config["sources"]:
        try:
            items = parse_feed(fetch(source["url"], config), source, config["wire_services"])
            report.append({"source": source["id"], "ok": True, "items": len(items)})
            all_items += items
        except Exception as err:  # one broken feed must not stop the run
            report.append({"source": source["id"], "ok": False, "error": f"{type(err).__name__}: {err}"[:200]})
    kept = in_window(all_items, news_date, now)
    by_url = {}
    for item in kept:  # the same URL can appear in two feeds of one publisher
        if item["url"] in by_url:
            by_url[item["url"]]["front"] = by_url[item["url"]]["front"] or item["front"]
        else:
            by_url[item["url"]] = item
    return list(by_url.values()), report


def main():
    news_date = sys.argv[1] if len(sys.argv) > 1 else today_in_boston()
    items, report = collect(news_date)
    out = CACHE / news_date
    out.mkdir(parents=True, exist_ok=True)
    (out / "items.json").write_text(json.dumps({"date": news_date, "fetched_at": iso(datetime.now(timezone.utc)),
                                                "report": report, "items": items}, indent=2) + "\n")
    ok = sum(r["ok"] for r in report)
    print(f"{news_date}: {ok}/{len(report)} feeds OK, {len(items)} items inside the Boston day window")
    for r in report:
        if not r["ok"]:
            print(f"  feed failed: {r['source']}: {r['error']}")


if __name__ == "__main__":
    main()
