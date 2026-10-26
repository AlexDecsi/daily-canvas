"""Check a story brief before any art is made.

A brief (logs/research/<date>/brief.json) is what Claude writes after choosing
the day's stories: one focal story, up to two supporting stories, the verified
facts, and the sources behind them. This checker blocks publication when:

- a source was published after the news date's cutoff (future information leak)
- the focal story lacks two independent outlets (wire copies and aggregators don't count)
- a source link isn't https, or a timestamp is missing or unreadable
- a public figure is drawn without a verified action
- no source for a story is from the news date itself (it may belong to another day)
- the brief has the wrong number of stories, or empty or overlong facts

Run:  python3 src/news/brief.py 2026-10-25
Exit code 0 = OK to make art; 1 = blocked (problems are printed).
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from timewindow import day_window, parse_timestamp  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
MAX_FACT_CHARS = 300


def independent_groups(sources):
    """Distinct outlet groups that count as independent corroboration.

    A story republished from a wire service counts as that wire service, not as the outlet:
    two outlets running the same AP story are one source; an AP report and an AFP report are two.
    Set "wire" to the service name ("AP", "AFP", "Reuters"), or true if the service is unknown.
    """
    groups = set()
    for s in sources:
        if s.get("kind") == "aggregator":
            continue
        wire = s.get("wire")
        if wire:
            groups.add(f"wire:{wire if isinstance(wire, str) else 'unknown'}")
        else:
            groups.add(s.get("group") or s.get("publisher"))
    return groups


def check(brief):
    """Return (errors, warnings). Any error blocks the entry."""
    errors, warnings = [], []
    news_date = brief.get("date", "")
    try:
        start, cutoff = day_window(news_date)
    except ValueError:
        return [f"bad date: {news_date!r}"], []

    stories = brief.get("stories") or []
    focal = [s for s in stories if s.get("role") == "focal"]
    supporting = [s for s in stories if s.get("role") == "supporting"]
    if len(focal) != 1:
        errors.append(f"need exactly 1 focal story, found {len(focal)}")
    if len(supporting) > 2:
        errors.append(f"at most 2 supporting stories, found {len(supporting)}")
    if len(focal) + len(supporting) != len(stories):
        errors.append("every story needs role 'focal' or 'supporting'")
    if not brief.get("rationale"):
        errors.append("missing editorial rationale")

    for story in stories:
        name = story.get("name") or "(unnamed story)"
        facts = story.get("facts") or []
        if not facts:
            errors.append(f"{name}: no facts listed")
        for fact in facts:
            if len(fact) > MAX_FACT_CHARS:
                errors.append(f"{name}: a fact is longer than {MAX_FACT_CHARS} characters")
        for person in story.get("people") or []:
            if person.get("public_figure") and not person.get("verified_action"):
                errors.append(f"{name}: public figure {person.get('name')} has no verified action to depict")

        sources = story.get("sources") or []
        if not sources:
            errors.append(f"{name}: no sources")
        in_day = False
        for src in sources:
            url = src.get("url", "")
            if not url.startswith("https://"):
                errors.append(f"{name}: source link is not https: {url}")
            published = parse_timestamp(src.get("published_at"))
            if not published:
                errors.append(f"{name}: source has no readable publication time: {url}")
                continue
            if published > cutoff:
                errors.append(f"{name}: FUTURE LEAK, source published {src['published_at']} after cutoff "
                              f"{cutoff.isoformat()}: {url}")
            if published >= start:
                in_day = True

        groups = independent_groups(sources)
        if story.get("role") == "focal" and len(groups) < 2:
            errors.append(f"{name}: focal story needs 2 independent outlets, has {len(groups)} ({', '.join(sorted(groups)) or 'none'})")
        if story.get("role") == "supporting" and len(groups) < 2:
            if not story.get("notes"):
                errors.append(f"{name}: single-source supporting story must explain its confidence in 'notes'")
            else:
                warnings.append(f"{name}: single independent source; confidence noted")
        if sources and not in_day:
            if story.get("date_note"):
                warnings.append(f"{name}: no source from {news_date} itself; explained in date_note")
            else:
                errors.append(f"{name}: no source published on {news_date} (Boston time); it may belong to another "
                              f"day. Add 'date_note' only if it is genuinely that day's news (e.g. an ongoing story).")
    return errors, warnings


def main():
    news_date = sys.argv[1]
    brief = json.loads((ROOT / "logs" / "research" / news_date / "brief.json").read_text())
    errors, warnings = check(brief)
    for w in warnings:
        print(f"  ! {w}")
    for e in errors:
        print(f"  ✗ {e}")
    print("BLOCKED" if errors else "OK: brief passes checks")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
