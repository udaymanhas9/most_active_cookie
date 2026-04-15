"""Cookie log reader with date-based filtering"""

import logging
import os
from collections.abc import Iterator
from models import CookieEntry

logger = logging.getLogger(__name__)


class CookieLog:
    """CSV cookie log. Expects header row, timestamps descending."""

    def __init__(self, filepath: str) -> None:
        """Raises FileNotFoundError if filepath missing."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No such file: '{filepath}'")
        self.filepath = filepath

    def _iter_entries(self) -> Iterator[CookieEntry]:
        """Yield CookieEntry per data row. Skip malformed lines."""
        with open(self.filepath, "r") as f:
            next(f, None)  # Skip header

            for line in f:
                line = line.strip()

                if not line:
                    continue

                try:
                    yield CookieEntry.from_raw_line(line)
                except ValueError:
                    logger.warning("skipping malformed line: %r", line)

    def get_cookies_for_date(self, target_date: str) -> list[str]:
        """Return cookie IDs for target_date. Exits early using descending sort."""
        cookies = []

        for entry in self._iter_entries():
            if entry.date == target_date:
                cookies.append(entry.cookie)
            elif entry.date < target_date:
                break

        return cookies
