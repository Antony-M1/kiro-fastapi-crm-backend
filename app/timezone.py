"""
Centralized timezone utilities for the application.
All datetime operations should use these helpers to ensure consistent timezone handling.
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional
from functools import lru_cache


@lru_cache(maxsize=1)
def get_timezone() -> ZoneInfo:
    """Get the configured timezone. Cached for performance."""
    from app.config import settings
    return ZoneInfo(settings.TIMEZONE)


def now() -> datetime:
    """Get current datetime in the configured timezone."""
    return datetime.now(get_timezone())


def utc_now() -> datetime:
    """Get current datetime in UTC (timezone-aware)."""
    return datetime.now(ZoneInfo("UTC"))


def to_app_timezone(dt: datetime) -> datetime:
    """Convert a datetime to the application's configured timezone."""
    if dt.tzinfo is None:
        # Assume naive datetime is in UTC
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(get_timezone())


def to_utc(dt: datetime) -> datetime:
    """Convert a datetime to UTC."""
    if dt.tzinfo is None:
        # Assume naive datetime is in app timezone
        dt = dt.replace(tzinfo=get_timezone())
    return dt.astimezone(ZoneInfo("UTC"))


def from_timestamp(timestamp: float) -> datetime:
    """Create a timezone-aware datetime from a Unix timestamp."""
    return datetime.fromtimestamp(timestamp, tz=get_timezone())


def add_hours(hours: int, base: Optional[datetime] = None) -> datetime:
    """Add hours to a datetime (defaults to current time)."""
    base = base or now()
    return base + timedelta(hours=hours)


def add_days(days: int, base: Optional[datetime] = None) -> datetime:
    """Add days to a datetime (defaults to current time)."""
    base = base or now()
    return base + timedelta(days=days)


def clear_timezone_cache():
    """Clear the timezone cache. Useful for testing or config changes."""
    get_timezone.cache_clear()
