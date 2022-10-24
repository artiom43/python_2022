import zoneinfo
from datetime import datetime

DEFAULT_TZ_NAME = "Europe/Moscow"


def now() -> datetime:
    """Return now in default timezone"""
    dt = datetime.now(zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    # print(dt, datetime.now())
    return dt


def strftime(dt: datetime, fmt: str) -> str:
    """Return dt converted to string according to format in default timezone"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    else:
        dt = dt.astimezone(zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    # print(dt)
    dt_new = datetime.strftime(dt, fmt)
    return dt_new


def strptime(dt_str: str, fmt: str) -> datetime:
    """Return dt parsed from string according to format in default timezone"""
    dt = datetime.strptime(dt_str, fmt)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    else:
        dt = dt.astimezone(zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    return dt


def diff(first_dt: datetime, second_dt: datetime) -> int:
    """Return seconds between two datetimes rounded down to closest int"""
    if second_dt.tzinfo is None:
        second_dt = second_dt.replace(tzinfo=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    else:
        second_dt = second_dt.astimezone(zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    if first_dt.tzinfo is None:
        first_dt = first_dt.replace(tzinfo=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    else:
        first_dt = first_dt.astimezone(zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    dt = second_dt - first_dt
    return int(dt.total_seconds())


def timestamp(dt: datetime) -> int:
    """Return timestamp for given datetime rounded down to closest int"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    else:
        dt = dt.astimezone(zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    tmstp = dt.timestamp()
    return int(tmstp)


def from_timestamp(ts: float) -> datetime:
    """Return datetime from given timestamp"""
    return datetime.fromtimestamp(ts, tz=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
