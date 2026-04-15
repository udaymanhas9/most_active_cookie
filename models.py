"""Data model for cookie log entries."""

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class CookieEntry:
    """Immutable cookie log row: cookie ID + date (YYYY-MM-DD)."""

    cookie: str
    date: str

    @classmethod
    def from_raw_line(
        cls, line: str
    ) -> Self:
        """Parse 'cookie,timestamp' CSV line into CookieEntry."""

        cookie, timestamp = line.strip().split(",", 1)
        date = timestamp[:10]
        return cls(cookie=cookie, date=date)
