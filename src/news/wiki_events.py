"""Find what was in the news on a PAST date, using Wikipedia's Current Events page.

Feeds only hold the last day or two, so missed days (backfill) need another
source. Wikipedia keeps a dated page per day ("Portal:Current events/2026
October 20") listing events with links to news reports. To avoid hindsight, we
read the page AS IT EXISTED at the news date's cutoff (end of that Boston day),
not today's version, which may contain later edits.

This is discovery only: each linked source still needs its own publication
time checked (article_meta.py) and must pass brief.py.

    python3 src/news/wiki_events.py 2026-10-20
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from timewindow import day_window, iso  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT / "config" / "sources.json").read_text())
API = CONFIG["historical"]["wikipedia_api"]

LINK = re.compile(r"\[(https?://[^\s\]]+)\s+([^\]]+)\]")


def page_title(news_date):
    d = date.fromisoformat(news_date)
    return f"Portal:Current events/{d.year} {d.strftime('%B')} {d.day}"


def revision_at_cutoff(news_date):
    """Fetch the page's wikitext as of the end of the Boston news day."""
    _, cutoff = day_window(news_date)
    params = {"action": "query", "prop": "revisions", "titles": page_title(news_date), "rvlimit": 1,
              "rvstart": iso(cutoff), "rvdir": "older", "rvprop": "content|timestamp|ids", "rvslots": "main",
              "format": "json", "formatversion": 2}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": CONFIG["user_agent"]})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    pages = data.get("query", {}).get("pages", [])
    if not pages or "revisions" not in pages[0]:
        return None
    rev = pages[0]["revisions"][0]
    return {"revid": rev["revid"], "timestamp": rev["timestamp"], "text": rev["slots"]["main"]["content"]}


def plain(wikitext):
    text = LINK.sub("", wikitext)
    text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\{\{[^}]*\}\}", "", text)
    text = re.sub(r"<ref[^>]*>.*?</ref>|<[^>]+>", "", text)
    text = text.replace("'''", "").replace("''", "")
    return re.sub(r"\s+", " ", text).strip(" *:;()")


def parse_events(wikitext):
    """Return a list of {category, topic, text, sources:[{url, label}]} from the day page."""
    events, category, topics = [], None, {}
    for line in wikitext.splitlines():
        stripped = line.strip()
        header = re.match(r"^(?:;|''')\s*([^']+?)\s*(?:''')?$", stripped)
        if header and not stripped.startswith("*"):
            category = header.group(1).strip()
            continue
        bullet = re.match(r"^(\*+)\s*(.*)$", stripped)
        if not bullet:
            continue
        depth, body = len(bullet.group(1)), bullet.group(2)
        links = [{"url": u, "label": plain(l)} for u, l in LINK.findall(body)]
        text = plain(body)
        if not links:  # a topic heading such as "* [[Russian invasion of Ukraine]]"
            topics[depth] = text
            continue
        topic = " / ".join(topics[d] for d in sorted(topics) if d < depth)
        events.append({"category": category, "topic": topic, "text": text, "sources": links})
    return events


def main():
    news_date = sys.argv[1]
    rev = revision_at_cutoff(news_date)
    out = ROOT / "logs" / "research" / news_date
    out.mkdir(parents=True, exist_ok=True)
    if not rev:
        print(f"No version of '{page_title(news_date)}' existed by the cutoff; date stays unresolved.")
        return 1
    events = parse_events(rev["text"])
    (out / "wiki_events.json").write_text(json.dumps({
        "date": news_date, "page": page_title(news_date), "revision_id": rev["revid"],
        "revision_time": rev["timestamp"], "events": [{**e, "text": e["text"][:300]} for e in events]}, indent=2) + "\n")
    print(f"{page_title(news_date)}: revision {rev['revid']} from {rev['timestamp']} (cutoff-safe), {len(events)} events")
    for e in events[:12]:
        print(f"  [{e['category']}] {e['text'][:100]}  ({', '.join(s['label'] for s in e['sources'])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
