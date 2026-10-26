"""Confirm when an article was published, straight from the article page.

Used to double-check source timestamps (especially for past dates, where
sources come from Wikipedia rather than our feeds). Respects robots.txt and a
per-run fetch cap. Doesn't bypass paywalls: it only reads the page's public
metadata (meta tags, JSON-LD, <time>).

    python3 src/news/article_meta.py https://example.com/some-article
"""

import json
import re
import sys
import urllib.error
import urllib.request
import urllib.robotparser
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from timewindow import iso, parse_timestamp  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT / "config" / "sources.json").read_text())
UA = CONFIG["user_agent"]
_fetches = 0
_robots = {}

META_PATTERNS = [
    r'<meta[^>]+(?:property|name|itemprop)=["\'](?:article:published_time|og:published_time|datePublished|'
    r'pubdate|publish-date|parsely-pub-date|sailthru\.date|dc\.date)["\'][^>]+content=["\']([^"\']+)["\']',
    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name|itemprop)=["\'](?:article:published_time|'
    r'og:published_time|datePublished)["\']',
    r'"datePublished"\s*:\s*"([^"]+)"',
    r'<time[^>]+datetime=["\']([^"\']+)["\']',
]


def allowed(url):
    parts = urlparse(url)
    base = f"{parts.scheme}://{parts.netloc}"
    if base not in _robots:
        rp = urllib.robotparser.RobotFileParser(base + "/robots.txt")
        try:
            rp.read()
        except Exception:
            rp = None  # robots.txt couldn't be read at all: be conservative and don't fetch
        _robots[base] = rp
    rp = _robots[base]
    return False if rp is None else rp.can_fetch(UA, url)


def published_time(url):
    """Return {'published_at': ISO or None, 'method': ..., 'note': ...} for one article URL."""
    global _fetches
    if _fetches >= CONFIG["limits"]["article_fetches_per_run"]:
        return {"published_at": None, "method": None, "note": "fetch cap reached for this run"}
    if not url.startswith("https://"):
        return {"published_at": None, "method": None, "note": "not https"}
    if not allowed(url):
        return {"published_at": None, "method": None, "note": "robots.txt disallows fetching"}
    _fetches += 1
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as resp:
            page = resp.read(1_500_000).decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as err:
        return {"published_at": None, "method": None, "note": f"fetch failed: {err}"[:150]}
    for pattern in META_PATTERNS:
        m = re.search(pattern, page, re.IGNORECASE)
        if m and parse_timestamp(m.group(1)):
            return {"published_at": iso(parse_timestamp(m.group(1))), "method": "page metadata", "note": ""}
    return {"published_at": None, "method": None, "note": "no publication time found on page"}


if __name__ == "__main__":
    print(json.dumps(published_time(sys.argv[1]), indent=2))
