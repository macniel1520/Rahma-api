from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

UTC = ZoneInfo("UTC")


def now_utc() -> dt.datetime:
    return dt.datetime.now(tz=UTC)
