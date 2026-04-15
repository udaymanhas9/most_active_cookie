"""Cookie counting and most active determination"""

from collections import Counter


class CookieCounter:
    """Counts cookies. Finds most active."""

    def __init__(self, cookies: list[str]) -> None:
        """Args: cookies — list of cookie ID strings (dupes ok)."""

        self._counts = Counter(cookies)

    def most_active(self) -> list[str]:
        """Return cookie(s) with highest count. Empty list if no input."""
        if not self._counts:
            return []

        max_count = max(self._counts.values())

        return [cookie for cookie, count in self._counts.items() if count == max_count]
