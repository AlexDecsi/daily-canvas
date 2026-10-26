"""Group reports about the same event and rank events by independent coverage.

Grouping is by headline word overlap. It's deliberately simple and can be
wrong, so the ranked list is a shortlist for Claude's editorial judgment, not
a decision. Ranking follows the owner's focus (config/sources.json, editorial_focus):
what major US outlets lead with first, Boston/New England news next, international
news only when US outlets give it prominence.

Run from the project folder (after feeds.py):
    python3 src/news/cluster.py 2026-10-25
Writes logs/research/<date>/candidates.json: titles, links, outlets and times
only, no publisher summaries.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from timewindow import parse_timestamp  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

STOPWORDS = set("""a an the and or but of in on at to for from by with as is are was were be been being it its this that
these those after before over under into about than then new says say said will would could can may might not no
how why what who when where which amid more most up down out off you your we our they their he she his her them us
live latest update updates news video watch report reports week day today year years first last two three one""".split())


def tokens(title):
    words = re.findall(r"[a-z0-9']+", title.lower().replace("’", "'"))
    out = set()
    for w in words:
        w = w.strip("'")
        if w.endswith("'s"):
            w = w[:-2]
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        if w and w not in STOPWORDS and len(w) > 2:
            out.add(w)
    return out


def similar(a, b):
    """Two headlines describe the same event if they share enough distinctive words."""
    if not a or not b:
        return False
    shared = a & b
    return len(shared) >= 3 or (len(shared) >= 2 and len(shared) / len(a | b) >= 0.25)


def cluster(items):
    """Greedy grouping: each item joins the first group it is similar to, else starts a new one."""
    groups = []
    for item in sorted(items, key=lambda i: i["published_at"] or ""):
        toks = tokens(item["title"])
        for g in groups:
            if any(similar(toks, t) for t in g["_tokens"]):
                g["items"].append(item)
                g["_tokens"].append(toks)
                break
        else:
            groups.append({"items": [item], "_tokens": [toks]})
    return groups


BOSTON_WORDS = []  # filled from config by load_focus()


def load_focus():
    cfg = json.loads((ROOT / "config" / "sources.json").read_text())
    BOSTON_WORDS[:] = cfg.get("editorial_focus", {}).get("boston_keywords", [])


def signals(group):
    """The facts the score is built from, kept so the ranking can be explained."""
    items = [i for i in group["items"] if i["kind"] != "aggregator" and not i["wire"]]
    us = {i["group"] for i in items if i.get("region", "us") in ("us", "boston")}
    boston = {i["group"] for i in items if i.get("region") == "boston"}
    intl = {i["group"] for i in items if i.get("region") == "intl"} - us
    front = {i["group"] for i in items if i.get("front")}
    # an outlet's own name (e.g. "The Boston Globe") doesn't make a story local
    text = " ".join((i["title"] + " " + i.get("summary", "")).lower().replace(i.get("publisher", "").lower(), "")
                    for i in group["items"])
    local = sorted({w.strip() for w in BOSTON_WORDS
                    if re.search(r"(?<![a-z])" + re.escape(w.strip()) + r"(?![a-z])", text)})
    if not local and len(boston) >= 2 and len(boston) * 2 > len(us):
        local = ["covered mainly by Boston outlets"]  # e.g. a story about a Massachusetts town not in the keyword list
    return {"us_outlets": len(us), "intl_outlets": len(intl), "front_pages": len(front), "boston_local": local}


def score(group):
    """US coverage and front-page prominence dominate; Boston news gets a boost; international adds little."""
    s = signals(group)
    return (10 * s["us_outlets"] + 3 * s["intl_outlets"] + 6 * s["front_pages"]
            + (15 if s["boston_local"] else 0) + min(len(group["items"]), 10))


def rank(items, keep=25):
    if not BOSTON_WORDS:
        load_focus()
    ranked = []
    for g in sorted(cluster(items), key=score, reverse=True)[:keep]:
        its = g["items"]
        times = [parse_timestamp(i["published_at"]) for i in its]
        ranked.append({
            "headline": its[0]["title"],
            "score": score(g),
            "signals": signals(g),
            "independent_outlets": sorted({i["publisher"] for i in its if i["kind"] != "aggregator" and not i["wire"]}),
            "first_seen": min(times).isoformat().replace("+00:00", "Z"),
            "reports": [{"publisher": i["publisher"], "group": i["group"], "kind": i["kind"], "wire": i["wire"],
                         "title": i["title"], "url": i["url"], "published_at": i["published_at"]} for i in its],
        })
    return ranked


def main():
    news_date = sys.argv[1]
    cache = json.loads((ROOT / "cache" / "news" / news_date / "items.json").read_text())
    ranked = rank(cache["items"])
    out = ROOT / "logs" / "research" / news_date
    out.mkdir(parents=True, exist_ok=True)
    (out / "candidates.json").write_text(json.dumps({"date": news_date, "fetched_at": cache["fetched_at"],
                                                     "items_considered": len(cache["items"]),
                                                     "candidates": ranked}, indent=2) + "\n")
    print(f"{len(cache['items'])} items -> {len(ranked)} ranked candidates")
    for c in ranked[:15]:
        sig = c["signals"]
        local = " [BOSTON]" if sig["boston_local"] else ""
        print(f"  {c['score']:3}  US {sig['us_outlets']:2}  intl {sig['intl_outlets']}  front {sig['front_pages']:2}{local}  {c['headline'][:80]}")


if __name__ == "__main__":
    main()
