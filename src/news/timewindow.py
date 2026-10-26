"""Dates and times for the news day.

A "news date" is a calendar day in Boston (America/New_York), including
daylight-saving changes. Everything the entry for that date may use must have
been published before the end of that Boston day: the "cutoff".
"""

from datetime import date, datetime, time, timedelta, timezone
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo

BOSTON = ZoneInfo("America/New_York")


def day_window(news_date):
    """Return (start, cutoff) in UTC for a Boston calendar day. news_date: 'YYYY-MM-DD' or date."""
    if isinstance(news_date, str):
        news_date = date.fromisoformat(news_date)
    start = datetime.combine(news_date, time(0, 0), tzinfo=BOSTON)
    end = datetime.combine(news_date + timedelta(days=1), time(0, 0), tzinfo=BOSTON)
    return start.astimezone(timezone.utc), (end - timedelta(seconds=1)).astimezone(timezone.utc)


def today_in_boston(now=None):
    now = now or datetime.now(timezone.utc)
    return now.astimezone(BOSTON).date().isoformat()


def parse_timestamp(text):
    """Parse RSS (RFC 822) or ISO 8601 timestamps into an aware UTC datetime; None if unreadable."""
    if not text:
        return None
    text = text.strip()
    try:
        dt = parsedate_to_datetime(text)
    except (TypeError, ValueError, IndexError):
        try:
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt.tzinfo is None:  # a timestamp with no zone is ambiguous; assume UTC and let callers flag it
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def iso(dt):
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
