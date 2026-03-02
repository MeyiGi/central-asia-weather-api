"""
time_utils.py

Just some helpers for dealing with datetime strings and conversions.
I kept running into the same parsing logic in multiple places so I pulled it out here.
"""

from datetime import datetime


def parse_iso_datetime(time_str: str) -> datetime | None:
    """
    Try to parse a datetime string in ISO 8601 format.
    Returns None if it fails instead of blowing up — let the caller decide what to do.

    Examples:
        "2025-01-29T00:00"     -> works
        "2025-01-29 00:00:00"  -> works
        "not-a-date"           -> returns None
    """
    if not time_str or not isinstance(time_str, str):
        return None

    cleaned = time_str.strip()

    try:
        return datetime.fromisoformat(cleaned)
    except ValueError:
        return None


def format_datetime_for_display(dt: datetime) -> str:
    """
    Just a consistent way to print datetimes in logs/responses.
    e.g. "2025-01-29 00:00 UTC"
    """
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def find_closest_time(target: datetime, available_times: list[datetime]) -> datetime | None:
    """
    Given a list of available datetimes, return the one closest to `target`.
    Returns None if the list is empty (no point crashing over that).

    I use this when the user's requested time doesn't exactly match a GRIB step.
    """
    if not available_times:
        return None

    # min() with a key is cleaner than sorting the whole list
    closest = min(available_times, key=lambda t: abs((t - target).total_seconds()))
    return closest


def seconds_between(dt1: datetime, dt2: datetime) -> float:
    """
    Returns absolute difference in seconds between two datetimes.
    """
    return abs((dt1 - dt2).total_seconds())